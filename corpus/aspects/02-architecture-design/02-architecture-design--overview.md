---
id: aspect-02-architecture-design
title: "Architecture & Design"
group: "P — Plan & Design"
kind: universal
gated_archetypes: []
cross_cutting: true
lifecycle_stages: ["①", "②"]
anchors: ["SWEBOK-KA2", "SWEBOK-KA3", "ISO-12207-2026-catalog-scope", "arc42", "C4"]
evidence_track: lit
status: review-needed
last_updated: "2026-06-25"
sources:
  - "https://www.computer.org/education/bodies-of-knowledge/software-engineering"
  - "https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions"
  - "https://adr.github.io/madr/"
  - "https://www.industrialempathy.com/posts/design-docs-at-google/"
  - "https://arc42.org/overview"
  - "https://c4model.com/"
  - "https://www.iso.org/standard/78176.html"
  - "https://www.thoughtworks.com/insights/articles/fitness-function-driven-development"
  - "https://research.jku.at/en/publications/using-architecture-decision-records-in-open-source-projects-an-ms/"
claim: "Senior engineers choose a deliberate architectural style for the system's quality attributes, capture each significant decision as a lightweight ADR, document just enough (arc42/C4/design-doc), and where it matters guard the chosen properties with executable fitness functions — design is decided and recorded before code, not reverse-engineered after."
maps_from: ["docs/adr"]
census_todo: "Deferred — needs a targeted workflow-content/topology survey; the existing census records hold derived flags only (not tree contents), so this metric (e.g. architectural-style mix, fitness-function presence, C4/arc42 doc structure) is not offline-derivable. Low priority."
---

> **Standard (claim):** Pick an architectural style deliberately for the target quality attributes, record every significant decision as a lightweight ADR, document *just enough* (arc42 / C4 / design-doc), and guard the chosen properties with fitness functions — design is decided and written *before* code, not reverse-engineered after.
> **Evidence:** [lit] dominant (named standards) + [census] for the publish-axis (ADR/design-doc adoption) · **Confidence:** high · **Kind:** universal · cross-cutting · **Stage:** ①, ②

**Seed sub-aspects:** `architectural styles (layered/microservice/event/hexagonal)` · `ADRs (cross-cutting)` · `quality-attribute tactics` · `DDD / bounded contexts` · `data architecture` · `rendering strategy (web)` · `fitness functions`

## What professional engineers do

- **Choose a style deliberately, driven by quality attributes — not by default.** Architecture is the set of structures + their significant decisions (SWEBOK KA *Software Architecture*; KA *Software Design*). Seniors name the style on purpose: **layered/modular-monolith** as the boring default (lowest coordination cost), **hexagonal/ports-and-adapters** to isolate a domain core from I/O, **event-driven** for decoupling/async fan-out, **microservices** only when independent deploy/scale/team-autonomy actually pays for the distributed-systems tax. The style follows the dominant quality attributes (C3 NFRs in the contract), not fashion. [lit]
- **Map design to quality-attribute tactics.** Each ISO/IEC 25010:2023 attribute has known tactics: *performance* → caching, async, read replicas; *reliability* → redundancy, timeouts, circuit breakers, bulkheads; *security* → least-privilege boundaries, trust-zone isolation; *maintainability* → modular decomposition, dependency inversion. Seniors trace each significant NFR to a concrete structural tactic rather than hoping for it. [lit]
- **Record significant decisions as ADRs — by default, lightweight.** One short immutable record per *architecturally significant* decision: context → decision → consequences (Nygard 2011; MADR template). Significant = affects structure, NFRs, dependencies, or is hard to reverse. ADRs are the cheapest insurance against a decision silently flipping mid-build; the rationale ("why not X") is the part code can never show. Never write empty ritual stubs — only real decisions. [lit]
- **Document just enough — arc42 / C4 / design-doc, not a 100-page tome.** **arc42** = 12-section tailorable template (goals, constraints, context, solution strategy, building blocks, runtime, deployment, crosscutting, decisions, quality, risks, glossary) — keep only the sections that carry weight. **C4** (Brown) = a 4-level zoomable map: Context → Container → Component → Code; most teams draw only Context + Container. **Google-style design doc** = a 3–20 page doc written *before* coding, reviewed like code, centered on tradeoffs — "a code review before the code exists." [lit]
- **Define bounded contexts (DDD) before sharing a model everywhere.** Strategic DDD: split the domain into bounded contexts with explicit ubiquitous language; do not force one canonical model across contexts (that couples everything). Context boundaries become the module/service seams and the data-ownership lines. [lit]
- **Decide data architecture explicitly.** Ownership (one writer per dataset / per bounded context), source-of-truth, schema-evolution + migration strategy, and consistency model (strong vs eventual). Data coupling is the hardest to undo later, so it is a first-class design decision, not an ORM afterthought. [lit]
- **Pick a web rendering strategy on purpose (web archetype).** SSR / SSG / CSR / ISR / streaming is an architectural choice driven by SEO, time-to-interactive, and data freshness — chosen up front, not inherited from a framework default. [lit]
- **Guard the chosen properties with fitness functions.** Where an attribute matters (layering rules, dependency direction, latency budget, bundle size, coverage floor), encode it as an *executable* check that fails the build on violation (Ford/Parsons/Kua, *Building Evolutionary Architectures*, 2017). This is what keeps architecture from eroding silently between commits. [lit]

## Evidence (lit + census)

