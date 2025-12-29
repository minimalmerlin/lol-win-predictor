"""
Configuration file for LoL Win Prediction System
=================================================
Centralized configuration for all data paths and training parameters.
"""

import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / 'data'
MODELS_DIR = BASE_DIR / 'models'
CHAMPION_DATA_DIR = DATA_DIR / 'champion_data'

# Training data paths
# PRIMARY: Use this for training - continuously growing dataset
TRAINING_DATA_PATH = DATA_DIR / 'clean_training_data_massive.csv'

# FALLBACK 1: Items dataset (freshly fetched by pipeline)
TRAINING_DATA_ITEMS = DATA_DIR / 'clean_training_data_items.csv'

# FALLBACK 2: Smaller dataset for quick testing
TRAINING_DATA_FALLBACK = DATA_DIR / 'clean_training_data.csv'

# Champion data files
CHAMPION_STATS_PATH = CHAMPION_DATA_DIR / 'champion_stats.json'
ITEM_BUILDS_PATH = CHAMPION_DATA_DIR / 'item_builds.json'
BEST_TEAMMATES_PATH = CHAMPION_DATA_DIR / 'best_teammates.json'
CHAMPION_SYNERGIES_PATH = CHAMPION_DATA_DIR / 'champion_synergies.json'

# Model paths
CHAMPION_PREDICTOR_PATH = MODELS_DIR / 'champion_predictor.pkl'
WIN_PREDICTOR_RF_PATH = MODELS_DIR / 'win_predictor_rf.pkl'
WIN_PREDICTOR_LR_PATH = MODELS_DIR / 'win_predictor_lr.pkl'
MODEL_PERFORMANCE_PATH = MODELS_DIR / 'performance.json'

# Model backup directory
MODEL_BACKUP_DIR = MODELS_DIR / 'backups'

# Training parameters
TRAINING_CONFIG = {
    'test_size': 0.2,  # 20% test split
    'random_state': 42,
    'min_matches_for_training': 100,  # Minimum matches required
    'rf_params': {
        'n_estimators': 100,
        'max_depth': 20,
        'min_samples_split': 10,
        'min_samples_leaf': 5,
        'random_state': 42,
        'n_jobs': -1
    },
    'lr_params': {
        'max_iter': 1000,
        'random_state': 42
    }
}

# Data collection settings
CRAWLER_STATE_DIR = DATA_DIR / 'crawler_state'
TARGET_MATCHES = 50000  # Target for massive dataset

# Create directories if they don't exist
for directory in [DATA_DIR, MODELS_DIR, CHAMPION_DATA_DIR, MODEL_BACKUP_DIR, CRAWLER_STATE_DIR]:
    directory.mkdir(parents=True, exist_ok=True)


def get_training_data_path():
    """
    Get the path to the training data file with intelligent fallback.

    Priority order:
    1. clean_training_data_massive.csv (merged dataset)
    2. clean_training_data_items.csv (freshly fetched by pipeline)
    3. clean_training_data.csv (legacy small dataset)

    Returns the first file that exists with enough matches.
    """
    candidates = [
        ('massive', TRAINING_DATA_PATH),
        ('items', TRAINING_DATA_ITEMS),
        ('fallback', TRAINING_DATA_FALLBACK)
    ]

    for name, path in candidates:
        if path.exists():
            try:
                # Check if file has enough data
                with open(path, 'r') as f:
                    line_count = sum(1 for _ in f) - 1  # Subtract header

                if line_count >= TRAINING_CONFIG['min_matches_for_training']:
                    print(f"✓ Using {name} dataset: {path} ({line_count} matches)")
                    return path
                else:
                    print(f"⚠️  {name} dataset has only {line_count} matches (need {TRAINING_CONFIG['min_matches_for_training']})")
            except Exception as e:
                print(f"⚠️  Error reading {name} dataset: {e}")
                continue

    # If we get here, no valid dataset was found
    raise FileNotFoundError(
        f"No valid training data found. Searched:\n"
        f"  1. {TRAINING_DATA_PATH} (massive dataset)\n"
        f"  2. {TRAINING_DATA_ITEMS} (items dataset)\n"
        f"  3. {TRAINING_DATA_FALLBACK} (fallback dataset)\n"
        f"Minimum required: {TRAINING_CONFIG['min_matches_for_training']} matches"
    )


def get_data_info():
    """Get information about available datasets"""
    info = {}

    for name, path in [
        ('massive_dataset', TRAINING_DATA_PATH),
        ('small_dataset', TRAINING_DATA_FALLBACK)
    ]:
        if path.exists():
            with open(path, 'r') as f:
                line_count = sum(1 for _ in f) - 1
            info[name] = {
                'path': str(path),
                'matches': line_count,
                'exists': True
            }
        else:
            info[name] = {
                'path': str(path),
                'matches': 0,
                'exists': False
            }

    return info
