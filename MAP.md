# 리서치 코퍼스 지도 — **생성물이다. 손으로 고치지 마라.**

> `node tools/build-routes.mjs` 가 만든다. 최신 여부는 `--check` (낡으면 exit 1).
> 기계용은 `ROUTES.jsonl`, 이 파일은 **사람이 구조를 보는 표면**이다.

## 이 코퍼스는 두 겹이다

**물리 배치**(출처·무결성 체계)와 **검색 등급**(작업 중 접근 체계)은 **일부러 다르다.**
물리 이동은 2026-08-08에 부결됐다 — 검증기가 경로를 하드코딩하고, 경로를 값으로 갖는 대장이 3겹이며,
`corpus`(근거)↔`interpretation`(판단) 경계가 이 코퍼스의 인식론적 핵심이기 때문이다.
**대신 등급을 이 지도로 보여준다.**

| 등급 | 개수 | 뜻 |
|---|---|---|
| `active` | 45 | 첫 홉 **후보 풀** (전부 읽는 집합이 아니다) |
| `decision` | 10 | 프로젝트 판단 — **권위로** 찾는다 |
| `meta` | 8 | 코퍼스 사용법 — 이 지도가 대체한다 |
| `reference` | 141 | **물어봤을 때만** — 과거 하네스·원시 census |
| `archive` | 12 | 검색 제외 (폐기·legacy) |

**질의는 `station + archetype` 2축이다.** `risk` 는 부결 — 문서 속성이 아니라 작업 속성이라서.

## active — 첫 홉 후보

