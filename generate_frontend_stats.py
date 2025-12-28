import pandas as pd
import json
import os
from config import TRAINING_DATA_PATH
from utils.ddragon import get_champion_mapping

def main():
    print("Generating Frontend Stats...")
    if not TRAINING_DATA_PATH.exists():
        print(f"Training data not found at {TRAINING_DATA_PATH}")
        return

    # Load Data & Mapping
    print(f"Loading data from {TRAINING_DATA_PATH}...")
    df = pd.read_csv(TRAINING_DATA_PATH, usecols=['blue_win'] + [f'blue_champ_{i}' for i in range(1,6)] + [f'red_champ_{i}' for i in range(1,6)])
    print(f"Loaded {len(df)} matches")

    id_to_name, patch_version = get_champion_mapping()
    print(f"Using patch version: {patch_version}")

    stats_db = {}

    # Process Winners
    print("Processing winning teams...")
    winners = pd.concat([
        df[df['blue_win']==1][[f'blue_champ_{i}' for i in range(1,6)]],
        df[df['blue_win']==0][[f'red_champ_{i}' for i in range(1,6)]].rename(columns=lambda x: x.replace('red', 'blue'))
    ])

    for _, row in winners.iterrows():
        ids = [i for i in row.values if i in id_to_name]
        for my_id in ids:
            name = id_to_name[my_id]
            if name not in stats_db:
                stats_db[name] = {'partners': [], 'wins': 0}
            stats_db[name]['wins'] += 1
            stats_db[name]['partners'].extend([id_to_name[pid] for pid in ids if pid != my_id])

    # Export
    print("Generating final stats...")
    from collections import Counter
    final = {
        name: {
            "name": name,
            "total_wins": d['wins'],
            "best_teammates": [
                {"name": k, "count": v}
                for k, v in Counter(d['partners']).most_common(5)
            ]
        }
        for name, d in stats_db.items()
    }

    out = 'lol-coach-frontend/public/data/champion_stats.json'
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w') as f:
        json.dump(final, f, indent=2)

    print(f"✅ Generated stats for {len(final)} champions")
    print(f"✅ Saved to {out}")
    print("Done.")

if __name__ == "__main__":
    main()
