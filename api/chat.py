"""
Vercel serverless function for chat endpoint
"""

import json
import os
from typing import Dict, Any

# Simple mock responses for Vercel deployment
BUSINESS_RESPONSES = {
    "services": "TechFlow Solutions offers web development, mobile development, cloud solutions, and consulting services. We work with modern technologies like React, Node.js, Python, and cloud platforms.",
    "pricing": "Our pricing varies by project complexity. Web development starts at $5,000, mobile apps from $10,000, and cloud solutions from $3,000. Contact us for a detailed quote.",
    "company": "TechFlow Solutions is a leading software development company founded in 2018. We specialize in delivering innovative technology solutions for businesses worldwide.",
    "default": "I'm TechFlow Solutions' business assistant. I can help with questions about our services, pricing, and company information. What would you like to know?"
}

HEALTHCARE_RESPONSES = {
    "diabetes": "Diabetes is a metabolic disorder characterized by high blood sugar levels. Type 1 develops in childhood, Type 2 is most common and related to insulin resistance. Symptoms include increased thirst, frequent urination, and fatigue.",
    "blood_pressure": "Normal blood pressure is less than 120/80 mmHg. High blood pressure (hypertension) is often called the 'silent killer' as it typically has no symptoms. Risk factors include age, family history, and lifestyle factors.",
    "heart_disease": "Heart disease prevention includes maintaining a healthy diet, regular exercise, not smoking, managing stress, and regular health screenings including blood pressure and cholesterol checks.",
    "default": "I'm a healthcare information assistant. I provide general health information for educational purposes only. This should not replace professional medical advice."
}

def get_mock_response(message: str, bot_type: str) -> str:
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
            return HEALTHCARE_RESPONSES["blood_pressure"]
        elif any(word in message_lower for word in ["heart", "cardiac", "prevention"]):
            return HEALTHCARE_RESPONSES["heart_disease"]
        else:
            return HEALTHCARE_RESPONSES["default"]
    
    return "I'm here to help! Please ask me a question."

def handler(request):
    """Vercel serverless function handler"""
    
    # Handle CORS
    if request.method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
            },
            'body': ''
        }
    
    if request.method != 'POST':
        return {
            'statusCode': 405,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({"error": "Method not allowed"})
        }
    
    try:
        # Parse request body
        if hasattr(request, 'body'):
            body = json.loads(request.body)
        else:
            body = json.loads(request.get_body())
        
        message = body.get('message', '')
        bot_type = body.get('botType', 'business')
        
        if not message:
            return {
                'statusCode': 400,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({"error": "Message is required"})
            }
        
        # Generate response
        response = get_mock_response(message, bot_type)
        
        # Add medical disclaimer for healthcare responses
        if bot_type == "healthcare" and "educational purposes" not in response:
            response += "\n\n⚠️ **Medical Disclaimer**: This information is for educational purposes only and should not replace professional medical advice."
        
        result = {
            "response": response,
            "type": bot_type,
            "confidence": 0.85,
            "sources": 1,
            "mode": "vercel_serverless"
        }
        
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps(result)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({"error": str(e)})
        }

# For Vercel deployment
def main(request):
    return handler(request)
