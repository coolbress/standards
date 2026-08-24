---
id: aspect-01-requirements-planning--decision-record-standard
title: "Decision-record family + ADR standard + IS/ISN'T-an-ADR refactor rubric (DEFINITIVE)"
parent: aspect-01-requirements-planning
kind: research-log
evidence_track: lit
status: review-needed
last_updated: "2026-06-26"
method: "Deep anti-supersede survey (2026-06-26): Nygard original, MADR (adr.github.io/madr), AWS Prescriptive Guidance, MS Azure WAF, Google design-docs, Rust/IETF RFC, ThoughtWorks Radar, ISO/IEC/IEEE 42010, Zimmermann ozimmer.ch. Defines the FINAL ADR standard + the boundary of what IS vs ISN'T an ADR + a refactor rubric for an existing ADR set."
---

# Decision-record family + ADR standard

## KINDS — five decision-adjacent docs that get confused (don't interchange)
| Kind | Tense | Mutable? | Scope | Purpose / vs ADR |
|---|---|---|---|---|
| **ADR** | "we decided" | **immutable** once accepted | one closed decision | RECORDS a made decision + rationale + consequences |
| **RFC** | "we propose" | open during review | one proposal | EXPLORES before deciding (Motivation/Alternatives/Unresolved); may become an ADR |
| **Design doc / tech spec** | mixed | live then archived | one feature/system design | EXPLORES the full design space (goals/non-goals/diagrams/trade-offs); 1–20pp |
| **Decision log** | — | append-only index | indexes all ADRs | a summary TABLE over ADRs, not a decision doc |
| **Steering / constitution** | present-tense RULE | amended in place | governing rules corpus | a standing RULE, not a time-stamped decision; no status lifecycle |

## ADR proper
**Required sections — Nygard minimal (the dominant default for lean/greenfield):**
**Title** (numbered noun phrase) · **Status** (proposed→accepted→superseded/deprecated/rejected) · **Context**
(forces, value-neutral facts) · **Decision** (active voice, "we will…") · **Consequences** (ALL — incl.
negative/neutral; the highest-value, most-skipped section). Nygard norm = 1–2 pages.
**MADR full (collaborative/enterprise):** adds Decision-Drivers · Considered-Options · per-option Pros/Cons ·
Confirmation · More-info · YAML front-matter (status/date/deciders). Use the option-comparison scaffold ONLY
when alternatives genuinely need weighing. **Recommended default = Nygard-minimal + lightweight metadata
(date/deciders/related)** — exactly what gingoa's ADRs already do.

**Naming:** `NNNN-kebab-case-title.md` (4-digit zero-padded dominant; numbers never reused; superseded keeps
its number). **Location:** `docs/adr/` (most greppable) or `docs/decisions/` (MADR) or `doc/adr/` (Nygard) —
census ~equal; pick one. **Status lifecycle:** proposed → accepted (**immutable** — supersede, never edit) →
superseded-by-NNNN | deprecated | rejected (keep rejected — prevents re-litigation). **Publish:** committed to
VCS alongside code (the reason ADRs beat wiki entries — diffable, PR-reviewable); proposed ADR = a PR, merge =
accept. gingoa's `Publish: local/team` on internal ADRs is a sound extra qualifier.

## The IS / ISN'T-an-ADR boundary
**Architecturally-significant test (Richards/Ford via AWS; Zimmermann; 42010 ASR; Booch "costly to change").**
Write an ADR iff the decision affects ≥1 of: **structure · NFRs · dependencies · interfaces · construction
techniques (libs/frameworks/tools)** AND is **hard to reverse / cross-cutting**. Binary check: (1) would a new
member be misled by not knowing this was decided? (2) would reversing it require non-trivial restructuring or
renegotiating contracts? Both yes → ADR.

**Misclassification list (often wrongly filed as ADRs) → where they belong:**
| Looks like | Why not an ADR | Belongs in |
|---|---|---|
| "We will support multi-tenant accounts" | a product REQUIREMENT (what), not an architectural choice (how) | **PRD** / feature spec |
| "All files use kebab-case" | a standing RULE (amended in place, no status) | **steering** (AGENTS/CLAUDE, .editorconfig, CONTRIBUTING) |
| "How to deploy a hotfix" | a PROCEDURE, not a decision | **runbook / how-to** |
| "Migrate DB in Q3" | a TASK/plan with a deadline | **issue tracker / plan** |
| "Proposed: adopt GraphQL [options open]" | an open PROPOSAL under discussion | **RFC** |
| 15-section design w/ diagrams+schemas titled ADR | a DESIGN DOC; cramming kills ADR-log navigability | **design.md** (+ a short ADR linking it) |

## Refactor rubric (apply to each existing decision record, in order)
1. standing RULE (persists, amended in place)? → **MOVE-to-steering**.
2. product REQUIREMENT (what the product does)? → **MOVE-to-PRD**.
3. step-by-step PROCEDURE? → **MOVE-to-runbook**.
4. TASK/milestone with a deadline? → **DELETE-from-ADRs → issue tracker**.
5. open PROPOSAL (options unevaluated, not committed)? → **MOVE-to-RFC** (convert to ADR when closed).
6. detailed DESIGN (diagrams/schemas/impl)? → **MOVE-to-design-doc** (extract a short decision-ADR linking it).
7. substantially DUPLICATES another ADR? → **MERGE** (keep fuller, cross-ref, supersede the dup).
8. factually wrong + fully reversed + no historical value? → **DELETE** (rare; default = preserve superseded/rejected).
Else → **KEEP-as-ADR**; verify it has Title/Status/Context/Decision/Consequences(incl. negatives).
Quick examples: "chose PostgreSQL because JSONB+expertise" KEEP · "use 2-space indent" →steering · "users reset
password via email" →PRD · "deploy steps" →runbook · "migrate to k8s Q4" →issue · "propose gRPC (discussing)"
→RFC · "use TypeScript" KEEP (construction technique, cross-cutting) · "MIT license" borderline-KEEP (lightweight).

## Sources
Nygard 2011 https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions · MADR
https://adr.github.io/madr/ · adr.github.io https://adr.github.io/ · AWS ADR process
https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html ·
MS Azure WAF ADR https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record ·
Google design docs https://www.industrialempathy.com/posts/design-docs-at-google/ · Rust RFC
https://github.com/rust-lang/rfcs/blob/master/0000-template.md · ADR-vs-RFC https://candost.blog/adrs-rfcs-differences-when-which/ ·
Zimmermann ADR-significance https://ozimmer.ch/practices/2021/04/23/AnyDecisionRecords.html + MADR primer
https://ozimmer.ch/practices/2022/11/22/MADRTemplatePrimer.html · MS decision-log
https://microsoft.github.io/code-with-engineering-playbook/design/design-reviews/decision-log/ · ISO/IEC/IEEE
42010 https://www.iso.org/standard/74393.html · ThoughtWorks lightweight-ADR https://www.thoughtworks.com/radar/techniques/lightweight-architecture-decision-records
