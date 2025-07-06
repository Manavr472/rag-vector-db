"""
Vercel serverless function for system info endpoint
"""

import json

def handler(request):
    """System info endpoint"""
    
    # Handle CORS
    if request.method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
            },
            'body': ''
        }
    
    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({
            "system": "Dual AI QA Bot System",
            "mode": "vercel_serverless",
            "deployment": "auto",
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
    }

# For Vercel deployment
def main(request):
    return handler(request)
