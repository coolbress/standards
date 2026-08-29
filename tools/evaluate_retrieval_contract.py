#!/usr/bin/env python3
"""Deterministic routing baseline for the corpus progressive-disclosure contract.

This does not measure model intelligence. It verifies that a pre-registered question
set has an INDEX-reachable target, expected evidence/status/freshness anchors, and a
bounded two-document read surface. A blind fresh-context agent check is the separate
behavioral rung.
"""

from __future__ import annotations

import json
import re
import sys
from collections import deque
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT
CORPUS = RESEARCH / "corpus"
INDEX = CORPUS / "INDEX.md"
CASES = RESEARCH / "audit" / "retrieval-cases.jsonl"
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")


def frontmatter_value(text: str, key: str) -> str | None:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*[\"']?([^\n\"']+)", text)
    return match.group(1).strip() if match else None


def local_links(path: Path) -> list[Path]:
    result: list[Path] = []
    for raw in LINK_RE.findall(path.read_text(encoding="utf-8")):
        target = raw.strip().split()[0].strip("<>")
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        target = unquote(target.split("#", 1)[0])
        if not target:
            continue
        resolved = (path.parent / target).resolve()
        if resolved.is_file() and (resolved == CORPUS or CORPUS in resolved.parents):
            result.append(resolved)
    return result


def shortest_hops(target: Path) -> int | None:
    queue: deque[tuple[Path, int]] = deque([(INDEX.resolve(), 0)])
    visited = {INDEX.resolve()}
    while queue:
        path, hops = queue.popleft()
        if path == target.resolve():
            return hops
        if hops >= 2:
            continue
        for linked in local_links(path):
            if linked not in visited:
                visited.add(linked)
                queue.append((linked, hops + 1))
    return None


def main() -> int:
    errors: list[str] = []
    cases = [json.loads(line) for line in CASES.read_text(encoding="utf-8").splitlines() if line.strip()]
    dimensions: set[str] = set()
    total_markdown_bytes = sum(path.stat().st_size for path in CORPUS.rglob("*.md"))
    max_ratio = 0.0
    max_hops = 0

    if len(cases) < 30:
        errors.append(f"expected at least 30 retrieval cases, found {len(cases)}")

    for case in cases:
        dimensions.update(item.strip() for item in case["dimension"].split(","))
        target = CORPUS / case["expected_path"]
        if not target.is_file():
            errors.append(f"{case['id']} missing target: {case['expected_path']}")
            continue
        hops = shortest_hops(target)
        if hops is None:
            errors.append(f"{case['id']} target not reachable from INDEX within 2 hops")
        else:
            max_hops = max(max_hops, hops)
        text = target.read_text(encoding="utf-8")
        for anchor in case.get("anchors", []):
            if anchor.casefold() not in text.casefold():
                errors.append(f"{case['id']} missing anchor {anchor!r} in {case['expected_path']}")
        expected_status = case.get("expected_status")
        if expected_status and frontmatter_value(text, "status") != expected_status:
            errors.append(f"{case['id']} status mismatch in {case['expected_path']}")
        expected_freshness = case.get("expected_freshness")
        if expected_freshness and frontmatter_value(text, "freshness") != expected_freshness:
            errors.append(f"{case['id']} freshness mismatch in {case['expected_path']}")
        ratio = (INDEX.stat().st_size + target.stat().st_size) / total_markdown_bytes
        max_ratio = max(max_ratio, ratio)
        if ratio > 0.20:
            errors.append(f"{case['id']} read surface exceeds 20% of corpus Markdown: {ratio:.3f}")

    required_dimensions = {"topic", "lifecycle", "evidence", "status", "freshness"}
    missing_dimensions = sorted(required_dimensions - dimensions)
    if missing_dimensions:
        errors.append(f"missing retrieval dimensions: {missing_dimensions}")

    print("Retrieval contract evaluation")
    print(f"METRIC cases={len(cases)}")
    print(f"METRIC dimensions={','.join(sorted(dimensions))}")
    print(f"METRIC max_index_hops={max_hops}")
    print(f"METRIC max_two_document_context_ratio={max_ratio:.4f}")
    print("CHECK model_behavior=SEPARATE blind-fresh-context-review")
    for error in errors:
        print(f"FAIL {error}")
    print(f"RESULT {'PASS' if not errors else 'FAIL'} errors={len(errors)}")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
