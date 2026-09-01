"""제3자 리뷰 계기의 **파싱·집계 규칙** 시험. 네트워크를 안 탄다.

🔴 순수 함수만 시험한다 — 네트워크를 타는 함수는 **음성 시험이 안 되고**,
통과만 하는 검사는 증명이 약하다(`check_purpose_sync`·`check_skill_firing` 에서 배운 것).
"""

from __future__ import annotations

import pathlib
import unittest

import check_review_signal as mod


def cmt(login: str, sev: str | None, path: str, commit: str = "c1") -> dict[str, object]:
    badge = f"![{sev} Badge](https://img.shields.io/badge/{sev}-orange?style=flat)" if sev else ""
    return {
        "user": {"login": login},
        "body": f"**{badge}  제목**\n\n본문",
        "path": path,
        "commit_id": commit,
    }


class Severity(unittest.TestCase):
    def test_reads_the_badge(self) -> None:
        self.assertEqual(mod.severity_of("**![P1 Badge](https://x) 제목**"), "P1")
        self.assertEqual(mod.severity_of("**![P0 Badge](https://x) 제목**"), "P0")

    def test_no_badge_is_unknown(self) -> None:
        self.assertEqual(mod.severity_of("그냥 댓글"), "?")
        self.assertEqual(mod.severity_of(""), "?")

    def test_first_badge_wins(self) -> None:
        # 한 댓글에 배지가 둘이면 앞엣것이 그 댓글의 것이다.
        self.assertEqual(mod.severity_of("![P2 Badge](x) ... ![P0 Badge](x)"), "P2")


class Reviewer(unittest.TestCase):
    def test_matches_case_insensitively(self) -> None:
        self.assertTrue(mod.is_reviewer("chatgpt-codex-connector[bot]"))
        self.assertTrue(mod.is_reviewer("ChatGPT-Codex-Connector[bot]"))

    def test_rejects_everyone_else(self) -> None:
        # 🔴 사람 댓글이나 다른 봇을 세면 신호비가 통째로 틀어진다.
        self.assertFalse(mod.is_reviewer("coolbress"))
        self.assertFalse(mod.is_reviewer("github-actions[bot]"))
        self.assertFalse(mod.is_reviewer(""))


class Tally(unittest.TestCase):
    def test_counts_by_severity(self) -> None:
        t = mod.tally([cmt(mod.REVIEWER, "P1", "a.py"), cmt(mod.REVIEWER, "P2", "b.py")], {})
        self.assertEqual(t["findings"], 2)
        self.assertEqual(t["sev_P1"], 1)
        self.assertEqual(t["sev_P2"], 1)

    def test_ignores_other_authors(self) -> None:
        t = mod.tally([cmt("coolbress", "P1", "a.py")], {})
        self.assertEqual(t["findings"], 0)

    def test_touched_after_needs_the_same_path(self) -> None:
        # 그 커밋 뒤에 **그 파일이** 바뀌어야 센다.
        t = mod.tally([cmt(mod.REVIEWER, "P1", "a.py")], {"c1": {"a.py"}})
        self.assertEqual(t["touched_after"], 1)
        self.assertEqual(t["touched_P1"], 1)

    def test_a_different_file_changing_does_not_count(self) -> None:
        # 🔴 여기가 대리지표의 경계다 — 다른 파일이 바뀐 것은 **반영이 아니다.**
        t = mod.tally([cmt(mod.REVIEWER, "P1", "a.py")], {"c1": {"b.py"}})
        self.assertEqual(t["touched_after"], 0)

    def test_no_later_commit_means_not_touched(self) -> None:
        t = mod.tally([cmt(mod.REVIEWER, "P1", "a.py")], {})
        self.assertEqual(t["touched_after"], 0)


class ItRefusesToDrawALine(unittest.TestCase):
    """🔴 **판정선을 상수로 박는 것을 막는다** — `R5-2` 에서 배운 것.

    표본이 쌓이기 전에 문턱을 그으면 *시험 데이터에서 읽은 θ* 가 된다.
    """

    def test_enough_is_a_discussion_trigger_not_a_gate(self) -> None:
        src = pathlib.Path(mod.__file__).read_text(encoding="utf-8")
        self.assertIn("판정선을 긋지 않는다", src)
        # 계기는 **항상 0 으로 끝난다** — 벽이 아니다.
        self.assertIn("RESULT INFO", src)
        self.assertNotIn("RESULT FAIL", src)


