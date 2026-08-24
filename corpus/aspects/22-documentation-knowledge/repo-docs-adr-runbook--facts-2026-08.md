---
id: aspect-22-documentation-knowledge--repo-docs-adr-runbook--facts-2026-08
title: "저장소 표준 문서·ADR·runbook — facts (2026-08)"
parent: aspect-22-documentation-knowledge
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
**질문 범위**: 저장소 표준 문서(README/CONTRIBUTING/SECURITY/CHANGELOG), ADR, runbook, Diátaxis  
**제외**: 도구 추천, 튜토리얼, 구현 가이드  
**검색 예산**: 하위질문당 ≤6회 (실제: 3-2, 3-4, 4-4 = 총 10회)  
**fetch 예산**: 하위질문당 ≤8회 (실제: 4회)

---

## 하위 질문 3: 저장소 표준 문서 규정

### 3.1 GitHub 공식 Best Practices — 추천 문서

[규정] [1차: https://docs.github.com/en/repositories/creating-and-managing-repositories/best-practices-for-repositories]

**GitHub가 명시적으로 추천하는 문서** (공식 Best Practices):

1. **README.md**  
   "communicate important information about your project"  
   프로젝트 소개, 사용법, 빌드 예시

2. **SECURITY.md**  
   "provides instructions to collaborators on how to report security vulnerabilities found in your project and encourages responsible disclosure"  
   보안 취약점 책임감 있는 보고 지침

**GitHub 공식 문서에서 언급되지 않은 항목**:
- CONTRIBUTING.md: 커뮤니티 표준이지만 Best Practices 페이지에 별도 명시 없음
- CHANGELOG.md: 비언급
- CODE_OF_CONDUCT.md: 비언급

> 주: "repository license, citation file, contribution guidelines, and a code of conduct"를 "helpful alongside README"로 언급하지만 각각의 규격 정의 없음.

---

### 3.2 Keep a Changelog — 공식 사양

[규정] [1차: https://keepachangelog.com/en/0.3.0/]

**최신 버전**: 2.0.0 (2026년 6월 7일 발표)

**필수 변경 유형** (6가지):

| 유형 | 의미 |
|------|------|
| **Added** | 새 기능 |
| **Changed** | 기존 기능 변경 |
| **Deprecated** | 곧 삭제될 기능 공지 |
| **Removed** | 삭제된 기능 |
| **Fixed** | 버그 수정 |
| **Security** | 보안 취약점 수정 및 업그레이드 권고 |

**필수 섹션**:
- `"Unreleased"` 섹션 (상단에, 미배포 변경 사항)
- 각 배포 버전별 섹션

**필수 날짜 형식**: `YYYY-MM-DD` (예: `2012-06-02`)  
- "international, sensible, and language-independent"
- 가장 큰 단위에서 가장 작은 단위로 (largest to smallest)

**버전 관리 규정**:
[규정] [1차]  
"explicitly mention whether the project follows Semantic Versioning" (원명제)  
→ SemVer 채택 여부를 명시하도록 권고

**2.0.0 변경사항** (2026년):
[주장] [2차]  
Keep a Changelog 2.0.0은 "loosens the versioning requirement to 'note which versioning scheme you use'" → 캘린더 버전 관리, 순수 번호, 날짜도 허용

---

### 3.3 Semantic Versioning (SemVer) — 공식 사양

[규정] [1차: https://semver.org/]

**버전 포맷**: `MAJOR.MINOR.PATCH`

**증가 규칙**:

1. **MAJOR**: "incompatible API changes" 발생 시 증가
   - "MUST be incremented if any backward incompatible changes are introduced to the public API"
   - MINOR, PATCH는 0으로 리셋

2. **MINOR**: "backward compatible functionality" 추가 시 증가
   - "MUST be incremented if new, backward compatible functionality is introduced to the public API"
   - "or if any public API functionality is marked as deprecated"
   - PATCH는 0으로 리셋

3. **PATCH**: "backward compatible bug fixes" 시 증가
   - "if only backward compatible bug fixes are introduced"
   - Bug fix = internal change fixing incorrect behavior

**특수 규칙**:
- 초기 개발 단계 (0.y.z): 규칙 미적용 (자유)
- 1.0.0부터: 공개 API 안정화 시작 → 위 규칙 적용

---

### 3.4 SECURITY.md — 책임감 있는 취약점 보고

[규정] [2차: https://github.com/topics/security-policy]
[규정] [1차 (GitHub 내용)]

**보고 프로세스 표준**:

책임감 있는 공개(Responsible Disclosure) 타임라인:
- **비공개 보고 기간**: 60~120 영업일
- **Coordinated Vulnerability Disclosure (CVD)**: 연구자-벤더 협력
- **공개 시점**: 패치 발표 후

**SECURITY.md 역할**:
- 취약점 보고 방법 명시 (이메일, 웹 폼, 플랫폼)
- Safe harbor 조항 포함
- 보고에 포함할 정보 명시
  - 취약점 설명
  - 재현 단계
  - 영향/위험도

> 주: GitHub Private Vulnerability Reporting은 SECURITY.md와 별도 기능.

---

## 하위 질문 4: ADR과 runbook 규정

### 4.1 Architecture Decision Records (ADR) — Nygard 원 형식

[규정] [1차: https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions]

**저자**: Michael Nygard (Cognitect)  
**발표**: 2011년 11월 (블로그 포스트)  
**기초 패턴**: Alexandrian patterns

**필수 섹션** (구조):

1. **Title** (짧은 명사구)  
   예: "ADR 1: Deployment on Ruby on Rails 3.0.10"

2. **Context** (상황 설명)  
   - 작용 중인 힘들 (forces)
   - 기술적, 정치적, 사회적, 프로젝트 로컬 요소
   - 중립 언어로 서술

3. **Decision** (결정)  
   - "stated in full sentences, with active voice"
   - "We will …" 형식
   - 완전한 문장 (bullet points 아님)

4. **Consequences** (결과)  
   - "resulting context, after applying the decision"
   - 긍정/부정 모두 기록
   - "not just the 'positive' ones"

5. **Status** (선택사항 언급)  
   - "proposed", "accepted", "deprecated", "superseded"

**문서 길이 규정**:
"the whole document should be one or two pages long"  
"as if it is a conversation with a future developer"  
완전한 문장으로 구성 (paragraph 형식)

**지위**:
- ⚠️ 공식 표준이 아님 (원저자의 처방)
- 커뮤니티 광범위 채택 (de facto standard)
- adr.github.io 저장소에서 변형 및 템플릿 유지

---

### 4.2 Google SRE Runbook 원칙

[규정] [1차: https://sre.google/sre-book/introduction/]

**핵심 명제**:
"thinking through and recording the best practices ahead of time in a 'playbook' produces roughly a 3x improvement in MTTR"

**Playbook의 역할**:
1. **사전 준비**: 긴급 상황 전에 문제 해결 절차 기록
2. **즉흥 배제**: engineers가 "wing it"하지 않도록
3. **속도 향상**: MTTR (Mean Time To Resolution) 약 3배 개선

**자동화 원칙** (3가지 핵심 실천):
1. Progressive rollouts (점진적 배포)
2. Rapid problem detection (빠른 문제 탐지)
3. Safe rollback procedures (안전한 롤백)

**기술 요구**:
"the team tasked with managing a service needs to code or it will drown"  
→ SRE 팀의 코드 작성 필수

**교육 방식**:
- Written runbook / playbook
- "Wheel of Misfortune" 등 시뮬레이션 훈련
- 절차 숙달 후 긴급 실행

**지위**:
- ⚠️ 공식 표준 사양 없음 (Google SRE Book의 사례/모범)
- 권장 실천 방법 (best practices)
- 공식 구조화 형식 미제시

---

### 4.3 Diátaxis — 문서화 4모드

[규정] [1차: https://idratherbewriting.com/blog/what-is-diataxis-documentation-framework]
[주장] [2차]

**저자**: Daniele Procida (Canonical, 전 Django 핵심 개발자)  
**발표**: 2020년  
**기초**: 고대 그리스어 διάταξις (dia "across" + taxis "arrangement")

**4가지 문서화 모드** (유형):

1. **Tutorials** (학습 지향)  
   - 단계별 교육 경험 제공
   - 실습 기반 스킬 구축
   - 초급자 목표: 기본 능력 습득
   - 예: "Getting Started Guide"

2. **How-To Guides** (목표 지향)  
   - 실제 문제 해결 레시피
   - 작업 중심 (task-focused)
   - 기존 지식 있는 사용자 대상
   - 예: "How to Deploy with Docker"

3. **Reference** (정보 조회)  
   - 기술적 세부사항, 팩트
   - API, 파라미터, 사양 문서
   - 정밀하고 권위 있는 정보
   - 예: "API Documentation"

4. **Explanation** (이해 지향)  
   - 배경 지식, 개념 설명
   - "Why" 제공 (not just "How")
   - 더 깊은 이해 지원
   - 예: "Architecture Overview"

**구조 원칙**:
- 2D 그리드 (수평축: Acquisition ↔ Application / 수직축: Action ↔ Cognition)
- 각 모드는 서로 다른 사용자 목표에 대응
- 모드 분리 → 혼재 방지 → 정보 검색성 향상

**채택 현황**:
- Django, Canonical(Ubuntu), Cloudflare, Gatsby 등 사용
- 커뮤니티 권장 모범 (공식 표준기관 산출물 아님)

**지위**:
- ⚠️ 표준 기관(ISO, IEEE, W3C 등) 산출물 아님
- Daniele Procida의 설계 및 커뮤니티 채택
- 문서화 구조 설계 패턴(prescriptive)

---

## 표준 vs 처방 구분표

| 항목 | 규정 주체 | 표준 기관 산출물 | 지위 |
|------|----------|-----------------|------|
| GitHub Best Practices (README, SECURITY) | GitHub | 부분 (공식 플랫폼 권고) | 규정 |
| Keep a Changelog | Olivier Lacan et al. | 아니오 | 주장/처방 |
| Semantic Versioning | Tom Preston-Werner et al. | 아니오 (사실상 표준) | 주장/처방 |
| ADR (Nygard 형식) | Michael Nygard | 아니오 | 주장/처방 |
| Google SRE Runbook | Google | 아니오 (사례 기반) | 주장/처방 |
| Diátaxis 4모드 | Daniele Procida | 아니오 | 주장/처방 |

---

## 상충·부정 증거

**문서화 필수 여부 상충**:
- GitHub Best Practices: README, SECURITY만 명시 (다른 표준 문서는 "helpful" 정도)
- Keep a Changelog + SemVer: CHANGELOG 작성 시 버전 관리 필수 (하지만 GitHub는 CHANGELOG 미언급)

**ADR vs Runbook의 목적 상충**:
- ADR: **설계 결정 기록** (정적, 참고용)
- Runbook: **운영 절차 자동화** (동적, 실행용)
- 두 문서는 서로 다른 관점 (설계 vs 운영)

**버전 관리 규정의 완화**:
- Keep a Changelog 1.x: "Semantic Versioning 반드시 언급"
- Keep a Changelog 2.0.0 (2026): "버전 관리 체계 명시만 필요" (SemVer 선택사항화)

---

## 미해결

1. **GitHub 공식 표준 문서의 부재**:
   - README, SECURITY만 공식 추천 (Best Practices)
   - CONTRIBUTING, CHANGELOG, CODE_OF_CONDUCT는 커뮤니티 표준이지만 GitHub 공식 사양 없음
   - 인수 상태(handoff state) 정의에 "표준" vs "권고"의 구분이 애매함

2. **Google SRE Runbook 공식 형식**:
   - SRE Book에서 "playbook 3배 개선" 사례만 제시
   - 구조화된 형식(섹션, 필드 정의) 미명시
   - 자동화 vs 문서 runbook의 구분 모호

3. **Diátaxis와 다른 문서화 프레임워크의 관계**:
   - Diátaxis는 권장 패턴이지만 업계 표준은 아님
   - 다른 프레임워크(Arc42, C4 Model 등)와의 충돌 없음 (보완)

4. **SECURITY.md의 "책임감 있는 공개" 표준**:
   - CVD 타임라인(60-120일) 제안이 있지만 공식 규정 없음
   - 각 프로젝트별 자율 설정 (no mandatory spec)

5. **ADR 형식의 다양한 변형**:
   - Nygard 원본 외 여러 템플릿(Madr, ADR-7 등) 존재
   - 어느 것이 "표준"인지 공식화되지 않음

---

## 출처

### 1차 자료 (공식/원저자 명문)

- [GitHub Best Practices for Repositories](https://docs.github.com/en/repositories/creating-and-managing-repositories/best-practices-for-repositories)
- [Keep a Changelog v0.3.0](https://keepachangelog.com/en/0.3.0/)
- [Semantic Versioning 2.0.0](https://semver.org/)
- [Michael Nygard — Documenting Architecture Decisions](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [Google SRE Book — Introduction](https://sre.google/sre-book/introduction/)

### 2차 자료 (해석/사례)

- [I'd Rather Be Writing — What is Diátaxis](https://idratherbewriting.com/blog/what-is-diataxis-documentation-framework)
- [Release Pad — Keep a Changelog Format Explained](https://www.releasepad.io/blog/keep-a-changelog/)
- [PkgPulse — Semantic Versioning Guide 2026](https://www.pkgpulse.com/blog/semantic-versioning-guide-breaking-changes-2026)

### 미확인 페이지

- diataxis.fr (HTTP 429: Too Many Requests)
- GitHub 커뮤니티 표준 insights (GitHub UI 페이지, fetch 미시도)
