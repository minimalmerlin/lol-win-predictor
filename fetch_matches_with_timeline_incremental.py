"""
Enhanced Match Data Fetcher with Timeline (INCREMENTAL SAVING)
===============================================================

IMPROVEMENTS:
- ✅ Incremental CSV saving (every 10 matches)
- ✅ Progress tracking with timestamps
- ✅ Resume capability (skips already processed matches)
- ✅ Error recovery (continues on API errors)
- ✅ Real-time progress output

Fetches match data from Riot API including:
- Champion picks (Draft Phase)
- Items (End Game)
- Timeline snapshots at 10min, 15min, 20min (Game State)

Timeline Features per Snapshot:
- Gold (total, current, gold per second)
- XP and Level
- CS (minions killed, jungle minions)
- Objectives (Dragons, Barons, Towers destroyed)
- Kills, Deaths, Assists

Author: Victory AI System
Date: 2025-12-29
Version: 2.0 (Incremental)
"""

import requests
import pandas as pd
import time
import os
import json
from dotenv import load_dotenv
from typing import Dict, List, Optional, Set
from datetime import datetime
from pathlib import Path

# Load environment variables
load_dotenv()

# ================= CONFIGURATION =================
API_KEY = os.getenv("RIOT_API_KEY")
if not API_KEY:
    raise ValueError("RIOT_API_KEY not found. Create .env file with your API key.")

REGION_ROUTING = "europe"
START_PLAYER_NAME = "Agurin"
START_PLAYER_TAG = "EUW"
TARGET_MATCHES = 10000  # Increased from 5000 for better ML training data
OUTPUT_FILE = "data/training_data_with_timeline.csv"
PROGRESS_FILE = "data/crawler_state/timeline_progress.json"
SAVE_INTERVAL = 10  # Save every 10 matches

# Timeline snapshot times (in minutes)
SNAPSHOT_TIMES = [10, 15, 20]
# =================================================

headers = {"X-Riot-Token": API_KEY}


def load_progress() -> Dict:
    """Load progress from previous runs"""
    progress_path = Path(PROGRESS_FILE)

    if progress_path.exists():
        with open(progress_path, 'r') as f:
            return json.load(f)

    return {
        'seen_matches': [],
        'seen_puuids': [],
        'total_matches_collected': 0,
        'last_updated': None,
        'session_start': datetime.now().isoformat()
    }


def save_progress(progress: Dict):
    """Save current progress"""
    progress_path = Path(PROGRESS_FILE)
    progress_path.parent.mkdir(parents=True, exist_ok=True)

    progress['last_updated'] = datetime.now().isoformat()

    with open(progress_path, 'w') as f:
        json.dump(progress, f, indent=2)


def load_existing_data() -> pd.DataFrame:
    """Load existing CSV data if available"""
    output_path = Path(OUTPUT_FILE)

    if output_path.exists():
        print(f"  ✓ Existing data found: {output_path}")
        df = pd.read_csv(output_path)
        print(f"  ✓ Loaded {len(df)} existing matches")
        return df

    return pd.DataFrame()


def append_to_csv(new_matches: List[Dict], output_file: str):
    """Append new matches to CSV (incremental saving)"""
    output_path = Path(output_file)

    if not new_matches:
        return

    new_df = pd.DataFrame(new_matches)

    if output_path.exists():
        # Append to existing file
        existing_df = pd.read_csv(output_path)
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
        combined_df.to_csv(output_path, index=False)
        print(f"  ✓ Appended {len(new_matches)} matches (Total: {len(combined_df)})")
    else:
        # Create new file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        new_df.to_csv(output_path, index=False)
        print(f"  ✓ Created CSV with {len(new_matches)} matches")


def get_puuid(game_name: str, tag_line: str) -> Optional[str]:
    """Get PUUID from Riot ID"""
    url = f"https://{REGION_ROUTING}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    resp = requests.get(url, headers=headers)

    if resp.status_code == 200:
        return resp.json()['puuid']

    print(f"❌ Error fetching PUUID ({game_name}#{tag_line}): {resp.status_code}")
    return None


def get_match_ids(puuid: str, count: int = 20) -> List[str]:
    """Get recent ranked match IDs for a player"""
    url = f"https://{REGION_ROUTING}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
    params = {
        'queue': 420,  # Ranked Solo/Duo
        'start': 0,
        'count': count
    }

    resp = requests.get(url, headers=headers, params=params)

    if resp.status_code == 200:
        return resp.json()
    elif resp.status_code == 429:
        print("⚠️  Rate limit! Waiting 10 seconds...")
        time.sleep(10)
        return get_match_ids(puuid, count)

    return []


