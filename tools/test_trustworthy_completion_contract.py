"""Regression checks for the approved trustworthy-completion contract."""

from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORTH = ROOT / "interpretation" / "foundation" / "goppi-worth-hypothesis.md"
PROTOCOL = (
    ROOT
    / "interpretation"
    / "foundation"
    / "trustworthy-completion-evaluation-protocol.md"
)


def section(text: str, start: str, end: str) -> str:
    return text.split(start, 1)[1].split(end, 1)[0]


class TrustworthyCompletionContractTests(unittest.TestCase):
    def test_comprehension_is_required_for_tcr(self) -> None:
        text = WORTH.read_text(encoding="utf-8")
        definition = section(text, "### Trustworthy completion", "### 네 가지 결과 상태")
        self.assertIn("**이해 가능성:**", definition)
        self.assertIn("위 여섯 조건을 모두 통과", text)

    def test_comprehension_is_a_product_go_gate(self) -> None:
        text = WORTH.read_text(encoding="utf-8")
        go_section = section(text, "## 확증시험 전에 고정할 GO 문장", "## 상속 실험의 재해석")
        self.assertIn("이해 가능성과 적정 의존", go_section)
        self.assertIn("중대한 오해", go_section)

    def test_protocol_excludes_material_misconception(self) -> None:
        text = PROTOCOL.read_text(encoding="utf-8")
        comprehension = section(text, "### Comprehension and informed decision", "### Process earnedness")
        self.assertIn("다른 조건이 맞아도 trustworthy completion이 아니다", comprehension)

    def test_reliance_denominators_cover_the_full_matrix(self) -> None:
        text = PROTOCOL.read_text(encoding="utf-8")
        reliance = section(text, "### Appropriate reliance", "### Comprehension and informed decision")
        for marker in ("RAIR eligible", "RSR eligible", "agreement/control case", "joint-error/control case"):
            self.assertIn(marker, reliance)
        self.assertIn("NOT-ESTIMABLE", reliance)
        self.assertIn("해당 GO gate를 `INCONCLUSIVE`", reliance)

    def test_human_grading_has_a_masking_leakage_audit(self) -> None:
        text = PROTOCOL.read_text(encoding="utf-8")
        masking = section(text, "### Grader masking and leakage audit", "## 8. Primary 계산")
        self.assertIn("arm을 추측", masking)
        self.assertIn("의미 정보는 제거하지 않는다", masking)
        self.assertIn("primary outcome/assurance score가 lock", masking)

    def test_attribution_precedes_final_product_go(self) -> None:
        text = PROTOCOL.read_text(encoding="utf-8")
        decision = section(text, "## 11. 제품과 component 판정", "## 12. 아직 하지 않은 것")
        self.assertIn("PROVISIONAL-GO/PENDING-ATTRIBUTION", decision)
        self.assertIn("최종 GO 전에 실행", decision)
        self.assertIn("최종 product", decision)

    def test_thresholds_keep_comprehension_rair_and_rsr_separate(self) -> None:
        text = PROTOCOL.read_text(encoding="utf-8")
        worksheet = section(text, "## 9. Threshold-calibration worksheet", "## 10. 중단·무효 조건")
        self.assertIn("| comprehension floor |", worksheet)
        self.assertIn("| RAIR floor + required/not-required |", worksheet)
        self.assertIn("| RSR floor + required/not-required |", worksheet)


if __name__ == "__main__":
    unittest.main()
