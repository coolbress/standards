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
    def _issue(state: str, comments: int = 0, resimple: bool = False,
               body: str = "채널: 대화") -> dict[str, object]:
        return {
            "state": state,
            "comments": [{"body": body} for _ in range(comments)],
            "labels": ([{"name": mod.RESIMPLE}] if resimple else []) + [{"name": mod.LABEL}],
        }

    def test_closed_with_an_answer_comment_counts_as_answered(self) -> None:
        rows = [("standards", self._issue("CLOSED", comments=2))]
        self.assertEqual(mod.summarise(rows)["answered"], 1)

    def test_progress_report_alone_is_not_an_answer(self) -> None:
        """🔴 **코멘트가 있다 ≠ 답이 왔다.** 실측에서 그 코멘트들은 진행 보고였다.

        진행 보고 하나로 ⓐ 의 *성공* 이 되면 계기가 재겠다던 것을 안 재는 것이다
        (제3자 리뷰 8회차 · 2026-09-01). 답은 **채널을 적은 코멘트**다.
        """
        rows = [("standards", self._issue("CLOSED", comments=1, body="진행 중입니다"))]
        got = mod.summarise(rows)
        self.assertEqual(got["answered"], 0)
        self.assertEqual(got["incomplete"], 1, "답 없는 회부가 ⓐ 분자에서 빠져야 한다")

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
        self.assertEqual(mod.unbridged(rows, "…를 standards#141 에서 정했다…"), [])

    def test_closed_referral_absent_from_records_is_caught(self) -> None:
        rows = [("standards", {"state": "CLOSED", "number": 999, "labels": [], "comments": []})]
        self.assertEqual(mod.unbridged(rows, "관계 없는 본문"), [("standards", 999)])

    def test_open_referral_needs_no_record_yet(self) -> None:
        """아직 안 정해진 것에 기록을 요구하면 검사가 소음이 된다."""
        rows = [("standards", {"state": "OPEN", "number": 999, "labels": [], "comments": []})]
        self.assertEqual(mod.unbridged(rows, ""), [])

    def test_issue_url_form_also_counts(self) -> None:
        rows = [("standards", {"state": "CLOSED", "number": 141, "labels": [], "comments": []})]
        self.assertEqual(mod.unbridged(rows, "…https://github.com/coolbress/standards/issues/141 참조…"), [])

    def test_record_dirs_are_committed_ones(self) -> None:
        self.assertEqual(set(mod.RECORD_DIRS), {"direction", "audit"})


class PrBodyMarkerIsTheSecondMeans(unittest.TestCase):
    """2026-09-01 · `GAPS` R5-37 ⓑ — PR 본문의 `회부:` 표시를 센다.

    🔴 **음성 시험이 핵심이다.** 표시만 있으면 통과시키면 계기가 아무것도 안 재게 된다 —
    종류가 없는 줄과 채널이 없는 줄이 **각각 잡혀야** 눈금이 뜻을 갖는다.
    """

    GOOD = "회부: decision:input — 어휘를 A 로 갈까 B 로 갈까 → 답: A (채널: 대화)"

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

    def test_needs_simpler_in_the_meta_field_is_counted(self) -> None:
        """재요청은 **메타 칸**(끝 괄호) 안에 적는다 — 물음에 쓴 것과 갈라야 한다."""
        line = f"회부: decision:input — 물었다 → 답: 응 (채널: 대화 · {mod.RESIMPLE})"
        self.assertEqual(mod.summarise_marks([("standards", 1, line)])["resimple"], 1)

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


