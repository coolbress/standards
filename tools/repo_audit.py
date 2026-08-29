#!/usr/bin/env python3
"""서버 설정 drift 감사 — 읽기만 한다.

왜 여기(`standards`)에 있나: 감사 문서 B-4 가 *"같은 저장소 안의 수정 가능한
workflow 하나만 믿지 않는다"* 고 규정한다. 감사 대상이 감사자를 수정할 수 있으면
감사가 아니다. 그래서 대상 저장소 밖에서 돌린다.

무엇을 하지 않나: **아무것도 고치지 않는다.** 기대값과 실제값의 차이만 보고한다.
고치는 것은 사람의 결정이다.
"""

from __future__ import annotations

import re

import base64

import json
import subprocess
import sys

# 감사 대상. **새 프로젝트를 만들면 여기에 한 줄 더한다** —
# 템플릿에서 뜬 프로젝트는 기대값이 전부 같으므로(아래 PROJECT_*) 그 한 줄이면 끝난다.
# 🔴 여기 없으면 감사되지 않는다. 만든 저장소가 감사 밖에 있으면 벽이 있는지 아무도 안 본다.
REPOS = [
    "coolbress/standards",
    "coolbress/workflows",
    "coolbress/project-template",
    "coolbress/divcal",  # 2026-08-27 · 첫 완주 프로젝트
]
ACTIONS_APP_ID = 15368        # GitHub Actions
CODE_SCANNING_APP_ID = 57789  # github-advanced-security (CodeQL 집계 검사)

# 검사 이름 → 그 이름을 보고해도 되는 **유일한** 앱.
# 🔴 여기 없는 이름은 GitHub Actions(15368) 여야 한다 — 기본을 느슨하게 두지 않는다.
# 왜 지도가 필요한가: 처음엔 "출처는 전부 15368" 로 하드코딩돼 있었다.
# CodeQL 을 required 로 올리자 **정당하게 다른 앱에 묶인 것을 "안 묶임" 으로** 읽었다.
# 검사기의 '맞음' 모델이 현실을 못 따라가면 그때부터 검사기가 거짓말을 한다.
EXPECTED_APP: dict[str, int] = {"CodeQL": CODE_SCANNING_APP_ID}

# 🔴 저장소별로 **어떤 검사가 있어야 하는가.**
# 왜 필요한가: 이전 판은 *"있는 검사의 출처가 맞는가"* 만 봤다. 그러면
# **누가 CodeQL·secrets·canary 를 룰셋에서 지워도 감사기가 초록을 말한다.**
# drift 감사의 일이 정확히 그걸 잡는 것이다. 기대값을 적어 두지 않으면 비교할 것이 없다.
# 검사를 늘리거나 줄이려면 **여기를 같이 고친다** — 그게 "의도한 변경" 의 증거다.
# ── 템플릿에서 뜬 프로젝트의 기본 기대값 ─────────────────────────
# `new-project.sh` 가 거는 것과 **같아야 한다.** 둘이 갈라지면 새 저장소가
# 태어나자마자 drift 로 잡히거나(예전에 그랬다) 잡혀야 할 것이 안 잡힌다.
PROJECT_CHECKS = {
    "CodeQL",
    "ci / pr-title", "ci / lint", "ci / typecheck", "ci / test", "ci / build", "ci / secrets",
    "ci / diff-size",
}
PROJECT_ACTION_PATTERNS = ["astral-sh/setup-uv@*", "coolbress/workflows/*"]

# Actions allowlist 에 허용된 패턴. `selected` 인 것만 보면 **패턴이 넓어져도 모른다.**
# 여기 없는 저장소는 위 PROJECT_* 를 기대값으로 쓴다.
EXPECTED_ACTION_PATTERNS: dict[str, list[str]] = {
    "coolbress/standards": [],
    "coolbress/workflows": ["astral-sh/setup-uv@*"],
    # 🔴 `coolbress/workflows/*` 가 필요하다 — `uses:` 로 부르는 재사용 워크플로도
    # allowlist 대상이다. 빠지면 첫 CI 가 startup_failure 로 죽어 저장소가 잠긴다.
    "coolbress/project-template": ["astral-sh/setup-uv@*", "coolbress/workflows/*"],
}

