# AI QA Bot Backend

Flask backend for the Dual AI QA Bot System featuring:

- **Business Bot**: Uses ReACT (Reasoning, Acting, Observing) technique for business inquiries
- **Healthcare Bot**: Uses Self-Ask with Search technique for medical questions

## Features

### Business Bot (ReACT Technique)
- Reasoning-based query processing
- Context retrieval from business knowledge base
- Professional responses for TechFlow Solutions

### Healthcare Bot (Self-Ask Technique)
- Complex question decomposition
- Medical information retrieval
- Includes appropriate medical disclaimers

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment**:
   ```bash
   cp .env.template .env
   # Edit .env with your API keys
   ```

3. **Run the server**:
   ```bash
   python server.py
   ```

## API Endpoints

- `POST /api/chat` - Chat with bots
  ```json
  {
    "message": "Your question here",
    "botType": "business" // or "healthcare"
  }
  ```

- `GET /api/health` - Health check
- `GET /api/info` - System information

## Configuration

The system supports both Gemini embeddings and free sentence transformers. Set `USE_SENTENCE_TRANSFORMERS=true` in your `.env` file to use the free option.

## Note

Healthcare information is provided for educational purposes only and should not replace professional medical advice.
