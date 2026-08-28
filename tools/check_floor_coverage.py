#!/usr/bin/env python3
"""센서스가 **재는** 산출물마다 바닥이 **입장을 밝혔는가**를 검사한다.

`AGENTS.md` 가 이 결함의 첫 사례였다 — 코퍼스가 채택률을 재고 있는데 바닥이 인용조차
안 했다. 우연인 줄 알았는데 **종류**였다(`audit/PURPOSE-DIRECTION-AUDIT.ko.md`):
이슈 폼(47.9%)·머지 방법(96.6%)이 같은 형태로 더 나왔다.

**바닥이 실물보다 적으면 셋이 생긴다** — 역산이 필요해지고, 드리프트를 못 잡고,
`presence≠adequacy` 를 못 건다(`CONTRIBUTING` 이 정확히 셋째였다).

그래서 규칙은 **"요구하라"** 가 아니라 **"입장을 밝혀라"** 다. 안 쓰는 것도 정당하지만
**적힌 기각과 침묵은 다르다** — 침묵은 다음 사람이 *"빠뜨린 건가"* 를 매번 다시 묻게 만든다.
`CODEOWNERS` 가 이미 기각을 적어뒀고, 그게 이 검사가 요구하는 형태다.

⚠️ 이 검사는 **입장이 있는지**만 본다. 그 입장이 옳은지는 못 본다.

🔴 **산문 `[census]` 줄은 일부러 안 훑는다.** 2026-08-28 에 해 봤다 — 측면 문서의
`[census]` 줄에서 백틱 토큰을 뽑으니 후보 **62개**가 나왔는데 거의 전부 오탐이었다:
센서스 경로(`census-data/...`) · 내부 칼럼명(`semver_ratio`·`cc_adopted`) ·
다른 생태계 도구(`Cargo.lock`·`pnpm-lock.yaml`·`vitest` — 바닥은 **의도적 Python 전용**이다) ·
잡음(`undefined`). **오탐이 신호를 묻으면 검사가 무시된다.**

대신 **구조화된 센서스 둘**을 본다. 같은 방식으로 재고 잡음이 없다 — 실측으로
`census-expanded` 확장이 후보 **1건**만 냈다(`dockerfile`).
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
FLOOR = ROOT / "direction/05-the-output-floor.md"

#: 이 채택률 아래는 묻지 않는다. 야생에서 드문 것을 전부 해명하게 하면
#: 바닥이 문진표가 된다 — 그 자체가 P40(불필요한 방해) 위반이다.
THRESHOLD = 20.0

#: 센서스 칼럼 → 바닥 본문에서 찾을 표기. 정규식이다.
#: 🔴 코퍼스가 실제로 쓰는 말을 넣는다. 형태가 달라 못 찾으면 검사가 문서를 고치게 만든다.
NAMES: dict[str, str] = {
    "has_ci": r"\bCI\b",
    "readme": r"README",
    "gitignore": r"gitignore",
    "license": r"LICENSE|라이선스",
    "contributing": r"CONTRIBUTING",
    "security": r"SECURITY",
    "changelog": r"CHANGELOG",
    "coc": r"CODE_OF_CONDUCT|CoC|행동강령",
    "codeowners": r"CODEOWNERS",
    "editorconfig": r"editorconfig",
    "has_lockfile": r"락파일|lockfile|uv\.lock",
    "dependabot": r"Dependabot",
    "agents_md": r"AGENTS\.md",
    "claude_md": r"CLAUDE\.md",
    "pr_template": r"PR 템플릿|PULL_REQUEST",
    "has_issue_tmpl": r"이슈 폼|ISSUE_TEMPLATE",
    "squash_allowed": r"머지 방법|squash",
    "gitattributes": r"gitattributes",
    "funding": r"FUNDING",
    "discussions": r"Discussions",
    "adr_dir": r"\bADR\b",
    "env_example": r"env\.example",
}

#: 롤업 — 상위 항목이 입장을 밝히면 같이 해명된 것으로 본다.
ROLLUP = {
    "coc_covenant": "coc",
    "dep_update_bot": "dependabot",
    "merge_commit_allowed": "squash_allowed",
    "rebase_allowed": "squash_allowed",
    "issue_config": "has_issue_tmpl",
}

#: `census-expanded` 만 쓰는 이름. 위 NAMES 와 합쳐 쓴다.
NAMES_EXPANDED: dict[str, str] = {
    "ci": r"\bCI\b",
    "issue_template": r"이슈 폼|ISSUE_TEMPLATE",
    "security_md": r"SECURITY",
    "code_of_conduct": r"CODE_OF_CONDUCT|CoC|행동강령",
    "lockfile": r"락파일|lockfile",
    "runtime_pin": r"런타임 핀|python-version|버전 고정",
    "linter": r"린터|ruff",
    "formatter": r"포매터|format",
    "typechecker": r"타입|mypy",
    "test_framework": r"테스트|pytest",
    "precommit_hooks": r"pre-commit",
    "task_runner": r"태스크 러너",
    "supply_chain": r"공급망",
    "has_releases": r"릴리스",
    "has_release_notes": r"릴리스 노트|변경 요약",
    "semver_any": r"SemVer",
    "cc_adopted": r"Conventional Commits",
    "dockerfile": r"Dockerfile|컨테이너",
    "devcontainer": r"devcontainer|개발 컨테이너",
}

SKIP = {"repo", "stars", "eco", "mono", "cli", "lib", "app", "primary_lang",
        "topics", "n_workflows", "issue_forms", "issue_md",
        "license_recognized", "license_spdx",
        # census-expanded 전용 메타
        "created", "source", "manifest", "sc_overall", "sc"}

#: 재는 센서스들. **구조화된 것만** 넣는다 (위 산문 주석 참조).
CENSUSES = (
    ("census-governance-floor", ROOT / "corpus/census-data/census-governance-floor/records.json"),
    ("census-expanded", ROOT / "corpus/census-data/census-expanded/records.json"),
)


def unaccounted() -> list[tuple[str, str, float]]:
    """입장이 없는 (센서스, 칼럼, 채택률) 을 돌려준다."""
    floor = FLOOR.read_text(encoding="utf-8")
    lookup = {**NAMES, **NAMES_EXPANDED}
    out: list[tuple[str, str, float]] = []
    for census, path in CENSUSES:
        records = json.loads(path.read_text(encoding="utf-8"))
        total = len(records)
        for col in records[0]:
            if col in SKIP:
                continue
            rate = 100 * sum(1 for r in records if r.get(col)) / total
            if rate < THRESHOLD:
                continue
            pattern = lookup.get(ROLLUP.get(col, col))
            if pattern is None or not re.search(pattern, floor, re.IGNORECASE):
                out.append((census, col, rate))
    return sorted(out, key=lambda x: -x[2])


def main() -> int:
    missing = unaccounted()
    names = " · ".join(c for c, _ in CENSUSES)
    print(f"바닥 커버리지 — {names} 가 재는 산출물에 입장이 있는가 (임계 {THRESHOLD:.0f}%)")
    for census, col, rate in missing:
        print(f"  🔴 {census:24s} {col:20s} {rate:5.1f}%  바닥에 요구도 기각도 없다")
    print(f"\nMETRIC unaccounted={len(missing)}")
    if missing:
        print("RESULT FAIL — 요구하거나, 왜 안 쓰는지 적어라. 침묵은 안 된다")
        return 1
    print("RESULT PASS — 임계 위 산출물 전부 입장이 있다")
    return 0


if __name__ == "__main__":
    sys.exit(main())
