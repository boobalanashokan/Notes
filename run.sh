#!/usr/bin/env bash

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null)"
cd "$REPO_ROOT"

if command -v python >/dev/null 2>&1; then
    PYTHON="python"
elif command -v python3 >/dev/null 2>&1; then
    PYTHON="python3"
else
    echo "ERROR: Python was not found."
    exit 1
fi

"$PYTHON" scripts/tracker.py
echo
git status --short