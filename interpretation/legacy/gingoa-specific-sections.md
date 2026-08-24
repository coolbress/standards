> ⚠️ **아카이브 (2026-08-02 감사)** — gingoa 시절 원문 보존본. 내부 상대 링크는 원 위치 기준이라 깨져 있을 수 있다. 활성 문서는 `../../corpus/`를 보라.

# Legacy gingoa-specific sections extracted from the evidence corpus

> Migration date: 2026-08-02. These are historical application decisions, not general evidence.
> The byte-for-byte pre-migration corpus is recoverable from
> `.scratch/research/archive/2026-08-02/pre-curation-snapshot.tar.gz`.

## `.scratch/research/corpus/aspects/01-requirements-planning/01-requirements-planning--overview.md`

- Former `gingoa_applied`: `"docs/PRD.md"`

## Implications for gingoa
- gingoa runs ① as a **generative, Socratic inception interview** (it fills the gap a non-engineer can't
  articulate), producing one durable handoff artifact: the **contract** (C1–C8) that deterministically
  selects the ② foundation set — archetype/stack pick templates, NFRs tune quality gates, the MVP cut
  picks the walking-skeleton slice, acceptance criteria seed the first tests. (`01-planning §5`.)
- Requirement language is normative (RFC 2119 MUST/SHOULD/MAY + 29148 well-formedness) so the PRD is
  machine-actionable, mapping onto Spec Kit's Specify→Plan→Tasks→Implement (① = Specify+Plan).
- **The DEFINITIVE planning-document standard (anti-supersede, 2026-06-26).** Two deep surveys (canonical
  templates + a 500k+-file gh census) fix the ① artifact family for good: the **document KINDS × sections ×
  naming × location × publish** standard is [`planning-document-family.md`](planning-document-family.md), and
  the **decision-record / ADR standard + IS-vs-ISN'T-an-ADR refactor rubric** is
  [`decision-record-standard.md`](decision-record-standard.md). Headlines: constitution layer in the wild =
  **`AGENTS.md`/`CLAUDE.md`** (census 130k/40k ≫ `constitution.md` 2k); per-feature quartet = `spec.md`/
  `design.md`/`plan.md`/`tasks.md`; `PRD.md` is the project-requirements winner. **gingoa's FINAL ① set =
  constitution(AGENTS/CLAUDE) + `prd.yml`(SSOT)→`PRD.md`(generated) + `docs/adr/`**; per-feature spec/design/
  plan/tasks are ③-JIT; **standalone `BACKLOG.md` is dropped** (committed product-backlog is non-standard —
  feature inventory = PRD §Scope, work backlog = Issues). ADR = Nygard-minimal, `docs/adr/NNNN-kebab`, ①→④.
- **gingoa already applied this to itself:** its own LOCKED contract — intent layer (C1–C4/C8) from the
  Socratic interview, derived layer (C5/C6) from the OSS-tooling standard — lives at
  `docs/PRD.md` (+ `prd.yml`,
  `adr/`). Per the publish axis these sit at their canonical `docs/` path but are gitignored (team-shared,
  not auto-pushed).
- **Brownfield ①-plan adoption (2026-07-02).** The greenfield elicit path assumes gingoa authors the PRD at
  maximum ignorance; when gingoa is pointed at an *existing* project the ①-plan input already partially exists.
  The field's de-facto branch is **present-same → IMPORT · present-different → CONVERT · absent →
  REVERSE-ENGINEER** — and reverse-engineering is always **flatten-first** (codebase → structured digest →
  derive PRD, never code → PRD directly; BMAD `document-project`/Aider/Repomix), with every derived field
  **INFERRED until the user confirms** (feeds gingoa's lock/seal gate). This is the ①-plan slice of the
  cross-stage `adopt` model → [`brownfield-planning-adoption.md`](brownfield-planning-adoption.md) (spine in
  [`../../lifecycle.md`](../../lifecycle.md) §New vs Adopt).

## `.scratch/research/corpus/aspects/01-requirements-planning/constitution-authoring-standard.md`

## gingoa application
Mandatory artifact (gingoa is AI-agent-operated, and emits one for every project it builds). gingoa's
`CLAUDE.md`(SSOT) + `AGENTS.md`(mirror) follow this: North-star + exact Build&verify (incl. single-test) +
Code-style + Architecture (one-way core→adapter) + Commits&PRs + **Boundaries (Always/Ask/Never)**, <200 lines.
The **elicit/scaffold feature must emit a user project's `AGENTS.md`+`CLAUDE.md` to this skeleton** (the
constitution kind from `planning-document-family.md`). Relates to aspect-27 (AGENTS.md is its anchor) + aspect-22.

## `.scratch/research/corpus/aspects/01-requirements-planning/decision-record-standard.md`