class ThirdPartyReviewFindings20260901(unittest.TestCase):
    """제3자 리뷰가 문 셋. **셋 다 계기가 재겠다던 것을 안 재게 만드는 결함**이었다."""

    def test_p1_pr_re_requests_reach_the_reported_metric(self) -> None:
        """P1 — PR 표시의 `needs-simpler` 가 ⓑ 에서 사라지면 **사전등록 지표가 조용히 초록**이 된다.

        분모(`referrals_total`)는 올라가는데 ⓑ 는 안 올라가는 조합이 가능해선 안 된다.
        """
        r = mod.rates({"closed": 1, "resimple": 1, "answered": 1, "incomplete": 1},
                      {"marks": 1, "resimple": 1, "incomplete": 1})
        self.assertEqual(r["b_total"], 2, "ⓑ 가 두 수단을 합치지 않는다")
        source = Path(mod.__file__).read_text(encoding="utf-8")
        self.assertIn("resimple_total=", source, "ⓑ 합산 지표가 METRIC 에 없다")
        self.assertIn("pr_resimple=", source, "PR 쪽 ⓑ 가 METRIC 에 없다")

    def test_p2_unreadable_source_is_not_zero(self) -> None:
        """P2 fail-open — 원천을 못 읽으면 **0 이 아니라 실패**여야 한다.

        🔴 **소스에 문구가 있는지로 재지 않는다.** 처음엔 그렇게 썼는데 판정을 `if False:` 로
        죽여도 **문자열은 남아 시험이 초록이었다** — *실행되지 않은 경로의 초록은 증거가 아니다.*
        그래서 **`gh` 를 못 찾게 만든 채 도구를 실제로 돌린다**(네트워크는 안 탄다 — 애초에 못 부른다).
        """
        import os
        import subprocess
        import sys

        env = {**os.environ, "PATH": ""}
        out = subprocess.run([sys.executable, str(mod.__file__)],
                             capture_output=True, text=True, env=env, check=False)
        self.assertEqual(out.returncode, 1, f"못 읽었는데 실패로 안 끝났다:\n{out.stdout[-600:]}")
        self.assertIn("RESULT FAIL — 못 읽은 원천이 있다", out.stdout)
        self.assertIn("unreadable_sources=", out.stdout)

    def test_fetch_failure_is_recorded_not_swallowed(self) -> None:
        """🔬 실제로 부른다 — 존재하지 않는 명령이면 실패가 **기록**돼야 한다."""
        before = len(mod.FETCH_FAILURES)
        self.assertIsNone(mod._json(["gh-does-not-exist-r5-37", "--json", "x"]))
        self.assertEqual(len(mod.FETCH_FAILURES), before + 1)
        mod.FETCH_FAILURES.pop()


class SecondRoundReviewFindings20260901(unittest.TestCase):
    """제3자 리뷰 2회차가 문 다섯. 🔴 **첫 회차 수정이 만든 것도 있다** — 고치면서 새로 벌어진다."""

    def test_p1_pr_markers_need_a_committed_record(self) -> None:
        """P1 — **PR 본문은 저장소 밖이다.** 머지 뒤에도 고쳐지고 지워진다.

        *"머지 커밋에 인용된다"* 고 적었던 것이 **사실이 아니었다.** 이슈에 걸었던 다리를 PR 에도 건다.
        """
        marks = [("standards", 224, "회부: decision:input — 물었다 → 답: 응 (채널: 대화)")]
        self.assertEqual(mod.unbridged_marks(marks, "아무 인용도 없는 본문"), [("standards", 224)])
        self.assertEqual(mod.unbridged_marks(marks, "결정은 standards#224 에서 오갔다"), [])
        self.assertEqual(mod.unbridged_marks(marks, "https://github.com/coolbress/standards/pull/224 참조"), [])

    def test_p1_the_wrong_claim_is_corrected_everywhere(self) -> None:
        """🔴 한 곳만 고치면 요약이 갈린다 — 네 곳이 같은 말을 해야 한다."""
        doc = mod.__doc__ or ""
        self.assertNotIn("머지 커밋에 인용된다** — 이슈보다 찾기 쉽다", doc)
        for path in ("direction/04-the-plan.md", "audit/GAPS.ko.md", "NEXT.md"):
            text = (mod.ROOT / path).read_text(encoding="utf-8")
            self.assertNotIn("PR 본문은 **리뷰를 거치고 머지 커밋에 인용된다**", text, path)

    def test_p2_alpha_rate_counts_both_paths(self) -> None:
        """P2 — ⓐ 를 이슈만으로 내면 1/1(100%) 인데 실제로는 1/2(50%) 다. **행동으로 잰다.**"""
        counts = {"closed": 1, "resimple": 0, "answered": 1, "incomplete": 0}
        mcounts = {"marks": 1, "resimple": 1, "incomplete": 1}
        r = mod.rates(counts, mcounts)
        self.assertEqual((r["a_denom"], r["a_numer"]), (2, 1))
        self.assertEqual(r["b_total"], 1, "ⓑ 가 PR 표시의 재요청을 안 세고 있다")

    def test_p2_marker_without_an_answer_is_flagged(self) -> None:
        """P2 — 물음만 적힌 표시는 **회부의 절반**이다. 분모엔 넣되 따로 센다."""
        marks = [("standards", 1, "회부: decision:input — 물었다 (채널: 대화)"),
                 ("standards", 2, "회부: decision:input — 물었다 → 답: 응 (채널: 대화)")]
        counts = mod.summarise_marks(marks)
        self.assertEqual(counts["unanswered"], 1)
        self.assertEqual(counts["marks"], 2, "분모에서는 빼지 않는다 — 회부는 일어났다")

    def test_p2_hitting_the_fetch_cap_is_a_failure(self) -> None:
        """P2 — `standards` 는 **이미 머지된 PR 208건**이라 200 상한을 넘어 있었다.

        상한에 닿으면 조용히 잘려 `referrals_total` 이 줄고 **예전 관측이 사라진다.**
        """
        source = Path(mod.__file__).read_text(encoding="utf-8")
        self.assertIn("FETCH_LIMIT", source)
        self.assertIn("상한", source)
        self.assertNotIn('"--limit", "200"', source, "200 상한이 아직 남아 있다")
        self.assertGreaterEqual(mod.FETCH_LIMIT, 1000)


