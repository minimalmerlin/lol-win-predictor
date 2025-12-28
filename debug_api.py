import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Key from environment variable
API_KEY = os.getenv("RIOT_API_KEY")
if not API_KEY:
    raise ValueError("RIOT_API_KEY not found in environment variables. Please create a .env file with your API key.") 
REGION = 'euw1'

HEADERS = {"X-Riot-Token": API_KEY}

def debug_challenger():
    url = f"https://{REGION}.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5"
    print(f"Rufe URL auf: {url}")
    
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
        print(f"Fehler: {response.status_code}")
        return

    data = response.json()
    if 'entries' not in data:
        print("Keine 'entries' gefunden!")
        print(data.keys())
        return

    entries = data['entries']
    if not entries:
        print("Liste 'entries' ist leer.")
        return

    # Wir schauen uns den ersten Spieler genau an
    first_player = entries[0]
    print("\n--- DATEN DES ERSTEN SPIELERS ---")
    print(json.dumps(first_player, indent=2))
    print("---------------------------------")
    
    # Check auf bekannte ID-Felder
    possible_ids = ['summonerId', 'playerOrTeamId', 'puuid', 'uuid']
    found = [k for k in first_player.keys() if k in possible_ids]
    print(f"Gefundene ID-Felder: {found}")

if __name__ == "__main__":
    debug_challenger()