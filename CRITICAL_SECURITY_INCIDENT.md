# 🚨 CRITICAL SECURITY INCIDENT - 2026-01-02

## Incident Summary

**Severity**: CRITICAL
**Date**: 2026-01-02 13:22:36 (Commit `bf3de82`)
**Status**: ⚠️ SECRETS STILL ACTIVE - IMMEDIATE ROTATION REQUIRED

### What Happened

The file `.env.vercel.new` containing ALL production secrets was accidentally committed to the public GitHub repository in commit `bf3de82033d2b3930efa487a7cb583dfd4437304`.

### Leaked Credentials (5 GitGuardian Incidents)

1. **PostgreSQL Credentials**
   - Username: `postgres`
   - Password: `C2ePaa4rxU8fuw28`
   - Host: `db.gnkhponqrnivdijybgnx.supabase.co`
   - Connection strings exposed (pooled + direct)

2. **Supabase Service Role JWT**
   - Full admin access key: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imdua2hwb25xcm5pdmRpanliZ254Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzA0MDY5NywiZXhwIjoyMDgyNjE2Njk3fQ...`
   - ⚠️ Bypasses ALL Row Level Security (RLS) policies

3. **Supabase JWT Secret**
   - Secret: `qlgHj7MVArsHBZGU5+SZtUzQn1FqvK2BfZRD5cfYGsS3PozXfUMOSg5O2+YHUzybV7KIo7kIUv2sSIu/jDDPcg==`
   - Used to sign/verify ALL Supabase JWTs

4. **Generic High Entropy Secrets**
   - Supabase Secret Key: `sb_secret_7pUsrnKMT45a1_4e6yQLzQ_ocuyuDZi`
   - Internal API Key: `victory-secret-key-2025`

5. **Riot API Key** (already leaked before)
   - Key: `RGAPI-9860c50d-0d24-441b-a350-fbce693ce6c8`

## ⚠️ IMMEDIATE ACTIONS REQUIRED (WITHIN 1 HOUR)

### 1. Rotate Supabase Credentials (HIGHEST PRIORITY)

**Why First**: Service Role Key bypasses ALL security - attacker has full database access!

#### Step 1: Reset Database Password
```bash
1. Go to: https://supabase.com/dashboard/project/gnkhponqrnivdijybgnx/settings/database
2. Click "Reset Database Password"
3. Generate new password (save to password manager)
4. Click "Reset Password"
```

#### Step 2: Rotate JWT Secret (Invalidates ALL tokens)
```bash
1. Go to: https://supabase.com/dashboard/project/gnkhponqrnivdijybgnx/settings/api
2. Under "JWT Settings" → Click "Generate new JWT secret"
3. CONFIRM (this will invalidate ALL existing JWTs!)
4. Copy new Service Role Key
5. Copy new Anon Key
```

### 2. Update Vercel Environment Variables

```bash
# After rotating credentials, update Vercel:
cd "/Users/merlinmechler/Library/Mobile Documents/com~apple~CloudDocs/Data Analysis/Win_Predicition_System_WR"

# Remove old POSTGRES_URL
echo "y" | vercel env rm POSTGRES_URL production
echo "y" | vercel env rm POSTGRES_URL preview
echo "y" | vercel env rm POSTGRES_URL development

# Add new POSTGRES_URL (replace with new password)
printf "postgresql://postgres.gnkhponqrnivdijybgnx:NEW_PASSWORD@aws-1-eu-central-1.pooler.supabase.com:5432/postgres?sslmode=require" | vercel env add POSTGRES_URL production
printf "postgresql://postgres.gnkhponqrnivdijybgnx:NEW_PASSWORD@aws-1-eu-central-1.pooler.supabase.com:5432/postgres?sslmode=require" | vercel env add POSTGRES_URL preview
printf "postgresql://postgres.gnkhponqrnivdijybgnx:NEW_PASSWORD@aws-1-eu-central-1.pooler.supabase.com:5432/postgres?sslmode=require" | vercel env add POSTGRES_URL development

# Update Supabase Service Role Key
vercel env rm SUPABASE_SERVICE_ROLE_KEY production
printf "NEW_SERVICE_ROLE_KEY" | vercel env add SUPABASE_SERVICE_ROLE_KEY production

# Update Supabase Anon Key
vercel env rm NEXT_PUBLIC_SUPABASE_ANON_KEY production
printf "NEW_ANON_KEY" | vercel env add NEXT_PUBLIC_SUPABASE_ANON_KEY production
```

### 3. Rotate Riot API Key

```bash
1. Go to: https://developer.riotgames.com/
2. Delete existing API key
3. Generate new API key
4. Update in Vercel:
   vercel env rm RIOT_API_KEY production
   printf "NEW_RIOT_KEY" | vercel env add RIOT_API_KEY production
```

### 4. Update Local Environment

```bash
# Update your local .env file with new credentials
nano .env

# Replace:
# - POSTGRES_PASSWORD with new password
# - POSTGRES_URL with new connection string
# - RIOT_API_KEY with new key
# - SUPABASE_SERVICE_ROLE_KEY with new key
```

## 📊 Impact Assessment

### Potential Attack Vectors

1. **Full Database Access**
   - Attacker can read/write/delete ALL data
   - Service Role Key bypasses Row Level Security
   - Access to user data, match history, model data

2. **JWT Forgery**
   - Can create valid JWTs for ANY user
   - Impersonate administrators
   - Bypass authentication entirely

3. **Riot API Abuse**
   - Can make API calls on your behalf
   - Risk of rate limit violations
   - Possible account suspension

### Timeline

- **13:22:36 UTC (2026-01-02)**: Secrets committed to GitHub (commit `bf3de82`)
- **~13:22:36 UTC**: GitGuardian detected 5 incidents (email sent)
- **~13:35 UTC**: Secrets removed from git (commit `673e53d`)
- **⚠️ CURRENT**: Secrets still active in Supabase/Vercel

**Exposure Window**: ~13 minutes and counting until credentials rotated

## ✅ Remediation Checklist

- [x] Remove `.env.vercel.new` from git
- [x] Add `.env.vercel*` to `.gitignore`
- [x] Push security fix commit
- [ ] **Rotate Supabase Database Password** (PRIORITY 1)
- [ ] **Rotate Supabase JWT Secret** (PRIORITY 2)
- [ ] **Update all Vercel Environment Variables**
- [ ] **Rotate Riot API Key**
- [ ] **Update local .env file**
- [ ] **Test application after rotation**
- [ ] **Monitor Supabase logs for suspicious activity**

## 🔍 Post-Incident Review

### Root Cause

The command `vercel env pull .env.vercel.new` was used to download environment variables, and the resulting file was accidentally staged and committed by the automated commit that included:
- Deleted Next.js API routes
- New `app/champion/[name]/page.tsx`
- **Unintentionally**: `.env.vercel.new`

### Prevention Measures

1. ✅ Added `.env.vercel*` to `.gitignore`
2. ✅ Added `package-lock 2.json` to `.gitignore`
3. 🔄 TODO: Review git pre-commit hooks to block secret commits
4. 🔄 TODO: Enable GitGuardian pre-commit scanning

## 📞 Support

If you encounter issues during credential rotation:
- **Supabase Support**: https://supabase.com/dashboard/support
- **Vercel Support**: https://vercel.com/support
- **Riot Developer Support**: https://developer.riotgames.com/

---

**Last Updated**: 2026-01-02 13:35 UTC
**Status**: 🔴 ACTIVE INCIDENT - Credentials rotation in progress
