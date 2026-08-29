"""`check_corpus_identity` 시험. **네트워크는 안 탄다.**

🔴 이 검사의 요점은 **되돌리라고 하지 않는 것**이다. *"gingoa's TS/Node choice"* 는 그때 그
프로젝트가 무엇을 정했는지에 대한 **참인 기록**이라, 이름을 바꾸면 기록이 거짓이 된다.
검사는 **늘지 않게** 잡을 뿐이다.
"""

from __future__ import annotations

import unittest

import check_corpus_identity as mod


class SubjectVersusMention(unittest.TestCase):
    """단순 언급은 역사 서술이라 **정상**이다. 주어 자리만 센다."""

    def test_english_possessive_is_a_subject(self) -> None:
        self.assertTrue(mod.SUBJECT.search("gingoa's ① output set"))
        self.assertTrue(mod.SUBJECT.search("goppi_final's decision"))

    def test_korean_particles_are_subjects(self) -> None:
        """🔬 처음에 영어 소유격만 세어 37 로 잡았다가 돌려보니 52 였다."""
        for s in ("gingoa 의 선택", "goppi 가 정했다", "claudeck 는 그랬다", "gingoa 은 달랐다"):
            self.assertTrue(mod.SUBJECT.search(s), s)

    def test_plain_mention_is_not_flagged(self) -> None:
        """*'과거 gingoa에서 승계'* 같은 문장은 역사 서술이다 — 잡으면 검사가 소음이 된다."""
        for s in ("과거 gingoa에서 승계했다", "goppi 하네스는 폐기됐다", "legacy/judgments/goppi/"):
            self.assertIsNone(mod.SUBJECT.search(s), s)


class BaselineHasNoSlack(unittest.TestCase):
    def test_baseline_equals_the_measured_count(self) -> None:
        """🔴 한 칸이라도 남기면 **새 문서 하나가 조용히 들어온다.**"""
        self.assertEqual(len(mod.offenders()), mod.BASELINE_FILES)

    def test_baseline_is_documented(self) -> None:
        doc = mod.__doc__ or ""
        self.assertIn("기준선", doc)


class TheReadingRuleStands(unittest.TestCase):
    def test_guide_carries_the_rule(self) -> None:
        self.assertTrue(mod.guide_carries_the_reading_rule(),
                        "GUIDE.ko.md 에 읽는 규칙이 없다 — 옛 이름이 이 저장소를 가리키는 것처럼 읽힌다")

    def test_guide_itself_is_exempt(self) -> None:
        """규칙을 설명하는 문서는 예시로 옛 이름을 든다. 자기를 세면 안 된다."""
        self.assertNotIn(str(mod.GUIDE.relative_to(mod.ROOT)), mod.offenders())

    def test_the_front_door_no_longer_carries_an_old_name(self) -> None:
        """🔴 `GUIDE.ko.md` 의 제목이 *'goppi_final 리서치 코퍼스 안내'* 였다 —
        코퍼스가 **폐기된 하네스의 이름으로 자기를 소개**하고 있었다."""
        head = mod.GUIDE.read_text(encoding="utf-8")[:400]
        for name in mod.OLD_NAMES:
            self.assertNotIn(f"{name}_final 리서치", head)
            self.assertNotIn(f'title: "{name}', head)
