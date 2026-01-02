"""
LoL Intelligent Coach API - Vercel Serverless Entrypoint
=========================================================

This is the main entrypoint for Vercel Python Serverless Functions.
Vercel expects a variable named 'app' to be exported.

Architecture: Vercel Single Project
- Frontend: Next.js (lol-coach-frontend/)
- Backend: Python Serverless Functions (api/)
- Database: Vercel Postgres
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from api.core.config import settings
from api.core.logging import logger
from api.services.ml_engine import ml_engine

# Import all routers
from api.routers import predictions, champions, items, live_game, stats


# ============================================================================
# LIFESPAN EVENT (Load ML Models)
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load ML models on startup, cleanup on shutdown"""
    logger.info("🚀 Vercel Serverless: Loading ML models...")
    try:
        await ml_engine.load_all_models()
        logger.info("✓ ML models loaded successfully")
    except Exception as e:
        logger.error(f"❌ Failed to load ML models: {e}")
        # Continue anyway - app will work with limited functionality

    yield  # App is running

    # Cleanup on shutdown (if needed)
    logger.info("👋 Shutting down...")


# Create FastAPI app (Vercel will use this)
app = FastAPI(
    title="LoL Intelligent Coach API",
    description="AI-powered League of Legends win prediction and coaching system",
    version="2.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan
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
        "service": "LoL Intelligent Coach API",
        "version": "2.1.0",
        "deployment": "Vercel Serverless",
        "endpoints": {
            "docs": "/api/docs",
            "champion_matchup": "/api/predict-champion-matchup",
            "game_state": "/api/predict-game-state",
            "game_state_v2": "/api/predict-game-state-v2 (NEW: 79.28% accuracy)",
            "champion_stats": "/api/champion-stats",
            "champion_search": "/api/champions/search?query=yasuo",
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
        "deployment": "Vercel Serverless",
        "models_loaded": health_status,
        "game_state_predictor_info": (
            ml_engine.game_state_predictor.get_model_info()
            if ml_engine.game_state_predictor and ml_engine.game_state_predictor.is_loaded
            else None
        )
    }


# ============================================================================
# VERCEL SERVERLESS HANDLER
# ============================================================================

# Vercel automatically uses this 'app' variable for serverless deployments
# No need to run uvicorn.run() - Vercel handles that
