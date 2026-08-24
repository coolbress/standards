---
id: aspect-07-construction-code-review
title: "Software Construction & Code Review"
group: "C — Construct & Verify"
kind: universal
gated_archetypes: []
cross_cutting: false
lifecycle_stages: ["③"]
anchors: ["SWEBOK-KA4", "Google-eng-practices"]
evidence_track: lit
status: review-needed
last_updated: "2026-06-25"
sources:
  - "https://www.computer.org/education/bodies-of-knowledge/software-engineering"
  - "https://google.github.io/eng-practices/review/"
  - "https://google.github.io/eng-practices/review/developer/small-cls.html"
  - "https://google.github.io/eng-practices/review/reviewer/standard.html"
  - "https://research.google/pubs/modern-code-review-a-case-study-at-google/"
  - "https://itrevolution.com/product/accelerate/"
claim: "Construction is a reviewed change-unit loop: small self-contained changes written test-first to a fixed style, each gated by mandatory lightweight peer review (≥1 approval, CL ≈100 lines) before merge."
maps_from: []
---

> **Standard (claim):** Construction is a reviewed change-unit loop — small self-contained changes, written test-first to a fixed style, each gated by mandatory lightweight peer review (≥1 approval, CL ≈100 lines) before merge.
> **Evidence:** [lit] SWEBOK KA4 · Google eng-practices · Sadowski et al. ICSE-SEIP 2018 · Accelerate/DORA · **Confidence:** high · **Kind:** universal · **Stage:** ③

**Seed sub-aspects:** `coding standards` · `code review (CL size / duties)` · `TDD` · `defensive coding` · `complexity budgets` · `AI-assisted-code hygiene`

