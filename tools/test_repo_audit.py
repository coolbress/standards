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
        "name": "x",
        "allow_merge_commit": False,
        "allow_rebase_merge": False,
        "allow_squash_merge": True,
        "delete_branch_on_merge": True,
        "security_and_analysis": {
            "secret_scanning": {"status": "enabled"},
            "secret_scanning_push_protection": {"status": "enabled"},
            "dependabot_security_updates": {"status": "enabled"},
        },
    },
    "repos/x/vulnerability-alerts": True,  # 204 = 켜져 있다
    "repos/x/actions/permissions": {"sha_pinning_required": True, "allowed_actions": "selected"},
    "repos/x/actions/permissions/workflow": {
        "default_workflow_permissions": "read", "can_approve_pull_request_reviews": False},
    "repos/x/actions/permissions/selected-actions": {
        "github_owned_allowed": True, "verified_allowed": False, "patterns_allowed": []},
    "repos/x/rulesets": [{"id": 1}],
    "repos/x/code-scanning/default-setup": {"state": "configured"},
    "repos/x/rulesets/1": {
        "enforcement": "active",
        "bypass_actors": [],
        "conditions": {"ref_name": {"include": ["~DEFAULT_BRANCH"], "exclude": []}},
        "rules": [
            {"type": "deletion"},
            {"type": "non_fast_forward"},
            {"type": "pull_request", "parameters": {"allowed_merge_methods": ["squash"],
                                                    "required_approving_review_count": 0}},
            {
                "type": "required_status_checks",
                "parameters": {
                    "strict_required_status_checks_policy": True,
                    "required_status_checks": [
                        {"context": "ci / lint", "integration_id": repo_audit.ACTIONS_APP_ID}
                    ],
                },
            },
        ],
    },
}

# 시험용 기대값 — 실제 저장소 표를 건드리지 않는다.
repo_audit.EXPECTED_CHECKS["x"] = {"ci / lint"}
repo_audit.EXPECTED_ACTION_PATTERNS["x"] = []


def _both(overrides: dict[str, Any], status: int = 200) -> tuple[list[str], list[str]]:
    table = {**CLEAN, **overrides}
    orig_gh, orig_st = repo_audit.gh, repo_audit.gh_status
    repo_audit.gh = lambda path: table.get(path)
    repo_audit.gh_status = lambda path: status
    try:
        return repo_audit.audit("x")
    finally:
        repo_audit.gh, repo_audit.gh_status = orig_gh, orig_st


def _run(overrides: dict[str, Any]) -> list[str]:
    return _both(overrides)[0]


