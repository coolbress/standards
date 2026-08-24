# Track 4 (raw) — Incremental adoption / legacy ratchet & baseline mechanisms

Research thread for gingoa's brownfield **relaxed green-gate** (②): existing code may be RED overall; only
gingoa-ADDED items must be proven green; existing gaps AUDITED, not clobbered.

## Architectural patterns (macro)
- **Strangler Fig** (Fowler 2004): build new alongside legacy, migrate incrementally until legacy dies. Existing
  left running/unmodified; the gate is whether each NEW component passes before traffic switches. Existing = audit,
  new = block. martinfowler.com/bliki/StranglerFigApplication.html
- **Branch by Abstraction** (Fowler): abstraction layer over the supplier; old+new coexist behind it via feature
  flags; swap gradually. The seam that lets old/new coexist. martinfowler.com/bliki/BranchByAbstraction.html
- **Ratchet pattern** (Dusty Burwell 2019): a floor that only rises, never falls. New violations blocked immediately;
  existing grandfathered but must not INCREASE (regression = fail). Distinct from hard-gate (all-now, disruptive) and
  no-gate (unlimited decay). dustyburwell.com/2019/05/29/ratchets

## Per-tool mechanism table
| Tool | Mechanism | Existing | New | Audit vs block | Baseline storage |
|---|---|---|---|---|---|
| **SonarQube "Clean as You Code"** | new-code period (date/version/commit/branch); quality gate on NEW-code metrics only | shown in "overall", never gates | block if new-code gate fires | existing=audit, new=block | server-side period (no checked-in file) |
| **ESLint Bulk Suppressions** (v9.24, Apr 2025) | `--suppress-all` → `eslint-suppressions.json`; suppressed rules still RUN but existing not reported | suppressed (audit) | block (exit 1) | existing=suppressed, new=block | `eslint-suppressions.json` committed |
| **betterer** | snapshot count/locations → `.betterer.results`; worse→fail, better→auto-update, same→pass | tracked, allowed | fail if count↑ | ratchet | `.betterer.results` committed |
| **tsc-baseline** | `save` hashes current TS errors; `check` surfaces only new | hashed/filtered | block (new only) | existing=filtered, new=block | hash baseline file committed |
| **TS strict incremental** | `typescript-strict-plugin` / per-module tsconfig / `// @ts-strict-ignore` | legacy excluded | new files checked strict | existing=excluded, new=block | per-file comment or tsconfig allowlist |
| **RuboCop `.rubocop_todo.yml`** | `--auto-gen-config` per-file excludes / cop disables; `--regenerate-todo` | excluded | block on non-excluded | existing=excluded, new=block | `.rubocop_todo.yml` committed |
| **mypy incremental** | per-module `ignore_errors=True`; `--follow-imports`; strict per-module | suppressed via config | new modules fully checked | existing=suppressed, new=block | `mypy.ini`/`pyproject.toml` sections |
| **Semgrep `--baseline-commit`** | scans at baseline SHA + HEAD; reports only NEW since baseline | excluded | block (exit 1) new only | existing=audit, new=block | git commit SHA (env `SEMGREP_BASELINE_REF`) |
| **Pylint ratchet** | count/score per category; must not increase | counted floor | fail if ↑ | ratchet | count file / CI var; `pylint-ignore` pkg |
| **git-blame-ignore-revs** | `.git-blame-ignore-revs` SHAs skipped by blame | formatting commits invisible | n/a | audit-only (no gate) | `.git-blame-ignore-revs` committed |
| **CodeClimate/Qlty diff coverage** | coverage on CHANGED lines only; min % on new/modified | overall tracked separately | block PR if diff-cov low | existing=audit, new=block | server-side |
| **OpenRewrite / jscodeshift (codemods)** | AST transforms applied to ALL existing at once → clean state, then full gate | eliminated (not suppressed) | full gate after | transition step | output IS new state |

## Taxonomy (three strategies + supports)
- **A. Diff/Period gate** (SonarQube, Semgrep baseline, CodeClimate): gate scoped to a time-window/commit-range;
  pre-existing outside window never surfaced in the blocking gate (read-only "overall" view). Baseline = date/version/SHA
  (no checked-in file). **Highest abstraction** — no enumeration, just a temporal boundary.
- **B. Snapshot/baseline file** (ESLint suppressions, betterer, tsc-baseline, RuboCop todo): all current violations
  enumerated in a COMMITTED file; anything not in it is new → blocks. Updated deliberately. Precise per-violation.
- **C. Per-module/file config exclusion** (mypy, TS `@ts-strict-ignore`): existing files excluded at config level; new
  files without the exclusion are strict. Coarsest, simplest.
- **Support: codemods** (one-time mechanical cleanup so A/B/C can tighten). **Support: git-blame-ignore-revs** (keep
  blame clean after a formatting codemod; no gate role).

## Reference standard
**SonarQube "Clean as You Code" (CaYC)** = the canonical, formally-named "gate new, audit pre-existing" methodology
(default quality gate of the most-deployed quality platform; stated as an org methodology, not just a flag). The
new-code "period" abstraction is the most general baseline; the commit-SHA form (Semgrep/Sonar "specific analysis") is
most reproducible in CI. For a CHECKED-IN baseline without a running server, **betterer** (purpose-built, any
lint/test/typecheck, auto-ratchet) is the idiomatic JS/TS analog; **ESLint bulk suppressions** is now the first-party
ESLint answer.

## Transferable to gingoa's brownfield relaxed green-gate — Strategy A at the ITEM level
| gingoa concept | analogue |
|---|---|
| gingoa-added floor items | "new code" (the gate condition set) |
| existing project state | "overall code" — visible in audit, never gates |
| relaxed green-gate | CaYC gate: fires only on the new/added slice |
| brownfield baseline | Sonar "specific analysis" / Semgrep baseline commit — snapshot of pre-adoption state |
| audit of existing gaps | "overall code" view / full-scan report (non-blocking) |
| only added items proven green | each floor item's check runs against gingoa-added content only |

**Implementation shape:** on `adopt` (or scaffold brownfield mode): (1) AUDIT pass over all pre-existing floor checks →
report as inventory (audit-only, exit 0) = the "specific analysis" baseline; (2) for each gingoa-ADDED item → run STRICT,
fail if not green = the "new code gate"; (3) store the audit inventory machine-readably (like `.betterer.results` /
`eslint-suppressions.json`) so later runs distinguish known-pre-existing from newly-introduced; (4) as the adopter fixes
gaps, the inventory shrinks (`--update`/`--prune`). **Ratchet control:** pre-existing violation count must never INCREASE
(12 grandfathered → never 13); if it falls, auto-update the baseline.

## Sources
Fowler StranglerFig / BranchByAbstraction / patterns-legacy-displacement · Dusty Burwell ratchets · SonarQube CaYC (new-code) ·
ESLint suppressions + v9.24 release · betterer results-file + repo · tsc-baseline · RuboCop auto-gen-config · mypy existing_code ·
Semgrep diff-aware findings-ci · git-blame --ignore-revs-file · CodeClimate/Qlty · OpenRewrite / jscodeshift · TS TSConfig · Pylint FAQ.
