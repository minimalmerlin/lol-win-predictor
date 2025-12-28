"""
Vercel Serverless Function - Root Endpoint
===========================================
"""
from flask import Flask, jsonify
from flask_cors import CORS
from utils.ddragon import get_champion_mapping

app = Flask(__name__)
CORS(app)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def handler(path):
    return jsonify({"status": "online", "message": "LoL Coach API", "version": "2.0.0"})

@app.route('/api/predict', methods=['POST'])
def predict():
    # ... dein bestehender Code für die Vorhersage ...
    # Angenommen, dein Modell spuckt aus: prediction = 1 (Win)
    
    # NEU: Mapping holen (wird gecached)
    id_to_name, patch_version = get_champion_mapping()
    
    # Beispiel: Wenn du Champion-IDs zurückgibst, wandle sie hier um
    # (Das ist optional, meist macht das Frontend die Darstellung)
    
    return jsonify({
        'prediction': prediction,
        'patch_version': patch_version, # WICHTIG: Version ans Frontend senden
        'win_probability': win_prob
    })