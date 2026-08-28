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
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CENSUS = ROOT / "corpus/census-data/census-governance-floor/records.json"
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

SKIP = {"repo", "stars", "eco", "mono", "cli", "lib", "app", "primary_lang",
        "topics", "n_workflows", "issue_forms", "issue_md",
        "license_recognized", "license_spdx"}


def unaccounted() -> list[tuple[str, float]]:
    records = json.loads(CENSUS.read_text(encoding="utf-8"))
    floor = FLOOR.read_text(encoding="utf-8")
    total = len(records)
    out: list[tuple[str, float]] = []
    for col in records[0]:
        if col in SKIP:
            continue
        rate = 100 * sum(1 for r in records if r.get(col)) / total
        if rate < THRESHOLD:
            continue
        target = ROLLUP.get(col, col)
        pattern = NAMES.get(target)
        if pattern is None:
            out.append((col, rate))
            continue
        if not re.search(pattern, floor, re.IGNORECASE):
            out.append((col, rate))
    return sorted(out, key=lambda x: -x[1])


def main() -> int:
    missing = unaccounted()
    print(f"바닥 커버리지 — 센서스가 재는 산출물에 입장이 있는가 (임계 {THRESHOLD:.0f}%)")
    for col, rate in missing:
        print(f"  🔴 {col:22s} {rate:5.1f}%  바닥에 요구도 기각도 없다")
    print(f"\nMETRIC unaccounted={len(missing)}")
    if missing:
        print("RESULT FAIL — 요구하거나, 왜 안 쓰는지 적어라. 침묵은 안 된다")
        return 1
    print("RESULT PASS — 임계 위 산출물 전부 입장이 있다")
    return 0


if __name__ == "__main__":
    sys.exit(main())
