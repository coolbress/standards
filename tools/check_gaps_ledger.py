#!/usr/bin/env python3
"""`GAPS` 대장의 **종료 표기가 하나인가**를 본다.

## 왜 이게 검사여야 하나 (2026-08-28)

*"격차가 몇 건 남았나"* 를 물었더니 **19 라고 답했고 틀렸다.** 실제로는 15 였다.
네 행(`R5-1`·`R5-8`·`R5-10`·`R5-13`)이 **제목에 "종료" 라고 적혀 있는데 취소선이 없어서**
열린 것으로 세어졌다. 즉 종료 표기가 **두 가지**였고 **아무것도 그걸 붙들지 않았다.**

🔴 **이건 오늘 하루 종일 고친 그 병이 격차 대장 자신에게 있던 것이다** —
*문서에만 있는 규칙은 발화하지 않는다.* 그리고 이 문서는 *"다음에 뭘 할지"* 의 정본이라,
숫자가 틀리면 **남은 일의 크기를 잘못 안다.**

## 표기는 하나다

| 상태 | 표기 |
|---|---|
| **닫힘** | `\\| ~~**R5-N**~~ ✅ **종료 YYYY-MM-DD — …**` |
| **열림** | `\\| **R5-N** …` |

행 안에 `✅ ① 완료` 같은 **부분 진행**을 적는 것은 자유다. 그건 행의 상태가 아니라 내용이다.
행의 상태를 정하는 것은 **취소선 하나뿐**이다.

읽기 전용이다.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "audit" / "GAPS.ko.md"

ROW = re.compile(r"^\| (~~)?\*\*(R5-\d+)\*\*(~~)?(.*)$", re.M)
DATE = re.compile(r"\d{4}-\d{2}-\d{2}")

#: 닫힘을 뜻하는 낱말. 🔴 `종류` 는 아니다 — `R5-28` 의 제목이 *"…— 종류다"* 라서
#: 느슨하게 매칭하면 열린 행을 닫힌 것으로 읽는다.
DONE_WORDS = ("종료", "닫힘")

#: 닫힌 행이 **원래 표를 그대로 보존**하는 지점. 이 뒤는 역사다.
HISTORY_MARKER = "원래 문제 ↓"


def rows(text: str) -> list[tuple[str, bool, str, str]]:
    """(id, 닫힘인가, 첫 칸, 나머지)"""
    out: list[tuple[str, bool, str, str]] = []
    for match in ROW.finditer(text):
        struck = bool(match.group(1) and match.group(3))
        rest = match.group(4)
        head, _, tail = rest.partition("|")
        out.append((match.group(2), struck, head.strip(), tail))
    return out


def problems(parsed: list[tuple[str, bool, str, str]]) -> list[str]:
    found: list[str] = []
    seen: set[str] = set()
    for gid, closed, head, tail in parsed:
        if gid in seen:
            found.append(f"{gid}: ID 가 두 번 나온다")
        seen.add(gid)

        says_done = any(w in head for w in DONE_WORDS)
        if says_done and not closed:
            found.append(
                f"{gid}: 제목이 '종료' 라는데 **취소선이 없다** — 열린 것으로 세어진다. "
                f"`| ~~**{gid}**~~` 로 적어라"
            )
        if closed and not says_done:
            found.append(f"{gid}: 취소선은 있는데 '종료'/'닫힘' 이라고 안 적혀 있다")
        if closed and not DATE.search(head):
            found.append(f"{gid}: 닫혔는데 **날짜가 없다** — 언제 닫혔는지 못 판다")
        # 🔴 `⬜` 는 **종료문 안**에 있을 때만 문제다. 닫힌 행은 뒤에 원래 표를
        # 그대로 보존하는데(append-only), 거기 있는 `⬜` 는 **역사이지 할 일이 아니다.**
        # 구분자는 `원래 문제 ↓`. 이걸 안 가르면 닫힌 행 6개가 전부 오탐으로 뜬다 — 실제로 그랬다.
        live = head.split(HISTORY_MARKER)[0] if HISTORY_MARKER in head else head
        if closed and "⬜" in live:
            found.append(f"{gid}: 닫혔는데 종료문에 `⬜` 가 남아 있다 — 둘 중 하나가 거짓말이다")
    return found


def main() -> int:
    if not LEDGER.is_file():
        print(f"대장이 없다: {LEDGER}")
        return 1
    parsed = rows(LEDGER.read_text(encoding="utf-8"))
    if not parsed:
        print("대장에서 R5-* 행을 하나도 못 읽었다 — 표 형식이 바뀌었나")
        return 1

    found = problems(parsed)
    open_ids = [gid for gid, closed, _, _ in parsed if not closed]
    closed_n = len(parsed) - len(open_ids)

    print(f"GAPS 대장 — {LEDGER.relative_to(ROOT)}")
    for message in found:
        print(f"  🔴 {message}")
    print(f"\n  열린 격차 {len(open_ids)}건: {' '.join(sorted(open_ids, key=lambda g: int(g[3:])))}")
    print(f"METRIC gaps_open={len(open_ids)} gaps_closed={closed_n} notation_problems={len(found)}")
    if found:
        print("RESULT FAIL — 종료 표기가 하나가 아니다. 남은 일의 크기를 잘못 알게 된다")
        return 1
    print("RESULT PASS — 표기가 하나다. 위 숫자가 정본이다")
    return 0


if __name__ == "__main__":
    sys.exit(main())
