#!/usr/bin/env bash
# Run a queue of commands (one per line) from a file. Stops after MAX_FAIL consecutive failures.
set -euo pipefail
cd "$(dirname "$0")/.."
QUEUE="${1:-scripts/experiment_queue.example.txt}"
MAX_FAIL="${MAX_FAIL:-3}"
FAIL=0
LINE=0
if [[ ! -f "$QUEUE" ]]; then
  echo "launch_batch: missing queue file: $QUEUE" >&2
  exit 1
fi
while IFS= read -r cmd || [[ -n "$cmd" ]]; do
  LINE=$((LINE + 1))
  [[ -z "${cmd// }" ]] && continue
  [[ "$cmd" =~ ^# ]] && continue
  echo "=== batch line $LINE: $cmd ==="
  if bash -c "$cmd"; then
    FAIL=0
  else
    FAIL=$((FAIL + 1))
    echo "launch_batch: command failed ($FAIL / $MAX_FAIL)"
    if (( FAIL >= MAX_FAIL )); then
      echo "launch_batch: stopping (too many consecutive failures)"
      exit 1
    fi
  fi
done < "$QUEUE"
echo "launch_batch: queue finished"
