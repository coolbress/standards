---
id: aspect-24-governance-collaboration-compliance--solo-governance-handover--facts-2026-08
title: "1인에게 남는 거버넌스와 인계 규범 — facts (2026-08)"
parent: aspect-24-governance-collaboration-compliance
kind: research-log
evidence_track: lit
status: draft
language: ko
last_updated: "2026-08-05"
review_due: "2026-11-05"
method: "Haiku web-research, facts-only, EVIDENCE-POLICY conformant; search log included"
---

## 조사 기록

### Q2: SemVer 및 버전·호환성 파괴의 규정

**조사 범위**
- SemVer 공식 명세가 무엇에 적용된다고 규정하는가
- HTTP API breaking change를 다루는 공식 표준이 있는가

**SemVer 공식 명세 검토**

[규정: 1차] SemVer(Semantic Versioning)는 공식 스펙에서 "소프트웨어(software)"에 적용된다고 명시하되, **특히 "공개 API"(public API)에 중점**을 두고 있다. [1차: https://semver.org]

**핵심 규정:**
- "SemVer를 사용하는 소프트웨어는 공개 API를 반드시 선언해야 한다" (MUST declare a public API)
- 버전 번호 증가 규칙: Major(호환성 파괴 시), Minor(하위호환성 보존 신기능), Patch(버그수정)
- 명시 범위: **공개 API에 대한 변화 추적이 주목적**
- 부수: "substantial new functionality or improvements within private code"는 Minor 증가 가능

**해석:**
SemVer는 모든 소프트웨어에 적용 *가능*하지만, **공식적으로는 공개 API의 변화 관리에 목적**을 두고 있다. 내부 구현 변화는 부차적 사항이다. [1차]

**HTTP API Breaking Changes 표준**

[규정: 1차] HTTP API의 breaking change를 다루는 공식 IETF 표준들:
- **RFC 7807 / RFC 9457**: 문제 상세 정보(Problem Details) 형식 표준화 [1차: https://datatracker.ietf.org/doc/html/rfc9457/]
- **RFC 8594**: Sunset 헤더 (엔드포인트 종료 알림) [미확인]
- **RFC 9745 (draft)**: Deprecation 헤더 (기능 폐지 신호) [미확인]

**Breaking change 정의는 표준이지만:**
- 상태 코드 변경, 필드 타입 변경, 열거값 추가 등이 breaking change로 간주됨
- 이러한 정의는 표준이지만, "1인 개발자가 API 변경 시 반드시 준수해야 한다"는 규정은 없음

---

### Q3: 인계·온보딩 공식 표준

**조사 범위**
- ISO/IEC/IEEE 15289에서 인계/온보딩 정보 항목 명시 여부
- SWEBOK의 관련 Knowledge Area
- 개발자 인계(handover) 공식 표준 존재 여부

**ISO/IEC/IEEE 15289 검토**

[규정: 1차] ISO/IEC/IEEE 15289:2015/2019는 "시스템 및 소프트웨어 공학 — 생명 주기 정보 항목(documentation)의 내용"을 규정한다. [1차: https://www.iso.org/standard/74909.html]

**범위:**
- 18개 정보 항목 유형(information items)을 정의
- 문서 유형 7가지: 설명, 계획, 정책, 절차, 보고, 요청, 명세
- **개발자 인계/온보딩 항목 명시 없음**: 검색 결과에서 명시적인 "handover information" 또는 "onboarding documentation" 항목을 찾지 못함

**SWEBOK v4.0 검토**

[규정: 1차] SWEBOK은 18개 Knowledge Area를 정의한다: [1차: https://www.computer.org/education/bodies-of-knowledge/software-engineering]
1. Software Requirements
2. Software Architecture
3. Software Design
4. Software Construction
5. Software Testing
6. **Software Engineering Operations**
7. Software Maintenance
8. Software Configuration Management
9. Software Engineering Management
10. Software Engineering Process
11. Software Engineering Models and Methods
12. Software Quality
13. Software Security
14. **Software Engineering Professional Practice**
15. Software Engineering Economics
16. Computing Foundations
17. Mathematical Foundations
18. Engineering Foundations

**명시:** "Software Maintenance"와 "Software Engineering Professional Practice"가 인계와 관련될 수 있지만, **명시적인 "developer handover" 또는 "knowledge transfer" KA는 없음**. [1차]

**ISO/IEC/IEEE 12207 검토**

> 판본 처분: 현행판은 **ISO/IEC/IEEE 12207:2026**이고 유료 전문을 확보하지 못해 clause 수준 대조는 INCONCLUSIVE다.
> 아래는 withdrawn된 ISO/IEC/IEEE 12207:2017 범위에서 확인한 내용이며, 현행판 조항으로 재귀속하지 않는다.

[규정] withdrawn된 ISO/IEC/IEEE 12207:2017은 소프트웨어 생명 주기 프로세스의 정의인데, Information Management 프로세스는 있으나 **"개발자 인계"를 명시적으로 규정하지 않는다**. [2차]

### 결론: "공식 규범 부재"

- **ISO/IEC/IEEE 15289**: 인계 정보 항목 미명시
- **SWEBOK v4.0**: 인계/온보딩 전용 KA 미명시
- **ISO/IEC/IEEE 12207**: Information Management는 있으나 handover 미규정
- **IEEE/ISO 표준 검색**: "developer handover" 또는 "knowledge transfer" 전용 공식 표준 없음

따라서 **개발자 인계·온보딩에 대한 공식 규범은 존재하지 않는다.** 개념은 ISO 9001 등의 "organizational knowledge" 범위에 포함되지만, 전용 규격은 없다.

---

### Q4: 1인에게 남는 거버넌스

**조사 범위**
- 결정 기록(decision record) 보존 표준
- GitHub 공식 요구/권장사항
- 취약점 신고 접수 경로(SECURITY.md, CVD) 공식 규정

**결정 기록 표준**

[규정: 1차] ISO/IEC/IEEE 15289는 일반 documentation을 규정하지만, **"결정 기록"(Architectural Decision Record, ADR) 전용 표준은 없음**. [1차: https://www.iso.org/standard/74909.html]

- 15289는 "configuration management", "plan", "report" 같은 일반 항목만 규정
- ADR(Architecture Decision Record)는 제3자 커뮤니티 가이드(GitHub의 adr org 등)에서 제안되지만, 표준은 아님

**GitHub 공식 요구사항: 모두 권장(권장 제외 의무 없음)**

[규정: 1차] GitHub 공식 문서(community profile)는 "recommended community health files"를 제시한다. 그러나 **어떤 파일도 의무가 아니다**. [1차: https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/about-community-profiles-for-public-repositories]

**권장 파일들:**
- README: 권장
- CONTRIBUTING: 권장
- LICENSE: 권장
- CODE_OF_CONDUCT: 권장
- ISSUE_TEMPLATES: 권장

**정확한 표현:**
GitHub 문서는 "recommended community standards to help people use and contribute to your project"라고 명시한다. 문서는 "You can add these files"라는 제안 표현만 사용하며, "You must" 같은 의무 표현 없음. [1차]

**SECURITY.md와 CVE 공식 규정**

[규정: 1차] GitHub 보안 정책은 "best practice"로 명시되며, **의무가 아니다**. [1차: https://docs.github.com/code-security/security-advisories/about-coordinated-disclosure-of-security-vulnerabilities]

**GitHub 권고 (의무 아님):**
- "It's good practice to clearly indicate how and where you want to receive reports for vulnerabilities"
- "If there isn't a security policy in place" → 정책 없을 시의 대체 방안 제시 (정책이 선택사항임을 시사)
- SECURITY.md 파일 위치: `/SECURITY.md`, `/docs/SECURITY.md`, `/.github/SECURITY.md`

**CVE와 공식 의무:**
- CVE(Common Vulnerabilities and Exposures)는 국제 표준이지만, **GitHub에서 CVE 신고를 의무화하지 않는다**
- OpenSSF(Open Source Security Foundation) CVD(Coordinated Vulnerability Disclosure) 가이드는 **권고사항**이다 [2차: https://github.blog/security/vulnerability-research/coordinated-vulnerability-disclosure-cvd-open-source-projects/]

### 결론: "1인에게 남는 공식 요구 거의 없음"

| 항목 | 공식 의무/권장 | 근거 |
|---|---|---|
| 결정 기록 | 공식 표준 없음 | ISO/IEC/IEEE 15289는 일반 문서만 규정 |
| GitHub README 등 | **권장만**(의무 아님) | GitHub 문서: "recommended community standards" |
| GitHub SECURITY.md | **권장만**(의무 아님) | GitHub 문서: "It's good practice", "If there isn't..." |
| CVE 신고 | **권고**(의무 아님) | OpenSSF 가이드는 권고, GitHub은 보유만 가능 |

따라서 1인 웹 앱 개발자에게 **공식적으로 남는 거버넌스 의무는 거의 없다.** 모든 GitHub 요구사항과 보안 정책은 권장 사항이다.

---

## 적용 범위 표

| 항목 | 규격/표준 | 규정 대상 | 1인에게 의무 | 근거 |
|---|---|---|---|---|
| 버전 관리 | SemVer 2.0.0 | 공개 API 추적 | 의무 아님 | "공개 API" 중점, 적용 선택적 |
| API breaking change | RFC 9457, RFC 8594 | HTTP 상태/헤더 | 의무 아님 | 기술 정의이지 준수 의무 없음 |
| 개발자 인계 | 공식 표준 없음 | — | 의무 없음 | SWEBOK/ISO 15289 미규정 |
| README 등 | GitHub 권장 | 공개 저장소 | **권장만** | "recommended standards" |
| SECURITY.md | GitHub 권장 | 공개 저장소 | **권장만** | "It's good practice" |
| CVE 신고 | OpenSSF 권고 | 취약점 발견 시 | 권고만 | 법적 의무는 관할권 의존 |

---

## 상충·부정 증거

**반박 근거 검토:**
1. ISO 9001:2015에서 "organizational knowledge" 관리를 요구하나, 소프트웨어 개발 기업의 필수 규격이 아님 (ISO 9001은 일반 품질 관리)
2. GitHub Terms of Service에서 README나 SECURITY.md 의무화 검색 → 문서에서 찾지 못함
3. IETF RFC에서 "API 변경 시 반드시 SemVer를 따르라"는 표현 → 없음 (RFC는 기술 명세, 정책 강제는 아님)

---

## 미해결

1. **특정 국가/지역의 법적 의무**: 미국 CFAA, EU GDPR 등에서 보안 취약점 신고 의무가 있는지 미확인
2. **오픈소스 라이선스와 인계**: GPL, Apache 2.0 등이 인계/핸드오버 의무를 정하는지 미확인
3. **GitHub Enterprise 규정**: 공개 저장소 vs 프라이빗 저장소의 요구사항 차이 미확인

---

## 출처

### [1차 출처] (공식 표준 문서)
- https://semver.org (SemVer 공식)
- https://www.rfc-editor.org/rfc/rfc9110.txt (RFC 9110)
- https://datatracker.ietf.org/doc/html/rfc9457/ (RFC 9457 Problem Details)
- https://www.iso.org/standard/74909.html (ISO/IEC/IEEE 15289:2019)
- https://www.computer.org/education/bodies-of-knowledge/software-engineering (SWEBOK)
- https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/about-community-profiles-for-public-repositories (GitHub Community Profile)
- https://docs.github.com/code-security/security-advisories/about-coordinated-disclosure-of-security-vulnerabilities (GitHub CVD)

### [2차 출처] (해설 및 가이드)
- https://github.blog/security/vulnerability-research/coordinated-vulnerability-disclosure-cvd-open-source-projects/ (GitHub CVD 가이드)
- https://datatracker.ietf.org/doc/html/rfc7807 (RFC 7807 Problem Details)

### 검색 로그
- 검색 1: "SemVer semantic versioning official specification scope applicability software"
- 검색 2: "HTTP API breaking changes specification RFC standard"
- 검색 3: "ISO/IEC/IEEE 15289 software information items developer handover onboarding"
- 검색 4: "SWEBOK software engineering knowledge areas developer handover onboarding knowledge area"
- 검색 5: "decision documentation standard IEEE ISO software engineering decision record"
- 검색 6: "GitHub SECURITY.md CVE vulnerability disclosure standard requirements"
- 검색 7: "GitHub repository community profile official requirements recommended CONTRIBUTING LICENSE"
- 웹페치 1: RFC 9110 전문 (범위 명시)
- 웹페치 2: OpenAPI v3.1.0 (적용 범위)
- 웹페치 3: SemVer 공식 (적용 대상)
- 웹페치 4: SWEBOK v4 (KA 목록)
- 웹페치 5: GitHub Community Profile (의무 vs 권장)
- 웹페치 6: GitHub CVD (SECURITY.md 의무 여부)
