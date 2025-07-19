#!/bin/bash

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Running install script..."
    ./install.sh
fi

# Activate virtual environment
source venv/bin/activate

# Run the server
python -m src.server