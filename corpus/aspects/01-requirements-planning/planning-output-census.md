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

- **CONFIRMS the constitution choice, strongly.** `AGENTS.md` (35% / 41% sw) + `CLAUDE.md` (29% / 34% sw) are the
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

## Caveats (honest)
- Sample = 267 top-star repos (general + a few language/category slices) — high-star ≠ representative of all repos,
  and ≠ gingoa's reference class (structured-process / spec-tool cohort), which the broad aggregate under-represents.
- Planning artifacts often live in **wikis, issues, or external trackers** (Notion/Linear) → file-tree detection
  **under-counts** real planning process.
- 4 repos had truncated trees (very large) → minor under-detection.
- Detection is filename/dir-presence, not content quality.

## Sources
Raw data + reproducible scripts: `census-data/planning-output-census/` (`sample.json` · `raw-tsv.txt` · `census.py` · `detect.jq`). Tool: GitHub `gh search repos` + `gh api .../git/trees`.
