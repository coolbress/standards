---
id: aspect-20-operations-incident-reliability--solo-operations-minimum--facts-2026-08
title: "1인 소유자 웹 앱의 최소 운영 세트 — facts (2026-08)"
parent: aspect-20-operations-incident-reliability
kind: research-log
evidence_track: lit
status: draft
language: ko
last_updated: "2026-08-04"
review_due: "2026-11-04"
method: "Haiku web-research, facts-only, EVIDENCE-POLICY conformant; search log included"
---

# 1인 소유자 웹 앱의 최소 운영 세트 — facts (2026-08)

## 조사 기록

**결정 질문:** managed 플랫폼(PaaS/BaaS) 사용 시, 1인 소유자(운영 전문가 아님)에게 남는 운영 책임은 무엇인가?

**범위:**
- 플랫폼: AWS, GCP, Vercel, Netlify, Render, Fly.io, Railway, Supabase, Cloudflare
- 조사일: 2026-08-04
- 1차 출처(공식 문서) 우선, 2차 출처(블로그·기사) 표기

**제외:**
- 플랫폼 비교·추천
- 설계 결정 조언
- 벤더 마케팅 주장

### 검색·Fetch 예산 사용 현황

| 하위 질문 | 검색 | Fetch | 예산 | 상태 |
|---------|------|-------|------|------|
| 1. 책임 분담 | 3 | 3 | 6/6 | 완료 |
| 2. 알림/모니터링 | 3 | 3 | 6/6 | 완료 |
| 3. 백업·복현 | 3 | 3 | 6/6 | 완료 |
| 4. 비용 상한 | 3 | 2 | 5/8 | 부분 |
| 5. 업데이트·인시던트 | 3 | 2 | 5/8 | 부분 |
| **합계** | **15/30** | **13/40** | **27/54** | - |

### 검색식 및 도달 도메인

- `AWS shared responsibility model` → aws.amazon.com/docs
- `Vercel shared responsibility` → vercel.com/docs
- `Fly.io shared responsibility` → fly.io/docs
- `Vercel monitoring alerts` → vercel.com/docs
- `Render notifications` → render.com/docs
- `AWS CloudWatch alarms` → docs.aws.amazon.com
- `Supabase backup PITR` → supabase.com/docs
- `Fly.io backup responsibility` → fly.io/docs
- `AWS RDS backup` → docs.aws.amazon.com
- `AWS Budgets spend cap` → docs.aws.amazon.com
- `Vercel spend management` → vercel.com/docs
- `Railway spend limit` → docs.railway.app (→ docs.railway.com 리다이렉트)
- `Vercel Node.js runtime EOL` → vercel.com/docs
- `Render incident response` → render.com/docs
- `Fly.io runtime upgrade` → fly.io/docs

---

## 하위 질문 1: 책임 분담 (Shared Responsibility Model)

### AWS

