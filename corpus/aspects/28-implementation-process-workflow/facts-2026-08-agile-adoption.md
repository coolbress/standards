---
id: aspect-28-implementation-process-workflow--facts-2026-08-agile-adoption
title: "Agile frameworks & adoption — facts (2026-08)"
parent: aspect-28-implementation-process-workflow
kind: research-log
evidence_track: lit
status: draft
language: ko
last_updated: "2026-08-02"
method: "Haiku web-research agents, facts-only rules ([정의/규정]/[데이터]/[주장] labels), source-tier tagged [1차]/[2차]; session-lead verified"
---

# 애자일 프레임워크: 규정과 채택 현황

## 개요

애자일 선언문(2001)은 개인과 상호작용, 동작하는 소프트웨어, 고객 협력, 변화 대응을 네 가지 가치로 제시한다. Scrum, Kanban, XP, SAFe, Shape Up 등 다섯 가지 주요 구현 방식이 존재하며, 프레임워크마다 역할·이벤트·산출물 정의에서 차이를 보인다. Scrum이 70% 채택률로 지배적이고, 하이브리드 접근이 31%로 성장 중이며, 예측형은 24% 감소(2020-2023)했다.

---

## 애자일 선언문 (2001)

### [정의/규정] 네 가지 가치

"우리는 다음을 가치 있게 여긴다:
- 과정과 도구보다 **개인과 상호작용**
- 광범위한 문서보다 **동작하는 소프트웨어**
- 계약 협상보다 **고객과의 협력**
- 계획을 따르기보다 **변화에 대한 대응**

오른쪽 항목도 가치가 있지만, 왼쪽 항목을 더 가치 있게 여긴다." [https://agilemanifesto.org/](https://agilemanifesto.org/)

### [정의/규정] 12가지 원칙

