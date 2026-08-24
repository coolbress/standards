---
id: aspect-10-supply-chain-security
title: "Software Supply Chain Security"
group: "C — Construct & Verify"
kind: cross-cutting
gated_archetypes: []
cross_cutting: true
lifecycle_stages: ["②", "④"]
anchors: ["NIST-SSDF-PS", "SLSA-v1.2", "OpenSSF-Scorecard", "OpenSSF-Baseline", "in-toto", "Sigstore"]
evidence_track: census+lit
status: review-needed
last_updated: "2026-06-27"
sources:
  - "https://csrc.nist.gov/pubs/sp/800/218/final"
  - "https://csrc.nist.gov/Projects/ssdf"
  - "https://slsa.dev/spec/v1.2/build-requirements"
  - "https://slsa.dev/spec/v1.2/source-requirements"
  - "https://scorecard.dev/"
  - "https://api.securityscorecards.dev/"
  - "https://baseline.openssf.org/"
  - "https://in-toto.io/"
  - "https://www.sigstore.dev/"
  - "https://cyclonedx.org/"
  - "https://spdx.dev/"
  - "https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions"
claim: "Senior teams treat the build/distribution path as an attackable asset — pin dependencies and CI Actions by digest, run a least-privilege CI with scanning + a dependency-update bot, and (at distribution) emit an SBOM plus signed provenance attestations — but wild adoption is low (Pinned-Deps ~3/10, Signed-Releases ~1/10), so a non-engineer harness must scaffold the baseline by default rather than rely on the ecosystem."
maps_from: ["census-data/census-dev-environment"]
census_todo: "RESOLVED offline (gh-API=0): the Scorecard supply-chain checks are now census-backed from the `sc` field across census-governance + census-expanded — Pinned-Dependencies (strong 20-27%), Token-Permissions (24-26%), Signed-Releases (15%), Dependency-Update-Tool (94%, small n). Still deferred (low priority): publish-channel and SBOM-tool share (CycloneDX vs SPDX, cosign vs attest-build-provenance) are not offline-derivable — the census records hold derived flags only, not tree/workflow contents; converting those to [census] adoption % needs a targeted workflow-content survey."
---

> **Standard (claim):** _Treat the build + distribution path as an attackable asset: pin deps/Actions by digest, run a least-privilege scanned CI with a dep-update bot, and at distribution emit an SBOM + signed provenance — and because the wild floor is low, scaffold the baseline by default._
> **Evidence:** census+lit (OpenSSF Scorecard API over 429 repos + named standards) · **Confidence:** high · **Kind:** cross-cutting · **Stage:** ②, ④

**Seed sub-aspects:** `SBOM (CycloneDX / SPDX)` · `provenance / attestation` · `artifact signing` · `dependency lifecycle / upgrade policy (Renovate/Dependabot)` · `pinned GH Actions` · `least-privilege CI`

## What professional engineers do

