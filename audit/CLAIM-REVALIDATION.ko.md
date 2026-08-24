# 상속 문서 50개 — load-bearing claim 재검증 register

> 검사일: 2026-08-02 · 범위: gingoa에서 상속된 `status: review-needed` 50개 문서의 **설계 결정을
> 떠받치는 최상위 주장**. 문서의 모든 문장을 verified로 만드는 검사가 아니다. 기존 출처의 종류·범위,
> 현재 공식 자료, local census/experiment의 모집단, 법·제품의 시효성을 대조했다.

## 판정 코드

- `RETAIN-RN/SPLIT`: 가치 있는 근거가 있으나 복합 보편 주장을 원자 claim으로 나누고 범위를 좁혀야 함.
- `RETAIN-RN/LOCAL`: 재현 가능한 local evidence지만 표본 밖으로 일반화할 수 없음.
- `RETAIN-RN/VOLATILE`: 제품·법·버전 행동이 섞여 현행 1차 자료 재확인이 필요함.
- `RETAIN-RN/SYNTHESIS`: 좋은 설계안이지만 객관적 사실이 아니라 goppi/project 선택임.
- `SUPERSEDED`: 더 현재적이고 claim-register가 있는 문서가 설계 근거를 대신함; 원문은 역사/깊이용.

`RN`은 active corpus에 보존하지만 설계의 verified premise로 쓰지 않는다는 뜻이다. 이번 pass에서
`verified`로 승격한 상속 문서는 0개다. 이는 실패가 아니라 근거보다 강한 도장을 찍지 않은 결과다.

## 50/50 disposition

