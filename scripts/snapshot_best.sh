#!/usr/bin/env bash
# Copy champion code, optional artifacts, git hash, and parsed metrics into results/best/<TAG>/.
set -euo pipefail
cd "$(dirname "$0")/.."
TAG="${1:?usage: snapshot_best.sh <tag_name>}"
DEST="results/best/${TAG}"
mkdir -p "${DEST}"
cp train_gpt.py "${DEST}/"
[[ -f final_model.int8.ptz ]] && cp final_model.int8.ptz "${DEST}/" || true
[[ -f final_model.int6.ptz ]] && cp final_model.int6.ptz "${DEST}/" || true
[[ -f train.log ]] && cp train.log "${DEST}/" || true
git rev-parse HEAD 2>/dev/null > "${DEST}/git_commit.txt" || echo "unknown" > "${DEST}/git_commit.txt"
if [[ -f "${DEST}/train.log" ]]; then
  python3 parse_logs.py "${DEST}/train.log" --json > "${DEST}/metrics.json"
else
  echo '{}' > "${DEST}/metrics.json"
fi
echo "snapshot -> ${DEST}"
