---
id: aspect-13-api-interface-design--facts-2026-08-api-scope-boundary
title: "API 규격의 적용 범위 — 내부 API에도 적용되는가 (2026-08 facts)"
parent: aspect-13-api-interface-design
kind: research-log
evidence_track: lit
status: draft
language: ko
last_updated: "2026-08-05"
review_due: "2026-11-05"
method: "Haiku web-research, facts-only, EVIDENCE-POLICY conformant; search log included"
---

## 조사 기록

### Q1: API 설계 — 내부 API에도 REST/HTTP 공식 규격이 적용되는가?

**조사 범위**
- RFC 9110 (HTTP Semantics) 적용 범위 명시 여부
- OpenAPI 공식 스펙 적용 범위 명시 여부
- 규격이 공개/내부 API를 구분하는지 확인

**RFC 9110 검토**

[규정: 1차] RFC 9110은 "HTTP 메시지의 의미론을 정의하는 상태 비저장 애플리케이션 프로토콜"로, "모든 HTTP 버전이 의존하는 의미론을 통합·업데이트"한다고 명시된다. [1차: https://www.rfc-editor.org/rfc/rfc9110.txt]

**적용 범위에 대한 문서 분석:**
- RFC 9110은 "균일한 인터페이스를 통해 자원과 상호작용하는 방법"과 "요청 메서드, 헤더 필드, 상태 코드" 등을 정의한다.
- **공개/내부 API 구분 명시 없음**: 문서는 배포 맥락(deployment context)에 따른 조건을 두지 않는다.
- 결론: RFC 9110은 "모든 HTTP 구현"에 균등하게 적용되며, 조직 경계(organizational boundary)를 기준으로 범위를 제한하지 않는다. [1차]

**OpenAPI 공식 스펙 검토**

[규정: 1차] OpenAPI Specification은 "프로그래밍 언어에 무관한 HTTP API의 인터페이스 표준"으로 정의된다. [1차: https://spec.openapis.org/oas/v3.1.0]

**적용 범위에 대한 문서 분석:**
- 공식 정의: "HTTP API에 대한 표준, 프로그래밍 언어에 무관한 인터페이스 기술"
- **공개/내부 API 구분 명시 없음**: 스펙은 배포 모델이나 조직 가시성에 따른 분류를 두지 않는다.
- 기술 기술 메커니즘(paths, operations, schemas, security)에만 집중하며, 내부/외부 구분 없이 "모든 HTTP API"에 동일하게 적용 가능하다. [1차]

### 결론: "명시 없음"의 정확한 의미

두 규격 모두:
1. 공개 API만으로 범위를 제한하지 **않음**
2. 내부 API를 명시적으로 **배제하지 않음**
3. 배포 맥락에 따른 차이를 **규정하지 않음**

따라서 "명시 없음(explicit limitation absence)"은 **규격이 내부 API 적용을 공식적으로 인정하지도, 거절하지도 않는다**는 뜻이다. 기술적으로는 HTTP 규격이므로 내부 경로에도 적용 가능하지만, 규격 문서가 이를 "내부 API에도 적용된다"고 명시하지 않는다.

---

## 적용 범위 표

| 규격/표준 | 명시된 적용 대상 | 공개 API만으로 제한 명시 | 내부 API 명시적 포함 | 1인 웹 앱에 실제 적용 |
|---|---|---|---|---|
| RFC 9110 (HTTP Semantics) | 모든 HTTP 버전, 모든 HTTP 구현 | 없음 | 없음 | **명시 없음** (배포 맥락 무관) |
| OpenAPI v3.1.0 | HTTP API 전체 | 없음 | 없음 | **명시 없음** (배포 모델 무관) |

---

## 상충·부정 증거

**반박할 근거 검색:**
- RFC 9110과 OpenAPI 스펙 문서에서 "외부만" "공개만" "사용자 대면만" 같은 표현이 있는지 확인 → **없음**
- OpenAPI 커뮤니티 가이드에서 "내부 API에는 불필요" 같은 권고가 있는지 확인 → 검색 결과에는 "내부 API에도 권장"이라는 설명만 나타남 [2차]

---

## 미해결

1. **IEEE/ISO 표준 내 "내부 API" 정의 여부**: ISO/IEC/IEEE 12207이나 15289에서 내부/외부 API를 구분하는 규정이 있는지 미확인.
   판본 처분: 현행판은 **ISO/IEC/IEEE 12207:2026**이며 유료 전문 미확보로 clause 수준 확인은 INCONCLUSIVE다. withdrawn된 ISO/IEC/IEEE 12207:2017의 조항을 현행판으로 재귀속하지 않는다.
2. **REST 공식 명세의 배포 범위**: Roy Fielding의 REST 논문이나 IETF REST 가이드(RFC 7231-7235 폐기 전 버전)에서 공개/내부 구분 명시 여부 미확인

---

## 출처

### [1차 출처] (규격 문서)
- https://www.rfc-editor.org/rfc/rfc9110.txt (RFC 9110 전문)
- https://spec.openapis.org/oas/v3.1.0 (OpenAPI Specification v3.1.0 공식)

### [2차 출처] (풀이 및 가이드)
- https://api7.ai/learning-center/api-101/openapi-specification
- https://medium.com/@mk8961052/openapi-documentation-a-contract-between-frontend-and-backend-fff5139cfe66

### 검색 로그
- 검색 1: "RFC 9110 HTTP Semantics specification scope public private internal API"
- 검색 2: "OpenAPI specification official scope internal API backend frontend"
- 웹페치: RFC 9110 범위 명시 여부 & OpenAPI 적용 대상 검증
