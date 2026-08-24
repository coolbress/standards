# Synthesis — gingoa's greenfield-vs-brownfield ADOPTION MODEL (cross-lifecycle)

Analyzed output of the 5-track brownfield-adoption research (tracks 1–5 in this dir). Answers: *how does the pipeline
run for a NEW project, and how should gingoa attach to an EXISTING project across ①plan → ②foundation → ③implement →
④release?* This is a **cross-cutting** concern (spans ①②④); it does not fit one locked aspect — final fold location
(aspect sub-doc(s) vs a `lifecycle.md` overlay section) is a human-gated decision (see "Fold plan" below).

> Evidence: track1-scaffolders · track2-idp-onboarding · track3-spec-driven-brownfield ·
> track4-ratchet-incremental-adoption · track5-census-existing-repo-mode (all in this dir).

## 1. The core model — two modes, one spine

**Two modes, a distinct verb each (census finding 5 — a separate brownfield verb is the emerging convention, NOT
`scaffold --overwrite`): `new` (greenfield, exists today) · `adopt` (brownfield, unbuilt).**

The cross-cutting spine of `adopt`, common to every stage (the industry consensus across IDP + scaffolders + spec tools):
1. **Detect** — read the existing tree/docs; never assume.
2. **Coexist, don't collide** — install gingoa's own managed artifacts into a reserved namespace / as additive files;
   surface conflicts on shared files, never silently clobber (census: refuse/prompt dominate 57%; silent-overwrite 6%).
3. **Propose, don't push** — additive/missing items are written to a **branch + PR** for human approval (Backstage
   register-existing PR pattern), not committed to the user's `main`.
4. **Audit-only by default, non-blocking** — the production-floor check runs read-only and REPORTS a gap inventory;
   an existing project may be RED and still adoptable (IDP consensus: scorecards are visibility, not gates).
5. **Ownership baseline** — write one committed lineage file so every future lifecycle `update` has a merge base
   (census: `.copier-answers.yml` is the reference; ADR-0003/0017 already reserve copier `update`).

## 2. Per-stage behavior

### ①plan (Elicit) — the requirements doc may be PRESENT / ABSENT / DIFFERENT-FORMAT
Grounded in track-3 (BMAD/spec-kit/OpenSpec) + census docs-mode split:
- **present, same format** (a valid prd.yml/PRD.md) → **IMPORT**: validate EARS, gap-fill via targeted interview.
- **present, different format** (Confluence/JIRA/README) → **CONVERT**: agent ingests + maps to prd.yml schema, flags
  fields with no source.
- **absent / code-only** → **REVERSE-ENGINEER**: *flatten the codebase into a structured digest first* (the universal
  first step — BMAD `document-project`, Aider repo-map, Repomix), then derive prd.yml from the digest.
