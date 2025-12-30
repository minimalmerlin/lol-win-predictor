# 📁 Project Structure - LoL Intelligent Coach

**Projekt-Größe**: 844MB (nach Cleanup von ~9GB)

## 🎯 Production Files (Essential)

### **Backend API** (Python/FastAPI)
```
api_v2.py                          # Main FastAPI application (33KB)
dynamic_build_generator.py         # AI Build Generator (25KB)
intelligent_item_recommender.py    # Item Recommender (17KB)
riot_live_client.py                # Live Game API Integration (10KB)
```

### **Frontend** (Next.js)
```
lol-coach-frontend/
├── app/                           # Next.js 14 App Router
│   ├── page.tsx                   # Dashboard
│   ├── draft/page.tsx             # Draft Assistant + AI Builds
│   ├── live/page.tsx              # Live Game Tracker
│   └── champion/[name]/page.tsx   # Champion Details
├── components/
│   ├── ChampionSearch.tsx         # Fuzzy Search Component
│   └── ui/                        # shadcn/ui Components
└── lib/
    └── riot-assets.ts             # Riot CDN Integration
```

### **ML Models & Data**
```
models/
├── champion_predictor.pkl         # Champion Matchup Model
├── win_predictor_rf.pkl           # Win Prediction Model
├── performance.json               # Model Metrics
└── backups/                       # Model Backups

data/
├── champion_data/                 # Champion Stats (139 champions)
│   ├── champion_stats.json
│   ├── item_builds.json
│   └── best_teammates.json
└── processed_match_ids.txt
```

### **Configuration**
```
requirements.txt                   # Python Dependencies
vercel.json                        # Vercel Deployment Config
Procfile                           # Cloud Platform Start Command
runtime.txt                        # Python Version (3.11)
.gitignore                         # Git Ignore Rules
```

### **Documentation**
```
README.md                          # GitHub README
DEPLOYMENT_GUIDE.md                # Deployment Instructions
FEATURE_OVERVIEW.md                # Feature Documentation (German)
ROADMAP.md                         # Future Features
QUICK_START_GUIDE.md               # Quick Start Guide
README_MASSIVE_TRAINING.md         # ML Training Info
```

---

## 🗑️ Removed Files (Cleanup)

### **Obsolete Code** (~200KB)
- `api_server.py` - Old Flask API
- `app.py` - Old Flask app
- `Win_predicition_generator.py` - Merged into api_v2.py
- `item_recommender.py` - Old version
- `champion_predictor.py` - Standalone version

### **Training Scripts** (~100KB)
- `auto_trainer.py`
- `train_model.py`
- `process_all_kaggle_data.py`
- `kaggle_data_loader.py`
- `calculate_team_synergies.py`

### **Data Collection** (~70KB)
- `collect_champion_data.py`
- `collect_diverse.py`
- `collect_from_summoner.py`
- `collect_smart.py`
- `extract_champion_item_data.py`
- `extract_item_builds.py`

### **Test Files** (~30KB)
- `test_all_features.py`
- `test_model.py`
- `test_predictions.py`
- `test_api_v2.sh`

### **Large Data** (~8.2GB!)
- `kaggle_data/` - 7GB raw training data
- `venv/` - 1.2GB virtual environment
- `__pycache__/` - 300KB compiled Python
- `logs/` - Log files

### **Redundant Docs** (~40KB)
- `PROGRESS.md`, `STATUS.md`
- `QUICK_START.md` (duplicate)
- `TEST_API.md`
- `IMPROVEMENTS_SUMMARY.md`
- `FRONTEND_GUIDE.md`

---

## 📊 Final Statistics

**Before Cleanup**: ~9GB
**After Cleanup**: 844MB
**Space Saved**: 8.2GB (91% reduction!)

**Files Remaining**: 14 Python files, 6 Markdown docs, 4 config files
**All Essential**: ✅ Production ready!

---

**Ready for Deployment!** 🚀