class KindMustComeFromItsOwnField(unittest.TestCase):
    """🔴 필수 칸을 **물음 텍스트가 채울 수 있으면** 그건 필수 칸이 아니다 (제3자 리뷰 P2)."""

    def test_kind_in_the_question_does_not_satisfy_the_field(self) -> None:
        line = "회부: 이 요청을 decision:approval 로 분류할까 → 답: 예 (채널: 대화)"
        self.assertIsNone(mod.kind_of_line(line))
        self.assertEqual(mod.summarise_marks([("s", 1, line)])["unkinded"], 1)

    def test_the_field_itself_still_reads(self) -> None:
        self.assertEqual(
            mod.kind_of_line("회부: decision:escalation — 막혔다 → 답: 내가 한다 (채널: 대화)"),
            "decision:escalation")


class IncompleteRecordsAreNotSuccesses(unittest.TestCase):
    """🔴 답이 안 적힌 회부가 ⓐ 의 **성공**으로 세어지면 비율이 좋아진다 (제3자 리뷰 P2)."""

    def test_unanswered_marker_counts_as_incomplete(self) -> None:
        marks = [("s", 1, "회부: decision:input — 물었다 (채널: 대화)")]
        self.assertEqual(mod.summarise_marks(marks)["incomplete"], 1)

    def test_both_flaws_on_one_line_are_counted_once(self) -> None:
        """🔬 재요청이면서 답도 없는 표시를 **두 번 빼면** 분자가 음수로 간다."""
        marks = [("s", 1, f"회부: decision:input — 물었다 {mod.RESIMPLE}")]
        self.assertEqual(mod.summarise_marks(marks)["incomplete"], 1)

    def test_a_complete_marker_is_not_incomplete(self) -> None:
        marks = [("s", 1, "회부: decision:input — 물었다 → 답: 응 (채널: 대화)")]
        self.assertEqual(mod.summarise_marks(marks)["incomplete"], 0)

    def test_alpha_numerator_subtracts_incomplete_records(self) -> None:
        """답 없는 표시 하나뿐이면 ⓐ 는 **1건 중 0건**이어야 한다 — 100% 가 아니다."""
        r = mod.rates({"closed": 0, "resimple": 0, "answered": 0, "incomplete": 0},
                      {"marks": 1, "resimple": 0, "incomplete": 1})
        self.assertEqual((r["a_denom"], r["a_numer"]), (1, 0))

    def test_alpha_numerator_subtracts_closed_issues_without_an_answer(self) -> None:
        """🔬 이슈 쪽도 같다 — 닫혔는데 답이 없는 회부가 성공으로 세어지면 안 된다."""
        r = mod.rates({"closed": 1, "resimple": 0, "answered": 0, "incomplete": 1},
                      {"marks": 0, "resimple": 0, "incomplete": 0})
        self.assertEqual((r["a_denom"], r["a_numer"]), (1, 0))

    def test_a_fully_recorded_referral_counts_as_success(self) -> None:
        """🔬 음성의 반대편 — 제대로 적힌 회부까지 깎으면 계기가 쓸모없다."""
        r = mod.rates({"closed": 1, "resimple": 0, "answered": 1, "incomplete": 0},
                      {"marks": 1, "resimple": 0, "incomplete": 0})
        self.assertEqual((r["a_denom"], r["a_numer"]), (2, 2))


