"""`check_pr_title_conformance` 의 어휘·판정 시험. **네트워크는 안 탄다.**

가장 중요한 시험은 마지막 것이다 — **도구의 어휘가 `direction/05` 와 갈리지 않는가.**
갈리면 이 검사가 거짓말을 한다: 바닥이 허용한 타입을 도구가 위반으로 세거나 그 반대다.
오늘 그 형태의 결함을 여섯 번 찾았으므로 여기서는 시험으로 묶는다.
"""

from __future__ import annotations

import pathlib
import unittest

from check_pr_title_conformance import OURS, STANDARD, THRESHOLD, TITLE

FLOOR = pathlib.Path(__file__).resolve().parent.parent / "direction/05-the-output-floor.md"


class TitleMatching(unittest.TestCase):
    def test_accepts_standard_and_scoped_and_breaking(self) -> None:
        for title in ("feat: 월별 표를 찍는다",
                      "fix(ci): 핀을 올린다",
                      "feat!: 잡 이름을 바꾼다",
                      "docs(kickoff): 0절을 고친다"):
            self.assertIsNotNone(TITLE.match(title), title)

    def test_accepts_our_extended_vocabulary(self) -> None:
        # 🔴 표준 어휘로만 재면 standards 가 70.5% 로 보인다. 실측된 오탐이다.
        for title in ("research: C-2 측정", "audit: 목적 → 방향 감사",
                      "decide: 결정 다섯 종료", "move: 이사 배치 1"):
            self.assertIsNotNone(TITLE.match(title), title)

    def test_rejects_a_bare_summary(self) -> None:
        self.assertIsNone(TITLE.match("계보 정정 — 여섯 번째 하네스 발견"))

    def test_rejects_a_type_with_no_summary(self) -> None:
        self.assertIsNone(TITLE.match("feat:"))


class StaysAlignedWithTheFloor(unittest.TestCase):
    """도구와 바닥이 갈리면 검사가 거짓말을 한다."""

    def test_every_type_is_listed_in_the_floor(self) -> None:
        floor = FLOOR.read_text(encoding="utf-8")
        missing = [t for t in STANDARD + OURS if f"`{t}`" not in floor]
        self.assertEqual(
            missing, [],
            f"도구가 허용하는 타입이 direction/05 §우리 타입 어휘 에 없다: {missing}. "
            "둘을 같이 고쳐라 — 갈리면 이 검사가 거짓말을 한다.",
        )

    def test_threshold_matches_the_floor(self) -> None:
        self.assertIn(
            f"{THRESHOLD:.0f}%", FLOOR.read_text(encoding="utf-8"),
            "전환 조건 ⓑ 의 임계가 바닥에 안 적혀 있다",
        )
