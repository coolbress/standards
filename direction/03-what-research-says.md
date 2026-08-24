# 03 — 리서치는 무엇을 말하는가

> 갱신 2026-08-24 · rev1 · 근거는 전부 `corpus/`에 있다. 여기는 **방향에 걸리는 것만** 추린 색인이다.

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
> | ❌ **코퍼스에 없음** | — | **중앙값 24줄 · 응답 4시간 · DORA 리뷰속도 50%** · **"브랜치 다이어그램은 ceremony"** · **"다중 승인자·형식 체크리스트는 DORA 안티패턴"** — 아래 ⚠️ 표시 |
>
> **아직 안 옮긴 것**: Git Flow 창시자의 2020 note · 테스트 피라미드 80/15/5 · TDD 순서 효과 ·
> feature flag 부채. `audit/GAPS.ko.md` R5-1에 등재했다.

1. 고성과의 공통분모는 브랜치 모델이 아니라 **"작게, 자주, 빨리 통합"** — 활성 브랜치 ≤3, 하루 1회 머지, **브랜치 수명 몇 시간**
2. Git Flow는 **창시자가 2020년에 웹앱에 비추천**했다
3. **리뷰의 제1 변수는 엄격함이 아니라 속도** — 빠른 팀이 배포 성과 **50% 높음**. Google 응답 규범 1영업일, 실측 중앙값 **4시간**
4. 리뷰의 전제는 **작은 변경** — Google 중앙값 **24줄**, 100줄 적정 / 1000줄 과대, **400줄 넘으면 결함 발견율 급락**
5. 진짜 CI = 메인라인 + 자동빌드 + 자기검증 테스트 + **10분 이내** + **깨지면 즉시 수리**. *"이것이 없으면 나머지는 장식이다"*
6. Delivery ≠ Deployment. feature flag는 **부채**
7. 테스트 피라미드 — Google 실측 80/15/5
8. **TDD의 "테스트 먼저" 순서 자체는 효과 불분명** — 효과의 원천은 *잘게 균일한 스텝 + 항상 테스트가 따라오는 것*
9. **"Done" = 머지 전 CI 녹색 + 리뷰 승인**
10. Conventional Commits 같은 형식 규약은 **자동화가 소비할 때만** 가치 — 아니면 cargo cult

### 하중을 받는 것 vs 의식(ceremony)

> 하중을 받는 것은 *"브랜치 수명 단축 + 매일 통합"이라는 **행동**"* 이지 모델의 이름이 아니다.
> **브랜치 다이어그램을 정교하게 그리는 것 자체는 ceremony다.**
>
> 그리고 **다중 필수 승인자·형식적 체크리스트 채우기는 DORA가 명시한 안티패턴**이다 — 변경 배치를 키운다.

## 게이트는 어디에 있어야 하나

[`corpus/aspects/05-scm-workflow/`](../corpus/aspects/05-scm-workflow/) — tension T3:

> **pre-commit 훅은 게이트가 될 수 없다** — `--no-verify`로 우회된다.
> **진짜 게이트는 CI + 브랜치 보호다.**

census: 브랜치 보호가 강하게 걸린 저장소는 **10~13%**뿐이다 → *"바로 그 게이트를 기본 ON으로 켜야 한다"*

⚠️ **플랜 제약**: GitHub Free에서 룰셋은 **공개 저장소에만** 적용된다. 비공개는 Pro 이상.
그리고 Actions 분은 공개 무제한 / 비공개 Free 2,000분·월
([`04-build-ci-engineering/visibility-provision-matrix.md`](../corpus/aspects/04-build-ci-engineering/visibility-provision-matrix.md) ·
[`05-scm-workflow/github-enforcement-boundaries--facts-2026-08.md`](../corpus/aspects/05-scm-workflow/github-enforcement-boundaries--facts-2026-08.md)).

## 이슈·PR은 어떻게 쓰나

[`corpus/aspects/24-governance-collaboration-compliance/issue-pr-writing-conventions.md`](../corpus/aspects/24-governance-collaboration-compliance/issue-pr-writing-conventions.md)
(census N=6,582 저장소 · 20,837 템플릿 필드)

- **이슈 우선은 크기 조건부다 — 보편 규칙이 아니다.** 사소한 변경은 바로 PR. 이슈 필수는 *방향이 불확실한* 작업에만
- **이슈 제목에 커밋 규약을 걸지 마라** — 야생에서 CC 이슈 제목은 **≈1%**. PR 제목만
- 이슈 폼: 도움말 **87%**(사실상 필수) · required는 **본문 필드에** 걸고 체크박스엔 안 건다
- PR 템플릿: **빈 체크리스트**가 표준(62%) · 중앙값 3절 · "type of change"는 소수(11.5%)이고 **CC를 쓰면 뺀다**
- ⚠️ **이슈 폼의 `required`는 REST/CLI 경로에 걸리지 않는다** — 에이전트는 `gh issue create`를 쓴다.
  **집행은 CI 가드가 정본이다** (GEB-003·004)

