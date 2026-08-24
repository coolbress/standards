#!/usr/bin/env python3
"""Focused regression tests for validator failures found by independent review."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from validate_corpus import claim_table_errors, missing_aspect_files


class ClaimTableTests(unittest.TestCase):
    def setUp(self) -> None:
        self.sources = {"SRC-ONE"}

    def test_valid_six_field_claim(self) -> None:
        text = "| ABC-001 | empirical | bounded claim | `SRC-ONE` | high | 2027-01-01 |"
        count, errors = claim_table_errors(text, self.sources)
        self.assertEqual(1, count)
        self.assertEqual([], errors)

    def test_rejects_source_outside_evidence_and_blank_fields(self) -> None:
        text = "| ABC-001 | invalid-class | claim cites SRC-ONE | | | |"
        count, errors = claim_table_errors(text, self.sources)
        self.assertEqual(1, count)
        self.assertTrue(any("invalid class" in item for item in errors))
        self.assertTrue(any("blank evidence" in item for item in errors))
        self.assertTrue(any("blank confidence" in item for item in errors))
        self.assertTrue(any("blank expiry" in item for item in errors))
        self.assertTrue(any("Evidence field" in item for item in errors))

    def test_rejects_wrong_field_count(self) -> None:
        text = "| ABC-001 | empirical | claim | `SRC-ONE` |"
        count, errors = claim_table_errors(text, self.sources)
        self.assertEqual(1, count)
        self.assertTrue(any("expected 6" in item for item in errors))

    def test_rejects_prefix_collision_and_mixed_invalid_ids(self) -> None:
        text = (
            "| ABC-001 | empirical | claim | "
            "`SRC-ONE-NOT-REGISTERED`; `BOGUS` | high | 2027-01-01 |"
        )
        count, errors = claim_table_errors(text, self.sources)
        self.assertEqual(1, count)
        self.assertTrue(any("SRC-ONE-NOT-REGISTERED" in item for item in errors))
        self.assertTrue(any("BOGUS" in item for item in errors))
        self.assertTrue(any("no registered source ID" in item for item in errors))

    def test_allows_known_local_claim_reference_with_direct_source(self) -> None:
        text = "\n".join(
            [
                "| ABC-001 | empirical | source claim | `SRC-ONE` | high | 2027-01-01 |",
                "| ABC-002 | synthesis | combined claim | ABC-001; `SRC-ONE` | high | 2027-01-01 |",
            ]
        )
        count, errors = claim_table_errors(text, self.sources)
        self.assertEqual(2, count)
        self.assertEqual([], errors)

    def test_does_not_parse_quoted_numeric_source_as_local_claim(self) -> None:
        text = "| ABC-001 | normative | claim | `NIST-GAI-600-1` | high | 2027-01-01 |"
        count, errors = claim_table_errors(text, {"NIST-GAI-600-1"})
        self.assertEqual(1, count)
        self.assertEqual([], errors)


class AspectStructureTests(unittest.TestCase):
    def test_reports_directory_without_aspect_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            present = Path(directory) / "01-present"
            absent = Path(directory) / "02-absent"
            present.mkdir()
            absent.mkdir()
            # Renamed 2026-08-08: the overview file is `<topic>--overview.md`, not `_aspect.md`.
            # The old name repeated identically across all 28 topic directories.
            (present / "01-present--overview.md").write_text("---\n---\n", encoding="utf-8")
            self.assertEqual(
                [absent / "02-absent--overview.md"], missing_aspect_files([present, absent])
            )

    def test_old_aspect_filename_no_longer_satisfies_the_check(self) -> None:
        """A stale `_aspect.md` must NOT count as present.

        Without this the rename could half-land: a directory keeping the old name
        would pass silently and the validator would report green on a broken tree.
        """
        with tempfile.TemporaryDirectory() as directory:
            stale = Path(directory) / "03-stale"
            stale.mkdir()
            (stale / "_aspect.md").write_text("---\n---\n", encoding="utf-8")
            self.assertEqual([stale / "03-stale--overview.md"], missing_aspect_files([stale]))


if __name__ == "__main__":
    unittest.main()
