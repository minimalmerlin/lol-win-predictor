"""
Champion Detail Endpoint
Returns detailed stats, item builds, and synergies for a specific champion
"""
from flask import Flask, jsonify
from flask_cors import CORS
import json
import os
from difflib import get_close_matches

app = Flask(__name__)
CORS(app)

def load_champion_data():
    """Load all champion data files"""
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        data_dir = os.path.join(base_dir, 'data', 'champion_data')

        # Load champion stats
        with open(os.path.join(data_dir, 'champion_stats.json'), 'r', encoding='utf-8') as f:
            stats = json.load(f)

        # Load item builds
        with open(os.path.join(data_dir, 'item_builds.json'), 'r', encoding='utf-8') as f:
            builds = json.load(f)

        # Load best teammates
        with open(os.path.join(data_dir, 'best_teammates.json'), 'r', encoding='utf-8') as f:
            teammates = json.load(f)

        return stats, builds, teammates
    except Exception as e:
        print(f"Error loading champion data: {e}")
        return {}, {}, {}

def find_champion_match(champion_name, available_champions):
    """Find the best match for a champion name (fuzzy matching)"""
    # Exact match (case-insensitive)
    for champ in available_champions:
        if champ.lower() == champion_name.lower():
            return champ, 1.0, True

    # Fuzzy match
    matches = get_close_matches(champion_name, available_champions, n=1, cutoff=0.6)
    if matches:
        return matches[0], 0.8, False

    return None, 0.0, False

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def handler(path):
    # Extract champion name from path (remove leading slash if present)
    champion_name = path.strip('/') if path else ''

    if not champion_name:
        return jsonify({"error": "Champion name is required"}), 400

    # Load all data
    stats_data, builds_data, teammates_data = load_champion_data()

    if not stats_data:
        return jsonify({"error": "Failed to load champion data"}), 500

    # Find champion (with fuzzy matching)
    matched_champion, match_quality, exact_match = find_champion_match(
        champion_name,
        list(stats_data.keys())
    )

    if not matched_champion:
        return jsonify({
            "error": "Champion not found",
            "searched_for": champion_name
        }), 404

    # Get champion stats
    champion_stats = stats_data.get(matched_champion, {})

    # Get item builds
    champion_builds = builds_data.get(matched_champion, {})
    if isinstance(champion_builds, dict):
        top_builds = champion_builds.get('top_builds', [])
        total_games = champion_builds.get('total_games', 0)
        all_builds_count = champion_builds.get('total_unique_builds', len(top_builds))
    else:
        top_builds = []
        total_games = 0
        all_builds_count = 0

    # Get best teammates
    champion_teammates = teammates_data.get(matched_champion, [])

    # Build response
    response = {
        "champion": matched_champion,
        "match_quality": match_quality,
        "exact_match": exact_match,
        "stats": {
            "games": champion_stats.get('games', 0),
            "wins": champion_stats.get('wins', 0),
            "losses": champion_stats.get('losses', 0),
            "win_rate": champion_stats.get('win_rate', 0.0),
            "picks": champion_stats.get('picks', 0),
            "bans": champion_stats.get('bans', 0)
        },
        "item_builds": {
            "champion": matched_champion,
            "found": len(top_builds) > 0,
            "total_games": total_games,
            "top_builds": top_builds[:10],  # Limit to top 10
            "all_builds_count": all_builds_count
        },
        "best_teammates": champion_teammates[:10],  # Limit to top 10
        "has_synergy_data": len(champion_teammates) > 0
    }

    return jsonify(response)
