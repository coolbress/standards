---
id: aspect-22-documentation-knowledge
title: "Documentation & Knowledge Management"
group: "G — Cross-cutting Practice & Governance"
kind: cross-cutting
gated_archetypes: []
cross_cutting: true
lifecycle_stages: ["all"]
anchors: ["Diataxis", "IEEE-ISO-15289", "docs-as-code"]
evidence_track: census+lit
status: review-needed
last_updated: "2026-06-25"
sources:
  - "https://diataxis.fr/"
  - "https://www.writethedocs.org/guide/docs-as-code/"
  - "https://www.iso.org/standard/74345.html"
  - "https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions"
  - "https://adr.github.io/madr/"
  - "https://research.jku.at/en/publications/using-architecture-decision-records-in-open-source-projects-an-ms/"
  - "https://keepachangelog.com/en/1.1.0/"
  - "https://www.swagger.io/specification/"
  - "https://sre.google/sre-book/being-on-call/"
  - "https://docs.vale.sh/topics/styles"
  - "https://docs.github.com/en/contributing/collaborating-on-github-docs/using-the-content-linter"
claim: "Senior teams treat docs as versioned code organized by reader-intent (Diátaxis: tutorial/how-to/reference/explanation), ship a standard repo-doc set (README/CONTRIBUTING/SECURITY/CHANGELOG), record significant decisions as ADRs, generate API/runbook reference from source, and keep all of it fresh via CI link/freshness checks rather than as a one-time write."
maps_from: ["census-data/census-governance", "census-data/census-expanded"]
---

> **Standard (claim):** Treat documentation as **versioned code organized by reader-intent** — Diátaxis four modes, a standard repo-doc set, ADRs for decisions, generated reference (OpenAPI/runbooks), and CI-enforced freshness — not a one-time write.
> **Evidence:** census+lit (429-repo governance survey + 938-repo expanded survey, recency-weighted) · **Confidence:** high (file-doc census strong; ADR/runbook lean lit) · **Kind:** cross-cutting · **Stage:** all

**Seed sub-aspects:** `Diátaxis 4-mode` · `README / CONTRIBUTING / SECURITY / CHANGELOG` · `ADR records` · `API docs (OpenAPI)` · `runbooks` · `doc freshness / link-check` · `knowledge management (lessons-learned / bus-factor)`

## What professional engineers do

- **Organize by reader-intent, not by topic (Diátaxis).** Four distinct modes, each a separate doc with one job: **tutorial** (learning-oriented, guaranteed-success walkthrough), **how-to guide** (task-oriented recipe), **reference** (information-oriented, dry + complete), **explanation** (understanding-oriented, the "why"). Mixing modes in one page is the classic failure; the rule is **one doc = one purpose**. `[lit]`
- **Docs-as-code.** Docs live in the repo as plain-text/Markdown, version-controlled alongside code, changed via PR + review, and built/checked in CI. Same toolchain, same gates as code → docs stay in sync and reviewable. `[lit]`
- **Ship the standard repo-doc set.** Near-universal: **README** (orientation + quickstart), **LICENSE**. Strongly expected: **CONTRIBUTING**, **SECURITY.md** (vuln disclosure), **CODE_OF_CONDUCT** (public OSS), **CHANGELOG** (Keep a Changelog format), plus **issue/PR templates** and **CODEOWNERS** for review routing. `[census]`
- **Record significant decisions as ADRs.** One short immutable record per architecturally-significant decision — **status / context / decision / consequences** (Nygard; MADR is the Markdown standard). Append-only log under `docs/adr/`; supersede rather than rewrite. Captures the *why* that code can never show. `[lit]`
- **Generate reference from source of truth.** API reference from **OpenAPI/Swagger** specs (or typed schema), CLI `--help`, docstring extractors — generated, never hand-transcribed, so it can't drift. `[lit]`
- **Runbooks for operations.** Each alert/oncall scenario has a runbook: symptoms → diagnosis → mitigation steps → escalation. Google SRE: a good runbook roughly **3×** improves MTTR vs improvisation; treated as living ops reference. `[lit]`
- **Lint + gate docs in CI (freshness AND content).** Run doc linters in CI at code-linter seriousness:
  **link-checkers** (lychee/markdown-link-check), **markdownlint** (structure), **Vale** (prose/style +
  terminology), **cspell/codespell** (spelling), doc-build-must-pass. For a **public/internal doc split**, a
  **forbidden-terms / de-jargon gate** (Vale `reject.txt`/`Vale.Avoid`, or a custom grep job) fails CI when
  internal jargon/codenames leak into public docs — used by GitHub/GitLab/Datadog/Grafana/Stoplight. Census:
  markdownlint 8.7k / Vale 6.9k CI-workflow mentions. Stale or jargon-leaking docs are a defect class; this is
  a gate, not a hope. Full survey: [`content-ci-linting-and-jargon-gate.md`](content-ci-linting-and-jargon-gate.md). `[lit][census]`
