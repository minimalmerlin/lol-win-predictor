# 🚀 Lokale Entwicklung Setup

## Backend API URL Konfiguration

Das Frontend benötigt die Backend API URL, um Vorhersagen zu machen.

### Option 1: Environment Variable (Empfohlen)

Erstelle eine `.env.local` Datei im `lol-coach-frontend` Verzeichnis:

```bash
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000
API_URL=http://localhost:8000

# Internal API Key (optional für lokale Entwicklung)
INTERNAL_API_KEY=your-secret-key-here
```

### Option 2: Automatischer Fallback

Wenn keine Environment Variable gesetzt ist, verwendet das Frontend automatisch `http://localhost:8000` als Fallback.

## Lokale Entwicklung starten

1. **Backend starten** (im Hauptverzeichnis):
   ```bash
   python api_v2.py
   ```
   Backend läuft dann auf: http://localhost:8000

2. **Frontend starten** (im lol-coach-frontend Verzeichnis):
   ```bash
   cd lol-coach-frontend
   npm install  # Falls noch nicht gemacht
   npm run dev
   ```
   Frontend läuft dann auf: http://localhost:3000

3. **Testen**: Öffne http://localhost:3000 und teste die Champion-Vorhersage

## Production Setup

Für Production (Vercel/Railway):

1. **Railway Backend**: Setze `NEXT_PUBLIC_API_URL` auf deine Railway URL
2. **Vercel Frontend**: Setze die Environment Variables in Vercel Dashboard

Siehe `VERCEL_ENV_VARS.txt` für Details.

