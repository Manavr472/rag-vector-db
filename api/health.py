"""
Vercel serverless function for health check endpoint
"""

import json

def handler(request):
    """Health check endpoint"""
    
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
            "status": "healthy",
            "mode": "vercel_serverless",
            "bots": ["business", "healthcare"],
            "features": ["Serverless deployment", "Auto-scaling"]
        })
    }

# For Vercel deployment
def main(request):
    return handler(request)
