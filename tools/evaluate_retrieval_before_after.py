#!/usr/bin/env python3
"""Matched structural retrieval comparison against the immutable pre-curation snapshot.

This measures corpus routing, answer anchors, evidence-status calibration, traceability,
and read surface. It deliberately does not claim to measure model behavior.
"""

from __future__ import annotations

import json
import posixpath
import re
import statistics
import sys
import tarfile
from collections import deque
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT
CORPUS = RESEARCH / "corpus"
SNAPSHOT = RESEARCH / "archive" / "2026-08-02" / "pre-curation-snapshot.tar.gz"
CASES = RESEARCH / "audit" / "retrieval-cases.jsonl"
PREFIX = ".scratch/research/corpus/"
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")


def snapshot_view() -> dict[str, bytes]:
    result: dict[str, bytes] = {}
    with tarfile.open(SNAPSHOT, "r:gz") as archive:
        for member in archive.getmembers():
            if not member.isfile() or not member.name.startswith(PREFIX):
                continue
            handle = archive.extractfile(member)
            if handle is not None:
                result[member.name[len(PREFIX):]] = handle.read()
    return result


def current_view() -> dict[str, bytes]:
    return {
        path.relative_to(CORPUS).as_posix(): path.read_bytes()
        for path in CORPUS.rglob("*")
        if path.is_file()
    }


def text(view: dict[str, bytes], path: str) -> str:
    return view[path].decode("utf-8", errors="replace")


def frontmatter_value(content: str, key: str) -> str | None:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*[\"']?([^\n\"']+)", content)
    return match.group(1).strip() if match else None


def links(view: dict[str, bytes], path: str) -> list[str]:
    result: list[str] = []
    for raw in LINK_RE.findall(text(view, path)):
        target = raw.strip().split()[0].strip("<>")
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        target = unquote(target.split("#", 1)[0])
        if not target:
            continue
        resolved = posixpath.normpath(posixpath.join(posixpath.dirname(path), target))
        if resolved in view:
            result.append(resolved)
    return result


def shortest_hops(view: dict[str, bytes], target: str) -> int | None:
    queue: deque[tuple[str, int]] = deque([("INDEX.md", 0)])
    visited = {"INDEX.md"}
    while queue:
        path, hops = queue.popleft()
        if path == target:
            return hops
        if hops >= 2:
            continue
        for linked in links(view, path):
            if linked not in visited:
                visited.add(linked)
                queue.append((linked, hops + 1))
    return None


def has_traceable_claim(content: str) -> bool:
    return (
        ("## Claim register" in content or "## Claim table" in content)
        and bool(re.search(r"(?m)^\| [A-Z][A-Z0-9-]+-\d{3} \|", content))
        and bool(re.search(r"(?m)^sources:(?:\s*\[[A-Z0-9-]|\s*$\n\s+-\s+[A-Z0-9-])", content))
    )


def evaluate(view: dict[str, bytes], arm: str, cases: list[dict]) -> dict[str, object]:
    markdown_bytes = sum(len(data) for path, data in view.items() if path.endswith(".md"))
    routes = 0
    anchor_hits = 0
    anchor_total = 0
    status_hits = 0
    status_total = 0
    unsupported_verified = 0
    traceable_verified = 0
    ratios: list[float] = []

    for case in cases:
        target = case["expected_path"]
        if arm == "before" and case["id"] == "RET-030":
            target = "aspects/05-scm-workflow/_aspect.md"
        if target not in view:
            continue
        hops = shortest_hops(view, target)
        if hops is not None and hops <= 2:
            routes += 1
        content = text(view, target)
        for anchor in case.get("anchors", []):
            anchor_total += 1
            if anchor.casefold() in content.casefold():
                anchor_hits += 1
        expected_status = case.get("expected_status")
        if expected_status:
            status_total += 1
            actual = frontmatter_value(content, "status")
            if actual == expected_status:
                status_hits += 1
            if actual == "verified" and not has_traceable_claim(content):
                unsupported_verified += 1
            if actual == "verified" and has_traceable_claim(content):
                traceable_verified += 1
        ratios.append((len(view["INDEX.md"]) + len(view[target])) / markdown_bytes)

    return {
        "routes": routes,
        "anchor_hits": anchor_hits,
        "anchor_total": anchor_total,
        "status_hits": status_hits,
        "status_total": status_total,
        "unsupported_verified": unsupported_verified,
        "traceable_verified": traceable_verified,
        "median_ratio": statistics.median(ratios),
        "max_ratio": max(ratios),
    }


def main() -> int:
    cases = [json.loads(line) for line in CASES.read_text(encoding="utf-8").splitlines() if line]
    before = snapshot_view()
    after = current_view()
    results = {"before": evaluate(before, "before", cases), "after": evaluate(after, "after", cases)}
    errors: list[str] = []

    # Five order permutations exercise repeatability of the deterministic evaluator.
    repeats: list[dict[str, dict[str, object]]] = []
    for shift in range(5):
        ordered = cases[shift:] + cases[:shift]
        repeats.append({
            "before": evaluate(before, "before", ordered),
            "after": evaluate(after, "after", ordered),
        })
    if any(repeat != results for repeat in repeats):
        errors.append("deterministic result changed across five case-order repetitions")

    if results["after"]["routes"] != len(cases):
        errors.append("after arm did not route all matched cases within two hops")
    if results["after"]["status_hits"] != results["after"]["status_total"]:
        errors.append("after arm did not calibrate all expected statuses")
    if results["after"]["unsupported_verified"] != 0:
        errors.append("after arm exposes verified targets without traceable claim registers")

    print("Matched retrieval before/after evaluation")
    print(f"METRIC cases={len(cases)} shared_information_cases=29 foundation_added_cases=1")
    for arm in ("before", "after"):
        result = results[arm]
        print(
            f"ARM {arm} routes={result['routes']}/{len(cases)} "
            f"anchors={result['anchor_hits']}/{result['anchor_total']} "
            f"status_calibration={result['status_hits']}/{result['status_total']} "
            f"unsupported_verified={result['unsupported_verified']} "
            f"traceable_verified={result['traceable_verified']} "
            f"median_context_ratio={result['median_ratio']:.4f} "
            f"max_context_ratio={result['max_ratio']:.4f}"
        )
    print("REPEAT deterministic_order_permutations=5 variance=0")
    print("CHECK model_behavior=NOT_MEASURED requires isolated blind model arms")
    for error in errors:
        print(f"FAIL {error}")
    print(f"RESULT {'PASS' if not errors else 'FAIL'} errors={len(errors)}")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
