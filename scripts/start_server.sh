#!/bin/bash
set -e

# Ensure environment is set up
if [ ! -d ".venv" ]; then
  echo "Python virtual environment not found. Please run scripts/init.sh to set up your environment first."
  exit 1
fi

# Activate virtual environment
source .venv/bin/activate

# Run tests (which also runs linting)
./scripts/run_tests.sh
RUN_TESTS_EXIT_CODE=$?
if [ $RUN_TESTS_EXIT_CODE -ne 0 ]; then
  echo "Pre-checks failed (scripts/run_tests.sh). Server will NOT start."
  exit $RUN_TESTS_EXIT_CODE
fi

echo "All checks passed. Starting the server..."

# Start the server
uvicorn github_mcp.server:app --reload --host 0.0.0.0 --port 8000 