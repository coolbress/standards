"""`check_template_drift` 의 필터 시험. **네트워크는 안 탄다.**

`shared()` 가 생성기 전용 파일을 빼는지만 본다. 안 빼면 **모든 인스턴스가 영원히
드리프트로 보이고**, 그러면 검사가 무시된다 — 오탐이 신호를 묻는 그 형태다.
실제로 처음 돌렸을 때 `tests/test_app.py` 가 오탐으로 잡혔다.
"""

from __future__ import annotations

import unittest

import pathlib

from check_template_drift import ANSWERS, GENERATOR_ONLY, shared

SOURCE = pathlib.Path(__file__).resolve().parent / "check_template_drift.py"


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

    def test_template_only_copier_files_are_filtered(self) -> None:
        # `copier.yml` 과 답 파일의 **템플릿**은 인스턴스로 안 간다.
        # 안 빼면 모든 인스턴스가 영원히 "3개 부족" 으로 보인다.
        self.assertEqual(
            shared({
                "copier.yml",
                "{{ _copier_conf.answers_file }}.jinja",
                "tests/test_copier_template.py",
            }),
            set(),
        )

    def test_answers_file_name_is_the_copier_default(self) -> None:
        # 인스턴스 탐지가 이 이름에 걸려 있다. 바뀌면 인스턴스를 0개로 본다.
        self.assertEqual(ANSWERS, ".copier-answers.yml")


class InstanceDetection(unittest.TestCase):
    """인스턴스 탐지가 **404 를 통과시키지 않는가.**

    🔴 실측 사고: `gh api …/contents/… --jq .content -H "Accept: …raw+json"` 로 존재를
    확인했더니 **404 도 통과해 인스턴스가 9개**로 잡혔다(실제 1개). `--jq` 와 raw Accept 를
    같이 쓰면 응답이 JSON 이 아니라 `--jq` 가 무의미해지고, `check=False` 라 오류도 안 난다.

    네트워크를 타는 함수라 호출은 못 하지만, **알려진 나쁜 형태가 다시 들어오는 것**은 막는다.
    `test_issue_forms` 의 YAML alias 함정 검사와 같은 부류다.
    """

    def test_detection_judges_by_exit_code_not_output(self) -> None:
        src = SOURCE.read_text(encoding="utf-8")
        body = src[src.index("def _has_answers") : src.index("def instances")]
        self.assertIn("returncode == 0", body, "종료코드로 판정하지 않는다")

        # 🔴 **주석·docstring 은 빼고 명령줄만 본다.** 처음엔 함수 전체를 훑었는데
        # docstring 이 이 버그를 *설명하며* `--jq` 를 언급해 시험이 자기 오탐을 냈다.
        command = [
            ln for ln in body.splitlines()
            if '"gh"' in ln or '"api"' in ln or ln.strip().startswith('f"repos/')
        ]
        self.assertTrue(command, "명령줄을 못 찾았다 — 시험이 아무것도 안 보고 있다")
        self.assertNotIn(
            "--jq", "\n".join(command),
            "존재 확인에 `--jq` 를 쓰면 404 가 통과한다 — 실측으로 인스턴스가 9개로 잡혔다",
        )

    def test_the_template_itself_is_not_counted_as_an_instance(self) -> None:
        src = SOURCE.read_text(encoding="utf-8")
        self.assertIn("if n == TEMPLATE_NAME", src, "템플릿 자신을 인스턴스로 센다")
