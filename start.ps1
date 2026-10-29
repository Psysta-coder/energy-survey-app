# start.ps1 - starts the LOCAL test server (this computer only).
#
# Run from the project folder with:
#   powershell -ExecutionPolicy Bypass -File .\start.ps1
#
# If port 5000 is busy, use another port, for example:
#   powershell -ExecutionPolicy Bypass -File .\start.ps1 -Port 5050

param([int]$Port = 5000)

Set-Location -Path $PSScriptRoot

$venvPython = ".\.venv\Scripts\python.exe"
if (-not (Test-Path $venvPython)) {
    Write-Host "The environment is not set up yet. Run setup.ps1 first." -ForegroundColor Red
    exit 1
}

$env:APP_PORT = "$Port"
Write-Host "Starting the LOCAL test server at http://127.0.0.1:$Port"
Write-Host "Fictional data only. Press Ctrl+C in this window to stop the server."
& $venvPython "app.py"
exit $LASTEXITCODE
