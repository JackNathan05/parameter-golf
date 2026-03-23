# Experiment prompt template

Fill this in before each automated or manual experiment.

## Context

- **Champion `val_bpb`:** _e.g. 1.2244_
- **Champion artifact bytes:** _e.g. under 16,000,000_
- **Allowed scope:** `train_gpt.py` only (unless overridden)

## This run

- **Research wave:** _e.g. Wave 4 — training dynamics_
- **Hypothesis bucket:** _e.g. SWA window / warmdown_

## Hypothesis

_One sentence: what you believe will lower `val_bpb` and why._

## Exact changes

_Bullet list or patch summary — minimal diff._

## Expected mechanism

_How this should improve bits-per-byte without breaking constraints._

## Risks

_What could go wrong (instability, slower wall clock, larger artifact)._

## Success criteria

- `val_bpb` improves vs champion by at least: ___
- Artifact ≤ 16,000,000 bytes
- No invalid evaluation change (unless this run is explicitly about eval)

## Revert condition

_Revert if:_ score worse than champion, crash, oversize artifact, or unclear log.

## Command to run evaluation

```bash
# Example — adjust for your machine
RUN_ID=exp_001 torchrun --standalone --nproc_per_node=1 train_gpt.py
# then:
python parse_logs.py results/runs/exp_001/train.log --json
python artifact_check.py final_model.int8.ptz
python evaluate_candidate.py --log results/runs/exp_001/train.log --change-summary "..." --champion-bpb ...
```

## Required output format (after run)

- hypothesis (repeat)
- exact diff / env vars
- `val_bpb`, artifact bytes, train seconds
- accept / reject / repeat
- one-line next experiment idea
