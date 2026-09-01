"""`check_decision_referrals` 시험. **네트워크는 안 탄다** (순수 판정만 본다).

🔴 이 도구가 왜 있나: `direction/04` 가 기록 수단을 못박아 뒀는데 **아무것도 그걸
발화시키지 않았다** — 실측 회부 0건. *수단은 적어뒀는데 안 쓴다* 는 이 저장소가 오늘
하루 종일 고친 결함의 형태다. **행동을 바꾸기 전에 계기부터 단다.**
"""

from __future__ import annotations

import unittest
from collections.abc import Mapping
from pathlib import Path
from typing import Any

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
        source = Path(mod.__file__).read_text(encoding="utf-8") if mod.__file__ else ""
        self.assertIn("RESULT INFO", source)

    def test_missing_labels_is_a_failure(self) -> None:
        """다만 **수단 자체가 없으면** 실패다 — 그건 눈금이 0 인 게 아니라 계기가 없는 것이다."""
        source = Path(mod.__file__).read_text(encoding="utf-8")
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


class ThreeKindsNotOne(unittest.TestCase):
    """회부는 한 종류가 아니다 — Approval · Input · Escalation 은 **트리거도 대기 방식도 다르다.**"""

    def test_three_kinds_are_defined(self) -> None:
        self.assertEqual(
            set(mod.KINDS), {"decision:approval", "decision:input", "decision:escalation"}
        )

    def test_kind_is_read_from_labels(self) -> None:
        issue = {"labels": [{"name": mod.LABEL}, {"name": "decision:escalation"}]}
        self.assertEqual(mod.kind_of(issue), "decision:escalation")

    def test_missing_kind_is_detected(self) -> None:
        """종류가 없으면 **긴급도를 못 가린다.**"""
        self.assertIsNone(mod.kind_of({"labels": [{"name": mod.LABEL}]}))

    def test_summarise_counts_each_kind(self) -> None:
        # 🔴 명시한다 — 값이 섞인 dict 리터럴은 `object` 로 좁혀져 시그니처와 안 맞는다.
        rows: list[tuple[str, Mapping[str, Any]]] = [
            ("s", {"state": "OPEN", "labels": [{"name": "decision:input"}], "comments": []}),
            ("s", {"state": "OPEN", "labels": [{"name": "decision:input"}], "comments": []}),
            ("s", {"state": "OPEN", "labels": [], "comments": []})]
        got = mod.summarise(rows)
        self.assertEqual((got["decision:input"], got["unkinded"]), (2, 1))


class ChannelIsRecorded(unittest.TestCase):
    """*"who approved what, when, **via which channel**"* — 대화로 온 답을 옮기면
    **내가 정확히 옮겼는지를 아무도 검증할 수 없다.** 그 사실을 남긴다."""

    def test_channel_marker_is_found_in_any_comment(self) -> None:
        issue = {"comments": [{"body": "일반 답"}, {"body": f"{mod.CHANNEL_MARKER} 대화"}]}
        self.assertTrue(mod.has_channel(issue))

    def test_absent_channel_is_detected(self) -> None:
        self.assertFalse(mod.has_channel({"comments": [{"body": "그냥 답"}]}))


class TheBridgeToCommittedRecords(unittest.TestCase):
    """🔴 **RFC 는 이슈에 살아도 되지만 결정은 커밋된다.**

    이슈는 저장소 밖이라 diff 도 PR 리뷰도 없다 — 코퍼스가 위키를 물리치며 든 이유다.
    지금까지 지켜진 건 **우연이었고, 우연은 규율이 아니다.**
    """

    def test_closed_referral_cited_in_records_passes(self) -> None:
        rows = [("standards", {"state": "CLOSED", "number": 141, "labels": [], "comments": []})]
        self.assertEqual(mod.unbridged(rows, "…를 #141 에서 정했다…"), [])

    def test_closed_referral_absent_from_records_is_caught(self) -> None:
        rows = [("standards", {"state": "CLOSED", "number": 999, "labels": [], "comments": []})]
        self.assertEqual(mod.unbridged(rows, "관계 없는 본문"), [("standards", 999)])

    def test_open_referral_needs_no_record_yet(self) -> None:
        """아직 안 정해진 것에 기록을 요구하면 검사가 소음이 된다."""
        rows = [("standards", {"state": "OPEN", "number": 999, "labels": [], "comments": []})]
        self.assertEqual(mod.unbridged(rows, ""), [])

    def test_issue_url_form_also_counts(self) -> None:
        rows = [("standards", {"state": "CLOSED", "number": 141, "labels": [], "comments": []})]
        self.assertEqual(mod.unbridged(rows, "…/issues/141 참조…"), [])

    def test_record_dirs_are_committed_ones(self) -> None:
        self.assertEqual(set(mod.RECORD_DIRS), {"direction", "audit"})


