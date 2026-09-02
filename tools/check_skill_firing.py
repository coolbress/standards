#!/usr/bin/env python3
"""**스킬이 실사용에서 뜨는가**를 세션 전사에서 센다. 계기이지 판정이 아니다.

우리 설계 전체가 *"안내 층이 발화한다"* 는 가정 위에 서 있는데 **한 번도 안 쟀다.**
[`direction/07`](../direction/07-design-rules.md) 원칙 03 이 스스로 단서를 단다 —
***"막는 것에만 검증됐고 보여주는 것에는 미검증이다."***
🔴 **goppi 가 죽은 방식이 그 형태다** — 합성 공격 0/4 를 다 막고 실사용 11건에 침묵했다.

## 왜 전사인가 (2026-08-30 실측으로 골랐다)

| 후보 | 판정 |
|---|---|
| `claude plugin eval` | 🔴 **early access 게이트** — 실행 전에 거부된다(종료코드 1) |
| OTel 텔레메트리 | 🟡 **된다**(콘솔 익스포터·수집기 불필요) — 그러나 **지금부터만** 재고 매번 환경변수가 필요하며 `plugin.name` 이 `"third-party"` 로 **익명화**된다 |
| **세션 전사** | 🟢 **소급 가능 · 비용 0 · 켤 필요 없음.** 도구 이름과 입력이 그대로 있다 |

## 🔴 이 계기가 **못 재는 것**

***사용자가 `/이름` 을 쳤나, 모델이 스스로 골랐나*** 를 **구분하지 못한다.**
미검증의 핵심이 후자인데 **전사에도 텔레메트리에도 그 표시가 없다**(2026-08-30 실측 —
`skill_activated` 이벤트도 `invocation_trigger` 속성도 **존재하지 않는다**).
공식 요청이 열려 있다: `anthropics/claude-code` **#35319**.

## 🔴 비율로 세지 않는다

*"Skill 호출 ÷ 전체 도구 호출"* 은 **허영 지표**다 — 스킬 한 번이 `Bash` 50번을 이끌면 그것도 1이다.
시중 경고가 같은 말을 한다: *"궤적 전체를 봐야지 최종 답만 보면 안 된다."*
그래서 **사건으로 센다** — 언제 · 어느 프로젝트 · 어떤 스킬.

⚠️ **판정선을 긋지 않는다.** *"몇 건이면 좋은가"* 를 모른다. 상한을 상상으로 박는 것은
`GAPS` R5-2 에서 이미 피한 실수다 — 그때는 **건강한 분포에서 θ 를 쟀다.**
🔒 **출력은 스킬 이름과 프로젝트 슬러그뿐이다** — 프롬프트도 파일 내용도 찍지 않는다.
"""

from __future__ import annotations

import json
import pathlib
import sys
from collections import Counter

TRANSCRIPTS = pathlib.Path.home() / ".claude" / "projects"

#: 우리가 배포한 스킬·커맨드. 이것들이 뜨는지가 이 계기의 첫 질문이다.
# 2026-09-02: `kickoff`·`where-is-the-truth` 는 플러그인 0.10.0 에서 지웠고 `playbook` 이 들어왔다.
# 옛 이름을 남기는 이유 — 지난 전사에 찍힌 사건은 그때 우리 것이었다. 지우면 과거 눈금이 0 으로 바뀐다.
OURS = ("playbook", "kickoff", "new-project", "floor-check", "review", "where-is-the-truth")

#: 우리 스킬이 플러그인으로 뜰 때의 이름 공간.
OUR_PLUGIN = "coolbress-standards"


