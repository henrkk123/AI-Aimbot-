#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# Logging
LOG_FILE="$DIR/training_debug.log"
exec > >(tee -a "$LOG_FILE") 2>&1

echo "=================================================="
echo "   🏋️ STARTING TRAINING UI"
echo "   $(date)"
echo "=================================================="

# Helper
check_cmd() {
    if ! command -v "$1" &> /dev/null; then
        echo "❌ CRITICAL ERROR: '$1' command not found."
        read -p "Press Enter to exit..."
        exit 1
    fi
}
check_cmd "python"

# Venv
if [ -d ".venv" ]; then
    echo "✅ Using Virtual Environment"
    source .venv/bin/activate
else
    echo "Using system python..."
fi

# Run
python gui_training.py

echo "--------------------------------"
echo "Process ended."
# Keep open if it crashes fast
read -p "Press Enter to close..."
exit 0
