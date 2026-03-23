#!/usr/bin/env bash
# Copy champion artifacts into results/best/ for a named tag.
set -euo pipefail
TAG="${1:?usage: snapshot_best.sh <tag_name>}"
DEST="results/best/${TAG}"
mkdir -p "${DEST}"
cp train_gpt.py "${DEST}/"
[[ -f final_model.int8.ptz ]] && cp final_model.int8.ptz "${DEST}/" || true
[[ -f train.log ]] && cp train.log "${DEST}/" || true
echo "snapshot -> ${DEST}"
