# Linux - Filesystem & shell

Status: Done

## Purpose
This topic covers the basic command-line operations needed to inspect, organize, and move files in a Linux environment. The goal is to be comfortable using the shell without relying on a GUI and to understand how to create project scaffolds reproducibly.

## Core commands

- `pwd` shows the current directory.
- `ls` lists files and folders.
- `cd` changes the active directory.
- `mkdir` creates new directories.
- `touch` creates empty files.
- `cp`, `mv`, and `rm` copy, move, and remove files.
- `cat`, `less`, `head`, and `tail` inspect file contents.
- `grep` and `find` search content and locate files.
- Pipes (`|`) and redirection (`>`, `>>`, `<`) connect commands and save output.
- Wildcards such as `*` and `?` and proper quoting help target files safely.

## Practical example

```bash
pwd
ls -la
mkdir -p project/backend project/frontend/src project/Foundations project/scripts
cd project
touch README.md
cp README.md README.backup
mv README.backup backend/
ls backend/
head -n 20 README.md
grep -R "FastAPI" .
```

## Repo setup script

A small shell script can scaffold a project structure consistently:

```bash
#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-$(pwd)}"
mkdir -p "$ROOT/backend" \
         "$ROOT/frontend/public" \
         "$ROOT/frontend/src/pages" \
         "$ROOT/frontend/src/assets" \
         "$ROOT/Foundations" \
         "$ROOT/scripts"

for dir in "$ROOT/backend" "$ROOT/frontend/public" "$ROOT/frontend/src/pages" "$ROOT/frontend/src/assets" "$ROOT/Foundations" "$ROOT/scripts"; do
  touch "$dir/.gitkeep"
  rm -f "$dir/.gitkeep"
done

printf 'Project structure created under %s\n' "$ROOT"
```

This mirrors the project layout used here: backend services, a frontend app, foundational notes, and supporting scripts.
