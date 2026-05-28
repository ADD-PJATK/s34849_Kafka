#!/usr/bin/env bash
# scripts/run_tests.sh — install deps and run all integration tests
set -e
cd "$(dirname "$0")/.."
echo "Installing dependencies..."
pip install -r mock/server/requirements.txt --quiet
echo "Running tests..."
python -m pytest integration/tests/ -v
