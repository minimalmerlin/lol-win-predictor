# 🚀 VERCEL DEPLOYMENT CHECKLIST

## ⚠️ CRITICAL: Environment Variables Setup

**Diese Environment Variables MÜSSEN in Vercel Project Settings gesetzt werden, bevor das Backend funktioniert!**

### Vercel Dashboard Schritte:
1. Gehe zu: https://vercel.com/dashboard
2. Wähle dein Projekt: `lol-win-predictor`
3. Gehe zu: **Settings** → **Environment Variables**
4. Füge die folgenden Variablen hinzu:

---

## 📋 Required Environment Variables

### 1. Database Connection (CRITICAL)
```
SUPABASE_URL=postgresql://postgres.[PROJECT_ID]:[PASSWORD]@aws-0-eu-central-1.pooler.supabase.com:6543/postgres
```
- **Where to find**: Supabase Dashboard → Project Settings → Database
- **Format**: PostgreSQL connection string with pooler (port 6543, not 5432)
- **Critical**: Without this, ALL API endpoints will return 500 errors

### 2. API Key (OPTIONAL but recommended)
```
NEXT_PUBLIC_INTERNAL_API_KEY=your-secret-key-here
```
- **Purpose**: Protect internal API routes from unauthorized access
- **Generation**: Use `openssl rand -hex 32` to generate a secure key
- **Note**: If not set, API will work but without authentication

### 3. Frontend API URL (OPTIONAL)
```
NEXT_PUBLIC_API_URL=
```
- **Default**: Empty string (uses relative paths `/api/*`)
- **When to set**: Only if you want to use a separate backend deployment
- **Recommended**: Leave empty for Vercel monorepo setup

---

## 🔧 vercel.json Configuration

**Status**: ✅ ALREADY CONFIGURED

The `vercel.json` file has been updated with correct rewrites:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    },
    {
      "src": "lol-coach-frontend/package.json",
      "use": "@vercel/next"
    }
  ],
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "/api/index.py"
    }
  ]
}
```

**What this does**:
- Routes ALL `/api/*` requests to FastAPI backend (`api/index.py`)
- Frontend uses relative paths → seamless routing on Vercel
- No CORS issues, no proxy needed

---

## 🧪 Testing Production Deployment

### 1. API Health Check
```bash
curl https://your-domain.vercel.app/health
```
**Expected Response**:
```json
{
  "status": "healthy",
  "models_loaded": {
    "champion_matchup": true,
    "game_state": false
  }
}
```

### 2. Champion Stats Endpoint
```bash
curl https://your-domain.vercel.app/api/champion-stats?limit=5
```
**Expected Response**:
```json
{
  "champions": [
    {"name": "Ahri", "games": 150, "wins": 90, "win_rate": 0.6, ...}
  ],
  "total_champions": 168
}
```

### 3. Frontend Dashboard
- Open: `https://your-domain.vercel.app`
- Check: Stats should load (not show "Keine Champion-Daten verfügbar")
- Check Browser Console: Should see `[DEBUG]` logs

---

## 🐛 Troubleshooting

### Error: "Keine Champion-Daten verfügbar"
**Possible Causes**:
1. ❌ `SUPABASE_URL` not set in Vercel → **CHECK ENV VARS**
2. ❌ Database connection failed → **CHECK SUPABASE DASHBOARD (is DB paused?)**
3. ❌ API routing broken → **CHECK vercel.json rewrites**

**How to Debug**:
```bash
# Check Vercel Function Logs
vercel logs --follow

# Check specific deployment
vercel logs [DEPLOYMENT_URL]
```

### Error: 404 on /api/* endpoints
**Possible Causes**:
1. ❌ `vercel.json` rewrites not applied → **RE-DEPLOY**
2. ❌ `api/index.py` build failed → **CHECK BUILD LOGS**

**Fix**: Commit changes, push to GitHub, wait for automatic deployment

### Error: 500 Internal Server Error
**Possible Causes**:
1. ❌ `SUPABASE_URL` missing or malformed
2. ❌ Database credentials incorrect
3. ❌ Python dependencies missing

**Fix**: Check Vercel Function Logs for Python stack trace

---

## 📊 Expected Behavior

### ✅ Correct Production Behavior
- `/` → Next.js homepage (stats load from `/api/champion-stats`)
- `/api/champion-stats` → FastAPI endpoint (returns JSON from Supabase)
- `/champions/Ahri` → Next.js dynamic route (champion detail page)
- `/health` → FastAPI health check (returns status JSON)

### ❌ Incorrect Behavior (Pre-Fix)
- `/api/champion-stats` → 404 Not Found
- Dashboard shows: "Keine Champion-Daten verfügbar"
- Browser Console: fetch errors to localhost:8000

---

## 🔄 Deployment Process

### Automatic Deployment (Recommended)
1. **Commit changes**: `git add -A && git commit -m "fix: production routing"`
2. **Push to GitHub**: `git push origin main`
3. **Vercel auto-deploys**: Wait ~2 minutes
4. **Check deployment**: https://vercel.com/dashboard

### Manual Deployment (Alternative)
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy from root directory
cd "/path/to/Win_Predicition_System_WR"
vercel --prod
```

---

## 📝 Checklist Before Going Live

- [ ] ✅ `SUPABASE_URL` set in Vercel Environment Variables
- [ ] ✅ `vercel.json` has correct rewrites (`/api/:path*` → `/api/index.py`)
- [ ] ✅ `app/live/page.tsx` uses relative paths (not `localhost:8000`)
- [ ] ✅ Build successful locally (`npm run build`)
- [ ] ✅ Git committed and pushed to GitHub
- [ ] ✅ Vercel deployment successful (check dashboard)
- [ ] ✅ `/health` endpoint returns 200 OK
- [ ] ✅ `/api/champion-stats` returns JSON data
- [ ] ✅ Dashboard loads stats (not fallback text)
- [ ] ✅ Browser Console shows `[DEBUG]` logs

---

## 🎯 Final Verification

Once deployed, test these critical paths:

1. **Homepage**: https://your-domain.vercel.app
   - Should load stats from API
   - Should NOT show "Keine Champion-Daten verfügbar"

2. **Champion Search**: Search for "Ahri" → Click result
   - Should navigate to `/champions/Ahri`
   - Should NOT 404

3. **Stats Page**: https://your-domain.vercel.app/stats
   - Should load champion table
   - Should allow filtering/sorting

4. **API Direct**: https://your-domain.vercel.app/api/champion-stats
   - Should return JSON (not HTML error page)
   - Should include `"champions"` array

---

**Last Updated**: 2025-12-31
**Status**: ✅ Configuration Complete - Ready for Deployment
**Next Step**: Set `SUPABASE_URL` in Vercel Dashboard → Deploy → Test
