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

🔵 **2026-08-28 (2) — 재는 방식이 두 층이 됐다** (`project-template` v2.0.0).

템플릿 내용이 `template/` 아래로 내려가고(`_subdirectory`) 이름 치환이 jinja 로 들어가면서,
**저장소 루트의 파일 목록은 더 이상 인스턴스가 받는 것이 아니게 됐다.** 그대로 뒀더니
`missing_files=29` 가 나왔다 — **전부 가짜였다.** 그래서 두 가지를 고쳤다:

① **판 비교(주 신호)** — 인스턴스의 `_commit` 이 템플릿의 **최신 태그**와 같은가.
   copier 가 태그를 고르므로 이게 *"따라왔는가"* 의 **정확한 정의**다. 파일 목록보다 싸고 정확하다.
② **파일 비교(보조)** — `template/` 접두사를 벗기고, `.jinja` 접미사를 벗기고,
   **`{{ }}` 가 든 경로는 뺀다**(답에 따라 이름이 달라져 이름으로 비교할 수 없다).

읽기 전용이다.
"""

from __future__ import annotations

import base64
import re
import subprocess
import sys

TEMPLATE_OWNER = "coolbress"
TEMPLATE_NAME = "project-template"
TEMPLATE = f"{TEMPLATE_OWNER}/{TEMPLATE_NAME}"

#: 렌더 대상이 사는 곳. `copier.yml` 의 `_subdirectory` 와 같아야 한다.
#: 🔴 이걸 안 벗기면 템플릿의 모든 파일이 "인스턴스에 없다" 로 나온다 — 실제로 29개가 그랬다.
SUBDIR = "template/"

#: 아키타입과 무관하게 인스턴스로 안 가는 것.
BUILD_ONLY = ("dist/",)

#: `copier.yml` 의 **아키타입 조건부 제외** 줄 모양:
#: `- "{% if archetype not in ['web','backend','data-ml'] %}.env.example{% endif %}"`
#:
#: 🔴 **목록을 이 파일에 베껴두지 않는다.** 예전 판은 `.env.example` 과
#: `tests/test_env_example.py` 를 상수로 들고 있었다 — 템플릿이 규칙을 고치면 갈리고,
#: **갈렸다는 걸 아무도 모른다.** 이 저장소가 반복해 고쳐온 결함의 형태다.
#: 그래서 규칙은 **템플릿의 `copier.yml` 이 정본**이고 여기서 읽는다.
GATED_EXCLUDE = re.compile(
    r"\{%-?\s*if\s+archetype\s+not\s+in\s+\[(?P<archetypes>[^\]]*)\]\s*-?%\}"
    r"(?P<path>[^{}\n]+)"
    r"\{%-?\s*endif\s*-?%\}"
)


def parse_gated_excludes(body: str) -> list[tuple[frozenset[str], str]]:
    """*"이 아키타입이 아니면 이 파일은 안 만든다"* 규칙을 `copier.yml` 본문에서 읽는다.

    낸 것: `(허용 아키타입 집합, 인스턴스에서의 경로)` 목록. 네트워크를 안 탄다 — 시험 가능하다.
    """
    rules: list[tuple[frozenset[str], str]] = []
    for m in GATED_EXCLUDE.finditer(body):
        allowed = frozenset(
            a.strip().strip("\'\"") for a in m.group("archetypes").split(",") if a.strip()
        )
        path = m.group("path").strip()
        if allowed and path:
            rules.append((allowed, path))
    return rules


def _emitted(path: str) -> str | None:
    """템플릿 저장소의 경로를 **인스턴스에서 갖는 이름**으로 바꾼다. 비교 불가면 None."""
    if not path.startswith(SUBDIR):
        return None                      # 루트 = 템플릿 자신의 것. 인스턴스로 안 간다
    rel = path[len(SUBDIR):]
    if "{{" in rel:
        return None                      # 답에 따라 이름이 달라진다 — 이름으로 비교할 수 없다
    if rel.endswith(".jinja"):
        rel = rel[: -len(".jinja")]      # `.jinja` 는 렌더 지시이지 이름의 일부가 아니다
    return rel


def latest_tag() -> str | None:
    out = subprocess.run(
        ["gh", "api", f"repos/{TEMPLATE}/tags", "--jq", ".[0].name"],
        capture_output=True, text=True, check=False,
    )
    return out.stdout.strip() or None if out.returncode == 0 else None


def _decoded(repo: str, path: str) -> str | None:
    """저장소의 파일 하나를 텍스트로. 없거나 못 읽으면 None."""
    out = subprocess.run(
        ["gh", "api", f"repos/{repo}/contents/{path}",
         "--jq", ".content", "-H", "Accept: application/vnd.github+json"],
        capture_output=True, text=True, check=False,
    )
    if out.returncode != 0:
        return None
    try:
        return base64.b64decode(out.stdout.strip()).decode("utf-8")
    except (ValueError, UnicodeDecodeError):
        return None


def _answer(repo: str, key: str) -> str | None:
    body = _decoded(repo, ANSWERS)
    if body is None:
        return None
    for line in body.splitlines():
        if line.startswith(f"{key}:"):
            return line.split(":", 1)[1].strip()
    return None


def instance_commit(repo: str) -> str | None:
    """인스턴스가 어느 판에서 왔다고 적어두었나 (`.copier-answers.yml` 의 `_commit`)."""
    return _answer(repo, "_commit")


def instance_archetype(repo: str) -> str | None:
    """인스턴스가 어느 아키타입으로 태어났나. 조건부 파일 판정의 입력이다."""
    return _answer(repo, "archetype")


def gated_rules() -> list[tuple[frozenset[str], str]] | None:
    """템플릿의 `copier.yml` 에서 아키타입 조건부 제외 규칙을 읽는다. 못 읽으면 None."""
    body = _decoded(TEMPLATE, "copier.yml")
    if body is None:
        return None
    return parse_gated_excludes(body) or None


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
    """템플릿이 **내보내는** 이름들. 아키타입 조건은 여기서 안 본다 — 인스턴스마다 다르다."""
    emitted = {e for e in (_emitted(p) for p in paths) if e is not None}
    return {p for p in emitted if not any(p.startswith(g) or p == g for g in BUILD_ONLY)}


def classify(
    files: set[str],
    archetype: str | None,
    emitted: set[str],
    rules: list[tuple[frozenset[str], str]],
) -> tuple[list[str], list[str]]:
    """인스턴스 하나를 판정한다 — **없는 것**과 **남은 것** 둘 다.

    🔴 **남은 것(잉여)을 보는 것이 이 함수의 신설 이유다.** 예전 판은 *템플릿에서 인스턴스를 뺀 것*
    한 방향만 봤고, 그래서 `divcal`(cli)이 `.env.example` 을 **v2.2.0 까지 따라온 뒤에도**
    들고 있는 것을 아무도 못 봤다. `copier update` 는 **새로 제외 대상이 된 파일을 지우지 않는다.**

    아키타입을 못 읽으면 조건부 파일은 **어느 방향으로도 판정하지 않는다** — 모르는 것을
    안다고 말하지 않는다.
    """
    gated = {p for _, p in rules}
    allowed_here = {p for allowed, p in rules if archetype in allowed} if archetype else set()
    required = (emitted - gated) | allowed_here
    missing = sorted(required - files)
    extra = sorted(
        p for allowed, p in rules
        if archetype is not None and archetype not in allowed and p in files
    )
    return missing, extra


def main() -> int:
    print(f"템플릿 드리프트 — {TEMPLATE} 대비")

    # 🔴 **fail-closed.** 규칙을 못 읽었으면 `CLEAN` 이라고 말하지 않는다 —
    # 눈이 먼 채로 초록을 내는 검사는 없느니만 못하다(이 저장소가 여러 번 겪은 형태다).
    rules = gated_rules()
    if rules is None:
        print("  🔴 `copier.yml` 의 아키타입 조건부 제외 줄을 하나도 못 읽었다.")
        print("     템플릿을 못 읽었거나 규칙 모양이 바뀐 것이다 — `GATED_EXCLUDE` 를 고쳐라.")
        print("\nMETRIC gated_rules=0")
        print("RESULT BLIND — 규칙을 못 읽었으므로 판정하지 않는다")
        return 1

    repos = instances()
    if not repos:
        print("  인스턴스가 없다")
        return 0
    emitted = shared(_files(TEMPLATE))
    rows = [
        (repo, *classify(_files(repo), instance_archetype(repo), emitted, rules))
        for repo in repos
    ]
    tag = latest_tag()
    behind = 0
    stale = 0
    left = 0
    for repo, missing, extra in rows:
        # ① 판 비교 — copier 가 태그를 고르므로 이게 "따라왔는가" 의 정확한 정의다.
        at = instance_commit(repo)
        if tag and at and at != tag:
            stale += 1
            print(f"  🔶 {repo:30s} {at} → 최신은 {tag} · `copier update` 를 돌릴 때다")
        elif tag and at:
            print(f"  ✅ {repo:30s} {at} (최신)")
        else:
            print(f"  ❔ {repo:30s} 판을 못 읽었다 (tag={tag} commit={at})")
        # ② 파일 비교 — 판이 같아도 손으로 지운 것이 있을 수 있다.
        for m in missing:
            print(f"       ↳ 없는 파일: {m}")
        # ③ 잉여 비교 — `copier update` 는 새로 제외 대상이 된 파일을 **지우지 않는다.**
        for e in extra:
            print(f"       ↳ 🔴 아키타입에 안 맞는데 남아 있는 파일: {e}")
        behind += len(missing)
        left += len(extra)
    print(f"\nMETRIC instances={len(rows)} stale_versions={stale} "
          f"missing_files={behind} extra_files={left} gated_rules={len(rules)}")
    if behind or stale or left:
        print("RESULT DRIFT — 인스턴스가 템플릿을 안 따라왔다. `copier update` 를 돌리고 PR 을 열어라")
        print("  ⚠️ 파일 10개 이상이거나 인스턴스 3개 이상이면 GAPS R5-32(copier)를 다시 연다")
        return 1
    print("RESULT CLEAN — 인스턴스가 템플릿을 따라와 있다")
    return 0


if __name__ == "__main__":
    sys.exit(main())
