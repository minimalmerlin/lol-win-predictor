# Model Training Guide

## Overview

This project uses clean training data **without data leakage** to train win prediction models. The system is designed to:
- Automatically grow with the dataset
- Use configurable paths for all data
- Prevent data leakage by only using champion IDs as features
- Provide reasonable accuracy (~50-55% is expected)

## Why ~50% Accuracy is Good

**IMPORTANT**: An accuracy of ~50-55% is actually **correct** for this task!

- We only use **champion team compositions** (10 champion IDs) as features
- No gold, kills, towers, or other in-game stats
- No data from future game state
- This is pure draft prediction based only on picks

The old 90.9% accuracy indicated **data leakage** - the model had access to game outcome information.

## Quick Start

### 1. Collect More Data

Run the data collection script (continuously adds new matches):

```bash
python fetch_massive_data.py
```

The script:
- Fetches ranked matches from Riot API
- Saves to `data/clean_training_data_massive.csv`
- Tracks progress in `data/crawler_state/`
- Can be stopped and resumed anytime
- Target: 5000 matches (configured in `config.py`)

### 2. Train Models

Once you have enough data (>100 matches minimum):

```bash
python train_model.py
```

This will:
- Load data from `data/clean_training_data_massive.csv`
- Train Random Forest and Logistic Regression models
- Backup old models to `models/backups/`
- Save new models to `models/`
- Show performance metrics

### 3. Monitor Dataset Growth

```python
from config import get_data_info

info = get_data_info()
print(info)
```

## Configuration

All paths and parameters are centralized in [`config.py`](config.py):

```python
# Data paths
TRAINING_DATA_PATH = 'data/clean_training_data_massive.csv'  # Main dataset
TRAINING_DATA_FALLBACK = 'data/clean_training_data.csv'      # Small test set

# Training parameters
TRAINING_CONFIG = {
    'test_size': 0.2,           # 20% test split
    'random_state': 42,
    'min_matches_for_training': 100,
    'rf_params': {
        'n_estimators': 100,
        'max_depth': 20,
        ...
    }
}
```

## Current Dataset Status

Run this to check current data:

```bash
python -c "from config import get_data_info; import json; print(json.dumps(get_data_info(), indent=2))"
```

Expected output:
```json
{
  "massive_dataset": {
    "path": "data/clean_training_data_massive.csv",
    "matches": 1613,
    "exists": true
  },
  "small_dataset": {
    "path": "data/clean_training_data.csv",
    "matches": 100,
    "exists": true
  }
}
```

## Model Performance Tracking

Performance metrics are saved to `models/performance.json`:

```json
{
  "accuracy": 0.5139,
  "roc_auc": 0.4865,
  "timestamp": "2025-12-28T15:18:22.123456",
  "matches_count": 1613,
  "training_config": {...}
}
```

## Data Format

### Input CSV Format

```csv
match_id,blue_win,blue_champ_1,blue_champ_2,blue_champ_3,blue_champ_4,blue_champ_5,red_champ_1,red_champ_2,red_champ_3,red_champ_4,red_champ_5
EUW1_6859979556,1,126,57,112,235,69,68,32,157,429,111
```

- `match_id`: Unique match identifier
- `blue_win`: 1 if blue team won, 0 if red team won
- `blue_champ_X`: Champion ID for blue team position X
- `red_champ_X`: Champion ID for red team position X

### Features Used

**Only these 10 features** are used (to prevent data leakage):
- `blue_champ_1` through `blue_champ_5`
- `red_champ_1` through `red_champ_5`

No gold, kills, towers, game duration, or any other in-game statistics are used.

## Automated Growth

The system is designed to grow automatically:

1. **Data Collection**: `fetch_massive_data.py` continuously adds matches
2. **Training**: `train_model.py` uses all available data
3. **API**: Models are loaded dynamically and can be hot-reloaded

### Adding More Data

Just run `fetch_massive_data.py` again. It will:
- Resume from where it stopped (using state files)
- Avoid duplicate matches
- Append new data to the CSV
- Grow organically

Then retrain:
```bash
python train_model.py
```

## Model Files

- `models/win_predictor_rf.pkl`: Random Forest model (main model)
- `models/win_predictor_lr.pkl`: Logistic Regression (baseline)
- `models/performance.json`: Performance metrics
- `models/backups/`: Automatic backups before retraining

## Troubleshooting

### "Accuracy > 85% might indicate data leakage"

This warning appears if accuracy is suspiciously high. Check:
1. Only champion IDs are used as features
2. No future game state leaked into training data
3. Train/test split is proper

### "No training data found"

Make sure you have at least 100 matches in either:
- `data/clean_training_data_massive.csv`, or
- `data/clean_training_data.csv`

Run `fetch_massive_data.py` to collect data.

### Dataset isn't growing

Check the crawler state:
```bash
ls -lh data/crawler_state/
wc -l data/crawler_state/seen_matches.txt
```

If stuck, you can delete the state files to start fresh (will re-crawl):
```bash
rm data/crawler_state/*.txt
```

## Best Practices

1. **Retrain regularly** as dataset grows (every 500-1000 new matches)
2. **Monitor performance.json** to track model improvements
3. **Keep backups** (automatic in `models/backups/`)
4. **Check data balance**: Blue wins should be ~50% (balanced dataset)

## Next Steps

As the dataset grows to 5000+ matches, you can:
1. Increase model complexity (more trees, deeper depth)
2. Add champion synergy features
3. Implement ensemble methods
4. Add champion role information

But always verify: **no data leakage!**
