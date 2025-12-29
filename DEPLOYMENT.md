# 🚀 Deployment Guide - Victory AI

## Übersicht

Victory AI besteht aus **zwei Teilen**:
1. **Backend (FastAPI)** - Python ML-API mit Modellen
2. **Frontend (Next.js)** - React-basiertes UI

**Wichtig**: Das Frontend braucht das Backend! Du musst beide deployen.

---

## ✅ Was bereits automatisch läuft

### GitHub Actions Pipeline (Daily Updates)
- **Schedule**: Täglich um 04:00 UTC
- **Was passiert**:
  1. Fetcht neue Match-Daten von Riot API
  2. Merged alle Datenquellen
  3. Generiert Item Builds
  4. Trainiert ML-Modelle neu
  5. **Commited automatisch** zurück ins Repo

**Ergebnis**: Jeden Tag werden:
- `models/` (trainierte Modelle) aktualisiert
- `lol-coach-frontend/public/data/model_performance.json` aktualisiert
- Diese Änderungen werden automatisch ins Repo gepusht

---

## 🎯 Frontend Deployment (Vercel)

### Schritt 1: Vercel Projekt erstellen

1. Gehe zu [vercel.com](https://vercel.com)
2. Klicke "Add New Project"
3. Import dein GitHub Repo: `minimalmerlin/lol-win-predictor`
4. **Root Directory**: `lol-coach-frontend`
5. Framework: Next.js (wird automatisch erkannt)

### Schritt 2: Environment Variables setzen

In Vercel Project Settings → Environment Variables:

```bash
# Backend API URL (setze das nach Backend-Deployment)
NEXT_PUBLIC_API_URL=https://your-backend-api.railway.app
API_URL=https://your-backend-api.railway.app

# API Key (optional, für Produktion)
INTERNAL_API_KEY=your-secret-key-here
```

### Schritt 3: Deploy Settings

- **Build Command**: `npm run build` (default)
- **Output Directory**: `.next` (default)
- **Install Command**: `npm install` (default)

### Schritt 4: Deploy

- Klicke "Deploy"
- Vercel baut automatisch bei jedem Push zu `main`

**Wichtig**: Vercel deployed **automatisch** bei jedem GitHub Push!
→ Wenn GitHub Actions um 04:00 Uhr Modelle aktualisiert und pusht, deployed Vercel automatisch das neue Frontend mit aktualisierten Stats!

---

## 🐍 Backend Deployment (Railway / Render)

### Option A: Railway (Empfohlen)

1. Gehe zu [railway.app](https://railway.app)
2. "New Project" → "Deploy from GitHub Repo"
3. Wähle `minimalmerlin/lol-win-predictor`

#### Railway Settings:

**Root Directory**: `/` (nicht lol-coach-frontend!)

**Build Command**:
```bash
pip install -r requirements.txt
```

**Start Command**:
```bash
uvicorn api_v2:app --host 0.0.0.0 --port $PORT
```

**Environment Variables**:
```bash
PORT=8000
ENV=production
RIOT_API_KEY=RGAPI-your-api-key-here
INTERNAL_API_KEY=your-secret-key-here
ALLOWED_ORIGINS=https://your-frontend.vercel.app,https://victory-ai.vercel.app
```

**Deploy**: Railway deployed automatisch bei Push zu `main`!

---

### Option B: Render

1. Gehe zu [render.com](https://render.com)
2. "New Web Service" → Connect GitHub Repo
3. Wähle `minimalmerlin/lol-win-predictor`

#### Render Settings:

- **Root Directory**: `/`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn api_v2:app --host 0.0.0.0 --port $PORT`
- **Environment**: Python 3.11

**Environment Variables**: Gleiche wie Railway (siehe oben)

---

## 🔄 Automatischer Daily Update Flow

### Was passiert täglich um 04:00 UTC:

```
┌─────────────────────────────────────────────┐
│  GitHub Actions Pipeline (04:00 UTC)        │
├─────────────────────────────────────────────┤
│  1. Fetch new matches from Riot API         │
│  2. Merge training data                     │
│  3. Generate item builds                    │
│  4. Train ML models                         │
│  5. Copy performance.json to frontend/      │
│  6. Git commit + push to main               │
└─────────────────┬───────────────────────────┘
                  │
                  ├──> Trigger Vercel Deploy
                  │    └─> Frontend mit neuen Stats
                  │
                  └──> Trigger Railway Deploy
                       └─> Backend mit neuen Modellen
```

**Resultat**: Jeden Tag werden automatisch:
- ✅ Neue Daten gesammelt
- ✅ Modelle neu trainiert
- ✅ Frontend Stats aktualisiert (Accuracy, Match Count)
- ✅ Automatisch deployed (Vercel + Railway)

**Du musst nichts machen!** 🎉

---

## 📊 Stats werden automatisch aktualisiert

### Frontend zeigt jetzt dynamisch:

1. **Model Accuracy**: Aus `model_performance.json`
2. **Match Count**: Aus `model_performance.json`
3. **Last Updated**: Timestamp aus JSON

**Wie es funktioniert**:
```typescript
// Frontend lädt Stats beim Page Load
const { stats } = useModelStats();

// Zeigt an:
<div>{formatAccuracy(stats.accuracy)}</div>  // z.B. "52.0%"
<div>{formatMatchCount(stats.matches_count)}</div>  // z.B. "12.8K"
```

**Datenquelle**: `lol-coach-frontend/public/data/model_performance.json`

Diese Datei wird automatisch bei jedem Training aktualisiert!

---

## ⚙️ Manuelle Pipeline Trigger (optional)

Du kannst die Pipeline auch manuell starten:

1. Gehe zu GitHub Actions
2. Klicke "Victory AI Daily Loop"
3. "Run workflow" → Wähle Optionen:
   - **Skip data fetching**: ✅ (wenn du nur Modell neu trainieren willst)
   - **Skip data merging**: ❌
   - **Skip data processing**: ❌
   - **Skip model training**: ❌

---

## 🔍 Deployment Checklist

### Vor dem ersten Deploy:

- [ ] Backend deployed auf Railway/Render
- [ ] Frontend deployed auf Vercel
- [ ] Backend-URL in Vercel ENV gesetzt (`NEXT_PUBLIC_API_URL`)
- [ ] RIOT_API_KEY in Railway ENV gesetzt
- [ ] CORS in Backend konfiguriert (ALLOWED_ORIGINS)
- [ ] Erster Testlauf: Rufe Frontend auf → sollte mit Backend kommunizieren

### Nach jedem GitHub Actions Run:

- [ ] Vercel deployed automatisch (check Vercel Dashboard)
- [ ] Railway deployed automatisch (check Railway Dashboard)
- [ ] Frontend zeigt neue Stats (check `/` Homepage)
- [ ] Backend hat neue Modelle (check `/api/stats/model`)

---

## 🐛 Troubleshooting

### Frontend kann Backend nicht erreichen

**Symptom**: "Backend API URL not configured"

**Fix**:
```bash
# In Vercel Environment Variables
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
```

### Backend CORS Error

**Symptom**: Browser Console zeigt "CORS policy blocked"

**Fix**: In Railway/Render ENV:
```bash
ALLOWED_ORIGINS=https://your-frontend.vercel.app,https://another-domain.com
```

### Stats zeigen alte Werte

**Symptom**: Frontend zeigt "50,000+ Matches" obwohl Pipeline 12,834 hat

**Fix**:
1. Check ob `lol-coach-frontend/public/data/model_performance.json` existiert
2. Check ob GitHub Actions erfolgreich war
3. Force re-deploy in Vercel

---

## 📝 Nächste Schritte

1. **Backend deployen** (Railway/Render)
2. **Frontend deployen** (Vercel)
3. **Environment Variables setzen**
4. **Erste Pipeline manuell triggern** (optional)
5. **Ab morgen 04:00 UTC**: Läuft alles automatisch! 🚀

**Fertig!** Das System updated sich jetzt täglich selbst.

---

**Author**: Merlin Mechler
**Date**: 2025-12-29
**Version**: 2.1.0
