---
id: aspect-01-requirements-planning--elicitation-prior-art
title: "AI-agentic requirement elicitation — prior-art survey + techniques to steal"
parent: aspect-01-requirements-planning
kind: research-log
evidence_track: lit
status: review-needed
last_updated: "2026-06-26"
method: "OSS + academic survey (2026-06-26) — spec-driven tools, agentic PRD/elicitation frameworks, RE academic literature; feeds gingoa's ① elicit feature (US-2) design"
---

# AI-agentic requirement elicitation — prior-art survey

Why this exists: gingoa's ① stage turns a **non-engineer's vague idea** into a senior-grade requirements
document. This logs the prior-art survey that grounds the ① `elicit` feature design (US-2).

> **Reading note (updated 2026-06-27).** This doc is the *historical survey*. Two of its sections — **Naming &
> publish-location** and **① artifact-SET completeness** — are written as open questions but their decisions are
> now **SETTLED**: see [`planning-document-family.md`](planning-document-family.md) (the definitive ① kind set +
> naming + publish) and ADR-0020 (`contract`→`PRD`, feature-map retired, constitution = `AGENTS.md`/`CLAUDE.md`,
> standalone backlog dropped, `prd.yml` = SSOT). They are kept here as the **evidence behind those calls**, not
> as live debates. The **elicitation techniques** (below) feed US-2 and are carried forward, with empirical
> grounding, in [`elicitation-interview-build-standard.md`](elicitation-interview-build-standard.md).

## The landscape
**Spec-driven dev tools** (assume the user can articulate; *generate-then-clarify*):
- **GitHub Spec Kit** (`github/spec-kit`, ⭐111k, MIT) — `/constitution → /specify → /clarify → /plan → /analyze → /tasks → /implement`. Artifacts: `constitution.md` (project-wide) + per-feature `spec.md`/`plan.md`/`tasks.md` (+ research/data-model/contracts). Clarify = sequential coverage-based questioning appended to spec; completeness gate = a HUMAN-checked checklist ("unit tests for English"). Weakness (Fowler): review-overload (≤7 files/feature), spec↔code drift unsolved, **no non-engineer scaffolding**.
- **AWS Kiro** (IDE, proprietary) — `requirements.md` (**EARS** notation: `WHEN <trigger> THE SYSTEM SHALL <response>`) → `design.md` → `tasks.md`; `.kiro/steering/{product,tech,structure}.md` = persistent memory. **2–4 targeted clarifying questions** after a draft (workspace-scanned → stack-specific). **Cascade invalidation** (req change → design+tasks rerun). "Analyze Requirements" neurosymbolic consistency pass. Weakness: IDE-locked; "sledgehammer for a nut" on small changes.
- **Tessl** — spec-as-source (code `GENERATED FROM SPEC`). **AVOID**: recreates the MDD/MDA maintenance-failure (spec must be as detailed as the code).
- **OpenSpec** — brownfield delta specs (`ADDED/MODIFIED/REMOVED`); thin elicitation.

**Agentic elicitation / PRD frameworks** (closer to interview-first):
- **BMAD-METHOD** (`bmad-code-org/BMAD-METHOD`, ⭐49k, MIT) — multi-persona (Analyst "Mary" → PM → Architect…). **Advanced Elicitation skill**: a 75-technique library (12 categories incl. pre-mortem, inversion, Socratic, **paradox stress-tests** Braess/Theseus/Sorites, anti-bias). It is a *post-draft refinement loop* (5 methods offered → apply → approve), **user-controlled [x] stop**. Web-bundle (cheap chat LLM for planning) + IDE (metered for impl) = smart cost split. Weakness: menu-driven (non-engineer must pick a method); not a pre-gen Socratic interview.
- **pm-skills**, **slgoodrich/agents** (3 independent PRD reviewers), **agent-pm** — mostly post-hoc synthesis, not live elicitation.

