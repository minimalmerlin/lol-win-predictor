"""
Game State Win Predictor Training Script
==========================================
Trains a REAL game state predictor using timeline data (10min, 15min, 20min snapshots).

This is THE MEISTERWERK - predicting who will win based on actual in-game performance!

Features Used (per snapshot):
- Gold (total, diff)
- XP (total, diff)
- Level (total)
- CS (minions + jungle)
- Objectives (Dragons, Barons, Towers)
- Kills (total, diff)

Target Accuracy: >70% (significantly better than draft phase ~52%)

The model learns:
- How gold advantages translate to wins
- When kill deficits can be overcome
- How objectives (dragons, barons) impact victory
- Comeback mechanics (teams behind at 10min but winning at 20min)

Author: Victory AI System
Date: 2025-12-29
"""

import pandas as pd
import numpy as np
import joblib
import json
import logging
from pathlib import Path
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report, confusion_matrix
from typing import List, Tuple

from config import (
    MODEL_BACKUP_DIR,
    TRAINING_CONFIG
)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Paths
TIMELINE_DATA_PATH = Path('data/training_data_with_timeline.csv')
GAME_STATE_MODEL_PATH = Path('models/game_state_predictor.pkl')
GAME_STATE_PERF_PATH = Path('models/game_state_performance.json')


