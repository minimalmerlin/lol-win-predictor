"""
CSV → PostgreSQL Migration Script
==================================

Migrates League of Legends match data from CSV to PostgreSQL (Supabase).

Features:
- Automatic deduplication (match_id PRIMARY KEY)
- Normalizes champions into separate table
- Extracts timeline snapshots (10min, 15min, 20min)
- Batch processing for performance
- Progress tracking
- Error handling with rollback

Usage:
    python migrate_csv_to_postgres.py

Author: Claude + Merlin
Date: 2025-12-29
"""

import pandas as pd
import psycopg2
from psycopg2.extras import execute_batch
import os
from pathlib import Path

# ========================================
# CONFIGURATION
# ========================================

# Database Connection (Direct, not pooled)
DATABASE_URL = os.environ.get('POSTGRES_URL')
if not DATABASE_URL:
    raise ValueError("POSTGRES_URL environment variable is required. Please set it in .env file.")

# CSV Input File
CSV_FILE = "data/training_data_with_timeline.csv"

# Batch size for bulk inserts
BATCH_SIZE = 100

# ========================================
# HELPER FUNCTIONS
# ========================================

def connect_db():
    """Connect to PostgreSQL database"""
    return psycopg2.connect(DATABASE_URL)


def migrate_match(conn, row):
    """
    Insert a single match into matches table.
    Uses ON CONFLICT DO NOTHING for automatic deduplication.
    """
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO matches (match_id, game_duration, blue_win)
            VALUES (%s, %s, %s)
            ON CONFLICT (match_id) DO NOTHING
        """, (
            row['match_id'],
            float(row['game_duration']),
            bool(row['blue_win'])
        ))


def migrate_champions(conn, row):
    """
    Insert 10 champion picks (5 blue + 5 red) for a match.
    Uses ON CONFLICT DO NOTHING to handle duplicates.
    """
    champions_data = []

    # Blue Team (positions 1-5)
    for i in range(1, 6):
        col = f'blue_champ_{i}'
        if col in row and pd.notna(row[col]):
            champions_data.append((
                row['match_id'],
                'blue',
                int(row[col]),
                i
            ))

    # Red Team (positions 1-5)
    for i in range(1, 6):
        col = f'red_champ_{i}'
        if col in row and pd.notna(row[col]):
            champions_data.append((
                row['match_id'],
                'red',
                int(row[col]),
                i
            ))

    if champions_data:
        with conn.cursor() as cur:
            execute_batch(cur, """
                INSERT INTO match_champions (match_id, team, champion_id, position)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (match_id, team, position) DO NOTHING
            """, champions_data, page_size=len(champions_data))


def migrate_snapshots(conn, row):
    """
    Insert timeline snapshots (10min, 15min, 20min) for a match.
    Only inserts snapshots that exist in the data (short games might not have all).
    """
    snapshots_data = []

    for snapshot_time in [10, 15, 20]:
        prefix = f't{snapshot_time}_'

        # Check if this snapshot exists in the data
        gold_col = f'{prefix}blue_gold'
        if gold_col not in row or pd.isna(row[gold_col]):
            continue  # Skip this snapshot (game was too short)

        try:
            snapshot = (
                row['match_id'],
                snapshot_time,
                # Gold
                int(row[f'{prefix}blue_gold']),
                int(row[f'{prefix}red_gold']),
                int(row[f'{prefix}gold_diff']),
                # XP
                int(row[f'{prefix}blue_xp']),
                int(row[f'{prefix}red_xp']),
                int(row[f'{prefix}xp_diff']),
                # Level
                int(row[f'{prefix}blue_level']),
                int(row[f'{prefix}red_level']),
                # CS
                int(row[f'{prefix}blue_cs']),
                int(row[f'{prefix}red_cs']),
                # Objectives
                int(row.get(f'{prefix}blue_dragons', 0)),
                int(row.get(f'{prefix}red_dragons', 0)),
                int(row.get(f'{prefix}blue_barons', 0)),
                int(row.get(f'{prefix}red_barons', 0)),
                int(row.get(f'{prefix}blue_towers', 0)),
                int(row.get(f'{prefix}red_towers', 0)),
                # Kills
                int(row[f'{prefix}blue_kills']),
                int(row[f'{prefix}red_kills']),
                int(row[f'{prefix}kill_diff'])
            )
            snapshots_data.append(snapshot)
        except (KeyError, ValueError) as e:
            print(f"⚠️  Skipping snapshot {snapshot_time}min for {row['match_id']}: {e}")
            continue

    if snapshots_data:
        with conn.cursor() as cur:
            execute_batch(cur, """
                INSERT INTO match_snapshots (
                    match_id, snapshot_time,
                    blue_gold, red_gold, gold_diff,
                    blue_xp, red_xp, xp_diff,
                    blue_level, red_level,
                    blue_cs, red_cs,
                    blue_dragons, red_dragons,
                    blue_barons, red_barons,
                    blue_towers, red_towers,
                    blue_kills, red_kills, kill_diff
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (match_id, snapshot_time) DO NOTHING
            """, snapshots_data, page_size=len(snapshots_data))


# ========================================
# MAIN MIGRATION
# ========================================

def main():
    print("=" * 80)
    print("CSV → PostgreSQL MIGRATION")
    print("=" * 80)

    # Check if CSV exists
    csv_path = Path(CSV_FILE)
    if not csv_path.exists():
        print(f"❌ Error: CSV file not found: {CSV_FILE}")
        return

    # Load CSV
    print(f"\n📁 Loading CSV: {CSV_FILE}")
    try:
        df = pd.read_csv(csv_path)
        print(f"✅ Loaded {len(df)} matches from CSV")
        print(f"   Columns: {len(df.columns)}")
    except Exception as e:
        print(f"❌ Error loading CSV: {e}")
        return

    # Connect to Database
    print(f"\n🔌 Connecting to PostgreSQL...")
    try:
        conn = connect_db()
        conn.autocommit = False  # Use transactions for safety
        print("✅ Connected to Supabase PostgreSQL")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return

    # Migration Statistics
    stats = {
        'matches_inserted': 0,
        'champions_inserted': 0,
        'snapshots_inserted': 0,
        'errors': 0
    }

    # Migrate Data
    print(f"\n📊 Migrating {len(df)} matches...")
    print("=" * 80)

    try:
        for idx, row in df.iterrows():
            try:
                # 1. Insert Match
                migrate_match(conn, row)
                stats['matches_inserted'] += 1

                # 2. Insert Champions (10 per match)
                migrate_champions(conn, row)
                stats['champions_inserted'] += 10

                # 3. Insert Snapshots (1-3 per match)
                migrate_snapshots(conn, row)
                stats['snapshots_inserted'] += 3  # Approximate

                # Commit every BATCH_SIZE matches
                if (idx + 1) % BATCH_SIZE == 0:
                    conn.commit()
                    print(f"✓ Migrated {idx + 1}/{len(df)} matches ({(idx+1)/len(df)*100:.1f}%)")

            except Exception as e:
                stats['errors'] += 1
                print(f"❌ Error migrating match {row.get('match_id', 'unknown')}: {e}")
                conn.rollback()
                continue

        # Final commit
        conn.commit()
        print(f"✓ Migrated {len(df)}/{len(df)} matches (100.0%)")

    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        conn.rollback()
        return
    finally:
        conn.close()

    # Verify Migration
    print("\n" + "=" * 80)
    print("📊 VERIFYING MIGRATION")
    print("=" * 80)

    try:
        conn = connect_db()
        cur = conn.cursor()

        # Count rows in each table
        cur.execute("SELECT COUNT(*) FROM matches")
        matches_count = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM match_champions")
        champions_count = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM match_snapshots")
        snapshots_count = cur.fetchone()[0]

        cur.close()
        conn.close()

        print(f"\n✅ Database Row Counts:")
        print(f"   matches: {matches_count}")
        print(f"   match_champions: {champions_count}")
        print(f"   match_snapshots: {snapshots_count}")

        print(f"\n📈 Migration Statistics:")
        print(f"   Matches processed: {stats['matches_inserted']}")
        print(f"   Champions processed: ~{stats['champions_inserted']}")
        print(f"   Snapshots processed: ~{stats['snapshots_inserted']}")
        print(f"   Errors: {stats['errors']}")

        # Validation
        expected_champions = matches_count * 10
        expected_snapshots_min = matches_count * 1  # At least 10min snapshot
        expected_snapshots_max = matches_count * 3  # All 3 snapshots

        print(f"\n🔍 Data Quality Checks:")
        if champions_count >= expected_champions * 0.9:
            print(f"   ✅ Champions: {champions_count}/{expected_champions} expected (~{champions_count/expected_champions*100:.0f}%)")
        else:
            print(f"   ⚠️  Champions: {champions_count}/{expected_champions} expected (LOW!)")

        if expected_snapshots_min <= snapshots_count <= expected_snapshots_max:
            print(f"   ✅ Snapshots: {snapshots_count} (range: {expected_snapshots_min}-{expected_snapshots_max})")
        else:
            print(f"   ⚠️  Snapshots: {snapshots_count} (expected: {expected_snapshots_min}-{expected_snapshots_max})")

    except Exception as e:
        print(f"❌ Verification failed: {e}")

    print("\n" + "=" * 80)
    print("✅ MIGRATION COMPLETE!")
    print("=" * 80)


if __name__ == "__main__":
    main()
