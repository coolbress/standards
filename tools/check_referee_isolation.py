#!/usr/bin/env python3
"""**심판이 선수와 같은 PR 에서 바뀌지 않는가** (`GAPS` R5-46).

## 왜 이게 있나

🔬 **구체적 실패 시나리오**(제3자 감사 P1 · 2026-09-01): 기능 변경과 **함께** 벽의 조건을
느슨하게 바꾼다 → **CI 는 초록이고 리뷰도 새 기준을 따라 통과** → *계약은 약해졌는데*
**완료로 판정**된다. 🔴 **검사로 못 잡는 형태다** — 벽이 느슨해지면 **더 잘 통과한다.**

같은 모양을 한 번 막았다: `workflows/pr-review.yml` 이 *리뷰어의 지시 변경 + 다른 변경*
조합을 막는다(`AGENTS.md` §Code Review Rules). **이 검사는 그 규율을 벽 자체에 넓힌다.**

## 무엇이 심판인가 — **좁게 고른다**

⚠️ **전부 보호하면 아무것도 못 고친다**(R5-46 이 못 박은 규율). 그래서 여기 넣는 것은
***다른 변경을 판정하는 것*** 뿐이다.

| 넣는다 | 왜 |
|---|---|
| `.github/workflows/*.yml` · `*.yaml` (**직계 자식만**) | **벽과 그 배선.** 재사용 워크플로 **핀**도 여기 있다 — 핀을 내리면 옛 판정이 돌아온다. 🔬 **둘 다 받는다** — GitHub Actions 가 둘 다 읽으므로 하나만 지키면 **확장자만 바꿔 빠져나간다** |
| `ruleset.json` | 벽의 실물(이 저장소엔 없고 `workflows` 에 있다 — 이식성 때문에 남긴다) |

| 안 넣는다 | 왜 |
|---|---|
| `AGENTS.md` | §Code Review Rules 는 **이미** `workflows/pr-review.yml` 이 핀으로 지킨다. 파일 전체를 넣으면 평범한 편집이 다 막힌다 — **두 번 막으면 아무것도 못 고친다** |
| `tools/test_*.py` | 도구와 그 시험은 **한 단위**다. 갈라 막으면 TDD 가 불가능해진다. ⚠️ *느슨해진 시험* 은 이 검사가 아니라 **리뷰**가 본다 |

## 규율

**심판만 바꾸는 PR 은 통과한다** — 밀반입할 것이 **없기** 때문이다.
`04` §리팩터링 분리(Fowler·Google)와 같은 모양이다.

🔧 **배선은 별도 PR 이다 — 이 검사 자신의 규칙 때문이다.** `ci.yml` 에 스텝을 붙이는 것이
**심판 변경**이라 도구·문서와 같은 PR 에 못 넣는다. 그래서 **표시·검사** 와 **배선** 을 갈랐다.
⚠️ **배선 전에는 이 검사가 아무것도 안 막는다** — 규칙이 문서에만 있는 상태이고,
이 저장소는 그 상태를 여러 번 겪었다. **두 PR 을 붙여서 머지한다.**

🔴 **못 읽으면 실패다.** 변경 목록을 못 구하면 *통과* 가 아니라 **모른다** 이고,
이 저장소는 그걸 통과로 읽어 여러 번 데었다.
"""

from __future__ import annotations

import os
import subprocess
import sys
from collections.abc import Sequence

#: 심판. 🔴 **늘리기 전에 위 표를 읽어라** — 넓히면 벽이 아니라 족쇄가 된다.
REFEREE_PREFIXES = (".github/workflows/",)
REFEREE_SUFFIXES = (".yml", ".yaml")
REFEREE_NAMES = ("ruleset.json",)


