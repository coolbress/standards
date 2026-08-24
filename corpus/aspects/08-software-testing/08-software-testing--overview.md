---
id: aspect-08-software-testing
title: "Software Testing"
group: "C — Construct & Verify"
kind: universal
gated_archetypes: []
cross_cutting: true
lifecycle_stages: ["③"]
anchors: ["SWEBOK-KA5", "ISO-25010", "test-pyramid"]
evidence_track: census+lit
status: review-needed
last_updated: "2026-06-25"
sources:
  - "https://www.computer.org/education/bodies-of-knowledge/software-engineering"
  - "https://martinfowler.com/articles/practical-test-pyramid.html"
  - "https://martinfowler.com/bliki/TestPyramid.html"
  - "https://iso25000.com/index.php/en/iso-25000-standards/iso-25010"
  - "https://docs.pact.io/"
  - "https://martinfowler.com/bliki/ContractTest.html"
  - "https://increment.com/reliability/eradicating-non-determinism-in-tests/"
  - "https://testing.googleblog.com/2020/12/test-flakiness-one-of-main-challenges.html"
  - "https://mutation-testing.org/"
claim: "A senior-grade project tests in a pyramid (many fast unit tests, fewer integration, very few e2e) wired into the CI test gate, treats coverage as a non-regression floor (never a target), uses contract tests across service/library boundaries, and quarantines flaky tests rather than tolerating them."
maps_from: ["census-data/census-dev-environment"]
---

> **Standard (claim):** _Test in a pyramid (many fast unit, fewer integration, very few e2e) wired into the CI `test` gate; coverage is a non-regression floor (never a target); contracts cover boundaries; flaky tests are quarantined, not tolerated._
> **Evidence:** test_framework 88% simple / 86% weighted / **90% at N=938** `[census]` + test-pyramid / SWEBOK-KA5 `[lit]` · **Confidence:** high (universal core; coverage-gating is a maturity tier) · **Kind:** universal · cross-cutting · **Stage:** ③

**Seed sub-aspects:** `unit / integration / e2e` · `contract testing (Pact)` · `property / mutation` · `BDD` · `test data / fixtures` · `coverage-as-floor` · `flakiness` · `archetype matrices (browser/device/multi-version)`

## What professional engineers do

- **A test harness is table stakes; the runner config + `tests/` ship at scaffold time.** A test runner (`vitest`/`pytest`/`go test`/`cargo test`) with a `tests/` tree is the durable construct-phase floor: **test_framework 88% simple / 86% weighted / 90% at N=938** — one of the few flags that survives sample-doubling almost unmoved `[census]`. SWEBOK KA5 frames testing as dynamic verification against expected behavior over a finite, well-chosen set of cases `[lit]`.
- **Shape the suite as a pyramid.** Many small fast **unit** tests at the base, **some** integration/service tests in the middle, **very few** end-to-end tests at the top — and *push every test as far down the pyramid as it will go* (Vocke/Fowler, *The Practical Test Pyramid*, 2018) `[lit]`. The inverted "ice-cream cone" (mostly slow e2e) is the named anti-pattern: slow feedback, flaky, redundant with lower layers.
- **Wire tests into the CI gate, not just locally.** `test` is one of the four unbypassable CI checks (lint·typecheck·**test**·build); CI 92–93% is the enforced merge gate `[census]` (see aspect-04). A passing local run is not the gate — the server-side run is.
- **Coverage is a floor, never a target.** Track coverage to catch *regressions* (ratchet: new code must not drop the line), but do not chase a number — gaming coverage (asserting nothing, testing getters) is a known failure mode. Census backs this as a *maturity*, not birth, default: **coverage_config 25% simple → 17% weighted (↓−8), 13% at N=938** `[census]` — highest in libraries (43%) `[census]`. Goodhart applies: a coverage *quota* becomes a bad metric.
- **Contract tests at every boundary.** Where a consumer and provider are deployed/released independently (service↔service, library↔consumer), **consumer-driven contract tests** (Pact) verify the integration without a full e2e environment — the consumer's expectations become a versioned contract the provider verifies in its own pipeline (Fowler, *ContractTest*; Pact docs) `[lit]`. This replaces brittle, slow cross-service e2e for most integration coverage.
- **Property & mutation testing for high-value logic (senior tier).** **Property-based** testing (Hypothesis/fast-check/proptest) asserts invariants over generated inputs rather than hand-picked examples — finds edge cases example tests miss. **Mutation testing** (Stryker/`mutmut`/PIT) measures *test effectiveness* by injecting faults and checking the suite catches them — the honest answer to "is my coverage real?" `[lit]`. Applied to parsers, contracts, money/date logic — not every module.
- **BDD where behavior is the spec.** Gherkin/`given-when-then` (Cucumber/behave) ties acceptance criteria to executable scenarios; valuable when non-engineers own the spec, overhead otherwise. The senior default is plain unit/integration tests with descriptive names; BDD is opt-in for stakeholder-facing acceptance.
- **Deterministic, isolated test data.** Fixtures/factories over shared mutable state; each test sets up and tears down its own data; no ordering dependence; no real network/clock/randomness (inject them). Non-determinism is the root cause of flakiness (Fowler, *Eradicating Non-Determinism in Tests*) `[lit]`.
- **Treat flaky tests as bugs — quarantine, don't tolerate.** A test that passes and fails on identical code erodes trust in the whole suite. Senior practice: detect (re-run / flakiness dashboards), **quarantine** out of the blocking gate, file a fix, and delete-or-fix on a deadline — never `retry` blindly in CI (Google Testing Blog; Fowler) `[lit]`.

