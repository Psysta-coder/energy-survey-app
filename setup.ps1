# setup.ps1 - one-time setup for the LOCAL fictional-data test app.
#
# Run from the project folder with:
#   powershell -ExecutionPolicy Bypass -File .\setup.ps1
#
# -ExecutionPolicy Bypass applies to this one command only. It does not change
# any system setting.

Set-Location -Path $PSScriptRoot

function Stop-Setup([string]$message) {
    Write-Host ""
    Write-Host "SETUP STOPPED: $message" -ForegroundColor Red
    Write-Host "Read the troubleshooting section in SETUP_FA.md (Persian guide)." -ForegroundColor Yellow
    exit 1
}

function Invoke-Step([string]$exe, [string[]]$arguments, [string]$description) {
    Write-Host ""
    Write-Host ">> $description" -ForegroundColor Cyan
    & $exe @arguments
    if ($LASTEXITCODE -ne 0) {
        Stop-Setup "$description failed (exit code $LASTEXITCODE)."
    }
}

# 1. Find Python 3.10 or newer.
$pythonExe = $null
$pythonPrefix = @()
if (Get-Command py -ErrorAction SilentlyContinue) {
    $pythonExe = "py"
    $pythonPrefix = @("-3")
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonExe = "python"
}
if (-not $pythonExe) {
    Stop-Setup "Python was not found. Install Python 3.12 from python.org and tick 'Add python.exe to PATH'."
}

$versionText = & $pythonExe @pythonPrefix -c "import sys; print(sys.version_info[0], sys.version_info[1])"
if ($LASTEXITCODE -ne 0 -or -not $versionText) {
    Stop-Setup "Python could not be started. Reinstall Python from python.org and tick 'Add python.exe to PATH'."
}
$parts = "$versionText".Trim().Split(" ")
if ([int]$parts[0] -lt 3 -or ([int]$parts[0] -eq 3 -and [int]$parts[1] -lt 10)) {
    Stop-Setup "Python 3.10 or newer is needed. Found version $($parts[0]).$($parts[1])."
}
Write-Host "Python found: version $($parts[0]).$($parts[1])"

# 2. Create the private environment (only once).
if (-not (Test-Path ".\.venv\Scripts\python.exe")) {
    $venvArgs = @($pythonPrefix) + @("-m", "venv", ".venv")
    Invoke-Step $pythonExe $venvArgs "Creating the private Python environment (.venv)"
} else {
    Write-Host "Private environment (.venv) already exists. Skipping."
}

$venvPython = ".\.venv\Scripts\python.exe"

# 3. Install Flask (needs internet once).
Invoke-Step $venvPython @("-m", "pip", "install", "-r", "requirements.txt") "Installing Flask from requirements.txt"

# 4. Create the database tables (safe to repeat; existing data is kept).
Invoke-Step $venvPython @("manage.py", "init-db") "Creating the test database"

# 5. Create the first researcher account in this window.
Invoke-Step $venvPython @("manage.py", "ensure-researcher") "Creating the first researcher account (you type it here; the password is hidden)"

Write-Host ""
Write-Host "Setup finished." -ForegroundColor Green
Write-Host "Next step: powershell -ExecutionPolicy Bypass -File .\start.ps1"
exit 0
