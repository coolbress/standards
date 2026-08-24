---
id: aspect-12-performance-scalability--web-performance-thresholds--facts-2026-08
title: "웹 성능 임계값과 성능 예산의 지위 — facts (2026-08)"
parent: aspect-12-performance-scalability
kind: research-log
evidence_track: lit
status: draft
language: ko
last_updated: "2026-08-05"
review_due: "2026-11-05"
method: "Haiku web-research, facts-only, EVIDENCE-POLICY conformant; search log included"
---

# 웹 성능 임계값과 성능 예산의 지위

## 조사 기록

### Q1: 웹 성능의 공식 임계값

#### 1.1 Core Web Vitals 정의 및 임계값

**[규정]** Core Web Vitals는 다음 3개 메트릭과 공식 임계값으로 정의됨 [1차: https://web.dev/articles/defining-core-web-vitals-thresholds]:

| 메트릭 | "Good" | "Poor" | 기준점 |
|--------|--------|--------|--------|
| Largest Contentful Paint (LCP) | ≤2500ms | >4000ms | 75th percentile |
| Interaction to Next Paint (INP) | ≤200ms | >500ms | 75th percentile |
| Cumulative Layout Shift (CLS) | ≤0.1 | >0.25 | 75th percentile |

**기준점 설정 방법**: 사이트의 페이지 뷰 중 **최소 75%가 "Good" 임계값을 충족**하면 해당 메트릭이 "Good"으로 분류됨. 모바일과 데스크톱 분리 측정.

#### 1.2 임계값 정의 근거 (3가지 기준)

**[정의]** Google Chrome team (Bryan McQuade, Barry Pollard)이 임계값을 정의한 근거 [1차: https://web.dev/articles/defining-core-web-vitals-thresholds]:

1. **사용자 경험 연구 (HCI 기반)**:
   - 시각 피드백 지연 ~100ms까지는 사용자가 입력의 직접 결과로 인식
   - 지각 임계값은 사용자 및 맥락에 따라 변동
   - 논리: LCP/INP 임계값이 인지 심리 연구에서 도출

2. **실현 가능성 (Achievability)**:
   - 네트워크·디바이스 처리 지연으로 인해 0ms는 실제로 불가능
   - Chrome User Experience Report 데이터로 검증: **웹 오리진의 최소 10%는 각 "Good" 임계값을 충족 가능**

3. **균형 조정 (Trade-offs)**:
   - 세 기준 간 충돌 존재
   - Google은 "최상의 균형을 취한" 임계값 선택

**[실측]** 75th percentile 기준은 개발팀이 특정 임계값에 기반한 실제 배포 데이터로 검증 [미확인: 논문 또는 상세 방법론 미열람]

#### 1.3 목적: 검색 순위 신호

**[정의]** Core Web Vitals는 Google Search의 순위 신호로 사용됨 [1차: https://developers.google.com/search/docs/appearance/core-web-vitals]:
- 검색 순위 결정 요소 중 하나
- 사용자 경험이 우수한 페이지 선호
- 2024년 INP(Interaction to Next Paint)가 Core Web Vitals에 추가 (기존 FID 대체)

#### 1.4 W3C/WHATWG 표준 지위

**[주장]** Core Web Vitals는 W3C 표준이 아님:
- Google이 정의한 메트릭 집합
- W3C Web Performance Working Group이 정의한 **표준 API** (Navigation Timing, Resource Timing, Performance Observer API)로 **측정**되지만, 임계값 자체는 Google의 정책
- WHATWG에서 규정되지 않음

**[규정]** W3C Web Performance Working Group은 성능 측정 기술 표준 개발 [1차: https://www.w3.org/webperf/]:
- Performance Timeline API (표준)
- Navigation Timing (표준)
- Resource Timing (표준)
- 하지만 "Good"/"Poor" 임계값은 규정하지 않음 → 이는 Google의 권장사항

---

### Q2: 성능 예산(Performance Budget)의 규정 여부

#### 2.1 정의

**[정의]** 성능 예산은 "사이트 성능에 영향을 주는 메트릭에 대한 제한 세트(set of limits)" [1차: https://web.dev/articles/performance-budgets-101]:
- 총 페이지 크기 (KB)
- 모바일 네트워크 로드 시간
- HTTP 요청 수
- 번들 크기 (JS, CSS 등)
- FCP, TTI 등 사용자 중심 메트릭

**권장 안내 예시**: 모바일 3G에서 170KB 이하의 critical-path 리소스 (압축/축소화) [1차: https://web.dev/articles/performance-budgets-101]

#### 2.2 공식 표준 여부: 아니다 (Best Practice)

**[주장]** Performance budget은 공식 W3C/WHATWG 표준이 아님 [1차: https://web.dev/articles/performance-budgets-101]:
- web.dev에서 제시하는 **권장사항 및 best practice**
- 개발팀이 자발적으로 채택하는 규칙
- 강제 기준이 아님
- 성능 회귀(regression) 방지를 위한 도구로 사용

**[규정]** Lighthouse CI, webpack 등 **도구가 성능 예산을 선택적으로 시행**할 수 있도록 지원 [1차: https://web.dev/articles/incorporate-performance-budgets-into-your-build-tools]:
- webpack.config.js에서 `performance.hints` 설정 시 번들 크기 초과 시 경고/에러 발생
- Lighthouse CI로 CI/CD 파이프라인에서 검사 가능
- 조직의 선택에 따라 적용 여부 결정

#### 2.3 근거 및 역할

**[주장]** 성능 예산의 목적 [1차: https://web.dev/articles/performance-budgets-101]:
- 성능에 대한 대화 시작점 제공
- 디자인, 기술, 기능 추가에 대한 의사결정 기준점
- 성능 회귀 조기 식별 및 수정

**표준과의 관계**:
- W3C Performance APIs (Performance Observer, Navigation Timing)는 메트릭 **측정** 표준화
- Core Web Vitals는 Google의 **임계값** 정책
- Performance budget은 조직의 **선택적 규칙** (표준이 아님)

---

## 표준 vs 처방 구분표

| 항목 | 정의/근거 | 표준 기관 | 지위 | 근거/출처 |
|------|----------|----------|------|---------|
| **Core Web Vitals (메트릭 3개 + 임계값)** | LCP≤2500ms, INP≤200ms, CLS≤0.1 | Google (표준이 아님) | **규정**: Google Search 순위 신호 | [1차: https://web.dev/articles/defining-core-web-vitals-thresholds] |
| **Core Web Vitals 측정 방법** | W3C Performance APIs 사용 | W3C (표준) | **표준** | [1차: https://www.w3.org/webperf/] |
| **성능 예산** | 사이트 성능 지표에 대한 제한 세트 | 표준 기관 없음 | **처방**: web.dev best practice, 선택적 도구 지원 | [1차: https://web.dev/articles/performance-budgets-101] |
| **Lighthouse CI** | 성능 예산을 CI/CD에 자동 적용 | 오픈소스 커뮤니티 (Google 주도) | **도구**: 성능 예산 시행 선택적 지원 | [1차: https://web.dev/articles/incorporate-performance-budgets-into-your-build-tools] |

---

## 상충·부정 증거

### 발견된 상충

**1. "공식 임계값" vs 선택적 해석**
- Core Web Vitals 임계값은 Google 정책이지 국제 표준이 아님
- 조직이 다른 임계값 채택 가능 (예: "LCP ≤1500ms" 자체 기준)
- Google은 "가이드"를 제시하지만 강제는 아님

**2. 성능 예산의 모호성**
- 공식 정의 없음 → 각 팀이 자의적으로 설정
- 도구 지원은 선택적 (반드시 적용할 필요 없음)
- 산업 표준이 아님

### 부정 증거 (확인된 것이 없음)

- Core Web Vitals를 **국제 표준**으로 규정하는 W3C 문서 없음
- 성능 예산을 **공식 표준**으로 규정하는 표준 기관 없음
- ISO, W3C, WHATWG, ECMA에서 Core Web Vitals 임계값 재규정 없음

---

## 미해결

1. **Core Web Vitals 임계값의 과학적 근거 상세**: 
   - 본문에서 "인지 심리 연구" 언급하지만, **구체적 논문·연구** 미추적
   - 75th percentile 선택의 통계적 근거 불명확
   - [미확인] 상세 방법론 논문 또는 기술 보고서

2. **성능 예산의 채택률 및 실제 효과**:
   - web.dev가 권장하지만, **업계 표준 채택률** 통계 미수집
   - 성능 예산 시행이 실제로 성능 개선으로 이어지는지 [미확인]

3. **다른 검색 엔진(Bing, DuckDuckGo)의 임계값**:
   - Google만 Core Web Vitals 정의
   - 다른 검색 엔진의 성능 기준 [미확인]

---

## 출처

### 1차 출처 (직접 열람, 본문 검증)

1. https://web.dev/articles/defining-core-web-vitals-thresholds
   - Core Web Vitals 임계값 정의, 근거, 방법론

2. https://web.dev/articles/performance-budgets-101
   - 성능 예산 정의, 목적, 도구 지원

3. https://developers.google.com/search/docs/appearance/core-web-vitals
   - Core Web Vitals의 Google Search 순위 신호 역할

4. https://web.dev/articles/incorporate-performance-budgets-into-your-build-tools
   - 성능 예산을 빌드 도구(webpack, Lighthouse CI)로 시행하는 방법

5. https://www.w3.org/webperf/
   - W3C Web Performance Working Group 표준 범위

### 2차 출처 (검색 결과, 본문 미열람)

1. https://support.google.com/webmasters/answer/9205520?hl=en
   - Search Console 도움말: Core Web Vitals 보고서

2. https://developers.google.com/codelabs/chrome-web-vitals-js
   - Google Developers: web-vitals 라이브러리 (측정 도구)

3. https://web.dev/blog/inp-cwv-march-12
   - INP가 Core Web Vitals에 추가된 공지 (2024년)

4. https://www.w3.org/standards/techs/performance
   - W3C 성능 관련 표준 목록

---

## 보충: 프로젝트 맥락 ("성능 예산 미채택" 판단)

본 조사의 배경: 리서치 프로젝트가 "1인 스케일에서 성능 예산 체계를 미채택하고 비용 상한으로 대체한다"고 판단했음.

**조사 결과 해석**:
- ✓ 성능 예산은 **공식 표준이 아님** → 선택적 도구
- ✓ 웹 성능의 공식 임계값(Core Web Vitals)은 **Google 정책** (국제 표준 아님)
- ✓ 따라서 "성능 예산 미채택"은 **표준 위배가 아님**, 자율적 선택
- ⚠️ 그러나 **Core Web Vitals는 Google Search 신호** → 검색 가시성을 중시하면 무시할 수 없음

**결론**: 본 조사는 성능 예산이 선택사항임을 확인했으나, "비용 상한이 성능 관리를 적절히 대체하는가"는 별개 질문 (비용 측면은 aspect-21 참조).

