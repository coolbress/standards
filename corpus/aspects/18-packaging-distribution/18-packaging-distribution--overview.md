---
id: aspect-18-packaging-distribution
title: "Packaging & Distribution"
group: "R — Release & Operate"
kind: gated
gated_archetypes: ["published"]
cross_cutting: false
lifecycle_stages: ["④"]
anchors: ["npm-provenance", "SLSA", "Homebrew", "winget", "App-Store-guidelines"]
evidence_track: census+lit
status: review-needed
last_updated: "2026-06-27"
sources:
  - "https://semver.org/"
  - "https://docs.npmjs.com/generating-provenance-statements"
  - "https://slsa.dev/spec/v1.2/build-requirements"
  - "https://docs.brew.sh/How-to-Create-and-Maintain-a-Tap"
  - "https://github.com/microsoft/winget-pkgs"
  - "https://goreleaser.com/"
  - "https://dora.dev/guides/dora-metrics-four-keys/"
claim: "Senior engineers ship from a tagged, SemVer'd CI release that publishes to the archetype's canonical channel (registry / binary tap / container / app store) with build provenance — the artifact is a reproducible CI output, never a hand-uploaded local build."
maps_from: ["census-data/census-release-ops"]
census_todo: "Signing now census-backed offline (gh-API=0) from the Scorecard `sc` field — Signed-Releases strong 15% / present 17% (census-governance n=103). Still deferred (low priority): publish-CHANNEL share (npm vs PyPI vs Homebrew vs winget vs goreleaser) is not offline-derivable — the census records hold derived flags only, not workflow/tree contents; converting channel mix to [census] adoption % needs a targeted workflow-content survey."
---

> 🔄 **분류 정정 2026-08-28** (`GAPS` R5-16 ②ⓐ): `kind: universal` · `gated_archetypes: []` → **`kind: gated` · `["published"]`**. claim 이 *"publishes to the archetype's **canonical channel**"* 을 전제한다. 안 배포하는 로컬 스크립트에 registry·app store 를 요구할 수 없다. `published` 는 측면 21 이 이미 쓰는 **조건 축** 값이다.
>
> `[]` 는 *universal* 을 뜻하므로(`_schema.md` §3.1) 그대로 두면 **바닥이 로컬 CLI 스크립트에도 이걸 요구한다.** claim 본문과 분류가 어긋나 있었다.

> **Standard (claim):** Ship from a tagged, SemVer'd CI release that publishes to the archetype's canonical channel (registry / binary tap / container / app store) with build provenance — the artifact is a reproducible CI output, never a hand-uploaded local build.
> **Evidence:** 429-repo release-ops census + named standards (SemVer, npm provenance, SLSA, Homebrew/winget) · **Confidence:** High (release-half is hard census data; provenance/signing is `[lit]`-led, near-absent in the wild) · **Kind:** universal · **Stage:** ④

**Seed sub-aspects:** `registry publish (npm/PyPI/crates/Maven)` · `binary distribution (Homebrew/winget/goreleaser)` · `container / Helm publish` · `app-store submission / staged rollout` · `self-update` · `provenance`

