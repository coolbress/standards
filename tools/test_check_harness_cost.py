"""`check_harness_cost` 시험. **네트워크는 안 탄다** (순수 계산만 본다).

🔴 이 계기가 왜 있나: **이 저장소의 창립 실패가 유지비다** — 여섯 세대가 *하네스를 돌보느라
프로젝트를 못 굴려서* 죽었다. 그런데 그것을 재는 눈금이 **하나도 없었다.**
"""

from __future__ import annotations

import unittest
from datetime import UTC, datetime
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
        self.assertIsNotNone(got)
        self.assertAlmostEqual(got or 0.0, 0.75)

    def test_empty_denominator_is_none_not_zero(self) -> None:
        """🔴 분모가 0 인데 `0%` 로 찍으면 **좋은 결과처럼 읽힌다.**

        이 저장소가 `check_decision_referrals` 에서 이미 한 번 배운 형태다.
        """
        self.assertIsNone(mod.ratio(0, 0))

    def test_all_harness_is_one(self) -> None:
        got = mod.ratio(5, 0)
        self.assertIsNotNone(got)
        self.assertAlmostEqual(got or 0.0, 1.0)


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


class TheWindowIsWhatSeesASpike(unittest.TestCase):
    """🔴 **평생 누적만 재면 지금의 유지비 급증이 창립 이력에 묻힌다** (제3자 리뷰 P1 · 2026-09-02).

    누적 318:23 위에 이번 달 20:3 이 얹혀도 비율은 **93% 그대로**다 —
    그게 바로 `R5-45` 가 잡으라던 시나리오인데 **원래 못 봤다.**
    """

    NOW = datetime(2026, 9, 2, tzinfo=UTC)

    def test_a_recent_merge_is_inside(self) -> None:
        self.assertTrue(mod.within("2026-09-01T00:00:00Z", self.NOW))

    def test_an_old_merge_is_outside(self) -> None:
        self.assertFalse(mod.within("2026-06-01T00:00:00Z", self.NOW))

    def test_the_boundary_is_exclusive_at_the_window_edge(self) -> None:
        self.assertTrue(mod.within("2026-08-04T00:00:00Z", self.NOW))     # 29일 전
        self.assertFalse(mod.within("2026-08-03T00:00:00Z", self.NOW))    # 30일 전

    def test_an_unreadable_timestamp_is_neither_in_nor_out(self) -> None:
        """🔴 **`None` 이어야 한다.** 처음엔 `False`(창 밖)를 줬는데 그건 **조용히 세다 마는 것**이고
        *지금 유지비* 가 실제보다 **작아** 보인다 — 창은 급증을 보라고 만든 눈금이다."""
        self.assertIsNone(mod.within("", self.NOW))
        self.assertIsNone(mod.within("어제", self.NOW))

    def test_unreadable_timestamps_fail_the_run(self) -> None:
        source = Path(mod.__file__).read_text(encoding="utf-8")
        self.assertIn("undated", source)
        self.assertIn("`mergedAt` 을 못 읽었다", source)

    def test_the_window_would_expose_a_spike(self) -> None:
        """🔬 누적은 안 움직이는데 창은 움직인다 — 그게 이 눈금의 존재 이유다."""
        lifetime = mod.ratio(318 + 20, 23 + 3)
        window = mod.ratio(20, 3)
        self.assertAlmostEqual(lifetime or 0.0, 0.929, places=2)
        self.assertAlmostEqual(window or 0.0, 0.870, places=2)
