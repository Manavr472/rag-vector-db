from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
import time
import google.generativeai as genai
import pinecone
from pinecone import Pinecone, ServerlessSpec
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.schema import Document
from sentence_transformers import SentenceTransformer
from datasets import load_dataset
import json

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

app = Flask(__name__)
CORS(app)

# Configuration classes from notebooks

# Configuration classes from notebooks
class Config:
    def __init__(self):
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        self.pinecone_api_key = os.getenv('PINECONE_API_KEY')
        self.embedding_model = "models/embedding-001"
        self.chat_model = "gemini-1.5-flash"
        self.max_tokens = 150
        self.temperature = 0.1
        self.use_sentence_transformers = False
        self.sentence_transformer_model = "all-MiniLM-L6-v2"
        self.index_name = "business-qa-bot-gemini"
        self.dimension = 768 if not self.use_sentence_transformers else 384
        self.metric = "cosine"
        self.chunk_size = 1000
        self.chunk_overlap = 200
        self.top_k_results = 5
        
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)

class HealthcareConfig:
    def __init__(self):
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        self.pinecone_api_key = os.getenv('PINECONE_API_KEY')
        self.embedding_model = "models/embedding-001"
        self.chat_model = "gemini-1.5-flash"
        self.max_tokens = 200
        self.temperature = 0.2
        self.use_sentence_transformers = False
        self.sentence_transformer_model = "all-MiniLM-L6-v2"
        self.index_name = "healthcare-qa-bot"
        self.dimension = 768 if not self.use_sentence_transformers else 384
        self.metric = "cosine"
        self.chunk_size = 800
        self.chunk_overlap = 150
        self.top_k_results = 7
        self.max_iterations = 3
        self.confidence_threshold = 0.7
        
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)

# Sample knowledge data - in production, this would be loaded from a proper knowledge base
SAMPLE_BUSINESS_KNOWLEDGE = [
    {
        "content": """
        TechFlow Solutions is a leading software development company founded in 2018. 
        We specialize in web applications, mobile development, and cloud solutions.
        
        Our Mission: To deliver innovative technology solutions that drive business growth.
        Our Vision: To be the most trusted technology partner for businesses worldwide.
        
        Core Values:
        - Innovation: We embrace cutting-edge technologies
        - Quality: We deliver excellence in every project
        - Collaboration: We work closely with our clients
        - Integrity: We maintain the highest ethical standards
        """,
        "source": "company_overview"
    },
    {
        "content": """
        Services Offered:
        
        1. Web Development
        - Frontend: React, Vue.js, Angular, Next.js
        - Backend: Node.js, Python, Java, Go
        - Full-stack solutions, API development, microservices
        
        2. Mobile Development
        - Native iOS and Android apps
        - Cross-platform with React Native, Flutter
        - Progressive Web Apps (PWAs)
        
        3. Cloud Solutions
        - AWS, Azure, Google Cloud
        - DevOps and CI/CD, serverless architecture
        - Cloud migration services, containerization
        
        4. Consulting Services
        - Technology strategy, digital transformation
        - IT audits, security assessments
        - Agile coaching, project management
        """,
        "source": "services"
    },
    {
        "content": """
        Pricing Structure:
        
        Web Development:
        - Simple websites: $5,000 - $15,000
        - Complex web applications: $20,000 - $100,000+
        - E-commerce platforms: $15,000 - $50,000
        
        Mobile Development:
        - Simple mobile apps: $10,000 - $30,000
        - Complex mobile apps: $40,000 - $150,000+
        - Cross-platform solutions: 20% additional cost savings
        
        Cloud & DevOps:
        - Cloud migration: $5,000 - $25,000
        - DevOps setup: $3,000 - $15,000
        - Monthly managed services: $2,000 - $10,000
        
        Hourly rates: $75 - $150 per hour depending on expertise level
        """,
        "source": "pricing"
    }
]