def get_match_details(match_id: str) -> Optional[Dict]:
    """Get match details"""
    url = f"https://{REGION_ROUTING}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    resp = requests.get(url, headers=headers)

    if resp.status_code == 200:
        return resp.json()
    elif resp.status_code == 429:
        print("⚠️  Rate limit! Waiting 10 seconds...")
        time.sleep(10)
        return get_match_details(match_id)
    elif resp.status_code == 404:
        return None

    return None


def get_match_timeline(match_id: str) -> Optional[Dict]:
    """Get match timeline with frame-by-frame data"""
    url = f"https://{REGION_ROUTING}.api.riotgames.com/lol/match/v5/matches/{match_id}/timeline"
    resp = requests.get(url, headers=headers)

    if resp.status_code == 200:
        return resp.json()
    elif resp.status_code == 429:
        print("⚠️  Rate limit! Waiting 10 seconds...")
        time.sleep(10)
        return get_match_timeline(match_id)
    elif resp.status_code == 404:
        return None

    return None


def extract_snapshot_stats(frame: Dict, team_id: int) -> Dict:
    """
    Extract aggregated team stats from a timeline frame

    Args:
        frame: Timeline frame
        team_id: 100 (blue) or 200 (red)

    Returns:
        Dict with aggregated team stats
    """
    team_stats = {
        'total_gold': 0,
        'total_xp': 0,
        'total_level': 0,
        'total_minions': 0,
        'total_jungle_minions': 0,
        'avg_position_x': 0,
        'avg_position_y': 0,
    }

    participant_count = 0

    for part_id_str, part_data in frame['participantFrames'].items():
        part_id = int(part_id_str)

        # Participants 1-5 are team 100 (blue), 6-10 are team 200 (red)
        participant_team = 100 if part_id <= 5 else 200

        if participant_team == team_id:
            team_stats['total_gold'] += part_data.get('totalGold', 0)
            team_stats['total_xp'] += part_data.get('xp', 0)
            team_stats['total_level'] += part_data.get('level', 0)
            team_stats['total_minions'] += part_data.get('minionsKilled', 0)
            team_stats['total_jungle_minions'] += part_data.get('jungleMinionsKilled', 0)

            pos = part_data.get('position', {})
            team_stats['avg_position_x'] += pos.get('x', 0)
            team_stats['avg_position_y'] += pos.get('y', 0)

            participant_count += 1

    # Average position
    if participant_count > 0:
        team_stats['avg_position_x'] /= participant_count
        team_stats['avg_position_y'] /= participant_count

    return team_stats


def extract_objectives_at_time(frames: List[Dict], target_timestamp: int) -> Dict:
    """
    Extract objectives (dragons, barons, towers) up to a specific time

    Args:
        frames: List of timeline frames
        target_timestamp: Timestamp in milliseconds

    Returns:
        Dict with objective counts per team
    """
    objectives = {
        'blue_dragons': 0,
        'red_dragons': 0,
        'blue_barons': 0,
        'red_barons': 0,
        'blue_towers': 0,
        'red_towers': 0,
        'blue_kills': 0,
        'red_kills': 0
    }

    for frame in frames:
        if frame['timestamp'] > target_timestamp:
            break

        for event in frame.get('events', []):
            event_type = event.get('type')

            # Dragon kills
            if event_type == 'ELITE_MONSTER_KILL' and event.get('monsterType') == 'DRAGON':
                killer_team_id = event.get('killerTeamId')
                if killer_team_id == 100:
                    objectives['blue_dragons'] += 1
                elif killer_team_id == 200:
                    objectives['red_dragons'] += 1

            # Baron kills
            elif event_type == 'ELITE_MONSTER_KILL' and event.get('monsterType') == 'BARON_NASHOR':
                killer_team_id = event.get('killerTeamId')
                if killer_team_id == 100:
                    objectives['blue_barons'] += 1
                elif killer_team_id == 200:
                    objectives['red_barons'] += 1

            # Tower destroys
            elif event_type == 'BUILDING_KILL' and event.get('buildingType') == 'TOWER_BUILDING':
                killer_team_id = event.get('killerTeamId')
                if killer_team_id == 100:
                    objectives['blue_towers'] += 1
                elif killer_team_id == 200:
                    objectives['red_towers'] += 1

            # Champion kills
            elif event_type == 'CHAMPION_KILL':
                killer_id = event.get('killerId', 0)
                if 1 <= killer_id <= 5:
                    objectives['blue_kills'] += 1
                elif 6 <= killer_id <= 10:
                    objectives['red_kills'] += 1

    return objectives


