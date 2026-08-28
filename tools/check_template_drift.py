#!/usr/bin/env python3
"""템플릿에서 뜬 저장소가 **템플릿을 따라오고 있는가**를 잰다.

`gh repo create --template` 은 **시점 복사**다. 복사가 끝나면 원본과 연결이 끊긴다 —
템플릿을 고쳐도 인스턴스는 그대로다. 2026-08-28 하루에만 *"기존 인스턴스는 자동으로
안 바뀐다"* 를 **세 번** 적었다(`AGENTS.md` · CONTRIBUTING 시험 · 이슈 폼).
**세 번 같은 문장을 쓰면 그건 결함이다.**

🔵 **`copier` 를 쓰지 않기로 했다**(`GAPS` R5-32). `copier update` 가 이 문제를 정확히
풀지만, 도입하려면 템플릿을 jinja 로 바꾸고 **`new-project.sh` 의 생성 경로를 재작성**해야 한다 —
그 경로의 **fail-closed 보증은 실사용 중 두 번 발화한 하드윈**이고 시험 14개가 지킨다.
인스턴스 **1개 · 드리프트 4파일** 에서 그걸 흔드는 것은 손해다.

대신 **드리프트를 보이게** 만든다. 따라잡는 것은 사람이 하되 **모르고 지나치지는 않게.**

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
)


def _files(repo: str) -> set[str]:
    out = subprocess.run(
        ["gh", "api", f"repos/{repo}/git/trees/HEAD?recursive=1",
         "--jq", '.tree[] | select(.type=="blob") | .path'],
        capture_output=True, text=True, check=False,
    ).stdout
    return {ln for ln in out.splitlines() if ln}


def instances() -> list[str]:
    out = subprocess.run(
        ["gh", "repo", "list", "coolbress", "--limit", "100",
         "--json", "name,templateRepository",
         # 🔴 `templateRepository` 에 `nameWithOwner` 는 없다 — `name` + `owner.login` 이다.
         "--jq", f'.[] | select(.templateRepository.name=="{TEMPLATE_NAME}" '
                 f'and .templateRepository.owner.login=="{TEMPLATE_OWNER}") | .name'],
        capture_output=True, text=True, check=False,
    ).stdout
    return [f"coolbress/{n}" for n in out.splitlines() if n]


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
