# LoL Coach Backend (Refactored)

## Struktur

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI App Initialisierung
│   ├── core/
│   │   ├── config.py           # Environment Configuration
│   │   └── logging.py          # Logging Setup
│   ├── schemas/                # Pydantic Request/Response Models
│   │   ├── prediction.py
│   │   ├── champion.py
│   │   ├── item.py
│   │   └── stats.py
│   ├── services/               # Business Logic & ML Services
│   │   └── ml_engine.py        # Model Loading & Caching
│   └── routers/                # API Endpoints
│       ├── predictions.py      # /api/predict-*
│       ├── champions.py        # /api/champions/*
│       ├── items.py            # /api/item-*
│       ├── live_game.py        # /api/live/*
│       └── stats.py            # /api/stats*
├── run.py                      # Server Runner
└── README.md                   # This file
```

## Start Server

### Vom Backend-Verzeichnis:
```bash
cd backend
python run.py
```

### Oder mit uvicorn direkt:
```bash
cd backend
uvicorn app.main:app --reload --port 8080
```

## Swagger Docs

Nach dem Start verfügbar unter:
- http://localhost:8080/docs (Swagger UI)
- http://localhost:8080/redoc (ReDoc)

## Environment Variables

Konfigurierbar über `.env` Datei oder Umgebungsvariablen:

- `ENV` - Environment (development/production)
- `INTERNAL_API_KEY` - API Key für Production
- `ALLOWED_ORIGINS` - CORS Origins (comma-separated)
- `PORT` - Server Port (default: 8080)

## Migration von api_v2.py

Die alte Datei wurde nach `api_v2_legacy.py.bak` umbenannt.

**Keine Breaking Changes**: Alle API-Endpunkte sind identisch.
