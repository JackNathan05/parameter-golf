#!/usr/bin/env python3
"""
Parse `train_gpt.py` / `train_gpt_mlx.py` training logs and extract val_bpb, timing, artifact size.

Usage:
  python parse_logs.py path/to/train.log
  python parse_logs.py path/to/train.log --json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Any

ARTIFACT_LINE = re.compile(
    r"Total submission size (?:int6\+zstd|int8\+zlib):\s*(\d+)\s*bytes",
    re.IGNORECASE,
)
ARTIFACT_FALLBACK = re.compile(r"Total submission size:\s*(\d+)\s*bytes", re.IGNORECASE)
FOOTER_VAL_BPB = re.compile(r"^val_bpb:\s*([\d.+-eE]+)\s*$", re.MULTILINE)
FOOTER_ARTIFACT = re.compile(r"^artifact_bytes:\s*(\d+)\s*$", re.MULTILINE)
FINAL_EXACT_BPB = re.compile(
    r"final_\w+_exact\s+val_loss:[\d.]+\s+val_bpb:([\d.+-eE]+)"
)
STEP_LINE_BPB = re.compile(
    r"step:\s*(\d+)/\d+\s+.*val_bpb:([\d.]+)",
)
TRAIN_TIME_MS = re.compile(r"train_time:\s*(\d+)\s*ms")


def parse_training_log(text: str) -> dict[str, Any]:
    text = text.replace("\r\n", "\n")
    status: str = "ok"
    if "Traceback (most recent call last)" in text or re.search(
        r"\bCUDA out of memory\b", text
    ):
        status = "crash"
    elif re.search(r"^Error:\s", text, re.MULTILINE) and "train_time:" not in text.split(
        "Error:"
    )[-1][:200]:
        status = "crash"

    val_bpb: float | None = None
    m_footer_v = FOOTER_VAL_BPB.search(text)
    if m_footer_v:
        val_bpb = float(m_footer_v.group(1))

    if val_bpb is None:
        matches = list(FINAL_EXACT_BPB.finditer(text))
        if matches:
            val_bpb = float(matches[-1].group(1))

    if val_bpb is None:
        matches = list(STEP_LINE_BPB.finditer(text))
        if matches:
            val_bpb = float(matches[-1].group(2))

    artifact_bytes: int | None = None
    m_footer_a = FOOTER_ARTIFACT.search(text)
    if m_footer_a:
        artifact_bytes = int(m_footer_a.group(1))
    if artifact_bytes is None:
        am = list(ARTIFACT_LINE.finditer(text))
        if am:
            artifact_bytes = int(am[-1].group(1))
    if artifact_bytes is None:
        am = list(ARTIFACT_FALLBACK.finditer(text))
        if am:
            artifact_bytes = int(am[-1].group(1))

    train_seconds: float | None = None
    ms_matches = [int(m.group(1)) for m in TRAIN_TIME_MS.finditer(text)]
    if ms_matches:
        train_seconds = max(ms_matches) / 1000.0

    artifact_path: str | None = None
    if "final_model.int8.ptz" in text:
        artifact_path = "final_model.int8.ptz"
    elif "final_model.int6" in text or "int6+zstd" in text.lower():
        artifact_path = "final_model.int6.ptz"  # name may vary; log still has size

    if val_bpb is None:
        status = "parse_error"
    elif artifact_bytes is None:
        status = "parse_error"

    if status == "ok" and artifact_bytes is not None and artifact_bytes > 16_000_000:
        status = "oversize"

    if status == "ok" and "stopping_early: wallclock_cap" in text:
        pass  # still ok

    return {
        "val_bpb": val_bpb,
        "train_seconds": train_seconds,
        "artifact_path": artifact_path,
        "artifact_bytes": artifact_bytes,
        "status": status,
    }


def main() -> None:
    p = argparse.ArgumentParser(description="Parse Parameter Golf training logs.")
    p.add_argument("log_path", help="Path to train.log (or similar)")
    p.add_argument("--json", action="store_true", help="Print JSON only")
    args = p.parse_args()

    try:
        with open(args.log_path, encoding="utf-8", errors="replace") as f:
            text = f.read()
    except OSError as e:
        print(json.dumps({"status": "parse_error", "error": str(e)}))
        sys.exit(2)

    record = parse_training_log(text)
    if args.json:
        print(json.dumps(record, indent=2))
    else:
        for k, v in record.items():
            print(f"{k}: {v}")


if __name__ == "__main__":
    main()
