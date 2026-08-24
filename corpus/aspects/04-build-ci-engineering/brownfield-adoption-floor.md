---
id: aspect-04-build-ci-engineering--brownfield-adoption-floor
title: "Brownfield ②-foundation adoption — audit-mode floor, 3-way disposition, ownership baseline, relaxed green-gate"
parent: aspect-04-build-ci-engineering
kind: research-log
evidence_track: census+lit
status: review-needed
last_updated: "2026-07-02"
method: "Three-thread survey (2026-07-02): (1) scaffolder/generator brownfield modes — copier, cruft, Yeoman, Nx, Plop, Hygen, degit, create-next-app; (2) platform-engineering / IDP onboarding & audit — Backstage, Cortex, OpsLevel, Port, Humanitec/Score, Kratix; (3) incremental-adoption / legacy ratchet — SonarQube CaYC, ESLint bulk-suppressions, betterer, Semgrep baseline, RuboCop todo, Fowler Strangler/ratchet; + a 51-tool census. Raw: census-data/brownfield-adoption/track1,2,4,5. Grounds the ②-foundation behaviour of a future `adopt` mode; cross-stage spine in lifecycle.md §New vs Adopt."
---

# Brownfield ②-foundation adoption — how the production-floor behaves against an EXISTING tree

Why this exists: aspect-04's floor (and the [`foundation-floor-artifact-checklist`](foundation-floor-artifact-checklist.md))
is a **greenfield** contract — gingoa renders it into an empty tree it owns, atomically, green-or-refuse. When
gingoa is pointed at an **existing** project the floor is *partially present*, the project may be RED, and gingoa
owns nothing yet. This logs how the field adopts an existing project into a managed floor without clobbering it,
and derives gingoa's ②-foundation adoption behaviour. This is the ② slice of the cross-stage `adopt` model (spine
in [`lifecycle.md`](../../lifecycle.md) §New vs Adopt; the ①-plan slice is
[`../01-requirements-planning/brownfield-planning-adoption.md`](../01-requirements-planning/brownfield-planning-adoption.md)).

## The five ② mechanics (each grounded in a reference standard)

### 1. Audit-mode floor — read-only, non-blocking
Run the floor check in a **read-only AUDIT mode** over the existing tree → a maturity report (per-item
PASS / FAIL / CONFLICT + tier). The audit **never blocks** (exit 0 even if fully RED): an existing project can
be non-compliant and still adoptable. This is IDP unanimity — Port "audit and visibility tools, not enforcement";
OpsLevel Maturity Report "does not block anything"; Cortex scorecards "aspirational"; Backstage Tech Insights
nudges, never gates. `[lit]` The reference model is the **OpsLevel Rubric + Maturity Report** (ordered
Bronze/Silver/Gold tiers, per-item pass/fail with "how to fix", never a deploy gate); Port's "Basic" entry tier
means a project with *zero* floor items is still adoptable. gingoa mechanism: point the existing floor predicate
at a non-gingoa tree in read-only mode.

### 2. 3-way disposition per artifact — missing / equal / different
The universal scaffolder algorithm (copier/cruft): **missing → add · equal → skip · different → CONFLICT**. Only
"different" is contested. copier resolves it with a **3-way merge** (base = re-render at the recorded template
commit · ours = project on disk · theirs = re-render at new template), conflicts as inline git markers or `.rej`.
Census: of 48 determinate tools only **3 (6%)** do a true 3-way merge (copier, cruft, mrm) — most brownfield
support is a blunt `--force` clobber or an add-one-thing generator. `[census]` gingoa gets the 3-way base for
free via the copier shell-out (ADR-0003) once the ownership baseline exists (mechanic 4).

### 3. Additive-first conflict posture — never clobber by default
Purely-new files are added silently; a conflict is surfaced **only** on a file that is both present AND diverged.
This is gingoa's refinement of the census safe-default: collision handling is dominated by refuse-unless-forced
(29%) and prompt-per-file (28%); silent-overwrite is rare (6%). `[census]` No shipped tool formalizes
"prefer adding new over surfacing conflicts on existing," so additive-first is a genuine contribution. Writes go
to a **branch + PR**, never a push to the user's `main` (Backstage register-existing PR pattern) — detect →
propose → human approves. `[lit]`

