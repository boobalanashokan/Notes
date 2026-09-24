
$ErrorActionPreference = "Stop"

$RepoRoot = (git rev-parse --show-toplevel).Trim()
Set-Location $RepoRoot

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw "Python was not found. Install Python 3 to refresh progress."
}

python scripts\tracker.py
Write-Host ""
git status --short
