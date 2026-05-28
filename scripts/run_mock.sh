#!/usr/bin/env bash
# scripts/run_mock.sh — install deps and start the mock server on port 8000
set -e
cd "$(dirname "$0")/.."
echo "Installing dependencies..."
pip install -r mock/server/requirements.txt --quiet
echo "Starting mock server at http://localhost:8000 ..."
echo "Open mock/client-dashboard/index.html in a browser to view the dashboard."
echo "Press Ctrl+C to stop."
python mock/server/server.py
