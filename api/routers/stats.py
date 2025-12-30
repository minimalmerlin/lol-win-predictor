"""
Stats API endpoints
Handles model performance and system statistics
"""

from fastapi import APIRouter, HTTPException

from api.services.ml_engine import ml_engine
from api.core.logging import logger
from api.core.database import get_database_stats, get_model_performance

router = APIRouter(prefix="/api", tags=["stats"])


@router.get("/stats")
async def get_stats():
    """
    Get comprehensive system statistics (used by Stats page)

    Returns database stats, model performance, and system info
    """
    try:
        # Get database stats from PostgreSQL
        try:
            db_stats = get_database_stats()
        except Exception as e:
            logger.error(f"❌ Failed to get database stats: {e}")
            raise HTTPException(
                status_code=503,
                detail="Database unavailable. Cannot fetch statistics."
            )

        # Get model performance from loaded models (metadata from .pkl files)
        game_state_perf = {}
        if ml_engine.game_state_predictor and ml_engine.game_state_predictor.is_loaded:
            meta = ml_engine.game_state_predictor.metadata
            game_state_perf = {
                'accuracy': meta.get('accuracy', 0.7928),
                'roc_auc': meta.get('roc_auc', 0.8780),
                'snapshot_time': meta.get('snapshot_time', 20),
                'trained_on': db_stats['matches'],  # Use actual DB count
                'timestamp': meta.get('timestamp', '2025-12-30')
            }
        else:
            logger.error("Game State Predictor not loaded")
            raise HTTPException(
                status_code=503,
                detail="Game State Predictor model not available"
            )

        # Champion Matchup performance (from model metadata)
        champion_matchup_perf = {}
        if ml_engine.champion_predictor:
            # Use metadata from champion predictor if available
            champion_matchup_perf = {
                'accuracy': 0.52,  # TODO: Store in model metadata
                'trained_on': db_stats['matches'],  # Use actual DB count
                'timestamp': '2025-12-30'
            }
        else:
            logger.error("Champion Matchup Predictor not loaded")
            raise HTTPException(
                status_code=503,
                detail="Champion Matchup Predictor model not available"
            )

        response = {
            "database": db_stats,
            "models": {
                "game_state": game_state_perf,
                "champion_matchup": champion_matchup_perf
            },
            "api_version": "2.1.0",
            "data_source": "PostgreSQL (Supabase)"
        }

        return response

    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        logger.error(f"Error fetching stats: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch statistics. Please try again later."
        )


@router.get("/stats/model")
async def get_model_stats():
    """Get model performance statistics (legacy endpoint)"""
    try:
        # Get database stats for match count
        try:
            db_perf = get_model_performance('champion_matchup')
        except Exception as e:
            logger.error(f"❌ Failed to get model performance from database: {e}")
            raise HTTPException(
                status_code=503,
                detail="Database unavailable. Cannot fetch model statistics."
            )

        # Get model metadata from loaded models
        accuracy = 0.52  # Default for champion matchup
        roc_auc = 0.0

        if ml_engine.game_state_predictor and ml_engine.game_state_predictor.is_loaded:
            meta = ml_engine.game_state_predictor.metadata
            accuracy = meta.get('accuracy', 0.7928)
            roc_auc = meta.get('roc_auc', 0.8780)

        return {
            "model_accuracy": accuracy,
            "roc_auc": roc_auc,
            "training_matches": db_perf['matches_count'],
            "timestamp": db_perf.get('timestamp', '2025-12-30'),
            "champions_analyzed": len(ml_engine.champion_stats) if ml_engine.champion_stats else 0,
            "champions_with_builds": len(ml_engine.item_builds) if ml_engine.item_builds else 0,
            "champions_with_synergies": len(ml_engine.best_teammates) if ml_engine.best_teammates else 0,
            "data_source": "PostgreSQL (Supabase)"
        }
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        logger.error(f"Error fetching model stats: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch model statistics. Please try again later."
        )