## gingoa application
gingoa's ADR FORMAT is already correct (Nygard-minimal + date/deciders/related, `NNNN-kebab` in
`docs/adr/`). **RESOLVED (2026-06-27):** the refactor rubric was applied to all 20 ADRs — **all KEEP, 0
reclassified** (recorded in ADR-0020's follow-up). Borderline checks held: 0002/0006 = tactic-adoption ·
0008/0014 = principle-adoption (a valid ADR; the standing rule is also mirrored in `CLAUDE.md` Boundaries) ·
0010/0011/0012 = decided mechanisms under explicit "decide-now, build-later" timing, not open RFCs.

## `.scratch/research/corpus/aspects/02-architecture-design/02-architecture-design--overview.md`

- Former `gingoa_applied`: `"docs/adr"`

## Implications for gingoa

- **Already applied — `docs/adr/`.** gingoa dogfoods this aspect: 12 MADR-lite ADRs capturing its own architecturally-significant decisions (cross-host shared-plugin + per-host manifests, no-mutate host homes, copier shell-out, bundled pipeline core, hard-blocking production floor, the AI-harness 8th archetype, etc.), each context/decision/consequences, with provenance lifted from the ① contract (`PRD.md` §C7) + the feature-map Socratic interview. `gingoa_applied: docs/adr`.
- **Publish-axis baked in.** Per census (ADR 2–4%, design-doc 11–16%), gingoa's ADR README defaults records to 🔒 **local/team**, un-ignored per-file for OSS transparency — matching the two-axis discipline (`_schema.md` §4 (methodology)).
- **① scaffolds the design decisions.** The Socratic inception (① contract C3 NFRs, C5 archetype, C7 ADRs) extracts the style + quality-attribute targets + significant decisions the non-engineer wouldn't think to record; gingoa plays the *senior reviewer* role of the Google design-doc review.
- **② projects design into structure.** Archetype (C5) + NFRs (C3) select the building-block layout and which fitness functions to seed (e.g. monorepo dependency-direction checks, coverage floors, supply-chain gates) — making the production floor the *executable* form of the chosen architecture (cf. ADR-0008 hard-blocking floor).
- **Mechanism-timing:** architecture-level decisions are made at ①/②; detailed per-mechanism implementation is authored JIT at ③ (the per-feature spec).

## `.scratch/research/corpus/aspects/03-dev-environment/03-dev-environment--overview.md`

- Former `gingoa_applied`: `"docs/prd.yml"`

## Implications for gingoa
<!-- How gingoa enforces / scaffolds this. Link gingoa_applied when applied to gingoa itself. -->

- gingoa **scaffolds the reproducible floor by default** at ②: runtime pin + package-manager pin (T2), committed lockfile (T4), and a task runner exposing the exact `lint · typecheck · test · build` verbs CI runs — so local and CI never diverge. The non-engineer never hand-edits a version.
- **`.env.example` + compose** are activated archetype-conditionally (web/backend/data-ml) from the contract, not shipped blindly; `.editorconfig` is a 🟨 nicety, `.gitattributes` (`* text=auto`) is in the universal base for cross-platform safety.
- **Devcontainer is opt-in**, surfaced only for team/onboarding-heavy or polyglot projects (census-justified — not a universal requirement).
- **gingoa applied this to itself** (`docs/prd.yml` + the shipped config): C5=cli, C6=TS/pnpm → ships `.nvmrc` (Node 22) + Corepack pin (T2), committed `pnpm-lock.yaml` (T4), `.editorconfig` + `.gitattributes`, pnpm-script task runner; rules **Dockerfile/devcontainer OUT** (a cli with no container hosting). DoD = `pnpm lint && typecheck && test && build` green on a walking skeleton — the local↔CI parity contract embodied. This is gingoa dogfooding its own ②-foundation standard.

## `.scratch/research/corpus/aspects/04-build-ci-engineering/04-build-ci-engineering--overview.md`

- Former `gingoa_applied`: `"docs/PRD.md"`

## Implications for gingoa

gingoa's ② scaffold treats the four-check CI gate as the **production-minimum-floor** — *executable, hard-blocking checks that pass CI, not docs* (**ADR-0008**). Applied to gingoa itself (`docs/PRD.md`):
- **C6 = TS/pnpm** selects `package.json` + **committed pnpm-lock.yaml** + Corepack/`.nvmrc` pins, `biome.json` (lint+format), `vitest`, `tsconfig` — i.e. the four CI checks `npm run lint · typecheck · test · build` (mirrored in `CLAUDE.md` Build & test).
- **C3 Security HIGH** adds to the floor: **pinned GitHub Actions (by SHA)**, **least-privilege CI token perms**, secret-scan, dependency audit — the SLSA/OpenSSF supply-chain posture `[lit]`.
- **C5 = cli, single-package:** **monorepo split deferred to ADR-0004** — affected-graph/workspace tooling is *not* scaffolded until a 2nd publishable package appears (census: monorepo conditional set; YAGNI).
- **②→③ exit gate (C4):** a walking skeleton (cross-host attach + ping) that is **deployable and CI-green on first commit** — the build/CI engineering is what makes that exit gate real.
- **Full ② floor artifact checklist + repo-context conditioning:** the independent senior-expected bootstrap
  artifact set (VCS/build/CI/quality/test/security/config/dev-env/docs/governance), the most-commonly-missed
  list, and the **public/private · free/GHAS · solo/team conditioning rule** (e.g. Semgrep-OSS-for-private vs
  CodeQL-for-public SAST; branch-protection & Dependabot-npm gated on visibility) →
  [`foundation-floor-artifact-checklist.md`](foundation-floor-artifact-checklist.md).
- **Provision-by-visibility (② build branches on the user's private/public choice):** the authoritative
  GitHub-Docs matrix of which floor features are gated by visibility×plan (CodeQL/secret-scanning/branch-
  protection/environments = ⛔ on private-free; Dependabot-alerts = free), each gated feature's OSS substitute,
  the PRIVATE-default vs PUBLIC-default floor, and the `--make-public` flip list →
  [`visibility-provision-matrix.md`](visibility-provision-matrix.md). **The elicit ① contract MUST carry a
  `visibility` field so ② picks the right column.**
- **Brownfield ②-foundation adoption (2026-07-02).** The floor above is a *greenfield* contract (render into an
  empty owned tree, atomic, green-or-refuse). Pointed at an *existing* project the floor is partially present,
  the project may be RED, and gingoa owns nothing yet — so ② adoption follows five field-grounded mechanics:
  **(1)** run the floor predicate in a read-only **AUDIT mode** (non-blocking maturity report — OpsLevel/Port
  IDP consensus: audit ≠ gate); **(2)** **3-way disposition** missing→add / equal→skip / different→CONFLICT
  (copier/cruft); **(3)** **additive-first** — write only what's missing, surface conflicts via a branch+PR,
  never clobber, never push to `main` (Backstage register); **(4)** an **ownership baseline** (`.copier-answers.yml`
  synthetic empty-base) so future lifecycle rides `copier update` (ADR-0003/0017 — census-validated); **(5)** a
  **relaxed green-gate** — gate only gingoa-ADDED items green, grandfather + ratchet the pre-existing violations
  (SonarQube "Clean as You Code"). This ② slice is the most self-contained of the `adopt` model (reuses the floor
  predicate; does not touch the elicit engine) → [`brownfield-adoption-floor.md`](brownfield-adoption-floor.md)
  (spine in [`../../lifecycle.md`](../../lifecycle.md) §New vs Adopt).

## `.scratch/research/corpus/aspects/04-build-ci-engineering/visibility-provision-matrix.md`

## gingoa application
gingoa is **private + Free + solo** → it is exactly the PRIVATE-default floor: Semgrep (added 2026-06-26),
gitleaks (`security.yml`), `pnpm audit`, CODEOWNERS (file present, enforcement deferred), CI four-check.
Branch-protection/required-review/environments are **launch deferrals** (② foundation), *now explained by
this matrix* (private-free-gated, not oversights). The elicit ① contract MUST capture `visibility` so the ②
build picks the right column; the `--make-public` flip list above is the ④/launch checklist.

## `.scratch/research/corpus/aspects/05-scm-workflow/05-scm-workflow--overview.md`

- Former `gingoa_applied`: `"docs/prd.yml"`

## Implications for gingoa
<!-- How gingoa enforces / scaffolds this. Link gingoa_applied when applied to gingoa itself. -->

gingoa scaffolds and enforces the workflow as the foundation's non-bypassable spine — and crucially defaults-ON the *protective* half that the census shows is rare in the wild (review-before-merge 41%, branch-protection 13%), because the non-engineer user has no peer review and cannot recover a broken `main`:

- **Branching:** trunk-based / GitHub Flow with short-lived branches as the harness's working model; pipeline tiers branch off `main` (gingoa's own MEMORY: PR-first, CC/Codex attach).
- **CI gate:** `.github/workflows/ci.yml` runs lint · typecheck · test · build on every push/PR — the ②→③ green-light (CLAUDE.md: CI gates all four).
- **Conventional Commits (T1):** scaffolds `.github/workflows/pr-title.yml`; gingoa's own convention is **PR title = Conventional Commits** (becomes the squash-merge commit), **issue title = plain summary** (MEMORY: issue-convention).
- **Branch protection ⚖️:** default-ON required review + required green checks on `main` — adopted *above* census median on `[lit]` (Accelerate, OpenSSF) grounds, not popularity.
- **CODEOWNERS:** scaffolded for monorepo / multi-team archetypes.
- **Applied to gingoa itself:** the workflow contract (archetype → which workflow components fire) is encoded in `docs/prd.yml`; gingoa's commit/PR rules live in `CLAUDE.md`. See `gingoa_applied`.

## `.scratch/research/corpus/aspects/06-config-secrets/06-config-secrets--overview.md`

- Former `gingoa_applied`: `"docs/PRD.md"`

## Implications for gingoa

- gingoa scaffolds a committed, value-less **`.env.example`** for service archetypes (census-justified: env_example 36% weighted) and gitignores the real `.env`.
- gingoa's foundation enforces **no-secrets-in-source** as a production-floor gate: `docs/PRD.md` **C3 Security HIGH** mandates "**secret-scan in CI**," and the Security NFR (CONTRACT §, prd.yml) requires "**no secrets in repo**" + supply-chain hardening (pinned actions, least-priv CI token perms, dep audit). This is the gingoa-applied link.
- gingoa itself has a **near-zero runtime secret surface** (an install CLI + template projector), so secret-stores/rotation/feature-flags are scaffolded *for the user's project* by archetype rather than used by gingoa internally — consistent with the cross-cutting, archetype-scaled model above.
- **Startup validation** and **feature flags** are lit-led (no census signal yet); gingoa should treat them as recommended/archetype-gated scaffolds, not universal mandates, until the `census_todo` survey lands.

## `.scratch/research/corpus/aspects/07-construction-code-review/07-construction-code-review--overview.md`

- Former `gingoa_applied`: `"docs/PRD.md"`

## Implications for gingoa
- **Direct application:** this aspect *is* gingoa's stage-③ pipeline. `docs/PRD.md` **US-4 Orchestrate (③)** = "the harness drives implementation at the right ceremony tier — Tier 0–3 pipeline (Issue→Plan→TDD→review→PR) enforced per change size." The seed sub-aspects map 1:1: TDD skill (test-first), code-review skill + review rounds R1/R2 (mandatory ≥1 approval), Conventional-Commits history, CI gating (lint/typecheck/test/build, per CLAUDE.md "Build & test").
- **Enforcement (already built):** biome (lint+format) + vitest (test) + tsc (typecheck) gate every push/PR; the `pr-title` and CI workflows are the non-bypassable gate (`--no-verify` forbidden by constitution).
- **Scaffolding for users:** the harness *fills the gap a non-engineer can't ask for* — it routes change size to a tier, runs TDD on their behalf, and runs the review round as the senior reviewer they don't have. CL-size + review-bar discipline is the harness's, not the user's, responsibility.
- **AI-code hygiene is gingoa's core threat model** (PRD.md: the user "cannot review architecture, will accept whatever is generated — the harness must protect them"): every generated diff passes the same review/test/CI gates before it can merge.

## `.scratch/research/corpus/aspects/08-software-testing/08-software-testing--overview.md`

- Former `gingoa_applied`: `"docs/PRD.md"`

## Implications for gingoa

gingoa's ③ construct phase treats the test harness + the CI `test` gate as the **production-minimum-floor** (executable, hard-blocking — not docs), and drives feature work via **TDD: each C2 acceptance criterion becomes a first failing test** before code. Applied to gingoa itself (`docs/PRD.md` / `prd.yml`):

- **C6 = TS/pnpm** selects **`vitest` config + `tests/`** as part of the L1 ecosystem fill; `npm test` (vitest) is the `test` rung of the four-check CI gate, mirrored in `CLAUDE.md` Build & test.
- **C3 Reliability = HIGH** pins the test obligations to the install/uninstall critical paths: **idempotency + lossless-uninstall tests** and **coverage on the install/uninstall paths** — i.e. coverage-as-floor scoped to the weak-link paths a non-engineer can't recover from, not a global %.
- **Maintainability = HIGH** mandates that **every shipped guardrail is itself tested** — the harness does not ship an unverified guardrail.
- **C2 acceptance criteria** are written as **Done = testable**; US-2's deferred criteria must be hardened into tests before ship — TDD is the bridge from contract AC to executable verification.
- **Contract/property/mutation** are reference-tier here: gingoa's own fail-closed render contract (ADR-0003 copier shell-out) is the natural site for contract-style + property tests as the renderer grows; not scaffolded universally.

## `.scratch/research/corpus/aspects/09-application-security/09-application-security--overview.md`

- Former `gingoa_applied`: `"docs/PRD.md"`

## Implications for gingoa
<!-- How gingoa enforces / scaffolds this. Link gingoa_applied when applied to gingoa itself. -->

- gingoa's **C3 Security = HIGH** (`docs/PRD.md`, `prd.yml`) makes the floor non-negotiable and **min-dimension scored** — breadth never lowers it.
- ② **production-minimum floor** emits security as *failing CI checks*, not docs (`ADR-0008/0014`): runtime env-var validation (boot fails on missing/invalid) + **secret-scan (gitleaks)** + **dependency audit** + **pinned GH Actions (SHA)** + **least-privilege CI token permissions** + `.github/dependabot.yml`. These are hard-blocking — **ADR-0008** (hard-blocking production floor).
- **Auth + risk zones are blocked or expert-mode-gated** for non-engineers — **ADR-0012** (risk-zone block / expert-mode), **ADR-0009** (archetype). Custom/hand-rolled auth is not on the paved road.
- **Supply chain is gingoa's live risk** (it ships a plugin + npm package, `prd.yml §risk_zones`): so L3 mandates pinned actions, least-priv CI, dep audit at ②; SBOM/provenance/signed-releases are *additional* at ④ (the census-confirmed gap, Signed-Releases 1.2/10).
- **Narrative artifacts stay local** — gingoa's own threat-model / secret-flow narrative is 🔒 (gitignored, like `docs/adr/*`), per the publish split; `SECURITY.md` (🌐) ships as the public VDP channel.
- The census directly **back-grounds gingoa's thesis**: because pinning (3.1/10), token hardening (26%), and enforced review (41%) are rare in the wild, a non-engineer harness must *install* them by default — the whole reason C3 is HIGH.

## `.scratch/research/corpus/aspects/10-supply-chain-security/10-supply-chain-security--overview.md`

- Former `gingoa_applied`: `"docs/prd.yml"`

## Implications for gingoa

gingoa applies this aspect to itself — see the shipped **`security.yml`/`dependabot.yml`** (Pinned GH Actions (SHA), Least-privilege CI `permissions:`, dependency audit + `.github/dependabot.yml`) and **`docs/PRD.md` C3 "Security HIGH"** (L3 production-floor: secret-scan · pinned Actions · least-priv token perms · dep audit · supply-chain gates). The PRD trips `supply_chain_distribution: true`, mandating the full hardening set.

How the harness enforces/scaffolds it:
- **②-time scaffold (default-on):** lockfile + runtime pin in the core trio; `.github/dependabot.yml`; a CI workflow that ships **SHA-pinned Actions** and **`permissions:` scoped read-by-default**; secret-scan + `*-audit` step. These are the rare-but-default safety rails the census says won't appear on their own (Pinned-Deps 2.4, Token-Perms 2.6).
- **Production-floor gate (ADR-0008, hard-blocking):** the floor fails the build if the CI workflow uses tag-pinned Actions or grants blanket token write — turning the [census] gap into an enforced rung rather than advice.
- **④-time (distribution archetype):** release automation emits an SBOM + signed provenance (Sigstore/`attest-build-provenance`); Signed-Releases (census 1.2/10) is exactly the gap gingoa's distribution archetype must not inherit.
- **Posture surfaced:** Scorecard provides the measurable, non-file baseline gingoa reports against, so "well built" includes a checkable supply-chain score rather than a vibe.

## `.scratch/research/corpus/aspects/11-maintainability-techdebt-refactoring/11-maintainability-techdebt-refactoring--overview.md`

- Former `gingoa_applied`: `"docs/prd.yml"`

## Implications for gingoa

- **Already applied — `docs/prd.yml` (C3 NFR `maintainability: priority high`).** gingoa's own contract names the maintainability target: "shared core → per-host adapters; typed composable modules; **every guardrail itself tested**" — i.e. modular decomposition + testability designed in, dogfooding this aspect. `gingoa_applied: docs/prd.yml`.
- **Debt register = ADRs + deferred-feature map.** gingoa logs deliberate-prudent debt as ADRs (e.g. ADR-0004 monorepo split *deferred*; ADR-0011 GUI *post-v1*) and `could`-tier items in the contract scope, not silent TODOs — the contract's two-axis discipline keeps shortcuts visible and rationale'd.
- **② production floor makes the ceilings executable.** ADR-0008's hard-blocking production floor projects per-commit complexity/format/lint budgets (biome) + test gates into the scaffolded CI (`.github/workflows/ci.yml` lint·typecheck·test·build), so maintainability erosion fails the build — the executable form of the C3 NFR, mirroring SonarQube's new-code-only philosophy.
- **Refactoring/legacy discipline is a harness skill, not advice.** gingoa ships `preparatory-refactoring` (separate refactor commit, all tests green) and TDD/characterization-test practice as first-class skills, encoding "make the change easy, then make it" and "pin behavior before you touch it" so the non-engineer's agent does it by default.
- **②/③ projection of architecture tests.** Where the chosen archetype has real module seams (monorepo dependency direction), ② seeds the corresponding fitness function (cross-link aspect 02); for gingoa's current cli single-package archetype these are lightweight (lint + typed boundaries) by design.
- **Mechanism-timing:** maintainability *targets* are set at ① (C3) and *enforced* continuously (every commit/PR) — it is the cross-cutting "all-stages" aspect, fired at each lifecycle gate.

## `.scratch/research/corpus/aspects/12-performance-scalability/12-performance-scalability--overview.md`

- Former `gingoa_applied`: `""`

## Implications for gingoa

gingoa **scaffolds** this for USER projects of the gated archetypes — at ③ it should help the user state explicit performance budgets (latency/throughput/resource ceilings, peak capacity) as part of the contract, and at ③→④ wire a perf/benchmark harness plus a perf-regression CI gate (load test for web/backend, micro-benchmark gate for library, frame/startup budgets for mobile, throughput/cost budgets for data-ml). It should default in caching guidance, statelessness for scale-out archetypes, and SRE overload patterns (load shedding, retry budgets) for backend services.

gingoa's **own** archetype is `cli` + `ai-harness` — neither is in `gated_archetypes`, so the aspect does **not** trigger for gingoa itself (a CLI has no peak-load capacity plan; the harness's cost is bounded by the host model/IO, not a request-throughput budget). Hence `gingoa_applied` is left empty: gingoa applies a light "don't be gratuitously slow / no obvious N+1" hygiene bar, not the full performance-efficiency + capacity-planning rig.

