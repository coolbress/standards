---
id: aspect-01-requirements-planning--planning-document-family
title: "Planning/spec document family — KINDS × sections/content/naming/location/publish (DEFINITIVE)"
parent: aspect-01-requirements-planning
kind: research-log
evidence_track: census+lit
status: review-needed
last_updated: "2026-06-27"
method: "Deep anti-supersede survey (2026-06-26): canonical templates (Spec Kit spec/plan/tasks/constitution, Kiro requirements/design/tasks/steering, BMAD PRD/brief, OpenSpec, ISO-29148, EARS, classic PRD templates, Scrum) + a 500k+-file gh naming census. Defines the FINAL standard for what planning/spec documents exist, their sections, naming, location, and publish norm. Reconstructs gingoa's ① set."
---

# Planning / spec document family — the definitive standard

Six dimensions per the owner ask: **종류(KINDS) · sections · content · naming · location · publish**. Built to
be FINAL (not re-litigated). Two evidence tracks: canonical templates `[lit]` + a gh filename census `[census]`.

## gh naming census (2026-06-26, `gh api search/code total_count`; estimates, code-search caveats apply)
`AGENTS.md` **129,696** · `CLAUDE.md` **40,200** · `plan.md` 42,552 · `spec.md` 41,696 · `design.md` 36,496 ·
`ROADMAP.md` 18,440 · `requirements.md` 10,760 · `tasks.md` 9,808 · **`PRD.md` 8,644** · `vision.md` 2,776 ·
`constitution.md` 2,080 · `product-requirements.md` 1,104. ADR: `docs/adr`+0001 5,088 · `doc/adr` 2,616 ·
`docs/decisions` 2,556. **Reading:** the constitution layer in the wild = **AGENTS.md/CLAUDE.md** (170k
combined ≫ constitution.md 2k); per-feature quartet spec/plan/design/tasks dominates; `PRD.md` is the
project-requirements winner (8× `product-requirements.md`).

## KINDS — the complete set, adjudicated
| Kind | Level | Verdict | Canonical name | Notes |
|---|---|---|---|---|
| **Constitution / steering** | project | **STANDARD** | `AGENTS.md`+`CLAUDE.md` (or `constitution.md` / `steering/{product,tech,structure}.md`) | governing rules+stack+structure; census-dominant via AGENTS/CLAUDE |
| **PRD** (product requirements) | project | **STANDARD** | `PRD.md` | the project "what & why"; NOT the per-feature spec |
| **Per-feature requirements spec** | feature (③ JIT) | **STANDARD** | `spec.md` / `requirements.md` | user stories + EARS/Given-When-Then acceptance |
| **Technical design** | feature (③) | **STANDARD** | `design.md` | architecture + data model + API design + key decisions |
| **Implementation plan** | feature (③) | **STANDARD** | `plan.md` | tech context · structure · constitution-check gate |
| **Tasks breakdown** | feature (③) | **STANDARD** | `tasks.md` | ordered work items, `[P]` parallel markers |
| **ADR** | ①→④ | **STANDARD** | `docs/adr/NNNN-kebab.md` | one closed decision; see `decision-record-standard.md` |
| Vision / brief / charter | project | OPTIONAL | `vision.md` / README §Vision | a section for small projects; separate file for products |
| Roadmap | project | OPTIONAL (product teams) | `ROADMAP.md` | not a requirements artifact |
| Glossary · personas · NFR · risk · acceptance-criteria | — | **SECTION, not a file** (promote only if domain-heavy / 4+ personas) | inside PRD or per-feature spec | standalone files = bloat/duplication |
| Data model · API contract | feature | STANDARD **machine file** when shared/independently-reviewed | `data-model.md` · `contracts/*.yaml` (OpenAPI etc.) | else a `design.md` section |
| **Product backlog** | — | **NOT a committed repo doc** | GitHub Issues / tracker | the WORK backlog is execution, not a spec; do NOT commit `backlog.md` |

