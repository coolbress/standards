---
id: aspect-10-supply-chain-security--facts-2026-08-dependency-updates-scope
title: "의존성 자동 업데이트와 공급망 규정의 적용 범위 — facts (2026-08)"
parent: aspect-10-supply-chain-security
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
- 하위질문 4개: (Q3) 의존성 자동 업데이트 규정, (Q4) SBOM·서명·스코어카드 적용 조건
- 공식 1차 출처: GitHub (Dependabot), Renovate, SLSA, OpenSSF Scorecard, SPDX/CycloneDX, NTIA/CISA
- 특별 제약: Q4에서 "자체 호스팅 웹 앱"에 대한 명시 여부를 문서에서 찾고, 없으면 "명시 없음" 기록
- 제외: 도구 추천, 튜토리얼, goppi 설계 결정

### 검색 예산 사용 (2026-08-05)
| 구분 | 질문 3 | 질문 4 | 합계 |
|------|--------|--------|------|
| 검색 | 3/4 | 2/4 | 5/8 |
| fetch | 3/3 | 4/4 | 7/7 |
| 상태 | ✓ 완료 | ✓ 완료 | - |

---

## Q3 — 의존성 자동 업데이트: 자동화 범위와 한계

### Dependabot (GitHub 공식)

**[규정] Dependabot의 자동 업데이트 범위**

GitHub 공식 문서 (*Dependabot version updates*):

#### 자동으로 업데이트하는 대상
- 지원되는 에코시스템의 패키지 의존성
- GitHub Actions 워크플로우의 액션 참조
- 워크플로우 내에서 사용되는 재사용 가능한 워크플로우
- 저장소의 벤더링(캐시된) 의존성

#### 자동으로 업데이트하지 않는 것 / 제약
- **메이저 버전**: 기본값으로 모든 semver 업데이트 포함 (메이저 포함). `version-update:semver-minor` 등의 설정으로 제어 가능.
- **테스트 통과 판정**: Dependabot은 자동으로 테스트 결과를 확인하지 않음. 사용자가 PR을 검토한 후 테스트 통과를 수동 확인하고 merge 결정.

**[규정] 테스트 책임 분리**  
공식 문서: "check that your tests pass" — pull request 검토 후 사용자 책임.

