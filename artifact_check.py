#!/usr/bin/env python3
"""
Verify a submission artifact (file) is within the 16,000,000-byte cap.

Usage:
  python artifact_check.py path/to/file.ptz
  python artifact_check.py path/to/file.ptz --limit 16000000
"""

from __future__ import annotations

import argparse
import os
import sys

DEFAULT_LIMIT = 16_000_000


def main() -> None:
    p = argparse.ArgumentParser(description="Check artifact file size vs Parameter Golf cap.")
    p.add_argument("path", help="Path to artifact file")
    p.add_argument(
        "--limit",
        type=int,
        default=DEFAULT_LIMIT,
        help=f"Max bytes (default {DEFAULT_LIMIT})",
    )
    args = p.parse_args()

    path = args.path
    if not os.path.isfile(path):
        print(f"artifact_check: not a file: {path}", file=sys.stderr)
        sys.exit(2)

    n = os.path.getsize(path)
    ok = n <= args.limit
    print(f"bytes: {n}")
    print(f"limit: {args.limit}")
    print(f"ok: {ok}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
