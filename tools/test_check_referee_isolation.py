"""`check_referee_isolation` 시험. **네트워크도 git 도 안 탄다** (순수 판정만 본다).

🔴 이 검사가 왜 있나: 벽이 **느슨해지면 더 잘 통과한다.** 초록이 오히려 증거처럼 보인다 —
그래서 *검사로 못 잡는* 형태이고, **조합을 막는 것**만이 남는 수단이다(`GAPS` R5-46).
"""

from __future__ import annotations

import contextlib
import io
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
    def _run(self) -> tuple[int, str]:
        with contextlib.redirect_stdout(io.StringIO()) as out:
            code = mod.main()
        return code, out.getvalue()

    def test_unreadable_diff_is_a_failure_not_a_pass(self) -> None:
        """🔴 변경 목록을 못 구하면 *통과* 가 아니라 **모른다** 이다.

        **`main()` 을 실제로 돌린다** — 소스 문자열만 보면 판정을 뒤집어도 초록이다
        (제3자 리뷰 · 2026-09-02. 이 세션에서 네 번째로 같은 것을 배운다).
        """
        original = mod.changed_files
        mod.changed_files = lambda: None
        try:
            code, printed = self._run()
        finally:
            mod.changed_files = original
        self.assertEqual(code, 1, f"못 읽었는데 통과했다:\n{printed}")
        self.assertIn("RESULT FAIL", printed)

    def test_a_mixed_pr_actually_fails(self) -> None:
        """🔬 이 검사가 막으려는 **유일한 모양**을 실제로 돌려서 확인한다."""
        original = mod.changed_files
        mod.changed_files = lambda: ([".github/workflows/ci.yml", "tools/x.py"], "origin/main")
        try:
            code, printed = self._run()
        finally:
            mod.changed_files = original
        self.assertEqual(code, 1)
        self.assertIn("RESULT FAIL — 벽을 고치는 PR", printed)

    def test_a_referee_only_pr_passes(self) -> None:
        """🔬 반대편 — 심판만 바꾸는 PR 은 통과해야 한다(밀반입할 게 없다)."""
        original = mod.changed_files
        mod.changed_files = lambda: ([".github/workflows/ci.yml"], "origin/main")
        try:
            code, printed = self._run()
        finally:
            mod.changed_files = original
        self.assertEqual(code, 0)
        self.assertIn("RESULT PASS", printed)

    def test_a_non_ascii_workflow_path_is_still_a_referee(self) -> None:
        """🔴 git 기본 출력은 비ASCII 경로를 따옴표로 감싼다 — `-z` 로 원문을 받아야 한다."""
        self.assertTrue(mod.is_referee(".github/workflows/검사.yml"))
        source = Path(mod.__file__).read_text(encoding="utf-8")
        self.assertIn('"-z"', source)

    def test_the_referee_set_is_narrow_on_purpose(self) -> None:
        """🔴 넓히면 벽이 아니라 족쇄가 된다 — 왜 좁은지가 문서에 있어야 한다."""
        doc = mod.__doc__ or ""
        self.assertIn("전부 보호하면 아무것도 못 고친다", doc)
        self.assertIn("안 넣는다", doc)


class ItSaysWhatItComparedAgainst(unittest.TestCase):
    """🔴 스택 PR 을 로컬에서 돌리면 기본값 `main` 과 비교해 **아래 PR 의 변경까지 섞인다.**

    실측(2026-09-01): 배선 PR 에서 `referee=0` 이 나와 *심판을 안 건드린다* 로 읽힐 뻔했다.
    **무엇과 비교했는지 안 찍으면 숫자를 못 읽는다.**
    """

    def test_the_base_is_printed(self) -> None:
        source = Path(mod.__file__).read_text(encoding="utf-8")
        self.assertIn('print(f"  기준 {base} 대비', source)

    def test_changed_files_returns_the_base_too(self) -> None:
        source = Path(mod.__file__).read_text(encoding="utf-8")
        self.assertIn("tuple[list[str], str] | None", source)
        self.assertIn("GITHUB_BASE_REF", source)


class ReviewFindingsOn227(unittest.TestCase):
    def test_only_yaml_under_workflows_is_a_referee(self) -> None:
        """🔴 디렉터리 접두만 보면 README 까지 심판이 되어 **평범한 PR 이 막힌다.**"""
        self.assertFalse(mod.is_referee(".github/workflows/README.md"))
        self.assertTrue(mod.is_referee(".github/workflows/ci.yml"))
        self.assertTrue(mod.is_referee(".github/workflows/ci.yaml"))

    def test_renames_are_not_collapsed(self) -> None:
        """🔴 이름 변경 탐지가 켜져 있으면 목적지만 보여 **벽을 치우는 PR 이 통과한다.**"""
        source = Path(mod.__file__).read_text(encoding="utf-8")
        self.assertIn('"--no-renames"', source)

    def test_both_workflow_extensions_are_documented(self) -> None:
        """🔴 코드가 받는데 문서가 안 적으면 **적히지 않은 제약**을 강제하는 것이다.

        ⚠️ **세 곳이 같은 말을 해야 한다** — 모듈 표 · `AGENTS.md` · 함수 docstring.
        앞의 둘만 고치고 함수를 빼먹어 계약이 갈렸다(제3자 리뷰 2회 · 2026-09-01·02).
        """
        self.assertTrue(mod.is_referee(".github/workflows/ci.yaml"))
        self.assertIn("*.yaml", mod.__doc__ or "")
        self.assertIn("yaml", mod.is_referee.__doc__ or "")
        root = Path(mod.__file__).resolve().parent.parent
        self.assertIn("*.yaml", (root / "AGENTS.md").read_text(encoding="utf-8"))

    def test_the_wiring_split_is_explained(self) -> None:
        """배선 전에는 아무것도 안 막는다 — 그 사실이 도구에 적혀 있어야 한다."""
        doc = mod.__doc__ or ""
        self.assertIn("배선은 별도 PR", doc)
        self.assertIn("배선 전에는 이 검사가 아무것도 안 막는다", doc)


class OnlyDirectChildrenAreWorkflows(unittest.TestCase):
    """🔴 GitHub Actions 는 `.github/workflows/` **바로 밑**만 워크플로로 읽는다."""

    def test_a_nested_yaml_is_not_a_referee(self) -> None:
        """`…/archive/ci.yml` 은 **돌지 않는 파일**이다 — 막으면 오탐이다."""
        self.assertFalse(mod.is_referee(".github/workflows/archive/ci.yml"))

    def test_a_direct_child_still_is(self) -> None:
        self.assertTrue(mod.is_referee(".github/workflows/ci.yml"))
        self.assertTrue(mod.is_referee(".github/workflows/third-party.yaml"))