1. 변화하는 요구사항을 환영하라. 심지어 개발 후기라도. 애자일은 변화를 고객의 경쟁 우위로 이용한다.
2. 일하는 소프트웨어를 자주 전달하라. 몇 주에서 몇 개월까지, 짧은 기간을 선호한다.
3. 사업 담당자와 개발자는 프로젝트 전체에 걸쳐 매일 함께 일해야 한다.
4. 동기부여된 개인들로 프로젝트를 구성하라. 필요한 환경과 지원을 주고 일을 끝내도록 신뢰하라.
5. 팀 내와 팀 간 정보 전달의 가장 효율적이고 효과적인 방법은 면대면 대화다.
6. 동작하는 소프트웨어가 진도의 주요 척도다.
7. 애자일 프로세스는 지속 가능한 개발을 한다. 스폰서, 개발자, 사용자가 무한정 일정한 속도를 유지할 수 있어야 한다.
8. 기술적 우수성과 좋은 설계에 지속적으로 주의를 기울이면 민첩성이 향상된다.
9. 단순함은 필수다. 하지 않을 일의 양을 최대화하는 기술이다.
10. 최고의 아키텍처, 요구사항, 설계는 자기 조직화하는 팀에서 나온다.
11. 정기적으로 팀은 더 효과적이 되는 방법을 생각하고, 그에 따라 행동을 조정하고 다듬는다.
12. 가장 높은 우선순위는 고객에게 가치 있는 소프트웨어를 빨리 그리고 계속 전달하는 것이다. [https://agilemanifesto.org/principles.html](https://agilemanifesto.org/principles.html)

---

## Scrum (2020 가이드)

### [정의/규정] 역할

**Product Owner**: 제품 가치를 최대화하는 것에 책임. 제품 목표 수립, 백로그 항목 생성 및 우선순위 지정, 투명성 보장. [https://scrumguides.org/scrum-guide.html](https://scrumguides.org/scrum-guide.html)

**Scrum Master**: Scrum 프레임워크 확립에 책임. 팀 코칭, 장애물 제거, 이벤트 진행. Product Owner를 백로그 관리로 지원하고, 조직의 Scrum 도입을 촉진.

**Developers**: Sprint마다 사용 가능한 증분 생성에 참여. Sprint 계획 수립, 품질 기준 유지, 매일 계획 적응, 상호 책임성 보유.

### [정의/규정] 다섯 가지 이벤트

1. **Sprint** (컨테이너 이벤트): 1개월 이하의 고정 시간박스
2. **Sprint Planning**: Sprint 목표 설정 및 완료할 작업 선정
3. **Daily Scrum**: Developer 15분 일일 회의, Sprint 목표 진도 점검
4. **Sprint Review**: 완료 작업 이해관계자 제시 및 피드백 수집
5. **Sprint Retrospective**: 프로세스 개선 방법 반성 및 조정

### [정의/규정] 세 가지 산출물

1. **Product Backlog**: 제품 개선에 필요한 것의 우선순위 있는 목록
2. **Sprint Backlog**: Sprint 목표, 선정된 항목, 전달 계획 포함
3. **Increment**: Product 목표로의 구체적 디딤돌, 사용 가능하고 검증됨

### [정의/규정] Definition of Done

제품이 공식적으로 "완료"된 상태의 형식적 정의. 공유된 완료 기준을 제공하며, 증분 공개 전에 충족되어야 함.

---

## Kanban (Anderson 원칙)

### [정의/규정] 네 가지 원칙

1. 지금 하고 있는 것으로부터 시작하라
2. 점진적 변화를 통해 진화시키라
3. 기존 역할과 프로세스를 존중하라
4. 모든 레벨에서 리더십을 권장하라

[https://djaa.com/revisiting-the-principles-and-general-practices-of-the-kanban-method/](https://djaa.com/revisiting-the-principles-and-general-practices-of-the-kanban-method/)

### [정의/규정] 여섯 가지 핵심 실천

1. 일의 시각화 (Visualize Work)
2. 진행 중인 작업 제한 (Limit WIP)
3. 흐름 관리 (Manage Flow)
4. 명시적 정책 수립 (Make Policies Explicit)
5. 피드백 루프 추가 (Add Feedback Loops)
6. 협력적 개선 (Improve Collaboratively)

Kanban은 점진적이고 진화적인 프로세스 변경을 위한 접근법이며, 연속적 개선을 기초로 한다.

---

## Extreme Programming (XP, Beck)

### [정의/규정] 12가지 핵심 실천

1. **Test-Driven Development**: 코드 작성 전 자동화된 단위 테스트 작성
2. **Planning Game**: 반복 시작 시 팀과 고객이 기능 토론 및 승인
3. **On-site Customer**: 고객이 개발 중 지속적으로 질문 답변 및 우선순위 결정
4. **Pair Programming**: 두 개발자가 같은 코드를 공동으로 작업
5. **Code Refactoring**: 코드 지속적 개선, 중복 제거, 일관성 증대
6. **Continuous Integration**: 개발자가 매일 여러 번 코드 커밋, 자동 테스트로 오류 감지
7. **Small Releases**: MVP 빠르게 배포, 그 후 작은 증분 업데이트
8. **Simple Design**: 모든 테스트를 통과하는 가장 간단한 설계
9. **Coding Standards**: 팀 차원의 코딩 규칙 및 스타일 규약
10. **Collective Code Ownership**: 모든 팀원이 시스템 설계 책임 공유
11. **System Metaphor**: 신입자도 이해 가능한 일관된 이름 규칙
12. **40-Hour Week**: 주당 최대 45시간 작업, 연장은 그 다음 주 없음

[https://www.altexsoft.com/blog/extreme-programming-values-principles-and-practices/](https://www.altexsoft.com/blog/extreme-programming-values-principles-and-practices/)

---

## SAFe (Scaled Agile Framework)

### [정의/규정] 네 가지 구조 레벨

1. **Team Level**: 기본 운영 단위, 반복 기간 2주. 팀이 직접 가치 창출.
2. **Program Level**: 50-130명 규모의 "Agile Release Train"(ART)으로 다수 팀 포함. 솔루션 전달 담당.
3. **Large Solution Level**: 두 개 이상 ART가 고객에게 가치 제공 필요 시. "Solution Train"으로 구성.
4. **Portfolio Level**: 가장 높은 수준. 전략적 비즈니스 목표를 실행과 연결, 투자 자금 관리, 전략 주제 정의, 가치 스트림 조정.

SAFe의 네 가지 구성: Essential SAFe, Large Solution SAFe, Portfolio SAFe, Full SAFe

[https://www.atlassian.com/agile/agile-at-scale/what-is-safe](https://www.atlassian.com/agile/agile-at-scale/what-is-safe)

---

## Shape Up (Basecamp)

### [정의/규정] 핵심 규정

**6주 사이클**: "6주는 의미 있는 무언가를 끝내기에 충분히 길고, 처음부터 마감이 임박해 보일 정도로 충분히 짧다." [https://basecamp.com/shapeup/0.3-chapter-01](https://basecamp.com/shapeup/0.3-chapter-01)

**Betting Table**: 쿨다운(2주) 기간에 이해관계자들이 다음 사이클에 할 프로젝트를 결정하는 회의. 팀 가용성, 비즈니스 우선순위, 최근 작업 패턴을 기반으로 판단. CEO, CTO, 선임 프로그래머, 제품 전략가 참석. "이후 다른 사람이 개입하거나 예약된 작업을 방해할 수 없다." [https://basecamp.com/shapeup/2.2-chapter-08](https://basecamp.com/shapeup/2.2-chapter-08)

**Circuit Breaker**: 팀이 배정된 사이클 내에 작업을 완료하지 못하면, 기본적으로 프로젝트 연장은 없다. 이는 "처음 기대치의 배수를 투자하는 위험을 제거하고, 먼저 재검토가 필요한 개념을 막는다." 범위 확대를 방지.

**No Backlog**: Shape Up는 전통적 백로그를 명시적으로 거부한다. "중요한 아이디어는 자연스럽게 돌아온다." 대신 분산된 목록에서 관리하며, 실제로 가치 있을 때 회수된다. "몇 가지 잠재적 베팅"만 유지.

---

## 채택 통계

### [데이터] State of Agile 2026

- **Scrum**: 약 70% (가장 광범위 도입) [https://staragile.com/blog/state-of-agile](https://staragile.com/blog/state-of-agile)
- **Kanban**: 약 50%
- **조직 전체 애자일 사용**: 97%가 어느 정도 애자일 개발 방식 사용 보고

### [데이터] 다양한 조사 통합

- Scrum: 63-87% (조사에 따라 범위 있음)
- Kanban: 56%
- ScrumBan: 27%
- Iterative: 20%
- Scrum/XP Hybrid: 13%

### [데이터] PMI Pulse of the Profession 2024

**접근법별 채택 추세 (2020-2023)**:
- **Agile**: +6% 증가 (하지만 2022-2023에는 8.8% 감소)
- **Hybrid**: 20% → 31% 증가 (+11%)
- **Predictive**: 2020 대비 24% 감소

**5년 이후 기대 (2028-2029)**:
- 76%가 애자일 사용 증가 예상
- 73%가 하이브리드 접근 증가 예상
- 34%가 예측형 감소 예상

**핵심 발견**: "애자일, 하이브리드, 예측형 프로젝트 관리 접근법은 모두 비슷한 성과를 제공할 수 있다. 성공은 한 방법론을 엄격히 준수하는 것이 아니라 올바른 접근법 선택이다."

[https://www.pmi.org/learning/thought-leadership/future-of-project-work](https://www.pmi.org/learning/thought-leadership/future-of-project-work)

---

## Scrum에 대한 공표된 비판

### 출처가 특정된 비판

[주장] Ron Jeffries는 ronjeffries.com의 "Dark Scrum" 에세이에서 Scrum이 실무에서 과도한 미시관리로 변질되어 "프로그래머의 세계가 안전하지 않아진다"고 주장한다. [https://ronjeffries.com/articles/016-09ff/time-was/]

[주장] Martin Fowler는 2018년 "The State of Agile Software in 2018" 연설에서 "Agile Industrial Complex"가 팀에 프로세스를 강제하는 것이 문제이며, 많은 실무에서 애자일의 본래 가치와 원칙을 무시하는 "허위 애자일"이 관행이라고 주장한다. [https://martinfowler.com/agile.html]

[주장] Allen Holub는 홈페이지 holub.com에서 Scrum이 "팀의 진정한 민첩성 능력 부족에 기초한 타협"을 만들며, 시간 기반 계획 같은 구식 관행을 수용한다고 비판한다. [https://holub.com/philosophy.html]

[주장] Basecamp는 Shape Up 방법론에서 백로그를 "영원히 자라나며 깨진 약속들의 재고"로 묘사하며 명시적으로 거부하고, Sprint 은유가 "끝에 피로함을 느끼는" 의미를 포함한다며 전통적 Sprint 기반 개발을 반대한다. [https://basecamp.com/shapeup/0.3-chapter-01]

[데이터] 2026년 State of Agile 조사에서 응답자의 40% 이상이 변화 저항, 리더십 참여 부족, 조직과 애자일 가치관의 불일치를 주요 채택 장애물로 지적했다. [https://staragile.com/blog/state-of-agile]

[데이터] 동일 조사에서 조직의 84%가 자신들이 높은 수준의 애자일 역량에 미달한다고 인정했으며, 이는 프레임워크를 완전히 숙달하지 못하면서도 채택하는 현황을 나타낸다. [https://staragile.com/blog/state-of-agile]

---

## 출처

> [1차] = 원저자·원기관 발행 / [2차] = 제3자의 정리·집계

- [1차] [Agile Manifesto](https://agilemanifesto.org/)
- [1차] [Agile Manifesto - 12 Principles](https://agilemanifesto.org/principles.html)
- [1차] [The 2020 Scrum Guide](https://scrumguides.org/scrum-guide.html)
- [1차] [Kanban Method - David J. Anderson School](https://djaa.com/revisiting-the-principles-and-general-practices-of-the-kanban-method/)
- [2차] [Extreme Programming - AltexSoft](https://www.altexsoft.com/blog/extreme-programming-values-principles-and-practices/)
- [2차] [SAFe Framework - Atlassian](https://www.atlassian.com/agile/agile-at-scale/what-is-safe)
- [1차] [Shape Up - Basecamp](https://basecamp.com/shapeup)
- [1차] [Shape Up - Introduction Chapter](https://basecamp.com/shapeup/0.3-chapter-01)
- [1차] [Shape Up - Betting Table Chapter](https://basecamp.com/shapeup/2.2-chapter-08)
- [2차] [State of Agile 2026](https://staragile.com/blog/state-of-agile)
- [1차] [PMI Pulse of the Profession 2024](https://www.pmi.org/learning/thought-leadership/future-of-project-work)
