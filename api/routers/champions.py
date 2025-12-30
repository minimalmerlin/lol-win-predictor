"""
Champion API endpoints
Handles champion stats, search, and details
"""

from fastapi import APIRouter, HTTPException

from api.schemas.champion import ChampionStatsResponse
from api.services.ml_engine import ml_engine
from api.core.logging import logger

router = APIRouter(prefix="/api", tags=["champions"])


@router.get("/champion-stats", response_model=ChampionStatsResponse)
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
    if not ml_engine.champion_stats:
        raise HTTPException(status_code=503, detail="Champion stats not loaded")

    try:
        # Filter and format
        champions_list = []
        for name, stats in ml_engine.champion_stats.items():
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
            total_champions=len(ml_engine.champion_stats)
        )

    except Exception as e:
        logger.error(f"Error fetching champion stats: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch champion statistics. Please try again later."
        )


@router.get("/champions/list")
async def get_champions_list():
    """Get list of all available champions"""
    if not ml_engine.champion_stats:
        raise HTTPException(status_code=503, detail="Champion stats not loaded")

    return {
        "champions": sorted(list(ml_engine.champion_stats.keys())),
        "total": len(ml_engine.champion_stats)
    }


@router.get("/champions/search")
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
    if not ml_engine.item_recommender:
        raise HTTPException(status_code=503, detail="Item Recommender not loaded")

    try:
        results = ml_engine.item_recommender.search_champions(
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
        logger.error(f"Error searching champions: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to search champions. Please try again later."
        )


@router.get("/champions/{champion_name}")
async def get_champion_details(champion_name: str):
    """
    Get detailed information about a specific champion

    Returns:
    - Champion stats
    - Best teammates
    - Item builds
    - Fuzzy match if exact name not found
    """
    if not ml_engine.item_recommender:
        raise HTTPException(status_code=503, detail="Item Recommender not loaded")

    try:
        # Fuzzy match the champion name
        matches = ml_engine.item_recommender.fuzzy_find_champion(champion_name, threshold=0.6)

        if not matches:
            raise HTTPException(
                status_code=404,
                detail=f"Champion '{champion_name}' not found"
            )

        # Use best match
        matched_champion = matches[0][0]
        match_quality = matches[0][1]

        # Get champion stats
        stats = ml_engine.champion_stats.get(matched_champion, {}) if ml_engine.champion_stats else {}

        # Get item builds
        item_builds_data = ml_engine.item_recommender.get_item_builds(
            champion=matched_champion,
            top_n=10
        )

        # Get best teammates
        teammates = ml_engine.best_teammates.get(matched_champion, []) if ml_engine.best_teammates else []

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
        logger.error(f"Error fetching champion details: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch champion details. Please try again later."
        )