def _with_checks(checks: list[dict[str, Any]], expected: set[str]) -> list[str]:
    """요구 검사 목록만 바꾼 룰셋으로 돌린다 (나머지 규칙은 정상 상태로 둔다)."""
    rs = {**CLEAN["repos/x/rulesets/1"]}
    rs["rules"] = [dict(r) for r in rs["rules"]]
    rs["rules"][-1] = {"type": "required_status_checks",
                       "parameters": {"strict_required_status_checks_policy": True,
                                      "required_status_checks": checks}}
    saved = repo_audit.EXPECTED_CHECKS["x"]
    repo_audit.EXPECTED_CHECKS["x"] = expected
    try:
        return _run({"repos/x/rulesets/1": rs})
    finally:
        repo_audit.EXPECTED_CHECKS["x"] = saved


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

    def test_missing_security_block_is_unknown_not_disabled(self) -> None:
        """🔴 A-1 이후 이 감사기가 두 번째로 거짓말할 뻔한 자리.

        `security_and_analysis` 는 **관리자에게만** 실려 온다. 없다는 것은
        "꺼짐" 이 아니라 "못 봤다" 다. 에이전트 토큰으로 돌렸더니 이걸
        꺼짐으로 읽어 **거짓 결함 18건**이 났었다.
        """
        meta = {k: v for k, v in CLEAN["repos/x"].items() if k != "security_and_analysis"}
        bad, unknown = _both({"repos/x": meta})
        self.assertFalse([g for g in bad if g.startswith("보안: 시크릿")])
        self.assertIn("읽을 권한이 없다", " ".join(unknown))

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

    def test_codeql_may_come_from_the_code_scanning_app(self) -> None:
        """🔴 감사기가 세 번째로 거짓말할 뻔한 자리.

        출처를 15368 하나로 하드코딩해 뒀더니, CodeQL 을 required 로 올리는 순간
        **정당하게 다른 앱에 묶인 것을 "안 묶임" 으로** 읽었다.
        """
        self.assertEqual(_with_checks(
            [{"context": "ci / lint", "integration_id": repo_audit.ACTIONS_APP_ID},
             {"context": "CodeQL", "integration_id": repo_audit.CODE_SCANNING_APP_ID}],
            {"ci / lint", "CodeQL"}), [])

    def test_codeql_from_the_wrong_app_is_a_finding(self) -> None:
        self.assertIn("출처가 안 묶였거나 틀렸다", " ".join(_with_checks(
            [{"context": "CodeQL", "integration_id": repo_audit.ACTIONS_APP_ID}], {"CodeQL"})))

    def test_language_specific_analyze_job_must_not_be_required(self) -> None:
        """저장소마다 언어가 다르다. 없는 언어를 요구하면 저장소가 잠긴다."""
        self.assertIn("저장소가 잠긴다", " ".join(_with_checks(
            [{"context": "Analyze (python)", "integration_id": repo_audit.ACTIONS_APP_ID}],
            {"Analyze (python)"})))

    def test_check_source_not_pinned_to_actions_app(self) -> None:
        """이름만 요구하면 아무나 그 이름으로 초록을 올릴 수 있다."""
        self.assertIn("출처가 안 묶였거나 틀렸다", " ".join(_with_checks(
            [{"context": "ci / lint", "integration_id": 99999}], {"ci / lint"})))


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


class TestFailClosed(unittest.TestCase):
    """토큰이 없으면 keyring 으로 떨어지지 않고 **멈춘다.**

    🔴 회귀 시험이 필요한 이유: 이 성질은 주석으로 두 판을 버텼는데
    **구현이 안 돼 있었다.** 문서가 아니라 시험이 지켜야 한다.
    """

    def test_no_token_exits(self) -> None:
        import os
        from unittest import mock

        # `/tmp` 에 쓰지 않는다 — gh 설정이 없는 HOME 을 흉내내는 값일 뿐이다
        with (mock.patch.dict(os.environ, {"HOME": "/tmp"}, clear=True),  # noqa: S108
              self.assertRaises(SystemExit) as cm):
            repo_audit._env()
        self.assertIn("GH_TOKEN", str(cm.exception))

    def test_token_is_passed_through(self) -> None:
        import os
        from unittest import mock

        with mock.patch.dict(os.environ, {"HOME": "/tmp", "GH_TOKEN": "t"}, clear=True):  # noqa: S108 — 위와 같다
            self.assertEqual(repo_audit._env().get("GH_TOKEN"), "t")


class TestActionsAllowlist(unittest.TestCase):
    def test_widened_patterns_are_caught(self) -> None:
        sel = {"github_owned_allowed": True, "verified_allowed": False,
               "patterns_allowed": ["*"]}
        self.assertIn("allowlist 패턴이 다르다",
                      " ".join(_run({"repos/x/actions/permissions/selected-actions": sel})))

    def test_verified_allowed_is_caught(self) -> None:
        sel = {"github_owned_allowed": True, "verified_allowed": True, "patterns_allowed": []}
        self.assertIn("verified_allowed 가 켜짐",
                      " ".join(_run({"repos/x/actions/permissions/selected-actions": sel})))


