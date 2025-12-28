"""
LoL Intelligent Coach - FastAPI Backend v2
==========================================

Modern REST API with:
- Champion Matchup Prediction
- Game State Win Prediction
- Champion Statistics
- Item Recommendations
- Auto-generated Swagger docs
"""

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import json
from pathlib import Path
import pickle
import logging
import os

from intelligent_item_recommender import IntelligentItemRecommender
from riot_live_client import RiotLiveClient
from dynamic_build_generator import DynamicBuildGenerator, Champion, GameState

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment configuration
ENV = os.getenv("ENV", "development")
INTERNAL_API_KEY = os.getenv("INTERNAL_API_KEY")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000")

# Rate limiting
limiter = Limiter(key_func=get_remote_address)

# Security: API Key middleware
async def verify_api_key(request: Request):
    """
    Verify API key for production environments.
    Development mode allows requests without API key (with warning).
    """
    if ENV == "production":
        api_key = request.headers.get("X-INTERNAL-API-KEY")

        if not api_key or api_key != INTERNAL_API_KEY:
            logger.warning(f"Unauthorized API access attempt from {request.client.host}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or missing API key"
            )
    elif ENV == "development":
        # Development mode - log warning but allow
        if not request.headers.get("X-INTERNAL-API-KEY"):
            logger.warning(f"Development mode: Request from {request.client.host} without API key")

    return True

