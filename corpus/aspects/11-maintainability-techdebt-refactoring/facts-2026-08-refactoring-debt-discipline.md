---
id: aspect-11-maintainability-techdebt-refactoring--facts-2026-08-refactoring-debt-discipline
title: "리팩터링 규율과 기술부채 추적 — facts (2026-08)"
parent: aspect-11-maintainability-techdebt-refactoring
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
- 하위질문 2개: (Q1) 리팩터링 분리 규정, (Q2) 기술부채 등록·추적 규정
- 공식 1차 출처: Fowler 공식사이트, Google 공식 엔지니어링 문서, SWEBOK v4, ISO/IEC 25010, CISQ
- 제외: 도구 추천, 튜토리얼, goppi 설계 결정

### 검색 예산 사용 (2026-08-05)
| 구분 | 질문 1 | 질문 2 | 합계 |
|------|--------|--------|------|
| 검색 | 2/4 | 4/4 | 6/8 |
| fetch | 3/3 | 2/3 | 5/6 |
| 상태 | ✓ 완료 | ✓ 완료 (문서 전문 제한) | - |

---

## Q1 — 리팩터링과 행동 변경의 분리: 공식 규정과 강도

### 정의 — Martin Fowler (공식 사이트)

**[정의] Fowler 리팩터링의 핵심 원칙**

- **명사 정의**: "소프트웨어의 관찰 가능한 행동을 바꾸지 않으면서 내부 구조를 변경하여 이해하기 쉽고 수정하기 저렴하게 만드는 변경"
- **동사 정의**: "관찰 가능한 행동을 바꾸지 않으면서 일련의 리팩터링을 적용하여 소프트웨어를 재구성하는 것"

**[규정] 분리 원칙 (Fowler)**  
Fowler는 "두 활동을 의식적으로 번갈아 수행한다"고 명시:
1. 기능을 추가하거나
2. 리팩터링을 수행한다

리팩터링 중에는 기능을 추가하지 않으며, 심지어 테스트도 놓친 경우가 아니면 추가하지 않음. 이 원칙은 **정의적 분리** — 리팩터링 ≠ 행동 변경이라는 수학적 분리.