**Academic RE-with-LLM** (the only true *interview-first* + automated-stop systems):
- **iReDev** (arXiv:2507.13081, ACM TOSEM) — 6-agent blackboard (Interviewer/EndUser/Deployer/Analyst/Archivist/Reviewer). Interviewer: open-ended + Socratic + **5W1H coverage** + MoSCoW-as-dialogue; **hard limit ≤2 questions/turn**. **Stop = Reviewer validates vs ISO/IEC/IEEE 29148** quality attrs (clarity/feasibility/verifiability/traceability/consistency) — the only evidence-grounded automated stop found. +46.9% req diversity; SRS completeness 3.2→4.2/5.
- **LLMREI** (arXiv:2507.02564) — **least-to-most structured prompt** (explicit role/education/domain/complexity adaptation) measurably beats a generic "be an interviewer" prompt (73.7% req elicited, ≈ trained human). ~50% of questions were context-dependent (adaptive follow-ups emerge from the LLM).
- **Elicitron** (arXiv:2404.16045, Stanford/Autodesk) — **serial persona generation** (each new item sees all prior) → far more diverse coverage; "empathic lead-user" probes surface latent NFRs.
- **AIRE'23** — graph/branching interviews are HARDER for LLMs than structured-prompt-with-hidden-coverage; **15–20 turns optimal**. → don't build a formal state machine.
- **Follow-Up-Question-Generation** (RE'25) — follow-up quality depends on FULL prior context (keep a running window).

**"Ouroboros" = noise for ①.** All variants (August-murr, tomzx, razzant, Agent-Wars) are self-improving *code/research* loops (self-modification), NOT elicitation. Only the metaphor ("each turn improves the next") = the serial-context technique above.

## The decisive gap (= gingoa's wedge)
Fowler's SDD essay + the arXiv SDD survey + every tool critique agree: **every tool assumes the user can already articulate requirements with some precision — they are engineer-facing; non-engineer scaffolding is universally thin.** The only true interview-first systems are academic (not shipped). gingoa's north star ("a non-engineer develops like a senior") is exactly this market blank.

## Techniques to steal → consolidated in the build standard
The 10 techniques this survey extracted — interview-first adaptive Socratic · ≤2 questions/turn · hidden
5W1H×{functional·NFR·constraint·risk} coverage tracker · serial context · risk-adjusted depth (8/12/18-turn,
15–20 cap) · automated 29148-completeness-stop + risk-gate · least-to-most structured prompt · post-draft
adversarial stress-test · EARS/Given-When-Then acceptance · machine-SSOT + human-view artifact pair — are
turned into the actionable, empirically-grounded recipe in
[`elicitation-interview-build-standard.md`](elicitation-interview-build-standard.md) (the active US-2 build doc).

## Avoid
spec-as-source/generative (Tessl, MDD failure) · exposing the technique menu to the user (BMAD) · fixed question lists / formal graph state-machine (AIRE) · unbounded artifacts (Spec Kit 7-file) · user-only stop · >20-turn marathons.

## Naming & publish-location — fresh survey (2026-06-26)
Two follow-up questions the owner raised — *(a) do the artifact names match the field?* and *(b) is keeping
①-output OFF the remote actually standard?* Two parallel surveys (spec-driven tools + ADR/docs-as-code +
a 10k-repo empirical study). Both findings **challenge a prior gingoa default** — recorded here as evidence;
the gingoa decision is the owner's call (open).

**(a) Naming — `prd.yml`/`PRD.md` diverges from the de-facto vocabulary.** Across Spec Kit
(`spec.md`/`plan.md`/`tasks.md`, `constitution.md`), Kiro (`requirements.md`/`design.md`/`tasks.md`,
`steering/`), BMAD (`prd.md`/`architecture.md`), OpenSpec (`spec.md`/`proposal.md`), Tessl (`*.spec.md`),
and ISO/IEC/IEEE 29148 (StRS/SyRS/**SRS**) — the planning-artifact vocabulary is **"spec" / "requirements"
/ "PRD" / "design"**, *never* "contract". The word **"contract" has three strong prior meanings** that
collide: API/consumer-driven contract testing (Pact, OpenAPI; Spec Kit itself names its API artifact
`contracts/api-spec.json`), design-by-contract (Meyer/Eiffel pre/post/invariant), and the **2025-26
emerging `PRD.md`/AgentContract = AI-agent behavioral-governance** file (present-tense rules a la
CLAUDE.md). A developer seeing `prd.yml`/`PRD.md` most likely reads "API contract" or "agent
governance", not "requirements". Closest standard-aligned set: **`spec.yml` + `SPEC.md` + `BACKLOG.md`**
(Tessl/OpenSpec vocab) or **`requirements.yml` + `REQUIREMENTS.md` + `TASKS.md`** (Kiro vocab). Caveat in
gingoa's favor: gingoa's artifact is *project-level* (meta/intent/risk/derived/adrs), nearer Spec Kit's
**`constitution.md`** / Kiro's **`steering/`** than a per-feature spec — so a project-charter framing
("the agreement on what we're building") is a *defensible* reason to keep "contract", at a real legibility
cost. The **machine-SSOT + human-prose-view split itself is sound and ahead of the field** — no surveyed
tool emits a YAML SSOT + MD mirror at the requirements layer (closest precedents are OpenAPI `openapi.yaml`
+ docs and Terraform `*.tf` + rendered docs, both at the *infra/API* layer, not planning). [lit]

**(b) Publish-location — for an END-USER project, the standard is COMMIT-to-repo, not local.** This
*reverses* the naive read of gingoa's 13–19% publish-axis census. Reference-class matters:
- **Spec-driven-tool cohort (the right reference class) → unanimous commit.** Spec Kit: "specs that live
  outside version control are wishes; specs in version control are requirements." Kiro: "store specs
  directly in your project repository alongside the code." BMAD: "every artifact … immediately committed
  to a Git repository … an auditable blueprint." OpenSpec: "they should be checked in … collaborate
  through git — PRs, reviews." 4/4 design their spec artifacts to be committed + pushed. [lit]
- **ADR / docs-as-code community → 15-yr commit consensus.** Nygard, Fowler (`doc/adr`), GDS Way
  ("architecture decisions … stored in version control … in that application's code repository"),
  adr-tools (`doc/architecture/decisions/`), MADR — unanimous: decision records live in the repo. [lit]
- **Broad-OSS 13–19% is selection bias, not a counter-signal.** A 2026 10k-repo study found `docs/` in
  37.4% of repos — but that population is dominated by solo hobby libraries with *no* requirements process
  (they have no PRD because they need none). gingoa's target user (non-engineer + agent building
  *production-grade* software = a structured process) is exactly the spec-tool cohort, **not** the random
  public-repo aggregate. The census measured the wrong reference class for this decision. [census→reframed]
- **Adjudication.** The "broad OSS rarely exposes planning docs" and "spec tools always commit specs"
  tension dissolves on reference-class: the spec-tool + ADR cohorts ARE gingoa's users; the OSS aggregate
  is not. **Verdict: the elicit FEATURE's emitted artifacts should DEFAULT to a committed dir (pushed),
  override-to-local for NDA'd/private concepts.** Distinct from gingoa-the-harness gitignoring *its own*
  `docs/internal/` dogfood scratch (a legitimate harness-internal choice; says nothing about what the
  feature defaults to for an end-user project). [lit]

## ① artifact-SET completeness — is the *kind set* standard? (survey 2026-06-26)
Owner asked whether the ① output *kinds* match what real repos/tools produce — anything missing or bloated?
Surveyed Spec Kit · Kiro · BMAD · OpenSpec · ISO-29148 · Scrum · PMBOK · Fowler/Thoughtworks. Verdict on the
candidate set {`PRD.md`+`prd.yml`, `BACKLOG.md`, `docs/adr/`}:

- **MISSING (the one real gap): a `constitution`/`steering` layer DISTINCT from the PRD.** *Every* leading SDD
  tool ships it — Spec Kit **`constitution.md`** (immutable principles governing how specs become code),
  Kiro **`steering/`** (`product.md`·`tech.md`·`structure.md` = product purpose + approved stack/tooling +
  folder/naming conventions), BMAD product-brief + decision-log. It is the project's non-negotiable
  rules/stack/structure that governs every requirement — separate from the requirements themselves. **For
  gingoa's OWN project this is NOT missing — `CLAUDE.md`/`AGENTS.md` IS the constitution** (Spec Kit & Kiro
  both accept `AGENTS.md` as the steering/constitution equivalent). The gap is in the **FEATURE output spec**:
  the elicit skill should emit the user project's **`AGENTS.md`/`CLAUDE.md` (constitution)** as a ① artifact
  (gingoa is already a CLAUDE/AGENTS-centered harness → native fit), or a governed "principles" PRD section
  promoted to a file for any project with a persistent agent. [lit]
- **BLOAT / restructure flags:**
  - **`prd.yml` + `PRD.md` as two hand-maintained files = non-standard overhead.** No surveyed tool keeps a
    parallel machine+human pair; standard is YAML-frontmatter-in-one-`.md`, OR **generate one from the other**.
    → keep the split ONLY with **`prd.yml` = SSOT, `PRD.md` = a generated/derived render** (no parallel hand-edit).
  - **`BACKLOG.md` is redundant with PRD user-stories AT ①.** Spec Kit/Kiro/OpenSpec embed stories in the
    requirements doc; BMAD *generates* the backlog from the PRD as a later (②-③) sequenced step. → keep
    `BACKLOG.md` only as a **PRD-DERIVED, stage-mapped view** (the ③ feature-pick runtime), not a parallel SSOT.
  - **`docs/adr/` = KEEP** — Nygard/MADR standard, begins at planning, one file per real decision; not overkill.
- **Minimal-complete standard ① set:** (1) **constitution/steering** (= `AGENTS.md`/`CLAUDE.md`), (2) **PRD**
  (problem·users·stories+acceptance·NFR·MoSCoW·risk; vision/personas/glossary/risk are *sections inside*, not
  separate files), (3) **ADRs**. Roadmap · sequenced-backlog · threat-model · design/tasks = ②+ (not ①). [lit]
- **gingoa verdict:** ADD constitution to the ① output set (native = AGENTS/CLAUDE); make **`prd.yml` the SSOT
  and `PRD.md`/`BACKLOG.md` DERIVED** views; ADRs unchanged. (`prd.yml` SSOT + generated human views also
  resolves the "two-files" bloat — gingoa's machine-SSOT design is *correct* precisely because the others derive.)

## Sources
Spec Kit https://github.com/github/spec-kit · Kiro https://kiro.dev/docs/specs/ · Fowler SDD https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html · EARS https://alistairmavin.com/ears/ · BMAD https://github.com/bmad-code-org/BMAD-METHOD + advanced-elicitation SKILL.md · iReDev https://arxiv.org/abs/2507.13081 · LLMREI https://arxiv.org/abs/2507.02564 · Elicitron https://arxiv.org/abs/2404.16045 · AIRE'23 https://aire-ws.github.io/aire23/papers/AIRE_03.pdf · Follow-Up-QG https://github.com/anmolsinghal98/Requirements-Elicitation-Follow-Up-Question-Generation · SDD survey arXiv:2602.00180 · OpenSpec https://github.com/Fission-AI/OpenSpec · Tessl https://docs.tessl.io/

**Naming & publish survey (2026-06-26):** Spec Kit docs https://github.github.com/spec-kit/ + gitignore disc. https://github.com/github/spec-kit/discussions/2304 · Kiro specs best-practices https://kiro.dev/docs/specs/best-practices/ + steering https://kiro.dev/docs/steering/ · OpenSpec concepts https://github.com/Fission-AI/OpenSpec/blob/main/docs/concepts.md · Tessl specs https://tessl.io/blog/spec-driven-development-10-things-you-need-to-know-about-specs/ · 29148 templates https://www.reqview.com/doc/iso-iec-ieee-29148-templates/ · PRD.md governance pattern https://whatsonyourbrain.com/contract-style-comments-contractmd · AgentContract https://github.com/agentcontract/spec · Fowler ADR https://martinfowler.com/bliki/ArchitectureDecisionRecord.html · GDS Way ADRs https://gds-way.digital.cabinet-office.gov.uk/standards/architecture-decisions.html · adr-tools https://github.com/npryce/adr-tools · "Design docs belong in repos" https://www.junaidahmad.ca/articles/design-docs-belong-in-repos · 10k-repo study arXiv:2605.16701 https://arxiv.org/html/2605.16701

**① artifact-set survey (2026-06-26):** Spec Kit spec-driven.md (constitution as governance) https://github.com/github/spec-kit/blob/main/spec-driven.md + constitution-vs-agent-context disc. https://github.com/github/spec-kit/discussions/1056 · Kiro steering (product/tech/structure) https://kiro.dev/docs/steering/ · BMAD planning https://deepwiki.com/bmad-code-org/BMAD-METHOD/4.4-phase-2:-planning-workflows · Fowler SDD-3-tools https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html · Scrum Guide https://scrumguides.org/scrum-guide.html · PMBOK project charter https://pressbooks.ulib.csuohio.edu/project-management-navigating-the-complexity/chapter/3-1-project-charter/ · Augment "Constitutional SDD"/AGENTS.md https://www.augmentcode.com/guides/what-is-spec-driven-development
