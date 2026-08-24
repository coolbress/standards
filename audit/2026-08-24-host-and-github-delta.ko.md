# 리서치 유닛 기록 — 호스트 표면 · GitHub 집행 경계 · 프로젝트 간 재사용 (2026-08-24)

> append-only 감사 기록. 이 유닛은 **소유자 요청**으로 열렸다 — 기성품 스택으로 전환하기 위한 설계에
> 앞서, 기존 코퍼스에서 낡거나 어긋난 항목을 찾아 갱신하고 빈칸을 채운다.

## 질문 (4개, 각각 종료 기준 있음)

| # | 질문 | 종료 기준 | 결과 |
|---|---|---|---|
| Q1 | Free 플랜 + 비공개 저장소에서 룰셋/브랜치 보호가 집행되는가 | 1차 근거 또는 재현 가능한 실측 | **닫힘** — 선행 문서가 이미 규정. 실측으로 확인 |
| Q2 | 이슈 폼의 `required`가 REST/CLI 경로에도 걸리는가 | 1차 근거 | **닫힘** — 걸리지 않음 (GEB-003·004) |
| Q3 | 저장소 바닥을 여러 프로젝트에 반복 설치하지 않는 기계장치와 그 경계 | 세 장치 각각 '무엇이 옮겨지는가' 확정 | **부분** — 경계 확정, 비공개 재사용 워크플로 실행은 미검증 |
| Q4 | 2026-07-02 이후 Claude Code 에이전트 표면 중 코퍼스와 어긋난 것 | 어긋난 항목이 1차 출처로 특정될 것 | **닫힘** — 2건(중첩·동시 한계) |

**검색일**: 2026-08-24 · **출처 등급**: 1차(공급자 공식 문서) 우선, 모델 지형만 2차로 격리
**포함**: 위 4개 질문에 직접 답하는 공식 문서와 로컬 API 실측
**제외**: Team/Enterprise 플랜 동작 · Codex CLI 현행 표면 · Issue Types · 외부 브리지 실행 검증

## 산출물

| 문서 | 성격 |
|---|---|
| `corpus/aspects/05-scm-workflow/github-enforcement-boundaries--facts-2026-08.md` | 신규 (research-log) |
| `corpus/aspects/04-build-ci-engineering/cross-project-reuse--facts-2026-08.md` | 신규 (research-log) |
| `corpus/aspects/27-ai-harness-archetype/claude-code-agent-surface--facts-2026-08.md` | 신규 (research-log) |
| `corpus/aspects/27-ai-harness-archetype/multi-agent-orchestration-standard.md` | 정정 1행 (중첩 5단 → 3단) |
| `corpus/aspects/27-ai-harness-archetype/hooks-commands-subagents-standard.md` | 확인 노트 1건 |
| `corpus/aspects/05-scm-workflow/github-workflow-current.md` | GHW-003에 포인터 1건 |
| 부모 overview 3건 | Sub-documents 링크 |

## 실제로 어긋났던 것 (전수)

1. `multi-agent-orchestration-standard.md`: 서브에이전트 중첩 **"up to 5 levels"** → 현행 **기본 3단**
2. 같은 문서: 동시 실행 한계 미기재 → 현행 **최대 20**

**그것뿐이다.** 코퍼스 본체는 7주가 지났음에도 대부분 현행과 맞았다.

## 조사 과정에서 발생한 오판 2건 (기록 — 되풀이 방지)

이 유닛의 중간 보고는 **없는 결함을 두 번 보고했다.** 둘 다 같은 원인이다: **선행 문서를 끝까지 찾지 않고
신규성을 주장했다.**

| # | 잘못된 주장 | 실제 | 왜 놓쳤나 |
|---|---|---|---|
| 1 | "서브에이전트 frontmatter 8개 필드가 코퍼스에 없다" | `hooks-commands-subagents-standard.md`가 `fable`·`isolation: worktree` 포함 **이미 전부 수록** | 전략 문서(`multi-agent-orchestration-standard.md`)의 요약표만 읽고 **컴포넌트 문서를 읽지 않았다**. 두 층은 의도적으로 분리돼 있고, 호스트 세부의 정본은 컴포넌트 쪽이다 |
| 2 | "Free+비공개 룰셋 불가는 새 사실" | `visibility-provision-matrix.md`(2026-06-26)가 `PRIV-free ⛔`로 **이미 규정** | 주제가 05(scm)에 있을 것이라 가정하고 05만 검색했다. **가시성×플랜 게이트는 04(build-ci)에 산다** |

