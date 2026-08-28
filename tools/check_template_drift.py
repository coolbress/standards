#!/usr/bin/env python3
"""템플릿에서 뜬 저장소가 **템플릿을 따라오고 있는가**를 잰다.

`gh repo create --template` 은 **시점 복사**다. 복사가 끝나면 원본과 연결이 끊긴다 —
템플릿을 고쳐도 인스턴스는 그대로다. 2026-08-28 하루에만 *"기존 인스턴스는 자동으로
안 바뀐다"* 를 **세 번** 적었다(`AGENTS.md` · CONTRIBUTING 시험 · 이슈 폼).
**세 번 같은 문장을 쓰면 그건 결함이다.**

✅ **2026-08-28 — `copier` 로 전환했다**(R5-32 정정). 처음엔 *"생성 경로를 흔든다"* 며 안 하기로
했는데 **그 비용 추정이 틀렸다** — fail-closed 보증은 `trap cleanup EXIT` 하나이고 **콘텐츠가
어떻게 들어오는지와 무관**하다. 실패경로 시험은 목 하나(30줄)와 케이스 하나로 **15/15** 가 됐다.

그래도 이 검사는 남는다. `copier update` 는 **사람이 돌려야** 하고, **안 돌리면 드리프트는 그대로**다.
이 검사가 *"지금 돌릴 때다"* 를 알려준다.

인스턴스 탐지도 바뀌었다 — `templateRepository`(GitHub 의 *generated from*)는 `--template` 경로에서만
붙는다. 이제 **`.copier-answers.yml` 이 있는 저장소**가 인스턴스다. **그게 더 낫다** — 어느 판에서
태어났는지(`_commit`)까지 알려준다.

읽기 전용이다.
"""

from __future__ import annotations

import subprocess
import sys

TEMPLATE_OWNER = "coolbress"
TEMPLATE_NAME = "project-template"
TEMPLATE = f"{TEMPLATE_OWNER}/{TEMPLATE_NAME}"

#: 생성기가 지우거나 이름을 바꾸는 것 — 인스턴스에 없는 게 **정상**이다.
#: `bootstrap.sh` 는 실행 뒤 자기를 지우고(`divcal` 커밋 72c3d80), `src/app/` 은 이름이 바뀐다.
GENERATOR_ONLY = (
    "bootstrap.sh",              # 실행 뒤 자기를 지운다 (divcal 커밋 72c3d80)
    "tests/test_bootstrap_name.py",  # 생성기의 시험 — 같이 사라진다
    "src/app/",                  # `src/<프로젝트이름>/` 으로 이름이 바뀐다
    "tests/test_app.py",         # `tests/test_<프로젝트이름>.py` 로 이름이 바뀐다
    "dist/",                     # 빌드 산출물
    "{{ _copier_conf.answers_file }}.jinja",  # 답 파일의 **템플릿** — 인스턴스엔 렌더된 판이 간다
    "copier.yml",                # 템플릿 설정 — 인스턴스로 안 간다
    "tests/test_copier_template.py",  # 그 설정의 시험 — 같이 안 간다
)


def _files(repo: str) -> set[str]:
    out = subprocess.run(
        ["gh", "api", f"repos/{repo}/git/trees/HEAD?recursive=1",
         "--jq", '.tree[] | select(.type=="blob") | .path'],
        capture_output=True, text=True, check=False,
    ).stdout
    return {ln for ln in out.splitlines() if ln}


ANSWERS = ".copier-answers.yml"


def _has_answers(repo: str) -> bool:
    """답 파일이 있나. **종료코드로 판정한다** — 404 는 non-zero 다.

    🔴 `--jq` 와 raw Accept 헤더를 같이 쓰면 404 도 통과한다(실측: 인스턴스가 9개로 잡혔다).
    """
    return subprocess.run(
        ["gh", "api", f"repos/{repo}/contents/{ANSWERS}", "--silent"],
        capture_output=True, text=True, check=False,
    ).returncode == 0


def instances() -> list[str]:
    """`.copier-answers.yml` 을 가진 저장소가 인스턴스다.

    🔴 `templateRepository`(GitHub 의 *generated from*)로 찾지 않는다 — 그건 `--template`
    경로에서만 붙고, copier 로 만든 저장소에는 **없다.** 답 파일이 더 정확하고,
    `_commit` 까지 알려준다.
    """
    names = subprocess.run(
        ["gh", "repo", "list", TEMPLATE_OWNER, "--limit", "100", "--no-archived",
         "--json", "name", "--jq", ".[].name"],
        capture_output=True, text=True, check=False,
    ).stdout.split()
    found = []
    for n in names:
        if n == TEMPLATE_NAME:
            continue
        if _has_answers(f"{TEMPLATE_OWNER}/{n}"):
            found.append(f"{TEMPLATE_OWNER}/{n}")
    return found


def shared(paths: set[str]) -> set[str]:
    return {p for p in paths if not any(p.startswith(g) or p == g for g in GENERATOR_ONLY)}


def drift() -> list[tuple[str, list[str]]]:
    tmpl = shared(_files(TEMPLATE))
    return [(repo, sorted(tmpl - _files(repo))) for repo in instances()]


def main() -> int:
    rows = drift()
    print(f"템플릿 드리프트 — {TEMPLATE} 대비")
    if not rows:
        print("  인스턴스가 없다")
        return 0
    behind = 0
    for repo, missing in rows:
        mark = "✅" if not missing else "🔶"
        print(f"  {mark} {repo:30s} 안 따라온 파일 {len(missing)}개")
        for m in missing:
            print(f"       ↳ {m}")
        behind += len(missing)
    print(f"\nMETRIC instances={len(rows)} missing_files={behind}")
    if behind:
        print("RESULT DRIFT — 인스턴스가 템플릿을 안 따라왔다. PR 로 따라잡아라")
        print("  ⚠️ 파일 10개 이상이거나 인스턴스 3개 이상이면 GAPS R5-32(copier)를 다시 연다")
        return 1
    print("RESULT CLEAN — 인스턴스가 템플릿을 따라와 있다")
    return 0


if __name__ == "__main__":
    sys.exit(main())
