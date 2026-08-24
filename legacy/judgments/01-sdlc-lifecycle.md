> ⚠️ **SUPERSEDED (2026-08-02)** — 이 문서의 사실 부분은 `../corpus/aspects/*/facts-2026-08-*.md`로, 판정 부분은 `../corpus/methods/` 및 `foundation/` 문서로 대체됐다. 역사 기록으로 보존하며, 활성 근거로 인용하지 않는다.

# 실무 소프트웨어 프로젝트의 End-to-End 라이프사이클 (2024–2026 기준)

> 조사 목적: 비개발자가 전문 엔지니어처럼 소프트웨어를 만들도록 돕는 AI 에이전트 하네스 설계의 기초 자료.
> 원칙: 교과서 이론이 아니라 "잘하는 팀이 실제로 하는 것"과 "형식적 절차(ceremony) vs 실제 하중을 받는 관행(load-bearing)"의 구분에 집중.

## 요약

1. 현대의 라이프사이클은 "단계의 순차 통과"가 아니라 **작은 단위로 전 단계를 반복 통과**하는 구조다. Discovery→요구사항→설계→구현→테스트→릴리스→운영이 하나의 큰 폭포가 아니라, 기능 단위마다 도는 짧은 루프다.
2. Waterfall의 원조 Royce(1970)조차 순차 모델을 "위험하며 실패를 부른다"고 썼다. 순수 waterfall은 원래부터 권장된 적이 없다 ([dwheeler.com](https://dwheeler.com/essays/waterfall.html)).
3. 실제 채택률: Scrum 계열이 애자일 팀의 87%로 지배적이나 ([Parabol 통계](https://www.parabol.co/resources/agile-statistics/)), 전체 프로젝트 세계에서는 예측형 44% / 하이브리드 32% / 애자일 26%로 하이브리드가 급성장 중이다 ([PMI Pulse 2024](https://pmwares.com/pmi-pulse-of-the-profession-2024-summary-key-insights/)).
4. 성과를 가르는 것은 방법론 이름이 아니라 **기술 관행**이다: trunk-based development, CI/CD, 작은 배치, 자동화된 테스트 — DORA 연구가 반복 검증 ([DORA 2024](https://dora.dev/research/2024/dora-report/)).
5. Elite 팀(응답자의 ~19%)은 온디맨드 배포, 변경 리드타임 1일 미만, 변경 실패율 ~5%, 복구 1시간 미만 ([Octopus 클러스터 분석](https://octopus.com/blog/2024-devops-performance-clusters)).
6. 필수 아티팩트는 놀랄 만큼 적다: 문제 정의 1장(one-pager/PRD), 설계 문서(design doc/RFC), 결정 기록(ADR), 자동화 테스트, 배포 파이프라인, 운영 런북/포스트모템. 나머지 대부분은 규모가 만들어낸 조율 비용이다.
7. 소규모 팀에서 역할은 사라지는 게 아니라 **접힌다**: 아키텍처 오너십, 품질 오너십, 실행 오너십 세 가지가 누군가에게 귀속되기만 하면 된다 ([Fraction](https://www.hirefraction.com/blog/optimal-dev-team-structure-for-small-teams/)).
8. 실패의 최대 원인은 코딩이 아니라 **요구사항과 검증**이다: CHAOS 30년 데이터에서 성공률은 ~31%에 정체, 소형 프로젝트 성공률 ~90% vs 대형 <10% ([OpenCommons CHAOS 정리](https://opencommons.org/CHAOS_Report_on_IT_Project_Outcomes)).
9. 대형 IT 프로젝트는 평균 45% 예산 초과, 예측 가치의 56% 미달, 17%는 회사 존립을 위협 ([McKinsey-Oxford](https://www.mckinsey.com/capabilities/tech-and-ai/our-insights/delivering-large-scale-it-projects-on-time-on-budget-and-on-value)) — 처방은 "작게 쪼개고, 일찍 통합하고, 항상 동작 상태를 유지"다.
10. AI 시대의 새 데이터: AI 도입은 개인 생산성을 올리지만 배포 안정성을 해친다(검증이 병목) — 검증·리뷰 체계 없이 코드 생산량만 늘리면 성과가 나빠진다 ([DORA 2024/2025](https://dora.dev/research/2024/dora-report/)).

---

## 1. 실제 라이프사이클: 단계는 살아있고, 순서는 죽었다

교과서적 단계 구분(discovery → 요구사항 → 설계 → 구현 → 테스트 → 릴리스 → 운영)은 여전히 유효하다. 바뀐 것은 **단위와 주기**다. 잘하는 팀은 이 전체 사이클을 프로젝트당 1번이 아니라 기능(feature)당 1번, 심하게는 하루에 여러 번 돈다.

### 1.1 Discovery / 문제 정의
- 현대 프로덕트 팀은 discovery(무엇을 만들지 알아내기)와 delivery(만들기)를 **같은 팀이 병렬로, 지속적으로** 수행한다. Jeff Patton과 Marty Cagan이 2012년경 "dual-track agile"로 정식화했고, Teresa Torres의 『Continuous Discovery Habits』(2021)가 실무 표준을 만들었다 ([Product Talk](https://www.producttalk.org/rise-modern-product-discovery/), [LogRocket 정리](https://blog.logrocket.com/product-management/dual-track-agile-continuous-discovery/)).
- 핵심 오해 주의: dual-track은 "기획팀 따로, 개발팀 따로"가 아니다. Cagan은 "같은 팀이 두 활동을 한다"고 명시한다.
- Basecamp의 Shape Up은 다른 접근: 사이클 시작 전에 시니어가 문제를 "shaping"(문제 + 대략적 해법 + **appetite**=투자 상한 시간)하고, betting table에서 6주 사이클에 베팅한다. 6주를 넘기면 자동 중단(circuit breaker) — 기한 연장이 아니라 재사고를 강제한다 ([Shape Up](https://basecamp.com/shapeup/2.2-chapter-08)).
- **하중을 받는 원칙**: "해법보다 문제 먼저". Lenny Rachitsky 등 상위 프로덕트 템플릿들의 공통점은 문제 이해와 해법 설계를 분리하는 것이다 ([Lenny's Newsletter PRD 사례집](https://www.lennysnewsletter.com/p/prds-1-pagers-examples)).

### 1.2 요구사항
- 실무의 요구사항은 "완결된 명세서"가 아니라 **점진적으로 구체화되는 대화의 기록**이다. 큰 문서 대신: one-pager(문제/가설/성공지표) → 백로그의 유저 스토리/티켓 → 각 티켓의 acceptance criteria로 내려간다.
- CHAOS 리포트 계열 데이터에서 실패 요인 1위는 일관되게 불완전한 요구사항과 사용자 참여 부족이고, 성공 요인 1~3위는 사용자 참여, 경영진 지원, 명확한 요구사항 선언이다 ([원조 CHAOS 1994 PDF](https://personal.utdallas.edu/~chung/SYSM6309/chaos_report.pdf)).
- 잘하는 팀의 실제 관행: 요구사항을 "완성"하려 하지 않고, **다음 한 조각을 만들 만큼만** 명확히 한 뒤 동작하는 소프트웨어로 검증하고 다시 요구사항으로 돌아온다.

### 1.3 설계
- Google의 design doc 문화가 업계 표준의 원형: 코딩 전에 저자가 비교적 비형식적인 문서로 목표, 제약, **검토한 트레이드오프와 기각한 대안**을 기록하고 리뷰받는다. 형식보다 "왜 이 결정인가"가 핵심이다 ([Design Docs at Google](https://www.industrialempathy.com/posts/design-docs-at-google/)).
- Uber, Squarespace, HashiCorp 등은 같은 것을 RFC라 부른다. Uber는 수십 명 규모일 때 시작해 수천 명까지 스케일했고, 복잡한 제안에는 승인자(approver) 필드를 붙였다 ([Pragmatic Engineer](https://blog.pragmaticengineer.com/scaling-engineering-teams-via-writing-things-down-rfcs/), [HashiCorp RFC 템플릿](https://www.hashicorp.com/en/how-hashicorp-works/articles/rfc-template)).
- Squarespace의 교훈: RFC를 써도 깊은 리뷰가 없으면 "미묘하게 결함 있는, 필요 이상으로 복잡한 시스템"이 나온다. 이들은 리뷰 결과를 "Yes, if"(조건부 승인) 형태로 구조화했다 ([Squarespace Engineering](https://engineering.squarespace.com/blog/2019/the-power-of-yes-if)).
- **설계 문서를 쓰는 기준** (전부 쓰는 게 아니다): 결정을 되돌리기 어렵거나, 여러 팀/서비스에 영향을 주거나, 트레이드오프가 클 때. 그 이하는 티켓 설명이나 PR 설명으로 충분하다 ([Pragmatic Engineer: RFCs, Design Docs, ADRs](https://newsletter.pragmaticengineer.com/p/rfcs-and-design-docs)).

### 1.4 구현
- 지배적 관행은 **작은 변경 + 잦은 통합**이다. Fowler의 CI 정의: 모든 팀원이 최소 하루 1회 메인라인에 통합하고, 매 통합을 자동 빌드+테스트로 검증한다 ([martinfowler.com CI](https://martinfowler.com/articles/continuousIntegration.html)). Fowler는 장수 피처 브랜치에서 CI 도구만 돌리는 것을 "CI theater"라 부른다.
- Trunk-based development: 활성 브랜치 3개 미만, 브랜치 수명 하루 미만이 기준. DORA가 고성과와의 상관을 반복 확인한 핵심 역량이다 ([trunkbaseddevelopment.com](https://trunkbaseddevelopment.com/), [DORA capabilities](https://dora.dev/capabilities/trunk-based-development/)).
- Google 코드 리뷰 표준: 리뷰의 목적은 "코드베이스의 전반적 건강이 시간이 지날수록 좋아지게 하는 것". CL(변경)은 작게 쪼개고, 리뷰 응답은 **최대 1영업일**, 큰 CL은 분할을 요청하는 게 기본 대응이다 ([Small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html), [Speed of Reviews](https://google.github.io/eng-practices/review/reviewer/speed.html)).
- 미완성 작업은 feature flag 뒤에 숨겨 main에 머지한다 — 이것이 브랜치 수명을 짧게 유지하는 실무적 열쇠다 ([LaunchDarkly](https://launchdarkly.com/blog/what-is-progressive-delivery-all-about/)).

### 1.5 테스트 / 검증
- 표준 모델은 test pyramid: 다수의 빠른 단위 테스트 + 일부 통합 테스트 + 극소수의 E2E 테스트 ([Practical Test Pyramid, martinfowler.com](https://martinfowler.com/articles/practical-test-pyramid.html)). Google Testing Blog는 E2E 편중이 느리고 flaky한 파이프라인을 만든다며 "Just Say No to More End-to-End Tests"를 명시했다 ([Google Testing Blog](https://testing.googleblog.com/2015/04/just-say-no-to-more-end-to-end-tests.html)).
- 잘하는 팀에서 테스트는 별도 "단계"가 아니라 구현과 동시에 작성되고 파이프라인에서 매 커밋마다 실행된다. "QA 단계로 넘긴다"는 모델은 고성과 팀에서 사라졌다.
- Continuous Delivery의 정의 자체가 검증이다: "소프트웨어를 언제나 프로덕션에 넣을 수 있는 상태로 유지"하며, 파이프라인이 그 상태를 지속적으로 시험한다 ([continuousdelivery.com](https://continuousdelivery.com/foundations/continuous-integration/)).

### 1.6 릴리스
- 현대 릴리스의 핵심 아이디어는 **deploy(코드 반영)와 release(사용자 노출)의 분리**다. Feature flag로 코드를 먼저 배포(dark launch)하고, 노출은 나중에 단계적으로 켠다 ([Flagsmith](https://www.flagsmith.com/blog/progressive-delivery)).
- Progressive delivery: canary(일부 사용자만), blue-green, 단계적 확대. GitHub는 신기능을 내부 직원에게만 먼저 켜는 "staff ships"를 운영한다 ([LaunchDarkly](https://launchdarkly.com/blog/what-is-progressive-delivery-all-about/)).
- 브랜치 전략은 GitHub flow(브랜치 → PR → 리뷰 → main 머지 → 배포)가 사실상의 기본값이다 ([GitHub Docs](https://docs.github.com/en/get-started/using-github/github-flow)).

### 1.7 운영 / 유지보수
- Google SRE의 기여: 운영을 소프트웨어 문제로 취급. 온콜 로테이션, 런북(playbook), 인시던트 커맨더 체계 ([SRE incident management](https://sre.google/resources/practices-and-processes/incident-management-guide/)).
- **Blameless postmortem**이 문화의 핵심: 개인 비난 없이 기여 원인을 기록하고, 교정 액션 아이템을 도출해 조직 전체에 공유한다. "포스트모템의 가치는 그것이 만들어내는 학습에 비례한다" ([SRE Book: Postmortem Culture](https://sre.google/sre-book/postmortem-culture/)).
- 유지보수는 별도 국면이 아니라 라이프사이클의 대부분이다 — 운영에서 얻은 신호(에러, 사용 데이터, 인시던트)가 discovery로 다시 흘러들어가 루프를 닫는다.

---

## 2. 단계별 아티팩트: 필수 vs 형식

| 단계 | 아티팩트 | 판정 | 근거 |
|---|---|---|---|
| Discovery | **One-pager / PRD** (문제, 왜 지금, 성공 지표) | **필수** — 단, 1~2장. 긴 PRD는 형식 | "팀이 실제로 쓸 템플릿이 옳은 템플릿" ([Lenny](https://www.lennysnewsletter.com/p/prds-1-pagers-examples)) |
| Discovery | Shape Up식 pitch + appetite(투자 상한) | 강력 — 시간 상한이 스코프 폭주의 구조적 방어 | [Shape Up](https://basecamp.com/shapeup/0.3-chapter-01) |
| 요구사항 | 백로그 티켓 + **acceptance criteria** | 필수(검증 가능성의 원천). 상세 명세서 전체는 형식 | CHAOS 성공요인 "명확한 요구사항" ([CHAOS](https://personal.utdallas.edu/~chung/SYSM6309/chaos_report.pdf)) |
| 설계 | **Design doc / RFC** — 영향 큰 변경에만 | 조건부 필수 (기준: 되돌리기 어려움, 다팀 영향, 큰 트레이드오프) | [Google](https://www.industrialempathy.com/posts/design-docs-at-google/), [Spotify ADR 기준](https://engineering.atspotify.com/2020/04/when-should-i-write-an-architecture-decision-record) |
| 설계 | **ADR** (결정 1건 = 문서 1건, 마크다운, 코드 저장소에 보관) | 필수 — 가장 비용 대비 효과 높은 문서 | [Google Cloud](https://docs.cloud.google.com/architecture/architecture-decision-records), [Spotify](https://engineering.atspotify.com/2020/04/when-should-i-write-an-architecture-decision-record) |
| 구현 | 작은 PR/CL + 리뷰 기록 | 필수 | [Google eng-practices](https://google.github.io/eng-practices/review/developer/small-cls.html) |
| 테스트 | 자동화 테스트 스위트 (피라미드형) | **필수 — 가장 하중을 받는 아티팩트** | [Practical Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html) |
| 테스트 | 별도 테스트 계획서, 수동 테스트 시나리오 문서 | 대부분 형식 (규제 산업 제외) | CD 원칙상 검증은 파이프라인에 내장 ([continuousdelivery.com](https://continuousdelivery.com/foundations/continuous-integration/)) |
| 릴리스 | CI/CD 파이프라인 정의 (코드로) | 필수 | [DORA CD capability](https://dora.dev/capabilities/continuous-delivery/) |
| 운영 | **런북**(장애 시 대응 절차), 모니터링/알림 | 필수 (운영하는 서비스라면) | [SRE incident guide](https://sre.google/resources/practices-and-processes/incident-management-guide/) |
| 운영 | **Blameless postmortem** | 필수 (인시던트 발생 시) | [SRE Book](https://sre.google/sre-book/postmortem-culture/) |
| 전반 | 상태 보고서, 간트 차트, 상세 산정 문서 | 대부분 형식 — 고성과 팀은 배포 데이터 자체가 상태 보고 | DORA 4 metrics가 대체 ([DORA](https://dora.dev/)) |

추가 근거 — 문서화 품질 자체가 성과 역량이다: DORA는 양질의 내부 문서가 다른 기술 역량들의 효과를 증폭한다는 것을 확인했다 ([DORA documentation quality](https://dora.dev/capabilities/documentation-quality/)).

주의할 반례 — Shape Up은 아예 **백로그 자체를 형식으로 간주**하고 유지하지 않는다(중요한 아이디어는 다시 돌아온다는 논리). 백로그가 필수인지는 업계 내 실제 논쟁 지점이다 ([Shape Up](https://basecamp.com/shapeup/2.1-chapter-07)).

---

## 3. 역할: 무엇을 기여하고, 작은 팀에서 어떻게 접히나

### 3.1 각 역할의 실제 기여
- **PM**: 문제 선택과 우선순위. "무엇을, 왜"의 오너. 산출물은 one-pager/PRD와 우선순위가 매겨진 백로그. 해법 지시가 아니라 문제와 성공 기준 정의가 본질 ([Lenny](https://www.lennysnewsletter.com/p/prds-1-pagers-examples)).
- **디자이너**: 문제의 사용자 측 구조화(플로우, 프로토타입)와 discovery 참여. Torres 모델에서 PM-디자이너-엔지니어 트리오가 discovery의 기본 단위다 ([Product Talk](https://www.producttalk.org/rise-modern-product-discovery/)).
- **엔지니어**: 구현 + 설계 결정 + 자기 코드의 검증. 현대 관행에서 테스트 작성은 엔지니어의 일이지 QA의 일이 아니다.
- **QA**: 고성과 조직에서 "수동 검사 게이트"에서 **품질 인프라 구축자**(테스트 전략, 자동화 프레임워크, 탐색적 테스트)로 이동했다. 별도 QA 단계는 CD와 양립 불가.
- **SRE/운영**: 신뢰성의 오너 — SLO, 모니터링, 온콜, 인시던트 대응, 포스트모템 주관 ([sre.google](https://sre.google/workbook/table-of-contents/)).

### 3.2 소규모 팀에서의 접힘
- 역할이 아니라 **책임 영역**이 보존 대상이다: 아키텍처 오너십 / 품질 오너십 / 실행 오너십 세 가지가 커버되면 2인 팀이 엉성한 6인 팀보다 빠르다 ([Fraction](https://www.hirefraction.com/blog/optimal-dev-team-structure-for-small-teams/)).
- 초기 스타트업에서 전담 PM은 오히려 비권장: 창업자와 엔지니어가 프로덕트를 직접 소유하는 게 낫고, PM은 엔지니어가 프로덕트 방향을 끌 시간이 없어질 때 필요해진다 ([AOL/Surge AI CEO 인터뷰](https://www.aol.com/surge-ais-ceo-says-never-045052984.html)).
- QA 없는 팀의 실무 패턴: QA/PM/UX를 "공유 모자(shared hat)"로 두되 각 영역의 지정 리드를 정한다 — 아무도 소유하지 않는 영역(orphan)을 없애는 게 핵심 ([Fraction](https://www.hirefraction.com/blog/optimal-dev-team-structure-for-small-teams/)).
- **하네스 설계 시사점**: 1인 비개발자 사용자의 경우 이 모든 역할이 "사용자 + 에이전트"로 접힌다. 사용자는 PM 역할(문제, 우선순위, 수용 판정)만은 위임할 수 없고, 에이전트는 엔지니어/QA/SRE의 검증 책임을 스스로 짊어져야 한다.

---

## 4. 방법론의 현실: 이름보다 관행

### 4.1 데이터가 말하는 실제 분포 (2024–2026)
- 애자일을 표방하는 팀 내부: Scrum 87%, Kanban 56%, ScrumBan 27% (중복 응답 — 절반 이상의 팀이 1년 내 프레임워크를 바꾸거나 겹쳐 쓴다). 2주 스프린트가 65%로 표준 ([Parabol/State of Agile 정리](https://www.parabol.co/resources/agile-statistics/)).
- 전체 프로젝트 관리 세계(PMI Pulse 2024): 예측형(waterfall 계열) 44%, **하이브리드 32%**, 애자일 26%. 하이브리드는 2020→2023 사이 57% 성장, 예측형은 24% 감소. 주목: 세 접근법 간 프로젝트 성과 차이는 유의미하지 않았다 ([PMI Pulse 2024 요약](https://pmwares.com/pmi-pulse-of-the-profession-2024-summary-key-insights/)).
- 즉 "방법론 이름"은 성과를 예측하지 못한다. 성과를 예측하는 것은 아래의 기술 관행이다.

### 4.2 DORA: 성과를 실제로 가르는 것
- 4대 지표: 배포 빈도, 변경 리드타임, 변경 실패율, 복구 시간. 2024년 클러스터: Elite 19% / High 22% / Medium 35% / Low 25%. Elite는 온디맨드 배포, 리드타임 <1일, 실패율 ~5%, 복구 <1시간 ([Octopus 분석](https://octopus.com/blog/2024-devops-performance-clusters), [DORA 2024](https://dora.dev/research/2024/dora-report/)).
- 핵심 통찰: **속도와 안정성은 트레이드오프가 아니다**. 잘하는 팀은 둘 다 좋다 — 작은 배치가 두 가지 모두의 원인이기 때문 ([RedMonk 분석](https://redmonk.com/rstephens/2024/11/26/dora2024/)).
- 성과 예측 역량: trunk-based development, CI/CD, 테스트 자동화, 느슨한 결합 아키텍처, 그리고 2024년 강조된 사용자 중심성(user-centricity)과 안정적 우선순위 — 우선순위가 흔들리는 조직은 생산성 하락 + 번아웃 급증 ([DORA 2024](https://dora.dev/research/2024/dora-report/)).
- AI 관련 (하네스 설계에 직결): 2024년 AI 도입은 개인 생산성·문서 품질을 올리지만 **딜리버리 처리량과 안정성을 낮췄다**. 2025년엔 처리량은 개선됐지만 불안정성은 지속 — 원인 진단은 "검증 세금": AI 생성 코드의 리뷰·검증이 하류 병목이 된다 ([DORA 2024](https://dora.dev/research/2024/dora-report/), [RDEL의 2025 리포트 분석](https://rdel.substack.com/p/rdel-112-whats-ai-impact-on-software), [DX 정리](https://getdx.com/blog/dora-metrics/)).

### 4.3 Waterfall의 진실
- Royce(1970)는 순차 다이어그램을 그린 뒤 곧바로 "이 구현은 위험하며 실패를 부른다", "단순한 방법은 대형 개발에서 작동한 적이 없다"고 썼고 반복·피드백 루프를 제안했다. 후대가 앞 페이지만 읽고 표준으로 만들었다 ([dwheeler.com](https://dwheeler.com/essays/waterfall.html), [Changelog](https://changelog.com/posts/waterfall-doesnt-mean-what-you-think-it-means)).
- 실무 결론: 오늘날 "waterfall이냐 agile이냐"는 잘못된 질문이다. 실제 변수는 (a) 배치 크기, (b) 통합 빈도, (c) 피드백 루프 길이다. 이 세 값이 작으면 뭐라고 부르든 잘 돌아간다.

---

## 5. 프로젝트가 실패하는 방식 — 증거 기반

1. **불명확한 요구사항 / 사용자 미참여** — CHAOS 계열 데이터의 부동의 1위 실패 요인. 성공 요인 1위는 사용자 참여 ([CHAOS 원문](https://personal.utdallas.edu/~chung/SYSM6309/chaos_report.pdf), [OpenCommons 정리](https://opencommons.org/CHAOS_Report_on_IT_Project_Outcomes)).
2. **규모 그 자체** — 소형 프로젝트 성공률 ~90%, 대형 <10% ([OpenCommons](https://opencommons.org/CHAOS_Report_on_IT_Project_Outcomes)). 대형 IT 프로젝트($15M+)는 평균 45% 예산 초과, 가치 56% 미달, 17%는 회사 존립 위협("black swan"), 기간이 1년 늘 때마다 비용 초과 평균 15%p 증가 ([McKinsey-Oxford, 5,400개 프로젝트](https://www.mckinsey.com/capabilities/tech-and-ai/our-insights/delivering-large-scale-it-projects-on-time-on-budget-and-on-value)). → 처방: 쪼개라.
3. **스코프 크리프** — 통제되지 않는 변경과 불명확한 목표. 구조적 방어책은 변경 금지가 아니라 Shape Up의 appetite(시간 상한 고정, 스코프 가변)와 circuit breaker다 ([Shape Up](https://basecamp.com/shapeup/2.3-chapter-09), [DesignRush/CHAOS](https://news.designrush.com/project-success-rate-discovery-phase-scope-creep)).
4. **빅뱅 통합** — 부품을 다 만들고 마지막에 합치는 방식은 위험을 끝으로 미룬다. 처방은 walking skeleton: 가장 얇은 end-to-end 조각을 최우선으로 만들어 배포·테스트하고, 그 뒤로는 항상 동작 상태를 유지하며 살을 붙인다 (Cockburn, Crystal Clear; [97 Things](https://yoshi389111.github.io/kinokobooks/soft_en/Start_with_a_Walking_Skeleton.htm), [해설](https://www.defmyfunc.com/2019_10_18_walking_skeleton/)). Fowler의 CI도 같은 문제의 처방이다 ([martinfowler.com](https://martinfowler.com/articles/continuousIntegration.html)).
5. **검증 부재 / 지연** — 검증이 늦을수록 결함 수정 비용이 커지고, 검증이 없으면 "존재하는 코드"가 "동작하는 코드"로 오인된다. CD의 존재 이유가 이것이며, AI 시대엔 DORA가 확인한 "검증 세금"으로 더 심해진다 ([continuousdelivery.com](https://continuousdelivery.com/), [DORA 2024](https://dora.dev/research/2024/dora-report/)).
6. **불안정한 우선순위** — 조직이 우선순위를 자주 뒤집으면 생산성 하락과 번아웃 급증 (DORA 2024의 주요 발견, [DORA 2024](https://dora.dev/research/2024/dora-report/)).
7. **설계 리뷰 부재** — 문서를 써도 깊은 리뷰가 없으면 미묘한 결함과 과잉 복잡성이 통과된다 ([Squarespace](https://engineering.squarespace.com/blog/2019/the-power-of-yes-if)).

---

## 6. AI 에이전트 하네스 설계에의 함의 (조사 결과의 압축)

- **루프가 단위다**: 하네스는 "단계 순서"가 아니라 "얇은 수직 조각 하나당 discovery→검증까지 도는 루프"를 기본 단위로 삼아야 한다. 첫 산출물은 walking skeleton이어야 한다.
- **최소 아티팩트 세트**: one-pager(문제/성공기준) → 조건부 design doc → ADR(결정마다) → acceptance criteria가 달린 작은 작업 단위 → 자동 테스트 → 파이프라인 → (운영 시) 런북/포스트모템. 이 이상은 규모가 요구하기 전까지 ceremony다.
- **비개발자 사용자에게 위임 불가능한 역할은 PM뿐**: 문제 정의, appetite(투자 상한) 결정, 수용 판정. 나머지 역할(설계·구현·QA·SRE)의 책임은 하네스가 구조적으로 짊어져야 한다.
- **검증이 병목이자 승부처**: DORA의 AI 발견이 정확히 이 하네스의 존재 이유를 뒷받침한다 — 생성은 싸졌고 검증이 비싸졌다. 하네스의 가치는 코드 생산이 아니라 검증 체계(테스트 피라미드, 작은 배치, 리뷰, 점진 릴리스)의 자동 내장에 있다.
- **시간 상한 > 스코프 상한**: 스코프 크리프 방어는 Shape Up식 appetite + circuit breaker가 실증된 구조다.

---

## 부록: 1차 소스 목록

- DORA Accelerate State of DevOps 2024: https://dora.dev/research/2024/dora-report/
- DORA capabilities (trunk-based, CD, documentation): https://dora.dev/capabilities/
- Martin Fowler, Continuous Integration: https://martinfowler.com/articles/continuousIntegration.html
- Martin Fowler(사이트), Practical Test Pyramid: https://martinfowler.com/articles/practical-test-pyramid.html
- Google Testing Blog, Just Say No to More End-to-End Tests: https://testing.googleblog.com/2015/04/just-say-no-to-more-end-to-end-tests.html
- Design Docs at Google (Malte Ubl): https://www.industrialempathy.com/posts/design-docs-at-google/
- Google eng-practices (code review): https://google.github.io/eng-practices/
- Google SRE Book, Postmortem Culture: https://sre.google/sre-book/postmortem-culture/
- Pragmatic Engineer, Scaling Engineering Teams via RFCs: https://blog.pragmaticengineer.com/scaling-engineering-teams-via-writing-things-down-rfcs/
- Squarespace, The Power of "Yes, if": https://engineering.squarespace.com/blog/2019/the-power-of-yes-if
- Spotify, When Should I Write an ADR: https://engineering.atspotify.com/2020/04/when-should-i-write-an-architecture-decision-record
- Google Cloud, ADR overview: https://docs.cloud.google.com/architecture/architecture-decision-records
- Basecamp, Shape Up (전문 무료): https://basecamp.com/shapeup
- Lenny's Newsletter, PRD/1-pager 사례: https://www.lennysnewsletter.com/p/prds-1-pagers-examples
- Product Talk (Teresa Torres), Rise of Modern Product Discovery: https://www.producttalk.org/rise-modern-product-discovery/
- PMI Pulse of the Profession 2024 요약: https://pmwares.com/pmi-pulse-of-the-profession-2024-summary-key-insights/
- Standish CHAOS (원문 1994): https://personal.utdallas.edu/~chung/SYSM6309/chaos_report.pdf / 정리: https://opencommons.org/CHAOS_Report_on_IT_Project_Outcomes
- McKinsey-Oxford, Delivering large-scale IT projects: https://www.mckinsey.com/capabilities/tech-and-ai/our-insights/delivering-large-scale-it-projects-on-time-on-budget-and-on-value
- David Wheeler, The Waterfall Model (Royce 1970 해설): https://dwheeler.com/essays/waterfall.html
- Trunk Based Development: https://trunkbaseddevelopment.com/
- GitHub flow: https://docs.github.com/en/get-started/using-github/github-flow
- LaunchDarkly, Progressive Delivery: https://launchdarkly.com/blog/what-is-progressive-delivery-all-about/
