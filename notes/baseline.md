# Parameter Golf — baseline and objective

## Challenge objective

- **Metric:** FineWeb validation **bits per byte (`val_bpb`)** — lower is better (tokenizer-agnostic compression).
- **Record track constraints:** training must complete within **10 minutes wall-clock on 8× H100 (SXM)**; submitted artifact must be **≤ 16,000,000 bytes** total (model + bundled code as defined by the repo’s export path).
- **Non-record track:** same 16MB artifact cap; compute budget can exceed the 10-minute / 8×H100 rule (see repo README “Notable Non-Record Runs”).

## Allowed innovation areas

Architecture (depth, tying, recurrence, attention variants), quantization and packing, training dynamics (LR, WD, SWA/EMA, QAT), tokenizer/representation ideas that stay within challenge rules, and eval/reporting choices that are explicit and comparable.

## What counts as a winning improvement

A change that **lowers `val_bpb`** on the official validation protocol while keeping the **artifact valid** and the **declared training/eval setup** honest and reproducible. For leaderboard claims, gains must align with the **10-minute / 8×H100** path.

## What would invalidate a result

- Artifact over **16MB** (or wrong accounting of what counts toward the cap).
- Changing validation or metrics **without** documenting it as the experiment.
- Scores that depend on **hidden data**, undisclosed extra training, or non-reproducible local patches.
- Claiming record-track compliance without evidence (logs, wall-clock, hardware).

## Exit criteria (Phase 1)

You can state in one paragraph: the score is **`val_bpb`** on FineWeb val; hard limits are **16MB artifact** and **10 min / 8×H100** for record submissions; this lab optimizes **`val_bpb`** under those constraints; you must not break **reproducibility** or **artifact validity**.

## Baseline statistics (fill in after runs)

After you run 3–5 baseline seeds with **no code changes**, record here:

| Stat | Value |
|------|--------|
| Baseline mean `val_bpb` | _TBD_ |
| Min / max | _TBD_ |
| Artifact size range (bytes) | _TBD_ |
| Train wall time range (seconds) | _TBD_ |
| Instability / variance notes | _TBD_ |
