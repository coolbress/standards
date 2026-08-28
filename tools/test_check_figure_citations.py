"""`check_figure_citations` 의 판정 로직 시험.

파일시스템을 타지 않게 `missing_labels` 만 본다 — 저장소 내용이 바뀌어도
이 시험은 안 흔들리고, 흔들려야 할 것은 기준선이다.
"""

from __future__ import annotations

import unittest

from check_figure_citations import PAIR, missing_labels


class PairDetection(unittest.TestCase):
    def test_finds_pairs_in_both_notations(self) -> None:
        for text in ("CONTRIBUTING(75/70%)", "present 62% / 41%", "≈ 100% uni / 100% wgt"):
            self.assertTrue(PAIR.search(text), text)

    def test_ignores_a_lone_percentage(self) -> None:
        self.assertIsNone(PAIR.search("README ≈ 100% 유일한 보편"))


class LabelDetection(unittest.TestCase):
    def test_bare_pair_is_missing_both(self) -> None:
        # direction/05 가 실제로 이랬다 — 축도 n 도 없어 adequate 로 오독됐다.
        self.assertEqual(missing_labels("CONTRIBUTING(75/70%)"), ["축", "n"])

    def test_uni_wgt_with_n_is_complete(self) -> None:
        self.assertEqual(missing_labels("CONTRIBUTING ≈ 75% uni / 70% wgt (n=938)"), [])

    def test_present_adequate_with_n_is_complete(self) -> None:
        self.assertEqual(missing_labels("present 61.5% / adequate 41.2% (n=2,000)"), [])

    def test_axis_in_block_header_counts(self) -> None:
        # 절 머리글에 축을 선언하는 관례를 인정한다 (aspect 22 가 그렇게 쓴다).
        block = "**Census (recency-weighted, w = 0.5^(age/2yr))**, n=938\n- CONTRIBUTING 75% / 70%"
        self.assertEqual(missing_labels(block), [])

    def test_axis_without_n_is_still_incomplete(self) -> None:
        self.assertEqual(missing_labels("uni / wgt 로 75% / 70%"), ["n"])


if __name__ == "__main__":
    unittest.main()