## `.scratch/research/corpus/aspects/13-api-interface-design/13-api-interface-design--overview.md`

- Former `gingoa_applied`: `""`

## Implications for gingoa

- gingoa **scaffolds this for USER projects of the gated archetypes**: for a `backend` user project, generate an OpenAPI (or AsyncAPI for event-driven) skeleton wired into CI with a spec-lint + breaking-change diff gate, idempotency-key guidance on mutating POSTs, and rate-limit/error-shape stubs. For a `library` user project, set up a public-surface + SemVer deprecation discipline. For a `cli` user project, scaffold POSIX flag parsing, categorized exit codes, stdout/stderr split, and a `--json` mode.
- **gingoa's own archetype is `cli` + `ai-harness`.** The `cli` facet *does* trigger the CLI-UX slice — the install/attach CLI should honor POSIX flags, meaningful exit codes, and a machine-readable (`--json`) mode as its interface contract. The HTTP/OpenAPI and AsyncAPI slices do **not** fire for gingoa itself (no served HTTP/event API).
- `gingoa_applied` left empty until gingoa's install-CLI interface contract is recorded under `docs/internal/` (e.g. the CLI's flag/exit-code contract).

## `.scratch/research/corpus/aspects/14-data-management-migrations/14-data-management-migrations--overview.md`

