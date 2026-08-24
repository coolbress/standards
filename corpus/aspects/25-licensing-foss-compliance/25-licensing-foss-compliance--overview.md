---
id: aspect-25-licensing-foss-compliance
title: "Licensing & FOSS Compliance"
group: "G — Cross-cutting Practice & Governance"
kind: cross-cutting
gated_archetypes: []
cross_cutting: true
lifecycle_stages: ["①"]
anchors: ["SPDX-2.3", "REUSE-2.0", "OpenChain-ISO-5230"]
evidence_track: census+lit
status: review-needed
last_updated: "2026-07-05"
sources:
  - "https://spdx.dev/learn/handling-license-info/"
  - "https://spdx.github.io/spdx-spec/v2.3/SPDX-license-expressions/"
  - "https://reuse.software/spec-3.2/"
  - "https://reuse.software/tutorial/"
  - "https://www.openchainproject.org/license-compliance"
  - "https://choosealicense.com/"
  - "https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository"
  - "https://www.apache.org/licenses/contributor-agreements.html"
  - "https://developercertificate.org/"
claim: "Senior teams pick a single deliberate outbound license, declare it machine-readably (a root LICENSE plus per-file SPDX identifiers, REUSE-clean), continuously scan inbound dependency licenses for compatibility/policy violations in CI, and gate contributions through DCO or a CLA — license presence is effectively universal (~96–99% of real repos)."
maps_from: ["census-data/census-governance"]
---

> **Standard (claim):** _Pick one deliberate outbound license, declare it machine-readably (LICENSE + SPDX, REUSE-clean), scan inbound dependency licenses in CI for compatibility/policy, and gate contributions via DCO/CLA._
> **Evidence:** census+lit (license presence ~96–99%) · **Confidence:** high · **Kind:** cross-cutting · **Stage:** ①

**Seed sub-aspects:** `license selection / compatibility (inbound/outbound)` · `SPDX identifiers / REUSE` · `dependency license scanning` · `CLA / DCO` · `dual-licensing` · `export control`

## What professional engineers do

