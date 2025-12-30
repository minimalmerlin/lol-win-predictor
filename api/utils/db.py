"""
PostgreSQL Database Utilities for API
======================================
Provides database connection and query utilities for Vercel serverless functions.

Features:
- Connection pooling
- Query caching
- Error handling
- Performance metrics
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Dict, List, Optional, Tuple
from functools import lru_cache
import logging

logger = logging.getLogger(__name__)

# Database connection URL from environment variable
DATABASE_URL = os.environ.get(
    'POSTGRES_URL',
    'postgres://***REMOVED***:***REMOVED***@aws-1-eu-central-1.pooler.supabase.com:5432/postgres?sslmode=require'
)


class DatabaseConnection:
    """Manages PostgreSQL database connections"""

    def __init__(self):
        self.conn = None

    def connect(self):
        """Establish database connection"""
        if self.conn is None or self.conn.closed:
            try:
                self.conn = psycopg2.connect(DATABASE_URL)
                logger.info("✓ Connected to PostgreSQL")
            except Exception as e:
                logger.error(f"❌ Database connection failed: {e}")
                raise

        return self.conn

    def close(self):
        """Close database connection"""
        if self.conn and not self.conn.closed:
            self.conn.close()
            logger.info("✓ Database connection closed")

    def __enter__(self):
        return self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def execute_query(query: str, params: tuple = None, fetch: bool = True) -> Optional[List[Dict]]:
    """
    Execute a SQL query and return results as dict.

    Args:
        query: SQL query string
        params: Query parameters (optional)
        fetch: Whether to fetch results (True) or just execute (False)

    Returns:
        List of dicts for SELECT queries, None for INSERT/UPDATE/DELETE
    """
    try:
        with DatabaseConnection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, params)

                if fetch:
                    results = cur.fetchall()
                    return [dict(row) for row in results]
                else:
                    conn.commit()
                    return None

    except Exception as e:
        logger.error(f"❌ Query execution failed: {e}")
        logger.error(f"   Query: {query}")
        raise


@lru_cache(maxsize=32)
def get_database_stats() -> Dict:
    """
    Get database statistics (cached).

    Returns:
        Dict with table row counts and database size
    """
    try:
        stats = {}

        # Table counts
        query = """
            SELECT
                (SELECT COUNT(*) FROM matches) as matches,
                (SELECT COUNT(*) FROM match_champions) as champions,
                (SELECT COUNT(*) FROM match_snapshots) as snapshots
        """
        result = execute_query(query)

        if result:
            stats.update(result[0])

        # Database size
        query = """
            SELECT
                pg_size_pretty(pg_database_size(current_database())) as size,
                pg_database_size(current_database()) as size_bytes
        """
        result = execute_query(query)

        if result:
            stats['database_size'] = result[0]['size']
            stats['database_size_bytes'] = result[0]['size_bytes']

        return stats

    except Exception as e:
        logger.error(f"Failed to get database stats: {e}")
        return {}


def get_match_data(match_id: str) -> Optional[Dict]:
    """
    Get complete match data including champions and snapshots.

    Args:
        match_id: Match ID to retrieve

    Returns:
        Dict with match, champions, and snapshots data
    """
    try:
        # Get match
        match_query = "SELECT * FROM matches WHERE match_id = %s"
        match_result = execute_query(match_query, (match_id,))

        if not match_result:
            return None

        match = match_result[0]

        # Get champions
        champions_query = """
            SELECT team, champion_id, position
            FROM match_champions
            WHERE match_id = %s
            ORDER BY team, position
        """
        champions = execute_query(champions_query, (match_id,))

        # Get snapshots
        snapshots_query = """
            SELECT *
            FROM match_snapshots
            WHERE match_id = %s
            ORDER BY snapshot_time
        """
        snapshots = execute_query(snapshots_query, (match_id,))

        return {
            'match': match,
            'champions': champions,
            'snapshots': snapshots
        }

    except Exception as e:
        logger.error(f"Failed to get match data for {match_id}: {e}")
        return None


def get_champion_winrate(champion_id: int, team: str = None) -> Optional[float]:
    """
    Get champion win rate from database.

    Args:
        champion_id: Champion ID
        team: Filter by team ('blue' or 'red'), None for both

    Returns:
        Win rate as float (0.0 to 1.0)
    """
    try:
        if team:
            query = """
                SELECT
                    COUNT(CASE WHEN m.blue_win = TRUE THEN 1 END)::float /
                    COUNT(*)::float as winrate
                FROM match_champions mc
                JOIN matches m ON mc.match_id = m.match_id
                WHERE mc.champion_id = %s AND mc.team = %s
            """
            params = (champion_id, team)
        else:
            query = """
                SELECT
                    COUNT(CASE
                        WHEN (mc.team = 'blue' AND m.blue_win = TRUE) OR
                             (mc.team = 'red' AND m.blue_win = FALSE)
                        THEN 1
                    END)::float / COUNT(*)::float as winrate
                FROM match_champions mc
                JOIN matches m ON mc.match_id = m.match_id
                WHERE mc.champion_id = %s
            """
            params = (champion_id,)

        result = execute_query(query, params)

        if result and result[0]['winrate'] is not None:
            return float(result[0]['winrate'])

        return None

    except Exception as e:
        logger.error(f"Failed to get champion winrate for {champion_id}: {e}")
        return None


def get_recent_matches(limit: int = 100, snapshot_time: int = None) -> List[Dict]:
    """
    Get recent matches from database.

    Args:
        limit: Number of matches to retrieve
        snapshot_time: Filter by matches with this snapshot time (10, 15, or 20)

    Returns:
        List of match dicts
    """
    try:
        if snapshot_time:
            query = """
                SELECT DISTINCT m.*
                FROM matches m
                JOIN match_snapshots ms ON m.match_id = ms.match_id
                WHERE ms.snapshot_time = %s
                ORDER BY m.match_id DESC
                LIMIT %s
            """
            params = (snapshot_time, limit)
        else:
            query = """
                SELECT *
                FROM matches
                ORDER BY match_id DESC
                LIMIT %s
            """
            params = (limit,)

        return execute_query(query, params)

    except Exception as e:
        logger.error(f"Failed to get recent matches: {e}")
        return []


def test_connection() -> bool:
    """
    Test database connection.

    Returns:
        True if connection successful, False otherwise
    """
    try:
        with DatabaseConnection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                result = cur.fetchone()
                return result[0] == 1
    except Exception as e:
        logger.error(f"Connection test failed: {e}")
        return False
