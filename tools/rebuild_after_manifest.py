#!/usr/bin/env python3
"""Rebuild the generated active-corpus manifest after an approved curation change."""

from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "corpus"
MANIFEST = ROOT / "audit" / "after-manifest.tsv"


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def main() -> None:
    rows = ["path\tbytes\tmtime_epoch\tsha256\tstate"]
    for path in sorted(item for item in CORPUS.rglob("*") if item.is_file()):
        stat = path.stat()
        rows.append(
            f"{path.relative_to(ROOT)}\t{stat.st_size}\t{int(stat.st_mtime)}\t{digest(path)}\tactive"
        )
    temporary = MANIFEST.with_suffix(".tsv.tmp")
    temporary.write_text("\n".join(rows) + "\n", encoding="utf-8")
    temporary.replace(MANIFEST)
    print(f"WROTE {MANIFEST.relative_to(ROOT)} records={len(rows) - 1}")


if __name__ == "__main__":
    main()

