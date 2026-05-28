# scripts/run_tests.ps1 — install deps and run all integration tests
Set-Location "$PSScriptRoot\.."
Write-Host "Installing dependencies..."
pip install -r mock/server/requirements.txt --quiet
Write-Host "Running tests..."
python -m pytest integration/tests/ -v
