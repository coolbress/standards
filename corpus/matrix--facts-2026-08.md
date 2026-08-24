# 2026-08 facts 패스 — 교차 검증 대상 목록

> **성격**: 2026-08-02 facts-only 패스(11개 sub-doc)의 **품질 관리 부속 문서**. 새 리서치 없음, 의견 없음.
> 주제별 항해는 [`INDEX.md`](INDEX.md)와 각 aspect의 Sub-documents 절이 담당한다 (2026-08-02 슬림화 —
> 이전 판의 주제별 요약 A~O는 facts sub-doc 본문과 중복이라 제거; 전문은 archive 스냅샷에 보존).
>
> 아래 번호는 facts 패스의 원 파일 번호다:
> 06→`aspects/28-…/sdlc-models--facts-2026-08.md` · 07→`aspects/01-…/requirements--facts-2026-08.md` ·
> 08→`aspects/02-…/design-practice--facts-2026-08.md` · 09→`aspects/07-…/codereview--facts-2026-08.md` ·
> 10→`aspects/08-…/testing--facts-2026-08.md` · 11→`aspects/04-…/cicd-release--facts-2026-08.md` ·
> 12→`aspects/20-…/operations-sre--facts-2026-08.md` · 13→`aspects/28-…/agile-adoption--facts-2026-08.md` ·
> 14→`aspects/09-…/security-sdlc--facts-2026-08.md` · 15→`aspects/01-…/estimation-failure-data--facts-2026-08.md` ·
> 16→`aspects/24-…/roles-teams--facts-2026-08.md`

## 출처 간 수치·표현 상이 목록 (교차 검증 대상)

| 항목 | 상이 내용 | 파일 |
|---|---|---|
| Google 모노레포 개발자 수 | "35,000명" vs "수만 명" — 출처·시점 상이 | 09 / 11 |
| 테스트 비율 | Google 80/15/5 vs Fowler 계열 ~70/20/10 표현 | 10 |
| Scrum 채택률 | 단일 조사 ~70% vs 조사 통합 63–87% | 13 |
| CHAOS 수치 | 수치 자체(15) vs 방법론 비판(Eveleens&Verhoef, 15) 병존 | 15 |
| Boehm 곡선 | 원 주장(최대 200배) vs 2001 완화(≈5:1, 소규모) | 15 |
| DORA 수치의 경유 | Elite/Low 배수·클러스터·AI 영향 수치가 2차 사이트 경유 | 11, 15 |
| ISO 12207 판본 | 현행판은 ISO/IEC/IEEE 12207:2026이다. withdrawn된 ISO/IEC/IEEE 12207:2017의 상세 분류를 현행판 조항으로 재귀속하지 않는다 (감사 disposition 준수 — 유료 전문 미확보로 clause mapping은 INCONCLUSIVE 유지) | 06 |
| PMI 2024 표현 | 채택 분포(해석층 01)와 추세 %(사실층 13)가 서로 다른 절단면 | 01 / 13 |

## 1차 출처 재확인 우선 대상 (결론 문서 작성 전)

수치가 결론의 근거로 쓰일 가능성이 높으면서 현재 2차 경유인 것:

1. DORA 배수·클러스터 → dora.dev 원문
2. CHAOS 연도별 수치 → Standish 원문/학술 정리 (+ Eveleens&Verhoef 비판 병기 유지)
3. State of Agile 채택률 → digital.ai 원문
4. AI 영향 수치 (15 §8 — Faros AI 블로그 경유, 문서 내 주의 표기) → DORA 2025 원문
5. 페어 프로그래밍 결함 발견율 (tuple.app 경유) → 원 논문
6. McKinsey-Oxford 수치 → mckinsey.com 원문 (해석층 01에 1차 링크 존재)

재확인 실행 시 각 facts 파일의 해당 claim에 직접 반영하고, 이 목록에서 지운다. 전부 지워지면 이 문서는
소멸 대상이다 (수치 상이 목록은 claim-level revalidation register로 흡수).
