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
    echo "⚠️  Initializing Python Brain..."
    python -m venv .venv
fi

source .venv/bin/activate
# Force check requirements every time to ensure updates (like customtkinter) are applied
pip install ultralytics fastapi uvicorn[standard] websockets pynput pyautogui mss opencv-python customtkinter packaging pillow

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

if [ ! -f "dist/index.html" ]; then
    echo "🏗️  Building Overlay (First Run)..."
    npm run build
fi

# Run in Production Mode
echo "🚀 Launching Production Mode..."
npm run start

# Cleanup
echo "🛑 Shutting down AI Core..."
kill $SERVER_PID
exit 0
