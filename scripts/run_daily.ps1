$ErrorActionPreference = 'Stop'
$Project = Split-Path -Parent $PSScriptRoot
Set-Location $Project
if (Test-Path '.venv\Scripts\python.exe') { & '.venv\Scripts\python.exe' '-m' 'app.main' } else { & 'python' '-m' 'app.main' }
exit $LASTEXITCODE
