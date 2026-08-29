"""`check_gaps_ledger` 의 표기 시험. **네트워크는 안 탄다.**

🔴 이 검사가 왜 있나: *"격차가 몇 건 남았나"* 에 **19 라고 답했고 틀렸다.** 실제로는 15 였다.
종료 표기가 두 가지였고 아무것도 그걸 붙들지 않았다. 이 시험은 그 상태로 **되돌아가지
않는다는 것**을 지킨다.
"""

from __future__ import annotations

import unittest

from check_gaps_ledger import LEDGER, problems, rows


def parse(text: str) -> list[str]:
    return problems(rows(text))


class Notation(unittest.TestCase):
    def test_closed_without_strikethrough_is_caught(self) -> None:
        """🔴 이게 실제로 일어난 실패다 — 네 행이 이 모양이라 열린 것으로 세어졌다."""
        bad = "| **R5-99** ✅ **종료 2026-08-24** 무엇 | 문제 | 판단 | 처방 |"
        found = parse(bad)
        self.assertTrue(any("취소선이 없다" in f for f in found), found)

    def test_strikethrough_without_the_word_is_caught(self) -> None:
        bad = "| ~~**R5-98**~~ 그냥 지웠다 2026-08-24 | 문제 | 판단 | 처방 |"
        self.assertTrue(any("안 적혀 있다" in f for f in parse(bad)))

    def test_closed_without_a_date_is_caught(self) -> None:
        """언제 닫혔는지 못 재면 대장이 이력을 잃는다."""
        bad = "| ~~**R5-97**~~ ✅ **종료** 무엇 | 문제 | 판단 | 처방 |"
        self.assertTrue(any("날짜가 없다" in f for f in parse(bad)))

    def test_duplicate_id_is_caught(self) -> None:
        dup = ("| ~~**R5-96**~~ ✅ **종료 2026-08-24** 하나 | a | b | c |\n"
               "| ~~**R5-96**~~ ✅ **종료 2026-08-25** 둘 | a | b | c |")
        self.assertTrue(any("두 번 나온다" in f for f in parse(dup)))

    def test_a_correct_closed_row_passes(self) -> None:
        ok = "| ~~**R5-95**~~ ✅ **종료 2026-08-28 — 했다.** 원래 문제 ↓ | 문제 | 판단 | ⬜ 옛 처방 |"
        self.assertEqual(parse(ok), [])

    def test_open_row_passes(self) -> None:
        ok = "| **R5-94** 아직 안 된 것 | 문제 | 판단 | ⬜ 처방 |"
        self.assertEqual(parse(ok), [])


class WordChoice(unittest.TestCase):
    def test_jongryu_is_not_jongryo(self) -> None:
        """🔴 `R5-28` 의 제목이 *"— 종류다"* 다. 느슨하게 매칭하면 **열린 행을 닫힌 것으로 읽는다.**"""
        ok = "| **R5-93** 실물이 하는데 바닥이 안 적는다 — 종류다 | a | b | ⬜ c |"
        self.assertEqual(parse(ok), [])


class HistoryIsNotATodo(unittest.TestCase):
    def test_checkbox_after_the_marker_is_history(self) -> None:
        """닫힌 행은 원래 표를 그대로 보존한다(append-only). 거기 `⬜` 는 역사다."""
        ok = "| ~~**R5-92**~~ ✅ **종료 2026-08-28 — 했다.** 원래 문제 ↓ | a | b | ⬜ 옛 처방 |"
        self.assertEqual(parse(ok), [])

    def test_checkbox_inside_the_closing_text_is_caught(self) -> None:
        """🔬 이걸로 `R5-31` 의 *"라벨 붙이기는 남는다"* 를 실제로 찾아냈다."""
        bad = "| ~~**R5-91**~~ ✅ **종료 2026-08-28 — 했다.** ⬜ 그런데 이건 남는다. 원래 문제 ↓ | a | b | c |"
        self.assertTrue(any("종료문에 `⬜`" in f for f in parse(bad)), parse(bad))


class RealLedger(unittest.TestCase):
    def test_the_real_ledger_is_consistent(self) -> None:
        self.assertEqual(parse(LEDGER.read_text(encoding="utf-8")), [])


class DoneWordInAnUncheckedBox(unittest.TestCase):
    """🔬 `R5-17` 이 이 모양이라 **다 끝나고도 사흘을 열려 있었다**.

    같은 행의 배치 2·4 는 `✅` 인데 배치 3 만 `⬜ **배치 3 완료**` 였다.
    **낱말은 *완료* 인데 상자가 미완**이면 둘 중 하나가 거짓말이다.
    """

    def test_unchecked_box_followed_by_done_word_is_caught(self) -> None:
        bad = "| **R5-89** 무엇 | a | b | ⬜ **배치 3 완료 2026-08-26 (…)** |"
        self.assertTrue(any("미완 상자인데" in f for f in parse(bad)), parse(bad))

    def test_checked_box_with_done_word_passes(self) -> None:
        ok = "| **R5-88** 무엇 | a | b | ✅ **배치 3 완료 2026-08-26** · ⬜ 배치 4 는 남았다 |"
        self.assertEqual(parse(ok), [])

    def test_unchecked_box_with_a_real_todo_passes(self) -> None:
        """진짜 남은 일은 통과해야 한다 — 안 그러면 검사가 미완 상자 자체를 금지하게 된다."""
        ok = "| **R5-87** 무엇 | a | b | ⬜ **소유자 결정**: 어느 쪽으로 갈지 |"
        self.assertEqual(parse(ok), [])

    def test_the_done_word_must_be_near(self) -> None:
        """멀리 떨어진 '완료' 까지 잡으면 정상 행이 전부 빨개진다."""
        far = "⬜ " + ("x" * 60) + " 완료"
        self.assertEqual(parse(f"| **R5-86** 무엇 | a | b | {far} |"), [])
