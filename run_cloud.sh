#!/usr/bin/env bash
# Tier B: promoted run on a multi-GPU box (e.g. 8× H100). Capture reproducibility metadata.

set -euo pipefail
cd "$(dirname "$0")"

RUN_ID="${RUN_ID:-cloud_promoted}"
OUT="results/runs/${RUN_ID}"
mkdir -p "${OUT}"

{
  echo "commit: $(git rev-parse HEAD 2>/dev/null || echo unknown)"
  echo "date_utc: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "hostname: $(hostname)"
  echo "cuda_visible: ${CUDA_VISIBLE_DEVICES:-}"
} > "${OUT}/run_meta.txt"

export RUN_ID
export DATA_PATH="${DATA_PATH:-./data/datasets/fineweb10B_sp1024}"
export TOKENIZER_PATH="${TOKENIZER_PATH:-./data/tokenizers/fineweb_1024_bpe.model}"

NPROC="${NPROC:-8}"
torchrun --standalone --nproc_per_node="${NPROC}" train_gpt.py 2>&1 | tee "${OUT}/train.log"

echo "Log: ${OUT}/train.log meta: ${OUT}/run_meta.txt"
