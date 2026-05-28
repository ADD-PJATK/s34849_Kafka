#!/usr/bin/env bash
# scripts/demo.sh — end-to-end demo: start server, run pipeline, run tests, stop server
# Run from repo root after bugs are fixed. All tests should pass.
set -e
cd "$(dirname "$0")/.."

echo "=== AA4 End-to-End Demo ==="
echo ""

echo "[1/4] Installing dependencies..."
pip install -r mock/server/requirements.txt --quiet

echo "[2/4] Starting mock server (background)..."
python mock/server/server.py &
SERVER_PID=$!
sleep 3

echo "[3/4] Running integration pipeline..."
python integration/pipeline/run_pipeline.py

echo "[4/4] Running tests..."
python -m pytest integration/tests/ -v

echo ""
echo "Stopping mock server (PID $SERVER_PID)..."
kill "$SERVER_PID" 2>/dev/null || true

echo ""
echo "=== Demo complete ==="
echo "Check out/ for anonymized pipeline output."
