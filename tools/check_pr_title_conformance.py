#!/usr/bin/env python3
"""PR 제목의 Conventional Commits 준수율을 잰다 — **표준 어휘로**.

## 2026-08-28 정정 — 확장 어휘를 접었다

전판은 `research`·`audit`·`decide`·`move` 를 **우리 어휘**로 두고 그것까지 통과시켰다.
그 판단이 **하루를 못 버텼다**: 목록이 `direction/05` 에 적혀 있는 상태에서 새 세션의
에이전트가 **`record:` 와 `anchor:` 를 즉석에서 만들었고**(PR #123 · #125), 둘 다 실은
`docs:` 였다 — 목록에 없는 걸 만든 게 아니라 **있는 걸 안 쓴 것**이다.

🔴 **커스텀 어휘는 그것을 읽어야만 성립한다.** 모델이 커밋 타입을 고를 때 꺼내는 것은
훈련에 있는 목록이고, `docs:` 는 모든 모델의 가중치에 있지만 `research:` 는 이 저장소의
문서 한 줄에만 있다. 그리고 **안 읽히는 것이 이 저장소의 반복 결함이다.**

그래서 타입은 `@commitlint/config-conventional` 과 같게 두고 **지역 의미는 scope 가 진다**
(규격이 그렇게 시킨다 — `CONVENTIONAL-COMMITS-SPEC`: *"Additional types are not mandated"*,
scope 는 자유형). `research:` → `docs(research):` 로 **잃는 것이 없다.**

## 두 가지를 잰다

① **어휘 합의** — `direction/05` 에 적힌 타입 목록과 이 파일의 `STANDARD` 가 **같은가.**
   갈리면 이 검사가 거짓말을 한다. 세 소비자(바닥 문서 · 이 검사 · `ci / pr-title`)가
   **하나의 목록**을 봐야 한다는 것이 이번 정정의 요점이다.
② **준수율** — 판정은 **`CUTOFF` 이후 머지된 PR** 로만 한다. 집행은 앞을 향하기 때문이다.
   그 이전은 맥락으로만 찍는다(소급해서 막지 않는다).

읽기 전용이다. `gh` 로 머지된 PR 제목만 본다.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FLOOR = ROOT / "direction" / "05-the-output-floor.md"

REPOS = ("coolbress/workflows", "coolbress/project-template",
         "coolbress/divcal", "coolbress/standards")

#: `@commitlint/config-conventional` 과 같다. `direction/05` 와 **같아야 한다**(①이 확인).
STANDARD = ("feat", "fix", "docs", "style", "refactor", "perf",
            "test", "build", "ci", "chore", "revert")

#: 접은 타입 → 앞으로 쓸 것. 위반을 **꾸짖는 대신 갈 곳을 알려주려고** 둔다.
RETIRED = {
    "research": "docs(research)", "audit": "docs(audit)",
    "decide": "docs(decision)", "decision": "docs(decision)", "decisions": "docs(decision)",
    "record": "docs", "anchor": "docs", "floor": "docs",
    "move": "refactor(layout)", "deps": "build(deps)", "security": "fix(security)",
}

TITLE = re.compile(rf"^({'|'.join(STANDARD)})(\([\w.\-/ ]+\))?!?: .+")
TYPE_OF = re.compile(r"^([A-Za-z]+)")

#: 표준 어휘가 발효하는 날. 이 **이후** 머지된 PR 로만 판정한다.
#: 🔴 결정이 2026-08-28 에 머지되므로 그날 것들은 **결정보다 앞선다** — 소급하지 않는다.
#: 처음에는 판정 대상이 0건이라 통과한다. 그게 맞다 — 집행의 시작점은 비어 있다.
CUTOFF = "2026-08-29"

#: 이 아래로 떨어지면 `ci / pr-title` 을 만든다 (`direction/05` 전환 조건 ⓑ).
THRESHOLD = 95.0

LIMIT = "300"

#: 바닥에서 타입 목록을 찾는 자리. 문구가 바뀌면 ①이 소리 내며 죽는다 — 조용히 통과하지 않는다.
VOCAB_ANCHOR = "**타입 목록은 이제 `@commitlint/config-conventional` 과 같다:**"


def floor_vocabulary() -> tuple[str, ...] | None:
    """바닥이 적어둔 타입 목록. 못 찾으면 None (그 자체가 결함이다)."""
    if not FLOOR.is_file():
        return None
    lines = FLOOR.read_text(encoding="utf-8").splitlines()
    for i, line in enumerate(lines):
        if VOCAB_ANCHOR in line:
            for nxt in lines[i + 1 : i + 4]:
                found = re.findall(r"`([a-z]+)`", nxt)
                if found:
                    return tuple(found)
    return None


def vocabulary_agrees() -> tuple[bool, str]:
    floor = floor_vocabulary()
    if floor is None:
        return False, f"바닥에서 타입 목록을 못 찾았다 (앵커: {VOCAB_ANCHOR!r})"
    if set(floor) != set(STANDARD):
        only_floor = sorted(set(floor) - set(STANDARD))
        only_here = sorted(set(STANDARD) - set(floor))
        return False, f"바닥에만 {only_floor} · 검사에만 {only_here}"
    return True, f"{len(STANDARD)}종 일치"


def merged_prs(repo: str) -> list[dict[str, str]]:
    out = subprocess.run(
        ["gh", "pr", "list", "--repo", repo, "--state", "merged",
         "--limit", LIMIT, "--json", "number,title,mergedAt"],
        capture_output=True, text=True, check=False,
    ).stdout
    rows: list[dict[str, str]] = json.loads(out or "[]")
    return rows


def main() -> int:
    agrees, detail = vocabulary_agrees()
    print(f"① 어휘 합의 — 바닥 vs 검사: {'✅ ' if agrees else '🔴 '}{detail}")

    graded: list[tuple[str, int, int, list[str]]] = []
    legacy_bad = 0
    legacy_total = 0
    retired_seen: dict[str, int] = {}
    for repo in REPOS:
        prs = merged_prs(repo)
        if not prs and repo == REPOS[0]:
            print("PR 을 하나도 못 읽었다 — `gh auth status` 를 확인해라")
            return 1
        bad: list[str] = []
        graded_n = 0
        for pr in prs:
            fresh = (pr.get("mergedAt") or "")[:10] >= CUTOFF
            conforms = bool(TITLE.match(pr["title"]))
            if not conforms:
                match = TYPE_OF.match(pr["title"])
                head = match.group(1) if match else ""
                if head in RETIRED:
                    retired_seen[head] = retired_seen.get(head, 0) + 1
            if fresh:
                graded_n += 1
                if not conforms:
                    bad.append(f"#{pr['number']} {pr['title']}")
            else:
                legacy_total += 1
                legacy_bad += 0 if conforms else 1
        graded.append((repo, graded_n - len(bad), graded_n, bad))

    print(f"\n② 준수율 — {CUTOFF} 이후 머지된 PR 만 판정한다 (집행은 앞을 향한다)")
    total = sum(n for _, _, n, _ in graded)
    ok = sum(k for _, k, _, _ in graded)
    for repo, k, n, bad in graded:
        if not n:
            print(f"  ·  {repo:32s} 판정 대상 없음")
            continue
        rate = 100 * k / n
        print(f"  {'✅' if rate >= THRESHOLD else '🔴'} {repo:32s} {k:3d}/{n:3d}  {rate:5.1f}%")
        for b in bad:
            head = TYPE_OF.match(b.split(" ", 1)[1] if " " in b else "")
            hint = RETIRED.get(head.group(1)) if head else None
            print(f"       ↳ {b[:70]}" + (f"   → `{hint}:` 를 써라" if hint else ""))

    if legacy_total:
        legacy_rate = 100 * (legacy_total - legacy_bad) / legacy_total
        print(f"\n  (맥락) {CUTOFF} 이전 {legacy_total}건 중 표준 어휘 준수 {legacy_rate:.1f}% — "
              "소급해서 막지 않는다")
    if retired_seen:
        print("  (맥락) 접은 타입 사용: "
              + " · ".join(f"{k}→{RETIRED[k]} {v}건" for k, v in sorted(retired_seen.items())))

    rate = 100 * ok / total if total else 100.0
    print(f"\nMETRIC vocabulary_agrees={int(agrees)} conformance={rate:.1f}% "
          f"n={total} legacy_n={legacy_total} threshold={THRESHOLD:.0f}")
    if not agrees:
        print("RESULT FAIL — 바닥과 검사의 타입 목록이 갈렸다. 하나로 맞춰라")
        return 1
    if total and rate < THRESHOLD:
        print("RESULT FAIL — 표준 어휘를 안 지킨 PR 이 있다 (direction/05 §정정)")
        return 1
    print("RESULT PASS — 표준 어휘로 지켜지고 있다")
    return 0


if __name__ == "__main__":
    sys.exit(main())
