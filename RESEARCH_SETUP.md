# Parameter Golf — research lab setup

This file supplements the upstream [README](README.md) with **your** fork workflow and local paths. Official challenge docs: [openai/parameter-golf](https://github.com/openai/parameter-golf).

## Fork and remotes

- **Your fork:** [github.com/JackNathan05/parameter-golf](https://github.com/JackNathan05/parameter-golf)
- Recommended remotes:
  - `origin` → your fork (push here)
  - `upstream` → `https://github.com/openai/parameter-golf.git` (pull updates)

```bash
cd parameter-golf
git remote rename origin upstream   # if origin was openai
git remote add origin https://github.com/JackNathan05/parameter-golf.git
git fetch origin
```

## Python environment

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```

For MLX on Apple Silicon, follow the main README MLX section (additional packages as listed there).

## Local machine (fill in)

| Field | Value |
|--------|--------|
| OS | e.g. Windows 10 / macOS / Linux |
| GPU | e.g. none / 1× RTX / Apple M-series |
| Path | This repo: `parameter-golf/` |

**CUDA vs MLX:** Use `train_gpt.py` + `torchrun` when you have NVIDIA GPUs; use `train_gpt_mlx.py` on Apple Silicon for fast local iteration.

## Data

Download FineWeb shards per `data/README.md` and the main README, e.g.:

```bash
python data/cached_challenge_fineweb.py --variant sp1024 --train-shards 1
```

## Where logs go

- **Scripts in this lab:** `results/runs/<RUN_ID>/train.log` (see `run_local.sh` / `run_local.ps1`)
- **Manual runs:** redirect `stdout` to a file or use `tee` so `parse_logs.py` can read it.

## Re-run baseline (CUDA example)

From repo root, with data in place:

```bash
set RUN_ID=baseline_sp1024
set DATA_PATH=./data/datasets/fineweb10B_sp1024
set TOKENIZER_PATH=./data/tokenizers/fineweb_1024_bpe.model
torchrun --standalone --nproc_per_node=1 train_gpt.py
```

Then:

```bash
python parse_logs.py <path-to-train.log> --json
python artifact_check.py final_model.int8.ptz
```

PowerShell: use `run_local.ps1` or set `$env:RUN_ID` etc. the same way.

## Research loop files

| File | Purpose |
|------|---------|
| `program.md` | Human policy for agents |
| `prompts/*.md` | Agent system / experiment / review prompts |
| `parse_logs.py` | Extract metrics from logs |
| `artifact_check.py` | 16MB cap check |
| `evaluate_candidate.py` | Append `results/experiments.csv` |
| `estimate_runtime.py` | Heuristic record-track time label |
| `results/experiments.csv` | Experiment ledger |
| `submission_summary.md` | Template for PR / writeup |
| `scripts/snapshot_best.sh` | Save champion snapshot + `metrics.json` + `git_commit.txt` |
| `scripts/revert_last.sh` | Restore `train_gpt.py` from `results/best/<tag>/` |
| `scripts/launch_batch.sh` | Run `scripts/experiment_queue.example.txt` (or custom queue) |
| `scripts/package_submission.sh` | Bundle `submission_package/<name>/` for review |

Copies of **`docs/PROGRESS.md`** and **`docs/ROADMAP.md`** track lab status and the full development track.
