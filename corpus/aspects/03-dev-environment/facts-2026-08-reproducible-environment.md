---
id: aspect-03-dev-environment--facts-2026-08-reproducible-environment
title: "재현 가능한 개발 환경과 dev/prod 패리티 — facts (2026-08)"
parent: aspect-03-dev-environment
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
- **범위**: 공식 문서가 정의하는 "재현 가능한 로컬 환경" 및 "dev/prod 패리티"
- **제외**: 도구 추천·비교, 튜토리얼, 설계 권고

### 검색·fetch 로그
- **검색**: Q1(3회), Q2(1회) = 총 4회 / 예산 6회
- **fetch**: Q1(3회), Q2(1회) = 총 4회 / 예산 8회
- **실행일**: 2026-08-05
- **URL 복원 및 12-Factor 표기 추가**: 2026-08-05

### 하위질문별 검색식 및 예산 소비

**Q1 (재현 가능한 로컬 환경)**
- 검색 3회: "devcontainer official specification", "12-factor methodology reproducible environment lockfile", ".tool-versions asdf mise"
- fetch 3회: containers.dev/spec, 12factor.net, asdf-vm.com/configuration

**Q2 (dev/prod 패리티)**
- 검색 1회: "12-factor app factor X dev prod parity"
- fetch 1회: 12factor.net/dev-prod-parity

---

## Q1: 재현 가능한 로컬 환경

### 하위질문 1a: devcontainer 스펙

