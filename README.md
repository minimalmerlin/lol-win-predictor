# ⚔️ LoL Intelligent Coach

AI-powered League of Legends coaching platform with real-time win prediction, dynamic item builds, and live game tracking.

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![Python](https://img.shields.io/badge/python-3.11-green)
![Next.js](https://img.shields.io/badge/next.js-14-black)
![Accuracy](https://img.shields.io/badge/ML%20accuracy-52.0%25%20(Draft%20Only)-yellow)

## 🎯 Features

### 1. **Draft Phase Assistant + AI Build Generator** 📋🤖
- Interactive champion selection for both teams
- Real-time win probability during draft (52.0% baseline - draft-only prediction)
- Role selection for all champions (Top/Jungle/Mid/ADC/Support)
- **AI-Generated Personalized Item Builds** based on:
  - Your champion & role
  - Ally team composition
  - Enemy team composition & roles
  - Game state (Leading/Even/Losing)
  - Item stats & synergies
- Situational items (vs AP Heavy, vs AD Heavy, vs Healers, When Ahead, When Behind)
- Timeline-based builds (Early/Mid/Late game)

### 2. **Live Game Tracker** 🎮
- Automatic game detection via Riot Live Client API
- Real-time win probability updates
- Live game stats (Gold, Kills, Towers, Dragons, Barons)
- Strategic recommendations based on current game state
- Auto-refresh every 30 seconds

## 🚀 Quick Start

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for deployment instructions.

**Made with ❤️ for the League of Legends community**