SAMPLE_HEALTHCARE_KNOWLEDGE = [
    {
        "content": """
        Diabetes is a group of metabolic disorders characterized by high blood sugar levels over a prolonged period. 
        There are three main types:
        
        Type 1 Diabetes: Usually develops in childhood, the body doesn't produce insulin.
        Type 2 Diabetes: Most common form, the body doesn't use insulin properly.
        Gestational Diabetes: Develops during pregnancy.
        
        Common symptoms include increased thirst, frequent urination, fatigue, and blurred vision.
        """,
        "source": "diabetes_overview"
    },
    {
        "content": """
        Hypertension (High Blood Pressure) is often called the "silent killer" because it typically has no symptoms.
        
        Normal blood pressure: Less than 120/80 mmHg
        Elevated: 120-129 systolic and less than 80 diastolic
        Stage 1 hypertension: 130-139 systolic or 80-89 diastolic
        Stage 2 hypertension: 140/90 mmHg or higher
        
        Risk factors include age, family history, obesity, lack of physical activity, tobacco use, and too much salt.
        Treatment may include lifestyle changes and medications.
        """,
        "source": "hypertension_guide"
    },
    {
        "content": """
        Heart Disease Prevention:
        
        Lifestyle modifications:
        - Maintain a healthy diet rich in fruits, vegetables, whole grains
        - Exercise regularly (at least 150 minutes of moderate activity per week)
        - Don't smoke and limit alcohol consumption
        - Manage stress effectively
        - Maintain a healthy weight
        
        Regular health screenings:
        - Blood pressure checks
        - Cholesterol testing
        - Diabetes screening
        - Regular check-ups with healthcare provider
        """,
        "source": "heart_disease_prevention"
    }
]

# Enhanced EmbeddingManager with fallback knowledge
class EmbeddingManager:
    def __init__(self, config):
        self.config = config
        self.pc = Pinecone(api_key=config.pinecone_api_key) if config.pinecone_api_key else None
        self.index = None
        
        # Load appropriate knowledge base
        if hasattr(config, 'max_iterations'):  # Healthcare config
            self.knowledge_base = SAMPLE_HEALTHCARE_KNOWLEDGE
        else:  # Business config
            self.knowledge_base = SAMPLE_BUSINESS_KNOWLEDGE
        
        if self.pc:
            try:
                self.index = self.pc.Index(config.index_name)
            except:
                print(f"Could not connect to index: {config.index_name}")
        
        if config.use_sentence_transformers:
            self.embedding_model = SentenceTransformer(config.sentence_transformer_model)
        else:
            self.embedding_model = GoogleGenerativeAIEmbeddings(
                model=config.embedding_model,
                google_api_key=config.gemini_api_key
            ) if config.gemini_api_key else None
    
    def generate_embeddings(self, texts):
        if self.config.use_sentence_transformers:
            return self.embedding_model.encode(texts).tolist()
        elif self.embedding_model:
            return self.embedding_model.embed_documents(texts)
        return []
    
    def search_similar(self, query, top_k=None):
        if top_k is None:
            top_k = self.config.top_k_results
        
        # Try Pinecone first
        if self.index and self.embedding_model:
            try:
                query_embedding = self.generate_embeddings([query])[0]
                results = self.index.query(
                    vector=query_embedding,
                    top_k=top_k,
                    include_metadata=True
                )
                
                documents = []
                for match in results['matches']:
                    documents.append({
                        'text': match['metadata'].get('text', ''),
                        'source': match['metadata'].get('source', 'unknown'),
                        'score': match['score']
                    })
                
                if documents:
                    return documents
            except Exception as e:
                print(f"Pinecone search error: {e}")
        
        # Fallback to simple text matching with sample knowledge
        return self._fallback_search(query, top_k)
    
    def _fallback_search(self, query, top_k):
        """Simple text-based search in sample knowledge base"""
        query_words = set(query.lower().split())
        
        scored_docs = []
        for doc in self.knowledge_base:
            content_words = set(doc['content'].lower().split())
            # Simple word overlap scoring
            overlap = len(query_words.intersection(content_words))
            if overlap > 0:
                score = overlap / len(query_words)
                scored_docs.append({
                    'text': doc['content'],
                    'source': doc['source'],
                    'score': score
                })
        
        # Sort by score and return top results
        scored_docs.sort(key=lambda x: x['score'], reverse=True)
        return scored_docs[:top_k]