## What professional engineers do
- **Tagged CI release is the unit of distribution.** A SemVer `vMAJOR.MINOR.PATCH` tag triggers a release workflow that builds, attaches notes, and publishes — not a developer running `npm publish` from a laptop. `[census]` 89/86% of repos publish tagged GitHub Releases; 86/80% use SemVer (tag `semver_ratio` weighted-mean **0.72**). Release notes accompany 88/85%. Median cadence between releases **7 days**.
- **Registry publish (library/cli).** Publish to the ecosystem's canonical registry from CI on tag: npm / PyPI / crates.io / Maven Central. Pin the publishing identity to CI (OIDC/Trusted Publishing) rather than a long-lived token. Commit the lockfile so the published tree is reproducible (`[census]` lockfile-commit 57/61%, foundation §3).
- **Build provenance / attestation.** Publish a signed provenance statement linking the artifact to its source commit + build instructions. `[lit]` npm provenance generates this via Trusted Publishing (OIDC) on a cloud CI runner, signed through **Sigstore** (ephemeral certs + transparency log), aligning with **SLSA Build L2+** (hosted platform, signed provenance). This is the single biggest gap between standard and practice — `[census]` Signed-Releases is **1.2% weighted** in the wild.
- **Binary distribution (cli/desktop).** Cross-compile per OS/arch in CI and publish to package managers: **Homebrew** (formula for CLIs via a tap; cask for GUI `.app`/`.dmg`/`.pkg`), **winget** (YAML manifest PR'd to `microsoft/winget-pkgs`), Scoop, apt/rpm. **goreleaser** is the canonical orchestrator — one tag → cross-platform builds, checksums, GitHub release, Homebrew tap + Scoop manifest updates in one pass.
- **Container / Helm publish (backend/service/monorepo).** Build + push an immutable, digest-pinned image to a registry (GHCR/ECR/Docker Hub) from CI; ship a versioned Helm chart for k8s consumers. `[census]` (n=429 · uniform / weighted) container **53/62%** (backend **79%**), cd_deploy **64/68%**.
- **App-store submission / staged rollout (mobile).** Submit signed builds through App Store Connect / Play Console; gate user exposure behind **staged/phased rollout** (e.g. 1%→10%→100%) so a bad build is caught before full reach. App-store review is an external gate the harness cannot file — posture + checklist only.
- **Self-update (cli/desktop).** Long-lived installed binaries check a release feed and update in place (signature-verified) so users aren't stranded on an old version.
- **Changelog is the human-facing distribution artifact.** Keep-a-Changelog `CHANGELOG.md` + Conventional-Commits history feeds auto-generated notes & SemVer bumps. `[census]` (n=429 · uniform / weighted) changelog **55/52%**; CC-adopted (≥30% of commits) **45/67%** — the fastest-rising ④ signal (+22 weighted).

## Evidence (lit + census)
- `[lit]` **SemVer 2.0.0** — versioning grammar every registry/distribution channel keys off (https://semver.org/).
- `[lit]` **npm provenance / Trusted Publishing** — OIDC-driven, Sigstore-signed provenance + publish attestations; explicitly "does not guarantee no malicious code" — it is transparency, not assurance (https://docs.npmjs.com/generating-provenance-statements).
- `[lit]` **SLSA v1.2 Build-track Levels** (unchanged from v1.0) — L1 provenance exists (may be unsigned); **L2** hosted platform + signed provenance; **L3** hardened, isolated builds with inaccessible signing secrets (https://slsa.dev/spec/v1.2/build-requirements).
- `[lit]` **Homebrew tap** (formula vs cask; CLIs = formula) (https://docs.brew.sh/How-to-Create-and-Maintain-a-Tap) · **winget** community manifest repo (https://github.com/microsoft/winget-pkgs) · **goreleaser** cross-platform release orchestration (https://goreleaser.com/).
- `[census]` 429-repo release-ops survey (recency-weighted `w=0.5^(age/2yr)`, ref 2026-06-24): has_releases **89/86**, release_notes **88/85**, semver_any **86/80** (ratio 0.72), changelog **55/52**, cc_adopted **45/67**, container **53/62** (backend 79), cd_deploy **64/68**, iac 28/29, observability 18/17. Release cadence median **7 days** (n=378).
- `[census]` **Signed-Releases** (OpenSSF Scorecard `sc`, derived offline gh-API=0; governance n=103, mean 1.2/10): strong **15%** / present **17%** — provenance/signing is the supply-chain blind spot, the ~15% adoption grounding the [lit]-mandated signing gap. Senior practice (`[lit]`), rare in the wild. The lower n is an honest coverage limit (the check needs release visibility). (Source: census-governance `sc`; methodology `_schema.md` §4 (methodology).)
- `[lit]` **DORA Four Keys** — deployment frequency proxies the 7-day cadence; release automation drives the velocity half (https://dora.dev/guides/dora-metrics-four-keys/).

## Archetype variations
- **library:** registry publish (releases 91, semver 92) + provenance + changelog. No container/binary/app-store. The cleanest case: "publish a versioned package."
- **cli:** registry **and/or** binary distribution — cross-compiled goreleaser artifacts to Homebrew/winget/Scoop (releases **95**, notes 95). Often a self-update channel.
- **backend-service:** container is the artifact (container **79**, cd_deploy 67) — digest-pinned image + optional Helm chart, not a registry package.
- **monorepo:** per-package versioning (changesets/Nx/Turbo release), mixed channels (container 68, cd 83) — multiple artifacts from one tag.
- **web-app:** built bundle deployed via CD (cd 70); "distribution" = a deploy, not a published package.
- **mobile:** app-store submission + signed builds + staged rollout — observability/container ≈ 0; the channel is the store, gated by external review.
- **data-ml:** weakest release discipline (releases 65, semver 43) — many are research repos, not shipped products; treat publish as conditional, not mandated.

## Tradeoffs / what's ruled out
- **Ruled out: hand-uploaded local builds.** A laptop `publish` defeats provenance and reproducibility — the artifact must be a CI output. Cost: requires CI publish credentials/OIDC wiring up front.
- **Provenance/signing — `[lit]`-mandated despite 1.2% census.** This is a *do-it* (senior practice) decision, not a *publish-because-everyone-does*; the census says don't expect to find it, the standard says ship it. Cheap via Trusted Publishing; no excuse to skip.
- **Don't cargo-cult ops channels onto libraries.** IaC/container/app-store on a pure library is waste — channel follows archetype (the C5 branch). Mandating container on a library is the inverse error of skipping it on a service.
- **App-store review is non-automatable** — the harness prepares the submission + posture but cannot pass the gate; staged rollout mitigates blast radius but adds release latency.
- **SLSA L3 (hardened isolated builds) is aspirational for most** — L2 (signed provenance on a hosted platform) is the realistic, near-free floor; L3 demands platform controls most teams don't run.

## Sources
- SemVer 2.0.0 — https://semver.org/
- npm provenance / Trusted Publishing — https://docs.npmjs.com/generating-provenance-statements
- SLSA v1.2 Build-track Levels (unchanged from v1.0) — https://slsa.dev/spec/v1.2/build-requirements
- Homebrew: How to Create and Maintain a Tap — https://docs.brew.sh/How-to-Create-and-Maintain-a-Tap
- winget community manifest repo — https://github.com/microsoft/winget-pkgs
- GoReleaser — https://goreleaser.com/
- DORA Four Keys — https://dora.dev/guides/dora-metrics-four-keys/
