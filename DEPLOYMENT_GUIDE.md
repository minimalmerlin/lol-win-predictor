# 🚀 Deployment Guide - LoL Intelligent Coach

Dieses Projekt kann auf verschiedene Arten deployed werden. Hier ist die **einfachste Methode mit Railway**.

---

## ✨ Option 1: Railway (EMPFOHLEN)

Railway hostet sowohl Backend als auch Frontend automatisch.

### Schritt 1: Projekt auf GitHub pushen

```bash
# Wenn noch nicht initialisiert:
git init
git add .
git commit -m "Initial commit - Ready for deployment"

# GitHub Repository erstellen und pushen
git remote add origin https://github.com/DEIN-USERNAME/lol-intelligent-coach.git
git branch -M main
git push -u origin main
```

### Schritt 2: Railway Account erstellen

1. Gehe zu [railway.app](https://railway.app)
2. Klicke "Login" → "Login with GitHub"
3. Autorisiere Railway

### Schritt 3: Backend deployen

1. Klicke "New Project"
2. Wähle "Deploy from GitHub repo"
3. Wähle dein Repository
4. Railway erkennt automatisch Python
5. **Wichtig:** Setze folgende Environment Variables:
   - `PORT` = `8080` (oder leer lassen, Railway setzt automatisch)
   - `PYTHON_VERSION` = `3.11`

### Schritt 4: Frontend deployen

1. Im gleichen Railway Project, klicke "+ New"
2. Wähle "GitHub Repo" → Gleicher Repo
3. Setze **Root Directory** = `lol-coach-frontend`
4. Setze Environment Variable:
   - `NEXT_PUBLIC_API_URL` = `https://DEIN-BACKEND-URL.railway.app`
   (Die Backend URL findest du im Backend Service unter "Settings" → "Domains")

### Schritt 5: URLs erhalten

- **Backend URL**: `https://PROJEKT-NAME.railway.app`
- **Frontend URL**: `https://PROJEKT-NAME-frontend.railway.app`

**Fertig!** Deine App ist jetzt online! 🎉

---

## 🔧 Option 2: Vercel (Frontend) + Railway (Backend)

### Backend auf Railway:
Siehe Schritte 1-3 oben.

### Frontend auf Vercel:

1. Gehe zu [vercel.com](https://vercel.com)
2. Login mit GitHub
3. "New Project" → Wähle dein Repository
4. **Root Directory** = `lol-coach-frontend`
5. **Environment Variables**:
   - `NEXT_PUBLIC_API_URL` = `https://DEIN-BACKEND-URL.railway.app`
6. Deploy!

**Vorteil:** Vercel ist spezialisiert auf Next.js und extrem schnell.

---

## 💰 Kosten

### Railway (Free Tier):
- $5 Credits pro Monat (kostenlos)
- Reicht für ~500-1000 Requests/Tag
- Kein Credit Card nötig für Free Tier

### Vercel (Hobby):
- Frontend komplett kostenlos
- Unbegrenzte Requests
- Kein Credit Card nötig

### Zusammen: $0/Monat für Hobby-Nutzung! 🎉

---

## 🔒 Wichtig: Secrets & Environment Variables

**Für Railway/Vercel:**

Backend Environment Variables:
```bash
PORT=8080
PYTHON_VERSION=3.11
```

Frontend Environment Variables:
```bash
NEXT_PUBLIC_API_URL=https://your-backend-url.railway.app
```

---

## 🐛 Troubleshooting

### Problem: "Module not found"
**Lösung:** Stelle sicher, dass `requirements.txt` alle Dependencies enthält:
```bash
pip freeze > requirements.txt
```

### Problem: "Port already in use"
**Lösung:** Railway setzt `$PORT` automatisch. Nutze in `api_v2.py`:
```python
port = int(os.environ.get("PORT", 8080))
uvicorn.run("api_v2:app", host="0.0.0.0", port=port)
```

### Problem: Frontend kann Backend nicht erreichen
**Lösung:**
1. Prüfe ob `NEXT_PUBLIC_API_URL` korrekt gesetzt ist
2. Stelle sicher, dass Backend CORS erlaubt:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In Production: Nur deine Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Problem: Models/Data nicht gefunden
**Lösung:** Stelle sicher, dass alle Model-Dateien und Daten im Git Repository sind:
```bash
git add models/
git add data/
git commit -m "Add models and data"
git push
```

---

## 📊 Nach dem Deployment

### Custom Domain hinzufügen (Optional):

**Railway:**
1. Gehe zu Service → Settings → Domains
2. Klicke "Generate Domain" oder "Custom Domain"
3. Wenn Custom: Setze CNAME Record bei deinem Domain-Provider

**Vercel:**
1. Project Settings → Domains
2. Add Domain
3. Folge den DNS-Anweisungen

---

## 🎯 Testen nach Deployment

```bash
# Backend testen
curl https://your-backend-url.railway.app/api/champions/list

# Frontend besuchen
open https://your-frontend-url.vercel.app
```

---

## 📝 Updates deployen

Wenn du Code-Änderungen machst:

```bash
git add .
git commit -m "Update feature XYZ"
git push
```

**Railway/Vercel deployen automatisch bei jedem Push!** 🚀

---

## 🆘 Support

Falls Probleme auftreten:
1. Prüfe Railway/Vercel Logs
2. GitHub Issues erstellen
3. Railway/Vercel Support kontaktieren

---

**Happy Deploying! 🎉**
