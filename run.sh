#!/bin/bash

echo "================================================"
echo "Build Sheet Generator V3 - Starting Server"
echo "================================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/upgrade dependencies
echo "Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Start the Flask server
echo ""
echo "Starting web server..."
echo "Access the application at: http://localhost:5000"
echo "Or from another computer: http://YOUR-IP-ADDRESS:5000"
echo ""
echo "Press CTRL+C to stop the server"
echo ""
python app.py
