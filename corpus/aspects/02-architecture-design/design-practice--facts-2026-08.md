---
id: aspect-02-architecture-design--design-practice--facts-2026-08
title: "Architecture & design practice — facts (2026-08)"
parent: aspect-02-architecture-design
kind: research-log
evidence_track: lit
status: draft
language: ko
last_updated: "2026-08-02"
method: "Haiku web-research agents, facts-only rules ([정의/규정]/[데이터]/[주장] labels), source-tier tagged [1차]/[2차]; session-lead verified"
---

# 소프트웨어 아키텍처와 설계 문서 실제

## 개요

현대 소프트웨어 산업에서 아키텍처 의사결정을 문서화하는 관행은 Google의 설계 문서(Design Doc) 문화, 각 조직의 RFC(Request for Comments) 프로세스, Michael Nygard의 ADR(Architecture Decision Record) 원형, 그리고 C4 모델로 체계화되었다. 설계 문서는 구현 전 명확성을 확보하는 효율적 수단이며, 각 회사는 규모 확대에 따라 이를 조직의 핵심 협업 도구로 진화시켰다.

---

## Google 설계 문서 (Design Doc)

### 정의 및 목적

[정의/규정] Malte Ubl은 설계 문서를 다음과 같이 정의한다: "설계 문서는 소프트웨어 설계에 대한 합의를 촉진하고 현재 및 미래의 구현자, 유지보수자, 기타 이해관계자를 위해 이를 문서화하는 데 사용되는 문서" [https://www.industrialempathy.com/posts/design-doc-a-design-doc/]

[정의/규정] Ubl의 설계 문서 구조는 6개 섹션으로 구성된다: (1) 메타정보(제목, 저자, 날짜, 상태), (2) 컨텍스트·범위·목표, (3) 개요, (4) 상세 설계, (5) 교차 문제(보안, 성능, 모니터링), (6) 검토된 대안 [https://www.industrialempathy.com/posts/design-doc-a-design-doc/]

[주장] Ubl은 "완전히 작동하는 구현으로 초기 소프트웨어 설계를 발전시키는 것이 비효율적임이 증명되었다"고 주장하며, 설계 문서가 이러한 비효율성을 해결한다고 설명한다 [https://medium.com/@cramforce/design-docs-a-design-doc-a152f4484c6b]

### 작성 시기

[주장] 설계 문서는 요구사항 확립 후, 본격적인 구현 시작 전에 작성되어야 한다 [https://medium.com/@cramforce/design-docs-a-design-doc-a152f4484c6b]

---

## ADR (Architecture Decision Record)

### 원형: Michael Nygard의 형식

[정의/규정] Michael Nygard는 2011년 "Documenting Architecture Decisions"에서 ADR을 소개했다. 그는 이렇게 기술한다: "새로운 팀원이 프로젝트에 합류할 때 과거의 의사결정에 당황할 수 있다. 근거나 결과를 이해하지 못하면, 이 사람은 두 가지 선택지만 남겨진다: 맹목적으로 의사결정을 받아들이거나 맹목적으로 변경하는 것" [https://adr.github.io/]

[정의/규정] Nygard의 ADR 템플릿은 5개 섹션으로 구성된다: (1) Title, (2) Status(제안됨, 수용됨, 거절됨, 폐기됨, 대체됨), (3) Context(의사결정 동기), (4) Decision(제안되거나 실행된 변경), (5) Consequences(이 변경으로 더 쉽거나 어려워진 것) [https://github.com/joelparkerhenderson/architecture-decision-record/tree/main/locales/en/templates/decision-record-template-by-michael-nygard]

[주장] ADR은 가볍고 실용적인 아키텍처 의사결정 기록 방식으로, 민첩 개발 프로세스에 적합하도록 설계되었다 [https://adr.github.io/]

---

## RFC (Request for Comments) 프로세스

### Uber의 RFC 도입

[데이터] Uber는 RFC 프로세스를 채택하여 DUCK 형식을 발전시켰다. 초기 엔지니어 인원이 작을 때 도입되어 회사가 급속도로 성장하면서도 지식 공유와 사일로 제거를 지원했다. 수십 명에서 수천 명의 엔지니어로 확대되는 상황에서도 확장되었다 [https://newsletter.pragmaticengineer.com/p/software-engineering-rfc-and-design]

### 회사별 RFC 적용

[데이터] Uber는 서비스별로 RFC를 구분한다: 서비스는 아키텍처 변경, SLA, 의존성, 성능 테스트, 보안, 모니터링을 다루고, 모바일은 UI/UX, 네트워크 상호작용, 라이브러리 의존성, 분석, 접근성을 다룬다 [https://newsletter.pragmaticengineer.com/p/software-engineering-rfc-and-design]

[데이터] Spotify는 "RFCs와 ADRs가 문화에 깊이 내재되어 있으며, 조직개편과 같은 비기술적 변경에도 사용된다"고 한다 [https://newsletter.pragmaticengineer.com/p/software-engineering-rfc-and-design]

[데이터] Sourcegraph는 RFC의 기본 구조를 "Summary, Background, Problem, Proposal, Definition of success"로 설정하며, RFC를 경량화되고 저비용의 프로세스로 의도했다 [https://newsletter.pragmaticengineer.com/p/software-engineering-rfc-and-design]

### RFC로 엔지니어링 팀 확대

[주장] RFC 프로세스는 구현 전 명확한 계획을 통해 팀의 규모 확대를 지원한다. 계획을 문서화하면 조직 전체 엔지니어가 피드백을 제공하고, 중복 이니셔티브를 발견하며, 표준화된 접근을 조정할 수 있다 [https://blog.pragmaticengineer.com/scaling-engineering-teams-via-writing-things-down-rfcs/]

[주장] "모든 사람이 프로젝트 수행 방식에 동의하면, 접근 방식을 문서에 옮기는 것은 간단해야 한다"는 주장으로, 문서 작성이 잠재된 이견을 드러낸다고 설명한다 [https://blog.pragmaticengineer.com/scaling-engineering-teams-via-writing-things-down-rfcs/]

---

## C4 모델

### 정의와 구조

[정의/규정] C4 모델은 Context, Container, Component, Code의 네 계층으로 소프트웨어 아키텍처를 시각화하는 계층적 접근법이다 [https://c4model.com/introduction]

[정의/규정] 네 계층은 다음과 같이 정의된다: (1) System Context Diagram - "소프트웨어 시스템이 둘러싼 세계에 어떻게 맞는지 보여줌", (2) Container Diagram - "범위 내 소프트웨어 시스템 내부의 애플리케이션과 데이터 저장소 표시", (3) Component Diagram - "개별 컨테이너 내부의 컴포넌트 표시", (4) Code Diagram - "개별 컴포넌트의 코드 수준 구현 표시" [https://c4model.com/introduction]

---

## Walking Skeleton (Cockburn)

### 정의

[정의/규정] Alistair Cockburn은 Walking Skeleton을 "시스템의 작은 엔드-투-엔드 기능을 수행하는 작은 구현"으로 정의한다 [https://medium.com/kayvan-kaseb/using-walking-skeleton-approach-in-software-development-943c3d69a8c0]

[정의/규정] "최종 아키텍처를 사용할 필요는 없지만, 주요 아키텍처 컴포넌트를 연결해야 한다. 아키텍처와 기능성은 이후 병행하여 진화할 수 있다" [https://medium.com/kayvan-kaseb/using-walking-skeleton-approach-in-software-development-943c3d69a8c0]

### 목적

[주장] Walking Skeleton은 배포 파이프라인이 작동함을 확인함으로써 프로젝트를 시작하는 최선의 방법이다. 소프트웨어의 가치가 프로덕션에서 실현되므로, 릴리스 수단을 프로젝트 초기부터 확립한다 [https://medium.com/kayvan-kaseb/using-walking-skeleton-approach-in-software-development-943c3d69a8c0]

---

## Tracer Bullet (Pragmatic Programmer)

### 정의 및 원리

[정의/규정] Hunt와 Thomas는 tracer bullet을 "UI, 비즈니스 로직, 데이터베이스를 통해 엔드-투-엔드 실행이 이루어지는 골격 애플리케이션"으로 정의한다 [https://www.artima.com/articles/tracer-bullets-and-prototypes]

[정의/규정] "Tracer bullet 코드는 불완전하지만 완결되어 있으며, 최종 시스템의 골격을 이루는 부분이다" [https://www.artima.com/articles/tracer-bullets-and-prototypes]

### 프로토타이핑과의 차이

[정의/규정] Hunt와 Thomas는 다음과 같이 구별한다: "프로토타이핑은 학습 도구이며, 의도적으로 폐기되도록 설계된다. 반면 tracer bullet은 점진적 개선을 통해 프로덕션 소프트웨어로 진화한다" [https://www.artima.com/articles/tracer-bullets-and-prototypes]

[주장] "더 빠르게 피드백을 얻을수록, 궤도를 벗어난 범위는 더 작아진다"는 원리로 반복적 피드백의 중요성을 강조한다 [https://www.artima.com/articles/tracer-bullets-and-prototypes]

---

## 아키텍처 리뷰 프로세스

### 목적과 이점

[정의/규정] 아키텍처 리뷰는 "IT 시스템의 컴포넌트, 설계 의사결정, 코드베이스, 문서, 기술 전략을 분석하는 것"이다 [https://www.redhat.com/en/blog/architecture-design-review]

[데이터] Red Hat은 설계 리뷰의 7가지 이점을 제시한다: (1) 품질 - 경험 있는 피어의 피드백이 실수를 줄임, (2) 커뮤니케이션, (3) 문서화, (4) 표준화, (5) 기준 상향, (6) 기술 부채 추적, (7) 재사용성 [https://www.redhat.com/en/blog/architecture-design-review]

### 프로세스

[정의/규정] 설계 리뷰 프로세스는 다음 단계를 포함한다: (1) 설계자가 문제 및 제안된 솔루션을 상세히 기술한 문서 제출, (2) 리뷰어가 기술적, 전략적 측면의 피드백 제공, (3) 양측 협업으로 피드백 기반 설계 개선, (4) 승인으로 구현 진행 허가 [https://www.redhat.com/en/blog/architecture-design-review]

---

## 출처

> [1차] = 원저자·원기관 발행 / [2차] = 제3자의 정리·집계

- [1차] https://www.industrialempathy.com/posts/design-doc-a-design-doc/ - Malte Ubl 설계 문서 정의
- [1차] https://medium.com/@cramforce/design-docs-a-design-doc-a152f4484c6b - Malte Ubl Medium 아티클
- [1차] https://adr.github.io/ - Architecture Decision Records 공식 사이트
- [2차] https://github.com/joelparkerhenderson/architecture-decision-record/tree/main/locales/en/templates/decision-record-template-by-michael-nygard - Michael Nygard ADR 템플릿
- [1차] https://c4model.com/introduction - C4 모델 공식 사이트
- [2차] https://medium.com/kayvan-kaseb/using-walking-skeleton-approach-in-software-development-943c3d69a8c0 - Walking Skeleton 설명
- [1차] https://www.artima.com/articles/tracer-bullets-and-prototypes - Tracer Bullets (Hunt/Thomas 본인 인터뷰 — 제3자 게재, 발언은 원저자)
- [2차] https://newsletter.pragmaticengineer.com/p/software-engineering-rfc-and-design - Pragmatic Engineer RFC와 설계 문서 비교
- [2차] https://blog.pragmaticengineer.com/scaling-engineering-teams-via-writing-things-down-rfcs/ - RFC로 엔지니어링 팀 확대
- [2차] https://www.redhat.com/en/blog/architecture-design-review - 아키텍처 설계 리뷰 프로세스
