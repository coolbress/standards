"""`check_dead_end_signals` 시험. **네트워크는 안 탄다** (신호 B 와 순수 계산만 본다).

🔴 이 도구의 요점은 **θ 를 상상해서 박지 않는 것**이다. 등재된 근거가
*"θ is read from healthy validation episodes and never from test data"* 라고 못박는다.
시험이 그 성질을 지킨다.
"""

from __future__ import annotations

import unittest

import check_dead_end_signals as mod


class ThetaComesFromMeasurement(unittest.TestCase):
    def test_theta_is_one_above_the_healthy_maximum(self) -> None:
        """상수가 아니라 **측정에서 나온 수**여야 한다."""
        self.assertEqual(mod.THETA, mod.HEALTHY_MAX_OBSERVED + 1)

    def test_healthy_maximum_is_documented_not_guessed(self) -> None:
        """모듈 문서에 **언제 무엇을 재서** 이 값이 나왔는지 적혀 있어야 한다."""
        doc = mod.__doc__ or ""
        self.assertIn("healthy validation episodes", doc)
        for token in ("106", "88", "θ = 2"):
            self.assertIn(token, doc, f"실측 근거 {token} 이 문서에 없다")

    def test_theta_is_at_least_two(self) -> None:
        """θ=1 이면 **한 번 빨간 것도 막다른 길**이 되어 계기판이 소음이 된다."""
        self.assertGreaterEqual(mod.THETA, 2)


class TwoSignalsExist(unittest.TestCase):
    """처방이 *"감지 신호 **2개 이상**"* 을 요구한다. 하나만 있으면 미이행이다."""

    def test_both_signals_are_implemented(self) -> None:
        self.assertTrue(callable(mod.signal_a))
        self.assertTrue(callable(mod.signal_b))

    def test_signal_b_reads_the_real_ledger(self) -> None:
        """B 는 네트워크 없이 git 이력만 읽는다 — 목 없이 실제로 돌아야 한다."""
        self.assertIsInstance(mod.signal_b(), list)

    def test_the_ledger_path_exists(self) -> None:
        self.assertTrue(mod.LEDGER.is_file(), "GAPS 대장을 못 찾으면 신호 B 가 조용히 0 이 된다")
