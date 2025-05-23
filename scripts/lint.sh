#!/bin/bash
set -e

# Ensure environment is set up
if [ ! -d ".venv" ]; then
  echo "Python virtual environment not found. Please run scripts/init.sh to set up your environment first."
  exit 1
fi

# Activate virtual environment
source .venv/bin/activate

# Run formatters and linters
black --check github_mcp tests
isort --check-only github_mcp tests
flake8 github_mcp tests 