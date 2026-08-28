#!/usr/bin/env python3
"""수치 인용에 **축과 표본이 붙어 있는가**를 검사한다.

이 파일은 규약이 아니라 **검사**다. `direction/05` 가 한때 `X/Y` 를 두 가지 다른
뜻으로 썼다 — 한 줄은 `present/adequate`(n=2,000), 다른 줄은 `uni/wgt`(n=938) —
그런데 **어느 쪽도 그걸 밝히지 않았다.** 아래만 읽은 사람은 *"adequate 70%"* 로
읽는데 실제는 41.2% 다. 숫자는 맞고 결론이 틀리는 형태다.

문장으로 *"축을 밝혀라"* 라고 적어두면 발화하지 않는다. 그래서 센다.

**기준선 대비**로 판정한다(URL 감사와 같은 방식): 기존 후보는 막지 않고
**새 위반만** 막는다. 후보를 하나씩 원 데이터셋까지 추적해 고치면서 기준선을 내린다.
추적 없이 고치면 *"숫자는 맞고 축이 틀린"* 상태를 새로 만든다.
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASELINE = ROOT / "audit" / "figure-citation-baseline.json"

GLOBS = ("*.md", "direction/*.md", "audit/*.md", "corpus/aspects/*/*.md")

#: `75/70%` · `62% / 41%` · `≈ 100% uni / 100% wgt`
PAIR = re.compile(r"\d{1,3}\s*%?\s*(?:uni)?\s*/\s*\d{1,3}\s*%")
#: 축을 밝히는 어휘. 하나라도 있으면 읽는 사람이 두 수를 구분할 수 있다.
AXIS = re.compile(r"uni\b|wgt|weighted|가중|present\s*/|adequa|sw\b", re.IGNORECASE)
N_DECL = re.compile(r"\b[nN]\s*=\s*[\d,]+")

#: 앞 몇 줄까지를 같은 문맥으로 볼 것인가. 절 머리글에 축을 선언하는 관례를 인정한다.
CONTEXT_LINES = 8


def missing_labels(context: str) -> list[str]:
    """문맥에서 빠진 표기를 돌려준다. 파일 없이 시험할 수 있게 떼어 놨다."""
    return [
        name for name, rx in (("축", AXIS), ("n", N_DECL)) if not rx.search(context)
    ]


def findings() -> list[tuple[str, int, str]]:
    out: list[tuple[str, int, str]] = []
    seen: set[pathlib.Path] = set()
    for glob in GLOBS:
        for path in sorted(ROOT.glob(glob)):
            if not path.is_file() or path in seen:
                continue
            seen.add(path)
            lines = path.read_text(encoding="utf-8").splitlines()
            for i, line in enumerate(lines):
                if not PAIR.search(line):
                    continue
                ctx = "\n".join(lines[max(0, i - CONTEXT_LINES) : i + 1])
                missing = missing_labels(ctx)
                if missing:
                    rel = path.relative_to(ROOT).as_posix()
                    out.append((rel, i + 1, "·".join(missing)))
    return out


def main() -> int:
    found = findings()
    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))["max_findings"]

    print("수치 인용 — 축·표본 표기 검사")
    for rel, line, missing in found:
        print(f"  🔶 {rel}:{line}  ({missing} 미표기)")

    print(f"\nMETRIC findings={len(found)} baseline={baseline}")
    if len(found) > baseline:
        print("RESULT FAIL — 새 위반이 늘었다. 축(uni/wgt · present/adequate)과 n 을 같이 적어라")
        return 1
    if len(found) < baseline:
        print(f"RESULT PASS — 줄었다. audit/figure-citation-baseline.json 을 {len(found)} 로 내려라")
        return 0
    print("RESULT PASS — 기준선과 같다")
    return 0


if __name__ == "__main__":
    sys.exit(main())
