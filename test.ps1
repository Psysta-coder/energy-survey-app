# test.ps1 - runs the automated tests (fictional data only; no server needed).
#
# Run from the project folder with:
#   powershell -ExecutionPolicy Bypass -File .\test.ps1

Set-Location -Path $PSScriptRoot

$venvPython = ".\.venv\Scripts\python.exe"
if (-not (Test-Path $venvPython)) {
    Write-Host "The environment is not set up yet. Run setup.ps1 first." -ForegroundColor Red
    exit 1
}

& $venvPython -m unittest discover -s tests -v
$code = $LASTEXITCODE

Write-Host ""
if ($code -eq 0) {
    Write-Host "RESULT: ALL TESTS PASSED" -ForegroundColor Green
} else {
    Write-Host "RESULT: SOME TESTS FAILED. Copy the messages above and send them for help." -ForegroundColor Red
}
exit $code
