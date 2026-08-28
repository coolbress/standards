#!/usr/bin/env python3
"""`direction/` 이 코퍼스 문서를 **이름으로만** 부르는 자리를 찾는다.

왜 이게 검사여야 하나 (2026-08-28, `GAPS` R5-29):
바닥이 `AGENTS.md` 를 문서 묶음에 넣으면서 근거인 `planning-output-census` 를
**백틱 이름으로만** 적었다. 링크가 아니라 이름이면 —

  1. **사람이 찾아야 한다.** 28개 측면 어디에 있는지 문서가 말해주지 않는다.
  2. 🔴 **`validate_corpus` 의 claim 불변식이 발화하지 않는다.** 그 검사는
     `corpus/...md` **경로 인용**에만 걸린다. 이름으로 부르면 claim 없는 문서를
     근거로 세워도 조용히 통과한다 — 우회로가 열려 있는 것이다.

그래서 R5-29 를 고칠 때 **좌표가 아니라 부류**를 잡는다. 이름으로 부르는 자리를
전부 찾아 경로로 바꾸고, 다시 생기면 여기서 막는다.

⚠️ 개념어와 문서 이름을 헷갈리지 않으려고 **실제 코퍼스 파일 stem 과 정확히 일치**할 때만 센다.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORPUS = ROOT / "corpus"
DIRECTION = ROOT / "direction"

# 백틱 안의 kebab-case 토큰. 코퍼스 파일 이름 규칙(`<topic>--<artifact>`)을 담는다.
BACKTICKED = re.compile(r"`([a-z0-9][a-z0-9.-]{6,})`")
PATH_CITE = re.compile(r"corpus/([A-Za-z0-9_./-]+)\.md")

BASELINE = 0


def corpus_stems() -> dict[str, Path]:
    return {p.stem: p for p in CORPUS.rglob("*.md")}


def findings(direction: Path, stems: dict[str, Path]) -> list[tuple[str, str, Path]]:
    out: list[tuple[str, str, Path]] = []
    for doc in sorted(direction.glob("*.md")):
        text = doc.read_text(encoding="utf-8")
        linked = {m.rsplit("/", 1)[-1] for m in PATH_CITE.findall(text)}
        for name in sorted(set(BACKTICKED.findall(text))):
            if name in stems and name not in linked:
                out.append((doc.name, name, stems[name]))
    return out


def main() -> int:
    stems = corpus_stems()
    found = findings(DIRECTION, stems)
    for doc, name, target in found:
        rel = target.relative_to(ROOT)
        print(f"NAME-ONLY {doc}: `{name}` — 경로 링크가 없다 (있어야 할 곳: {rel})")
    print(f"CHECK name_only_citations found={len(found)} baseline={BASELINE}")
    if len(found) > BASELINE:
        print("RESULT FAIL — 이름으로만 부르면 claim 불변식이 발화하지 않는다. 경로로 인용해라.")
        return 1
    print("RESULT PASS — 코퍼스 근거는 전부 경로로 인용된다")
    return 0


if __name__ == "__main__":
    sys.exit(main())
