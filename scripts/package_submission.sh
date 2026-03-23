#!/usr/bin/env bash
# Collect artifact, log, train_gpt.py, git hash, and parsed metrics into submission_package/<NAME>/.
set -euo pipefail
cd "$(dirname "$0")/.."
NAME="${1:?usage: package_submission.sh <package_name> [path/to/train.log]}"
LOG_SRC="${2:-}"
OUT="submission_package/${NAME}"
mkdir -p "${OUT}"

cp train_gpt.py "${OUT}/"

if [[ -n "$LOG_SRC" && -f "$LOG_SRC" ]]; then
  cp "$LOG_SRC" "${OUT}/train.log"
elif [[ -f train.log ]]; then
  cp train.log "${OUT}/train.log"
else
  shopt -s nullglob
  runs=(results/runs/*/train.log)
  if ((${#runs[@]} > 0)); then
    latest="${runs[0]}"
    for f in "${runs[@]}"; do
      [[ "$f" -nt "$latest" ]] && latest="$f"
    done
    cp "$latest" "${OUT}/train.log"
  fi
  shopt -u nullglob
fi

shopt -s nullglob
for f in final_model.int8.ptz final_model.int6.ptz; do
  [[ -f "$f" ]] && cp "$f" "${OUT}/" && break
done
shopt -u nullglob

{
  git rev-parse HEAD 2>/dev/null || echo "unknown"
  echo "packaged_utc: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "hostname: $(hostname)"
} > "${OUT}/git_commit.txt"

LOG="${OUT}/train.log"
if [[ -f "$LOG" ]]; then
  python3 parse_logs.py "$LOG" --json > "${OUT}/metrics.json"
  PTZ=( "${OUT}"/final_model.*.ptz )
  if ((${#PTZ[@]})) && [[ -f "${PTZ[0]}" ]]; then
    python3 artifact_check.py "${PTZ[0]}" > "${OUT}/artifact_check.txt" 2>&1 || true
  else
    echo "no .ptz in package" > "${OUT}/artifact_check.txt"
  fi
else
  echo '{"error":"no train.log in package"}' > "${OUT}/metrics.json"
fi

echo "Wrote ${OUT}"
ls -la "${OUT}"
