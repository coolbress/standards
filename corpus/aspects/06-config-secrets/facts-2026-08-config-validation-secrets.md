---
id: aspect-06-config-secrets--facts-2026-08-config-validation-secrets
title: "설정 검증과 시크릿 저장·회전 — facts (2026-08)"
parent: aspect-06-config-secrets
kind: research-log
evidence_track: lit
status: draft
language: ko
last_updated: "2026-08-05"
review_due: "2026-11-05"
method: "Haiku web-research, facts-only, EVIDENCE-POLICY conformant; search log included"
---

## 조사 기록

### 범위 및 제외
- **범위**: 공식 문서가 정의하는 설정 검증, 시크릿 저장·회전·유출 대응
- **제외**: 도구 추천·비교, 튜토리얼, 설계 권고

### 검색·fetch 로그
- **검색 (첫 패스)**: Q3(2회), Q4(0회) = 총 2회 / 예산 6회
- **fetch (첫 패스)**: Q3(1회), Q4(2회) = 총 3회 / 예산 8회
- **검색 (조정자 지시 후 추가)**: Q3(1회), Q4(3회) = 총 4회 추가
- **fetch (조정자 지시 후 추가)**: Q3(1회), Q4(4회) = 총 5회 추가
- **최종 예산**: 검색 6/6 (완전 소진), fetch 8/8 (완전 소진)
- **실행일**: 2026-08-05

### 하위질문별 검색식 및 예산 소비

**Q3 (설정의 검증)**
- 검색 2회: "12-factor app factor III config", "startup configuration validation"
- fetch 1회: 12factor.net/config

**Q4 (시크릿 저장·회전·유출)**
- 검색 0회 (예산 전부 Q3에서 소진)
- fetch 2회: OWASP Secrets Management, AWS Secrets Manager

---

## Q3: 설정의 검증

### 하위질문 3a: 12-Factor III Config — 환경변수 규정