EXPECTED_CHECKS: dict[str, set[str]] = {
    "coolbress/standards": {"integrity", "CodeQL"},
    # 🔴 여기만 `canary / *` 다 — 이 저장소의 호출잡 이름이 `ci` 가 아니라 `canary` 라서다.
    # 검사 이름은 {호출잡}/{피호출잡} 이므로 `ci / diff-size` 를 걸면 그 이름이
    # 영원히 보고되지 않아 자기잠금이 된다 (workflows v3.3.0 노트).
    "coolbress/workflows": {
        "integrity", "CodeQL",
        "canary / pr-title", "canary / lint", "canary / typecheck", "canary / test",
        "canary / build", "canary / secrets", "canary / diff-size",
    },
    "coolbress/project-template": {
        "CodeQL",
        "ci / pr-title", "ci / lint", "ci / typecheck", "ci / test", "ci / build", "ci / secrets",
        "ci / diff-size",
    },
}


def _env() -> dict[str, str]:
    """`gh` 에 넘길 환경.

    🔴 **토큰을 반드시 물려준다.** 안 넘기면 `gh` 가 keyring 의 **관리자 자격증명**으로
    떨어진다 — 그러면 이 감사기가 *에이전트가 볼 수 있는 것*이 아니라
    *관리자가 볼 수 있는 것*을 보고하게 된다. **`env -u GH_TOKEN` 을 코드로 하는 것과 같다.**
    (A-1 권한 분리 · `audit/TEMPLATE-WORKFLOWS-AUDIT` §A-1 이 금지하는 바로 그 행위다.)

    감사기는 **에이전트와 같은 눈**으로 봐야 한다. 못 보는 것은 `unknown` 으로 보고한다.
    """
    env = {"PATH": "/usr/bin:/bin:/usr/local/bin:/opt/homebrew/bin",
           "HOME": subprocess.os.environ.get("HOME", "")}
    found = False
    for key in ("GH_TOKEN", "GITHUB_TOKEN"):
        if subprocess.os.environ.get(key):
            env[key] = subprocess.os.environ[key]
            found = True
    if not found:
        # 🔴 fail-closed. 토큰이 없으면 `gh` 가 **keyring 의 관리자 자격증명**으로 떨어진다.
        # 그러면 이 감사기가 *에이전트가 볼 수 있는 것*이 아니라 *관리자가 볼 수 있는 것*을
        # 보고한다 — 조용히. 주석으로 "물려준다" 고 써 두는 것으로는 안 된다.
        sys.exit(
            "🔴 GH_TOKEN(또는 GITHUB_TOKEN)이 없다. 이 감사기는 **에이전트와 같은 눈**으로\n"
            "   봐야 하므로 keyring 으로 떨어지지 않고 여기서 멈춘다.\n"
            "   사람이 관리자 눈으로 보려면 토큰을 명시적으로 넘겨라:\n"
            "     ~/workflows/tools/with-admin-token.sh python3 tools/repo_audit.py\n"
            "   🔴 `GH_TOKEN=<토큰> 명령` 형태로 쓰지 마라 — 셸 히스토리에 남는다.\n"
            "   ⚠️ 이건 **사고를 막는 장치**다. 같은 OS 사용자면 어떤 프로세스든 keyring 에\n"
            "      닿을 수 있으므로, 진짜 경계는 OS 수준 분리가 필요하다."
        )
    return env


def gh(path: str) -> object | None:
    """`gh api` 한 번. 실패는 None.

    ⚠️ 204 No Content 를 실패로 읽으면 안 된다 — `vulnerability-alerts` 는
    켜져 있을 때 **본문 없이 204** 를 준다. 첫 판이 이걸 실패로 읽어
    켜져 있는 것을 꺼졌다고 보고했다.
    """
    r = subprocess.run(["gh", "api", path], capture_output=True, text=True, env=_env())
    if r.returncode != 0:
        return None
    if not r.stdout.strip():
        return True  # 204 = 켜져 있다
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        return None


