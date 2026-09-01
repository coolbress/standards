"""`check_harness_cost` 시험. **네트워크는 안 탄다** (순수 계산만 본다).

🔴 이 계기가 왜 있나: **이 저장소의 창립 실패가 유지비다** — 여섯 세대가 *하네스를 돌보느라
프로젝트를 못 굴려서* 죽었다. 그런데 그것을 재는 눈금이 **하나도 없었다.**
"""

from __future__ import annotations

import unittest
from pathlib import Path

import check_harness_cost as mod


class WhatCountsAsWhich(unittest.TestCase):
    def test_the_three_harness_repos_are_named(self) -> None:
        self.assertEqual(set(mod.HARNESS), {"standards", "workflows", "project-template"})

    def test_divcal_is_the_product(self) -> None:
        self.assertEqual(set(mod.PRODUCT), {"divcal"})

    def test_summarise_splits_the_two_sides(self) -> None:
        got = mod.summarise({"standards": 30, "workflows": 20,
                             "project-template": 10, "divcal": 5})
        self.assertEqual(got, {"harness": 60, "product": 5})

    def test_unknown_repos_are_ignored(self) -> None:
        """🔬 오탐 — 목록에 없는 저장소를 몰래 어느 쪽에 넣으면 비율이 거짓말한다."""
        got = mod.summarise({"standards": 3, "someone-else": 99})
        self.assertEqual(got, {"harness": 3, "product": 0})


class RatioDoesNotLie(unittest.TestCase):
    def test_ratio_is_harness_over_total(self) -> None:
        got = mod.ratio(3, 1)
        assert got is not None
        self.assertAlmostEqual(got, 0.75)

    def test_empty_denominator_is_none_not_zero(self) -> None:
        """🔴 분모가 0 인데 `0%` 로 찍으면 **좋은 결과처럼 읽힌다.**

        이 저장소가 `check_decision_referrals` 에서 이미 한 번 배운 형태다.
        """
        self.assertIsNone(mod.ratio(0, 0))

    def test_all_harness_is_one(self) -> None:
        got = mod.ratio(5, 0)
        assert got is not None
        self.assertAlmostEqual(got, 1.0)


class ItIsAnInstrumentThatFailsClosed(unittest.TestCase):
    def test_no_threshold_is_drawn(self) -> None:
        """🔴 임계값을 지금 그으면 **표본 하나로 상상해서 긋는 것**이다(R5-2 규율)."""
        source = Path(mod.__file__).read_text(encoding="utf-8")
        self.assertIn("RESULT INFO", source)
        self.assertIn("판정선은 긋지 않았다", source)

    def test_unreadable_source_is_a_failure(self) -> None:
        """🔴 못 읽은 저장소를 0 으로 세면 **비율이 거짓말을 한다.**"""
        source = Path(mod.__file__).read_text(encoding="utf-8")
        self.assertIn("RESULT FAIL — **못 읽은 것을 0 으로 읽지 않는다.**", source)

    def test_hitting_the_cap_is_a_failure(self) -> None:
        """🔬 `standards` 는 이미 머지된 PR 이 200건을 넘었다 — 상한은 실제로 닿는다."""
        source = Path(mod.__file__).read_text(encoding="utf-8")
        self.assertIn("상한", source)
        self.assertIn("truncated", source)

    def test_the_doc_says_the_ratio_alone_cannot_decide(self) -> None:
        """🔴 하네스가 *비싼* 것과 제품이 *아직 하나뿐인* 것은 **같은 숫자로 보인다.**"""
        doc = mod.__doc__ or ""
        self.assertIn("비율만으로는 못 가른다", doc)
