---
id: aspect-19-observability-telemetry--facts-2026-08-structured-logging-metrics
title: "구조화 로깅과 최소 메트릭 — facts (2026-08)"
parent: aspect-19-observability-telemetry
kind: research-log
evidence_track: lit
status: draft
language: ko
last_updated: "2026-08-05"
review_due: "2026-11-05"
method: "Haiku web-research, facts-only, EVIDENCE-POLICY conformant"
---

## 조사 기록

**일시**: 2026-08-05  
**질문 범위**: 구조화 로깅과 HTTP 메트릭 규정  
**제외**: 도구 추천, 튜토리얼, 구현 가이드  
**검색 예산**: 하위질문당 ≤6회 (실제: 1-4, 2-4 = 총 8회)  
**fetch 예산**: 하위질문당 ≤8회 (실제: 8회)

---

## 하위 질문 1: 구조화 로깅 규정

### 1.1 OpenTelemetry 로그 규약 — LogRecord 데이터 모델

[규정] [1차: https://opentelemetry.io/docs/specs/otel/logs/data-model/]

OpenTelemetry 사양이 LogRecord에 정의한 필드:

| 필드명 | 타입 | 설명 |
|--------|------|------|
| **Timestamp** | uint64 | UNIX epoch 이후 나노초 |
| **ObservedTimestamp** | uint64 | 이벤트 관측 시각 (나노초) |
| **TraceId** | byte sequence | 분산 추적 ID |
| **SpanId** | byte sequence | 스팬 ID |
| **TraceFlags** | byte | 추적 플래그 |
| **SeverityText** | string | 심각도 문자열 표현 |
| **SeverityNumber** | integer (1-24) | 심각도 숫자 (1=TRACE~24=FATAL) |
| **Body** | AnyValue | 로그 본문/메시지 |
| **Attributes** | Attribute Collection | 구조화된 속성 (key-value) |
| **Resource** | Resource object | 리소스 정보 |
| **InstrumentationScope** | Instrumentation Scope | 계측 범위 |
| **EventName** | string | 이벤트 이름 |

**상관 ID (Correlation)**:
[규정] [1차: https://opentelemetry.io/docs/specs/otel/logs/]  
- TraceId와 SpanId를 로그에 자동 첨부하여 로그-트레이스 직접 상관
- W3C Trace Context 규약 채택 ("includes [TraceId] and [SpanId]")
- "If SpanId is present TraceId SHOULD be also present" (강권 권고, SHOULD)

**민감정보 처리**:
[미확인] OpenTelemetry 사양 본문에서 민감정보 필터링·마스킹에 대한 규정 찾지 못함.

**로그 레벨 규정**:
[미해결] SeverityNumber 범위(1-24)만 정의됨. 표준 매핑표(예: 1=TRACE, 5=DEBUG, 9=INFO 등) 확인 필요. 현재 보유 자료에 매핑 규칙 없음.

---

### 1.2 12-Factor App 로그 팩터 — 원 명제

[규정] [1차: https://12factor.net/logs]

**핵심 명제**:
- "A twelve-factor app never concerns itself with routing or storage of its output stream"
- 앱은 stdout에 "unbuffered" 이벤트 스트림 작성
- "stream of aggregated, time-ordered events collected from the output streams of all running processes"
- 로그 저장소/라우팅은 실행 환경(execution environment) 책임

**원문에 명시된 속성**:
- "one event per line" (행 단위 이벤트)
- 원본 텍스트 형식 (raw text format)

**미언급 항목**:
[미해결] 
- 로그 레벨(INFO, WARN, ERROR): 12-Factor 원문에 언급 없음
- 구조화 형식(JSON): 원문에서 명시 안 함
- 민감정보 처리: 원문에서 언급 안 함

> 주: 12-Factor는 "로그를 어디에 저장할까"만 규정. "로그 내용을 어떻게 구조화할까"는 별도 표준 필요.

---

## 하위 질문 2: 최소 메트릭 세트 + RED/USE 출처

### 2.1 OpenTelemetry Semantic Conventions — HTTP 서버 메트릭

[규정] [1차: https://opentelemetry.io/docs/specs/semconv/http/http-metrics/]

**공식 정의 메트릭 (HTTP 서버)**:

| 메트릭명 | 단위 | 계기 타입 | 안정성 | 상태 |
|----------|------|---------|--------|------|
| `http.server.request.duration` | seconds (s) | Histogram | Stable | Recommended |
| `http.server.active_requests` | {request} | UpDownCounter | Development | Opt-In |
| `http.server.request.body.size` | Bytes (By) | Histogram | Development | Opt-In |
| `http.server.response.body.size` | Bytes (By) | Histogram | Development | Opt-In |

**필수 속성** (모든 메트릭):
- `http.request.method`
- `url.scheme`

**조건부 필수**:
- `error.type` (오류 발생 시)
- `http.response.status_code` (수신/송신 시)
- `http.route` (가능하면)

> 주: `http.server.request.duration`이 유일한 **Stable** 메트릭. 나머지는 Development 상태.

---

### 2.2 RED 방법론 — 출처와 정의

[주장] [2차: https://thenewstack.io/monitoring-microservices-red-method/]
[주장] [2차: https://grafana.com/blog/the-red-method-how-to-instrument-your-services/]

**저자**: Tom Wilkie  
**도입 시기**: 2015년 (Weaveworks에서)  
**정의**: Rate, Errors, Duration (3가지 신호)

- **Rate**: 초당 요청 수
- **Errors**: 실패한 요청 수
- **Duration**: 응답 시간 분포

**지위**: 
- ⚠️ **표준 기관 산출물 아님**
- Tom Wilkie의 개인 처방 (서비스 모니터링에 최적화)
- Google Four Golden Signals의 요청 중심 개편

---

### 2.3 USE 방법론 — 출처와 정의

[주장] [2차: https://www.brendangregg.com/usemethod.html]
[주장] [2차: https://www.brendangregg.com/USEmethod/use-linux.html]

**저자**: Brendan Gregg  
**정의**: Utilization, Saturation, Errors (3가지 신호)

- **Utilization**: 자원 활용률
- **Saturation**: 대기 부하
- **Errors**: 오류율

**지위**: 
- ⚠️ **표준 기관 산출물 아님**
- Brendan Gregg의 개인 처방 (시스템 성능 분석)
- 하드웨어/소프트웨어 리소스 모니터링용

---

## 표준 vs 처방 구분표

| 항목 | 규정 주체 | 표준 기관 산출물 | 지위 |
|------|----------|-----------------|------|
| OpenTelemetry LogRecord | OpenTelemetry | 예 (open standard) | 규정 |
| OpenTelemetry HTTP Metrics | OpenTelemetry | 예 (open standard) | 규정 |
| 12-Factor 로그 팩터 | Adam Wiggins et al. | 아니오 (커뮤니티 실천) | 주장/처방 |
| RED 메트릭 | Tom Wilkie | 아니오 | 주장/처방 |
| USE 메트릭 | Brendan Gregg | 아니오 | 주장/처방 |

---

## 상충·부정 증거

**로그 구조화에 대한 상충**:
- OpenTelemetry: "Attributes collection"으로 key-value 구조화 강조
- 12-Factor: 원문에서 구조화 형식 미규정 (stdout 스트림만)

**메트릭 방법론의 경쟁**:
- RED vs USE는 대안 관계 (리소스 중심 vs 요청 중심)
- 둘 다 표준이 아니므로 선택 문제

---

## 미해결

1. **OpenTelemetry SeverityNumber 표준 매핑**: 
   - 현재: 1-24 범위만 정의
   - 필요: TRACE(1)=DEBUG(5)?=INFO(9)? 등 공식 이름 매핑표

2. **12-Factor 로그 레벨 규정**:
   - 원문에 로그 레벨 개념 없음
   - 권고 레벨 체계 확인 필요 (하위 위임?)

3. **민감정보 처리 공식 규정**:
   - OpenTelemetry: 규약 없음 (Attributes 필터링은 구현 선택)
   - 12-Factor: "keep free of sensitive" 권고만 (규정 아님)

4. **SemConv HTTP 메트릭의 선택 이유**:
   - RED/USE 중 어느 것에 대응? 공식 매핑 없음
   - "Recommended"(1개) vs "Opt-In"(3개) 비율 정당화 미제시

---

## 출처

### 1차 자료 (공식 표준 기관)

- [OpenTelemetry Logs Specification](https://opentelemetry.io/docs/specs/otel/logs/)
- [OpenTelemetry Logs Data Model](https://opentelemetry.io/docs/specs/otel/logs/data-model/)
- [OpenTelemetry HTTP Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/http/http-metrics/)
- [12-Factor App — Logs](https://12factor.net/logs)

### 2차 자료 (저자/커뮤니티 해석)

- [The New Stack — The RED Method](https://thenewstack.io/monitoring-microservices-red-method/)
- [Grafana Labs — The RED Method](https://grafana.com/blog/the-red-method-how-to-instrument-your-services/)
- [Brendan Gregg — USE Method](https://www.brendangregg.com/usemethod.html)
- [Brendan Gregg — USE Method Linux Checklist](https://www.brendangregg.com/USEmethod/use-linux.html)

### 미확인 페이지

- diataxis.fr (하위질문 범위 아님)
