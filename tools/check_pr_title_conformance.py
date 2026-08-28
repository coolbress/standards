#!/usr/bin/env python3
"""PR 제목의 Conventional Commits 준수율을 잰다. **전환 조건 ⓑ 를 측정으로 바꾼다.**

`direction/05` 가 *"준수율이 95% 아래로 떨어지면 `ci / pr-title` 을 만든다"* 라고 적었는데
**그 숫자를 재는 것이 없었다.** 오늘 하루 종일 고친 그 병(*문서에만 있는 규칙은 발화하지 않는다*)
을 전환 조건 자체가 다시 만들고 있었다.

🔴 **표준 어휘로만 재면 안 된다.** 2026-08-28 실측: 표준 11종으로 재니 `standards` 가 70.5% 로
보였는데 "위반" 32건이 전부 `research:`·`audit:`·`decision:`·`move:` — **문서·리서치 저장소의
확장 어휘**였다. 표준 `commitlint` 를 그대로 넣었으면 **정당한 PR 30건을 막았을 것**이다.
그래서 어휘를 **바닥과 같은 목록**으로 둔다.

읽기 전용이다. `gh` 로 머지된 PR 제목만 본다.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys

REPOS = ("coolbress/workflows", "coolbress/project-template",
         "coolbress/divcal", "coolbress/standards")

#: `direction/05` §우리 타입 어휘 와 **같아야 한다.** 갈리면 이 검사가 거짓말을 한다.
STANDARD = ("feat", "fix", "docs", "style", "refactor", "perf",
            "test", "build", "ci", "chore", "revert")
OURS = ("research", "audit", "decide", "decision", "move", "deps", "security")

TITLE = re.compile(
    rf"^({'|'.join(STANDARD + OURS)})(\([\w.\-/ ]+\))?!?: .+"
)

#: 이 아래로 떨어지면 `ci / pr-title` 을 만든다 (`direction/05` 전환 조건 ⓑ).
THRESHOLD = 95.0

LIMIT = "300"


def conformance() -> list[tuple[str, int, int, list[str]]]:
    rows: list[tuple[str, int, int, list[str]]] = []
    for repo in REPOS:
        out = subprocess.run(
            ["gh", "pr", "list", "--repo", repo, "--state", "merged",
             "--limit", LIMIT, "--json", "number,title"],
            capture_output=True, text=True, check=False,
        ).stdout
        prs = json.loads(out or "[]")
        bad = [f"#{p['number']} {p['title']}" for p in prs if not TITLE.match(p["title"])]
        rows.append((repo, len(prs) - len(bad), len(prs), bad))
    return rows


def main() -> int:
    rows = conformance()
    total = sum(n for _, _, n, _ in rows)
    ok = sum(k for _, k, _, _ in rows)
    if total == 0:
        print("PR 을 하나도 못 읽었다 — `gh auth status` 를 확인해라")
        return 1

    print(f"PR 제목 규약 준수율 — 임계 {THRESHOLD:.0f}%")
    for repo, k, n, bad in rows:
        rate = 100 * k / n if n else 100.0
        mark = "✅" if rate >= THRESHOLD else "🔴"
        print(f"  {mark} {repo:32s} {k:3d}/{n:3d}  {rate:5.1f}%")
        for b in bad:
            print(f"       ↳ {b[:78]}")

    rate = 100 * ok / total
    print(f"\nMETRIC conformance={rate:.1f}% n={total} threshold={THRESHOLD:.0f}")
    if rate < THRESHOLD:
        print("RESULT FAIL — 전환 조건 ⓑ 성립. `ci / pr-title` 을 만들 때다 (direction/05)")
        return 1
    print("RESULT PASS — 강제 없이 지켜지고 있다. 전환 조건 ⓑ 미성립")
    return 0


if __name__ == "__main__":
    sys.exit(main())
