---
id: aspect-01-requirements-planning
title: "Requirements & Planning"
group: "P — Plan & Design"
kind: universal
gated_archetypes: []
cross_cutting: false
lifecycle_stages: ["①"]
anchors: ["SWEBOK-KA1", "ISO-29148", "PMBOK7-Uncertainty"]
evidence_track: lit
status: review-needed
last_updated: "2026-06-25"
sources:
  - "https://www.iso.org/standard/72089.html"
  - "https://ieeexplore.ieee.org/document/8559686"
  - "https://www.iso.org/standard/78176.html"
  - "https://www.computer.org/education/bodies-of-knowledge/software-engineering"
  - "https://datatracker.ietf.org/doc/html/rfc2119"
  - "https://arxiv.org/abs/1611.10288"
  - "https://www.mountaingoatsoftware.com/agile/user-stories"
  - "https://xp123.com/invest-in-good-stories-and-smart-tasks/"
  - "https://www.agilebusiness.org/dsdm-project-framework/moscow-prioritisation.html"
  - "https://theleanstartup.com/principles"
  - "https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions"
  - "https://adr.github.io/madr/"
  - "https://www.industrialempathy.com/posts/design-docs-at-google/"
  - "https://research.jku.at/en/publications/using-architecture-decision-records-in-open-source-projects-an-ms/"
  - "https://github.com/github/spec-kit"
  - "https://kiro.dev/"
  - "https://github.com/bmad-code-org/BMAD-METHOD"
  - "https://arxiv.org/abs/2507.13081"
  - "https://arxiv.org/abs/2507.02564"
  - "https://arxiv.org/abs/2404.16045"
  - "https://alistairmavin.com/ears/"
  - "https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html"
  - "https://martinfowler.com/bliki/ArchitectureDecisionRecord.html"
  - "https://gds-way.digital.cabinet-office.gov.uk/standards/architecture-decisions.html"
  - "https://arxiv.org/html/2605.16701"
  - "https://cdn.standards.iteh.ai/samples/72089/62bb2ea1ef8b4f33a80d984f826267c1/ISO-IEC-IEEE-29148-2018.pdf"
  - "https://www.cwnp.com/req-eng/"
  - "https://ieeecs-media.computer.org/media/education/swebok/swebok-v4.pdf"
  - "https://www.perforce.com/resources/alm/requirements-traceability-matrix"
  - "https://www.scrum.org/resources/blog/walking-through-definition-ready"
  - "https://agilealliance.org/glossary/definition-of-ready/"
  - "https://www.atlassian.com/agile/product-management/prioritization-framework"
claim: "Senior practice turns a vague idea into a precise, machine-actionable requirements baseline — INVEST user stories with acceptance criteria, an ISO/IEC 25010 NFR sweep, 29148/RFC-2119 requirement quality, a MoSCoW scope cut, and ADR-recorded decisions — because under-specified requirements are the #1 RE pain (NaPiRE) and rigorous specs are what AI coding agents must be given, not guess."
maps_from: ["census-data/census-governance"]
---

> **Standard (claim):** Turn a non-engineer's idea into a precise requirements baseline — INVEST stories
> with acceptance criteria, an ISO 25010 NFR sweep, 29148/RFC-2119 requirement quality, a MoSCoW scope cut,
> and ADR-recorded decisions — so the build runs from a spec, not a guess.
> **Evidence:** lit-anchored, partially censused (planning-artifact *presence* only) · **Confidence:** high · **Kind:** universal · **Stage:** ①

**Seed sub-aspects** (expand during collection): `elicitation (Socratic)` · `functional + NFR (ISO-25010 sweep)` · `29148 quality (full §5.2.5–5.2.6 set)` · `MoSCoW / scope cut` · `risk register (non-security)` · `estimation-light` · `DoR / DoD / acceptance criteria`

## What professional engineers do
Before writing code, a senior engineer converts intent into a durable, reviewable baseline. The work
follows the **SWEBOK v4 Software Requirements** flow — **elicit → analyze → specify → validate** [lit, normative] —
producing artifacts an agent (or another engineer) can build from without guessing.

