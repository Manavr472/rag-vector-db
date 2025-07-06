# Vercel Deployment Troubleshooting Guide

## Error: "No Output Directory named 'public' found"

This error occurs when Vercel can't properly detect the Next.js application structure in a monorepo setup. Here are several solutions:

## Solution 1: Use Vercel CLI with Project Settings

1. **Delete the current Vercel project** (if already created):
   ```bash
   vercel remove your-project-name
   ```

2. **Deploy with specific settings**:
   ```bash
   vercel --build-env NEXT_PUBLIC_API_URL=https://your-domain.vercel.app
   ```

3. **Configure in Vercel Dashboard**:
   - Go to your project settings
   - Set **Framework Preset**: Next.js
   - Set **Root Directory**: `frontend`
   - Set **Build Command**: `npm run build`
   - Set **Output Directory**: `.next` (leave as default)
   - Set **Install Command**: `npm install`

## Solution 2: Alternative vercel.json Configuration

Replace the current `vercel.json` with:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "frontend/package.json",
      "use": "@vercel/next"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/api/$1"
    },
    {
      "handle": "filesystem"
    },
    {
      "src": "/(.*)",
      "dest": "/frontend/$1"
    }
  ]
}
```

## Solution 3: Move Frontend to Root (Simplest)

If other solutions don't work, restructure the project:

1. Move all files from `frontend/` to the root directory
2. Move `api/` Python files to root `api/` directory
3. Update `vercel.json`:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/next"
    },
    {
      "src": "api/*.py",
      "use": "@vercel/python"
    }
  ]
}
```

## Solution 4: Deploy Frontend and API Separately

### Deploy Frontend:
1. Create a new Vercel project for just the frontend
2. Point it to the `frontend/` directory
3. Update API calls to use absolute URLs

### Deploy API:
1. Use Vercel Functions or another serverless platform
2. Update CORS settings
3. Update frontend to call the deployed API

## Current Configuration Details

**Current vercel.json**:
- Framework: Next.js in `frontend/` directory
- API: Python functions in `api/` directory
- Routes: API requests go to `/api/*`, everything else to frontend

**If deployment fails, try this step-by-step approach**:

1. **Local testing**:
   ```bash
   cd frontend
   npm run build
   npm start
   ```

2. **Vercel deployment**:
   ```bash
   vercel --prod
   ```

3. **Check build logs** in Vercel dashboard for specific errors

4. **Environment variables** (if needed):
   - Add `GEMINI_API_KEY` and `PINECONE_API_KEY` in Vercel dashboard
   - Set `NODE_ENV=production`

## Alternative Platforms

If Vercel continues to have issues, consider:

1. **Netlify**: Better for monorepos
2. **Railway**: Simpler Python/Node.js deployment
3. **Render**: Good for full-stack applications
4. **Heroku**: Traditional but reliable

## Support Files Created

- `.vercelignore`: Excludes unnecessary files
- Updated `next.config.js`: Removed standalone output
- Root `package.json`: Proper build scripts

Choose the solution that works best for your setup!
