---
id: aspect-24-governance-collaboration-compliance--roles-teams--facts-2026-08
title: "Roles & team structures — facts (2026-08)"
parent: aspect-24-governance-collaboration-compliance
kind: research-log
evidence_track: lit
status: draft
language: ko
last_updated: "2026-08-02"
method: "Haiku web-research agents, facts-only rules ([정의/규정]/[데이터]/[주장] labels), source-tier tagged [1차]/[2차]; session-lead verified"
---

# 소프트웨어 조직의 역할과 팀 구조

## 개요

소프트웨어 조직의 역할 정의는 Product Manager, Product Owner, Project Manager 간 구분이 핵심이며, 개별 기여자 커리어 래더(Staff Engineer, Tech Lead, Engineering Manager)는 공표된 조직의 프레임워크를 통해 정의된다 [정의/규정]. 팀 구조는 Team Topologies의 4가지 팀 유형과 3가지 상호작용 모드, Conway's Law의 조직-설계 상관관계, Amazon의 two-pizza team, Spotify의 squad 모델 등으로 설명된다 [이론]. 실증 연구는 3-7명 규모 팀의 생산성이 최적이라고 보고한다 [데이터].

---

## 1. 역할 정의 [정의/규정]

### Product Manager vs Product Owner vs Project Manager

