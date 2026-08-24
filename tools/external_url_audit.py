#!/usr/bin/env python3
"""Check every URL in active corpus Markdown plus the canonical source registry."""

from __future__ import annotations

import argparse
import hashlib
import json
import socket
import ssl
import subprocess
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from validate_corpus import CORPUS, extract_external_urls


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "audit"
LEDGER = AUDIT / "external-url-status.jsonl"
META = AUDIT / "external-url-status-meta.json"
CHECKER_VERSION = 1
VALID_STATUSES = {
    "reachable",
    "redirected",
    "access-blocked",
    "dead",
    "http-error",
    "network-error",
}
ACCESS_BLOCKED_CODES = {401, 403, 405, 406, 407, 409, 418, 423, 425, 429, 451}
DEAD_CODES = {404, 410}


def url_set_digest(urls: set[str]) -> str:
    payload = "\n".join(sorted(urls)) + "\n"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def classify_http(code: int, requested_url: str, final_url: str) -> str:
    if 200 <= code < 400:
        return "redirected" if final_url != requested_url else "reachable"
    if code in ACCESS_BLOCKED_CODES:
        return "access-blocked"
    if code in DEAD_CODES:
        return "dead"
    return "http-error"


def curl_fallback(url: str, timeout: float, retries: int) -> dict[str, object] | None:
    """Use the system trust store when Python's TLS/network stack cannot classify an endpoint."""
    command = [
        "curl",
        "--location",
        "--silent",
        "--show-error",
        "--output",
        "/dev/null",
        "--range",
        "0-1023",
        "--max-time",
        str(timeout),
        "--retry",
        str(retries),
        "--write-out",
        "%{http_code}\t%{url_effective}",
        url,
    ]
    try:
        completed = subprocess.run(command, capture_output=True, text=True, timeout=timeout * (retries + 2))
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None
    fields = completed.stdout.strip().split("\t", 1)
    if completed.returncode != 0:
        return None
    if len(fields) != 2 or not fields[0].isdigit() or int(fields[0]) == 0:
        return None
    code = int(fields[0])
    final_url = fields[1]
    return {
        "status": classify_http(code, url, final_url),
        "http_status": code,
        "final_url": final_url,
        "method": "curl-GET-range-fallback",
        "detail": completed.stderr.strip() or "Classified with system curl fallback.",
    }


def check_one(url: str, timeout: float, retries: int) -> dict[str, object]:
    checked_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    last_error = ""
    attempts = 0
    for attempt in range(1, retries + 2):
        attempts = attempt
        request = Request(
            url,
            headers={
                "User-Agent": "goppi-final-research-link-audit/1.0",
                "Accept": "text/html,application/pdf,application/json,*/*;q=0.8",
                "Range": "bytes=0-1023",
            },
            method="GET",
        )
        try:
            with urlopen(request, timeout=timeout, context=ssl.create_default_context()) as response:
                code = int(response.getcode() or 200)
                final_url = response.geturl()
                response.read(1024)
                return {
                    "url": url,
                    "checked_at": checked_at,
                    "status": classify_http(code, url, final_url),
                    "http_status": code,
                    "final_url": final_url,
                    "attempts": attempts,
                    "method": "GET-range",
                    "content_verified": False,
                    "detail": "Endpoint response only; claim-supporting content was not verified.",
                }
        except HTTPError as exc:
            code = int(exc.code)
            final_url = exc.geturl() or url
            status = classify_http(code, url, final_url)
            if status in {"access-blocked", "dead"}:
                return {
                    "url": url,
                    "checked_at": checked_at,
                    "status": status,
                    "http_status": code,
                    "final_url": final_url,
                    "attempts": attempts,
                    "method": "GET-range",
                    "content_verified": False,
                    "detail": str(exc.reason),
                }
            last_error = f"HTTP {code}: {exc.reason}"
        except (URLError, TimeoutError, socket.timeout, ssl.SSLError, ValueError) as exc:
            last_error = f"{type(exc).__name__}: {exc}"
        if attempt <= retries:
            time.sleep(min(0.75 * attempt, 2.0))
    fallback = curl_fallback(url, timeout, retries)
    if fallback is not None:
        return {
            "url": url,
            "checked_at": checked_at,
            "status": fallback["status"],
            "http_status": fallback["http_status"],
            "final_url": fallback["final_url"],
            "attempts": attempts + 1,
            "method": fallback["method"],
            "content_verified": False,
            "detail": f"urllib={last_error}; curl={fallback['detail']}",
        }
    status = "http-error" if last_error.startswith("HTTP ") else "network-error"
    return {
        "url": url,
        "checked_at": checked_at,
        "status": status,
        "http_status": None,
        "final_url": None,
        "attempts": attempts,
        "method": "GET-range",
        "content_verified": False,
        "detail": last_error,
    }


def write_ledger(records: list[dict[str, object]], started_at: str) -> None:
    records.sort(key=lambda item: str(item["url"]))
    urls = {str(item["url"]) for item in records}
    counts = Counter(str(item["status"]) for item in records)
    AUDIT.mkdir(parents=True, exist_ok=True)
    temporary_ledger = LEDGER.with_suffix(".jsonl.tmp")
    temporary_ledger.write_text(
        "".join(json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n" for item in records),
        encoding="utf-8",
    )
    temporary_ledger.replace(LEDGER)
    meta = {
        "schema_version": 1,
        "checker_version": CHECKER_VERSION,
        "started_at": started_at,
        "completed_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "corpus_root": str(CORPUS.relative_to(ROOT)),
        "url_count": len(urls),
        "url_set_sha256": url_set_digest(urls),
        "counts": dict(sorted(counts.items())),
        "semantics": {
            "reachable_or_redirected": "An endpoint returned 2xx/3xx; content support was not assessed.",
            "access_blocked": "The server responded but denied/limited this checker; content is unverified.",
            "dead": "The endpoint returned 404 or 410.",
            "http_or_network_error": "No healthy/blocked/dead disposition was established after retries.",
        },
    }
    temporary_meta = META.with_suffix(".json.tmp")
    temporary_meta.write_text(json.dumps(meta, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary_meta.replace(META)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=16)
    parser.add_argument("--timeout", type=float, default=15.0)
    parser.add_argument("--retries", type=int, default=1)
    args = parser.parse_args()
    urls = extract_external_urls(CORPUS)
    started_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    print(f"Checking {len(urls)} URLs with workers={args.workers} timeout={args.timeout}s retries={args.retries}")
    records: list[dict[str, object]] = []
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(check_one, url, args.timeout, args.retries): url for url in urls}
        for index, future in enumerate(as_completed(futures), 1):
            records.append(future.result())
            if index % 50 == 0 or index == len(futures):
                counts = Counter(str(item["status"]) for item in records)
                print(f"PROGRESS {index}/{len(futures)} {dict(sorted(counts.items()))}", flush=True)
    write_ledger(records, started_at)
    counts = Counter(str(item["status"]) for item in records)
    print(f"WROTE {LEDGER.relative_to(ROOT)} records={len(records)} counts={dict(sorted(counts.items()))}")
    return 1 if any(counts[name] for name in ("dead", "http-error", "network-error")) else 0


if __name__ == "__main__":
    raise SystemExit(main())
