# 🚀 Vercel Deployment Setup

## Übersicht

Dieses Projekt verwendet **zwei separate Vercel-Projekte**:
1. **Backend** (Root-Verzeichnis) - FastAPI mit ML-Modellen
2. **Frontend** (lol-coach-frontend/) - Next.js App

---

## Schritt 1: Backend auf Vercel deployen

### 1.1 Backend-Projekt erstellen

1. Gehe zu [Vercel Dashboard](https://vercel.com)
2. Klicke **"Add New Project"**
3. Importiere dein GitHub Repository
4. **Konfiguration**:
   - **Framework Preset**: `Other`
   - **Root Directory**: `.` (Root-Verzeichnis)
   - **Build Command**: (leer lassen)
   - **Output Directory**: (leer lassen)

### 1.2 Environment Variables für Backend

In Vercel Backend Settings → Environment Variables:

```bash
# Python Version
PYTHON_VERSION=3.11

# Environment
ENV=production

# API Key (optional, für Frontend-Backend Kommunikation)
INTERNAL_API_KEY=your-secret-key-here

# CORS Origins (wird nach Frontend-Deployment aktualisiert)
ALLOWED_ORIGINS=https://your-frontend.vercel.app
```

### 1.3 Backend URL notieren

Nach dem Deployment erhältst du eine URL wie:
```
https://win-predicition-system-wr.vercel.app
```

**KOPIERE DIESE URL!** Du brauchst sie für das Frontend.

---

## Schritt 2: Frontend auf Vercel deployen

### 2.1 Frontend-Projekt erstellen

1. Gehe zu [Vercel Dashboard](https://vercel.com)
2. Klicke **"Add New Project"** (neues Projekt!)
3. Importiere das **gleiche** GitHub Repository
4. **Konfiguration**:
   - **Framework Preset**: `Next.js` (wird automatisch erkannt)
   - **Root Directory**: `lol-coach-frontend`
   - **Build Command**: `npm run build` (default)
   - **Output Directory**: (default)

### 2.2 Environment Variables für Frontend

**WICHTIG**: Diese müssen gesetzt werden!

In Vercel Frontend Settings → Environment Variables:

```bash
# Backend API URL (von Schritt 1.3)
NEXT_PUBLIC_API_URL=https://win-predicition-system-wr.vercel.app

# Backend API URL (für Server-Side Rendering)
API_URL=https://win-predicition-system-wr.vercel.app

# Internal API Key (muss identisch mit Backend sein)
INTERNAL_API_KEY=your-secret-key-here
```

**Wichtig**: 
- `NEXT_PUBLIC_API_URL` muss die **Backend-URL** sein (nicht die Frontend-URL!)
- Setze diese für **alle Environments** (Production, Preview, Development)

### 2.3 Redeploy

Nach dem Setzen der Environment Variables:
1. Gehe zu Deployments
2. Klicke auf das neueste Deployment
3. Klicke "Redeploy"

---

## Schritt 3: CORS aktualisieren

Nach dem Frontend-Deployment:

1. Gehe zum **Backend-Projekt** in Vercel
2. Settings → Environment Variables
3. Aktualisiere `ALLOWED_ORIGINS`:
   ```bash
   ALLOWED_ORIGINS=https://your-frontend.vercel.app,https://your-backend.vercel.app
   ```
4. Redeploy Backend

---

## Lokale Entwicklung

Für lokale Entwicklung:

1. **Backend starten**:
   ```bash
   python api_v2.py
   ```
   Läuft auf: http://localhost:8000

2. **Frontend starten**:
   ```bash
   cd lol-coach-frontend
   npm run dev
   ```
   Läuft auf: http://localhost:3000

3. **Environment Variable** (optional):
   Erstelle `lol-coach-frontend/.env.local`:
   ```bash
   NEXT_PUBLIC_API_URL=http://localhost:8000
   API_URL=http://localhost:8000
   ```

Das Frontend verwendet automatisch `http://localhost:8000` als Fallback, wenn keine Environment Variable gesetzt ist.

---

## Troubleshooting

### Problem: "Backend API URL not configured"

**Lösung**: 
1. Prüfe, ob `NEXT_PUBLIC_API_URL` in Vercel gesetzt ist
2. Stelle sicher, dass die URL die **Backend-URL** ist (nicht Frontend!)
3. Redeploy Frontend nach dem Setzen der Variable

### Problem: CORS Fehler

**Lösung**:
1. Prüfe `ALLOWED_ORIGINS` im Backend
2. Stelle sicher, dass die Frontend-URL enthalten ist
3. Redeploy Backend

### Problem: Backend nicht erreichbar

**Lösung**:
1. Prüfe, ob das Backend-Projekt auf Vercel deployed ist
2. Teste die Backend-URL direkt im Browser: `https://your-backend.vercel.app/health`
3. Prüfe die Backend-Logs in Vercel

---

## URLs nach Deployment

- **Backend**: `https://your-backend-project.vercel.app`
- **Frontend**: `https://your-frontend-project.vercel.app`

Beide werden automatisch bei jedem Git Push aktualisiert! 🚀