- **Knowledge management / bus-factor.** Onboarding docs, lessons-learned / postmortems (blameless), an architecture overview so understanding survives staff turnover. The goal: no single point of knowledge failure. `[lit]`

## Evidence (lit + census)

- **Diátaxis** (Daniele Procida) — the four-mode authoring grammar; adopted by Django, Gatsby, Cloudflare docs. → https://diataxis.fr/ `[lit]`
- **Docs-as-code** (Write the Docs) — version control + plain text + review + CI for docs. → https://www.writethedocs.org/guide/docs-as-code/ `[lit]`
- **ISO/IEC/IEEE 15289:2019** — information items (content) for systems/software life-cycle processes; the standards anchor for *what* documents a process produces. → https://www.iso.org/standard/74345.html `[lit]`
- **ADR** — Nygard, "Documenting Architecture Decisions" (2011): status/context/decision/consequences. → https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions · **MADR** → https://adr.github.io/madr/ `[lit]`
- **ADR adoption (MSR study)** — Buchgeher et al., *Using Architecture Decision Records in Open Source Projects* (IEEE Access 2023, 900+ repos): ADR adoption is low but rising yearly; ~50% of ADR repos hold only 1–5 records ("tried, didn't stick"); Nygard template dominant. Matches our census ADR ≈ 2–4%. → https://research.jku.at/en/publications/using-architecture-decision-records-in-open-source-projects-an-ms/ `[lit]`
- **Keep a Changelog 1.1.0** — human-curated, Unreleased-section CHANGELOG convention. → https://keepachangelog.com/en/1.1.0/ `[lit]`
- **OpenAPI Specification** — machine-readable API contract → generated reference. → https://www.swagger.io/specification/ `[lit]`
- **Google SRE Book** — runbooks/playbooks as living ops reference (MTTR impact). → https://sre.google/sre-book/being-on-call/ `[lit]`

**Census (recency-weighted, `w = 0.5^(age/2yr)`):**
- **README ≈ 100%** uni / 100% wgt (n=938) — and 97/99 in the 429-foundation survey: the only truly universal doc. `[census]`
- **CONTRIBUTING ≈ 75% / 70%**, **SECURITY.md ≈ 56% / 60%** (rising on weight), **CHANGELOG ≈ 52% / 51%**, **CODE_OF_CONDUCT ≈ 42% / 39%**, **CODEOWNERS ≈ 26% / 30%** (n=938). `[census]`
- **Issue templates ≈ 76% / 78%**, **PR templates ≈ 53% / 54%** (n=938) — process-doc-as-form, well-adopted. `[census]` **↑ Widened N=2000** (`census-issue-pr/census2k.py`, 2026-07-05, same tree-based case-insensitive detection): issue templates **68%**, PR templates **44%** — lower at the wider star-depth (the top-938 are more governed), confirming the same well-adopted pattern holds deeper into the top-2000-by-stars software field. `[census]`
- **Planning/design docs in tree** (n=429): any planning artifact **13% uni / 19% wgt / 17% young**; design-doc 11→**16%**; formal **ADR dir 2–4%**; RFC dir 1–2%. Decision-docs are *made* (senior practice) but rarely *published* to public remotes. `[census]`