**Product Manager**: 제품 비전·전략을 정의하고 고객·시장 요구를 이해하며, 기능 우선순위와 cross-functional 정렬을 이끈다 [Aha의 역할 설명: https://www.aha.io/roadmapping/guide/product-management/what-is-the-role-of-a-product-manager]. 이는 단일 보편 표준이 아니라 제품관리 도구 공급자의 역할 모델이다.

**Product Owner**: Scrum Guide 2020에서 Product Owner는 제품 가치 극대화와 Product Backlog의 목표·항목·순서·투명성에 책임을 진다 [https://scrumguides.org/scrum-guide.html]. 이는 Scrum의 accountability 정의이며 모든 조직의 직무기술서로 일반화하지 않는다.

**Project Manager**: Aha의 비교 설명에서 Project Manager는 제품전략 자체가 아니라 특정 프로젝트의 실행을 감독해 일정과 예산 안에서 완료되도록 하는 역할이다 [https://www.aha.io/roadmapping/guide/product-management/what-is-the-role-of-a-product-manager]. 조직·방법론별 차이가 있으므로 보편적 권한 경계로 고정하지 않는다.

### Engineering Career Ladders [정의/규정]

**Dropbox Career Framework**: 엔지니어링 역할을 "Core Responsibilities (CR)—영향력 있는 업무가 무엇인지 정의하는 핵심 행동"으로 정의한다 [https://dropbox.tech/culture/our-updated-engineering-career-framework]. 프레임워크는 단일 역할과 직급 조합(예: "IC5 Staff Security Engineer")에 대한 완전한 설명을 제공하며, IC4+ 엔지니어가 tech lead나 architect로서 다양한 역할을 충족할 수 있는 방법을 다룬다. 2023년 업데이트에서는 기술적 역량 기대치, 비즈니스 인식, 의사결정 및 협업에 대한 명확성을 추가했다.

**GitLab Engineering Roles**: Management track과 Individual Contributor track을 병렬로 운영한다:
- Management: Engineering Manager → Senior Manager, Engineering → Director, Engineering → Senior Director, Engineering → VP of Engineering
- IC Track: Engineer → Senior Engineer → Staff Engineer → Principal Engineer → Distinguished Engineer → Senior Distinguished Engineer → Engineering Fellow

각 IC 역할은 관리 자격에 상응하는 조직적 영향력을 정의한다. Principal Engineer는 "Senior Engineering Manager의 개인기여자 등가물"이고, Distinguished Engineer는 "Director, Engineering의 개인기여자 등가물"이며, Engineering Fellow는 "VP of Engineering의 개인기여자 등가물로서 조직 전체의 최고 수준 복잡도의 기술 문제를 해결한다" [https://handbook.gitlab.com/job-description-library/engineering/engineering-management/].

---

## 2. 팀 구조 이론 및 모델 [이론]

### Team Topologies: 4가지 팀 유형과 3가지 상호작용 모드 [정의/규정]

**4가지 팀 유형** (Skelton & Pais):

1. **Stream-aligned teams**: "일반적으로 비즈니스 도메인의 세그먼트에서 업무 흐름에 정렬된 팀". 핸드오프 없이 결과를 end-to-end로 소유한다.
2. **Platform teams**: "다른 팀 유형의 그룹화로서 Stream-aligned 팀의 전달을 가속화하기 위한 내부 제품을 제공한다" [https://teamtopologies.com/key-concepts].
3. **Enabling teams**: "Stream-aligned 팀이 장애물을 극복하도록 돕고 누락된 역량을 감지한다". 임시적이고 초점이 맞춰진 지원이다.
4. **Complicated Subsystem teams**: 상당한 수학/계산/기술 전문성이 필요한 특화 영역을 처리한다.

**3가지 상호작용 모드**:
1. **Collaboration**: "새로운 것들(API, 실행, 기술 등)을 발견하기 위해 정의된 기간 동안 함께 작업한다"
2. **X-as-a-Service**: "한 팀이 제공하고 한 팀이 어떤 것을 '서비스로' 소비한다"—최소한의 지속적 상호작용
3. **Facilitation**: "한 팀이 다른 팀을 돕고 멘토링한다"—임시적 지원 [https://teamtopologies.com/key-concepts]

### Conway's Law [이론, 주장]

**원문**: Melvin Conway는 "지원된 조직은 그 조직의 통신 구조의 복사인 설계를 생산하도록 제약된다"고 정의했다 [https://www.melconway.com/Home/Conways_Law.html]. 원제목은 "How Do Committees Invent?"으로 1967년 Harvard Business Review에 거부당한 후 1968년 4월 Datamation에 게재되었다.

**영향**: Fred Brooks는 《The Mythical Man-Month》에서 이를 인용하며 "Conway's Law"라고 명명했고, 이를 통해 소프트웨어 엔지니어링 커뮤니티에 광범위하게 전파되었다.

### Amazon Two-Pizza Team [정의/규정]

**정의**: "두 개의 피자로 먹일 수 있을 만큼의 크기—이상적으로 10명 미만의 팀" [https://aws.amazon.com/executive-insights/content/amazon-two-pizza-team/]. 단일 제품 또는 서비스에 대한 focused responsibility를 유지하며 전체 고객 생명주기에 걸쳐 명확한 책임을 생성한다.

**rationale**: Amazon이 성장하며 민첩성이 감소하자 이 구조를 도입했다. 마이크로서비스 아키텍처와 분산된 자율적 팀을 결합하여 대규모 엔터프라이즈로 성장하면서 스타트업 같은 속도를 유지했다 [https://aws.amazon.com/executive-insights/content/amazon-two-pizza-team/].

### Spotify Model [주장, 이론]

**구조**: Squads (기능 cross-functional팀, 독립 배포) → Tribes (관련 제품 영역) → Chapters (규율 리더십/인원 관리) → Guilds (공동관심 커뮤니티) [https://www.atlassian.com/agile/agile-at-scale/spotify].

**중요 제한사항**: 원 2012년 논문은 Spotify가 30-40개 squads를 가질 때 작성되었으나, 2019년까지 수백 명의 엔지니어를 보유했고 "그 논문에 설명된 모델이 더 이상 그들이 작동하는 방식과 맞지 않는다"고 인정했다 [https://www.atlassian.com/agile/agile-at-scale/spotify]. 저자들은 "Spotify 모델은 20% 구조와 80% 문화이며, 자율성, 심리적 안전, 실험 의지, 실패 용인 문화가 있어야만 작동한다"고 명시했다 [주장].

---

## 3. 팀 크기 연구 [데이터]

**QSM 연구**: "3-7명 팀이 소프트웨어 개발 프로젝트의 최적 팀 규모이며, 특히 5-7명 데이터셋이 최고 성능을 보였고, 3-5명 데이터셋이 매우 가깝다" [https://www.qsm.com/team-size-can-be-key-successful-software-project]. 또한 "한 연구는 최적 팀 규모를 4.6명으로 파악했다" [데이터].

**대규모 팀의 비용**: "9명 이상 팀은 더 작은 팀보다 현저히 생산성이 낮다. 추가 인원은 일정을 약 30% 단축했지만 프로젝트 비용은 350% 증가했고, 추가 인원은 테스트 중 수정해야 할 결함을 500% 더 생산했다" [https://www.qsm.com/blog/2019/4-key-studies-team-size]. 대규모 팀은 비용이 3-4배 더 많이 들고 결함이 2-3배 더 많다 [데이터].

---

## 4. 발견과 전달 [정의/규정]

### Dual-Track Agile (Continuous Discovery) [정의/규정]

**정의**: Marty Cagan은 "발견 트랙은 검증된 제품 백로그 항목을 빠르게 생성하는 것에 관한 것이고, 전달 트랙은 릴리스 가능한 소프트웨어를 생성하는 것에 관한 것이다"고 정의했다 [https://www.svpg.com/dual-track-agile/]. 개념은 "발견과 전달의 병렬 특성을 포착한다"이며, 발견팀이 모든 제품 백로그 항목을 완전히 정의하기 전에 전달팀이 개발을 시작할 수 있다.

**원점**: 개념은 Jeff Patton에 의해 처음 공유되었고 Cagan이 채택했다. Cagan은 나중에 "프로세스보다 기본 원리에 중점을 두기" 위해 용어를 "Continuous Discovery와 Continuous Delivery"로 변경했다 [주장].

---

## 5. 소규모 팀과 스타트업의 역할 통합

공표된 문서는 소규모 팀/스타트업에서 역할 통합에 대한 구체적 정의를 제시하지 않는다. 다만 Dropbox와 GitLab의 프레임워크 모두 "단일 역할과 직급 조합"을 명시적으로 다루며, 개인이 기술적 전문성과 리더십 책임을 동시에 수행할 수 있음을 인정한다. 실제 역할 통합은 조직 문맥과 팀 규모에 따라 변동한다.

---

## 출처 목록

> [1차] = 원저자·원기관 발행 / [2차] = 제3자의 정리·집계

- [2차·vendor role model] [https://www.aha.io/roadmapping/guide/product-management/what-is-the-role-of-a-product-manager](https://www.aha.io/roadmapping/guide/product-management/what-is-the-role-of-a-product-manager)
- [1차·Scrum definition] [https://scrumguides.org/scrum-guide.html](https://scrumguides.org/scrum-guide.html)
- [1차] [https://dropbox.tech/culture/our-updated-engineering-career-framework](https://dropbox.tech/culture/our-updated-engineering-career-framework)
- [1차] [https://handbook.gitlab.com/job-description-library/engineering/engineering-management/](https://handbook.gitlab.com/job-description-library/engineering/engineering-management/)
- [1차] [https://teamtopologies.com/key-concepts](https://teamtopologies.com/key-concepts)
- [1차] [https://www.melconway.com/Home/Conways_Law.html](https://www.melconway.com/Home/Conways_Law.html)
- [1차] [https://aws.amazon.com/executive-insights/content/amazon-two-pizza-team/](https://aws.amazon.com/executive-insights/content/amazon-two-pizza-team/)
- [2차] [https://www.atlassian.com/agile/agile-at-scale/spotify](https://www.atlassian.com/agile/agile-at-scale/spotify)
- [2차] [https://www.qsm.com/team-size-can-be-key-successful-software-project](https://www.qsm.com/team-size-can-be-key-successful-software-project)
- [2차] [https://www.qsm.com/blog/2019/4-key-studies-team-size](https://www.qsm.com/blog/2019/4-key-studies-team-size)
- [1차] [https://www.svpg.com/dual-track-agile/](https://www.svpg.com/dual-track-agile/)
