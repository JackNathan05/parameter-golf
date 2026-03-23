#!/usr/bin/env bash
# Cheap proxy run: small batch / short iteration budget. Adjust for your machine.
# Logs go to results/runs/${RUN_ID}/train.log

set -euo pipefail
cd "$(dirname "$0")"

RUN_ID="${RUN_ID:-local_proxy}"
OUT="results/runs/${RUN_ID}"
mkdir -p "${OUT}"

export RUN_ID
export DATA_PATH="${DATA_PATH:-./data/datasets/fineweb10B_sp1024}"
export TOKENIZER_PATH="${TOKENIZER_PATH:-./data/tokenizers/fineweb_1024_bpe.model}"

# Example: single-GPU smoke (override in environment)
NPROC="${NPROC:-1}"

if [[ "${USE_MLX:-0}" == "1" ]]; then
  echo "MLX proxy: see README / train_gpt_mlx.py for env vars"
  python3 train_gpt_mlx.py 2>&1 | tee "${OUT}/train.log"
else
  torchrun --standalone --nproc_per_node="${NPROC}" train_gpt.py 2>&1 | tee "${OUT}/train.log"
fi

echo "Log: ${OUT}/train.log"