## Archetype variations

- **No gated archetypes** — every project gets README + LICENSE + decision-recording; the *set* scales with archetype.
- **Library / published:** reference docs + generated API docs are primary; **CHANGELOG** is mandatory (consumers track breaking changes); thorough README quickstart.
- **Backend-service / data-ml:** **runbooks** + operational docs become first-class (oncall, dashboards, escalation); OpenAPI reference for HTTP APIs.
- **Web-app / mobile:** user-facing how-to/tutorials weigh more; design-doc adoption is highest here per census (web-app anyplan ≈ 21%).
- **Monorepo / multi-team:** **CODEOWNERS** (census 32→33% for monorepo) + per-package READMEs + an architecture overview to manage cross-team knowledge; ADR adoption highest among monorepos (6%).
- **CLI:** `--help`/man-page reference + README usage examples carry most weight.

## Tradeoffs / what's ruled out

- **Ruled out: heavyweight upfront doc suites** (full ISO 15289 information-item set, wiki sprawl) for small projects — they rot faster than they help. Ship the *minimum reader-intent-complete* set and grow it.
- **Ruled out: hand-maintained API/reference docs** — they drift from code; generate from spec/source instead.
- **Tension — ADR rarity vs senior practice:** the MSR study + our census show ADRs barely adopted in the wild (2–4%), yet they are a clear senior practice (capture the irreversible "why"). Resolution per the corpus two-axis rule: **do it `[lit]`, but keep local/team by default** (`plans/`, `docs/internal/`), publish opt-in — matching the 13–19% public-planning reality.
- **Tradeoff — docs-as-code friction:** PR+CI gates on docs slow trivial edits but are the only durable way to keep docs in sync; net-positive at production grade.
- **Tradeoff — freshness gates have false positives** (link-checkers flag rate-limited/ephemeral URLs); mitigate with allowlists rather than dropping the gate.

## Sources
- Diátaxis — https://diataxis.fr/
- Docs as Code (Write the Docs) — https://www.writethedocs.org/guide/docs-as-code/
- ISO/IEC/IEEE 15289:2019 — https://www.iso.org/standard/74345.html
- Nygard, Documenting Architecture Decisions — https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions
- MADR — https://adr.github.io/madr/
- Buchgeher et al., ADRs in OSS (IEEE Access 2023) — https://research.jku.at/en/publications/using-architecture-decision-records-in-open-source-projects-an-ms/
- Keep a Changelog 1.1.0 — https://keepachangelog.com/en/1.1.0/
- OpenAPI Specification — https://www.swagger.io/specification/
- Google SRE Book, Being On-Call — https://sre.google/sre-book/being-on-call/

## Sub-documents
- [`facts-2026-08-repo-docs-adr-runbook.md`](facts-2026-08-repo-docs-adr-runbook.md) — *research-log (ko)* — 2026-08 facts-only pass (R2-2): README/CONTRIBUTING/SECURITY/CHANGELOG의 근거 · ADR 원형식(Nygard) · runbook. **Keep a Changelog·Diátaxis·ADR·SRE runbook은 표준 기관 산출물이 아님**(표준 vs 처방 구분표 포함).
- [`content-ci-linting-and-jargon-gate.md`](content-ci-linting-and-jargon-gate.md) — *research-log* — content/prose linting in CI (markdownlint/Vale/cspell/link-check) + the de-jargon (forbidden-internal-terms) gate for a public/internal doc split: lit + gh adoption census + the de-facto-tool verdict.
