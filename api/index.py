"""
Vercel Serverless Function - Root Endpoint
===========================================
"""
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def handler(path):
    return jsonify({"status": "online", "message": "LoL Coach API", "version": "2.0.0"})
