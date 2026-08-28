"""`check_citation_status` 시험. **네트워크는 안 탄다.**

🔴 왜 이 검사가 필요했나: README **절대규칙 3** 이 2026-08-24 에
*"인용 지점에 status 를 병기한다"* 로 개정됐는데 **아무것도 그걸 지키지 않았다.**
실측 — `direction` 이 인용하는 코퍼스 문서 **14건 중 10건이 덜 익었는데 병기 0건**.
"""

from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import check_citation_status as mod


class CitationStatus(unittest.TestCase):
    def _fixture(self, body: str, status: str | None = "draft", name: str = "x.md") -> list:
        with TemporaryDirectory() as raw:
            root = Path(raw)
            corpus = root / "corpus" / "a"
            corpus.mkdir(parents=True)
            front = f"---\nstatus: {status}\n---\n" if status else "# no frontmatter\n"
            (corpus / name).write_text(front, encoding="utf-8")
            direction = root / "direction"
            direction.mkdir()
            (direction / "05.md").write_text(body, encoding="utf-8")
            return mod.findings(direction, root / "corpus")

    def test_draft_without_annotation_is_caught(self) -> None:
        found = self._fixture("근거는 [문서](../corpus/a/x.md) 다.")
        self.assertEqual([f[3] for f in found], ["draft"])

    def test_draft_with_annotation_passes(self) -> None:
        self.assertEqual(self._fixture("근거는 [문서](../corpus/a/x.md) *(draft)* 다."), [])

    def test_annotation_on_the_next_line_passes(self) -> None:
        """링크 뒤에서 줄바꿈하는 문단이 실제로 있다."""
        self.assertEqual(self._fixture("근거는 [문서](../corpus/a/x.md)\n*(draft)* 다."), [])

    def test_verified_needs_no_annotation(self) -> None:
        """막으려는 것은 **덜 익은 근거가 익은 척하는 것**이다."""
        self.assertEqual(self._fixture("[문서](../corpus/a/x.md)", status="verified"), [])

    def test_wrong_status_word_does_not_satisfy(self) -> None:
        """`review-needed` 문서에 `draft` 를 적으면 안 된다 — 병기가 거짓이 된다."""
        found = self._fixture("[문서](../corpus/a/x.md) *(draft)*", status="review-needed")
        self.assertEqual([f[3] for f in found], ["review-needed"])

    def test_claimless_documents_are_exempt(self) -> None:
        """규범·절차·역사 기록은 claim 문서가 아니다. 목록은 `validate_corpus` 것을 끌어쓴다."""
        name = sorted(mod.CLAIMLESS_OK)[0]
        self.assertEqual(self._fixture(f"[문서](../corpus/a/{name})", status=None, name=name), [])

    def test_real_repository_is_clean(self) -> None:
        self.assertEqual(mod.findings(mod.DIRECTION, mod.CORPUS), [])


class ListIsNotDuplicated(unittest.TestCase):
    def test_claimless_list_comes_from_validate_corpus(self) -> None:
        """🔵 복제하면 두 곳이 되고, 두 곳이 되면 갈린다."""
        import validate_corpus as vc

        self.assertIs(mod.CLAIMLESS_OK, vc.CLAIMLESS_OK)
