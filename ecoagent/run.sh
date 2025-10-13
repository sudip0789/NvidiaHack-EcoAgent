#!/bin/bash

# EcoAgent Quick Start Script

echo "🌍 EcoAgent - Environmental Reporting System"
echo "=============================================="
echo ""

# Check if .env exists and has API key
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    echo "Please create a .env file with your NVIDIA_API_KEY"
    exit 1
fi

# Check if API key is set
if grep -q "your_api_key_here" .env; then
    echo "⚠️  WARNING: Please update your NVIDIA_API_KEY in .env file"
    echo "Get your API key from: https://build.nvidia.com/"
    echo ""
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 Starting Streamlit dashboard..."
echo ""

# Run Streamlit
streamlit run ui/dashboard.py
