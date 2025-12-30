# LoL Coach API - Vercel Serverless Backend

## Struktur

```
api/
├── index.py                    # Vercel Entrypoint (FastAPI app)
├── core/
│   ├── config.py               # Environment Configuration
│   └── logging.py              # Logger Setup
├── schemas/                    # Pydantic Request/Response Models
│   ├── prediction.py
│   ├── champion.py
│   ├── item.py
│   └── stats.py
├── services/                   # Business Logic & ML Services
│   └── ml_engine.py            # ML Model Loading & Caching
├── routers/                    # API Endpoints
│   ├── predictions.py          # /api/predict-*
│   ├── champions.py            # /api/champions/*
│   ├── items.py                # /api/item-*
│   ├── live_game.py            # /api/live/*
│   └── stats.py                # /api/stats*
└── utils/                      # Helper Functions
    ├── db.py                   # Database Utilities
    └── ddragon.py              # Data Dragon API
```

## Deployment Architecture

**Vercel Single Project**:
- Frontend: Next.js (`lol-coach-frontend/`)
- Backend: Python Serverless Functions (`api/`)
- Database: Vercel Postgres

## Vercel Serverless Details

### Entry Point
- File: `api/index.py`
- Export: `app` (FastAPI instance)
- Vercel automatically detects and deploys this

### Cold Start
- Vercel loads ML models on first request (startup event)
- Models are cached between invocations (within same instance)
- Subsequent requests are fast (~100-200ms)

### Environment Variables
Set in Vercel Dashboard:
- `ENV` - Environment (development/production)
- `INTERNAL_API_KEY` - API Key for security
- `ALLOWED_ORIGINS` - CORS origins (comma-separated)
- `VERCEL_ENV` - Auto-set by Vercel (production detection)

### Memory & Timeout
Configured in `vercel.json`:
- Memory: 1024 MB
- Timeout: 30 seconds

## Local Development

### Run Locally with Vercel CLI
```bash
vercel dev
```

### Or with FastAPI directly
```bash
cd api
uvicorn index:app --reload --port 8000
```

## API Endpoints

### Predictions
- `POST /api/predict-champion-matchup` - Team composition prediction
- `POST /api/predict-game-state` - Game state prediction (legacy)
- `POST /api/predict-game-state-v2` - Advanced game state (79.28% accuracy)

### Champions
- `GET /api/champion-stats` - Champion statistics
- `GET /api/champions/list` - All champions
- `GET /api/champions/search?query=yasuo` - Search champions
- `GET /api/champions/{champion_name}` - Champion details

### Items
- `POST /api/item-recommendations` - Item recommendations
- `POST /api/item-recommendations-intelligent` - AI-powered recommendations
- `POST /api/draft/dynamic-build` - Dynamic build path

### Live Game
- `GET /api/live/status` - Check if game is running
- `GET /api/live/game-data` - Current game data
- `GET /api/live/predict` - Live win prediction

### Stats
- `GET /api/stats` - System statistics
- `GET /api/stats/model` - Model performance

### Documentation
- `/api/docs` - Swagger UI
- `/api/redoc` - ReDoc
- `/` - API Health Check

## Migration Notes

**From**:
- `api_v2.py` (1295 lines monolith)
- `backend/app/` (FastAPI modular, but not Vercel-compatible)

**To**:
- `api/` (Vercel Serverless compatible structure)

**Changes**:
- ✅ Removed `uvicorn.run()` (Vercel handles server)
- ✅ Changed imports from `app.*` to `api.*`
- ✅ Single entry point (`api/index.py`)
- ✅ Configured `vercel.json` for routing

**No Breaking Changes**: All API endpoints remain identical.
