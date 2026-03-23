#!/usr/bin/env python3
"""
Evaluate one training run: parse logs, optional artifact size override, append results/experiments.csv.

Usage:
  python evaluate_candidate.py --log train.log --change-summary "EMA sweep" --seed 42
  python evaluate_candidate.py --log train.log --artifact final_model.int8.ptz --champion-bpb 1.20
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
import uuid
from datetime import datetime, timezone

from parse_logs import parse_training_log

CSV_PATH = os.path.join("results", "experiments.csv")
CSV_FIELDS = [
    "run_id",
    "timestamp",
    "branch",
    "seed",
    "mode",
    "change_summary",
    "val_bpb",
    "artifact_bytes",
    "train_seconds",
    "status",
    "accepted",
    "notes",
]


def main() -> None:
    p = argparse.ArgumentParser(description="Log a Parameter Golf experiment row.")
    p.add_argument("--log", required=True, help="Path to training log file")
    p.add_argument("--artifact", default=None, help="Optional path to artifact; overrides byte count")
    p.add_argument("--run-id", default=None, help="Defaults to a short UUID")
    p.add_argument("--branch", default="", help="Git branch name")
    p.add_argument("--seed", default="", help="Random seed")
    p.add_argument("--mode", default="cuda", help="e.g. cuda | mlx | proxy")
    p.add_argument("--change-summary", default="", help="One-line description of the change")
    p.add_argument("--champion-bpb", type=float, default=None, help="Current best val_bpb; if set, sets accepted")
    p.add_argument("--margin", type=float, default=0.0, help="Require improvement by at least this much")
    p.add_argument("--notes", default="", help="Extra notes for the ledger")
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Print row only; do not append CSV",
    )
    args = p.parse_args()

    with open(args.log, encoding="utf-8", errors="replace") as f:
        text = f.read()
    rec = parse_training_log(text)

    artifact_bytes = rec.get("artifact_bytes")
    if args.artifact:
        if not os.path.isfile(args.artifact):
            print(f"evaluate_candidate: artifact not found: {args.artifact}", file=sys.stderr)
            sys.exit(2)
        artifact_bytes = os.path.getsize(args.artifact)
        if artifact_bytes > 16_000_000:
            rec["status"] = "oversize"

    val_bpb = rec.get("val_bpb")
    status = rec.get("status", "parse_error")

    accepted = ""
    if args.champion_bpb is not None and val_bpb is not None and status == "ok":
        if val_bpb < args.champion_bpb - args.margin:
            accepted = "yes"
        else:
            accepted = "no"
    elif status != "ok":
        accepted = "no"

    run_id = args.run_id or str(uuid.uuid4())[:12]
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    row = {
        "run_id": run_id,
        "timestamp": ts,
        "branch": args.branch,
        "seed": str(args.seed),
        "mode": args.mode,
        "change_summary": args.change_summary,
        "val_bpb": f"{val_bpb:.8f}" if val_bpb is not None else "",
        "artifact_bytes": str(artifact_bytes) if artifact_bytes is not None else "",
        "train_seconds": f"{rec['train_seconds']:.3f}" if rec.get("train_seconds") is not None else "",
        "status": status,
        "accepted": accepted,
        "notes": args.notes,
    }

    if args.dry_run:
        print(row)
        return

    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
    write_header = not os.path.isfile(CSV_PATH) or os.path.getsize(CSV_PATH) == 0
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        if write_header:
            w.writeheader()
        w.writerow(row)

    print(f"Appended to {CSV_PATH}: run_id={run_id} status={status} accepted={accepted or '?'}")


if __name__ == "__main__":
    main()
