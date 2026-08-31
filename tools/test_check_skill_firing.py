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


class PluginQualifiedNames(unittest.TestCase):
    """🔴 플러그인으로 배포하면 이름이 `플러그인:스킬` 로 뜬다.

    실측(2026-08-31 · `divcal`): 전사에 `coolbress-standards:kickoff` 가 찍혔는데
    맨 이름만 맞추던 첫 판은 그걸 **0으로 셌다.** 하마터면 *"무기고 안내가 안 먹혔다"* 는
    **틀린 결론**을 낼 뻔했다 — **계기가 틀리면 판정도 틀린다.**
    """

    def test_a_plugin_qualified_name_counts_as_ours(self) -> None:
        # ⚠️ 파일의 `line()` 헬퍼를 쓴다 — 손으로 지은 JSON 은 실제 전사 모양이 아니었다.
        self.assertEqual(
            mod.skill_events(line("Skill", "coolbress-standards:kickoff")),
            ["coolbress-standards:kickoff"],
        )

    def test_someone_elses_skill_is_still_not_ours(self) -> None:
        """⚠️ 접미가 같다고 남의 것을 우리 것으로 세면 안 된다 — 그건 반대 방향 오류다."""
        for name in ("other-plugin:tdd", "obra:brainstorming"):
            self.assertNotIn(name.rsplit(":", 1)[-1], mod.OURS, name)


class OwnershipIsNamespaced(unittest.TestCase):
    """**남의 플러그인의 동명 스킬을 우리 것으로 세면 안 된다.**

    🔴 이 시험이 없어서 첫 정정이 반대쪽으로 틀렸다. `OURS` 에 `review` 가 있고
    설치된 `codex` 플러그인에 `review` 가 있으므로 **실재하는 충돌**이다.
    `ci / review` 의 제3자가 잡았다 — 그리고 *"반대 방향 시험이 `OURS` 에 없는
    이름만 써서 이 경로를 재현 못 한다"* 는 것까지 짚었다. 그 말이 맞았다.
    """

    def test_bare_name_is_ours(self) -> None:
        self.assertTrue(mod.is_ours("kickoff"))

    def test_our_plugin_prefix_is_ours(self) -> None:
        self.assertTrue(mod.is_ours("coolbress-standards:kickoff"))

    def test_someone_elses_plugin_with_the_same_skill_name_is_not_ours(self) -> None:
        # 🔴 핵심. 맨 이름만 보면 `review` 라서 우리 것으로 세어 버린다.
        self.assertIn("review", mod.OURS)
        self.assertFalse(mod.is_ours("codex:review"))
        self.assertFalse(mod.is_ours("other-plugin:review"))

    def test_unrelated_skill_is_not_ours(self) -> None:
        self.assertFalse(mod.is_ours("tdd"))
