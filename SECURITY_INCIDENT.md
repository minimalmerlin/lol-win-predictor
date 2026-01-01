# 🚨 SECURITY INCIDENT - Geleakte Credentials

**Zeitpunkt**: 2026-01-01 13:19 UTC
**Commit**: `db20496` (docs: Add deployment success documentation)
**Status**: ⚠️ AKTIV - SOFORTIGE MASSNAHMEN ERFORDERLICH

## 🔴 Was wurde geleakt (GitGuardian Detection):

1. **PostgreSQL Credentials** (Supabase)
   - Username: `postgres.gnkhponqrnivdijybgnx`
   - Password: `C2ePaa4rxU8fuw28`
   - Host: `aws-1-eu-central-1.pooler.supabase.com`
   - Database: `postgres`

2. **Riot Games API Key**
   - Key: `RGAPI-9860c50d-0d24-441b-a350-fbce693ce6c8`

## ✅ Bereits durchgeführt:

1. ✅ Secrets aus neuem Commit entfernt (Commit `2cd20d2`)
2. ✅ Placeholder-Text eingefügt
3. ✅ Gepusht zu GitHub

## 🚨 SOFORTIGE MASSNAHMEN ERFORDERLICH:

### 1. Riot API Key rotieren (HÖCHSTE PRIORITÄT)
⏰ **JETZT SOFORT**

1. Gehe zu https://developer.riotgames.com/
2. Login mit deinem Account
3. **Regenerate API Key** (alter Key wird ungültig)
4. Kopiere den neuen Key
5. Aktualisiere in:
   - Lokale `.env` Datei
   - Vercel Environment Variables

**Warum kritisch**: Der alte Key ist öffentlich auf GitHub und kann von jedem missbraucht werden!

### 2. Supabase PostgreSQL Password rotieren
⏰ **INNERHALB VON 24 STUNDEN**

1. Gehe zu https://supabase.com/dashboard
2. Wähle dein Projekt: `gnkhponqrnivdijybgnx`
3. Settings → Database → Database Password
4. **Reset Database Password**
5. Kopiere die neue Connection String
6. Aktualisiere in:
   - Lokale `.env` Datei
   - Vercel Environment Variables (POSTGRES_URL)

**Warum kritisch**: Mit den Credentials kann jemand:
- Daten lesen/ändern/löschen
- DoS durch Query-Spam
- Kostenpflichtige Ressourcen verbrauchen

### 3. Git History bereinigen (OPTIONAL, aber empfohlen)

**Option A: Force-Push mit Rewrite (⚠️ DESTRUKTIV)**
```bash
cd "/Users/merlinmechler/Library/Mobile Documents/com~apple~CloudDocs/Data Analysis/Win_Predicition_System_WR"
git rebase -i db20496~1
# Im Editor: Zeile "pick db20496" → "drop db20496"
git push --force-with-lease
```

**Option B: BFG Repo-Cleaner**
```bash
brew install bfg
bfg --delete-files DEPLOYMENT_SUCCESS.md
git reflog expire --expire=now --all
git gc --prune=now --aggressive
git push --force
```

**⚠️ WARNUNG**: Force-Push bricht History! Nur machen, wenn kein Team-Zugriff besteht.

## 📊 Risiko-Assessment

| Credential | Öffentlich seit | Kritikalität | Status |
|------------|-----------------|--------------|--------|
| Riot API Key | 01.01.2026 13:19 | 🔴 HOCH | ⏳ Rotation erforderlich |
| PostgreSQL Password | 01.01.2026 13:19 | 🔴 HOCH | ⏳ Rotation erforderlich |
| Supabase Anon Key | - | 🟡 MITTEL | ✅ Nicht geleakt (designed für public) |

## 🛡️ Langfristige Maßnahmen

1. ✅ `.env` in `.gitignore` (bereits vorhanden)
2. ✅ Secrets nur in Vercel Environment Variables
3. ⏳ Pre-commit Hook installieren (git-secrets)
4. ⏳ Dependabot Alerts aktivieren
5. ⏳ Regelmäßige Key-Rotation (alle 90 Tage)

## 📝 Timeline

- **13:19 UTC**: Secrets committed (`db20496`)
- **13:19 UTC**: GitGuardian Alert ausgelöst
- **13:22 UTC**: Secrets aus neuem Commit entfernt (`2cd20d2`)
- **⏳ PENDING**: Riot API Key Rotation
- **⏳ PENDING**: PostgreSQL Password Rotation

## ✅ Verification Checklist

Nach Rotation der Secrets:

- [ ] Riot API Key rotiert (https://developer.riotgames.com/)
- [ ] Neuer Key in `.env` eingetragen
- [ ] Neuer Key in Vercel Environment Variables
- [ ] PostgreSQL Password rotiert (Supabase Dashboard)
- [ ] Neue Connection String in `.env`
- [ ] Neue Connection String in Vercel Environment Variables
- [ ] Alte Connection String funktioniert nicht mehr (testen)
- [ ] Neuer Build auf Vercel erfolgreich
- [ ] API-Endpoints funktionieren mit neuen Credentials

---

**⚠️ WICHTIG**: Bis zur vollständigen Rotation sind deine Credentials öffentlich einsehbar!

**Kontakt bei Fragen**: GitGuardian Support / Riot Games Support
