"""`check_referee_isolation` 시험. **네트워크도 git 도 안 탄다** (순수 판정만 본다).

🔴 이 검사가 왜 있나: 벽이 **느슨해지면 더 잘 통과한다.** 초록이 오히려 증거처럼 보인다 —
그래서 *검사로 못 잡는* 형태이고, **조합을 막는 것**만이 남는 수단이다(`GAPS` R5-46).
"""

from __future__ import annotations

import unittest
from pathlib import Path

import check_referee_isolation as mod


class WhatCountsAsReferee(unittest.TestCase):
    def test_workflows_are_referees(self) -> None:
        self.assertTrue(mod.is_referee(".github/workflows/third-party.yml"))
        self.assertTrue(mod.is_referee(".github/workflows/ci.yml"))

    def test_ruleset_is_a_referee(self) -> None:
        self.assertTrue(mod.is_referee("ruleset.json"))

    def test_agents_md_is_not_a_referee_here(self) -> None:
        """🔴 §Code Review Rules 는 **이미** `workflows/pr-review.yml` 이 핀으로 지킨다.

        파일 전체를 심판에 넣으면 평범한 편집이 다 막힌다 — **두 번 막으면 아무것도 못 고친다.**
        """
        self.assertFalse(mod.is_referee("AGENTS.md"))

    def test_tests_are_not_referees(self) -> None:
        """도구와 그 시험은 **한 단위**다. 갈라 막으면 TDD 가 불가능해진다."""
        self.assertFalse(mod.is_referee("tools/test_check_gaps_ledger.py"))
        self.assertFalse(mod.is_referee("tools/check_gaps_ledger.py"))

    def test_a_lookalike_path_is_not_a_referee(self) -> None:
        """🔬 오탐 — `.github/` 밑이라고 다 벽이 아니다."""
        self.assertFalse(mod.is_referee(".github/PULL_REQUEST_TEMPLATE.md"))
        self.assertFalse(mod.is_referee("docs/workflows/ci.yml"))


class TheRuleIsAboutCombination(unittest.TestCase):
    """**심판만 바꾸는 PR 은 통과한다** — 밀반입할 것이 없기 때문이다."""

    def test_referee_only_is_allowed(self) -> None:
        referee, player = mod.split([".github/workflows/third-party.yml"])
        self.assertEqual((len(referee), len(player)), (1, 0))

    def test_player_only_is_allowed(self) -> None:
        referee, player = mod.split(["tools/x.py", "NEXT.md"])
        self.assertEqual((len(referee), len(player)), (0, 2))

    def test_the_combination_is_what_is_caught(self) -> None:
        """🔴 이게 막으려는 유일한 모양이다 — 벽을 무르게 하면서 다른 것을 같이 넣는 것."""
        referee, player = mod.split([".github/workflows/ci.yml", "tools/x.py"])
        self.assertTrue(referee and player)

    def test_empty_diff_is_allowed(self) -> None:
        self.assertEqual(mod.split([]), ([], []))


class ItFailsClosed(unittest.TestCase):
    def test_unreadable_diff_is_a_failure_not_a_pass(self) -> None:
        """🔴 변경 목록을 못 구하면 *통과* 가 아니라 **모른다** 이다.

        이 저장소는 *못 잰 것을 통과로 읽어* 여러 번 데었다(`direction/07` §반복해서 무는 실패).
        """
        source = Path(mod.__file__).read_text(encoding="utf-8")
        self.assertIn("RESULT FAIL — **못 읽은 것을 통과로 읽지 않는다.**", source)
        self.assertIn("if changed is None:", source)

    def test_the_referee_set_is_narrow_on_purpose(self) -> None:
        """🔴 넓히면 벽이 아니라 족쇄가 된다 — 왜 좁은지가 문서에 있어야 한다."""
        doc = mod.__doc__ or ""
        self.assertIn("전부 보호하면 아무것도 못 고친다", doc)
        self.assertIn("안 넣는다", doc)
