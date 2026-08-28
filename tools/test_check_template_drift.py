"""`check_template_drift` 의 필터 시험. **네트워크는 안 탄다.**

`shared()` 가 생성기 전용 파일을 빼는지만 본다. 안 빼면 **모든 인스턴스가 영원히
드리프트로 보이고**, 그러면 검사가 무시된다 — 오탐이 신호를 묻는 그 형태다.
실제로 처음 돌렸을 때 `tests/test_app.py` 가 오탐으로 잡혔다.
"""

from __future__ import annotations

import unittest

from check_template_drift import GENERATOR_ONLY, shared


class GeneratorOnlyFilter(unittest.TestCase):
    def test_drops_files_the_generator_removes_or_renames(self) -> None:
        got = shared({
            "bootstrap.sh",
            "tests/test_bootstrap_name.py",
            "tests/test_app.py",
            "src/app/__init__.py",
            "src/app/py.typed",
            "dist/thing.whl",
        })
        self.assertEqual(got, set())

    def test_keeps_shared_files(self) -> None:
        keep = {
            ".github/ISSUE_TEMPLATE/bug.yml",
            "tests/test_contributing.py",
            "CONTRIBUTING.md",
            "AGENTS.md",
        }
        self.assertEqual(shared(keep), keep)

    def test_project_code_is_not_in_the_template_set(self) -> None:
        # 인스턴스 고유 코드는 템플릿에 없으므로 애초에 비교 대상이 아니다.
        self.assertEqual(shared({"src/divcal/cli.py"}), {"src/divcal/cli.py"})

    def test_filter_list_is_not_empty(self) -> None:
        # 비면 필터가 아무것도 안 하고 모든 인스턴스가 드리프트로 보인다.
        self.assertTrue(GENERATOR_ONLY)