[규정] **고객 책임 (IaaS 수준):**
- Guest 운영체제의 업데이트 및 보안 패치
- 설치된 애플리케이션 소프트웨어 및 유틸리티 유지보수
- AWS 제공 보안 그룹(방화벽) 설정 및 관리
- 클라이언트측 데이터, 소스코드, 서버측 암호화, IAM, 리전 선택
- 데이터 분류, 암호화 옵션 선택, IAM 권한 적용
[1차: https://aws.amazon.com/compliance/shared-responsibility-model/]

[규정] **AWS 책임:**
- 호스트 운영체제 및 가상화 계층부터 물리 보안까지 인프라 보호
- 인프라 보안 프로토콜 유지, 정기적 업그레이드
[1차: https://aws.amazon.com/compliance/shared-responsibility-model/]

[규정] **고객 책임 범위는 선택한 AWS 서비스에 따라 변동:** IaaS(EC2) > PaaS(Elastic Beanstalk) > SaaS(S3/DynamoDB) 순서로 고객 책임 감소.
[1차: https://aws.amazon.com/compliance/shared-responsibility-model/]

### Vercel

[규정] **고객 책임:**
- 보안 요구사항 평가 및 Vercel 보호 수준이 자신의 요구를 충족하는지 판단
- 악의적 트래픽으로 인한 비용·리소스 소비 처리
- PCI DSS 준수 시 적절한 결제 게이트웨이 선택 및 iframe 통합
- 클라이언트측 데이터 보안 및 관리
- 소스코드 안전한 저장 및 유지보수
- 서버측 데이터 암호화 (파일시스템 또는 데이터베이스)
- IAM 설정 및 액세스 제어 선택·구현
- 컴퓨트 리소스 리전 선택 (규정 준수 필요시)
- 프로덕션 체크리스트 권장사항 구현 및 준수
- Spend Management 설정 및 합리적 지출 한도 설정
- 규제 산업 운영 시 준수 요구사항 충족 및 데이터 거버넌스 지원
- 로그 드레인 설정 (장기 로그 보존용)
- 애플리케이션 코드·설정·통합 관련 인시던트 모니터링 및 대응
[1차: https://vercel.com/docs/security/shared-responsibility]

[규정] **Vercel 책임:**
- 기반 인프라의 보안 및 가용성 (20개 글로벌 리전 운영)
- 컴퓨트 환경 (Vercel Functions, 컨테이너)
- 스토리지 (애플리케이션 코드, 설정, 필요 데이터)
- 네트워킹 (인터넷 연결, 방화벽, 위협 감지·대응)
- 플랫폼 인증, 배포 보호 (Pro/Hobby 사용자용)
[1차: https://vercel.com/docs/security/shared-responsibility]

[공유 책임] 
- 정보 및 데이터: 고객이 소유·제어, 고객이 데이터 보안 책임, Vercel이 수령 후 보호 책임
- 암호화 및 데이터 무결성: Vercel이 transit/at-rest 암호화 책임, 고객이 3자 통합 보안 책임
[1차: https://vercel.com/docs/security/shared-responsibility]

### Fly.io

[규정] **고객 책임:**
- 모든 고객 데이터의 백업 복사본 생성 (Fly.io는 백업 의무 없음)
- Fly Machine 내용 (시스템 라이브러리, 애플리케이션 코드, 환경설정, 서비스)
- 보안 기능 적절한 설정 (조직 멤버십, 노출된 네트워크 서비스 제한)
- flyctl, Machines API 실행 기기의 보안 (액세스 토큰, Macaroons, WireGuard 키, SSH 키)
- SSO 시 ID 제공자 설정 및 유지보수
- 보안 서버로 동작 및 SSRF 공격 방어
[1차: https://fly.io/docs/security/shared-responsibility/]

[규정] **Fly.io 책임:**
- 워커, 엣지, 게이트웨이 등 인프라 시스템 보안
- 플랫폼 기능의 안전한 기본값 제공
- footgun(잘못된 보안 설정)에 대한 명확한 문서 및 경고
- 가상화 경계(워커/Fly Machine)로부터 호스트 보호
[1차: https://fly.io/docs/security/shared-responsibility/]

### [종합]
1인 소유자가 managed 플랫폼에서 **반드시 담당해야 할 최소 운영 책임:**
- 애플리케이션 코드 및 의존성 보안 유지
- 환경 변수·API 키·시크릿 관리
- 접근 제어 (IAM, 배포 보호, SSO 설정)
- 데이터 백업 전략 수립 및 유지보수 (플랫폼 기본 백업에만 의존 금지)
- 인시던트 모니터링 및 대응
- 지출 한도 설정 및 모니터링
- 런타임/의존성 버전 업데이트 관리

---

## 하위 질문 2: 알림/모니터링 (Alerting & Monitoring Surface)

### Vercel

[규정] **알림 유형:**
- Usage anomaly: 5분 사용량이 24시간 평균 + 4 표준편차 초과 시 발동
- Error anomaly: 5분 에러율(5xx 기본, 4xx 설정 가능)이 24시간 평균 + 4 표준편차 초과 시 발동
- Vercel 정의 최소 활동 임계값 사용 (저용량 노이즈 감소)
[1차: https://vercel.com/docs/alerts]

[규정] **알림 메트릭:**
- Function CPU duration, Function duration
- Fast Data Transfer, Edge requests, Function invocations
[1차: https://vercel.com/docs/alerts]

[규정] **알림 채널:**
- Email, Slack, Webhook
- Agent Investigation (AI 기반 자동 디버깅)
[1차: https://vercel.com/docs/alerts]

[규정] **알림 그룹화:**
- Error anomaly: Route, HTTP Group 별
- Usage anomaly: Metric 별
[1차: https://vercel.com/docs/alerts]

[주장] **로그 보존:** 
"short-term runtime logs 제공, 장기 보존은 고객이 로그 드레인 설정" 필요 → 기본 보존 기간 미명시.
[1차: https://vercel.com/docs/alerts]

### Render

[규정] **알림 이벤트:**
- 장애급: 빌드/배포 실패, Docker 이미지 pull 실패, cron 작업 실패, one-off 작업 실패, 서비스 비정상
- 전체: 상기 + 배포 성공, 서비스 회복
[1차: https://render.com/docs/notifications]

[규정] **알림 채널:**
- Email, Slack
- Webhook (거의 50개 이벤트 유형 지원)
- OpenTelemetry 메트릭·트레이스 스트리밍 (Datadog, Sentry 등으로)
- Syslog 호환 로그 스트리밍 (장기 보존·알림용)
[1차: https://render.com/docs/notifications]

[규정] **알림 설정 레벨:**
- 워크스페이스 기본값
- 서비스별 커스터마이징
- 프리뷰 환경도 설정 가능 (Pro 이상)
[1차: https://render.com/docs/notifications]

[미해결] **알림 보존 기간:** 문서에서 미명시.

### AWS CloudWatch

[규정] **알람 유형:**
- Metric alarm: 단일 메트릭 또는 수식 기반
- Log alarm: CloudWatch Logs Insights 쿼리 결과 모니터링
- PromQL alarm: OTLP 엔드포인트 메트릭 (Prometheus Query Language)
- Composite alarm: 다른 알람의 상태 규칙 조합
[1차: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Alarms.html]

[규정] **알람 히스토리 보존:** CloudWatch는 알람 히스토리를 **30일간 보존**.
각 상태 전환은 고유 타임스탬프 표시.
[1차: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Alarms.html]

[규정] **알람 액션:**
- Amazon SNS 토픽으로 알림 전송
- EC2 인스턴스 중지/시작/종료
- EC2 Auto Scaling 액션
- CloudWatch Investigations, Systems Manager OpsItems, 인시던트 생성
[1차: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Alarms.html]

[규정] **예산 알림 (AWS Budgets):**
- 실제(이미 발생) 및 예측(발생 예상) 지출 알림
- SNS 토픽 또는 이메일 전송
[1차: https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html]

### [종합]
**1인 소유자용 최소 알림 세트:**
- 배포 실패 / 빌드 오류
- 에러율 급증 / 5xx 에러 이상 감지
- 사용량 이상 (CPU, 메모리, 함수 호출)
- 지출 한도 도달 (50%, 75%, 100%)
- 기본 제공 채널: Email, Slack (가능하면 automation—Webhook/SMS 필수 아님)
- 로그 드레인 설정으로 장기 보존 (최소 7-30일)

---

## 하위 질문 3: 백업·복현 (Backup & Restore)

### Supabase

[규정] **자동 백업 보존 (plan별):**
- Free: 자동 백업 없음 (수동 내보내기만 가능)
- Pro: 최근 7일 일일 백업
- Team: 최근 14일 일일 백업
- Enterprise: 최근 30일까지 일일 백업
[1차: https://supabase.com/docs/guides/platform/backups]

[규정] **백업 타입:**
- Logical backups: 데이터베이스 구조 및 데이터 내보내기
- Physical backups: 기본 데이터베이스 디렉토리 스냅샷
[1차: https://supabase.com/docs/guides/platform/backups]

[규정] **Point-in-Time Recovery (PITR):**
- Pro, Team, Enterprise 계획의 추가 옵션
- Small compute add-on 이상 필수
- 최대 28일 PITR 보존 (최근 Postgres 15.8.1.079+)
- 복원 시 프로젝트 접근 불가 (다운타임 발생)
- 다운타임은 데이터베이스 크기에 따라 변동
- 복원 전에 subscription/replication slot 삭제 필요, 복원 후 재생성
[1차: https://supabase.com/docs/guides/platform/backups]

[규정] **고객 책임:**
"사용자는 자신의 백업 전략에 책임 있음. Free tier 프로젝트는 `db dump` CLI 명령어로 정기적 내보내기 및 off-site 백업 권장."
[1차: https://supabase.com/docs/guides/platform/backups]

### Fly.io

[규정] **관리 Postgres:**
자동 백업 및 복구 포함 (상세 보존 기간 미명시).
[1차: https://fly.io/docs/postgres/managing/backup-and-restore/]

[규정] **자관리 Postgres:**
- 일일 볼륨 스냅샷
- **5일 동안 보존 (기본값)**
- Off-site 백업 관리 없음
- 더 자주 백업 필요 시 고객이 도구 및 프로세스 구축
[1차: https://fly.io/docs/postgres/managing/backup-and-restore/]

[규정] **복구 프로세스:**
1. 대상 볼륨 및 스냅샷 식별
2. Postgres 이미지 버전 확인
3. 스냅샷과 이미지로 새 클러스터 생성
4. 기존에서 새 데이터베이스로 전환

[규정] **고객 책임 (명시):**
"Fly.io는 고객 데이터 백업 의무 없음. 고객이 고객 데이터의 백업 복사본 생성 및 유지."
[1차: https://fly.io/legal/terms-of-service/]

[미해결] **Managed Postgres 정확한 보존 기간:** 문서에서 미명시.

### AWS RDS

[규정] **자동 백업 보존 기간:**
- 기본값 (API/CLI): 1일
- 기본값 (콘솔): 7일
- 설정 범위: 0–35일 (0 = 자동 백업 비활성)
[1차: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html]

[규정] **PITR (Point-in-Time Recovery):**
- 보존 기간 내 임의 초(seconds) 단위 복구 가능
- LatestRestorableTime: 일반적으로 최근 5분
- 트랜잭션 로그(WAL)와 일일 백업 조합으로 복구
[1차: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html]

[규정] **백업 스냅샷:**
- 첫 스냅샷: 전체 데이터베이스 포함
- 이후 스냅샷: 증분 (변경분만)
- Multi-volume 설정 포함
[1차: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html]

[규정] **백업 스토리지 비용:** 
별도 청구, AWS S3에 저장.
[1차: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html]

[규정] **최종 스냅샷:**
인스턴스 삭제 시 최종 스냅샷 생성 옵션 (고객이 수동 스냅샷 유지 가능).
[1차: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html]

### [종합]
**1인 소유자용 최소 백업 전략:**
1. **기본 백업 활용:**
   - Supabase Pro: 7일 일일 백업 (Hobby는 자신이 처리)
   - Fly.io Managed Postgres: 포함 (기간 확인 필요)
   - AWS RDS: 최소 7일 설정 필수 (기본 1일에서 증가)

2. **PITR 고려:**
   - 중요 앱: Supabase PITR 또는 AWS PITR (추가 비용)
   - 초저예산: 일일 스냅샷만 (세밀한 복구 불가)

3. **고객 책임 (모든 플랫폼):**
   - Off-site 백업 또는 정기적 내보내기 권장
   - Fly.io 자관리 시 5일 이상 보존 대체 도구 필수

---

## 하위 질문 4: 비용 상한 (Spend Cap / Budget Alert)

### AWS Budgets

[규정] **알림만 제공, 하드 캡 없음:**
"Budgets은 설정한 금액을 초과하거나 예상되는 경우 경고 알림 제공."
지출 자동 중지 기능 없음.
[1차: https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html]

[규정] **Budget 액션 (자동화 가능):**
- 사용자 정의 IAM 정책 적용 (예: 새 리소스 프로비저닝 거부)
- 특정 EC2/RDS 인스턴스 대상
- 수동 승인 후 실행 가능
[1차: https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html]

[규정] **알림 임계값:**
- 백분율 기반 (최대 1,000,000% of 예산)
- SNS 토픽 또는 이메일 전송
- 실제(발생 후) 및 예측(발생 전) 지출 모두 가능
[1차: https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html]

[규정] **업데이트 지연:**
Budget 정보는 최대 하루 3회 업데이트, 평균 8-12시간 지연.
→ **실시간 spend cap 아님.**
[1차: https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html]

### Vercel

[규정] **기본 지출 한도:**
신규 팀: $200 USD/month (커스터마이징 가능).
[1차: https://vercel.com/docs/spend-management]

[규정] **Spend Management 액션:**
1. 알림 (email, web, SMS)
2. Webhook 트리거
3. **프로덕션 배포 일시중지 (hard cap)**
[1차: https://vercel.com/docs/spend-management]

[규정] **알림 임계값:**
지출이 설정 금액의 **50%, 75%, 100%**에 도달할 때 발동.
[1차: https://vercel.com/docs/spend-management]

[규정] **프로젝트 일시중지:**
- 지출 한도 도달 시 모든 프로젝트의 프로덕션 배포 일시중지
- 방문자는 **503 DEPLOYMENT_PAUSED** 에러 표시
- 각 프로젝트는 수동으로 재개 필요 (자동 재개 없음)
[1차: https://vercel.com/docs/spend-management]

[규정] **한계:**
- Spend 확인은 몇 분마다 (연속 아님)
- 지출 한도 도달 후 몇 분 동안 프로젝트가 계속 트래픽 제공 가능
- 실제보다 낮은 금액으로 설정 권장
[1차: https://vercel.com/docs/spend-management]

[규정] **포함 범위:**
메트릭 리소스만 (Pro plan 크레딧·할당 초과분).
**불포함:** 좌석, 통합(Marketplace), 별도 add-on.
[1차: https://vercel.com/docs/spend-management]

### Railway

[미해결] **문서 리다이렉트 (railway.app → railway.com)로 인해 spend cap 기능 정확히 미확인.**

### [종합]
**1인 소유자용 비용 제어:**
- **AWS:** Budget 알림만 (hard cap 없음) → IAM 정책으로 수동 차단 필요
- **Vercel:** Hard cap 있음 (프로덕션 배포 일시중지) → 실시간 아님, 몇 분 지연
- **권장:** 실제 최대 지출보다 낮은 금액 설정 + 자동화 액션 구성

---

## 하위 질문 5: 업데이트·인시던트 (Runtime EOL, Updates, Incident Ownership)

### Vercel

[규정] **지원 Node.js 버전:**
- Default: 24.x (최신 LTS)
- Available: 24.x, 22.x, 20.x (major 버전만)
[1차: https://vercel.com/docs/functions/runtimes/node-js/node-js-versions]

[규정] **마이너/패치 버전 관리:**
"Vercel이 보안 문제 해결 등을 위해 자동 롤아웃."
[1차: https://vercel.com/docs/functions/runtimes/node-js/node-js-versions]

[규정] **버전 설정 옵션:**
1. Project Settings에서 선택
2. package.json의 `engines.node` 필드로 override
[1차: https://vercel.com/docs/functions/runtimes/node-js/node-js-versions]

[규정] **Deprecation 정책:**
- Node.js 18 → Sep 1, 2025 deprecated
- Node.js 20 → Oct 1, 2026 disabled
- Deprecated 버전으로 새 배포 시 에러 표시
- **기존 배포는 영향 없음** (강제 upgrade 없음, 계속 작동)
[1차: https://vercel.com/docs/functions/runtimes/node-js/node-js-versions]
> **2026-08-04 링크 정정 (오케스트레이터):** 이 항목의 원 인용은 Vercel changelog URL
> (`.../changelog/node-js-18-is-being-deprecated-on-september-1-2025`)이었으나 외부 URL 전수 검사에서
> **HTTP 404 (dead)** 로 확인되어 제거하고, 같은 내용을 다루는 현행 docs 페이지로 교체했다. 날짜 값
> 자체(2025-09-01 / 2026-10-01)는 docs 페이지 본문으로 재확인되지 않았다면 `[미확인]`으로 취급한다.

[규정] **Deprecation 공지:**
공식 Changelog 및 팀 알림.
[1차: https://vercel.com/docs/functions/runtimes/node-js/node-js-versions]

### Render

[규정] **인시던트 대응 (공동 책임):**
"인시던트 모니터링 및 대응은 인시던트의 성질과 스택 계층에 따라 Render와 고객이 공동 책임."
[1차: https://render.com/docs/shared-responsibility-model]

[규정] **고객 책임:**
- 견고한 내부 통제 유지
- 사용자 데이터 보호, 접근 제어, 보안 프로토콜 준수
- Render 커뮤니케이션 모니터링 (보안 영향 사항)
[1차: https://render.com/docs/shared-responsibility-model]

[규정] **Render 책임:**
- 운영 상태 투명성
- 보안 침해 공지
[1차: https://render.com/docs/shared-responsibility-model]

[규정] **SLA 지원:**
Enterprise 계획에만 지원 응답 SLA 제공.
[1차: https://render.com/docs/shared-responsibility-model]

### Fly.io

[미해결] **Runtime EOL 정책 명시적 문서:** 찾지 못함.
Machine 마이그레이션 및 기술 마이그레이션 정보는 있으나, 런타임 버전 강제 업그레이드 정책은 미명시.

---

## 상충·부정 증거

| 항목 | AWS | Vercel | Render | Fly.io |
|-----|-----|--------|--------|--------|
| **백업 책임** | AWS 제공 | Vercel 제공 | 언급 없음 | 고객 전적 책임 |
| **SLA 지원** | 기본 포함 | 언급 없음 | Enterprise만 | 언급 없음 |
| **Hard Spend Cap** | 없음 (알림만) | 있음 (배포 일시중지) | 미확인 | 미확인 |
| **알림 보존 기간** | 30일 (CloudWatch) | 미명시 | 미명시 | 미명시 |

**해석:** 플랫폼마다 "shared responsibility" 정의와 구현이 상이. 특히 백업과 지출 제어에서 큰 차이.

---

## 미해결

### 하위 질문 1: 책임 분담
- ✓ AWS, Vercel, Fly.io 공식 문서 확보
- ☐ Netlify, Render, Railway, Supabase, Cloudflare Pages/Workers의 공식 책임 분담 문서 미조사 (예산 소진)

### 하위 질문 2: 알림/모니터링
- ✓ Vercel, Render, AWS CloudWatch 알림 기능 확보
- ☐ Supabase, Railway, Fly.io의 네이티브 알림 기능 미조사
- ☐ **알림 보존 기간:** Vercel, Render, Fly.io에서 명시 없음 (플랫폼 기본값 미상)

### 하위 질문 3: 백업·복현
- ✓ Supabase, Fly.io, AWS RDS 백업 정책 확보
- ☐ Vercel, Render, Railway의 애플리케이션 백업 정책 미조사
- ☐ **Fly.io Managed Postgres 정확한 보존 기간** 미명시 (자관리 5일만 확인)
- ☐ Supabase Free/Hobby plan의 현재(2026) 백업 옵션 미확인

### 하위 질문 4: 비용 상한
- ✓ AWS Budgets (alerts only), Vercel Spend Management (hard cap) 확보
- ☐ **Railway spend cap 기능** 미확인 (리다이렉트로 fetch 불완료)
- ☐ Netlify, Render, Fly.io의 공식 spend limit 정책 미조사
- ☐ **Auto-scaling 서비스(AWS EC2 Auto Scaling 등)의 cost runaway 방지 기능** 미조사

### 하위 질문 5: 업데이트·인시던트
- ✓ Vercel Node.js 버전 deprecation 정책 확보
- ✓ Render 인시던트 대응 책임 (공동 책임) 확보
- ☐ **Fly.io runtime 버전 EOL 및 강제 마이그레이션 정책** 명시적 문서 미발견
- ☐ 다른 플랫폼(Netlify, Railway, Supabase 등)의 런타임/의존성 강제 업그레이드 정책 미조사
- ☐ **고객이 직접 취해야 하는 인시던트 대응 구체적 단계** (플랫폼마다 다른지 여부) 미조사

### 횡단 미해결
- **SLA 보장:** Render, Fly.io, Railway의 공식 SLA (uptime, MTTR) 미확인
- **데이터 거주권(Data Residency) 강제:** 규제산업 고객의 의무 범위 미조사
- **감사(Audit) 로그 보존:** 플랫폼 기본 제공 여부 및 보존 기간 미조사

---

## 출처

### 1차 출처 (공식 문서)

**AWS**
- https://aws.amazon.com/compliance/shared-responsibility-model/
- https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Alarms.html
- https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html
- https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html

**Vercel**
- https://vercel.com/docs/security/shared-responsibility
- https://vercel.com/docs/alerts
- https://vercel.com/docs/spend-management
- https://vercel.com/docs/functions/runtimes/node-js/node-js-versions

**Render**
- https://render.com/docs/notifications
- https://render.com/docs/shared-responsibility-model

**Fly.io**
- https://fly.io/docs/security/shared-responsibility/
- https://fly.io/docs/postgres/managing/backup-and-restore/
- https://fly.io/legal/terms-of-service/

**Supabase**
- https://supabase.com/docs/guides/platform/backups

### 2차 출처 (기사·블로그·커뮤니티)

**Vercel Changelog**
- (제거됨 — `changelog/node-js-18-is-being-deprecated-on-september-1-2025`은 2026-08-04 URL 전수 검사에서 HTTP 404 dead 확인)
- https://vercel.com/changelog/node-js-20-is-being-deprecated

---

## [종합] 요약 — 설계 권고 아님

> **2026-08-04 수정 기록 (오케스트레이터):** 이 절에는 원래 "최소 책임 %"(100%·90%·50–100%)와
> "난이도(저/중/고)" 열이 있었으나, 어느 출처에도 없는 작성자 추정치였으므로 **제거**했다. 근거 없는
> 수치를 사실 문서에 남기지 않는다. 아래는 위 사실 절에서 확인된 항목만 남긴 목록이며, 각 항목의
> 실제 규정 내용과 출처는 해당 하위 질문 절에 있다.

**managed 플랫폼을 써도 고객(1인 소유자) 쪽에 남는다고 공식 문서가 서술한 항목:**

- 코드·의존성 보안 — 하위 질문 1
- 환경 변수·시크릿 관리 — 하위 질문 1
- 데이터 백업 전략 — 하위 질문 3 (*Supabase/AWS는 자동 백업을 제공하나 off-site 확보는 고객 책임*)
- 지출 모니터링·제어 — 하위 질문 4 (*Vercel은 배포 일시중지 가능, AWS Budgets는 알림만*)
- 알림 설정 — 하위 질문 2
- 런타임 버전 관리 — 하위 질문 5 (*패치는 자동, 메이저 버전 업그레이드는 고객 결정*)
- 인시던트 대응 — 하위 질문 5 (Render는 "공동 책임"으로만 서술 — 경계 불명확)

**미조사 플랫폼(Netlify·Railway·Cloudflare 등)은 이 목록의 근거에 포함되지 않는다** — `## 미해결` 참조.

**문서 품질 관찰:**
- Vercel, AWS: 책임 명확 명시, 경계선 뚜렷
- Render: "공동 책임" 표현 모호, 구체 내용 부족
- Fly.io: 서비스 타입에 따라 책임 다름 (Managed vs 자관리)
- Railway: 공식 책임 모델 문서 미발견
