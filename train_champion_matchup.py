"""
Champion Matchup Predictor Training Script
===========================================
Trains the champion matchup prediction model with enhanced features.

Features Used:
1. Champion IDs (10 features: 5 blue + 5 red)
2. Champion Win Rates (7 features: avg, max, min for each team + diff)
3. Total: 17 features for better prediction accuracy

This script:
- Loads champion stats for win rates
- Prepares features with champion IDs + win rates
- Trains Random Forest model
- Evaluates and saves model with encoder
- Tracks performance metrics

Author: Victory AI System
Date: 2025-12-29
"""

import pandas as pd
import numpy as np
import json
import joblib
import logging
from pathlib import Path
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report, confusion_matrix

from config import (
    get_training_data_path,
    CHAMPION_PREDICTOR_PATH,
    MODEL_BACKUP_DIR,
    TRAINING_CONFIG
)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ChampionMatchupTrainer:
    """Trains the Champion Matchup Prediction Model"""

    def __init__(self):
        self.champion_stats = {}
        self.champion_to_id = {}
        self.id_to_champion = {}
        self.model = None

    def load_champion_stats(self):
        """Load champion statistics (win rates)"""
        logger.info("=" * 80)
        logger.info("LOADING CHAMPION STATISTICS")
        logger.info("=" * 80)

        stats_path = Path('./data/champion_data/champion_stats.json')

        if not stats_path.exists():
            logger.warning(f"⚠️  Champion stats not found at {stats_path}")
            logger.warning("   Will use default 50% win rate for all champions")
            return

        with open(stats_path, 'r') as f:
            self.champion_stats = json.load(f)

        logger.info(f"✓ Loaded stats for {len(self.champion_stats)} champions")

    def get_champion_winrate(self, champion_id: int) -> float:
        """
        Get win rate for a champion by ID

        Args:
            champion_id: Champion ID (numeric)

        Returns:
            Win rate (0-1), defaults to 0.5 if not found
        """
        # Find champion name from ID
        champion_name = self.id_to_champion.get(champion_id)

        if not champion_name:
            return 0.5

        # Get stats
        stats = self.champion_stats.get(champion_name, {})
        return stats.get('win_rate', 0.5)

    def load_and_prepare_data(self):
        """Load training data and prepare features with win rates"""
        logger.info("=" * 80)
        logger.info("LOADING TRAINING DATA")
        logger.info("=" * 80)

        # Load data
        data_path = get_training_data_path()
        logger.info(f"Using data file: {data_path}")

        df = pd.read_csv(data_path)
        logger.info(f"✓ Loaded {len(df)} matches")

        # Build champion encoder (ID -> Name mapping)
        self._build_champion_encoder(df)

        # Features: Champion IDs
        champ_cols = [
            'blue_champ_1', 'blue_champ_2', 'blue_champ_3', 'blue_champ_4', 'blue_champ_5',
            'red_champ_1', 'red_champ_2', 'red_champ_3', 'red_champ_4', 'red_champ_5'
        ]

        # Target
        target_col = 'blue_win'

        # Check columns
        missing_cols = set(champ_cols + [target_col]) - set(df.columns)
        if missing_cols:
            raise ValueError(f"Missing columns: {missing_cols}")

        # Prepare feature matrix
        logger.info("\n" + "=" * 80)
        logger.info("PREPARING FEATURES WITH WIN RATES")
        logger.info("=" * 80)

        X_champs = df[champ_cols].values
        y = df[target_col].values

        # Calculate win rate features for each match
        logger.info("Calculating win rate features for each match...")

        win_rate_features = []
        for idx, row in enumerate(X_champs):
            blue_champs = row[:5]
            red_champs = row[5:]

            # Get win rates
            blue_winrates = [self.get_champion_winrate(int(cid)) for cid in blue_champs]
            red_winrates = [self.get_champion_winrate(int(cid)) for cid in red_champs]

            # Calculate aggregates
            blue_avg = np.mean(blue_winrates)
            red_avg = np.mean(red_winrates)
            blue_max = np.max(blue_winrates)
            red_max = np.max(red_winrates)
            blue_min = np.min(blue_winrates)
            red_min = np.min(red_winrates)
            wr_diff = blue_avg - red_avg

            win_rate_features.append([
                blue_avg, red_avg,
                blue_max, red_max,
                blue_min, red_min,
                wr_diff
            ])

            if (idx + 1) % 1000 == 0:
                logger.info(f"  Processed {idx + 1}/{len(X_champs)} matches...")

        win_rate_features = np.array(win_rate_features)

        # Combine champion IDs + win rate features
        X = np.hstack([win_rate_features, X_champs])

        logger.info(f"\n✓ Feature engineering complete")
        logger.info(f"  Feature shape: {X.shape}")
        logger.info(f"  Features: 7 win rate stats + 10 champion IDs = 17 total")

        # Data distribution
        logger.info(f"\nTarget distribution:")
        blue_wins = np.sum(y == 1)
        red_wins = np.sum(y == 0)
        logger.info(f"  Blue wins: {blue_wins} ({blue_wins / len(y) * 100:.1f}%)")
        logger.info(f"  Red wins: {red_wins} ({red_wins / len(y) * 100:.1f}%)")

        return X, y, len(df)

    def _build_champion_encoder(self, df: pd.DataFrame):
        """Build champion ID <-> Name encoder from data"""
        logger.info("\nBuilding champion encoder...")

        # Get all unique champion IDs
        champ_cols = [
            'blue_champ_1', 'blue_champ_2', 'blue_champ_3', 'blue_champ_4', 'blue_champ_5',
            'red_champ_1', 'red_champ_2', 'red_champ_3', 'red_champ_4', 'red_champ_5'
        ]

        all_champ_ids = set()
        for col in champ_cols:
            all_champ_ids.update(df[col].unique())

        # Map IDs to names using champion stats
        # First, build reverse lookup
        champ_id_to_name = {}
        for champ_name, stats in self.champion_stats.items():
            champ_id = stats.get('id')
            if champ_id:
                champ_id_to_name[champ_id] = champ_name

        # Build encoders
        self.champion_to_id = {}
        self.id_to_champion = {}

        for champ_id in all_champ_ids:
            champ_name = champ_id_to_name.get(int(champ_id), f"Champion_{int(champ_id)}")
            self.champion_to_id[champ_name] = int(champ_id)
            self.id_to_champion[int(champ_id)] = champ_name

        logger.info(f"✓ Built encoder for {len(self.champion_to_id)} champions")

    def train_model(self, X_train, y_train, X_test, y_test):
        """Train Random Forest model for champion matchup prediction"""
        logger.info("\n" + "=" * 80)
        logger.info("TRAINING CHAMPION MATCHUP PREDICTOR")
        logger.info("=" * 80)

        # Use same RF params as win predictor for consistency
        rf_params = TRAINING_CONFIG['rf_params'].copy()
        logger.info(f"\nParameters: {rf_params}")

        self.model = RandomForestClassifier(**rf_params)

        logger.info("\nTraining model...")
        self.model.fit(X_train, y_train)

        # Evaluate
        logger.info("\nEvaluating model...")
        y_pred = self.model.predict(X_test)
        y_pred_proba = self.model.predict_proba(X_test)[:, 1]

        accuracy = accuracy_score(y_test, y_pred)
        roc_auc = roc_auc_score(y_test, y_pred_proba)

        logger.info(f"\n✓ Training complete!")
        logger.info(f"  Accuracy: {accuracy:.4f} ({accuracy * 100:.2f}%)")
        logger.info(f"  ROC-AUC: {roc_auc:.4f}")

        # Detailed metrics
        logger.info(f"\nClassification Report:")
        print(classification_report(y_test, y_pred, target_names=['Red Win', 'Blue Win']))

        logger.info(f"\nConfusion Matrix:")
        print(confusion_matrix(y_test, y_pred))

        # Feature importance (top features)
        logger.info(f"\nTop 10 Most Important Features:")
        feature_names = [
            'blue_avg_wr', 'red_avg_wr', 'blue_max_wr', 'red_max_wr',
            'blue_min_wr', 'red_min_wr', 'wr_diff',
            'blue_c1', 'blue_c2', 'blue_c3', 'blue_c4', 'blue_c5',
            'red_c1', 'red_c2', 'red_c3', 'red_c4', 'red_c5'
        ]

        importances = self.model.feature_importances_
        indices = np.argsort(importances)[::-1][:10]

        for i, idx in enumerate(indices, 1):
            logger.info(f"  {i}. {feature_names[idx]}: {importances[idx]:.4f}")

        return accuracy, roc_auc

    def save_model(self, accuracy: float, roc_auc: float, matches_count: int):
        """Save trained model with encoder and metadata"""
        logger.info("\n" + "=" * 80)
        logger.info("SAVING MODEL")
        logger.info("=" * 80)

        # Backup old model
        if CHAMPION_PREDICTOR_PATH.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = MODEL_BACKUP_DIR / f"champion_predictor_{timestamp}.pkl"
            import shutil
            shutil.copy(CHAMPION_PREDICTOR_PATH, backup_path)
            logger.info(f"  Backed up old model to: {backup_path.name}")

        # Package model with encoder
        model_package = {
            'model': self.model,
            'champion_to_id': self.champion_to_id,
            'id_to_champion': self.id_to_champion,
            'metadata': {
                'accuracy': float(accuracy),
                'roc_auc': float(roc_auc),
                'matches_count': int(matches_count),
                'features': 17,
                'feature_description': '7 win rate stats + 10 champion IDs',
                'timestamp': datetime.now().isoformat(),
                'version': '2.0'
            }
        }

        # Save with joblib (better compatibility)
        joblib.dump(model_package, CHAMPION_PREDICTOR_PATH)
        logger.info(f"✓ Saved model to: {CHAMPION_PREDICTOR_PATH}")

        # Also save performance separately for tracking
        performance = {
            'model': 'champion_matchup',
            'accuracy': float(accuracy),
            'roc_auc': float(roc_auc),
            'matches_count': int(matches_count),
            'timestamp': datetime.now().isoformat()
        }

        perf_path = CHAMPION_PREDICTOR_PATH.parent / 'champion_matchup_performance.json'
        with open(perf_path, 'w') as f:
            json.dump(performance, f, indent=2)

        logger.info(f"✓ Saved performance metrics to: {perf_path.name}")


