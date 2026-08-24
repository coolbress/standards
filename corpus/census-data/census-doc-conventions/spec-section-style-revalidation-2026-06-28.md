# Per-feature spec — SECTIONS × AUTHORING-STYLE re-validation (2026-06-28)

> Raw deposit (research-deposit-rule). Owner-requested deep re-research scoped to **(1) the content SECTIONS a
> per-feature spec contains and (2) its AUTHORING STYLE**, and the central question **"do architecture + design
> decisions + rejected alternatives live in the requirements spec or in a separate design doc?"** Method: a
> WebSearch/WebFetch researcher across authoritative standards/papers + modern SDD frameworks + practitioner
> articles + real high-profile repos, **plus** a fresh GitHub `search/code` filename census run locally.
> Learnings folded into [`../../aspects/01-requirements-planning/planning-document-family.md`](../../aspects/01-requirements-planning/planning-document-family.md)
> (the "Re-validation (2026-06-28)" section). Supersedes nothing; **sharpens** the spec/design boundary from the
> 2026-06-27 pass (which left a doc-level Decisions & Rationale ambiguity, REFINE note b).

## Fresh GitHub census (2026-06-28, `gh api search/code total_count`; code-search caveats apply)

| Query | total_count |
|---|---|
| `filename:spec.md` (any path) | **44,640** |
| `filename:design.md` (any path) | **37,024** |
| `filename:requirements.md` (any path) | **10,776** |
| `filename:spec.md path:docs/specs` | 3,632 |
| `filename:design.md path:docs/specs` | **4,552** |
| `filename:requirements.md path:.kiro/specs` | 2,112 |
| `filename:design.md path:.kiro/specs` | **2,492** |

**Reading — the separation signal is decisive.** `design.md` (37k) is nearly as prevalent as `spec.md` (44.6k)
globally; a world that merged design into the spec would not produce that many standalone `design.md` files.
Inside the canonical per-feature directories the co-occurrence is near-1:1 and design **leads**: `docs/specs/`
holds *more* `design.md` (4,552) than `spec.md` (3,632); `.kiro/specs/` holds *more* `design.md` (2,492) than
`requirements.md` (2,112). The cohort that runs a structured per-feature spec process keeps **two separate files
(requirements + design)** as the norm — not one merged file.

## Authoritative SECTION lists (verbatim / closely-paraphrased; primary sources)

### Standards / papers
- **ISO/IEC/IEEE 29148:2018 SRS** — Ch1 Introduction (Purpose · Scope · Refs · Defs) · Ch2 Overall/Product
  Description (Product perspective · functions · user characteristics · **Constraints** · **Assumptions &
  Dependencies** · apportioning) · Ch3 Specific Requirements (External interfaces · Functions · Usability ·
  Performance · DB · **Design constraints** · Standards compliance · System attributes) · Ch4 Verification ·
  Ch5 Supporting info. **SRS is implementation-free; design lives in a separate SDD.** Individual-requirement
  quality (§5.2.5, 10 props): necessary · appropriate · unambiguous · complete · **singular** · feasible ·
  **verifiable** · correct · conforming · **traceable**. Set quality (§5.2.6): complete · consistent · feasible ·
  comprehensible · validatable.
- **IEEE 830-1998 SRS** — §1 Introduction · §2 Overall Description (incl. §2.5 **Design and Implementation
  Constraints** = bounds ON the solution, not the design) · §3 Specific Requirements · §4/§5 appendices/index.
  Props: unambiguous · complete · consistent · ranked · verifiable · modifiable · traceable.
- **IEEE 1016-2009 SDD** — the SEPARATE design description: System overview · **Architecture** · Detailed design
  (Data · Component · Interface) · design decisions + rationale. Explicitly the home of architecture/decisions the
  SRS excludes.
- **SWEBOK v4 KA1** — activities, not a template; names **"Acceptance Criteria-Based Requirements Specification"**
  as a first-class approach (validates EARS/GWT) and **Requirements Tracing** (§7) as a first-class activity.
  Requirements (KA1) is a distinct Knowledge Area from **Software Design (KA2)**.