def process_match_with_timeline(match_data: Dict, timeline_data: Dict) -> Optional[Dict]:
    """
    Process match and timeline data to extract features

    Returns:
        Dict with all features for training, or None if invalid
    """
    info = match_data['info']

    # Skip non-ranked or invalid games
    if info.get('queueId') != 420:  # Ranked Solo/Duo
        return None

    # Skip short games (< 15 minutes)
    game_duration_minutes = info['gameDuration'] / 60
    if game_duration_minutes < 15:
        return None

    row = {
        'match_id': match_data['metadata']['matchId'],
        'game_duration': game_duration_minutes
    }

    # Extract champions and win condition
    blue_team = []
    red_team = []

    for p in info['participants']:
        if p['teamId'] == 100:
            blue_team.append(p)
        else:
            red_team.append(p)

    # Who won?
    row['blue_win'] = 1 if blue_team[0]['win'] else 0

    # Champion IDs
    for i, p in enumerate(blue_team):
        row[f'blue_champ_{i+1}'] = p['championId']

    for i, p in enumerate(red_team):
        row[f'red_champ_{i+1}'] = p['championId']

    # Extract items (end game)
    for i, p in enumerate(blue_team):
        for item_idx in range(7):
            row[f'blue_item_{i+1}_{item_idx}'] = p.get(f'item{item_idx}', 0)

    for i, p in enumerate(red_team):
        for item_idx in range(7):
            row[f'red_item_{i+1}_{item_idx}'] = p.get(f'item{item_idx}', 0)

    # Process timeline snapshots
    if timeline_data and 'info' in timeline_data and 'frames' in timeline_data['info']:
        frames = timeline_data['info']['frames']
        frame_interval = timeline_data['info']['frameInterval'] / 1000 / 60  # Convert to minutes

        for snapshot_min in SNAPSHOT_TIMES:
            # Skip if game didn't reach this time
            if game_duration_minutes < snapshot_min:
                continue

            # Find frame closest to snapshot time
            target_frame_idx = int(snapshot_min / frame_interval)

            if target_frame_idx >= len(frames):
                continue

            frame = frames[target_frame_idx]
            target_timestamp = snapshot_min * 60 * 1000  # Convert to milliseconds

            # Extract team stats
            blue_stats = extract_snapshot_stats(frame, 100)
            red_stats = extract_snapshot_stats(frame, 200)

            # Extract objectives
            objectives = extract_objectives_at_time(frames, target_timestamp)

            # Store snapshot features
            prefix = f't{snapshot_min}_'

            # Gold
            row[f'{prefix}blue_gold'] = blue_stats['total_gold']
            row[f'{prefix}red_gold'] = red_stats['total_gold']
            row[f'{prefix}gold_diff'] = blue_stats['total_gold'] - red_stats['total_gold']

            # XP
            row[f'{prefix}blue_xp'] = blue_stats['total_xp']
            row[f'{prefix}red_xp'] = red_stats['total_xp']
            row[f'{prefix}xp_diff'] = blue_stats['total_xp'] - red_stats['total_xp']

            # Level
            row[f'{prefix}blue_level'] = blue_stats['total_level']
            row[f'{prefix}red_level'] = red_stats['total_level']

            # CS
            row[f'{prefix}blue_cs'] = blue_stats['total_minions'] + blue_stats['total_jungle_minions']
            row[f'{prefix}red_cs'] = red_stats['total_minions'] + red_stats['total_jungle_minions']

            # Objectives
            row[f'{prefix}blue_dragons'] = objectives['blue_dragons']
            row[f'{prefix}red_dragons'] = objectives['red_dragons']
            row[f'{prefix}blue_barons'] = objectives['blue_barons']
            row[f'{prefix}red_barons'] = objectives['red_barons']
            row[f'{prefix}blue_towers'] = objectives['blue_towers']
            row[f'{prefix}red_towers'] = objectives['red_towers']
            row[f'{prefix}blue_kills'] = objectives['blue_kills']
            row[f'{prefix}red_kills'] = objectives['red_kills']
            row[f'{prefix}kill_diff'] = objectives['blue_kills'] - objectives['red_kills']

    return row


