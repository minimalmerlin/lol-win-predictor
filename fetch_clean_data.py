import requests
import pandas as pd
import time
import os

# KONFIGURATION
API_KEY = 'R'  # Hier Key einfügen
REGION = 'euw1'
ROUTING = 'europe'
COUNT_MATCHES = 100  # Wie viele Matches sollen geladen werden? (Für Test erst mal 100, später 1000+)

# Header für Requests
HEADERS = {
    "X-Riot-Token": API_KEY
}

def get_challenger_players():
    """Holt eine Liste von High-Elo Spielern (Challenger), um gute Matches zu finden."""
    url = f"https://{REGION}.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5"
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            return response.json()['entries']
        else:
            print(f"Fehler beim Holen der Challenger-Liste: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error: {e}")
        return []

def get_puuid_by_summoner_id(summoner_id):
    """Wandelt SummonerID in PUUID um (nötig für Match-V5)."""
    url = f"https://{REGION}.api.riotgames.com/lol/summoner/v4/summoners/{summoner_id}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()['puuid']
    return None

def get_match_ids(puuid, count=20):
    """Holt die letzten Match-IDs eines Spielers."""
    url = f"https://{ROUTING}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}&queue=420" # Queue 420 = Ranked Solo/Duo
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    return []

def get_match_details(match_id):
    """
    Das Herzstück: Extrahiert NUR Champions und Winner.
    Kein Gold, keine Kills -> Kein Data Leakage.
    """
    url = f"https://{ROUTING}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 429:
        print("Rate Limit erreicht. Warte 10 Sekunden...")
        time.sleep(10)
        return get_match_details(match_id) # Retry
        
    if response.status_code != 200:
        return None

    data = response.json()
    
    # Check ob Classic Mode (kein ARAM, kein Arena)
    if data['info']['gameMode'] != 'CLASSIC':
        return None

    row = {'match_id': match_id}
    
    # Teams sortieren
    participants = data['info']['participants']
    
    blue_team = []
    red_team = []
    blue_win = False
    
    for p in participants:
        if p['teamId'] == 100:
            blue_team.append(p['championId'])
            # Win Status von einem Blue-Player checken
            blue_win = p['win']
        else:
            red_team.append(p['championId'])
            
    # Wir brauchen genau 5 vs 5
    if len(blue_team) != 5 or len(red_team) != 5:
        return None
        
    # Daten in Row schreiben
    for i, champ_id in enumerate(blue_team):
        row[f'blue_champ_{i+1}'] = champ_id
        
    for i, champ_id in enumerate(red_team):
        row[f'red_champ_{i+1}'] = champ_id
        
    row['blue_win'] = 1 if blue_win else 0
    
    return row

def main():
    if not os.path.exists('data'):
        os.makedirs('data')
        
    print("1. Hole Challenger Spieler...")
    challengers = get_challenger_players()
    if not challengers:
        return

    # Wir nehmen nur die ersten 50 Spieler, das reicht für viele Matches
    target_players = challengers[:50]
    
    all_match_ids = set()
    
    print("2. Sammle Match IDs...")
    for i, player in enumerate(target_players):
        print(f"  Verarbeite Spieler {i+1}/{len(target_players)}...")
        puuid = get_puuid_by_summoner_id(player['summonerId'])
        if puuid:
            matches = get_match_ids(puuid)
            for m in matches:
                all_match_ids.add(m)
            time.sleep(1.2) # Kleines Delay um Rate Limits zu schonen
            
        if len(all_match_ids) >= COUNT_MATCHES:
            break
            
    print(f"Gefundene Unique Matches: {len(all_match_ids)}")
    
    clean_data = []
    
    print("3. Downloade Match Details (Das dauert einen Moment)...")
    for i, match_id in enumerate(list(all_match_ids)[:COUNT_MATCHES]):
        if i % 10 == 0:
            print(f"  Fortschritt: {i}/{COUNT_MATCHES}")
            
        row = get_match_details(match_id)
        if row:
            clean_data.append(row)
        
        time.sleep(1.2) # Rate Limit Schutz (Riot erlaubt ca 20 requests/sec oder 100/2min je nach key)

    # Speichern
    df = pd.DataFrame(clean_data)
    output_file = 'data/clean_training_data.csv'
    df.to_csv(output_file, index=False)
    
    print(f"\nFERTIG! {len(df)} saubere Matches gespeichert in {output_file}")
    print("Spalten:", df.columns.tolist())

if __name__ == "__main__":
    main()