class GameStatePredictorTrainer:
    """Trains the Game State Win Prediction Model"""

    def __init__(self, snapshot_time: int = 15):
        """
        Args:
            snapshot_time: Which snapshot to use (10, 15, or 20 minutes)
        """
        self.snapshot_time = snapshot_time
        self.model = None
        self.feature_names = []

    def load_and_prepare_data(self) -> Tuple[np.ndarray, np.ndarray, int]:
        """Load timeline data and prepare features"""
        logger.info("=" * 80)
        logger.info("LOADING TIMELINE TRAINING DATA")
        logger.info("=" * 80)

        if not TIMELINE_DATA_PATH.exists():
            raise FileNotFoundError(
                f"Timeline data not found at {TIMELINE_DATA_PATH}. "
                "Run fetch_matches_with_timeline.py first!"
            )

        df = pd.read_csv(TIMELINE_DATA_PATH)
        logger.info(f"✓ Loaded {len(df)} matches with timeline data")
        logger.info(f"  Total columns: {len(df.columns)}")

        # Filter matches that have data at our snapshot time
        snapshot_prefix = f't{self.snapshot_time}_'
        snapshot_cols = [col for col in df.columns if snapshot_prefix in col]

        logger.info(f"\nUsing {self.snapshot_time}-minute snapshot")
        logger.info(f"  Found {len(snapshot_cols)} snapshot features")

        # Remove rows with missing snapshot data
        df_filtered = df.dropna(subset=[f'{snapshot_prefix}blue_gold'])
        logger.info(f"  Matches with {self.snapshot_time}min data: {len(df_filtered)}")

        if len(df_filtered) < 100:
            raise ValueError(
                f"Not enough matches with {self.snapshot_time}min data. "
                f"Need at least 100, got {len(df_filtered)}"
            )

        # Define features to use
        feature_cols = [
            # Gold features
            f'{snapshot_prefix}blue_gold',
            f'{snapshot_prefix}red_gold',
            f'{snapshot_prefix}gold_diff',

            # XP features
            f'{snapshot_prefix}blue_xp',
            f'{snapshot_prefix}red_xp',
            f'{snapshot_prefix}xp_diff',

            # Level
            f'{snapshot_prefix}blue_level',
            f'{snapshot_prefix}red_level',

            # CS
            f'{snapshot_prefix}blue_cs',
            f'{snapshot_prefix}red_cs',

            # Objectives
            f'{snapshot_prefix}blue_dragons',
            f'{snapshot_prefix}red_dragons',
            f'{snapshot_prefix}blue_barons',
            f'{snapshot_prefix}red_barons',
            f'{snapshot_prefix}blue_towers',
            f'{snapshot_prefix}red_towers',

            # Kills
            f'{snapshot_prefix}blue_kills',
            f'{snapshot_prefix}red_kills',
            f'{snapshot_prefix}kill_diff',
        ]

        # Check all features exist
        missing_cols = set(feature_cols) - set(df_filtered.columns)
        if missing_cols:
            logger.warning(f"Missing features: {missing_cols}")
            feature_cols = [col for col in feature_cols if col in df_filtered.columns]

        self.feature_names = feature_cols

        logger.info(f"\nFinal feature set ({len(feature_cols)} features):")
        for col in feature_cols:
            print(f"  - {col}")

        # Prepare X and y
        X = df_filtered[feature_cols].values
        y = df_filtered['blue_win'].values

        logger.info(f"\nFeature matrix shape: {X.shape}")
        logger.info(f"\nTarget distribution:")
        blue_wins = np.sum(y == 1)
        red_wins = np.sum(y == 0)
        logger.info(f"  Blue wins: {blue_wins} ({blue_wins / len(y) * 100:.1f}%)")
        logger.info(f"  Red wins: {red_wins} ({red_wins / len(y) * 100:.1f}%)")

        # Feature statistics
        logger.info(f"\nFeature Statistics:")
        df_stats = pd.DataFrame(X, columns=feature_cols)
        logger.info(f"  Gold diff range: [{df_stats[f'{snapshot_prefix}gold_diff'].min():.0f}, "
                   f"{df_stats[f'{snapshot_prefix}gold_diff'].max():.0f}]")
        logger.info(f"  Kill diff range: [{df_stats[f'{snapshot_prefix}kill_diff'].min():.0f}, "
                   f"{df_stats[f'{snapshot_prefix}kill_diff'].max():.0f}]")

        return X, y, len(df_filtered)

    def train_random_forest(self, X_train, y_train, X_test, y_test):
        """Train Random Forest model"""
        logger.info("\n" + "=" * 80)
        logger.info("TRAINING RANDOM FOREST (GAME STATE PREDICTOR)")
        logger.info("=" * 80)

        # Use optimized RF params
        rf_params = TRAINING_CONFIG['rf_params'].copy()
        logger.info(f"\nParameters: {rf_params}")

        self.model = RandomForestClassifier(**rf_params)

        logger.info("\nTraining...")
        self.model.fit(X_train, y_train)

        # Evaluate
        logger.info("\nEvaluating...")
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

        # Feature importance
        logger.info(f"\nTop 10 Most Important Features:")
        importances = self.model.feature_importances_
        indices = np.argsort(importances)[::-1][:10]

        for i, idx in enumerate(indices, 1):
            logger.info(f"  {i}. {self.feature_names[idx]}: {importances[idx]:.4f}")

        return accuracy, roc_auc

    def train_gradient_boosting(self, X_train, y_train, X_test, y_test):
        """Train Gradient Boosting model (often better for tabular data)"""
        logger.info("\n" + "=" * 80)
        logger.info("TRAINING GRADIENT BOOSTING (Alternative Model)")
        logger.info("=" * 80)

        gb_params = {
            'n_estimators': 100,
            'max_depth': 10,
            'learning_rate': 0.1,
            'subsample': 0.8,
            'random_state': 42
        }

        logger.info(f"\nParameters: {gb_params}")

        model = GradientBoostingClassifier(**gb_params)

        logger.info("\nTraining...")
        model.fit(X_train, y_train)

        # Evaluate
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1]

        accuracy = accuracy_score(y_test, y_pred)
        roc_auc = roc_auc_score(y_test, y_pred_proba)

        logger.info(f"\n✓ Training complete!")
        logger.info(f"  Accuracy: {accuracy:.4f} ({accuracy * 100:.2f}%)")
        logger.info(f"  ROC-AUC: {roc_auc:.4f}")

        return model, accuracy, roc_auc

    def save_model(self, accuracy: float, roc_auc: float, matches_count: int):
        """Save trained model and metadata"""
        logger.info("\n" + "=" * 80)
        logger.info("SAVING GAME STATE PREDICTOR")
        logger.info("=" * 80)

        # Backup old model
        if GAME_STATE_MODEL_PATH.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = MODEL_BACKUP_DIR / f"game_state_predictor_{timestamp}.pkl"
            import shutil
            shutil.copy(GAME_STATE_MODEL_PATH, backup_path)
            logger.info(f"  Backed up old model to: {backup_path.name}")

        # Package model
        model_package = {
            'model': self.model,
            'feature_names': self.feature_names,
            'snapshot_time': self.snapshot_time,
            'metadata': {
                'accuracy': float(accuracy),
                'roc_auc': float(roc_auc),
                'matches_count': int(matches_count),
                'features': len(self.feature_names),
                'snapshot_time_minutes': self.snapshot_time,
                'timestamp': datetime.now().isoformat(),
                'version': '1.0'
            }
        }

        # Save with joblib
        joblib.dump(model_package, GAME_STATE_MODEL_PATH)
        logger.info(f"✓ Saved model to: {GAME_STATE_MODEL_PATH}")

        # Save performance
        performance = {
            'model': 'game_state_predictor',
            'snapshot_time': self.snapshot_time,
            'accuracy': float(accuracy),
            'roc_auc': float(roc_auc),
            'matches_count': int(matches_count),
            'timestamp': datetime.now().isoformat()
        }

        with open(GAME_STATE_PERF_PATH, 'w') as f:
            json.dump(performance, f, indent=2)

        logger.info(f"✓ Saved performance to: {GAME_STATE_PERF_PATH.name}")