## 기획은 어떻게 이끄나

[`corpus/aspects/01-requirements-planning/elicitation-interview-build-standard.md`](../corpus/aspects/01-requirements-planning/elicitation-interview-build-standard.md)
— 7개 선행연구 계열 종합

| 층 | 처방 |
|---|---|
| 질문 **스타일** | Mom Test — 유도·가정 질문 금지, **과거의 구체적 행동**에 근거, 80% 듣기 |
| 질문 **선택** | 다음 질문 = **기대 정보이득 최대** |
| **분량** | **턴당 ≤2문항**, 위험별 깊이 **8/12/18턴**, 상한 15~20 |
| **표기법** | **EARS** (`WHEN/IF/WHILE… SHALL`) + 요구사항마다 **적합 기준** |
| **완결성** | GORE **안티목표** — *"뭐가 잘못될 수 있나"*에서 역산 |
| **잠금** | `[NEEDS CLARIFICATION]` 마커 **0개**일 때만 확정 |

**실증**: LLM 후속질문은 사람 수준이고, **"흔한 인터뷰 실수 프레임워크"를 주면 사람을 이긴다** (RE'25).
→ 인터뷰 스킬에는 질문 목록만이 아니라 **하지 말아야 할 실수 목록**을 넣어야 한다.

**추적성**: 인수기준마다 **안정 ID**(`AC-1`…)를 붙이고, `AC-n → 검사 ID → 검사 파일` 매핑표를 만든다.
매핑할 수 없는 인수기준은 **`UNVERIFIABLE`로 표시하고 알린다 — 조용히 통과시키지 않는다**
([`legacy/judgments/goppi/foundation/workflow-standard.md`](../legacy/judgments/goppi/foundation/workflow-standard.md) WF-01).

## 여러 모델을 어떻게 쓰나

[`corpus/aspects/27-ai-harness-archetype/multi-agent-orchestration-standard.md`](../corpus/aspects/27-ai-harness-archetype/multi-agent-orchestration-standard.md)

- 지배적 토폴로지 = **오케스트레이터-워커 + 컨텍스트 격리**. 연구 평가에서 **+90.2%**, 다만 **토큰 ~15배**
- 🔴 **단일 작성자 원칙**(Cognition) — 병렬 작업자는 **지능을 기여하지 행동을 하지 않는다.**
  *"행동에는 암묵적 결정이 실리고, 충돌하는 결정은 나쁜 결과를 낳는다"*
- **생성자-검증자** — 작성자의 컨텍스트가 **없는** 리뷰어가 오히려 버그를 더 찾는다(PR당 +2건, 58% 심각).
  교차 컨텍스트 리뷰 **+16% F1**
- **교차벤더 라우팅은 비용이 아니라 역량 최적화**
- **정적 역할 배정이 프로덕션 표준** — 동적 per-query 라우팅은 아직 연구 단계
- ⚠️ 대부분의 **코딩 작업은 다중 에이전트에 부적합** — 진짜 병렬 가능한 하위작업이 적다

호스트 제약: 서브에이전트 `model` 필드는 **Anthropic 모델만** 받는다(`fable` 포함).
외부 모델 경로는 **MCP 또는 셸아웃 둘뿐**
([`claude-code-agent-surface--facts-2026-08.md`](../corpus/aspects/27-ai-harness-archetype/claude-code-agent-surface--facts-2026-08.md) CAS-001·006).

## 일을 어떻게 라우팅하나

[`corpus/aspects/28-implementation-process-workflow/`](../corpus/aspects/28-implementation-process-workflow/)

- **깊이는 위험에 비례** — 하나의 무거운 파이프라인을 모든 변경에 돌리지 않는다
- **계획은 산출물이다** — 컨텍스트에만 두지 말고 파일로
- **검증은 객관 신호로** — 컴파일러·테스트·린터. **자기평가는 신뢰할 수 없다**
- **실패를 경계 짓는다** — 재시도 상한 + 진동 감지
- **되돌릴 수 없는 행위 전에 사람** — write-staging이 비가역을 가역으로 바꾼다
- **머지는 적대적·교차벤더 리뷰 뒤에** — LLM 심판은 **자기선호 편향**이 있어 자기 작업의 심판으로 약하다

## 생성 코드도 같은 게이트

[`corpus/aspects/07-construction-code-review/`](../corpus/aspects/07-construction-code-review/)

> 생성된 코드는 **같은 게이트**를 지난다 — 리뷰·테스트·스타일. **신뢰로 머지되지 않는다.**
> 작성자가 모든 줄을 소유하고 설명할 수 있어야 하며, **리뷰어는 프롬프트가 아니라 diff를 리뷰한다.**
