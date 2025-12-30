"""
Champions List Endpoint
"""
from flask import Flask, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

def get_champions_list():
    """Load champions from champion_stats.json"""
    try:
        # Get the path to champion_stats.json
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        stats_file = os.path.join(base_dir, 'data', 'champion_data', 'champion_stats.json')

        # Load and return champion names
        with open(stats_file, 'r', encoding='utf-8') as f:
            champion_stats = json.load(f)
            champions = sorted(list(champion_stats.keys()))
            return champions
    except Exception as e:
        print(f"Error loading champion stats: {e}")
        # Fallback to a basic list if file not found
        return [
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

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def handler(path):
    champions = get_champions_list()
    return jsonify({"champions": champions, "total": len(champions)})
