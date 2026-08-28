#!/usr/bin/env python3
"""`direction/` 이 **덜 익은 코퍼스 문서를 인용할 때 status 를 병기하는가**.

## 왜 이게 검사여야 하나 (`GAPS` R5-4)

README **절대규칙 3** 의 원문은 *"`review-needed`·`draft` 문서를 인용하지 않는다"* 였다.
2026-08-02 감사에서 **상속 `verified` 50건이 전부 강등**되면서 그 규칙은 사문이 됐다 —
지키면 `direction` 이 **거의 아무것도 인용할 수 없다.**

그래서 2026-08-24 에 **"인용 지점에 status 를 병기한다"** 로 개정했다.
🔴 **그런데 개정만 하고 아무것도 그걸 지키지 않았다.** 2026-08-28 실측: `direction` 이 경로로
인용하는 코퍼스 문서 **14건 중 10건이 `draft`/`review-needed`** 인데 병기는 **0건**이었다.

*문서에만 있는 규칙은 발화하지 않는다* — 오늘 하루 종일 고친 그 병이 **절대규칙 자신**에게 있었다.

## 무엇을 요구하나

인용한 **그 줄**(또는 바로 다음 줄)에 대상 문서의 status 낱말이 있어야 한다.

    [`planning-output-census`](../corpus/.../planning-output-census.md) *(review-needed)*

`verified` 는 병기하지 않아도 된다 — 규칙이 막으려는 것은 **덜 익은 근거가 익은 척하는 것**이다.
`CLAIMLESS_OK`(규범·절차·역사 기록)는 애초에 claim 문서가 아니므로 면제한다.

읽기 전용이다.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from validate_corpus import CLAIMLESS_OK

ROOT = Path(__file__).resolve().parent.parent
CORPUS = ROOT / "corpus"
DIRECTION = ROOT / "direction"

CITE = re.compile(r"corpus/([A-Za-z0-9_./-]+\.md)")
STATUS = re.compile(r"^status:\s*(\S+)", re.M)

#: 병기가 필요한 status. `verified` 만 면제된다.
NEEDS_NOTE = frozenset({"draft", "review-needed", "imported", "superseded", "retracted"})

BASELINE = 0


def findings(direction: Path, corpus: Path) -> list[tuple[str, int, str, str]]:
    out: list[tuple[str, int, str, str]] = []
    for doc in sorted(direction.glob("*.md")):
        lines = doc.read_text(encoding="utf-8").splitlines()
        for i, line in enumerate(lines):
            for rel in dict.fromkeys(CITE.findall(line)):
                name = rel.rsplit("/", 1)[-1]
                if name in CLAIMLESS_OK:
                    continue
                target = corpus / rel
                if not target.is_file():
                    continue
                match = STATUS.search(target.read_text(encoding="utf-8"))
                status = match.group(1) if match else "(status 없음)"
                if status not in NEEDS_NOTE and match:
                    continue
                # 같은 줄 + 바로 다음 줄까지 본다 (링크 뒤에서 줄바꿈하는 문단이 있다)
                window = line + " " + (lines[i + 1] if i + 1 < len(lines) else "")
                if match and status in window:
                    continue
                out.append((doc.name, i + 1, name, status))
    return out


def main() -> int:
    found = findings(DIRECTION, CORPUS)
    for doc, line_no, name, status in found:
        print(f"NO-STATUS {doc}:{line_no}  {name}  → `{status}` 를 인용 지점에 병기해라")
    print(f"CHECK citation_status found={len(found)} baseline={BASELINE}")
    if len(found) > BASELINE:
        print("RESULT FAIL — 덜 익은 근거가 익은 척한다 (README 절대규칙 3)")
        return 1
    print("RESULT PASS — 덜 익은 인용은 전부 status 를 달고 있다")
    return 0


if __name__ == "__main__":
    sys.exit(main())
