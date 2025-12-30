"""
Prediction API endpoints
Handles champion matchup and game state predictions
"""

from fastapi import APIRouter, HTTPException, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.schemas.prediction import (
    ChampionMatchupRequest,
    GameStateRequest,
    GameStateV2Request,
    PredictionResponse
)
from app.services.ml_engine import ml_engine
from app.core.logging import logger
from app.core.config import settings

router = APIRouter(prefix="/api", tags=["predictions"])
limiter = Limiter(key_func=get_remote_address)


async def verify_api_key(request: Request):
    """
    Verify API key for production environments.
    Development mode allows requests without API key (with warning).
    """
    if settings.ENV == "production":
        api_key = request.headers.get("X-INTERNAL-API-KEY")

        if not api_key or api_key != settings.INTERNAL_API_KEY:
            logger.warning(f"Unauthorized API access attempt from {request.client.host}")
            raise HTTPException(
                status_code=401,
                detail="Invalid or missing API key"
            )
    elif settings.ENV == "development":
        # Development mode - log warning but allow
        if not request.headers.get("X-INTERNAL-API-KEY"):
            logger.warning(f"Development mode: Request from {request.client.host} without API key")

    return True


@router.post("/predict-champion-matchup", response_model=PredictionResponse, dependencies=[])
@limiter.limit("10/minute")
async def predict_champion_matchup(request: Request, body: ChampionMatchupRequest):
    """
    Predict win probability based on champion team compositions

    Returns:
    - Blue/Red team win probabilities
    - Prediction text
    - Confidence level
    - Champion win-rate details
    """
    # Verify API key
    await verify_api_key(request)

    if not ml_engine.champion_predictor:
        raise HTTPException(status_code=503, detail="Champion Predictor not loaded")

    try:
        result = ml_engine.champion_predictor.predict(
            blue_champions=body.blue_champions,
            red_champions=body.red_champions
        )

        return PredictionResponse(
            blue_win_probability=result['blue_win_probability'],
            red_win_probability=result['red_win_probability'],
            prediction=result['prediction'],
            confidence=result['confidence'],
            details={
                'blue_avg_winrate': result['blue_avg_winrate'],
                'red_avg_winrate': result['red_avg_winrate'],
                'model': 'champion_matchup',
                'accuracy': '61.6%'
            }
        )

    except ValueError as e:
        # User input errors (e.g., unknown champion)
        logger.warning(f"Invalid input for champion matchup prediction: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid request: {str(e)}")
    except Exception as e:
        logger.error(f"Error in champion matchup prediction: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Internal server error during prediction. Please try again later."
        )


@router.post("/predict-game-state", response_model=PredictionResponse, dependencies=[])
@limiter.limit("10/minute")
async def predict_game_state(http_request: Request, request: GameStateRequest):
    """
    Predict win probability based on current game state

    Returns:
    - Blue/Red team win probabilities
    - Prediction text
    - Confidence level
    - Game state analysis
    """
    # Verify API key
    await verify_api_key(http_request)

    if not ml_engine.win_predictor:
        raise HTTPException(status_code=503, detail="Win Predictor not loaded")

    try:
        # Calculate diffs
        kill_diff = request.blue_kills - request.red_kills
        gold_diff = request.blue_gold - request.red_gold
        tower_diff = request.blue_towers - request.red_towers
        dragon_diff = request.blue_dragons - request.red_dragons

        # Prepare features
        game_state = {
            'game_duration': request.game_duration,
            'blue_kills': request.blue_kills,
            'blue_deaths': request.blue_deaths,
            'blue_assists': request.blue_assists,
            'blue_gold': request.blue_gold,
            'blue_towers': request.blue_towers,
            'blue_dragons': request.blue_dragons,
            'blue_barons': request.blue_barons,
            'blue_vision_score': request.blue_vision_score,
            'red_kills': request.red_kills,
            'red_deaths': request.red_deaths,
            'red_assists': request.red_assists,
            'red_gold': request.red_gold,
            'red_towers': request.red_towers,
            'red_dragons': request.red_dragons,
            'red_barons': request.red_barons,
            'red_vision_score': request.red_vision_score,
            'kill_diff': kill_diff,
            'gold_diff': gold_diff,
            'tower_diff': tower_diff,
            'dragon_diff': dragon_diff
        }

        # Predict
        blue_prob = ml_engine.win_predictor.predict_single(game_state)
        red_prob = 1 - blue_prob

        # Generate prediction text
        if blue_prob > 0.7:
            prediction = "Blue Team strongly favored"
            confidence = "high"
        elif blue_prob > 0.6:
            prediction = "Blue Team favored"
            confidence = "medium"
        elif blue_prob < 0.3:
            prediction = "Red Team strongly favored"
            confidence = "high"
        elif blue_prob < 0.4:
            prediction = "Red Team favored"
            confidence = "medium"
        else:
            prediction = "Even game"
            confidence = "low"

        return PredictionResponse(
            blue_win_probability=blue_prob,
            red_win_probability=red_prob,
            prediction=prediction,
            confidence=confidence,
            details={
                'kill_diff': kill_diff,
                'gold_diff': gold_diff,
                'tower_diff': tower_diff,
                'dragon_diff': dragon_diff,
                'game_duration': request.game_duration,
                'model': 'random_forest',
                'accuracy': '97.9%'
            }
        )

    except ValueError as e:
        # User input errors
        logger.warning(f"Invalid input for game state prediction: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid request: {str(e)}")
    except Exception as e:
        logger.error(f"Error in game state prediction: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Internal server error during prediction. Please try again later."
        )


@router.post("/predict-game-state-v2", response_model=PredictionResponse, dependencies=[])
@limiter.limit("10/minute")
async def predict_game_state_v2(http_request: Request, request: GameStateV2Request):
    """
    🆕 NEW: Predict win probability using the advanced Game State Predictor

    This model is trained on 10,000 matches with timeline data and achieves
    79.28% accuracy (compared to ~52% for draft-only predictions).

    Features used:
    - Gold (total and diff)
    - XP (total and diff)
    - Level
    - CS (minions killed)
    - Kills (total and diff)
    - Objectives (Dragons, Barons, Towers)

    Returns:
    - Blue/Red team win probabilities
    - Prediction text
    - Confidence level
    - Game state analysis
    """
    # Verify API key
    await verify_api_key(http_request)

    if not ml_engine.game_state_predictor or not ml_engine.game_state_predictor.is_loaded:
        raise HTTPException(status_code=503, detail="Game State Predictor not loaded")

    try:
        result = ml_engine.game_state_predictor.predict(
            blue_gold=request.blue_gold,
            red_gold=request.red_gold,
            blue_xp=request.blue_xp,
            red_xp=request.red_xp,
            blue_level=request.blue_level,
            red_level=request.red_level,
            blue_cs=request.blue_cs,
            red_cs=request.red_cs,
            blue_kills=request.blue_kills,
            red_kills=request.red_kills,
            blue_dragons=request.blue_dragons,
            red_dragons=request.red_dragons,
            blue_barons=request.blue_barons,
            red_barons=request.red_barons,
            blue_towers=request.blue_towers,
            red_towers=request.red_towers
        )

        return PredictionResponse(
            blue_win_probability=result['blue_win_probability'],
            red_win_probability=result['red_win_probability'],
            prediction=result['prediction'],
            confidence=result['confidence'],
            details=result['details']
        )

    except ValueError as e:
        logger.warning(f"Invalid input for game state v2 prediction: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid request: {str(e)}")
    except Exception as e:
        logger.error(f"Error in game state v2 prediction: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Internal server error during prediction. Please try again later."
        )
