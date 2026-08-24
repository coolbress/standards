> ⚠️ **SUPERSEDED (2026-08-02)** — 이 문서의 사실 부분은 `../corpus/aspects/*/facts-2026-08-*.md`로, 판정 부분은 `../corpus/methods/` 및 `foundation/` 문서로 대체됐다. 역사 기록으로 보존하며, 활성 근거로 인용하지 않는다.

# 제품 기획과 요구사항: 막연한 아이디어에서 검증 가능한 작업으로

> 조사 목적: 프로 소프트웨어 팀이 "무엇을 만들지"를 어떻게 결정하고, 막연한 아이디어를 빌드 가능하고 검증 가능한 스펙으로 바꾸는가. AI 에이전트 하네스(비개발자가 프로처럼 소프트웨어를 만들게 돕는)의 설계 기반 자료. 조사일: 2026-08-02.

## 요약

1. 프로는 해결책이 아니라 **문제부터 심문**한다. "그 기능 좋아요?"가 아니라 "지난번에 그 문제가 생겼을 때 어떻게 했나요?"를 묻는다 (The Mom Test).
2. 모든 강력한 스펙 문서의 공통 뼈대는 **문제 정의 + 성공 기준 + Non-goals(안 할 것)** — 회사가 달라도 이 3개는 반복해서 등장한다.
3. 현대 PRD는 얇다. 1-pager가 기본이고, 풀 PRD는 스테이크홀더가 많을 때만. 솔루션 상세보다 문제·성공지표·경계가 핵심.
4. Design Doc/RFC는 "구현 매뉴얼"이 아니라 **트레이드오프와 대안을 드러내는 장치**이며, 결정의 이유는 ADR로 리포지토리에 남긴다.
5. 작업 분해의 황금률은 **수직 슬라이스**: 레이어별(DB→백엔드→UI)이 아니라 사용자 가치 단위로 얇게 끝까지 자른다. 첫 슬라이스는 walking skeleton/tracer bullet.
6. 인수 기준은 "존재 여부"가 아니라 **테스트 가능성**이 본질이다 (INVEST의 T). Given/When/Then이든 체크리스트든, "무엇이 참이면 완료인가"가 적혀 있어야 한다.
7. MVP의 원래 의미는 제품이 아니라 **학습 실험**이다. 실무에선 "가장 위험한 가정부터 검증"(RAT)과 "Earliest Testable/Usable/Lovable"로 왜곡을 교정한다.
8. 추정은 구조적으로 실패한다(불확실성의 원뿔). 잘하는 팀은 정확한 추정 대신 **시간 고정 + 범위 가변**(Shape Up의 appetite, scope hammering)으로 문제를 뒤집는다.
9. 솔로/초소형 팀에서 살아남는 산출물: 문제 한 문단, 성공 기준, non-goals, 인수 기준, 얇은 첫 슬라이스. 죽는 것: 스토리 포인트, 추정 회의, 승인 보드, 풀 PRD.
10. 하네스 시사점: 비개발자의 막연한 요청 → "문제·성공기준·non-goals·인수기준" 4요소를 인터뷰로 추출하고, walking skeleton부터 수직 슬라이스로 배열하는 것이 프로 관행의 최소 재현이다.

---

## 1. 막연한 아이디어를 심문하는 법

### 1.1 The Mom Test — 질문의 규칙