class TestWallCompleteness(unittest.TestCase):
    """🔴 이전 판은 *"있는 검사의 출처가 맞는가"* 만 봤다.

    그러면 **누가 CodeQL·secrets·canary 를 룰셋에서 지워도 감사기가 초록을 말한다.**
    drift 감사의 일이 정확히 그걸 잡는 것이다.
    """

    def _rs(self, **over: Any) -> dict[str, Any]:
        return {**CLEAN["repos/x/rulesets/1"], **over}

    def test_missing_required_check_is_caught(self) -> None:
        rs = self._rs(rules=[
            {"type": "deletion"}, {"type": "non_fast_forward"},
            {"type": "pull_request", "parameters": {"allowed_merge_methods": ["squash"]}},
            {"type": "required_status_checks",
             "parameters": {"strict_required_status_checks_policy": True,
                            "required_status_checks": []}},
        ])
        self.assertIn("'ci / lint' 가 사라졌다", " ".join(_run({"repos/x/rulesets/1": rs})))

    def test_unexpected_required_check_is_reported(self) -> None:
        rs = self._rs()
        rs["rules"] = [dict(r) for r in rs["rules"]]
        rs["rules"][-1] = {"type": "required_status_checks",
                           "parameters": {"strict_required_status_checks_policy": True,
                                          "required_status_checks": [
                                              {"context": "ci / lint",
                                               "integration_id": repo_audit.ACTIONS_APP_ID},
                                              {"context": "surprise",
                                               "integration_id": repo_audit.ACTIONS_APP_ID}]}}
        self.assertIn("기대하지 않은 요구 검사 'surprise'", " ".join(_run({"repos/x/rulesets/1": rs})))

    def test_deleted_rule_is_caught(self) -> None:
        """규칙이 통째로 지워지면 출처만 보는 검사로는 안 잡힌다."""
        rs = self._rs(rules=[r for r in CLEAN["repos/x/rulesets/1"]["rules"]
                             if r["type"] not in ("deletion", "non_fast_forward")])
        got = " ".join(_run({"repos/x/rulesets/1": rs}))
        self.assertIn("기본 브랜치 삭제 금지", got)
        self.assertIn("강제 푸시 금지", got)

    def test_strict_off_is_caught(self) -> None:
        rs = self._rs()
        rs["rules"] = [dict(r) for r in rs["rules"]]
        rs["rules"][-1] = {"type": "required_status_checks",
                           "parameters": {"strict_required_status_checks_policy": False,
                                          "required_status_checks": [
                                              {"context": "ci / lint",
                                               "integration_id": repo_audit.ACTIONS_APP_ID}]}}
        self.assertIn("strict 가 꺼짐", " ".join(_run({"repos/x/rulesets/1": rs})))

    def test_merge_method_widened_is_caught(self) -> None:
        rs = self._rs()
        rs["rules"] = [dict(r) for r in rs["rules"]]
        rs["rules"][2] = {"type": "pull_request",
                          "parameters": {"allowed_merge_methods": ["squash", "merge"]}}
        self.assertIn("squash 전용이 아니다", " ".join(_run({"repos/x/rulesets/1": rs})))

    def test_multiple_rulesets_are_caught(self) -> None:
        """[0] 만 보면 룰셋이 여럿일 때 엉뚱한 것을 본다."""
        self.assertIn("룰셋이 2개다", " ".join(_run(
            {"repos/x/rulesets": [{"id": 1, "name": "main protection"}, {"id": 2, "name": "몰래"}]})))

    def test_approval_count_change_is_caught(self) -> None:
        """승인 1을 걸면 솔로는 자기 PR 을 승인 못 해 머지가 영원히 막힌다."""
        rs = self._rs()
        rs["rules"] = [dict(r) for r in rs["rules"]]
        rs["rules"][2] = {"type": "pull_request",
                          "parameters": {"allowed_merge_methods": ["squash"],
                                         "required_approving_review_count": 1}}
        self.assertIn("머지가 막힌다", " ".join(_run({"repos/x/rulesets/1": rs})))

    def test_squash_off_means_no_merge_button(self) -> None:
        meta = {**CLEAN["repos/x"], "allow_squash_merge": False}
        self.assertIn("머지할 방법이 없다", " ".join(_run({"repos/x": meta})))

    def test_wall_pointed_at_wrong_branch_is_caught(self) -> None:
        rs = self._rs(conditions={"ref_name": {"include": ["refs/heads/dev"], "exclude": []}})
        self.assertIn("기본 브랜치가 아니다", " ".join(_run({"repos/x/rulesets/1": rs})))