- **Outbound license selection (deliberate, day-one).** Choose ONE explicit license at repo creation, not by accident. Permissive (MIT/Apache-2.0/BSD-3) for max adoption; copyleft (GPL/AGPL/MPL/LGPL) when reciprocity/share-alike is the goal. Apache-2.0 is preferred over MIT when an **explicit patent grant** matters. The choice is a product decision (adoption vs. reciprocity vs. patent posture), made via `choosealicense.com` heuristics and recorded — a missing/ambiguous license = legally "all rights reserved," which kills reuse. `[lit]`
- **Inbound/outbound compatibility.** The outbound license must be compatible with every inbound dependency license. One-directional rules: permissive deps flow into anything; **GPL is "viral"** (linking GPL code forces GPL outbound); AGPL extends copyleft to network use; proprietary/no-license deps are uncompilable into FOSS output. Senior teams maintain an allowlist/denylist policy (e.g. allow MIT/Apache/BSD/ISC; flag GPL/AGPL; deny "no license" / SSPL / commercial-only) and treat a license-compatibility break as a build failure. `[lit]`
- **Machine-readable declaration: SPDX + REUSE.** A root `LICENSE`/`LICENSE.txt` is table stakes (GitHub auto-detects it). Beyond that, mature projects add **SPDX short identifiers** (`SPDX-License-Identifier: Apache-2.0`) and copyright headers per file, and aim for **REUSE compliance** (REUSE Spec 3.2): every file has `SPDX-FileCopyrightText` + `SPDX-License-Identifier` headers, a `LICENSES/` folder holds full texts named by SPDX id, and `reuse lint` runs in CI. Result = unambiguous, tool-readable provenance of every file. `[lit]`
- **Dependency license scanning in CI.** Generate an **SBOM** (SPDX or CycloneDX) and run an automated license scanner against the policy on every push: `license-checker`/`license-compliance` (npm), `pip-licenses`/`pip-audit` (Python), `cargo-deny` (Rust), `go-licenses` (Go), or cross-stack tools (FOSSA, ScanCode, Trivy, Snyk, GitHub's dependency-review-action). Block the PR on a disallowed/unknown license. Pair with a lockfile so the resolved license set is reproducible. `[lit]`
- **Contribution gating: DCO vs. CLA.** Inbound IP must be clean. Two standard mechanisms: **DCO** (Developer Certificate of Origin) — each commit carries a `Signed-off-by` trailer asserting the contributor's right to submit; lightweight, Linux-kernel origin, enforced by the DCO bot/GitHub App. **CLA** (Contributor License Agreement) — contributor grants the project a copyright/patent license (sometimes assignment); heavier, needed when relicensing/dual-licensing rights are required; enforced by CLA-assistant bots. Pick one per project; DCO for community-permissive, CLA when a steward needs relicensing latitude. `[lit]`
- **Dual-licensing / commercial.** Vendors offering FOSS + paid editions hold all copyright (via CLA) so they can ship the same code under e.g. GPL (community) and a commercial license (enterprise) — the "open-core" model. Requires the CLA upfront; cannot be retrofitted onto contributions made under the original license. `[lit]`
- **Export control & sanctions.** US-hosted projects fall under EAR; open, publicly-available encryption source code is largely exempt but may require a one-time **TSU notification email to BIS/NSA** (EAR 740.13(e)). Practical hygiene: an `ECCN`/export note in docs for crypto-bearing projects, and awareness that platform ToS (GitHub) already enforces sanctions geoblocking. Low salience for most app repos; material for crypto libraries. `[lit]`
- **Org-scale program (OpenChain).** At company scale, license compliance is run as a *program*, not per-repo heroics: **OpenChain ISO/IEC 5230:2020** specifies the key process touchpoints, role assignment, and sustainability requirements for a conformant FOSS-compliance program (self-certifiable). This is the governance umbrella over all the per-repo practices above. `[lit]`

## Evidence (lit + census)

- `[census]` **License presence is effectively universal.** Expanded census n=938: **96%** carry a root license file. Governance census n=429 (OSSF Scorecard subset n=252): the **License** check scores **mean 9.7 / weighted 9.8**, with **99% (uniform) / 100% (weighted)** of repos "strong" — the single highest-adoption, flattest-distribution hygiene signal in the entire scorecard. Cross-validated against the foundation census's independent ~97% license-file rate. (`census-data/census-governance/stats.json`, `census-data/census-expanded/records.json`)
- `[census]` **Below the LICENSE file, declaration depth drops sharply.** Per-file SPDX headers / REUSE compliance and automated dependency-license scanning are *not* censused as separate fields here but are well below the ~96% license-file ceiling in practice — i.e. "has a LICENSE" is near-universal, "is REUSE-clean + scans deps in CI" is the senior-tier delta. (see `census_todo`) **↑ Adequacy pilot (n=2000, `census-data/census-gov-adequacy/`, 2026-07-05):** even the LICENSE *file* hides a gap — **91% present but only 78% carry a recognizable standard-license signature** (~13pp are custom/stub/non-SPDX text) — a concrete presence≠adequacy instance one step below the presence ceiling.
- `[census]` **Widened/deeper N re-confirms LICENSE as the single most-universal artifact, with a persistent unrecognized tail and permissive dominance.** Governance-floor census n=6,582 (top-starred repos, star floor 29, 2026-07-05): **LICENSE present 94% · SPDX-recognized 82%** (recognized-given-present 87%) — the ~13–18pp custom/unrecognized `NOASSERTION` tail survives at this wider N. Outbound-license distribution (top SPDX): **MIT ≈40% · Apache-2.0 ≈26% · unrecognized/NOASSERTION ≈12% · GPL-3.0 ≈6% · AGPL-3.0 ≈3% · BSD-3-Clause ≈3%**, with MPL-2.0/GPL-2.0/BSD-2 in the low single digits — permissive (MIT+Apache-2.0) is ~two-thirds of all outbound-license choice. (`census-data/census-governance-floor/`)
- `[lit]` **SPDX** — license identifiers & expressions, SPDX-spec v2.3. https://spdx.github.io/spdx-spec/v2.3/SPDX-license-expressions/ · https://spdx.dev/learn/handling-license-info/
- `[lit]` **REUSE 3.2** — per-file `SPDX-FileCopyrightText` + `SPDX-License-Identifier`, `LICENSES/` folder, `reuse lint`. https://reuse.software/spec-3.2/ · https://reuse.software/tutorial/
- `[lit]` **OpenChain ISO/IEC 5230:2020** — requirements for a conformant FOSS license-compliance program (process touchpoints, roles, sustainability). https://www.openchainproject.org/license-compliance
- `[lit]` **License selection** — choosealicense.com (permissive vs. copyleft vs. patent-grant heuristics). https://choosealicense.com/
- `[lit]` **DCO** (developercertificate.org sign-off) and **CLA** (Apache contributor agreements) as the two inbound-IP gating mechanisms. https://developercertificate.org/ · https://www.apache.org/licenses/contributor-agreements.html

## Archetype variations

- **Library / package (highest stakes).** Outbound license is a *consumption gate* — permissive (MIT/Apache-2.0) maximizes downstream adoption; SPDX in package manifest (`license` field) is mandatory for ecosystem tooling. Apache-2.0's patent grant matters most here. REUSE compliance and a published SBOM are differentiators.
- **CLI / app / backend-service.** License file still near-universal, but the team is mostly a *license consumer*: the dominant risk is inbound dependency compatibility (a GPL/AGPL transitive dep contaminating a permissive product), so CI dependency-license scanning is the high-value control. Outbound license can be permissive or even source-available.
- **Web-app / SaaS.** **AGPL awareness is critical** — AGPL deps trigger network-use copyleft, forcing source disclosure for the hosted service; many orgs denylist AGPL outright. Export/crypto rarely material.
- **Data/ML.** Distinct *dataset* and *model-weight* licenses (CC-BY, CC0, OpenRAIL, Llama-style use-restricted) sit alongside code licenses; "open weights ≠ OSI-open." Track model/data provenance separately from code.
- **Crypto/security libraries.** The export-control sub-aspect activates (EAR TSU notification for encryption source).
- No archetype is *gated out* — license presence is the floor everywhere (`gated_archetypes: []`).

## Tradeoffs / what's ruled out

- **Permissive vs. copyleft** = adoption vs. reciprocity. Permissive maximizes reuse but lets proprietary forks close the code; copyleft preserves freedom but repels some corporate adopters. No universal right answer — it's an intent decision, which is why it must be *recorded*, not defaulted silently.
- **CLA vs. DCO.** CLA enables relicensing/dual-licensing but adds contributor friction (legal signing) and centralizes power in the steward — community-hostile if overdone. DCO is frictionless and community-trusted but forecloses unilateral relicensing. Ruled out: requiring *both*, or a copyright-*assignment* CLA without a strong steward reason.
- **Full REUSE per-file headers** add real maintenance cost; for a small single-license repo, a root LICENSE + SPDX in the manifest is "good enough" and full REUSE is optional polish — don't gold-plate.
- **Ruled out:** shipping with no license (legally all-rights-reserved, unusable), mixing incompatible licenses unscanned, vendoring code of unknown provenance, and treating license compliance as a one-time launch checkbox rather than a continuous CI gate.

## Sources

- https://spdx.dev/learn/handling-license-info/
- https://spdx.github.io/spdx-spec/v2.3/SPDX-license-expressions/
- https://reuse.software/spec-3.2/
- https://reuse.software/tutorial/
- https://www.openchainproject.org/license-compliance
- https://choosealicense.com/
- https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository
- https://www.apache.org/licenses/contributor-agreements.html
- https://developercertificate.org/

## Sub-documents
- [`facts-2026-08-license-obligations.md`](facts-2026-08-license-obligations.md) — *research-log (ko)* — 2026-08 facts-only pass (R2-4): **라이선스 원문 4종 직접 확인** — AGPL-3.0 §13 네트워크 사용 조항 · GPL-3.0 · MIT · Apache-2.0 §4 · 조문 인용표(조항 번호·요구 내용·조건절) · SPDX 식별자와 REUSE 규격.
