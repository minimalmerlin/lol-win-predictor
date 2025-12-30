"""
Vercel Serverless Function - Database Statistics
=================================================
Provides statistics about the training data and model performance.

Data Source: PostgreSQL (10,000 matches)
"""

import json
import sys
from pathlib import Path
from flask import Flask, jsonify, request
from flask_cors import CORS

# Add parent directory to path
base_dir = Path(__file__).parent.parent
sys.path.insert(0, str(base_dir))
sys.path.insert(0, str(base_dir / 'api'))

try:
    from utils.db import get_database_stats, test_connection, get_champion_winrate
except ImportError as e:
    print(f"Import error: {e}")
    get_database_stats = None
    test_connection = None

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'], defaults={'path': ''})
@app.route('/<path:path>', methods=['GET'])
def handler(path=''):
    """
    Get database and model statistics.

    Returns:
        {
            "database": {
                "matches": 10000,
                "champions": 100000,
                "snapshots": 29384,
                "size": "36 MB"
            },
            "models": {
                "game_state": {
                    "accuracy": 0.7928,
                    "roc_auc": 0.8780,
                    "snapshot_time": 20
                },
                "champion_matchup": {
                    "accuracy": 0.52
                }
            }
        }
    """
    try:
        # Test database connection
        if test_connection and not test_connection():
            return jsonify({
                "error": "Database unavailable",
                "detail": "Could not connect to PostgreSQL database"
            }), 503

        # Get database stats
        db_stats = {}
        if get_database_stats:
            db_stats = get_database_stats()

        # Load model performance files
        game_state_perf = {}
        champion_matchup_perf = {}

        try:
            perf_path = base_dir / 'models' / 'game_state_performance.json'
            if perf_path.exists():
                with open(perf_path, 'r') as f:
                    game_state_perf = json.load(f)
        except Exception as e:
            print(f"Could not load game state performance: {e}")

        try:
            perf_path = base_dir / 'models' / 'champion_matchup_performance.json'
            if perf_path.exists():
                with open(perf_path, 'r') as f:
                    champion_matchup_perf = json.load(f)
        except Exception as e:
            print(f"Could not load champion matchup performance: {e}")

        # Build response
        response = {
            "database": {
                "matches": db_stats.get('matches', 0),
                "champions": db_stats.get('champions', 0),
                "snapshots": db_stats.get('snapshots', 0),
                "size": db_stats.get('database_size', 'unknown'),
                "connection": "healthy"
            },
            "models": {
                "game_state": {
                    "accuracy": game_state_perf.get('accuracy', 0),
                    "roc_auc": game_state_perf.get('roc_auc', 0),
                    "snapshot_time": game_state_perf.get('snapshot_time', 20),
                    "trained_on": game_state_perf.get('matches_count', 0),
                    "timestamp": game_state_perf.get('timestamp', 'unknown')
                },
                "champion_matchup": {
                    "accuracy": champion_matchup_perf.get('accuracy', 0),
                    "trained_on": champion_matchup_perf.get('matches_count', 0),
                    "timestamp": champion_matchup_perf.get('timestamp', 'unknown')
                }
            },
            "api_version": "2.0.0",
            "data_source": "PostgreSQL"
        }

        return jsonify(response)

    except Exception as e:
        print(f"Stats error: {e}")
        import traceback
        traceback.print_exc()

        return jsonify({
            "error": "Internal server error",
            "detail": str(e)
        }), 500


@app.route('/champion/<int:champion_id>', methods=['GET'])
def champion_stats(champion_id):
    """
    Get statistics for a specific champion.

    Args:
        champion_id: Champion ID (e.g., 104 for Graves)

    Returns:
        {
            "champion_id": 104,
            "overall_winrate": 0.523,
            "blue_side_winrate": 0.518,
            "red_side_winrate": 0.527,
            "games_played": 450
        }
    """
    try:
        if not get_champion_winrate:
            return jsonify({
                "error": "Database utilities not available"
            }), 503

        # Get win rates
        overall_wr = get_champion_winrate(champion_id)
        blue_wr = get_champion_winrate(champion_id, 'blue')
        red_wr = get_champion_winrate(champion_id, 'red')

        if overall_wr is None:
            return jsonify({
                "error": "Champion not found",
                "detail": f"No data for champion ID {champion_id}"
            }), 404

        # Get games played
        from utils.db import execute_query

        games_query = """
            SELECT COUNT(*) as games
            FROM match_champions
            WHERE champion_id = %s
        """
        games_result = execute_query(games_query, (champion_id,))
        games_played = games_result[0]['games'] if games_result else 0

        return jsonify({
            "champion_id": champion_id,
            "overall_winrate": round(overall_wr, 4) if overall_wr else None,
            "blue_side_winrate": round(blue_wr, 4) if blue_wr else None,
            "red_side_winrate": round(red_wr, 4) if red_wr else None,
            "games_played": games_played
        })

    except Exception as e:
        print(f"Champion stats error: {e}")
        import traceback
        traceback.print_exc()

        return jsonify({
            "error": "Internal server error",
            "detail": str(e)
        }), 500