Rob Fitzpatrick의 The Mom Test는 고객 인터뷰의 사실상 표준이다. 핵심 규칙 3개 ([momtestbook.com](https://www.momtestbook.com/), [요약](https://readingraphics.com/book-summary-the-mom-test/)):

1. **내 아이디어 말고 상대의 삶에 대해 말하라.**
2. **미래의 가정이 아니라 과거의 구체적 사실을 물어라.**
3. **말을 줄이고 들어라.**

- 나쁜 질문: "이거 좋은 아이디어 같아요?", "X 기능 있으면 사시겠어요?" → 의견과 가설적 답변만 유도. 엄마조차 상처 주지 않으려 거짓말한다.
- 좋은 질문: "왜 그걸 굳이 하세요?"(동기), "마지막으로 그 일이 있었을 때를 처음부터 말해주세요"(실제 행동), "다른 방법은 뭘 써보셨어요?"(문제의 절실함 측정).
- 원칙: **문제는 고객의 소유, 해결책은 만드는 사람의 소유.** 인터뷰는 사실 수집이지 아이디어 승인 투표가 아니다 ([Mom Test 요약 PDF](https://inkubator.si/wp-content/uploads/2020/05/The-Mom-Test-by-@robfitz.pdf)).

**하네스 관점 (load-bearing)**: "다른 방법은 뭘 써보셨어요?"는 특히 강력하다 — 아무것도 안 해봤다면 그 문제는 해결할 만큼 아프지 않은 것이다. 비개발자 사용자의 "이런 앱 만들어줘"에도 동일하게 적용된다.

### 1.2 문제 좁히기 — Shape Up의 "진짜 뭐가 문제죠?"

Basecamp Shape Up은 원시 아이디어(raw idea)에 대한 기본 반응을 "흥미롭네요. 언젠가는요(Interesting. Maybe some day)"로 규정하고, 요청을 액면 그대로 받지 말고 "**진짜로 뭐가 안 되고 있죠?**"를 파고들라고 한다. 캘린더 요청 사례: 실제 필요는 '종합 캘린더'가 아니라 '빈 시간 보기'였고, 이 구체화 덕에 작은 appetite 안에 들어가는 해법이 가능해졌다 ([Shape Up Ch.3](https://basecamp.com/shapeup/1.2-chapter-03)).

### 1.3 해결책 전에 성공 기준 — Outcome 우선

- Teresa Torres의 **Opportunity Solution Tree**: 맨 위에 원하는 outcome(성과) 하나 → 그 아래 고객 opportunity(문제/니즈) → 해결책 후보 → 가정 테스트. 성과가 먼저 있어야 어떤 기회가 유관한지 판단할 수 있고, feature factory식 로드맵을 막는다 ([producttalk.org](https://www.producttalk.org/opportunity-solution-trees/)).
- Lenny Rachitsky의 템플릿 분석에서도 최상위 공통점은 "**문제 진술을 정확히 하는 것이 모든 문제 해결의 단 하나 가장 중요한 단계**"이며, 엘리트 템플릿(Intercom, Asana, Shape Up, 1-pager)은 전부 문제 이해와 솔루션 설계를 분리한다 ([Lenny's Newsletter](https://www.lennysnewsletter.com/p/prds-1-pagers-examples), [분석](https://www.prodmgmt.world/blog/prd-template-guide)).

### 1.4 Amazon Working Backwards / PR-FAQ

출시가 끝난 미래 시점의 **가짜 보도자료 1쪽 + FAQ**를 먼저 쓴다. 고객 언어로 "고객이 누구인가, 무슨 문제를 풀며, 왜 놀라운가"에 답하지 못하면 — 즉 보도자료가 고객을 설레게 하지 못하면 — 엔지니어를 붙이기 전에 아이디어를 재작업하거나 죽인다 ([workingbackwards.com](https://workingbackwards.com/concepts/working-backwards-pr-faq-process/), [ProductPlan](https://www.productplan.com/glossary/working-backward-amazon-method)). "존재하기 전에 왜 중요한지 설명 못 하면 만들지 말라"는 필터.

### 1.5 GitLab의 검증 트랙

GitLab 핸드북은 문제가 불명확할 때 Build 트랙과 분리된 **Validation 트랙**을 돌리며, 산출물은 **Opportunity Canvas**(문제, 대상 사용자, 가설, 확신 수준을 담는 1장짜리 캔버스)다. 검증 단계의 목표는 "문제에 대한 명확한 이해와, 그것을 이해관계자에게 전달할 단순한 방법" ([GitLab handbook](https://handbook.gitlab.com/handbook/product/product-processes/), [problem validation](https://handbook.gitlab.com/handbook/product/ux/ux-research/problem-validation-and-methods/)).

**Load-bearing vs ceremony**: 문제 진술·타깃 사용자·성공 기준은 load-bearing. 캔버스라는 '양식' 자체, 인터뷰 횟수 쿼터 같은 것은 ceremony — 솔로 규모에선 한 문단으로 충분하다.

---

## 2. PRD의 실전 — 얇아진 문서

### 2.1 현대 lean PRD에 실제로 들어가는 것

Lenny Rachitsky가 수집한 실제 기업 템플릿(Square Kevin Yien, Asana, Intercom, Figma 등)의 공통 요소 ([Lenny's Newsletter](https://www.lennysnewsletter.com/p/prds-1-pagers-examples), [템플릿 모음 분석](https://www.prodmgmt.world/blog/prd-template-guide)):

1. **문제 진술** — 문서 상단에 강한 몇 문장으로. (1위 공통 요소)
2. **Non-goals / No-gos** — 안 할 것의 명시. (2위 공통 요소; Square 템플릿과 Shape Up 피치가 특히 강조)
3. **성공의 정의** — 구체적으로 무엇이 성공인지. 트레이드오프 판단의 기준이 된다.
4. **타임라인/사이즈** — 긴박감 유지와 범위 폭발 방지.
5. 솔루션 개요, 단계별 흐름 — 상세 사양이 아니라 방향.

### 2.2 1-pager vs 풀 PRD

- 기본값은 **1-pager**: 문제, 대상, 성공 기준, 제안 방향, non-goals. Lenny 본인의 선호 템플릿도 1-pager다 ([Lenny's templates](https://www.lennysnewsletter.com/p/my-favorite-templates-issue-37), [Confluence판](https://www.atlassian.com/software/confluence/templates/lennys-product-requirements)).
- 풀 PRD는 이해관계자가 많고(법무·마케팅·플랫폼팀), 실패 비용이 크고, 비동기 정렬이 필요할 때. Figma류의 "종합 템플릿"이 이 용도 ([같은 출처](https://www.lennysnewsletter.com/p/prds-1-pagers-examples)).
- **건너뛰는 경우**: 문제가 자명하고 팀이 작고 대화로 정렬이 되면 PRD 없이 이슈/피치 하나로 간다. Basecamp는 PRD 대신 6주 appetite에 맞춘 **피치(pitch)** 문서 하나만 쓴다 — 5가지 재료: 문제(현상 유지가 왜 안 되는지 보여주는 **구체적 스토리 하나**), appetite, 러프한 솔루션, rabbit holes(빠질 함정 명시), no-gos ([Shape Up Ch.6](https://basecamp.com/shapeup/1.5-chapter-06)).

**Load-bearing vs ceremony**: load-bearing은 문제 진술 + 성공 기준 + non-goals + rabbit holes. ceremony는 경쟁 분석 슬라이드, 페르소나 문서, 승인란, 장문의 배경 설명 — 큰 조직의 정치적 정렬용이며 작은 팀에선 삭제 대상.

---

## 3. Design Doc / RFC / ADR — 엔지니어링의 결정 기록

### 3.1 Google Design Docs

Google 문화의 정리 ([Design Docs at Google, Malte Ubl](https://www.industrialempathy.com/posts/design-docs-at-google/)):

- **구성**: Context와 scope / Goals와 non-goals / 설계(트레이드오프 강조) / **검토한 대안과 기각 이유** / Cross-cutting concerns(보안·프라이버시·관측성). 시스템 컨텍스트 다이어그램, API 스케치 포함.
- **핵심 철학**: "엔지니어의 일은 코드 생산이 아니라 문제 해결이다." 문서의 존재 이유는 **변경이 싼 시점에 문제를 조기 발견**하는 것.
- **쓸 때**: 설계가 모호하거나, 조직적 합의가 필요하거나, cross-cutting concern이 자주 누락되는 팀일 때.
- **안 쓸 때 (중요)**: 해법이 자명하고 트레이드오프가 적을 때, 문서가 '구현 매뉴얼'이 될 때, 문제를 아직 몰라서 프로토타이핑이 먼저일 때.
- 길이: 큰 프로젝트 10–20쪽, 증분 개선은 1–3쪽 "미니 design doc"도 유효.

### 3.2 RFC 문화 — 회사별 스펙트럼

Pragmatic Engineer의 80+개사 조사 ([RFCs and Design Docs](https://blog.pragmaticengineer.com/rfcs-and-design-docs/)):

- Uber(SLA·롤아웃·멀티 DC 섹션), Stripe, Spotify("RFC/ADR이 문화에 내장 — 조직 개편 같은 비기술 변화에도 사용") 등 대부분의 빅테크가 사용. 눈에 띄는 예외는 Meta.
- 경량 극단: Sourcegraph는 5개 섹션(Summary, Background, Problem, Proposal, **Definition of Success**)뿐.
- 리뷰 모델: 전면 공개 리뷰(Sourcegraph, Zapier) ↔ 지정 승인자 서명 ↔ 선택적 적용. 규모가 클수록 의무화 경향.
- 핵심 인용(Stedi): "문서를 쓰는 것은 요구사항과 가정을 표면화하고 추론을 명료하게 만드는 방법이다."

### 3.3 ADR (Architecture Decision Records)

Michael Nygard의 원전 ([Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions), [adr.github.io](https://adr.github.io/)):

- 형식 5개: **Title / Context(중립적으로 기술한 힘들) / Decision("We will...") / Status / Consequences(긍정·부정 모두)**. 1–2쪽.
- 동기: "프로젝트에서 가장 추적하기 어려운 것은 특정 결정 뒤의 동기다." 맥락 없는 신규 멤버는 결정을 맹목적으로 수용(정체)하거나 맹목적으로 뒤집는다(파손).
- 코드와 같은 리포지토리에 보관. "큰 문서는 절대 최신으로 유지되지 않는다. 작고 모듈화된 문서라야 갱신될 가능성이라도 있다." 번호는 재사용하지 않고, 뒤집힌 결정은 삭제 대신 superseded로 표시.

**Load-bearing vs ceremony**: load-bearing은 "검토한 대안 + 기각 이유 + 결과"의 기록 — 이것이 미래의 자신/에이전트가 결정을 안전하게 뒤집을 수 있게 한다. ceremony는 승인 위원회, 무거운 템플릿 강제. 솔로 규모에선 ADR이 design doc보다 오래 살아남는 형식이다(짧고, 리포지토리에 있고, 갱신 부담이 없어서).

---

## 4. 작업 분해: 에픽 → 스토리 → 태스크

### 4.1 유저 스토리의 본질 — 문서가 아니라 대화

Mike Cohn ([mountaingoatsoftware.com/agile/user-stories](https://www.mountaingoatsoftware.com/agile/user-stories)):

- 템플릿: "**As a <사용자>, I want <목표> so that <이유>**". 형식 자체보다 요구사항을 '쓰는 것'에서 '논의하는 것'으로 초점을 옮기는 게 목적.
- **3C: Card(계획용 메모) / Conversation(디테일을 채우는 대화) / Confirmation(완료 판정 테스트)**. 스토리는 "미래 대화의 자리표시자"다.
- 에픽은 큰/덜 상세한 스토리이며, 착수 전에 한 이터레이션에 들어갈 크기의 스토리들로 분해된다. 디테일 추가 방법은 두 가지: 스토리 분할, 또는 **conditions of satisfaction(인수 기준)** 추가.

### 4.2 INVEST 기준

Bill Wake, 2003 원전 ([xp123.com](https://xp123.com/articles/invest-in-good-stories-and-smart-tasks/)):

- **I**ndependent(순서 무관하게 잡을 수 있게) / **N**egotiable("좋은 스토리는 본질을 담지 디테일을 담지 않는다") / **V**aluable(개발자가 아니라 고객에게 가치) / **E**stimable(상대 크기를 가늠할 만큼은 이해) / **S**mall / **T**estable("**테스트를 쓸 수 있을 만큼 원하는 걸 이해했다**").
- 태스크는 SMART(Specific, Measurable, Achievable, Relevant, Time-boxed).
- **하네스 관점**: 6개 중 가장 load-bearing한 것은 V와 T다. V가 없으면 수평 슬라이스(인프라만 만드는 스토리)가 생기고, T가 없으면 "완료" 주장을 검증할 수 없다.

### 4.3 인수 기준 형식: Given/When/Then vs 체크리스트

- **Given/When/Then**: BDD(Dan Terhorst-North, Chris Matts)에서 유래. Given=사전 조건, When=검증할 행동, Then=기대 결과. 비즈니스 이해관계자도 읽을 수 있으면서 실행 가능한 테스트(Cucumber 등)로 이어지는 "specification by example" ([Martin Fowler, GivenWhenThen](https://martinfowler.com/bliki/GivenWhenThen.html)).
- **체크리스트**("~하면 완료"): 형식은 가볍고 대부분의 팀이 실제로 쓰는 방식. Cohn의 conditions of satisfaction이 이 형태 ([Mountain Goat](https://www.mountaingoatsoftware.com/agile/user-stories)).
- 실무 판단: 형식은 ceremony, **검증 가능성이 load-bearing**. GWT는 (a) 상태 의존적 동작, (b) 자동화 테스트로 직결할 때 가치가 있고, 단순 기능엔 체크리스트가 오버헤드가 적다.

### 4.4 수직 슬라이싱 — 분해의 황금률

Richard Lawrence / Humanizing Work 가이드 ([splitting user stories](https://www.humanizingwork.com/the-humanizing-work-guide-to-splitting-user-stories/)):

- 좋은 스토리는 **수직 슬라이스**: 가치 전달에 필요한 만큼 모든 아키텍처 레이어를 관통. 수평 슬라이스(DB만, API만, UI만)는 단독으로 아무 가치도 없고 조율 비용만 낳는다.
- 9가지 분할 패턴: 워크플로 단계(전체 흐름의 단순판 먼저) / CRUD 연산 분리 / 비즈니스 룰 변형 분리 / 데이터 변형 / 입력 방식(단순 UI 먼저) / 대규모 공수 분리 / 단순/복잡(엣지케이스 유예) / 성능 유예(일단 동작 먼저) / 스파이크 분리(불확실성 연구).
- 좋은 분할의 조건: 저가치 조각을 **버릴 수 있게** 만들 것, 조각 크기가 비슷할 것, INVEST 유지.

### 4.5 스토리 매핑 — 평평한 백로그의 해독제

Jeff Patton ([jpattonassociates.com/story-mapping](https://www.jpattonassociates.com/story-mapping/)):

- "사용자의 여정을 이야기하며 그 이야기를 모델로 만든다"는 단순한 아이디어. 가로축 = 사용자의 활동 순서(backbone), 세로축 = 우선순위/릴리스.
- 평평한 백로그의 문제: 전체 그림이 없어서 팀이 "기능 논쟁에 매몰"되고, 릴리스를 사용자 경험 단위가 아니라 기능 목록 단위로 자르게 된다.
- 릴리스 슬라이싱: 지도를 가로로 잘라 "이 줄까지가 첫 릴리스" — 각 릴리스가 여정 전체를 관통하는 얇은 경험이 되게 한다.

### 4.6 Walking Skeleton / Tracer Bullet / Steel Thread — 첫 슬라이스의 기술

- **Walking skeleton** (Alistair Cockburn): "자동으로 빌드·배포·엔드투엔드 테스트 가능한, 실제 기능의 가장 얇은 조각의 구현". 실 기능 전에 **전달 파이프라인 전체가 작동함을 증명**한다 ([Code Climate](https://codeclimate.com/legacy/kickstart-your-next-project-with-a-walking-skeleton), [defmyfunc](https://www.defmyfunc.com/2019_10_18_walking_skeleton/)).
- **Tracer bullet** (Pragmatic Programmer): UI→비즈니스 로직→DB까지 한 줄기 실행 경로를 먼저 뚫는다. 예광탄이 빗나가면 조정해서 다시 쏜다 — 얇게 만들었기에 조정 비용이 낮다 ([Artima 인터뷰](https://www.artima.com/intv/tracerP.html)).
- **Steel thread**: 같은 계열의 용어로, 시스템의 핵심 유스케이스 하나를 관통하는 얇은 엔드투엔드 구현을 먼저 세우고 거기에 살을 붙이는 접근 ([Jim Newbery 정리](https://tinnedfruit.com/list/20180815)).
- **하네스 관점 (매우 load-bearing)**: 이 셋은 사실상 같은 원칙 — "통합·배포 리스크를 프로젝트 첫날 소진하라". 에이전트가 앱을 만들 때 "모든 화면의 스캐폴드"가 아니라 "핵심 시나리오 하나가 끝까지 도는 것"을 1번 마일스톤으로 삼아야 한다는 뜻.

---

## 5. 스코핑과 순서 결정

### 5.1 MVP — 원래 의미와 왜곡

- Eric Ries의 원의: MVP는 **build-measure-learn 루프의 첫 단계**이자 validated learning("극단적 불확실성 속에서 진전을 입증하는 엄밀한 방법")의 도구다. 제품 1.0이 아니라 학습 장치 ([theleanstartup.com/principles](http://theleanstartup.com/principles)).
- 흔한 왜곡: "허접한 첫 릴리스"의 별칭이 되어, 테스트라기엔 너무 크고 제품이라기엔 너무 조악한 것을 만들게 됨 ([Rik Higham](https://hackernoon.com/the-mvp-is-dead-long-live-the-rat-233d5d16ab02)).
- 교정 1 — **RAT (Riskiest Assumption Test)**: "MVP라는 말의 결함은 그것이 제품이 아니라는 것. 가장 위험한 가정을 찾아 그것을 테스트하는 데 필요한 것 이상은 만들지 말라" ([The MVP is dead. Long live the RAT.](https://medium.com/hackernoon/the-mvp-is-dead-long-live-the-rat-233d5d16ab02)). 순서 결정 원칙: **가장 위험한 가정 먼저**.
- 교정 2 — Henrik Kniberg의 **Earliest Testable → Usable → Lovable Product**: 유명한 스케이트보드→자전거→오토바이→자동차 그림. 요점은 '미니멈'이 아니라 '**가장 이른 피드백**'. 바퀴 하나(수평 슬라이스)가 아니라 스케이트보드(불완전해도 타지는 것)를 먼저 ([Making sense of MVP, Crisp blog](https://blog.crisp.se/2016/01/25/henrikkniberg/making-sense-of-mvp)).

### 5.2 Shape Up: Appetite — 추정의 역전

- **Appetite = 추정이 아니라 시간 예산.** "추정은 설계에서 시작해 숫자로 끝난다. Appetite는 숫자에서 시작해 설계로 끝난다." 이 기능에 조직 자원을 얼마나 쓸 가치가 있는지를 먼저 정하고, 그 안에 들어가는 해법을 설계한다 ([Shape Up Ch.3](https://basecamp.com/shapeup/1.2-chapter-03)).
- **Fixed time, variable scope**: 고정된 마감이 창의적 제약이 되어 품질-범위 트레이드오프를 강제한다.
- **Scope hammering**: 이상(ideal)이 아니라 **현재의 고객 현실(baseline)과 비교**하며 "이게 정말 필수인가? 없이 출시하면 무슨 일이 나나?"를 반복해 범위를 두들겨 깎는다. Nice-to-have는 ~표시만 하고 보통 영영 출시되지 않는다. "**범위를 자르는 것은 품질을 낮추는 게 아니다. 선택이 제품을 특정 부분에서 더 낫게 만든다**" ([Shape Up Ch.14](https://basecamp.com/shapeup/3.5-chapter-14)).
- **Circuit breaker**: 사이클 안에 못 끝낸 프로젝트는 자동 연장되지 않는다. 이는 shaping 실패의 신호이며, 시간을 더 주는 게 아니라 다시 생각해야 한다는 뜻 ([Shape Up Ch.8](https://basecamp.com/shapeup/2.2-chapter-08)). 연장은 남은 게 전부 진짜 must-have이고 전부 "내리막"(완전히 이해된 실행만 남은) 작업일 때만.
- **Bets, not backlogs**: 백로그는 가짜 가시성과 무한한 할일 축적을 낳는다. 사이클마다 잘 shaped된 소수의 베팅만 검토 ([Shape Up Ch.7-8](https://basecamp.com/shapeup/2.2-chapter-08)).

### 5.3 Iteration vs Increment — Patton의 모나리자

- **Incremental**: 모나리자를 손부터 완벽하게, 다음 팔, 다음 얼굴… 전체 그림은 맨 끝에야 보인다.
- **Iterative**: 먼저 연필 스케치 전체 → 채색 → 디테일. 처음부터 전체 그림이 보이고 방향을 조정할 수 있다.
- 실무는 둘의 결합(iterative + incremental)이 정답이며, 순수 incremental은 "조각 단위 폭포수"가 되기 쉽다 ([정리 1](https://itsadeliverything.com/revisiting-the-iterative-incremental-mona-lisa), [정리 2](https://blackswanfarming.com/iterations-vs-increments-mona-lisa-and-mr-fox/)).
- 순서 결정 종합: **① 가장 위험한 가정 → ② walking skeleton → ③ 가치 순 수직 슬라이스 → ④ scope hammering으로 마감 사수**.

---

## 6. 추정의 현실

### 6.1 왜 실패하는가

- **불확실성의 원뿔(Cone of Uncertainty)**: 프로젝트 초기의 추정은 잘 해도 **4배 범위**(4주짜리가 1주일 수도 16주일 수도)로 빗나간다. 이는 최선의 경우이고, 프로젝트가 변동성을 줄이도록 운영되지 않으면 원뿔이 아니라 끝까지 좁혀지지 않는 "구름"이 된다 ([Steve McConnell/Construx](https://www.construx.com/books/the-cone-of-uncertainty/), [Coding Horror](https://blog.codinghorror.com/the-mysterious-cone-of-uncertainty/)).
- 근본 원인: 추정은 "무엇을 만들지 안다"를 전제하는데, 소프트웨어 작업은 본질적으로 novel하고 요구사항은 계속 모호하다. 게다가 추정치는 "프로그래머를 더 빨리 일하게 하는 몽둥이"로 오용되고, 고정 범위에 대한 집착을 낳는다 ([Ron Jeffries, The NoEstimates Movement](https://ronjeffries.com/xprog/articles/the-noestimates-movement/)).

### 6.2 팀이 실제로 하는 것

- **T-shirt sizing**: 초기 단계·큰 단위에서 XS–XXL 상대 크기만 잡는다. 숫자의 거짓 정밀도를 피하는 용도 ([Asana 가이드](https://asana.com/resources/t-shirt-sizing)).
- **NoEstimates / 흐름 기반**: 추정 대신 작업을 작게 썰어 연속 흐름으로 배달하고, 예측이 필요하면 실측 **cycle time** 데이터를 쓴다. 단 Jeffries 본인도 절대주의를 경계 — 고객이 비용 추정을 요구하는 현실 문제는 남는다 ([ronjeffries.com](https://ronjeffries.com/xprog/articles/the-noestimates-movement/)).
- **날짜가 아니라 범위를 자른다**: Shape Up의 appetite + scope hammering + circuit breaker가 가장 체계화된 형태. 마감은 고정, 협상 대상은 범위 ([Shape Up Ch.14](https://basecamp.com/shapeup/3.5-chapter-14)).

**Load-bearing vs ceremony**: load-bearing은 "시간 상한을 먼저 정하고 범위를 그에 맞춘다"는 역전, 그리고 상대 크기 감각(이건 반나절짜리 vs 이건 몇 주짜리). ceremony는 플래닝 포커, 스토리 포인트 정산, 번다운 차트 — 대규모 조직의 조율 장치이지 산출물의 품질과는 무관.

---

## 7. 솔로 빌더 / 초소형 팀으로의 스케일 다운

### 7.1 살아남는 산출물 (load-bearing 코어)

위 관행들의 공통 분모를 개인 규모로 압축하면:

1. **문제 한 문단 + 성공 기준** — Mom Test식으로 검증된 실제 문제, "무엇이 참이면 성공인가". (Shape Up 피치의 문제+구체적 스토리, Sourcegraph RFC의 Definition of Success에 해당)
2. **Non-goals** — 모든 엘리트 템플릿의 2위 공통 요소는 규모와 무관하게 유효하다. 범위 폭발은 솔로에게 더 치명적이다 ([prodmgmt.world 분석](https://www.prodmgmt.world/blog/prd-template-guide)).
3. **인수 기준(체크리스트면 충분)** — "테스트를 쓸 수 있을 만큼 이해했는가"(INVEST의 T)가 유일한 완료 판정 수단.
4. **첫 마일스톤 = walking skeleton** — 얇은 엔드투엔드 슬라이스로 통합 리스크 조기 소진.
5. **Appetite** — "이 기능에 이틀 이상 안 쓴다"는 시간 예산. 추정 대신.
6. **짧은 결정 기록(ADR-lite)** — 리포지토리 안의 몇 줄짜리 "왜 이렇게 했나". Nygard의 통찰("작은 문서만 갱신될 가능성이 있다")은 솔로에서 더 강하게 성립 ([cognitect](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)).

### 7.2 죽는 산출물 (조직 조율용 ceremony)

- 풀 PRD, 승인 워크플로, 위원회식 RFC 리뷰 — 존재 이유가 '다수 이해관계자의 비동기 정렬'이므로 이해관계자가 1–2명이면 소멸.
- 스토리 포인트, 플래닝 포커, 벨로시티/번다운 — 팀 간 조율·보고 장치.
- 백로그 관리 — Shape Up의 지적("가짜 가시성, 무한 축적")은 솔로에서 특히 맞다. 베팅할 소수만 남기고 버린다 ([Shape Up](https://basecamp.com/shapeup/2.2-chapter-08)).
- 스펙 문서화의 손익분기 원칙: "스펙이 여러 PR·여러 서비스·여러 사람(또는 에이전트)에 재사용되면 비용을 회수한다. 한 번 읽히고 말 문서라면 회수하지 못한다" — design doc을 쓸 일이었으면 스펙을 쓰고, 아니면 생략 ([Microsoft, Spec-Driven Development](https://developer.microsoft.com/blog/spec-driven-development-ai-native-engineering/), [소규모 팀 적용 논의](https://lumo-mate.com/blog/en/spec-driven-development-small-teams-2026)).

### 7.3 AI 에이전트 하네스에 대한 시사점

비개발자의 막연한 요청을 프로의 스펙으로 바꾸는 최소 파이프라인은 위 관행의 직역이다:

1. **인터뷰는 Mom Test 규칙으로**: 사용자의 아이디어 승인("이렇게 만들까요? 좋죠?")이 아니라 과거의 구체적 행동·현재의 대안·절실함을 캐묻는다. "지금은 이 문제를 어떻게 처리하세요?"가 스펙의 씨앗.
2. **스펙 4요소**: 문제(구체적 스토리 1개) / 성공 기준(검증 가능한 형태) / non-goals / 인수 기준 체크리스트. 여기에 appetite(시간 예산)와 rabbit holes(예상 함정)를 더하면 Shape Up 피치와 동형이 된다.
3. **계획은 수직 슬라이스 + 위험 우선**: 1번 작업은 항상 walking skeleton. 이후 슬라이스는 "버릴 수 있는가"로 검증. 수평 슬라이스(모델 전부 → API 전부 → UI 전부)는 하네스가 명시적으로 금지해야 할 안티패턴.
4. **추정 대신 appetite + scope hammering**: 에이전트가 "얼마나 걸릴까"를 약속하는 대신, 시간/시도 예산을 넘기면 circuit breaker처럼 멈추고 범위 재협상을 사용자에게 되돌린다.
5. **결정은 ADR-lite로 리포지토리에**: 미래 세션의 에이전트(=신규 팀원과 동일한 처지)가 결정을 맹목적으로 뒤집지 않게 하는 유일한 장치.

---

## 부록: 핵심 원전 목록

| 주제 | 원전 |
|---|---|
| 문제 심문 | [The Mom Test](https://www.momtestbook.com/) · [Shape Up Ch.3](https://basecamp.com/shapeup/1.2-chapter-03) · [Opportunity Solution Tree](https://www.producttalk.org/opportunity-solution-trees/) · [Amazon PR/FAQ](https://workingbackwards.com/concepts/working-backwards-pr-faq-process/) |
| PRD | [Lenny's PRD/1-pager 모음](https://www.lennysnewsletter.com/p/prds-1-pagers-examples) · [Shape Up 피치 Ch.6](https://basecamp.com/shapeup/1.5-chapter-06) · [GitLab Product Processes](https://handbook.gitlab.com/handbook/product/product-processes/) |
| Design Doc/RFC/ADR | [Design Docs at Google](https://www.industrialempathy.com/posts/design-docs-at-google/) · [Pragmatic Engineer RFC 조사](https://blog.pragmaticengineer.com/rfcs-and-design-docs/) · [Nygard ADR](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) |
| 작업 분해 | [Cohn 유저 스토리](https://www.mountaingoatsoftware.com/agile/user-stories) · [Wake INVEST](https://xp123.com/articles/invest-in-good-stories-and-smart-tasks/) · [Fowler GWT](https://martinfowler.com/bliki/GivenWhenThen.html) · [스토리 분할 가이드](https://www.humanizingwork.com/the-humanizing-work-guide-to-splitting-user-stories/) · [Patton 스토리 매핑](https://www.jpattonassociates.com/story-mapping/) |
| 스코핑 | [Kniberg MVP](https://blog.crisp.se/2016/01/25/henrikkniberg/making-sense-of-mvp) · [Higham RAT](https://hackernoon.com/the-mvp-is-dead-long-live-the-rat-233d5d16ab02) · [Lean Startup 원칙](http://theleanstartup.com/principles) · [Shape Up Ch.14](https://basecamp.com/shapeup/3.5-chapter-14) |
| 추정 | [Cone of Uncertainty](https://www.construx.com/books/the-cone-of-uncertainty/) · [Jeffries NoEstimates](https://ronjeffries.com/xprog/articles/the-noestimates-movement/) |
