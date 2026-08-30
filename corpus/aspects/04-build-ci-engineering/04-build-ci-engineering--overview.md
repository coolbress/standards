---
id: aspect-04-build-ci-engineering
title: "Build & CI Engineering"
group: "F — Foundation & Build"
kind: universal
gated_archetypes: []
cross_cutting: true
lifecycle_stages: ["②"]
anchors: ["SWEBOK-KA4", "SWEBOK-KA6", "Accelerate", "SLSA-reproducible"]
evidence_track: census+lit
status: review-needed
last_updated: "2026-07-05"
sources:
  - "https://itrevolution.com/product/accelerate/"
  - "https://12factor.net/"
  - "https://scorecard.dev/"
  - "https://slsa.dev/spec/v1.2/build-requirements"
  - "https://slsa.dev/spec/v1.2/source-requirements"
  - "https://docs.npmjs.com/cli/v11/configuring-npm/package-lock-json/"
  - "https://blog.rust-lang.org/2023/08/29/committing-lockfiles/"
  - "https://reproducible-builds.org/docs/definition/"
  - "https://turborepo.com/docs/crafting-your-repository/running-tasks"
  - "https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows"
claim: "A senior-grade project ships an unbypassable CI gate (lint·typecheck·test·build) that is the real merge gate — not local hooks — with pinned runtime/PM, a committed lockfile, and (in monorepos) an affected-graph build, so every change is validated reproducibly before reaching main."
maps_from: ["census-data/census-dev-environment"]
census_todo: "Deferred — needs a targeted workflow-content/topology survey; the existing census records hold derived flags only (not tree contents), so this metric (e.g. cache-key strategy, affected-graph wiring, hermetic-build posture) is not offline-derivable. Low priority."
---

> **Standard (claim):** _A senior-grade project ships an unbypassable CI gate (lint·typecheck·test·build) as the real merge gate — not local hooks — with pinned runtime/PM, a committed lockfile, and (in monorepos) affected-graph builds, validating every change reproducibly before main._
> **Evidence:** CI 92–93% `[census]` + Accelerate/OpenSSF `[lit]` · **Confidence:** high (universal core) · **Kind:** universal · cross-cutting · **Stage:** ②

**Seed sub-aspects:** `CI pipeline (lint·typecheck·test·build)` · `build graph / affected (monorepo)` · `caching` · `reproducible / hermetic builds` · `runtime + PM pins` · `lockfile policy`

## What professional engineers do

- **CI gate = the four checks, always green to merge.** A `.github/workflows/ci.yml` runs **lint · typecheck · test · build** on every push/PR and is the merge gate. This is the most durable foundation signal after README/license: **CI 92% simple / 91% weighted / 93% at N=938** `[census]`. CI being the *enforced* gate (vs. advisory) is the Accelerate continuous-integration capability `[lit]`.
- **CI over local hooks (the bypass argument).** Pre-commit hooks are an *ergonomic* helper, not a gate — they are locally skippable (`--no-verify`). The real gate must be server-side and unbypassable. Census confirms the split: CI 92% vs. precommit hooks 33% (20% at N=938) `[census]`; OpenSSF Code-Review-enforced is only ~41% in the wild `[census/Scorecard]`, so a non-engineer harness must *raise* this — broken code reaching main is the weak link.
- **Pin the runtime + package manager.** `.nvmrc`/`.tool-versions` + Corepack/`uv` so every machine and CI runner resolves the same toolchain. Adoption is a minority but **rising** (runtime_pin 24→28 weighted, pkg_manager_pin 19) `[census]`; the senior bar sits *above* the census (Twelve-Factor II/X, OpenSSF Pinned-Dependencies avg 3.1/10 `[lit]`) because environment drift is unrecoverable for the target user.
- **Commit the lockfile.** `pnpm-lock.yaml`/`uv.lock`/`Cargo.lock` committed → deterministic dependency resolution. Now a weighted majority (lockfile 57→61) `[census]`; npm "strongly recommends" committing, Cargo (2023) says even libraries should `[lit]`. App/CLI = always commit; library = recommended.
- **Build graph / affected runs (monorepo only).** In a monorepo, CI runs only the **affected** projects' tasks via a task graph (Turborepo/Nx), with topological ordering and per-task inputs. build_config is 88% in monorepos vs. 65% overall `[census]`; this is YAGNI for single-package repos (gate only when archetype=monorepo).
- **Caching.** Cache the dependency store and build/task outputs keyed by lockfile hash + inputs (GitHub Actions cache, Turbo/Nx remote cache). Caching is a *speed* lever; correctness still rests on the lockfile + pins, not the cache. SLSA L3 explicitly calls out **cache poisoning** as a build-isolation threat `[lit, normative]`.
- **Reproducible / hermetic builds (maturity tier).** The senior aspiration is byte-for-byte reproducibility (Reproducible-Builds.org) and isolated builds. SLSA v1.2's **Build track** makes **provenance + build isolation** the requirement (L1 provenance exists → L2 signed by a hosted builder → L3 hardened/isolated, non-forgeable) — these Build-track levels are unchanged from v1.0 — and treats *hermetic* and *reproducible* as future/optional, not mandated `[lit, normative]`. (The **Source track**, incl. "Source L2 = continuous, immutable, signed history" and "Source L3 = enforced technical controls", is a **v1.2 addition** — it did not exist in v1.0, which carried the Build track only.) Practical floor: pinned actions (by SHA), least-privilege CI token permissions, no network in test where avoidable.

