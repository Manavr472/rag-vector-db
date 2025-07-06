@echo off
echo 🚀 Deploying AI QA Bot System to Vercel...

REM Check if Vercel CLI is installed
vercel --version >nul 2>&1
if errorlevel 1 (
    echo 📦 Installing Vercel CLI...
    npm install -g vercel
)

REM Login to Vercel (if not already logged in)
echo 🔐 Checking Vercel authentication...
vercel whoami || vercel login

REM Deploy to production
echo 🚀 Deploying to production...
vercel --prod

echo ✅ Deployment complete!
echo 🌐 Your app is now live on Vercel!
pause
