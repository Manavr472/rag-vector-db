# 🤖 AI QA Bot Backend - Quick Start Guide

## 🚨 Connection Error Fix

If you're getting `ECONNREFUSED` error, the Flask backend isn't running. Here's how to fix it:

## Option 1: Quick Demo (Recommended for Testing)

**For immediate testing without API setup:**

```bash
cd frontend/api
python demo_server.py
```

This runs a demo version with mock responses that works without any API keys.

## Option 2: Full Server (Requires API Setup)

### Step 1: Install Dependencies
```bash
cd frontend/api
pip install flask flask-cors python-dotenv
```

### Step 2: Set up Environment
```bash
# Copy template
cp .env.template .env

# Edit .env file and add your API keys:
# GEMINI_API_KEY=your_key_here
# PINECONE_API_KEY=your_key_here (optional)
```

### Step 3: Start Server
```bash
python server.py
```

**Or use the startup scripts:**
- Windows: Double-click `start_server.bat`
- Python: `python start_server.py`

## Option 3: Minimal Setup

If you want to test with minimal dependencies:

```bash
cd frontend/api
pip install flask flask-cors
python demo_server.py
```

## 🔧 Troubleshooting

### Backend not starting?
1. Check Python version: `python --version` (need 3.8+)
2. Install Flask: `pip install flask flask-cors`
3. Try demo server first: `python demo_server.py`

### Frontend can't connect?
1. Make sure backend is running on port 5000
2. Check if localhost:5000 is accessible
3. Ensure CORS is enabled (already configured)

### API errors?
1. Start with demo_server.py first
2. Check .env file has correct API keys
3. Verify network connection for external APIs

## 📡 Server Endpoints

Once running, test these endpoints:

- `GET http://localhost:5000/api/health` - Health check
- `POST http://localhost:5000/api/chat` - Chat with bots
- `GET http://localhost:5000/api/info` - System info

## 🎯 Next Steps

1. **Start with demo**: `python demo_server.py`
2. **Test in browser**: Visit `http://localhost:5000`
3. **Configure frontend**: Make sure your Next.js app is pointing to localhost:5000
4. **Add real APIs**: Configure .env with your API keys for full functionality

## 💡 Pro Tips

- Use `demo_server.py` for quick testing
- Use `server.py` for full AI functionality  
- Check console output for helpful debug info
- Both servers run on port 5000 by default