def is_ours(name: str) -> bool:
    """이 스킬 이름이 **우리 것**인가.

    맨 이름(`kickoff`)도 플러그인 형태(`coolbress-standards:kickoff`)도 우리 것이다.
    🔴 **그러나 `codex:review` 는 아니다.** 첫 정정이 `rsplit(":")[-1]` 로 맨 이름만 봐서
    **남의 플러그인의 동명 스킬을 우리 것으로 셌다** — `OURS` 에 `review` 가 있고
    `codex` 플러그인에 `review` 가 있으므로 **가상이 아니라 실재하는 경로**다.
    계기를 고치다가 계기를 반대쪽으로 틀리게 만든 것이고, `ci / review` 의 제3자가 잡았다.
    """
    plugin, _, bare = name.rpartition(":")
    if plugin and plugin != OUR_PLUGIN:
        return False
    return bare in OURS


def skill_events(text: str) -> list[str]:
    """전사 한 편에서 **`Skill` 도구 호출**의 스킬 이름만 뽑는다.

    파일을 안 읽는다 — 순수 함수라야 시험이 된다.
    """
    names: list[str] = []
    for line in text.splitlines():
        if '"tool_use"' not in line or '"Skill"' not in line:
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        message = record.get("message")
        blocks = message.get("content") if isinstance(message, dict) else None
        if not isinstance(blocks, list):
            continue
        for block in blocks:
            if not isinstance(block, dict) or block.get("type") != "tool_use":
                continue
            if block.get("name") != "Skill":
                continue
            payload = block.get("input")
            names.append(str(payload.get("skill", "?")) if isinstance(payload, dict) else "?")
    return names


def scan(root: pathlib.Path) -> dict[str, list[str]]:
    """프로젝트 슬러그 → 뜬 스킬 이름들."""
    found: dict[str, list[str]] = {}
    if not root.is_dir():
        return found
    for project in sorted(p for p in root.iterdir() if p.is_dir()):
        names: list[str] = []
        for transcript in project.glob("*.jsonl"):
            names.extend(skill_events(transcript.read_text(encoding="utf-8", errors="ignore")))
        if names:
            found[project.name] = names
    return found


def main() -> int:
    found = scan(TRANSCRIPTS)
    print("스킬이 실사용에서 뜨는가 — 계기 (판정 아님)")
    if not TRANSCRIPTS.is_dir():
        print(f"  ⚪ 전사가 없다: {TRANSCRIPTS} — 다른 기계이거나 CI 다")
        print("\nRESULT INFO — 잴 데이터가 없다")
        return 0

    totals: Counter[str] = Counter()
    for project, names in sorted(found.items(), key=lambda kv: -len(kv[1])):
        totals.update(names)
        print(f"  {project[:44]:46s} {len(names):3d}건  {', '.join(sorted(set(names)))}")

    # 🔴 **`플러그인:스킬` 형태도 우리 것이다** (2026-08-31 정정).
    # 플러그인으로 배포한 뒤 메뉴에 `coolbress-standards:kickoff` 로 뜬다.
    # 맨 이름만 맞추던 첫 판은 `divcal` 의 실제 발화를 **0으로 셌고**, 하마터면
    # *"무기고 안내가 안 먹혔다"* 는 **틀린 결론**을 낼 뻔했다.
    # **계기가 틀리면 판정도 틀린다** — 오늘 이 형태로 여러 번 걸렸다.
    # 🔴 그리고 그 정정이 **반대쪽으로 틀렸다** — `is_ours` 를 읽어라.
    ours_seen: dict[str, int] = {}
    for name, n in totals.items():
        if is_ours(name):
            ours_seen[name] = n
    print(f"\nMETRIC skill_events={sum(totals.values())} distinct_skills={len(totals)} "
          f"projects_with_skills={len(found)} ours={sum(ours_seen.values())}")
    print(f"  우리 스킬: {ours_seen or '아직 한 번도 안 떴다'}")
    print("  ⚠️ 사용자가 쳤는지 모델이 골랐는지는 **구분 못 한다** (전사·텔레메트리 둘 다 표시가 없다)")
    print("RESULT INFO — 계기판이다. 판정선은 긋지 않았다")
    return 0


if __name__ == "__main__":
    sys.exit(main())
