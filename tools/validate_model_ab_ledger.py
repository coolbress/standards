#!/usr/bin/env python3
"""Verify the six raw fresh-context retrieval outputs against their audit manifest."""

from __future__ import annotations

import csv
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "audit" / "model-ab-raw"
MANIFEST = RAW / "MANIFEST.tsv"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    errors: list[str] = []
    with MANIFEST.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    if len(rows) != 6:
        errors.append(f"expected 6 raw result rows, found {len(rows)}")
    identities: set[tuple[str, str]] = set()
    for row in rows:
        identity = (row["arm"], row["repetition"])
        if identity in identities:
            errors.append(f"duplicate arm/repetition {identity}")
        identities.add(identity)
        path = RAW / row["raw_file"]
        if not path.is_file():
            errors.append(f"missing raw result {row['raw_file']}")
            continue
        content = path.read_text(encoding="utf-8")
        if path.stat().st_size != int(row["raw_bytes"]):
            errors.append(f"raw byte mismatch {row['raw_file']}")
        if sha256(path) != row["sha256"]:
            errors.append(f"raw hash mismatch {row['raw_file']}")
        questions = re.findall(r"(?m)^Q(10|[1-9]) \|", content)
        if questions != [str(number) for number in range(1, 11)]:
            errors.append(f"question set mismatch {row['raw_file']}: {questions}")
        if f"ARM={row['arm']} | REP={row['repetition']}" not in content:
            errors.append(f"arm/repetition marker mismatch {row['raw_file']}")
        proxy = re.search(
            r"Context-cost proxy:\s*(\d+)(?: unique)? files,\s*([\d,]+) bytes",
            content,
        )
        if not proxy:
            errors.append(f"missing context-cost calculation {row['raw_file']}")
        elif (
            int(proxy.group(1)) != int(row["context_files"])
            or int(proxy.group(2).replace(",", "")) != int(row["context_bytes"])
        ):
            errors.append(f"context-cost mismatch {row['raw_file']}")
        if "UNAVAILABLE" not in content or "model" not in content.casefold():
            errors.append(f"missing model identity limitation {row['raw_file']}")
    print("Retrieval model A/B raw-ledger validation")
    print(f"METRIC rows={len(rows)} identities={len(identities)}")
    for error in errors:
        print(f"FAIL {error}")
    print(f"RESULT {'PASS' if not errors else 'FAIL'} errors={len(errors)}")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())

