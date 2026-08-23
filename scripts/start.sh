#!/bin/bash
# Cyber Risk Platform - Start Script

set -e

echo "🔒 Cyber Risk Quantification Platform"
echo "======================================"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.12+"
    exit 1
fi

# Setup server
echo "📦 Setting up server..."
cd server

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -q -r requirements.txt

echo "🚀 Starting server on http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/api/docs"
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
SERVER_PID=$!

# Setup client
echo ""
echo "🎨 Starting client..."
cd ../client

if command -v python3 &> /dev/null; then
    echo "📱 Client available at http://localhost:5500"
    python3 -m http.server 5500 &
    CLIENT_PID=$!
else
    echo "⚠️  Open client/index.html directly in your browser"
fi

echo ""
echo "✅ Platform started!"
echo "   Server: http://localhost:8000"
echo "   Client: http://localhost:5500"
echo ""
echo "Press Ctrl+C to stop"

# Wait for interrupt
trap "kill $SERVER_PID $CLIENT_PID 2>/dev/null; exit" INT
wait