class FourthRoundReviewFindings20260901(unittest.TestCase):
    """3회차 수정이 만든 것 셋. 🔴 **고치면서 새로 벌어진다** — 그래서 매번 다시 읽는다."""

    def test_issue_side_is_not_subtracted_twice(self) -> None:
        """닫힌 회부 하나가 재요청이면서 답도 없으면 `1-1-1 = -1` 이라 **-100%** 가 찍혔다."""
        rows = [("s", {"state": "CLOSED", "labels": [{"name": mod.RESIMPLE}], "comments": []})]
        counts = mod.summarise(rows)
        self.assertEqual(counts["incomplete"], 1, "합집합으로 한 번만 세야 한다")
        r = mod.rates(counts, {"marks": 0, "resimple": 0, "incomplete": 0})
        self.assertEqual((r["a_denom"], r["a_numer"]), (1, 0))
        self.assertGreaterEqual(r["a_numer"], 0, "분자가 음수로 가면 안 된다")

    def test_answer_must_sit_after_the_arrow(self) -> None:
        """🔬 물음 안의 `답:` 은 답이 아니다 — 종류 칸에서 물었던 것과 같은 결함."""
        line = "회부: decision:input — 출력에 답: 접두사를 넣을까 (채널: 대화)"
        counts = mod.summarise_marks([("s", 1, line)])
        self.assertEqual(counts["unanswered"], 1)
        self.assertEqual(counts["incomplete"], 1)

    def test_a_real_answer_still_reads(self) -> None:
        line = "회부: decision:input — 물었다 → 답: 응 (채널: 대화)"
        self.assertEqual(mod.summarise_marks([("s", 1, line)])["unanswered"], 0)

    def test_report_is_gated_on_either_source(self) -> None:
        """이슈 0건 + PR 표시 1건이면 `referrals_total=1` 인데 *"회부 0건"* 이라고 말했다."""
        source = Path(mod.__file__).read_text(encoding="utf-8")
        self.assertIn('if total or mcounts["marks"]:', source)


class FifthRoundReviewFindings20260901(unittest.TestCase):

    def test_the_bridge_admits_what_it_cannot_protect(self) -> None:
        """🔴 다리가 **지워진 표시는 못 잡는다** — 그걸 적어두지 않으면 과신한다."""
        doc = mod.unbridged_marks.__doc__ or ""
        self.assertIn("조용히 줄어드는데", doc)
        self.assertIn("R5-47", doc)


class SixthRoundReviewFindings20260901(unittest.TestCase):
    """🔴 같은 결함을 **네 번** 물렸다(종류 · 답 · 채널 · needs-simpler).

    칸마다 때우는 대신 `parse_marker` 로 **한 번 쪼갠다** — 다섯 번째 필드가 생겨도 같은 구멍이 안 난다.
    """

    def test_channel_is_read_only_from_the_meta_field(self) -> None:
        line = "회부: decision:input — 출력에 채널: 접두사를 넣을까 → 답: 예"
        self.assertEqual(mod.summarise_marks([("s", 1, line)])["no_channel"], 1)

    def test_needs_simpler_in_the_question_is_not_a_re_request(self) -> None:
        line = f"회부: decision:input — {mod.RESIMPLE} 라벨을 붙일까 → 답: 아니오 (채널: 대화)"
        counts = mod.summarise_marks([("s", 1, line)])
        self.assertEqual(counts["resimple"], 0, "물음에 쓴 라벨 이름이 재요청으로 세어졌다")
        self.assertEqual(counts["incomplete"], 0)

    def test_a_fully_formed_marker_parses_every_field(self) -> None:
        f = mod.parse_marker("회부: decision:approval — 지울까 → 답: 그래 (채널: 대화)")
        self.assertEqual(f["kind"], "decision:approval")
        self.assertTrue(f["answered"])
        self.assertEqual(f["channel"], "대화")
        self.assertFalse(f["resimple"])

    def test_parentheses_in_the_question_do_not_break_the_meta_field(self) -> None:
        """🔬 실물이 그렇다 — #224 의 표시에 물음 안 괄호가 둘 있다."""
        f = mod.parse_marker(
            "회부: decision:input — ⓐ(이슈 코멘트)로 갈까 ⓑ(PR 표시)로 갈까 → 답: ⓑ (채널: 대화)")
        self.assertEqual(f["channel"], "대화")
        self.assertTrue(f["answered"])

    def test_an_empty_answer_is_not_an_answer(self) -> None:
        self.assertFalse(mod.parse_marker("회부: decision:input — 물었다 → 답:  (채널: 대화)")["answered"])


