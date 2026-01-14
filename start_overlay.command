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

# Auto-Heal: Python
if [ ! -d ".venv" ]; then
    echo "⚠️  First time run? Initializing Python Brain..."
    python -m venv .venv
    source .venv/bin/activate
    pip install ultralytics fastapi uvicorn[standard] websockets pynput pyautogui mss opencv-python
else
    echo "✅ Found Virtual Environment (.venv)"
    source .venv/bin/activate
fi

# Auto-Heal: UI
if [ ! -d "overlay-ui/node_modules" ]; then
    echo "⚠️  UI Dependencies missing. Installing now..."
    echo "   (This takes about 1-2 minutes, please wait)"
    cd overlay-ui
    npm install
    cd ..
    echo "✅ UI Ready."
else
    echo "✅ UI Dependencies Found."
fi

# Start Frontend
echo "🎨 Starting Liquid UI..."
cd overlay-ui
# We try 'npm run electron' which works in dev. 
# If you built the app, we could launch the .app instead, but this is safer for dev.
npm run dev:all

# Cleanup
echo "🛑 Shutting down AI Core..."
kill $SERVER_PID
exit 0
