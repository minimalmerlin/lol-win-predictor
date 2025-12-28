"""
Riot API Match Crawler with Item Data
Fetches match data including items (item0-item6) for each participant.
Saves to data/clean_training_data_items.csv
"""

import requests
import time
import csv
import os
from datetime import datetime

# ==================== CONFIGURATION ====================
API_KEY = "YOUR_RIOT_API_KEY_HERE"  # REPLACE WITH YOUR API KEY
REGION = "europe"  # Match-V5 Region (europe, americas, asia, sea)
PLATFORM = "euw1"  # Platform for Summoner-V4 (euw1, na1, kr, etc.)

# Rate limiting: 20 requests per second, 100 requests per 2 minutes
REQUESTS_PER_SECOND = 20
REQUESTS_PER_2_MIN = 100

# Output file
OUTPUT_FILE = "data/clean_training_data_items.csv"
HEADERS = {
    "X-Riot-Token": API_KEY
}

# ==================== RATE LIMITER ====================
class RateLimiter:
    def __init__(self, per_second=20, per_2min=100):
        self.per_second = per_second
        self.per_2min = per_2min
        self.last_request_time = 0
        self.request_times_2min = []

    def wait(self):
        """Wait to respect rate limits"""
        now = time.time()

        # Per-second limit
        time_since_last = now - self.last_request_time
        if time_since_last < 1.0 / self.per_second:
            time.sleep(1.0 / self.per_second - time_since_last)

        # Per-2-minute limit
        self.request_times_2min = [t for t in self.request_times_2min if now - t < 120]
        if len(self.request_times_2min) >= self.per_2min:
            sleep_time = 120 - (now - self.request_times_2min[0])
            if sleep_time > 0:
                print(f"⏳ Rate limit: Sleeping {sleep_time:.1f}s")
                time.sleep(sleep_time)

        self.last_request_time = time.time()
        self.request_times_2min.append(self.last_request_time)

limiter = RateLimiter(REQUESTS_PER_SECOND, REQUESTS_PER_2_MIN)

# ==================== API FUNCTIONS ====================

def get_challenger_summoners(platform=PLATFORM, count=50):
    """Get top Challenger summoner IDs"""
    url = f"https://{platform}.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5"
    limiter.wait()

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            data = response.json()
            summoner_ids = [entry['summonerId'] for entry in data['entries'][:count]]
            print(f"✅ Fetched {len(summoner_ids)} Challenger summoners")
            return summoner_ids
        elif response.status_code == 429:
            print("⚠️  Rate limited (429). Retrying in 120s...")
            time.sleep(120)
            return get_challenger_summoners(platform, count)
        else:
            print(f"❌ Error fetching Challengers: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Exception: {e}")
        return []


