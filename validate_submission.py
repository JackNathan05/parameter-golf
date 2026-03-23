#!/usr/bin/env python3
"""
Run Parameter Golf pre-submission checks (artifact size, log parse, optional git clean).

Usage:
  python validate_submission.py --log train.log --artifact final_model.int8.ptz
  python validate_submission.py --log results/runs/my_run/train.log --artifact final_model.int8.ptz --strict
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys

from parse_logs import parse_training_log

ARTIFACT_LIMIT = 16_000_000
REPO_ROOT = os.path.dirname(os.path.abspath(__file__))


def main() -> int:
    p = argparse.ArgumentParser(description="Validity checklist helper for Parameter Golf.")
    p.add_argument("--log", required=True, help="Path to training log")
    p.add_argument("--artifact", default=None, help="Path to compressed .ptz artifact")
    p.add_argument(
        "--strict",
        action="store_true",
        help="Fail if log status is not ok/timeout or val_bpb missing",
    )
    p.add_argument(
        "--limit",
        type=int,
        default=ARTIFACT_LIMIT,
        help=f"Max artifact bytes (default {ARTIFACT_LIMIT})",
    )
    args = p.parse_args()

    checks: list[tuple[str, bool, str]] = []

    if not os.path.isfile(args.log):
        print(f"FAIL: log not found: {args.log}")
        return 1

    with open(args.log, encoding="utf-8", errors="replace") as f:
        rec = parse_training_log(f.read())

    vb = rec.get("val_bpb")
    st = rec.get("status", "parse_error")
    ab = rec.get("artifact_bytes")

    checks.append(("log parses", st not in ("parse_error", "crash"), f"status={st}"))
    checks.append(("val_bpb present", vb is not None, str(vb)))
    checks.append(("artifact size in log", ab is not None, str(ab)))
    if ab is not None:
        checks.append((f"artifact <= {args.limit} (from log)", ab <= args.limit, f"{ab}"))

    if args.artifact:
        if not os.path.isfile(args.artifact):
            checks.append(("artifact file exists", False, args.artifact))
        else:
            sz = os.path.getsize(args.artifact)
            checks.append(("artifact file on disk", True, f"{sz} bytes"))
            checks.append((f"on-disk <= {args.limit}", sz <= args.limit, f"{sz}"))

    if args.strict and st not in ("ok", "timeout"):
        checks.append(("strict: log status ok/timeout", False, st))

    dirty = False
    try:
        out = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=10,
        )
        if out.returncode == 0:
            dirty = bool(out.stdout.strip())
    except (OSError, subprocess.TimeoutExpired):
        pass
    ok_all = True
    for name, ok, detail in checks:
        mark = "OK " if ok else "FAIL"
        print(f"{mark}  {name}: {detail}")
        if not ok:
            ok_all = False

    if dirty:
        print("NOTE  git working tree is dirty (optional to clean before packaging)")

    print(json.dumps(rec, indent=2))
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
