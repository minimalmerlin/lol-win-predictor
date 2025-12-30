"""
Vercel Serverless Function - Champion Matchup Prediction
========================================================
Predicts win probability based on champion team compositions using ML models.
"""

import json
import os
import sys
from pathlib import Path
from flask import Flask, jsonify, request
from flask_cors import CORS

# Add parent directory to path to import modules
base_dir = Path(__file__).parent.parent
sys.path.insert(0, str(base_dir))

try:
    from champion_matchup_predictor import ChampionMatchupPredictor
except ImportError as e:
    print(f"Import error: {e}")
    ChampionMatchupPredictor = None

app = Flask(__name__)
CORS(app)

# Global model instance (cached across invocations in Vercel)
_predictor = None

def load_predictor():
    """Load the champion matchup predictor model (cached)"""
    global _predictor
    
    if _predictor is not None:
        return _predictor
    
    if ChampionMatchupPredictor is None:
        print("ChampionMatchupPredictor not available")
        return None
    
    try:
        model_path = base_dir / 'models' / 'champion_predictor.pkl'
        
        if not model_path.exists():
            print(f"Model not found at {model_path}")
            return None
        
        predictor = ChampionMatchupPredictor()
        predictor.load_model(str(model_path))
        _predictor = predictor
        print(f"✓ Predictor loaded successfully")
        return predictor
    except Exception as e:
        print(f"Error loading predictor: {e}")
        import traceback
        traceback.print_exc()
        return None

@app.route('/', methods=['POST'], defaults={'path': ''})
@app.route('/<path:path>', methods=['POST'])
def handler(path=''):
    """
    Vercel Serverless Function Handler
    
    Expected JSON body:
    {
        "blue_champions": ["MissFortune", "Lux", ...],
        "red_champions": ["Caitlyn", "Morgana", ...]
    }
    """
    try:
        # Get JSON body
        if request.is_json:
            body = request.get_json()
        else:
            body_data = request.data.decode('utf-8') if request.data else '{}'
            body = json.loads(body_data)
        
        blue_champions = body.get('blue_champions', [])
        red_champions = body.get('red_champions', [])
        
        # Validate input
        if not blue_champions or not red_champions:
            return jsonify({
                "error": "Missing blue_champions or red_champions",
                "detail": "Both blue_champions and red_champions must be provided as arrays"
            }), 400
        
        if not isinstance(blue_champions, list) or not isinstance(red_champions, list):
            return jsonify({
                "error": "Invalid input",
                "detail": "blue_champions and red_champions must be arrays"
            }), 400
        
        # Load predictor
        predictor = load_predictor()
        
        if predictor is None:
            return jsonify({
                "error": "Model not available",
                "detail": "Champion predictor model could not be loaded. Please check server logs."
            }), 503
        
        # Make prediction
        result = predictor.predict(
            blue_champions=blue_champions,
            red_champions=red_champions
        )
        
        # Return response in expected format
        return jsonify({
            "blue_win_probability": result['blue_win_probability'],
            "red_win_probability": result['red_win_probability'],
            "prediction": result['prediction'],
            "confidence": result['confidence'],
            "details": {
                "blue_avg_winrate": result['blue_avg_winrate'],
                "red_avg_winrate": result['red_avg_winrate'],
                "model": "champion_matchup",
                "accuracy": "61.6%"
            }
        })
        
    except ValueError as e:
        # User input errors
        return jsonify({
            "error": "Invalid request",
            "detail": str(e)
        }), 400
        
    except Exception as e:
        # Server errors
        print(f"Prediction error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "error": "Internal server error",
            "detail": f"An error occurred during prediction: {str(e)}"
        }), 500

