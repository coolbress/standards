"""스킬 발화 계기의 **파싱 규칙** 시험. 전사도 네트워크도 안 탄다.

🔴 순수 함수(`skill_events`)만 시험한다 — 파일을 읽는 함수는 음성 시험이 안 되고,
**통과만 하는 검사는 증명이 약하다**(`check_purpose_sync` 에서 배운 것과 같다).
"""

from __future__ import annotations

import json
import unittest

import check_skill_firing as mod


def line(name: str, skill: str | None = None) -> str:
    payload: dict[str, object] = {"type": "tool_use", "name": name}
    if skill is not None:
        payload["input"] = {"skill": skill}
    return json.dumps({"message": {"content": [payload]}}, ensure_ascii=False)


class SkillEvents(unittest.TestCase):
    def test_picks_skill_calls(self) -> None:
        text = "\n".join([line("Skill", "kickoff"), line("Skill", "last30days")])
        self.assertEqual(mod.skill_events(text), ["kickoff", "last30days"])

    def test_ignores_other_tools(self) -> None:
        """🔴 `Bash` 가 스킬로 세어지면 계기가 통째로 거짓말한다."""
        text = "\n".join([line("Bash"), line("WebSearch"), line("Skill", "kickoff")])
        self.assertEqual(mod.skill_events(text), ["kickoff"])

    def test_survives_broken_lines(self) -> None:
        """전사는 append 되는 파일이라 **잘린 줄**이 있을 수 있다. 거기서 죽으면 안 된다."""
        text = "\n".join(['{"tool_use" "Skill" 깨진 줄', line("Skill", "review"), ""])
        self.assertEqual(mod.skill_events(text), ["review"])

    def test_missing_input_does_not_crash(self) -> None:
        self.assertEqual(mod.skill_events(line("Skill")), ["?"])

    def test_empty_transcript_is_empty(self) -> None:
        self.assertEqual(mod.skill_events(""), [])

    def test_our_skill_list_matches_shipped_commands(self) -> None:
        """🔴 `OURS` 가 낡으면 *우리 것이 떴나* 에 영영 0 이 나온다."""
        for name in ("kickoff", "new-project", "floor-check", "review", "where-is-the-truth"):
            self.assertIn(name, mod.OURS)

    def test_instrument_never_fails_the_build(self) -> None:
        """계기다. 판정하지 않는다 — 종료코드는 항상 0 이어야 한다."""
        self.assertEqual(mod.main(), 0)
