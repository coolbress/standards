#!/usr/bin/env python3
"""Separate inherited gingoa decisions from the evidence corpus.

This migration is intentionally narrow and deterministic:
- only Markdown files under corpus/aspects are considered;
- project-specific H2 sections are extracted verbatim into interpretation/legacy;
- gingoa_applied frontmatter is preserved in the extraction record, then removed;
- inherited `verified` statuses are downgraded to `review-needed`.

Run without --apply for a dry run. A full pre-migration archive is required.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT
ASPECTS = RESEARCH / "corpus" / "aspects"
OUTPUT = RESEARCH / "interpretation" / "legacy" / "gingoa-specific-sections.md"
SNAPSHOT = RESEARCH / "archive" / "2026-08-02" / "pre-curation-snapshot.tar.gz"

TARGET_HEADINGS = {
    "implications for gingoa",
    "gingoa application",
}


def split_h2_sections(text: str, *, downgrade_inherited_status: bool) -> tuple[str, list[str]]:
    lines = text.splitlines(keepends=True)
    kept: list[str] = []
    removed: list[str] = []
    current: list[str] = []
    removing = False

    for line in lines:
        match = re.match(r"^##\s+(.+?)\s*$", line)
        if match:
            if removing and current:
                removed.append("".join(current).rstrip() + "\n")
                current = []
            removing = match.group(1).strip().lower() in TARGET_HEADINGS
        if removing:
            current.append(line)
        else:
            kept.append(line)

    if removing and current:
        removed.append("".join(current).rstrip() + "\n")

    result = "".join(kept)
    result = re.sub(r"(?m)^gingoa_applied:\s*(.*)\n", "", result)
    if downgrade_inherited_status:
        result = re.sub(r"(?m)^status:\s*verified\s*$", "status: review-needed", result)
    return result, removed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    if args.apply and not SNAPSHOT.is_file():
        raise SystemExit(f"required recovery snapshot missing: {SNAPSHOT}")

    # OUTPUT is the durable completion marker for the one-time inherited-status
    # migration. Later verified documents must not be downgraded by a re-run.
    downgrade_inherited_status = not OUTPUT.is_file()
    changed: list[tuple[Path, str, list[str], str | None]] = []
    for path in sorted(ASPECTS.rglob("*.md")):
        original = path.read_text(encoding="utf-8")
        applied_match = re.search(r"(?m)^gingoa_applied:\s*(.*)$", original)
        revised, removed = split_h2_sections(
            original,
            downgrade_inherited_status=downgrade_inherited_status,
        )
        if revised != original:
            changed.append(
                (path, revised, removed, applied_match.group(1).strip() if applied_match else None)
            )

    extracted_count = sum(len(item[2]) for item in changed)
    print(f"files_changed={len(changed)}")
    print(f"sections_extracted={extracted_count}")
    print(f"mode={'apply' if args.apply else 'dry-run'}")

    if not args.apply:
        for path, _, removed, applied in changed:
            flags = []
            if removed:
                flags.append(f"sections={len(removed)}")
            if applied:
                flags.append("gingoa_applied")
            if re.search(r"(?m)^status:\s*verified\s*$", path.read_text(encoding="utf-8")) \
                    and downgrade_inherited_status:
                flags.append("status-review")
            print(f"{path.relative_to(ROOT)}\t{','.join(flags)}")
        return 0

    output_lines = [
        "# Legacy gingoa-specific sections extracted from the evidence corpus\n",
        "\n",
        "> Migration date: 2026-08-02. These are historical application decisions, not general evidence.\n",
        "> The byte-for-byte pre-migration corpus is recoverable from\n",
        "> `.scratch/research/archive/2026-08-02/pre-curation-snapshot.tar.gz`.\n",
        "\n",
    ]
    for path, revised, removed, applied in changed:
        path.write_text(revised, encoding="utf-8")
        if not removed and not applied:
            continue
        rel = path.relative_to(ROOT)
        output_lines.append(f"## `{rel}`\n\n")
        if applied:
            output_lines.append(f"- Former `gingoa_applied`: `{applied}`\n\n")
        for section in removed:
            output_lines.append(section)
            output_lines.append("\n")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("".join(output_lines), encoding="utf-8")
    print(f"extraction_output={OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
