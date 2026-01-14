#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# Logging setup
LOG_FILE="$DIR/launcher_debug.log"
exec > >(tee -a "$LOG_FILE") 2>&1

echo "=================================================="
echo "   🚀 LAUNCHING CV-OVERLAY PRO SYSTEM"
echo "   $(date)"
echo "=================================================="

# Helper to check commands
check_cmd() {
    if ! command -v "$1" &> /dev/null; then
        echo "❌ CRITICAL ERROR: '$1' command not found."
        echo "   Please install it or check your PATH."
        # Keep open for user to read
        read -p "Press Enter to exit..."
        exit 1
    fi
}

check_cmd "python"
check_cmd "npm"

# Virtual Env Check
if [ -d ".venv" ]; then
    echo "✅ Found Virtual Environment (.venv)"
    source .venv/bin/activate
else
    echo "⚠️  No .venv found. Using system python."
    echo "   (Make sure you installed dependencies with: pip install -r requirements.txt)"
fi

# Cleanup old processes
pkill -f "python server.py"

# Start Backend
echo "🧠 Starting AI Core (server.py)..."
python server.py &
SERVER_PID=$!
echo "✅ Server PID: $SERVER_PID"

echo "⏳ Waiting 3 seconds for engine warmup..."
sleep 3

# Check if server is actually running
if ! ps -p $SERVER_PID > /dev/null; then
   echo "❌ ERROR: Backend died immediately. Check 'launcher_debug.log' details."
   echo "   Possible cause: Missing dependencies (ultralytics, fastapi, etc.)"
   read -p "Press Enter to exit..."
   exit 1
fi

# Start Frontend
echo "🎨 Starting Liquid UI..."
cd overlay-ui
# We try 'npm run electron' which works in dev. 
# If you built the app, we could launch the .app instead, but this is safer for dev.
npm run electron

# Cleanup
echo "🛑 Shutting down AI Core..."
kill $SERVER_PID
exit 0