- Former `gingoa_applied`: `""`

## Implications for gingoa
<!-- How gingoa enforces / scaffolds this. Link gingoa_applied when applied to gingoa itself. -->

- **gingoa scaffolds this for USER projects of the gated archetypes (`backend`, `data-ml`).** When a user's project owns a datastore, gingoa should scaffold: a migrations directory wired to a versioned tool (Flyway/Alembic-class) with a schema-history table; a CI step that applies migrations to a throwaway DB to validate them; an expand-contract checklist surfaced at stage ③ for any breaking schema change; and a documented backup + PITR posture with explicit RPO/RTO and a rehearsed-restore expectation.
- **gingoa's own archetype (cli + ai-harness) does NOT trigger this aspect.** gingoa has no production persistent datastore of record — its "state" is source-controlled files and generated manifests, versioned by git rather than schema migrations. Therefore `gingoa_applied` stays empty: gingoa references this standard to build *for users*, but does not apply it to itself.

## `.scratch/research/corpus/aspects/15-accessibility-ux/15-accessibility-ux--overview.md`

- Former `gingoa_applied`: `""`

## Implications for gingoa

- **gingoa scaffolds this for USER projects of the gated archetypes only.** When a user's project is `web` or `mobile`, gingoa's ③-stage scaffolding should: set WCAG 2.2 **AA** as the contract target, wire a11y CI (`@axe-core/playwright` or `jest-axe`, `eslint-plugin-jsx-a11y`, Lighthouse a11y budget), seed an accessible-by-default component baseline (labeled inputs, focus-visible, contrast-checked tokens), and flag EN 301 549 / EAA legal exposure if the user targets the EU market.
- **gingoa's own archetype (cli + ai-harness) does NOT trigger this aspect** — there is no human-facing GUI surface, so WCAG/EN 301 549 do not apply to gingoa itself. CLI usability is handled elsewhere. Therefore `gingoa_applied` is left empty.

