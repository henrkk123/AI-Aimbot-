#!/bin/bash
echo "🚀 Starting High-Performance Overlay System..."

# 1. Start Backend (Python)
# Check if venv exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
else
    echo "⚠️ Warning: No .venv found. Trying system python..."
fi

echo "🧠 Initializing Vision Engine (Server)..."
# Run Uvicorn directly to make it easier to kill. 
# --log-level error to keep it clean, but we want to see startup logs.
python server.py &
PID_BACKEND=$!

echo "✅ Backend ID: $PID_BACKEND"
echo "⏳ Waiting for server to warm up..."
sleep 3

# 2. Start Frontend (Electron)
echo "🎨 Launching UI (Overlay)..."
cd overlay-ui
# npm run electron calls 'electron .' 
# But we need to make sure the vite server is accessible or just load the file.
# Since we are in dev, we use 'npm run dev:all' which runs vite AND electron.
npm run dev:all

# Cleanup
echo "🛑 Shutting down backend..."
kill $PID_BACKEND
echo "👋 Done."