## Evidence (lit + census)

- **Test harness is a universal, durable floor:** test_framework 88 simple / 86 weighted / **90 at N=938** (smplΔ ≈ +2 — confirms mandate) `[census]`. Runner winners (weighted): **pytest 98 · vitest 62 · go-test 42 · jest 31 · cargo-test 30 · playwright 6** `[census]` → harness defaults JS/TS **vitest** · Py **pytest** · Rust cargo · Go go.
- **Coverage gating is a maturity signal, not a birth default:** coverage_config 25→**17** weighted (↓−8), **13 at N=938** `[census]`; archetype split: **library 43%** (publishers gate hardest) vs. web-app 12, cli 14, data-ml 13 `[census]` — confirms coverage belongs in conditional/maturity, not universal core.
- **playwright present but rare (6)** `[census]` → e2e is a thin top layer, consistent with the pyramid `[lit]`.
- **`[lit]` anchors:** SWEBOK KA5 Software Testing (test levels: unit/integration/system; techniques) · Fowler/Vocke *The Practical Test Pyramid* & *TestPyramid* bliki · Fowler *ContractTest* + Pact (consumer-driven contracts) · ISO/IEC 25010 (functional-suitability / reliability quality characteristics that tests verify) · Fowler *Eradicating Non-Determinism in Tests* + Google Testing Blog (flakiness).

## Archetype variations

- **library:** highest coverage discipline (coverage_config 43% `[census]`); **cross-version test matrix** (multiple language/runtime versions) is the library-specific axis; public-API contract tests for consumers; property tests for pure logic.
- **backend-service:** integration tests against a real DB (Testcontainers); **consumer-driven contract tests** (Pact) replace full cross-service e2e; load/perf as a separate track (ISO-25010 performance-efficiency).
- **web-app (gated browser matrix):** **e2e/browser** tests (Playwright/Cypress) across a *bounded* browser set + component tests; the pyramid caps e2e count to high-value journeys `[lit]`; visual-regression optional.
- **mobile (gated device matrix):** instrumented + UI tests across a **device/OS matrix**; emulator + a slice of real devices; the matrix is the cost driver — keep it small.
- **cli:** golden-file / snapshot tests of stdout/exit-codes + a few end-to-end invocation tests; fast unit base for arg parsing and core logic.
- **data-ml:** data-validation + pipeline tests; non-determinism (seeds, float tolerance) is first-class; coverage low in the wild (13%) `[census]`.

## Tradeoffs / what's ruled out

- **Coverage as a *target* — ruled out.** Drives Goodhart gaming (assertionless tests, trivial getters); use it as a non-regression ratchet only. Census also shows coverage-gating is a maturity, not day-one, default (17% weighted) `[census]`.
- **Broad e2e suites ("ice-cream cone") — ruled out.** Flaky, slow, redundant with lower layers; e2e is the thin top reserved for genuine user journeys; integration coverage moves to contract tests `[lit]`.
- **Blind CI retries for flaky tests — ruled out.** Hides real bugs and decays trust; quarantine + fix-with-deadline instead `[lit]`.
- **Mutation/property testing everywhere — ruled out (cost).** High signal but slow; scope to high-value/invariant-rich modules, not every file.
- **BDD as a universal default — ruled out.** Overhead unless non-engineers own the acceptance spec; plain descriptive unit/integration tests are the senior default.

## Sources

- SWEBOK (KA5 Software Testing) — https://www.computer.org/education/bodies-of-knowledge/software-engineering
- Ham Vocke / Martin Fowler — The Practical Test Pyramid (2018) — https://martinfowler.com/articles/practical-test-pyramid.html
- Martin Fowler — TestPyramid (bliki) — https://martinfowler.com/bliki/TestPyramid.html
- ISO/IEC 25010 (product quality model) — https://iso25000.com/index.php/en/iso-25000-standards/iso-25010
- Pact — consumer-driven contract testing — https://docs.pact.io/
- Martin Fowler — ContractTest — https://martinfowler.com/bliki/ContractTest.html
- Martin Fowler — Eradicating Non-Determinism in Tests — https://increment.com/reliability/eradicating-non-determinism-in-tests/
- Google Testing Blog — Test Flakiness — https://testing.googleblog.com/2020/12/test-flakiness-one-of-main-challenges.html
- Mutation Testing — https://mutation-testing.org/

## Sub-documents
- [`testing--facts-2026-08.md`](testing--facts-2026-08.md) — *research-log (ko)* — 2026-08 facts-only pass: pyramid/trophy originals · Google test sizes 80/15/5 + flakiness data · TDD meta-analyses · coverage guidance · mutation testing at Google · ISTQB levels.
