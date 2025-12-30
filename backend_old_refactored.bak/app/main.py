"""
LoL Intelligent Coach - FastAPI Backend v2 (Refactored)
=======================================================

Clean architecture with modular routers:
- /api/predict-* -> predictions router
- /api/champions/* -> champions router
- /api/item-* -> items router
- /api/live/* -> live_game router
- /api/stats* -> stats router
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.core.config import settings
from app.core.logging import logger
from app.services.ml_engine import ml_engine

# Import all routers
from app.routers import predictions, champions, items, live_game, stats


# Create FastAPI app
app = FastAPI(
    title="LoL Intelligent Coach API",
    description="AI-powered League of Legends win prediction and coaching system",
    version="2.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Rate limiting setup
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS - Production-ready with environment-based origins
logger.info(f"CORS allowed origins: {settings.cors_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# STARTUP / SHUTDOWN EVENTS
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Load ML models and data on startup"""
    await ml_engine.load_all_models()


# ============================================================================
# INCLUDE ROUTERS
# ============================================================================

# Prediction endpoints
app.include_router(predictions.router)

# Champion endpoints
app.include_router(champions.router)

# Item endpoints
app.include_router(items.router)

# Live game endpoints
app.include_router(live_game.router)

# Stats endpoints
app.include_router(stats.router)


# ============================================================================
# ROOT ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """API Root - Health Check"""
    return {
        "status": "healthy",
        "service": "LoL Intelligent Coach API v2",
        "version": "2.1.0",
        "endpoints": {
            "docs": "/docs",
            "champion_matchup": "/api/predict-champion-matchup",
            "game_state": "/api/predict-game-state",
            "game_state_v2": "/api/predict-game-state-v2 (NEW: 79.28% accuracy)",
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
    health_status = ml_engine.get_health_status()

    return {
        "status": "healthy",
        "models_loaded": health_status,
        "game_state_predictor_info": (
            ml_engine.game_state_predictor.get_model_info()
            if ml_engine.game_state_predictor and ml_engine.game_state_predictor.is_loaded
            else None
        )
    }


# ============================================================================
# RUN SERVER
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    # Development or Production server
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=not settings.IS_PRODUCTION,  # Disable reload in production
        log_level="info"
    )