def gh_status(path: str) -> int:
    """HTTP 상태 코드만 돌려준다. 0 = 알 수 없음.

    🔴 왜 `gh()` 로는 부족한가: `gh()` 는 모든 실패를 None 으로 뭉갠다.
    그러면 **"권한이 없어 못 봤다"(403)** 와 **"꺼져 있다"** 를 구별할 수 없다.
    A-1(권한 분리) 이후 에이전트 자격증명은 code-scanning 을 **읽지도 못한다** —
    그걸 "꺼짐" 으로 보고하면 이 감사기가 또 거짓말을 하는 것이다.
    """
    r = subprocess.run(["gh", "api", path, "-i"], capture_output=True, text=True, env=_env())
    for line in (r.stdout or r.stderr).splitlines():
        if line.startswith("HTTP/"):
            parts = line.split()
            if len(parts) > 1 and parts[1].isdigit():
                return int(parts[1])
    return 0


def audit(repo: str) -> tuple[list[str], list[str]]:
    """(어긋난 것, 확인하지 못한 것) 을 돌려준다.

    🔴 둘을 가르는 이유: **"검사했는데 틀렸다"** 와 **"검사하지 못했다"** 는 다른 문장이다.
    뭉치면 감사기가 초록/빨강을 잘못 말한다 — 이 파일이 두 번 그랬다:
      ① 204 No Content 를 실패로 읽어 **켜진 기능을 꺼졌다고** 보고했다
      ② A-1 이후 에이전트 토큰으로 돌리자 **권한이 없어 안 보이는 것**을 전부 *"꺼짐"* 으로
         읽어 **거짓 결함 18건**을 냈다

    이 감사기가 보는 것은 대부분 **관리자만 읽을 수 있는 서버 설정**이다.
    그래서 자격증명에 `Administration: Read-only` 가 없으면 **거의 아무것도 확인할 수 없고**,
    그때는 CLEAN 이라고 말하면 안 된다 — **눈 감은 감사기의 초록이 가장 나쁘다.**
    """
    bad: list[str] = []
    unknown: list[str] = []

    def blocked(path: str) -> bool:
        return gh_status(path) in (403, 404)

    meta = gh(f"repos/{repo}") or {}
    if not isinstance(meta, dict) or "name" not in meta:
        unknown.append("저장소 메타데이터를 읽지 못했다")
        return bad, unknown

    # 머지 방법 — 룰셋 의도(squash 전용)와 저장소 설정이 같은 말을 해야 한다 (B-3)
    if meta.get("allow_merge_commit") or meta.get("allow_rebase_merge"):
        bad.append("머지: squash 전용이 아니다")
    # squash 까지 꺼지면 **머지 버튼이 하나도 없다** — 룰셋은 멀쩡한데 아무것도 못 들어간다.
    if not meta.get("allow_squash_merge"):
        bad.append("머지: squash 도 꺼져 있다 (머지할 방법이 없다)")
    if not meta.get("delete_branch_on_merge"):
        bad.append("머지: 브랜치 자동 삭제가 꺼짐")

    # 보안 바닥 (C-1) — `security_and_analysis` 는 **관리자에게만** 실려 온다.
    # 없다는 것은 "꺼짐" 이 아니라 "못 봤다" 다.
    if "security_and_analysis" not in meta:
        unknown.append("보안: 시크릿 탐지·푸시 보호·Dependabot 을 읽을 권한이 없다")
    else:
        sa = meta["security_and_analysis"] or {}
        for key, label in (("secret_scanning", "시크릿 탐지"),
                           ("secret_scanning_push_protection", "푸시 보호"),
                           ("dependabot_security_updates", "Dependabot 보안 업데이트")):
            if (sa.get(key) or {}).get("status") != "enabled":
                bad.append(f"보안: {label} 꺼짐")

    if blocked(f"repos/{repo}/vulnerability-alerts"):
        unknown.append("보안: Dependabot 취약점 경보를 읽을 권한이 없다")
    elif gh(f"repos/{repo}/vulnerability-alerts") is None:
        bad.append("보안: Dependabot 취약점 경보 꺼짐")

    # Actions — 파일 습관이 아니라 서버가 강제해야 한다 (B-1)
    if blocked(f"repos/{repo}/actions/permissions"):
        unknown.append("Actions: 정책(SHA 강제·allowlist)을 읽을 권한이 없다")
    else:
        perms = gh(f"repos/{repo}/actions/permissions") or {}
        if not perms.get("sha_pinning_required"):
            bad.append("Actions: 서버 SHA 강제가 꺼짐")
        # SHA 핀은 "무엇이 바뀌지 않는가", allowlist 는 "무엇이 돌 수 있는가" — 다른 문장이다.
        if perms.get("allowed_actions") != "selected":
            bad.append(f"Actions: allowlist 가 꺼짐 (allowed_actions={perms.get('allowed_actions')})")
        else:
            # 🔴 `selected` 인 것만 보면 **목록이 넓어져도 모른다.**
            sel = gh(f"repos/{repo}/actions/permissions/selected-actions") or {}
            if not sel.get("github_owned_allowed"):
                bad.append("Actions: GitHub 소유 Action 이 막혀 있다 (checkout 이 안 돈다)")
            if sel.get("verified_allowed"):
                bad.append("Actions: verified_allowed 가 켜짐 — 검증 마켓플레이스 전체가 열린다")
            want_pat = EXPECTED_ACTION_PATTERNS.get(repo, PROJECT_ACTION_PATTERNS)
            got_pat = sorted(sel.get("patterns_allowed") or [])
            if got_pat != sorted(want_pat):
                bad.append(f"Actions: allowlist 패턴이 다르다 (기대 {sorted(want_pat)}, 실제 {got_pat})")

    # SAST — 공개 저장소는 CodeQL default setup 이다 (소유자 결정 2026-08-27)
    if blocked(f"repos/{repo}/code-scanning/default-setup"):
        unknown.append("SAST: CodeQL 설정을 읽을 권한이 없다")
    else:
        setup = gh(f"repos/{repo}/code-scanning/default-setup")
        state = setup.get("state") if isinstance(setup, dict) else None
        if state != "configured":
            bad.append(f"SAST: CodeQL default setup 이 켜져 있지 않다 (state={state})")

    # 벽 (B-2)
    if blocked(f"repos/{repo}/rulesets"):
        unknown.append("벽: 룰셋을 읽을 권한이 없다")
        return bad, unknown
    rulesets = gh(f"repos/{repo}/rulesets") or []
    if not rulesets:
        bad.append("벽: 룰셋이 없다")
        return bad, unknown
    # 🔴 [0] 만 보면 **룰셋이 여러 개일 때 엉뚱한 것을 본다.**
    # 하나만 있어야 한다 — 여러 개면 어느 것이 진짜 벽인지 사람이 정해야 한다.
    if len(rulesets) > 1:
        names = ", ".join(str(r.get("name")) for r in rulesets)
        bad.append(f"벽: 룰셋이 {len(rulesets)}개다 ({names}) — 어느 것이 벽인지 불명확하다")
    rs = gh(f"repos/{repo}/rulesets/{rulesets[0]['id']}") or {}
    if rs.get("enforcement") != "active":
        bad.append(f"벽: enforcement={rs.get('enforcement')}")
    if rs.get("bypass_actors"):
        bad.append(f"벽: bypass_actors 가 비어 있지 않다 ({len(rs['bypass_actors'])}건)")
    # 어떤 브랜치를 지키는가 — 기본 브랜치가 아니면 벽이 엉뚱한 곳에 서 있는 것이다.
    include = ((rs.get("conditions") or {}).get("ref_name") or {}).get("include")
    if include != ["~DEFAULT_BRANCH"]:
        bad.append(f"벽: 대상이 기본 브랜치가 아니다 (include={include})")

    # 🔴 규칙 자체가 사라졌는지 본다. 출처만 보면 **규칙이 통째로 지워져도 초록**이다.
    types = {r["type"] for r in rs.get("rules", [])}
    for t, label in (("deletion", "기본 브랜치 삭제 금지"),
                     ("non_fast_forward", "강제 푸시 금지"),
                     ("pull_request", "PR 필수"),
                     ("required_status_checks", "검사 필수")):
        if t not in types:
            bad.append(f"벽: '{label}' 규칙이 없다")

    pr_rule = next((r for r in rs.get("rules", []) if r["type"] == "pull_request"), None)
    if pr_rule:
        if (pr_rule["parameters"].get("allowed_merge_methods") or []) != ["squash"]:
            bad.append("벽: 머지 방법이 squash 전용이 아니다")
        # 현행 정책은 0 이다 (A-2, 소유자 결정) — 솔로는 자기 PR 을 승인할 수 없다.
        # 0 이 아니게 되면 **머지가 영원히 막힌다.** 정책을 바꿨다면 여기도 바꿔라.
        approvals = pr_rule["parameters"].get("required_approving_review_count")
        if approvals != 0:
            bad.append(f"벽: 필수 승인 수가 {approvals} 다 — 솔로는 자기 PR 을 승인할 수 없어 머지가 막힌다")

    for rule in rs.get("rules", []):
        if rule["type"] != "required_status_checks":
            continue
        params = rule["parameters"]
        if not params.get("strict_required_status_checks_policy"):
            bad.append("벽: strict 가 꺼짐 (낡은 main 위의 초록이 인정된다)")
        # 🔴 완전성 — 기대한 검사가 **전부 있는가**. 없으면 누가 지워도 초록이다.
        actual = {c["context"] for c in params["required_status_checks"]}
        want = EXPECTED_CHECKS.get(repo, PROJECT_CHECKS)
        for miss in sorted(want - actual):
            bad.append(f"벽: 요구 검사 '{miss}' 가 사라졌다")
        for extra in sorted(actual - want):
            bad.append(f"벽: 기대하지 않은 요구 검사 '{extra}' — 의도한 변경이면 EXPECTED_CHECKS 를 고쳐라")
        for check in rule["parameters"]["required_status_checks"]:
            ctx = check["context"]
            want = EXPECTED_APP.get(ctx, ACTIONS_APP_ID)
            got = check.get("integration_id")
            if got != want:
                bad.append(
                    f"벽: '{ctx}' 의 출처가 안 묶였거나 틀렸다 (기대 app {want}, 실제 {got})"
                )
            # 🔴 언어별 CodeQL 잡을 요구하면 안 된다 — 저장소마다 언어가 다르다.
            # 없는 언어를 요구하면 그 이름이 영원히 보고되지 않아 저장소가 잠긴다.
            if ctx.startswith("Analyze ("):
                bad.append(f"벽: '{ctx}' 는 언어별 잡이라 요구하면 안 된다 (저장소가 잠긴다)")
    return bad, unknown