## `.scratch/research/corpus/aspects/16-privacy-data-protection/16-privacy-data-protection--overview.md`

- Former `gingoa_applied`: `""`

## Implications for gingoa

- gingoa **scaffolds** this aspect for **USER** projects whose archetype is `handles-user-data`: a data inventory / record-of-processing stub, DSAR (access/erasure/export) operations wired to the data model, consent-record schema, a DPIA checklist gate at stage ③, retention-TTL conventions, and a breach-runbook stub with the 72-hour clock. It surfaces the lawful-basis question during the ① contract interview so privacy is designed in, not retrofitted.
- gingoa's **own** archetype (**cli + ai-harness**) handles **no personal data** of end users — the gate does **not** fire for gingoa itself. `gingoa_applied` stays empty. (Caveat for later: if gingoa ever ships telemetry or stores user content, this aspect activates on gingoa and `gingoa_applied` should point at the relevant `docs/internal/` decision.)

## `.scratch/research/corpus/aspects/17-release-engineering/17-release-engineering--overview.md`

- Former `gingoa_applied`: `"docs/PRD.md"`

## Implications for gingoa

- **Release core is universal and scaffolded by default.** gingoa provisions SemVer tagging + a release-automation workflow (tagged GitHub Release + generated notes) + Conventional-Commits-driven changelog for **every** shipping archetype. This is already the gingoa contract: **US-5 Release/Ops** requires "SemVer + Conventional-Commits release automation, CHANGELOG, rollback path, supply-chain gates; DORA/SLO posture surfaced" (`docs/PRD.md` §C2). gingoa already dogfoods CC + Conventional-Commits PR titles (`CLAUDE.md` "Commits & PRs").
- **Operational half branches on archetype (contract C5).** The derived layer selects container/CD/IaC/observability-as-code only when the archetype runs a service — backend/monorepo get the full ops stack, library/cli get publish-only. This matches the census archetype split and avoids cargo-cult ops.
- **`[lit]` posture, not repo files, for the ops tail.** SLO definitions, runbooks, incident retros, on-call, DORA dashboards are *produced (literature) but not pushed to the public remote* — intrinsically off-repo and partly security-sensitive (publish-axis rule, `_schema.md` §4 (publish-axis)). observability-as-code (prometheus/otel config) ships as public config where archetype-relevant; **SLO targets / retros stay internal.**
- **Measurement target = DORA.** gingoa frames ④ quality against the Four Keys: release automation → deploy frequency (census proxy: weekly cadence), CI+tests → low change-failure rate, rollback path + observability → fast recovery. It instruments toward these without claiming to census attainment.
- **Rollback is a first-class gate.** A defined revert path (the `rollback`/`hotfix` skills) is required of every release, satisfying the contract's "rollback path" NFR and the DORA recovery lever.
- **Provenance + SRE artifact set (the ④ build-spec).** The full release+operate artifact checklist — the
  **supply-chain provenance half** (SBOM · SLSA provenance · Cosign signing · checksum manifest) this aspect
  is thin on, plus the **SRE/operate half** (SLO doc · error-budget policy · OTel three-pillars · burn-rate
  alerts · runbook-per-alert · blameless postmortem + action-item tracking · DORA instrumentation · vuln
  management) — is the ④ build-time spec: [`release-operate-artifact-checklist.md`](release-operate-artifact-checklist.md).
  It also grounds **aspect-18** (packaging/provenance) and **aspect-20** (operate) — the ④ items previously
  unbound to a mechanism.

## `.scratch/research/corpus/aspects/18-packaging-distribution/18-packaging-distribution--overview.md`

- Former `gingoa_applied`: `"docs/prd.yml"`

## Implications for gingoa
gingoa **applies this to itself** (`docs/prd.yml`): archetype = **cli single-package**, `distribution: [plugin-marketplace, npm-cli]`, `supply_chain_distribution: true` → an L3 supply-chain floor (pinned actions, least-priv CI, dep audit). It ships a Claude Code plugin (marketplace manifest) **and** an npm package (`bin: gingoa`, `pnpm-lock.yaml` committed). What gingoa scaffolds for users:
- **Release automation laid in ②, runs in ④:** SemVer + Conventional-Commits → auto changelog + tagged GitHub Release; emitted as a **release workflow + skill** (④ release).
- **Channel by archetype (C5 branch):** library → registry publish; cli → registry + binary (goreleaser/Homebrew/winget); service → container; mobile → app-store posture. The harness emits the matching publish workflow.
- **Provenance by default:** publish via OIDC/Trusted Publishing with Sigstore-signed provenance (SLSA L2+) — closing the 1.2%-census gap as a craft default, not an opt-in.
- **Outward-publish gate:** gingoa *prepares everything* (version, changelog, tag, rollback path) but the actual outward publish/deploy **requires explicit owner confirmation** — emitted as a **hook**. Publish-axis: local/team by default; pushing to a public registry is a deliberate act.

## `.scratch/research/corpus/aspects/19-observability-telemetry/19-observability-telemetry--overview.md`

- Former `gingoa_applied`: `""`

## Implications for gingoa

- **Gate by archetype, never universal.** gingoa activates this aspect only for service archetypes (backend/web/monorepo/data-ml) via the contract's service axis (C5-style branch); for library/cli it is a no-op — matching the census tail, not cargo-culting.
- **Scaffold observability-as-code, prescribe posture.** When gated, gingoa scaffolds the *public* layer (OTel SDK wiring + OTLP export, golden-signal/RED dashboards-as-code, Prometheus/SLO yaml stubs) and supplies *guidance + runbook/SLO templates* for the off-repo half framed by DORA Four Keys + Google SRE — the irreducible "you now have a service to *operate*" advisory layer for a non-engineer.
- **Honest evidence.** Because adoption is a sparse, off-repo tail, gingoa treats the do-it standard as `[lit]` (senior practice) while the publish decision uses the `[census]`/survey numbers — the two-axis discipline (`_schema.md §4`).
- **gingoa-applied:** none yet — gingoa is an early-stage harness/CLI (C5=cli, C6=TS) with no running service of its own, so no observability ADR exists. Leave `gingoa_applied` empty until a service component lands.

## `.scratch/research/corpus/aspects/20-operations-incident-reliability/20-operations-incident-reliability--overview.md`

- Former `gingoa_applied`: `"docs/PRD.md"`

## Implications for gingoa

