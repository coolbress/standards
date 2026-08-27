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


def gh(path: str) -> object | None:
    """`gh api` 한 번. 실패는 None.

    ⚠️ 204 No Content 를 실패로 읽으면 안 된다 — `vulnerability-alerts` 는
    켜져 있을 때 **본문 없이 204** 를 준다. 첫 판이 이걸 실패로 읽어
    켜져 있는 것을 꺼졌다고 보고했다.
    """
    r = subprocess.run(
        ["gh", "api", path], capture_output=True, text=True,
        env={"PATH": "/usr/bin:/bin:/usr/local/bin:/opt/homebrew/bin", "HOME": subprocess.os.environ.get("HOME", "")},
    )
    if r.returncode != 0:
        return None
    if not r.stdout.strip():
        return True  # 204 = 켜져 있다
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        return None


def audit(repo: str) -> list[str]:
    """기대값과 다른 것만 문자열로 돌려준다."""
    bad: list[str] = []
    meta = gh(f"repos/{repo}") or {}

    # 머지 방법 — 룰셋 의도(squash 전용)와 저장소 설정이 같은 말을 해야 한다 (B-3)
    if meta.get("allow_merge_commit") or meta.get("allow_rebase_merge"):
        bad.append("머지: squash 전용이 아니다")
    if not meta.get("delete_branch_on_merge"):
        bad.append("머지: 브랜치 자동 삭제가 꺼짐")

    # 보안 바닥 (C-1)
    sa = meta.get("security_and_analysis") or {}
    for key, label in (("secret_scanning", "시크릿 탐지"),
                       ("secret_scanning_push_protection", "푸시 보호"),
                       ("dependabot_security_updates", "Dependabot 보안 업데이트")):
        if (sa.get(key) or {}).get("status") != "enabled":
            bad.append(f"보안: {label} 꺼짐")
    if gh(f"repos/{repo}/vulnerability-alerts") is None:
        bad.append("보안: Dependabot 취약점 경보 꺼짐")

    # Actions — 파일 습관이 아니라 서버가 SHA 를 강제해야 한다 (B-1)
    perms = gh(f"repos/{repo}/actions/permissions") or {}
    if not perms.get("sha_pinning_required"):
        bad.append("Actions: 서버 SHA 강제가 꺼짐")
    # SHA 핀은 "무엇을" 도는지는 안 정한다. 무엇이 돌 수 있는지는 allowlist 가 정한다.
    # 둘은 다른 문장이라 따로 검사한다.
    if perms.get("allowed_actions") != "selected":
        bad.append(f"Actions: allowlist 가 꺼짐 (allowed_actions={perms.get('allowed_actions')})")

    # 벽 (B-2)
    rulesets = gh(f"repos/{repo}/rulesets") or []
    if not rulesets:
        bad.append("벽: 룰셋이 없다")
        return bad
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
    return bad


def main() -> int:
    drift = 0
    for repo in REPOS:
        problems = audit(repo)
        drift += len(problems)
        print(f"{'🔴' if problems else '✅'} {repo}")
        for p in problems:
            print(f"     {p}")
    print(f"\nRESULT {'DRIFT' if drift else 'CLEAN'} findings={drift}")
    return 1 if drift else 0


if __name__ == "__main__":
    sys.exit(main())