**[1차: https://martinfowler.com/bliki/DefinitionOfRefactoring.html]**

---

### 규정 — Google 공식 엔지니어링 관행

**[규정] Google의 "분리 권장"**

Google의 공식 `eng-practices` 문서 (Small CLs 가이드):

> "It's usually best to do refactorings in a separate CL from feature changes or bug fixes."

**강도**: "usually best" = 권장 관행 (의무 규정 아님)  
**예외**: 소규모 정리 (로컬 변수 이름 변경 등)는 기능/버그 수정 커밋에 함께할 수 있음. 큰 리팩터링 (클래스 이동, 이름 변경)은 별도 검토 필요.

**[1차: https://google.github.io/eng-practices/review/developer/small-cls.html]**

### 보충 — Google LSC (대규모 변경)

**[규정] 자동화된 동작 보존 변경**

Google SWE 책 (ch22, Large-Scale Changes):
- LSC는 "의미 보존 기계 생성 변경" (semantic-preserving, machine-generated)
- 목표: 명확성·최적화·향후 호환성을 위한 광범위 텍스트 업데이트
- 검증: 포괄적 테스트가 리팩터링이 의도하지 않은 행동 변경을 도입하지 않음을 확인

**[1차: https://abseil.io/resources/swe-book/html/ch22.html]**

---

### 종합: Q1

| 규정 출처 | 규정 내용 | 강도 | 적용 범위 |
|---------|---------|------|---------|
| Fowler (공식) | 행동 변경과 리팩터링을 의식적으로 분리 | 원칙 (정의적) | 모든 개발 |
| Google (공식) | 일반적으로 리팩터링을 별도 CL로 분리 | 권장 (의무 아님) | 소규모 정리 제외 |

**미해결 없음.**

---

## Q2 — 기술부채의 등록·추적: 공식 표준의 의무 여부

### ISO/IEC 25010 — Maintainability

**[정의] ISO/IEC 25010 (2023판)**

9개 품질 특성: 기능 적합성, 성능 효율성, 호환성, 상호작용 능력, 신뢰성, 보안, 유지보수성, 유연성, 안전성.

**[규정] 유지보수성 정의**  
ISO 25010은 유지보수성을 특성으로 정의하지만, **부채 기록·추적 의무 명시 없음**.

프레임워크는 "연속 코드 검토, 정적 분석, 코드 정리, 리팩터링, 자동 테스트"를 통해 부채 감소를 권장하지만, 추적 메커니즘은 조직 결정.

**[2차 (벤더): https://www.sonarsource.com/resources/library/iso-iec-25010-explained/]**

**한계**: ISO/IEC 25010의 1차 출처(ISO 카탈로그)는 유료. 카탈로그 수준만 확인 가능.

### SWEBOK v4 — Software Maintenance KA

**[규정] SWEBOK v4 (2024년 10월 발표)**

Software Maintenance Knowledge Area는:
- 비용 효율적 소프트웨어 지원을 위한 활동 (운영 수명 전 기간)
- 리팩터링, 기술부채 관리, 문서 유지 포함

**명시 없음**: 부채를 "기록하거나 추적"하라는 구체적 요구 사항 문서에 명시되지 않음 (v4 전문 접근 제한, 공개 요약만 확인 가능).

**[1차 (카탈로그 수준): https://www.computer.org/education/bodies-of-knowledge/software-engineering]** **[미확인 — 전문 유료]**

### CISQ Technical Debt Standard

**[상태] 서버 에러로 접근 불가**

CISQ는 "Automated Technical Debt" 표준을 발표했으나, 공식 웹사이트 접근 불가 (HTTP 522 Unknown Status).

**[미확인 — CISQ "Technical Debt Standard" 페이지(`it-cisq.org`)는 2026-08-05 전수 검사에서 HTTP 522(원서버 응답 없음). URL을 인용에서 제거해 링크 검사 대상에서 뺀다]**

### 산업 관행 vs. 표준

**[주장] 기술부채 추적 권장**

검색 결과 (Medium, Mark Heath, 개발사):
- "기술부채 레지스터"에 알려진 부채를 기록하라는 권장
- Jira, GitHub Issues 같은 백로그 도구에 부채 항목을 추적하라는 권장
- "부채를 추적하지 않으면 관리할 수 없다"는 모범 사례

**그러나**: 이는 **권장 (best practice)**, 공식 표준의 의무 규정 아님.

**[2차: https://markheath.net/post/technical-debt-register]**  
**[2차: https://othercode.io/blog/technical-debt-records]**  
**[2차: https://www.zendesk.com/blog/technical-debt/]**

### 종합: Q2

| 규정 출처 | 부채 추적 의무? | 증거 | 강도 |
|---------|------------|------|------|
| ISO/IEC 25010 | **명시 없음** | 유지보수성 특성 정의만; 추적 메커니즘은 조직 결정 | 표준 |
| SWEBOK v4 | **명시 없음** | 부채 관리 언급, 구체적 기록·추적 요구 미확인 (문서 전문 제한) | 가이드 |
| CISQ TD Standard | **미확인** | 접근 불가 (HTTP 522) | - |
| 산업 관행 | 권장 | GitHub, Jira 추적 권장; 개발사 블로그, 전문가 권고 | 모범 사례 |

**미해결:**
1. SWEBOK v4 원문에서 부채 추적 의무 명시 여부 (전문 문서 접근 제한)
2. CISQ Technical Debt Standard 요구 사항 (웹사이트 접근 불가)

---

## 상충·부정 증거

**없음.**

---

## 출처

### 1차 (공식 문서, 개방 접근)

- **Fowler, Martin.** "Definition Of Refactoring." *Martin Fowler's Bliki*, https://martinfowler.com/bliki/DefinitionOfRefactoring.html
- **Google.** "Small CLs." *Google Engineering Practices Documentation*, https://google.github.io/eng-practices/review/developer/small-cls.html
- **Google.** "Large-Scale Changes (Chapter 22)." *Software Engineering at Google*, https://abseil.io/resources/swe-book/html/ch22.html
- **IEEE Computer Society.** "Guide to the Software Engineering Body of Knowledge (SWEBOK) v4.0." https://www.computer.org/education/bodies-of-knowledge/software-engineering (2024년 10월 발표; 전문은 구독 모델)

### 2차 (실무 가이드, 개발사 블로그, 벤더 해설, 학술)

- **Heath, Mark.** "How should you track technical debt?" *Mark Heath's Blog*, https://markheath.net/post/technical-debt-register
- **otherCode.** "Technical Debt Records." *otherCode Software Studio Blog*, https://othercode.io/blog/technical-debt-records
- **Zendesk.** "What is technical debt and how to manage it effectively." *Zendesk Blog*, https://www.zendesk.com/blog/technical-debt/
- **Sonar (벤더).** "ISO/IEC 25010 Explained: 9 Software Quality Characteristics That Matter." *Sonar Resource Library*, https://www.sonarsource.com/resources/library/iso-iec-25010-explained/ (ISO 25010에 대한 벤더 해설; 1차 출처는 ISO 카탈로그)
- **Interlynk.** "CycloneDX vs SPDX: Choosing an SBOM Format for Regulatory Compliance (2026 Edition)." https://www.interlynk.io/resources/cyclonedx-vs-spdx-sbom-format (SBOM 최소 요소 및 관리 맥락)

### 미확인 (접근 불가)

- **CISQ.** "Technical Debt Standard." — 사이트가 HTTP 522로 응답해 본문 미확보. URL은 링크 검사 대상에서 제외(재시도는 review_due 때).
