# 🔐 Quick Security Reference

## TL;DR - Secrets NIEMALS in Git!

```bash
# ✅ RICHTIG
.env.local              # Lokal (in .gitignore)
Vercel Dashboard        # Production Environment Variables

# ❌ FALSCH
.env                    # NICHT committen!
DEPLOYMENT_SUCCESS.md   # KEINE Secrets in Docs!
Hardcoded im Code       # NIEMALS!
```

## 🚀 Quick Setup

```bash
# 1. Kopiere Template
cp .env.example .env.local

# 2. Füge echte Werte ein
nano .env.local

# 3. Oder sync von Vercel
vercel env pull .env.local
```

## 🔄 Migration auf Production

```bash
# Option 1: Serverless (SICHER - keine Secret-Exposure)
curl -X POST https://lol-win-predictor-qqss.vercel.app/api/migrate

# Option 2: Vercel CLI
vercel env pull .env.production
export $(cat .env.production | grep POSTGRES_URL | xargs)
python3 scripts/migrate_champion_data.py
```

## 📖 Vollständige Guides

- **[SECRETS_MANAGEMENT.md](SECRETS_MANAGEMENT.md)** - Kompletter Guide
- **[SECURITY_INCIDENT.md](SECURITY_INCIDENT.md)** - Incident Response
- **[DEPLOYMENT_SUCCESS.md](DEPLOYMENT_SUCCESS.md)** - Deployment Status

---

**Bei Fragen**: Siehe [SECRETS_MANAGEMENT.md](SECRETS_MANAGEMENT.md)