| ID | 문서 | 재검증한 load-bearing claim | 판정 · 이유/조치 |
|---|---|---|---|
| C50-01 | `01-requirements-planning/01-requirements-planning--overview.md` | INVEST+ISO sweep+29148+MoSCoW+ADR가 보편 baseline | RETAIN-RN/SPLIT · 각 기법은 서로 다른 선택; “#1 pain”과 AI 전이 별도 증거 필요 |
| C50-02 | `01-requirements-planning/brownfield-planning-adoption.md` | 기존 요구를 present/absent/different-format으로 처리하는 adoption algorithm | RETAIN-RN/SYNTHESIS · 유용한 goppi 절차이지 산업 표준 아님 |
| C50-03 | `01-requirements-planning/constitution-authoring-standard.md` | AGENTS/CLAUDE 문서의 정답 구조와 작성 규칙 | RETAIN-RN/VOLATILE · host surface와 권고가 변함; 공식 format 사실과 authoring 선택을 분리 |
| C50-04 | `01-requirements-planning/decision-record-standard.md` | 모든 significant decision의 특정 ADR family/형식 | RETAIN-RN/SPLIT · ADR 개념은 근거 있음; significance와 format은 조직 선택 |
| C50-05 | `01-requirements-planning/elicitation-interview-build-standard.md` | 7 prior-art family를 결합한 interview engine이 build standard | RETAIN-RN/SYNTHESIS · 제품 설계안; 실제 target-user task study 필요 |
| C50-06 | `01-requirements-planning/elicitation-prior-art.md` | 조사 도구/기법에서 가져올 기능 목록 | RETAIN-RN/VOLATILE · 시장/제품 동작은 갱신 필요; 비교 사실과 제안을 분리 |
| C50-07 | `01-requirements-planning/planning-document-family.md` | PRD/spec/plan의 definitive 종류·이름·위치 | RETAIN-RN/SYNTHESIS · 조직별 문서 체계를 goppi convention으로 과장함 |
| C50-08 | `01-requirements-planning/planning-output-census.md` | 267 high-star repo prevalence가 권장 floor를 정함 | RETAIN-RN/LOCAL · 관측 표본은 보존; 인과·품질·전체 모집단으로 일반화 금지 |
| C50-09 | `01-requirements-planning/requirements-engineering-craft.md` | traceability·DoR·우선순위 기법 묶음이 보편 craft | RETAIN-RN/SPLIT · 고전 RE와 agile 관행의 적용 조건이 다름 |
| C50-10 | `02-architecture-design/02-architecture-design--overview.md` | 모든 프로젝트가 style+ADR+C4/arc42+fitness function을 선행 | RETAIN-RN/SPLIT · 품질 tradeoff는 유지; 산출물과 시점은 risk/decision별 조건부 |
| C50-11 | `03-dev-environment/03-dev-environment--overview.md` | lockfile commit과 parity로 byte-identical toolchain 보장 | RETAIN-RN/SPLIT · library/app convention 차이; lockfile은 전체 toolchain 동일성 보장 아님 |
| C50-12 | `04-build-ci-engineering/04-build-ci-engineering--overview.md` | lint/typecheck/test/build 4종의 unbypassable CI가 보편 | RETAIN-RN/SPLIT · 실제 claim에 맞는 verify가 기준; 언어/산출물별 gate가 다름 |
| C50-13 | `04-build-ci-engineering/brownfield-adoption-floor.md` | audit-mode와 3-way disposition이 표준 adoption 방식 | RETAIN-RN/SYNTHESIS · do-no-harm 구현안으로 보존, 효과 평가 필요 |
| C50-14 | `04-build-ci-engineering/foundation-floor-artifact-checklist.md` | 특정 file set이 canonical production floor | RETAIN-RN/SYNTHESIS · production-output rubric의 결과면으로 대체; 파일 presence≠adequacy |
| C50-15 | `04-build-ci-engineering/visibility-provision-matrix.md` | private/public에 따라 자동 provision할 정확한 파일/설정 | RETAIN-RN/VOLATILE · host 기능·요금제·정책 변동; irreversible choice는 사용자 결정 |
| C50-16 | `05-scm-workflow/05-scm-workflow--overview.md` | daily trunk+review+CI+CC+CODEOWNERS를 non-engineer에게 default-on | SUPERSEDED · `github-workflow-current.md`가 제품 사실과 bounded default를 분리; compulsory bundle 기각 |
| C50-17 | `06-config-secrets/06-config-secrets--overview.md` | 모든 config는 env, 모든 프로젝트는 store/rotation/feature flag | RETAIN-RN/SPLIT · 12-Factor는 service 맥락; secret·flag 통제는 노출/운영 조건별 |
| C50-18 | `07-construction-code-review/07-construction-code-review--overview.md` | TDD+1 approval+약 100-line CL이 보편 construction loop | RETAIN-RN/SPLIT · small change/review 근거는 유지; 수치와 TDD 의무는 조직/위험별 |
| C50-19 | `08-software-testing/08-software-testing--overview.md` | pyramid+coverage floor+contract test+quarantine가 모든 프로젝트의 표준 | RETAIN-RN/SPLIT · oracle·위험·아키타입별 test strategy가 먼저; 도구 묶음은 조건부 |
| C50-20 | `09-application-security/09-application-security--overview.md` | SAST/DAST/scan/audit 전부를 CI gate로 넣으면 senior security | RETAIN-RN/SPLIT · threat-driven controls 유지; 모든 도구를 gate하는 것은 오탐/맥락 고려 필요 |
| C50-21 | `10-supply-chain-security/10-supply-chain-security--overview.md` | digest pin+bot+SBOM+signed provenance를 보편 default | RETAIN-RN/SPLIT · distribution/blast-radius별 수준 필요; prevalence는 local census 범위만 |
| C50-22 | `11-maintainability-techdebt-refactoring/11-maintainability-techdebt-refactoring--overview.md` | CI complexity budget+debt register+Boy Scout+strangler+characterization 모두 의무 | RETAIN-RN/SPLIT · 각 기법 적용 신호가 다르고 universal bundle 근거 없음 |
| C50-23 | `12-performance-scalability/12-performance-scalability--overview.md` | profiling/load/perf-CI/stateless/cache/load-shed가 runtime archetype 공통 | RETAIN-RN/SPLIT · 측정 목표는 유지; tactics와 CI gate는 병목/architecture별 |
| C50-24 | `13-api-interface-design/13-api-interface-design--overview.md` | 모든 interface를 먼저 machine-described/versioned하고 HTTP는 idempotent | RETAIN-RN/SPLIT · public boundary 계약은 유지; format/version/idempotency는 protocol semantics별 |
| C50-25 | `14-data-management-migrations/14-data-management-migrations--overview.md` | forward-only expand-contract+WAL PITR가 모든 persistence의 표준 | RETAIN-RN/SPLIT · DB/availability별; WAL은 PostgreSQL 계열의 구체 구현 |
| C50-26 | `15-accessibility-ux/15-accessibility-ux--overview.md` | 모든 web/mobile은 WCAG AA+axe CI, EN 301 549가 EU 전체 법적 요구 | RETAIN-RN/VOLATILE · 시장/제품/법 적용 범위 필요; axe alone은 conformance proof 아님 |
| C50-27 | `16-privacy-data-protection/16-privacy-data-protection--overview.md` | 개인데이터면 DSAR/consent log/72h 통지가 항상 동일하게 적용 | RETAIN-RN/VOLATILE · 관할·role·예외·위험에 따라 달라 법률 검토 필요 |
| C50-28 | `17-release-engineering/17-release-engineering--overview.md` | SemVer+Conventional Commits+자동 changelog+DORA가 보편 release | RETAIN-RN/SPLIT · 공개 API/versioned artifact 여부와 조직 목적별 선택 |
| C50-29 | `17-release-engineering/release-operate-artifact-checklist.md` | ④ 단계의 특정 artifact checklist가 completeness 표준 | RETAIN-RN/SYNTHESIS · 새 8면 rubric과 아키타입 gate에 매핑 후 필요한 항목만 활성화 |
| C50-30 | `18-packaging-distribution/18-packaging-distribution--overview.md` | tagged SemVer CI+provenance+canonical channel만 허용 | RETAIN-RN/SPLIT · one-off/internal/distribution별; local upload 금지는 risk-based choice |
| C50-31 | `19-observability-telemetry/19-observability-telemetry--overview.md` | OTel three pillars+RED/USE+SLO alert가 모든 서비스 표준 | RETAIN-RN/SPLIT · 필요한 신호는 failure mode별; prevalence 수치는 survey/local scope |
| C50-32 | `20-operations-incident-reliability/20-operations-incident-reliability--overview.md` | SLO/error budget/on-call/postmortem/DR/DORA bundle이 모든 운영 표준 | RETAIN-RN/SPLIT · 조직 규모 SRE를 solo owner에게 직접 이식 불가; R1-9로 scale-down |
| C50-33 | `21-economics-cost-sustainability/21-economics-cost-sustainability--overview.md` | 모든 metered cloud와 규제 조직에 하나의 FinOps/SCI/CSRD loop | RETAIN-RN/VOLATILE · 법 threshold·관할·조직 scope 갱신 필요 |
| C50-34 | `22-documentation-knowledge/22-documentation-knowledge--overview.md` | 모든 repo에 Diátaxis+표준 파일+ADR+generated ref+CI freshness | RETAIN-RN/SPLIT · 독자·배포·결정 규모별; 문서 목록보다 audience/task가 기준 |
| C50-35 | `22-documentation-knowledge/content-ci-linting-and-jargon-gate.md` | prose lint와 forbidden jargon gate가 일반 content CI 표준 | RETAIN-RN/SYNTHESIS · 프로젝트 vocabulary/오탐 기준을 실험해야 함 |
| C50-36 | `23-developer-experience/23-developer-experience--overview.md` | golden path+self-service+SPACE, multi-team에서만 IDP | RETAIN-RN/SPLIT · SPACE의 다차원성은 근거; 정확한 platform threshold는 조직별 |
| C50-37 | `24-governance-collaboration-compliance/24-governance-collaboration-compliance--overview.md` | CoC/license/security를 day one, CODEOWNERS/branch protection으로 협업 | RETAIN-RN/SPLIT · 공개·기여·소유 구조별; gingoa 적용 문장은 legacy로 이미 분리 |
| C50-38 | `24-governance-collaboration-compliance/issue-pr-writing-conventions.md` | GitHub form schema와 권장 writing convention이 하나의 표준 | RETAIN-RN/VOLATILE · schema 사실은 공식 docs로 갱신, 문구/필수 field는 project 선택 |
| C50-39 | `25-licensing-foss-compliance/25-licensing-foss-compliance--overview.md` | 단일 license+모든 파일 SPDX+scan+DCO/CLA가 보편 | RETAIN-RN/SPLIT · distribution/contribution/legal policy별; 법률 자문 대체 금지 |
| C50-40 | `26-mlops-ml-lifecycle/26-mlops-ml-lifecycle--overview.md` | 모든 production ML에 co-version+CI/CD/CT+registry+drift/retrain 전체 stack | RETAIN-RN/SPLIT · model lifecycle/규제/변화율별; AI Act 정보는 별도 현행 법 검증 필요 |
| C50-41 | `27-ai-harness-archetype/27-ai-harness-archetype--overview.md` | full floor+정해진 capability-layer catalog가 mature harness | SUPERSEDED · `harness-control-plane-standard.md` 6-plane map과 `agent-threat-model.md`가 현재 근거 |
| C50-42 | `27-ai-harness-archetype/hooks-commands-subagents-standard.md` | hooks/commands/subagents의 정확한 3-component 표준 | RETAIN-RN/VOLATILE · host별 surface/통합 변화; 제품 사실과 선택 matrix를 분리 |
| C50-43 | `27-ai-harness-archetype/host-config-schemas.md` | 특정 Claude/Codex version schema가 cross-host 사실 | RETAIN-RN/LOCAL · 캡처 버전의 evidence로 보존; 현재 host 구현 전 재-census 필요 |
| C50-44 | `27-ai-harness-archetype/mcp-server-standard.md` | protocol normative facts+vendor tool craft가 하나의 frontier standard | RETAIN-RN/VOLATILE · MCP 2025-11-25 normative 부분은 현행; vendor synthesis 원자화 필요 |
| C50-45 | `27-ai-harness-archetype/multi-agent-orchestration-standard.md` | orchestrator-worker가 dominant, single-writer가 hard boundary, +90.2%/~15× 일반화 | RETAIN-RN/SPLIT · Anthropic 특정 research eval/업체 의견; 보편 topology 규칙 아님 |
| C50-46 | `27-ai-harness-archetype/plugin-marketplace-memory-standard.md` | plugin/marketplace/memory의 공통 3-artifact 표준 | RETAIN-RN/VOLATILE · host별 packaging/state가 다르고 빠르게 변함; poisoning은 threat model로 이동 |
| C50-47 | `27-ai-harness-archetype/prompts-and-evals-standard.md` | prompt technique/model parameter/eval 수치가 하나의 frontier standard | RETAIN-RN/VOLATILE · model-version 권고는 빠르게 만료; 결과 기반 eval 원칙만 원자화 후보 |
| C50-48 | `27-ai-harness-archetype/skill-authoring-standard.md` | SKILL.md 구조+500-line+eval/security가 단일 normative standard | RETAIN-RN/SPLIT · spec-required field와 vendor best practice/size heuristic 분리 필요 |
| C50-49 | `28-implementation-process-workflow/28-implementation-process-workflow--overview.md` | 모든 구현은 plan-first+subagents+cross-vendor adversarial review | RETAIN-RN/SPLIT · risk tailoring/verification은 유지; multiagent/vendor topology는 조건부 선택 |
| C50-50 | `28-implementation-process-workflow/research-log.md` | process tailoring 문헌이 특정 agentic workflow 전체를 뒷받침 | RETAIN-RN/SPLIT · 고전 process 근거와 최신 agent experiment를 별도 claim register로 분리 |

## 집계와 설계 사용 규칙

| disposition | 문서 수 |
|---|---:|
| RETAIN-RN/SPLIT | 28 |
| RETAIN-RN/SYNTHESIS | 7 |
| RETAIN-RN/VOLATILE | 11 |
| RETAIN-RN/LOCAL | 2 |
| SUPERSEDED | 2 |
| **합계** | **50** |

> 위 집계는 자동 검사에서 행 ID와 실제 `review-needed` 파일 set을 대조한다. 수동 표의 분류 수가
> 달라지면 이 요약보다 행 자체와 검사 결과가 우선한다.

기획 시에는 같은 주제의 `verified` claim register가 있으면 그것을 먼저 사용한다. 이 register의
`SUPERSEDED` 두 문서는 현재 설계 근거로 사용하지 않는다. 나머지 48개는 아이디어와 출처 후보를 찾는
용도로만 읽고, 채택할 문장은 원자 claim으로 새 문서에 옮겨 현재 1차 자료와 scope/expiry를 붙인 뒤에만
verified premise가 된다.
