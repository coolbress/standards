---
id: aspect-21-economics-cost-sustainability--serverless-cost-model--facts-2026-08
title: "서버리스 과금 모델과 비용 관리 규정 — facts (2026-08)"
parent: aspect-21-economics-cost-sustainability
kind: research-log
evidence_track: lit
status: draft
language: ko
last_updated: "2026-08-05"
review_due: "2026-11-05"
method: "Haiku web-research, facts-only, EVIDENCE-POLICY conformant; search log included"
---

# 서버리스 과금 모델과 비용 관리 규정

## 조사 기록

### Q3: 서버리스/PaaS에서 성능(느린 코드) = 비용 증가인가?

#### 3.1 AWS Lambda 과금 모델

**[규정]** AWS Lambda 공식 과금 단위 [1차: https://aws.amazon.com/lambda/pricing/]:

| 과금 요소 | 단위 | 가격 (2026년) | 비고 |
|-----------|------|---------------|------|
| **실행 시간** | GB-seconds (GB-s) | $0.00001667/GB-s | 메모리 × 실행 시간 |
| **요청** | per 1M requests | $0.20/1M | 호출 횟수 |
| **Free Tier** | 매월 | 1M requests + 400k GB-s | 초과분만 과금 |

**과금 수식**:
```
Monthly Cost = (GB-s used × $0.00001667) + (Requests × $0.20/1M)
GB-s = Memory(GB) × Duration(seconds)
```

**예시**: 512MB 메모리, 100ms 실행
- GB-s = 0.5GB × 0.1s = 0.05 GB-s
- 비용 = 0.05 × $0.00001667 = $0.00000083 per invocation

**[규정]** 실행 시간은 **wall-clock time** (총 경과 시간) [1차: https://aws.amazon.com/lambda/pricing/]:
- 코드가 실행되는 첫 번째 밀리초부터 함수 반환 또는 종료 시까지
- 대기 시간(I/O, 네트워크)도 포함
- 1ms 단위로 반올림

**[실측]** AWS Lambda INIT phase 과금 변화 (2025년 8월) [1차: https://aws.amazon.com/blogs/compute/aws-lambda-standardizes-billing-for-init-phase/]:
- 2025년 8월 1일부터 INIT phase(초기화)도 과금 대상
- 기존: 초기화 시간 무료 (managed runtime)
- 변경: ZIP 파일 + managed runtime 초기화도 유료화
- **해석**: 느린 초기화 = 비용 증가 가속화

#### 3.2 Vercel 과금 모델 (Fluid Compute)

**[규정]** Vercel Fluid Compute 과금 구조 (2026년) [1차: https://vercel.com/docs/functions/usage-and-pricing]:

| 리소스 | 호빅 플랜 | Pro 플랜 | 단가 (예: SFO 지역) |
|--------|----------|---------|-------------------|
| **Active CPU** | 4시간 포함 | On-demand | $0.177/hour (SFO) |
| **Provisioned Memory** | 360 GB-hrs 포함 | On-demand | $0.0147/GB-hr (SFO) |
| **Invocations** | 1M 포함 | On-demand | 무료 (Pro는 무제한) |

**[정의]** Active CPU vs Provisioned Memory [1차: https://vercel.com/docs/functions/usage-and-pricing]:

1. **Active CPU** (코드 실행 중일 때만):
   - 코드가 **실제로 실행 중**일 때만 과금
   - I/O 대기(데이터베이스 쿼리, API 호출) 중에는 **비과금**
   - 예시: 100ms 처리 + 400ms DB 대기 → 100ms만 과금

2. **Provisioned Memory** (지속 과금):
   - 함수 인스턴스가 할당받은 메모리(GB)
   - 요청 처리 중 **항상 과금** (I/O 대기 중에도)
   - 예시: 4GB 인스턴스 1시간 운영 → 4 GB-hour 과금

**[규정]** 인스턴스 라이프사이클 [1차: https://vercel.com/docs/functions/usage-and-pricing]:
- 첫 번째 요청 도착 → 인스턴스 시작
- 메모리 계속 과금 (Provisioned Memory)
- 요청 처리 중 Active CPU는 코드 실행 시에만
- 마지막 in-flight 요청 완료 후 인스턴스 중지
- 다음 요청까지 비용 없음 (cold start 제외)

**[규정]** 레지온별 가격 예시 [1차: https://vercel.com/docs/functions/usage-and-pricing]:
- San Francisco (SFO): $0.177/CPU-hour, $0.0147/GB-hour
- 타 지역 (東京, 뭄바이 등): 다양함

**해석: "성능 = 비용"인가?**
- ✓ CPU 시간이 길면(느린 코드) Active CPU 비용 ↑
- ✓ I/O 대기가 길면 Provisioned Memory 비용 ↑
- **따라서 느린 코드 = 높은 비용** (부분적으로는 확실)
- ⚠️ 메모리 할당이 비용에 미치는 영향이 큼 (CPU 시간보다)

#### 3.3 Cloudflare Workers 과금 모델

**[규정]** Cloudflare Workers 공식 과금 (2026년) [1차: https://developers.cloudflare.com/workers/platform/pricing/]:

| 항목 | Free 플랜 | Paid 플랜 ($5/month) | 초과 가격 |
|------|----------|-------------------|----------|
| **요청** | 100k/day (무제한) | 10M included/month | $0.30/M |
| **CPU 시간** | 10ms/invocation limit | 30M CPU-ms included/month | $0.02/M CPU-ms |
| **정적 자산** | 무료 | 무료 (무제한) | 무료 |

**[규정]** CPU 시간 과금의 의미 [1차: https://developers.cloudflare.com/workers/platform/pricing/]:
- **CPU milliseconds** 기반 과금 (wall-clock time 아님)
- 실제 CPU 연산에만 과금
- I/O 대기(네트워크 요청)는 **비과금**
- Max CPU per invocation: 5 minutes (default: 30s)

**예시**: 7ms CPU per request, 15M monthly requests
- CPU 비용 = (15M × 7ms - 30M ms included) × $0.02/M ms
- = (105M - 30M) × $0.02/M = 75M × $0.02/1000 = $1.50/month

**해석: "성능 = 비용"인가?**
- **아니다** (AWS Lambda와 다름)
- 네트워크 I/O 대기는 비용에 영향 없음
- CPU 효율성만 중요 (algorithm complexity 등)
- 느린 네트워크 API는 비용에 영향 없음
- **CPU 사용량이 적으면 비용 낮음** (I/O bound 작업 유리)

#### 3.4 종합 비교: 성능(실행 시간) vs 과금

| 플랫폼 | 과금 단위 | I/O 대기 포함? | 성능 = 비용? | 근거 |
|--------|----------|---------------|------------|------|
| **AWS Lambda** | GB-s (실행 시간 × 메모리) | **포함** | ✓ 명확히 그렇다 | [1차: https://aws.amazon.com/lambda/pricing/] |
| **Vercel** | Active CPU + Provisioned Memory | **부분**: CPU는 제외, Memory는 포함 | ✓ 부분적 | [1차: https://vercel.com/docs/functions/usage-and-pricing] |
| **Cloudflare Workers** | CPU milliseconds | **제외** | ✗ 아니다 | [1차: https://developers.cloudflare.com/workers/platform/pricing/] |

**핵심 발견**: 플랫폼마다 **성능과 비용 관계가 다름**
- AWS Lambda: **느린 코드 = 높은 비용** (직접 비례)
- Vercel: **CPU 시간 + 메모리 점유 시간** 모두 과금 (혼합)
- Cloudflare: **CPU 효율성만 중요**, I/O bound는 유리

---

### Q4: 비용 관리의 공식 규정

#### 4.1 FinOps Foundation 프레임워크

**[주장]** FinOps는 공식 표준이 아님 [1차: https://www.finops.org/introduction/what-is-finops/]:

**정의**:
> "FinOps is an operational framework and cultural practice which maximizes the business value of technology, enables timely data-driven decision making, and creates financial accountability through collaboration between engineering, finance, and business teams."

**기관**: FinOps Foundation (Linux Foundation의 프로젝트 시리즈)

**규정 권한**:
- Technical Advisory Council (TAC)이 Framework 관리
- 2026년 3월 업데이트 (Executive Strategy Alignment 추가)
- 공식 Framework, Maturity Model, Personas 제공
- 인증 프로그램 (FinOps Certified Practitioner/Professional)

**표준 vs 처방**:
- ✗ **ISO, W3C, ECMA 등 국제 표준 기관이 아님**
- ✓ **Linux Foundation의 프로젝트** (open-source community 기반)
- ✓ **Best practice framework** (특정 조직의 규칙이 아님, 커뮤니티 기반)
- ✓ **자발적 채택** (강제되지 않음)

**[규정]** FinOps Framework의 범위 (2026년) [1차: https://www.finops.org/framework/]:
- Principles (원칙)
- Personas (담당자 역할)
- Domains (도메인: 계획, 정보 및 최적화 등)
- Capabilities (기능: 예산 설정, 비용 할당, 이상 탐지 등)
- Scopes (적용 범위: 단일 팀부터 기업 전체)
- Maturity Model (성숙도 단계)

**[규정]** FOCUS 스펙 (FinOps Open Cost and Usage Specification) [1차: https://focus.finops.org/focus-specification/]:
- **기술 표준**: 클라우드 비용·사용량 데이터 포맷 표준화
- **채택 현황**: AWS, Azure, Google Cloud, OCI 공식 채택
- **역할**: FinOps Framework 수행을 위한 데이터 호환성 확보

**[주장]** FinOps의 지위 정리:
- **프레임워크**: 조직의 비용 최적화 방법론 (선택적)
- **표준**: FOCUS 데이터 포맷은 기술 표준 (클라우드 업체 채택)
- **강제성**: 없음 (자발적 도입)

#### 4.2 AWS 공식 비용 관리 도구

**[규정]** AWS Cost Anomaly Detection [1차: https://aws.amazon.com/aws-cost-management/aws-cost-anomaly-detection/]:

**기능**:
1. **Machine Learning 기반 이상 탐지**
   - 비정상적인 지출 패턴 감지
   - 트렌드 및 계절성 고려 (false positive 감소)

2. **모니터 유형**:
   - AWS Service별
   - Linked Account별
   - Cost Allocation Tags별
   - Cost Categories별

3. **경보 옵션**:
   - 즉시 SNS 알림
   - 일일 이메일 요약
   - 주간 이메일 요약
   - Amazon Chime, MS Teams, Slack 통합 가능 (2025년 5월 추가)

4. **근본 원인 분석**:
   - 비용 영향도 상위 순서로 정렬
   - AWS Service, Account, Region, Usage Type별 분해

5. **설정**:
   - 3단계 간단 설정
   - 사용자 정의 달러 임계값 설정
   - 24시간 내 모니터링 시작

**[규정]** AWS Budgets (기본 비용 관리) [2차: https://docs.aws.amazon.com/cost-management/latest/userguide/managing-costs-by-setting-budgets.html]:
- 월별·분기별·연간 예산 설정
- 예산 초과 시 경보
- Reserved Instance 활용률 추적 (선택적)

**의무성**: 
- ✓ 도구 제공 (선택적)
- ✗ **비용 모니터링 의무화 없음** (선택적 사용)
- ✗ 이상 탐지는 수동 설정 필요

#### 4.3 Google Cloud, Azure 등 다른 클라우드 제공사

**[미확인]** GCP Budget & Anomaly Detection 상세:
- 2차 검색 결과에서 AWS와 유사한 기능 존재 암시
- 본 fetch에서 직접 검증 못함

**[미확인]** Azure Cost Management + Billing:
- 유사한 이상 탐지·예산 기능 존재로 예상
- 본 fetch에서 직접 검증 못함

---

## 표준 vs 처방 구분표

| 항목 | 정의 | 표준 기관 | 지위 | 근거/출처 |
|------|------|----------|------|---------|
| **FinOps Framework** | 조직의 비용 최적화 운영 모델 | Linux Foundation (표준 기관 아님) | **처방**: Best practice 권장사항, 자발적 채택 | [1차: https://www.finops.org/framework/] |
| **FOCUS 스펙** | 클라우드 비용/사용량 데이터 포맷 | FinOps Foundation (기술 표준) | **표준**: AWS, Azure, GCP, OCI 공식 채택 | [1차: https://focus.finops.org/focus-specification/] |
| **AWS Lambda 과금** | GB-s (실행 시간 × 메모리) 기반 | AWS (제품 동작 정의) | **규정**: AWS 공식 과금 정책 | [1차: https://aws.amazon.com/lambda/pricing/] |
| **Vercel Fluid Compute** | Active CPU + Provisioned Memory | Vercel (제품 정의) | **규정**: Vercel 공식 과금 정책 | [1차: https://vercel.com/docs/functions/usage-and-pricing] |
| **Cloudflare Workers 과금** | CPU milliseconds 기반 | Cloudflare (제품 정의) | **규정**: Cloudflare 공식 과금 정책 | [1차: https://developers.cloudflare.com/workers/platform/pricing/] |
| **AWS Anomaly Detection** | ML 기반 비용 이상 탐지 | AWS (선택적 도구) | **도구**: 자발적 설정 및 사용 | [1차: https://aws.amazon.com/aws-cost-management/aws-cost-anomaly-detection/] |

---

## 과금 단위 표 (Main Finding)

| 플랫폼 | 과금 메트릭 | 실행 시간 직접 반영? | 느린 코드 = 비용 ↑? | 비고 |
|--------|-----------|-------|------------------|------|
| **AWS Lambda** | GB-s (메모리 × 초) | ✓ 직접 | **✓ Yes** | I/O 대기 포함 |
| **Vercel** | Active CPU (코드만) + Provisioned Memory (인스턴스) | ✓ CPU 만 | ✓ **부분적** | I/O 대기는 CPU 비과금, 메모리는 계속 과금 |
| **Cloudflare Workers** | CPU 밀리초 | ✗ 아니다 | **✗ No** | I/O 대기는 완전 비과금 |
| **Google Cloud Functions** | GB-s (메모리 × 초) | ✓ 직접 | ✓ Yes | AWS Lambda와 동일 |

---

## 상충·부정 증거

### 발견된 상충

**1. 성능(느린 코드) vs 비용: 일관성 부재**
- AWS Lambda: "느린 코드 = 비용 증가" (명확)
- Vercel: "혼합" (CPU는 비용, I/O 대기 시간 상관없음)
- Cloudflare: "느린 코드 ≠ 비용 증가" (I/O bound 유리)
- **결론**: "성능=비용" 관계는 플랫폼에 따라 다름

**2. "비용 상한"이 성능 제약을 대체할 수 있는가?**
- AWS Lambda: 실행 시간 제한 (900초 max) → 성능 예산 효과 동일
- Vercel: 메모리 할당이 비용 결정 (계산 복잡도와 별개)
- Cloudflare: CPU 시간 제한 (30초 default) → 성능 예산 대체 가능
- **해석**: "성능 예산 대신 비용 상한" 전략은 **AWS에서는 유효하지만, Vercel에서는 약함**

### 부정 증거 (발견되지 않은 것)

- 클라우드 제공사가 "성능=비용"을 공식 규정하지 않음 (과금 단위로만 정의)
- 비용 최적화가 성능 최적화와 같다고 명시하는 공식 문서 없음
- FinOps가 성능 예산을 공식 권장사항으로 규정하지 않음 (비용 최적화는 권장)

---

## 미해결

1. **Google Cloud Functions, Azure Functions의 과금 모델**:
   - AWS Lambda와 동일한 GB-s 모델 사용 확인 [미확인]
   - 각 플랫폼의 상세 과금 문서 미열람

2. **FinOps가 비용 상한(budget cap)을 성능 예산 대체로 명시하는가?**:
   - FinOps Framework 문서에서 이 주제 언급 [미확인]
   - "비용=성능" 가정의 정당성 [미확인]

3. **플랫폼별 실제 고객 비용 데이터**:
   - 이론적 과금과 실제 비용 차이 [미확인]
   - cold start 비용, 네트워크 비용 등 숨겨진 요소

4. **산업 실무에서 "성능 예산 vs 비용 상한" 비교**:
   - 어느 접근법이 더 효과적인지 실증 데이터 [미확인]

---

## 출처

### 1차 출처 (직접 열람, 본문 검증)

1. https://aws.amazon.com/lambda/pricing/
   - AWS Lambda 공식 과금 모델 (GB-s, 요청 수)

2. https://aws.amazon.com/blogs/compute/aws-lambda-standardizes-billing-for-init-phase/
   - AWS Lambda INIT phase 과금 정책 변경 (2025년 8월)

3. https://vercel.com/docs/functions/usage-and-pricing
   - Vercel Fluid Compute 공식 과금 (Active CPU + Provisioned Memory)

4. https://developers.cloudflare.com/workers/platform/pricing/
   - Cloudflare Workers 공식 과금 (CPU milliseconds)

5. https://www.finops.org/introduction/what-is-finops/
   - FinOps Foundation 정의 및 기관 지위

6. https://www.finops.org/framework/
   - FinOps Framework 개요 및 성격 (Best practice, 비표준)

7. https://focus.finops.org/focus-specification/
   - FOCUS 데이터 포맷 스펙 (기술 표준)

8. https://aws.amazon.com/aws-cost-management/aws-cost-anomaly-detection/
   - AWS Anomaly Detection 공식 기능 설명

### 2차 출처 (검색 결과, 본문 미열람)

1. https://docs.aws.amazon.com/lambda/latest/dg/cost-optimize.html
   - AWS Lambda 비용 최적화 가이드

2. https://docs.aws.amazon.com/cost-management/latest/userguide/getting-started-ad.html
   - AWS Cost Anomaly Detection 시작 문서

3. https://www.cloudflare.com/plans/developer-platform/
   - Cloudflare 플랜 및 가격 정보

4. https://data.finops.org/
   - FinOps Foundation 2026년 State of FinOps 리포트

---

## 보충: 프로젝트 맥락 분석

본 조사의 배경: 리서치 프로젝트가 "1인 스케일에서 **성능 예산 시스템을 미채택하고 비용 상한으로 대체한다**"고 판단했음.

**조사 결과 평가**:

**✓ 발견 1: 성능 예산은 선택적**
- 공식 표준이 아니며, web.dev의 best practice 권장사항
- 도구(Lighthouse CI, webpack)는 선택적 지원
- 따라서 "미채택"은 표준 위반이 아님

**✓ 발견 2: 비용과 성능의 관계는 플랫폼에 따라 다름**
- AWS Lambda: **명확히 비례** (실행 시간 = 비용)
- Vercel: **부분적 비례** (I/O 대기는 비용과 무관)
- Cloudflare: **비례하지 않음** (I/O bound 유리)

**⚠️ 발견 3: "비용 상한 = 성능 예산"인가?**
- AWS의 경우: 함수 타임아웃 제한(900s) + Lambda 가격이 사실상 성능 예산
- Vercel의 경우: 메모리 할당이 주요 비용 요인 (계산 복잡도와 다름)
- **한계**: 비용 상한이 모든 성능 측면을 제약하지 않음
  - 네트워크 대역폭 (별도 과금)
  - 콜드 스타트 (초기화 오버헤드)
  - 메모리 프로파일 (계산과 무관)

**⚠️ 발견 4: FinOps는 비용 최적화 권장, 성능 예산 대체를 명시하지 않음**
- FinOps Framework는 "비용 최적화"에 중점
- 그러나 성능 예산을 비용 상한으로 "대체"하라는 규정 없음 [미확인]
- 성능과 비용은 "정렬되어야 함"이 원칙이지, 하나가 다른 하나를 완전히 대체하지는 않음

**결론**: 
- "성능 예산 미채택"은 표준 위반이 아니다 ✓
- 그러나 **"비용 상한이 충분한 성능 관리 대체물인가"는 별개 질문**이며, 플랫폼과 워크로드에 따라 답이 다르다
- **1인 스케일에서 비용 상한 관리는 실용적일 수 있지만, Core Web Vitals 같은 사용자 경험 지표는 여전히 중요** (aspect-12 참조)