- **Elicitation (Socratic).** Don't take a feature wishlist at face value; *draw out* problem, users,
  must-have outcomes, quality bars (security? scale? uptime?), and constraints via a structured inception
  interview. SWEBOK names elicitation as the first KA activity; a non-engineer doesn't know NFRs or
  acceptance criteria are even askable, so the interviewer fills that gap. [lit]
- **Functional baseline + acceptance criteria.** Capture functionality as **user stories** ("As a ⟨role⟩
  I want ⟨feature⟩ so that ⟨value⟩"), each meeting **INVEST** (Independent, Negotiable, Valuable,
  Estimable, Small, Testable) and each carrying **testable acceptance criteria** that define "done" per
  story — not a vague "should work." [lit]
- **NFR sweep (ISO/IEC 25010).** Functional needs alone are insufficient. Sweep the **9 product-quality
  characteristics** of ISO/IEC 25010:2023 (functional suitability, performance efficiency, compatibility,
  interaction capability, reliability, security, maintainability, flexibility, **safety** [added 2023]) as
  a checklist so reliability/security/safety are named in ① — not discovered in production. [lit]
- **Requirement quality (29148 + RFC 2119).** Write each requirement against the **full ISO/IEC/IEEE
  29148:2018 well-formedness set**, not a subset. Each *individual* requirement (§5.2.5) must be
  **necessary · appropriate · unambiguous · complete · singular · feasible · verifiable · correct ·
  conforming · traceable** (10 characteristics); the requirement *set* (§5.2.6) must be **complete ·
  consistent · feasible · comprehensible · able-to-be-validated** (5). Use the
  `[condition][subject][action][object][constraint]` shape and **RFC 2119 / BCP 14** keyword levels
  (uppercase **MUST/SHOULD/MAY** = normative, lowercase = prose). This is the difference between a spec an
  agent can build and a hope it must interpret. [lit]
- **Validate, and trace.** Specifying is not validating — SWEBOK v4 KA1 makes **validation** a distinct
  activity (requirements reviews/inspection, prototyping, model validation, **every requirement carries an
  acceptance test**), and the 29148 quality set above is the machine pass-criterion (Spec Kit's `/analyze`
  is the cross-artifact-consistency analogue). Each requirement gets a stable ID and a forward/backward
  **traceability** link (req → ADR/design → acceptance-test), so a spec change can cascade deterministically
  for an agent rather than silently desync. The craft of validate + trace (and the classic elicitation/
  stakeholder/prioritization toolkit) is in [`requirements-engineering-craft.md`](requirements-engineering-craft.md). [lit]
- **Definition of Ready (entry gate).** Mirror of the DoD: before a story enters build it must be
  **DoR-clean** — INVEST satisfied, acceptance criteria present, dependencies/assumptions resolved, and
  29148-clean — so the agent is never handed an under-specified item. (See
  [`requirements-engineering-craft.md`](requirements-engineering-craft.md).) [lit]
- **MoSCoW / scope cut.** Classify every item **Must / Should / Could / Won't**; the Must set is the MVP.
  DSDM guidance keeps Must effort ≲60% so the first slice ships. Pairs with the **Lean Startup MVP** —
  the simplest version that maximizes validated learning. (MoSCoW filters the MVP cut; **RICE** ranks many
  candidates and **Kano** classifies basic/performance/delighter — see
  [`requirements-engineering-craft.md`](requirements-engineering-craft.md).) [lit]
- **Risk register (non-security).** Surface delivery/technical/assumption risks early as a lightweight,
  living list — the planning counterpart to the NFR sweep; security-specific risk lives in its own aspect.
  [inferred]
- **Estimation-light.** Stories are sized only enough to confirm they're *Estimable* and *Small* (the
  E/S in INVEST) and to right-size the MVP cut — not heavyweight upfront estimation. [inferred]
- **Decision record (ADR/MADR).** Record each architecturally significant decision as one short
  **ADR** (Nygard: status / decision / consequences; **MADR** is the Markdown form) so rationale survives
  and decisions don't silently reverse mid-build. Google's **design-doc** practice is the same senior
  instinct: a short doc written *before* code, reviewed like code, trade-offs front and center
  ("a code review before the code"). [lit]
