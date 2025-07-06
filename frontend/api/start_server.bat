@echo off
echo 🤖 Starting AI QA Bot Backend Server...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo 💡 Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Change to the script directory
cd /d "%~dp0"

REM Check if virtual environment should be created
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing dependencies...
pip install -q flask flask-cors python-dotenv

REM Check for .env file
if not exist ".env" (
    if exist ".env.template" (
        echo 📝 Creating .env file from template...
        copy ".env.template" ".env"
        echo.
        echo ⚠️  Please edit .env file and add your API keys before running the server
        echo 🔑 You need GEMINI_API_KEY and optionally PINECONE_API_KEY
        echo.
        pause
        exit /b 1
    )
)

REM Start the server
echo.
echo 🚀 Starting Flask server...
echo 📡 Server will be available at http://localhost:5000
echo 🔄 Press Ctrl+C to stop the server
echo.
python server.py

pause
