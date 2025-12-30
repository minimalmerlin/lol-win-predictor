"""
ML Model Loading Service
Handles loading and caching of all ML models and data
"""

import json
from pathlib import Path
from typing import Optional, Dict

from api.core.logging import logger

# Import model classes from parent directory
import sys
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from champion_matchup_predictor import ChampionMatchupPredictor
from win_prediction_model import WinPredictionModel
from game_state_predictor import GameStatePredictor
from intelligent_item_recommender import IntelligentItemRecommender
from riot_live_client import RiotLiveClient
from dynamic_build_generator import DynamicBuildGenerator


class MLEngine:
    """
    Manages all ML models and data loading
    Singleton pattern - only one instance exists
    """

    def __init__(self):
        # ML Models
        self.champion_predictor: Optional[ChampionMatchupPredictor] = None
        self.win_predictor: Optional[WinPredictionModel] = None
        self.game_state_predictor: Optional[GameStatePredictor] = None

        # Data
        self.champion_stats: Optional[Dict] = None
        self.item_builds: Optional[Dict] = None
        self.best_teammates: Optional[Dict] = None

        # Services
        self.item_recommender: Optional[IntelligentItemRecommender] = None
        self.riot_live_client: Optional[RiotLiveClient] = None
        self.build_generator: Optional[DynamicBuildGenerator] = None

    async def load_all_models(self):
        """Load all ML models and data on startup"""
        logger.info("🚀 Loading models...")

        # Champion Stats (from PostgreSQL) - LOAD FIRST (needed by other models)
        try:
            from api.core.database import get_champion_stats
            self.champion_stats = get_champion_stats()
            logger.info(f"✓ Champion Stats loaded from DB ({len(self.champion_stats)} champions)")
        except Exception as e:
            logger.error(f"❌ Failed to load Champion Stats from DB: {e}")
            raise RuntimeError("Database required for champion stats. Check SUPABASE_URL.")

        # Champion Matchup Predictor (needs champion_stats)
        try:
            self.champion_predictor = ChampionMatchupPredictor()
            self.champion_predictor.load_model('./models/champion_predictor.pkl', champion_stats=self.champion_stats)
            logger.info("✓ Champion Predictor loaded")
        except Exception as e:
            logger.error(f"❌ Failed to load Champion Predictor: {e}")

        # Win Prediction Model (try RF, fallback to LR)
        try:
            self.win_predictor = WinPredictionModel()
            # Try Random Forest first (best accuracy but large file)
            try:
                self.win_predictor.load_model('./models/win_predictor_rf.pkl')
                logger.info("✓ Win Predictor loaded (Random Forest)")
            except:
                # Fallback to Linear Regression (smaller file, still good)
                self.win_predictor.load_model('./models/win_predictor_lr.pkl')
                logger.info("✓ Win Predictor loaded (Linear Regression - fallback)")
        except Exception as e:
            logger.error(f"❌ Failed to load Win Predictor: {e}")

        # Game State Predictor (NEW - 79.28% accuracy with timeline data)
        try:
            self.game_state_predictor = GameStatePredictor()
            self.game_state_predictor.load_model('./models/game_state_predictor.pkl')
            logger.info(f"✓ Game State Predictor loaded (Accuracy: {self.game_state_predictor.metadata.get('accuracy', 0)*100:.2f}%)")
        except Exception as e:
            logger.error(f"❌ Failed to load Game State Predictor: {e}")

        # Item Builds (from PostgreSQL)
        try:
            from api.core.database import get_item_builds
            self.item_builds = get_item_builds()
            if len(self.item_builds) == 0:
                logger.warning("⚠️  Item builds empty (match_items table not yet implemented)")
            else:
                logger.info(f"✓ Item Builds loaded from DB ({len(self.item_builds)} champions)")
        except Exception as e:
            logger.warning(f"⚠️  Item builds not available: {e}")

        # Intelligent Item Recommender (needs champion_stats and item_builds)
        try:
            self.item_recommender = IntelligentItemRecommender(
                data_dir='./data/champion_data',
                champion_stats=self.champion_stats,
                item_builds=self.item_builds
            )
            logger.info("✓ Intelligent Item Recommender loaded")
        except Exception as e:
            logger.error(f"❌ Failed to load Intelligent Item Recommender: {e}")

        # Best Teammates (from PostgreSQL)
        try:
            from api.core.database import get_best_teammates
            self.best_teammates = get_best_teammates()
            logger.info(f"✓ Best Teammates loaded from DB ({len(self.best_teammates)} champions)")
        except Exception as e:
            logger.error(f"❌ Failed to load Best Teammates from DB: {e}")
            self.best_teammates = {}  # Empty fallback (non-critical feature)

        # Riot Live Client
        try:
            self.riot_live_client = RiotLiveClient()
            logger.info("✓ Riot Live Client initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Riot Live Client: {e}")

        # Dynamic Build Generator (needs champion_stats and item_builds)
        try:
            self.build_generator = DynamicBuildGenerator(
                data_dir='./data/champion_data',
                champion_stats=self.champion_stats,
                item_builds=self.item_builds
            )
            logger.info("✓ Dynamic Build Generator initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Build Generator: {e}")

        logger.info("🎉 All models loaded successfully!")

    def get_health_status(self) -> Dict:
        """Get health status of all loaded models"""
        return {
            "champion_predictor": self.champion_predictor is not None,
            "win_predictor": self.win_predictor is not None,
            "game_state_predictor": self.game_state_predictor is not None and self.game_state_predictor.is_loaded,
            "champion_stats": self.champion_stats is not None,
            "item_builds": self.item_builds is not None,
            "item_recommender": self.item_recommender is not None,
            "best_teammates": self.best_teammates is not None
        }


# Global ML Engine instance (singleton)
ml_engine = MLEngine()
