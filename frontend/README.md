# AI QA Bot Frontend

A modern Next.js frontend for the Business and Healthcare AI QA bots with ChatGPT-style interface.

## Features

- 🎨 **Modern UI**: ChatGPT-inspired interface with smooth animations
- 🌓 **Dark/Light Theme**: Toggle between themes with system preference detection
- 🤖 **Dual Bot Support**: Switch between Business and Healthcare assistants
- 📱 **Responsive Design**: Works on desktop, tablet, and mobile
- ⚡ **Real-time Chat**: Instant responses with typing indicators
- 🎯 **Clean Architecture**: Separate frontend and backend with API routes

## Quick Start

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Start Development Server
```bash
npm run dev
```

### 3. Start Python Backend
```bash
cd frontend/api
pip install flask flask-cors
python server.py
```

### 4. Open Browser
Visit `http://localhost:3000`

## Project Structure

```
frontend/
├── app/
│   ├── api/chat/route.ts        # Next.js API route
│   ├── components/
│   │   └── ThemeProvider.tsx    # Theme context
│   ├── globals.css              # Global styles
│   ├── layout.tsx               # Root layout
│   └── page.tsx                 # Main chat interface
├── api/
│   └── server.py                # Flask backend server
├── package.json
├── tailwind.config.js
└── next.config.js
```

## Integration with AI Bots

To connect with your actual AI bots:

1. **Refactor notebook code** into importable Python modules
2. **Update `api/server.py`** to import your bot classes:
   ```python
   from your_business_bot import EnhancedBusinessQABot
   from your_healthcare_bot import HealthcareQABot
   ```
3. **Initialize bots** with proper configuration
4. **Replace placeholder responses** with actual bot.ask() calls

## Features

### Theme Support
- Auto-detects system preference
- Persistent theme selection
- Smooth transitions

### Bot Switching
- Toggle between Business and Healthcare bots
- Visual indicators for each bot type
- Context-aware messaging

### Chat Interface
- Auto-expanding textarea
- Typing indicators
- Message animations
- Scrollable history
- Mobile-friendly design

## Technology Stack

- **Frontend**: Next.js 14, React 18, TypeScript
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **Backend**: Flask, Python
- **API**: Next.js API Routes + Flask

## Development

### Frontend Development
```bash
npm run dev     # Start Next.js dev server
npm run build   # Build for production
npm run start   # Start production server
```

### Backend Development
```bash
python api/server.py  # Start Flask server
```

### Environment Variables
Create `.env.local` in frontend directory:
```
NEXT_PUBLIC_API_URL=http://localhost:5000
```

## Deployment

### Vercel (Frontend)
```bash
npm run build
# Deploy to Vercel
```

### Python Backend
Deploy Flask app to your preferred platform (Railway, Heroku, etc.)

This provides a production-ready chat interface for your AI QA bots with modern UX and seamless bot switching.