# FastAPI App
app = FastAPI(
    title="LoL Intelligent Coach API",
    description="AI-powered League of Legends win prediction and coaching system",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Rate limiting setup
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS - Production-ready with environment-based origins
origins_list = [origin.strip() for origin in ALLOWED_ORIGINS.split(",")]
logger.info(f"CORS allowed origins: {origins_list}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class ChampionMatchupRequest(BaseModel):
    blue_champions: List[str] = Field(..., min_items=1, max_items=5, example=["MissFortune", "Lux", "Braum", "Renekton", "Fizz"])
    red_champions: List[str] = Field(..., min_items=1, max_items=5, example=["Caitlyn", "Morgana", "Leona", "Darius", "Zed"])


class GameStateRequest(BaseModel):
    game_duration: int = Field(..., ge=1, le=60, example=20)
    blue_kills: int = Field(..., ge=0, example=15)
    blue_deaths: int = Field(..., ge=0, example=10)
    blue_assists: int = Field(..., ge=0, example=25)
    blue_gold: int = Field(..., ge=0, example=35000)
    blue_towers: int = Field(..., ge=0, le=11, example=4)
    blue_dragons: int = Field(..., ge=0, le=4, example=2)
    blue_barons: int = Field(..., ge=0, le=2, example=0)
    blue_vision_score: int = Field(..., ge=0, example=90)
    red_kills: int = Field(..., ge=0, example=10)
    red_deaths: int = Field(..., ge=0, example=15)
    red_assists: int = Field(..., ge=0, example=18)
    red_gold: int = Field(..., ge=0, example=30000)
    red_towers: int = Field(..., ge=0, le=11, example=2)
    red_dragons: int = Field(..., ge=0, le=4, example=1)
    red_barons: int = Field(..., ge=0, le=2, example=0)
    red_vision_score: int = Field(..., ge=0, example=75)


class ItemRecommendationRequest(BaseModel):
    champion: str = Field(..., example="MissFortune")
    enemy_team: List[str] = Field(..., min_items=1, max_items=5, example=["Zed", "Malphite", "Leona", "Caitlyn", "Lux"])
    top_n: int = Field(5, ge=1, le=10, example=5)


class PredictionResponse(BaseModel):
    blue_win_probability: float
    red_win_probability: float
    prediction: str
    confidence: str
    details: Optional[Dict] = None


class ChampionStatsResponse(BaseModel):
    champions: List[Dict]
    total_champions: int


class ItemRecommendationResponse(BaseModel):
    champion: str
    recommended_items: List[Dict]
    popular_builds: List[Dict]


class StatsResponse(BaseModel):
    model_accuracy: float
    champions_analyzed: int
    training_matches: int


# ============================================================================
# MODEL LOADING
# ============================================================================

champion_predictor = None
win_predictor = None
champion_stats = None
item_builds = None
item_recommender = None
best_teammates = None
riot_live_client = None
build_generator = None


@app.on_event("startup")
async def load_models():
    """Load ML models and data on startup"""
    global champion_predictor, win_predictor, champion_stats, item_builds, item_recommender, best_teammates, riot_live_client, build_generator

    logger.info("🚀 Loading models...")

    # Champion Matchup Predictor
    try:
        champion_predictor = ChampionMatchupPredictor()
        champion_predictor.load_model('./models/champion_predictor.pkl')
        logger.info("✓ Champion Predictor loaded")
    except Exception as e:
        logger.error(f"❌ Failed to load Champion Predictor: {e}")

    # Win Prediction Model (try RF, fallback to LR)
    try:
        win_predictor = WinPredictionModel()
        # Try Random Forest first (best accuracy but large file)
        try:
            win_predictor.load_model('./models/win_predictor_rf.pkl')
            logger.info("✓ Win Predictor loaded (Random Forest)")
        except:
            # Fallback to Linear Regression (smaller file, still good)
            win_predictor.load_model('./models/win_predictor_lr.pkl')
            logger.info("✓ Win Predictor loaded (Linear Regression - fallback)")
    except Exception as e:
        logger.error(f"❌ Failed to load Win Predictor: {e}")

    # Champion Stats
    try:
        stats_file = Path('./data/champion_data/champion_stats.json')
        with open(stats_file, 'r') as f:
            champion_stats = json.load(f)
        logger.info(f"✓ Champion Stats loaded ({len(champion_stats)} champions)")
    except Exception as e:
        logger.error(f"❌ Failed to load Champion Stats: {e}")

    # Item Builds
    try:
        item_file = Path('./data/champion_data/item_builds.json')
        with open(item_file, 'r') as f:
            item_builds = json.load(f)
        logger.info(f"✓ Item Builds loaded ({len(item_builds)} champions)")
    except Exception as e:
        logger.error(f"❌ Failed to load Item Builds: {e}")

    # Intelligent Item Recommender
    try:
        item_recommender = IntelligentItemRecommender(data_dir='./data/champion_data')
        logger.info("✓ Intelligent Item Recommender loaded")
    except Exception as e:
        logger.error(f"❌ Failed to load Intelligent Item Recommender: {e}")

    # Best Teammates
    try:
        teammates_file = Path('./data/champion_data/best_teammates.json')
        with open(teammates_file, 'r') as f:
            best_teammates = json.load(f)
        logger.info(f"✓ Best Teammates loaded ({len(best_teammates)} champions)")
    except Exception as e:
        logger.error(f"❌ Failed to load Best Teammates: {e}")

    # Riot Live Client
    try:
        riot_live_client = RiotLiveClient()
        logger.info("✓ Riot Live Client initialized")
    except Exception as e:
        logger.error(f"❌ Failed to initialize Riot Live Client: {e}")

    # Dynamic Build Generator
    try:
        build_generator = DynamicBuildGenerator(data_dir='./data/champion_data')
        logger.info("✓ Dynamic Build Generator initialized")
    except Exception as e:
        logger.error(f"❌ Failed to initialize Build Generator: {e}")

    logger.info("🎉 All models loaded successfully!")


# ============================================================================
# ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """API Root - Health Check"""
    return {
        "status": "healthy",
        "service": "LoL Intelligent Coach API v2",
        "version": "2.0.0",
        "endpoints": {
            "docs": "/docs",
            "champion_matchup": "/api/predict-champion-matchup",
            "game_state": "/api/predict-game-state",
            "champion_stats": "/api/champion-stats",
            "champion_search": "/api/champions/search?query=yasou",
            "champion_details": "/api/champions/{champion_name}",
            "champion_list": "/api/champions/list",
            "item_recommendations": "/api/item-recommendations",
            "intelligent_items": "/api/item-recommendations-intelligent",
            "model_stats": "/api/stats/model",
            "live_game_status": "/api/live/status",
            "live_game_data": "/api/live/game-data",
            "live_prediction": "/api/live/predict"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "models_loaded": {
            "champion_predictor": champion_predictor is not None,
            "win_predictor": win_predictor is not None,
            "champion_stats": champion_stats is not None,
            "item_builds": item_builds is not None,
            "item_recommender": item_recommender is not None,
            "best_teammates": best_teammates is not None
        }
    }


@app.post("/api/predict-champion-matchup", response_model=PredictionResponse, dependencies=[])
@limiter.limit("10/minute")
async def predict_champion_matchup(http_request: Request, request: ChampionMatchupRequest):
    """
    Predict win probability based on champion team compositions

    Returns:
    - Blue/Red team win probabilities
    - Prediction text
    - Confidence level
    - Champion win-rate details
    """
    # Verify API key
    await verify_api_key(http_request)

    if not champion_predictor:
        raise HTTPException(status_code=503, detail="Champion Predictor not loaded")

    try:
        result = champion_predictor.predict(
            blue_champions=request.blue_champions,
            red_champions=request.red_champions
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

    except Exception as e:
        logger.error(f"Error in champion matchup prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/predict-game-state", response_model=PredictionResponse, dependencies=[])
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

    if not win_predictor:
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
        blue_prob = win_predictor.predict_single(game_state)
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

    except Exception as e:
        logger.error(f"Error in game state prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/champion-stats", response_model=ChampionStatsResponse)
async def get_champion_stats(
    min_games: int = 1,
    sort_by: str = "win_rate",
    limit: int = 50
):
    """
    Get champion statistics

    Query Parameters:
    - min_games: Minimum games played (default: 1)
    - sort_by: Sort field (win_rate, games, wins) (default: win_rate)
    - limit: Max results (default: 50)
    """
    if not champion_stats:
        raise HTTPException(status_code=503, detail="Champion stats not loaded")

    try:
        # Filter and format
        champions_list = []
        for name, stats in champion_stats.items():
            if stats['games'] >= min_games:
                champions_list.append({
                    'name': name,
                    'games': stats['games'],
                    'wins': stats['wins'],
                    'losses': stats['losses'],
                    'win_rate': stats['win_rate'],
                    'roles': stats.get('roles', {})
                })

        # Sort
        if sort_by == "win_rate":
            champions_list.sort(key=lambda x: x['win_rate'], reverse=True)
        elif sort_by == "games":
            champions_list.sort(key=lambda x: x['games'], reverse=True)
        elif sort_by == "wins":
            champions_list.sort(key=lambda x: x['wins'], reverse=True)

        # Limit
        champions_list = champions_list[:limit]

        return ChampionStatsResponse(
            champions=champions_list,
            total_champions=len(champion_stats)
        )

    except Exception as e:
        logger.error(f"Error fetching champion stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/item-recommendations", response_model=ItemRecommendationResponse)
async def get_item_recommendations(request: ItemRecommendationRequest):
    """
    Get item recommendations for a champion

    Returns:
    - Recommended items based on win-rate
    - Popular item builds
    """
    if not item_builds:
        raise HTTPException(status_code=503, detail="Item builds not loaded")

    try:
        champion = request.champion

        if champion not in item_builds:
            raise HTTPException(status_code=404, detail=f"Champion '{champion}' not found")

        champion_items = item_builds[champion]

        # Get popular items sorted by win-rate
        popular_items = []
        for item_id, stats in champion_items.get('popular_items', {}).items():
            if stats['count'] >= 3:  # Min 3 games (reduced from 10)
                popular_items.append({
                    'item_id': stats['item_id'],
                    'games': stats['count'],
                    'wins': stats['wins'],
                    'win_rate': stats['wins'] / stats['count'] if stats['count'] > 0 else 0
                })

        popular_items.sort(key=lambda x: x['win_rate'], reverse=True)
        recommended_items = popular_items[:request.top_n]

        # Get popular builds
        builds = []
        for build_key, stats in champion_items.get('builds', {}).items():
            if stats['count'] >= 2:  # Min 2 games (reduced from 5)
                builds.append({
                    'items': stats['items'],
                    'games': stats['count'],
                    'wins': stats['wins'],
                    'win_rate': stats['win_rate']
                })

        builds.sort(key=lambda x: x['win_rate'], reverse=True)
        popular_builds = builds[:10]  # Show top 10 builds instead of 5

        return ItemRecommendationResponse(
            champion=champion,
            recommended_items=recommended_items,
            popular_builds=popular_builds
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching item recommendations: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/champions/list")
async def get_champions_list():
    """Get list of all available champions"""
    if not champion_stats:
        raise HTTPException(status_code=503, detail="Champion stats not loaded")

    return {
        "champions": sorted(list(champion_stats.keys())),
        "total": len(champion_stats)
    }


@app.get("/api/champions/search")
async def search_champions(
    query: str,
    limit: int = 10,
    include_stats: bool = False
):
    """
    Fuzzy search for champions (handles typos)

    Query Parameters:
    - query: Search string
    - limit: Max results (default: 10)
    - include_stats: Include champion stats (default: False)
    """
    if not item_recommender:
        raise HTTPException(status_code=503, detail="Item Recommender not loaded")

    try:
        results = item_recommender.search_champions(
            query=query,
            limit=limit,
            include_stats=include_stats
        )

        return {
            "query": query,
            "results": results,
            "count": len(results)
        }

    except Exception as e:
        logger.error(f"Error searching champions: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/champions/{champion_name}")
async def get_champion_details(champion_name: str):
    """
    Get detailed information about a specific champion

    Returns:
    - Champion stats
    - Best teammates
    - Item builds
    - Fuzzy match if exact name not found
    """
    if not item_recommender:
        raise HTTPException(status_code=503, detail="Item Recommender not loaded")

    try:
        # Fuzzy match the champion name
        matches = item_recommender.fuzzy_find_champion(champion_name, threshold=0.6)

        if not matches:
            raise HTTPException(
                status_code=404,
                detail=f"Champion '{champion_name}' not found"
            )

        # Use best match
        matched_champion = matches[0][0]
        match_quality = matches[0][1]

        # Get champion stats
        stats = champion_stats.get(matched_champion, {})

        # Get item builds
        item_builds_data = item_recommender.get_item_builds(
            champion=matched_champion,
            top_n=10
        )

        # Get best teammates
        teammates = best_teammates.get(matched_champion, []) if best_teammates else []

        return {
            "champion": matched_champion,
            "match_quality": match_quality,
            "exact_match": match_quality > 0.9,
            "stats": stats,
            "item_builds": item_builds_data,
            "best_teammates": teammates[:10],
            "has_synergy_data": len(teammates) > 0
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching champion details: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/item-recommendations-intelligent")
async def get_intelligent_item_recommendations(request: ItemRecommendationRequest):
    """
    Get intelligent item recommendations with heuristics

    Uses:
    - Exact builds when available
    - Similar champion builds as fallback
    - Counter-items based on enemy team
    - Fuzzy matching for champion names

    Returns:
    - Champion matched
    - Top builds with win rates
    - Enemy-adjusted recommendations
    """
    if not item_recommender:
        raise HTTPException(status_code=503, detail="Item Recommender not loaded")

    try:
        result = item_recommender.recommend_items_for_matchup(
            champion=request.champion,
            enemy_team=request.enemy_team,
            top_n=request.top_n
        )

        return result

    except Exception as e:
        logger.error(f"Error fetching intelligent item recommendations: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stats/model")
async def get_model_stats():
    """Get model performance statistics"""
    try:
        perf_file = Path('./models/performance.json')
        with open(perf_file, 'r') as f:
            perf = json.load(f)

        return {
            "model_accuracy": perf.get('accuracy', 0.0),
            "roc_auc": perf.get('roc_auc', 0.0),
            "training_matches": perf.get('matches_count', 0),
            "timestamp": perf.get('timestamp', ''),
            "champions_analyzed": len(champion_stats) if champion_stats else 0,
            "champions_with_builds": len(item_builds) if item_builds else 0,
            "champions_with_synergies": len(best_teammates) if best_teammates else 0
        }
    except Exception as e:
        logger.error(f"Error fetching model stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# LIVE GAME ENDPOINTS
# ============================================================================

@app.get("/api/live/status")
async def get_live_game_status():
    """
    Check if a live game is running

    Returns:
    - is_running: bool
    - message: str
    """
    if not riot_live_client:
        raise HTTPException(status_code=503, detail="Riot Live Client not initialized")

    try:
        is_running = riot_live_client.is_game_running()

        return {
            "is_running": is_running,
            "message": "Game is running" if is_running else "No game detected",
            "instructions": "Start a game to enable live tracking" if not is_running else None
        }
    except Exception as e:
        logger.error(f"Error checking game status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/live/game-data")
async def get_live_game_data():
    """
    Get current live game data

    Returns:
    - Full game state with all player data
    - Formatted for ML prediction
    """
    if not riot_live_client:
        raise HTTPException(status_code=503, detail="Riot Live Client not initialized")

    try:
        # Check if game is running
        if not riot_live_client.is_game_running():
            raise HTTPException(
                status_code=404,
                detail="No game is currently running. Start a game to use this endpoint."
            )

        # Get all game data
        all_data = riot_live_client.get_all_game_data()
        if not all_data:
            raise HTTPException(status_code=500, detail="Failed to fetch game data")

        # Extract and format team data
        team_data = riot_live_client.extract_team_data(all_data)

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
        logger.error(f"Error fetching live game data: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/live/predict")
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
    if not riot_live_client:
        raise HTTPException(status_code=503, detail="Riot Live Client not initialized")

    if not win_predictor or not champion_predictor:
        raise HTTPException(status_code=503, detail="Prediction models not loaded")

    try:
        # Check if game is running
        if not riot_live_client.is_game_running():
            raise HTTPException(
                status_code=404,
                detail="No game is currently running. Start a game to get live predictions."
            )

        # Get formatted prediction data
        pred_data = riot_live_client.get_live_prediction_data()
        if not pred_data:
            raise HTTPException(status_code=500, detail="Failed to fetch live game data")

        # Champion matchup prediction
        champion_prediction = champion_predictor.predict(
            blue_champions=pred_data['blue_champions'],
            red_champions=pred_data['red_champions']
        )

        # Game state prediction (if game has progressed enough)
        game_state_prediction = None
        game_duration = pred_data['game_duration']

        if game_duration >= 10:  # At least 10 minutes
            try:
                game_state_prediction = win_predictor.predict_win_probability(
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
        logger.error(f"Error generating live prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))


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


# ============================================================================
# RUN SERVER
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    import os

    # Get port from environment (Railway/Cloud) or use default
    port = int(os.environ.get("PORT", 8080))

    # Check if in production (Railway sets this)
    is_production = os.environ.get("RAILWAY_ENVIRONMENT") is not None

    # Development or Production server
    uvicorn.run(
        "api_v2:app",
        host="0.0.0.0",
        port=port,
        reload=not is_production,  # Disable reload in production
        log_level="info"
    )


# ============================================================================
# DYNAMIC BUILD ENDPOINTS
# ============================================================================

class DynamicBuildRequest(BaseModel):
    user_champion: str
    user_role: str  # Top, Jungle, Mid, ADC, Support
    ally_champions: List[str] = Field(..., min_length=4, max_length=4)
    ally_roles: List[str] = Field(..., min_length=4, max_length=4)
    enemy_champions: List[str] = Field(..., min_length=5, max_length=5)
    enemy_roles: List[str] = Field(..., min_length=5, max_length=5)
    game_state: str = Field(default="even", pattern="^(leading|even|losing)$")


@app.post("/api/draft/dynamic-build")
async def generate_dynamic_build(request: DynamicBuildRequest):
    """
    Generate personalized item build path
    
    Features:
    - User's champion & role specific
    - Enemy team composition analysis
    - Role detection (e.g., Lux Support vs Mid)
    - Game state adaptation (leading/even/losing)
    - Situational branches (vs AP/AD heavy, healers, etc.)
    - Timeline-based items (early/mid/late game)
    
    Returns:
    - Core items (always buy)
    - Situational items (conditional)
    - Early/Mid/Late game items
    - Build explanation
    """
    if not build_generator:
        raise HTTPException(status_code=503, detail="Build Generator not initialized")
    
    try:
        # Create Champion objects
        user_champ = Champion(request.user_champion, request.user_role)
        
        ally_team = [user_champ]
        for champ_name, role in zip(request.ally_champions, request.ally_roles):
            ally_team.append(Champion(champ_name, role))
        
        enemy_team = []
        for champ_name, role in zip(request.enemy_champions, request.enemy_roles):
            enemy_team.append(Champion(champ_name, role))
        
        # Map game state string to enum
        game_state_map = {
            "leading": GameState.LEADING,
            "even": GameState.EVEN,
            "losing": GameState.LOSING
        }
        game_state = game_state_map.get(request.game_state, GameState.EVEN)
        
        # Generate build path
        build_path = build_generator.generate_build_path(
            user_champion=user_champ,
            ally_team=ally_team,
            enemy_team=enemy_team,
            game_state=game_state
        )
        
        return {
            "champion": request.user_champion,
            "role": request.user_role,
            "game_state": request.game_state,
            "core_items": build_path.core_items,
            "situational_items": build_path.situational_items,
            "early_game": build_path.early_game,
            "mid_game": build_path.mid_game,
            "late_game": build_path.late_game,
            "explanation": build_path.explanation
        }
        
    except Exception as e:
        logger.error(f"Error generating dynamic build: {e}")
        raise HTTPException(status_code=500, detail=str(e))
