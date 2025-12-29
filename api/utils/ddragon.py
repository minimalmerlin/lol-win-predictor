import requests
import functools

# Cache das Ergebnis, damit wir nicht bei jedem Request Riot fragen (spart Zeit)
@functools.lru_cache(maxsize=1)
def get_champion_mapping():
    """
    Holt aktuelle Champion-Daten und erstellt eine Map:
    ID (int) -> Name (str)
    z.B. {266: "Aatrox", 103: "Ahri"}
    """
    try:
        # 1. Version holen
        versions = requests.get("https://ddragon.leagueoflegends.com/api/versions.json").json()
        latest = versions[0]
        
        # 2. Daten holen
        url = f"https://ddragon.leagueoflegends.com/cdn/{latest}/data/en_US/champion.json"
        data = requests.get(url).json()['data']
        
        # 3. Mapping erstellen
        # Riot's 'key' ist die ID als String, wir brauchen Int für das Modell
        id_to_name = {}
        for champ_name, champ_data in data.items():
            champ_id = int(champ_data['key'])
            id_to_name[champ_id] = champ_data['name']
            
        return id_to_name, latest
        
    except Exception as e:
        print(f"Error fetching DataDragon: {e}")
        return {}, "14.1.1"

# Test
if __name__ == "__main__":
    mapping, version = get_champion_mapping()
    print(f"Patch: {version}")
    print(f"Gefundene Champions: {len(mapping)}")
    print(f"ID 266 ist: {mapping.get(266)}")