"""
Item Recommendation API endpoints
Handles item recommendations and dynamic builds
"""

from fastapi import APIRouter, HTTPException
import sys
from pathlib import Path

from api.schemas.item import ItemRecommendationRequest, ItemRecommendationResponse, DynamicBuildRequest
from api.services.ml_engine import ml_engine
from api.core.logging import logger

# Import for dynamic build
sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from dynamic_build_generator import Champion, GameState

router = APIRouter(prefix="/api", tags=["items"])


@router.post("/item-recommendations", response_model=ItemRecommendationResponse)
async def get_item_recommendations(request: ItemRecommendationRequest):
    """
    Get item recommendations for a champion

    Returns:
    - Recommended items based on win-rate
    - Popular item builds
    """
    if not ml_engine.item_builds:
        raise HTTPException(status_code=503, detail="Item builds not loaded")

    try:
        champion = request.champion

        if champion not in ml_engine.item_builds:
            raise HTTPException(status_code=404, detail=f"Champion '{champion}' not found")

        champion_items = ml_engine.item_builds[champion]

        # Handle both formats: dict with 'popular_items'/'builds' keys, or list directly
        if isinstance(champion_items, dict):
            # Dict format - extract popular_items and builds
            popular_items = []
            for item_id, stats in champion_items.get('popular_items', {}).items():
                if stats.get('count', 0) >= 3:  # Min 3 games (reduced from 10)
                    popular_items.append({
                        'item_id': stats.get('item_id', item_id),
                        'games': stats.get('count', 0),
                        'wins': stats.get('wins', 0),
                        'win_rate': stats.get('wins', 0) / stats.get('count', 1) if stats.get('count', 0) > 0 else 0
                    })

            popular_items.sort(key=lambda x: x['win_rate'], reverse=True)
            recommended_items = popular_items[:request.top_n]

            # Get popular builds
            builds = []
            for build_key, stats in champion_items.get('builds', {}).items():
                if stats.get('count', 0) >= 2:  # Min 2 games (reduced from 5)
                    builds.append({
                        'items': stats.get('items', []),
                        'games': stats.get('count', 0),
                        'wins': stats.get('wins', 0),
                        'win_rate': stats.get('win_rate', 0.0)
                    })

            builds.sort(key=lambda x: x['win_rate'], reverse=True)
            popular_builds = builds[:10]  # Show top 10 builds instead of 5
        elif isinstance(champion_items, list):
            # List format - convert to expected format
            recommended_items = []
            popular_builds = []

            # Extract items from builds in list format
            for build_item in champion_items:
                if isinstance(build_item, dict):
                    items = build_item.get('items', [])
                    games = build_item.get('games', build_item.get('count', 0))
                    wins = build_item.get('wins', 0)

                    if games >= 2:
                        popular_builds.append({
                            'items': items,
                            'games': games,
                            'wins': wins,
                            'win_rate': wins / games if games > 0 else 0.0
                        })

            popular_builds.sort(key=lambda x: x['win_rate'], reverse=True)
            popular_builds = popular_builds[:10]
            recommended_items = []  # Can't extract individual items from list format easily
        else:
            recommended_items = []
            popular_builds = []

        return ItemRecommendationResponse(
            champion=champion,
            recommended_items=recommended_items,
            popular_builds=popular_builds
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching item recommendations: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch item recommendations. Please try again later."
        )


@router.post("/item-recommendations-intelligent")
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
    if not ml_engine.item_recommender:
        raise HTTPException(status_code=503, detail="Item Recommender not loaded")

    try:
        result = ml_engine.item_recommender.recommend_items_for_matchup(
            champion=request.champion,
            enemy_team=request.enemy_team,
            top_n=request.top_n
        )

        return result

    except ValueError as e:
        # User input errors (e.g., unknown champion)
        logger.warning(f"Invalid input for intelligent item recommendations: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid request: {str(e)}")
    except Exception as e:
        logger.error(f"Error fetching intelligent item recommendations: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to generate intelligent item recommendations. Please try again later."
        )


@router.post("/draft/dynamic-build")
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
    if not ml_engine.build_generator:
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
        build_path = ml_engine.build_generator.generate_build_path(
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

    except ValueError as e:
        # User input errors
        logger.warning(f"Invalid input for dynamic build generation: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid request: {str(e)}")
    except Exception as e:
        logger.error(f"Error generating dynamic build: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to generate dynamic build. Please try again later."
        )
