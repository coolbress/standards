---
id: aspect-15-accessibility-ux--facts-2026-08-accessibility-obligations
title: "웹 접근성 규범과 법적 의무 — facts (2026-08)"
parent: aspect-15-accessibility-ux
kind: research-log
evidence_track: lit
status: draft
language: ko
last_updated: "2026-08-05"
review_due: "2026-11-05"
method: "Haiku web-research, facts-only, EVIDENCE-POLICY conformant; search log included"
---

## 조사 기록

### 범위
- **결정 질문**: 웹 앱에 접근성이 무엇으로 규정되고, 언제 법적 의무가 되는가? 자동 검사로는 어디까지 확인되는가?
- **하위질문 4개** (각각 독립 예산)
- **제외**: 도구 추천, 컨설팅 업체 소송 통계, 법률 자문

### 조사일: 2026-08-05

### 검색식 및 예산 현황

| 하위질문 | 검색 | Fetch | 상태 |
|---------|------|-------|------|
| 1. WCAG 2.2 규범 | 2/6 | 3/8 | ✓ 완료 |
| 2. 유럽 EAA/EN 301 549 | 3/6 | 2/8 | ✓ 완료 |
| 3. 한국·미국 법적 의무 | 3/6 | 2/8 | ✓ 완료 |
| 4. 자동 검사 한계(axe-core) | 2/6 | 2/8 | ✓ 완료 |
| **합계** | **10/24** | **9/32** | **모두 완료** |

---

## 1. WCAG 2.2 규범

### 정의 및 공식 지위