## Per-kind: sections (MUST/REC) · naming · location · publish
**Constitution (`AGENTS.md`/`CLAUDE.md`)** — §Product-overview · §Tech-stack(approved+excluded) · §Structure/
conventions · §Architectural-constraints(+ADR links) · §Security-baseline · §Testing-mandate (all MUST) ·
§Coding-conventions · §Governance/amendment (REC). Location: repo root / `.specify/memory` / `.kiro/steering`.
**Committed+pushed; set up FIRST.** No status-lifecycle (amended in place). Tech-stack/structure = structured.
**Full authoring standard** (section skeleton · <200-line / dual-file SSOT+mirror rule · anti-patterns · the
exact build/boundaries sections): [`constitution-authoring-standard.md`](constitution-authoring-standard.md).

**PRD (`PRD.md`)** — §Executive-summary · §Problem · §Goals & success-metrics · §Target-users/personas ·
§Scope (in/out + **feature list**) · §Functional-requirements (high-level) · §NFRs (ISO-25010, system-wide)
(MUST) · §User-journeys · §Assumptions & dependencies · §Risks · §Open-questions (REC) · §release-strategy ·
§appendix (OPTIONAL). Location `docs/PRD.md` (never under a feature folder). **Committed+pushed.** Goals/metrics
+ NFRs = structured (tables); rest prose.

**Per-feature spec (`spec.md`/`requirements.md`)** — §Feature-overview(→PRD link) · §User-stories (P1/P2/P3) ·
§Acceptance-criteria (**EARS** `WHEN <trigger> THE SYSTEM SHALL <response>` or Given-When-Then) · §Functional-
requirements (FR-NNN) (MUST) · §feature-NFRs(delta over PRD) · §Edge-cases · §Assumptions · §Out-of-scope ·
§`[NEEDS CLARIFICATION]` (REC). Location `docs/specs/<feature-slug>/spec.md`. **Committed+pushed.** Stories/AC
= structured.

**Design (`design.md`)** — §Overview(→spec) · §Architecture · §Data-model · §API/interface · §Key-design-
decisions(alternatives+rationale) · §Error-handling · §Security (MUST) · §Testing-strategy · §NFR-approach ·
§Dependencies/impact · §Open-questions (REC). Same feature folder. **Committed.** Data-model/API → machine file.

**Plan (`plan.md`)** — §Summary · §Technical-context · §Project-structure · §Constitution-check gate (MUST) ·
§Complexity-tracking · §Phase-overview (REC). **Tasks (`tasks.md`)** — phased ordered tasks (`T001`, `[P]`),
dependency map. Same folder. **Committed.**

## Boundary A — PROJECT vs PER-FEATURE (no duplication)
Project (write once): vision · business goals/OKRs · system personas · **system-wide NFR baseline** · approved
stack/structure (constitution) · **high-level feature list** (PRD scope). Per-feature (JIT): feature user-
stories+acceptance · **feature NFR deltas (cite the baseline)** · architecture/data/API design · tasks. Rule:
the PRD lists features; each feature's `spec.md` defines one. NFRs split: baseline→PRD, tighter→spec.

## Boundary B — separate FILE vs SECTION
Always a file: constitution, PRD, per-feature spec/design/plan/tasks, API contract, CHANGELOG. Section-by-
default (promote only if heavy): NFRs, personas, glossary, risk register, acceptance-criteria, data-model.
**Never a committed file:** product backlog (→ issue tracker).

## Machine-SSOT vs prose
Structured (yaml/table/schema): tech-stack, goals/metrics, NFR thresholds, user-stories+acceptance, data-model,
API contracts, tasks. Prose: problem, context, rationale, design narrative. A machine-SSOT + generated human
view is sound **only if one is generated from the other** (no parallel hand-maintenance).

## gingoa reconstruction (FINAL ① set — supersedes the earlier PRD+BACKLOG+ADR call)
1. **Constitution = `AGENTS.md` + `CLAUDE.md`** (census-validated dominant form; gingoa is already
   CLAUDE/AGENTS-centered → native). The elicit FEATURE emits the user project's AGENTS/CLAUDE.
2. **PRD = `prd.yml` (machine SSOT) → `PRD.md` (GENERATED human view)** — not hand-parallel. The PRD's
   §Scope/feature-list IS the feature inventory.
