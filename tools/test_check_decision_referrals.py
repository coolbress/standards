"""`check_decision_referrals` 시험. **네트워크는 안 탄다** (순수 판정만 본다).

🔴 이 도구가 왜 있나: `direction/04` 가 기록 수단을 못박아 뒀는데 **아무것도 그걸
발화시키지 않았다** — 실측 회부 0건. *수단은 적어뒀는데 안 쓴다* 는 이 저장소가 오늘
하루 종일 고친 결함의 형태다. **행동을 바꾸기 전에 계기부터 단다.**
"""

from __future__ import annotations

import unittest

import check_decision_referrals as mod


class MechanismMustExist(unittest.TestCase):
    """계기가 없는 것과 눈금이 0 인 것은 **다르다.**

    🔴 **라벨이 실제로 깔렸는지는 여기서 안 본다.** 그건 `gh` 를 타는 **서버 사실**이고,
    CI 에는 네트워크·자격증명이 없다. 처음에 여기 넣었다가 CI 만 빨개졌다 —
    *"네트워크는 안 탄다"* 고 적어놓고 타는 시험을 쓴 것이다.
    서버 사실은 `tools/repo_audit.py` 가 본다(거기가 그런 검사의 자리다).
    """

    def test_both_labels_are_named(self) -> None:
        self.assertEqual(mod.LABEL, "decision")
        self.assertEqual(mod.RESIMPLE, "needs-simpler")


class PreRegistrationIsHonoured(unittest.TestCase):
    def test_the_doc_states_it_is_a_strengthening_not_a_relaxation(self) -> None:
        """🔴 수단을 바꾸는 순간 **왜 완화가 아닌지**가 문서에 있어야 한다.

        §판정 기준이 *"결과를 보고 기준을 옮기지 않는다"* 로 시작하기 때문이다.
        """
        doc = mod.__doc__ or ""
        self.assertIn("완화가 아니라 강화", doc)
        for axis in ("분모", "ⓑ", "ⓒ", "작업량"):
            self.assertIn(axis, doc, f"강화 판정의 축 {axis} 가 문서에 없다")

    def test_the_doc_records_the_measurement_that_opened_the_gap(self) -> None:
        doc = mod.__doc__ or ""
        self.assertIn("0건", doc, "사전등록된 곳에 회부가 0건이었다는 실측이 없다")


class ItIsAnInstrumentNotAWall(unittest.TestCase):
    def test_zero_referrals_is_not_a_failure(self) -> None:
        """회부가 0 인 것은 **아직 안 물었다**일 수도 있다. 그걸로 빨개지면 안 된다."""
        source = (mod.__file__ and open(mod.__file__, encoding="utf-8").read()) or ""
        self.assertIn("RESULT INFO", source)

    def test_missing_labels_is_a_failure(self) -> None:
        """다만 **수단 자체가 없으면** 실패다 — 그건 눈금이 0 인 게 아니라 계기가 없는 것이다."""
        source = open(mod.__file__, encoding="utf-8").read()
        self.assertIn("RESULT FAIL — 수단이 설치되지 않았다", source)


class CountingWorksOnBothPaths(unittest.TestCase):
    """🔬 **빈 경우만 돌려본 것이 초록이었다.**

    처음 판은 `(comments or 0) > 0` 이라 **코멘트가 없을 때만** 통과했고, 첫 회부에 답이
    달리는 순간 `TypeError: '>' not supported between 'list' and 'int'` 로 터졌다.
    *실행되지 않은 경로의 초록은 증거가 아니다* — 그래서 **양쪽을 다 돌린다.**
    """

    @staticmethod
    def _issue(state: str, comments: int = 0, resimple: bool = False) -> dict[str, object]:
        return {
            "state": state,
            "comments": [{"body": "x"} for _ in range(comments)],
            "labels": ([{"name": mod.RESIMPLE}] if resimple else []) + [{"name": mod.LABEL}],
        }

    def test_closed_with_comments_counts_as_answered(self) -> None:
        rows = [("standards", self._issue("CLOSED", comments=2))]
        self.assertEqual(mod.summarise(rows)["answered"], 1)

    def test_closed_without_comments_is_not_answered(self) -> None:
        """닫혔는데 답이 없는 회부 — *조용히 닫은 것*이라 드러나야 한다."""
        rows = [("standards", self._issue("CLOSED"))]
        self.assertEqual(mod.summarise(rows)["answered"], 0)

    def test_open_referrals_are_not_closed(self) -> None:
        rows = [("standards", self._issue("OPEN", comments=3))]
        got = mod.summarise(rows)
        self.assertEqual((got["total"], got["closed"]), (1, 0))

    def test_needs_simpler_is_counted(self) -> None:
        rows = [("standards", self._issue("CLOSED", comments=1, resimple=True))]
        self.assertEqual(mod.summarise(rows)["resimple"], 1)

    def test_empty_input_does_not_crash(self) -> None:
        self.assertEqual(mod.summarise([])["total"], 0)
