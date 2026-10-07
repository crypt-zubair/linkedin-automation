$ErrorActionPreference = 'Stop'
$Project = Split-Path -Parent $PSScriptRoot
Set-Location $Project

py -3.13 -m venv .venv
& '.venv\Scripts\python.exe' -m pip install --upgrade pip
& '.venv\Scripts\python.exe' -m pip install -r requirements.txt

Write-Host 'Python environment is ready.'
Write-Host 'Next: install Ollama, then run: ollama pull llama3.2'
Write-Host 'Then copy .env.example to .env and fill the LinkedIn values.'
