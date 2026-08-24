#!/usr/bin/env python3
"""Offline structural validator for the active goppi_final research corpus."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT
CORPUS = RESEARCH / "corpus"
ASPECTS = CORPUS / "aspects"
SOURCE_REGISTRY = CORPUS / "_meta" / "sources.jsonl"
AFTER_MANIFEST = RESEARCH / "audit" / "after-manifest.tsv"
CLAIM_REVALIDATION = RESEARCH / "audit" / "CLAIM-REVALIDATION.ko.md"
EXTERNAL_URL_LEDGER = RESEARCH / "audit" / "external-url-status.jsonl"
EXTERNAL_URL_META = RESEARCH / "audit" / "external-url-status-meta.json"

ALLOWED_STATUS = {
    "imported",
    "draft",
    "review-needed",
    "verified",
    "superseded",
    "retracted",
}
ASPECT_REQUIRED = {
    "id",
    "title",
    "group",
    "kind",
    "lifecycle_stages",
    "evidence_track",
    "status",
    "last_updated",
    "sources",
    "claim",
}
SUBDOC_REQUIRED = {
    "id",
    "title",
    "parent",
    "kind",
    "evidence_track",
    "status",
    "last_updated",
}
CURATED_REQUIRED = {
    "id",
    "title",
    "kind",
    "status",
    "last_updated",
    "evidence_track",
    "freshness",
    "sources",
}
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
EXTERNAL_URL_RE = re.compile(r"https?://[^\s<>\]}]+")
CLAIM_ID_RE = re.compile(r"^[A-Z][A-Z0-9-]+-\d{3}$")
EVIDENCE_ID_RE = re.compile(r"`([A-Z][A-Z0-9-]+)`")
COMPACT_CLAIM_REF_RE = re.compile(r"\b([A-Z][A-Z0-9-]+)-(\d{3})(?:/(\d{3}))?\b")
ALLOWED_CLAIM_CLASSES = {
    "definition",
    "normative",
    "empirical",
    "vendor-behavior",
    "synthesis",
    "local-census",
}
EXTERNAL_URL_STATUSES = {
    "reachable",
    "redirected",
    "access-blocked",
    "dead",
    "http-error",
    "network-error",
}
ACCESS_BLOCKED_CODES = {401, 403, 405, 406, 407, 409, 418, 423, 425, 429, 451}


def extract_external_urls(root: Path) -> set[str]:
    urls: set[str] = set()
    for path in root.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        urls.update(normalize_external_url(match) for match in EXTERNAL_URL_RE.findall(text))
    registry = root / "_meta" / "sources.jsonl"
    if registry.is_file():
        for line in registry.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                url = str(json.loads(line).get("url", ""))
            except json.JSONDecodeError:
                continue  # The registry schema pass reports malformed JSON separately.
            if url.startswith(("http://", "https://")):
                urls.add(url)
    return urls


def normalize_external_url(candidate: str) -> str:
    """Trim prose/Markdown delimiters while preserving balanced URL parentheses."""
    candidate = candidate.rstrip(".,;:'\"`")
    while candidate.endswith(")") and candidate.count(")") > candidate.count("("):
        candidate = candidate[:-1]
    return candidate


def external_url_set_digest(urls: set[str]) -> str:
    return hashlib.sha256(("\n".join(sorted(urls)) + "\n").encode("utf-8")).hexdigest()


def iso_12207_edition_warning(text: str) -> str | None:
    generic = re.compile(r"ISO[- /]?(?:IEC[- /]?(?:IEEE[- /]?)?)?12207", re.I)
    current = re.compile(r"ISO[- /]?(?:IEC[- /]?(?:IEEE[- /]?)?)?12207(?:[: -])2026", re.I)
    historical = re.compile(r"ISO[- /]?(?:IEC[- /]?(?:IEEE[- /]?)?)?12207(?:[: -])2017", re.I)
    if not generic.search(text):
        return None
    if not current.search(text):
        return "ISO 12207 reference lacks an explicit current-edition disposition"
    disposition = r"(?:withdrawn|폐기|역사적|historical)"
    for match in historical.finditer(text):
        edition = re.escape(match.group(0))
        before = text[max(0, match.start() - 100):match.end()]
        after = text[match.start():min(len(text), match.end() + 180)]
        tied_before = re.search(disposition + r"(?:(?![.!?]\s).){0,80}" + edition, before, re.I | re.S)
        tied_after = re.search(edition + r"(?:(?![.!?]\s).){0,160}" + disposition, after, re.I | re.S)
        if not (tied_before or tied_after):
            return "ISO 12207:2017 reference is not locally marked withdrawn or historical"
    return None


def external_url_record_errors(record: dict[str, object], expected_url: str) -> list[str]:
    errors: list[str] = []
    required = {
        "url",
        "checked_at",
        "status",
        "http_status",
        "final_url",
        "attempts",
        "method",
        "content_verified",
        "detail",
    }
    missing = sorted(required - set(record))
    if missing:
        errors.append(f"missing fields {missing}")
        return errors
    if record.get("url") != expected_url:
        errors.append("URL key does not match record URL")
    status = str(record.get("status", ""))
    if status not in EXTERNAL_URL_STATUSES:
        errors.append(f"invalid status {status!r}")
    if record.get("content_verified") is not False:
        errors.append("reachability ledger must not claim content verification")
    if not str(record.get("detail", "")).strip():
        errors.append("detail is blank")
    try:
        checked = datetime.fromisoformat(str(record.get("checked_at", "")).replace("Z", "+00:00"))
        if checked.tzinfo is None:
            errors.append("checked_at must include a timezone")
        else:
            age_seconds = (datetime.now(timezone.utc) - checked).total_seconds()
            if age_seconds > 30 * 86400:
                errors.append("record is older than 30 days")
            if age_seconds < -300:
                errors.append("checked_at is more than five minutes in the future")
    except ValueError:
        errors.append("invalid checked_at")
    attempts = record.get("attempts")
    if not isinstance(attempts, int) or attempts < 1:
        errors.append("attempts must be a positive integer")
    if not str(record.get("method", "")).strip():
        errors.append("method is blank")
    code = record.get("http_status")
    final_url = record.get("final_url")
    if status in {"reachable", "redirected"}:
        if not isinstance(code, int) or not 200 <= code < 400:
            errors.append("healthy status lacks a 2xx/3xx HTTP code")
        if not str(final_url or "").startswith(("http://", "https://")):
            errors.append("healthy status lacks a final HTTP(S) URL")
    if status == "access-blocked":
        if code not in ACCESS_BLOCKED_CODES:
            errors.append("access-blocked status lacks an allowed HTTP code")
        if not str(final_url or "").startswith(("http://", "https://")):
            errors.append("access-blocked status lacks a final HTTP(S) URL")
    if status == "dead" and code not in {404, 410}:
        errors.append("dead status lacks HTTP 404/410")
    return errors


def validate_external_url_ledger(
    expected_urls: set[str],
) -> tuple[str, dict[str, int], list[str], list[str]]:
    """Validate exact coverage/freshness; endpoint results are not content verification."""
    counts: dict[str, int] = defaultdict(int)
    warnings: list[str] = []
    errors: list[str] = []
    if not EXTERNAL_URL_LEDGER.is_file() or not EXTERNAL_URL_META.is_file():
        warnings.append("external URL reachability ledger is missing")
        return "SKIPPED", dict(counts), warnings, errors
    try:
        meta = json.loads(EXTERNAL_URL_META.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"invalid external URL meta JSON: {exc}")
        return "INVALID", dict(counts), warnings, errors
    records: dict[str, dict[str, object]] = {}
    for number, line in enumerate(EXTERNAL_URL_LEDGER.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"invalid external URL ledger line {number}: {exc}")
            continue
        url = str(record.get("url", ""))
        if not url:
            errors.append(f"external URL ledger line {number} has no URL")
            continue
        if url in records:
            errors.append(f"duplicate external URL ledger record: {url}")
        records[url] = record
        status = str(record.get("status", ""))
        if status in EXTERNAL_URL_STATUSES:
            counts[status] += 1
        errors.extend(f"external URL ledger {url}: {message}" for message in external_url_record_errors(record, url))
    if set(records) != expected_urls:
        missing = sorted(expected_urls - set(records))
        extra = sorted(set(records) - expected_urls)
        errors.append(f"external URL ledger set mismatch: missing={missing[:5]}, extra={extra[:5]}")
    expected_digest = external_url_set_digest(expected_urls)
    if meta.get("url_set_sha256") != expected_digest:
        errors.append("external URL meta digest does not match current corpus URL set")
    if meta.get("url_count") != len(expected_urls):
        errors.append("external URL meta count does not match current corpus URL set")
    if meta.get("schema_version") != 1 or meta.get("checker_version") != 1:
        errors.append("external URL meta has unsupported schema/checker version")
    if meta.get("counts") != dict(sorted(counts.items())):
        errors.append("external URL meta counts do not match ledger records")
    completed_at = str(meta.get("completed_at", ""))
    try:
        completed = datetime.fromisoformat(completed_at.replace("Z", "+00:00"))
        if completed.tzinfo is None:
            raise ValueError("timezone required")
        age_days = (datetime.now(timezone.utc) - completed).total_seconds() / 86400
        if age_days > 30:
            warnings.append(f"external URL reachability ledger is stale ({age_days:.1f} days)")
        if age_days < -(5 / 1440):
            errors.append("external URL meta completed_at is more than five minutes in the future")
    except ValueError:
        errors.append("external URL meta has invalid completed_at")
    unresolved = counts.get("dead", 0) + counts.get("http-error", 0) + counts.get("network-error", 0)
    if unresolved:
        warnings.append(
            "external URL dispositions unresolved: "
            f"dead={counts.get('dead', 0)} http-error={counts.get('http-error', 0)} "
            f"network-error={counts.get('network-error', 0)}"
        )
    return "EXECUTED", dict(counts), warnings, errors


def parse_frontmatter(path: Path) -> dict[str, str] | None:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        return None
    result: dict[str, str] = {}
    for line in lines[1:]:
        if line == "---":
            return result
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$", line)
        if match:
            result[match.group(1)] = match.group(2).strip().strip('"')
    return None


def parse_frontmatter_source_ids(path: Path) -> list[str]:
    """Read the simple block-list form used by curated `sources:` metadata."""
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        return []
    in_sources = False
    result: list[str] = []
    for line in lines[1:]:
        if line == "---":
            break
        sources_match = re.match(r"^sources:\s*(.*)$", line)
        if sources_match:
            in_sources = True
            inline = sources_match.group(1).strip()
            if inline.startswith("[") and inline.endswith("]"):
                result.extend(
                    item.strip().strip('"\'')
                    for item in inline[1:-1].split(",")
                    if item.strip()
                )
                break
            continue
        if in_sources and re.match(r"^[A-Za-z_][A-Za-z0-9_-]*:\s*", line):
            break
        if in_sources:
            match = re.match(r"^\s+-\s+(.+?)\s*$", line)
            if match:
                result.append(match.group(1).strip('"\''))
    return result


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalized_h2_sections(path: Path) -> list[tuple[str, str]]:
    """Return substantial normalized H2 bodies for exact structural-repeat checks."""
    text = path.read_text(encoding="utf-8")
    matches = list(re.finditer(r"(?m)^##\s+(.+?)\s*$", text))
    result: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[match.end():end]
        normalized = re.sub(r"\s+", " ", body).strip().lower()
        if len(normalized) >= 300:
            result.append((match.group(1).strip(), normalized))
    return result


def claim_table_errors(text: str, registry_ids: set[str]) -> tuple[int, list[str]]:
    """Validate six-field claim rows and source placement in the Evidence column."""
    count = 0
    errors: list[str] = []
    seen: set[str] = set()
    rows: list[list[str]] = []
    for line in text.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if not cells or not CLAIM_ID_RE.fullmatch(cells[0]):
            continue
        count += 1
        claim_id = cells[0]
        if claim_id in seen:
            errors.append(f"duplicate claim ID {claim_id}")
        seen.add(claim_id)
        if len(cells) != 6:
            errors.append(f"claim row {claim_id} has {len(cells)} fields; expected 6")
            continue
        rows.append(cells)
        _claim_id, claim_class, claim, evidence, confidence, expiry = cells
        if claim_class not in ALLOWED_CLAIM_CLASSES:
            errors.append(f"claim row {claim_id} has invalid class {claim_class!r}")
        for label, value in {
            "claim": claim,
            "evidence": evidence,
            "confidence": confidence,
            "expiry": expiry,
        }.items():
            if not value:
                errors.append(f"claim row {claim_id} has blank {label}")
    for cells in rows:
        claim_id, _claim_class, _claim, evidence, _confidence, _expiry = cells
        quoted_ids = EVIDENCE_ID_RE.findall(evidence)
        local_claim_refs: set[str] = set()
        unquoted_evidence = EVIDENCE_ID_RE.sub("", evidence)
        for match in COMPACT_CLAIM_REF_RE.finditer(unquoted_evidence):
            prefix, first, second = match.groups()
            local_claim_refs.add(f"{prefix}-{first}")
            if second:
                local_claim_refs.add(f"{prefix}-{second}")
        for reference in sorted(local_claim_refs):
            if reference not in seen:
                errors.append(f"claim row {claim_id} has unknown local claim reference {reference}")
        for reference in quoted_ids:
            if reference not in registry_ids and reference not in seen:
                errors.append(f"claim row {claim_id} has unregistered evidence ID {reference}")
        if not any(reference in registry_ids for reference in quoted_ids):
            errors.append(f"claim row {claim_id} Evidence field has no registered source ID")
    return count, errors


def aspect_overview_path(aspect_dir: Path) -> Path:
    """Aspect overview file for a topic directory.

    Renamed 2026-08-08: `_aspect.md` -> `<topic>--overview.md`.
    The old name was identical across all 28 directories, so any filename-level
    search returned 28 indistinguishable hits. The rename map and the
    irreversibility safeguard are recorded in `audit/rename-map-2026-08-08.json`.
    Naming rule: `_schema.md` section 2.1 (`<topic>--<artifact>.md`).
    """
    return aspect_dir / f"{aspect_dir.name}--overview.md"


def is_aspect_overview(path: Path) -> bool:
    """True for the per-topic overview file (formerly `_aspect.md`)."""
    return path.name == f"{path.parent.name}--overview.md"


def missing_aspect_files(aspect_dirs: list[Path]) -> list[Path]:
    return [aspect_overview_path(path) for path in aspect_dirs if not aspect_overview_path(path).is_file()]


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    metrics: dict[str, int] = {}

    files = sorted(path for path in CORPUS.rglob("*") if path.is_file())
    markdown = [path for path in files if path.suffix == ".md"]
    metrics["active_files"] = len(files)
    metrics["markdown_files"] = len(markdown)

    manifest_records: dict[str, tuple[int, str]] = {}
    if not AFTER_MANIFEST.is_file():
        errors.append("missing after-manifest.tsv")
    else:
        lines = [line for line in AFTER_MANIFEST.read_text(encoding="utf-8").splitlines() if line]
        if not lines or lines[0] != "path\tbytes\tmtime_epoch\tsha256\tstate":
            errors.append("invalid after-manifest.tsv header")
        for line in lines[1:]:
            fields = line.split("\t")
            if len(fields) != 5:
                errors.append(f"invalid after-manifest row: {line}")
                continue
            path_text, bytes_text, _mtime, digest, state = fields
            if state != "active":
                errors.append(f"invalid after-manifest state for {path_text}: {state}")
            manifest_records[path_text] = (int(bytes_text), digest)
        current_paths = {str(path.relative_to(ROOT)) for path in files}
        if set(manifest_records) != current_paths:
            errors.append("after-manifest path set does not match active corpus")
        for path in files:
            rel = str(path.relative_to(ROOT))
            record = manifest_records.get(rel)
            if record and record != (path.stat().st_size, sha256(path)):
                errors.append(f"after-manifest size/hash mismatch: {rel}")
    metrics["after_manifest_records"] = len(manifest_records)

    dead = [
        path for path in files
        if path.suffix == ".pyc" or "__pycache__" in path.parts or path.stat().st_size == 0
    ]
    if dead:
        errors.extend(f"dead/generated active artifact: {path.relative_to(ROOT)}" for path in dead)

    by_hash: dict[str, list[Path]] = defaultdict(list)
    for path in files:
        if path.stat().st_size:
            by_hash[sha256(path)].append(path)
    duplicate_groups = [group for group in by_hash.values() if len(group) > 1]
    metrics["nonempty_duplicate_groups"] = len(duplicate_groups)
    for group in duplicate_groups:
        errors.append("exact duplicate: " + ", ".join(str(path.relative_to(ROOT)) for path in group))

    aspect_dirs = sorted(path for path in ASPECTS.iterdir() if path.is_dir())
    metrics["aspect_directories"] = len(aspect_dirs)
    if len(aspect_dirs) != 28:
        errors.append(f"expected 28 aspect directories, found {len(aspect_dirs)}")
    expected_numbers = [f"{number:02d}" for number in range(1, 29)]
    actual_numbers = sorted(path.name[:2] for path in aspect_dirs)
    if actual_numbers != expected_numbers:
        errors.append(f"aspect ID set mismatch: {actual_numbers}")
    for missing_aspect in missing_aspect_files(aspect_dirs):
        errors.append(f"missing aspect overview: {missing_aspect.relative_to(ROOT)}")

    curated = sorted(ASPECTS.rglob("*.md"))
    verified_count = 0
    review_needed_count = 0
    verified_documents: list[Path] = []
    for path in curated:
        meta = parse_frontmatter(path)
        if meta is None:
            errors.append(f"missing/invalid frontmatter: {path.relative_to(ROOT)}")
            continue
        required = ASPECT_REQUIRED if is_aspect_overview(path) else SUBDOC_REQUIRED
        missing = sorted(required - set(meta))
        if missing:
            errors.append(f"missing metadata {missing}: {path.relative_to(ROOT)}")
        status = meta.get("status")
        if status not in ALLOWED_STATUS:
            errors.append(f"invalid status {status!r}: {path.relative_to(ROOT)}")
        if status == "verified":
            verified_count += 1
            verified_documents.append(path)
            freshness = meta.get("freshness")
            if freshness not in {"durable", "versioned", "volatile"}:
                errors.append(f"verified document missing freshness: {path.relative_to(ROOT)}")
            if freshness in {"versioned", "volatile"} and "review_due" not in meta:
                errors.append(f"verified versioned/volatile document missing review_due: {path.relative_to(ROOT)}")
        if status == "review-needed":
            review_needed_count += 1

    metrics["verified_aspect_documents"] = verified_count
    metrics["review_needed_aspect_documents"] = review_needed_count

    review_needed_paths = {
        str(path.relative_to(ASPECTS))
        for path in curated
        if (parse_frontmatter(path) or {}).get("status") == "review-needed"
    }
    audited_review_paths: set[str] = set()
    audited_ids: list[str] = []
    if not CLAIM_REVALIDATION.is_file():
        errors.append("missing CLAIM-REVALIDATION.ko.md")
    else:
        for line in CLAIM_REVALIDATION.read_text(encoding="utf-8").splitlines():
            match = re.match(r"^\| (C50-\d{2}) \| `([^`]+)` \|", line)
            if match:
                audited_ids.append(match.group(1))
                audited_review_paths.add(match.group(2))
        expected_ids = [f"C50-{number:02d}" for number in range(1, 51)]
        if audited_ids != expected_ids:
            errors.append("claim-revalidation IDs must be exactly C50-01..C50-50 in order")
        if audited_review_paths != review_needed_paths:
            missing = sorted(review_needed_paths - audited_review_paths)
            extra = sorted(audited_review_paths - review_needed_paths)
            errors.append(
                f"claim-revalidation file set mismatch: missing={missing}, extra={extra}"
            )
    metrics["claim_revalidation_rows"] = len(audited_ids)

    for path in markdown:
        if ASPECTS in path.parents:
            continue
        meta = parse_frontmatter(path)
        if meta is None or meta.get("status") != "verified":
            continue
        verified_documents.append(path)
        missing = sorted(CURATED_REQUIRED - set(meta))
        if missing:
            errors.append(f"missing verified metadata {missing}: {path.relative_to(ROOT)}")
        freshness = meta.get("freshness")
        if freshness not in {"durable", "versioned", "volatile"}:
            errors.append(f"verified document missing freshness: {path.relative_to(ROOT)}")
        if freshness in {"versioned", "volatile"} and "review_due" not in meta:
            errors.append(f"verified versioned/volatile document missing review_due: {path.relative_to(ROOT)}")
    metrics["verified_documents_total"] = len(verified_documents)

    registry_ids: set[str] = set()
    if not SOURCE_REGISTRY.is_file():
        errors.append("missing source registry")
    else:
        for number, line in enumerate(SOURCE_REGISTRY.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"invalid source JSONL line {number}: {exc}")
                continue
            missing = {"id", "title", "publisher", "url", "source_type", "authority_for", "accessed_at", "freshness"} - set(record)
            if missing:
                errors.append(f"source line {number} missing {sorted(missing)}")
            source_id = record.get("id")
            if source_id in registry_ids:
                errors.append(f"duplicate source id: {source_id}")
            if source_id:
                registry_ids.add(source_id)
            if not str(record.get("url", "")).startswith("https://"):
                errors.append(f"source URL must be HTTPS: {source_id}")
    metrics["registered_sources"] = len(registry_ids)

    verified_source_refs = 0
    verified_claim_rows = 0
    for path in verified_documents:
        meta = parse_frontmatter(path) or {}
        source_ids = parse_frontmatter_source_ids(path)
        if not source_ids and meta.get("evidence_track") != "none":
            errors.append(f"verified document has no source IDs: {path.relative_to(ROOT)}")
        for source_id in source_ids:
            verified_source_refs += 1
            if source_id not in registry_ids:
                errors.append(
                    f"unregistered source ID {source_id!r}: {path.relative_to(ROOT)}"
                )
        if meta.get("kind") == "reference":
            claim_count, claim_errors = claim_table_errors(
                path.read_text(encoding="utf-8"), registry_ids
            )
            if not claim_count:
                errors.append(f"verified reference has no claim rows: {path.relative_to(ROOT)}")
            verified_claim_rows += claim_count
            errors.extend(f"{message}: {path.relative_to(ROOT)}" for message in claim_errors)
    metrics["verified_source_references"] = verified_source_refs
    metrics["verified_claim_rows"] = verified_claim_rows

    external_urls = extract_external_urls(CORPUS)
    broken_internal_count = 0
    for path in markdown:
        text = path.read_text(encoding="utf-8")
        for raw_target in LINK_RE.findall(text):
            target = raw_target.strip().split()[0].strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = unquote(target.split("#", 1)[0])
            if not target:
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                broken_internal_count += 1
                errors.append(f"broken internal link: {path.relative_to(ROOT)} -> {raw_target}")
    metrics["external_urls"] = len(external_urls)
    metrics["broken_internal_links"] = broken_internal_count
    external_check, external_counts, external_warnings, external_errors = validate_external_url_ledger(
        external_urls
    )
    for status, count in external_counts.items():
        metrics[f"external_url_{status.replace('-', '_')}"] = count
    warnings.extend(external_warnings)
    errors.extend(external_errors)

    repeated_sections: dict[str, list[tuple[Path, str]]] = defaultdict(list)
    for path in markdown:
        for heading, normalized in normalized_h2_sections(path):
            repeated_sections[hashlib.sha256(normalized.encode("utf-8")).hexdigest()].append(
                (path, heading)
            )
    repeated_groups = [group for group in repeated_sections.values() if len(group) > 1]
    metrics["exact_repeated_section_groups"] = len(repeated_groups)
    for group in repeated_groups:
        errors.append(
            "exact repeated substantial section: "
            + ", ".join(f"{path.relative_to(ROOT)}#{heading}" for path, heading in group)
        )

    legacy_patterns = {
        "gingoa_applied:": re.compile(r"(?m)^gingoa_applied:"),
        "Implications for gingoa": re.compile(r"(?mi)^##\s+Implications for gingoa\s*$"),
        "gingoa application": re.compile(r"(?mi)^##\s+gingoa application\s*$"),
    }
    for path in curated:
        text = path.read_text(encoding="utf-8")
        for label, pattern in legacy_patterns.items():
            if pattern.search(text):
                errors.append(f"legacy project section/field {label}: {path.relative_to(ROOT)}")

    stale_anchor_files: list[tuple[Path, str]] = []
    for path in markdown:
        warning = iso_12207_edition_warning(path.read_text(encoding="utf-8"))
        if warning:
            stale_anchor_files.append((path, warning))
    if stale_anchor_files:
        warnings.extend(
            f"{warning}: {path.relative_to(ROOT)}" for path, warning in stale_anchor_files
        )
    metrics["iso_12207_edition_warnings"] = len(stale_anchor_files)

    print("Corpus validation")
    for key in sorted(metrics):
        print(f"METRIC {key}={metrics[key]}")
    count_text = " ".join(f"{key}={value}" for key, value in sorted(external_counts.items()))
    print(f"CHECK external_reachability={external_check} {count_text}".rstrip())
    for warning in warnings:
        print(f"WARN {warning}")
    for error in errors:
        print(f"FAIL {error}")
    print(f"RESULT {'PASS' if not errors else 'FAIL'} errors={len(errors)} warnings={len(warnings)}")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