- **EARS (Mavin, RE'09)** — 6 patterns: Ubiquitous `The <sys> shall <resp>` · State `While <pre>, the <sys>
  shall …` · Event `When <trigger>, the <sys> shall …` · Optional `Where <feature>, the <sys> shall …` ·
  Unwanted `If <trigger>, then the <sys> shall …` · Complex (While+When).
- **RFC 2119 / 8174** — MUST/SHALL · MUST NOT/SHALL NOT · SHOULD · SHOULD NOT · MAY; normative **only when
  uppercase** (8174).

### Modern SDD frameworks (their ACTUAL templates)
- **GitHub Spec-Kit** — `spec.md` (User Scenarios & Testing [mandatory] · Requirements: Functional + Key Entities
  [mandatory] · Success Criteria [mandatory] · Assumptions · inline `[NEEDS CLARIFICATION]`) = **"WHAT users need
  and WHY", implementation-free**. `plan.md` (Summary · Technical Context · Constitution Check · Project Structure ·
  Complexity Tracking) = **the HOW; tech stack + architectural decisions live here**. `tasks.md` (phased by user
  story, `[P]` parallel markers). → **spec/design split across files.**
- **Amazon Kiro** — `requirements.md` (EARS acceptance criteria "WHEN … THE SYSTEM SHALL …" · FRs · edge cases ·
  regression "SHALL CONTINUE TO") = WHAT. `design.md` (architecture · sequence diagrams · data models · **tech
  choices** · error handling · testing strategy) = HOW. `tasks.md`. → **explicit separate files.**
- **OpenSpec** — `proposal.md` (rationale/scope) · `specs/` (requirements + scenarios) · `design.md` (technical
  approach) · `tasks.md`. → **four separate artifacts.**
- **BMAD-METHOD** — PM persona → PRD; **Architect persona → architecture** (separate by persona/artifact).
- **Tessl** — spec-as-source (MDD); a different paradigm (the spec *is* the codegen model), not a per-feature
  requirements doc — excluded as non-comparable (per martinfowler.com analysis).

### Practitioner / governance (note: RFC-class are a DIFFERENT artifact type)
- **Google design doc (Ubl)** — Context/Scope · Goals/Non-Goals · **The Actual Design** · **Alternatives
  Considered** · Cross-cutting concerns. (A *design* doc — presupposes requirements; drives to design + alts.)
- **Pragmatic Engineer survey** — Google/Uber/Sourcegraph: PRD and engineering design doc **run side-by-side as
  separate documents**; Stripe/Peloton use PRDs AND design docs AND ADRs separately.
- **Rust RFC** — Summary · Motivation · Guide-level · Reference-level · Drawbacks · **Rationale and alternatives** ·
  Prior art · Unresolved. **Python PEP 12** — Abstract · Motivation · Specification · **Rationale** · **Rejected
  Ideas**. **K8s KEP** — Summary · Motivation(Goals/Non-Goals/User-Stories/Risks) · Proposal · **Design Details** ·
  PRR · Drawbacks · **Alternatives**. All three keep motivation ≠ design as *sections* in one file because they are
  **community-deliberation proposals**, not build-time per-feature specs.

## Question B — verdict (STRONG, not contested)
1. **Requirements spec (`spec.md`/`requirements.md`) = implementation-free WHAT** — user stories · EARS acceptance ·
   FR-NNN · NFR deltas · edge cases · assumptions/constraints · out-of-scope. **No architecture, no tech choices, no
   alternatives.** Unanimous: ISO 29148, IEEE 830, SWEBOK KA1, Spec-Kit, Kiro, OpenSpec.
2. **Design doc (`design.md`/`plan.md`/SDD) = HOW** — architecture · data model · API · **key design decisions with
   alternatives + rationale** · error handling · security · testing strategy. Unanimous: IEEE 1016, SWEBOK KA2,
   Spec-Kit `plan.md`, Kiro `design.md`, Google design doc.
3. **ADRs = individually significant decisions, separate `docs/adr/NNNN-kebab.md`** (Nygard/MADR/GDS/AWS).
4. **The merge exception (RFC/PEP/KEP/RFD) is a different artifact class** (community deliberation) — do NOT import
   into per-feature implementation specs. Even they separate motivation from design as sections.

## Authoring-style standard (consolidated, cited)
- Per-requirement: the **29148 §5.2.5 ten properties** (esp. **singular** · **verifiable** · **traceable** ·
  **implementation-free/appropriate**); the **set-level §5.2.6 five**.
- Acceptance criteria in **EARS** (event-driven `WHEN … SHALL` dominant; state `WHILE`; unwanted `IF … THEN`);
  Gherkin/GWT only when the AC must double as an executable test.
- Normative keywords **RFC 2119 uppercase** SHALL/SHOULD/MAY.
- **FR-NNN stable IDs** + backward (→ source/PRD) and forward (→ design → test) links = the RTM spine.
- **INVEST** per user story (story = container; EARS AC = the verifiability inside it).
- **Structured** (lists/tables/EARS/numeric thresholds) for stories/AC/FR/NFR/tasks; **prose** for context/rationale.
- **`[NEEDS CLARIFICATION]` inline** at each ambiguity (Spec-Kit; agent-scannable; lock-gate "0 markers").

## Definitive standard (the synthesis to fold)
> A per-feature spec is **four files** under `docs/specs/<slug>/`: **`spec.md`** (implementation-free requirements:
> overview → user stories P1/P2/P3 → EARS acceptance → FR-NNN (RFC 2119, singular, verifiable, traceable) → NFR
> deltas → edge cases → assumptions/constraints → out-of-scope; `[NEEDS CLARIFICATION]` inline) · **`design.md`**
> (architecture → data model → API → **key design decisions + alternatives + rationale** → error handling →
> security → testing strategy → NFR approach) · **`plan.md`** · **`tasks.md`**. Architecture + decisions + rejected
> alternatives belong in **`design.md`** (significant ones additionally as `docs/adr/NNNN-kebab.md`), **never in
> `spec.md`.** Confirmed by ISO 29148:2018, IEEE 830/1016, SWEBOK v4, Spec-Kit, Kiro, OpenSpec; the fresh census
> shows design.md co-occurring with (and slightly out-numbering) spec.md inside the canonical dirs.

## Sources
ISO/IEC/IEEE 29148:2018 https://ieeexplore.ieee.org/document/8559686 · 29148 SRS LaTeX template
https://github.com/wxinix/IEEE-29148-SRS-LaTeX-Template · well-architected-guide 29148
https://www.well-architected-guide.com/documents/iso-iec-ieee-29148-template/ · IEEE 830-1998
https://standards.ieee.org/standard/830-1998.html · IEEE 1016-2009 https://ieeexplore.ieee.org/document/5167255/ ·
SWEBOK v4 KA1 http://swebokwiki.org/Chapter_1:_Software_Requirements · EARS (Mavin RE'09)
https://alistairmavin.com/ears/ · https://dl.acm.org/doi/10.1109/RE.2009.9 · RFC 2119
https://datatracker.ietf.org/doc/html/rfc2119 · RFC 8174 https://www.rfc-editor.org/rfc/rfc8174.html · Spec-Kit
templates https://github.com/github/spec-kit/tree/main/templates · Kiro specs https://kiro.dev/docs/specs/ ·
Kiro best-practices https://kiro.dev/docs/specs/best-practices/ · OpenSpec https://github.com/Fission-AI/OpenSpec ·
BMAD-METHOD https://github.com/bmad-code-org/BMAD-METHOD · martinfowler SDD-3-tools
https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html · Google design docs (Ubl)
https://www.industrialempathy.com/posts/design-docs-at-google/ · Pragmatic Engineer RFC/design docs
https://newsletter.pragmaticengineer.com/p/software-engineering-rfc-and-design · Oxide RFD
https://rfd.shared.oxide.computer/rfd/0001 · K8s KEP template
https://github.com/kubernetes/enhancements/blob/master/keps/NNNN-kep-template/README.md · Rust RFC template
https://github.com/rust-lang/rfcs/blob/master/0000-template.md · Python PEP 12 https://peps.python.org/pep-0012/ ·
ProductCompass PRD https://www.productcompass.pm/p/prd-template · Nygard ADR
https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions · MADR https://adr.github.io/madr/ ·
Perforce RTM https://www.perforce.com/resources/alm/requirements-traceability-matrix
