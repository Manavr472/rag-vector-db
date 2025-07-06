# 🤖 Dual AI QA Bot System

Advanced conversational AI system featuring two specialized bots using cutting-edge RAG techniques.

## 🎯 Features

- **Business Bot**: ReACT (Reasoning, Acting, Observing) for business inquiries
- **Healthcare Bot**: Self-Ask with Search for medical questions  
- **Modern UI**: Next.js frontend with dark/light themes
- **Auto-Deploy**: Ready for Vercel deployment

## 🚀 Quick Deploy to Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/your-username/Business-bot)

**One-click deployment! No setup required.**

## 🏗️ Local Development

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Backend (Optional)
```bash
cd frontend/api
pip install -r requirements.txt
python demo_server.py
```

## 📚 Documentation

- [Vercel Deployment Guide](VERCEL_DEPLOYMENT.md) - Complete deployment instructions
- [Frontend Setup](frontend/README.md) - Frontend-specific details
- [API Documentation](frontend/api/README.md) - Backend API details

## 🛠️ Tech Stack

- **Frontend**: Next.js 14, TypeScript, Tailwind CSS
- **Backend**: Python serverless functions
- **AI**: Google Gemini, Pinecone (optional)
- **Deployment**: Vercel with automatic scaling

## 🎮 Try It Live

The system works out-of-the-box with intelligent mock responses for demonstration purposes.

For full AI capabilities, configure API keys in your deployment environment.

## � Files

```
Business-bot/
├── bot.ipynb                   # Business QA Bot (ReACT pattern)
├── healthcare_qa_bot.ipynb    # Healthcare QA Bot (Self-Ask pattern)
├── frontend/                   # Next.js web interface
│   ├── app/                   # Next.js app directory
│   ├── api/server.py          # Python Flask backend
│   └── package.json           # Frontend dependencies
├── .env                       # API keys
└── README.md                  # This file
```

## 🚀 Setup

### Backend (AI Bots)
1. **Install packages:**
   ```bash
   pip install google-generativeai pinecone-client langchain-google-genai sentence-transformers datasets pandas numpy python-dotenv
   ```

2. **Create `.env` file:**
   ```
   GEMINI_API_KEY=your_key_here
   PINECONE_API_KEY=your_key_here
   ```
   - Get Gemini key: [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Get Pinecone key: [Pinecone.io](https://www.pinecone.io/)

3. **Run notebooks in Jupyter/VS Code**

### Frontend (Web Interface)
1. **Install frontend:**
   ```bash
   cd frontend
   npm install
   ```

2. **Start servers:**
   ```bash
   # Terminal 1 - Python backend
   cd frontend/api
   pip install flask flask-cors
   python server.py

   # Terminal 2 - Next.js frontend  
   cd frontend
   npm run dev
   ```

3. **Open browser:** `http://localhost:3000`

## � Web Interface

**Features:**
- ChatGPT-style interface with dark/light theme
- Switch between Business and Healthcare bots
- Real-time chat with typing indicators
- Mobile-responsive design
- Modern UI with smooth animations

**Access:** `http://localhost:3000` after running setup

## �🏢 Business Bot (`bot.ipynb`)

**Features:** ReACT pattern, advanced reranking, business knowledge, analytics
**Use for:** Customer service, sales support, company information

```python
enhanced_qa_bot.ask_with_analytics("What are your pricing options?")
```

## 🏥 Healthcare Bot (`healthcare_qa_bot.ipynb`)

**Features:** Self-Ask pattern, medical datasets, safety disclaimers, conversation handling
**Use for:** Medical information, symptoms, treatments (educational only)

```python
healthcare_bot.ask("What are the symptoms of diabetes?")
```

## 🔄 Key Differences

| Feature | Business Bot | Healthcare Bot |
|---------|-------------|----------------|
| **Pattern** | ReACT (multi-step reasoning) | Self-Ask (question decomposition) |
| **Data** | Business knowledge base | Hugging Face medical datasets |
| **Safety** | Business compliance | Medical disclaimers |
| **Best for** | Complex business queries | Medical Q&A with safety |

## 🛠️ Tech Stack

- **LLM:** Google Gemini 1.5 Flash
- **Embeddings:** Gemini (768-dim) or Sentence Transformers (384-dim)  
- **Vector DB:** Pinecone
- **Framework:** LangChain

## ⚠️ Disclaimers

- **Business Bot**: Demo purposes only
- **Healthcare Bot**: Educational only - consult healthcare professionals for medical advice

---
