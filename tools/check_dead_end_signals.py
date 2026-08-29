#!/usr/bin/env python3
"""요구 ⑥ — **막다른 길에 빠진 것을 언제 아는가**를 잰다 (`GAPS` R5-2).

## 왜 상한을 상수로 안 정하나

등재된 근거가 그렇게 말한다. `AGENT-FAILURE-TELEMETRY-2026` 원문:
*"θ is read from **healthy validation episodes** and never from test data."*
즉 *"3회 실패하면 막다른 길"* 같은 수를 **상상해서 박지 않는다** — 이 저장소들이 **실제로
건강했을 때** 어땠는지를 재서 그 바깥을 이상으로 본다.

🔬 2026-08-29 실측(네 저장소 · PR 실행 106건 · 브랜치 88개):
**브랜치당 CI 실패 중앙값 0 · p90 0 · 최대 1.** 실패가 있었던 다섯 브랜치는 **전부 한 번에 고쳐졌다.**
→ **건강한 최대치가 1 이므로 θ = 2.** 두 번째 실패부터가 분포 바깥이다.

## 신호는 둘이다 (처방: 2개 이상 정의 · CI 관측 가능한 것 1개 배선)

| | 무엇을 잡나 | 어디서 읽나 |
|---|---|---|
| **A. 도구오류 연쇄** | 한 브랜치가 초록이 되기까지 **θ 회 이상** 실패한다 | **CI 실행 로그** (배선된 것) |
| **B. 되돌아옴** | 닫았던 격차가 **다시 열린다** — *끝났다고 믿었는데 아니었다* | `GAPS` 의 git 이력 |

⚠️ 이건 **벽이 아니라 계기판**이다. 막다른 길은 사람이 판정한다 —
이 도구는 *"평소와 다르다"* 를 **제때** 말할 뿐이다. 그게 요구 ⑥ 의 지표(*감지까지 걸린 시간*)다.

읽기 전용이다.
"""

from __future__ import annotations

import json
import re
import statistics
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "audit" / "GAPS.ko.md"

REPOS = ("standards", "workflows", "project-template", "divcal")
RUN_LIMIT = "120"

#: 건강한 실행에서 읽은 값보다 하나 위. 상수가 아니라 **측정에서 나온 수**다.
HEALTHY_MAX_OBSERVED = 1
THETA = HEALTHY_MAX_OBSERVED + 1

GAP_OPEN = re.compile(r"^\+\| \*\*(R5-\d+)\*\*", re.M)


def _runs(repo: str) -> list[dict[str, str]]:
    out = subprocess.run(
        ["gh", "run", "list", "--repo", f"coolbress/{repo}", "--limit", RUN_LIMIT,
         "--json", "conclusion,event,headBranch"],
        capture_output=True, text=True, check=False,
    )
    return json.loads(out.stdout or "[]") if out.returncode == 0 else []


def signal_a() -> tuple[dict[tuple[str, str], int], list[int]]:
    """브랜치별 CI 실패 횟수와 그 분포."""
    failures: dict[tuple[str, str], int] = {}
    seen: set[tuple[str, str]] = set()
    for repo in REPOS:
        for run in _runs(repo):
            if run.get("event") != "pull_request":
                continue
            key = (repo, run.get("headBranch") or "?")
            seen.add(key)
            if run.get("conclusion") not in ("success", "skipped", None):
                failures[key] = failures.get(key, 0) + 1
    return failures, sorted(failures.get(k, 0) for k in seen)


def signal_b() -> list[str]:
    """닫았던 격차가 다시 열린 적이 있나 — `GAPS` 의 커밋 이력에서 읽는다."""
    out = subprocess.run(
        ["git", "log", "-p", "--reverse", "--format=%H", "--", str(LEDGER.relative_to(ROOT))],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )
    if out.returncode != 0:
        return []
    closed: set[str] = set()
    reopened: list[str] = []
    for line in out.stdout.splitlines():
        if line.startswith("+| ~~**R5-"):
            match = re.search(r"R5-\d+", line)
            if match:
                closed.add(match.group(0))
        elif line.startswith("+| **R5-"):
            match = re.search(r"R5-\d+", line)
            if match and match.group(0) in closed:
                reopened.append(match.group(0))
    return reopened


def main() -> int:
    failures, distribution = signal_a()
    if not distribution:
        print("CI 실행을 하나도 못 읽었다 — `gh auth status` 를 확인해라")
        return 1

    healthy_max = max(distribution)
    median = statistics.median(distribution)
    over = sorted((k for k, v in failures.items() if v >= THETA), key=lambda k: -failures[k])

    print("요구 ⑥ — 막다른 길 신호")
    print(f"\n  A. 도구오류 연쇄 — 브랜치 {len(distribution)}개 · "
          f"실패 중앙값 {median:g} · 최대 {healthy_max} · θ={THETA}")
    for key in over:
        print(f"     🔴 {key[0]}/{key[1]}  실패 {failures[key]}회 — 평소와 다르다")
    if not over:
        print("     ✅ θ 이상으로 헤맨 브랜치 없음")
    if healthy_max > HEALTHY_MAX_OBSERVED:
        print(f"     ⚠️ 건강한 최대치가 {healthy_max} 로 올라갔다 — "
              f"θ 를 다시 재라 (지금 코드의 값은 {HEALTHY_MAX_OBSERVED})")

    reopened = signal_b()
    print(f"\n  B. 되돌아옴 — 닫았다 다시 열린 격차 {len(reopened)}건")
    for gid in reopened:
        print(f"     🔶 {gid} — 끝났다고 믿었는데 아니었다")
    if not reopened:
        print("     ✅ 되돌아온 격차 없음")

    print(f"\nMETRIC dead_end_theta={THETA} branches_over_theta={len(over)} "
          f"healthy_max={healthy_max} gaps_reopened={len(reopened)}")
    print("RESULT INFO — 계기판이다. 막다른 길은 사람이 판정한다")
    return 0


if __name__ == "__main__":
    sys.exit(main())
