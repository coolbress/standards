---
id: aspect-08-software-testing--facts-2026-08-testing
title: "Testing practice — facts (2026-08)"
parent: aspect-08-software-testing
kind: research-log
evidence_track: lit
status: draft
language: ko
last_updated: "2026-08-02"
method: "Haiku web-research agents, facts-only rules ([정의/규정]/[데이터]/[주장] labels), source-tier tagged [1차]/[2차]; session-lead verified"
---

# 소프트웨어 테스팅 실증 연구 및 업계 기준

## 개요

테스트 피라미드는 Mike Cohn(2009)이 "Succeeding with Agile"에서 제시한 자동화 테스트 분포 메타포로, 유닛 테스트 기반 구조를 강조한다 [https://www.leapwork.com/blog/what-is-test-automation]. Martin Fowler의 Practical Test Pyramid는 이를 발전시켜, 테스트 수준별 유지보수성과 실행 속도의 트레이드오프를 다룬다 [https://martinfowler.com/articles/practical-test-pyramid.html]. 이 문서는 테스트 전략에 관한 공표된 데이터와 업계 정의를 정리한다.

---

## 테스트 피라미드

### Mike Cohn의 원형 구조 [정의/규정]

테스트 피라미드는 세 층으로 구성된다 [https://www.mountaingoatsoftware.com/blog/the-forgotten-layer-of-the-test-automation-pyramid]:
- **유닛 테스트(기저)**: 단일 함수/모듈 범위, 최대량
- **서비스 테스트(중층)**: 애플리케이션 서비스 레벨, UI를 거치지 않음
- **UI 테스트(정점)**: 사용자 인터페이스 테스트, 최소량

Cohn은 UI 테스트의 단점을 "불안정(Brittle)", "작성 비용 높음(Expensive)", "실행 시간 길음(Time consuming)"으로 지적했다 [https://dev.to/mhossen/rethinking-the-test-pyramid-a-balanced-view-from-code-to-customer-5bhl].

### Martin Fowler의 실용적 개선 [정의/규정]

Fowler는 테스트 중복을 제거하고 빠른 피드백을 우선시할 것을 권장한다 [https://martinfowler.com/articles/practical-test-pyramid.html]. 각 층의 특성:
- **유닛 테스트**: 공개 인터페이스 테스트, 수천 개를 분 단위 실행
- **통합 테스트**: 외부 시스템(DB, API, 파일시스템) 상호작용 검증, 단일 통합점별 테스트
- **계약 테스트(Contract Tests)**: 팀 간 서비스 인터페이스 호환성 보장
- **UI/E2E 테스트**: 핵심 사용자 경로만 테스트, 유지보수 비용 높음

"높은 수준일수록 적은 수의 테스트를 가져야 한다"는 핵심 원칙이다.

---

## Google의 테스트 크기 분류

### 크기 정의 [정의/규정]

Google은 테스트를 크기별로 분류한다(자원과 실행 시간 기준) [https://testing.googleblog.com/2010/12/test-sizes.html]:
- **소형 테스트**: 60초 미만 실행, 단일 스레드/프로세스/머신, 네트워크/DB/파일시스템 접근 불가
- **중형 테스트**: 300초(5분) 미만 실행, 외부 자원 부분 접근 가능
- **대형 테스트**: 900초(15분) 미만 실행, E2E/시스템 테스트, 네트워크/DB/UI 접근 가능

### 공표된 비율 [데이터]

Google의 권장 배분: 70% 유닛 테스트, 20% 통합 테스트, 10% E2E 테스트 [https://testing.googleblog.com/2015/04/just-say-no-to-more-end-to-end-tests.html].

---

## E2E 테스트에 대한 Google의 주장 [주장]

"Just Say No to More End-to-End Tests"(2015)에서 Google은 E2E 테스트의 문제점을 제시한다 [https://testing.googleblog.com/2015/04/just-say-no-to-more-end-to-end-tests.html]:
- **느린 피드백**: 유닛 테스트보다 훨씬 오래 실행
- **불안정성(Flakiness)**: 실제 코드 오류와 무관하게 실패
- **디버깅 어려움**: 실패 원인 추적이 시간 소모적
- **유지보수 부담**: 시스템 진화에 따른 지속적 수정 필요

Google은 E2E 테스트를 높은 가치 시나리오에만 제한하고, 테스트 피라미드 구조를 유지할 것을 권장한다.

---

## Testing Trophy (Kent C. Dodds)

### 구조 [정의/규정]

Dodds는 2018년 Testing Trophy를 제시한다 [https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications]:
- **정적 분석(Static)**: ESLint, Flow 같은 코드 분석 도구
- **유닛 테스트**: 개별 함수/클래스/객체 테스트, 의존성 mock 처리
- **통합 테스트(가장 큰 투자)**: 여러 유닛이 협력하는 경우 테스트
- **E2E 테스트**: mock 최소화, 실제 사용 시나리오

### 핵심 원칙 [주장]

"The more your tests resemble the way your software is used, the more confidence they can give you." Dodds는 테스트가 실제 사용 패턴을 반영할수록 신뢰도가 높아진다고 주장한다 [https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications]. 투자(개발 시간) 대비 회수(신뢰도)를 극대화하는 것이 목표다.

---

## Flaky 테스트

### Google의 데이터 [데이터]

"Software Engineering at Google" 11장은 flaky 테스트를 분석한다 [https://abseil.io/resources/swe-book/html/ch11.html]. Google의 flaky 비율은 약 0.15%로, 매일 수천 건의 flake가 발생함을 의미한다. Google은 flake 비율이 1%에 가까워지면 테스트 가치가 감소한다고 보고한다.

### 원인 및 대응 [정의/규정]

비결정적 행동(시간, 스레드 스케줄링, 네트워크 지연)이 주요 원인이다. 대응 방식은 자동 재실행(flake 비율이 낮을 때 CPU 사이클로 엔지니어 시간 절감)이나, 모든 테스트가 hermetic해야 한다는 원칙이다: 테스트가 환경 설정, 실행, 정리에 필요한 모든 정보를 포함해야 한다.

---

## TDD 실증 연구

### 메타분석 결과 [데이터]

Rafique와 Mišić의 메타분석(2013, 27개 연구)은 TDD가 생산성에 거의 영향이 없음을 발견했다 [https://link.springer.com/article/10.1007/s10664-016-9490-0]. 산업 실험에서는 생산성이 저하되었으나, 학술 실험에서는 증가했다.

### Fucci 연구 [데이터]

Fucci et al.(2018, 2021)의 종단 연구는 TDD가 외부 품질과 개발자 생산성에 통계적으로 유의미한 영향을 주지 않음을 보고했다 [https://neverworkintheory.org/2016/10/05/test-driven-development.html]. 연구들은 TDD가 기능 품질을 개선할 수 있으나 생산성 향상은 미흡함을 보여준다.

---

## 코드 커버리지

### 업계 기준 [데이터]

Google은 커버리지 목표를 [https://testing.googleblog.com/2020/08/code-coverage-best-practices.html]:
- 60%: 수용 가능(Acceptable)
- 75%: 칭찬할 만함(Commendable)
- 90%: 모범적(Exemplary)

성숙한 조직은 70~85% 라인 커버리지를 유지한다.

### 위험 기반 접근 [주장]

고정 목표보다 코드 중요도별 차등 목표를 권장한다 [https://testing.googleblog.com/2020/08/code-coverage-best-practices.html]: 결제/인증/데이터 무결성은 90% 이상, UI/관리 도구는 60~70%. 테스트 개수보다 "어디"에 커버리지가 집중되었는지와 테스트가 실제로 행동을 검증하는지가 중요하다.

---

## Mutation Testing

### 정의 [정의/규정]

Mutation testing은 프로그램에 작은 오류(mutant)를 삽입하여 테스트 스위트의 탐지 능력을 평가한다 [https://research.google/pubs/state-of-mutation-testing-at-google/]. 테스트가 mutant를 탐지할 때(테스트 실패) "kill"한다고 표현하고, 스위트 가치는 kill된 mutant 비율로 측정된다.

### Google의 산업 사용 사례 [데이터]

Google은 "Practical Mutation Testing at Scale"(2021)에서 확장 가능한 mutation testing 시스템을 발표한다 [https://research.google/pubs/practical-mutation-testing-at-scale-a-view-from-google/]. 시스템은:
- 코드 리뷰 중 변경된 코드만 mutation(전체 코드베이스 대신)
- 관련성 낮은 mutant 필터링
- 과거 성능 기반 mutation operator 선택

Google의 6,000명 엔지니어와 14,000명 코드 작성자가 의무 코드 리뷰 프로세스에서 사용한다.

---

## ISTQB 테스트 레벨

### 정의 [정의/규정]

ISTQB Foundation Level은 네 가지 테스트 레벨을 정의한다 [https://glossary.istqb.org/]:

**컴포넌트 테스팅(유닛 테스팅)**
단일 함수, 클래스, 모듈, 저장 프로시저의 로직을 독립적으로 검증. Test double(stub, mock, fake)로 의존성 대체.

**통합 테스팅**
통합된 컴포넌트 간 인터페이스와 상호작용을 검증. 모듈 경계의 결함 노출.

**시스템 테스팅**
완전 통합 애플리케이션을 지정된 요구사항에 대해 검증.

**수용 테스팅(Acceptance Testing)**
비즈니스 필요 충족 여부 판단. 시스템 테스팅(기술 요구사항)과 달리 사업상 요구사항 검증.

---

## 출처

> [1차] = 원저자·원기관 발행 / [2차] = 제3자의 정리·집계

- [2차] Cohn, M. "Succeeding with Agile" (2009) – https://www.leapwork.com/blog/what-is-test-automation
- [1차] Fowler, M. "The Practical Test Pyramid" – https://martinfowler.com/articles/practical-test-pyramid.html
- [1차] Google Testing Blog "Test Sizes" (2010) – https://testing.googleblog.com/2010/12/test-sizes.html
- [1차] Google Testing Blog "Just Say No to More End-to-End Tests" (2015) – https://testing.googleblog.com/2015/04/just-say-no-to-more-end-to-end-tests.html
- [1차] Google Testing Blog "Code Coverage Best Practices" (2020) – https://testing.googleblog.com/2020/08/code-coverage-best-practices.html
- [1차] Dodds, K. C. "The Testing Trophy and Testing Classifications" – https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications
- [1차] Abseil Software Engineering at Google, Chapter 11: Testing Overview – https://abseil.io/resources/swe-book/html/ch11.html
- [1차] Abseil Software Engineering at Google, Chapter 14: Test Sizes – https://abseil.io/resources/swe-book/html/ch14.html
- [1차] Google Research "Practical Mutation Testing at Scale" (2021) – https://research.google/pubs/practical-mutation-testing-at-scale-a-view-from-google/
- [1차] Google Research "State of Mutation Testing at Google" – https://research.google/pubs/state-of-mutation-testing-at-google/
- [1차] Rafique & Mišić, "The Effects of Test-Driven Development on External Quality and Productivity: A Meta-Analysis" – https://link.springer.com/article/10.1007/s10664-016-9490-0
- [2차] Never Working In Theory, "Test-Driven Development" – https://neverworkintheory.org/2016/10/05/test-driven-development.html
- [1차] ISTQB Glossary – https://glossary.istqb.org/
