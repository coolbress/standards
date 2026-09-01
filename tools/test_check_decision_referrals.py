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


class ExamplesInsideFencesAreNotReferrals(unittest.TestCase):
    """🔴 실물에서 물린 결함 — 이 도구가 **자기 사용법 예시를 회부로 셌다.**

    형식을 설명하는 PR 마다 분모가 부푼다. 그러면 `referrals_total` 이 *행동* 이 아니라
    *문서를 몇 번 썼나* 를 재게 되고, **계기가 재겠다던 것을 안 재는 것**이 된다.
    """

    BODY = (
        "회부: decision:input — 진짜로 물었다 → 답: 그래 (채널: 대화)\n"
        "\n"
        "형식은 이렇다:\n"
        "```\n"
        "회부: decision:input — <물음> → 답: <답> (채널: 대화)\n"
        "```\n"
    )

    def test_only_the_real_referral_is_counted(self) -> None:
        lines = mod.marker_lines(self.BODY)
        self.assertEqual(len(lines), 1)
        self.assertIn("진짜로 물었다", lines[0])

    def test_a_body_that_is_only_an_example_counts_zero(self) -> None:
        """🔬 음성 — 예시밖에 없는 본문은 **0건**이어야 한다."""
        only_example = "```\n회부: decision:input — <물음> → 답: <답>\n```\n"
        self.assertEqual(mod.marker_lines(only_example), [])

    def test_language_tagged_fence_also_counts_as_a_fence(self) -> None:
        body = "```text\n회부: decision:input — 예시\n```\n"
        self.assertEqual(mod.marker_lines(body), [])


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

    def test_p2_prose_mention_is_not_a_referral(self) -> None:
        """🔬 음성 — 줄 가운데의 언급은 회부가 아니다."""
        prose = "이번 PR 은 회부: 표시를 검사한다\n"
        self.assertEqual(mod.marker_lines(prose), [])

    def test_p2_line_head_with_a_list_bullet_still_counts(self) -> None:
        """목록으로 여러 건 적는 것은 정상 사용이다 — 그것까지 버리면 과잉이다."""
        body = "- 회부: decision:input — 물었다 → 답: 응 (채널: 대화)\n"
        self.assertEqual(len(mod.marker_lines(body)), 1)

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
        self.assertEqual(mod.unbridged_marks(marks, "결정은 #224 에서 오갔다"), [])
        self.assertEqual(mod.unbridged_marks(marks, ".../pull/224 참조"), [])

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

    def test_p2_tilde_fence_is_a_fence(self) -> None:
        """🔬 음성 — 마크다운은 물결 펜스도 쓴다."""
        self.assertEqual(mod.marker_lines("~~~text\n회부: decision:input — 예시\n~~~\n"), [])

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
    def test_indented_code_block_is_not_a_marker(self) -> None:
        """🔬 음성 — 마크다운은 **4칸 들여쓰기도 코드블록**이다. 펜스만 막아선 부족했다."""
        body = "형식은 이렇다:\n\n    회부: decision:input — <물음> → 답: <답> (채널: 대화)\n"
        self.assertEqual(mod.marker_lines(body), [])

    def test_tab_indented_example_is_not_a_marker(self) -> None:
        self.assertEqual(mod.marker_lines("\t회부: decision:input — 예시 → 답: 응"), [])

    def test_a_real_marker_at_the_line_head_still_reads(self) -> None:
        body = "회부: decision:input — 진짜 → 답: 응 (채널: 대화)\n"
        self.assertEqual(len(mod.marker_lines(body)), 1)

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
    def test_example_inside_an_html_comment_is_not_a_marker(self) -> None:
        """🔴 이 저장소의 PR 템플릿이 실제로 HTML 주석으로 안내한다 — 거기 예시를 넣으면
        **머지되는 PR 마다** 분모가 부푼다."""
        body = ("<!--\n회부: decision:input — <물음> → 답: <답> (채널: 대화)\n-->\n"
                "회부: decision:input — 진짜 → 답: 응 (채널: 대화)\n")
        lines = mod.marker_lines(body)
        self.assertEqual(len(lines), 1)
        self.assertIn("진짜", lines[0])

    def test_single_line_html_comment_is_stripped(self) -> None:
        self.assertEqual(mod.marker_lines("<!-- 회부: decision:input — 예시 → 답: 응 -->"), [])

    def test_channel_may_contain_parentheses(self) -> None:
        """🔬 `rfind(\"(\")` 는 안쪽 괄호를 집는다 — 바깥 괄호를 찾아야 한다."""
        f = mod.parse_marker("회부: decision:input — 물었다 → 답: 예 (채널: Slack (#ops))")
        self.assertEqual(f["channel"], "Slack (#ops)")
        self.assertTrue(f["answered"])

    def test_no_meta_field_still_parses(self) -> None:
        f = mod.parse_marker("회부: decision:input — 물었다 → 답: 예")
        self.assertEqual(f["channel"], "")
        self.assertTrue(f["answered"])
