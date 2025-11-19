#!/bin/bash
# Setup script for test environment

set -e

echo "=== Kali MCP Test Suite Setup ==="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version)
echo "Found: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "=== Setup Complete! ==="
echo ""
echo "To run tests:"
echo "  source venv/bin/activate"
echo "  make test"
echo ""
echo "Or:"
echo "  source venv/bin/activate"
echo "  pytest"
echo ""
echo "For more options, run: make help"