class PrBodyMarkerIsTheSecondMeans(unittest.TestCase):
    """2026-09-01 · `GAPS` R5-37 ⓑ — PR 본문의 `회부:` 표시를 센다.

    🔴 **음성 시험이 핵심이다.** 표시만 있으면 통과시키면 계기가 아무것도 안 재게 된다 —
    종류가 없는 줄과 채널이 없는 줄이 **각각 잡혀야** 눈금이 뜻을 갖는다.
    """

    GOOD = "회부: decision:input — 어휘를 A 로 갈까 B 로 갈까 → 답: A (채널: 대화)"

    def test_marker_line_is_picked_out_of_a_body(self) -> None:
        body = f"## 무엇을 했나\n어쩌고.\n\n{self.GOOD}\n\n## 검사\n초록."
        self.assertEqual(mod.marker_lines(body), [self.GOOD])

    def test_body_without_marker_yields_nothing(self) -> None:
        self.assertEqual(mod.marker_lines("## 무엇을 했나\n표시가 없다."), [])

    def test_empty_body_does_not_crash(self) -> None:
        self.assertEqual(mod.marker_lines(""), [])

    def test_kind_is_read_from_the_line(self) -> None:
        self.assertEqual(mod.kind_of_line(self.GOOD), "decision:input")

    def test_line_without_a_kind_is_caught(self) -> None:
        """🔬 음성 — 종류가 없으면 `None` 이어야 한다. 아니면 긴급도를 못 가린다."""
        self.assertIsNone(mod.kind_of_line("회부: 뭔가 물었다 → 답: 응"))

    def test_summarise_counts_kinds_and_gaps(self) -> None:
        marks = [
            ("standards", 1, self.GOOD),
            ("standards", 2, "회부: decision:approval — 지울까 → 답: 그래"),   # 채널 없음
            ("workflows", 3, "회부: 종류를 안 적었다 → 답: 응 (채널: 대화)"),   # 종류 없음
        ]
        counts = mod.summarise_marks(marks)
        self.assertEqual(counts["marks"], 3)
        self.assertEqual(counts["unkinded"], 1)
        self.assertEqual(counts["no_channel"], 1)
        self.assertEqual(counts["decision:input"], 1)
        self.assertEqual(counts["decision:approval"], 1)

    def test_needs_simpler_in_a_marker_line_is_counted(self) -> None:
        marks = [("standards", 1, f"{self.GOOD} {mod.RESIMPLE}")]
        self.assertEqual(mod.summarise_marks(marks)["resimple"], 1)

    def test_empty_marks_do_not_crash(self) -> None:
        self.assertEqual(mod.summarise_marks([])["marks"], 0)

    def test_only_merged_prs_are_counted(self) -> None:
        """🔴 닫힌 채 버려진 PR 의 본문은 결정이 아니다. 소스가 `--state merged` 여야 한다."""
        source = Path(mod.__file__).read_text(encoding="utf-8")
        self.assertIn('"--state", "merged"', source)


class TheMeansChangeIsRecordedHonestly(unittest.TestCase):
    """🔴 2026-08-29 의 변경은 **네 축 다** 강해졌다. 2026-09-01 의 변경은 **셋만** 그렇다.

    그걸 *"이번에도 강화다"* 로 적으면 §판정 기준의 *"결과를 보고 기준을 옮기지 않는다"* 를
    말로만 지키는 것이 된다. **작업량이 줄어든다는 사실이 문서에 있어야 한다.**
    """

    def test_the_doc_admits_the_cost_axis_gets_cheaper(self) -> None:
        doc = mod.__doc__ or ""
        self.assertIn("작업량", doc)
        self.assertIn("줄어든다", doc, "작업량이 줄어든다는 것을 문서가 인정해야 한다")

    def test_the_doc_says_which_number_settles_it(self) -> None:
        """완화인지 아닌지는 **눈금이 답한다** — 그 판정 방법이 문서에 있어야 한다."""
        doc = mod.__doc__ or ""
        self.assertIn("분모가 안 늘면", doc)

    def test_the_issue_means_is_not_removed(self) -> None:
        self.assertIn("이슈 수단을 걷어내지 않는다", mod.__doc__ or "")