- **Why now (AI era).** Spec-first is validated not just by classic RE but by the AI coding frontier:
  **GitHub Spec Kit** and **Amazon Kiro** independently converge on rigorous-spec → agent-implement
  (Specify → Plan → Tasks → Implement), treating the spec as a living, executable artifact because
  coding agents need unambiguous instruction. [lit]
- **AI-agentic elicitation — the non-engineer frontier.** A 2026 survey of spec-driven tools (Spec Kit,
  Kiro, Tessl, OpenSpec), agentic PRD frameworks (BMAD-METHOD), and RE-with-LLM research (iReDev,
  LLMREI, Elicitron) found one universal gap: **every shipped tool assumes the user can already
  articulate requirements (engineer-facing); non-engineer scaffolding is thin.** The only true
  *interview-first* + automated-stop systems are academic. The evidence-backed elicitation techniques:
  **≤2 questions/turn** (iReDev), **least-to-most prompts with expertise/complexity adaptation** (LLMREI,
  measurably > generic prompts), a **hidden 5W1H × {functional/NFR/constraint/risk} coverage tracker**,
  **serial context** (each question sees all prior — Elicitron), **risk-adjusted depth** (8/12/18 turns,
  15–20 cap — AIRE), **automated completeness-stop vs ISO 29148 quality attributes** (iReDev), a
  **post-draft adversarial stress-test** (pre-mortem/inversion/paradox — BMAD), and **EARS / Given-When-
  Then** acceptance. AVOID spec-as-source code-generation (Tessl = the MDD maintenance-failure) and
  fixed question lists / formal interview state-machines (harder for LLMs than structured prompts). Full
  survey + technique catalog: [`elicitation-prior-art.md`](elicitation-prior-art.md). [lit]

## Evidence (lit + census)
**Literature.**
- SWEBOK v4 *Software Requirements* KA — elicit/analyze/specify/validate flow. [lit, normative]
- ISO/IEC/IEEE 29148:2018 — well-formed-requirement characteristics: 10 *individual* (§5.2.5: necessary,
  appropriate, unambiguous, complete, singular, feasible, verifiable, correct, conforming, traceable) +
  5 *set-level* (§5.2.6: complete, consistent, feasible, comprehensible, able-to-be-validated). [lit]
- ISO/IEC 25010:2023 — 9-characteristic product-quality model (safety added 2023); supersedes the 2011
  8-attribute model. [lit]
- RFC 2119 + RFC 8174 (BCP 14) — requirement-level keywords. [lit, normative]
- Connextra/Cohn *User Stories Applied* (2004) + INVEST (Wake, XP123, 2003). [lit]
- MoSCoW (Clegg 1994; DSDM) — Must effort ≲60%, Could ~20%. [lit, normative]
- Lean Startup (Ries 2011) — MVP / build-measure-learn. [lit]
- ADR (Nygard 2011) + MADR (adr.github.io). [lit]
- **NaPiRE** ("Naming the Pain in RE", Méndez Fernández & Wagner et al., *EMSE* 2017; 228 companies /
  10 countries): industry RE problem **#1 = incomplete/hidden requirements**, #2 = team↔customer
  communication flaws, under-specification, moving targets — empirical proof of the exact gap the harness
  fills. [lit]
- Buchgeher et al. (*IEEE Access* 2023, 900+ repos): ADR adoption low but rising yearly; ~50% of
  ADR-using repos hold only 1–5 ADRs ("tried but didn't stick") — corroborates the census ADR scarcity.
  [lit]

**Census (429 repos, ref 2026-06-24, `census-governance/`).** Planning artifacts are a *publish*
signal, not a quality measure — only the *presence* of public ①-output is censusable; contract content
is absent from repos, so ①'s body stays `[lit]`:
- Any planning artifact (ADR/RFC/design-doc): **13% uniform / 19% weighted / 17% young**. [census]
- design-doc 11→**16%** weighted (most common, rising); formal **ADR dir 2–4%** (scarce); RFC 2%. [census]
- By archetype: web-app 21% · monorepo 20% · other 14% · backend-service 13% · data-ml 13% · cli 10% ·
  **library 5% · mobile 0%** — team/collaborative projects record decisions in writing far more. [census]

