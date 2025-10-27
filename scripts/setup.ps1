<#
.\scripts\setup.ps1

# Creates a virtual environment (if missing), installs Python dependencies
# and installs Playwright browsers. Run this from the repository root or
# run it directly; it uses the script directory to locate the repo root.
#>

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
# repository root is the parent of the scripts directory
$RepoRoot = Resolve-Path (Join-Path $ScriptDir '..')
Set-Location $RepoRoot

Write-Host "Repository root: $RepoRoot"

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "python not found in PATH. Please install Python from https://www.python.org/ and reopen PowerShell."
    exit 1
}


if (-not (Test-Path -Path "$RepoRoot\.venv")) {
    Write-Host "Creating virtual environment .venv..."
    python -m venv .venv
}
else {
    Write-Host "Virtual environment .venv already exists."
}

$PyExe = Join-Path $RepoRoot ".venv\Scripts\python.exe"
if (-not (Test-Path -Path $PyExe)) {
    Write-Error "Virtual environment python not found at $PyExe. Ensure venv creation succeeded or activate a Python environment manually."
    exit 1
}

Write-Host "Upgrading pip and installing Python requirements..."
& $PyExe -m pip install -U pip
& $PyExe -m pip install -r "$RepoRoot\requirements.txt"

Write-Host "Installing Playwright browsers (this may take a while)..."
& $PyExe -m playwright install --with-deps

Write-Host "Setup complete. Run tests with: .\scripts\run-tests.ps1"