def get_puuid_from_summoner_id(summoner_id, platform=PLATFORM):
    """Convert Summoner ID to PUUID"""
    url = f"https://{platform}.api.riotgames.com/lol/summoner/v4/summoners/{summoner_id}"
    limiter.wait()

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            return response.json()['puuid']
        elif response.status_code == 429:
            print("⚠️  Rate limited (429). Retrying in 120s...")
            time.sleep(120)
            return get_puuid_from_summoner_id(summoner_id, platform)
        else:
            print(f"❌ Error fetching PUUID for {summoner_id}: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None


def get_match_ids(puuid, region=REGION, count=20):
    """Get recent ranked match IDs for a PUUID"""
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
    params = {
        "type": "ranked",
        "start": 0,
        "count": count
    }
    limiter.wait()

    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            print("⚠️  Rate limited (429). Retrying in 120s...")
            time.sleep(120)
            return get_match_ids(puuid, region, count)
        else:
            print(f"❌ Error fetching match IDs: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Exception: {e}")
        return []


def get_match_data(match_id, region=REGION):
    """Fetch full match data including items"""
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    limiter.wait()

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            print("⚠️  Rate limited (429). Retrying in 120s...")
            time.sleep(120)
            return get_match_data(match_id, region)
        else:
            print(f"❌ Error fetching match {match_id}: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None


# ==================== DATA PROCESSING ====================

def extract_match_rows(match_data):
    """Extract participant rows with item data from match JSON"""
    if not match_data or 'info' not in match_data:
        return []

    info = match_data['info']
    participants = info.get('participants', [])

    if len(participants) != 10:
        return []  # Only 5v5 matches

    rows = []
    for participant in participants:
        row = {
            'match_id': match_data['metadata']['matchId'],
            'game_duration': info.get('gameDuration', 0),
            'champion_id': participant.get('championId', 0),
            'team_id': participant.get('teamId', 0),
            'win': 1 if participant.get('win', False) else 0,
            'kills': participant.get('kills', 0),
            'deaths': participant.get('deaths', 0),
            'assists': participant.get('assists', 0),
            'gold_earned': participant.get('goldEarned', 0),
            'total_damage': participant.get('totalDamageDealtToChampions', 0),
            'vision_score': participant.get('visionScore', 0),
            'item0': participant.get('item0', 0),
            'item1': participant.get('item1', 0),
            'item2': participant.get('item2', 0),
            'item3': participant.get('item3', 0),
            'item4': participant.get('item4', 0),
            'item5': participant.get('item5', 0),
            'item6': participant.get('item6', 0),
        }
        rows.append(row)

    return rows


def save_to_csv(rows, filepath=OUTPUT_FILE):
    """Append rows to CSV file"""
    file_exists = os.path.isfile(filepath)

    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, 'a', newline='', encoding='utf-8') as f:
        fieldnames = ['match_id', 'game_duration', 'champion_id', 'team_id', 'win',
                      'kills', 'deaths', 'assists', 'gold_earned', 'total_damage',
                      'vision_score', 'item0', 'item1', 'item2', 'item3', 'item4',
                      'item5', 'item6']
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerows(rows)


# ==================== MAIN CRAWLER ====================

def main():
    """Main crawler loop"""
    print("🚀 Starting Riot Match Crawler with Item Data")
    print(f"📁 Output: {OUTPUT_FILE}")
    print(f"⚙️  Rate limits: {REQUESTS_PER_SECOND}/s, {REQUESTS_PER_2_MIN}/2min\n")

    if API_KEY == "YOUR_RIOT_API_KEY_HERE":
        print("❌ ERROR: Please set your Riot API key in the API_KEY variable!")
        return

    # Step 1: Get Challenger summoners
    summoner_ids = get_challenger_summoners(PLATFORM, count=50)
    if not summoner_ids:
        print("❌ No summoners found. Exiting.")
        return

    total_matches = 0
    processed_match_ids = set()

    # Step 2: For each summoner, get their PUUIDs and matches
    for idx, summoner_id in enumerate(summoner_ids, 1):
        print(f"\n[{idx}/{len(summoner_ids)}] Processing summoner: {summoner_id}")

        # Get PUUID
        puuid = get_puuid_from_summoner_id(summoner_id, PLATFORM)
        if not puuid:
            print(f"⚠️  Skipping (no PUUID)")
            continue

        # Get match IDs
        match_ids = get_match_ids(puuid, REGION, count=20)
        print(f"  📊 Found {len(match_ids)} matches")

        # Fetch each match
        for match_id in match_ids:
            if match_id in processed_match_ids:
                continue

            match_data = get_match_data(match_id, REGION)
            if not match_data:
                continue

            rows = extract_match_rows(match_data)
            if rows:
                save_to_csv(rows)
                processed_match_ids.add(match_id)
                total_matches += 1
                print(f"  ✅ Match {match_id}: {len(rows)} rows saved (Total: {total_matches})")
            else:
                print(f"  ⚠️  Match {match_id}: No valid data")

    print(f"\n🎉 Crawling complete! Total matches: {total_matches}")
    print(f"📁 Data saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