def is_referee(path: str) -> bool:
    """`.github/workflows/` **바로 밑**의 **`*.yml`·`*.yaml`** 과 `ruleset.json` 만 심판이다.

    🔴 **디렉터리 접두만 보면 안 된다** — `.github/workflows/README.md` 까지 심판이 되어
    **평범한 PR 이 막힌다**(제3자 리뷰 · 2026-09-01). 넓히면 벽이 아니라 족쇄다.
    🔬 **`.yaml` 도 받는다** — Actions 가 둘 다 읽으므로 하나만 지키면 **확장자만 바꿔 빠져나간다.**
    ⚠️ **모듈 표 · `AGENTS.md` · 이 docstring 이 같은 말을 해야 한다** — 앞의 둘만 고치고
    여기를 빼먹어 계약이 갈렸다(제3자 리뷰 · 2026-09-02).
    """
    if path in REFEREE_NAMES:
        return True
    # 🔴 **직계 자식만.** GitHub Actions 는 `.github/workflows/` **바로 밑**만 워크플로로
    # 읽는다 — `…/archive/ci.yml` 은 **돌지 않는 파일**이라 심판이 아니다. 접두만 보면
    # 그런 보관 파일이 평범한 PR 을 막는다(제3자 리뷰 · 2026-09-02).
    return (path.startswith(REFEREE_PREFIXES)
            and path.endswith(REFEREE_SUFFIXES)
            and "/" not in path[len(REFEREE_PREFIXES[0]):])


def split(changed: Sequence[str]) -> tuple[list[str], list[str]]:
    """(심판, 선수). **순수 함수라 네트워크도 git 도 안 탄다.**"""
    referee = [p for p in changed if is_referee(p)]
    player = [p for p in changed if not is_referee(p)]
    return referee, player


def changed_files() -> tuple[list[str], str] | None:
    """(바뀐 파일, 비교 기준). **못 구하면 `None`** — 빈 목록과 다르다.

    🔴 **무엇과 비교했는지 찍는다.** 스택 PR 을 로컬에서 돌리면 기본값 `main` 과 비교해
    **아래 PR 의 변경까지 섞여 보인다** — 실측에서 `referee=0` 이 나와 *심판을 안 건드린다* 로
    읽힐 뻔했다(2026-09-01). CI 는 `GITHUB_BASE_REF` 를 준다.
    """
    base = os.environ.get("GITHUB_BASE_REF") or "main"
    for ref in (f"origin/{base}", base):
        merge_base = subprocess.run(["git", "merge-base", ref, "HEAD"],
                                    capture_output=True, text=True, check=False)
        if merge_base.returncode != 0:
            continue
        # 🔴 **`--no-renames`.** 이름 변경 탐지가 켜져 있으면 `git diff --name-only` 가
        # **목적지만** 낸다 — `ci.yml` → `ci.disabled` 로 옮기면서 다른 것을 같이 넣으면
        # 심판이 0으로 보여 **벽을 치우는 PR 이 통과한다**(제3자 리뷰 · 2026-09-01).
        diff = subprocess.run(["git", "diff", "--no-renames", "--name-only",
                               merge_base.stdout.strip(), "HEAD"],
                              capture_output=True, text=True, check=False)
        if diff.returncode == 0:
            return [ln for ln in diff.stdout.splitlines() if ln.strip()], ref
    return None


def main() -> int:
    print("심판이 선수와 같이 바뀌지 않는가 — R5-46")
    found = changed_files()
    if found is None:
        print("  🔴 변경 목록을 못 구했다 — 기준 브랜치를 못 찾는다.")
        print("RESULT FAIL — **못 읽은 것을 통과로 읽지 않는다.** `git fetch origin main` 뒤 다시 돌려라")
        return 1

    changed, base = found
    referee, player = split(changed)
    print(f"  기준 {base} 대비 — 바뀐 파일 {len(changed)} · 심판 {len(referee)} · 선수 {len(player)}")
    for path in referee:
        print(f"     ⚖️  {path}")
    print(f"\nMETRIC changed={len(changed)} referee={len(referee)} player={len(player)}")

    if referee and player:
        print("  🔴 한 PR 이 **심판과 선수를 같이** 바꾼다:")
        for path in player[:6]:
            print(f"     · {path}")
        if len(player) > 6:
            print(f"     … 외 {len(player) - 6}개")
        print("RESULT FAIL — 벽을 고치는 PR 은 **벽만** 고쳐라. "
              "느슨해진 벽은 **더 잘 통과하므로** 검사로는 못 잡는다")
        return 1
    if referee:
        print("RESULT PASS — 심판만 바꾼다. 밀반입할 것이 없다")
        return 0
    print("RESULT PASS — 심판을 안 건드린다")
    return 0


if __name__ == "__main__":
    sys.exit(main())
