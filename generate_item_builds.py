import pandas as pd
import json
import os
from collections import Counter
from utils.ddragon import get_champion_mapping

# Pfad zur CSV mit den Item-Daten
DATA_FILE = "data/clean_training_data_items.csv"
OUTPUT_JSON = "lol-coach-frontend/public/data/item_builds.json"

def main():
    print("--- BUILDING ITEM SETS ---")

    if not os.path.exists(DATA_FILE):
        print("Keine Daten gefunden.")
        return

    # Lade CSV (Fehlertolerant)
    try:
        df = pd.read_csv(DATA_FILE, on_bad_lines='skip')
    except Exception as e:
        print(f"Fehler beim Lesen der CSV: {e}")
        return

    print(f"Analysiere {len(df)} Matches...")

    id_to_name, _ = get_champion_mapping()
    champion_items = {}

    # Helper: Items aus einer Zeile extrahieren (nur Gewinner!)
    def process_row(row):
        # Blue Team gewonnen? -> Nimm Blue Items
        if row['blue_win'] == 1:
            team_prefix = 'blue'
        else:
            team_prefix = 'red' # Red hat gewonnen

        for i in range(1, 6): # Spieler 1-5
            champ_col = f'{team_prefix}_champ_{i}'
            if champ_col not in row: continue

            champ_id = row[champ_col]
            if pd.isna(champ_id): continue

            champ_name = id_to_name.get(int(champ_id), str(int(champ_id)))

            if champ_name not in champion_items:
                champion_items[champ_name] = []

            # Items 0-5 sammeln (Item 6 ist oft Ward, lassen wir weg für Core Build)
            for item_idx in range(6):
                item_col = f'{team_prefix}_item_{i}_{item_idx}'
                item_id = row.get(item_col, 0)
                if item_id and item_id != 0: # 0 = Leerer Slot
                    champion_items[champ_name].append(int(item_id))

    # Iteriere durch DataFrame
    df.apply(process_row, axis=1)

    # Aggregieren: Top 6 Items pro Champ
    final_builds = {}
    for name, items in champion_items.items():
        if not items: continue

        # Die häufigsten 6 Items
        common = Counter(items).most_common(6)
        build = [item_id for item_id, count in common]

        # Auffüllen falls < 6 (mit 0 oder Platzhalter)
        while len(build) < 6:
            build.append(0)

        final_builds[name] = build

    # Speichern
    os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)
    with open(OUTPUT_JSON, 'w') as f:
        json.dump(final_builds, f, indent=2)

    print(f"✓ Builds für {len(final_builds)} Champions generiert.")
    print(f"✓ Gespeichert in {OUTPUT_JSON}")

if __name__ == "__main__":
    main()
