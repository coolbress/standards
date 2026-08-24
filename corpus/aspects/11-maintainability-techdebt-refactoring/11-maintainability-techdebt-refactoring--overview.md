---
id: aspect-11-maintainability-techdebt-refactoring
title: "Maintainability, Tech Debt & Refactoring"
group: "Q — Quality Attributes"
kind: cross-cutting
gated_archetypes: []
cross_cutting: true
lifecycle_stages: ["all"]
anchors: ["SWEBOK-KA7", "ISO-25010-Maintainability"]
evidence_track: lit
status: review-needed
last_updated: "2026-06-25"
sources:
  - "https://www.computer.org/education/bodies-of-knowledge/software-engineering"
  - "https://www.iso.org/standard/78176.html"
  - "https://martinfowler.com/bliki/TechnicalDebt.html"
  - "https://martinfowler.com/books/refactoring.html"
  - "https://martinfowler.com/bliki/StranglerFigApplication.html"
  - "https://www.archunit.org/"
  - "https://deptrac.github.io/deptrac/"
  - "https://docs.sonarsource.com/sonarqube-server/latest/user-guide/metric-definitions/"
  - "https://understandlegacycode.com/blog/characterization-tests-or-approval-tests/"
claim: "Senior engineers treat maintainability as a first-class quality attribute: they keep complexity/coupling under explicit budgets enforced in CI, refactor continuously (Boy-Scout) and structurally (strangler fig) in commits kept separate from behavior changes, log known shortcuts as a tracked debt register rather than silent rot, and pin legacy under characterization tests before touching it."
maps_from: ["docs/prd.yml (C3 maintainability NFR; ADR-0008 floor)"]
census_todo: "Deferred — needs a targeted workflow-content/topology survey; the existing census records hold derived flags only (not tree contents), so this metric (e.g. named debt-register presence, ArchUnit/Deptrac architecture-test adoption, complexity-budget gates) is not offline-derivable. Low priority."
---

> **Standard (claim):** Maintainability is a first-class quality attribute, not a virtue. Seniors hold complexity/coupling to explicit CI-enforced budgets, refactor continuously (Boy-Scout) and structurally (strangler fig) in commits separated from behavior change, log shortcuts in a tracked debt register instead of letting them rot, and pin legacy under characterization tests before touching it.
> **Evidence:** [lit] dominant (named standards/practices) + light [census] (the publish-axis lives mostly under aspects 04/07) · **Confidence:** high · **Kind:** cross-cutting · **Stage:** all

**Seed sub-aspects:** `debt register (ADR-tagged)` · `complexity / coupling metrics` · `refactoring discipline (Boy-Scout / strangler)` · `modularity enforcement (ArchUnit/Deptrac)` · `legacy / characterization tests` · `deprecation & disposal`

## What professional engineers do

