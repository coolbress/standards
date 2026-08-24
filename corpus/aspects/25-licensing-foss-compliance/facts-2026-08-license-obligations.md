---
id: aspect-25-licensing-foss-compliance--facts-2026-08-license-obligations
title: "라이선스 의무 조문과 식별·스캔 규정 — facts (2026-08)"
parent: aspect-25-licensing-foss-compliance
kind: research-log
evidence_track: lit
status: draft
language: ko
last_updated: "2026-08-05"
review_due: "2026-11-05"
method: "Haiku web-research, facts-only, EVIDENCE-POLICY conformant; search log included"
---

## 조사 기록

**질문 범위**: 라이선스 조문의 원문 (AGPL-3.0 §13, GPL-3.0, MIT, Apache-2.0); SPDX 식별자 및 REUSE 규격의 공식 요구사항; 의존성 라이선스 스캔 규정.

**제외**: 법적 해석, 의무 판단, 규정 권장.

**조사일**: 2026-08-05

**예산 사용**:
- Q3 라이선스 조문: 검색 4/6, fetch 4/8
- Q4 SPDX/REUSE/스캔: 검색 4/6, fetch 3/8
- **총 검색**: 8/12, **총 fetch**: 7/16

---

## 조문 인용표

| 라이선스 | 섹션 | 조항명 | 규범 강도 | 요구 내용 | 조건절 |
|---------|------|--------|----------|---------|--------|
| AGPL-3.0 | §13 | Remote Network Interaction | MUST | "프로그램을 원격으로 상호작용하는 경우, 사용자에게 대응 소스(Corresponding Source)를 받을 수 있는 기회를 저명하게 제공해야 한다" | 수정된 프로그램이 컴퓨터 네트워크를 통한 원격 상호작용을 지원하는 경우 |
| GPL-3.0 | §1-§5 | Distribution & Notice | MUST | "모든 사본에 저작권 공지와 라이선스 사본을 포함해야 한다; 수정 시 명시적 공지를 포함해야 한다" | 프로그램 배포 시 |
| MIT | (전체) | Notice Requirement | MUST | "소프트웨어의 모든 사본 또는 실질적 부분에 저작권 공지와 허가 공지를 포함해야 한다" | 배포 시 |
| Apache-2.0 | §4(a) | License Copy | MUST | "라이선스 사본을 배포해야 한다" | 저작물 재배포 시 |
| Apache-2.0 | §4(b) | Modification Notice | MUST | "수정된 파일은 수정을 명시하는 저명한 공지를 포함해야 한다" | 파일 수정 시 |
| Apache-2.0 | §4(c) | Source Attribution | MUST | "저작권, 특허, 상표, 귀속 공지를 원본 작업에서 유지해야 한다" | Derivative Works 배포 시 |
| Apache-2.0 | §4(d) | NOTICE File | MUST | "NOTICE 파일이 있으면 읽을 수 있는 귀속 공지 사본을 포함해야 한다" | NOTICE 파일이 원본에 있는 경우 |

---

## Q3: 라이선스 조문 원문 및 요구사항

### Q3a: AGPL-3.0 Section 13 (Remote Network Interaction)

