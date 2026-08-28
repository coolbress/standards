---
id: aspect-01-requirements-planning--planning-output-census
title: "Planning-output prevalence census — 267 high-star GitHub repos"
parent: aspect-01-requirements-planning
kind: census
evidence_track: census
status: review-needed
last_updated: "2026-06-27"
method: "Sampled census (2026-06-27): `gh search repos --stars '>500'` across general + TS/Python/framework/cli slices → 267 distinct repos (221 software). Per repo, one recursive `git/trees` fetch → boolean detection of planning/spec artifacts. Raw data + scripts in census-data/planning-output-census/ (sample.json, raw-tsv.txt, census.py, detect.jq). Tally computed from raw-tsv.txt. The collecting agent hit a session limit before writing this doc; the lead computed the tally from the complete raw data."
---

# Planning-output prevalence — 267 high-star repos

How often do top-starred GitHub repos commit each planning/spec artifact. **n=267** (221 software, 4 truncated trees).

| Artifact | all % | software % | n |
|---|---|---|---|
| `docs/` dir | 64.4 | 72.9 | 172 |
| `CHANGELOG.md` | 43.1 | 48.0 | 115 |
| **`AGENTS.md`** | **34.8** | **41.2** | 93 |
| **`CLAUDE.md`** | **28.8** | **33.9** | 77 |
| `specs/` dir | 15.7 | 17.6 | 42 |
| `ROADMAP.md` | 5.6 | 6.8 | 15 |
| RFC / `rfcs/` | 3.4 | 3.6 | 9 |
| **ADRs** (`docs/adr` / `adr` / `decisions`) | **1.1** | 1.4 | 3 |
| `requirements.md` | 0.7 | 0.9 | 2 |
| **`PRD.md`** | **0.4** | 0.5 | 1 |
| `.kiro` (Kiro) | 0.7 | 0.9 | 2 |
| `.specify` (Spec-Kit) | 0.4 | 0.5 | 1 |
| `openspec/` | 0.4 | 0.5 | 1 |

## What it confirms / challenges for gingoa's ① output set

- **CONFIRMS the constitution choice, strongly.** `AGENTS.md` (**35% all / 41% sw** — n=267 all, n=221 software) + `CLAUDE.md` (**29% all / 34% sw**) are the
  **most-adopted of any planning artifact measured** — the agent constitution is now mainstream in top repos.
  gingoa shipping `AGENTS.md`+`CLAUDE.md` as a ① artifact is squarely the de-facto standard (validates
  [`constitution-authoring-standard.md`](constitution-authoring-standard.md)). `docs/` (64%) + `CHANGELOG.md`
  (43%) confirm the doc baseline.
- **CONTEXTUALISES the PRD/ADR choice (does NOT challenge it).** `PRD.md` (0.4%), `requirements.md` (0.7%), and
  committed `ADRs` (1.1%) are **rare even among top-star repos.** This is the **selection-bias signal**, not a
  counter-argument: the top-OSS aggregate is dominated by libraries/tools with *no requirements process*, so they
  commit no PRD/ADR because they need none. gingoa's reference class — a non-engineer + agent building
  *production-grade* software (a structured process) — is the spec-driven-tool cohort, which **does** commit these
  (see [`elicitation-prior-art.md`](elicitation-prior-art.md) §Naming-and-publish, already adjudicated). The census
  REINFORCES that committing a PRD/ADR is a deliberate structured-process choice, above the broad-aggregate norm —
  exactly what gingoa's elicit feature emits *for that cohort*, defaulting to committed.
- **`prd.yml` (machine SSOT) is novel — 0 repos.** No surveyed repo ships a YAML requirements SSOT + generated
  prose view at the planning layer (closest precedents are OpenAPI/Terraform at the API/infra layer). gingoa's
  machine-SSOT design is **ahead of the field**, not a deviation from a standard that doesn't exist.
- **`specs/` (16%) aligns with per-feature specs being ③-JIT.** Some structured repos keep a `specs/` dir — the
  home gingoa reserves for the ③ per-feature `docs/specs/<slug>/spec.md`, not the ① project PRD.
