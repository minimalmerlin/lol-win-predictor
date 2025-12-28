#!/usr/bin/env python3
"""
Local Development Server for LoL Coach API
==========================================
Simulates Vercel serverless functions for local development.
Runs on http://localhost:8080
"""

import os
import sys
from pathlib import Path
from flask import Flask, jsonify, request
from flask_cors import CORS

# Add project root to Python path
BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend development

# Health check endpoint
@app.route('/health')
def health():
    return jsonify({
        'status': 'ok',
        'message': 'LoL Coach API - Development Server',
        'version': '2.0.0'
    })

# Root endpoint
@app.route('/')
def root():
    return jsonify({
        'status': 'online',
        'message': 'LoL Coach API',
        'version': '2.0.0',
        'environment': 'development'
    })

# Champion search endpoint
@app.route('/api/champions/search')
def search_champions():
    """Search champions with fuzzy matching"""
    query = request.args.get('query', '').strip()
    limit = int(request.args.get('limit', 10))
    include_stats = request.args.get('include_stats', 'false').lower() == 'true'

    if not query or len(query) < 2:
        return jsonify({'results': []})

    # Import champion search logic
    from api.champions.search import handler as search_handler

    # Create a mock request object for the Vercel function
    class MockRequest:
        def __init__(self, args):
            self.args = args
            self.method = 'GET'

    mock_request = MockRequest(request.args)

    # Call the Vercel function handler
    try:
        response = search_handler(mock_request)
        return response
    except Exception as e:
        return jsonify({'error': str(e), 'results': []}), 500

# Champion list endpoint
@app.route('/api/champions/list')
def list_champions():
    """Get all available champions"""
    from api.champions.list import handler as list_handler

    class MockRequest:
        def __init__(self):
            self.method = 'GET'

    try:
        response = list_handler(MockRequest())
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Champion stats endpoint
@app.route('/api/champion-stats')
def champion_stats():
    """Get champion statistics"""
    from api.champions.stats import handler as stats_handler

    class MockRequest:
        def __init__(self, args):
            self.args = args
            self.method = 'GET'

    try:
        response = stats_handler(MockRequest(request.args))
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Champion detail endpoint
@app.route('/api/champions/<champion_name>')
def champion_detail(champion_name):
    """Get detailed champion information"""
    from api.champions.detail import handler as detail_handler

    class MockRequest:
        def __init__(self, champion_name):
            self.champion_name = champion_name
            self.method = 'GET'

    try:
        response = detail_handler(MockRequest(champion_name))
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Champion matchup prediction
@app.route('/api/predict-champion-matchup', methods=['POST'])
def predict_matchup():
    """Predict champion matchup outcome"""
    from api.champions.predict import handler as predict_handler

    class MockRequest:
        def __init__(self, json_data):
            self.json = json_data
            self.method = 'POST'

    try:
        response = predict_handler(MockRequest(request.json))
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Item recommendations
@app.route('/api/item-recommendations', methods=['POST'])
def item_recommendations():
    """Get item recommendations for a champion"""
    from api.champions.items import handler as items_handler

    class MockRequest:
        def __init__(self, json_data):
            self.json = json_data
            self.method = 'POST'

    try:
        response = items_handler(MockRequest(request.json))
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print('🚀 Starting LoL Coach Development Server...')
    print('📡 Server running on http://localhost:8080')
    print('🔍 API Endpoints:')
    print('   - GET  /health')
    print('   - GET  /api/champions/search?query=<name>')
    print('   - GET  /api/champions/list')
    print('   - GET  /api/champion-stats')
    print('   - GET  /api/champions/<name>')
    print('   - POST /api/predict-champion-matchup')
    print('   - POST /api/item-recommendations')
    print('')

    app.run(
        host='0.0.0.0',
        port=8080,
        debug=True,
        threaded=True
    )