## What professional engineers do
- **Coding standards (enforced, not aspirational).** One agreed style per language, applied by an auto-formatter + linter so style is never a review topic. Naming, structure, and idioms are codebase-consistent; the standard runs in pre-commit and CI, not in reviewers' heads. [lit] SWEBOK KA4 "Coding"; [census] linter/format config present in 61% of canonical harnesses (73% of application harnesses).
- **Test-first / TDD.** Behavior is specified by a failing test before the implementing code (RED→GREEN→REFACTOR); tests ship in the same change-unit as the code. Continuous integration keeps trunk always green. [lit] SWEBOK KA4 "Construction Testing"; Accelerate links test automation + CI to delivery performance. [census] tests present in 92% of canonical harnesses (96% of application harnesses).
- **Code review — mandatory, lightweight, fast.** Every change requires ≥1 reviewer approval before merge; review is informal and tool-assisted, not a heavyweight inspection. The reviewer's job: would this *improve overall code health* even if imperfect? Approve once it's a net positive — never block on "could be better." Author and reviewer have asymmetric duties (author keeps CLs small + self-explanatory; reviewer responds within a business day). [lit] Google eng-practices; Sadowski et al. (Google) ICSE-SEIP 2018 — near-universal at Google, optimized for speed + education over defect-finding.
- **Small changelists (CL size = the primary review lever).** ~100 lines is a reasonable CL; ~1000 is too large. One self-contained change per CL → faster reviews, fewer bugs, easier rollback, better design. Reviewers may reject a CL outright solely for being too large. [lit] Google eng-practices "small CLs."
- **Defensive coding.** Validate inputs at boundaries, fail fast with clear errors, make illegal states unrepresentable (types/assertions), handle errors explicitly rather than swallowing. Construction-time technique selection (data structures, error handling, concurrency primitives) is a deliberate SWEBOK KA4 activity. [lit] SWEBOK KA4 "Managing Construction / Coding."
- **Complexity budgets.** Prefer the simplest construction that works; keep functions/modules small and cohesive; treat rising cyclomatic complexity, duplication, and coupling as review-blocking smells. Refactor continuously (Boy-Scout rule) so design stays polishable inside small CLs. [lit] SWEBOK KA4 "Construction for Quality / Reduction in Complexity."
- **AI-assisted-code hygiene.** Generated code is held to the *same* gates — it is reviewed, tested, and style-conformed like any other change, never merged on trust. The author owns and can explain every line; the reviewer reviews the diff, not the prompt. [inferred] direct application of the review-bar duty to generated diffs (gingoa's core threat model — see Implications).

## Evidence (lit + census)
- [lit] **SWEBOK v3/v4, KA4 Software Construction** — coding, construction testing, reuse, quality, managing construction. IEEE Computer Society. https://www.computer.org/education/bodies-of-knowledge/software-engineering
- [lit] **Google Engineering Practices ("How to do a code review" + "The CL author's guide")** — mandatory ≥1 approval; reviewer standard = "improve overall code health"; CL ≈100 lines / 1000 too large; respond within one business day. https://google.github.io/eng-practices/review/ · https://google.github.io/eng-practices/review/developer/small-cls.html · https://google.github.io/eng-practices/review/reviewer/standard.html
- [lit] **Sadowski, Söderberg, Church, Sipko, Bacchelli — "Modern Code Review: A Case Study at Google," ICSE-SEIP 2018** — review is near-universal, lightweight, and valued primarily for education + knowledge transfer over defect detection. https://research.google/pubs/modern-code-review-a-case-study-at-google/
- [lit] **Forsgren, Humble, Kim — Accelerate (2018, DORA)** — CI, trunk-based development, and test automation are causal capabilities for elite delivery performance. https://itrevolution.com/product/accelerate/
- [census] dev-environment/harness census (n=36 canonical, n=200 full; recency-weighted): **tests 92% / lint+format cfg 61% / pre-commit 28%** (canonical, all); application-harness subset **tests 96% / lint 73%**. Source: `census-data/harness-census/SUMMARY.md §A`. → Tests + a linter are the floor; pre-commit enforcement is opt-in, not a census norm.

## Archetype variations
- **Universal aspect** — no gated archetypes. The review/test loop applies to every archetype; only the *ceremony* scales (gingoa's Tier 0–3, below).
- **Library / SDK:** defensive coding + public-API stability dominate; CLs gate on backward-compat and doc/test coverage of the surface.
- **Service / web-backend:** review weighs error handling, idempotency, and rollback safety; CI gating + trunk-green is non-negotiable.
- **CLI / harness (gingoa itself):** "every shipped guardrail is itself tested" — generated guardrails get the same review/test bar as product code.
- **Prototype / content-only repos:** lower ceremony (smaller change-units may skip a full review round) but never skip the green-CI floor; [census] the long tail ships tests at ~76% even unverified.

## Tradeoffs / what's ruled out
- **Heavyweight formal inspections (Fagan-style) are ruled out** in favor of lightweight tool-assisted review — the Google evidence shows the formal model's overhead doesn't pay back for most teams. [lit] Sadowski 2018.
- **Large CLs are ruled out** even when "logically one feature": reviewability and rollback-ability beat author convenience.
- **Style debates in review are ruled out** — delegated to the formatter/linter; humans review behavior + design only.
- **Cost:** mandatory review + test-first adds latency to each change; mitigated by small CLs (fast partial reviews) and fast reviewer SLAs. The tradeoff is accepted because the alternative — unreviewed, untested, undisciplined commits — is precisely the ③ gap gingoa exists to close.
- **Coverage-as-target is ruled out** as a primary lever (Goodhart); tests track behavior specs, not a percentage.

## Sources
- https://www.computer.org/education/bodies-of-knowledge/software-engineering (SWEBOK KA4)
- https://google.github.io/eng-practices/review/
- https://google.github.io/eng-practices/review/developer/small-cls.html
- https://google.github.io/eng-practices/review/reviewer/standard.html
- https://research.google/pubs/modern-code-review-a-case-study-at-google/ (Sadowski et al., ICSE-SEIP 2018)
- https://itrevolution.com/product/accelerate/ (Forsgren/Humble/Kim, DORA)

## Sub-documents
- [`codereview--facts-2026-08.md`](codereview--facts-2026-08.md) — *research-log (ko)* — 2026-08 facts-only pass: Google eng-practices review criteria · ICSE-2018/Microsoft/SmartBear review data · pair-programming data · git workflow prescriptions · Conventional Commits.
