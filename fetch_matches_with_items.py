import requests
import pandas as pd
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ================= CONFIGURATION =================
# API Key from environment variable
API_KEY = os.getenv("RIOT_API_KEY")
if not API_KEY:
    raise ValueError("RIOT_API_KEY not found in environment variables. Please create a .env file with your API key.")

REGION_ROUTING = "europe"   # Für Match-V5 (europe, americas, asia)
START_PLAYER_NAME = "Agurin" # Seed Player (High Elo Jungler)
START_PLAYER_TAG = "EUW"
TARGET_MATCHES = 5000       # Zielanzahl
OUTPUT_FILE = "data/clean_training_data_items.csv"
# =================================================

headers = {
    "X-Riot-Token": API_KEY
}

def get_puuid(game_name, tag_line):
    """Holt die PUUID via Account-V1 (Modern Way)"""
    url = f"https://{REGION_ROUTING}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        return resp.json()['puuid']
    print(f"❌ Fehler bei PUUID Fetch ({game_name}#{tag_line}): {resp.status_code}")
    return None

def get_match_ids(puuid, count=20):
    """Holt Match IDs via Match-V5"""
    # queue=420 ist Ranked Solo/Duo
    url = f"https://{REGION_ROUTING}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?queue=420&start=0&count={count}"
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        return resp.json()
    return []

def get_match_details(match_id):
    """Lädt Details eines Matches"""
    url = f"https://{REGION_ROUTING}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    resp = requests.get(url, headers=headers)

    if resp.status_code == 200:
        return resp.json()
    elif resp.status_code == 429:
        print("⚠️ Rate Limit! Warte 10 Sekunden...")
        time.sleep(10)
        return get_match_details(match_id) # Retry
    elif resp.status_code == 404:
        return None
    return None

def process_match(data):
    """Extrahiert Champions, Win und ITEMS (0-6)"""
    info = data['info']
    row = {'match_id': data['metadata']['matchId']}

    blue_team = []
    red_team = []

    for p in info['participants']:
        # Daten pro Spieler extrahieren
        p_data = {
            'championId': p['championId'],
            'win': p['win'],
            'item0': p.get('item0', 0),
            'item1': p.get('item1', 0),
            'item2': p.get('item2', 0),
            'item3': p.get('item3', 0),
            'item4': p.get('item4', 0),
            'item5': p.get('item5', 0),
            'item6': p.get('item6', 0)
        }
        if p['teamId'] == 100:
            blue_team.append(p_data)
        else:
            red_team.append(p_data)

    # Wer hat gewonnen?
    row['blue_win'] = 1 if blue_team[0]['win'] else 0

    # Blue Team Spalten
    for i, p in enumerate(blue_team):
        idx = i + 1
        row[f'blue_champ_{idx}'] = p['championId']
        for item_idx in range(7):
            row[f'blue_item_{idx}_{item_idx}'] = p[f'item{item_idx}']

    # Red Team Spalten
    for i, p in enumerate(red_team):
        idx = i + 1
        row[f'red_champ_{idx}'] = p['championId']
        for item_idx in range(7):
            row[f'red_item_{idx}_{item_idx}'] = p[f'item{item_idx}']

    return row

def main():
    print(f"🚀 Starte Crawler mit Seed: {START_PLAYER_NAME}#{START_PLAYER_TAG}")

    # Sicherstellen, dass Ordner existiert
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    # 1. Seed PUUID holen
    seed_puuid = get_puuid(START_PLAYER_NAME, START_PLAYER_TAG)
    if not seed_puuid:
        print("❌ Seed-Player nicht gefunden. Prüfe API Key.")
        return

    processed_matches = set()

    # Vorhandene Daten laden um Duplikate zu vermeiden
    if os.path.exists(OUTPUT_FILE):
        try:
            df_exist = pd.read_csv(OUTPUT_FILE)
            processed_matches = set(df_exist['match_id'].unique())
            print(f"ℹ️ Bereits {len(processed_matches)} Matches vorhanden.")
        except:
            pass

    # Pool von Spielern, die wir noch scannen wollen
    puuid_pool = [seed_puuid]
    batch_rows = []

    while len(processed_matches) < TARGET_MATCHES and puuid_pool:
        current_puuid = puuid_pool.pop(0)
        match_ids = get_match_ids(current_puuid, count=20)

        for mid in match_ids:
            if mid in processed_matches:
                continue
            if len(processed_matches) >= TARGET_MATCHES:
                break

            data = get_match_details(mid)
            if not data: continue

            try:
                row = process_match(data)
                batch_rows.append(row)
                processed_matches.add(mid)
                print(f"✅ Match gespeichert ({len(processed_matches)}/{TARGET_MATCHES})")

                # Snowballing: Nimm 2 Spieler aus diesem Match in den Pool auf
                parts = data['metadata']['participants']
                for p_uuid in parts[:2]:
                    if p_uuid not in puuid_pool:
                        puuid_pool.append(p_uuid)

            except Exception as e:
                print(f"Fehler: {e}")

            # Batch Save alle 10 Matches
            if len(batch_rows) >= 10:
                df = pd.DataFrame(batch_rows)
                header = not os.path.exists(OUTPUT_FILE)
                df.to_csv(OUTPUT_FILE, mode='a', header=header, index=False)
                batch_rows = []
                print("💾 Batch gesichert.")

        time.sleep(0.5) # Schonung der API

    # Rest speichern
    if batch_rows:
        df = pd.DataFrame(batch_rows)
        header = not os.path.exists(OUTPUT_FILE)
        df.to_csv(OUTPUT_FILE, mode='a', header=header, index=False)

    print("🏁 Crawling fertig.")

if __name__ == "__main__":
    main()
