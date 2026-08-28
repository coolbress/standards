"""`check_pr_title_conformance` 의 어휘 시험. **네트워크는 안 탄다.**

🔴 이 시험의 핵심은 ①이다 — **바닥의 타입 목록과 검사의 목록이 갈리지 않는가.**
갈리면 검사가 거짓말을 하고, 그게 이번 정정을 부른 결함이다: 목록은 있는데
아무것도 그 목록을 붙들고 있지 않았다.
"""

from __future__ import annotations

import unittest

from check_pr_title_conformance import (
    RETIRED,
    STANDARD,
    TITLE,
    floor_vocabulary,
    vocabulary_agrees,
)


class VocabularyAgreement(unittest.TestCase):
    def test_floor_and_checker_agree(self) -> None:
        agrees, detail = vocabulary_agrees()
        self.assertTrue(agrees, f"바닥과 검사의 타입 목록이 갈렸다: {detail}")

    def test_floor_list_is_actually_found(self) -> None:
        """앵커 문구가 바뀌면 **소리 내며 죽어야 한다.** 조용히 통과하면 검사가 꺼진 것이다."""
        self.assertIsNotNone(floor_vocabulary(), "바닥에서 타입 목록을 못 찾았다")

    def test_vocabulary_is_the_commitlint_conventional_set(self) -> None:
        self.assertEqual(
            set(STANDARD),
            {"feat", "fix", "docs", "style", "refactor", "perf",
             "test", "build", "ci", "chore", "revert"},
        )


class TitlePattern(unittest.TestCase):
    def test_standard_types_pass(self) -> None:
        for good in ("feat: 새 기능", "fix(cli): 고침", "docs(research): 코퍼스 추가",
                     "refactor(layout)!: 재배치", "build(deps): 올림"):
            self.assertTrue(TITLE.match(good), good)

    def test_retired_types_fail(self) -> None:
        """접은 타입은 **통과하면 안 된다.** 통과시키면 정정이 무의미하다."""
        for bad in ("research: 코퍼스 추가", "decide: 결정", "record: 기록",
                    "anchor: 앵커", "move: 이사"):
            self.assertFalse(TITLE.match(bad), bad)

    def test_missing_summary_fails(self) -> None:
        self.assertFalse(TITLE.match("feat:"))
        self.assertFalse(TITLE.match("제목만 있다"))


class RetiredMap(unittest.TestCase):
    def test_every_retired_type_points_at_a_standard_type(self) -> None:
        """대체 안내가 **또 다른 비표준**이면 사람을 잘못된 곳으로 보낸다."""
        for old, new in RETIRED.items():
            head = new.split("(")[0]
            self.assertIn(head, STANDARD, f"{old} → {new} 의 {head} 가 표준이 아니다")

    def test_retired_and_standard_do_not_overlap(self) -> None:
        self.assertEqual(set(RETIRED) & set(STANDARD), set())


if __name__ == "__main__":
    unittest.main()