def archetype_vocabulary_drift() -> list[str]:
    """템플릿이 **묻는 아키타입**과 코퍼스가 **게이트에 쓰는 종류**가 같은가.

    🔴 2026-08-28 실측: 갈려 있었다. 코퍼스는 10종을 쓰는데 `copier.yml` 은 4종을 묻고
    **`service` 는 코퍼스에 아예 없었다** — `/kickoff` 에서 *service* 라고 답하면
    **게이트 걸린 측면 어디에도 안 걸린다.** 층이 답 위에 서 있는데 답이 어휘 밖이었다.

    정본은 코퍼스다. 그 값들은 리서치에서 나왔고, 템플릿 질문은 그 아래다.
    """
    from validate_corpus import ARCHETYPE_KINDS

    raw = subprocess.run(
        ["gh", "api", "repos/coolbress/project-template/contents/copier.yml",
         "--jq", ".content"],
        capture_output=True, text=True, check=False,
    )
    if raw.returncode != 0 or not raw.stdout.strip():
        return ["⚪ 템플릿의 copier.yml 을 못 읽었다"]
    body = base64.b64decode(raw.stdout.strip()).decode("utf-8")
    block = body.split("\narchetype:", 1)
    if len(block) < 2:
        return ["템플릿에 archetype 질문이 없다"]
    offered = set(re.findall(r"^\s{4}[^:\n]+:\s*([a-z][a-z0-9-]*)\s*$", block[1], re.M))
    extra = sorted(offered - ARCHETYPE_KINDS)
    if extra:
        return [f"템플릿이 코퍼스에 없는 아키타입을 묻는다: {extra} "
                f"(코퍼스 종류 축: {sorted(ARCHETYPE_KINDS)})"]
    return []


