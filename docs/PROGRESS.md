# Parameter Golf — progress log

**Fork (push target):** [github.com/JackNathan05/parameter-golf](https://github.com/JackNathan05/parameter-golf)  
**Upstream:** [openai/parameter-golf](https://github.com/openai/parameter-golf)

Local clone for this workspace lives in `parameter-golf/` (`origin` → fork, `upstream` → OpenAI). Synced copies of this file and `Roadmap.md` live in **`parameter-golf/docs/`** for the git repo.

---

## Completed

### Environment / repo

- [x] Cloned official `parameter-golf` into `parameter-golf/` (shallow clone of upstream).
- [x] Git remotes: `origin` → `JackNathan05/parameter-golf`, `upstream` → `openai/parameter-golf` (see `parameter-golf/.git/config`).
- [x] Pushed research lab tooling to fork (`main`).

### Roadmap Phase 1 — objective and notes

- [x] `parameter-golf/notes/baseline.md` — challenge objective, constraints, invalid results, placeholders for baseline stats (fill after real runs).
- [x] `parameter-golf/notes/leaderboard_notes.md` — patterns from the public leaderboard (quantization, depth, SWA/EMA, etc.).

### Roadmap Phase 2 — setup doc (supplement to upstream README)

- [x] `parameter-golf/RESEARCH_SETUP.md` — venv, remotes, log paths, baseline command sketch, table for local machine specs.

### Roadmap Phase 3 / §8 — research loop tooling

- [x] `parameter-golf/program.md` — agent policy (optimize `val_bpb`, 16MB cap, edit `train_gpt.py` only, priority order, revert rules).
- [x] `parameter-golf/parse_logs.py` — parses logs; status `ok` | `crash` | `oversize` | `parse_error` | **`timeout`** (wall-clock cap hit); `--json` output.
- [x] `parameter-golf/artifact_check.py` — verifies a file is ≤ 16,000,000 bytes (configurable `--limit`).
- [x] `parameter-golf/evaluate_candidate.py` — treats **`timeout` like `ok`** for metric acceptance when comparing to champion.
- [x] `parameter-golf/results/experiments.csv` — experiment ledger.
- [x] Smoke-test row from bundled record log (not your hardware).

### Roadmap Phase 5 — two-tier / runtime

- [x] `parameter-golf/estimate_runtime.py`, `run_local.sh`, `run_local.ps1`, `run_cloud.sh`.

### Roadmap Phase 7 — agent prompts

- [x] `parameter-golf/prompts/system_prompt.md`, `experiment_prompt.md`, `review_prompt.md`.

### Roadmap Phase 8 — folders + scripts

- [x] `results/accepted/`, `rejected/`, `best/`, `runs/` (with `.gitkeep`).
- [x] `scripts/snapshot_best.sh` — copies `train_gpt.py`, artifacts, **`metrics.json`**, **`git_commit.txt`**.
- [x] `scripts/revert_last.sh` / `revert_last.ps1` — restore `train_gpt.py` from `results/best/<tag>/`.
- [x] `scripts/launch_batch.sh` + `scripts/experiment_queue.example.txt` — queue runner (`MAX_FAIL` default 3).
- [x] `submission_package/` in `.gitignore` (generated bundles).

### Roadmap Phase 9 — submission engineering

- [x] `scripts/package_submission.sh` — packs `submission_package/<name>/` (optional second arg: path to `train.log`).
- [x] `submission_summary.md` — PR/writeup template.

### Docs in repo

- [x] `parameter-golf/docs/PROGRESS.md` — copy of this file.
- [x] `parameter-golf/docs/ROADMAP.md` — copy of workspace `Roadmap.md`.

---

## Not done yet (next)

- [ ] Roadmap Phase 2 milestone: venv, `pip install -r requirements.txt`, **your** baseline train + eval + artifact + size check on real hardware.
- [ ] Fill `notes/baseline.md` table with real baseline mean/min/max and variance.
- [ ] Replace or supplement the smoke-test row with your own experiment rows.
- [ ] Roadmap §8 Task 7: one manual “agent-style” experiment in `train_gpt.py`, then automate loops.

---

*Last updated: 2026-03-23*