class ReACTAgent:
    """ReACT (Reasoning, Acting, Observing) Agent for Business QA"""
    def __init__(self, config, embedding_manager):
        self.config = config
        self.embedding_manager = embedding_manager
        self.max_steps = 3
        
        if config.gemini_api_key:
            self.llm = ChatGoogleGenerativeAI(
                model=config.chat_model,
                google_api_key=config.gemini_api_key,
                temperature=config.temperature,
                max_tokens=config.max_tokens
            )
        else:
            self.llm = None
    
    def reason(self, query, context, step_num):
        """Generate reasoning/thought for current step"""
        if not self.llm:
            return f"Analyzing query: {query[:100]}..."
        
        reasoning_prompt = f"""
        You are analyzing a business query. Consider what information is needed to answer it well.
        
        Query: {query}
        Step: {step_num}
        Current context: {len(context) if context else 0} pieces of information found
        
        What should we think about or search for next? Be specific and actionable.
        Respond with just your reasoning (1-2 sentences).
        """
        
        try:
            response = self.llm.invoke(reasoning_prompt)
            return response.content[:200] if hasattr(response, 'content') else "Analyzing query requirements..."
        except:
            return f"Step {step_num}: Searching for relevant business information..."
    
    def act(self, thought, query, existing_context):
        """Take action based on reasoning - search for information"""
        # Extract search terms from thought and query
        search_query = query
        if "search" in thought.lower() or "find" in thought.lower():
            # Use original query for search
            search_results = self.embedding_manager.search_similar(search_query, top_k=3)
        else:
            search_results = self.embedding_manager.search_similar(query, top_k=5)
        
        return search_results
    
    def observe(self, action_results):
        """Observe results of action"""
        if not action_results:
            return "No relevant information found in knowledge base."
        
        observation = f"Found {len(action_results)} relevant documents"
        if action_results:
            top_score = max(r.get('score', 0) for r in action_results)
            observation += f" with highest relevance score: {top_score:.3f}"
        
        return observation
    
    def process_query(self, query):
        """Main ReACT process"""
        context = []
        conversation_log = []
        
        for step in range(1, self.max_steps + 1):
            # Reason
            thought = self.reason(query, context, step)
            conversation_log.append(f"Think {step}: {thought}")
            
            # Act
            action_results = self.act(thought, query, context)
            conversation_log.append(f"Act {step}: Searched knowledge base")
            
            # Observe
            observation = self.observe(action_results)
            conversation_log.append(f"Observe {step}: {observation}")
            
            # Add new results to context
            context.extend(action_results)
            
            # Stop if we have enough context or no new results
            if len(context) >= 5 or not action_results:
                break
        
        return context, conversation_log

class BusinessBot:
    def __init__(self):
        self.config = Config()
        self.embedding_manager = EmbeddingManager(self.config)
        self.react_agent = ReACTAgent(self.config, self.embedding_manager)
        self.greeting_handler = GreetingHandler(self.config)
        
        if self.config.gemini_api_key:
            self.chat_model = ChatGoogleGenerativeAI(
                model=self.config.chat_model,
                google_api_key=self.config.gemini_api_key,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            )
        else:
            self.chat_model = None
    
    def ask(self, question):
        try:
            question = question.strip()
            
            # Handle greetings and conversational inputs
            if self.greeting_handler.is_conversational(question):
                greeting_response = self.greeting_handler.generate_business_greeting_response(question)
                if greeting_response:
                    return {
                        "response": greeting_response,
                        "type": "business_conversational",
                        "confidence": 0.9
                    }
            
            # Use ReACT agent for business queries
            context, reasoning_log = self.react_agent.process_query(question)
            
            # Generate final response
            if not self.chat_model:
                response = "Business bot is not properly configured. Please check your API keys."
                confidence = 0.0
            else:
                if not context:
                    context_text = "No specific information found in the knowledge base."
                else:
                    context_texts = []
                    for doc in context[:5]:  # Limit to top 5 for response generation
                        source = doc.get('source', 'Unknown')
                        text = doc.get('text', '')
                        score = doc.get('score', 0)
                        context_texts.append(f"Source: {source} (Relevance: {score:.3f})\n{text}")
                    context_text = "\n\n---\n\n".join(context_texts)
                
                system_prompt = """You are a professional business assistant for TechFlow Solutions, a leading software development company. 
                You help with questions about services, pricing, company information, and business inquiries. 
                Use the provided context to give accurate, helpful, and professional responses."""
                
                user_prompt = f"""Context:\n{context_text}\n\nQuestion: {question}\n\nProvide a comprehensive and professional answer based on the context. If the context doesn't contain relevant information, provide a helpful general response about our business capabilities."""
                
                try:
                    full_prompt = f"{system_prompt}\n\n{user_prompt}"
                    response_obj = self.chat_model.invoke(full_prompt)
                    response = response_obj.content if hasattr(response_obj, 'content') else str(response_obj)
                    confidence = 0.85 if context else 0.4
                except Exception as e:
                    response = "I'm having trouble processing your request right now. Please try again later, or contact us directly for immediate assistance."
                    confidence = 0.2
            
            return {
                "response": response,
                "type": "business",
                "confidence": confidence,
                "sources": len(context),
                "reasoning_steps": len(reasoning_log) // 3  # Each step has Think, Act, Observe
            }
            
        except Exception as e:
            return {
                "response": "I'm experiencing technical difficulties. Please try again later or contact our support team.",
                "type": "business",
                "confidence": 0.0,
                "error": str(e)
            }