class SeventhRoundReviewFindings20260901(unittest.TestCase):

    def test_channel_may_contain_parentheses(self) -> None:
        """🔬 `rfind(\"(\")` 는 안쪽 괄호를 집는다 — 바깥 괄호를 찾아야 한다."""
        f = mod.parse_marker("회부: decision:input — 물었다 → 답: 예 (채널: Slack (#ops))")
        self.assertEqual(f["channel"], "Slack (#ops)")
        self.assertTrue(f["answered"])

    def test_no_meta_field_still_parses(self) -> None:
        f = mod.parse_marker("회부: decision:input — 물었다 → 답: 예")
        self.assertEqual(f["channel"], "")
        self.assertTrue(f["answered"])


class EighthRoundReviewFindings20260901(unittest.TestCase):

    def test_empty_channel_entry_is_not_a_channel(self) -> None:
        """`(채널: · needs-simpler)` 가 채널 `"· needs-simpler"` 로 잡혀 조용히 통과했다."""
        f = mod.parse_marker(f"회부: decision:input — 물었다 → 답: 예 (채널: · {mod.RESIMPLE})")
        self.assertEqual(f["channel"], "")
        self.assertTrue(f["resimple"])

    def test_kind_distribution_includes_pr_markers(self) -> None:
        source = Path(mod.__file__).read_text(encoding="utf-8")
        self.assertIn("counts[kind] + mcounts[kind]", source,
                      "종류 분포가 PR 표시를 안 합친다")


class NinthRoundReviewFindings20260901(unittest.TestCase):

    def test_pr_channel_gap_reaches_the_metric_line(self) -> None:
        """사람이 읽는 절은 잡는데 METRIC 에 없으면 **수집기는 0 으로 기록한다.**"""
        source = Path(mod.__file__).read_text(encoding="utf-8")
        self.assertIn("pr_no_channel=", source)


class TenthRoundReviewFindings20260901(unittest.TestCase):

    def test_progress_comment_mentioning_the_word_is_not_an_answer(self) -> None:
        """🔬 *"답변에는 채널: 항목도 적어야 합니다"* 는 진행 보고이지 답이 아니다.

        🔴 **호출부까지 잰다.** 처음엔 `_has_channel_field` 만 직접 봐서, `has_channel` 을
        부분문자열로 되돌리는 변이를 **못 잡았다** — 시험이 실제 경로를 안 탔다.
        """
        self.assertFalse(mod._has_channel_field("진행 중 — 답변에는 채널: 항목도 적어야 합니다"))
        rows = [("standards", {"state": "CLOSED", "labels": [{"name": mod.LABEL}],
                               "comments": [{"body": "진행 중 — 답변에는 채널: 항목도 적어야 합니다"}]})]
        got = mod.summarise(rows)
        self.assertEqual(got["answered"], 0, "진행 보고가 답으로 세어졌다")
        self.assertEqual(got["no_channel"], 1)
        self.assertEqual(got["incomplete"], 1)

    def test_a_real_answer_comment_still_reads(self) -> None:
        """🔬 실물 그대로 — 닫힌 회부 넷의 답 코멘트가 이 꼴이다."""
        real = "## ✅ 처리 — ⓑ (안 넣습니다)\n\n**채널: 대화(Claude Code 세션)** — 소유자 …"
        self.assertTrue(mod._has_channel_field(real))

    def test_plain_channel_line_reads_too(self) -> None:
        self.assertTrue(mod._has_channel_field("채널: 대화"))


