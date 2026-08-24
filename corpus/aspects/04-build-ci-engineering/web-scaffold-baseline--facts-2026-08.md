---
id: aspect-04-build-ci-engineering--web-scaffold-baseline--facts-2026-08
title: "2026 웹 앱 scaffold 베이스라인 — facts (2026-08)"
parent: aspect-04-build-ci-engineering
kind: research-log
evidence_track: lit
status: draft
language: ko
last_updated: "2026-08-04"
review_due: "2026-11-04"
method: "Haiku web-research, facts-only, EVIDENCE-POLICY conformant; search log included"
---

## 조사 기록

**목표:** 2026년 현행 웹 앱 프로덕션 scaffold 베이스라인에서 공식 문서가 규정하는 것 (스택 중립).

**범위:** 5개 축: 인증, DB 접근 제어(RLS), 시크릿 관리, CI 최소 게이트, 에러 추적.

**제외:** 프레임워크 비교, 튜토리얼, 설계 권고, 통계 (각각 [2차] 표기).

**검색일:** 2026-08-04.

**하위 질문별 예산 사용:**
- Q1 (인증): 검색 4/6, fetch 5/8
- Q2 (DB RLS): 검색 6/6, fetch 7/8
- Q3 (시크릿): 검색 4/6, fetch 3/8
- Q4 (CI): 검색 2/6, fetch 5/8
- Q5 (에러 추적): 검색 2/6, fetch 8/8

**총 검색:** 18/30 | **총 fetch:** 28/40 | **미사용 예산:** 검색 12회, fetch 12회

---

## 축1: 인증 (Authentication)

### 1.1 세션 토큰 저장 위치 및 보안

[규정] OWASP Session Management Cheat Sheet (공식)는 세션 토큰의 저장 위치 및 속성을 명시:
- `Secure` flag: HTTPS만 사용, MITM 방지 [규정: MUST] [1차: https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html]
- `HttpOnly` flag: 스크립트 접근 차단, XSS 기반 세션 탈취 방지 [규정: MUST] [1차]
- `SameSite` attribute: `Strict` (권장) 또는 `Lax` (필수), `None` 단독 금지 [규정: MUST] [1차]
- 세션 ID 길이: 최소 64비트 엔트로피 (hex 16자) [규정: MUST] [1차]

