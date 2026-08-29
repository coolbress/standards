"""도달 검사의 **판정 규칙** 시험. 네트워크를 안 탄다.

🔴 가장 중요한 것은 **전이 도달**이다. `direction/` → `GAPS` → `SKILL-OVERLAP` 처럼
대장이 한 번 가리키면 그 아래는 따라갈 수 있다. 전이를 안 세면 **고아가 13개로 보이는데
실제는 3개**다(2026-08-30 실측 — 처음 진단이 그렇게 틀렸다).
"""

from __future__ import annotations

import unittest

import check_audit_reachability as mod


class Reachability(unittest.TestCase):
    def test_real_repo_has_no_new_orphans(self) -> None:
        """기준선 대비다 — 기존 고아는 통과, 새 고아만 막는다."""
        self.assertEqual(mod.main(), 0)

    def test_baseline_entries_are_still_real_files(self) -> None:
        """🔴 기준선이 없는 파일을 들고 있으면 **고쳐진 것을 못 알아챈다.**"""
        import json

        baseline = json.loads(mod.BASELINE.read_text(encoding="utf-8"))["orphans"]
        for name in baseline:
            self.assertTrue((mod.AUDIT / name).is_file(), f"기준선의 {name} 이 없다")

    def test_orphans_are_a_subset_of_audit_docs(self) -> None:
        self.assertLessEqual(set(mod.orphans()), set(mod.audit_docs()))

    def test_reachable_includes_transitively_linked_docs(self) -> None:
        """`GAPS` 는 `direction/` 이 직접 가리키고, 그 아래 문서들도 도달로 친다."""
        reached = mod.reachable(mod.audit_docs())
        self.assertIn("GAPS.ko.md", reached)
        self.assertIn("ARSENAL.ko.md", reached)
        self.assertIn("PLUGIN-DESIGN.ko.md", reached,
                      "오늘 만든 설계 문서가 정본에서 안 닿으면 다음 세션이 못 찾는다")
