#!/bin/bash
set -e

# Remove existing virtual environment if it exists
if [ -d ".venv" ]; then
  echo "Removing existing .venv directory to ensure a fresh environment..."
  rm -rf .venv
fi

# Create fresh virtual environment following removal above
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