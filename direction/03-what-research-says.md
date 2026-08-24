# 03 — 리서치는 무엇을 말하는가

> 갱신 2026-08-25 · rev2 · 근거는 전부 `corpus/`에 있다. 여기는 **방향에 걸리는 것만** 추린 색인이다.
> **하중 18건 재검증(프로그램 #49) 배치 1~5 완료** — 판정은 각 항목에 인라인으로 붙어 있다.

## 현업 팀이 실제로 하는 것 — 10줄

> ⚠️ **출처 재지정 (2026-08-24 · Fable 5 적대 검수 지적)**
> 이 절의 첫 판은 [`legacy/judgments/research-interpretation/02-engineering-practices.md`](../legacy/judgments/research-interpretation/02-engineering-practices.md)를
> 출처로 적었는데, 그 문서 1행에 ***"활성 근거로 인용하지 않는다"*** 배너가 붙어 있다
> (`legacy/README` 인용 규칙 2와도 충돌). **현행 코퍼스로 재지정했고, 코퍼스에 없는 수치는 그렇게 표시했다.**
>
> | 출처 | status | 무엇을 받치나 |
> |---|---|---|
> | [`05-scm-workflow--overview.md`](../corpus/aspects/05-scm-workflow/05-scm-workflow--overview.md) | `review-needed` | trunk ≤3·매일 통합 · 브랜치보호 10~13% · 리뷰강제 41% · T3(훅은 게이트 아님) |
> | [`07-...--overview.md`](../corpus/aspects/07-construction-code-review/07-construction-code-review--overview.md) · [`codereview--facts-2026-08.md`](../corpus/aspects/07-construction-code-review/codereview--facts-2026-08.md) | `review-needed` / `draft` | 리뷰 필수·경량·빠름 · CL ~100줄 · **400 LOC 임계** · 생성코드 동일 게이트 |
> | [`cicd-release--facts-2026-08.md`](../corpus/aspects/04-build-ci-engineering/cicd-release--facts-2026-08.md) | `draft` | **10분 빌드**(Fowler 1차 URL) · CI 실무 |
> | ✅ **2026-08-24 재검증 완료(배치 A)** | `codereview--facts` **CR-005~008** | **중앙값 24줄**=유지 · **4시간**=수정(응답→전 과정 지연) · **DORA 50%**=삭제(출처 없음) · **"다중 승인자·체크리스트 DORA 안티패턴"**=삭제(오귀속) |
> | ✅ **2026-08-24 재검증 완료(배치 B)** | `github-workflow-current` **GHW-008·009** | **Git Flow 2020 note**=출처 부착(미승계가 아니었다) · **"브랜치 다이어그램은 ceremony"**=프로젝트 판단으로 재분류(연구 결과 아님) |
> | ✅ **2026-08-24 재검증 완료(배치 C)** | `testing--facts` **TDD-001·002** · `17 overview` **REL-001·002** | **TDD 순서**=유지(1차 출처 부착 + 표본 한정) · **feature flag 부채**=한정 추가(*"carrying cost"* 이지 부채가 아니다) |
>
> **아직 안 옮긴 것**: Git Flow 창시자의 2020 note · 테스트 피라미드 80/15/5 · TDD 순서 효과 ·
> feature flag 부채. `audit/GAPS.ko.md` R5-1에 등재했다.

1. 고성과의 공통분모는 브랜치 모델이 아니라 **"작게, 자주, 빨리 통합"** — 활성 브랜치 ≤3, 하루 1회 머지, **브랜치 수명 몇 시간** ✅ **2026-08-25 1차 출처 직접 확인**(`github-workflow-current` **GHW-010**): 세 수치 전부 dora.dev 원문 그대로다 — *"three or fewer active branches"* · *"Merge branches to trunk at least once a day"* · *"branches … typically last no more than a few hours"*. ⚠️ **단 근거는 페이지 자신이 밝히듯 *"Analysis of DORA data from 2016 and 2017"*, 즉 설문 분석의 상관 진술**이지 저장소 계측이 아니다
2. Git Flow는 **창시자가 2020년에 웹앱에 비추천**했다 — ✅ **2026-08-24 1차 출처 확인**(`github-workflow-current` **GHW-008**). 단 **전면 철회가 아니라 범위 한정**이다: *"명시적으로 버전이 붙는 소프트웨어·다중 버전 지원에는 여전히 맞을 수 있다"*
3. **리뷰는 빨라야 한다** — Google 응답 규범 1영업일. ⚠️ **2026-08-24 재검증**: *"빠른 팀이 배포 성과 50% 높음"* 은 **1차 출처에서 찾을 수 없어 삭제**했다(`codereview--facts` **CR-007**). 그리고 실측 *"중앙값 4시간"* 은 **응답 시간이 아니라 전체 리뷰 과정의 지연**이다 — 첫 피드백은 소형 1시간 미만·대형 약 5시간(**CR-006**)
4. 리뷰의 전제는 **작은 변경** — Google 중앙값 **24줄**, 100줄 적정 / 1000줄 과대, **200줄 목표 · 400줄 상한**(⚠️ 2026-08-24 재검증 — *"급락"* 은 원문에 없다. `codereview--facts` CR-001~003)
5. 진짜 CI = 메인라인 + 자동빌드 + 자기검증 테스트 + **10분 이내** + **깨지면 즉시 수리**. *"이것이 없으면 나머지는 장식이다"*
6. Delivery ≠ Deployment. feature flag 는 **보유 비용(carrying cost)** 을 갖는다 — ⚠️ **2026-08-24 재검증**: 원문은 *"부채"* 가 아니라 *"inventory which comes with a carrying cost"* 라 하고, **토글 수명별로 구분**한다 (Permissioning 은 수년 존속이 설계 의도). *"feature flag = 부채"* 는 과일반화였다 (`17 overview` **REL-001·002**)
7. 테스트 피라미드 — Google 실측 80/15/5
8. **TDD 의 "테스트 먼저" 순서(sequencing)는 영향이 없었다** — ✅ **2026-08-24 1차 출처 확인**: *"Sequencing… had no important influence"*, 효과의 원천은 ***granularity 와 uniformity*** (잘게·균일한 사이클)다 (`testing--facts` **TDD-001**). ⚠️ 표본은 **전문 개발자 39명 · 82 데이터 포인트** — *"순서는 무의미하다"* 가 아니라 *"이 연구는 순서의 영향을 발견하지 못했다"* 로 쓴다 (**TDD-002**)
9. **"Done" = 머지 전 CI 녹색** ⚠️ **2026-08-24 재검증**(`28 overview` **IPW-011~013**): Scrum 은 DoD 의 **내용을 규정하지 않는다** — *"quality measures required for the product"* 까지다. 실증 근거는 따로 있다(DoD 24개·항목 143개 분석: **테스트 16/24 · 코드리뷰 13/24**, 단 편의표집). **그리고 이 저장소의 룰셋은 `required_approving_review_count: 0` 이라 "리뷰 승인" 이 요구되지 않는다** — 이전 판의 정의는 실제 룰셋과 어긋나 있었다
10. Conventional Commits 같은 형식 규약은 **자동화가 소비할 때만** 가치 — 아니면 cargo cult

### 하중을 받는 것 vs 의식(ceremony)

> 하중을 받는 것은 *"브랜치 수명 단축 + 매일 통합"이라는 **행동**"* 이지 모델의 이름이 아니다.
>
> ⚠️ **2026-08-24 재검증 — 두 부분을 갈랐다.**
> **앞 문장(행동이 하중을 받는다)은 리서치가 받친다**: DORA 의 *"≤3 active branches · 하루 1회 이상 trunk 병합"*
> ([`05 overview`](../corpus/aspects/05-scm-workflow/05-scm-workflow--overview.md)). 단 그 수치는 **설문 자기보고**이지
> 저장소 계측이 아니다(`github-workflow-current` **GHW-009**, 2026-08-25 **GHW-010** 으로 1차 확인 승격).
>
> **뒷 문장(*"브랜치 다이어그램을 정교하게 그리는 것 자체는 ceremony다"*)은 리서치가 아니다** —
> *"다이어그램을 그리는 행위"* 를 측정한 연구를 찾지 못했다. **프로젝트 판단으로 재분류**한다.
> `EVIDENCE-POLICY` 가 이름 붙인 범주 오류가 *"disguising author judgment as fact"* 다.
>
> ⚠️ **2026-08-24 재검증으로 삭제됨.** 이전 판은 *"다중 필수 승인자·형식적 체크리스트 채우기는 DORA가 명시한 안티패턴"* 이라 적었으나 **DORA 가 한 말이 아니다.** DORA 가 비판한 것은 **CAB·고위 관리자 등 팀 외부의 중량급 변경 승인**이고, 오히려 **팀 내 동료 리뷰를 권장**한다. 동료 리뷰의 승인자 수와 체크리스트는 DORA 범위 밖이다 (`codereview--facts` **CR-008**).
>
> 🔴 **2026-08-25 배치 5 — 이 삭제를 부분 복원했다.** *"다중 승인자"* 절반에는 **DORA 출처가 있다** —
> **trunk-based-development 역량 페이지의 *Common pitfalls*** 가 *"An overly heavy code-review process …
> **requires multiple approvals** before changes can be merged into trunk"* 을 **TBD 채택의 흔한 장애물**로 명시한다
> (`github-workflow-current` **GHW-011**). 다만 범위가 좁다 — ***코드리뷰 일반의 안티패턴이 아니라 trunk 기반 개발
> 채택의 장애물***이고, **체크리스트 쪽은 여전히 무출처**(해당 페이지 등장 0회)다.
> **배치 A 는 `streamlining-change-approval` 한 페이지만 보고 *"출처가 없다"* 고 적었다** — *"못 찾았다"* 와 다르다.
> 부수 확인: 같은 절이 *"Performing code reviews **asynchronously**"* 도 장애물로 들며 **동기 리뷰를 권한다.**

## 테스트는 어디에 있어야 하나 — 에이전트 코딩에서 특히 강하다

[`07 construction-code-review`](../corpus/aspects/07-construction-code-review/07-construction-code-review--overview.md) `review-needed` ·
[`08 software-testing`](../corpus/aspects/08-software-testing/08-software-testing--overview.md) `review-needed` ·
[`28 implementation-process`](../corpus/aspects/28-implementation-process-workflow/28-implementation-process-workflow--overview.md) `review-needed`

**① 테스트는 코드와 같은 변경 단위로 온다** (07, SWEBOK KA4)

> *"실패하는 테스트로 동작을 먼저 규정한다(RED→GREEN→REFACTOR). **테스트는 코드와 같은
> change-unit으로 실린다.** 지속 통합이 trunk를 항상 초록으로 유지한다."*

`04 foundation-floor`는 이를 **MUST**로 못 박는다 — *"tests required on **every PR**"*.
그리고 `08`은 test를 **우회 불가 4대 CI 검사**(lint·typecheck·**test**·build) 중 하나로 둔다.

**② ⭐ 에이전트에게는 이것이 자기평가의 대체물이다** (28)

> *"**객관 신호로 검증하고 자기평가로 하지 않는다.** 검증은 컴파일러·테스트러너·린터·타입체커 —
> **외부 진실**을 쓴다."*
>
> ✅ **2026-08-24 1차 출처 재검증 — 근거가 오히려 강해졌다** (`28 overview` **IPW-001~005**):
>
> - **외부 피드백 없는 자기교정은 성공 사례가 없다** — *"no prior work demonstrates successful self-correction
>   with feedback from prompted LLMs"* (**IPW-001**)
> - ⭐ **그러나 신뢰할 만한 외부 피드백이 있으면 잘 작동한다** — *"self-correction works well in tasks that can
>   use **reliable external feedback**"* (**IPW-002**). **이 절반이 이전 인용에서 빠져 있었다** —
>   테스트·CI 를 외부 진실로 쓰는 이 프로젝트 설계의 **가장 직접적인 근거**다
> - **내재적 자기교정은 성능을 떨어뜨리기도 한다** — 단 ⚠️ **추론 과제 한정**이고, 출처도
>   서베이가 아니라 Huang et al. 이다 (**IPW-003**, 출처 정정)
> - ⚠️ **Reflexion 인용은 방향이 반대였다** — Reflexion 은 *"자기교정이 안 된다"* 가 아니라
>   **피드백 기반 반복이 성공한다**는 논문이고, HumanEval 91% 는 **자체 생성 단위시험을 실제 실행한 신호**로
>   구동된다. 즉 **IPW-002 의 실례**다

**이것이 `direction/02` 진단이 실측한 것과 같은 형태다** — 확증시험에서 하네스의 자기평가는
*"항상 성공"* 을 보고했다. **테스트는 에이전트가 자기 작업에 대해 말하는 것을 기계 판정으로 바꾼다.**

**③ ⚠️ 다만 "테스트 먼저"라는 **순서 자체**의 효과는 불분명하다**

SUPERSEDED 문서(`legacy/judgments/research-interpretation/02-engineering-practices.md`)는
*"TDD의 순서 자체는 실증 연구상 효과가 불분명하고 현업 준수율도 낮다 — 효과의 원천은
**잘게 균일한 스텝 + 항상 테스트가 따라오는 것**"* 이라 적었다.
**코퍼스에 미승계**이므로 결정 근거로 쓰지 않는다(`GAPS` R5-1).

→ **하중을 받는 것은 "먼저"가 아니라 "함께"다.** 순서는 권고, **동반은 강제**로 나눈다.

## 게이트는 어디에 있어야 하나

[`corpus/aspects/05-scm-workflow/`](../corpus/aspects/05-scm-workflow/) — tension T3:

> **pre-commit 훅은 게이트가 될 수 없다** — `--no-verify`로 우회된다.
> **진짜 게이트는 CI + 브랜치 보호다.**
>
> ✅ **2026-08-24 git 1차 문서로 확인** (`28 overview` **IPW-005**): `--no-verify` 는
> *"bypasses the pre-commit and commit-msg hooks"*, `git push --no-verify` 는 *"the hook is bypassed completely"*.

census: 브랜치 보호가 강하게 걸린 저장소는 **10~13%**뿐이다 → *"바로 그 게이트를 기본 ON으로 켜야 한다"*
✅ **2026-08-24 원자료 재계산으로 확인** — `census-governance` 원본에서 Branch-Protection ≥8점이 **15/118 = 12.7%**. ⚠️ **분모 n=118 을 함께 읽어야 한다**: 429개 중 Scorecard 가 판정할 수 있었던 것만이고, 코퍼스가 그 한계를 *"honest coverage limit (the check needs admin/visibility)"* 로 명시한다.

⚠️ **플랜 제약**: GitHub Free에서 룰셋은 **공개 저장소에만** 적용된다. 비공개는 Pro 이상.
그리고 Actions 분은 공개 무제한 / 비공개 Free 2,000분·월
([`04-build-ci-engineering/visibility-provision-matrix.md`](../corpus/aspects/04-build-ci-engineering/visibility-provision-matrix.md) ·
[`05-scm-workflow/github-enforcement-boundaries--facts-2026-08.md`](../corpus/aspects/05-scm-workflow/github-enforcement-boundaries--facts-2026-08.md)).

## 이슈·PR은 어떻게 쓰나

[`corpus/aspects/24-governance-collaboration-compliance/issue-pr-writing-conventions.md`](../corpus/aspects/24-governance-collaboration-compliance/issue-pr-writing-conventions.md)
(census N=6,582 저장소 · 20,837 템플릿 필드)

- **이슈 우선은 크기 조건부다 — 보편 규칙이 아니다.** 사소한 변경은 바로 PR. 이슈 필수는 *방향이 불확실한* 작업에만 ✅ **재검증** — `05 overview` 원문 그대로: *"Issue-before-PR is **size-conditional, NOT universal**"*
- **이슈 제목에 커밋 규약을 걸지 마라** ✅ **2026-08-24 원자료 재계산** — 독립 표본 2개에서 재현됐다: 이슈 CC 비율 **top-2000 1% · top-500 2%**. 반면 **PR 은 33~45%**(≥70% 채택 저장소 21~34%). → *"이슈엔 안 쓰고 PR 엔 쓴다"* 는 대비가 핵심이다
- 이슈 폼: 도움말 **87%**(사실상 필수) · required는 **본문 필드에** 걸고 체크박스엔 안 건다 ✅ **원자료 재계산** — 도움말 **87.2%**(1차 패스 87.1% 와 사실상 동일 → 코퍼스가 *"a genuine population-wide floor"* 라 부른다). required 비율: textarea **57.8%** vs 체크박스 **3.4%**
- PR 템플릿: **빈 체크리스트**가 표준(62%) · 중앙값 3절 · "type of change"는 소수(11.5%)이고 **CC를 쓰면 뺀다** ✅ **원자료 재계산** — 1차 패스 62%/11.5%, **강건성 재확인 패스(N=6,582 풀)에서 63.2%/11.9%**. 중앙값 3절 동일. ⚠️ 이 절의 머리말이 *"N=6,582"* 와 1차 패스 퍼센트를 **같이 적어 패스를 섞고 있다** — 둘 다 코퍼스에 있으나 출처 패스가 다르다
- ⚠️ **이슈 폼의 `required`는 REST/CLI 경로에 걸리지 않는다** — 에이전트는 `gh issue create`를 쓴다.
  **집행은 CI 가드가 정본이다** (GEB-003·004)

## 기획은 어떻게 이끄나

[`corpus/aspects/01-requirements-planning/elicitation-interview-build-standard.md`](../corpus/aspects/01-requirements-planning/elicitation-interview-build-standard.md)
— 7개 선행연구 계열 종합

| 층 | 처방 |
|---|---|
| 질문 **스타일** | Mom Test — 유도·가정 질문 금지, **과거의 구체적 행동**에 근거, **말을 줄이고 듣는다**. ⚠️ *"80% 듣기"* 는 **1차 출처 미확인이라 내렸다**(**ELI-006**) |
| 질문 **선택** | 다음 질문 = **기대 정보이득 최대** |
| **분량** | **턴당 ≤2문항** ✅(iReDev 원문 확인 · **ELI-003**) · 🔴 위험별 깊이 **8/12/18턴** = **출처 없음, 프로젝트 판단**(**ELI-004**) · 상한 **15~20** 은 AIRE 원문에 있으나 *"생성할 **스크립트**의 목표 길이"* 다 |
| **표기법** | **EARS** — ⚠️ **패턴은 5개가 아니라 6개**이고 `WHERE`(선택 기능)가 빠져 있었다(**ELI-005**): 없음·`While`·`When`·`Where`·`If…Then`·조합 + 요구사항마다 **적합 기준** |
| **완결성** | GORE **안티목표** — *"뭐가 잘못될 수 있나"*에서 역산 |
| **잠금** | `[NEEDS CLARIFICATION]` 마커 **0개**일 때만 확정 |

**실증**: LLM 후속질문은 사람 수준이고, **"흔한 인터뷰 실수 프레임워크"를 주면 사람을 이긴다** (RE'25).
→ 인터뷰 스킬에는 질문 목록만이 아니라 **하지 말아야 할 실수 목록**을 넣어야 한다.

> ✅ **2026-08-25 1차 출처 확인 — 이 절에서 가장 강한 근거다** (`elicitation-interview-build-standard` **ELI-001**).
> 설계가 **통제실험 2개**다: 최소 가이드 조건에서 *"the LLM-generated questions are **no worse than** the
> human-authored questions with respect to clarity, relevancy, and informativeness"*, 그리고 실수 유형으로
> 가이드한 조건에서 *"LLM-generated questions **outperform** human-authored questions"*.
> **④ `/kickoff` 가 실수 목록을 핵심으로 삼은 판단은 그대로 선다.**
>
> ⚠️ **같은 절의 다른 수치는 그렇지 않다.** LLMREI 의 *"최대 73.7% 도출"* 은 **완전 60.94% + 부분 12.76%** 의 합이고
> 표본은 모의 인터뷰 33건·참가자 대부분 학생이다(**ELI-002**). 그리고 **`8/12/18턴` 은 인용한 두 논문 어디에도 없다**(**ELI-004**) —
> 배치 4 의 *"계획을 파일로"*(IPW-016)와 **같은 형태**다: 실재하는 논문을, 그 논문이 하지 않은 말의 근거로 달았다.

**추적성**: 인수기준마다 **안정 ID**(`AC-1`…)를 붙이고, `AC-n → 검사 ID → 검사 파일` 매핑표를 만든다.
매핑할 수 없는 인수기준은 **`UNVERIFIABLE`로 표시하고 알린다 — 조용히 통과시키지 않는다**
([`legacy/judgments/goppi/foundation/workflow-standard.md`](../legacy/judgments/goppi/foundation/workflow-standard.md) WF-01).

## 여러 모델을 어떻게 쓰나

[`corpus/aspects/27-ai-harness-archetype/multi-agent-orchestration-standard.md`](../corpus/aspects/27-ai-harness-archetype/multi-agent-orchestration-standard.md)

- 🔴 ~~지배적 토폴로지 =~~ **널리 서술되는 토폴로지 = 오케스트레이터-워커 + 컨텍스트 격리**. ⚠️ **2026-08-25 재검증으로 *"지배적"* 을 내렸다**(`multi-agent-orchestration-standard` **MAO-003**): 세 출처 어디에도 **채택률의 모집단 조사·설문·배포 통계가 없고**, Anthropic 은 **자사 아키텍처**를 서술할 뿐이다. 결정적으로 **같은 근거로 인용해 온 Cognition 이 정반대를 쓴다** — *"**No single approach to building agents has become the standard yet**"*. → **프로젝트 판단으로 재분류**
- **+90.2%** · **토큰 ~15배** ✅ **2026-08-25 1차 출처 확인**(**MAO-001·002**) — 수치는 원문 그대로다: *"outperformed single-agent Claude Opus 4 by 90.2% on **our internal research eval**"* · *"agents typically use about **4×** … multi-agent systems use about **15×** more tokens than chats"* · *"token usage by itself explains **80%** of the variance"*. ⚠️ **다만 벤더 내부 평가이고 표본 수·과제 구성·방법론이 공개돼 있지 않다.** 저자가 우수 영역을 *"breadth-first queries"* 로 스스로 좁힌다
- 🔴 **단일 작성자 원칙**(Cognition) — 병렬 작업자는 **지능을 기여하지 행동을 하지 않는다.**
  *"행동에는 암묵적 결정이 실리고, 충돌하는 결정은 나쁜 결과를 낳는다"*
  ✅ **2026-08-25 1차 출처 확인**(**MAO-004**) — 인용은 정확하다. 그 문장은 2024년 글의 **Principle 2 제목 그대로**이고,
  운용 규칙은 2025년 후속 글에 있다: *"multi-agent systems work best today when **writes stay single-threaded**
  and the additional agents contribute **intelligence rather than actions**."*
  ⚠️ **근거의 종류는 통제실험이 아니라 자사 운영 경험**이고, 예시(Flappy Bird)에는 저자 스스로 *"This may seem contrived"*
  라 단서를 달았다. ⚠️ 그리고 ***"single-writer"* 라는 이름은 이 코퍼스의 것**이다 — 원문 표현은 *"one writer"* · *"single-threaded"*
- **생성자-검증자** — 작성자의 컨텍스트가 **없는** 리뷰어가 오히려 버그를 더 찾는다.
  ✅ **2026-08-24 1차 출처 재검증** (`28 overview` **IPW-006~008**):
  - **근거는 통제실험이다** — 30개 산출물·150개 주입 오류·**360 리뷰**. CCR **F1 28.6%** vs 같은세션
    자기리뷰 24.6%(p=0.008, d=0.52). ⭐ **같은 세션에서 두 번 리뷰해도 한 번보다 낫지 않았다**(p=0.11)
    → **반복이 아니라 컨텍스트 분리 자체가 원인** (**IPW-006**)
  - ⚠️ **절대 성능은 낮다** — 최선 조건에서도 **오류의 약 71%를 놓친다.** *"+16%"* 는 **상대 개선**이다.
    **독립 리뷰어는 갖출 값이 있지만 안전망이 아니다** — 게이트는 여전히 CI 다 (**IPW-007**)
  - ⚠️ **이전 판은 이 문장에 Cognition 의 *"PR당 +2건, 58% 심각"* 을 근거로 붙였다.** 원문은
    *"an **average of 2 bugs per PR**"* 로 **절대값**이고 **대조군·방법론이 없다** — 비교 주장을
    받칠 수 없는 수치였다 (**IPW-008**)
- **교차벤더 라우팅은 비용이 아니라 역량 최적화** ✅ **재검증**(**IPW-009**) — *"The delegation logic becomes a **capability router** rather than a difficulty escalator."* 단 출처는 벤더 경험 보고다
- ~~**정적 역할 배정이 프로덕션 표준** — 동적 per-query 라우팅은 아직 연구 단계~~ ❌ **2026-08-24 재검증으로 삭제**(**IPW-010**) — 배포 통계가 없고, **같은 출처(Cognition)가 동적 교차벤더 라우팅을 *"in production for a meaningful stretch"* 로 돌렸다고 밝힌다.** 자기모순이었다
- ⚠️ 대부분의 **코딩 작업은 다중 에이전트에 부적합** — 진짜 병렬 가능한 하위작업이 적다. ⚠️ **2026-08-25 한정**(**MAO-005**): 원문은 단정이 아니라 **비교문**이다 — *"most coding tasks involve **fewer truly parallelizable tasks than research**"*. 저자가 실제로 든 부적합 조건은 과제 종류가 아니라 **구조**다 — *"domains that require **all agents to share the same context** or involve **many dependencies**"*. → *"코딩이라서 안 된다"* 가 아니라 ***"공유 컨텍스트·상호 의존이 많으면 안 된다"*** 로 쓴다

호스트 제약: 서브에이전트 `model` 필드는 **Anthropic 모델만** 받는다(`fable` 포함).
외부 모델 경로는 **MCP 또는 셸아웃 둘뿐**
([`claude-code-agent-surface--facts-2026-08.md`](../corpus/aspects/27-ai-harness-archetype/claude-code-agent-surface--facts-2026-08.md) CAS-001·006).

## 일을 어떻게 라우팅하나

[`corpus/aspects/28-implementation-process-workflow/`](../corpus/aspects/28-implementation-process-workflow/)

- **깊이는 위험에 비례** — 하나의 무거운 파이프라인을 모든 변경에 돌리지 않는다. ✅ **2026-08-25 1차 출처 확인**(`28 overview` **IPW-014·015**): Meta RADAR **535K+ diff**, 승인율 60.31%, 사고율 1/50. 🔴 **단 *"1/50"* 을 *"50배 안전"* 으로 읽으면 안 된다** — RADAR 를 통과하는 diff 는 **저위험으로 선별된 집단**이고, 저자가 *"diffs are not randomly assigned"* 라고 명시한 **관찰 연구**다
- **계획은 산출물이다** — 컨텍스트에만 두지 말고 파일로. ⚠️ **2026-08-25 재검증**(**IPW-016**): 근거로 인용해 온 **Plan-and-Solve·ReAct 는 프롬프트 안에서 계획을 세우는 기법**이고 **파일 영속화를 주장하지 않는다.** 리서치가 받치는 것은 *"계획을 먼저 세운다"* 까지이고, ***"파일로 남긴다"* 는 프로젝트 판단이다**
- **검증은 객관 신호로** — 컴파일러·테스트·린터. **자기평가는 신뢰할 수 없다** ✅ **재검증**(**IPW-001·002**) — 정확히는 *"외부 피드백이 없으면"* 이다. 외부 신호를 주면 작동한다
- **실패를 경계 짓는다** — 재시도 상한 + 진동 감지. ⚠️ **2026-08-25 재검증**(**IPW-017**): 문제의 실재와 구현 사례는 확인된다(정지 경계 없는 반복 경로 · `max_turns` · A→B→A 감지). **그러나 최적 상한값이나 보편적 진동 탐지법은 확립돼 있지 않다** — *"상한을 두라"* 까지가 근거이고 **얼마로 두는지는 판단이다**
- **되돌릴 수 없는 행위 전에 사람** — write-staging 이 비가역을 가역 쪽으로 옮긴다. ✅ **2026-08-25 1차 출처 확인**(**IPW-018**): 자율성은 **역량과 분리된 의도적 설계 결정**이고 5단계로 구분된다. write staging 은 **6대 아키텍처 전술 중 하나**이며 해당 논문이 **reversibility 를 명시적 설계 고려사항**으로 다룬다
- **머지는 적대적·교차벤더 리뷰 뒤에** — LLM 심판은 **자기선호 편향**이 있어 자기 작업의 심판으로 약하다. ✅ **2026-08-24 1차 출처 확인**(`28 overview` **IPW-004**): 자기인식 능력과 자기선호 강도가 파인튜닝 실험에서 **선형으로 동행**했다. ⚠️ 저자가 *"initial evidence"* 라 했으므로 **확정적 인과로 쓰지 않는다**

## 생성 코드도 같은 게이트

[`corpus/aspects/07-construction-code-review/`](../corpus/aspects/07-construction-code-review/)

> 생성된 코드는 **같은 게이트**를 지난다 — 리뷰·테스트·스타일. **신뢰로 머지되지 않는다.**
> 작성자가 모든 줄을 소유하고 설명할 수 있어야 하며, **리뷰어는 프롬프트가 아니라 diff를 리뷰한다.**