def main() -> int:
    drift = 0
    unknowns = 0
    for repo in REPOS:
        problems, unknown = audit(repo)
        drift += len(problems)
        unknowns += len(unknown)
        mark = "🔴" if problems else ("🟡" if unknown else "✅")
        print(f"{mark} {repo}")
        for p in problems:
            print(f"     {p}")
        for u in unknown:
            print(f"     ⚪ {u}")
    # R5-37: 회부 기록 수단(라벨)이 **실제로 깔려 있나.** 서버 사실이라 여기서 본다 —
    # 단위 시험은 네트워크를 안 탄다.
    from check_decision_referrals import LABEL, RESIMPLE, labels_installed

    no_labels = [r for r in ("standards", "workflows", "project-template", "divcal")
                 if not labels_installed(r)]
    if no_labels:
        print(f"🔴 회부 기록 수단 — 라벨 미설치: {', '.join(no_labels)} "
              f"(`{LABEL}`·`{RESIMPLE}`)")
        drift += len(no_labels)
    else:
        print(f"✅ 회부 기록 수단 — 네 저장소에 `{LABEL}`·`{RESIMPLE}` 라벨이 있다")

    # R5-38: 바닥의 **문서 묶음**을 아무도 안 보고 있었다 — 이 감사기는 서버 설정만 보고
    # `check_floor_coverage` 는 *바닥이 입장을 갖는가* 만 본다. 그 틈에서 두 저장소가
    # `AGENTS.md` 없이 서 있었다(`POC-001` — 측정된 계획 산출물 중 채택률 1위).
    # 🔵 `CLAUDE.md` 가 **심볼릭 링크인지**까지 본다 — 사본을 두면 둘이 갈린다(`CAS-001`).
    doc_gaps: list[str] = []
    for repo in ("standards", "workflows", "project-template", "divcal"):
        agents = gh(f"repos/coolbress/{repo}/contents/AGENTS.md")
        if agents is None:
            doc_gaps.append(f"{repo}: AGENTS.md 가 없다")
            continue
        # 🔴 `contents` API 는 **심볼릭을 따라가** `type: file` 로 준다.
        # 링크인지 보려면 **git tree 의 모드**(`120000`)를 봐야 한다 — 2026-08-29 실측.
        tree = gh(f"repos/coolbress/{repo}/git/trees/HEAD")
        entries = tree.get("tree", []) if isinstance(tree, dict) else []
        claude = next((e for e in entries if e.get("path") == "CLAUDE.md"), None)
        if claude is None:
            doc_gaps.append(f"{repo}: CLAUDE.md 가 없다")
        elif claude.get("mode") != "120000":
            doc_gaps.append(f"{repo}: CLAUDE.md 가 심볼릭 링크가 아니다 (사본은 갈린다)")
    if doc_gaps:
        print("🔴 문서 묶음 — AGENTS.md / CLAUDE.md")
        for d in doc_gaps:
            print(f"     {d}")
        drift += len(doc_gaps)
    else:
        print("✅ 문서 묶음 — 네 저장소에 AGENTS.md 가 있고 CLAUDE.md 는 심볼릭 링크다")

    vocab = archetype_vocabulary_drift()
    if vocab:
        unknown_only = all(v.startswith("⚪") for v in vocab)
        mark = "🟡" if unknown_only else "🔴"
        print(f"{mark} 아키타입 어휘 — 템플릿 질문 vs 코퍼스 게이트")
        for v in vocab:
            print(f"     {v}")
        if unknown_only:
            unknowns += len(vocab)
        else:
            drift += len(vocab)
    else:
        print("✅ 아키타입 어휘 — 템플릿 질문이 코퍼스 종류 축 안에 있다")

    # 🔴 **눈 감은 감사기의 초록이 가장 나쁘다.** 확인하지 못한 것이 있으면 CLEAN 이라 하지 않는다.
    verdict = "DRIFT" if drift else ("INCONCLUSIVE" if unknowns else "CLEAN")
    print(f"\nRESULT {verdict} findings={drift} unknown={unknowns}")
    if unknowns:
        print("\n⚪ 확인하지 못한 것이 있다. 이 감사기가 보는 것은 대부분 **관리자만 읽을 수 있는**")
        print("   서버 설정이다. 자격증명에 `Administration: Read-only` 를 주면 전부 확인된다 —")
        print("   **읽기만 주는 것이 요점이다. 벽을 읽되 옮기지는 못한다.**")
    if drift:
        return 1
    return 2 if unknowns else 0


if __name__ == "__main__":
    sys.exit(main())
