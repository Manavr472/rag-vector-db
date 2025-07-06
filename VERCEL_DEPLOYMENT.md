# 🚀 Vercel Deployment Guide

## 📁 Project Structure for Vercel

Your project should be organized like this for Vercel deployment:

```
Business-bot/
├── vercel.json              # Vercel configuration
├── requirements.txt         # Python dependencies for serverless functions
├── api/                     # Serverless functions
│   ├── chat.py             # Chat endpoint
│   ├── health.py           # Health check
│   └── info.py             # System info
├── frontend/               # Next.js app
│   ├── package.json
│   ├── next.config.js
│   └── app/
│       ├── layout.tsx
│       ├── page.tsx
│       └── components/
└── README.md
```

## 🔧 Deployment Steps

### 1. **Prepare Your Repository**

Make sure all files are committed to your Git repository:

```bash
git add .
git commit -m "Prepare for Vercel deployment"
git push origin main
```

### 2. **Deploy to Vercel**

#### Option A: Vercel CLI (Recommended)
```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy from project root
vercel --prod
```

#### Option B: Vercel Dashboard
1. Go to [vercel.com](https://vercel.com)
2. Click "New Project"
3. Import your GitHub repository
4. Vercel will auto-detect the configuration

### 3. **Environment Variables** (Optional)

If you want full AI functionality, add these in Vercel Dashboard:

- `GEMINI_API_KEY` - Your Google Gemini API key
- `PINECONE_API_KEY` - Your Pinecone API key (optional)

**Note**: The current deployment uses mock responses, so it works without API keys!

## 🎯 What Happens During Deployment

1. **Frontend**: Next.js app builds and deploys
2. **Backend**: Python functions become serverless endpoints
3. **API Routes**: 
   - `/api/chat` - Chat with bots
   - `/api/health` - Health check  
   - `/api/info` - System information

## ✅ Verification

After deployment, test these URLs:

- `https://your-app.vercel.app` - Main application
- `https://your-app.vercel.app/api/health` - Health check
- `https://your-app.vercel.app/api/info` - System info

## 🔄 Automatic Updates

Every push to your main branch will trigger automatic redeployment!

## 🐛 Troubleshooting

### Build Errors?
- Check `vercel.json` configuration
- Ensure `requirements.txt` has correct dependencies
- Verify Next.js configuration in `frontend/next.config.js`

### API Not Working?
- Check serverless function logs in Vercel dashboard
- Verify `/api/*` routes are properly configured
- Test endpoints individually

### Frontend Issues?
- Check browser console for errors
- Verify API calls are using correct paths
- Ensure CORS is properly configured

## 💡 Pro Tips

1. **Use Vercel Preview**: Every PR gets a preview deployment
2. **Check Logs**: View function logs in Vercel dashboard
3. **Environment Variables**: Add via Vercel dashboard for sensitive data
4. **Custom Domain**: Configure in Vercel dashboard settings

## 🎉 You're Ready!

Your AI QA Bot system will be live with:
- ✅ Automatic scaling
- ✅ Global CDN
- ✅ HTTPS by default
- ✅ Continuous deployment
