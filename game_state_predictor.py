"""
Game State Win Predictor
=========================
Wrapper class for the trained game state prediction model.
Uses timeline data (10min, 15min, 20min snapshots) for real in-game predictions.

Model Accuracy: 79.28% (20-minute snapshot)
Trained on: 10,000 matches with timeline data
"""

import joblib
import numpy as np
import logging
from pathlib import Path
from typing import Dict, Optional, List

logger = logging.getLogger(__name__)


class GameStatePredictor:
    """
    Game State Win Predictor using the trained timeline model.
    
    This model predicts win probability based on in-game statistics
    at specific time points (10min, 15min, 20min).
    
    Accuracy: 79.28% at 20-minute mark
    ROC-AUC: 0.8780
    """
    
    def __init__(self):
        self.model = None
        self.feature_names: List[str] = []
        self.snapshot_time: int = 20  # Default: 20-minute snapshot
        self.metadata: Dict = {}
        self.is_loaded = False
    
    def load_model(self, model_path: str = './models/game_state_predictor.pkl') -> bool:
        """Load the trained game state predictor model"""
        try:
            model_package = joblib.load(model_path)
            
            self.model = model_package['model']
            self.feature_names = model_package['feature_names']
            self.snapshot_time = model_package.get('snapshot_time', 20)
            self.metadata = model_package.get('metadata', {})
            self.is_loaded = True
            
            logger.info(f"✓ Game State Predictor loaded from {model_path}")
            logger.info(f"  Snapshot time: {self.snapshot_time} minutes")
            logger.info(f"  Features: {len(self.feature_names)}")
            logger.info(f"  Accuracy: {self.metadata.get('accuracy', 0)*100:.2f}%")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to load Game State Predictor: {e}")
            self.is_loaded = False
            return False
    
    def predict(self, 
                blue_gold: int,
                red_gold: int,
                blue_xp: int,
                red_xp: int,
                blue_level: int,
                red_level: int,
                blue_cs: int,
                red_cs: int,
                blue_kills: int,
                red_kills: int,
                blue_dragons: int = 0,
                red_dragons: int = 0,
                blue_barons: int = 0,
                red_barons: int = 0,
                blue_towers: int = 0,
                red_towers: int = 0) -> Dict:
        """
        Predict win probability based on game state.
        
        Args:
            blue_gold: Blue team total gold
            red_gold: Red team total gold
            blue_xp: Blue team total XP
            red_xp: Red team total XP
            blue_level: Blue team average level
            red_level: Red team average level
            blue_cs: Blue team total CS
            red_cs: Red team total CS
            blue_kills: Blue team total kills
            red_kills: Red team total kills
            blue_dragons: Blue team dragon count
            red_dragons: Red team dragon count
            blue_barons: Blue team baron count
            red_barons: Red team baron count
            blue_towers: Blue team tower count
            red_towers: Red team tower count
            
        Returns:
            Dict with prediction results
        """
        if not self.is_loaded:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        # Calculate diffs
        gold_diff = blue_gold - red_gold
        xp_diff = blue_xp - red_xp
        kill_diff = blue_kills - red_kills
        
        # Build feature vector in the correct order
        snapshot_prefix = f't{self.snapshot_time}_'
        
        feature_values = {
            f'{snapshot_prefix}blue_gold': blue_gold,
            f'{snapshot_prefix}red_gold': red_gold,
            f'{snapshot_prefix}gold_diff': gold_diff,
            f'{snapshot_prefix}blue_xp': blue_xp,
            f'{snapshot_prefix}red_xp': red_xp,
            f'{snapshot_prefix}xp_diff': xp_diff,
            f'{snapshot_prefix}blue_level': blue_level,
            f'{snapshot_prefix}red_level': red_level,
            f'{snapshot_prefix}blue_cs': blue_cs,
            f'{snapshot_prefix}red_cs': red_cs,
            f'{snapshot_prefix}blue_dragons': blue_dragons,
            f'{snapshot_prefix}red_dragons': red_dragons,
            f'{snapshot_prefix}blue_barons': blue_barons,
            f'{snapshot_prefix}red_barons': red_barons,
            f'{snapshot_prefix}blue_towers': blue_towers,
            f'{snapshot_prefix}red_towers': red_towers,
            f'{snapshot_prefix}blue_kills': blue_kills,
            f'{snapshot_prefix}red_kills': red_kills,
            f'{snapshot_prefix}kill_diff': kill_diff,
        }
        
        # Build feature array in correct order
        X = np.array([[feature_values.get(fname, 0) for fname in self.feature_names]])
        
        # Predict
        blue_prob = float(self.model.predict_proba(X)[0][1])
        red_prob = 1 - blue_prob
        
        # Determine prediction text and confidence
        if blue_prob > 0.7:
            prediction = "Blue Team strongly favored"
            confidence = "high"
        elif blue_prob > 0.6:
            prediction = "Blue Team favored"
            confidence = "medium"
        elif blue_prob < 0.3:
            prediction = "Red Team strongly favored"
            confidence = "high"
        elif blue_prob < 0.4:
            prediction = "Red Team favored"
            confidence = "medium"
        else:
            prediction = "Even game"
            confidence = "low"
        
        return {
            'blue_win_probability': round(blue_prob, 4),
            'red_win_probability': round(red_prob, 4),
            'prediction': prediction,
            'confidence': confidence,
            'details': {
                'gold_diff': gold_diff,
                'xp_diff': xp_diff,
                'kill_diff': kill_diff,
                'tower_diff': blue_towers - red_towers,
                'dragon_diff': blue_dragons - red_dragons,
                'snapshot_time': self.snapshot_time,
                'model': 'game_state_predictor',
                'accuracy': f"{self.metadata.get('accuracy', 0)*100:.2f}%"
            }
        }
    
    def get_model_info(self) -> Dict:
        """Get model metadata"""
        return {
            'is_loaded': self.is_loaded,
            'snapshot_time': self.snapshot_time,
            'features': len(self.feature_names),
            'accuracy': self.metadata.get('accuracy', 0),
            'roc_auc': self.metadata.get('roc_auc', 0),
            'matches_trained': self.metadata.get('matches_count', 0),
            'version': self.metadata.get('version', 'unknown')
        }
