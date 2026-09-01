#!/usr/bin/env python3
"""**하네스가 자기를 돌보는 데 얼마를 쓰나** (`GAPS` R5-45).

## 왜 이게 있나

🔴 **이 저장소의 창립 실패가 그것이다** — 여섯 세대가 *하네스를 돌보느라 프로젝트를 못 굴려서*
죽었다(`legacy/` · `direction/01` §대전제). **그런데 그것을 재는 눈금이 하나도 없었다.**

🔬 **구체적 실패 시나리오**(제3자 감사 P1 · 2026-09-01): 한 달에 제품 PR **3개** ·
하네스 유지보수 PR **20개**. **모든 검사는 초록이고, 그래서 아무도 못 본다.**
유지보수 PR 은 **품질이 좋을수록 더 초록**이라 계기가 없으면 **영원히 안 보인다.**

⚠️ *"얇다"* 는 지금 **주장이지 측정이 아니었다.** 이 도구가 그 주장을 숫자로 바꾼다.

## 무엇을 세나

| | |
|---|---|
| **하네스 PR** | `standards`(연구·방향) · `workflows`(벽·생성기) · `project-template`(템플릿) |
| **제품 PR** | `divcal` — 이 하네스로 굴린 **실제 프로젝트** |

**비율 = 하네스 / 전체.** 🔴 **창(window)이 있어야 뜻이 있다** (제3자 리뷰 P1 · 2026-09-02):
평생 누적만 재면 **지금 일어나는 유지비 급증이 창립 이력에 묻힌다** — 누적 318:23 위에
이번 달 20:3 이 얹혀도 비율은 **93% 그대로**다. 그게 바로 `R5-45` 가 잡으라던 시나리오다.
**그래서 최근 30일을 따로 낸다.** 🔴 **임계값은 안 긋는다**(`R5-2` 규율 — 건강한 분포를 보고 정한다).
**2~3개 프로젝트가 쌓인 뒤에** *하네스가 프로젝트보다 비싸지는 지점* 을 정한다.

⚠️ **비율만으로는 못 가른다** — 하네스가 *비싼* 것과 프로젝트가 *아직 하나뿐인* 것은
같은 숫자로 보인다. **그래서 제품 저장소 수도 같이 찍는다.**

🚫 **벽이 아니다.** 유지보수가 나쁜 게 아니라 **안 보이는 게** 나쁘다.

읽기 전용이고 **네트워크를 탄다**(CI 밖).
"""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import UTC, datetime
from typing import Any

HARNESS = ("standards", "workflows", "project-template")
PRODUCT = ("divcal",)

#: 한 번에 가져오는 상한. 🔴 **닿으면 실패로 본다** — 조용히 잘리면 비율이 거짓말을 한다.
#: 🔬 100 으로 뒀더니 `standards`(머지 208건)에서 **실제로 닿아 FAIL 이 났다** — 계기가 제 일을 했다.
RECENT = 1000

#: 🔴 **재는 창.** 평생 누적은 *이 저장소가 어떻게 생겼나* 를 재고, 창은 *지금 얼마를 쓰나* 를 잰다.
#: 둘 다 찍는다 — 하나만 보면 급증이 안 보이거나(누적) 표본이 없다(창).
WINDOW_DAYS = 30


def gh(args: list[str]) -> Any:
    try:
        out = subprocess.run(args, capture_output=True, text=True, check=False)
    except OSError:
        return None
    if out.returncode != 0:
        return None
    try:
        return json.loads(out.stdout or "null")
    except json.JSONDecodeError:
        return None


def merged_prs(repo: str) -> list[dict[str, Any]] | None:
    rows = gh(["gh", "pr", "list", "--repo", f"coolbress/{repo}", "--state", "merged",
               "--limit", str(RECENT), "--json", "number,title,mergedAt"])
    return rows if isinstance(rows, list) else None


