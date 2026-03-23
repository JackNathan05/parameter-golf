# First manual experiment (Roadmap §8 Task 7)

Goal: one **single-knob** change, full log, ledger row, artifact check — before automating with an agent.

## Option A — no code edit (env only)

Official `train_gpt.py` reads many knobs from environment (see `Hyperparameters`). Example: fixed baseline code, change only seed.

```bash
SEED=42 RUN_ID=exp_seed42 torchrun --standalone --nproc_per_node=1 train_gpt.py 2>&1 | tee results/runs/exp_seed42/train.log
```

Then:

```bash
python parse_logs.py results/runs/exp_seed42/train.log --json
python artifact_check.py final_model.int8.ptz
python evaluate_candidate.py --log results/runs/exp_seed42/train.log --seed 42 --change-summary "baseline duplicate seed 42" --champion-bpb <your_baseline>
```

## Option B — one-line code hypothesis

Edit **`train_gpt.py`** once (e.g. one default in `Hyperparameters` you can justify from `notes/ideas_backlog.md`). Keep the diff minimal; note hypothesis in `prompts/experiment_prompt.md`.

## Record

- Commit hash, `PG_EXPERIMENT_ID` in log (if you set it), `results/experiments.csv` row, artifact bytes.