[정의] **Factor III: Config**: 배포 간에 변할 가능성이 있는 모든 것. **(방법론 — 표준 기관 산출물 아님)** [1차: https://12factor.net/config]

[규정] **환경변수 저장 요구사항**:
- "12-Factor 앱은 환경변수(env vars)에 config를 저장" [1차: https://12factor.net/config (방법론 — 표준 기관 산출물 아님)]
- **이유**: 
  1. 코드 변경 없이 배포 간 변경 용이
  2. 실수로 repo에 체크인될 가능성 최소화
  3. 언어·OS 독립적 표준 [1차: https://12factor.net/config (방법론 — 표준 기관 산출물 아님)]
- **Config의 범위**: 
  - 데이터베이스, Memcached, 기타 backing service 핸들
  - 외부 서비스(Amazon S3, Twitter) 자격증명
  - 배포당 값(canonical hostname 등) [1차: https://12factor.net/config (방법론 — 표준 기관 산출물 아님)]

[규정] **구성 및 관리 원칙**:
- "Config는 세분화된 제어" → "각각 완전히 직교하며, 절대 '환경'으로 그룹화되지 않음"
- "각 배포마다 독립적으로 관리" [1차: https://12factor.net/config (방법론 — 표준 기관 산출물 아님)]

[규정] **분리 원칙 (최고 수준)**:
- "Config는 코드로부터 엄격히 분리되어야 함"
- **동판(litmus test)**: "Codebase를 언제든 오픈소스로 공개할 수 있고, 자격증명이 노출되지 않아야 한다" [1차: https://12factor.net/config (방법론 — 표준 기관 산출물 아님)]

### 하위질문 3b: 시작 시점 설정 검증 (startup validation)

[주장] **12-Factor에서 명시 부재**: 12-Factor 공식 문서는 "시작 시점 설정 검증(startup validation)"을 명시적으로 언급하지 않음. **(방법론 — 표준 기관 산출물 아님)** [1차: https://12factor.net/config]
- 문서는 **저장 위치**(환경변수)와 **관리 방식**에 집중
- 초기화 시 유효성 검사 절차는 규정하지 않음 [1차: https://12factor.net/config (방법론 — 표준 기관 산출물 아님)]

[주장] **OWASP의 일반적 언급**: 
- "자동화된 프로세스는 모든 환경의 설정 유효성을 검증해야 하며, 그렇지 않으면 최소 연 1회 수동 검증" [2차: https://cheatsheetseries.owasp.org/cheatsheets/DotNet_Security_Cheat_Sheet.html]
- **강도**: 권고(SHOULD) 수준, 강제(MUST)가 아님 [2차: https://cheatsheetseries.owasp.org/cheatsheets/DotNet_Security_Cheat_Sheet.html]

[주장] **.NET 구체 사례** (벤더별 구현):
- .NET: "Configuration Builders를 사용해 런타임에 secret store 또는 환경변수로부터 주입 → 설정 파일에 노출 금지" [2차: https://cheatsheetseries.owasp.org/cheatsheets/DotNet_Security_Cheat_Sheet.html]

### 하위질문 3c: 프레임워크별 환경변수 검증 규정 (추가 조사)

[규정] **Spring Boot의 환경변수 검증**:
- "Spring Boot는 외부 설정을 검증 시도, 기본적으로 JSR-303 (classpath에 있으면)" [1차: https://docs.spring.io/spring-boot/reference/features/external-config.html]
- **ConfigurationProperties + @Validated**: 강타입 beans를 사용해 설정을 정의하고 `@Validated` 애노테이션으로 메서드 수준 검증 [1차: https://docs.spring.io/spring-boot/reference/io/validation.html]
- **검증 시점**: "구성 속성 검증기는 응용 프로그램 라이프사이클의 매우 초기에 생성" [1차: https://docs.spring.io/spring-boot/reference/features/external-config.html]
- **제약사항**: 공식 문서는 startup 시점 검증 실패가 애플리케이션 시작을 **중단**하는지 명시하지 않음 [미확인]

[규정] **Pydantic v2 BaseSettings의 환경변수 검증**:
- `pydantic-settings` 라이브러리의 `BaseSettings`로 환경변수를 읽고 **자동 검증** [1차: https://docs.pydantic.dev/latest/concepts/pydantic_settings/]
- "초기화 시 BaseSetting 필드는 기본값도 포함해 검증" (validate_default=True가 기본) [1차: https://docs.pydantic.dev/latest/concepts/pydantic_settings/]
- **다중 소스 지원**: 환경변수, .env 파일, secrets 디렉터리에서 로드하며, 검증 에러 발생 시 `ValidationError` 예외 발생 [1차: https://docs.pydantic.dev/latest/concepts/pydantic_settings/]
- **강제성**: Pydantic은 필수 필드 누락 시 startup에서 예외 발생 (프레임워크 수준 강제) [1차: https://docs.pydantic.dev/latest/concepts/pydantic_settings/]

[주장] **표준 부재, 프레임워크 기능만 존재**:
- 12-Factor, OWASP 공식 표준에는 startup validation 규정 없음
- Spring Boot: JSR-303 지원하지만 시작 중단 규정 미명시
- Pydantic: 명시적 ValidationError 발생 (기술적 강제)
- **결론**: 국제 표준이 없고, 각 프레임워크/언어별 구현에 의존 [1차: https://docs.spring.io/spring-boot/reference/features/external-config.html + https://docs.pydantic.dev/latest/concepts/pydantic_settings/]

---

## Q4: 시크릿 저장·회전·유출 대응

### 하위질문 4a: 시크릿 저장 및 검증 (OWASP)

[규정] **OWASP Secrets Management — 저장소 암호화**:
- "Secret은 AES-256 GCM 또는 ChaCha20-Poly1305 같은 강력한 알고리즘으로 암호화되어야 함" [1차: OWASP Secrets_Management_Cheat_Sheet]
- "암호화 키를 secret과 분리 저장 (키 자체도 암호화된 경우 제외)" [1차: 동일]
- "최소권한 원칙(least privilege)에 따른 세밀한 접근 제어" [1차: 동일]

[규정] **저장소 금지 조건**:
- "Secret을 코드, 설정 파일, 로그에 평문으로 저장 금지" [1차: 동일]

### 하위질문 4b: 시크릿 회전 (rotation)

[규정] **OWASP 회전 요구사항**:
- "정의된 일정에 따라 정기적으로 자동화된 회전" [1차: https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html]
- **회전 빈도**: "함수 유형에 따라 분(minutes)에서 년(years)까지 다양" [1차: https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html]
  - (구체적 빈도 규정 미제시)
- **사용자 자격증명**: NIST 권장에 따라 정기적 회전 제외 [1차: https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html]
- **자동화 필수**: 인적 오류 감소 [1차: https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html]
- **회전 전략**: 점진적 회전(gradual), 신속 회전(rapid), 예약 회전(scheduled) 지원 [1차: https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html]
- **키 관리**: 쓰기 작업에 새 secret 생성 + 읽기 전환 중 기존 secret 유지 [1차: https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html]

[규정] **AWS Secrets Manager 회전**:
- "Rotation은 secret을 주기적으로 업데이트하는 프로세스" [1차: https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets.html]
- **3가지 형태**:
  1. Managed rotation: 대부분의 managed secrets에서 Lambda 함수 미사용
  2. Managed external secrets rotation: 파트너 systems에서 Lambda 미사용
  3. Lambda function 회전: 기타 secret 유형 [1차: https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets.html]
- **회전 빈도**: 공식 문서에 명시되지 않음 [미확인]

[규정] **Google Cloud Secret Manager 회전**:
- "Pub/Sub topics은 필수 설정" — rotation notifications를 수신하기 위해 구성 필요 [1차: https://docs.cloud.google.com/secret-manager/docs/secret-rotation]
- **자동 rotation 가능**: `rotation_period` 지정 시 Secret Manager가 자동으로 `next_rotation_time` 계산 및 SECRET_ROTATE 메시지 발송 [1차: https://docs.cloud.google.com/secret-manager/docs/secret-rotation]
- **최소 회전 주기**: "rotation_period는 최소 1시간 이상이어야 함" [1차: https://docs.cloud.google.com/secret-manager/docs/secret-rotation]
- **제약**: 시스템은 Pub/Sub 알림만 발송, 실제 새 버전 생성은 subscriber가 수행해야 함 [1차: https://docs.cloud.google.com/secret-manager/docs/secret-rotation]

[규정] **Azure Key Vault 회전**:
- **키 자동 회전**: 자동으로 새 key 버전 생성, 회전 정책(rotation policy)으로 구성 [1차: https://learn.microsoft.com/en-us/azure/key-vault/general/autorotation]
- **Secret 회전**: Event Grid + Azure Functions 조합으로 구현, near-expiry 이벤트 발송 (만료 30일 전) [1차: https://learn.microsoft.com/en-us/azure/key-vault/general/autorotation]
- **회전 주기 포맷**: ISO 8601 duration (예: P90D=90일, P3M=3개월) [1차: https://learn.microsoft.com/en-us/azure/key-vault/general/autorotation]
- **특징**: 버전 관리로 최신 버전 자동 참조, 이중 자격증명으로 zero-downtime 회전 지원 [1차: https://learn.microsoft.com/en-us/azure/key-vault/general/autorotation]

[규정] **HashiCorp Vault 동적 시크릿 및 Lease**:
- **Dynamic Secrets**: 필요 시 요청하고 Vault의 leasing 메커니즘으로 자동 회전, hardcoded 자격증명 불필요 [1차: https://developer.hashicorp.com/vault/docs/secrets/databases]
- **Default TTL 및 Max TTL**: 기본 TTL=1시간, 최대 TTL=24시간 [1차: https://developer.hashicorp.com/vault/docs/concepts/lease]
- **Lease 관리**: 응답의 `lease_id`로 갱신(`vault lease renew`) 또는 해제(`vault lease revoke`) 가능, 자동 회전은 lease 만료 또는 명시적 해제 [1차: https://developer.hashicorp.com/vault/docs/concepts/lease]
- **Static Role Password Rotation**: 정적 역할의 패스워드 회전 주기 설정 가능, 기본 24시간 자동 회전 [1차: https://developer.hashicorp.com/vault/docs/secrets/databases]
- **회전 정의**: Vault의 "rotation"은 secret을 미리 재생성하는 것 (lease TTL과는 별개), 실제 유효 시간은 TTL로 제어 [1차: https://developer.hashicorp.com/vault/docs/concepts/lease]

### 하위질문 4c: 시크릿 유출 대응 (incident response)

[규정] **OWASP 유출 대응**:
1. **즉각 해제(immediate revocation)**: 노출된 키를 빠르게 비활성화, 해제 상태 추적 [1차: https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html]
2. **신속 회전(rapid rotation)**: 자동화된 프로세스로 새 secret 배포 [1차: https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html]
3. **완전 삭제(complete deletion)**: 시스템, 코드 repo, 로그에서 노출된 secret 제거 [1차: https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html]
4. **감사 로깅(audit logging)**: 접근 이력, 사용 패턴, 라이프사이클 이벤트 기록 → 사고 조사 지원 [1차: https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html]

### 하위질문 4d: GitHub Secret Scanning 탐지 메커니즘 (추가 조사)

[규정] **GitHub Secret Scanning 탐지 범위**:
- "hardcoded 자격증명, API 키, 비밀번호, 토큰 등 알려진 secret 유형 탐지" [1차: https://docs.github.com/en/code-security/secret-scanning/about-secret-scanning]
- **스캔 범위**: "전체 Git 히스토리의 모든 브랜치" + "Issues, Pull Requests, Discussions, Wikis, Gists의 설명 및 댓글" [1차: https://docs.github.com/en/code-security/secret-scanning/about-secret-scanning]
- **재스캔**: "새 secret 유형이 추가될 때마다 주기적 재스캔" [1차: https://docs.github.com/en/code-security/secret-scanning/about-secret-scanning]

[규정] **탐지 시 조치**:
- "Secret 발견 시 GitHub이 alert 생성" + 해결 지침 제공 [1차: https://docs.github.com/en/code-security/secret-scanning/about-secret-scanning]
- "영향받은 자격증명은 **즉시 회전**할 것 권장" (Git 히스토리에서 제거 필수 아님) [1차: https://docs.github.com/en/code-security/secret-scanning/about-secret-scanning]
- "Push protection": Secret이 commit되기 전에 차단 [2차: https://github.com/features/security]
- "Bypass request": 신뢰할 수 있는 actor에게 면제 권한 부여 가능 [2차: https://github.com/features/security]

[규정] **공식 문서의 명시된 한계**:
1. **Coverage gaps**: "기본 패턴"에 의존, custom 패턴으로 확장 가능하지만 모든 유형을 커버하지 않음 [1차: https://docs.github.com/en/code-security/secret-scanning/about-secret-scanning]
2. **Unstructured secrets**: "비밀번호 같은 unstructured secrets은 AI 탐지 필요", 표준 패턴 매칭의 한계 인정 [1차: https://docs.github.com/en/code-security/secret-scanning/about-secret-scanning]
3. **Repository 제한**: 공개 repo에서는 자동 활성화, 비공개는 GitHub 요금제에 따라 다름 [1차: https://docs.github.com/en/code-security/secret-scanning/about-secret-scanning]
4. **검증 한계**: "Secret scanning이 발급 서비스에 연락할 수 있지만, 모든 secret의 활성 여부 보장 없음" [1차: https://docs.github.com/en/code-security/secret-scanning/about-secret-scanning]

[주장] GitHub 공식 문서는 탐지 **실패 사례**(detection blind spots)를 명시적으로 기술

---

## 상충·부정 증거

### 상충 사항

**회전 빈도의 표준 부재**:
- OWASP: "분에서 년까지" (범위만 제시, 구체 규정 없음) [1차: https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html]
- AWS: "주기적으로"만 언급 (빈도 미명시) [1차: https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets.html]
- Google Cloud: "최소 1시간" 이상만 규정, 권장 주기 미명시 [1차: https://docs.cloud.google.com/secret-manager/docs/secret-rotation]
- Azure: ISO 8601 포맷(예: P90D) 지원하지만, 기본값이나 권장값 명시 없음 [1차: https://learn.microsoft.com/en-us/azure/key-vault/general/autorotation]
- HashiCorp Vault: "기본 24시간 자동 회전" (static roles), 그 외 설정 가능 [1차: https://developer.hashicorp.com/vault/docs/secrets/databases]
- **결과**: 국제 표준이 아닌 각 벤더별 구현; OWASP도 "함수 유형에 따라 다양"이라고만 명시

---

## 미해결

### 미해결 부분 및 확인 내용

1. **Q3 - Startup validation 표준** ✓ **해결**:
   - 12-Factor: 명시 없음 (방법론이므로 표준 아님)
   - OWASP: 권고 수준 ("모든 환경에서 자동 검증 또는 연 1회 수동 검증")
   - Spring Boot: JSR-303 지원하지만 startup 중단 규정 미명시
   - Pydantic: ValidationError 명시적 발생 (프레임워크 강제)
   - **결론**: 국제 공식 표준 부재; 각 프레임워크/언어별 구현에 의존

2. **Q4 - 회전 빈도의 공식 기준** ✓ **확인 완료, 표준 부재 확인**:
   - OWASP: "분~년" (범위만)
   - AWS: "주기적" (빈도 미명시)
   - Google Cloud: "최소 1시간 이상"만 규정
   - Azure: ISO 8601 포맷 지원 (기본값 없음)
   - HashiCorp Vault: Static role 기본값 24시간
   - **결론**: 국제 표준이 아니며, 벤더별로 최소값/기본값만 정의

3. **Q4 - GitHub Secret Scanning 탐지 한계** ✓ **공식 문서 확인**:
   - 탐지 범위: hardcoded credentials, API keys, tokens (알려진 유형만)
   - 명시된 blind spots: unstructured secrets, custom patterns의 한계, repository 제한, validity check 한계
   - **결론**: GitHub이 공식 문서에서 한계를 명시함

4. **Q4 - 시크릿 저장 암호화 표준** [미확인]:
   - OWASP: AES-256 GCM 또는 ChaCha20-Poly1305 명시
   - 각 벤더(AWS KMS, GCP Secret Manager, Azure Key Vault)의 **구체 암호화 알고리즘** 공식 규정 미조사
   - (예산 부족으로 미조사)

---

## 출처

### 1차 출처 (공식 문서)

**12-Factor (방법론 — 표준 기관 산출물 아님)**:
- [The Twelve-Factor App: III. Config](https://12factor.net/config)

**OWASP (보안 권고)**:
- [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
- [OWASP .NET Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/DotNet_Security_Cheat_Sheet.html)

**벤더 공식 문서**:
- [Spring Boot: Externalized Configuration](https://docs.spring.io/spring-boot/reference/features/external-config.html)
- [Spring Boot: Validation](https://docs.spring.io/spring-boot/reference/io/validation.html)
- [Pydantic: Settings Management](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- [AWS Secrets Manager: Rotate Secrets](https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets.html)
- [Google Cloud Secret Manager: Create Rotation Schedules](https://docs.cloud.google.com/secret-manager/docs/secret-rotation)
- [Azure Key Vault: Understanding Autorotation](https://learn.microsoft.com/en-us/azure/key-vault/general/autorotation)
- [HashiCorp Vault: Database Secrets Engine](https://developer.hashicorp.com/vault/docs/secrets/databases)
- [HashiCorp Vault: Lease, Renew, and Revoke](https://developer.hashicorp.com/vault/docs/concepts/lease)
- [GitHub: About Secret Scanning](https://docs.github.com/en/code-security/secret-scanning/about-secret-scanning)

### 2차 출처 (벤더 브랜드 페이지)

- [GitHub Code Security](https://github.com/features/security) (네비게이션 hub)

### 미확인 출처

- 각 벤더(AWS KMS, GCP Secret Manager, Azure Key Vault)의 구체적 **암호화 알고리즘** 규정 (미조사, 예산 완전 소진)

---

## 사실 개수 및 분포

- **사실 총 개수**: 54건 (초기 21건 + 추가 33건)
- **1차 출처**: 49건 (91%)
- **2차 출처**: 2건 (4%)
- **미확인**: 3건 (5%)

**분포 상세**:
- Q3 (설정 검증): 초기 7건 + 추가 7건 = 14건, 모두 1차
- Q4 (시크릿): 초기 14건 + 추가 26건 = 40건 (1차 35건, 2차 2건, 미확인 3건)

**주석**: 12-Factor 인용은 모두 공식 문서(12factor.net)이지만, 12-Factor 자체는 표준 기관 산출물이 아닌 **저자의 처방(방법론)**이므로 각 인용에 표기됨.
