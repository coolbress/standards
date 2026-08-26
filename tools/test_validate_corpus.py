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


class ClaimIdShapeTests(unittest.TestCase):
    """R5-14: a bolded ID cell made the whole row invisible to the checker.

    `CLAIM_ID_RE` matches the cell in full, so `**ABC-001**` never matched and the
    row was skipped with `continue` — not reported, not counted, not checked.
    42 rows across six documents sat like that; every one of them had been written
    by the reverification program itself.
    """

    def test_bolded_claim_id_is_not_silently_skipped(self) -> None:
        plain = "| ABC-001 | empirical | bounded claim | `SRC-ONE` | high | 2027-01-01 |"
        bolded = "| **ABC-001** | empirical | bounded claim | `SRC-ONE` | high | 2027-01-01 |"
        plain_count, _ = claim_table_errors(plain, {"SRC-ONE"})
        bolded_count, _ = claim_table_errors(bolded, {"SRC-ONE"})
        self.assertEqual(1, plain_count)
        self.assertEqual(
            plain_count,
            bolded_count,
            "a bolded claim ID must not make the row invisible to the checker",
        )

    def test_unescaped_pipe_in_a_cell_is_reported_not_ignored(self) -> None:
        """R5-14 side finding: CAS-005 carried `http\|sse\|stdio` and split into 8 fields.

        Markdown renders `\|` as a literal pipe, but the checker splits naively, so the
        row silently gained two fields. It must surface as a field-count error.
        """
        row = "| ABC-002 | empirical | uses a\|b | `SRC-ONE` | high | 2027-01-01 |"
        _, errors = claim_table_errors(row, {"SRC-ONE"})
        self.assertTrue(
            any("expected 6" in message for message in errors),
            f"expected a field-count error, got {errors}",
        )


class DirectionCitationAnchorTests(unittest.TestCase):
    """R5-22: `direction` 이 claim table 없는 코퍼스 문서를 근거로 인용하면 사슬이 거기서 끝난다.

    2026-08-26 실측으로 두 건이 그 상태였다 — GHW-012(폐기 문서 인용)와
    IPC-001~003(앵커 없는 🟢). 검사를 붙였고, 이 시험은 그 검사가 **실제로
    빨간불이 될 수 있는지**를 잠근다. 초록인 검사가 초록인 이유가
    "위반이 없어서" 인지 "검사가 안 돌아서" 인지는 구별되어야 한다.
    """

    def test_claimless_document_is_detected(self) -> None:
        """claim 행이 없는 문서는 claim_table_errors 가 0 을 센다 — 검사의 판별 근거."""
        text = "# 산문뿐인 문서\n\n- 주장처럼 보이지만 claim 행이 아니다.\n"
        count, _ = claim_table_errors(text, {"SRC-ONE"})
        self.assertEqual(0, count)

    def test_claim_bearing_document_is_distinguished(self) -> None:
        text = "| ABC-001 | empirical | bounded claim | `SRC-ONE` | high | 2027-01-01 |"
        count, errors = claim_table_errors(text, {"SRC-ONE"})
        self.assertEqual(1, count)
        self.assertEqual([], errors)


if __name__ == "__main__":
    unittest.main()