### 4. Ownership baseline — a committed lineage file
The first `adopt` writes one committed answers file so every future lifecycle `update` has a merge base. The
census gold standard is a committed answers file at repo root: `.copier-answers.yml` (`_src_path` + `_commit` =
the merge-base key + answers), cruft `.cruft.json` (`commit` + `skip` glob = user-owned zone). Ownership baselines
are uncommon (~12% of tools) but the convention when present is unambiguous. `[census]` For first-time entry the
ecosystem consensus is a **synthetic empty-base 3-way** (copier #2486 `adopt` proposal; cruft `link`): existing =
ours, template = theirs, empty tree = synthetic base. ADR-0003/0017 already reserve this path — the census
**validates** that choice; do not reopen it. `[lit][census]`

### 5. Relaxed green-gate — gate NEW/added items, grandfather existing (+ ratchet)
A brownfield build may already be RED, so greenfield's "green-or-refuse" cannot apply. The reference methodology
is **SonarQube "Clean as You Code"**: gate on the *new-code* slice only; pre-existing violations show in "overall"
but never gate. `[lit]` Only gingoa-**ADDED** floor items are proven strictly green (the "new-code gate"); existing
gaps are audited and grandfathered. Store the audit inventory machine-readably (the `.betterer.results` /
`eslint-suppressions.json` / Semgrep-baseline pattern) so later runs distinguish known-pre-existing from
newly-introduced, and apply the **ratchet** (Burwell): the pre-existing violation count may only fall, never rise
(12 grandfathered → never 13). This is Strategy-A (diff/period gate) applied at the *floor-item* level. `[lit]`

### (+) `gingoa check` — CI drift
The cruft `check` pattern: a CI step that fails when the adopted project drifts from its recorded scaffold
version. First-class in the reference tools; gingoa should expose `check`/`diff`. `[lit]`

## Kratix caveat
Kratix is the lone "impose via provisioning" outlier (governance-through-provisioning, may modify the cluster) —
**not** a suitable analogy for a brownfield floor audit. The consensus everywhere else is audit = a reporting
surface, enforcement (if any) is a separate human-decided step.

## Implications for gingoa (②-foundation adoption)

1. `adopt` ② reuses the **existing floor predicate in a read-only AUDIT mode** — the audit engine already exists;
   the new work is the audit mode, the disposition/additive-write, the ownership-baseline writer, and `check`.
2. **Never clobber, never push:** additive-first writes to a branch + PR; conflicts surface as a diff the human
   resolves.
3. **Relaxed green-gate:** the audit exits 0 on a RED tree; only added items are gated green; the pre-existing
   count ratchets down.
4. The ownership baseline (`.copier-answers.yml` + synthetic base) is written on first adopt; thereafter lifecycle
   rides `copier update` — the exact path ADR-0003/0017 reserved. This ② slice is the most self-contained of the
   `adopt` model (does not touch the ①-plan elicit engine) — the natural first slice to build.

## Sources

- copier — Updating / Configuring · `adopt` proposal #2486 — <https://copier.readthedocs.io/> · <https://github.com/copier-org/copier/issues/2486>
- cruft — `link` / `update` / `check` · `.cruft.json` — <https://cruft.github.io/cruft/>
- Backstage — register an existing component (PR pattern) · Tech Insights — <https://backstage.io/docs/features/software-catalog/> · OpsLevel Maturity Report / Rubric — <https://www.opslevel.com/> · Port scorecards "audit not enforcement" — <https://docs.port.io/> · Cortex scorecards
- SonarQube "Clean as You Code" (new-code) — <https://docs.sonarsource.com/sonarqube-server/latest/user-guide/clean-as-you-code/> · Dusty Burwell "ratchets" — <https://www.dustyburwell.com/2019/05/29/ratchets.html> · Fowler StranglerFig — <https://martinfowler.com/bliki/StranglerFigApplication.html>
- betterer — <https://phenomnomnominal.github.io/betterer/> · ESLint bulk suppressions (v9.24) · Semgrep `--baseline-commit`
- Raw threads: `census-data/brownfield-adoption/track1-scaffolders.md`, `…/track2-idp-onboarding.md`, `…/track4-ratchet-incremental-adoption.md`, `…/track5-census-existing-repo-mode.md`
