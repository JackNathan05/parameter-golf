# Submission summary (Parameter Golf)

Fill this in for a leaderboard PR or your own records. Replace `_…_` placeholders.

## Title

_…_

## Author / handle

_…_

## Score

- **val_bpb:** _…_ (lower is better)
- **Source:** _e.g. final_int8_zlib_roundtrip_exact / sliding window (disclose if not standard)_

## Artifact size

- **Total bytes:** _…_ (must be ≤ 16,000,000)
- **Layout:** _e.g. int8+zlib + train_gpt.py_

## Train runtime

- **Wall-clock:** _…_ seconds
- **Hardware:** _e.g. 8× H100 SXM_
- **Record track:** _yes / no (non-record)_

## Core idea

_2–4 sentences: what you changed and why it should improve bpb._

## Exact changes from baseline

_Bullet list: arch, quantization, schedule, eval (if any)._

## Why it works

_Short mechanistic story._

## Risks / caveats

_Variance, eval differences, things that might not reproduce._

## Reproducibility steps

1. Commit: `git checkout <hash>`
2. Data: _cached_challenge_fineweb command_
3. Train: _exact env vars + torchrun command_
4. Verify: `python parse_logs.py train.log --json` and `python artifact_check.py final_model.int8.ptz`

## Validity checklist

- [ ] Artifact under 16,000,000 bytes  
- [ ] Code self-contained in `train_gpt.py` per challenge rules  
- [ ] Clean checkout reproduces  
- [ ] Logs parse; final score matches intended metric line  
- [ ] No undisclosed extra training or eval protocol changes  
