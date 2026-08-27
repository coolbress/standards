#!/usr/bin/env python3
"""서버 설정 drift 감사 — 읽기만 한다.

왜 여기(`standards`)에 있나: 감사 문서 B-4 가 *"같은 저장소 안의 수정 가능한
workflow 하나만 믿지 않는다"* 고 규정한다. 감사 대상이 감사자를 수정할 수 있으면
감사가 아니다. 그래서 대상 저장소 밖에서 돌린다.

무엇을 하지 않나: **아무것도 고치지 않는다.** 기대값과 실제값의 차이만 보고한다.
고치는 것은 사람의 결정이다.
"""

from __future__ import annotations

import json
import subprocess
import sys

REPOS = ["coolbress/standards", "coolbress/workflows", "coolbress/project-template"]
ACTIONS_APP_ID = 15368  # GitHub Actions — required check 의 유일한 인정 출처


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
    for key in ("GH_TOKEN", "GITHUB_TOKEN"):
        if subprocess.os.environ.get(key):
            env[key] = subprocess.os.environ[key]
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
    rs = gh(f"repos/{repo}/rulesets/{rulesets[0]['id']}") or {}
    if rs.get("enforcement") != "active":
        bad.append(f"벽: enforcement={rs.get('enforcement')}")
    if rs.get("bypass_actors"):
        bad.append(f"벽: bypass_actors 가 비어 있지 않다 ({len(rs['bypass_actors'])}건)")
    for rule in rs.get("rules", []):
        if rule["type"] != "required_status_checks":
            continue
        for check in rule["parameters"]["required_status_checks"]:
            if check.get("integration_id") != ACTIONS_APP_ID:
                bad.append(f"벽: '{check['context']}' 의 출처가 안 묶임 (다른 앱도 이 이름을 보고할 수 있다)")
    return bad, unknown


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
