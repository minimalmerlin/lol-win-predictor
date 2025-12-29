"""
Champions Search Endpoint with Fuzzy Matching
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from difflib import SequenceMatcher

app = Flask(__name__)
CORS(app)

def get_champion_data():
    """Load champions with stats from champion_stats.json"""
    try:
        # Get the path to champion_stats.json
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        stats_file = os.path.join(base_dir, 'data', 'champion_data', 'champion_stats.json')

        # Load champion stats
        with open(stats_file, 'r', encoding='utf-8') as f:
            champion_stats = json.load(f)
            return champion_stats
    except Exception as e:
        print(f"Error loading champion stats: {e}")
        return {}

def calculate_similarity(query, champion_name):
    """Calculate similarity score between query and champion name"""
    query_lower = query.lower()
    name_lower = champion_name.lower()

    # Exact match
    if query_lower == name_lower:
        return 1.0

    # Starts with
    if name_lower.startswith(query_lower):
        return 0.95

    # Contains
    if query_lower in name_lower:
        return 0.85

    # Fuzzy match using SequenceMatcher
    return SequenceMatcher(None, query_lower, name_lower).ratio()

def get_match_quality(similarity):
    """Determine match quality based on similarity score"""
    if similarity >= 0.9:
        return 'exact'
    elif similarity >= 0.7:
        return 'good'
    else:
        return 'partial'

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def handler(req):
    """
    Search champions with fuzzy matching
    Query params:
    - query: search term
    - q: alternative search term (for backwards compatibility)
    - limit: max results (default: 10)
    - include_stats: include champion stats (default: false)
    """
    # Support both 'query' and 'q' parameters
    query = request.args.get('query', request.args.get('q', '')).strip()
    limit = int(request.args.get('limit', 10))
    include_stats = request.args.get('include_stats', 'false').lower() == 'true'

    if not query or len(query) < 2:
        return jsonify({"results": []})

    # Load champion data
    champion_stats = get_champion_data()

    if not champion_stats:
        # Fallback if no data file
        return jsonify({"results": []})

    # Calculate similarity for all champions
    matches = []
    for champ_name, stats in champion_stats.items():
        similarity = calculate_similarity(query, champ_name)

        # Only include matches with similarity > 0.3
        if similarity > 0.3:
            result = {
                'name': champ_name,
                'similarity': similarity,
                'match_quality': get_match_quality(similarity),
                'has_builds': True
            }

            # Include stats if requested
            if include_stats and stats:
                result['stats'] = {
                    'games': stats.get('games', 0),
                    'win_rate': stats.get('win_rate', 0.0)
                }

            matches.append(result)

    # Sort by similarity (descending)
    matches.sort(key=lambda x: x['similarity'], reverse=True)

    # Limit results
    results = matches[:limit]

    return jsonify({"results": results})