- gingoa's own ④ contract already encodes this: **US-5 Release/Ops** provisions release + ops and surfaces **"DORA/SLO posture; outward publish requires explicit confirmation"** (`docs/PRD.md`) — matching the two-axis rule (build the posture; gate the public remote).
- **Scaffold (file-able):** for service archetypes, gingoa emits observability-as-code stubs, an incident-runbook template, a postmortem template, and DORA-key instrumentation hooks wired from release automation + CI. These are repo files for backend/monorepo/web; **omitted for library/cli** (archetype branch, contract field C5).
- **Surface, don't fabricate (the [lit] posture, tier C):** gingoa cannot create live SLOs/on-call/MTTR as repo files. For a non-engineer it raises the irreducible advisory: *"you now have a service to **operate**"* — defining SLO/error-budget, on-call, DR (RTO/RPO), and incident/postmortem flow per Google SRE + DORA + NIST 800-34, with SLO targets and retros kept **internal** (off the public remote).
- **Reliability is gingoa's own HIGH NFR** (`prd.yml` reliability: idempotent install, lossless uninstall, fail-closed render) — gingoa applies the same min-dimension reliability bar to itself that it provisions for users.
- **Min-dimension enforcement:** every covered archetype×ecosystem must clear the reliability floor; operations posture is the ④ stage-gate output, looping back to ③.

## `.scratch/research/corpus/aspects/21-economics-cost-sustainability/21-economics-cost-sustainability--overview.md`

- Former `gingoa_applied`: `""`

## Implications for gingoa

- gingoa **scaffolds this for USER projects only when the gate fires.** When the ① contract declares a `cloud` (metered-deploy) archetype, gingoa wires the FinOps starter set: a resource-tagging convention in the IaC scaffold, a budget + anomaly-alert default, and a `cost-per-unit` placeholder in the ops doc — Inform-phase ("Crawl") only, not a full FinOps practice.
- When the contract declares `published` **at org scale** with a sustainability/disclosure requirement, gingoa offers (opt-in) an SCI measurement stub (`SCI = (O+M)/R` template) and a pointer to ESRS/CSRD obligations — it does not auto-enable them.
- **SWEBOK-KA15** informs gingoa's own blueprint/spec gates: every build-vs-buy default it proposes should carry a one-line ROI/rationale (why this dependency, what it saves), per KA15's decision-record discipline — this is reference guidance, applied generically.
- **gingoa's own archetype (cli + ai-harness) does NOT trigger this aspect.** gingoa is not a metered cloud deployment and not an org-scale published operator, so neither the FinOps cost loop nor the SCI/CSRD disclosure loop applies to gingoa itself. `gingoa_applied` left empty.

## `.scratch/research/corpus/aspects/22-documentation-knowledge/22-documentation-knowledge--overview.md`

- Former `gingoa_applied`: `"docs/PRD.md"`

## Implications for gingoa

- **Reader-intent split is built into the corpus itself:** `_schema.md` mandates **one doc = one purpose** (Diátaxis discipline) — gingoa dogfoods this aspect in its own research corpus.
- **Two-doc-axis separation:** the general **standard** lives in this corpus; gingoa's **applied** decisions live in the tracked `docs/` (`PRD.md`, `prd.yml`, `docs/adr/`; the threat-model stays gitignored in `docs/internal/`). The PRD is gingoa's ① output that records *what + quality bar + archetype/stack + ADR log* — see `gingoa_applied`.
- **Scaffold the standard doc set:** the blueprint/foundation skill should emit README + LICENSE + CONTRIBUTING + SECURITY.md + CHANGELOG (Keep a Changelog) + issue/PR templates by default; CODEOWNERS for monorepo/multi-team; CODE_OF_CONDUCT for public OSS.
- **Scaffold-provenance manifest rides the doc set, not a new file (the *transparency floor*).** When gingoa auto-configures a project, *what it set up + why + how to change/off* is disclosed through the **existing doc set**, never a novel top-level file: **machine/update state → `.copier-answers.yml`** (the ownership baseline, aspect-04); **the human "what/why/off-switch" manifest → CONTRIBUTING.md** (the onboarding runbook, aspect-23); **README → a one-line pointer + quickstart** (its census role is orientation ≈100%, not a config dump). A dedicated **`SCAFFOLD.md` is rejected** — absent from the near-universal root roster (README/LICENSE/CONTRIBUTING/SECURITY/CHANGELOG/CoC/CODEOWNERS), it is nonstandard root clutter that competes with README; a **`.gingoa/` dotdir is rejected** — machine provenance already lives in `.copier-answers.yml`, so a 2nd tool dir fragments state. Delivery is **progressive disclosure, not a blocking confirm** (available-but-not-required, per the CNCF maturity read in aspect-23). This grounds the tier model's transparency floor — `three-tier-ledger.md` D7: *no auto-set item is invisible; tier controls loudness-of-why, not visibility.*
- **ADRs as a first-class habit:** gingoa records significant decisions as MADR records under `docs/adr/` (it already maintains a `docs/adr/` dir) — keep local by default, publish opt-in.
- **Generated reference + freshness in CI:** wire link-check + doc-build into the paved-road CI; generate API reference from OpenAPI/typed schema, never hand-write it.
- **De-jargon CI gate (public/internal split):** gingoa keeps internal working-notes local + a clean public face, so the paved road emits a **content gate** that fails CI when internal jargon leaks into public files — the *executable* form of the launch de-jargon gate (ADR-0008/0014 "a passing check, not a doc"). Start = custom grep job (no new dep); upgrade = Vale `reject.txt`. Scope to public dirs, excluding gitignored `docs/internal/`. See [`content-ci-linting-and-jargon-gate.md`](content-ci-linting-and-jargon-gate.md).
- **Knowledge management:** plans/specs kept as historical record (the cleanup skill deletes volatile plan files but **keeps the spec**), so the *why* survives — a bus-factor safeguard.

## `.scratch/research/corpus/aspects/22-documentation-knowledge/content-ci-linting-and-jargon-gate.md`

## gingoa application
Add a **de-jargon CI gate** to the ② floor (extends `aspects/04-…/foundation-floor-artifact-checklist.md`):
a job that scans the **public-facing tree** for the internal-jargon blocklist (`R1`/`R2`, `build-step`,
`aspect-NN`, `ADR-NNNN` internal refs, `.scratch`, `docs/internal`, `claudeck`, cryptic `①②③④`, `FEATURE-MAP`,
`FOUNDATION-PLAN`) and **fails on a leak** — the *executable* form of the launch de-jargon gate, matching
gingoa's "floor = a passing check, not a doc" principle (ADR-0008/0014). **Start = custom grep job** (no new
dependency, fits the TS/pnpm + grep-able floor); **upgrade path = Vale `reject.txt`** if/when public prose
linting is wanted. Scope it to public files only (root docs + `docs/` public dirs), excluding the gitignored
`docs/internal/` working-notes.

## `.scratch/research/corpus/aspects/23-developer-experience/23-developer-experience--overview.md`

- Former `gingoa_applied`: `""`

## Implications for gingoa