## Archetype variations
Universal aspect (fires for every archetype at ①) — what *varies* is emphasis, not whether it applies:
- **library / cli** — thin intent (small NFR surface); API contract & semver-compatibility decisions
  dominate the ADR set. Lowest real-world planning-doc adoption (library 5%, cli 10%) — gingoa still runs
  the full sweep, just yielding a smaller contract.
- **web-app / backend-service** — heavier NFR sweep (performance, security, reliability, uptime);
  highest census planning adoption (web 21%, backend 13%), so the PRD is richest here.
- **monorepo** — multi-package scope cut + ownership/boundary decisions; 20% adoption, the most
  ADR-prone (6%).
- **data-ml** — adds data-provenance, reproducibility, and model-quality NFRs to the 25010 sweep.
- **mobile** — 0% public planning artifacts in census, yet store-review / offline / device-matrix
  constraints make the NFR sweep *more* load-bearing — a clear gap the harness fills rather than mirrors.

No gated archetypes (`gated_archetypes: []`).

## Tradeoffs / what's ruled out
- **Scoped contract, not a generic PRD.** Each field is included *because* it selects a downstream
  foundation/build decision; fields that drive nothing in ②/③ are out of scope. Rules out exhaustive
  template-PRD bloat. [inferred]
- **Spec-first vs. just-build.** Rigorous up-front spec costs interview time; ruled *in* because under-
  specification is the empirically #1 failure mode (NaPiRE) and agents amplify ambiguity. Estimation and
  risk stay *light* to avoid waterfall over-planning.
- **Publish axis.** Planning *activity* follows literature (always do it). *Publishing* is **reference-class
  dependent** — a 2026-06-26 survey (see [`elicitation-prior-art.md`](elicitation-prior-art.md) §Naming &
  publish) sharpens the earlier 13–19% read: the broad-OSS census is the *wrong* reference class (solo hobby
  repos with no requirements process — selection bias). For gingoa's actual user (non-engineer building
  *production-grade* software = the spec-driven-tool + ADR cohort), that cohort is **unanimous: commit specs
  to the repo + push** (Spec Kit/Kiro/BMAD/OpenSpec; Nygard/GDS/adr-tools). → **the elicit FEATURE's
  end-user output should DEFAULT to a committed dir**, override-to-local for private/NDA concepts. Distinct
  from gingoa-the-harness gitignoring its *own* `docs/internal/` dogfood scratch (harness-internal choice).
  [open gingoa decision — owner call] [lit]
- **Measured presence ≠ measured quality.** The census proves only that public ADR/design-docs exist in
  13–19% of repos, not that planning was *good*; contract content isn't in repos, so the rigor claim
  rests on `[lit]`.

## Sources
- ISO/IEC/IEEE 29148:2018 — https://www.iso.org/standard/72089.html · https://ieeexplore.ieee.org/document/8559686 · §5.2.5–5.2.6 quality set: https://cdn.standards.iteh.ai/samples/72089/62bb2ea1ef8b4f33a80d984f826267c1/ISO-IEC-IEEE-29148-2018.pdf · https://www.cwnp.com/req-eng/
- ISO/IEC 25010:2023 — https://www.iso.org/standard/78176.html
- SWEBOK Guide v4.0 (IEEE CS, 2024) — https://www.computer.org/education/bodies-of-knowledge/software-engineering · KA1 PDF: https://ieeecs-media.computer.org/media/education/swebok/swebok-v4.pdf
- RFC 2119 / BCP 14 — https://datatracker.ietf.org/doc/html/rfc2119
- NaPiRE (Méndez Fernández & Wagner et al., EMSE 2017) — https://arxiv.org/abs/1611.10288
- User Stories (Connextra/Cohn) — https://www.mountaingoatsoftware.com/agile/user-stories
- INVEST (Wake, XP123 2003) — https://xp123.com/invest-in-good-stories-and-smart-tasks/
- MoSCoW (DSDM / Agile Business Consortium) — https://www.agilebusiness.org/dsdm-project-framework/moscow-prioritisation.html
- The Lean Startup (Ries 2011) — https://theleanstartup.com/principles
- ADR (Nygard 2011) — https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions
- MADR — https://adr.github.io/madr/
- Design Docs at Google (Ubl) — https://www.industrialempathy.com/posts/design-docs-at-google/
- Buchgeher et al., ADRs in OSS (IEEE Access 2023) — https://research.jku.at/en/publications/using-architecture-decision-records-in-open-source-projects-an-ms/
- GitHub Spec Kit — https://github.com/github/spec-kit
- Amazon Kiro — https://kiro.dev/
- BMAD-METHOD (brownfield `document-project`) — https://github.com/bmad-code-org/BMAD-METHOD
- OpenSpec (Fission AI, delta specs) — https://github.com/Fission-AI/OpenSpec
- Aider repo-map — https://aider.chat/docs/repomap.html · Repomix — https://repomix.com/