## Evidence (lit + census)

- **CI is near-universal and durable:** 92% simple / 91% weighted / **93% at N=938** — survives sample doubling (smplΔ ≈ +1) `[census]`. GitHub Actions dominates the CI provider axis (372/429; 80.0 vs. next 0.6) `[census]`.
- **Gate vs. hook split:** CI 92% vs. precommit 33% (20% at N=938); OpenSSF Code-Review-enforced ~41%, Branch-Protection ~13% (admin-token-limited, n=118) `[census/Scorecard]` — the non-file foundation that must be raised above the wild.
- **Pinning is rising but rare → raise it:** runtime_pin 24→28w, pkg_manager_pin 19; OpenSSF Pinned-Dependencies avg **3.1/10** (2.4 at the wider 938) `[census/Scorecard]` independently confirms pins are weak in the wild `[lit Twelve-Factor II/X; OpenSSF]`.
- **Lockfile now a majority:** 57→**61** weighted `[census]`; `[lit]` npm package-lock "strongly recommended"; Cargo committing-lockfiles (2023).
- **Build config is archetype-driven:** monorepo 88, mobile 91, web-app 79 vs. data-ml 30, cli 45 `[census]` — confirms build/affected-graph belongs in conditional, not core.
- **N=6,582 governance-floor re-census confirms the split at 6.5k scale** (`census-data/census-governance-floor/`, 2026-07-05, star-floor 29, archetype-stratified): CI present **85%** (GitHub-Actions-or-common-CI; k8s-style external CI like Prow is undetectable → slight undercount) — the near-universal CI floor holds. The DX/config-file floor is a **minority-and-archetype-gated** set — committed-lockfile 38% · **.editorconfig 21% (but 48% in monorepos)** · .gitattributes 29% · **pre-commit 5% overall / 28% in cli·tooling repos** (helper not a gate — `--no-verify`-bypassable, reinforcing CI-over-hooks) · .env.example 4% · dependency-update-bot (Dependabot/Renovate) 30% — so these belong in conditional sets, not the universal core `[census]`. **Reference-class caveat:** the ecosystem tag skews the aggregate down (Java over-represented & low-governance; Python under-counted because requirements.txt-only repos fail the manifest software-filter), so node/go/rust rates run ~**1.4×** the aggregate.
- **`[lit, normative]` anchors:** Accelerate (Forsgren/Humble/Kim 2018, CI capability) · SWEBOK KA4 Construction / KA6 Configuration-Management · SLSA v1.2 Build-track levels (+ the v1.2-new Source track) · Reproducible-Builds definition.

## Archetype variations

- **library / cli:** build→dist|bin in CI; release-automation builds artifacts; lockfile recommended (not blocking) for libraries (T4).
- **web-app / backend:** build config (vite/next) high (79); Dockerfile build common (backend 79%); `.env.example` for config parity (web-app 45%) `[census]`.
- **mobile:** platform build (android/ios), build_config 91% `[census]`; CI matrix per platform.
- **monorepo (conditional gate):** the only archetype where **build-graph / affected runs + workspace config (pnpm-workspace/turbo/nx) + CODEOWNERS** activate; build_config 88% `[census]`. Single-package repos run the whole suite — affected-graph is YAGNI.
- **data-ml:** lower build_config (30%) — CI often validates notebooks/pipelines rather than compiling.

## Tradeoffs / what's ruled out

- **Pre-commit hooks as *the* gate — ruled out.** Locally bypassable; CI is the enforceable gate (T3). Hooks remain an opt-in helper.
- **Reproducible/hermetic builds as a day-one mandate — ruled out (maturity tier).** SLSA itself treats hermetic/reproducible as future-direction, not Build L1–L3 requirements `[lit, normative]`; mandating zero-network hermetic builds at scaffold time is over-engineering for most archetypes. Floor = provenance posture + pinned actions + least-priv tokens.
- **Caching as a correctness mechanism — ruled out.** Cache is speed-only; correctness derives from lockfile + pins. Mis-keyed caches are a known hazard (SLSA cache-poisoning).
- **Following census popularity for tool defaults — ruled out.** Tool choice is the fastest-moving axis; defaults follow the *weighted* winner (ruff/uv, biome/pnpm rising), not simple install base.
- **`.editorconfig` in the CI/build core — demoted.** 39→19 weighted; modern formatters (biome/ruff) absorb it `[census]`.

