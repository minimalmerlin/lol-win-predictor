# Vercel Deployment Guide

## Overview
This project consists of two separate Vercel deployments:
1. **Backend** (Python FastAPI) - Root directory
2. **Frontend** (Next.js) - `lol-coach-frontend/` directory

## Backend Deployment

### Step 1: Deploy Backend
1. Go to [Vercel Dashboard](https://vercel.com)
2. Click "Add New Project"
3. Import your GitHub repository
4. Configure:
   - **Framework Preset:** Other
   - **Root Directory:** Keep as root (`.`)
   - **Build Command:** Leave empty
   - **Output Directory:** Leave empty

### Step 2: Note Backend URL
After deployment, note your backend URL (e.g., `https://win-predicition-system-wr.vercel.app`)

## Frontend Deployment

### Step 1: Deploy Frontend
1. Create a **new** Vercel project
2. Import the **same** GitHub repository
3. Configure:
   - **Framework Preset:** Next.js
   - **Root Directory:** `lol-coach-frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** Leave default

### Step 2: Set Environment Variable
In Vercel Frontend Settings → Environment Variables:
- **Name:** `NEXT_PUBLIC_API_URL`
- **Value:** Your backend URL from Step 1 (e.g., `https://win-predicition-system-wr.vercel.app`)
- **Environments:** Production, Preview, Development

### Step 3: Redeploy
After adding the environment variable, trigger a redeploy.

## Testing

1. Visit your frontend URL (e.g., `https://lol-coach-frontend.vercel.app`)
2. Try searching for a champion
3. The search should work via the serverless backend

## Notes

- Backend is serverless and stateless
- Champion data is currently hardcoded (static list)
- No database needed for basic functionality
- Both deployments auto-update on git push