def main():
    """Main training pipeline"""
    logger.info("\n" + "=" * 80)
    logger.info("CHAMPION MATCHUP PREDICTOR TRAINING")
    logger.info("ENHANCED WITH WIN RATE FEATURES")
    logger.info("=" * 80)

    trainer = ChampionMatchupTrainer()

    # Load champion stats
    trainer.load_champion_stats()

    # Load and prepare data
    X, y, total_matches = trainer.load_and_prepare_data()

    # Train/Test split
    logger.info("\n" + "=" * 80)
    logger.info("SPLITTING DATA")
    logger.info("=" * 80)

    test_size = TRAINING_CONFIG['test_size']
    random_state = TRAINING_CONFIG['random_state']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        random_state=random_state,
        stratify=y
    )

    logger.info(f"\nTrain/Test Split ({int((1-test_size)*100)}/{int(test_size*100)}):")
    logger.info(f"  Training set: {len(X_train)} matches")
    logger.info(f"  Test set: {len(X_test)} matches")

    # Train model
    accuracy, roc_auc = trainer.train_model(X_train, y_train, X_test, y_test)

    # Save model
    trainer.save_model(accuracy, roc_auc, total_matches)

    # Final summary
    logger.info("\n" + "=" * 80)
    logger.info("TRAINING COMPLETE!")
    logger.info("=" * 80)
    logger.info(f"\nChampion Matchup Predictor:")
    logger.info(f"  Accuracy: {accuracy * 100:.2f}%")
    logger.info(f"  ROC-AUC: {roc_auc:.4f}")
    logger.info(f"  Trained on: {total_matches} matches")
    logger.info(f"  Features: 17 (7 win rate stats + 10 champion IDs)")
    logger.info(f"\nModel saved to: {CHAMPION_PREDICTOR_PATH}")

    # Quality check
    if accuracy < 0.48:
        logger.warning("\n⚠️  WARNING: Accuracy < 48% - worse than random!")
        logger.warning("   This indicates a problem with the data or features.")
        return 1
    elif accuracy < 0.55:
        logger.warning("\n⚠️  WARNING: Accuracy < 55% - still low")
        logger.warning("   Consider adding more features or collecting more data.")
    else:
        logger.info("\n✓ Accuracy looks good (>= 55%)")
        logger.info("  Model should provide useful predictions.")

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