**일반화**: 이 코퍼스는 주제가 aspect 경계를 가로지르게 배치돼 있다(`MAP.md`가 물리 배치와 검색 등급을
일부러 다르게 둔 이유와 같다). **신규성을 주장하기 전에 `MAP.md`의 active 40건과 reference 114건을
주제어로 훑는 절차**를 밟아야 한다. 이번에는 밟지 않았다.

부수 효과로 조사자가 몰랐던 사실이 하나 드러났다 — **Actions 분은 공개 무제한 / 비공개 Free 2,000분·월**
(같은 matrix). CI를 집행 지점으로 삼는 설계의 예산 제약이다.

## 남은 것 (다음 유닛 후보)

| 우선 | 항목 |
|---|---|
| 높음 | 비공개 재사용 워크플로가 `access_level=user`에서 **실제 실행**되는지 1회 실측 |
| 중간 | GitHub Issue Types / `issue_field_values` — 폼보다 강한 집행 수단인가 |
| 중간 | Codex CLI 현행 서브에이전트 표면 (부모 문서가 스스로 재검증 경고) |
| 낮음 | 공개 `.github`가 비공개 저장소에도 상속되는지 |

## 부수 발견 — 링크 부패 2건 (이 유닛의 URL 감사가 잡음)

새 URL 5건을 추가하며 전체 828건을 재감사한 결과, **기존 코퍼스 링크 2건이 404로 죽어 있었다.**
이번 유닛의 질문과 무관하지만 감사 기록에 남긴다.

| URL | 상태 | 무게 |
|---|---|---|
| `https://iso25000.com/.../iso-25010` | 404 | **높음** — ISO/IEC 25010은 코퍼스 앵커 표준(품질 모델 9축). 인용처: `08-software-testing--overview.md` · `12-performance-scalability--overview.md` · `15-accessibility-ux--overview.md` |
| `https://docs.tessl.io/use/spec-driven-development-with-tessl` | 404 | 낮음 — 벤더 도구 문서. 인용처: `census-data/census-doc-conventions/spec-doc-revalidation-2026-06-27.md` |

**처분 안 함.** 대체 URL 확정과 인용 문서 수정은 별도 유닛이 필요하다(ISO는 유료 표준이라 공식
catalog 링크로 갈아끼워야 하며, 그 판단은 이 유닛의 범위 밖이다).
추가 감사 신호: `access-blocked`가 39→49로 늘었는데, 이는 단일 스윕 중 rate-limit(429) 가능성이 높고
링크 부패와 구분되지 않는다 — 재감사로만 판별된다.

## 후속 실측 — 관리자 우회 시험 (2026-08-24, 소유자 실행)

이 유닛의 "남은 것"에 없던 질문이 벽 설치 중에 생겼다: **룰셋의 `bypass_actors`를 비우면
소유자에게도 통하는가.** 에이전트는 보호 규칙을 강제로 넘는 실행이 차단돼 답할 수 없었고,
**소유자가 직접 실행해 답을 가져왔다.**

| 절차 | 결과 |
|---|---|
| 위반 브랜치 → PR #2 → CI 실패(`integrity` 12s) | `mergeStateStatus: BLOCKED` |
| `gh pr merge --squash --admin` | **거부** — `GraphQL: Repository rule violations found / Required status check "integrity" is failing.` |
| `main` 상태 | `92e07e0` 불변 · CI 초록 |

→ `github-enforcement-boundaries--facts-2026-08.md` GEB-005(local-census) · GEB-006(synthesis)로 편입.

**왜 이 한 건이 무게를 갖는가**: goppi 계열 하네스가 3개월간 답하지 못한 질문과 같은 형태다.
L0는 *"자물쇠는 협조 위에 선다"* · *"훅-ask 강제 vs allow 우회 판별 UNVERIFIED — 에이전트 실행 거부 ·
소유자만 관측 가능"* 을 고지했다. **이번에도 에이전트는 거부했고 소유자만 관측할 수 있었다** —
관측 경로의 모양까지 같다. 다른 것은 답이 나왔다는 점이고, 그 차이는 통제가
**같은 uid 안에 있느냐(훅) 서버 측이냐(룰셋)** 에서 온다.

**과잉 일반화 금지**: n=1, 단일 저장소·단일 룰셋 구성이다. 그리고 룰셋을 **비활성화·삭제한 뒤
머지하는 경로는 측정하지 않았다** — 그 경로는 여전히 열려 있다고 보아야 한다.
