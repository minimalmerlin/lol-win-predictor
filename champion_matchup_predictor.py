"""
Champion Matchup Predictor
==========================
Predicts win probability based on champion team compositions.
"""

import pickle
import json
from pathlib import Path
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class ChampionMatchupPredictor:
    """Predicts win probability based on champion compositions"""

    def __init__(self):
        self.model = None
        self.champion_stats = {}
        self.champion_to_id = {}
        self.id_to_champion = {}

    def load_model(self, model_path: str):
        """Load the trained champion matchup prediction model"""
        try:
            # Try joblib first (modern scikit-learn models)
            try:
                import joblib
                data = joblib.load(model_path)
            except:
                # Fallback to pickle for older models
                with open(model_path, 'rb') as f:
                    data = pickle.load(f)

            # Handle different pickle formats
            if isinstance(data, dict):
                self.model = data.get('model')
                # Support both old and new key names
                self.champion_to_id = data.get('champion_to_id') or data.get('champion_encoder', {})
                self.id_to_champion = data.get('id_to_champion') or data.get('reverse_encoder', {})
            else:
                self.model = data

            logger.info(f"✓ Champion Matchup Predictor loaded from {model_path}")
            logger.info(f"  Model type: {type(self.model).__name__}")
            logger.info(f"  Champions loaded: {len(self.champion_to_id)}")

            # Load champion stats for additional insights
            stats_path = Path('./data/champion_data/champion_stats.json')
            if stats_path.exists():
                with open(stats_path, 'r') as f:
                    self.champion_stats = json.load(f)

        except Exception as e:
            logger.error(f"Failed to load champion predictor: {e}")
            raise

    def predict(self, blue_champions: List[str], red_champions: List[str]) -> Dict:
        """
        Predict win probability for a champion matchup

        Args:
            blue_champions: List of champion names for blue team (1-5 champions)
            red_champions: List of champion names for red team (1-5 champions)

        Returns:
            Dict with prediction results including win probabilities and confidence
        """
        if not self.model:
            raise ValueError("Model not loaded. Call load_model() first.")

        # Normalize champion names (handle spaces, capitalization)
        blue_champions = [self._normalize_champion_name(c) for c in blue_champions]
        red_champions = [self._normalize_champion_name(c) for c in red_champions]

        # Convert champion names to IDs with case-insensitive lookup
        try:
            blue_ids = [self.champion_to_id[self._find_champion_in_encoder(champ)] for champ in blue_champions]
            red_ids = [self.champion_to_id[self._find_champion_in_encoder(champ)] for champ in red_champions]
        except ValueError as e:
            # Re-raise ValueError with helpful message
            raise
        except KeyError as e:
            raise ValueError(f"Unknown champion in encoder: {e}")

        # Pad to 5 champions (use 0 for missing slots)
        blue_ids = (blue_ids + [0] * 5)[:5]
        red_ids = (red_ids + [0] * 5)[:5]

        # Calculate winrate features
        blue_winrates = [self._get_champion_winrate(c) for c in blue_champions]
        red_winrates = [self._get_champion_winrate(c) for c in red_champions]

        blue_avg_winrate = sum(blue_winrates) / len(blue_winrates) if blue_winrates else 0.5
        red_avg_winrate = sum(red_winrates) / len(red_winrates) if red_winrates else 0.5
        blue_max_winrate = max(blue_winrates) if blue_winrates else 0.5
        red_max_winrate = max(red_winrates) if red_winrates else 0.5
        blue_min_winrate = min(blue_winrates) if blue_winrates else 0.5
        red_min_winrate = min(red_winrates) if red_winrates else 0.5
        winrate_diff = blue_avg_winrate - red_avg_winrate

        # Create feature vector with 17 features:
        # [blue_avg_wr, red_avg_wr, blue_max_wr, red_max_wr, blue_min_wr, red_min_wr, wr_diff,
        #  blue_champ_0, blue_champ_1, blue_champ_2, blue_champ_3, blue_champ_4,
        #  red_champ_0, red_champ_1, red_champ_2, red_champ_3, red_champ_4]
        features = [[
            blue_avg_winrate, red_avg_winrate,
            blue_max_winrate, red_max_winrate,
            blue_min_winrate, red_min_winrate,
            winrate_diff,
            *blue_ids, *red_ids
        ]]

        # Predict
        try:
            blue_win_prob = self.model.predict_proba(features)[0][1]
            red_win_prob = 1 - blue_win_prob
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            # Fallback to champion win rates
            blue_win_prob = blue_avg_winrate
            red_win_prob = red_avg_winrate
            # Normalize
            total = blue_win_prob + red_win_prob
            blue_win_prob = blue_win_prob / total
            red_win_prob = red_win_prob / total

        # Calculate confidence based on team sizes and probability gap
        confidence = self._calculate_confidence(blue_win_prob, len(blue_champions), len(red_champions))

        # Generate prediction text
        winner = "Blue Team" if blue_win_prob > red_win_prob else "Red Team"
        prob = max(blue_win_prob, red_win_prob)
        prediction = f"{winner} has a {prob * 100:.1f}% chance to win"

        # Get champion winrates for details
        blue_avg_wr = self._calculate_team_winrate(blue_champions)
        red_avg_wr = self._calculate_team_winrate(red_champions)

        return {
            'blue_win_probability': float(blue_win_prob),
            'red_win_probability': float(red_win_prob),
            'prediction': prediction,
            'confidence': confidence,
            'blue_avg_winrate': float(blue_avg_wr),
            'red_avg_winrate': float(red_avg_wr)
        }

    def _normalize_champion_name(self, name: str) -> str:
        """Normalize champion name (remove spaces, preserve CamelCase)"""
        # Remove spaces and preserve CamelCase
        # If name has spaces, capitalize each word
        # If name is already CamelCase (no spaces), preserve it
        name = name.strip()
        
        # If it has spaces, join and capitalize each word
        if ' ' in name:
            normalized = ''.join(word.capitalize() for word in name.split())
        elif name.isupper():
            # ALL_CAPS -> convert to CamelCase
            normalized = name.capitalize()
        elif name.islower():
            # all_lower -> convert to CamelCase
            normalized = name.capitalize()
        else:
            # Already CamelCase - preserve as is
            normalized = name
        
        return normalized

    def _find_champion_in_encoder(self, champion_name: str) -> str:
        """Find champion in encoder with case-insensitive lookup"""
        # Try exact match first
        if champion_name in self.champion_to_id:
            return champion_name
        
        # Case-insensitive lookup
        champion_lower = champion_name.lower()
        for encoded_name in self.champion_to_id.keys():
            if encoded_name.lower() == champion_lower:
                return encoded_name
        
        # If still not found, raise error with suggestions
        similar = [name for name in self.champion_to_id.keys() 
                  if champion_lower in name.lower() or name.lower() in champion_lower][:5]
        raise ValueError(
            f"Unknown champion: '{champion_name}'. "
            f"Similar champions: {similar if similar else 'None found'}"
        )

    def _get_champion_winrate(self, champion: str) -> float:
        """Get winrate for a single champion"""
        # Try exact match first
        if champion in self.champion_stats:
            return self.champion_stats[champion].get('win_rate', 0.5)
        
        # Case-insensitive lookup in stats
        champion_lower = champion.lower()
        for stat_name in self.champion_stats.keys():
            if stat_name.lower() == champion_lower:
                return self.champion_stats[stat_name].get('win_rate', 0.5)
        
        return 0.5

    def _calculate_team_winrate(self, champions: List[str]) -> float:
        """Calculate average winrate for a team of champions"""
        if not champions:
            return 0.5

        winrates = [self._get_champion_winrate(c) for c in champions]
        return sum(winrates) / len(winrates) if winrates else 0.5

    def _calculate_confidence(self, probability: float, blue_count: int, red_count: int) -> str:
        """Calculate confidence level based on probability gap and team sizes"""
        # Lower confidence if teams are incomplete
        if blue_count < 5 or red_count < 5:
            return "Low"

        # Confidence based on probability difference from 50%
        prob_diff = abs(probability - 0.5)

        if prob_diff > 0.15:  # More than 65% or less than 35%
            return "High"
        elif prob_diff > 0.08:  # Between 58-65% or 35-42%
            return "Medium"
        else:
            return "Low"
