---
id: aspect-03-dev-environment
title: "Dev Environment & Local Setup"
group: "F — Foundation & Build"
kind: universal
gated_archetypes: []
cross_cutting: false
lifecycle_stages: ["②"]
anchors: ["SWEBOK-KA4", "12-Factor-I/II/X", "devcontainer"]
evidence_track: census+lit
status: review-needed
last_updated: "2026-06-25"
sources:
  - "https://12factor.net/"
  - "https://containers.dev/"
  - "https://itrevolution.com/product/accelerate/"
  - "https://scorecard.dev/"
  - "https://docs.npmjs.com/cli/v11/configuring-npm/package-lock-json/"
  - "https://blog.rust-lang.org/2023/08/29/committing-lockfiles/"
  - "https://editorconfig.org/"
claim: "A senior local setup is reproducible by construction — runtime + package-manager pinned, lockfile committed, dev/prod parity kept (12-Factor), and a one-command bootstrap — so any contributor (or AI agent) gets a byte-identical toolchain without manual drift."
maps_from: ["census-data/census-dev-environment"]
---

> **Standard (claim):** A senior local setup is reproducible by construction — runtime + package-manager pinned, lockfile committed, dev/prod parity kept (12-Factor), and a one-command bootstrap — so any contributor (or AI agent) gets a byte-identical toolchain without manual drift.
> **Evidence:** census+lit (429/938-repo census + 12-Factor / devcontainer / OpenSSF) · **Confidence:** high · **Kind:** universal · **Stage:** ②

**Seed sub-aspects:** `reproducible local env (devcontainer/mise/Nix)` · `editorconfig` · `dev/prod parity & environment management` · `local backing services` · `cross-platform`

## What professional engineers do
<!-- The reference: how senior engineers handle Dev Environment & Local Setup. One pass per seed sub-aspect, evidence-tagged. -->

- **Pin the toolchain to data, not to "whatever's installed."** Commit a runtime pin (`.nvmrc`/`.tool-versions`/`rust-toolchain.toml`/`go` directive) **and** a package-manager pin (Corepack `packageManager` field, `uv`, pinned `cargo`) so the version is declarative and machine-resolvable. `[lit]` 12-Factor II (explicitly declare and isolate dependencies). Census shows this is *rare in the wild* (runtime_pin 24%, pkg_manager_pin 19%) yet rising (runtime_pin weighted 28% / young 30%) — a deliberate ⚖️ uplift above census because a non-engineer cannot diagnose or recover from version drift. `[census][lit]`
- **Commit the lockfile.** Exact transitive versions are reproducibility, not clutter: npm "strongly recommends" committing `package-lock.json`; Cargo (2023) reversed its guidance to "commit `Cargo.lock` even for libraries." Census: lockfile 57% → **61% weighted** (now a majority among recent repos). `[lit][census]`
- **One-command bootstrap + a task runner.** A new clone reaches a working state via a single entry point (`make`, `just`, `pnpm install && pnpm <task>`, `mise install`) rather than a prose checklist. Task runner present in ~59–66% of repos. The bootstrap installs the pinned toolchain, restores from lockfile, and exposes the same `lint/typecheck/test/build` verbs CI runs — local and CI execute *identical* commands. `[census][lit Accelerate]`
- **Reproducible env, escalating by need.** Tier the mechanism to the project: (1) **pins + lockfile + task runner** = the universal floor (works everywhere, zero daemon); (2) **devcontainer** (`devcontainer.json`, the open Dev Containers spec, Microsoft-maintained) for team onboarding / IDE-uniform setup; (3) **Nix/mise** for hermetic, cross-language pinning when the floor isn't enough. Devcontainer adoption is flat at 21% — an onboarding convenience, **not** a universal requirement. `[lit devcontainer][census]`
- **Dev/prod parity & environment config.** Keep environments as similar as possible and read config from the environment, never hard-coded. Ship a committed `.env.example` (real values gitignored) documenting every required variable; load via a `.env` loader. Census: env_example 18% → **36% weighted** (↑+18, the single biggest trend mover) — modern apps externalize config. `[lit 12-Factor I (codebase) / III (config) / X (dev-prod parity)][census]`
- **Local backing services as attached resources.** Databases/queues/caches run as swappable attached resources (12-Factor IV), typically via `docker-compose` for local dev to mirror prod topology. Conditional on archetype: Dockerfile 46% → **58% weighted** overall, **79%** for backend-service. `[lit 12-Factor IV][census]`
- **`.editorconfig` — demoted, not gone.** A cross-editor whitespace/charset baseline. Census shows it *declining* (39% → **19% weighted**, ↓−20) as modern formatters (biome/ruff/prettier) absorb the role — so it's a 🟨 nicety, no longer core. Editor recommendations (`.vscode/extensions.json`) ~21–24%. `[census]`
- **Cross-platform hygiene.** A committed `.gitattributes` normalizes line endings (`* text=auto`) so Windows/macOS/Linux contributors don't churn CRLF; gitattributes ~52–58%. Avoid OS-specific assumptions in the bootstrap (no bash-only scripts where Windows contributors exist). `[census]`

## Evidence (lit + census)
<!-- [lit] named papers/standards (cite URL) · [census] repo-survey numbers. Track: census+lit. -->