def main():
    """Main execution with incremental saving"""
    print("=" * 80)
    print("VICTORY AI - TIMELINE DATA FETCHER (INCREMENTAL)")
    print("=" * 80)
    print(f"\nConfiguration:")
    print(f"  Target matches: {TARGET_MATCHES}")
    print(f"  Snapshot times: {SNAPSHOT_TIMES} minutes")
    print(f"  Output file: {OUTPUT_FILE}")
    print(f"  Save interval: Every {SAVE_INTERVAL} matches")

    # Load progress
    print(f"\nLoading progress...")
    progress = load_progress()
    seen_matches = set(progress['seen_matches'])
    seen_puuids = set(progress['seen_puuids'])

    print(f"  ✓ Seen matches: {len(seen_matches)}")
    print(f"  ✓ Seen PUUIDs: {len(seen_puuids)}")

    # Load existing data
    existing_df = load_existing_data()
    total_collected = len(existing_df)

    if total_collected > 0:
        print(f"  ✓ Resuming from {total_collected} matches")

    # Get seed player PUUID
    print(f"\nFetching seed player: {START_PLAYER_NAME}#{START_PLAYER_TAG}")
    seed_puuid = get_puuid(START_PLAYER_NAME, START_PLAYER_TAG)

    if not seed_puuid:
        print("❌ Failed to get seed player PUUID")
        return

    print(f"✓ Seed PUUID: {seed_puuid[:8]}...")

    # Initialize queues
    if seed_puuid not in seen_puuids:
        seen_puuids.add(seed_puuid)

    puuid_queue = [seed_puuid] if not seen_puuids else list(seen_puuids)[:100]

    batch_matches = []
    session_start = datetime.now()

    print(f"\nStarting data collection...")
    print(f"Session started: {session_start.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    while total_collected < TARGET_MATCHES and puuid_queue:
        current_puuid = puuid_queue.pop(0)

        # Get matches for this player
        match_ids = get_match_ids(current_puuid, count=20)

        for match_id in match_ids:
            if match_id in seen_matches:
                continue

            if total_collected >= TARGET_MATCHES:
                break

            seen_matches.add(match_id)

            # Fetch match details
            try:
                match_data = get_match_details(match_id)

                if not match_data:
                    continue

                # Fetch timeline
                timeline_data = get_match_timeline(match_id)

                if not timeline_data:
                    print(f"⚠️  No timeline for {match_id}")
                    continue

                # Process match
                row = process_match_with_timeline(match_data, timeline_data)

                if row:
                    batch_matches.append(row)
                    total_collected += 1

                    # Collect new PUUIDs
                    for puuid in match_data['metadata']['participants']:
                        if puuid not in seen_puuids and len(puuid_queue) < 100:
                            seen_puuids.add(puuid)
                            puuid_queue.append(puuid)

                    # Progress update
                    elapsed = (datetime.now() - session_start).total_seconds()
                    rate = total_collected / elapsed if elapsed > 0 else 0
                    eta_seconds = (TARGET_MATCHES - total_collected) / rate if rate > 0 else 0
                    eta_minutes = eta_seconds / 60

                    print(f"[{datetime.now().strftime('%H:%M:%S')}] "
                          f"✓ {total_collected}/{TARGET_MATCHES} matches "
                          f"({total_collected / TARGET_MATCHES * 100:.1f}%) | "
                          f"Rate: {rate * 60:.1f} matches/min | "
                          f"ETA: {eta_minutes:.1f} min | "
                          f"Queue: {len(puuid_queue)} players")

                    # Save batch every SAVE_INTERVAL matches
                    if len(batch_matches) >= SAVE_INTERVAL:
                        append_to_csv(batch_matches, OUTPUT_FILE)

                        # Update progress
                        progress['seen_matches'] = list(seen_matches)
                        progress['seen_puuids'] = list(seen_puuids)
                        progress['total_matches_collected'] = total_collected
                        save_progress(progress)

                        batch_matches = []

            except Exception as e:
                print(f"❌ Error processing {match_id}: {e}")
                continue

            # Rate limit protection
            time.sleep(0.2)

    # Save remaining matches
    if batch_matches:
        append_to_csv(batch_matches, OUTPUT_FILE)
        progress['seen_matches'] = list(seen_matches)
        progress['seen_puuids'] = list(seen_puuids)
        progress['total_matches_collected'] = total_collected
        save_progress(progress)

    # Final summary
    print("\n" + "=" * 80)
    print(f"✅ DATA COLLECTION COMPLETE!")
    print("=" * 80)

    final_df = pd.read_csv(OUTPUT_FILE)

    print(f"\nFinal Dataset:")
    print(f"  Total matches: {len(final_df)}")
    print(f"  Columns: {len(final_df.columns)}")
    print(f"  Blue wins: {final_df['blue_win'].sum()} ({final_df['blue_win'].mean() * 100:.1f}%)")
    print(f"  Red wins: {len(final_df) - final_df['blue_win'].sum()} ({(1 - final_df['blue_win'].mean()) * 100:.1f}%)")

    session_end = datetime.now()
    duration = (session_end - session_start).total_seconds() / 60

    print(f"\nSession Summary:")
    print(f"  Started: {session_start.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Ended: {session_end.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Duration: {duration:.1f} minutes")
    print(f"  Average rate: {total_collected / duration:.1f} matches/minute")

    print("\n" + "=" * 80)
    print("Ready for Game State Predictor training!")
    print("=" * 80)


if __name__ == "__main__":
    main()