## Sub-documents
- [`requirements-engineering-craft.md`](requirements-engineering-craft.md) — *research-log* — classic RE craft: traceability (RTM/req-IDs) · validation & V&V (distinct from elicit/analyze) · elicitation-technique catalogue · stakeholder identification · Definition of Ready · prioritization beyond MoSCoW (RICE/Kano) · assumptions/constraints/dependencies · lightweight estimation.
- [`planning-document-family.md`](planning-document-family.md) — *research-log* — the DEFINITIVE planning/spec document family: KINDS × sections/content/naming/location/publish + project-vs-feature boundary + gh naming census.
- [`decision-record-standard.md`](decision-record-standard.md) — *research-log* — decision-record family (ADR/RFC/design-doc/decision-log/steering) + Nygard/MADR ADR sections + the IS/ISN'T-an-ADR refactor rubric.
- [`elicitation-prior-art.md`](elicitation-prior-art.md) — *research-log* — AI-agentic requirement-elicitation prior-art + naming/publish-location survey + the ① artifact-set verdict.
- [`brownfield-planning-adoption.md`](brownfield-planning-adoption.md) — *research-log* — the ①-plan slice of the `adopt` model: import / convert / reverse-engineer an existing project's requirements (flatten-first, INFERRED-until-confirmed); spec-driven-tool survey (BMAD/Spec Kit/Kiro/OpenSpec/Tessl/Aider).
- [`elicitation-interview-build-standard.md`](elicitation-interview-build-standard.md) — *reference* — the BUILD standard for the US-2 elicitation interview engine, across 7 prior-art families (AI-spec tools · Mom-Test/JTBD customer-discovery · classic RE Volere/Gause-Weinberg · GORE obstacle analysis · LLM info-gain question selection · EARS/Gherkin notation · Working-Backwards forcing function): question style/selection/coverage/architecture/output/lock-gate + the 3 layers a narrow view misses.
- [`constitution-authoring-standard.md`](constitution-authoring-standard.md) — *research-log* — how to author the agent constitution (`AGENTS.md`/`CLAUDE.md`): section skeleton, <200-line + dual-file SSOT/mirror rule, anti-patterns (empirical), discovery mechanics.
- [`planning-output-census.md`](planning-output-census.md) — *census* — planning-artifact prevalence across 267 high-star repos: AGENTS.md 35% / CLAUDE.md 29% (constitution = mainstream) · docs/ 64% · CHANGELOG 43% · but PRD.md 0.4% / ADRs 1.1% (rare in the broad aggregate = selection bias; standard in gingoa's structured-process cohort) · `prd.yml` machine-SSOT = 0 repos (novel / ahead of field).
- [`requirements--facts-2026-08.md`](requirements--facts-2026-08.md) — *research-log (ko)* — 2026-08 facts-only pass: ISO-29148 · 3C · INVEST · GWT/EARS · Mom Test · PRD/1-pager · PR/FAQ · Shape Up pitch/appetite, per-claim URLs + source-tier tags.
- [`estimation-failure-data--facts-2026-08.md`](estimation-failure-data--facts-2026-08.md) — *research-log (ko)* — 2026-08 facts-only pass: CHAOS figures + Eveleens&Verhoef critique side-by-side · McKinsey-Oxford · Boehm curve + 2001 revision · Cone of Uncertainty · Jørgensen estimation data · scope-creep stats · AI-impact figures (secondary-source flagged).
