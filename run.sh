#!/usr/bin/env bash

set -euo pipefail

# Go to the Git repository root
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null)" || {
    echo "ERROR: Not inside a Git repository."
    exit 1
}

cd "$REPO_ROOT"

echo "========================================"
echo " MLOps Study Notes - Git Automation"
echo "========================================"
echo

echo "[1/6] Current changes:"
git status --short
echo

# Find Python
if command -v python >/dev/null 2>&1; then
    PYTHON="python"
elif command -v python3 >/dev/null 2>&1; then
    PYTHON="python3"
else
    echo "ERROR: Python was not found."
    exit 1
fi

echo "[2/6] Running Python automation..."

# Update tracker from notes
if [[ -f "scripts/tracker.py" ]]; then
    echo "Running scripts/tracker.py..."
    "$PYTHON" scripts/tracker.py
fi

# Update README index if this script exists
if [[ -f "scripts/generate_readme.py" ]]; then
    echo "Running scripts/generate_readme.py..."
    "$PYTHON" scripts/generate_readme.py
fi

echo
echo "[3/6] Changes after automation:"
git status --short
echo

echo "[4/6] Staging changes..."
git add -A

if git diff --cached --quiet; then
    echo
    echo "No changes to commit."
    exit 0
fi

echo
echo "Staged changes:"
git diff --cached --stat
echo

echo "[5/6] Commit message"
read -r -p "Enter commit message: " COMMIT_MESSAGE

if [[ -z "${COMMIT_MESSAGE// }" ]]; then
    echo "ERROR: Commit message cannot be empty."
    exit 1
fi

echo
echo "[6/6] Creating commit..."
git commit -m "$COMMIT_MESSAGE"

echo
echo "========================================"
echo " Commit created successfully."
echo "========================================"
echo
echo "To push to GitHub:"
echo "git push"