3. **ADRs = `docs/adr/NNNN-kebab.md`**, ①→④ (see `decision-record-standard.md`).
4. **Per-feature (③ JIT): `spec.md` → `design.md` → `plan.md` + `tasks.md`** under `docs/specs/<slug>/`
   (gingoa's `plans/` is the planner runtime for plan/tasks).
5. **DROP standalone `BACKLOG.md`** — a committed product-backlog is non-standard (work backlog = GitHub
   Issues; feature inventory = PRD §Scope). gingoa's "which feature next" reads the PRD feature list + Issues.
   [revises the 2026-06-26-earlier "BACKLOG.md" decision on deeper evidence.]
Publish: all the above **commit+push** (visibility inherits; `--private` for NDA) per `_schema.md §4`; gingoa's
own `docs/internal/` stays local (self-dogfood working-notes register).

## Publish-location — the DEFINITIVE standard (two independent axes)
A recurring confusion ("should planning docs be local or remote?") conflates two orthogonal axes:

- **Axis 1 — in-repo-committed-and-pushed vs doc-tool / gitignored-local.** PRD + ADRs go **IN the repo, committed
  AND pushed.** The ADR consensus is explicit (Nygard · Fowler · MADR · Google Cloud · AWS · GDS): a decision
  record lives in the *shared* repo so it is PR-reviewable, travels with the code, and is correct at any commit. A
  spec-driven, **agent-consumed** PRD must be on the remote so any session/machine/collaborator's agent reads the
  same SSOT. **Gitignored-local (un-pushed) defeats the purpose** and is reserved ONLY for security-sensitive docs
  (the threat-model — publishing aids attackers) and internal IP / working-notes (this research corpus). PRD/ADR are
  NOT in that exception.
- **Axis 2 — public vs private remote = "is the project open-source?"** Pushing to a *private* remote keeps a doc
  off the public internet while still shared + version-controlled (proprietary); a *public* remote is the OSS norm
  (Rust RFCs, K8s KEPs are public). gingoa is open-source → public.

**Why the broad repo census shows PRD 0.4% / ADR 1.1%** (see [`planning-output-census.md`](planning-output-census.md))
— and why it does NOT refute commit+push:
- PRD is a **product-company artifact**, not an OSS one (an OSS library has no PM; product companies' code is
  private and their PRDs live in Notion/Confluence) → ~0% in public OSS by definition.
- ADRs are a **niche, newer discipline**, and decision history more often lives as **RFCs / design-docs / PR &
  issue threads / wikis** than a `docs/adr/` folder the census detects → true decision-recording is far above 1.1%.
- Top repos are run by **senior teams** who carry the requirement/decision context implicitly (head + issues) and
  don't *need* the explicit artifact. **gingoa's user is the opposite** — a non-engineer + an agent with no
  cross-session memory — so the committed PRD/ADR IS the scaffolding that substitutes for senior tribal knowledge
  and how the agent carries context across sessions (operating model: *evidence, not tribal knowledge*).
- The cohort that *does* run a structured / spec-driven process (Spec-Kit · Kiro · BMAD · OpenSpec + ADR adopters)
  commits+pushes **unanimously**; gingoa imposes that process → it IS that cohort, by design.

**Verdict (settled):** the elicit feature emits constitution + PRD + ADRs **committed and pushed** to the user's
repo; public/private follows the project's open-source posture; override-to-local only for genuinely sensitive
concepts. The broad-OSS rarity is selection bias + folder-name measurement, **not** a counter-standard.

## Re-validation (2026-06-27) — the per-feature-spec standard STANDS (no supersession)
An owner-requested re-validation re-ran the survey across four parallel angles — academic/standards, the
current SDD frameworks, a top-star GitHub census, and practitioner articles — scoped to four points:
**(1) spec storage location · (2) authoring/structure · (3) file naming · (4) publish-to-remote.** Verdict
(raw deposit: [`../../census-data/census-doc-conventions/spec-doc-revalidation-2026-06-27.md`](../../census-data/census-doc-conventions/spec-doc-revalidation-2026-06-27.md)):
- **NO point is superseded.** Naming (`spec.md`, no date prefix) and publish (commit+push) are CONFIRM-strong;
  structure (EARS AC + quartet) is CONFIRM; location (`docs/specs/`) is REFINE-but-stands.
- **Date-prefix is debunked for specs** — it originates in Jekyll `_posts/` (blog parsing) and MADR's `NNNN-`
  is an *ADR* log convention (number = permanent identity), neither applicable to per-feature specs. Spec-Kit's
  fixed `spec.md` is the direct precedent. (Confirms this doc's `spec.md` call against the generic-tool default.)
- **RFC/governance cluster ≠ feature-spec cluster:** RFC processes (Rust/K8s/PEP/React/Vue/Ember/Swift)
  number-prefix in a *dedicated repo* because the number is a citable identity; in-repo feature specs (Spec-Kit
  slug/`NNN-`, Kiro/OpenSpec bare slug) do not. gingoa's bare slug is in the Kiro mainstream — do not import the
  NNNN-prefix.
- **REFINE notes (enhancements, not supersessions):** (a) `docs/specs/` is the minority location — external
  mainstream is `specs/`-at-root (Spec-Kit) / tool-namespaced (`.kiro/`, `openspec/`); kept here for internal
  consistency with the locked `docs/adr/` + `docs/PRD.md`, but the **emit-side** (the elicit feature writing into
  a *user's* repo) should consider `specs/`-root or a configurable path (a US-3 / elicit-slice decision). (b) ISO
  29148 §5.1 allows a per-requirement *rationale* attribute (gingoa carries a coarser doc-level Decisions &
  Rationale). (c) Adopt `[NEEDS CLARIFICATION]` as an **inline** marker (Spec-Kit) — agent-scannable, and it
  strengthens the elicit lock-gate's "0 markers" check. (d) Folder `NNN-` numbering deferred (bare slug stands).

**Objective assessment — why the deliberate write+push direction is right, and the boundary condition.** The
~95% who keep no structured spec mostly rely on a *precondition* — senior tribal knowledge carried in heads /
issues / PR threads — that gingoa's user (a non-engineer + an agent with no cross-session memory) lacks; their
behaviour is therefore **non-transferable evidence**, and the directly-comparable spec-driven cohort is
unanimous. So the direction is right **for a falsifiable reason, not because "more process is better"** — and its
justification is **conditional** on two disciplines, collapsing to ceremony tax (the 95% would be right) if
either fails: (1) the spec is **load-bearing** — the EARS criteria *are* the tests and the agent actually reads
it (ADR-0014, evidence-not-theater) — not a decorative doc; (2) it is **risk/complexity-tiered** — only a
Tier-3-equivalent change earns a full spec (the routing tiers / ADR-0019), never "always spec". The **push**
itself is **low-regret and net-positive** (the single source of truth travels to every session / machine /
collaborator agent), and the **location is data-settled** (`docs/specs/` ≈ / ≥ root `specs/` globally — the
top-453 census + global code-search). The residual risk is therefore **spec *liveness* (drift / staleness), not
*where the file lives*** — managed by the spec lifecycle (durable-why, never edited to track code drift,
backfilled before merge) + traceability ([`requirements-engineering-craft.md`](requirements-engineering-craft.md)),
not by the path. Location/publish verification is **exhausted** (top-453 census + global code-search +
frameworks + standards all concordant); the remaining work is keeping specs alive — done while building, not
re-surveyed.

## Re-validation (2026-06-28) — SECTIONS × AUTHORING-STYLE deepened; the spec/design split is CONFIRM-STRONG
An owner-requested deep re-research scoped to **(1) the content SECTIONS a per-feature spec contains and (2) its
AUTHORING STYLE**, plus the central question **"do architecture + design decisions + rejected alternatives live in
the requirements spec or in a separate design doc?"** — across authoritative standards/papers + the modern SDD
frameworks + practitioner articles + real top repos, with a **fresh GitHub `search/code` census**. Raw deposit:
[`../../census-data/census-doc-conventions/spec-section-style-revalidation-2026-06-28.md`](../../census-data/census-doc-conventions/spec-section-style-revalidation-2026-06-28.md).

- **The per-feature section split is CONFIRM-STRONG (was structure=CONFIRM):** `spec.md`/`requirements.md` = the
  **implementation-free WHAT** (overview · user-stories P1/P2/P3 · **EARS** acceptance · FR-NNN · NFR-deltas ·
  edge-cases · assumptions/constraints · out-of-scope · inline `[NEEDS CLARIFICATION]`); **`design.md` = the HOW**
  (architecture · data-model · API · **key design decisions + alternatives + rationale** · error-handling ·
  security · testing-strategy · NFR-approach). Unanimous across ISO/IEC/IEEE 29148:2018, IEEE 830, IEEE 1016,
  SWEBOK v4 (KA1 Requirements ≠ KA2 Design), GitHub Spec-Kit (`spec.md` WHAT / `plan.md` HOW), AWS Kiro
  (`requirements.md` / `design.md`), OpenSpec. **Fresh census makes it empirical:** `design.md` (37,024) ≈
  `spec.md` (44,640) globally, and **inside the canonical dirs design.md out-numbers the requirements file** —
  `docs/specs/`: design.md 4,552 > spec.md 3,632; `.kiro/specs/`: design.md 2,492 > requirements.md 2,112. The
  structured-spec cohort keeps **two separate files**, not one merged file.
- **Architecture + decisions + rejected-alternatives belong in `design.md`** (and individually-significant ones
  additionally as `docs/adr/NNNN-kebab.md`) — **never in `spec.md`.** The RFC/PEP/KEP/RFD "merge" (motivation +
  design in one file) is a **different artifact class** (community *deliberation* proposals, evaluated holistically
  by reviewers), not a build-time per-feature implementation spec — do **not** import it. Even those separate
  motivation from design as sections.
- **This SHARPENS the 2026-06-27 REFINE note (b).** That note ("gingoa carries a coarser doc-level Decisions &
  Rationale", citing 29148 §5.1's optional *per-requirement* rationale attribute) must **not** be read as licensing
  a **doc-level Decisions/Architecture section inside the requirements spec**. 29148 §5.1 allows a terse rationale
  *attribute on a requirement*; it does **not** put the design-decision record in the SRS. The standard home is
  `design.md`. *(Anti-supersede: the formal §-lists at L55–63 were already split-correct; this pass removes the
  doc-level-merge ambiguity with stated, evidence-backed cause — lit-unanimous + the fresh census.)*
- **Governance consequence (flagged, not yet actioned).** gingoa's **spec skill** currently makes
  "Decisions & Rationale" the spec's *durable nucleus* and emits no per-slice `design.md`; the shipped `elicit`
  Slice-1 spec (and the drafted Slice-2a part) therefore **merge** architecture + decisions into `spec.md`. Per
  this evidence that is a **deviation from the standard gingoa itself imposes on user projects**. The
  standard-faithful reconciliation is to **split `spec.md` (WHAT) + `design.md` (HOW)** and update the spec skill
  (+ the constitution's spec guidance) accordingly. The skill's original rationale (the plan is gitignored/deleted,
  so the durable *why* must survive in a tracked file) is **satisfied by `design.md`** — which is itself tracked +
  kept — so the split loses nothing and gains standard-conformance + an implementation-free requirements spec.
- **Authoring-style standard (confirmed):** per-requirement = the **29148 §5.2.5 ten properties** (esp. singular ·
  verifiable · traceable · implementation-free) + the set-level §5.2.6 five; acceptance criteria in **EARS** (event
  `WHEN…SHALL` dominant; state `WHILE`; unwanted `IF…THEN`), Gherkin only when the AC must double as an executable
  test; normative keywords **RFC 2119 uppercase**; **FR-NNN stable IDs** with backward(→PRD/source) + forward(→
  design→test) links (the RTM spine); **INVEST** per story; **structured** (lists/EARS/numeric) for stories/AC/FR/
  NFR/tasks and **prose** for context/rationale; **`[NEEDS CLARIFICATION]` inline** at each ambiguity.

## Sources
Spec Kit spec/plan/tasks templates https://github.com/github/spec-kit/tree/main/templates + spec-driven.md ·
Kiro specs https://kiro.dev/docs/specs/ + steering https://kiro.dev/docs/steering/ · BMAD planning
https://github.com/bmad-code-org/BMAD-METHOD · OpenSpec https://openspec.dev/ · ISO/IEC/IEEE 29148
https://www.iso.org/standard/72089.html · EARS (Mavin 2009) https://ieeexplore.ieee.org/document/5328509 ·
PRD template https://www.productcompass.pm/p/prd-template · AltexSoft doc types
https://www.altexsoft.com/blog/technical-documentation-in-software-development-types-best-practices-and-tools/ ·
Fowler Ubiquitous Language https://martinfowler.com/bliki/UbiquitousLanguage.html · Scrum Guide
https://scrumguides.org/scrum-guide.html · **raw census evidence:** `census-data/census-doc-conventions/`
(stats.json + census.sh — the gh `search/code` counts cited above).