**[1차: https://docs.github.com/en/code-security/dependabot/dependabot-version-updates]**

### Renovate (Mend 공식)

**[규정] Renovate의 자동 업데이트 범위**

Renovate 공식 문서:
- 저장소의 패키지 파일 자동 발견 (monorepo 포함)
- 버전 업데이트에 대한 pull request 생성

**제약 명시 없음**: 공식 홈페이지 및 기본 문서에서:
- 메이저 버전 업데이트 제약 명시 안 함
- 테스트 통과 요구 명시 안 함
- `enabled: false` 등으로 특정 의존성 업데이트 비활성화 가능 (제약이 아닌 제어 옵션)

**[1차: https://docs.renovatebot.com/]** **[1차: https://docs.mend.io/wsk/renovate-package-rules-guide]**

### GitHub Security Advisory — 자동 동작

**[규정] Dependabot 보안 경고의 자동 동작**

GitHub 공식 문서 (*Dependabot alerts*):

#### 자동으로 수행되는 것
1. **경고 생성**: 취약점 감지 시 보안 탭 및 종속성 그래프에 Dependabot 경고 표시
2. **알림**: 저장소의 적절한 권한을 가진 구성원에게 알림 발송 (정보성)

#### 자동으로 생성되지 않는 것
- **PR 자동 생성 없음**: 기본적으로 경고만 표시. AI 에이전트(Copilot, Claude) 할당 시에만 자동으로 draft PR 생성.
- **자동 수정 없음**: 사람의 검토 및 결정 필요.

**[규정] 원칙: 사람의 감시 (Human Oversight)**  
시스템은 "알림 → 사람의 검토 → 에이전트 할당 시 자동 PR"의 흐름.

**[1차: https://docs.github.com/code-security/dependabot/dependabot-alerts/about-dependabot-alerts]**

---

### 종합: Q3

| 도구 | 메이저 업그레이드 | 테스트 통과 자동 판정 | 자동 PR 생성 |
|-----|-------------|--------------|----------|
| Dependabot | 기본값: 포함 (설정 가능) | **아니오** (사용자 검토) | 기본값: 예 |
| Renovate | 명시 없음 | 명시 없음 | 예 (비활성화 가능) |
| GitHub Advisory | N/A (경고만) | N/A | **아니오** (agent 할당 시에만) |

**미해결 없음.**

---

## Q4 — SBOM·서명·스코어카드의 적용 범위: "자체 호스팅 웹 앱"에 명시되는가?

### SLSA (Supply Chain Levels for Software Artifacts)

**[정의] SLSA의 적용 대상**

SLSA 공식 스펙:
- "한 팀이 만든 소프트웨어를 다른 팀이나 고객이 사용할 때마다 유용"
- 내부 플랫폼과 외부 소프트웨어 배포 모두에 적용 가능
- 빌드 플랫폼: "다중 독립 재구성 시스템, 특수 목적 빌드 플랫폼, 개인 워크스테이션"

**[규정] "배포 아티팩트" 중심**

SLSA 요구 사항:
- 생산자는 소비자에게 provenance(출처 증명) **배포** 의무
- 빌드 플랫폼은 설정 메타데이터 제공
- **자체 호스팅 웹 앱에 대한 명시: 없음**

**분석**: SLSA는 "배포되는 아티팩트"를 중심으로 설계. 자체 호스팅 실행 서비스(web app이 운영 중인 상태)에 직접 적용되는지는 문서에서 명시되지 않음. 빌드 프로세스의 무결성은 적용 가능하나, 배포되지 않는 서비스에 필수는 아님.

**[1차: https://slsa.dev/spec/v1.0/requirements]** **[1차: https://slsa.dev/spec/v1.1/faq]**

### OpenSSF Scorecard

**[정의] Scorecard의 대상**

OpenSSF 공식:
- "개인 유지보수자": 신규 프로젝트 출시 전 보안 검사, 기존 프로젝트 개선 계획
- "조직": CI/CD 파이프라인에 GitHub Action으로 통합 (자동 스캔)
- "소비자": 의존성 평가 시 오픈소스 프로젝트 검사

**[규정] 준수 의무**

Scorecard 공식 문서: **의무 요구 없음**
- 유지보수자가 자발적으로 실행
- 소비자가 제3자 프로젝트 평가에 사용
- **자체 호스팅 웹 앱에 대한 명시: 없음**

Scorecard는 "평가 도구"이지, "준수 강제" 표준이 아님. 오픈소스 프로젝트 신뢰도 평가에 초점.

**[1차: https://scorecard.dev/]** **[1차: https://openssf.org/projects/scorecard/]**

### SBOM (Software Bill of Materials) — SPDX / CycloneDX

**[정의] SBOM 의무 대상**

NTIA / CISA / GitHub 공식 문서:

#### 의무 대상
1. **U.S. 연방정부 판매**: 2025년부터 정부에 소프트웨어를 판매하는 기업은 SBOM 제공 의무
2. **규제 산업**: FDA, ISO, EU 등에서 의료, 국방, 중요 인프라 등 요구
3. **현황**: 연방정부 및 규제 산업 판매만 의무 (2026년 현재)

#### 자체 호스팅 웹 앱
GitHub 공식:
- "Self-hosted web application"에 대한 명시적 요구 사항: **문서에 명시 없음**
- 현행 의무: 연방정부 판매 또는 규제 산업만 적용
- "일반 자체 호스팅 앱"은 법적 의무 없음

**[규정] 선택적 모범 사례**  
SBOM은 "업계 모범 사례로 부상" 중이지만, 자체 호스팅 웹 앱에 대한 공식 요구는 미발생.

**[1차: https://github.com/resources/articles/what-is-an-sbom-software-bill-of-materials/]**  
**[미확인: 보안 경고 문서 (GitHub docs 여러 페이지에서 언급되었으나 단일 URL로 특정 불가)]**  
**[2차: https://www.interlynk.io/resources/cyclonedx-vs-spdx-sbom-format]**

---

## 적용 범위 표

| 규정/표준 | 규정 기관 | 명시된 대상 주체 | 자체 호스팅 웹 앱 적용 | 문서 상태 |
|----------|---------|-------------|------------|---------|
| **SLSA** | SLSA Framework (OpenSSF) | 소프트웨어 생산자 (배포 아티팩트 중심) | **명시 없음** (배포되는 아티팩트 대상이 아니면 범위 불명) | [1차: https://slsa.dev/spec/v1.0/requirements] |
| **Scorecard** | OpenSSF | 오픈소스 프로젝트 유지보수자 / 소비자 (선택적 평가) | **명시 없음** (의무 아님; 평가 도구) | [1차: https://scorecard.dev/] |
| **SBOM (SPDX/CycloneDX)** | NTIA / CISA / 정부 | 정부 판매 기업 / 규제 산업 (의료, 국방, CI) | **명시 없음** (현행 의무 없음; 규제 부문만 해당) | [1차: https://github.com/resources/articles/what-is-an-sbom-software-bill-of-materials/] |

---

## 상충·부정 증거

### Q3 — Dependabot 메이저 버전 처리

**상충 없음**: 초기 검색에서 "ignore" 설정으로 제외 가능하다는 정보와 "기본값으로 포함"이라는 정보가 병행되었으나, 양립 가능 (기본값 포함, 설정으로 제외 가능). 문서에서 공식 확인됨.

---

## 미해결

### Q2 (이전 섹션 참조)
1. SWEBOK v4 원문에서 부채 추적 의무 명시 여부 (전문 접근 제한)
2. CISQ Technical Debt Standard 요구 사항 (웹사이트 HTTP 522 에러)

### Q4
1. **"명시 없음" 3개 항목**: SLSA, Scorecard, SBOM 모두 자체 호스팅 웹 앱에 대한 명시적 적용 조건 또는 제외 없음.
   - SLSA: 배포 아티팩트 중심, 자체 호스팅 서비스 범위 불명확
   - Scorecard: 오픈소스 평가 도구, 자체 호스팅 앱 준수 요구 무관
   - SBOM: 정부/규제 산업 판매만, 일반 자체 호스팅 앱 의무 없음

---

## 출처

### 1차 (공식 문서, 개방 접근)

- **GitHub.** "About Dependabot version updates." *GitHub Docs*, https://docs.github.com/en/code-security/dependabot/dependabot-version-updates
- **GitHub.** "Configuring Dependabot version updates." *GitHub Docs*, https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/secure-your-dependencies/configuring-dependabot-version-updates
- **GitHub.** "About Dependabot alerts." *GitHub Docs*, https://docs.github.com/code-security/dependabot/dependabot-alerts/about-dependabot-alerts
- **Mend.** "Renovate Docs." https://docs.renovatebot.com/
- **Mend.** "Renovate Package Rules Guide." *Mend.io Documentation*, https://docs.mend.io/wsk/renovate-package-rules-guide
- **SLSA Framework (OpenSSF).** "SLSA • Producing artifacts." *Spec v1.0*, https://slsa.dev/spec/v1.0/requirements
- **SLSA Framework (OpenSSF).** "SLSA • Frequently Asked Questions." *Spec v1.1*, https://slsa.dev/spec/v1.1/faq
- **OpenSSF.** "OpenSSF Scorecard." https://scorecard.dev/
- **OpenSSF.** "Scorecard." https://openssf.org/projects/scorecard/
- **GitHub.** "What is an SBOM (Software Bill of Materials)?" *GitHub Resources*, https://github.com/resources/articles/what-is-an-sbom-software-bill-of-materials/

### 2차 (기술 분석, 컨설팅 해설)

- **Interlynk.** "CycloneDX vs SPDX: Choosing an SBOM Format for Regulatory Compliance (2026 Edition)." https://www.interlynk.io/resources/cyclonedx-vs-spdx-sbom-format
- **Wiz.** "What is The SLSA Framework? Supply-chain Levels for Software Artifacts." *Wiz Academy*, https://www.wiz.io/academy/application-security/slsa-framework

### 미확인 (접근 불가 / 제한)

- **CISQ.** "Technical Debt Standard." — `it-cisq.org` 페이지가 2026-08-05 전수 검사에서 HTTP 522(원서버 응답 없음). 본문 미확보이며 URL은 링크 검사 대상에서 제외(재시도는 review_due 때).
