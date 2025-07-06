"""
Vercel serverless function for chat endpoint
"""

import json
import os
from typing import Dict, Any

# Simple mock responses for Vercel deployment
BUSINESS_RESPONSES = {
    "services": """**TechFlow Solutions** offers comprehensive technology services:

• **Web Development**: React, Vue.js, Angular, Next.js
• **Mobile Development**: Native iOS/Android, React Native, Flutter
• **Cloud Solutions**: AWS, Azure, Google Cloud deployment
• **Consulting Services**: Digital transformation and strategy

We work with modern technologies to deliver scalable solutions.""",
    
    "pricing": """Our **pricing structure** varies by project complexity:

**Web Development:**
• Simple websites: $5,000 - $15,000
• Complex web applications: $20,000 - $100,000+
• E-commerce platforms: $15,000 - $50,000

**Mobile Development:**
• Simple mobile apps: $10,000 - $30,000
• Complex mobile apps: $40,000 - $150,000+

**Cloud & DevOps:**
• Cloud migration: $5,000 - $25,000
• DevOps setup: $3,000 - $15,000

*Contact us for a detailed quote tailored to your needs.*""",
    
    "company": """**TechFlow Solutions** is a leading software development company founded in 2018.

### Our Mission
To deliver innovative technology solutions that drive business growth.

### Our Vision  
To be the most trusted technology partner for businesses worldwide.

### Core Values
• **Innovation**: Embracing cutting-edge technologies
• **Quality**: Delivering excellence in every project
• **Collaboration**: Working closely with our clients
• **Integrity**: Maintaining the highest ethical standards""",
    
    "default": "I'm **TechFlow Solutions'** business assistant. I can help with questions about our *services*, *pricing*, and *company information*. What would you like to know?"
}

HEALTHCARE_RESPONSES = {
    "diabetes": """**Diabetes** is a group of metabolic disorders characterized by high blood sugar levels over a prolonged period.

### Types of Diabetes:
• **Type 1 Diabetes**: Usually develops in childhood, the body doesn't produce insulin
• **Type 2 Diabetes**: Most common form, the body doesn't use insulin properly  
• **Gestational Diabetes**: Develops during pregnancy

### Common Symptoms:
• Increased thirst
• Frequent urination
• Fatigue and weakness
• Blurred vision
• Slow-healing wounds""",
    
    "blood_pressure": """**Hypertension (High Blood Pressure)** is often called the *"silent killer"* because it typically has no symptoms.

### Blood Pressure Ranges:
• **Normal**: Less than 120/80 mmHg
• **Elevated**: 120-129 systolic and less than 80 diastolic
• **Stage 1 hypertension**: 130-139 systolic or 80-89 diastolic
• **Stage 2 hypertension**: 140/90 mmHg or higher

### Risk Factors:
• Age and family history
• Obesity and lack of physical activity
• Tobacco use and excessive salt intake
• Chronic stress

*Treatment may include lifestyle changes and medications.*""",
    
    "heart_disease": """### Heart Disease Prevention

**Lifestyle modifications:**
• Maintain a healthy diet rich in fruits, vegetables, whole grains
• Exercise regularly *(at least 150 minutes of moderate activity per week)*
• Don't smoke and limit alcohol consumption
• Manage stress effectively
• Maintain a healthy weight

**Regular health screenings:**
• Blood pressure checks
• Cholesterol testing  
• Diabetes screening
• Regular check-ups with healthcare provider

*Early prevention is key to maintaining heart health.*""",
    
    "default": "I'm a **healthcare information assistant**. I provide general health information for *educational purposes only*. This should not replace professional medical advice."
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