- **Treat maintainability as a measured quality attribute.** ISO/IEC 25010:2023 makes *maintainability* a top-level attribute with five sub-characteristics — **modularity, reusability, analysability, modifiability, testability**. SWEBOK KA *Software Maintenance* frames the work as adaptive/perfective/corrective/preventive and warns that maintenance is the majority of total lifecycle cost. Seniors design *for* modifiability up front (the cost-of-change lever) rather than apologising for it later. [lit]
- **Keep a tracked debt register — make debt visible, not silent.** Fowler's metaphor: tech debt = "deficiencies in internal quality that make it harder than it would ideally be to modify and extend," where you pay *interest* on every future change. The senior move is the **Technical Debt Quadrant** (deliberate/inadvertent × prudent/reckless): *prudent-deliberate* debt ("ship now, fix the seam in Q3") is logged with a rationale; *reckless* debt is the failure mode. Mechanism: a `// TODO(DEBT-123)`/`@deprecated` marker linked to a tracked issue/ADR, surfaced in review — debt that isn't written down silently compounds. [lit]
- **Budget complexity and coupling, then enforce it in CI.** Seniors set explicit ceilings — cyclomatic/cognitive complexity per function, file/function length, fan-in/fan-out coupling, duplication — and fail the build on regression rather than relying on willpower. **SonarQube** operationalises this with the *remediation-effort* model: a "technical-debt ratio" (estimated remediation cost ÷ cost-to-rewrite) graded A–E, plus a "new-code" quality gate so debt can only *decrease* on each PR. Linters (biome/eslint/ruff) carry the cheap per-commit ceilings. [lit]
- **Refactor continuously and structurally — and keep the commit separate.** Two disciplines: (1) **Boy-Scout rule** — leave each touched file a little cleaner; small in-flight refactors via Fowler's catalog (Extract Function, Move, Inline, Rename) under a green test suite. (2) **Preparatory refactoring** — "make the change easy, then make the easy change," with the refactor in its *own* commit, no behavior change, all tests still green. The non-negotiable rule: **never mix a refactor and a behavior change in the same commit** — it makes review and bisect impossible. [lit]
- **Migrate legacy with the strangler fig, not a big-bang rewrite.** For large structural change, route traffic through a façade and grow the replacement *incrementally* alongside the old system until the legacy is fully "strangled" and removed (Fowler) — each step independently shippable and reversible, avoiding the classic doomed rewrite. [lit]
- **Pin legacy under characterization tests before changing it.** Code without tests is "legacy" (Feathers). Before refactoring untested code, write **characterization tests** that lock in *current* behavior (golden/approval tests, even of bugs) so the refactor is provably behavior-preserving; find a *seam* to inject the test, then refactor safely. [lit]
- **Enforce modularity with executable architecture tests.** Intended dependency direction and layer boundaries are guarded by fitness functions — **ArchUnit** (JVM, bytecode-analysed rules run as unit tests), **Deptrac** (PHP layer/dependency rules), `eslint-plugin-boundaries`/`import-linter` (JS/Py), package-cycle checks — so erosion fails the build instead of accreting silently between commits. (Cross-link: aspect 02 fitness functions.) [lit]
- **Deprecate and dispose on a schedule, don't accrete.** Mark with `@deprecated` + a replacement pointer + a removal version; honour a deprecation window under semver; then actually *delete* dead code/feature flags/old branches. SWEBOK names *retirement/disposal* as a real lifecycle stage — unused code is negative-value maintenance surface. [lit]

## Evidence (lit + census)

- **SWEBOK Guide v4.0** (IEEE CS, 2024) — KA *Software Maintenance*: maintenance categories (adaptive/perfective/corrective/preventive), maintainability as designed-in cost-of-change, retirement/disposal stage. [lit] https://www.computer.org/education/bodies-of-knowledge/software-engineering
- **ISO/IEC 25010:2023** — *Maintainability* attribute with five sub-characteristics: modularity, reusability, analysability, modifiability, testability. [lit] https://www.iso.org/standard/78176.html
- **Fowler — Technical Debt + the Debt Quadrant** (deliberate/inadvertent × prudent/reckless): debt = internal-quality deficiency you pay interest on; prudent-deliberate is logged, reckless is the failure mode. [lit] https://martinfowler.com/bliki/TechnicalDebt.html
- **Fowler, *Refactoring* (2nd ed., 2018)** — the named refactoring catalog (Extract/Move/Inline/Rename) under green tests; Boy-Scout discipline; "make the change easy, then make the easy change." [lit] https://martinfowler.com/books/refactoring.html
- **Fowler — Strangler Fig Application** (rev. 2024) — incremental replacement of legacy behind a façade, each step shippable/reversible, vs. big-bang rewrite. [lit] https://martinfowler.com/bliki/StranglerFigApplication.html
- **Feathers, *Working Effectively with Legacy Code*** — "legacy = code without tests"; characterization tests + seams to pin behavior before refactoring. [lit] https://understandlegacycode.com/blog/characterization-tests-or-approval-tests/
- **ArchUnit** — JVM library: bytecode-analysed dependency/layer/cycle rules run as ordinary unit tests (build fails on architecture erosion). [lit] https://www.archunit.org/
- **Deptrac** — PHP static layer/dependency-rule enforcer (same fitness-function role for non-JVM). [lit] https://deptrac.github.io/deptrac/
- **SonarQube metric definitions** — *technical-debt ratio* (remediation effort ÷ rewrite cost) → A–E maintainability rating; complexity/duplication/cognitive-complexity metrics; "new-code" quality gate so debt only decreases per PR. [lit] https://docs.sonarsource.com/sonarqube-server/latest/user-guide/metric-definitions/
- **[census] publish-axis:** the *visible* enforcement of this aspect is mostly carried by lint/CI config (aspect 04/03 — biome/eslint/ruff ubiquitous in the dev-environment census) and review (aspect 07); a *named, separated* debt register or ArchUnit-style architecture test is rare in OSS. Maintainability is overwhelmingly a [lit]/practice aspect: seniors *do it*, repos rarely *publish a debt artifact*. No dedicated wider survey run — see `census_todo`. [census]