class PostMergeReviewFindings20260901(unittest.TestCase):
    """🔴 **머지 뒤에 온 것과 내가 놓친 것 다섯.** `#224` 의 findings 는 20건이 아니라 **32건**이었다 —
    내 요약이 원자료보다 작았다. 이 저장소의 대표 결함을 내가 그대로 했다."""

    def test_bare_number_from_another_repo_does_not_bridge(self) -> None:
        """네 저장소가 번호를 공유한다 — `workflows#224` 가 `standards#224` 인용으로 통과했다."""
        marks = [("workflows", 224, "회부: decision:input — 물었다 → 답: 응 (채널: 대화)")]
        self.assertEqual(mod.unbridged_marks(marks, "standards#224 에서 정했다"),
                         [("workflows", 224)])
        self.assertEqual(mod.unbridged_marks(marks, "workflows#224 에서 정했다"), [])

    def test_quoted_answer_delimiter_does_not_fill_the_answer(self) -> None:
        """형식을 논하는 물음이 답 칸을 채웠다."""
        line = "회부: decision:input — `→ 답:` 표기를 쓸까 (채널: 대화)"
        self.assertFalse(mod.parse_marker(line)["answered"])

    def test_a_real_answer_outside_backticks_still_reads(self) -> None:
        line = "회부: decision:input — `→ 답:` 표기를 쓸까 → 답: 아니오 (채널: 대화)"
        f = mod.parse_marker(line)
        self.assertTrue(f["answered"])
        self.assertEqual(f["channel"], "대화")

class ReviewFindingsOn226(unittest.TestCase):
    """`#226` 이 문 넷. 🔴 **셋이 분모를 *줄이는* 쪽**이라 오탐보다 나쁘다."""

    def test_marker_before_a_comment_opener_survives(self) -> None:
        body = "회부: decision:input — 진짜 → 답: 응 (채널: 대화) <!-- 보충 설명\n계속\n-->\n"
        lines = mod.marker_lines(body)
        self.assertEqual(len(lines), 1, "표시 뒤에 주석이 열리면 표시까지 버렸다")
        self.assertIn("진짜", lines[0])

    def test_double_backtick_span_is_masked_whole(self) -> None:
        """한 글자씩 짝지으면 ``` ``→ 답:`` ``` 의 가운데가 안 가려진다."""
        line = "회부: decision:input — ``→ 답:`` 표기를 쓸까 (채널: 대화)"
        self.assertFalse(mod.parse_marker(line)["answered"])

    def test_cited_matches_at_a_number_boundary(self) -> None:
        """`standards#224` 가 `standards#22` 의 인용으로 통과했다 — 오른쪽 경계."""
        self.assertFalse(mod.cited("standards", 22, "standards#224 에서 정했다"))
        self.assertTrue(mod.cited("standards", 224, "standards#224 에서 정했다"))
        self.assertTrue(mod.cited("standards", 22, "standards#22 에서 정했다"))

    def test_another_org_reference_does_not_count(self) -> None:
        """🔴 왼쪽 경계 — **다른 조직의** `otherorg/standards#22` 는 우리 인용이 아니다."""
        self.assertFalse(mod.cited("standards", 22, "otherorg/standards#22 를 봐라"))
        self.assertFalse(mod.cited("standards", 22, "elsewhere/coolbress/standards/pull/22"))
        self.assertFalse(mod.cited("standards", 22, "gitlab.com/coolbress/standards/pull/22"))

    def test_our_own_url_form_still_counts(self) -> None:
        """🔬 반대편 — 우리 URL 은 여전히 통과해야 한다(안 그러면 다리가 전부 빨개진다)."""
        self.assertTrue(mod.cited(
            "standards", 22, "https://github.com/coolbress/standards/pull/22 참조"))


class HostMustBeAnchored(unittest.TestCase):
    """🔴 `github.com` 을 아무 데서나 찾으면 **다른 호스트의 경로**도 우리 인용이 된다."""

    def test_a_path_that_merely_contains_the_hostname_does_not_count(self) -> None:
        self.assertFalse(mod.cited(
            "standards", 22, "https://example.com/github.com/coolbress/standards/pull/22"))

    def test_the_real_url_still_counts(self) -> None:
        self.assertTrue(mod.cited(
            "standards", 22, "https://github.com/coolbress/standards/pull/22"))


class QualifiedLocalReferencesCount(unittest.TestCase):
    def test_our_own_owner_qualified_form_is_accepted(self) -> None:
        self.assertTrue(mod.cited("standards", 22, "coolbress/standards#22 에서 정했다"))

    def test_another_owner_is_still_rejected(self) -> None:
        self.assertFalse(mod.cited("standards", 22, "otherorg/standards#22 를 봐라"))
        self.assertFalse(mod.cited("standards", 22, "x/coolbress/standards#22"))


