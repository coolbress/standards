---
id: corpus-taxonomy
title: "Engineering Evidence Taxonomy"
kind: navigation
status: review-needed
last_updated: "2026-08-02"
evidence_track: lit
freshness: versioned
review_due: "2026-10-02"
sources: [SWEBOK-4.0A, ISO-12207-2026]
---

# Engineering Evidence Taxonomy

## Status and finding

The inherited 28-aspect roster is retained for stable paths, but it is **provisional**, not “locked.” It has
good breadth, yet combines several different axes: software-engineering knowledge areas, quality attributes,
life-cycle activities, organizational practices, and one product archetype (`27 AI harness`). A mixed taxonomy
can still be an effective retrieval index; it must not be presented as a single industry-standard decomposition.

The previous rationale is preserved at `../legacy/judgments/gingoa/taxonomy.md`. Its ISO/IEC/IEEE 12207:2017
anchor is stale: the ISO catalog marks that edition withdrawn and ISO/IEC/IEEE 12207:2026 as the current edition.
SWEBOK V4.0a is the current IEEE Computer Society update and contains 18 Knowledge Areas.

## Stable roster

| Group | Aspect IDs |
|---|---|
| Plan and design | 01 Requirements & Planning; 02 Architecture & Design |
| Foundation and build | 03 Development Environment; 04 Build & CI; 05 SCM Workflow; 06 Config & Secrets |
| Construct and verify | 07 Construction & Review; 08 Testing; 09 Application Security; 10 Supply Chain Security; 28 Implementation Process |
| Quality attributes | 11 Maintainability; 12 Performance; 13 Interfaces; 14 Data & Migrations; 15 Accessibility & UX; 16 Privacy |
| Release and operate | 17 Release; 18 Packaging; 19 Observability; 20 Operations & Reliability; 21 Economics & Sustainability |
| Practice and governance | 22 Documentation; 23 Developer Experience; 24 Governance; 25 Licensing |
| Specialized | 26 MLOps; 27 AI Harness |

## Required facets

Do not create more top-level aspects merely to express another axis. Add metadata facets instead:

- `lifecycle_stages`: when the topic matters.
- `applicability`: universal, cross-cutting, or activation conditions.
- `archetypes`: CLI, library, web, backend, mobile, data/ML, monorepo, AI harness, and later gates.
- `evidence_track`: literature, local census, or both.
- `freshness`: durable, versioned, or volatile.
- `status`: draft, review-needed, verified, superseded, or retracted.
- `target_user_capability`: requirement expression, evidence comprehension, risk decision, and operational
  responsibility. This is a cross-cutting applicability axis—not a 29th engineering topic—and conditions
  aspects 01, 23, 27, solo operation, and last-mile support.

## Coverage audit result

The documented [`framework-crosswalk-2026.md`](methods/framework-crosswalk-2026.md) compares all 28 aspects
against current SWEBOK V4.0a, ISO/IEC/IEEE 12207:2026 catalog scope, and ISO/IEC 25010:2023 catalog scope. It
found broad lifecycle and quality coverage, retained six overlap boundaries, and identified target-user
capability, specialist compliance, data/service quality, AI-agent authority, solo operation, and last-mile
release as separate axes or extensions.

The taxonomy remains `review-needed`, not because the structural comparison is missing, but because detailed
ISO clause mapping is `INCONCLUSIVE` without licensed full text and a mixed retrieval taxonomy is not itself an
industry-standard decomposition. Framework coverage also does not prove a particular practice effective.

## Sources

- `SWEBOK-4.0A` — https://www.computer.org/education/bodies-of-knowledge/software-engineering
- `ISO-12207-2026` — https://www.iso.org/standard/90219.html
