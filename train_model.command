#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "🏋️ STARTING TRAINING UI..."
echo "--------------------------------"

# Check for venv
if [ -d ".venv" ]; then
    source .venv/bin/activate
else
    echo "Using system python..."
fi

python gui_training.py

echo "--------------------------------"
echo "Process ended. Close this window."
exit 0
