#!/usr/bin/env python3
"""증거 태그가 **처방과 실측을 구분하는가**를 검사한다.

🔴 왜 이 검사가 생겼나 (2026-08-30): claim 표의 `Class` 는 `normative`(**처방** — 표준·지침이
*그렇게 하라*고 한다)와 `empirical`(**실측** — 누가 세어보니 그렇더라)을 **구분한다.**
그런데 본문 불릿의 증거 태그는 **`[lit]` 하나로 둘을 담는다** — 실측 524건.

같은 태그 아래 이런 둘이 나란히 있다:

    MoSCoW — Must effort ≲60%          [lit]   ← **처방**. 아무도 60% 를 세지 않았다
    Buchgeher(900+ repos) ADR ~50%     [lit]   ← **실측**. 세어본 것이다

**이 저장소는 이 혼동으로 반복해서 데였다**(전부 `direction/05` 에 정정으로 남아 있다):
피라미드 비율(*"권고이지 실측이 아니다"* · `PYR-001`) · SAST L3(*"표준이 요구해서가 아니라
선택"*) · SLSA Source L2(*"서명이 아니다"* · `FFA-006`) · Cockburn 귀속(근거가 Medium 요약).
**넷 다 처방을 실측으로, 또는 그 반대로 읽은 것**이고, 넷 다 **사람이 나중에 알아채고** 고쳤다.

태그가 구분을 못 담으면 **정정은 매번 손으로** 나온다. 그래서 어휘를 넓힌다:

    [lit, normative]   표준·지침·규격이 **그렇게 하라고 한다**
    [lit, empirical]   누가 **세어봤다**. 그러면 n 도 같이 온다

**기준선 대비**로 판정한다(`check_figure_citations` 와 같은 방식) — 기존 것은 막지 않고
**새 위반만** 막는다. 524건을 한 번에 다시 태깅하면 **틀린 태그가 무태그보다 나쁘다.**
하나씩 원 출처를 열어 고치면서 기준선을 내린다.

⚠️ **수치가 있는 줄만 본다.** 혼동이 무는 자리가 거기다 — 수치 없는 산문에 태그를 요구하면
바닥이 문진표가 되고 그 자체가 P40(불필요한 방해) 위반이다.
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASELINE = ROOT / "audit" / "evidence-class-baseline.json"

#: 퍼센트 또는 `n=` — 증거 수치가 있는 줄
#  `2-4%` 를 EN DASH(U+2013)로 쓰는 범위가 실제로 있다 — 문자로 안 적고 코드포인트로 적는다(RUF001).
FIGURE = re.compile("(?<![\\w.])\\d{1,3}(?:[.\u2013-]\\d+)?%|(?<![\\w.])[nN]\\s*=\\s*\\d")
#: 한정어 없는 `[lit]`
BARE_LIT = re.compile(r"\[lit\]")
#: 같은 줄이 **이미 실측을 표시**하는가. 그러면 애매하지 않다.
MEASURED = re.compile(r"\[census\]|\[실측\]")


def untyped(text: str) -> list[tuple[int, str]]:
    """수치가 있는 줄에서 **애매한** `[lit]` 을 찾는다.

    🔴 **`[lit][census]` 는 세지 않는다** (2026-08-30 정정). 그런 줄은 이미 갈라져 있다 —
    `[lit]` 이 *SemVer 가 그렇게 하라고 한다*, `[census]` 가 *86% 가 그렇게 한다* 를 맡는다.
    처음 판은 그걸 다 세서 **68건 중 31건이 오탐**이었다. **오탐이 신호를 묻는다** —
    이 저장소가 `check_template_drift` 에서 두 번 겪은 그 형태다.
    """
    out: list[tuple[int, str]] = []
    for i, line in enumerate(text.splitlines(), 1):
        if FIGURE.search(line) and not MEASURED.search(line):
            out.extend((i, line.strip()) for _ in BARE_LIT.findall(line))
    return out


def survey(root: pathlib.Path) -> dict[str, int]:
    counts: dict[str, int] = {}
    for path in sorted(root.rglob("*.md")):
        found = untyped(path.read_text(encoding="utf-8"))
        if found:
            counts[path.relative_to(ROOT).as_posix()] = len(found)
    return counts


def main() -> int:
    counts = survey(ROOT / "corpus" / "aspects")
    total = sum(counts.values())
    base = json.loads(BASELINE.read_text(encoding="utf-8")) if BASELINE.exists() else {}
    limit = int(base.get("total", total))

    print("증거 태그 — 처방/실측 구분")
    print(f"METRIC untyped_lit_on_figure_lines={total}")
    print(f"METRIC baseline={limit}")

    if total > limit:
        worst = sorted(counts.items(), key=lambda kv: -kv[1])[:5]
        print(f"🔴 기준선({limit})보다 {total - limit}건 늘었다. 새 수치 줄은 한정어를 단다:")
        print("     [lit, normative] 표준이 그렇게 하라고 한다 · [lit, empirical] 누가 세어봤다")
        for path, n in worst:
            print(f"     {path}: {n}건")
        print("RESULT FAIL — 처방과 실측을 한 태그에 담는 줄이 늘었다")
        return 1

    if total < limit:
        print(f"🔵 기준선보다 {limit - total}건 줄었다. `{BASELINE.name}` 의 total 을 {total} 로 내려라.")
    print("RESULT PASS — 기준선 이하다")
    return 0


if __name__ == "__main__":
    sys.exit(main())
