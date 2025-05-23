#!/bin/bash
set -e

# Ensure environment is set up
if [ ! -d ".venv" ]; then
  echo "Python virtual environment not found. Running scripts/init.sh to set up your environment."
  ./scripts/init.sh
fi

# Activate virtual environment
source .venv/bin/activate

# Check if black, isort, and flake8 are installed
for tool in black isort flake8; do
  if ! command -v $tool &> /dev/null; then
    echo "$tool could not be found in the current environment."
    echo "Please check your requirements-dev.txt and scripts/init.sh."
    exit 1
  fi
done

if [[ "$1" == "--fix" ]]; then
  echo "Auto-fixing with black and isort..."
  black github_mcp tests
  isort github_mcp tests
  echo "Auto-fix complete. Please review any remaining flake8 issues below:"
  flake8 github_mcp tests || true
else
  echo "Checking code style (no changes will be made)..."
  black --check github_mcp tests || BLACK_FAIL=1
  isort --check-only github_mcp tests || ISORT_FAIL=1
  flake8 github_mcp tests || FLAKE8_FAIL=1

  if [[ $BLACK_FAIL || $ISORT_FAIL ]]; then
    echo
    echo "Some files do not comply with black or isort style guidelines."
    echo "To auto-fix formatting issues, run: ./scripts/lint.sh --fix"
    exit 1
  fi

  if [[ $FLAKE8_FAIL ]]; then
    echo
    echo "Some files do not comply with flake8 style guidelines. Please fix these issues manually."
    exit 1
  fi

  echo "All files comply with style guidelines."
fi 