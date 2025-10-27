<#
.\scripts\run-tests.ps1

# Activates or uses the venv python to run pytest and ensures reports dir exists.
# Run this after `setup.ps1`.
#>

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
# repository root is the parent of the scripts directory
$RepoRoot = Resolve-Path (Join-Path $ScriptDir '..')
Set-Location $RepoRoot

$PyExe = Join-Path $RepoRoot ".venv\Scripts\python.exe"
if (-not (Test-Path -Path $PyExe)) {
    Write-Error "Virtual environment python not found at $PyExe. Run .\scripts\setup.ps1 first."
    exit 1
}

$ReportsDir = Join-Path $RepoRoot "reports"
if (-not (Test-Path -Path $ReportsDir)) {
    New-Item -ItemType Directory -Path $ReportsDir | Out-Null
}

Write-Host "Running pytest..."
& $PyExe -m pytest -q