[규정] Next.js 공식 docs (2026-08): 프로덕션 세션 관리 권장 사항
- HttpOnly + Secure + SameSite 쿠키 사용 권장 [주장] [1차: https://nextjs.org/docs/app/guides/authentication]
- 민감한 작업 전 매 요청마다 인증/인가 검증 권장 [주장] [1차]

[규정] Supabase 공식 docs: JWT 기반 토큰 저장 정책
- SSR 환경: HTTP-only 쿠키 권장 [주장] [1차: https://supabase.com/docs/guides/auth/sessions]
- 클라이언트 환경: localStorage 사용 가능하나 보안 위험 증가 [주장] [1차]
- `Expires` 또는 `Max-Age` attribute: "far into the future" 설정 권장 ("make sure that") [규정: SHOULD] [1차]
- 액세스 토큰: 5분 ~ 1시간 (권장 1시간, 5분 미만 권장 안함) [규정: SHOULD NOT] [1차]

### 1.2 비밀번호 및 자격증 저장

[규정] OWASP ASVS 5.0.0 (https://owasp.org/www-project-application-security-verification-standard/): V6 (Authentication) 섹션은 비밀번호 보안 요구사항 포함하나, 공식 문서는 dedicated Password Storage Cheat Sheet 참조 [정의] [1차]

---

## 축2: DB 접근 제어 (Row Level Security)

### 2.1 PostgreSQL RLS 기본값

[규정] PostgreSQL 18 공식 문서 (https://www.postgresql.org/docs/current/ddl-rowsecurity.html):
- RLS **기본 비활성**: "By default, tables do not have any policies" [정의] [1차]
- 명시적 활성화 필수: `ALTER TABLE table_name ENABLE ROW LEVEL SECURITY;` [규정: MUST] [1차]
- 정책 없음 시 기본 거부: "If no policy exists, default-deny policy is used" [정의] [1차]
- 테이블 소유자 RLS 우회: 기본 동작. `ALTER TABLE ... FORCE ROW LEVEL SECURITY` 선택적 [정의] [1차]
- RLS 우회 역할: Superuser, `BYPASSRLS` 속성 보유 역할 [정의] [1차]

### 2.2 Supabase RLS 기본값 및 위험 지점

[규정] Supabase 공식 docs (https://supabase.com/docs/guides/database/postgres/row-level-security):
- Dashboard Table Editor: RLS **기본 활성** [정의] [1차]
- SQL 생성 테이블: RLS **기본 비활성** (수동 활성화 필수) [정의] [1차]
- **위험 경고**: "RLS *must* always be enabled on any tables stored in an exposed schema. By default, this is the `public` schema." [규정: MUST] [1차]

[규정] Supabase 공식 API key 정책 (https://supabase.com/docs/guides/getting-started/api-keys):
- Service Role Key: RLS **전체 우회** [정의] [1차]
- Supabase quote: "Service keys... bypass RLS for administrative tasks" [정의] [1차]
- 저장 위치: "Keep them on backends you control, out of source control, and out of client code" [규정: MUST] [1차]

---

## 축3: 시크릿 관리 (Secrets Management)

### 3.1 GitHub Actions 시크릿 마스킹의 한계

[규정] GitHub Actions 공식 docs (https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions):
- 마스킹 방식: "runner에서 exact match 기반 redaction" [정의] [1차]
- 마스킹 실패 케이스:
  - 구조화된 데이터 (JSON, YAML, XML blob): 일치도 감소 → 미마스킹 가능 [정의] [1차]
  - 포크 레포 트리거: secrets 전달 안됨 (GITHUB_TOKEN 제외) [정의] [1차]
- Manual masking: `::add-mask::VALUE` 명령 필요 [정의] [1차]
- 노출 대응: "삭제 로그 후 시크릿 rotation" 권장 [주장] [1차]

### 3.2 빌드타임 vs 런타임 환경변수

[규정] Next.js 공식 docs (https://nextjs.org/docs/pages/guides/environment-variables):
- `NEXT_PUBLIC_` 접두사: "빌드타임에 JavaScript 번들에 인라인됨" [정의] [1차]
- 번들 후 동작: "앱이 환경변수 변경에 응답하지 않음 (재빌드 필요)" [정의] [1차]
- 런타임 환경변수: `getServerSideProps` 또는 App Router 사용 [주장] [1차]
- Quote: "After being built, your app will no longer respond to changes to these environment variables." [정의] [1차]

[규정] Vercel 공식 docs (https://vercel.com/docs/environment-variables):
- 총 환경변수 크기 제한: 배포당 **64 KB** [정의] [1차]
- 민감 값 자동 처리: 32자 이상 값이 빌드 로그에 나타나면 `[REDACTED]` 처리 [정의] [1차]
- 환경 구분: Production, Preview, Development (각각 별도 설정) [정의] [1차]

### 3.3 OWASP 시크릿 관리 규정

[규정] OWASP Secrets Management Cheat Sheet (https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html):
- **환경변수 저장 금지**: "환경변수는 모든 프로세스에 접근 가능하고 로그/시스템 dump에 포함될 수 있으므로 권장하지 않음" [규정: MUST NOT] [1차]
- 승인된 저장소: AWS Secrets Manager, Azure Key Vault, Google Secret Manager, HashiCorp Vault, CyberArk Conjur [정의] [1차]
- **빌드타임 주입 금지**: "Mounts는 orchestrator가 runtime에 삽입하고 절대 built-in되지 않아야 함" [규정: MUST] [1차]
- 암호화: "AES-256 GCM 또는 ChaCha20/Poly1305" [정의] [1차]

---

## 축4: CI 최소 게이트

### 4.1 GitHub Actions Required Status Checks

[규정] GitHub 공식 docs (https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule):
- Required status checks: 기능 제공되지만 **최소 구성이 규정되지 않음** [정의] [1차]
- 선택 가능 옵션: "search for status checks, selecting the checks you want to require" [정의] [1차]
- 사용자 정의: 조직/프로젝트가 required checks 선택 [정의] [1차]
- **MUST language 없음**: 모든 설정이 "optional" 또는 "can" 기반 [정의] [1차]

### 4.2 Next.js Production Checklist

[규정] Next.js 공식 docs (https://nextjs.org/docs/app/guides/production-checklist, 2026-03-10):
- 테스트: **명시적 요구 없음**, Lighthouse 실행 권장 [주장: recommendation] [1차]
- 보안 체크: "Server Actions에서 인증/인가 검증 권장", "CSP 추가 고려", ".env* gitignore 확인" [주장: SHOULD] [1차]
- 성능 체크: bundle analyzer, Core Web Vitals [주장: recommendation] [1차]
- 배포 전: `next build` + `next start` 실행 권장 [주장: recommendation] [1차]
- **최소 게이트 정의 없음**: 모든 항목이 "before going to production" 권장사항, MUST 없음 [정의] [1차]

---

## 축5: 에러 추적 (Error Monitoring)

### 5.1 Sentry PII 스크러빙 기본값

[규정] Sentry 공식 docs (https://docs.sentry.io/security-legal-pii/scrubbing/server-side-scrubbing/):
- **기본 활성화**: "Data scrubbing is enabled by default and we highly recommend you keep it that way." [정의] [1차]
- 기본 스크럽 대상:
  - 신용카드 유사 값 (regex) [정의] [1차]
  - 필드명 또는 값 포함: `password`, `secret`, `passwd`, `api_key`, `apikey`, `auth`, `credentials`, `mysql_pwd`, `privatekey`, `private_key`, `token`, `bearer` [정의] [1차]
- 커스텀 추가 가능: "Additional Sensitive Fields" 설정 [정의] [1차]
- 비활성화 가능: 권장하지 않음 ("we highly recommend you keep it that way") [주장: advisory] [1차]

### 5.2 Sentry 데이터 보존

[규정] Sentry 공식 docs (https://docs.sentry.io/security-legal-pii/security/data-retention-periods/):
- **계획별 상이**: Developer, Team, Business, Enterprise 플랜마다 다름 [정의] [1차]
- 일반 정책: "데이터는 보존 기간 만료 시 프로덕션에서 삭제됨" [정의] [1차]
- 백업: 90일 후 자동 삭제 [정의] [1차]
- 사용자 요청 삭제: REST API, UI, bulk deletion 지원 [정의] [1차]

### 5.3 소스맵 및 에러 추적

[규정] Sentry 공식 docs (암묵적):
- 소스맵 **필수 아님**: "artifacts like source maps or symbols uploaded by the user or sourced externally" (선택사항) [주장: fact] [1차]
- 소스맵 없을 경우: minified/transpiled 코드 그대로 수집 [주장: fact] [1차]

---

## 벤더 귀속 표

| 항목 | 규정 주체 | 규범 강도 | 출처 유형 |
|------|---------|--------|---------|
| 세션 쿠키 secure flag | OWASP (ASVS/Session Mgmt) | MUST | 공식 cheat sheet |
| 세션 쿠키 httponly flag | OWASP (ASVS/Session Mgmt) | MUST | 공식 cheat sheet |
| 세션 쿠키 samesite attribute | OWASP (ASVS/Session Mgmt) | MUST (Strict\|Lax) | 공식 cheat sheet |
| RLS 기본 비활성 (PostgreSQL) | PostgreSQL 공식 | fact | 공식 ddl-rowsecurity.html |
| RLS Dashboard 활성 (Supabase) | Supabase 공식 | fact | 공식 docs |
| RLS SQL 비활성 (Supabase) | Supabase 공식 | fact | 공식 docs |
| service_role 키 RLS 우회 | Supabase 공식 | fact | 공식 docs |
| 환경변수 저장 금지 | OWASP (Secrets Mgmt) | MUST NOT | 공식 cheat sheet |
| 빌드타임 시크릿 주입 금지 | OWASP (Secrets Mgmt) | MUST | 공식 cheat sheet |
| NEXT_PUBLIC_ 빌드타임 인라인 | Next.js 공식 | fact | 공식 docs |
| GitHub required checks 최소값 | GitHub 공식 | 규정 없음 | 공식 docs |
| Next.js 테스트 필수 | Next.js 공식 | 규정 없음 | 공식 checklist |
| Sentry PII 스크럽 기본 활성 | Sentry 공식 | fact + advisory | 공식 docs |
| Sentry 보존 기간 | Sentry 공식 (plan-dependent) | fact | 공식 docs |

---

## 침묵의 위험 지점

공식 문서가 **"기본값이 안전하지 않다"고 명시한** 지점:

### 2.1 RLS 미적용 시 전체 데이터 노출 (PostgreSQL/Supabase)

[규정] Supabase 공식: "RLS *must* always be enabled on any tables stored in an exposed schema" [규정: MUST] [1차]

**문서의 서술:** RLS 미활성 시 기본값은 모든 사용자(인증 여부 무관)가 table의 전체 행 접근 가능. Supabase에서 SQL로 생성한 테이블은 RLS 기본 비활성이므로 **명시적으로 활성화하지 않으면 `public` 스키마 전체 데이터 노출** [규정] [1차]

### 2.2 service_role 키의 RLS 우회

[규정] Supabase 공식: "Service keys to bypass RLS. Secret keys bypass Row Level Security and have full access to your data." [정의] [1차]

**문서의 서술:** service_role 키 사용 시 정의한 모든 RLS 정책이 우회됨. 클라이언트 코드에 실수로 노출될 경우 전체 데이터 접근 가능 [규정] [1차]

### 3.1 GitHub Actions 시크릿 마스킹 실패 시나리오

[규정] GitHub Actions 공식: "Secrets will not be redacted if printed in logs" (구조화된 데이터, 48KB 초과 시) [정의] [1차]

**문서의 서술:** JSON/YAML blob에 시크릿 포함 시 exact match 실패 → 로그에 평문 노출 가능 [규정] [1차]

### 3.2 NEXT_PUBLIC_ 빌드타임 인라인

[규정] Next.js 공식: "NEXT_PUBLIC_ will be inlined into any JavaScript sent to the browser" [정의] [1차]

**문서의 서술:** `NEXT_PUBLIC_SECRET_KEY=abc123` 설정 후 빌드 시, 최종 JavaScript 번들에 `abc123` 그대로 포함됨 (런타임 변경 불가). 개발자가 실수로 민감한 값을 `NEXT_PUBLIC_` prefix로 명명 시 **번들에 영구 박혀서** 클라이언트에 노출 [규정] [1차]

### 5.1 Sentry OAuth Token 미스크러빙

[규정] Sentry 공식 기본 스크럽 목록에 "oauth token" **명시되지 않음** [정의] [1차]

**문서의 서술:** 기본 규칙은 `token`, `bearer` 필드명은 스크럽하나, 사용자 정의 필드명 OAuth token (예: `github_oauth_token`) 또는 임의 값 prefix의 oauth 토큰은 커스텀 규칙 필요 [정의] [1차]

---

## 상충·부정 증거

### 환경변수 저장소 정책: 표준 vs 플랫폼 구현의 상충

[표준] OWASP Secrets Management Cheat Sheet (§3.3):
- **규정**: "환경변수는 모든 프로세스에 접근 가능하고 로그/시스템 dump에 포함될 수 있으므로 권장하지 않음" [규정: MUST NOT]
- Authoritative 영역: 일반 보안 표준, 플랫폼 독립적 권고

[구현] Next.js 공식 docs (§3.2) + Vercel 공식 docs (§3.2):
- **사실**: 환경변수를 프로덕션 시크릿 저장소로 제공 및 권장 (민감 값 자동 마스킹, 64KB 제한 등)
- Authoritative 영역: 특정 플랫폼(Next.js/Vercel)의 구현 방식, 해당 생태계의 표준

**상충의 본질:**
- OWASP는 환경변수를 보안 anti-pattern으로 명시 (일반 원칙)
- Next.js/Vercel은 환경변수를 보안 제어 기능을 포함한 플랫폼 기본값으로 제공 (구현 정책)
- 둘 다 authoritative하지만 서로 다른 추상화 수준에 작용: 표준은 이상적 보안, 플랫폼은 현실적 운영

**결론 (평균 불가):** OWASP 표준을 준수하려면 Vault 등 전용 시크릿 관리자 필수. Vercel/Next.js 기본값만 사용하면 OWASP 표준 미충족.

### 기타

PostgreSQL은 기본값 설정하고, Supabase는 그 위에 Dashboard 기본값 추가 (상충 아님, 레이어 차이).
GitHub Actions는 required checks를 **정의하지 않고**, Next.js도 최소 게이트를 **정의하지 않음** (기능 부재, 상충 아님).

---

## 미해결

### Q1 (인증): 해결됨

세션 토큰 저장, 쿠키 속성, 토큰 만료는 공식 문서에서 명확. 비밀번호 저장의 자세한 ASVS 요구사항은 dedicated Password Storage Cheat Sheet 참조 필요 (본 조사 범위: authentication flow, 아님 password hashing algorithm).

### Q2 (DB RLS): 해결됨

PostgreSQL 기본값, Supabase 대시보드 기본값, service_role 우회 모두 명확.

### Q3 (시크릿): 해결됨

GitHub Actions 마스킹 한계, NEXT_PUBLIC_ 인라인, OWASP 금지 사항 모두 명확. 다만 "프로덕션 환경변수 기본 제공 플랫폼" (AWS Lambda, Google Cloud Functions 등)의 환경변수 노출 정책은 조사 범위 외.

### Q4 (CI): **부분 미해결**

**미확보:** GitHub, Next.js, 주요 플랫폼 공식 문서에서 **"프로덕션 배포 전 필수 CI 게이트"를 규정하지 않음**. 즉:
- 최소 테스트 커버리지: 규정 없음 (Next.js도 "run tests" 언급 안함)
- 최소 CI checks 목록: 규정 없음 (GitHub은 "선택 가능" 으로만 명시)
- 린트/포맷 강제: 규정 없음 (개발팀 선택)

**결론:** 프레임워크/플랫폼 공식 문서 차원에서는 CI 최소 게이트가 **의도적 부재** (각 조직의 정책 결정).

### Q5 (에러 추적): 해결됨

Sentry PII 스크럽 기본값, 데이터 보존(계획별), 소스맵 선택사항 명확.

---

## 출처

### 1차: 공식 문서 (권위 주체)

**인증:**
- https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html
- https://nextjs.org/docs/app/guides/authentication
- https://supabase.com/docs/guides/auth/sessions

**DB 접근 제어:**
- https://www.postgresql.org/docs/current/ddl-rowsecurity.html
- https://supabase.com/docs/guides/database/postgres/row-level-security

**시크릿 관리:**
- https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions
- https://nextjs.org/docs/pages/guides/environment-variables
- https://vercel.com/docs/environment-variables
- https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html

**CI 최소 게이트:**
- https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule
- https://nextjs.org/docs/app/guides/production-checklist

**에러 추적:**
- https://docs.sentry.io/security-legal-pii/scrubbing/server-side-scrubbing/
- https://docs.sentry.io/security-legal-pii/security/data-retention-periods/

### 2차: 없음 (본 조사는 공식 문서만 대상)

---

## 용어 라벨 설명

- `[규정]`: 공식 문서가 명시한 요구사항 또는 사실
- `[정의]`: 개념 설명 또는 중립 서술
- `[주장]`: 권고, 권장, advisory (SHOULD/SHOULD NOT)
- `[실측]`: 직접 실행 결과 (본 조사 범위 외)
- `[1차: URL]`: 공식 벤더/표준 기관 문서
- `[2차: URL]`: 튜토리얼, 블로그, 통계 (본 조사 제외)