def within(merged_at: str, now: datetime, days: int = WINDOW_DAYS) -> bool:
    """`mergedAt` 이 창 안인가. **순수 함수라 네트워크 없이 시험된다.**

    🔴 못 읽는 값은 **창 밖**으로 본다 — 창을 부풀리면 *지금 유지비* 가 실제보다 커 보인다.
    """
    try:
        when = datetime.fromisoformat(str(merged_at).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return False
    return (now - when).days < days


def ratio(harness: int, product: int) -> float | None:
    """하네스 비율. **분모가 0 이면 `None`** — *0%* 로 찍으면 좋은 결과처럼 읽힌다."""
    total = harness + product
    return harness / total if total else None


def summarise(counts: dict[str, int]) -> dict[str, int]:
    """(하네스 합, 제품 합). 순수 함수라 **네트워크 없이 시험된다.**"""
    return {"harness": sum(counts.get(r, 0) for r in HARNESS),
            "product": sum(counts.get(r, 0) for r in PRODUCT)}


def main() -> int:
    print("하네스 유지비 — 계기 (판정 아님 · `GAPS` R5-45)\n")
    counts: dict[str, int] = {}
    recent: dict[str, int] = {}
    unreadable: list[str] = []
    truncated: list[str] = []
    now = datetime.now(UTC)
    for repo in (*HARNESS, *PRODUCT):
        rows = merged_prs(repo)
        if rows is None:
            unreadable.append(repo)
            continue
        counts[repo] = len(rows)
        recent[repo] = sum(1 for pr in rows if within(str(pr.get("mergedAt") or ""), now))
        if len(rows) >= RECENT:
            truncated.append(repo)
        kind = "하네스" if repo in HARNESS else "제품 "
        print(f"  {kind}  coolbress/{repo:18s} 머지된 PR {len(rows):4d}"
              f"  (최근 {WINDOW_DAYS}일 {recent[repo]:3d})")

    got = summarise(counts)
    win = summarise(recent)
    r = ratio(got["harness"], got["product"])
    rw = ratio(win["harness"], win["product"])
    print(f"\n  평생 누적 — 하네스 {got['harness']} · 제품 {got['product']} · 제품 저장소 {len(PRODUCT)}개")
    print(f"  최근 {WINDOW_DAYS}일 — 하네스 {win['harness']} · 제품 {win['product']}")
    print("METRIC harness_prs={harness} product_prs={product} product_repos={n} "
          "harness_ratio={r} window_days={w} harness_prs_recent={hr} "
          "product_prs_recent={pr} harness_ratio_recent={rw} "
          "unreadable={u} truncated={t}".format(
              harness=got["harness"], product=got["product"], n=len(PRODUCT),
              r=f"{r:.3f}" if r is not None else "NA", w=WINDOW_DAYS,
              hr=win["harness"], pr=win["product"],
              rw=f"{rw:.3f}" if rw is not None else "NA",
              u=len(unreadable), t=len(truncated)))

    for label, got_, r_ in (("평생 누적", got, r), (f"최근 {WINDOW_DAYS}일", win, rw)):
        if r_ is not None:
            print(f"  {label} 하네스 비율 = "
                  f"{got_['harness']}/{got_['harness'] + got_['product']} = {r_:.0%}")
        else:
            print(f"  🔴 {label}: 분모가 0 이다 — 비율을 안 찍는다"
                  "(0% 로 찍으면 좋은 결과처럼 읽힌다)")
    print("  🔴 **급증은 창에서만 보인다** — 누적만 보면 창립 이력에 묻힌다(R5-45 의 시나리오).")

    print("\n  ⚠️ **비율만으로는 못 가른다** — 하네스가 *비싼* 것과 제품이 *아직 하나뿐인* 것이")
    print("     같은 숫자로 보인다. **2~3개 프로젝트가 쌓인 뒤에** 지점을 정한다(R5-2 규율).")
    print("  🚫 유지보수가 나쁜 게 아니라 **안 보이는 게** 나쁘다 — 이건 벽이 아니다.")

    if unreadable or truncated:
        for repo in unreadable:
            print(f"  🔴 못 읽었다: {repo}")
        for repo in truncated:
            print(f"  🔴 상한 {RECENT} 에 닿았다: {repo} — 잘렸을 수 있다")
        print("RESULT FAIL — **못 읽은 것을 0 으로 읽지 않는다.** 비율이 거짓말을 한다")
        return 1
    print("RESULT INFO — 계기판이다. 판정선은 긋지 않았다")
    return 0


if __name__ == "__main__":
    sys.exit(main())
