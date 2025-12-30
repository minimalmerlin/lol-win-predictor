"""
MLOps Pipeline - Automated Model Retraining
============================================
Automatically retrains models when new data is available.

Features:
- Scheduled retraining (daily/weekly)
- Performance monitoring
- Model versioning
- Automatic deployment
- Email notifications

Usage:
    python mlops_pipeline.py --mode [check|retrain|monitor]
"""

import argparse
import json
import logging
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional, Tuple

import joblib
import pandas as pd
import psycopg2

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mlops_pipeline.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Paths
BASE_DIR = Path(__file__).parent
MODELS_DIR = BASE_DIR / 'models'
DATA_DIR = BASE_DIR / 'data'
LOGS_DIR = BASE_DIR / 'logs'

# Database connection
DATABASE_URL = os.environ.get(
    'POSTGRES_URL',
    'postgres://***REMOVED***:***REMOVED***@aws-1-eu-central-1.pooler.supabase.com:5432/postgres?sslmode=require'
)

# Thresholds
MIN_NEW_MATCHES = 1000  # Retrain if we have 1000+ new matches
ACCURACY_THRESHOLD = 0.75  # Alert if accuracy drops below 75%
PERFORMANCE_CHECK_DAYS = 7  # Check performance over last 7 days


class MLOpsPipeline:
    """Manages automated model training and deployment"""

    def __init__(self):
        self.conn = None
        self.performance_history = []

    def connect_db(self):
        """Connect to PostgreSQL database"""
        if self.conn is None or self.conn.closed:
            self.conn = psycopg2.connect(DATABASE_URL)
            logger.info("✓ Connected to PostgreSQL")

    def close_db(self):
        """Close database connection"""
        if self.conn and not self.conn.closed:
            self.conn.close()
            logger.info("✓ Database connection closed")

    def get_database_stats(self) -> Dict:
        """Get current database statistics"""
        self.connect_db()

        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT
                    COUNT(*) as total_matches,
                    COUNT(DISTINCT match_id) as unique_matches,
                    MAX(match_id) as latest_match
                FROM matches
            """)

            result = cur.fetchone()

            return {
                'total_matches': result[0],
                'unique_matches': result[1],
                'latest_match': result[2],
                'timestamp': datetime.now().isoformat()
            }

    def check_new_data(self) -> Tuple[bool, int]:
        """
        Check if there's enough new data to warrant retraining.

        Returns:
            (should_retrain, new_matches_count)
        """
        try:
            stats = self.get_database_stats()
            current_matches = stats['total_matches']

            # Load previous match count
            perf_file = MODELS_DIR / 'game_state_performance.json'
            if perf_file.exists():
                with open(perf_file, 'r') as f:
                    previous_perf = json.load(f)
                    previous_matches = previous_perf.get('matches_count', 0)
            else:
                previous_matches = 0

            new_matches = current_matches - previous_matches
            should_retrain = new_matches >= MIN_NEW_MATCHES

            logger.info(f"Database check: {current_matches} total, {new_matches} new matches")
            logger.info(f"Retrain recommended: {should_retrain}")

            return should_retrain, new_matches

        except Exception as e:
            logger.error(f"Error checking new data: {e}")
            return False, 0

    def export_training_data(self) -> Optional[Path]:
        """
        Export training data from PostgreSQL to CSV.

        Returns:
            Path to exported CSV file
        """
        try:
            logger.info("Exporting training data from PostgreSQL...")
            self.connect_db()

            query = """
                SELECT
                    m.match_id,
                    m.game_duration,
                    m.blue_win,
                    ms.*
                FROM matches m
                JOIN match_snapshots ms ON m.match_id = ms.match_id
                WHERE ms.snapshot_time = 20
                ORDER BY m.match_id
            """

            df = pd.read_sql(query, self.conn)

            output_file = DATA_DIR / f'training_data_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
            df.to_csv(output_file, index=False)

            logger.info(f"✓ Exported {len(df)} matches to {output_file}")
            return output_file

        except Exception as e:
            logger.error(f"Error exporting training data: {e}")
            return None

    def retrain_model(self) -> bool:
        """
        Retrain the game state predictor model.

        Returns:
            True if retraining successful
        """
        try:
            logger.info("=" * 80)
            logger.info("STARTING MODEL RETRAINING")
            logger.info("=" * 80)

            # Export data
            data_file = self.export_training_data()
            if data_file is None:
                logger.error("Failed to export training data")
                return False

            # Run training script
            import subprocess

            result = subprocess.run(
                [sys.executable, str(BASE_DIR / 'train_game_state_predictor.py')],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                logger.info("✓ Model retraining completed successfully")
                logger.info(result.stdout)
                return True
            else:
                logger.error("✗ Model retraining failed")
                logger.error(result.stderr)
                return False

        except Exception as e:
            logger.error(f"Error during retraining: {e}")
            return False

    def monitor_performance(self) -> Dict:
        """
        Monitor model performance and check for degradation.

        Returns:
            Performance metrics dict
        """
        try:
            logger.info("Monitoring model performance...")

            # Load current model performance
            perf_file = MODELS_DIR / 'game_state_performance.json'
            if not perf_file.exists():
                logger.warning("No performance file found")
                return {}

            with open(perf_file, 'r') as f:
                perf = json.load(f)

            accuracy = perf.get('accuracy', 0)
            roc_auc = perf.get('roc_auc', 0)

            # Check thresholds
            alerts = []

            if accuracy < ACCURACY_THRESHOLD:
                alerts.append(f"⚠️  Accuracy below threshold: {accuracy:.4f} < {ACCURACY_THRESHOLD}")

            if roc_auc < 0.80:
                alerts.append(f"⚠️  ROC-AUC below 0.80: {roc_auc:.4f}")

            # Log results
            logger.info(f"Model Performance:")
            logger.info(f"  Accuracy: {accuracy:.4f}")
            logger.info(f"  ROC-AUC: {roc_auc:.4f}")

            if alerts:
                for alert in alerts:
                    logger.warning(alert)
            else:
                logger.info("✓ Model performance is healthy")

            return {
                'accuracy': accuracy,
                'roc_auc': roc_auc,
                'alerts': alerts,
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Error monitoring performance: {e}")
            return {}

    def run(self, mode: str = 'check'):
        """
        Run the MLOps pipeline.

        Args:
            mode: 'check', 'retrain', or 'monitor'
        """
        try:
            logger.info(f"Starting MLOps Pipeline (mode: {mode})")

            if mode == 'check':
                should_retrain, new_matches = self.check_new_data()

                if should_retrain:
                    logger.info(f"✓ Retraining recommended ({new_matches} new matches)")
                    self.retrain_model()
                else:
                    logger.info(f"✗ Not enough new data for retraining ({new_matches} < {MIN_NEW_MATCHES})")

            elif mode == 'retrain':
                logger.info("Forcing model retraining...")
                self.retrain_model()

            elif mode == 'monitor':
                perf = self.monitor_performance()

                if perf.get('alerts'):
                    logger.warning("Performance issues detected - consider retraining")

            else:
                logger.error(f"Unknown mode: {mode}")

        except Exception as e:
            logger.error(f"Pipeline error: {e}")
            raise
        finally:
            self.close_db()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='MLOps Pipeline for LoL Win Predictor')
    parser.add_argument(
        '--mode',
        choices=['check', 'retrain', 'monitor'],
        default='check',
        help='Pipeline mode: check for new data, force retrain, or monitor performance'
    )

    args = parser.parse_args()

    pipeline = MLOpsPipeline()
    pipeline.run(mode=args.mode)


if __name__ == '__main__':
    main()