- **Spec-driven tools (Spec-Kit/.kiro/openspec) are nascent (<1%).** gingoa is early in a category the constitution
  + docs/ baseline already make mainstream.

**Verdict:** gingoa's ① output set is empirically sound — the constitution is mainstream; the committed PRD/ADR is
a structured-process artifact (rare in the broad aggregate by selection bias, standard in gingoa's cohort); the
machine-SSOT `prd.yml` is a novel, defensible lead.

## Claim table — `direction` 이 기대는 수치 (2026-08-28 앵커 신설)

[`direction/05`](../../../direction/05-the-output-floor.md) 이 **바닥의 문서 묶음**을 정할 때 이 문서를
근거로 삼으면서 **이름으로만** 적었다 — claim table 이 없어 경로로 인용하면 `validate_corpus` 가
`RESULT FAIL` 을 냈기 때문이다(`GAPS` R5-29). `IPC-001`~`IPC-005` 와 **같은 자리의 문제**이고, 같은 방식으로 해소한다.

| Claim ID | Class | Claim and scope | Evidence | Confidence | 재검증 |
|---|---|---|---|---|---|
| POC-001 | local-census | **에이전트 헌법이 측정된 계획 산출물 중 1위다.** `AGENTS.md` **34.8% all / 41.2% sw**, `CLAUDE.md` **28.8% / 33.9%** — `docs/`(64.4/72.9) 를 빼면 어떤 계획 산출물보다 높고, `CHANGELOG.md`(43.1/48.0) 와 같은 급이다. → 바닥이 `AGENTS.md` 를 **문서 묶음에 넣는 근거**가 이것이다 | `PLANNING-OUTPUT-CENSUS-2026` (n=267 all · 221 sw) | medium-high | 2026-12-28 |
| POC-002 | local-census | 🔴 **이건 파일 존재율이지 품질이 아니다.** 탐지는 **파일·디렉터리 이름 존재**만 본다 — 내용을 안 읽는다. 그래서 이 표는 *"몇 %가 갖고 있나"* 에만 답하고 *"그게 쓸모 있나"* 에는 **답하지 않는다.** 후자는 `CAS-002`·`CAS-003` 이 맡는다(`C50-14` *presence ≠ adequacy* 와 같은 구분) | `PLANNING-OUTPUT-CENSUS-2026` | high | 2026-12-28 |
| POC-003 | local-census | **PRD·ADR 은 상위 저장소에서도 희귀하다** — `PRD.md` 0.4% · `requirements.md` 0.7% · 커밋된 ADR 1.1%. 🔶 **이건 기각 근거가 아니라 선택 편향 신호다**: top-OSS 총합은 요구 절차가 없는 라이브러리·도구가 지배한다. 바닥이 이 셋을 **묶음에 안 넣는** 근거로만 쓰고, *"쓰면 안 된다"* 로는 쓰지 않는다 | `PLANNING-OUTPUT-CENSUS-2026` | medium | 2026-12-28 |
| POC-004 | local-census | **모집단 한정.** 표본은 `stars>500` 상위 저장소 267개다 — **전체 GitHub 의 대표 표본이 아니다.** 게다가 계획 산출물은 위키·이슈·외부 트래커(Notion/Linear)에 사는 경우가 많아 파일트리 탐지는 **실제 계획 활동을 과소계수한다.** `IPC-004` 가 PR 템플릿에서 겪은 것과 **같은 한정**이다 | `PLANNING-OUTPUT-CENSUS-2026` | high | 2026-12-28 |

## Caveats (honest)
- Sample = 267 top-star repos (general + a few language/category slices) — high-star ≠ representative of all repos,
  and ≠ gingoa's reference class (structured-process / spec-tool cohort), which the broad aggregate under-represents.
- Planning artifacts often live in **wikis, issues, or external trackers** (Notion/Linear) → file-tree detection
  **under-counts** real planning process.
- 4 repos had truncated trees (very large) → minor under-detection.
- Detection is filename/dir-presence, not content quality.

## Sources
Raw data + reproducible scripts: `census-data/planning-output-census/` (`sample.json` · `raw-tsv.txt` · `census.py` · `detect.jq`). Tool: GitHub `gh search repos` + `gh api .../git/trees`.
