# scripts/demo.ps1 — end-to-end demo: start server, run pipeline, run tests, stop server
# Run from repo root after bugs are fixed. All tests should pass.
Set-Location "$PSScriptRoot\.."

Write-Host "=== AA4 End-to-End Demo ===" -ForegroundColor Cyan
Write-Host ""

Write-Host "[1/4] Installing dependencies..."
pip install -r mock/server/requirements.txt --quiet

Write-Host "[2/4] Starting mock server (background)..."
$server = Start-Process python -ArgumentList "mock/server/server.py" -PassThru -WindowStyle Hidden
Start-Sleep -Seconds 3

Write-Host "[3/4] Running integration pipeline..."
python integration/pipeline/run_pipeline.py

Write-Host "[4/4] Running tests..."
python -m pytest integration/tests/ -v

Write-Host ""
Write-Host "Stopping mock server..."
Stop-Process -Id $server.Id -Force -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "=== Demo complete ===" -ForegroundColor Green
Write-Host "Check out/ for anonymized pipeline output."
