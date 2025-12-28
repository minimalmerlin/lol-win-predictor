import requests
import pandas as pd
import time
import os
import urllib.parse
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import configuration
from config import TRAINING_DATA_PATH, CRAWLER_STATE_DIR, TARGET_MATCHES

# --- KONFIGURATION ---
# API Key from environment variable
API_KEY = os.getenv("RIOT_API_KEY")
if not API_KEY:
    raise ValueError("RIOT_API_KEY not found in environment variables. Please create a .env file with your API key.")
REGION_ROUTING = 'europe'
# TARGET_MATCHES and paths now come from config.py for consistency
OUTPUT_FILE = str(TRAINING_DATA_PATH)
STATE_DIR = str(CRAWLER_STATE_DIR)

# Seeds: Wir starten mit mehreren High-Elo Spielern, um breiter zu streuen
SEEDS = [
    ("Agurin", "EUW"),
    ("NoWay4u", "EUW"),
    ("Tolkin", "EUW"),
    ("Broxah", "EUW")
]

HEADERS = {"X-Riot-Token": API_KEY}

def load_state():
    """Lädt bereits besuchte IDs, um Duplikate nach Neustart zu vermeiden"""
    if not os.path.exists(STATE_DIR):
        os.makedirs(STATE_DIR)
    
    seen_puuids = set()
    seen_matches = set()
    
    if os.path.exists(f"{STATE_DIR}/seen_puuids.txt"):
        with open(f"{STATE_DIR}/seen_puuids.txt", 'r') as f:
            seen_puuids = set(line.strip() for line in f)
            
    if os.path.exists(f"{STATE_DIR}/seen_matches.txt"):
        with open(f"{STATE_DIR}/seen_matches.txt", 'r') as f:
            seen_matches = set(line.strip() for line in f)
            
    return seen_puuids, seen_matches

def save_state_item(filename, item):
    """Speichert ein einzelnes Item sofort in die State-Datei"""
    with open(f"{STATE_DIR}/{filename}", 'a') as f:
        f.write(f"{item}\n")

def get_puuid(name, tag):
    name_enc = urllib.parse.quote(name)
    tag_enc = urllib.parse.quote(tag)
    url = f"https://{REGION_ROUTING}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name_enc}/{tag_enc}"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 200: return resp.json()['puuid']
    return None

def make_request(url):
    """Robuste Request-Funktion mit Auto-Retry bei Rate Limits"""
    while True:
        try:
            resp = requests.get(url, headers=HEADERS)
            
            if resp.status_code == 200:
                return resp.json()
            elif resp.status_code == 429:
                wait_time = int(resp.headers.get('Retry-After', 10))
                print(f"    [RATE LIMIT] Pause für {wait_time} Sekunden...")
                time.sleep(wait_time + 1)
                continue
            elif resp.status_code == 403:
                print("!!! API KEY ABGELAUFEN ODER UNGÜLTIG !!!")
                exit()
            else:
                return None
        except Exception as e:
            print(f"    [ERROR] {e}. Warte 5s...")
            time.sleep(5)
            continue

def get_match_ids(puuid):
    url = f"https://{REGION_ROUTING}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=20&queue=420"
    return make_request(url) or []

def process_match(match_id):
    url = f"https://{REGION_ROUTING}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    data = make_request(url)
    
    if not data or data['info']['gameMode'] != 'CLASSIC':
        return None, []
        
    row = {'match_id': match_id}
    blue, red, participants = [], [], data['info']['participants']
    puuids_in_game = []
    
    for p in participants:
        puuids_in_game.append(p['puuid'])
        if p['teamId'] == 100:
            blue.append(p['championId'])
            row['blue_win'] = 1 if p['win'] else 0
        else:
            red.append(p['championId'])
            
    if len(blue) != 5 or len(red) != 5: return None, []
    
    for i, c in enumerate(blue): row[f'blue_champ_{i+1}'] = c
    for i, c in enumerate(red): row[f'red_champ_{i+1}'] = c
    
    return row, puuids_in_game

def main():
    if not os.path.exists('data'): os.makedirs('data')
    
    # State laden
    seen_puuids, seen_matches = load_state()
    queue_puuids = []
    
    # CSV Header schreiben, falls Datei neu
    if not os.path.exists(OUTPUT_FILE):
        df_dummy = pd.DataFrame(columns=['match_id', 'blue_win'] + 
                                      [f'blue_champ_{i}' for i in range(1,6)] + 
                                      [f'red_champ_{i}' for i in range(1,6)])
        df_dummy.to_csv(OUTPUT_FILE, index=False)

    print("--- 1. Initialisiere Seeds ---")
    for name, tag in SEEDS:
        pid = get_puuid(name, tag)
        if pid and pid not in seen_puuids:
            queue_puuids.append(pid)
            
    matches_collected = len(seen_matches)
    print(f"Bereits gesammelte Matches: {matches_collected}")
    print(f"Start mit {len(queue_puuids)} Seed-Spielern in der Queue.")

    while matches_collected < TARGET_MATCHES and (queue_puuids or len(seen_puuids) > 0):
        # Wenn Queue leer, nimm zufälligen bekannten Spieler (Fallback)
        if not queue_puuids:
            print("Queue leer - Recycle bekannte Spieler...")
            queue_puuids = list(seen_puuids)[:50] 
            
        current_puuid = queue_puuids.pop(0)
        
        # Holen & Merken
        if current_puuid in seen_puuids: # Schon gescraped?
            # Wir checken ihn trotzdem kurz auf neue Matches, wenn die Queue klein ist
            if len(queue_puuids) > 100: continue 
            
        save_state_item('seen_puuids.txt', current_puuid)
        seen_puuids.add(current_puuid)
        
        # Matches holen
        match_ids = get_match_ids(current_puuid)
        new_matches_found = 0
        
        for m_id in match_ids:
            if m_id in seen_matches: continue
            
            # Verarbeiten
            row, new_players = process_match(m_id)
            if row:
                # 1. Speichern in CSV (Append Mode)
                pd.DataFrame([row]).to_csv(OUTPUT_FILE, mode='a', header=False, index=False)
                
                # 2. State updaten
                save_state_item('seen_matches.txt', m_id)
                seen_matches.add(m_id)
                matches_collected += 1
                new_matches_found += 1
                
                # 3. Neue Spieler in Queue
                for np in new_players:
                    if np not in seen_puuids:
                        queue_puuids.append(np)
                
                print(f"[{matches_collected}/{TARGET_MATCHES}] Match gespeichert. Queue: {len(queue_puuids)}")
                
                if matches_collected >= TARGET_MATCHES:
                    print("ZIEL ERREICHT!")
                    return
            
            time.sleep(1.2) # Safety Sleep

        if new_matches_found == 0:
            print(f"  Keine neuen Matches bei Spieler ... gehe weiter.")

if __name__ == "__main__":
    main()