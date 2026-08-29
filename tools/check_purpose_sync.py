#!/usr/bin/env python3
"""**목적 한 줄이 갈리지 않는가**를 검사한다.

🔴 2026-08-30 실측: 저장소 **현관문**(`README.md`)이 인용한 목적 한 줄이 **두 판 뒤처져** 있었다.
그것도 rev7 이 ***명시적으로 기각한 문구***(*"최종 산출물이 시니어 엔지니어급이 **된다**"*)를
들고 있었다 — rev7 이 *"그건 **자기평가**다"* 라며 고친 바로 그 문장이다.

**요약이 원자료보다 오래 산다.** 이 저장소가 반복해 고쳐온 결함이고, 하필 **가장 먼저 읽히는 자리**였다.
문장으로 *"정본을 따라 고쳐라"* 라고 적어두면 발화하지 않는다. 그래서 센다.

정본은 [`direction/01`](../direction/01-what-i-want.md) §한 줄이다.
"""

from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CANON = ROOT / "direction" / "01-what-i-want.md"
FRONT_DOOR = ROOT / "README.md"


def canonical(text: str) -> str:
    """`01` §한 줄에서 목적 문장을 뽑는다. 인용 블록(`>`)만 이어 붙인다.

    🔴 **파일을 안 읽는다** — 순수 함수라야 음성 시험이 된다. *갈렸을 때 잡는가* 를
    확인하지 않으면 이 검사는 *통과만 하는* 검사다.
    """
    body = text.split("## 한 줄", 1)[1].split("**개정", 1)[0]
    quoted = [ln.strip().lstrip(">").strip() for ln in body.splitlines() if ln.strip().startswith(">")]
    return " ".join(part for part in quoted if part)


def flatten(text: str) -> str:
    """인용 표시(`>`)와 줄바꿈을 걷어내 **한 줄로** 편다.

    🔬 이 함수가 없었을 때 시험이 잡았다 — 정본을 **여러 줄 인용 블록**으로 옮기면
    줄마다 `>` 가 붙어 문장 사이에 끼고, 검사가 **멀쩡한 현관문을 틀렸다고** 한다.
    지금 `README` 가 한 줄이라 우연히 통과하고 있었을 뿐이다.
    """
    stripped = " ".join(ln.strip().lstrip(">").strip() for ln in text.splitlines())
    return " ".join(stripped.split())


def matches(front_door: str, want: str) -> bool:
    """줄바꿈·인용 표시가 어디서 나든 같은 문장으로 친다."""
    return flatten(want) in flatten(front_door)


def main() -> int:
    want = canonical(CANON.read_text(encoding="utf-8"))
    print("목적 한 줄이 정본과 같은가")
    if not want:
        print("RESULT FAIL — `direction/01` §한 줄에서 문장을 못 뽑았다. 이 검사가 눈이 멀었다")
        return 1

    if matches(FRONT_DOOR.read_text(encoding="utf-8"), want):
        print(f"  ✅ README.md — 정본과 같다 ({len(want)}자)")
        print("\nRESULT PASS — 현관문이 정본을 그대로 옮기고 있다")
        return 0

    print("  🔴 README.md 가 정본과 다른 목적 한 줄을 들고 있다")
    print(f"     정본: {want[:90]}…")
    print("\nRESULT FAIL — 현관문이 낡았다. `direction/01` §한 줄을 그대로 옮겨라")
    return 1


if __name__ == "__main__":
    sys.exit(main())
