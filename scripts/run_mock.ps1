# scripts/run_mock.ps1 — install deps and start the mock server on port 8000
Set-Location "$PSScriptRoot\.."
Write-Host "Installing dependencies..."
pip install -r mock/server/requirements.txt --quiet
Write-Host "Starting mock server at http://localhost:8000 ..."
Write-Host "Open mock/client-dashboard/index.html in a browser to view the dashboard."
Write-Host "Press Ctrl+C to stop."
python mock/server/server.py
