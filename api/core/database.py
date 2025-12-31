"""
Database Connection Module
Provides PostgreSQL connection to Supabase
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional, Dict, List
from contextlib import contextmanager

from api.core.logging import logger


# Database Configuration
# Priority: POSTGRES_URL (Vercel) > SUPABASE_URL > DATABASE_URL
SUPABASE_URL = os.getenv("POSTGRES_URL") or os.getenv("SUPABASE_URL") or os.getenv("DATABASE_URL")

# CRITICAL: Vercel's POSTGRES_URL uses postgres:// but SQLAlchemy needs postgresql://
if SUPABASE_URL and SUPABASE_URL.startswith("postgres://"):
    SUPABASE_URL = SUPABASE_URL.replace("postgres://", "postgresql://", 1)
    logger.info("✓ Converted postgres:// to postgresql:// for SQLAlchemy compatibility")

if not SUPABASE_URL:
    logger.warning("⚠️  Database URL not set - database features will be disabled")


def get_db_connection():
    """
    Get PostgreSQL connection to Supabase

    Returns:
        psycopg2 connection object

    Raises:
        RuntimeError: If database URL not configured
        psycopg2.Error: If connection fails
    """
    if not SUPABASE_URL:
        raise RuntimeError(
            "Database not configured. Set SUPABASE_URL or POSTGRES_URL environment variable."
        )

    try:
        conn = psycopg2.connect(
            SUPABASE_URL,
            cursor_factory=RealDictCursor  # Returns dicts instead of tuples
        )
        return conn
    except psycopg2.Error as e:
        logger.error(f"❌ Database connection failed: {e}")
        raise RuntimeError(f"Failed to connect to database: {e}")


@contextmanager
def get_db_cursor():
    """
    Context manager for database cursor

    Usage:
        with get_db_cursor() as cur:
            cur.execute("SELECT * FROM matches")
            rows = cur.fetchall()
    """
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        yield cur
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()


# ============================================================================
# CHAMPION STATS QUERIES
# ============================================================================

def get_champion_stats() -> Dict[str, Dict]:
    """
    Get champion statistics from database

    Returns:
        Dict mapping champion_id to stats:
        {
            "157": {  # Yasuo
                "games": 1234,
                "wins": 678,
                "losses": 556,
                "win_rate": 0.549,
                "roles": {"mid": 800, "top": 434}
            }
        }
    """
    with get_db_cursor() as cur:
        # Query aggregated champion stats
        cur.execute("""
            SELECT
                mc.champion_id,
                COUNT(*) as games,
                SUM(CASE WHEN m.blue_win AND mc.team = 'blue' THEN 1
                         WHEN NOT m.blue_win AND mc.team = 'red' THEN 1
                         ELSE 0 END) as wins,
                COUNT(*) - SUM(CASE WHEN m.blue_win AND mc.team = 'blue' THEN 1
                                     WHEN NOT m.blue_win AND mc.team = 'red' THEN 1
                                     ELSE 0 END) as losses
            FROM match_champions mc
            JOIN matches m ON mc.match_id = m.match_id
            GROUP BY mc.champion_id
            HAVING COUNT(*) >= 10  -- Min 10 games
            ORDER BY COUNT(*) DESC
        """)

        rows = cur.fetchall()

        # Format as dict
        stats = {}
        for row in rows:
            champ_id = str(row['champion_id'])
            games = row['games']
            wins = row['wins']
            losses = row['losses']

            stats[champ_id] = {
                'games': games,
                'wins': wins,
                'losses': losses,
                'win_rate': round(wins / games, 4) if games > 0 else 0.0,
                'roles': {}  # TODO: Implement role detection
            }

        logger.info(f"✓ Loaded champion stats for {len(stats)} champions from DB")
        return stats


def get_champion_winrate(champion_id: int) -> float:
    """Get win rate for a specific champion"""
    with get_db_cursor() as cur:
        cur.execute("""
            SELECT
                COUNT(*) as games,
                SUM(CASE WHEN m.blue_win AND mc.team = 'blue' THEN 1
                         WHEN NOT m.blue_win AND mc.team = 'red' THEN 1
                         ELSE 0 END) as wins
            FROM match_champions mc
            JOIN matches m ON mc.match_id = m.match_id
            WHERE mc.champion_id = %s
        """, (champion_id,))

        row = cur.fetchone()
        if row and row['games'] > 0:
            return round(row['wins'] / row['games'], 4)
        return 0.50  # Default 50% if no data


# ============================================================================
# ITEM BUILD QUERIES
# ============================================================================

def get_item_builds() -> Dict[str, Dict]:
    """
    Get item builds from database

    Note: This requires a match_items table (not yet implemented in schema).
    For now, returns empty dict.

    TODO: Implement match_items table and populate from match data
    """
    logger.warning("⚠️  Item builds from DB not yet implemented (requires match_items table)")
    return {}


def get_best_teammates() -> Dict[str, List]:
    """
    Get best teammate synergies from database

    Returns:
        Dict mapping champion_id to list of synergistic champions:
        {
            "157": [  # Yasuo
                {"champion_id": 64, "synergy_score": 0.65, "games": 123},
                ...
            ]
        }
    """
    with get_db_cursor() as cur:
        # Query champion pairs on same team with high win rate
        cur.execute("""
            WITH team_pairs AS (
                SELECT
                    mc1.champion_id as champ1,
                    mc2.champion_id as champ2,
                    mc1.team,
                    m.blue_win,
                    COUNT(*) as games
                FROM match_champions mc1
                JOIN match_champions mc2
                    ON mc1.match_id = mc2.match_id
                    AND mc1.team = mc2.team
                    AND mc1.champion_id < mc2.champion_id
                JOIN matches m ON mc1.match_id = m.match_id
                GROUP BY mc1.champion_id, mc2.champion_id, mc1.team, m.blue_win
                HAVING COUNT(*) >= 5  -- Min 5 games together
            )
            SELECT
                champ1,
                champ2,
                SUM(games) as total_games,
                SUM(CASE WHEN (blue_win AND team = 'blue') OR (NOT blue_win AND team = 'red')
                    THEN games ELSE 0 END)::FLOAT / SUM(games) as win_rate
            FROM team_pairs
            GROUP BY champ1, champ2
            HAVING SUM(games) >= 10
            ORDER BY win_rate DESC
            LIMIT 1000  -- Top 1000 synergies
        """)

        rows = cur.fetchall()

        # Build synergy dict
        synergies = {}
        for row in rows:
            champ1 = str(row['champ1'])
            champ2 = str(row['champ2'])

            # Add to both champions' lists
            for (c1, c2) in [(champ1, champ2), (champ2, champ1)]:
                if c1 not in synergies:
                    synergies[c1] = []

                synergies[c1].append({
                    'champion_id': int(c2),
                    'synergy_score': round(row['win_rate'], 4),
                    'games': row['total_games']
                })

        # Sort each champion's synergies by score
        for champ_id in synergies:
            synergies[champ_id].sort(key=lambda x: x['synergy_score'], reverse=True)
            synergies[champ_id] = synergies[champ_id][:10]  # Top 10 per champion

        logger.info(f"✓ Loaded teammate synergies for {len(synergies)} champions from DB")
        return synergies


# ============================================================================
# MODEL PERFORMANCE QUERIES
# ============================================================================

def get_model_performance(model_name: str) -> Optional[Dict]:
    """
    Get model performance metrics from database

    Since we don't have a dedicated model_performance table yet,
    we derive metrics from actual match data in the database.

    Args:
        model_name: Name of the model ('game_state', 'champion_matchup', etc.)

    Returns:
        Dict with performance metrics or None if not available
    """
    with get_db_cursor() as cur:
        # Get total match count from database
        cur.execute("SELECT COUNT(*) as count FROM matches")
        match_count = cur.fetchone()['count']

        # Get total snapshot count
        cur.execute("SELECT COUNT(*) as count FROM match_snapshots")
        snapshot_count = cur.fetchone()['count']

        # Return database-derived metrics
        # Model-specific accuracy should come from model metadata (pkl files)
        return {
            'matches_count': match_count,
            'snapshot_count': snapshot_count,
            'timestamp': '2025-12-30',  # TODO: Get from model metadata
            'data_source': 'PostgreSQL (Supabase)'
        }


def get_database_stats() -> Dict:
    """
    Get comprehensive database statistics

    Returns:
        Dict with matches, champions, snapshots, and size info
    """
    with get_db_cursor() as cur:
        # Get match count
        cur.execute("SELECT COUNT(*) as count FROM matches")
        match_count = cur.fetchone()['count']

        # Get unique champion count
        cur.execute("SELECT COUNT(DISTINCT champion_id) as count FROM match_champions")
        champion_count = cur.fetchone()['count']

        # Get snapshot count
        cur.execute("SELECT COUNT(*) as count FROM match_snapshots")
        snapshot_count = cur.fetchone()['count']

        # Get database size (PostgreSQL specific query)
        try:
            cur.execute("SELECT pg_database_size(current_database()) as size")
            db_size_bytes = cur.fetchone()['size']
            db_size_mb = round(db_size_bytes / (1024 * 1024), 2)
        except Exception as e:
            logger.warning(f"Could not get database size: {e}")
            db_size_mb = 0

        return {
            'matches': match_count,
            'champions': champion_count,
            'snapshots': snapshot_count,
            'size': f"{db_size_mb} MB",
            'connection': 'healthy'
        }


# ============================================================================
# HEALTH CHECK
# ============================================================================

def check_db_health() -> Dict:
    """Check database connection and get stats"""
    try:
        with get_db_cursor() as cur:
            # Get match count
            cur.execute("SELECT COUNT(*) as count FROM matches")
            match_count = cur.fetchone()['count']

            # Get champion count
            cur.execute("SELECT COUNT(DISTINCT champion_id) as count FROM match_champions")
            champion_count = cur.fetchone()['count']

            # Get snapshot count
            cur.execute("SELECT COUNT(*) as count FROM match_snapshots")
            snapshot_count = cur.fetchone()['count']

            return {
                'status': 'healthy',
                'matches': match_count,
                'champions': champion_count,
                'snapshots': snapshot_count,
                'connection': 'active'
            }
    except Exception as e:
        logger.error(f"❌ Database health check failed: {e}")
        return {
            'status': 'unhealthy',
            'error': str(e),
            'connection': 'failed'
        }
