# Deployment Guide

This guide details how to deploy CryptoGuide AI to production using **Railway** (Backend) and **Vercel** (Frontend).

## 1. Backend Deployment (Railway)

We host the FastAPI backend on Railway because of its native Python support and seamless Docker integration.

### Prerequisites
- GitHub repository with the `backend/` folder.
- Railway account.

### Steps
1. **New Project:** Go to Railway Dashboard -> "New Project" -> "Deploy from GitHub repo".
2. **Root Directory:** In Settings -> General -> "Root Directory", set it to `/backend`.
3. **Build Command:** Railway automatically detects `requirements.txt`. No custom build command needed.
4. **Start Command:**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
5. **Environment Variables:**
   Add the following variables in the "Variables" tab:
   - `OPENAI_API_KEY`: `sk-...`
   - `ANTHROPIC_API_KEY`: `sk-ant...`
   - `SUPABASE_URL`: `https://...`
   - `SUPABASE_KEY`: `...` (Service role key recommended for ingestion, Anon key okay for read-only RAG)
   - `PORT`: `8000` (Railway sets this automatically, but good to be explicit)

### Verification
- Once deployed, Railway provides a public URL (e.g., `https://backend-production.up.railway.app`).
- Visit `https://<YOUR_URL>/health` to confirm the RAG pipeline is ready.
- Visit `https://<YOUR_URL>/docs` to see the Swagger UI.

---

## 2. Frontend Deployment (Vercel)

We host the React frontend on Vercel for its Edge Network performance and zero-config React support.

### Prerequisites
- GitHub repository with the `frontend/` folder.
- Vercel account.

### Steps
1. **New Project:** Go to Vercel Dashboard -> "Add New..." -> "Project" -> Import your repo.
2. **Root Directory:** Edit "Root Directory" to `frontend`.
   - Vercel will automatically detect Vite.
3. **Build Settings:**
   - Framework Preset: `Vite`
   - Build Command: `npm run build`
   - Output Directory: `dist`
4. **Environment Variables:**
   - `VITE_API_URL`: The full URL of your deployed Railway backend (e.g., `https://backend-production.up.railway.app`).
   *Note: Do NOT add a trailing slash.*

### Verification
- Vercel will build and deploy.
- Visit the provided domain (e.g., `https://cryptoguide-ai.vercel.app`).
- Test a query to ensure the frontend can reach the backend (check Network tab for CORS errors if it fails).

---

## 3. Database (Supabase)

Since Supabase is a managed service, "deployment" just means ensuring production readiness.

### Checklist
1. **Network Restrictions:** If you enabled "Network Restrictions" in Supabase Settings, make sure to allow connections from:
   - Railway's IP ranges (or allow `0.0.0.0/0` if Railway IPs are dynamic).
   - Your local machine (for ingestion scripts).
2. **Table Policies (RLS):**
   - Our RAG pipeline uses the `service_role` key (or backend logic) to query. Ensure RLS isn't blocking the `postgres` role if you're using direct connection in the backend.

---

## 4. Post-Deployment Checks

1. **Comparison Mode:** Test the multi-protocol comparison to ensure timeout limits on Railway aren't hit (Railway limit is usually convenient, but Vercel serverless functions have a 10s default timeout — since we call from the client, browser timeout applies, which is safer).
2. **Latency:** First request might be slow due to "cold starts" if you are on free tiers.