**[원문 요약]** SPDX 공식 데이터베이스에서 추출 ([1차: https://spdx.org/licenses/AGPL-3.0.html]):

> "If you modify the Program, your modified version must prominently offer all users interacting with it remotely through a computer network an opportunity to receive the Corresponding Source of your modified version."

**[규범 강도]**: SHALL (의무)

**[주요 요구사항]**:
1. "네트워크 서버를 통해 표준적이고 관례적인 소프트웨어 복사 수단으로 대응 소스(Corresponding Source)에 접근할 수 있도록 제공해야 한다" ([1차: https://spdx.org/licenses/AGPL-3.0.html])
2. 네트워크 "루프홀" 방지 — 공개 서버에서 수정된 버전을 배포하는 경우 소스 공개 의무 ([1차: https://spdx.org/licenses/AGPL-3.0.html])

**[조건절]**: 프로그램이 "수정되었고" 컴퓨터 네트워크를 통한 "원격 상호작용을 지원하는 경우"

---

### Q3b: GPL-3.0 Notice Requirements

**[원문 요약]** SPDX 공식 데이터베이스에서 추출 ([1차: https://spdx.org/licenses/GPL-3.0-or-later.html]):

> "Each copy must display 'an appropriate copyright notice' prominently on the work itself; keep intact all notices stating that this License and any non-permissive terms apply; give all recipients a copy of this License along with the Program."

**[규범 강도]**: SHALL (의무)

**[세부 공지 요구사항]**:
1. **저작권 공지**: 모든 사본에 저명하게 표시 ([1차: https://spdx.org/licenses/GPL-3.0-or-later.html])
2. **라이선스 진술**: "이 라이선스와 §7에 따른 비허가 조건이 코드에 적용된다는 공지를 유지해야 한다" ([1차: https://spdx.org/licenses/GPL-3.0-or-later.html])
3. **보증 부재 공지**: "모든 보증 부재 공지를 보존하고 수신자에게 표시해야 한다" ([1차: https://spdx.org/licenses/GPL-3.0-or-later.html])
4. **수정 공지**: 수정된 코드 배포 시 "수정된 부분과 시기를 명시적으로 공지해야 한다" ([1차: https://spdx.org/licenses/GPL-3.0-or-later.html])

**[권고 지침]** FSF 권고: 각 소스 파일 시작 부분에 다음을 포함하는 보일러플레이트를 첨부:
- 프로그램 설명
- 저작권 정보
- 전체 GPL-3.0 텍스트 참조

([미확인]: 검색 결과만 확인, FSF 공식 페이지 원문 미열람)

**[조건절]**: 프로그램 배포 시 (이진 또는 소스)

---

### Q3c: MIT License Notice Requirement

**[원문 (완전)]** Open Source Initiative 공식 페이지에서 확인 ([1차: https://opensource.org/license/mit]):

> "The above copyright notice and this permission notice (including the next paragraph) shall be included in all copies or substantial portions of the Software."

**[규범 강도]**: SHALL (의무)

**[포함 요구사항]**:
1. 저작권 공지 (연도 및 저작권자 포함)
2. MIT 허가 공지 전체 텍스트

**[범위]**: "모든 사본 또는 실질적 부분" — 배포된 모든 버전에 필수; 모든 개별 파일이 아니라 "실질적 부분"에 포함 ([1차: https://opensource.org/license/mit])

**[책임 부인]**: 또한 포함: "THE SOFTWARE IS PROVIDED 'AS IS,' WITHOUT WARRANTY OF ANY KIND...IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE..." (조건이 아닌 이용 조건, 하지만 비공시는 위반) ([1차: https://opensource.org/license/mit])

**[조건절]**: 소프트웨어 배포 시

---

### Q3d: Apache-2.0 License Notice and Attribution Requirements

**[원문 — Section 4]** Apache Software Foundation 공식 라이선스에서 추출 ([1차: https://www.apache.org/licenses/LICENSE-2.0.html]):

#### §4(a): License Copy
> "You must give any other recipients of the Work or Derivative Works a copy of this License"

**[규범 강도]**: SHALL

#### §4(b): Modification Notice
> "You must cause any modified files to carry prominent notices stating that You changed the files"

**[규범 강도]**: SHALL

#### §4(c): Source Attribution
> "You must retain, in the Source form of any Derivative Works that You distribute, all copyright, patent, trademark, and attribution notices from the original work"

**[규범 강도]**: SHALL

**[제외 허용]**: "귀속이 귀 변경과 무관한 경우는 제외"

#### §4(d): NOTICE File Handling
> "If the original Work includes a NOTICE file, you must include a readable copy of the attribution notices contained within such NOTICE file in your distributed Derivative Works, placed in at least one of:
> - within a NOTICE text file distributed as part of the Derivative Works
> - within the Source form or documentation
> - within a display generated by the Derivative Works"

**[규범 강도]**: SHALL

**[조건절]**: 
- (a)(c): Derivative Works 배포 시
- (b): 파일 수정 시
- (d): 원본에 NOTICE 파일이 있는 경우

---

## Q4: SPDX 식별자 및 REUSE 규격 요구사항

### Q4a: SPDX 라이선스 식별자

**[정의]** SPDX 공식 스펙 ([1차: https://spdx.github.io/spdx-spec/v2.3/using-SPDX-short-identifiers-in-source-files/]):

**[형식 요구]**: `SPDX-License-Identifier: <SPDX License Expression>`

**[규범 강도]**: SHOULD (권고)

**[배치]**:
- "파일 시작 또는 근처에 배치" (권고)
- "일반적으로 주석 부분에 나타나야 함" (권고)
- "자체 라인에 나타나야 함" (규범: MUST)

**[내용 규정]**:
1. **단일 라이선스**: SPDX 라이선스 리스트의 단축 식별자 (예: `MIT`)
2. **버전 지정**: "+" 연산자로 "또는 이후" 버전 표시 가능 (예: `MIT+`)
3. **다중 라이선스**: OR/AND/WITH 연산자 사용하여 표현식 구성
   - OR: 선택적 라이선스
   - AND: 동시 라이선스
   - WITH: 예외 식별자 (예: `GPL-2.0-only WITH Classpath-exception-2.0`)
4. **줄 바꿈 금지**: "표현식은 단일 라인에 있어야 하며 중간에 줄 바꿈이 없어야 한다" (규범: MUST) ([1차: https://spdx.github.io/spdx-spec/v2.3/using-SPDX-short-identifiers-in-source-files/])

**[사용자 정의 라이선스]**: SPDX 리스트에 없는 라이선스는 `LicenseRef-` 형식 사용 (예: `SPDX-License-Identifier: LicenseRef-my-license`); 대응 라이선스 텍스트 제공 필요

---

### Q4b: REUSE Specification 3.3

**[목표]** Free Software Foundation Europe (FSFE)에서 정의 ([1차: https://reuse.software/spec-3.3/]):

> "comprehensive, unambiguous, human- and machine-readable copyright and licensing information for each individual file"

**[규범 강도]**: 사양(specification)이므로 MUST

**[적용 대상 파일]**: "모든 프로젝트 파일" (다음 제외):
- `LICENSES/` 디렉토리의 라이선스 파일
- 버전 관리 시스템 파일
- 서브모듈 및 Meson 서브프로젝트
- `REUSE.toml` 파일 및 `.reuse/` 디렉토리
- 0바이트 파일 및 심볼릭 링크

**[파일별 요구사항]** 각 대상 파일은 반드시 포함:
1. **저작권 공지** — 저작권자 이름 포함; 이상적으로는 연도 및 연락처도
2. **SPDX 라이선스 식별자** — "유효한 SPDX 라이선스 표현식"

**[구현 방법]** (세 가지 옵션):
1. **주석 헤더** (권장): 파일 또는 `.license` 동반 파일에 직접 포함
2. **REUSE.toml**: 중앙집중식 구성 파일, glob 패턴 사용
3. **DEP5** (더 이상 권장 안 함): 폐기된 대체 방식

**[라이선스 파일 요구사항]**: "프로젝트는 대상 파일이 라이선스되는 모든 라이선스에 대해 라이선스 파일을 포함해야 한다" — `LICENSES/` 디렉토리에 SPDX 식별자를 파일명으로 저장 (예: `LICENSES/MIT.txt`)

([1차: https://reuse.software/spec-3.3/])

---

### Q4c: 의존성 라이선스 스캔 규정

**[SBOM 표준]** Software Bill of Materials는 의존성 라이선스 문서화의 표준 형식 ([미확인]: 검색 스니펫만 확인, 공식 스펙 문서 미열람):

**[CycloneDX 스펙]** OWASP CycloneDX는 SBOM 표준 ([1차: https://cyclonedx.org/]):
- 라이선스는 CISA 2026 SBOM 최소 요소로 지정 ([미확인]: 검색 스니펫만 확인, 원문 미열람)
- "ECMA-424 표준"으로 공식화 ([미확인]: 스펙 본문 미확인)
- CycloneDX와 SPDX는 CRA(Cyber Resilience Act) 기계 판독 가능 SBOM 요구사항을 충족 ([미확인]: 검색 스니펫만 확인)

**[의존성 스캔 기능 요구]** (공식 표준이 아닌 실무 기준):
- SCA(Software Composition Analysis) 도구는 전체 의존성 트리 해석 필요 ([미확인]: 검색 스니펫만 확인)
- 직접 및 전이 의존성의 모든 패키지에 라이선스 첨부 필요

**[정책 요구]**: 라이선스 정책은 승인/금지 라이선스 및 예외 처리 규정 ([미확인]: 검색 스니펫만 확인) — 정책 부재 시 각 라이선스 결정이 임시성을 띤다

---

## 상충 및 부정 증거

없음. 모든 주요 라이선스 조문이 공식 출처에서 일관되게 공지 요구사항을 명시함.

---

## 미해결

1. **GPL-3.0 보일러플레이트 권고**: FSF 권고 (검색 결과 스니펫만 확인); FSF 공식 페이지 원문 미열람 ([미확인]).

2. **CycloneDX 스펙 본문**: 라이선스 정보 필드의 기술적 세부사항 (예: 필수 필드 이름, 형식 제약) 미확인. 공식 스펙 문서 자체 필요 ([미확인]: CycloneDX 메인 페이지는 개괄만 제공).

3. **SBOM 최소 요소**: CISA 2026 SBOM 최소 요소 지정 (검색 스니펫만 확인); 원문 미열람 ([미확인]).

4. **의존성 스캔 도구 요구사항**: SCA 도구의 의존성 트리 해석 및 라이선스 첨부 요구사항 (검색 스니펫만 확인); 공식 표준이 아닌 실무 관행임 ([미확인]).

5. **의존성 스캔의 규범 강도**: SBOM 최소 요소 지정은 CRA 규정이지, 모든 프로젝트에 "MUST" 요구하는 라이센싱 표준이 아님. 법적 의무 구분 필요.

6. **REUSE 채택 규범**: REUSE 사양은 권장 관행이지, 라이선스 법에 의해 의무화된 표준이 아님 (AGPL/GPL/MIT/Apache는 의무; REUSE는 준수 도구).

---

## 출처

### 1차 (공식 조문 및 스펙)

#### 라이선스 조문
- [SPDX: AGPL-3.0](https://spdx.org/licenses/AGPL-3.0.html) — GNU Affero GPL v3.0 공식 텍스트
- [SPDX: GPL-3.0-or-later](https://spdx.org/licenses/GPL-3.0-or-later.html) — GNU GPL v3.0 공식 텍스트
- [Open Source Initiative: MIT License](https://opensource.org/license/mit) — MIT 공식 텍스트
- [Apache Software Foundation: License 2.0](https://www.apache.org/licenses/LICENSE-2.0.html) — Apache-2.0 공식 텍스트

#### SPDX 식별자
- [SPDX Specification v2.3: Using SPDX Short Identifiers in Source Files](https://spdx.github.io/spdx-spec/v2.3/using-SPDX-short-identifiers-in-source-files/) — 공식 스펙

#### REUSE 규격
- [REUSE Specification 3.3](https://reuse.software/spec-3.3/) — FSFE 공식 스펙

#### SBOM 및 의존성 스캔
- [CycloneDX Official](https://cyclonedx.org/) — OWASP CycloneDX 공식 페이지 (상세 스펙 링크 포함)

### 2차 (해석, 요약, 가이드)

- [Free Software Foundation News: AGPLv3 Release](https://www.fsf.org/news/agplv3-pr)
- [FOSSA: Open Source Software Licenses 101 - GPL v3](https://fossa.com/blog/open-source-software-licenses-101-gpl-v3/)
- [Sbomify: MIT License Guide](https://sbomify.com/2026/01/22/mit-license-guide/)
- [Sbomify: Apache License 2.0 Guide](https://sbomify.com/2026/01/07/apache-license-2-guide/)
- [Mend: Top 10 Questions About The Apache License](https://www.mend.io/blog/top-10-apache-license-questions-answered/)
- [Kiuwan: SBOM Standards Complete Guide](https://www.kiuwan.com/blog/sbom-standards/)
- [Wiz: Guide to Standard SBOM Formats](https://www.wiz.io/academy/application-security/standard-sbom-formats)


### 미확인

- **CycloneDX 기술 명세 상세**: ECMA-424 표준 본문 미확인
- **의존성 스캔 공식 표준**: 라이선스 스캔을 규정하는 특정 공식 표준이 있는지 불명확 (SBOM 최소 요소는 CRA 규제이지 라이선싱 표준이 아님)
