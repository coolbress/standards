"""`check_floor_coverage` 의 판정 로직 시험.

이 검사가 지키는 것은 *"요구하라"* 가 아니라 *"입장을 밝혀라"* 다.
그래서 **기각을 적은 것도 통과해야** 한다 — 그게 안 되면 검사가 바닥을 문진표로 만든다.
"""

from __future__ import annotations

import unittest

from check_floor_coverage import (
    CENSUSES,
    NAMES,
    NAMES_EXPANDED,
    ROLLUP,
    THRESHOLD,
    unaccounted,
)


class Mapping(unittest.TestCase):
    def test_rollups_point_at_a_real_name(self) -> None:
        # 롤업 대상이 이름표에 없으면 하위 항목이 영원히 미해명으로 남는다.
        known = {**NAMES, **NAMES_EXPANDED}
        for child, parent in ROLLUP.items():
            self.assertIn(parent, known, f"{child} → {parent} 가 이름표에 없다")

    def test_every_census_file_exists(self) -> None:
        # 센서스 파일이 사라지면 검사가 조용히 아무것도 안 보게 된다.
        for name, path in CENSUSES:
            self.assertTrue(path.is_file(), f"{name} 센서스가 없다: {path}")

    def test_more_than_one_census_is_scanned(self) -> None:
        # 하나만 보면 다른 센서스의 산출물이 침묵으로 남는다 — 실제로 그랬다.
        self.assertGreaterEqual(len(CENSUSES), 2)

    def test_threshold_is_not_zero(self) -> None:
        # 0 이면 야생에서 드문 것까지 전부 해명하게 만든다 = P40 위반.
        self.assertGreater(THRESHOLD, 0)


class Coverage(unittest.TestCase):
    def test_floor_accounts_for_every_measured_artifact(self) -> None:
        missing = unaccounted()
        self.assertEqual(
            missing,
            [],
            "바닥이 입장을 안 밝힌 산출물이 있다. 요구하거나 §적힌 기각 에 적어라: "
            f"{[(c, col) for c, col, _ in missing]}",
        )


if __name__ == "__main__":
    unittest.main()
