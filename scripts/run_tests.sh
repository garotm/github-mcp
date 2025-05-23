#!/bin/bash
set -e

# Ensure environment is set up
if [ ! -d ".venv" ]; then
  echo "Python virtual environment not found. Please run scripts/init.sh to set up your environment first."
  exit 1
fi

# Activate virtual environment
source .venv/bin/activate

# Run linting first
./scripts/lint.sh
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  echo "Linting failed (scripts/lint.sh). Please fix lint errors before proceeding."
  exit $LINT_EXIT_CODE
fi

# Run tests
pytest tests
TEST_EXIT_CODE=$?
if [ $TEST_EXIT_CODE -ne 0 ]; then
  echo "Tests failed (pytest). Please fix test failures before proceeding."
  exit $TEST_EXIT_CODE
fi

echo "All linting and tests passed." 