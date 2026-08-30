"""`check_evidence_class` 시험. 네트워크는 안 탄다.

지켜야 하는 성질: **수치가 있는 줄에서만** 한정어 없는 `[lit]` 을 센다.
산문 전체에 태그를 요구하면 바닥이 문진표가 되고 그 자체가 P40 위반이다.
"""

from __future__ import annotations

import unittest

import check_evidence_class as mod


class Untyped(unittest.TestCase):
    def test_bare_lit_on_a_figure_line_is_caught(self) -> None:
        self.assertEqual(len(mod.untyped("- ADR 채택 ~50%. [lit]")), 1)

    def test_qualified_lit_passes(self) -> None:
        self.assertEqual(mod.untyped("- ADR 채택 ~50% (900 repos). [lit, empirical]"), [])
        self.assertEqual(mod.untyped("- Must effort ≲60%. [lit, normative]"), [])

    def test_bare_lit_without_a_figure_is_not_counted(self) -> None:
        """🔴 수치 없는 산문까지 요구하면 문진표가 된다."""
        self.assertEqual(mod.untyped("- 설계 결정은 기록한다. [lit]"), [])

    def test_census_tag_is_not_this_checks_business(self) -> None:
        """`[census]` 는 이미 실측이라고 말하고 있다 — 애매한 것은 `[lit]` 뿐이다."""
        self.assertEqual(mod.untyped("- 계획 산출물 13%. [census]"), [])

    def test_n_equals_also_counts_as_a_figure(self) -> None:
        self.assertEqual(len(mod.untyped("- 표본 n=938 이었다. [lit]")), 1)

    def test_version_numbers_are_not_figures(self) -> None:
        """`v1.29.0` 같은 것에 걸리면 오탐이 신호를 묻는다."""
        self.assertEqual(mod.untyped("- zizmor v1.29.0 을 쓴다. [lit]"), [])

    def test_real_corpus_is_at_or_below_baseline(self) -> None:
        self.assertEqual(mod.main(), 0)