- **Pin dependencies (and the build).** Lockfiles (`pnpm-lock.yaml`/`uv.lock`/`Cargo.lock`) pin the *resolved* graph by content hash; runtime versions pinned (`.nvmrc`/`packageManager`/`.python-version`). This makes builds reproducible and blocks silent transitive substitution. [lit] NIST SSDF PS-3 (archive/protect each release), [lit] SLSA Build L2+ (verified provenance over a controlled build).
- **Pin third-party GH Actions by commit SHA, not by tag.** `uses: actions/checkout@<40-char-sha>`, not `@v4` — a tag is mutable and a compromised upstream can repoint it (the 2025 `tj-actions/changed-files` incident). Renovate/Dependabot then bump the SHA with a readable changelog. [lit] GitHub Actions security-hardening; [lit] OpenSSF Scorecard *Pinned-Dependencies* check.
- **Least-privilege CI.** Default the workflow token to `permissions: read-all` (or `contents: read`) and grant write scopes only on the specific job that needs them; never expose secrets to PR-from-fork triggers (`pull_request_target` hygiene); avoid `Dangerous-Workflow` patterns (untrusted-input → `run:`). [lit] Scorecard *Token-Permissions* / *Dangerous-Workflow*.
- **Continuous dependency lifecycle.** A bot (Dependabot/Renovate) opens PRs for outdated/vulnerable deps; CI runs `pnpm audit`/`pip-audit`/`osv-scanner` to fail on known CVEs; an upgrade policy (auto-merge patch, review minor/major) keeps the graph fresh instead of letting it rot. [census] Dependabot is the dominant choice (~4:1). `[inferred]` **Private-repo Dependabot gotcha (gingoa-verified 2026-06-26).** *Why it fails now:* on a *private* repo Dependabot auto-routes the `npm` ecosystem through GitHub Packages (`npm.pkg.github.com`), which doesn't mirror the public registry → public deps fail to resolve (`ERR_PNPM_NO_MATCHING_VERSION`), and the public registry can't be scoped without a token (the `npm-registry` registries schema *requires* a token, so a token-less entry fails validation and the **whole config stops parsing** — taking other ecosystems down too). *Operational consequence of dropping the npm ecosystem:* npm version-bumps become **manual** (`pnpm update` / `pnpm up --latest`) — but **safely**: `pnpm audit` (CI, fail on high/critical) + Dependabot security **alerts** still force *security-critical* updates, so the only real cost is gradual **drift** (larger major-version jumps later), trivial for a small dev-dep set. *Forward path:* (1) floor = keep `github-actions` (works; auto-bumps the SHA-pins incl. node20→node24) + `pnpm audit` as the CVE gate; (2) **stay manual** while the dep set is small; (3) adopt **Renovate** (handles the private-repo routing) when npm auto-update is wanted or drift grows; (4) the limitation **disappears when the repo goes public**, where Dependabot npm just works — so revisit at ④ release / on going public. **Harness rule:** when gingoa scaffolds Dependabot, the **npm ecosystem is visibility-gated** — public repo → npm on; private repo → `github-actions`-only + Renovate optional.
- **Scan the source.** SAST/code-scanning (CodeQL) and secret-scanning in CI; for containers, image scanning. [lit] SSDF PW-7/PW-8 (review & test); Scorecard *SAST*.
- **At distribution: SBOM + signed provenance.** A published artifact ships a machine-readable bill of materials (CycloneDX or SPDX) and a signed provenance attestation binding the artifact to the build (in-toto / SLSA provenance, signed via Sigstore keyless `cosign` or GitHub's `attest-build-provenance`). Consumers verify the signature + provenance before trusting. [lit] SLSA v1.2 (Build track); [lit] in-toto; [lit] Sigstore. *Scope note:* an **SBOM file is producible at ②** (a static dependency-tree artifact — and the Scorecard *SBOM* check already rewards a source/pipeline SBOM file); only the **signing** half — signed provenance + release-signing — is genuinely a ④ release-tier control.
- **Measure the posture, don't assume it.** OpenSSF Scorecard scores a repo 0–10 per check; OpenSSF Baseline (formerly Security Baseline / 2025) gives a **tiered** minimum-bar checklist (**~41 controls across 3 maturity levels** — L1 universal floor / L2 = 2+ maintainers + a small consistent user base / L3 = a large, widely-adopted user base) that maps onto SSDF. The leveling is load-bearing: branch-protection + MFA-for-write sit at **L1**, signed-release + CI-test-gate at **L2**, and **non-author review + SAST + release-SBOM at L3** — so a small/solo project legitimately sits at L1 and defers the L3 controls by the standard's own design. Senior teams track the score and gate regressions. [lit] Scorecard; [lit] OpenSSF Baseline. *AI-harness note:* because gingoa builds **AI/foundation-model** software, **NIST SP 800-218A** — *Secure Software Development Practices for Generative AI and Dual-Use Foundation Models: An SSDF Community Profile* — augments the SSDF with model-development-specific tasks and is the relevant SSDF profile to track alongside SP 800-218. [lit]

## Evidence (lit + census)

- [lit] **NIST SP 800-218 (SSDF) v1.1** — Protect Software (PS), Produce Well-Secured Software (PW); the federal baseline behind SLSA/Scorecard. https://csrc.nist.gov/pubs/sp/800/218/final · **NIST SP 800-218A** — the GenAI / dual-use-foundation-model SSDF Community Profile (used in conjunction with 800-218; relevant because gingoa is an AI harness). https://csrc.nist.gov/Projects/ssdf
- [lit] **SLSA v1.2** — **Build track** provenance levels (L1 provenance exists → L2 signed by a hosted builder → L3 hardened/isolated, non-forgeable; *unchanged from v1.0*) **plus the v1.2-new Source track** (Source L2 = continuous/immutable/signed history — the level behind "sign your commits"; Source L3 = enforced technical controls). The Source track **did not exist in v1.0** (v1.0 carried the Build track only). https://slsa.dev/spec/v1.2/build-requirements · https://slsa.dev/spec/v1.2/source-requirements
- [lit] **OpenSSF Scorecard** — **~20 automated checks**; the foundation-relevant subset is Pinned-Dependencies, Token-Permissions, Branch-Protection, Signed-Releases, SAST, Dangerous-Workflow, Dependency-Update-Tool, Vulnerabilities, Binary-Artifacts, **SBOM**, **Webhooks** (the full ~20 also covers CI-Tests, Code-Review, Fuzzing, License, Maintained, Packaging, Contributors, CII-Best-Practices, Security-Policy). Note the **SBOM check exists at ②** — it scores an SBOM **file present in source/pipeline** (5/10), not only a release artifact (the other 5/10), so a buildable SBOM file is checkable pre-release; public API. https://scorecard.dev/ · https://api.securityscorecards.dev/ · checks list https://github.com/ossf/scorecard/blob/main/docs/checks.md
- [lit] **OpenSSF Baseline (OSPS)** — tiered minimum security requirements (~41 controls × 3 maturity levels × 6 lifecycle categories) for OSS projects; the leveling (L1 floor → L3 widely-adopted) is the named grounding for context-conditioned deferral. https://baseline.openssf.org/ · version doc https://baseline.openssf.org/versions/2025-02-25.html
- [lit] **in-toto** (supply-chain attestation framework) https://in-toto.io/ · **Sigstore** (keyless signing/transparency log) https://www.sigstore.dev/
- [lit] **CycloneDX** https://cyclonedx.org/ · **SPDX** https://spdx.dev/ — the two SBOM formats. **GitHub Actions hardening** (SHA-pin Actions, scope `permissions:`) https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions
- [census] **Scorecard `sc` field, derived offline (gh-API=0) over both samples** — census-governance (n=429) + census-expanded (n=938), 59% scored; `-1`=inconclusive dropped; recency-weighted; `_schema.md` §4 (methodology). "strong" = score ≥7/10. These confirm the [lit]-mandated supply-chain gaps are real in the wild → the harness must *lift* them:
  - **Pinned-Dependencies** strong **27%** (governance n=232, present 52%, mean 3.1/10) → **20%** (expanded n=527, present 42%) — *pinning is rare in the wild*, and erodes on the wider, less-elite sample.
  - **Token-Permissions** (least-priv CI) strong **26%** (governance n=225, mean 2.6) → **24%** (expanded n=502) — least-privilege CI tokens are uncommon.
  - **Signed-Releases** strong **15%** / present **17%** (governance n=103, mean 1.2) — release signing is the sharpest gap (the ④ supply-chain blind spot). Lower n is an honest coverage limit (the check needs release visibility).
  - **Dependency-Update-Tool** strong **94%** (governance n=36, small-n) — where the check is judgeable, a dep-update bot is near-universal; corroborates the file-census Dependabot reading.
  - **SAST** strong **36%** (governance n=247) → **24%** (expanded n=609), **Dangerous-Workflow** strong **91%** (governance n=226, most repos avoid the worst patterns), Branch-Protection strong 10–13%, Code-Review-enforced ~41% (cross-ref aspects 05/09).
  - File-census cross-check: **`security_md` 54%**, **`dep_bot` (Dependabot) 49/44%**, **lockfile 57/61%**, an aggregate **`supply_chain_security` flag (CodeQL/SBOM/SHA-pin) 28→20%** (drops to 17% on young repos). License 99% (Scorecard) corroborates the 97% file census → methodology trust.

**Net:** the *practices* are well-defined ([lit]) but adoption is low even among elite repos ([census]) — so for a non-engineer harness these are **default-on safety rails / opt-in advanced**, not "rely on the ecosystem to already have them."

## Archetype variations

- **Library / package / CLI (publishes an artifact):** full ④ obligation — SBOM + signed provenance + signed releases are in-scope, because consumers depend on *your* artifact. This is the highest-leverage archetype for signing.
- **Service / web app (deployed, not published):** SBOM is still valuable (vuln triage), but provenance matters most at the container-image boundary; least-priv CI + image scanning dominate over package signing.
- **Internal tool / script:** pin deps + least-priv CI + dep-bot is the proportionate floor; SBOM/signing usually deferred.
- **gingoa itself = distribution archetype** (`supply_chain_distribution: true` — it ships a plugin + npm package), so it inherits the full set. No archetype is *gated off* this aspect (cross-cutting), but the *depth* scales with whether you publish.

## Tradeoffs / what's ruled out

- **SHA-pinning vs. maintenance churn:** pinned digests need a bot to bump them or they rot; pinning *without* Renovate/Dependabot is worse than tag-pinning. Pin **and** automate, never one alone.
- **Strict least-priv vs. CI breakage:** `read-all` default surfaces friction (jobs that quietly needed write); accept the friction — failing closed beats a leaked write token.
- **Full SLSA L3 / keyless signing has real setup cost** — ruled out as a day-one default for non-publishing archetypes; reserved for the distribution archetype and opt-in elsewhere.
- **SBOM is documentation, not a guarantee** — it lists components, it does not prove them safe; pair with audit/scanning. "Has an SBOM" ≠ secure.
- **Ruled out:** treating Dependabot alerts as the whole program (alerts ≠ enforced gate), or committing binary artifacts (Scorecard *Binary-Artifacts*).

## Sources
- NIST SP 800-218 (SSDF) v1.1: https://csrc.nist.gov/pubs/sp/800/218/final · NIST SP 800-218A (GenAI/foundation-model SSDF profile): https://csrc.nist.gov/Projects/ssdf
- SLSA v1.2 — Build track: https://slsa.dev/spec/v1.2/build-requirements · Source track (new in v1.2): https://slsa.dev/spec/v1.2/source-requirements
- OpenSSF Scorecard (~20 checks, incl. SBOM + Webhooks): https://scorecard.dev/ · API: https://api.securityscorecards.dev/ · checks: https://github.com/ossf/scorecard/blob/main/docs/checks.md
- OpenSSF Baseline (OSPS, ~41 controls × 3 levels): https://baseline.openssf.org/ · https://baseline.openssf.org/versions/2025-02-25.html
- in-toto: https://in-toto.io/ · Sigstore: https://www.sigstore.dev/
- CycloneDX: https://cyclonedx.org/ · SPDX: https://spdx.dev/
- GitHub Actions security-hardening: https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions

## Sub-documents
- [`facts-2026-08-dependency-updates-scope.md`](facts-2026-08-dependency-updates-scope.md) — *research-log (ko)* — 2026-08 facts-only pass (R2-3): Dependabot·Renovate가 **하는 것과 하지 않는 것** · **적용 범위 표 — SLSA·Scorecard·SBOM 어느 것도 자체 호스팅 웹 앱 적용을 명시하지 않음**(SBOM 의무는 정부/규제 산업 판매 기준). 표준 §6의 aspect 10 기각 판단을 근거로 뒷받침.
