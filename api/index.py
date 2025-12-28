"""
Vercel Serverless Function Handler
===================================
Wraps the FastAPI app for Vercel deployment
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
from pathlib import Path

app = FastAPI(
    title="LoL Coach API",
    version="2.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple health check
@app.get("/")
def read_root():
    return {"status": "online", "message": "LoL Coach API"}

# Load champion list from static file
@app.get("/api/champions/list")
def get_champions():
    # For now, return a static list
    # You'll need to include champion_stats.json in your deployment
    champions = [
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
    return {"champions": champions, "total": len(champions)}

@app.get("/api/champions/search")
def search_champions(q: str = ""):
    champions = [
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

    if q:
        filtered = [c for c in champions if q.lower() in c.lower()]
        return {"results": [{"name": c} for c in filtered[:10]]}

    return {"results": []}

# Vercel handler
handler = app