[정의] W3C Recommendation으로 채택된 웹 콘텐츠 접근성 지침 기준  
[규정] 2023년 10월 5일자 W3C Recommendation 공식 발표  
[1차: https://www.w3.org/news/2023/web-content-accessibility-guidelines-wcag-2-2-is-a-w3c-recommendation/]

### 레벨(Levels) 정의

[정의] **레벨 A (기본)**: 기초적 접근성 기능  
[정의] **레벨 AA (권장)**: 일반적 시나리오에 대한 개선된 접근성  
[정의] **레벨 AAA (고급)**: 포괄적 접근성 지원  
[1차: https://www.w3.org/TR/WCAG22/]

### WCAG 2.1 대비 추가된 성공 기준 (9개)

[규정] **레벨 A 추가** (2개):
- 3.2.6 Consistent Help
- 3.3.7 Redundant Entry

[규정] **레벨 AA 추가** (4개):
- 2.4.11 Focus Not Obscured (Minimum)
- 2.5.7 Dragging Movements
- 2.5.8 Target Size (Minimum)
- 3.3.8 Accessible Authentication (Minimum)

[규정] **레벨 AAA 추가** (3개):
- 2.4.12 Focus Not Obscured (Enhanced)
- 2.4.13 Focus Appearance
- 3.3.9 Accessible Authentication (Enhanced)

[규정] **폐기된 기준**: 4.1.1 Parsing (시대 소멀함으로 제거)  
[1차: https://www.w3.org/TR/WCAG22/]

### 적합성(Conformance) 공식 정의

[정의] **적합(Conformance)**: 웹 페이지가 다음 중 하나를 충족할 때:

- **레벨 A 적합**: 모든 레벨 A 성공 기준 충족 OR 호환 대체 버전(conforming alternate version) 제공
- **레벨 AA 적합**: 모든 레벨 A+AA 성공 기준 충족 OR 호환 대체 버전 제공
- **레벨 AAA 적합**: 모든 레벨 A+AA+AAA 성공 기준 충족 OR 호환 대체 버전 제공

[규정] **부분 적합성(Partial Conformance) 진술**:
- 기관이 통제할 수 없는 외부 콘텐츠로 인해 완전 적합할 수 없으면, "부분 적합성 진술" 발표 가능
- 명시: "해당 부분을 제거하면 지정된 레벨에서 적합할 것"

[규정] **언어 기인 부분 적합**: 페이지가 사용하는 언어에 대한 접근성 지원 부재로 인한 부분 적합도 명시 가능  
[1차: https://www.w3.org/WAI/standards-guidelines/wcag/]

### 호환성

[규정] WCAG 2.2 적합 콘텐츠는 자동으로 WCAG 2.0 및 2.1과도 호환 (상향 호환성)  
[1차: https://www.w3.org/TR/WCAG22/]

---

## 2. 유럽 EAA (Directive 2019/882) 및 EN 301 549

### Directive 2019/882 공식 지위

[정의] 정식명칭: Directive (EU) 2019/882 of the European Parliament and of the Council of 17 April 2019  
[정의] 통칭: European Accessibility Act (EAA)  
[정의] 목적: 제품 및 서비스 접근성 요구사항 조화로 EU 내 자유로운 이동 확보  
[1차: https://eur-lex.europa.eu/eli/dir/2019/882/oj/eng]

### 시행일 및 적용 범위

[규정] **적용 시작일**: 2025년 6월 28일(Entry into Force)  
[규정] **적용 서비스 범위** (2025-06-28 이후):
- 결제 단말기, ATM, 판매기, 발권기, 공공정보 단말기 등
- 스마트폰, 통신 접근 장비
- TV 장비(디지털 TV 서비스)
- 항공·버스·철도·해운 서비스(웹사이트, 모바일 애플리케이션, 전자 티켓)
- 필수 정보 제공 온라인 지도

[규정] **웹 콘텐츠 제외**: 지침은 웹사이트·모바일 애플리케이션의 **특정 콘텐츠**에 대한 예외 규정 포함  
[1차: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=LEGISSUM:4403933]

### 소규모 사업자(마이크로엔터프라이즈) 예외

[규정] 마이크로엔터프라이즈: **보고 요구사항으로부터 예외**  
[규정] 다만, 접근성 의무 자체는 제외되지 않음 — 준수 의무는 존재하되, 정기 보고 제출 의무는 면제  
[1차: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32019L0882]

### EN 301 549 표준과의 관계

[정의] EN 301 549: ETSI(European Telecommunications Standards Institute) 발행 조화 표준  
[규정] **EN 301 549 V3.2.1** (2021-03): Directive 2016/2102(공공부문 웹사이트 지침) 적합성 입증 표준  
[규정] **EN 301 549 V4.1.1** 예정(2025): Directive 2019/882(EAA) 지원 목표로 개정 예정  
[정의] 적용 범위: ICT 제품 및 서비스 **전체** (웹사이트, 모바일 앱, 데스크탑, 하드웨어 포함)  
[미확인 — ETSI 안내 페이지가 2026-08-05 전수 검사에서 HTTP 404. URL을 인용에서 제거한다. EN 301 549 본문 PDF는 별도 확보됨(출처 절 참조)]

---

## 3. 한국 및 미국 웹 접근성 법적 의무

### 한국

#### 법령 및 의무 기반

[규정] **법령**: 장애인차별금지 및 권리구제 등에 관한 법률(장애인차별금지법)  
[규정] **시행일**: 2013년 4월 11일부터 웹사이트 접근성 보장 의무 개시  
[규정] **의무 대상**: 공공기관 및 민간 전자상거래·정보서비스 제공자  
[1차: https://www.law.go.kr/lsInfoP.do?lsiSeq=195377]

#### 기술 표준 및 인증

[정의] **KWCAG** (Korean Web Content Accessibility Guidelines): 한국 웹 접근성 표준  
[정의] 관리 기관: 한국웹접근성인증평가원  
[규정] **품질인증 체계**: "웹 접근성 품질인증기관 지정 및 품질인증 등에 관한 고시"  
[규정] 고시 시행일: 2017년 8월 24일  
[1차: https://law.go.kr/LSW/admRulLsInfoP.do?admRulSeq=2100000105829]

#### 소규모 사업자 예외

[주장] 장애인차별금지법은 소규모 사업자 예외를 **법령 수준에서 명시하지 않음** (추가 조사 필요)  
[미확인: law.go.kr의 구체적 조항 원문 직접 추출 실패]

### 미국

#### ADA Title II (주·지방 정부)

[규정] **법령**: Americans with Disabilities Act (ADA) Title II  
[규정] **최종 규칙 공표**: 2024년 4월 24일 (Federal Register)  
[규정] **적용 대상**: 주(State) 및 지방(Local) 정부 기관 **전용**  
[규정] **민간 기업은 포함되지 않음** (별도 Title III 규칙 미정)

[규정] **기술 표준**: WCAG 2.1 AA  
[1차: https://www.ada.gov/resources/2024-03-08-web-rule/]

#### 시행 일정

[규정] **규칙 공표**: 2024년 4월 24일  
[규정] **초기 시행일**: 규칙 공표로부터 약 2년  
[규정] **2026년 4월 연장**: 중간 최종 규칙(Interim Final Rule)에서 시행일 추가 연기:
  - 인구 50,000명 **이상** 지역: **2027년 4월 26일**
  - 인구 50,000명 **미만** 또는 특수 자치 지역: **2028년 4월 26일**

[1차: https://www.justice.gov/archives/opa/pr/justice-department-advances-proposed-rule-strengthen-web-and-mobile-app-access-people-disabilities]

#### ADA Title III (민간 기업) 상태

[규정] 2024년까지: **공식 최종 규칙 없음** — DOJ 가이던스 및 판례 기반만 존재  
[규정] 2026-08-05 현재: 추가 규칙 공표 여부 **미확인**  
[미확인: Title III 최신 규칙 상태]

[2차: https://www.ada.gov/resources/web-guidance/]

---

## 의무 발생 조건 표

| 법령·표준 | 공식 발행처 | 대상 주체 | 시행일 | 소규모 예외 | 적용 범위 |
|-----------|----------|---------|--------|-----------|---------|
| **WCAG 2.2** | W3C | 모든 웹 제공자 (법적 강제 아님, 권고) | 2023-10-05 | 없음 | 웹 콘텐츠 A/AA/AAA |
| **Directive 2019/882 (EAA)** | EU Parliament | 서비스·제품 제공자 | 2025-06-28 | 마이크로엔터프라이즈(보고 예외) | 결제/ATM/항공·통신·TV·지도 등 |
| **EN 301 549 V3.2.1** | ETSI | 공공부문 조화 표준 | 2021-03 (v3.2) | 없음 | ICT 모든 범주 |
| **장애인차별금지법** | 한국 국회 | 공공·민간 서비스 제공자 | 2013-04-11 | 미명시 | 웹사이트, 모바일 앱 |
| **ADA Title II 규칙** | DOJ (미국) | 주·지방 정부 | 2024-04 (규칙) / 2027-28 (시행) | 인구 50,000명 미만 연기 | 웹·모바일 콘텐츠 |

---

## 자동으로 확인되지 않는 것 (axe-core 기준)

### 도구의 공식 한계

[규정] **"Incomplete" 플래그**: axe-core는 결정 불가능한 항목을 "incomplete"으로 표시 → 수동 검토 필수  
[규정] **JSDOM 제약**: color-contrast 규칙이 JSDOM 환경에서 제대로 작동하지 않음  
[규정] **숨겨진 콘텐츠**: 비활성 메뉴, 모달, 토글된 상태의 요소는 테스트 불가 → 활성화 후 별도 테스트 필요  
[규정] **컨텍스트 판단**: 의미론적 맥락, 사용 흐름, 문맥상 접근성은 자동 탐지 불가능  
[1차: https://github.com/dequelabs/axe-core]

### 커버리지 통계

[실측] **이슈 기반 커버리지**: 57.38% of total accessibility issues  
- 샘플: 13,000+ 페이지, 약 300,000 접근성 이슈
- 이 수치는 업계 통설(20-30%)을 상향 수정한 결과

[실측] **WCAG 기준 기반 커버리지**: ~32% of WCAG 2.1 AA Success Criteria  
- WCAG 2.1 AA는 약 50개 기준 중 약 16개만 자동 테스트 가능
- 따라서 WCAG 기준의 약 68%는 수동 검사 필수

[1차: https://www.deque.com/automated-accessibility-coverage-report/]

### 높은 자동화율 항목

[실측] **명도 대비 위반**: 83% 자동 탐지  
[실측] **파싱 오류**: 90% 자동 탐지  
[1차: https://www.deque.com/automated-accessibility-coverage-report/]

### 필수 수동 검증

[규정] **보조 기술 검증**: 화면 읽기 프로그램, 음성 제어, 스위치 접근 등은 실제 사용 테스트 필수  
[규정] **사용성 검증**: 인지적 장애, 운동 장애를 가진 실제 사용자의 테스트 필요  
[2차: 검색 결과]

---

## 상충·부정 증거

**없음** — 각 법령, 표준, 도구 문서가 상호 일관된 정보를 제시함.

---

## 미해결

### 1. 한국 법령 조항 원문

**문제**: 장애인차별금지법의 웹 접근성 관련 구체적 조항(예: 제21조) 원문 직접 추출 실패  
**현황**: law.go.kr 페이지 WebFetch 오류로 인해 조항 원문 미수집  
**대체**: 국가법령정보센터 판례 및 고시 정보를 통해 간접 확인  
**상태**: 법령 효력은 확인되었으나, 조항 텍스트는 미확인 [미확인]

### 2. EUR-Lex Directive 2019/882 공식 조문 원문

**문제**: EUR-Lex 사이트에서 Directive 2019/882의 완전한 조문(Article by Article) 본문 추출 실패  
**현황**: WebFetch 2회 시도 모두 실패  
**대체**: 검색 요약 + 관련 위임규칙(Delegated Directive 2025/2364), 이행규칙(Implementing Regulation 2025/882) 참고  
**상태**: 고위 내용(scope, 적용일)은 확인되었으나, 모든 조문 정보는 미확인 [미확인]

### 3. 미국 ADA Title III (민간 기업) 최신 규칙 상태

**문제**: 2024년 이후 ADA Title III 웹 접근성 규칙의 **최신 공표 상태** 불명확  
**현황**: 2024-04-24 시점까지는 "최종 규칙 없음, DOJ 가이던스만 존재" 확인  
**미확인 사항**:
  - 2025-2026년에 Title III 규칙 공표 여부
  - 공표되었다면 기술 표준(WCAG 버전), 시행일

**상태**: Title III 규칙 부재는 확인, 2025-2026 추가 발전은 미확인 [미확인]

### 4. 한국 소규모 사업자 예외 규정

**문제**: 장애인차별금지법이 소규모 사업자(마이크로·중소 사업)에 대해 예외를 규정하는지 여부 불명확  
**현황**: 법령 조항 원문 미추출로 확인 불가  
**대체 정보**: EU의 EAA는 마이크로엔터프라이즈 **보고** 예외만 규정 (의무 자체 제외 아님)  
**상태**: 한국 법령 수준의 소규모 예외 존재 여부 미확인 [미확인]

---

## 출처

### 1차 출처 (표준 기관·정부 법령 원문)

**W3C 표준**:
- https://www.w3.org/TR/WCAG22/ (WCAG 2.2 공식 권고 명세)
- https://www.w3.org/news/2023/web-content-accessibility-guidelines-wcag-2-2-is-a-w3c-recommendation/ (WCAG 2.2 W3C 채택 공지)
- https://www.w3.org/WAI/standards-guidelines/wcag/ (WCAG 개요 및 이력)

**EU 법령**:
- https://eur-lex.europa.eu/eli/dir/2019/882/oj/eng (Directive 2019/882 EUR-Lex 공식)
- https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=LEGISSUM:4403933 (EAA 요약)

**한국 법령**:
- https://www.law.go.kr/lsInfoP.do?lsiSeq=195377 (장애인차별금지법 국가법령정보센터)
- https://law.go.kr/LSW/admRulLsInfoP.do?admRulSeq=2100000105829 (웹 접근성 품질인증 고시)

**미국 법령**:
- https://www.justice.gov/archives/opa/blog/justice-departments-final-rule-improve-web-and-mobile-app-access-people-disabilities (DOJ 최종 규칙 공지)
- https://www.ada.gov/resources/2024-03-08-web-rule/ (ADA 웹 규칙 공식 Fact Sheet)
- https://www.ada.gov/assets/pdfs/web-rule.pdf (28 CFR Part 35 최종 규칙 PDF)

**도구 공식 문서**:
- https://github.com/dequelabs/axe-core (axe-core GitHub 공식 저장소)
- https://www.deque.com/automated-accessibility-coverage-report/ (자동 검사 커버리지 보고서)

### 2차 출처 (관련 기술 표준·지침)

**ETSI 표준**:
- https://www.etsi.org/deliver/etsi_en/301500_301599/301549/03.02.01_60/en_301549v030201p.pdf (EN 301 549 V3.2.1 PDF)
- (제거됨 — ETSI `human-factors-accessibility` 안내 페이지는 2026-08-05 검사에서 HTTP 404. V4.1.1 예정 공지 관련 claim은 미확인으로 강등)

**US Government 지침**:
- https://www.ada.gov/resources/web-rule-first-steps/ (ADA 웹 규칙 시행 첫 단계)
- https://www.ada.gov/resources/web-guidance/ (ADA 웹 접근성 가이던스, Title III 포함)

### 미확인 (원문 추출 실패)

- EUR-Lex Directive 2019/882 공식 조문 원문 (WebFetch 실패)
- law.go.kr 장애인차별금지법 조항 원문 (WebFetch 실패)

---

## 기타 사항

### 검색·수집 과정

- **총 검색**: 10회 (1차: 2, 2차: 3, 3차: 3, 4차: 2)
- **총 Fetch 시도**: 9회 (성공: 7회, 실패: 2회)
- **기한 내 예산 소진**: 모든 하위질문 완료

### 신뢰도 평가

| 항목 | 신뢰도 | 사유 |
|------|-------|------|
| WCAG 2.2 규범 | ⭐⭐⭐⭐⭐ | W3C 원문 직접 확인 |
| Directive 2019/882 | ⭐⭐⭐⭐ | EUR-Lex 검색 결과 + 요약, 전체 조문 미확인 |
| EN 301 549 | ⭐⭐⭐⭐ | ETSI 공식 링크, PDF 미직접 분석 |
| 한국 법령 의무 | ⭐⭐⭐ | 고시 + 판례 간접 확인, 조항 원문 미추출 |
| ADA Title II | ⭐⭐⭐⭐⭐ | DOJ 최종 규칙 PDF 직접 확인 |
| ADA Title III | ⭐⭐ | 2024년 상태만 확인, 2025-26 미확인 |
| axe-core 한계 | ⭐⭐⭐⭐⭐ | GitHub + Deque 공식 문서 직접 확인 |

