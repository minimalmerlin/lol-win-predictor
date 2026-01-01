#!/usr/bin/env python3
"""
Champion Data Migration Script
Migrates champion statistics from local JSON files to PostgreSQL (Supabase)
"""

import json
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

# Override with NON_POOLING URL for direct connection (migration needs direct access)
postgres_url_non_pooling = os.getenv("POSTGRES_URL_NON_POOLING")
if postgres_url_non_pooling:
    # Convert postgres:// to postgresql:// for SQLAlchemy
    if postgres_url_non_pooling.startswith("postgres://"):
        postgres_url_non_pooling = postgres_url_non_pooling.replace("postgres://", "postgresql://", 1)
    os.environ["POSTGRES_URL"] = postgres_url_non_pooling

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.core.database import get_db_connection, logger

def load_champion_stats():
    """Load champion stats from JSON file"""
    data_file = Path(__file__).parent.parent / "data" / "champion_data" / "champion_stats.json"

    if not data_file.exists():
        logger.error(f"Champion stats file not found: {data_file}")
        return None

    with open(data_file, 'r') as f:
        return json.load(f)

def migrate_champion_stats():
    """Migrate champion statistics to PostgreSQL"""
    logger.info("🚀 Starting champion data migration...")

    # Load data
    champion_stats = load_champion_stats()
    if not champion_stats:
        logger.error("❌ Failed to load champion stats")
        return False

    logger.info(f"✓ Loaded {len(champion_stats)} champions from JSON")

    # Get database connection
    conn = get_db_connection()
    if not conn:
        logger.error("❌ Failed to connect to database")
        return False

    try:
        cursor = conn.cursor()

        # Create table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS champion_stats (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) UNIQUE NOT NULL,
                games INTEGER NOT NULL,
                wins INTEGER NOT NULL,
                losses INTEGER NOT NULL,
                win_rate FLOAT NOT NULL,
                picks INTEGER NOT NULL,
                bans INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        logger.info("✓ Table champion_stats ready")

        # Insert/Update champion stats
        inserted = 0
        updated = 0

        for champion_name, stats in champion_stats.items():
            try:
                # Check if exists first
                cursor.execute("SELECT id FROM champion_stats WHERE name = %s", (champion_name,))
                exists = cursor.fetchone()

                if exists:
                    # Update existing
                    cursor.execute("""
                        UPDATE champion_stats
                        SET games = %s, wins = %s, losses = %s, win_rate = %s,
                            picks = %s, bans = %s, updated_at = CURRENT_TIMESTAMP
                        WHERE name = %s
                    """, (
                        stats['games'], stats['wins'], stats['losses'],
                        stats['win_rate'], stats['picks'], stats['bans'],
                        champion_name
                    ))
                    updated += 1
                else:
                    # Insert new
                    cursor.execute("""
                        INSERT INTO champion_stats (name, games, wins, losses, win_rate, picks, bans)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (
                        champion_name,
                        stats['games'],
                        stats['wins'],
                        stats['losses'],
                        stats['win_rate'],
                        stats['picks'],
                        stats['bans']
                    ))
                    inserted += 1

            except Exception as e:
                logger.warning(f"⚠️  Error processing {champion_name}: {e}")
                continue

        conn.commit()

        logger.info(f"✅ Migration complete!")
        logger.info(f"   • Inserted: {inserted} champions")
        logger.info(f"   • Updated: {updated} champions")
        logger.info(f"   • Total: {inserted + updated} champions")

        # Verify
        cursor.execute("SELECT COUNT(*) as total FROM champion_stats")
        result = cursor.fetchone()
        total = result['total'] if result else 0
        logger.info(f"✓ Database now contains {total} champions")

        cursor.close()
        conn.close()

        return True

    except Exception as e:
        logger.error(f"❌ Migration failed: {e}")
        if conn:
            conn.rollback()
            conn.close()
        raise  # Re-raise to see the real error

if __name__ == "__main__":
    success = migrate_champion_stats()
    sys.exit(0 if success else 1)
