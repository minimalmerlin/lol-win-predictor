# 🔐 Secrets Management Guide

## ✅ Sichere Secret-Verwaltung für Vercel

### Wie es RICHTIG funktioniert:

```
Entwicklung (lokal)              Production (Vercel)
─────────────────────            ────────────────────
.env.local                   →   Vercel Environment Variables
(in .gitignore)                  (im Vercel Dashboard)
        ↓                                  ↓
  Python/Node liest              Vercel injiziert
  os.getenv()                    zur Runtime
        ↓                                  ↓
  ✅ Secrets bleiben lokal       ✅ Secrets bleiben auf Vercel
  ✅ NICHT in Git                ✅ NICHT in Git
```

## 📋 Setup-Anleitung

### Schritt 1: Lokale Entwicklung

```bash
# 1. Kopiere Template
cp .env.example .env.local

# 2. Fülle echte Werte ein
nano .env.local  # oder dein bevorzugter Editor

# 3. Verifiziere .gitignore
cat .gitignore | grep .env.local  # ✅ Sollte vorhanden sein
```

**Wichtig**: `.env.local` wird NIEMALS committed!

### Schritt 2: Vercel Production Setup

1. **Gehe zu Vercel Dashboard**:
   - https://vercel.com/dashboard
   - Wähle dein Projekt
   - Settings → Environment Variables

2. **Füge alle Secrets hinzu**:

   | Variable Name | Source | Environment |
   |---------------|--------|-------------|
   | `RIOT_API_KEY` | https://developer.riotgames.com/ | Production, Preview, Dev |
   | `POSTGRES_URL` | Supabase Dashboard → Database | Production, Preview, Dev |
   | `NEXT_PUBLIC_INTERNAL_API_KEY` | Generiere mit `openssl rand -hex 32` | Production, Preview, Dev |

3. **Klick "Save"** - Vercel deployt automatisch neu

### Schritt 3: Secrets lokal synchronisieren (optional)

Statt manuell `.env.local` zu pflegen:

```bash
# Holt automatisch alle Vercel Environment Variables
vercel env pull .env.local
```

**Vorteil**: Immer synchron mit Production!

## 🚫 Was NIEMALS in Git gehört:

```bash
# ❌ NIEMALS committen:
.env
.env.local
.env.production
.env.*.local

# ✅ NUR committen:
.env.example  # Template ohne echte Werte
```

## 🔧 Im Code verwenden

### Python (Backend)
```python
import os
from dotenv import load_dotenv

# Lokal: lädt .env.local
load_dotenv('.env.local')

# Auf Vercel: Environment Variables bereits verfügbar
RIOT_API_KEY = os.getenv("RIOT_API_KEY")
POSTGRES_URL = os.getenv("POSTGRES_URL")
```

### TypeScript (Frontend)
```typescript
// Next.js liest automatisch .env.local
const apiKey = process.env.NEXT_PUBLIC_RIOT_API_KEY;
const dbUrl = process.env.POSTGRES_URL;
```

**Hinweis**: `NEXT_PUBLIC_*` Variablen sind im Browser sichtbar - nur für nicht-sensitive Daten!

## 🛡️ Migration auf Production (OHNE Secret-Leak)

### Methode 1: Serverless Endpoint (✅ EMPFOHLEN)

```bash
# Nach dem Deployment
curl -X POST https://your-domain.vercel.app/api/migrate
```

**Vorteil**:
- Verwendet automatisch Vercel Environment Variables
- Kein manuelles Secret-Handling
- Keine Gefahr von Git-Leaks

### Methode 2: Vercel CLI

```bash
# 1. Secrets von Vercel holen
vercel env pull .env.production

# 2. Migration lokal ausführen (mit Production-DB)
export $(cat .env.production | grep POSTGRES_URL | xargs)
python3 scripts/migrate_champion_data.py
```

## ⚠️ Secret Rotation (nach Leak)

Falls Secrets geleakt wurden:

1. **Sofort rotieren**:
   - Riot API: https://developer.riotgames.com/ → Regenerate Key
   - Supabase: Dashboard → Database → Reset Password

2. **Überall aktualisieren**:
   - `.env.local` (lokal)
   - Vercel Environment Variables
   - Ggf. Team-Mitglieder benachrichtigen

3. **Git History bereinigen** (optional):
   ```bash
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch FILENAME" \
     --prune-empty --tag-name-filter cat -- --all
   git push --force --all
   ```

## 📊 Security Checklist

- [x] `.env.local` in `.gitignore`
- [x] Secrets nur in Vercel Environment Variables
- [x] `.env.example` als Template committed
- [x] Kein Hardcoding von Secrets im Code
- [x] Serverless Endpoint für Migrations (keine manuellen Secrets)
- [x] Regelmäßige Secret-Rotation (alle 90 Tage)

## 🔍 Leak-Detection

**GitGuardian** überwacht automatisch dein Repo:
- Erkennt geleakte API Keys, DB Credentials, etc.
- Sendet Alerts per Email
- Siehe: https://dashboard.gitguardian.com/

**Bei Alert**:
1. Sofort Secret rotieren
2. Vercel Environment Variables aktualisieren
3. Git History bereinigen (siehe oben)

## 📚 Weitere Resources

- [Vercel Environment Variables Docs](https://vercel.com/docs/environment-variables)
- [12-Factor App: Config](https://12factor.net/config)
- [GitGuardian Docs](https://docs.gitguardian.com/)
- [OWASP Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)

---

**Letzte Aktualisierung**: 2026-01-01
**Status**: ✅ Sichere Konfiguration aktiv
