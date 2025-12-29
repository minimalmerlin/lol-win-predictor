# 🚀 DEPLOYMENT - Schritt für Schritt

**Status**: Alles ist auf Git ✅ - Jetzt deployen!

---

## Teil 1: Backend auf Railway (5 Minuten)

### Schritt 1: Railway Account erstellen
1. Gehe zu **https://railway.app**
2. Klicke "Login" → "Login with GitHub"
3. Autorisiere Railway

### Schritt 2: Backend deployen
1. Klicke **"New Project"**
2. Wähle **"Deploy from GitHub repo"**
3. Suche und wähle: **`lol-win-predictor`**
4. Railway erkennt automatisch Python und deployed!

### Schritt 3: Environment Variables setzen

Klicke auf dein Projekt → **Variables** Tab → Füge hinzu:

```bash
# WICHTIG: Diese MÜSSEN gesetzt werden!

# 1. Dein Riot API Key (aus .env Datei)
RIOT_API_KEY=RGAPI-dein-key-hier

# 2. Production Mode
ENV=production

# 3. Port (Railway setzt das automatisch, aber zur Sicherheit)
PORT=8000

# 4. API Key für Frontend-Backend Kommunikation (generiere einen zufälligen String)
INTERNAL_API_KEY=dein-geheimer-key-12345

# 5. CORS - Setze später nach Vercel Deployment
# ALLOWED_ORIGINS wird nach Schritt 2 hinzugefügt
```

**Wie bekommst du RIOT_API_KEY?**
Öffne deine `.env` Datei im Projekt und kopiere den Key!

### Schritt 4: Deployment URL kopieren

Nach dem Deployment siehst du eine URL wie:
```
https://lol-win-predictor-production.up.railway.app
```

**KOPIERE DIESE URL!** Du brauchst sie für Vercel.

---

## Teil 2: Frontend auf Vercel (5 Minuten)

### Schritt 1: Vercel Account erstellen
1. Gehe zu **https://vercel.com**
2. Klicke "Sign Up" → "Continue with GitHub"
3. Autorisiere Vercel

### Schritt 2: Frontend deployen
1. Klicke **"Add New..." → "Project"**
2. Suche und wähle: **`lol-win-predictor`**
3. **WICHTIG**: Setze **Root Directory** auf: `lol-coach-frontend`
4. Framework: Next.js (automatisch erkannt)

### Schritt 3: Environment Variables setzen

Unter **"Environment Variables"** Tab → Füge hinzu:

```bash
# 1. Backend URL (von Railway Schritt 4)
NEXT_PUBLIC_API_URL=https://deine-railway-url.up.railway.app

# 2. Backend URL (nochmal für Server-Side)
API_URL=https://deine-railway-url.up.railway.app

# 3. API Key (gleicher wie in Railway)
INTERNAL_API_KEY=dein-geheimer-key-12345
```

### Schritt 4: Deploy starten
1. Klicke **"Deploy"**
2. Warte 2-3 Minuten
3. Du bekommst eine URL wie: `https://victory-ai.vercel.app`

**KOPIERE DIESE URL!**

---

## Teil 3: CORS in Railway updaten

### Zurück zu Railway

1. Gehe zu deinem Railway Projekt
2. Klicke **"Variables"** Tab
3. Füge hinzu oder editiere:

```bash
ALLOWED_ORIGINS=https://deine-vercel-url.vercel.app,https://victory-ai.vercel.app
```

**Beispiel**:
```bash
ALLOWED_ORIGINS=https://lol-coach-xyz.vercel.app,http://localhost:3000
```

(Das `localhost:3000` lässt du drin für lokale Tests)

4. Railway deployed automatisch neu (dauert 1 Minute)

---

## ✅ FERTIG! Teste die Deployment

### Test 1: Backend
Öffne in Browser:
```
https://deine-railway-url.up.railway.app/health
```

**Erwartete Antwort**:
```json
{
  "status": "healthy",
  "timestamp": "2025-12-29T...",
  "models_loaded": true
}
```

### Test 2: Frontend
Öffne in Browser:
```
https://deine-vercel-url.vercel.app
```

**Check**:
- ✅ Seite lädt
- ✅ Stats zeigen "52.0%" und "12.8K+ Matches"
- ✅ Keine CORS Errors in Browser Console (F12)

### Test 3: API Connection
Auf der Frontend-Seite:
1. Gehe zu "ANALYSIS MODULES" → Victory AI Tab
2. Wähle 5 Champions für Blue Team
3. Wähle 5 Champions für Red Team
4. Klicke "Predict Matchup"

**Erwartete Antwort**:
```
Blue Team: 48.2% Win Probability
Red Team: 51.8% Win Probability
```

Wenn das funktioniert → **PERFEKT! Alles deployed!** 🎉

---

## 🔄 Automatische Updates

Ab jetzt:
- **Jeden Tag um 04:00 UTC**: GitHub Actions läuft
- **04:02 UTC**: Neue Daten + Modelle werden gepusht
- **04:03 UTC**: Railway deployed automatisch neu
- **04:04 UTC**: Vercel deployed automatisch neu
- **04:05 UTC**: Deine Website hat neue Stats! ✨

**Du musst NIE wieder etwas tun!**

---

## 🐛 Troubleshooting

### Problem: "Backend API URL not configured"

**Fix**: Check Vercel Environment Variables
- `NEXT_PUBLIC_API_URL` muss gesetzt sein
- Wert muss Railway URL sein (mit `https://`)

### Problem: CORS Error in Browser Console

**Fix**: Check Railway Environment Variables
- `ALLOWED_ORIGINS` muss deine Vercel URL enthalten
- Format: `https://url1.com,https://url2.com` (komma-getrennt, keine Spaces!)

### Problem: Railway Deployment failed

**Fix**: Check Railway Logs
- Klicke "Deployments" → Letztes Deployment → "View Logs"
- Häufigster Fehler: `RIOT_API_KEY` nicht gesetzt

### Problem: Stats zeigen alte Werte (52.6% statt 52.0%)

**Wahrscheinlich**: `model_performance.json` wurde noch nicht geladen
- Check ob `lol-coach-frontend/public/data/model_performance.json` existiert auf GitHub
- Falls nicht: Laufe Pipeline einmal manuell (siehe DEPLOYMENT.md)

---

## 📊 Monitoring

### Railway Dashboard
- **URL**: https://railway.app/dashboard
- **Check**: Deployment Status, Logs, Metrics

### Vercel Dashboard
- **URL**: https://vercel.com/dashboard
- **Check**: Deployment Status, Analytics, Logs

### GitHub Actions
- **URL**: https://github.com/minimalmerlin/lol-win-predictor/actions
- **Check**: Pipeline Runs (täglich 04:00 UTC)

---

## 🎯 Nächste Schritte nach Deployment

1. **Teile deine URL**: Schicke `https://deine-vercel-url.vercel.app` an Freunde!
2. **Custom Domain** (optional):
   - Gehe zu Vercel → Projekt → Settings → Domains
   - Füge deine Domain hinzu (z.B. `victory-ai.com`)
3. **Analytics** (optional):
   - Vercel Analytics automatisch aktiv
   - Siehe User Count in Vercel Dashboard

---

**Author**: Merlin Mechler
**Date**: 2025-12-29
**Support**: Bei Problemen → Check Troubleshooting Section oben
