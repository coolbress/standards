"""목적 동기화 검사의 **음성 시험**. 네트워크도 파일도 안 탄다.

🔴 검사가 *통과만* 하는 것은 증명이 약하다 — **갈렸을 때 실제로 잡는가**를 봐야 한다.
`validate_corpus` 리팩터링에서 배운 것과 같다: 깨끗한 상태만 비교하면 오류 경로를 안 지난다.
"""

from __future__ import annotations

import unittest

import check_purpose_sync as mod

CANON_TEXT = mod.CANON.read_text(encoding="utf-8")


class PurposeSync(unittest.TestCase):
    def test_front_door_matches_canon(self) -> None:
        self.assertEqual(mod.main(), 0)

    def test_canonical_line_is_not_empty(self) -> None:
        """🔴 못 뽑으면 검사가 **눈이 먼 채로 초록**이 된다."""
        want = mod.canonical(CANON_TEXT)
        self.assertTrue(want)
        self.assertIn("포장", want, "rev8 의 '포장' 이 빠지면 정본 추출이 틀렸다")

    def test_drifted_front_door_is_caught(self) -> None:
        """음성 시험 — 현관문이 **옛 문구**를 들고 있으면 잡아야 한다."""
        stale = "# standards\n\n> *최종 산출물이 시니어 엔지니어급이 되며…*\n"
        self.assertFalse(mod.matches(stale, mod.canonical(CANON_TEXT)),
                         "갈렸는데 같다고 했다 — 검사가 아무것도 안 본다")

    def test_multiline_quote_block_still_matches(self) -> None:
        """🔬 **이 시험이 진짜 약점을 잡았다.**

        정본을 여러 줄 인용 블록으로 옮기면 줄마다 `>` 가 붙는다. 그걸 안 걷어내면
        검사가 **멀쩡한 현관문을 틀렸다고** 한다. 지금 `README` 가 한 줄이라
        우연히 통과하고 있었을 뿐이다.
        """
        want = mod.canonical(CANON_TEXT)
        words = want.split(" ")
        third = max(1, len(words) // 3)
        lines = [" ".join(words[i:i + third]) for i in range(0, len(words), third)]
        wrapped = "# x\n\n> " + "\n> ".join(lines) + "\n"
        self.assertTrue(mod.matches(wrapped, want), "여러 줄 인용을 못 알아본다")