## Sources

- Accelerate (Forsgren/Humble/Kim 2018) — https://itrevolution.com/product/accelerate/
- The Twelve-Factor App (II/X dependencies & dev-prod parity) — https://12factor.net/
- OpenSSF Scorecard (Pinned-Dependencies, Branch-Protection, CI-Tests) — https://scorecard.dev/
- SLSA v1.2 build requirements (Build-track levels, isolation, provenance — unchanged from v1.0) — https://slsa.dev/spec/v1.2/build-requirements
- SLSA v1.2 source requirements (Source track — new in v1.2; Source L2 = signed/protected history) — https://slsa.dev/spec/v1.2/source-requirements
- npm package-lock.json — https://docs.npmjs.com/cli/v11/configuring-npm/package-lock-json/
- Cargo committing lockfiles (2023) — https://blog.rust-lang.org/2023/08/29/committing-lockfiles/
- Reproducible Builds — definition — https://reproducible-builds.org/docs/definition/
- Turborepo running tasks (task graph / affected) — https://turborepo.com/docs/crafting-your-repository/running-tasks
- GitHub Actions dependency caching — https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows
- copier (3-way merge / answers-file) — https://copier.readthedocs.io/ · copier `adopt` proposal #2486 — https://github.com/copier-org/copier/issues/2486 · cruft — https://cruft.github.io/cruft/
- SonarQube "Clean as You Code" — https://docs.sonarsource.com/sonarqube-server/latest/user-guide/clean-as-you-code/ · Dusty Burwell "ratchets" — https://www.dustyburwell.com/2019/05/29/ratchets.html · Fowler StranglerFig — https://martinfowler.com/bliki/StranglerFigApplication.html

## Sub-documents
- [`cross-project-reuse--facts-2026-08.md`](cross-project-reuse--facts-2026-08.md) — *research-log (ko)* — 2026-08 표적 조사: 저장소 하나의 바닥을 **여러 프로젝트에 반복 설치하지 않는** 기계장치 3종(템플릿 저장소·재사용 워크플로·`.github` 상속)의 경계 — 무엇이 옮겨지고 무엇이 안 옮겨지며 갱신이 전파되는가. 비공개 재사용 저장소의 `access_level` 기본값 `none` 실측 포함.
- [`foundation-floor-artifact-checklist.md`](foundation-floor-artifact-checklist.md) — *research-log* — the ② bootstrap floor artifact checklist (VCS/build/CI/quality/test/security/config/dev-env/docs/governance) + repo-context conditioning.
- [`visibility-provision-matrix.md`](visibility-provision-matrix.md) — *research-log* — which floor features are gated by repo visibility×plan + the OSS substitute for each + private/public provision tables + the make-public flip list.
- [`brownfield-adoption-floor.md`](brownfield-adoption-floor.md) — *research-log* — the ②-foundation slice of the `adopt` model: audit-mode (read-only, non-blocking) · 3-way disposition · additive-first + propose-PR · ownership baseline (`.copier-answers.yml`) · relaxed green-gate (Clean-as-You-Code + ratchet); scaffolder/IDP/ratchet survey + 51-tool census.
- [`web-scaffold-baseline--facts-2026-08.md`](web-scaffold-baseline--facts-2026-08.md) — *research-log (ko)* — 2026-08 facts-only pass (GAPS R1-11): 2026 웹 앱 프로덕션 베이스라인 중 **공식 문서가 규정하는 것** — 세션/쿠키 속성(OWASP) · PostgreSQL/Supabase RLS 기본값과 service_role 우회 · GitHub Actions 시크릿 마스킹 한계와 `NEXT_PUBLIC_` 빌드타임 인라인 · required checks(최소 구성 규정 부재) · Sentry PII 스크러빙. **표준 권고 vs 플랫폼 구현의 상충**(시크릿의 환경변수 저장)을 병기. scaffold 기본값 설계(M7 서버측 통제 표)의 입력.
- [`cicd-release--facts-2026-08.md`](cicd-release--facts-2026-08.md) — *research-log (ko)* — 2026-08 facts-only pass: Fowler CI practices · CI/CD/CD definitions · feature-toggle taxonomy · blue-green/canary · DORA metrics & 2024 benchmarks · SemVer · release trains · CI-tool adoption stats · monorepo. (release-side content also serves aspect-17)
