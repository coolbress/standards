"""`check_template_drift` 의 경로 변환·필터 시험. **네트워크는 안 탄다.**

`shared()` 가 인스턴스로 안 가는 것을 빼는지 본다. 안 빼면 **모든 인스턴스가 영원히
드리프트로 보이고**, 그러면 검사가 무시된다 — 오탐이 신호를 묻는 그 형태다.
실제로 두 번 그랬다: 처음엔 `tests/test_app.py` 가, 그다음엔 `_subdirectory` 전환 뒤
**29개 전부**가 오탐이었다(템플릿 경로가 `template/` 로 내려갔는데 그대로 비교했다).
"""

from __future__ import annotations

import unittest

import pathlib

from check_template_drift import ANSWERS, GENERATOR_ONLY, SUBDIR, _emitted, shared

SOURCE = pathlib.Path(__file__).resolve().parent / "check_template_drift.py"


class SubdirectoryMapping(unittest.TestCase):
    """🔴 `_subdirectory` 전환 뒤 이게 없어서 **29개가 전부 오탐**이었다."""

    def test_root_files_are_not_emitted(self) -> None:
        for root_only in ("copier.yml", "pyproject.toml", "tests/test_copier_template.py",
                          "src/template_render/__init__.py", ".github/workflows/ci.yml"):
            self.assertIsNone(_emitted(root_only), f"{root_only} 은 템플릿 자신의 것이다")

    def test_subdirectory_prefix_is_stripped(self) -> None:
        self.assertEqual(_emitted("template/CONTRIBUTING.md"), "CONTRIBUTING.md")
        self.assertEqual(_emitted("template/.github/workflows/ci.yml"), ".github/workflows/ci.yml")

    def test_jinja_suffix_is_stripped(self) -> None:
        """`.jinja` 는 렌더 지시이지 이름의 일부가 아니다."""
        self.assertEqual(_emitted("template/pyproject.toml.jinja"), "pyproject.toml")
        self.assertEqual(_emitted("template/uv.lock.jinja"), "uv.lock")

    def test_answer_dependent_paths_are_skipped(self) -> None:
        """이름이 답에 따라 달라지므로 **이름으로 비교할 수 없다.** 세면 항상 틀린다."""
        for templated in ("template/src/{{ package_name }}/__init__.py",
                          "template/tests/test_{{ package_name }}.py.jinja",
                          "template/{{ _copier_conf.answers_file }}.jinja"):
            self.assertIsNone(_emitted(templated))


class GeneratorOnlyFilter(unittest.TestCase):
    def test_drops_archetype_conditional_files(self) -> None:
        """`.env.example` 은 service·data-ml 에만 간다 — cli 인스턴스에 없는 게 정상이다."""
        got = shared({
            "template/.env.example",
            "template/tests/test_env_example.py",
            "template/dist/thing.whl",
        })
        self.assertEqual(got, set())

    def test_keeps_shared_files(self) -> None:
        self.assertEqual(
            shared({
                "template/.github/ISSUE_TEMPLATE/bug.yml",
                "template/tests/test_contributing.py",
                "template/CONTRIBUTING.md",
                "template/AGENTS.md",
            }),
            {".github/ISSUE_TEMPLATE/bug.yml", "tests/test_contributing.py",
             "CONTRIBUTING.md", "AGENTS.md"},
        )

    def test_filter_list_is_not_empty(self) -> None:
        # 비면 필터가 아무것도 안 하고 모든 인스턴스가 드리프트로 보인다.
        self.assertTrue(GENERATOR_ONLY)


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
