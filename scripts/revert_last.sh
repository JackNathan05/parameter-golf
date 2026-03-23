#!/usr/bin/env bash
# Restore train_gpt.py from a snapshot under results/best/<TAG>/ (see snapshot_best.sh).
set -euo pipefail
cd "$(dirname "$0")/.."
TAG="${1:?usage: revert_last.sh <tag_name>}"
SRC="results/best/${TAG}/train_gpt.py"
if [[ ! -f "$SRC" ]]; then
  echo "revert_last: missing $SRC" >&2
  exit 1
fi
cp "$SRC" ./train_gpt.py
echo "restored train_gpt.py from $SRC"
if [[ -f "results/best/${TAG}/git_commit.txt" ]]; then
  echo "snapshot commit: $(cat "results/best/${TAG}/git_commit.txt")"
fi
