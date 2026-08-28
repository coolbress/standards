"""`check_name_only_citations` 가 실제로 잡는지 확인한다.

🔴 이 시험의 요점은 **검사가 꺼져 있지 않다는 것**이다. 이름으로만 부르는 인용을
심어두고 잡히는지 본다 — 안 잡히면 R5-29 가 되돌아와도 아무도 모른다.
"""

from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import check_name_only_citations as mod


class NameOnlyCitationTest(unittest.TestCase):
    def _fixture(self, direction_body: str) -> list[tuple[str, str, Path]]:
        with TemporaryDirectory() as raw:
            root = Path(raw)
            corpus = root / "corpus" / "aspects" / "01-x"
            corpus.mkdir(parents=True)
            (corpus / "planning-output-census.md").write_text("# doc", encoding="utf-8")
            direction = root / "direction"
            direction.mkdir()
            (direction / "05.md").write_text(direction_body, encoding="utf-8")
            stems = {p.stem: p for p in (root / "corpus").rglob("*.md")}
            return mod.findings(direction, stems)

    def test_backticked_name_without_path_is_caught(self) -> None:
        found = self._fixture("근거는 `planning-output-census` 다.")
        self.assertEqual([f[1] for f in found], ["planning-output-census"])

    def test_path_citation_is_accepted(self) -> None:
        body = "근거는 [`planning-output-census`](../corpus/aspects/01-x/planning-output-census.md) 다."
        self.assertEqual(self._fixture(body), [])

    def test_unrelated_backticked_token_is_ignored(self) -> None:
        """코퍼스 파일이 아닌 kebab-case 토큰(`uv-sync-locked` 같은 것)은 세지 않는다."""
        self.assertEqual(self._fixture("`some-other-token` 은 문서가 아니다."), [])

    def test_real_repository_is_clean(self) -> None:
        self.assertEqual(mod.findings(mod.DIRECTION, mod.corpus_stems()), [])


if __name__ == "__main__":
    unittest.main()
