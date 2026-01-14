#!/bin/bash

# Get the directory where the script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "=================================================="
echo "   🚀 LAUNCHING CV-OVERLAY PRO SYSTEM"
echo "=================================================="

# Check for venv
if [ -d ".venv" ]; then
    source .venv/bin/activate
else
    echo "⚠️  No .venv found. Using system python."
fi

# Kill old instances (cleanup)
pkill -f "python server.py"

# Start Server
echo "🧠 Starting AI Core (server.py)..."
python server.py > backend.log 2>&1 &
SERVER_PID=$!
echo "✅ Server PID: $SERVER_PID"

echo "⏳ Waiting for engine warmup..."
sleep 2

# Start Electron
echo "🎨 Starting Liquid UI..."
cd overlay-ui
npm run electron

# Cleanup when Electron closes
echo "🛑 Shutting down AI Core..."
kill $SERVER_PID
exit 0