- **SWEBOK Guide v4.0** (IEEE CS, 2024) — KA *Software Architecture* + KA *Software Design*: architecture = significant structures/decisions; design styles, quality-attribute analysis. [lit] https://www.computer.org/education/bodies-of-knowledge/software-engineering
- **ISO/IEC 25010:2023** — 9 quality attributes the design must target (performance, reliability, security, maintainability, safety, …); the attribute checklist that drives tactic selection. [lit] https://www.iso.org/standard/78176.html
- **ADR — Nygard 2011** + **MADR** (adr.github.io): one-page status/context/decision/consequences. [lit] https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions · https://adr.github.io/madr/
- **arc42** — 12-section tailorable architecture template ("what + how to document, pragmatically"). [lit] https://arc42.org/overview
- **C4 model** — Simon Brown; 4 zoom levels Context→Container→Component→Code. [lit] https://c4model.com/
- **Design Docs at Google** — Malte Ubl: 3–20pp, written before code, reviewed like code, tradeoff-centric. [lit] https://www.industrialempathy.com/posts/design-docs-at-google/
- **Architectural fitness functions** — Ford/Parsons/Kua, *Building Evolutionary Architectures* (2017): executable tests of how close the architecture is to its aim. [lit] https://www.thoughtworks.com/insights/articles/fitness-function-driven-development
- **[census] publish-axis (429-repo governance census, `census-governance/`):** *any* planning/design artifact present = **13% uniform / 19% weighted / 17% young**; **design-doc 11→16%** (rising, most common); formal **ADR dir 2–4%**; RFC 2%. By archetype: monorepo (anyplan 20%, adr 6%) and web (anyplan 21%) lead; **library 5% / mobile 0%**. → seniors *do* design (the doc is mostly [lit]), but they rarely *publish* the artifacts to a public remote. [census]
- **Buchgeher et al. (IEEE Access 2023, 900+ repos)** — corroborates the rarity: ADR adoption low but rising; ~50% of ADR repos hold only 1–5 records ("tried, didn't stick"); Nygard template dominates. Matches our 2–4% ADR figure. [lit] https://research.jku.at/en/publications/using-architecture-decision-records-in-open-source-projects-an-ms/

## Archetype variations

- **library / cli:** API/CLI surface design *is* the architecture — public contract + semver discipline matter more than internal layering. Lightweight: a README architecture note + ADRs for breaking choices; full arc42/C4 is overkill. Census confirms minimal published design (library anyplan 5%).
- **backend / web:** the richest design surface — style choice, bounded contexts, data ownership, deployment topology, and (web) rendering strategy all live. arc42 Context+Container + a design-doc earn their keep.
- **monorepo:** cross-package dependency direction + ownership boundaries (CODEOWNERS = enforced module seams); fitness functions for "no cross-package back-edges" are highly valuable. Highest census adoption (anyplan 20%, adr 6%).
- **data-ml:** pipeline/DAG topology, feature-store + dataset lineage, train/serve skew are the core design concerns; data architecture dominates.
- **mobile:** layered + platform-idiomatic (MVVM/MVI); 0% published design in census — design happens, publication doesn't.
- **ai-harness (8th archetype):** the contract/component-projection structure itself is the architecture; ADRs are the primary durable artifact (gingoa's own case — see below).
- No archetype is *gated* for this aspect — it is universal/cross-cutting; depth scales with the design surface.

## Tradeoffs / what's ruled out

- **Ruled out: BDUF (big design up front).** Document *just enough*; favor tailored arc42 sections + a few ADRs over an exhaustive spec that rots on first commit.
- **Ruled out: zero-design / reverse-engineered architecture.** "Just start coding and the structure will emerge" produces a big ball of mud and unrecorded decisions; the contract (① C3/C7) forces deliberate style + ADRs before ②.
- **Ruled out: microservices-by-default.** The distributed tax (network, eventual consistency, ops surface) is only justified by real independent-deploy/scale needs; modular monolith is the senior default.
- **Tension — record vs. publish:** decisions should always be *recorded* ([lit]) but the census shows seniors mostly *don't publish* them (ADR 2–4%). gingoa resolves this with the two-axis rule: write the ADR (do-it), default it local/team, publish opt-in.
- **Cost of fitness functions:** they add build-time + maintenance; apply only to attributes that actually matter, not as blanket ceremony.

## Sources

- SWEBOK Guide v4.0 (KA Software Architecture / Software Design) — https://www.computer.org/education/bodies-of-knowledge/software-engineering
- ISO/IEC 25010:2023 (quality model) — https://www.iso.org/standard/78176.html
- ADR (Nygard 2011) — https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions
- MADR — https://adr.github.io/madr/
- arc42 — https://arc42.org/overview
- C4 model (Simon Brown) — https://c4model.com/
- Design Docs at Google (Malte Ubl) — https://www.industrialempathy.com/posts/design-docs-at-google/
- Architectural fitness functions (Ford/Parsons/Kua) — https://www.thoughtworks.com/insights/articles/fitness-function-driven-development
- Buchgeher et al., ADRs in OSS (IEEE Access 2023) — https://research.jku.at/en/publications/using-architecture-decision-records-in-open-source-projects-an-ms/

## Sub-documents
- [`design-practice--facts-2026-08.md`](design-practice--facts-2026-08.md) — *research-log (ko)* — 2026-08 facts-only pass: Google design docs · company RFC processes · Nygard ADR · C4 · walking-skeleton/tracer-bullet originals.