| 종류 | 경로 | 이 문서가 답하는 것 |
|---|---|---|
| aspect-overview | `corpus/aspects/01-requirements-planning/01-requirements-planning--overview.md` | Senior practice turns a vague idea into a precise, machine-actionable requirements baselin |
| reference | `corpus/aspects/01-requirements-planning/elicitation-interview-build-standard.md` | Requirements-elicitation interview engine — the build standard (US-2 'Elicit') |
| census | `corpus/aspects/01-requirements-planning/planning-output-census.md` | Planning-output prevalence census — 267 high-star GitHub repos |
| aspect-overview | `corpus/aspects/02-architecture-design/02-architecture-design--overview.md` | Senior engineers choose a deliberate architectural style for the system's quality attribut |
| aspect-overview | `corpus/aspects/03-dev-environment/03-dev-environment--overview.md` | A senior local setup is reproducible by construction — runtime + package-manager pinned, l |
| aspect-overview | `corpus/aspects/04-build-ci-engineering/04-build-ci-engineering--overview.md` | A senior-grade project ships an unbypassable CI gate (lint·typecheck·test·build) that is t |
| aspect-overview | `corpus/aspects/05-scm-workflow/05-scm-workflow--overview.md` | Senior teams work on short-lived branches off trunk (≤3 active, merged daily) protected by |
| reference | `corpus/aspects/05-scm-workflow/github-workflow-current.md` | Current GitHub workflow — evidence and bounded defaults |
| aspect-overview | `corpus/aspects/06-config-secrets/06-config-secrets--overview.md` | Senior engineers externalize all config to the environment (12-Factor III), keep zero secr |
| aspect-overview | `corpus/aspects/07-construction-code-review/07-construction-code-review--overview.md` | Construction is a reviewed change-unit loop: small self-contained changes written test-fir |
| aspect-overview | `corpus/aspects/08-software-testing/08-software-testing--overview.md` | A senior-grade project tests in a pyramid (many fast unit tests, fewer integration, very f |
| aspect-overview | `corpus/aspects/09-application-security/09-application-security--overview.md` | Senior teams treat security as a build-time, evidence-producing discipline — threat-model  |
| aspect-overview | `corpus/aspects/10-supply-chain-security/10-supply-chain-security--overview.md` | Senior teams treat the build/distribution path as an attackable asset — pin dependencies a |
| aspect-overview | `corpus/aspects/11-maintainability-techdebt-refactoring/11-maintainability-techdebt-refactoring--overview.md` | Senior engineers treat maintainability as a first-class quality attribute: they keep compl |
| aspect-overview | `corpus/aspects/12-performance-scalability/12-performance-scalability--overview.md` | Senior engineers treat performance as a budgeted, measured quality attribute — set explici |
| aspect-overview | `corpus/aspects/13-api-interface-design/13-api-interface-design--overview.md` | Design the interface contract first and version it: a stable, machine-described surface (O |
| aspect-overview | `corpus/aspects/14-data-management-migrations/14-data-management-migrations--overview.md` | Senior teams evolve persistent schema only through versioned, forward-only, source-control |
| aspect-overview | `corpus/aspects/15-accessibility-ux/15-accessibility-ux--overview.md` | For web/mobile user products, senior engineers build to WCAG 2.2 Level AA as the floor — s |
| aspect-overview | `corpus/aspects/16-privacy-data-protection/16-privacy-data-protection--overview.md` | When a system handles personal data, senior engineers bake privacy in by design and by def |
| aspect-overview | `corpus/aspects/17-release-engineering/17-release-engineering--overview.md` | Senior teams ship via automated, SemVer-tagged releases driven from Conventional-Commits h |
| aspect-overview | `corpus/aspects/18-packaging-distribution/18-packaging-distribution--overview.md` | Senior engineers ship from a tagged, SemVer'd CI release that publishes to the archetype's |
| aspect-overview | `corpus/aspects/19-observability-telemetry/19-observability-telemetry--overview.md` | Senior engineers instrument services for the three pillars (structured logs, RED/USE metri |
| aspect-overview | `corpus/aspects/20-operations-incident-reliability/20-operations-incident-reliability--overview.md` | Senior teams operate a running service against explicit SLOs with an error-budget policy,  |
| aspect-overview | `corpus/aspects/21-economics-cost-sustainability/21-economics-cost-sustainability--overview.md` | Senior teams treat run-cost and carbon as first-class engineering metrics — FinOps cost vi |
| aspect-overview | `corpus/aspects/22-documentation-knowledge/22-documentation-knowledge--overview.md` | Senior teams treat docs as versioned code organized by reader-intent (Diátaxis: tutorial/h |
| aspect-overview | `corpus/aspects/23-developer-experience/23-developer-experience--overview.md` | A new contributor reaches a first green build/PR through a documented golden path and self |
| aspect-overview | `corpus/aspects/24-governance-collaboration-compliance/24-governance-collaboration-compliance--overview.md` | Senior teams make collaboration legible — decision rights recorded as ADRs, review/ownersh |
| aspect-overview | `corpus/aspects/25-licensing-foss-compliance/25-licensing-foss-compliance--overview.md` | Senior teams pick a single deliberate outbound license, declare it machine-readably (a roo |
| aspect-overview | `corpus/aspects/26-mlops-ml-lifecycle/26-mlops-ml-lifecycle--overview.md` | Production ML treats data, code, and models as co-versioned first-class artifacts driven t |
| unlabeled | `corpus/aspects/27-ai-harness-archetype/27-ai-harness-archetype--overview.md` | A mature AI-harness ships the full normal-software floor PLUS an additive capability layer |
| reference | `corpus/aspects/27-ai-harness-archetype/agent-threat-model.md` | Integrated Agent Authority, Credential, Egress, Injection, and Production Threat Model |
| evidence | `corpus/aspects/27-ai-harness-archetype/approval-attribution-channels--measured-2026-08.md` | 승인 귀속 채널 실측 — 사람 클릭을 증명할 수 있는가 |
| reference | `corpus/aspects/27-ai-harness-archetype/harness-control-plane-standard.md` | Agent Harness Control Plane, Execution Boundary, and Lifecycle |
| evidence | `corpus/aspects/27-ai-harness-archetype/hook-output-surfaces--measured-2026-08.md` | 훅 출력 표면 실측 — 하네스가 사용자에게 말할 수 있는가 |
| reference | `corpus/aspects/27-ai-harness-archetype/hooks-commands-subagents-standard.md` | Hooks · Slash-commands · Subagents build standard (the orchestration/lifecycle layer — the |
| evidence | `corpus/aspects/27-ai-harness-archetype/host-config-schemas.md` | Host config-integration schemas (cross-host adapter evidence) |
| reference | `corpus/aspects/27-ai-harness-archetype/mcp-server-standard.md` | MCP server build standard (Tools · Resources · Prompts — the frontier-AI standard) |
| reference | `corpus/aspects/27-ai-harness-archetype/multi-agent-orchestration-standard.md` | Multi-agent orchestration — the topology/when-to-dispatch standard (orchestrator-worker, s |
| reference | `corpus/aspects/27-ai-harness-archetype/plugin-marketplace-memory-standard.md` | Plugin · Marketplace · Memory build standard (the packaging + memory layer — the frontier- |
| evidence | `corpus/aspects/27-ai-harness-archetype/pretool-ask-exit-codes--measured-2026-08.md` | PreToolUse ask의 exit code 동작 실측 |
| reference | `corpus/aspects/27-ai-harness-archetype/prompts-and-evals-standard.md` | Prompts · Evals build standard (prompt authoring/versioning + eval-harness design — the fr |
| reference | `corpus/aspects/27-ai-harness-archetype/skill-authoring-standard.md` | Agent Skill authoring standard (SKILL.md — the frontier-AI build standard) |
| evidence | `corpus/aspects/27-ai-harness-archetype/stop-event-rendering--measured-2026-08.md` | Stop 이벤트 렌더 관측 |
| evidence | `corpus/aspects/27-ai-harness-archetype/user-channel-rendering--measured-2026-08.md` | 사용자 채널 렌더링 판정 — 사람 관측 |
| aspect-overview | `corpus/aspects/28-implementation-process-workflow/28-implementation-process-workflow--overview.md` | Implementation is driven by process tailored to each change's risk — light gates for trivi |

## decision — 프로젝트 판단 (근거가 아니다)

| 종류 | 경로 | 내용 |
|---|---|---|
| method | `corpus/methods/evidence-durability--grading-model.md` | 근거 수명 등급 모델 — 무엇이 안 바뀌고, 무엇이 바뀌며, 바뀌면 어디까지 무너지는가 |
| method | `corpus/methods/EVIDENCE-POLICY.md` | Evidence Review and AI-Readable Corpus Policy |
| reference | `corpus/methods/framework-crosswalk-2026.md` | SWEBOK V4.0a × ISO/IEC/IEEE 12207:2026 × ISO/IEC 25010:2023 × goppi 28-Aspects |
| reference | `corpus/methods/target-user-capability-model.md` | Target User Capability and Responsibility Model |
| reference | `corpus/methods/trustworthy-completion-evidence-model.md` | Trustworthy Completion, Assurance, and Appropriate Reliance Evidence Model |
| decision-record | `interpretation/foundation/goppi-workflow-standard.md` | goppi-workflow-standard |
| decision-record | `interpretation/foundation/goppi-worth-hypothesis.md` | goppi-worth-hypothesis |
| decision-record | `interpretation/foundation/production-output-rubric.md` | production-output-rubric |
| decision-record | `interpretation/foundation/steering-verification-design.md` | steering-verification-design |
| decision-record | `interpretation/foundation/trustworthy-completion-evaluation-protocol.md` | trustworthy-completion-evaluation-protocol |

## meta — 진입점

- `corpus/_meta/README.md`
- `corpus/_schema.md`
- `corpus/facts-2026-08-matrix.md`
- `corpus/GUIDE.ko.md`
- `corpus/INDEX.md`
- `corpus/lifecycle.md`
- `corpus/PROVENANCE.md`
- `corpus/TAXONOMY.md`

## archive — 검색에서 제외됨 (지우지 않았다)

- `imported/goppi/what-is-a-harness.md`
- `interpretation/00-overview.md`
- `interpretation/01-sdlc-lifecycle.md`
- `interpretation/02-engineering-practices.md`
- `interpretation/03-planning-and-requirements.md`
- `interpretation/04-solo-and-ai-assisted-dev.md`
- `interpretation/legacy/gingoa-guide.ko.md`
- `interpretation/legacy/gingoa-lifecycle.md`
- `interpretation/legacy/gingoa-schema.md`
- `interpretation/legacy/gingoa-specific-sections.md`
- `interpretation/legacy/gingoa-taxonomy.md`
- `interpretation/legacy/three-tier-ledger.md`

## reference — 141개, 물어봤을 때만

전문은 `ROUTES.jsonl` 에서 `tier="reference"` 로 조회한다. 종류별 개수:

- research-log: 51
- census: 45
- prior-art: 45