- **Invariant (track-3 de-facto):** *never treat an AI-generated spec as authoritative* — mark INFERRED vs CONFIRMED
  fields; require user confirmation before the doc can lock (feeds gingoa's existing lock/seal gate).

### ②foundation (Scaffold) — the biggest surface; a floor may be PARTIALLY present
Grounded in track-1 (copier/cruft 3-way) + track-2 (IDP audit) + track-4 (ratchet):
- **3-way disposition per artifact** (track-1 universal): **missing→add · equal→skip · different→CONFLICT**. Only
  "different" is contested.
- **Additive-first conflict UX** (gingoa's refinement + census safe-default): purely-new files are added silently;
  conflicts surface ONLY on files that are both present AND diverged — never clobber (write markers / a PR diff, let
  the human decide). copier's synthetic **empty-base 3-way merge** (issue #2486) + cruft `link` are the entry mechanism.
- **Ownership baseline**: `adopt` writes `.copier-answers.yml` with a synthetic `_commit` (the template version the
  project claims), then all future lifecycle rides `copier update` (real 3-way base). Census: this is the gold standard;
  ADR-0003/0017 already buy it.
- **Relaxed green-gate (the key ②-brownfield invariant)** — grounded in SonarQube "Clean as You Code" (reference
  standard) + OpsLevel Rubric/Maturity-Report: run `reconcileFloor` in **read-only AUDIT mode** over the existing tree →
  a maturity report (per-item PASS/FAIL/CONFLICT + tier). The audit **never blocks** (exit 0 even if fully RED). Only
  gingoa-**ADDED** items are proven green (the "new code gate"). Store the audit inventory machine-readably so later runs
  distinguish known-pre-existing from newly-introduced; **ratchet** so the pre-existing violation count can only fall.
- **`gingoa check`/`diff` (CI drift)** — cruft `check` pattern: fail CI when the adopted project drifts from its
  scaffold version.

### ③implement (Orchestrate) — mostly mode-agnostic (owner's own read, confirmed)
Once adopted, the project goes FORWARD on gingoa's harness, so `route`/ceremony is unchanged. Only reconciliation needed:
**absorb, don't override** any pre-existing conventions (branch protection, PR-title rules) the audit found — surface
them as already-satisfied floor items rather than re-imposing gingoa's.

### ④release (Release) — an existing release/deploy setup may DIFFER
Least-researched here (candidate for a follow-up dig). Principle from the spine: **detect the existing release mechanism
(tags, CI release workflow, changelog) and RESPECT vs REPLACE** — additive/incremental, not a forced swap. `planRelease`
already decides-only, so brownfield mainly affects the (future) execution slice + evidence gathering.

## 3. Design decisions (grounded; rejected alternatives named)
- **D-Ad-1 — a distinct `adopt` verb, not `scaffold --overwrite`.** Census finding 5: `new`-vs-in-place is a consistent
  ecosystem split (cargo new/init, copier copy/update, nx init/import, backstage scaffold/register). Rejected overloading
  scaffold (its greenfield atomic-clobber semantics are wrong for a live tree — [[brownfield-adoption-gap]]).
- **D-Ad-2 — audit-only, non-blocking floor in brownfield.** IDP unanimity (Port/Cortex/OpsLevel/Backstage: "not
  enforcement"). Rejected imposing the full green floor (fails hundreds of pre-existing violations; makes adoption
  impossible) and Kratix-style provisioning-enforcement (the lone "impose" outlier).
- **D-Ad-3 — gate NEW/added items green; grandfather existing (Clean-as-You-Code).** Reference standard = SonarQube
  CaYC. Rejected whole-repo gating (brownfield can't pass) and no-gate (unlimited decay) — the ratchet is the middle.
- **D-Ad-4 — ownership baseline = a committed answers file; lifecycle via copier update.** Census gold standard
  (copier/cruft). Rejected no-baseline (no future merge base → every update is a clobber).
- **D-Ad-5 — propose via PR, never push to main; additive-first on conflicts.** Backstage register pattern + census
  safe-default (never clobber). Rejected direct-write and silent-overwrite.
- **D-Ad-6 — ①docs: flatten-first, mark inferred, require confirmation.** track-3 de-facto (BMAD). Rejected trusting an
  AI-generated PRD as authoritative (the named industry failure mode).

## 4. Open questions (for the owner)
- **Verb surface:** one `adopt` verb with per-stage sub-behaviors, or per-stage adopt modes (`elicit --adopt`, `scaffold
  --adopt`, …)? (Census shows both; lean single `adopt` orchestrating the stages.)
- **Conflict resolution UX for a non-engineer:** PR-diff review vs inline markers vs a guided "keep mine / take gingoa's"
  prompt. (Census: prompt-per-file is common but assumes an engineer.)
- **④release depth:** is brownfield-release in scope now, or deferred until the release EXECUTION slice exists?
- **Fold location** (below).

## 5. What gingoa already has (reuse, don't rebuild)
- `render()` fail-closed atomic apply + `reconcileFloor` (pure, could add a read-only AUDIT mode) + `foundationReadiness`
  (the ②-input gate) + `planning.prd` carry (#60) + copier shell-out (ADR-0003) with `update` reserved (ADR-0017).
- The gap is: the `adopt` verb, audit-mode reconcile, the ①docs reverse-engineer/import path, the ownership-baseline
  writer, and `gingoa check`.

## Fold plan (human-gated — anti-drift; the 28-aspect set is locked)
This cross-cutting model does not fit one single-stage aspect. Proposed fold (owner to confirm):
- ②-mechanics (3-way, ownership baseline, audit-mode/relaxed-green-gate, ratchet) → aspect-03 (dev-environment) or
  aspect-04 (build-ci) sub-doc.
- ①docs brownfield (reverse-engineer/import/convert) → aspect-01 (requirements-planning) sub-doc.
- The cross-stage `adopt` spine → a `lifecycle.md` overlay section (it modifies every stage's behavior).
Until folded, THIS doc + tracks 1–5 are the reference. A future `adopt` feature is its own Tier-3 (US-level) build.