if __name__ == "__main__":
    unittest.main()


class RepoSelection(unittest.TestCase):
    """`--repo` 가 대상을 고르고 **우리 묶음 전용 검사를 꺼는가.**

    🔴 남의 저장소에 우리 거버넌스(라벨·`AGENTS.md`)를 요구하면 그건 감사가 아니라 참견이다.
    그리고 그 저장소는 **영원히 빨간불**이 되어 감사기가 무시당한다.
    """

    def test_no_argument_audits_our_four(self) -> None:
        repos, ours = repo_audit.selected([])
        self.assertEqual(repos, list(repo_audit.REPOS))
        self.assertTrue(ours, "우리 묶음이면 라벨·문서 검사가 돌아야 한다")

    def test_repo_argument_turns_our_only_checks_off(self) -> None:
        repos, ours = repo_audit.selected(["someone/thing"])
        self.assertEqual(repos, ["someone/thing"])
        self.assertFalse(ours, "남의 저장소에 우리 거버넌스를 요구하면 안 된다")

    def test_bare_name_defaults_to_our_owner(self) -> None:
        repos, _ = repo_audit.selected(["divcal"])
        self.assertEqual(repos, ["coolbress/divcal"])

    def test_repeated_flag_accumulates(self) -> None:
        repos, _ = repo_audit.selected(["a/b", "c"])
        self.assertEqual(repos, ["a/b", "coolbress/c"])

    def test_our_four_list_matches_the_audited_set(self) -> None:
        """🔴 `OURS` 와 `REPOS` 가 갈리면 라벨 검사가 엉뚱한 집합을 본다."""
        self.assertEqual(
            sorted(repo_audit.OURS),
            sorted(r.split("/", 1)[1] for r in repo_audit.REPOS),
        )


class WorkflowTokenPermissions(unittest.TestCase):
    """워크플로 토큰의 **기본 권한**을 서버에서 본다.

    🔴 파일마다 `permissions:` 를 적는 것과 **다른 문장이다** — 하나라도 빠뜨리면 그 워크플로가
    **쓰기 토큰**을 들고 돈다. 서버 기본값이 마지막 방어선이고, 2026-08-30 까지
    **아무도 이걸 안 봤다**(R5-38 과 같은 형태 — 실물은 맞았지만 **바뀌어도 몰랐다**).
    """

    def test_write_default_is_caught(self) -> None:
        bad, _ = _both({"repos/x/actions/permissions/workflow": {
            "default_workflow_permissions": "write", "can_approve_pull_request_reviews": False}})
        self.assertTrue([b for b in bad if "기본 권한이 read 가 아니다" in b], bad)

    def test_bot_approval_switch_is_caught(self) -> None:
        """🔴 봇이 PR 을 승인할 수 있으면 **승인이 도장이 된다.**

        우리는 승인 0 을 유지하지만, 이 스위치가 켜지면 **룰셋을 안 바꾸고도** 그 길이 열린다
        (`direction/01` 경계 ② *동료 리뷰를 시뮬레이션하지 않는다*).
        """
        bad, _ = _both({"repos/x/actions/permissions/workflow": {
            "default_workflow_permissions": "read", "can_approve_pull_request_reviews": True}})
        self.assertTrue([b for b in bad if "승인할 수 있다" in b], bad)

    def test_clean_state_passes(self) -> None:
        bad, _ = _both({})
        self.assertEqual([b for b in bad if "토큰" in b or "승인" in b], [])

    def test_unreadable_is_unknown_not_failure(self) -> None:
        """🔵 읽을 권한이 없는 것과 벽이 무너진 것은 **다른 문장이다.**"""
        _, unknown = _both({}, status=403)
        self.assertTrue([u for u in unknown if "기본 권한" in u], unknown)