class GreetingHandler:
    def __init__(self, config):
        self.llm = None
        if config.gemini_api_key:
            self.llm = ChatGoogleGenerativeAI(
                model=config.chat_model,
                google_api_key=config.gemini_api_key,
                temperature=config.temperature,
                max_tokens=config.max_tokens
            )

    def detect_intent(self, text):
        if not self.llm:
            # Simple keyword-based detection if LLM not available
            text_lower = text.lower().strip()
            if any(word in text_lower for word in ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]):
                return "greeting"
            elif any(word in text_lower for word in ["bye", "goodbye", "see you", "farewell"]):
                return "farewell"
            elif any(word in text_lower for word in ["thank", "thanks", "appreciate"]):
                return "thank_you"
            elif any(word in text_lower for word in ["how are you", "what are you", "who are you", "what can you do"]):
                return "about_bot"
            return "other"
        
        prompt = f"""
        Classify the following user message into one of these categories: 
        greeting, farewell, thank_you, about_bot, or other.
        
        Message: "{text}"
        Respond with only the category name.
        """
        try:
            response = self.llm.invoke(prompt)
            intent = response.content.strip().lower()
            return intent
        except:
            return "other"

    def generate_greeting_response(self, text):
        intent = self.detect_intent(text)
        
        if intent == "greeting":
            return "Hello! I'm here to help you with your questions. Feel free to ask me anything!"
        elif intent == "farewell":
            return "Thank you for chatting with me! Have a great day and feel free to come back anytime you have questions."
        elif intent == "thank_you":
            return "You're very welcome! I'm glad I could help. Is there anything else you'd like to know?"
        elif intent == "about_bot":
            return "I'm an AI assistant designed to help answer your questions and provide useful information. I can help with a wide range of topics. What would you like to know about?"
        
        return None

    def is_conversational(self, text):
        intent = self.detect_intent(text)
        return intent in ["greeting", "farewell", "thank_you", "about_bot"]

    def generate_business_greeting_response(self, text):
        """Generate business-specific greeting responses"""
        intent = self.detect_intent(text)
        
        if intent == "greeting":
            return "Hello! Welcome to TechFlow Solutions. I'm your business assistant, ready to help you with questions about our services, pricing, company information, and more. How can I assist you today?"
        elif intent == "farewell":
            return "Thank you for your interest in TechFlow Solutions! Have a great day, and don't hesitate to reach out if you need any assistance with your technology needs."
        elif intent == "thank_you":
            return "You're welcome! I'm glad I could help with your business inquiry. If you have any other questions about our services or would like to discuss a project, feel free to ask!"
        elif intent == "about_bot":
            return "I'm TechFlow Solutions' business assistant. I can help you learn about our software development services, pricing, company information, past projects, and answer any questions about working with us. What would you like to know?"
        
        return None

    def generate_healthcare_greeting_response(self, text):
        """Generate healthcare-specific greeting responses"""
        intent = self.detect_intent(text)
        
        if intent == "greeting":
            return "Hello! I'm your healthcare information assistant. I'm here to provide general health information and answer medical questions. Please remember that this is for educational purposes only and shouldn't replace professional medical advice. How can I help you today?"
        elif intent == "farewell":
            return "Take care and stay healthy! Remember, if you have any serious health concerns, please consult with a healthcare professional. Goodbye!"
        elif intent == "thank_you":
            return "You're welcome! I'm glad I could provide helpful health information. Remember, this is for educational purposes only. Always consult with healthcare professionals for medical advice."
        elif intent == "about_bot":
            return "I'm a healthcare information assistant that uses advanced AI to help answer medical questions and provide health information. I break down complex questions and search medical knowledge to give you comprehensive answers. However, please remember that this information is for educational purposes only and should not replace professional medical advice."
        
        return None

