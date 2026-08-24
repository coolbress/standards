---
id: aspect-09-application-security--facts-2026-08-security-sdlc
title: "Security in the SDLC — facts (2026-08)"
parent: aspect-09-application-security
kind: research-log
evidence_track: lit
status: draft
language: ko
last_updated: "2026-08-02"
method: "Haiku web-research agents, facts-only rules ([정의/규정]/[데이터]/[주장] labels), source-tier tagged [1차]/[2차]; session-lead verified"
---

# 소프트웨어 개발 라이프사이클 보안 실행 관례

## 개요

[정의/규정] 현대 소프트웨어 보안은 설계부터 운영까지 전체 라이프사이클을 포함한다. OWASP Top 10 2025 기준 주요 위협이 무엇인지, Microsoft SDL·OWASP ASVS·SAMM 등 주요 프레임워크가 규정하는 내용, threat modeling·secret 관리·공급망 보안 등 핵심 실행 관례를 정의한다. [데이터] Verizon DBIR 2026은 소프트웨어 취약점이 처음 초기 접근 벡터 1위를 차지했다고 보고한다. [주장] AI 생성 코드는 보안 문제의 새로운 원천으로 나타난다.

---

## OWASP Top 10:2025

[정의/규정] OWASP Top 10:2025는 웹 애플리케이션의 10대 비판적 보안 위험을 정의한다 [https://owasp.org/Top10/2025/]. 2025년 11월 공개, 2026년 1월 최종 배포되었으며, 2021 이후 첫 갱신본이다. 175,000+ CVE·248개 CWE를 분석하여 수립되었다.

**10대 위험 (순서대로)**:
1. A01:2025 - Broken Access Control (모든 테스트 애플리케이션의 ~94% 영향)
2. A02:2025 - Security Misconfiguration
3. A03:2025 - Software Supply Chain Failures
4. A04:2025 - Cryptographic Failures
5. A05:2025 - Injection
6. A06:2025 - Insecure Design
7. A07:2025 - Authentication Failures
8. A08:2025 - Software or Data Integrity Failures
9. A09:2025 - Security Logging and Alerting Failures
10. A10:2025 - Mishandling of Exceptional Conditions

[주장] 2025판은 개별 코드 결함에서 시스템 수준의 설정·의존성·운영 위험으로 무게 중심을 옮겼다 [https://orca.security/resources/blog/owasp-top-10-2025-key-changes/].

---

## Microsoft SDL (Security Development Lifecycle)

[정의/규정] Microsoft는 SDL을 소프트웨어 개발의 모든 단계에 보안·프라이버시 요구사항을 내재화하는 형식화된 프로세스로 정의한다 [https://learn.microsoft.com/en-us/compliance/assurance/assurance-microsoft-security-development-lifecycle].

**5개 핵심 단계** [https://learn.microsoft.com/en-us/compliance/assurance/assurance-microsoft-security-development-lifecycle]:
1. **Requirements**: 데이터 유형·알려진 위협·규제·교훈에 기반해 보안·프라이버시 요구사항을 명문화·추적
2. **Design**: Data Flow Diagram(DFD) 작성, threat model 수립·유지 (Microsoft Threat Modeling Tool 사용)
3. **Implementation**: 보안 설정 환경·내장 보안 검사를 갖춘 도구로 코딩
4. **Verification**: 수동 리뷰·정적 코드 분석·이진 분석·credential scanner·암호화 검증·fuzz testing·configuration 검증·Component Governance 실행. 침투 테스트 수행.
5. **Release**: 점진적 릴리스 (Ring 0~3 구조)

**2개 지원 활동**: 개발 전 Training, 배포 후 Response (사건 대응·모니터링).

---

## STRIDE Threat Modeling

[정의/규정] STRIDE는 Microsoft가 1999년 Loren Kohnfelder·Praerit Garg가 개발한 threat modeling 방법론이다 [https://drata.com/learn/risk/stride-threat-model]. Data Flow Diagram(DFD) 상의 각 요소(프로세스·데이터 저장소·데이터 흐름·외부 엔티티)에 위협 카테고리를 할당한다.

**6개 위협 카테고리**:
- **Spoofing**: 정체성 위장
- **Tampering**: 시스템 내 데이터 무단 변경
- **Repudiation**: 통신의 진정성 부인
- **Information Disclosure**: 기밀 정보 노출
- **Denial of Service**: 시스템 정상 실행 방지
- **Elevation of Privilege**: 허가된 것 이상의 접근 획득

---

## OWASP ASVS & SAMM

[정의/규정] **ASVS** (Application Security Verification Standard)는 웹 애플리케이션 기술 보안 제어를 테스트하기 위한 기초이자 개발자용 보안 요구사항 목록이다 [https://owasp.org/www-project-application-security-verification-standard/]. 5.0 (2025년 5월)은 약 350개 요구사항을 17개 챕터에 걸쳐 포함한다. 3개 검증 레벨(1~3)로 구조화되며, 각 요구사항은 테스트 가능한 문장으로 표기된다.

[정의/규정] **SAMM** (Software Assurance Maturity Model)은 조직의 특정 위험에 맞춘 소프트웨어 보안 전략을 수립·실행하도록 안내한다 [https://owaspsamm.org/model/design/security-requirements/]. ASVS는 "무엇을 검증할 것인가"를 정의하고, SAMM은 "어떻게 그것을 검증할 프로세스를 구축할 것인가"를 정의한다.

---

## 시크릿·설정 관리

[정의/규정] 12-Factor App 방법론은 "configuration을 환경 변수에 저장하라"고 규정한다 [https://12factor.net/]. API 키·데이터베이스 암호 등 민감 자격증명을 코드에 내재하거나 버전 제어에 커밋하지 않아야 한다. 이는 환경 간(개발·스테이징·운영) 동일한 애플리케이션이 런타임에 설정만 주입받아 실행되도록 한다.

[정의/규정] **GitHub Secret Scanning**은 Git 히스토리 전체를 스캔하여 하드코딩된 자격증명을 식별한다 [https://docs.github.com/en/code-security/secret-scanning/about-secret-scanning]. API 키·암호·토큰·개인키·연결 문자열 등을 감지하고, 제휴 서비스 제공자에 고지·유효성 검증·사용자 정의 패턴 기반 감지·AI 기반 미구조 시크릿 감지를 수행한다. 공개 저장소는 자동 보호, 프라이빗 저장소는 GitHub Advanced Security 필수.

---

## SLSA (Supply-Chain Levels for Software Artifacts)

[정의/규정] SLSA는 Open Source Security Foundation이 정의한 공급망 보안 프레임워크로, 위변조 방지·무결성 개선·패키지·인프라 보안을 위한 표준·제어를 제공한다 [https://slsa.dev/]. 제조사·소비자 모두에게 유용하다: 제조사는 공급망을 강화할 수 있고, 소비자는 패키지 신뢰 여부를 판단할 수 있다.

**4개 레벨 (Build Track)** [https://checkmarx.com/glossary/what-is-the-slsa-framework/]:
- **L0**: Provenance 없음
- **L1**: 기본 provenance 확립, 빌드 시스템이 provenance 기록
- **L2**: 호스팅 빌드·디지털 서명 추가, 위변조 방지
- **L3**: 플랫폼 격리·기밀성 제어·검증된 보안 플랫폼

**핵심 개념 (Provenance)**: 소프트웨어 아티팩트의 생성 방식에 대한 메타데이터. 소스 코드·빌드 시스템·빌드 단계·실행자·실행 사유 포함.

---

## SAST·DAST

[정의/규정] **정적 분석 (SAST)**은 소스 코드를 실행하지 않고 분석하여 보안 결함을 식별한다. 자격증명 노출 감지·코드 결함 발견에 효과적이지만, 런타임 동작을 반영하지 못한다 [https://learn.microsoft.com/en-us/compliance/assurance/assurance-microsoft-security-development-lifecycle].

[정의/규정] **동적 분석 (DAST)**은 실행 중인 애플리케이션에 malformed·예상 밖의 데이터를 공급하여 취약점을 발견한다. API·파서 호출, 오류 처리 검증을 포함한다. SAST는 개발 단계, DAST는 QA·스테이징 단계에서 주로 수행된다.

---

## Shift-Left 보안

[정의/규정] **Shift-Left**는 보안 테스트·실행을 소프트웨어 개발 라이프사이클의 더 초기 단계로 옮기는 방식이다 [https://www.harness.io/harness-devops-academy/what-is-shift-left-security]. 용어는 Larry Smith가 2001년 품질 보증을 조기에 통합하는 일반 개념으로 처음 사용했고 [https://www.jit.io/resources/devsecops/what-is-shift-left-security], 전통적으로 개발 말미에 추가되던 보안을 초기 단계로 옮기는 것을 의미한다. 취약점을 후기에 발견하면 수정 비용이 크게 증가한다.

---

## 보안 사고 데이터

[데이터] **Verizon DBIR 2026** [https://www.verizon.com/business/resources/reports/dbir/]은 2024년 11월~2025년 10월 31,000+ 보안 사건·22,000+ 확인된 침해를 145개국에서 분석했다. 중요 발견:
- **소프트웨어 취약점이 초기 접근 벡터 1위** (31%, 전년 20%에서 상승) [https://www.verizon.com/about/news/breach-industry-wide-dbir-finds]
- **중간 패치 시간 32일 → 43일** (34% 증가) [https://connect.tenable.com/discussions/vulnerability-watch/key-findings-from-the-verizon-dbir-2026-slower-vulnerability-remediation-meets-f/111972]
- 성숙한 팀: 중간 수정 시간 6~7개월
- [주장] 위협 행위자들이 취약점 연구·대상 선택·도구 개발에 생성 AI 활용 중 [https://www.dataprise.com/resources/blog/the-2026-verizon-dbir-is-here/]

---

## AI 생성 코드 보안: CVE-2025-48757

[데이터] **CVE-2025-48757**은 2025년 5월 공개된 Lovable (AI 웹사이트 빌드 도구) 취약점이다 [https://blog.vibecoder.me/post-mortem-lovable-cve-2025-48757]. Supabase Row-Level Security(RLS) 정책 부재로 인해 인증되지 않은 공격자가 생성 애플리케이션의 임의 데이터베이스 테이블을 읽고 쓸 수 있었다.

[데이터] **규모**: 1,645개 공개 Lovable 앱 중 1,645개 스캔 결과 170개 앱에 303개 취약 엔드포인트 발견 (약 10%) [https://www.superblocks.com/blog/lovable-vulnerabilities]. 개인정보·금융 기록·API 토큰·관리자 자격증명 노출.

[주장] 근본 원인: 단일 애플리케이션의 결함이 아니라 AI 도구의 설계 패턴이었다. Lovable은 사용자가 명시적으로 요청하지 않는 한 RLS를 구현하지 않았고, 사용자는 RLS가 필요한지 알 보안 지식이 부족했다 [https://blog.vibecoder.me/post-mortem-lovable-cve-2025-48757]. 사건 후 Lovable은 코드 생성 파이프라인에 RLS를 기본값으로 포함하도록 갱신했다.

[주장] AI 생성 코드의 보안 부채는 정규 코드의 5배 초과라는 연구가 보고되었다 [https://labs.cloudsecurityalliance.org/research/csa-research-note-ai-codegen-vulnerability-debt-20260406-csa/].

---

## 출처 목록

> [1차] = 원저자·원기관 발행 / [2차] = 제3자의 정리·집계

- [1차] [OWASP Top 10:2025](https://owasp.org/Top10/2025/)
- [2차] [Orca Security - OWASP Top 10 2025 Key Changes](https://orca.security/resources/blog/owasp-top-10-2025-key-changes/)
- [1차] [Microsoft Security Development Lifecycle (SDL)](https://learn.microsoft.com/en-us/compliance/assurance/assurance-microsoft-security-development-lifecycle)
- [2차] [Drata - STRIDE Threat Model](https://drata.com/learn/risk/stride-threat-model)
- [1차] [OWASP Application Security Verification Standard](https://owasp.org/www-project-application-security-verification-standard/)
- [1차] [OWASP SAMM - Security Requirements](https://owaspsamm.org/model/design/security-requirements/)
- [1차] [12-Factor App - Config](https://12factor.net/)
- [1차] [GitHub Secret Scanning](https://docs.github.com/en/code-security/secret-scanning/about-secret-scanning)
- [1차] [SLSA - Supply-chain Levels for Software Artifacts](https://slsa.dev/)
- [2차] [Checkmarx - SLSA Framework](https://checkmarx.com/glossary/what-is-the-slsa-framework/)
- [1차] [Verizon DBIR 2026](https://www.verizon.com/business/resources/reports/dbir/)
- [1차] [Verizon - Breach Industry-Wide DBIR Finds](https://www.verizon.com/about/news/breach-industry-wide-dbir-finds)
- [2차] [Tenable - Verizon DBIR 2026 Key Findings](https://connect.tenable.com/discussions/vulnerability-watch/key-findings-from-the-verizon-dbir-2026-slower-vulnerability-remediation-meets-f/111972)
- [2차] [Dataprise - 2026 Verizon DBIR](https://www.dataprise.com/resources/blog/the-2026-verizon-dbir-is-here/)
- [2차] [Harness - What is Shift-Left Security](https://www.harness.io/harness-devops-academy/what-is-shift-left-security)
- [2차] [Jit - Shift-Left Security](https://www.jit.io/resources/devsecops/what-is-shift-left-security)
- [2차?] [Vibe Coder Blog - CVE-2025-48757 Post-Mortem](https://blog.vibecoder.me/post-mortem-lovable-cve-2025-48757)
- [2차] [Superblocks - Lovable Vulnerability Explained](https://www.superblocks.com/blog/lovable-vulnerabilities)
- [1차] [Cloud Security Alliance - AI Codegen Vulnerability Debt](https://labs.cloudsecurityalliance.org/research/csa-research-note-ai-codegen-vulnerability-debt-20260406-csa/)
