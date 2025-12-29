# Vercel Single Project Setup

## Übersicht

Dieses Projekt hat **Backend und Frontend in einem einzigen Vercel-Projekt**. Die Python Serverless Functions sind im `api/` Verzeichnis, das Next.js Frontend im `lol-coach-frontend/` Verzeichnis.

## Projektstruktur

```
/
├── api/                          # Python Serverless Functions (Vercel)
│   ├── predict-champion-matchup.py
│   ├── champions/
│   └── ...
├── lol-coach-frontend/           # Next.js Frontend
│   ├── app/
│   │   └── api/                  # Next.js API Routes (Proxy)
│   └── ...
├── models/                       # ML Modelle
├── champion_matchup_predictor.py
├── api_v2.py                     # FastAPI (nur für lokale Entwicklung)
└── vercel.json
```

## Funktionsweise

### Production (Vercel)

1. **Frontend** (`lol-coach-frontend/`) wird als Next.js App deployed
2. **Backend** (`api/`) wird als Python Serverless Functions deployed
3. Beide sind unter der gleichen Domain erreichbar:
   - Frontend: `https://your-project.vercel.app`
   - Python Functions: `https://your-project.vercel.app/api/*`
   - Next.js API Routes: `https://your-project.vercel.app/api/*` (aber nur für Proxy)

### Request Flow

```
User → Frontend Component
  → Next.js API Route (/api/predict-champion-matchup)
    → Python Serverless Function (/api/predict-champion-matchup)
      → ML Model Prediction
        → Response zurück zum Frontend
```

**Wichtig**: Die Next.js API Route (`lol-coach-frontend/app/api/predict-champion-matchup/route.ts`) ist ein **Proxy**, der:
- In **Production**: Die Python Serverless Function im gleichen Projekt aufruft
- In **Development**: Den lokalen FastAPI Backend (`localhost:8000`) aufruft
- Bei **externem Backend**: Das externe Backend aufruft (wenn `NEXT_PUBLIC_API_URL` gesetzt ist)

## Environment Variables

### Für Vercel Deployment

**Keine Environment Variables nötig** für das Standard-Setup (alles im gleichen Projekt).

Optional:
- `NEXT_PUBLIC_API_URL`: Nur wenn du ein **separates Backend** verwendest
- `INTERNAL_API_KEY`: Nur für externe Backends

### Für lokale Entwicklung

1. **Backend starten**:
```bash
python api_v2.py
# Läuft auf http://localhost:8000
```

2. **Frontend starten**:
```bash
cd lol-coach-frontend
npm run dev
# Läuft auf http://localhost:3000
```

Die Next.js API Route erkennt automatisch `NODE_ENV=development` und ruft `localhost:8000` auf.

## Vercel Configuration

Die `vercel.json` ist minimal:

```json
{
  "version": 2
}
```

Vercel erkennt automatisch:
- Python Files in `/api/` → Serverless Functions
- Next.js App in `/lol-coach-frontend/` → Next.js Deployment

## Troubleshooting

### Problem: "Backend API URL not configured"

**Lösung**: Das ist normal, wenn alles im gleichen Projekt ist. Die Next.js API Route sollte automatisch die Python Serverless Function im gleichen Projekt aufrufen.

**Prüfen**:
1. Ist `NEXT_PUBLIC_API_URL` gesetzt? → Entfernen, wenn alles im gleichen Projekt ist
2. Läuft in Production? → Python Serverless Function sollte unter `/api/predict-champion-matchup` erreichbar sein
3. Läuft lokal? → Backend muss mit `python api_v2.py` gestartet sein

### Problem: Python Serverless Function wird nicht gefunden

**Prüfen**:
1. Ist `api/predict-champion-matchup.py` vorhanden?
2. Ist Flask installiert? (`requirements.txt` sollte `flask` und `flask-cors` enthalten)
3. Vercel Logs prüfen: Vercel Dashboard → Deployments → Function Logs

### Problem: Modelle werden nicht geladen

**Prüfen**:
1. Sind Modelle im `models/` Verzeichnis?
2. Ist der Pfad in `api/predict-champion-matchup.py` korrekt?
3. Vercel hat ein 50MB Limit für Serverless Functions - Modelle müssen klein genug sein

## Deployment Checklist

- [ ] `api/predict-champion-matchup.py` existiert
- [ ] `models/champion_predictor.pkl` existiert
- [ ] `requirements.txt` enthält alle Dependencies (Flask, scikit-learn, etc.)
- [ ] Keine `NEXT_PUBLIC_API_URL` gesetzt (wenn alles im gleichen Projekt)
- [ ] Vercel erkennt automatisch Python Functions und Next.js App

## Alternative: Separate Backend

Wenn du ein **separates Backend** (z.B. auf Railway) verwenden möchtest:

1. Setze `NEXT_PUBLIC_API_URL` in Vercel Environment Variables
2. Die Next.js API Route ruft dann das externe Backend auf
3. Python Serverless Functions werden nicht verwendet