class SelfAskAgent:
    """Self-Ask with Search Agent for Healthcare QA"""
    def __init__(self, config, embedding_manager):
        self.config = config
        self.embedding_manager = embedding_manager
        
        if config.gemini_api_key:
            self.llm = ChatGoogleGenerativeAI(
                model=config.chat_model,
                google_api_key=config.gemini_api_key,
                temperature=config.temperature,
                max_tokens=config.max_tokens
            )
        else:
            self.llm = None
    
    def decompose_question(self, main_question):
        """Break down complex question into sub-questions"""
        if not self.llm:
            # Simple heuristic decomposition
            if "and" in main_question.lower():
                parts = main_question.lower().split(" and ")
                return [part.strip() + "?" if not part.endswith("?") else part.strip() for part in parts]
            return [main_question]
        
        decomposition_prompt = f"""
        Break down this health question into 2-3 specific sub-questions that need to be answered to fully address the main question.
        
        Main question: {main_question}
        
        Provide sub-questions as a simple list, one per line, without numbering. Focus on the key components needed to answer comprehensively.
        """
        
        try:
            response = self.llm.invoke(decomposition_prompt)
            content = response.content if hasattr(response, 'content') else str(response)
            
            # Parse sub-questions
            sub_questions = []
            for line in content.strip().split('\n'):
                line = line.strip()
                if line and not line.startswith('-') and not line.startswith('•'):
                    # Clean up numbering and formatting
                    line = line.lstrip('123456789.- ')
                    if line and not line.lower().startswith('sub'):
                        if not line.endswith('?'):
                            line += '?'
                        sub_questions.append(line)
            
            return sub_questions[:3] if sub_questions else [main_question]
        except:
            return [main_question]
    
    def search_and_answer(self, question):
        """Search for information and provide answer for a specific question"""
        # Search for relevant information
        search_results = self.embedding_manager.search_similar(question, top_k=5)
        
        if not search_results:
            return {
                "answer": "I don't have specific information about this topic in my knowledge base.",
                "confidence": 0.2,
                "sources": []
            }
        
        # Prepare context from search results
        context_texts = []
        sources = []
        for doc in search_results:
            source = doc.get('source', 'Medical Database')
            text = doc.get('text', '')
            score = doc.get('score', 0)
            context_texts.append(f"{text}")
            sources.append(source)
        
        context = "\n\n".join(context_texts)
        
        # Generate answer using LLM
        if not self.llm:
            return {
                "answer": f"Based on available information: {context[:300]}...",
                "confidence": 0.5,
                "sources": sources[:3]
            }
        
        answer_prompt = f"""
        Based on the following medical information, provide a clear and accurate answer to the question.
        
        Question: {question}
        
        Medical Information:
        {context}
        
        Provide a helpful, accurate answer based on the information above. Be concise but comprehensive.
        """
        
        try:
            response = self.llm.invoke(answer_prompt)
            answer = response.content if hasattr(response, 'content') else str(response)
            
            # Calculate confidence based on search results quality
            avg_score = sum(doc.get('score', 0) for doc in search_results) / len(search_results)
            confidence = min(0.9, max(0.3, avg_score * 1.2))
            
            return {
                "answer": answer,
                "confidence": confidence,
                "sources": sources[:3]
            }
        except:
            return {
                "answer": f"Based on available medical information, here's what I found: {context[:200]}...",
                "confidence": 0.4,
                "sources": sources[:2]
            }
    
    def self_ask_process(self, main_question):
        """Main Self-Ask process"""
        # Step 1: Decompose the question
        sub_questions = self.decompose_question(main_question)
        
        # Step 2: Answer each sub-question
        sub_answers = []
        all_sources = []
        
        for sub_q in sub_questions:
            result = self.search_and_answer(sub_q)
            sub_answers.append({
                "question": sub_q,
                "answer": result["answer"],
                "confidence": result["confidence"]
            })
            all_sources.extend(result["sources"])
        
        # Step 3: Synthesize final answer
        if not self.llm:
            # Simple synthesis without LLM
            combined_answer = "\n\n".join([f"• {sa['answer']}" for sa in sub_answers])
            final_answer = f"Here's what I found:\n\n{combined_answer}"
            avg_confidence = sum(sa['confidence'] for sa in sub_answers) / len(sub_answers)
        else:
            # Use LLM for sophisticated synthesis
            sub_answers_text = "\n\n".join([
                f"Q: {sa['question']}\nA: {sa['answer']}" 
                for sa in sub_answers
            ])
            
            synthesis_prompt = f"""
            Based on the following sub-questions and answers, provide a comprehensive response to the main question.
            
            Main Question: {main_question}
            
            Sub-Questions and Answers:
            {sub_answers_text}
            
            Synthesize this information into a complete, well-structured answer to the main question.
            """
            
            try:
                response = self.llm.invoke(synthesis_prompt)
                final_answer = response.content if hasattr(response, 'content') else str(response)
                avg_confidence = sum(sa['confidence'] for sa in sub_answers) / len(sub_answers)
            except:
                combined_answer = "\n\n".join([f"• {sa['answer']}" for sa in sub_answers])
                final_answer = f"Based on my analysis:\n\n{combined_answer}"
                avg_confidence = sum(sa['confidence'] for sa in sub_answers) / len(sub_answers)
        
        return {
            "question": main_question,
            "answer": final_answer,
            "confidence": avg_confidence,
            "sources": list(set(all_sources)),  # Remove duplicates
            "sub_questions": sub_questions,
            "sub_answers": sub_answers
        }

