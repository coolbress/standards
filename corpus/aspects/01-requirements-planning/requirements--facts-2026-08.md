---
id: aspect-01-requirements-planning--requirements--facts-2026-08
title: "Requirements engineering — facts (2026-08)"
parent: aspect-01-requirements-planning
kind: research-log
evidence_track: lit
status: draft
language: ko
last_updated: "2026-08-02"
method: "Haiku web-research agents, facts-only rules ([정의/규정]/[데이터]/[주장] labels), source-tier tagged [1차]/[2차]; session-lead verified"
---

# 요구사항 엔지니어링 표준과 실제

## 개요

요구사항 엔지니어링(Requirements Engineering)은 시스템과 소프트웨어의 생명주기 전체에서 요구사항을 정의, 도출, 명시하고 관리하는 학제적 활동이다. ISO/IEC/IEEE 29148:2018은 이를 표준화한 국제규격이며, 실무에서는 사용자 스토리(3C), INVEST 기준, BDD 형식의 인수기준, 그리고 PRD/Shape Up 같은 산업별 방법론이 병행된다. 각 기법은 팀 간 대화와 검증 가능성을 강조한다.

---

## ISO/IEC/IEEE 29148:2018

[정의/규정] ISO/IEC/IEEE 29148:2018은 시스템과 소프트웨어 엔지니어링의 생명주기 프로세스에서 요구사항 엔지니어링을 다루는 국제 표준이다 [https://www.iso.org/standard/72089.html]. 이전의 IEEE 830-1998, IEEE 1233-1998, IEEE 1362-1998을 대체한다 [https://standards.ieee.org/ieee/29148/5289/].

[데이터] 표준의 핵심 내용:
- 요구사항의 구성(construct) 정의: 좋은 요구사항의 특성 명시
- 요구사항의 속성(attributes)과 특징(characteristics) 규정
- 생명주기 전체에서 요구사항 프로세스의 반복적·재귀적 적용 방법
- 텍스트 기반 요구사항 작성 지침 제공

---

## 사용자 스토리와 3C 형식

[정의/규정] 사용자 스토리는 Agile 방법론의 핵심 요구사항 명시 기법이다. Ron Jeffries가 2001년에 제시한 3C 모델(Card, Conversation, Confirmation)을 Mike Cohn이 『User Stories Applied: For Agile Software Development』(2004)에서 일반화하여 표준으로 확립했다 [https://www.mountaingoatsoftware.com/agile/user-stories].

[정의/규정] 3C의 정의:
- **Card(카드)**: 스토리의 출발점. 간단하고 명확한 서술로 포스트잇에 기록 가능한 수준의 설명 [https://caroli.org/en/user-story/]
- **Conversation(대화)**: 이해관계자(고객, 사용자, 개발자, 테스터)들 간의 구두 대화. 문서로 보충되기도 함
- **Confirmation(확인)**: 대화의 목표 달성 여부를 검증하는 단계. 인수기준과 테스트로 표현됨 [https://www.visual-paradigm.com/guide/agile-software-development/what-is-user-story/]

[주장] Cohn은 "user story는 미래 대화를 위한 플레이스홀더"라고 강조하며, 작성된 텍스트보다 대화 자체가 더 중요하다고 주장한다.

---

## INVEST 기준

[정의/규정] Bill Wake는 2003년에 INVEST 프레임워크를 제시하여 좋은 사용자 스토리가 갖춰야 할 기준을 정의했다 [https://xp123.com/invest-in-good-stories-and-smart-tasks/]. 각 글자는 다음 기준을 나타낸다:

- **Independent(독립적)**: 스토리는 개념적으로 겹치지 않으며 순서에 관계없이 구현 가능해야 함
- **Negotiable(협상 가능)**: 명시적 계약이 아니라 개발 중 고객과 개발자가 세부사항을 함께 구성하는 것을 허용
- **Valuable(가치 있는)**: 고객에게 실질적 가치를 전달해야 함. 아키텍처의 단일 계층이 아닌 수직적 분할 권장
- **Estimable(추정 가능)**: 팀이 스토리의 규모를 충분히 추정하여 우선순위와 스케줄 결정에 활용 가능
- **Small(작은)**: 대부분 수 주일 이내의 작업량. 범위와 추정치의 정확성을 높임
- **Testable(테스트 가능)**: "테스트를 작성할 수 있을 정도로 요구사항을 이해한다"는 암묵적 약속을 담음 [https://www.agilealliance.org/glossary/invest/]

[주장] Wake는 사용자 스토리를 "고객과 개발자가 효과적으로 협업할 수 있는 피진(pidgin) 언어"라고 표현한다.

---

## Acceptance Criteria와 BDD

[정의/규정] Acceptance Criteria는 스토리가 "완성"되었음을 입증하는 조건 집합이다. Given-When-Then(GWT) 형식은 Behavior-Driven Development(BDD)의 기초로, 시나리오 기반의 구조화된 작성법을 제공한다 [https://www.productmonk.io/p/given-when-then-acceptance-criteria].

[정의/규정] GWT 구조:
- **Given**: 초기 상태와 사전조건 설정
- **When**: 사용자 행동 또는 트리거 사건 기술
- **Then**: 기대하는 결과(observable consequences) 명시

[데이터] GWT 형식은 Gherkin이라는 도메인 특화 언어로 표현되며, 비기술 이해관계자도 기술 요구사항을 이해할 수 있게 설계됨 [https://guides.visual-paradigm.com/give-when-then-acceptance-criteria-for-user-stories-in-agile-development/]. BDD는 개발자, 테스터, 비즈니스 이해관계자 간 협업을 강조하는 Agile 방법론의 한 분파이다 [https://www.thoughtworks.com/en-us/insights/blog/applying-bdd-acceptance-criteria-user-stories].

---

## 요구사항 도출(Elicitation) 기법

[데이터] 일반적인 요구사항 도출 기법:
- **인터뷰(Interviews)**: 가장 광범위하게 사용되는 기법. 사실 검증, 모호성 해소, 최종 사용자 참여, 요구사항 식별에 활용. 구조화(predefined questions)와 비구조화(open format) 유형 존재 [https://www.businessanalystlearnings.com/ba-techniques/2013/7/18/interviews-requirements-elicitation-technique]
- **케이스 스터디, 프로토타입** 등이 함께 사용됨 [https://www.softwaretestinghelp.com/requirements-elicitation-techniques/]

[정의/규정] **The Mom Test**(Rob Fitzpatrick, 저자)는 고객으로부터 진실한 피드백을 얻기 위한 3가지 규칙을 제시한다 [https://www.shortform.com/blog/what-is-the-mom-test/]:

1. **당신의 아이디어를 피치하지 말 것**: 상품 개념을 직접 공개하면 상대방이 예의상 칭찬하거나 제안만 하게 됨. 대신 상대방의 일상, 목표, 현재의 문제해결 방법에 대해 물을 것
2. **과거의 구체적 행동을 묻기**: 현재 습관이나 가설적 미래 의견이 아닌 최근 사례와 구체적 사실. "어제 저녁 무엇을 했는가?"는 "이 제품을 쓸 건가?"보다 신뢰도 높음
3. **적게 말하고 많이 들을 것**: 질문자의 해석과 의견을 최소화하여 편향 방지 [https://durmonski.com/book-summaries/the-mom-test/]

---

## PRD와 1-Pager 템플릿

[데이터] **Lenny Rachitsky의 PRD 템플릿**: 3단계 프레임워크(문제 결정화 → 해결책 설계)를 따르며, 팀과 이해관계자의 정렬을 목표로 함. "문제 정의가 모든 문제 해결의 가장 중요한 단계"라고 강조 [https://www.lennysnewsletter.com/p/my-favorite-templates-issue-37]. 1-Pager는 문제 이해와 솔루션 설계를 분리하며, 성공 정의로 팀의 트레이드오프 결정 지원 [https://www.atlassian.com/software/confluence/templates/lennys-product-requirements].

[정의/규정] **Amazon의 PR/FAQ** (Working Backwards 방법론): 고객 중심 관점을 유지하는 전략적 사고를 위해 개발됨 [https://workingbackwards.com/resources/working-backwards-pr-faq/].

구조:
- **Press Release(1~1.5 페이지)**: 엄격한 템플릿 준수. 제목(Heading), 부제(Subheading), 요약 단락(city, outlet, date, overview), 문제(Problem), 솔루션(Solution), 인용문·시작하기(Quotes & Getting Started) 포함
- **External FAQs**: 고객 대면 질문(가격, 기능, 지원, 구매)
- **Internal FAQs**: 내부 이해관계자(재무, 마케팅, 운영, HR, 법무) 관심사. 시장 규모, 경쟁 차별화, 필요 역량, 의존성, 규제, 단위경제, 가정 등 다룸 [https://medium.com/agileinsider/press-releases-for-product-managers-everything-you-need-to-know-942485961e31]

---

## Shape Up의 Pitch와 Appetite

[정의/규정] **Shape Up** (Basecamp, Ryan Singer)의 Pitch는 5가지 필수 요소로 구성됨 [https://basecamp.com/shapeup/1.5-chapter-06]:

1. **Problem**: 기본 아이디어, 사용 사례, 혹은 우리를 동기부여한 관찰
2. **Appetite**: 얼마나 많은 시간을 소비할지, 그리고 이것이 솔루션을 어떻게 제약하는지
3. **Solution**: 핵심 요소를 즉시 이해 가능한 형태로 제시
4. **Rabbit Holes**: 실행 중 문제를 피하기 위해 명시할 세부사항
5. **No-gos**: 명시적으로 제외하는 기능이나 사용 사례

[정의/규정] **Appetite(예산시간)**는 "소비할 시간의 양으로, 소요 시간 추정이 아닌 제약조건으로 기능"한다 [https://basecamp.com/shapeup/1.5-chapter-06]. 팀이 솔루션에 할애할 의사가 있는 주(weeks) 수를 결정하며, 이 시간 범위가 솔루션의 경계가 된다. Shape Up에서는 2주(Small Batch) 또는 6주(Big Batch) 규모의 appetite를 규정 [https://www.prodify.group/blog/book-report-5-key-takeaways-from-shape-up-by-basecamps-ryan-singer].

---

## 출처

> [1차] = 원저자·원기관 발행 / [2차] = 제3자의 정리·집계

- [1차] [ISO/IEC/IEEE 29148:2018 표준](https://www.iso.org/standard/72089.html)
- [1차] [IEEE SA 공식 표준 페이지](https://standards.ieee.org/ieee/29148/5289/)
- [1차] [Mike Cohn, Mountain Goat Software - 사용자 스토리](https://www.mountaingoatsoftware.com/agile/user-stories)
- [2차] [Ron Jeffries의 3C 프레임워크](https://caroli.org/en/user-story/) (Paulo Caroli의 해설 — Jeffries 원문 아님)
- [2차] [Visual Paradigm - 사용자 스토리 정의](https://www.visual-paradigm.com/guide/agile-software-development/what-is-user-story/)
- [1차] [Bill Wake, XP123 - INVEST 기준](https://xp123.com/invest-in-good-stories-and-smart-tasks/)
- [1차] [Agile Alliance - INVEST 용어](https://www.agilealliance.org/glossary/invest/)
- [2차] [ProductMonk - Given/When/Then Acceptance Criteria](https://www.productmonk.io/p/given-when-then-acceptance-criteria)
- [2차] [Visual Paradigm - GWT 가이드](https://guides.visual-paradigm.com/give-when-then-acceptance-criteria-for-user-stories-in-agile-development/)
- [2차] [ThoughtWorks - BDD와 사용자 스토리](https://www.thoughtworks.com/en-us/insights/blog/applying-bdd-acceptance-criteria-user-stories)
- [2차] [Business Analyst Learnings - 인터뷰 기법](https://www.businessanalystlearnings.com/ba-techniques/2013/7/18/interviews-requirements-elicitation-technique)
- [2차] [Software Testing Help - 요구사항 도출 기법](https://www.softwaretestinghelp.com/requirements-elicitation-techniques/)
- [2차] [Shortform - The Mom Test](https://www.shortform.com/blog/what-is-the-mom-test/)
- [2차] [Durmonski - The Mom Test 요약](https://durmonski.com/book-summaries/the-mom-test/)
- [1차] [Lenny Rachitsky, Lenny's Newsletter - 템플릿](https://www.lennysnewsletter.com/p/my-favorite-templates-issue-37)
- [2차] [Atlassian Confluence - Lenny의 PRD 템플릿](https://www.atlassian.com/software/confluence/templates/lennys-product-requirements)
- [1차] [Working Backwards - Amazon PR/FAQ](https://workingbackwards.com/resources/working-backwards-pr-faq/)
- [2차] [Medium - PR/FAQ 제품 관리](https://medium.com/agileinsider/press-releases-for-product-managers-everything-you-need-to-know-942485961e31)
- [1차] [Basecamp - Shape Up Pitch 작성](https://basecamp.com/shapeup/1.5-chapter-06)
- [2차] [Prodify - Shape Up 핵심 요약](https://www.prodify.group/blog/book-report-5-key-takeaways-from-shape-up-by-basecamps-ryan-singer)