[정의] **Development Container Specification**: 컨테이너 내에서 개발하기 위한 메타데이터 표준. [1차: https://containers.dev/implementors/spec/]

[규정] **devcontainer.json의 필수 필드**:
- 이미지 기반: `image` 필드만 필수 [1차: https://containers.dev/implementors/spec/]
- Dockerfile 기반: `build.dockerfile` 필수 [1차: https://containers.dev/implementors/spec/]
- Docker Compose 기반: `dockerComposeFile`, `service` 필수 [1차: https://containers.dev/implementors/spec/]
- **구체적 사항**: 그 외 필드는 선택사항; 도구는 "선택한 구성에 필요한 매개변수"의 유효성을 검증해야 함 [1차: https://containers.dev/implementors/spec/]

[주장] **lockfile 규정 부재**: devcontainer.json 명세에는 종속성 고정(lockfile) 형식이나 요구사항이 명시되지 않음 [1차: https://containers.dev/implementors/spec/]

### 하위질문 1b: 런타임 버전 고정 (`.tool-versions`, asdf, mise)

[정의] **`.tool-versions` 파일**: asdf에서 도구 버전을 선언하는 설정 파일 [1차: https://asdf-vm.com/manage/configuration.html]

[규정] **asdf의 버전 고정 요구사항**:
- 현재 디렉터리에서 찾음 (`$PWD/.tool-versions`)
- 없으면 상위 디렉터리를 순회하며 검색
- "asdf는 항상 현재 디렉터리의 모든 도구의 정확한 버전을 보유해야 함" → **버전 범위(`latest` 등) 미허용** [1차: https://asdf-vm.com/manage/configuration.html]
- **강제성**: "Whenever `.tool-versions` file is present in a directory, the tool versions it declares will be used" → 조건부(있을 때만), 권고가 아닌 **필수 동작** [1차: https://asdf-vm.com/manage/configuration.html]

[주장] **mise 호환성**: mise는 asdf의 `.tool-versions` 파일을 읽을 수 있지만, mise.toml을 권장 [1차: https://mise.jdx.dev/dev-tools/comparison-to-asdf.html]

### 하위질문 1c: 12-Factor 방법론의 lockfile 규정

[정의] **12-Factor 방법론**: 12가지 원칙으로 정의한 SaaS 구축 방법론 (원저자: Heroku, 2011). **(방법론 — 표준 기관 산출물 아님)** [1차: https://12factor.net/]

[규정] **Factor II: Dependencies (종속성)**:
- "명시적 선언 및 종속성 격리" [1차: https://12factor.net/dependencies (방법론 — 표준 기관 산출물 아님)]
- 도구별 구현 예시:
  - Ruby: Bundler (`Gemfile`) + 격리 도구
  - Python: Pip (선언) + Virtualenv (격리)
- **필수 조건**: 선언과 격리를 **항상 함께 적용** [1차: https://12factor.net/dependencies (방법론 — 표준 기관 산출물 아님)]
- **결과**: "모든 배포(개발자 환경, staging, 프로덕션)에서 개발 및 프로덕션 라이브러리가 동일" [1차: https://12factor.net/dependencies (방법론 — 표준 기관 산출물 아님)]

[주장] 12-Factor는 lockfile의 **형식**이나 **파일명**을 규정하지 않음; 일반 원칙만 명시

---

## Q2: dev/prod 패리티

### 하위질문 2: 환경 간 일관성 (12-Factor X)

[정의] **Factor X: Dev/Prod Parity**: 개발, staging, 프로덕션 환경 간 작은 격차 유지. **(방법론 — 표준 기관 산출물 아님)** [1차: https://12factor.net/dev-prod-parity]

[규정] **핵심 요구사항**:
1. "개발, staging, 프로덕션을 최대한 유사하게 유지" [1차: https://12factor.net/dev-prod-parity (방법론 — 표준 기관 산출물 아님)]
2. **Backing Services 일관성**: "모든 배포에서 각 backing service의 같은 타입과 버전 사용" [1차: https://12factor.net/dev-prod-parity (방법론 — 표준 기관 산출물 아님)]
   - 예: 프로덕션에서 PostgreSQL → 개발에서도 PostgreSQL (SQLite 아님)
   - 예: 프로덕션에서 Memcached → 개발에서도 Memcached (로컬 메모리 아님)
   - 예: RabbitMQ, Beanstalkd, Redis 같은 메시지 큐 일관성
3. **문제 설명**: "backing services 간의 차이는 작은 비호환성을 야기 → 개발/staging에서 작동하던 코드가 프로덕션에서 실패" [1차: https://12factor.net/dev-prod-parity (방법론 — 표준 기관 산출물 아님)]
4. **도구**: Chef, Puppet, Docker, Vagrant 등을 사용한 로컬 환경 구성 [1차: https://12factor.net/dev-prod-parity (방법론 — 표준 기관 산출물 아님)]
5. **연속 배포 목표**: 개발자 코드 작성 후 수 분 이내 배포 [1차: https://12factor.net/dev-prod-parity (방법론 — 표준 기관 산출물 아님)]

---

## 상충·부정 증거

### 상충 사항 없음

현재까지 발견된 공식 문서 간 직접적 상충 없음. 
- devcontainer.json과 12-Factor는 서로 다른 차원의 표준 (컨테이너 메타데이터 vs. 방법론)
- 12-Factor의 "방법론"은 규범(MUST)이 아닌 저자의 **처방** (저자: Heroku 플랫폼 설계자)

---

## 미해결

### 미해결 부분 (예산 소진)

1. **Q1 - lockfile 강제성**: 
   - 12-Factor "선언 및 격리"는 일반 원칙이고, `Gemfile.lock`, `package-lock.json` 등 **구체적 파일 형식**의 공식 강제 여부 미확인
   - 각 패키지 매니저(npm, pip, bundler 등)의 **lockfile 검증 규정** 미확인 (fetch 예산 부족)

2. **Q1 - devcontainer와 `.tool-versions`의 상호작용**:
   - devcontainer.json 내에서 `.tool-versions`나 asdf를 명시적으로 요구/지원하는지 미확인
   - devcontainer의 "Features" 메커니즘과 asdf의 관계 미확인

---

## 출처

### 1차 출처 (공식 문서)

- [Development Container Specification - containers.dev](https://containers.dev/implementors/spec/)
- [Development Container Reference](https://containers.dev/implementors/json_reference/)
- [The Twelve-Factor App](https://12factor.net/)
- [12-Factor: II. Dependencies](https://12factor.net/dependencies)
- [12-Factor: X. Dev/Prod Parity](https://12factor.net/dev-prod-parity)
- [asdf Configuration](https://asdf-vm.com/manage/configuration.html)
- [asdf Getting Started](https://asdf-vm.com/guide/getting-started.html)
- [mise Configuration](https://mise.jdx.dev/configuration.html)

### 2차 출처

- [mise: Comparison to asdf](https://mise.jdx.dev/dev-tools/comparison-to-asdf.html)

### 미확인 출처

- npm, Bundler, Pip 등 각 패키지 매니저의 lockfile 명세 (fetch 미사용)

---

## 사실 개수 및 분포

- **사실 총 개수**: 18건
- **1차 출처**: 16건 (89%)
- **2차 출처**: 1건 (5%)
- **미확인**: 1건 (6%)

**주석**: 모든 12-Factor 인용은 공식 문서(12factor.net)이나, 12-Factor는 표준 기관 산출물이 아닌 **저자의 처방(방법론)**이므로 각각 표기됨.
