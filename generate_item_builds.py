import pandas as pd
import json
import os
import sys
from collections import Counter
from pathlib import Path
from utils.ddragon import get_champion_mapping
from config import ITEM_BUILDS_PATH

# IMPORTANT: Must use the items CSV, not the merged one (which has no item columns)
# Try multiple sources in order of preference
POSSIBLE_DATA_FILES = [
    "data/clean_training_data_items.csv",  # Primary: has item columns
    "data/clean_training_data_massive.csv", # Fallback: no items, will fail validation
]

OUTPUT_JSON = str(ITEM_BUILDS_PATH)

# Backend copy for API
BACKEND_OUTPUT = "data/champion_data/item_builds.json"

def main():
    print("=" * 80)
    print("GENERATING ITEM BUILDS")
    print("=" * 80)

    # Find available data file
    DATA_FILE = None
    for candidate in POSSIBLE_DATA_FILES:
        if os.path.exists(candidate):
            DATA_FILE = candidate
            print(f"✅ Found input: {DATA_FILE}")
            break

    if DATA_FILE is None:
        error_msg = "CRITICAL ERROR: No training data found!"
        print(f"❌ {error_msg}")
        print("\nSearched for:")
        for f in POSSIBLE_DATA_FILES:
            print(f"  - {f}")
        print("\nMake sure the fetch step completed successfully!")
        sys.exit(1)  # EXIT CODE 1 - HARD FAILURE

    print(f"Output: {OUTPUT_JSON}")
    print(f"Backup: {BACKEND_OUTPUT}")
    print()

    # CRITICAL: Hard fail if CSV is unreadable
    try:
        df = pd.read_csv(DATA_FILE, on_bad_lines='skip')
    except Exception as e:
        error_msg = f"CRITICAL ERROR: Failed to read CSV: {e}"
        print(f"❌ {error_msg}")
        sys.exit(1)  # EXIT CODE 1 - HARD FAILURE

    # Validate we got data
    if len(df) == 0:
        error_msg = "CRITICAL ERROR: CSV file is empty (0 matches)"
        print(f"❌ {error_msg}")
        sys.exit(1)  # EXIT CODE 1 - HARD FAILURE

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

    # Validate we generated builds
    if len(final_builds) == 0:
        error_msg = "CRITICAL ERROR: No item builds could be generated (0 champions)"
        print(f"❌ {error_msg}")
        print("\nPossible causes:")
        print("  - CSV has no item columns (use clean_training_data_items.csv)")
        print("  - Champion ID mapping failed")
        print("  - All item slots are empty")
        sys.exit(1)  # EXIT CODE 1 - HARD FAILURE

    # Save to frontend
    try:
        os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)
        with open(OUTPUT_JSON, 'w') as f:
            json.dump(final_builds, f, indent=2)
        print(f"✅ Frontend: {OUTPUT_JSON} ({len(final_builds)} champions)")
    except Exception as e:
        error_msg = f"CRITICAL ERROR: Failed to write frontend JSON: {e}"
        print(f"❌ {error_msg}")
        sys.exit(1)  # EXIT CODE 1 - HARD FAILURE

    # Save to backend (for API)
    try:
        os.makedirs(os.path.dirname(BACKEND_OUTPUT), exist_ok=True)
        with open(BACKEND_OUTPUT, 'w') as f:
            json.dump(final_builds, f, indent=2)
        print(f"✅ Backend:  {BACKEND_OUTPUT} ({len(final_builds)} champions)")
    except Exception as e:
        # Warning only - backend copy is optional
        print(f"⚠️  Warning: Failed to write backend copy: {e}")

    print()
    print("=" * 80)
    print(f"✅ ITEM BUILDS GENERATION COMPLETED SUCCESSFULLY")
    print(f"   Champions: {len(final_builds)}")
    print(f"   Matches:   {len(df)}")
    print("=" * 80)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n❌ Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