class BacktickRunsPairByLength(unittest.TestCase):
    def test_a_longer_run_inside_does_not_close_a_shorter_span(self) -> None:
        """🔴 위치 단위로 찾으면 **더 긴 묶음의 안쪽**을 닫는 것으로 읽는다."""
        line = "회부: decision:input — `foo`` → 답: bar` 표기를 쓸까 (채널: 대화)"
        self.assertFalse(mod.parse_marker(line)["answered"])

    def test_double_run_pairs_with_double_run(self) -> None:
        line = "회부: decision:input — ``→ 답:`` 표기를 쓸까 (채널: 대화)"
        self.assertFalse(mod.parse_marker(line)["answered"])

    def test_an_answer_outside_any_span_still_reads(self) -> None:
        """🔬 반대편 — 인용 밖의 진짜 답은 계속 읽혀야 한다."""
        line = "회부: decision:input — ``표기`` 를 쓸까 → 답: 아니오 (채널: 대화)"
        f = mod.parse_marker(line)
        self.assertTrue(f["answered"])
        self.assertEqual(f["channel"], "대화")


class UnmatchedRunDoesNotStopTheScan(unittest.TestCase):
    def test_a_later_span_is_still_masked(self) -> None:
        """🔴 짝 없는 묶음에서 멈추면 **그 뒤의 멀쩡한 인용이 통째로 안 가려진다.**"""
        line = "회부: decision:input — ` 짝없음 ``→ 답:`` 표기를 쓸까 (채널: 대화)"
        self.assertFalse(mod.parse_marker(line)["answered"])

    def test_an_answer_after_an_unmatched_run_still_reads(self) -> None:
        """🔬 반대편 — 짝 없는 묶음 뒤의 **진짜** 답은 계속 읽혀야 한다."""
        line = "회부: decision:input — ` 짝없음 → 답: 진짜 (채널: 대화)"
        self.assertTrue(mod.parse_marker(line)["answered"])


class MarkersLiveOnlyInThePreamble(unittest.TestCase):
    """🔵 **자리를 좁혀서 파서를 걷어냈다** (2026-09-01).

    본문 전체를 훑으니 예시를 걸러내려고 펜스·들여쓴 코드·HTML 주석을 차례로 때웠고,
    제3자 리뷰가 **그 가장자리로만 9건**을 물었다. 가장자리는 끝이 없다.
    🔴 이건 이 세션에서 배운 것의 한 층 위다 — *표시가 아무 데나 있을 수 있으면
    아무 데나 파싱해야 한다.* **규칙은 둘뿐이다: 첫 `##` 앞 · 열 0.**
    """

    REAL = "회부: decision:input — 진짜 → 답: 응 (채널: 대화)"

    def test_a_marker_in_the_preamble_counts(self) -> None:
        body = f"> 스택 안내\n\n{self.REAL}\n\n## 왜\n어쩌고\n"
        self.assertEqual(mod.marker_lines(body), [self.REAL])

    def test_anything_after_the_first_heading_is_ignored(self) -> None:
        """🔬 **설명·예시는 제목 아래에 산다** — 그래서 저절로 걸러진다."""
        body = f"{self.REAL}\n\n## 형식\n회부: decision:input — <물음> → 답: <답> (채널: 대화)\n"
        self.assertEqual(mod.marker_lines(body), [self.REAL])

    def test_a_fenced_example_under_a_heading_is_ignored_without_parsing(self) -> None:
        body = "## 형식\n```\n회부: decision:input — 예시 → 답: 응 (채널: 대화)\n```\n"
        self.assertEqual(mod.marker_lines(body), [])

    def test_an_indented_or_list_prefixed_line_is_not_a_marker(self) -> None:
        """🔴 **열 0 만** 인정한다 — 목록·들여쓰기를 받으면 다시 파싱이 필요해진다."""
        self.assertEqual(mod.marker_lines(f"  {self.REAL}\n"), [])
        self.assertEqual(mod.marker_lines(f"- {self.REAL}\n"), [])

    def test_a_mid_line_mention_is_not_a_marker(self) -> None:
        self.assertEqual(mod.marker_lines("이번 PR 은 회부: 표시를 검사한다\n"), [])

    def test_empty_body_does_not_crash(self) -> None:
        self.assertEqual(mod.marker_lines(""), [])

    def test_the_real_prs_would_still_be_counted(self) -> None:
        """🔬 실물 두 개(`#224`·`#227`)가 이 꼴이다 — 규칙을 좁히며 눈금을 깨지 않았다."""
        body = ("> 🔗 **#226 위에 쌓은 PR** (base = `docs/two-lessons`).\n\n"
                "회부: decision:approval — 어디까지 만들까 → 답: 계기만 (채널: 대화)\n\n## 왜\n")
        self.assertEqual(len(mod.marker_lines(body)), 1)


