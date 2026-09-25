#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-$(pwd)}"

mkdir -p "$ROOT/backend" \
         "$ROOT/frontend/public" \
         "$ROOT/frontend/src/pages" \
         "$ROOT/frontend/src/assets" \
         "$ROOT/Foundations" \
         "$ROOT/scripts"

# Keep the scaffold simple and consistent without burying the repo in empty files.
for dir in "$ROOT/backend" "$ROOT/frontend/public" "$ROOT/frontend/src/pages" "$ROOT/frontend/src/assets" "$ROOT/Foundations" "$ROOT/scripts"; do
  if [ ! -e "$dir/.gitkeep" ]; then
    : > "$dir/.gitkeep"
  fi
  rm -f "$dir/.gitkeep"
done

printf 'Project structure created under %s\n' "$ROOT"
