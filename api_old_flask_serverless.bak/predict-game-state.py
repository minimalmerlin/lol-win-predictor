"""
Vercel Serverless Function - Game State Prediction
===================================================
Predicts win probability based on real-time game state using ML models.

Model: Game State Predictor (79.28% accuracy)
Data Source: PostgreSQL (10,000 matches with timeline data)
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
    from game_state_predictor import GameStatePredictor
except ImportError as e:
    print(f"Import error: {e}")
    GameStatePredictor = None

app = Flask(__name__)
CORS(app)

# Global model instance (cached across invocations in Vercel)
_predictor = None

def load_predictor():
    """Load the game state predictor model (cached)"""
    global _predictor

    if _predictor is not None:
        return _predictor

    if GameStatePredictor is None:
        print("GameStatePredictor not available")
        return None

    try:
        model_path = base_dir / 'models' / 'game_state_predictor.pkl'

        if not model_path.exists():
            print(f"Model not found at {model_path}")
            return None

        predictor = GameStatePredictor()
        success = predictor.load_model(str(model_path))

        if not success:
            print("Failed to load predictor")
            return None

        _predictor = predictor
        print(f"✓ Game State Predictor loaded successfully")
        print(f"  Accuracy: {predictor.metadata.get('accuracy', 0)*100:.2f}%")
        print(f"  Snapshot time: {predictor.snapshot_time} minutes")

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
        "blue_gold": 25000,
        "red_gold": 23000,
        "blue_xp": 30000,
        "red_xp": 28000,
        "blue_level": 58,
        "red_level": 55,
        "blue_cs": 450,
        "red_cs": 420,
        "blue_kills": 12,
        "red_kills": 8,
        "blue_dragons": 2,
        "red_dragons": 1,
        "blue_barons": 0,
        "red_barons": 0,
        "blue_towers": 5,
        "red_towers": 3
    }
    """
    try:
        # Get JSON body
        if request.is_json:
            body = request.get_json()
        else:
            body_data = request.data.decode('utf-8') if request.data else '{}'
            body = json.loads(body_data)

        # Extract game state parameters (with defaults)
        blue_gold = body.get('blue_gold')
        red_gold = body.get('red_gold')
        blue_xp = body.get('blue_xp')
        red_xp = body.get('red_xp')
        blue_level = body.get('blue_level')
        red_level = body.get('red_level')
        blue_cs = body.get('blue_cs')
        red_cs = body.get('red_cs')
        blue_kills = body.get('blue_kills')
        red_kills = body.get('red_kills')

        # Optional parameters
        blue_dragons = body.get('blue_dragons', 0)
        red_dragons = body.get('red_dragons', 0)
        blue_barons = body.get('blue_barons', 0)
        red_barons = body.get('red_barons', 0)
        blue_towers = body.get('blue_towers', 0)
        red_towers = body.get('red_towers', 0)

        # Validate required parameters
        required = ['blue_gold', 'red_gold', 'blue_xp', 'red_xp',
                   'blue_level', 'red_level', 'blue_cs', 'red_cs',
                   'blue_kills', 'red_kills']

        missing = [param for param in required if body.get(param) is None]

        if missing:
            return jsonify({
                "error": "Missing required parameters",
                "detail": f"Missing: {', '.join(missing)}",
                "required": required
            }), 400

        # Validate types (must be numbers)
        try:
            blue_gold = int(blue_gold)
            red_gold = int(red_gold)
            blue_xp = int(blue_xp)
            red_xp = int(red_xp)
            blue_level = int(blue_level)
            red_level = int(red_level)
            blue_cs = int(blue_cs)
            red_cs = int(red_cs)
            blue_kills = int(blue_kills)
            red_kills = int(red_kills)
            blue_dragons = int(blue_dragons)
            red_dragons = int(red_dragons)
            blue_barons = int(blue_barons)
            red_barons = int(red_barons)
            blue_towers = int(blue_towers)
            red_towers = int(red_towers)
        except (ValueError, TypeError) as e:
            return jsonify({
                "error": "Invalid parameter types",
                "detail": "All parameters must be numbers"
            }), 400

        # Load predictor
        predictor = load_predictor()

        if predictor is None:
            return jsonify({
                "error": "Model not available",
                "detail": "Game state predictor model could not be loaded. Please check server logs."
            }), 503

        # Make prediction
        result = predictor.predict(
            blue_gold=blue_gold,
            red_gold=red_gold,
            blue_xp=blue_xp,
            red_xp=red_xp,
            blue_level=blue_level,
            red_level=red_level,
            blue_cs=blue_cs,
            red_cs=red_cs,
            blue_kills=blue_kills,
            red_kills=red_kills,
            blue_dragons=blue_dragons,
            red_dragons=red_dragons,
            blue_barons=blue_barons,
            red_barons=red_barons,
            blue_towers=blue_towers,
            red_towers=red_towers
        )

        # Return response
        return jsonify({
            "blue_win_probability": result['blue_win_probability'],
            "red_win_probability": result['red_win_probability'],
            "prediction": result['prediction'],
            "confidence": result['confidence'],
            "details": result['details']
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
