#!/usr/bin/env python3
"""
Startup script for the AI QA Bot Backend
This script helps you get the Flask server running with proper setup
"""

import os
import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_and_install_dependencies():
    """Check and install required dependencies"""
    print("📦 Checking dependencies...")
    
    required_packages = [
        'flask',
        'flask-cors', 
        'python-dotenv'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} is missing")
    
    if missing_packages:
        print(f"\n🔧 Installing missing packages: {', '.join(missing_packages)}")
        try:
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install'
            ] + missing_packages)
            print("✅ Dependencies installed successfully")
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies")
            print("💡 Try running: pip install flask flask-cors python-dotenv")
            return False
    
    return True

def check_env_file():
    """Check if .env file exists and has required keys"""
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    template_path = os.path.join(os.path.dirname(__file__), '.env.template')
    
    if not os.path.exists(env_path):
        print("⚠️  .env file not found")
        if os.path.exists(template_path):
            print("💡 Copying .env.template to .env")
            with open(template_path, 'r') as template:
                content = template.read()
            with open(env_path, 'w') as env_file:
                env_file.write(content)
            print("✅ .env file created from template")
            print("📝 Please edit .env file and add your API keys")
        else:
            print("💡 Please create a .env file with your API keys")
        return False
    
    print("✅ .env file found")
    return True

def start_server():
    """Start the Flask server"""
    print("\n🚀 Starting AI QA Bot Backend Server...")
    print("🏢 Business Bot: ReACT technique")
    print("🏥 Healthcare Bot: Self-Ask technique")
    print("📡 Server will run on http://localhost:5000")
    print("🔄 Starting in 3 seconds...")
    
    import time
    time.sleep(3)
    
    # Import and run the server
    try:
        from server import app
        app.run(debug=True, port=5000, host='0.0.0.0')
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False

def main():
    """Main startup routine"""
    print("🤖 AI QA Bot Backend Startup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Check and install dependencies
    if not check_and_install_dependencies():
        return
    
    # Check environment file
    env_exists = check_env_file()
    if not env_exists:
        print("\n⚠️  Please configure your .env file before starting the server")
        print("🔑 You need GEMINI_API_KEY and optionally PINECONE_API_KEY")
        return
    
    # Start the server
    start_server()

if __name__ == "__main__":
    main()
