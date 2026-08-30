"""`.gitattributes` 가 **실제로 무엇을 하는지** 검사한다. 네트워크는 안 탄다.

🔴 왜 생겼나 (2026-08-30 · `GAPS` R5-42): 이 항목은 한 번 **기각**됐다. 근거는
*"쓰임은 둘이다 — 개행 정규화와 LFS"* 였는데 **열거가 빠져 있었다.** git 1차 문서를 세니
git 자신이 정의하는 속성만 열둘이 넘고, 그중 GitHub 의 `linguist-generated` 는 파일을
diff 에서 접는다. 이 저장소는 **생성물 때문에 `ci / diff-size` 를 면제받은** 곳이라
그 쓰임이 바로 걸린다.
"""

from __future__ import annotations

import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ATTRS = ROOT / ".gitattributes"

# 쓰는 도구가 있는 것만 여기 있다. 손으로 관리하는 파일을 접으면 진짜 수정이 숨는다.
GENERATED = {
    "ROUTES.jsonl": "tools/build-routes.mjs",
    "audit/external-url-status.jsonl": "tools/external_url_audit.py",
    "audit/after-manifest.tsv": "tools/rebuild_after_manifest.py",
    "corpus/census-data/provenance/snapshot-manifest.json": "corpus/census-data/provenance/provenance.py",
}


def rules(text: str) -> list[tuple[str, list[str]]]:
    out = []
    for line in text.splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            pattern, *attrs = line.split()
            out.append((pattern, attrs))
    return out


class Attributes(unittest.TestCase):
    def setUp(self) -> None:
        self.rules = rules(ATTRS.read_text(encoding="utf-8"))

    def test_line_endings_are_normalized(self) -> None:
        self.assertIn("text=auto", dict(self.rules).get("*", []))

    def test_every_generated_ledger_is_folded(self) -> None:
        marked = {p for p, a in self.rules if "linguist-generated" in a}
        self.assertEqual(set(GENERATED) - marked, set(), "생성물인데 리뷰에서 안 접힌다")

    def test_marked_paths_still_exist(self) -> None:
        """🔵 낡은 규칙은 조용하다 — 안 맞는 패턴은 아무 일도 안 하고 남아 있다."""
        missing = [p for p, a in self.rules if "linguist-generated" in a and not (ROOT / p).exists()]
        self.assertEqual(missing, [], "없는 파일을 가리키는 규칙")

    def test_marked_files_really_are_written_by_a_tool(self) -> None:
        """🔴 **손으로 쓰는 파일을 접으면 진짜 수정이 숨는다.** 쓰는 도구가 있는지 본다."""
        for path, writer in GENERATED.items():
            src = (ROOT / writer).read_text(encoding="utf-8")
            name = Path(path).name
            self.assertIn(name, src, f"{writer} 가 {name} 을 안 쓴다 — 생성물 표시가 거짓이다")

    def test_no_rule_needs_local_git_config(self) -> None:
        """🔴 `diff=<이름>`·`merge=<이름>`·`filter=<이름>` 은 **각자 로컬 config** 가 있어야 돈다.

        커밋된 파일만으로 안 돈다 — 적어두면 *돌고 있다고 착각하게* 만든다.
        `pre-commit` 기각과 같은 형태다(원칙 01: 집행은 에이전트 밖에서).
        """
        bad = [
            f"{p}: {a}"
            for p, attrs in self.rules
            for a in attrs
            if a.partition("=")[0] in {"diff", "merge", "filter"}
            and a.partition("=")[2] not in {"", "true", "false"}
        ]
        self.assertEqual(bad, [], "로컬 설정이 있어야 도는 규칙")


class GitAgrees(unittest.TestCase):
    """문서가 아니라 **git 이 그렇게 읽는지**를 본다."""

    def test_git_check_attr_confirms(self) -> None:
        for path in GENERATED:
            out = subprocess.run(
                ["git", "check-attr", "linguist-generated", "--", path],
                cwd=ROOT, capture_output=True, text=True, check=True,
            ).stdout
            self.assertIn("linguist-generated: set", out, f"{path} 에 git 이 속성을 안 붙인다")
