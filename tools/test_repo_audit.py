"""`repo_audit` 자신을 검사한다.

왜 필요한가: 이 감사기는 **초록/빨강을 잘못 말한 전력이 있다.**
첫 판이 `204 No Content` 를 실패로 읽어 **켜져 있는 보안 기능을 꺼졌다고 보고**했다.
검사기가 거짓말하면 검사가 없는 것보다 나쁘다 — 없으면 최소한 안 믿는다.

그래서 `gh()` 를 가짜로 바꿔 **각 drift 를 하나씩 심고, 그것만 잡히는지** 본다.
"""

from __future__ import annotations

import unittest
from typing import Any

import repo_audit

CLEAN: dict[str, Any] = {
    "repos/x": {
        "allow_merge_commit": False,
        "allow_rebase_merge": False,
        "delete_branch_on_merge": True,
        "security_and_analysis": {
            "secret_scanning": {"status": "enabled"},
            "secret_scanning_push_protection": {"status": "enabled"},
            "dependabot_security_updates": {"status": "enabled"},
        },
    },
    "repos/x/vulnerability-alerts": True,  # 204 = 켜져 있다
    "repos/x/actions/permissions": {"sha_pinning_required": True, "allowed_actions": "selected"},
    "repos/x/rulesets": [{"id": 1}],
    "repos/x/code-scanning/default-setup": {"state": "configured"},
    "repos/x/rulesets/1": {
        "enforcement": "active",
        "bypass_actors": [],
        "rules": [
            {"type": "deletion"},
            {
                "type": "required_status_checks",
                "parameters": {
                    "required_status_checks": [
                        {"context": "ci / lint", "integration_id": repo_audit.ACTIONS_APP_ID}
                    ]
                },
            },
        ],
    },
}


def _both(overrides: dict[str, Any], status: int = 200) -> tuple[list[str], list[str]]:
    table = {**CLEAN, **overrides}
    orig_gh, orig_st = repo_audit.gh, repo_audit.gh_status
    repo_audit.gh = lambda path: table.get(path)  # type: ignore[assignment]
    repo_audit.gh_status = lambda path: status  # type: ignore[assignment]
    try:
        return repo_audit.audit("x")
    finally:
        repo_audit.gh, repo_audit.gh_status = orig_gh, orig_st  # type: ignore[assignment]


def _run(overrides: dict[str, Any]) -> list[str]:
    return _both(overrides)[0]


class TestRepoAudit(unittest.TestCase):
    def test_clean_repo_reports_nothing(self) -> None:
        self.assertEqual(_run({}), [])

    def test_204_is_enabled_not_failure(self) -> None:
        """첫 판이 틀렸던 바로 그 자리. True(=204)를 끄짐으로 읽으면 안 된다."""
        self.assertEqual(_run({}), [])
        self.assertIn("Dependabot 취약점 경보", " ".join(_run({"repos/x/vulnerability-alerts": None})))

    def test_merge_methods(self) -> None:
        got = _run({"repos/x": {**CLEAN["repos/x"], "allow_merge_commit": True}})
        self.assertIn("squash 전용이 아니다", " ".join(got))

    def test_secret_scanning_off(self) -> None:
        meta = {**CLEAN["repos/x"]}
        meta["security_and_analysis"] = {"secret_scanning": {"status": "disabled"}}
        self.assertEqual(len([g for g in _run({"repos/x": meta}) if g.startswith("보안:")]), 3)

    def test_sha_pinning_off(self) -> None:
        got = _run({"repos/x/actions/permissions": {"sha_pinning_required": False,
                                                    "allowed_actions": "selected"}})
        self.assertIn("서버 SHA 강제가 꺼짐", " ".join(got))

    def test_allowlist_off(self) -> None:
        """SHA 핀이 켜져 있어도 allowlist 가 꺼져 있으면 잡아야 한다 — 다른 문장이다."""
        got = _run({"repos/x/actions/permissions": {"sha_pinning_required": True,
                                                    "allowed_actions": "all"}})
        self.assertIn("allowlist 가 꺼짐", " ".join(got))
        self.assertNotIn("SHA", " ".join(got))

    def test_no_ruleset(self) -> None:
        self.assertEqual(_run({"repos/x/rulesets": []}), ["벽: 룰셋이 없다"])

    def test_bypass_actor_present(self) -> None:
        rs = {**CLEAN["repos/x/rulesets/1"], "bypass_actors": [{"actor_id": 5}]}
        self.assertIn("bypass_actors", " ".join(_run({"repos/x/rulesets/1": rs})))

    def test_check_source_not_pinned_to_actions_app(self) -> None:
        """이름만 요구하면 아무나 그 이름으로 초록을 올릴 수 있다."""
        rs = {
            **CLEAN["repos/x/rulesets/1"],
            "rules": [{"type": "required_status_checks",
                       "parameters": {"required_status_checks": [{"context": "ci / lint",
                                                                  "integration_id": 99999}]}}],
        }
        self.assertIn("출처가 안 묶임", " ".join(_run({"repos/x/rulesets/1": rs})))


class TestCodeQLAndUnknown(unittest.TestCase):
    def test_codeql_configured_is_clean(self) -> None:
        bad, unknown = _both({})
        self.assertEqual((bad, unknown), ([], []))

    def test_codeql_off_is_a_finding(self) -> None:
        bad, unknown = _both({"repos/x/code-scanning/default-setup": {"state": "not-configured"}})
        self.assertIn("CodeQL default setup 이 켜져 있지 않다", " ".join(bad))
        self.assertEqual(unknown, [])

    def test_403_is_unknown_not_a_finding(self) -> None:
        """🔴 이 파일이 존재하는 이유. 못 본 것을 '꺼짐' 으로 보고하면 안 된다.

        A-1 이후 에이전트 자격증명은 code-scanning 을 읽지 못한다(403).
        그건 정상 상태이므로 **빨강이 아니고**, 확인한 것도 아니므로 **초록도 아니다**.
        """
        bad, unknown = _both({"repos/x/code-scanning/default-setup": None}, status=403)
        self.assertEqual(bad, [])
        self.assertIn("읽을 권한이 없다", " ".join(unknown))


if __name__ == "__main__":
    unittest.main()
