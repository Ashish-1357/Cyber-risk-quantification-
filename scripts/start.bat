@echo off
REM Cyber Risk Platform - Start Script (Windows)

echo 🔒 Cyber Risk Quantification Platform
echo ======================================

REM Setup server
echo 📦 Setting up server...
cd server

if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate
pip install -q -r requirements.txt

echo 🚀 Starting server on http://localhost:8000
echo 📚 API Docs: http://localhost:8000/api/docs
start uvicorn main:app --reload --host 0.0.0.0 --port 8000

REM Setup client
echo.
echo 🎨 Starting client...
cd ..\client

echo 📱 Client available at http://localhost:5500
start python -m http.server 5500

echo.
echo ✅ Platform started!
echo    Server: http://localhost:8000
echo    Client: http://localhost:5500
pause
