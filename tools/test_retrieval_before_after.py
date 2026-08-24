#!/usr/bin/env python3
"""Regression tests for the matched retrieval evidence classifier."""

from __future__ import annotations

import unittest

from evaluate_retrieval_before_after import has_traceable_claim


class TraceableClaimTests(unittest.TestCase):
    def test_accepts_block_source_list_and_claim_table(self) -> None:
        content = """---
sources:
  - SRC-ONE
---
## Claim table
| ABC-001 | empirical | claim | `SRC-ONE` | high | 2027-01-01 |
"""
        self.assertTrue(has_traceable_claim(content))

    def test_rejects_verified_style_prose_without_claim_rows(self) -> None:
        content = """---
sources: [SRC-ONE]
---
## Claim register
This document says it is verified but has no atomic claim row.
"""
        self.assertFalse(has_traceable_claim(content))


if __name__ == "__main__":
    unittest.main()

