# 🤖 AI QA Bot Collection

Two advanced RAG (Retrieval Augmented Generation) systems using Google Gemini API and Pinecone vector database.

## 🚀 Setup

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

## 🏢 Business Bot (`bot.ipynb`)

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