if __name__ == "__main__":
    unittest.main()


class MergedWithOpenFindings(unittest.TestCase):
    """🔴 **머지 head 에 달린 지적은 정의상 아무도 안 고쳤다** — 그 뒤 커밋이 없다.

    실측(2026-09-01): 두 저장소에서 **PR 11개 · 지적 18건**이 그 상태였다. 오늘 것은 꼬리였고
    `#211`(벽을 세운 PR)과 `workflows#66` 도 **P1 을 처분 기록 없이** 머지했다.
    """

    HEAD = "e" * 40
    OLD = "a" * 40

    def _pr(self, merged: bool = True) -> dict[str, object]:
        return {"merged_at": "2026-09-01T00:00:00Z" if merged else None,
                "head": {"sha": self.HEAD}}

    def test_finding_on_the_merge_head_is_counted(self) -> None:
        cs = [{"original_commit_id": self.HEAD, "commit_id": self.HEAD}]
        self.assertEqual(mod.merged_unaddressed(self._pr(), cs), 1)

    def test_finding_on_an_older_commit_is_not_counted(self) -> None:
        """🔬 음성 — 그 뒤 커밋이 있으니 고쳤을 수 있다. 판단하지 않는다."""
        cs = [{"original_commit_id": self.OLD, "commit_id": self.HEAD}]
        self.assertEqual(mod.merged_unaddressed(self._pr(), cs), 0)

    def test_open_pr_is_not_counted(self) -> None:
        """🔬 음성 — 아직 열린 PR 은 고칠 기회가 남았다. 세면 소음이다."""
        cs = [{"original_commit_id": self.HEAD, "commit_id": self.HEAD}]
        self.assertEqual(mod.merged_unaddressed(self._pr(merged=False), cs), 0)

    def test_commit_of_prefers_the_original(self) -> None:
        """🔴 `commit_id` 는 GitHub 이 head 로 옮긴다 — 그걸 쓰면 대리지표가 통째로 어긋난다."""
        self.assertEqual(
            mod.commit_of({"original_commit_id": self.OLD, "commit_id": self.HEAD}), self.OLD)

    def test_commit_of_falls_back_when_original_is_absent(self) -> None:
        self.assertEqual(mod.commit_of({"commit_id": self.HEAD}), self.HEAD)

    def test_it_is_an_instrument_not_a_wall(self) -> None:
        """*findings 로 안 막는다* 는 `IPW-020` 으로 사전등록된 결정이다."""
        source = pathlib.Path(mod.__file__).read_text(encoding="utf-8")
        self.assertIn("RESULT INFO", source)
        self.assertNotIn("RESULT FAIL", source)


class LookupKeyMustMatchTheMapKey(unittest.TestCase):
    """🔴 **같은 뿌리에 네 번째로 물린 자리.**

    지도는 `original_commit_id` 로 만들어놓고 조회를 `commit_id` 로 했다. GitHub 이 그 값을
    head 로 옮기므로 **전부 빗나가 `after` 가 늘 빈 집합**이었고 대리지표가 조용히 낮아졌다
    (실측: 고치니 44% → 58%). *한 곳을 고칠 때 **같은 값을 읽는 다른 줄** 을 안 봤다.*
    """

    OLD = "a" * 40
    HEAD = "e" * 40
    BOT = "chatgpt-codex-connector[bot]"

    def _comment(self) -> dict[str, object]:
        # 🔬 실물 그대로 — 옛 커밋에 달렸는데 `commit_id` 는 head 로 옮겨져 있다.
        return {"user": {"login": self.BOT}, "path": "tools/x.py",
                "original_commit_id": self.OLD, "commit_id": self.HEAD,
                "body": "**![P2 Badge](x) 어떤 지적**"}

    def test_touched_after_is_found_via_the_original_commit(self) -> None:
        got = mod.tally([self._comment()], {self.OLD: {"tools/x.py"}})
        self.assertEqual(got["touched_after"], 1,
                         "조회 키가 지도 키와 다르다 — 대리지표가 조용히 0 이 된다")

    def test_a_file_not_touched_afterwards_is_not_counted(self) -> None:
        """🔬 음성 — 안 바뀐 것을 바뀌었다고 하면 대리지표가 부푼다."""
        got = mod.tally([self._comment()], {self.OLD: {"tools/other.py"}})
        self.assertEqual(got["touched_after"], 0)
        self.assertEqual(got["findings"], 1)
