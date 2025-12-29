# ✅ Deployment Checklist - Victory AI

**Estimated Time**: 10 Minuten
**Prerequisites**: GitHub Account, .env Datei mit RIOT_API_KEY

---

## 🎯 Quick Links

- **Railway**: https://railway.app
- **Vercel**: https://vercel.com
- **Detaillierte Anleitung**: [DEPLOY_NOW.md](./DEPLOY_NOW.md)

---

## Part 1: Backend (Railway) - 5 Min

### 1.1 Account Setup
- [ ] Gehe zu https://railway.app
- [ ] Login with GitHub
- [ ] Autorisiere Railway

### 1.2 Deploy Backend
- [ ] Klicke "New Project"
- [ ] "Deploy from GitHub repo"
- [ ] Wähle `lol-win-predictor`
- [ ] Warte auf automatisches Deployment (~2 Min)

### 1.3 Set Environment Variables
Klicke "Variables" Tab → Füge hinzu:

- [ ] `RIOT_API_KEY` = `[Kopiere aus deiner .env Datei]`
- [ ] `ENV` = `production`
- [ ] `PORT` = `8000`
- [ ] `INTERNAL_API_KEY` = `[Generiere zufälligen String, z.B. "victory-ai-secret-key-12345"]`
- [ ] `ALLOWED_ORIGINS` = `[Wird später gesetzt nach Vercel]`

### 1.4 Kopiere Backend URL
- [ ] Nach Deployment: Kopiere URL (z.B. `https://lol-win-predictor-production.up.railway.app`)
- [ ] Speichere URL in Notizen - brauchst du für Vercel!

**✅ Backend deployed!**

---

## Part 2: Frontend (Vercel) - 5 Min

### 2.1 Account Setup
- [ ] Gehe zu https://vercel.com
- [ ] Sign Up with GitHub
- [ ] Autorisiere Vercel

### 2.2 Deploy Frontend
- [ ] Klicke "Add New..." → "Project"
- [ ] Wähle `lol-win-predictor`
- [ ] **WICHTIG**: Root Directory = `lol-coach-frontend`
- [ ] Framework: Next.js (auto-detected)

### 2.3 Set Environment Variables
Unter "Environment Variables":

- [ ] `NEXT_PUBLIC_API_URL` = `[Deine Railway URL]`
- [ ] `API_URL` = `[Deine Railway URL]`
- [ ] `INTERNAL_API_KEY` = `[Gleicher String wie in Railway]`

**Beispiel**:
```
NEXT_PUBLIC_API_URL=https://lol-win-predictor-production.up.railway.app
API_URL=https://lol-win-predictor-production.up.railway.app
INTERNAL_API_KEY=victory-ai-secret-key-12345
```

### 2.4 Deploy & Copy URL
- [ ] Klicke "Deploy"
- [ ] Warte 2-3 Minuten
- [ ] Kopiere Vercel URL (z.B. `https://lol-coach-abc123.vercel.app`)

**✅ Frontend deployed!**

---

## Part 3: CORS Fix (Railway) - 1 Min

### 3.1 Update Railway CORS
- [ ] Zurück zu Railway → Dein Projekt → "Variables"
- [ ] Setze `ALLOWED_ORIGINS`:

**Format**:
```
ALLOWED_ORIGINS=https://deine-vercel-url.vercel.app,http://localhost:3000
```

**Beispiel**:
```
ALLOWED_ORIGINS=https://lol-coach-abc123.vercel.app,http://localhost:3000
```

- [ ] Railway deployed automatisch neu (~1 Min)

**✅ CORS konfiguriert!**

---

## Part 4: Testing - 2 Min

### 4.1 Test Backend
- [ ] Öffne: `https://deine-railway-url.up.railway.app/health`
- [ ] Erwarte: `{"status": "healthy", ...}`

### 4.2 Test Frontend
- [ ] Öffne: `https://deine-vercel-url.vercel.app`
- [ ] Check: Seite lädt
- [ ] Check: Stats zeigen "52.0%" und "12.8K+"
- [ ] Check: Keine CORS Errors in Console (F12)

### 4.3 Test API Connection
- [ ] Auf Frontend → "ANALYSIS MODULES" → Victory AI
- [ ] Wähle 10 Champions (5 Blue, 5 Red)
- [ ] Klicke "Predict Matchup"
- [ ] Erwarte: Win Probabilities werden angezeigt

**✅ Alles funktioniert!**

---

## 🎉 FERTIG!

### Was jetzt automatisch passiert:

**Jeden Tag um 04:00 UTC**:
1. GitHub Actions sammelt neue Daten
2. Trainiert Modelle neu
3. Pushed zu Git
4. Railway deployed automatisch
5. Vercel deployed automatisch
6. **Deine Website hat neue Stats!** ✨

**Du musst NIE wieder etwas tun!**

---

## 📊 Nächste Schritte (Optional)

### Custom Domain (Vercel)
- [ ] Vercel → Projekt → Settings → Domains
- [ ] Füge deine Domain hinzu (z.B. `victory-ai.com`)
- [ ] Folge DNS Setup Anleitung

### Monitoring
- [ ] Check Railway Dashboard: https://railway.app/dashboard
- [ ] Check Vercel Dashboard: https://vercel.com/dashboard
- [ ] Check GitHub Actions: https://github.com/minimalmerlin/lol-win-predictor/actions

### Share with Friends
- [ ] Teile deine URL!
- [ ] Sammle Feedback
- [ ] Watch die Stats wachsen 📈

---

## 🐛 Troubleshooting

**Problem**: Backend URL not configured
- **Fix**: Check Vercel Environment Variables

**Problem**: CORS Error
- **Fix**: Check Railway `ALLOWED_ORIGINS` Variable

**Problem**: Stats zeigen alte Werte
- **Fix**: Trigger GitHub Actions manuell oder warte bis 04:00 UTC

**Mehr Hilfe**: Siehe [DEPLOY_NOW.md](./DEPLOY_NOW.md) Troubleshooting Section

---

**Status**: ✅ Alles auf Git gepusht
**Ready to deploy**: JA!
**Follow**: [DEPLOY_NOW.md](./DEPLOY_NOW.md) für Details

**Viel Erfolg! 🚀**
