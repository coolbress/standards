#!/usr/bin/env python3
"""코퍼스가 **옛 하네스 이름을 현재 주어로** 쓰는 자리를 센다 (`GAPS` R5-5).

## 무엇이 문제였나

코퍼스는 폐기된 하네스들(`claudeck-v1` → `claudeck` → `gingoa` → `codex-native` → `goppi` →
`goppi_final`)을 위해 수집되기 시작했다. 그래서 그 시절 문서는 **그때의 이름으로 주어를 쓴다** —
*"gingoa's ① output set"* · *"gingoa's OWN archetype"*.

🔴 **가장 아팠던 곳은 현관문이었다**: `corpus/GUIDE.ko.md` 의 제목이
*"**goppi_final** 리서치 코퍼스 안내"* 였다 — 코퍼스가 **폐기된 하네스의 이름으로 자기를 소개**하고 있었다.
그건 고쳤다.

## 🔵 본문은 안 고친다 — 그게 이 검사의 요점이다

*"gingoa's TS/Node choice = the plurality"* 는 **그때 그 프로젝트가 무엇을 정했는지에 대한 참인 기록**이다.
이름을 바꾸면 **기록이 거짓이 된다.** 그래서 이 검사는 **되돌리라고 하지 않는다** —
**기준선을 잡아 더 늘지 않게** 한다(`check_figure_citations` 와 같은 방식).

읽는 규칙은 `GUIDE.ko.md` 상단에 있다: **코퍼스 본문의 옛 이름은 폐기된 하네스를 가리키지
이 저장소를 가리키지 않는다.**

읽기 전용이다.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORPUS = ROOT / "corpus"
GUIDE = CORPUS / "GUIDE.ko.md"

OLD_NAMES = ("gingoa", "goppi", "claudeck")

#: **주어 자리**만 센다 — 단순 언급(*"gingoa 에서 승계"*)은 역사 서술이라 정상이다.
SUBJECT = re.compile(
    r"\b(" + "|".join(OLD_NAMES) + r")(_final)?('s|’s|\s?의\s|\s?가\s|\s?는\s|\s?은\s)"
)

#: 2026-08-29 실측(파일 52 · 등장 186 · `GUIDE.ko.md` 제외). **줄이는 것이 목표가 아니다** — 늘지 않는 것이 목표다.
#: 🔵 정규식이 영어 소유격(`'s`)만이 아니라 **한국어 조사**(`의`·`가`·`는`·`은`)까지 본다 —
#: 처음에 영어 소유격만 세어 37 로 잡았다가 돌려보니 52 였다. **재보고 고친 수다.**
#: 🔴 여유를 두지 않는다 — 한 칸이라도 남기면 **새 문서 하나가 조용히 들어온다**(음성 시험으로 확인).
BASELINE_FILES = 52


def offenders() -> dict[str, int]:
    found: dict[str, int] = {}
    for path in sorted(CORPUS.rglob("*.md")):
        if path == GUIDE:
            continue          # 규칙을 설명하는 문서다 — 예시로 옛 이름을 든다
        hits = len(SUBJECT.findall(path.read_text(encoding="utf-8")))
        if hits:
            found[str(path.relative_to(ROOT))] = hits
    return found


def guide_carries_the_reading_rule() -> bool:
    if not GUIDE.is_file():
        return False
    text = GUIDE.read_text(encoding="utf-8")
    return "이 저장소가 아닙니다" in text and "폐기된 하네스" in text


def main() -> int:
    found = offenders()
    files, hits = len(found), sum(found.values())
    rule = guide_carries_the_reading_rule()

    print("코퍼스 정체성 — 옛 하네스 이름이 주어로 쓰인 자리")
    print(f"  {'✅' if rule else '🔴'} 읽는 규칙이 `GUIDE.ko.md` 에 있다")
    for path, n in sorted(found.items(), key=lambda kv: -kv[1])[:5]:
        print(f"     {n:3d}회  {path}")
    if files > 5:
        print(f"     … 외 {files - 5}개 파일")

    print(f"\nMETRIC identity_files={files} identity_hits={hits} baseline={BASELINE_FILES}")
    if not rule:
        print("RESULT FAIL — 읽는 규칙이 없다. 옛 이름이 이 저장소를 가리키는 것처럼 읽힌다")
        return 1
    if files > BASELINE_FILES:
        print(f"RESULT FAIL — 기준선({BASELINE_FILES})보다 늘었다. **새 문서는 옛 이름을 주어로 쓰지 않는다**")
        return 1
    print("RESULT PASS — 기준선 이하이고 읽는 규칙이 서 있다")
    return 0


if __name__ == "__main__":
    sys.exit(main())
