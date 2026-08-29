#!/usr/bin/env python3
"""감사 문서가 **정본에서 도달 가능한가**를 검사한다.

🔴 `direction/` 이 안 가리키는 `audit/` 문서는 **다음 세션이 못 찾는다.**
`divcal` 완주 회고가 실측으로 보인 그 병이다 — ***산문 속 포인터는 안 따라간다.***
가리키지도 않으면 존재 자체를 모른다.

**도달은 전이적이다.** `direction/` → `GAPS` → `SKILL-OVERLAP` 처럼 감사 문서가 감사 문서를
가리키는 것도 도달로 친다. 대장(`GAPS`)이 한 번 가리키면 그 아래는 따라갈 수 있기 때문이다.

⚠️ **전부 참조돼야 하는 것은 아니다.** 지나간 감사(`WORKFLOW-REVIEW-2026-08-05`)는
그 시점의 기록이고 다시 인용될 이유가 없을 수 있다. 그래서 **기준선 대비**로 판정한다 —
기존 고아는 막지 않고 **새 고아만** 막는다(`check_figure_citations` 와 같은 방식).

🔵 **이 검사가 왜 없었나** — 우리 검사들은 *바닥이 산출물에 입장을 갖나*(`check_floor_coverage`)와
*코퍼스를 경로로 부르나*(`check_name_only_citations`)를 본다. **감사 층이 정본에 매달려 있나**는
**아무도 안 보는 자리**였다. R5-38 과 같은 형태다.
"""

from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIRECTION = ROOT / "direction"
AUDIT = ROOT / "audit"
BASELINE = ROOT / "audit" / "audit-reachability-baseline.json"


def audit_docs() -> list[str]:
    """감사 층의 마크다운. 기준선 파일 자신은 제외된다(`.json` 이라 애초에 안 걸린다)."""
    return sorted(p.name for p in AUDIT.glob("*.md"))


def reachable(names: list[str]) -> set[str]:
    """`direction/` 에서 시작해 **전이적으로** 닿는 감사 문서.

    이름이 본문 어디에든 나오면 닿은 것으로 친다 — 경로 링크든 코드 스팬이든,
    **다음 사람이 그 이름으로 찾아갈 수 있으면** 도달이다.
    """
    seen: set[str] = set()
    frontier = [p.read_text(encoding="utf-8") for p in sorted(DIRECTION.glob("*.md"))]
    while frontier:
        text = frontier.pop()
        for name in names:
            if name in seen or name not in text:
                continue
            seen.add(name)
            frontier.append((AUDIT / name).read_text(encoding="utf-8"))
    return seen


def orphans() -> list[str]:
    names = audit_docs()
    return [n for n in names if n not in reachable(names)]


def main() -> int:
    found = orphans()
    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))["orphans"] if BASELINE.is_file() else []
    new = [n for n in found if n not in baseline]
    fixed = [n for n in baseline if n not in found]

    print("감사 문서가 정본에서 도달 가능한가")
    for name in found:
        mark = "🔴" if name in new else "⚪"
        print(f"  {mark} {name}")
    for name in fixed:
        print(f"  ✅ 이제 도달한다: {name}")
    print(f"\nCHECK audit_reachability orphans={len(found)} baseline={len(baseline)}")
    if new:
        print(f"RESULT FAIL — 새 고아 {len(new)}건. `direction/` 이 가리키지 않으면 "
              "다음 세션이 못 찾는다. 정본에서 링크하거나 기준선을 갱신해라")
        return 1
    print("RESULT PASS — 새로 끊긴 감사 문서가 없다")
    return 0


if __name__ == "__main__":
    sys.exit(main())
