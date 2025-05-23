#!/bin/bash
set -e

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install all dependencies (dev + runtime)
pip install -r requirements-dev.txt

# Show installed packages
pip list

echo "Environment setup complete. To activate later, run: source .venv/bin/activate" 