- **gingoa scaffolds this for USER projects.** The blueprint/scaffold should always emit a day-one onboarding runbook (`CONTRIBUTING.md` / dev-setup), a **one-command bootstrap**, and a working golden path — the walking-skeleton that runs green at commit-zero *is* the time-to-first-PR guarantee. Copier-based templates are gingoa's golden-path delivery mechanism.
- **DX metrics as guidance, not gates.** For most user archetypes gingoa surfaces SPACE/DORA as advisory framing; it does not impose telemetry on a solo project.
- **IDP is gated up, not down.** gingoa should only introduce platform-engineering / IDP scaffolding when a user project is explicitly multi-team — defaulting to a runbook + scaffolder for everyone else.
- **gingoa's own archetype (cli + ai-harness)** sits at the small end: it needs the onboarding runbook + one-command bootstrap + golden-path scaffolding, but **not** an internal developer platform. The platform-engineering sub-aspect does **not** fire for gingoa itself, so `gingoa_applied` is left empty here; gingoa's applied onboarding decisions live in `docs/internal/` once authored.

## `.scratch/research/corpus/aspects/24-governance-collaboration-compliance/24-governance-collaboration-compliance--overview.md`

- Former `gingoa_applied`: `"docs/PRD.md"`

## Implications for gingoa

Applied to gingoa itself in **`docs/PRD.md`** (C7 decisions → ADRs; C8 constraints; §9 contract→② handoff):

- **Decision rights** — gingoa records its own real decisions as **MADR ADRs** at `docs/adr/` (0001–0012). Per the publish-axis they are kept **local via file-level `.gitignore`**, opt-in to publish — directly applying the census 2–4% / not-public-default finding to itself.
- **Enforced review** — gingoa's own process is **PR-first, squash-merge, Conventional-Commits PR title (enforced by the `pr-title` workflow), never `--no-verify`**, with CI gating lint/typecheck/test/build on every push (the branch-protection + code-review controls the census shows are weakest in the wild).
- **Collaboration file set** — the harness scaffolds CONTRIBUTING / SECURITY / CODE_OF_CONDUCT / CODEOWNERS / issue+PR templates as the **archetype-conditional governance bundle** (CoC = public-gated, CODEOWNERS = monorepo/multi-team-gated), keyed off the contract's audience field — so a non-engineer gets the senior collaboration posture without knowing to ask.
- **Compliance/IP** — LICENSE (MIT, public) settled day-one; the production-floor (ADR-0008) wires supply-chain evidence (pinned GH Actions, least-privilege CI token, secret-scan, dependency audit) into CI, making the audit trail a by-product of normal flow.
- **Org structure** — gingoa is `cli` single-package / solo+AI today (ADR-0004 monorepo split deferred); Team Topologies is dormant but the boundary artifact (CODEOWNERS) is opt-in-ready for when a 2nd package/team lands.
- **Curation governance** — ADR-0010 (open marketplace + curation review) and ADR-0012 (risk-zone block + expert-mode gate) are gingoa's *product-level* governance decisions, themselves recorded as ADRs — dogfooding this aspect.
- **Internal/published boundary (self-contained remote artifacts)** — gingoa publishes its planning docs (PRD, ADRs) to tracked `docs/` while keeping its threat-model + research corpus gitignored (`docs/internal/`, `docs/research/`), and writes its remote issues / PRs / commit messages + the issue/PR templates **self-contained** — describing the change/product without citing those local-only artifacts or internal lifecycle/pipeline jargon (a PR reader with only the remote can follow it). Dogfooded at build-step 1: issue #1 + PR #2 were rewritten to drop ADR/corpus/plan references, and the issue/PR templates were made generic. The internal *thinking* is referenced only from other internal docs.

## `.scratch/research/corpus/aspects/25-licensing-foss-compliance/25-licensing-foss-compliance--overview.md`

- Former `gingoa_applied`: `"docs/PRD.md"`

## Implications for gingoa

