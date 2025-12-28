"""
Data Dragon API Utilities
Fetches champion mappings from Riot's Data Dragon API
"""
import requests
import json
from functools import lru_cache

@lru_cache(maxsize=1)
def get_champion_mapping():
    """
    Fetches the latest champion ID -> Name mapping from Data Dragon
    Returns: (dict mapping id to name, patch version string)
    """
    try:
        # Get latest version
        version_url = "https://ddragon.leagueoflegends.com/api/versions.json"
        versions = requests.get(version_url).json()
        latest_version = versions[0]

        # Get champion data
        champion_url = f"https://ddragon.leagueoflegends.com/cdn/{latest_version}/data/en_US/champion.json"
        response = requests.get(champion_url)
        data = response.json()

        # Build ID -> Name mapping
        id_to_name = {}
        for champ_data in data['data'].values():
            champ_id = int(champ_data['key'])  # Numeric ID
            champ_name = champ_data['name']    # Display name
            id_to_name[champ_id] = champ_name

        print(f"✅ Loaded {len(id_to_name)} champions from Data Dragon v{latest_version}")
        return id_to_name, latest_version

    except Exception as e:
        print(f"❌ Failed to fetch champion mapping: {e}")
        # Return empty mapping and fallback version
        return {}, "14.1.1"
