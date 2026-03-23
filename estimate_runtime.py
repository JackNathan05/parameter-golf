#!/usr/bin/env python3
"""
Rough runtime label for Parameter Golf record-track (10 min wall-clock on 8× H100).

This is a conservative heuristic, not a predictor. Use it to flag obviously risky configs
before spending money on cloud GPUs.

Usage:
  python estimate_runtime.py --train-seconds 600 --nproc 8
  python estimate_runtime.py --log train.log
  python estimate_runtime.py --train-seconds 4800 --nproc 1 --target-nproc 8
"""

from __future__ import annotations

import argparse
import json
import math
import sys

# Official record-track training cap (seconds)
DEFAULT_TARGET_CAP = 600.0
DEFAULT_TARGET_NPROC = 8


def label_runtime(
    train_seconds: float | None,
    nproc: int,
    target_nproc: int,
    target_cap: float,
    slack: float,
) -> dict:
    """
    Scale observed wall time by (nproc / target_nproc) * slack — optimistic strong scaling.
    If train_seconds is None, status is unknown.
    """
    out: dict = {
        "train_seconds_observed": train_seconds,
        "nproc": nproc,
        "target_nproc": target_nproc,
        "target_cap_seconds": target_cap,
        "slack": slack,
    }
    if train_seconds is None or train_seconds <= 0:
        out["scaled_seconds_est"] = None
        out["label"] = "unknown"
        out["note"] = "No reliable train_seconds; run parse_logs.py on a complete log."
        return out

    # Same GPU count as target: use observed wall time directly (no cross-machine scaling).
    # Fewer GPUs: optimistic strong scaling — time ∝ 1 / nproc for same global step.
    if nproc == target_nproc:
        scaled = train_seconds
    else:
        scaled = train_seconds * (nproc / float(target_nproc)) * slack
    out["scaled_seconds_est"] = round(scaled, 3)

    cap_epsilon = 5.0  # treat small overruns as "at wall" noise from logging / cap hits
    if scaled <= target_cap * 0.85:
        out["label"] = "safe"
        out["note"] = "Scaled wall time is comfortably under 10 min on 8× target (heuristic)."
    elif scaled <= target_cap + cap_epsilon:
        out["label"] = "risky"
        out["note"] = "Near the 10 min wall; verify on 8× H100; variance and cap hits are common."
    else:
        out["label"] = "invalid"
        out["note"] = "Scaled estimate exceeds 10 min — do not claim record track without re-benchmarking on 8× H100."

    return out


def main() -> None:
    p = argparse.ArgumentParser(description="Estimate record-track runtime feasibility (heuristic).")
    p.add_argument("--log", default=None, help="Training log; uses parse_logs.train_seconds")
    p.add_argument("--train-seconds", type=float, default=None, help="Wall-clock training seconds (from log)")
    p.add_argument("--nproc", type=int, default=1, help="GPU count used for the observed run")
    p.add_argument("--target-nproc", type=int, default=DEFAULT_TARGET_NPROC, help="Record-track GPU count (default 8)")
    p.add_argument("--target-cap", type=float, default=DEFAULT_TARGET_CAP, help="Record-track seconds (default 600)")
    p.add_argument(
        "--slack",
        type=float,
        default=1.15,
        help="Multiplicative pessimism on scaled time (default 1.15)",
    )
    p.add_argument("--json", action="store_true", help="Print JSON only")
    args = p.parse_args()

    train_seconds = args.train_seconds
    if args.log:
        try:
            from parse_logs import parse_training_log

            with open(args.log, encoding="utf-8", errors="replace") as f:
                rec = parse_training_log(f.read())
            train_seconds = rec.get("train_seconds")
        except OSError as e:
            print(json.dumps({"error": str(e)}))
            sys.exit(2)

    result = label_runtime(
        train_seconds,
        max(1, args.nproc),
        max(1, args.target_nproc),
        args.target_cap,
        max(1.0, args.slack),
    )
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        for k, v in result.items():
            print(f"{k}: {v}")


if __name__ == "__main__":
    main()
