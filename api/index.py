"""
Vercel Serverless Function Handler
===================================
Simple HTTP handler for Vercel deployment
"""

import json
from urllib.parse import parse_qs, urlparse

# Champion list
CHAMPIONS = [
    "Aatrox", "Ahri", "Akali", "Alistar", "Amumu", "Anivia", "Annie", "Ashe",
    "Aurelion Sol", "Azir", "Bard", "Blitzcrank", "Brand", "Braum", "Caitlyn",
    "Camille", "Cassiopeia", "Cho'Gath", "Corki", "Darius", "Diana", "Dr. Mundo",
    "Draven", "Ekko", "Elise", "Evelynn", "Ezreal", "Fiddlesticks", "Fiora",
    "Fizz", "Galio", "Gangplank", "Garen", "Gnar", "Gragas", "Graves", "Hecarim",
    "Heimerdinger", "Illaoi", "Irelia", "Ivern", "Janna", "Jarvan IV", "Jax",
    "Jayce", "Jhin", "Jinx", "Kalista", "Karma", "Karthus", "Kassadin", "Katarina",
    "Kayle", "Kayn", "Kennen", "Kha'Zix", "Kindred", "Kled", "Kog'Maw", "LeBlanc",
    "Lee Sin", "Leona", "Lissandra", "Lucian", "Lulu", "Lux", "Malphite", "Malzahar",
    "Maokai", "Master Yi", "Miss Fortune", "Mordekaiser", "Morgana", "Nami", "Nasus",
    "Nautilus", "Nidalee", "Nocturne", "Nunu", "Olaf", "Orianna", "Ornn", "Pantheon",
    "Poppy", "Quinn", "Rakan", "Rammus", "Rek'Sai", "Renekton", "Rengar", "Riven",
    "Rumble", "Ryze", "Sejuani", "Shaco", "Shen", "Shyvana", "Singed", "Sion", "Sivir",
    "Skarner", "Sona", "Soraka", "Swain", "Syndra", "Tahm Kench", "Taliyah", "Talon",
    "Taric", "Teemo", "Thresh", "Tristana", "Trundle", "Tryndamere", "Twisted Fate",
    "Twitch", "Udyr", "Urgot", "Varus", "Vayne", "Veigar", "Vel'Koz", "Vi", "Viktor",
    "Vladimir", "Volibear", "Warwick", "Wukong", "Xayah", "Xerath", "Xin Zhao", "Yasuo",
    "Yorick", "Zac", "Zed", "Ziggs", "Zilean", "Zyra"
]

def handler(request):
    """Vercel serverless function handler"""

    # Get path
    path = request.get('path', '/')
    query = request.get('query', {})

    # CORS headers
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': '*',
    }

    # Handle OPTIONS for CORS
    if request.get('method') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': ''
        }

    # Root endpoint
    if path == '/':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({"status": "online", "message": "LoL Coach API"})
        }

    # Champions list endpoint
    if path == '/api/champions/list':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({"champions": CHAMPIONS, "total": len(CHAMPIONS)})
        }

    # Champions search endpoint
    if path == '/api/champions/search':
        q = query.get('q', [''])[0] if isinstance(query.get('q'), list) else query.get('q', '')

        if q:
            filtered = [c for c in CHAMPIONS if q.lower() in c.lower()]
            results = [{"name": c} for c in filtered[:10]]
        else:
            results = []

        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({"results": results})
        }

    # 404 for unknown paths
    return {
        'statusCode': 404,
        'headers': headers,
        'body': json.dumps({"error": "Not found"})
    }
