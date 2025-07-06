"""
Minimal Flask server for testing the AI QA Bot system
This version works without external APIs for basic testing
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import time
import json

app = Flask(__name__)
CORS(app)

# Simple mock responses for testing
BUSINESS_RESPONSES = {
    "services": "TechFlow Solutions offers web development, mobile development, cloud solutions, and consulting services. We work with modern technologies like React, Node.js, Python, and cloud platforms.",
    "pricing": "Our pricing varies by project complexity. Web development starts at $5,000, mobile apps from $10,000, and cloud solutions from $3,000. Contact us for a detailed quote.",
    "company": "TechFlow Solutions is a leading software development company founded in 2018. We specialize in delivering innovative technology solutions for businesses worldwide.",
    "default": "I'm TechFlow Solutions' business assistant. I can help with questions about our services, pricing, and company information. What would you like to know?"
}

HEALTHCARE_RESPONSES = {
    "diabetes": "Diabetes is a metabolic disorder characterized by high blood sugar levels. Type 1 develops in childhood, Type 2 is most common and related to insulin resistance. Symptoms include increased thirst, frequent urination, and fatigue.",
    "blood pressure": "Normal blood pressure is less than 120/80 mmHg. High blood pressure (hypertension) is often called the 'silent killer' as it typically has no symptoms. Risk factors include age, family history, and lifestyle factors.",
    "heart disease": "Heart disease prevention includes maintaining a healthy diet, regular exercise, not smoking, managing stress, and regular health screenings including blood pressure and cholesterol checks.",
    "default": "I'm a healthcare information assistant. I provide general health information for educational purposes only. This should not replace professional medical advice."
}

def get_mock_response(message, bot_type):
    """Generate mock responses based on keywords"""
    message_lower = message.lower()
    
    if bot_type == "business":
        if any(word in message_lower for word in ["service", "what do you do", "development"]):
            return BUSINESS_RESPONSES["services"]
        elif any(word in message_lower for word in ["price", "cost", "pricing", "how much"]):
            return BUSINESS_RESPONSES["pricing"]
        elif any(word in message_lower for word in ["company", "about", "who are you"]):
            return BUSINESS_RESPONSES["company"]
        else:
            return BUSINESS_RESPONSES["default"]
    
    elif bot_type == "healthcare":
        if any(word in message_lower for word in ["diabetes", "blood sugar"]):
            return HEALTHCARE_RESPONSES["diabetes"]
        elif any(word in message_lower for word in ["blood pressure", "hypertension"]):
            return HEALTHCARE_RESPONSES["blood pressure"]
        elif any(word in message_lower for word in ["heart", "cardiac", "prevention"]):
            return HEALTHCARE_RESPONSES["heart disease"]
        else:
            return HEALTHCARE_RESPONSES["default"]
    
    return "I'm here to help! Please ask me a question."

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        message = data.get('message', '')
        bot_type = data.get('botType', 'business')
        
        if not message:
            return jsonify({"error": "Message is required"}), 400
        
        print(f"🔄 Processing {bot_type} query: {message[:50]}...")
        
        # Generate mock response
        response = get_mock_response(message, bot_type)
        
        # Add medical disclaimer for healthcare responses
        if bot_type == "healthcare" and "educational purposes" not in response:
            response += "\n\n⚠️ **Medical Disclaimer**: This information is for educational purposes only and should not replace professional medical advice."
        
        result = {
            "response": response,
            "type": bot_type,
            "confidence": 0.85,
            "sources": 1,
            "mode": "demo"
        }
        
        print(f"✅ Mock response generated")
        return jsonify(result)
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "mode": "demo",
        "bots": ["business", "healthcare"],
        "features": ["Basic keyword matching for demo"]
    })

@app.route('/api/info', methods=['GET'])
def info():
    return jsonify({
        "system": "AI QA Bot Demo System",
        "mode": "demo",
        "note": "This is a demo version with mock responses. Configure APIs for full functionality.",
        "bots": {
            "business": {
                "name": "Business QA Bot (Demo)",
                "description": "Demo responses for TechFlow Solutions inquiries"
            },
            "healthcare": {
                "name": "Healthcare QA Bot (Demo)", 
                "description": "Demo health information with disclaimers"
            }
        }
    })

@app.route('/')
def index():
    return jsonify({
        "message": "AI QA Bot Backend is running!",
        "mode": "demo",
        "endpoints": {
            "chat": "/api/chat",
            "health": "/api/health", 
            "info": "/api/info"
        }
    })

if __name__ == '__main__':
    print("🚀 Starting AI QA Bot Demo Server...")
    print("📡 Server running at http://localhost:5000")
    print("🔄 This is a demo version with mock responses")
    print("💡 Configure API keys in .env for full functionality")
    app.run(debug=True, port=5000, host='0.0.0.0')
