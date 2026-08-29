#!/usr/bin/env python3
"""Unit tests for external URL inventory and response classification."""

from __future__ import annotations

import hashlib
import subprocess
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

from external_url_audit import classify_http, curl_fallback, url_set_digest
from validate_corpus import (
    external_url_record_errors,
    extract_external_urls,
    iso_12207_edition_warning,
    normalize_external_url,
)


class ExternalUrlAuditTests(unittest.TestCase):
    def test_extracts_deduplicated_normalized_urls(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "one.md").write_text("https://example.com/a. https://example.com/a", encoding="utf-8")
            (root / "two.md").write_text("[x](https://example.org/b)", encoding="utf-8")
            (root / "_meta").mkdir()
            (root / "_meta" / "sources.jsonl").write_text(
                '{"url":"https://registry.example/source"}\n', encoding="utf-8"
            )
            self.assertEqual(
                {
                    "https://example.com/a",
                    "https://example.org/b",
                    "https://registry.example/source",
                },
                extract_external_urls(root),
            )

    def test_url_set_digest_is_order_independent(self) -> None:
        expected = hashlib.sha256(b"https://a.example\nhttps://b.example\n").hexdigest()
        self.assertEqual(expected, url_set_digest({"https://b.example", "https://a.example"}))

    def test_preserves_balanced_parentheses_and_trims_markdown_closer(self) -> None:
        doi = "https://dl.acm.org/doi/10.1016/S0164-1212(02)00156-5)"
        self.assertEqual(
            "https://dl.acm.org/doi/10.1016/S0164-1212(02)00156-5",
            normalize_external_url(doi),
        )
        self.assertEqual("https://example.com/(x)", normalize_external_url("https://example.com/(x)"))

    def test_classifies_response_without_claiming_content_verification(self) -> None:
        self.assertEqual("reachable", classify_http(200, "https://a", "https://a"))
        self.assertEqual("redirected", classify_http(200, "https://a", "https://b"))
        self.assertEqual("access-blocked", classify_http(403, "https://a", "https://a"))
        self.assertEqual("dead", classify_http(404, "https://a", "https://a"))
        self.assertEqual("http-error", classify_http(500, "https://a", "https://a"))

    def test_iso_generic_reference_requires_current_edition(self) -> None:
        self.assertIsNotNone(iso_12207_edition_warning("ISO 12207 process"))
        self.assertIsNone(iso_12207_edition_warning("ISO/IEC/IEEE 12207:2026 catalog scope"))

    def test_iso_historical_reference_requires_withdrawal_disposition(self) -> None:
        text = "ISO/IEC/IEEE 12207:2017 is withdrawn; ISO/IEC/IEEE 12207:2026 is current."
        self.assertIsNone(iso_12207_edition_warning(text))
        self.assertIsNotNone(
            iso_12207_edition_warning("ISO/IEC/IEEE 12207:2017 and ISO/IEC/IEEE 12207:2026")
        )
        unrelated = (
            "A different standard is withdrawn. ISO/IEC/IEEE 12207:2017 clause 6 requires tailoring. "
            "ISO/IEC/IEEE 12207:2026 is current."
        )
        self.assertIsNotNone(iso_12207_edition_warning(unrelated))

    def test_reachability_record_requires_timestamp_and_response_evidence(self) -> None:
        record = {
            "url": "https://example.com/",
            "checked_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "status": "reachable",
            "http_status": 200,
            "final_url": "https://example.com/",
            "attempts": 1,
            "method": "GET-range",
            "content_verified": False,
            "detail": "endpoint only",
        }
        self.assertEqual([], external_url_record_errors(record, record["url"]))
        broken = dict(record, checked_at="not-a-date", http_status=404, content_verified=True)
        errors = external_url_record_errors(broken, record["url"])
        self.assertTrue(any("invalid checked_at" in item for item in errors))
        self.assertTrue(any("2xx/3xx" in item for item in errors))
        self.assertTrue(any("must not claim content" in item for item in errors))

    def test_rejects_future_dated_and_blank_detail_record(self) -> None:
        record = {
            "url": "https://example.com/",
            "checked_at": "2099-01-01T00:00:00Z",
            "status": "reachable",
            "http_status": 200,
            "final_url": "https://example.com/",
            "attempts": 1,
            "method": "GET-range",
            "content_verified": False,
            "detail": "",
        }
        errors = external_url_record_errors(record, record["url"])
        self.assertTrue(any("future" in item for item in errors))
        self.assertTrue(any("detail is blank" in item for item in errors))

    @patch("external_url_audit.subprocess.run")
    def test_curl_fallback_rejects_nonzero_redirect_loop(self, run) -> None:
        run.return_value = subprocess.CompletedProcess(
            args=["curl"], returncode=47, stdout="302\thttps://example.com/loop", stderr="redirect loop"
        )
        self.assertIsNone(curl_fallback("https://example.com/loop", 1, 0))


if __name__ == "__main__":
    unittest.main()
