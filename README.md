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

### 📦 Deployment (10 Minutes)

**Everything is ready on Git!** Just follow the checklist:

1. **[DEPLOYMENT_CHECKLIST.md](./DEPLOYMENT_CHECKLIST.md)** - Interactive checklist (✅ Recommended!)
2. **[DEPLOY_NOW.md](./DEPLOY_NOW.md)** - Detailed step-by-step guide
3. **[DEPLOYMENT.md](./DEPLOYMENT.md)** - Technical documentation

**TL;DR**:
```bash
1. Deploy Backend → Railway (5 min)
2. Deploy Frontend → Vercel (5 min)
3. Set Environment Variables
4. Done! Auto-updates daily at 04:00 UTC ✨
```

### 🔄 Automatic Updates

Once deployed, the system updates itself **every day at 04:00 UTC**:
- ✅ Fetches new match data from Riot API
- ✅ Trains ML models with fresh data
- ✅ Updates frontend stats automatically
- ✅ Deploys to production via GitHub Actions

**You don't need to do anything!** 🎉

---

## 📚 Documentation

- **[FEATURE_OVERVIEW.md](./FEATURE_OVERVIEW.md)** - Complete feature documentation (German)
- **[DEPLOYMENT_CHECKLIST.md](./DEPLOYMENT_CHECKLIST.md)** - Quick deployment checklist
- **[DEPLOY_NOW.md](./DEPLOY_NOW.md)** - Step-by-step deployment guide
- **[DEPLOYMENT.md](./DEPLOYMENT.md)** - Technical deployment details

---

## 🛠️ Tech Stack

**Backend**:
- Python 3.11
- FastAPI (REST API)
- scikit-learn (ML Models)
- Riot Games API

**Frontend**:
- Next.js 14 (React)
- TypeScript
- Tailwind CSS
- shadcn/ui

**Infrastructure**:
- GitHub Actions (CI/CD)
- Railway (Backend Hosting)
- Vercel (Frontend Hosting)

---

**Made with ❤️ for the League of Legends community**