class HealthcareBot:
    def __init__(self):
        self.config = HealthcareConfig()
        self.embedding_manager = EmbeddingManager(self.config)
        self.self_ask_agent = SelfAskAgent(self.config, self.embedding_manager)
        self.greeting_handler = GreetingHandler(self.config)
        
    def ask(self, question):
        try:
            question = question.strip()
            
            # Handle greetings and conversational inputs
            if self.greeting_handler.is_conversational(question):
                greeting_response = self.greeting_handler.generate_healthcare_greeting_response(question)
                if greeting_response:
                    return {
                        "response": greeting_response,
                        "type": "healthcare_conversational",
                        "confidence": 0.9
                    }
            
            # Use Self-Ask agent for medical questions
            self_ask_result = self.self_ask_agent.self_ask_process(question)
            
            # Add medical disclaimer
            medical_disclaimer = "\n\n⚠️ **Medical Disclaimer**: This information is for educational purposes only and should not replace professional medical advice. Please consult with a healthcare provider for medical concerns."
            
            response = self_ask_result["answer"] + medical_disclaimer
            
            result = {
                "response": response,
                "type": "healthcare",
                "confidence": self_ask_result["confidence"],
                "sources": len(self_ask_result["sources"]),
                "sub_questions_count": len(self_ask_result["sub_questions"])
            }
            
            return result
            
        except Exception as e:
            return {
                "response": "I'm experiencing technical difficulties with healthcare information retrieval. Please consult with a healthcare professional for medical advice.",
                "type": "healthcare",
                "confidence": 0.0,
                "error": str(e)
            }

# Initialize bots
print("🤖 Initializing AI QA Bot System...")
business_bot = BusinessBot()
healthcare_bot = HealthcareBot()
print("✅ Both bots initialized successfully!")

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        message = data.get('message', '')
        bot_type = data.get('botType', 'business')
        
        if not message:
            return jsonify({"error": "Message is required"}), 400
        
        print(f"🔄 Processing {bot_type} query: {message[:50]}...")
        
        # Route to appropriate bot
        if bot_type == 'business':
            result = business_bot.ask(message)
        elif bot_type == 'healthcare':
            result = healthcare_bot.ask(message)
        else:
            return jsonify({"error": "Invalid bot type. Use 'business' or 'healthcare'"}), 400
        
        print(f"✅ Response generated with confidence: {result.get('confidence', 0):.2f}")
        return jsonify(result)
    
    except Exception as e:
        print(f"❌ Error processing request: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "bots": ["business", "healthcare"],
        "features": ["ReACT for business", "Self-Ask for healthcare"]
    })

@app.route('/api/info', methods=['GET'])
def info():
    """Get information about the bot system"""
    return jsonify({
        "system": "Dual AI QA Bot System",
        "bots": {
            "business": {
                "name": "Business QA Bot",
                "technique": "ReACT (Reasoning, Acting, Observing)",
                "description": "Helps with business inquiries about TechFlow Solutions"
            },
            "healthcare": {
                "name": "Healthcare QA Bot", 
                "technique": "Self-Ask with Search",
                "description": "Provides health information with medical disclaimers"
            }
        },
        "note": "All healthcare information is for educational purposes only"
    })

if __name__ == '__main__':
    print("🚀 Starting Dual AI QA Bot System...")
    print("🏢 Business Bot: ReACT technique for business queries")
    print("🏥 Healthcare Bot: Self-Ask technique for medical questions")
    print("📡 Server running on http://localhost:5000")
    app.run(debug=True, port=5000)
