"""
Live Game API endpoints
Handles live game tracking and predictions
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Optional

from api.services.ml_engine import ml_engine
from api.core.logging import logger

router = APIRouter(prefix="/api/live", tags=["live_game"])


@router.get("/status")
async def get_live_game_status():
    """
    Check if a live game is running

    Returns:
    - is_running: bool
    - message: str
    """
    if not ml_engine.riot_live_client:
        raise HTTPException(status_code=503, detail="Riot Live Client not initialized")

    try:
        is_running = ml_engine.riot_live_client.is_game_running()

        return {
            "is_running": is_running,
            "message": "Game is running" if is_running else "No game detected",
            "instructions": "Start a game to enable live tracking" if not is_running else None
        }
    except Exception as e:
        logger.error(f"Error checking game status: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to check game status. Please try again later."
        )


@router.get("/game-data")
async def get_live_game_data():
    """
    Get current live game data

    Returns:
    - Full game state with all player data
    - Formatted for ML prediction
    """
    if not ml_engine.riot_live_client:
        raise HTTPException(status_code=503, detail="Riot Live Client not initialized")

    try:
        # Check if game is running
        if not ml_engine.riot_live_client.is_game_running():
            raise HTTPException(
                status_code=404,
                detail="No game is currently running. Start a game to use this endpoint."
            )

        # Get all game data
        all_data = ml_engine.riot_live_client.get_all_game_data()
        if not all_data:
            raise HTTPException(status_code=500, detail="Failed to fetch game data")

        # Extract and format team data
        team_data = ml_engine.riot_live_client.extract_team_data(all_data)

        return {
            "game_running": True,
            "game_time": team_data.get('game_time', 0),
            "game_mode": team_data.get('game_mode'),
            "blue_team": team_data.get('blue_team'),
            "red_team": team_data.get('red_team')
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching live game data: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch live game data. Please try again later."
        )


@router.get("/predict")
async def get_live_win_prediction():
    """
    Get live win prediction for current game

    Automatically fetches current game state and predicts outcome

    Returns:
    - Win probabilities for both teams
    - Champion matchup analysis
    - Game state prediction
    - Recommendations
    """
    if not ml_engine.riot_live_client:
        raise HTTPException(status_code=503, detail="Riot Live Client not initialized")

    if not ml_engine.win_predictor or not ml_engine.champion_predictor:
        raise HTTPException(status_code=503, detail="Prediction models not loaded")

    try:
        # Check if game is running
        if not ml_engine.riot_live_client.is_game_running():
            raise HTTPException(
                status_code=404,
                detail="No game is currently running. Start a game to get live predictions."
            )

        # Get formatted prediction data
        pred_data = ml_engine.riot_live_client.get_live_prediction_data()
        if not pred_data:
            raise HTTPException(status_code=500, detail="Failed to fetch live game data")

        # Champion matchup prediction
        champion_prediction = ml_engine.champion_predictor.predict(
            blue_champions=pred_data['blue_champions'],
            red_champions=pred_data['red_champions']
        )

        # Game state prediction (if game has progressed enough)
        game_state_prediction = None
        game_duration = pred_data['game_duration']

        if game_duration >= 10:  # At least 10 minutes
            try:
                game_state_prediction = ml_engine.win_predictor.predict_win_probability(
                    game_duration=game_duration,
                    blue_kills=pred_data['blue_kills'],
                    blue_deaths=pred_data['blue_deaths'],
                    blue_assists=pred_data['blue_assists'],
                    blue_gold=pred_data['blue_gold'],
                    blue_towers=pred_data['blue_towers'],
                    blue_dragons=pred_data['blue_dragons'],
                    blue_barons=pred_data['blue_barons'],
                    blue_vision_score=pred_data['blue_vision_score'],
                    red_kills=pred_data['red_kills'],
                    red_deaths=pred_data['red_deaths'],
                    red_assists=pred_data['red_assists'],
                    red_gold=pred_data['red_gold'],
                    red_towers=pred_data['red_towers'],
                    red_dragons=pred_data['red_dragons'],
                    red_barons=pred_data['red_barons'],
                    red_vision_score=pred_data['red_vision_score']
                )
            except Exception as e:
                logger.warning(f"Game state prediction failed: {e}")

        return {
            "game_time": game_duration,
            "game_time_formatted": f"{game_duration}:00",
            "blue_team": {
                "champions": pred_data['blue_champions'],
                "kills": pred_data['blue_kills'],
                "deaths": pred_data['blue_deaths'],
                "gold": pred_data['blue_gold'],
                "towers": pred_data['blue_towers']
            },
            "red_team": {
                "champions": pred_data['red_champions'],
                "kills": pred_data['red_kills'],
                "deaths": pred_data['red_deaths'],
                "gold": pred_data['red_gold'],
                "towers": pred_data['red_towers']
            },
            "predictions": {
                "champion_matchup": {
                    "blue_win_probability": champion_prediction['blue_win_probability'],
                    "red_win_probability": champion_prediction['red_win_probability'],
                    "confidence": champion_prediction['confidence']
                },
                "game_state": game_state_prediction if game_state_prediction else {
                    "message": "Game too early for state prediction (need 10+ minutes)",
                    "blue_win_probability": None,
                    "red_win_probability": None
                }
            },
            "recommendation": _generate_live_recommendation(
                pred_data,
                champion_prediction,
                game_state_prediction
            )
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating live prediction: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to generate live prediction. Please try again later."
        )


def _generate_live_recommendation(pred_data: Dict, champion_pred: Dict, state_pred: Optional[Dict]) -> str:
    """Generate recommendation based on live game state"""

    blue_champ_prob = champion_pred['blue_win_probability']
    game_duration = pred_data['game_duration']

    # Early game (< 15 min)
    if game_duration < 15:
        if blue_champ_prob > 0.55:
            return "Strong early comp! Push your advantage and secure objectives."
        elif blue_champ_prob < 0.45:
            return "Play safe early game. Focus on farming and scaling."
        else:
            return "Even matchup. Focus on vision control and objective setup."

    # Mid/Late game (15+ min) - use state prediction if available
    if state_pred:
        blue_state_prob = state_pred.get('blue_win_probability', 0.5)

        gold_diff = pred_data['blue_gold'] - pred_data['red_gold']
        tower_diff = pred_data['blue_towers'] - pred_data['red_towers']

        if blue_state_prob > 0.65:
            return f"You're ahead! (Gold: +{gold_diff:,}) Keep pressure and don't throw."
        elif blue_state_prob < 0.35:
            return f"Behind (Gold: {gold_diff:,}). Secure vision, catch enemies, stall for scaling."
        else:
            return "Close game! Next teamfight is critical. Ward objectives."

    return "Monitor your progress and adjust strategy based on objectives."
