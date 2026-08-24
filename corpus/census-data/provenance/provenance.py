#!/usr/bin/env python3
"""Create and verify a content-addressed snapshot of census evidence.

This is deliberately offline. It does not claim to recover collection metadata
that the legacy artifacts never recorded; unknown values remain JSON null.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "snapshot-manifest.json"
INCLUDE_NAMES = {
    "records.json",
    "stats.json",
    "conventions-records.json",
    "conventions-stats.json",
    "conventions-6k-records.json",
    "conventions-6k-stats.json",
    "conventions-roster-records.json",
    "conventions-roster.json",
    "records-2k.json",
    "stats-2k.json",
    "taskform-records.json",
    "taskform-stats.json",
    "robustness.json",
    "robustness-report.md",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def role(path: Path) -> str:
    name = path.name
    if name.endswith(("records.json", "records-2k.json")):
        return "normalized-records"
    if name.endswith(("stats.json", "stats-2k.json")):
        return "derived-statistics"
    if path.suffix == ".py" or path.suffix == ".sh":
        return "collector-or-analysis-code"
    if path.suffix == ".json":
        return "derived-statistics"
    if name == "robustness-report.md":
        return "derived-report"
    return "supporting-evidence"


def candidates() -> list[Path]:
    selected: set[Path] = set()
    for path in ROOT.rglob("*"):
        if not path.is_file() or "__pycache__" in path.parts or path == MANIFEST:
            continue
        if path.name in INCLUDE_NAMES or path.suffix in {".py", ".sh"}:
            selected.add(path)
    return sorted(selected)


def snapshot() -> None:
    artifacts = []
    for path in candidates():
        artifact_role = role(path)
        artifacts.append(
            {
                "path": path.relative_to(ROOT).as_posix(),
                "role": artifact_role,
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
                "collected_at": None,
                "collection_time_status": (
                    "unknown-legacy-not-recorded"
                    if artifact_role == "normalized-records"
                    else "not-applicable-derived-or-code"
                ),
            }
        )
    payload = {
        "schema_version": 1,
        "snapshot_created_at": datetime.now(timezone.utc).isoformat(),
        "hash_algorithm": "sha256",
        "root": "docs/research/census-data",
        "scope": "normalized records, derived statistics, and executable census/analysis code",
        "limitations": [
            "Legacy collection timestamps and API versions were not recorded and are not inferred.",
            "Records are normalized per-repository evidence, not full GitHub API response archives.",
            "The research tree is intentionally gitignored; integrity is checked by this snapshot, not enforced by Git history.",
        ],
        "artifacts": artifacts,
    }
    MANIFEST.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {MANIFEST} ({len(artifacts)} artifacts)")


def validate() -> int:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    errors: list[str] = []
    paths: set[str] = set()
    for item in data.get("artifacts", []):
        rel = item.get("path")
        if not isinstance(rel, str) or rel in paths:
            errors.append(f"invalid or duplicate path: {rel!r}")
            continue
        paths.add(rel)
        path = ROOT / rel
        if not path.is_file():
            errors.append(f"missing: {rel}")
            continue
        if path.stat().st_size != item.get("bytes"):
            errors.append(f"size mismatch: {rel}")
        if sha256(path) != item.get("sha256"):
            errors.append(f"sha256 mismatch: {rel}")
        allowed_time_status = {"unknown-legacy-not-recorded", "not-applicable-derived-or-code"}
        if item.get("collected_at") is None and item.get("collection_time_status") not in allowed_time_status:
            errors.append(f"unexplained null collection time: {rel}")
    expected = {p.relative_to(ROOT).as_posix() for p in candidates()}
    for rel in sorted(expected - paths):
        errors.append(f"unmanifested in-scope artifact: {rel}")
    if errors:
        print("provenance validation failed:")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print(f"provenance validation passed: {len(paths)} artifacts")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("snapshot", "validate"))
    args = parser.parse_args()
    if args.command == "snapshot":
        snapshot()
        return 0
    return validate()


if __name__ == "__main__":
    raise SystemExit(main())