## Archetype variations

- **library / cli:** maintainability ≈ a small, stable public surface + low internal coupling; semver + a clear deprecation window is the dominant debt discipline (breaking change = the costliest debt). Heavy architecture-test tooling is overkill.
- **backend / web:** richest surface — complexity budgets + module-boundary fitness functions + strangler migrations earn their keep; SonarQube/quality-gate "new-code" enforcement is common on mature teams.
- **monorepo:** dependency-direction + no-cross-package-back-edges is *the* maintainability control (ArchUnit/Deptrac/import-linter + CODEOWNERS seams); duplication across packages is the headline debt.
- **data-ml:** debt is data/pipeline-shaped — schema drift, dead features, notebook-to-pipeline cruft, train/serve skew; characterization tests apply to transforms, not just code (cross-link aspect 26).
- **mobile:** platform-version churn drives *adaptive* maintenance; deprecation of old OS/SDK targets on a schedule is the core discipline.
- **ai-harness (8th archetype):** the harness's own guardrails/components are the maintenance surface — "every guardrail itself tested" (gingoa C3); debt lives as deferred ADRs (e.g. monorepo split, ADR-0004) rather than code TODOs.
- No archetype is *gated* — maintainability is universal/cross-cutting; tooling depth scales with codebase size and team coordination cost.

## Tradeoffs / what's ruled out

- **Ruled out: big-bang rewrite.** Strangler-fig incremental replacement is the senior default; full rewrites are high-risk and usually under-deliver — reserved for genuinely terminal legacy.
- **Ruled out: silent/reckless debt.** Undocumented shortcuts compound invisibly; the bar is *prudent-deliberate, logged* debt with a rationale, not zero debt (which over-engineers).
- **Ruled out: refactor mixed into a feature commit.** Always separate the (behavior-preserving) refactor commit from the behavior change — keeps review, bisect, and revert tractable.
- **Tension — coverage gate vs. velocity.** Hard complexity/debt ceilings on *all* code can stall delivery; the resolution is the **"new-code" gate** (debt may only decrease) rather than a blanket cleanup mandate.
- **Cost of architecture tests:** ArchUnit/Deptrac add maintenance; apply only where module boundaries actually matter (monorepo/large backend), not as blanket ceremony.
- **Refactoring without tests is gambling:** never refactor untested legacy without first writing characterization tests — otherwise "cleanup" silently changes behavior.

## Sources

- SWEBOK Guide v4.0 (KA Software Maintenance) — https://www.computer.org/education/bodies-of-knowledge/software-engineering
- ISO/IEC 25010:2023 (Maintainability quality attribute) — https://www.iso.org/standard/78176.html
- Fowler — Technical Debt (+ Debt Quadrant) — https://martinfowler.com/bliki/TechnicalDebt.html
- Fowler — *Refactoring* (2nd ed.) — https://martinfowler.com/books/refactoring.html
- Fowler — Strangler Fig Application — https://martinfowler.com/bliki/StranglerFigApplication.html
- Characterization tests / Feathers legacy-code discipline — https://understandlegacycode.com/blog/characterization-tests-or-approval-tests/
- ArchUnit — https://www.archunit.org/
- Deptrac — https://deptrac.github.io/deptrac/
- SonarQube metric definitions (technical-debt ratio, quality gate) — https://docs.sonarsource.com/sonarqube-server/latest/user-guide/metric-definitions/

## Sub-documents
- [`refactoring-debt-discipline--facts-2026-08.md`](refactoring-debt-discipline--facts-2026-08.md) — *research-log (ko)* — 2026-08 facts-only pass (R2-3): 리팩터링과 행동 변경의 분리(Fowler·Google eng-practices) · 기술부채 등록/추적 · ISO 25010 maintainability(전문 유료라 **카탈로그 수준까지만 1차**) · SWEBOK 전문 미확보.