- gingoa scaffolds **a root `LICENSE` as a day-one file** for every project it creates — matching the ~96–99% census floor, this is non-negotiable table stakes, not an option.
- The **outbound license is an explicit ① contract decision**, surfaced in the blueprint interview (permissive vs. copyleft, patent-grant need) and recorded in `docs/PRD.md` — never silently defaulted. The harness explains the tradeoff in plain terms to the non-engineer (the "craft gap" it fills).
- gingoa's paved-road CI should include an **inbound dependency-license scan** (stack-appropriate: `license-checker`/`pip-licenses`/`cargo-deny`/`go-licenses`) gating PRs against an allow/deny policy, plus optional SBOM emission — the senior-tier delta above the LICENSE-file floor.
- **Contribution gating:** default to **DCO sign-off** (lightweight, community-friendly, matches gingoa's Conventional-Commits + never-`--no-verify` posture); reserve a CLA only if a project needs relicensing/dual-license rights.
- **SPDX identifier in the package manifest** is scaffolded; full **REUSE per-file headers** offered as opt-in polish, not forced.
- **gingoa itself applies this:** ships **MIT** (`LICENSE`, `Copyright (c) 2026 coolbress`), declared in `docs/PRD.md §License` and the C7/C8 file map (`LICENSE` MIT, public-facing). → `gingoa_applied: docs/PRD.md`.

## `.scratch/research/corpus/aspects/26-mlops-ml-lifecycle/26-mlops-ml-lifecycle--overview.md`

- Former `gingoa_applied`: `""`

## Implications for gingoa

- gingoa **scaffolds this for USER projects of the `data-ml` archetype** — when the contract selects `data-ml`, gingoa should provision the lifecycle backbone (data versioning, experiment tracking, a model registry, CI/CD/CT pipeline scaffolding, and drift-monitoring hooks) and surface the maturity-level choice (L0→L2) so the non-engineer isn't silently dropped at L0.
- gingoa should treat the **EU-AI-Act high-risk controls as a conditional gate** layered on `data-ml`: when the user's project is regulated, the scaffold must add data-governance evidence, event logging, technical docs, and human-oversight hooks as first-class acceptance criteria.
- **gingoa's own archetype is `cli` + `ai-harness`** — it orchestrates LLM-host agents but does **not** train, version, or continuously retrain models, so this gated aspect does **not** fire for gingoa itself. `gingoa_applied` stays empty.
- The `ml-ops.org` Stack Canvas (11 blocks) is the natural checklist gingoa can project into a `data-ml` foundation plan, one block per scaffolded concern.

## `.scratch/research/corpus/aspects/27-ai-harness-archetype/27-ai-harness-archetype--overview.md`

- Former `gingoa_applied`: `"docs/adr/0009-ai-harness-archetype.md"`

## Implications for gingoa

gingoa **is** an AI-harness and dogfoods this aspect first (cli + harness, an **application harness**):

- gingoa already keeps the full L0 floor (② foundation) — confirmed correct by canonical APP harnesses; it ships the capability layer (adapters/, marketplace.json, gingoa-ping/SKILL.md) and treats the harness as a **first-class 8th archetype / L2′ module** that stage ② can emit. See `docs/adr/0009-ai-harness-archetype.md`.
- **Cross-host adapters** are core architecture (CLAUDE.md): a shared core projected into Claude-Code + Codex adapters via an install CLI; the config/manifest is JSON-Schema'd (census 64%) so the cross-host contract is machine-checkable.
- **Extensibility** = open marketplace + curation gate (ADR-0010): third-party skills/archetypes extend breadth while the review holds the floor.
- **Control-tower GUI** = local web app over MCP (ADR-0011), riding the MCP surface harnesses already expose — post-v1.
- gingoa enforces this by scaffolding the layer (skills/commands/hooks/prompts/mcp/manifest+schema/examples/templates/agent-md) as the harness archetype's emit target, and by gating every emitted harness on the same four CI checks (lint/typecheck/test/build) as any application archetype.

## `.scratch/research/corpus/aspects/27-ai-harness-archetype/multi-agent-orchestration-standard.md`

## Implications for gingoa
- **gingoa's own dev-loop already IS orchestrator-worker** (ADR-0013 row 28 `S(lead → sub-agent delegation, plan-as-artifact)`): planner → implementer → adversarial reviewers, each context-isolated with handoff artifacts (plan / diff / verdict). This research is the external grounding + boundary conditions for that, not a new direction.
- **The adversarial reviewer = the generator-verifier pattern** — Cognition's #1 endorsed production pattern. It is deliberately **read-only, returns findings, does not write**; the lead remains the single writer. A fresh/limited-context verifier is *empirically better* at breaking claims than the model that authored the artifact.
- **Reserve dispatch for high-value gates, not routine steps.** The 15× cost means multi-agent is for the elicit skeptic / architecture review / release audit — not every incremental edit. Routine writing stays single-threaded (ADR-0013 locus).
- **Deterministic core is the coordination substrate, not another agent.** gingoa keeps the *enforcement* (gates, lock, seal) in model-call-free `core`/CLI — host-neutral — so a dispatched worker's *judgment* is host-side while its *consequences* are enforced identically on both hosts. This sidesteps the coordination-in-real-time weakness the literature flags.
- **Cross-host delivery:** gingoa ships the *prompt artifact* (skill / agent definition); each host dispatches it (CC subagent; Codex subagent since 2026-06, or inline). Parity is preserved by keeping the shipped unit host-neutral and the enforcement in core — **not** by betting on either host's dispatch primitive.

## `.scratch/research/corpus/aspects/28-implementation-process-workflow/28-implementation-process-workflow--overview.md`

- Former `gingoa_applied`: `"docs/adr/0013-operating-model.md"`

## Implications for gingoa

gingoa's ③ implementation is driven by **claudeck v1's routing** (the live `~/.claude/{CLAUDE.md, hooks/routing-summary.md, docs/workflows, scripts/locate-ladder.sh}`), adopted because it is well-built — and now confirmed **substantially [lit]-validated by this aspect**, often a point-for-point match:

| claudeck routing element | This aspect's grounding |
|---|---|
| Tier 0/1/2/3 differentiated ceremony | process tailoring · ITIL tiers · Meta RADAR |
| plan-file-first (write + approve before code) | plan-as-artifact (Plan-and-Solve) |
| lead-coordinator + worktree subagents + cherry-pick | CAID · Anthropic multi-agent · context isolation |
| lead never writes production code (lean context) | Lost-in-the-Middle |
| TDD-always + Verify + deterministic pre-pass | objective-signal verification · Reflexion |
| 3-failure circuit-breaker + review-history oscillation check | MAST / AgentFixer failure-handling |
| Execution Confirmation Protocol Gate 3 (irreversible/outward → re-confirm) | autonomy-levels · write-staging · Model Spec |
| review-round R1 (Claude/Fable) + R2 (Codex), cross-vendor | PoLL diverse-jury · self-preference bias |
| R2 confirm/adjust/**drop** + evidence-bar (HIGH = code excerpt) | agreeableness-bias mitigation · cross-context review |

### Residual gaps in the adopted ③ driver (claudeck v1) vs this standard — and their deferral

Following claudeck v1 *perfectly* still leaves a few gaps vs THIS aspect (claudeck is the applied form, not a
1:1 implementation). Classify each by whether it can touch the **output** (the built artifact) or only the
**process** — only output-touching gaps are urgent:

| Residual gap (claudeck v1 vs aspect-28) | Output or process? | Disposition |
|---|---|---|
| **Tier classification keys on task TYPE** (verb triggers), not explicit **risk signals** (blast-radius / novelty / criticality / reversibility — RADAR-style) → a risky one-liner can be under-tiered | 🟡 borderline output (edge case) | **mitigated** by Rule 5b (respecting-constraints: arch-boundary + CLAUDE.md CRITICAL) + conservative manual escalation → safe to defer |
| **Coordinator context-budget not explicit** (no "externalize completed-step summaries" rule — Lost-in-the-Middle) | ⚪ process only | defer |
| **Review = vendor-diverse but not lens/detection-pattern-diverse** (CodeX-Verify: diverse detection patterns catch more) | ⚪ ~process (marginal catch-rate) | defer |

**Deferral rule (a gingoa operating decision):** an output-neutral (or already-mitigated) process gap is NOT
retrofitted onto the gingoa being built — it is deferred to gingoa's OWN ③-routing build, where gingoa
**evolves claudeck v1** (risk-signal tiering · explicit coordinator context-budget · lens-diverse review).
The current gingoa's output is unharmed by these gaps (it was built conservatively/thoroughly), so deferral
costs nothing. These three are the **ADR/backlog seeds for gingoa's ③ routing skill** (gingoa-supersedes-its-
predecessor). Distinguish from **builder-execution gaps** (a builder not following claudeck — closed by
following it) and **output gaps** (none observed in the current build).

gingoa's operating-model ADRs (0013 operating-model, 0014 evidence-contract-no-theater, 0015 module-boundaries)
are the applied decisions; this aspect is their general grounding. Raw research log + all citations:
[`research-log.md`](research-log.md) (co-located).

**Per-feature artifact DoD (③ output checklist, survey 2026-06-26).** Beyond the routing/process above, a
single feature's build must YIELD the standard artifact set (Spec Kit/Kiro · GitHub Flow · SWEBOK Construction/
Testing · Google code-review): tracking issue → JIT feature `spec.md` → design/plan → task breakdown → feature
branch + Conventional Commits → **failing-tests-first (TDD)** → production code → test suite → **PR w/ structured
description** → **CI green** (lint/type/test/build) → **code-review record + approval** → ADR(s) for mid-build
decisions. Three items a thin loop skips and gingoa's DoD must include: a **CHANGELOG `[Unreleased]` entry**
(written while context is fresh), a **docs/README update** (when behavior/CLI/API changes), and — *conditional*
— a **DB migration script** (schema change, aspect-14) + an **API/contract update** (public-surface change,
aspect-13). gingoa is already AHEAD on review (2-vendor adversarial vs single-LGTM). [lit]

