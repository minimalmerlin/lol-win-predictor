"""
Win Prediction Model
====================
Predicts win probability based on in-game state (kills, gold, towers, etc.)
"""

import pickle
import logging
from typing import Dict
import joblib

logger = logging.getLogger(__name__)


class WinPredictionModel:
    """Predicts win probability based on current game state"""

    def __init__(self):
        self.model = None
        self.model_type = None  # 'rf' (Random Forest) or 'lr' (Logistic Regression)

    def load_model(self, model_path: str):
        """Load the trained win prediction model
        
        Tries joblib first (better compatibility), falls back to pickle for legacy models.
        """
        try:
            # Try joblib first (better cross-version compatibility)
            try:
                data = joblib.load(model_path)
                logger.debug(f"Loaded model using joblib from {model_path}")
            except Exception as joblib_error:
                # Fallback to pickle for legacy models
                logger.warning(f"joblib failed, trying pickle: {joblib_error}")
                with open(model_path, 'rb') as f:
                    data = pickle.load(f)
                logger.debug(f"Loaded model using pickle from {model_path}")

            # Handle different formats
            if isinstance(data, dict):
                self.model = data.get('model')
            else:
                self.model = data

            # Detect model type from path
            if 'rf' in model_path.lower():
                self.model_type = 'rf'
            else:
                self.model_type = 'lr'

            if self.model is None:
                raise ValueError(f"Model not found in loaded data from {model_path}")

            logger.info(f"✓ Win Prediction Model loaded from {model_path} (type: {self.model_type})")

        except Exception as e:
            logger.error(f"Failed to load win predictor from {model_path}: {e}")
            raise

    def predict(self, game_state: Dict) -> Dict:
        """
        Predict win probability based on current game state

        Args:
            game_state: Dict with game state features:
                - game_duration: Game time in minutes
                - blue_kills, blue_deaths, blue_assists: Blue team KDA
                - blue_gold: Blue team total gold
                - blue_towers, blue_dragons, blue_barons: Blue team objectives
                - blue_vision_score: Blue team vision score
                - red_kills, red_deaths, red_assists: Red team KDA
                - red_gold: Red team total gold
                - red_towers, red_dragons, red_barons: Red team objectives
                - red_vision_score: Red team vision score

        Returns:
            Dict with prediction results
        """
        if not self.model:
            raise ValueError("Model not loaded. Call load_model() first.")

        # Prepare feature vector (order matches training)
        features = [[
            game_state.get('game_duration', 20),
            game_state.get('blue_kills', 0),
            game_state.get('blue_deaths', 0),
            game_state.get('blue_assists', 0),
            game_state.get('blue_gold', 0),
            game_state.get('blue_towers', 0),
            game_state.get('blue_dragons', 0),
            game_state.get('blue_barons', 0),
            game_state.get('blue_vision_score', 0),
            game_state.get('red_kills', 0),
            game_state.get('red_deaths', 0),
            game_state.get('red_assists', 0),
            game_state.get('red_gold', 0),
            game_state.get('red_towers', 0),
            game_state.get('red_dragons', 0),
            game_state.get('red_barons', 0),
            game_state.get('red_vision_score', 0)
        ]]

        # Predict
        try:
            blue_win_prob = self.model.predict_proba(features)[0][1]
            red_win_prob = 1 - blue_win_prob
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            # Fallback based on gold advantage
            blue_gold = game_state.get('blue_gold', 0)
            red_gold = game_state.get('red_gold', 0)
            total_gold = blue_gold + red_gold
            if total_gold > 0:
                blue_win_prob = blue_gold / total_gold
                red_win_prob = red_gold / total_gold
            else:
                blue_win_prob = 0.5
                red_win_prob = 0.5

        # Calculate confidence
        confidence = self._calculate_confidence(blue_win_prob)

        # Generate prediction text
        winner = "Blue Team" if blue_win_prob > red_win_prob else "Red Team"
        prob = max(blue_win_prob, red_win_prob)
        prediction = f"{winner} is favored to win ({prob * 100:.1f}%)"

        return {
            'blue_win_probability': float(blue_win_prob),
            'red_win_probability': float(red_win_prob),
            'prediction': prediction,
            'confidence': confidence,
            'model_type': self.model_type
        }

    def _calculate_confidence(self, probability: float) -> str:
        """Calculate confidence level based on probability"""
        # Confidence based on probability difference from 50%
        prob_diff = abs(probability - 0.5)

        if prob_diff > 0.20:  # More than 70% or less than 30%
            return "High"
        elif prob_diff > 0.10:  # Between 60-70% or 30-40%
            return "Medium"
        else:
            return "Low"