class HeadingBoundaryIsARealHeading(unittest.TestCase):
    REAL = "회부: decision:input — 진짜 → 답: 응 (채널: 대화)"

    def test_a_hash_run_without_space_is_not_a_heading(self) -> None:
        """🔴 `##not-a-heading` 에서 멈추면 **그 뒤의 진짜 표시가 사라진다.**"""
        body = f"##not-a-heading\n{self.REAL}\n\n## 무엇을 왜\n"
        self.assertEqual(mod.marker_lines(body), [self.REAL])

    def test_a_real_heading_still_stops(self) -> None:
        body = f"## 형식\n{self.REAL}\n"
        self.assertEqual(mod.marker_lines(body), [])

    def test_a_level_one_heading_also_stops(self) -> None:
        body = f"# 제목\n{self.REAL}\n"
        self.assertEqual(mod.marker_lines(body), [])


class UrlNeedsALeftBoundaryToo(unittest.TestCase):
    def test_a_glued_prefix_does_not_count(self) -> None:
        self.assertFalse(mod.cited(
            "standards", 22, "xhttps://github.com/coolbress/standards/issues/22"))

    def test_the_plain_url_still_counts(self) -> None:
        self.assertTrue(mod.cited(
            "standards", 22, "보라: https://github.com/coolbress/standards/issues/22"))

    def test_a_markdown_link_still_counts(self) -> None:
        """🔬 실물이 이 꼴이다 — `[#142](https://github.com/...)`."""
        self.assertTrue(mod.cited(
            "standards", 142, "[#142](https://github.com/coolbress/standards/issues/142)"))


class HeadingsInsideCommentsAreIgnored(unittest.TestCase):
    """🔴 이 저장소의 `PULL_REQUEST_TEMPLATE.md` 가 **주석 블록으로 시작**한다 — 실물 근거다.

    ⚠️ **주석 상태 하나만** 들고 다닌다. 걷어낸 파서(펜스·들여쓰기·목록)로 돌아가지 않는다.
    """

    REAL = "회부: decision:input — 진짜 → 답: 응 (채널: 대화)"

    def test_a_commented_out_heading_does_not_stop_the_scan(self) -> None:
        body = f"<!-- 안내\n# 옛 제목\n-->\n{self.REAL}\n\n## 무엇을 왜\n"
        self.assertEqual(mod.marker_lines(body), [self.REAL])

    def test_a_marker_inside_a_comment_is_not_counted(self) -> None:
        """🔬 음성 — 주석 안의 예시는 여전히 안 세어진다."""
        body = f"<!--\n회부: decision:input — 예시 → 답: 응 (채널: 대화)\n-->\n{self.REAL}\n"
        self.assertEqual(mod.marker_lines(body), [self.REAL])

    def test_a_single_line_comment_does_not_swallow_the_rest(self) -> None:
        body = f"<!-- 한 줄 -->\n{self.REAL}\n"
        self.assertEqual(mod.marker_lines(body), [self.REAL])

    def test_a_real_heading_after_the_comment_still_stops(self) -> None:
        body = f"<!-- 안내 -->\n## 형식\n{self.REAL}\n"
        self.assertEqual(mod.marker_lines(body), [])


class IndentedHeadingsAreHeadings(unittest.TestCase):
    def test_up_to_three_leading_spaces_still_stops(self) -> None:
        """마크다운은 선행 공백 3칸까지 제목으로 친다."""
        for pad in ("", " ", "  ", "   "):
            body = f"{pad}## 형식\n회부: decision:input — 예시 → 답: 응 (채널: 대화)\n"
            self.assertEqual(mod.marker_lines(body), [], f"pad={len(pad)}")

    def test_four_spaces_is_not_a_heading(self) -> None:
        """🔬 반대편 — 4칸부터는 코드블록이지 제목이 아니다."""
        real = "회부: decision:input — 진짜 → 답: 응 (채널: 대화)"
        self.assertEqual(mod.marker_lines(f"    ## 형식\n{real}\n"), [real])