- `[lit]` **The Twelve-Factor App** (Wiggins 2011) — I codebase, II dependencies (explicit/isolated → pin), III config-in-env, X dev/prod parity, IV backing services as attached resources. https://12factor.net/
- `[lit]` **Dev Containers spec** (`devcontainer.json`, open standard, Microsoft) — container-as-coding-environment, consistent across team + CI. https://containers.dev/
- `[lit]` **Accelerate** (Forsgren/Humble/Kim 2018) — local = CI parity, one-command reproducibility as a delivery-performance enabler. https://itrevolution.com/product/accelerate/
- `[lit, empirical]` **OpenSSF Scorecard / Pinned-Dependencies** — independently confirms pinning is weak in the wild (Pinned-Deps mean **3.1/10**, weighted 3.8; **27% uniform / 37% weighted** strong · n=429), reinforcing the ⚖️ uplift. https://scorecard.dev/
- `[lit]` npm `package-lock.json` ("strongly recommended" to commit) https://docs.npmjs.com/cli/v11/configuring-npm/package-lock-json/ · Cargo lockfiles 2023 (commit even for libraries) https://blog.rust-lang.org/2023/08/29/committing-lockfiles/ · EditorConfig https://editorconfig.org/
- `[census]` (429 software repos; weighted `w=0.5^(age/2yr)`; young = post-2021 n=163): runtime_pin **24/28/30** · pkg_manager_pin **19/18/20** · lockfile **57/61/61** · env_example **18/36/37** (↑+18) · dockerfile **46/58/62** (↑+12) · editorconfig **39/19/21** (↓−20) · task_runner **66/59/56** · devcontainer **21/21/22** · editor_recommendations **24/21/25** · gitattributes **58/52/54**.
- `[census]` archetype-conditional Dockerfile: backend-service **79%**, data-ml 57%, monorepo/web 52–53%; env_example: web-app **45%**, backend 24%, library 8%; devcontainer: mobile **0%**, data-ml 4%.

## Archetype variations
<!-- How this differs across archetypes. -->

- **Universal floor (all archetypes):** runtime + package-manager pin · committed lockfile · task runner with CI-identical verbs · `.gitattributes`. No archetype is exempt.
- **backend-service / data-ml / web-app:** Dockerfile + `docker-compose` for local backing services (Dockerfile 79/57/52%); web-app and backend ship `.env.example` (45% / 24%). These three benefit most from devcontainer/compose parity.
- **library / cli:** lighter — no backing services, no `.env`. Library lockfile guidance is 🟨 (the historical npm/Cargo debate; modern stance = commit anyway). Cli rarely containerizes (16%).
- **mobile:** platform SDK/build env dominates; devcontainer is effectively N/A (0% in census), `.env.example` rare (9%).
- **monorepo:** workspace-aware env (`pnpm-workspace`/turbo/nx) + highest devcontainer/onboarding tooling (31%) because contributor count is the driver.
- No *gated* archetypes here — this aspect is `universal`; only the *mechanism intensity* (compose, devcontainer) scales with archetype.

## Tradeoffs / what's ruled out

- **Devcontainer/Nix as a mandate — ruled out.** 21% flat adoption + heavy daemon/learning cost; mandating it would gold-plate a solo or cli project. Kept as opt-in for team/onboarding-heavy or polyglot repos. `[census]`
- **`.editorconfig` in the core — ruled out (demoted to 🟨).** Declining (19% weighted); modern formatters subsume it. Keep only as a cheap cross-editor courtesy.
- **Pre-commit hooks as the reproducibility/quality gate — ruled out as the *gate*.** Locally bypassable (`--no-verify`); the real gate is CI (T3). Hooks are an optional fast-feedback helper, not the enforcement boundary. `[lit Accelerate][census precommit 33%]`
- **"Works on my machine" prose READMEs — ruled out.** Manual setup steps drift and silently break; replaced by declarative pins + one-command bootstrap.
- **Pinning tension (T2):** census says pins are *rare* (19–24%) — but literature (12-Factor II, OpenSSF) + the non-engineer recovery argument override popularity. Held above census, by design, not taste.

## Sources
- https://12factor.net/ — The Twelve-Factor App (I/II/III/IV/X)
- https://containers.dev/ — Development Containers specification
- https://itrevolution.com/product/accelerate/ — Accelerate (Forsgren/Humble/Kim 2018)
- https://scorecard.dev/ — OpenSSF Scorecard (Pinned-Dependencies)
- https://docs.npmjs.com/cli/v11/configuring-npm/package-lock-json/ — npm lockfile guidance
- https://blog.rust-lang.org/2023/08/29/committing-lockfiles/ — Cargo lockfile guidance (2023)
- https://editorconfig.org/ — EditorConfig

## Sub-documents
- [`reproducible-environment--facts-2026-08.md`](reproducible-environment--facts-2026-08.md) — *research-log (ko)* — 2026-08 facts-only pass (R2-1): devcontainer 스펙 · 런타임 버전 고정(mise/asdf) · lockfile · dev/prod 패리티. **12-Factor는 표준 기관 산출물이 아닌 저자의 방법론**임을 각 인용에 표기.