def main():
    """Main training pipeline"""
    logger.info("\n" + "=" * 80)
    logger.info("GAME STATE WIN PREDICTOR TRAINING")
    logger.info("THE MEISTERWERK - REAL IN-GAME PREDICTION")
    logger.info("=" * 80)

    # Train models at different snapshot times
    best_accuracy = 0
    best_snapshot = None

    for snapshot_time in [10, 15, 20]:
        logger.info(f"\n\n{'=' * 80}")
        logger.info(f"TRAINING MODEL FOR {snapshot_time}-MINUTE SNAPSHOT")
        logger.info(f"{'=' * 80}\n")

        try:
            trainer = GameStatePredictorTrainer(snapshot_time=snapshot_time)

            # Load data
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

            # Train Random Forest
            accuracy_rf, roc_auc_rf = trainer.train_random_forest(X_train, y_train, X_test, y_test)

            # Train Gradient Boosting
            model_gb, accuracy_gb, roc_auc_gb = trainer.train_gradient_boosting(X_train, y_train, X_test, y_test)

            # Use best model
            if accuracy_gb > accuracy_rf:
                logger.info(f"\n✓ Gradient Boosting performs better ({accuracy_gb:.2%} vs {accuracy_rf:.2%})")
                trainer.model = model_gb
                accuracy = accuracy_gb
                roc_auc = roc_auc_gb
            else:
                logger.info(f"\n✓ Random Forest performs better ({accuracy_rf:.2%} vs {accuracy_gb:.2%})")
                accuracy = accuracy_rf
                roc_auc = roc_auc_rf

            # Track best snapshot time
            if accuracy > best_accuracy:
                best_accuracy = accuracy
                best_snapshot = snapshot_time

                # Save best model
                trainer.save_model(accuracy, roc_auc, total_matches)

            logger.info(f"\n{snapshot_time}-Minute Model Summary:")
            logger.info(f"  Accuracy: {accuracy * 100:.2f}%")
            logger.info(f"  ROC-AUC: {roc_auc:.4f}")

        except Exception as e:
            logger.error(f"Failed to train {snapshot_time}min model: {e}")
            continue

    # Final summary
    logger.info("\n" + "=" * 80)
    logger.info("TRAINING COMPLETE - THE MEISTERWERK IS READY!")
    logger.info("=" * 80)

    if best_snapshot:
        logger.info(f"\n🏆 Best Model: {best_snapshot}-minute snapshot")
        logger.info(f"   Accuracy: {best_accuracy * 100:.2f}%")
        logger.info(f"\nModel saved to: {GAME_STATE_MODEL_PATH}")

        # Quality assessment
        if best_accuracy >= 0.70:
            logger.info("\n✅ EXCELLENT! Accuracy >= 70%")
            logger.info("   This is SIGNIFICANTLY better than draft phase (~52%)")
            logger.info("   The model learned real game state patterns!")
        elif best_accuracy >= 0.65:
            logger.info("\n✓ GOOD! Accuracy >= 65%")
            logger.info("  Better than draft phase, but room for improvement")
        elif best_accuracy >= 0.60:
            logger.info("\n⚠️  MODERATE. Accuracy >= 60%")
            logger.info("   Better than draft, but needs more data or features")
        else:
            logger.info("\n⚠️  WARNING: Accuracy < 60%")
            logger.info("   Need more training data or feature engineering")

    return 0 if best_accuracy >= 0.65 else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
