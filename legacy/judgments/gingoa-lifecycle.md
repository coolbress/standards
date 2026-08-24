> ⚠️ **아카이브 (2026-08-02 감사)** — gingoa 시절 원문 보존본. 내부 상대 링크는 원 위치 기준이라 깨져 있을 수 있다. 활성 문서는 `../../corpus/`를 보라.

# Lifecycle × Aspect Activation Map

> The **overlay**: aspects hold the standard (WHAT); this map is gingoa's **activation layer** (WHEN). gingoa
> drives the user ①→②→③→④ and at each stage gate activates the aspects below. **Cross-cutting** aspects fire
> at EVERY stage (staging them as a single gate is how a discipline becomes a checkbox — esp. security).
> Generated from `TAXONOMY.md`; primary-stage tags live in each aspect's `lifecycle_stages`.

## ① 기획 / Planning
**Primary:** 01 Requirements & Planning · 02 Architecture & Design · 25 Licensing & FOSS Compliance

## ② 포석 / Foundation
**Primary:** 02 Architecture & Design · 03 Dev Environment & Local Setup · 04 Build & CI Engineering · 10 Software Supply Chain Security · 23 Developer Experience & Onboarding

## ③ 구현 / Implementation
**Primary:** 07 Software Construction & Code Review · 08 Software Testing · 12 Performance & Scalability · 13 API & Interface Design · 14 Data Management & Migrations · 15 Accessibility & UX / Interaction Capability · 16 Privacy & Data Protection · 19 Observability & Telemetry · 28 Implementation Process & Agentic Workflow

## ④ 릴리스·운영 / Release & Ops
**Primary:** 10 Software Supply Chain Security · 12 Performance & Scalability · 17 Release Engineering · 18 Packaging & Distribution · 19 Observability & Telemetry · 20 Operations, Incident & Reliability · 21 Software Economics, Cost & Sustainability

## ✚ Cross-cutting (fire at every stage)
02 Architecture & Design · 04 Build & CI Engineering · 05 SCM & Development Workflow · 06 Configuration & Secrets Management · 08 Software Testing · 09 Application Security · 10 Software Supply Chain Security · 11 Maintainability, Tech Debt & Refactoring · 22 Documentation & Knowledge Management · 23 Developer Experience & Onboarding · 24 Governance, Collaboration & Compliance · 25 Licensing & FOSS Compliance · 26 MLOps / ML Lifecycle · 27 AI-Harness Archetype

---

## ⇄ Mode overlay — `new` (greenfield) vs `adopt` (brownfield)

> A **second overlay axis**, orthogonal to the stage gates above: *is gingoa starting a project, or attaching
> to an existing one?* The stage → aspect activation is the same in both modes; what changes is **how each stage
> behaves** when the inputs already partially exist. `new` (greenfield) is what gingoa does today. `adopt`
> (brownfield) is designed-but-unbuilt — a distinct verb, not `scaffold --overwrite` (census: a separate
> brownfield verb is the emerging convention — `cargo new`/`init`, copier `copy`/`update`, `nx init`/`import`,
> backstage scaffold/register). Grounded across the aspect sub-docs + `census-data/brownfield-adoption/`.

**The `adopt` spine (common to every stage — the industry consensus across scaffolders + IDPs + spec tools):**
1. **Detect** — read the existing tree/docs; never assume.
2. **Coexist, don't collide** — additive files / a reserved namespace; surface conflicts on shared files, never
   silently clobber (census: refuse/prompt dominate ~57%; silent-overwrite ~6%).
3. **Propose, don't push** — missing/additive items go to a **branch + PR** for human approval, never a push to
   the user's `main` (Backstage register-existing pattern).
4. **Audit-only, non-blocking** — the production-floor check runs read-only and REPORTS a gap inventory; an
   existing project may be RED and still adoptable (IDP consensus: scorecards are visibility, not gates).
5. **Ownership baseline** — write one committed lineage file (`.copier-answers.yml`, synthetic empty-base) so
   every future lifecycle `update` has a merge base (ADR-0003/0017 reserve the copier-update path).

**Per-stage `adopt` behaviour:**
- **① 기획 (aspect-01)** — the planning doc may be present-same → IMPORT · present-different → CONVERT · absent →
  REVERSE-ENGINEER (flatten-first; INFERRED-until-confirmed). → [`aspects/01-requirements-planning/brownfield-planning-adoption.md`](aspects/01-requirements-planning/brownfield-planning-adoption.md)
- **② 포석 (aspect-04, + 03)** — the biggest surface: audit-mode floor · 3-way disposition · additive-first +
  propose-PR · ownership baseline · relaxed green-gate (Clean-as-You-Code + ratchet). The most self-contained
  `adopt` slice (reuses the floor predicate; the natural first build). → [`aspects/04-build-ci-engineering/brownfield-adoption-floor.md`](aspects/04-build-ci-engineering/brownfield-adoption-floor.md)
- **③ 구현 (aspect-28)** — largely **mode-agnostic**: once adopted the project goes forward on gingoa's harness.
  Only reconciliation: *absorb, don't override* any pre-existing conventions the audit found (branch protection,
  PR-title rules) — surface them as already-satisfied floor items.
- **④ 릴리스·운영 (aspect-17)** — an existing release/deploy setup may DIFFER; principle = **detect then RESPECT
  vs REPLACE** (additive/incremental, not a forced swap). Least-researched — a candidate follow-up dig; entangled
  with the (future) release-EXECUTION slice.

---
_Stage overlay derived from `TAXONOMY.md`; hand-maintained. Mode overlay added 2026-07-02 (brownfield-adoption research fold)._
