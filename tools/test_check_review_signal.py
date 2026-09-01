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
