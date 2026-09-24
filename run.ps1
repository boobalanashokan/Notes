```powershell
$ErrorActionPreference = "Stop"

Write-Host "========================================"
Write-Host " MLOps Study Notes - Git Automation"
Write-Host "========================================"
Write-Host ""

# Make sure we are inside a Git repository
git rev-parse --show-toplevel | Out-Null

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: This folder is not inside a Git repository."
    exit 1
}

# Move to Git repository root
$RepoRoot = (git rev-parse --show-toplevel).Trim()
Set-Location $RepoRoot

Write-Host "[1/6] Current changes:"
git status --short
Write-Host ""

# Check Python
$Python = Get-Command python -ErrorAction SilentlyContinue

if (-not $Python) {
    Write-Host "ERROR: Python was not found."
    exit 1
}

Write-Host "[2/6] Running Python automation..."

# Update tracker from notes
if (Test-Path "scripts\tracker.py") {
    Write-Host "Running scripts\tracker.py..."
    python scripts\tracker.py
}

# Update README index if available
if (Test-Path "scripts\generate_readme.py") {
    Write-Host "Running scripts\generate_readme.py..."
    python scripts\generate_readme.py
}

Write-Host ""
Write-Host "[3/6] Changes after automation:"
git status --short
Write-Host ""

Write-Host "[4/6] Staging changes..."
git add -A

# Check if there is anything to commit
git diff --cached --quiet

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "No changes to commit."
    exit 0
}

Write-Host ""
Write-Host "Staged changes:"
git diff --cached --stat
Write-Host ""

Write-Host "[5/6] Commit message"
$CommitMessage = Read-Host "Enter commit message"

if ([string]::IsNullOrWhiteSpace($CommitMessage)) {
    Write-Host "ERROR: Commit message cannot be empty."
    exit 1
}

Write-Host ""
Write-Host "[6/6] Creating commit..."

git commit -m $CommitMessage

Write-Host ""
Write-Host "========================================"
Write-Host " Commit created successfully."
Write-Host "========================================"
Write-Host ""
Write-Host "To push to GitHub:"
Write-Host "git push"
```
