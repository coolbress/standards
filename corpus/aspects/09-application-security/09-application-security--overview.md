---
id: aspect-09-application-security
title: "Application Security"
group: "C — Construct & Verify"
kind: cross-cutting
gated_archetypes: []
cross_cutting: true
lifecycle_stages: ["all"]
anchors: ["SWEBOK-KA13", "OWASP-SAMM", "OWASP-ASVS", "NIST-SSDF-PW", "BSIMM"]
evidence_track: lit
status: review-needed
last_updated: "2026-06-27"
sources:
  - "https://owasp.org/www-project-samm/"
  - "https://owasp.org/www-project-application-security-verification-standard/"
  - "https://owasp.org/www-project-top-ten/"
  - "https://owasp.org/Top10/2025/"
  - "https://owasp.org/www-community/Threat_Modeling_Process"
  - "https://csrc.nist.gov/pubs/sp/800/218/final"
  - "https://csrc.nist.gov/Projects/ssdf"
  - "https://www.bsimm.com/"
  - "https://securityscorecards.dev/"
  - "https://owasp.org/www-project-proactive-controls/"
claim: "Senior teams treat security as a build-time, evidence-producing discipline — threat-model the design, push verification (SAST/DAST/secret-scan/dep-audit) left into CI as gates, and harden the supply chain (pinned actions, least-privilege tokens, lockfiles) — measured against named maturity frameworks (SAMM/ASVS/SSDF) rather than ad-hoc."
census_todo: "RESOLVED offline (gh-API=0): the Scorecard security checks are now census-backed from the `sc` field across census-governance + census-expanded — SAST (strong 24-36%), Token-Permissions (24-26%), Security-Policy (55-67%), Dangerous-Workflow (91%). Still deferred (low priority): the secret-scan TOOL share (gitleaks vs trufflehog vs GitHub secret-scanning) is not offline-derivable — the census records hold derived flags only, not workflow/tree contents; it needs a targeted workflow-content survey."
maps_from: []
---

> **Standard (claim):** Security is a build-time, evidence-producing discipline — threat-model the design, push verification (SAST/DAST/secret-scan/dep-audit) left into CI as **failing gates**, and harden the supply chain — graded against named maturity frameworks (SAMM/ASVS/SSDF), not ad-hoc.
> **Evidence:** lit (named frameworks) + census (OpenSSF Scorecard, 429→938 repos) · **Confidence:** high · **Kind:** cross-cutting · **Stage:** all

**Seed sub-aspects:** `threat modeling (STRIDE / DFD)` · `secure-by-design` · `authn / authz` · `crypto / TLS` · `SAST / DAST` · `OWASP Top 10` · `vulnerability disclosure (VDP)` · `security education`

## What professional engineers do
<!-- The reference: how senior engineers handle Application Security. One pass per seed sub-aspect, evidence-tagged. -->

- **Threat modeling (STRIDE / DFD)** — Model the *design*, not the code: draw a data-flow diagram, enumerate trust boundaries, walk STRIDE (Spoofing, Tampering, Repudiation, Info-disclosure, DoS, Elevation) per element, record mitigations + accepted risks. Done early and re-run when the design shifts; the artifact is **kept internal** (a published threat model aids attackers). `[lit]`
- **Secure-by-design / proactive controls** — Bake defenses into defaults rather than bolting them on: validate all input at trust boundaries, encode/parameterize all output (no string-built SQL/HTML/shell), deny-by-default authz, fail closed. OWASP Proactive Controls / SAMM "Design" practice is the checklist. `[lit]`
- **AuthN / AuthZ** — **Never hand-roll auth or crypto.** Delegate authentication to a vetted provider/library (OIDC/OAuth2, Argon2/bcrypt for passwords); enforce authorization server-side on every request, object-level (avoid IDOR/BOLA), least-privilege roles. Sessions: short-lived, rotated, HttpOnly/Secure cookies. `[lit]`
- **Crypto / TLS** — TLS everywhere (HSTS), modern ciphers only; use standard primitives (AEAD, libsodium) — no custom algorithms, no ECB, no static IVs. Secrets in a manager/vault, never in source; rotate keys. `[lit]`
- **SAST / DAST / SCA (shift-left)** — Static analysis (CodeQL/Semgrep), dependency/SCA scanning (Dependabot/`npm audit`/Snyk), secret-scanning (gitleaks/GitHub secret-scanning), and DAST/ZAP for running web apps — all wired into **CI as gates that fail the build**, not advisory dashboards. New findings block merge; existing debt is triaged. `[lit][census]`
- **OWASP Top 10 as the floor** — Treat the **current Top 10:2025** (broken access control, security misconfiguration, **software supply chain failures**, crypto failures, injection, insecure design, SSRF folded in, etc.) as the minimum coverage checklist for web; ASVS as the deeper, level-tiered verification standard for assurance claims. **2025 is the canonical edition** (released Jan 2026, superseding 2021); its new **A03 "Software Supply Chain Failures"** category — grown out of 2021's "Vulnerable & Outdated Components" — is the explicit **app-sec ↔ supply-chain (aspect 10) bridge**, pulling build/dependency/distribution compromise into the web-risk floor. `[lit]`
- **Supply-chain hardening** — Lockfile + reproducible installs, **pin GitHub Actions to commit SHA**, **least-privilege CI token permissions** (default read-only `GITHUB_TOKEN`), dependency review, and at the release tier: SBOM + signed/provenance-attested artifacts (SLSA). Maps to SSDF **PW** (produce well-secured) + **PS** (protect the software). `[lit]`
- **Vulnerability disclosure (VDP)** — Ship a `SECURITY.md` with a private reporting channel + response SLA; for distributed software, a coordinated-disclosure + CVE/advisory process. `[lit][census]`
- **Security education / governance** — Maturity is *measured*: SAMM/BSIMM give a scored model of the org's security practices (governance→design→implementation→verification→operations) so investment targets the weakest stream, not the loudest. `[lit]`

## Evidence (lit + census)
<!-- [lit] named papers/standards (cite URL) · [census] repo-survey numbers. Track: lit. -->

- `[lit]` **SWEBOK KA13 (Software Security)** names security as a first-class engineering knowledge area spanning the whole lifecycle.
- `[lit]` **OWASP SAMM** — assessable maturity model (5 business functions × practices, levels 1–3). **OWASP ASVS** — leveled (L1–L3) verification requirements. **OWASP Top 10:2025** — the canonical risk floor for web (released Jan 2026, supersedes 2021); notably adds **A03 Software Supply Chain Failures** (the app-sec↔aspect-10 bridge, broadened from 2021's "Vulnerable & Outdated Components"). https://owasp.org/Top10/2025/ **OWASP Threat Modeling** — STRIDE/DFD process. **OWASP Proactive Controls** — secure-by-design checklist.
- `[lit]` **NIST SP 800-218 (SSDF) v1.1** — Secure Software Development Framework: practice groups **PO/PS/PW/RV** (prepare org · protect software · produce well-secured software · respond to vulns); the supply-chain + verification spine. **NIST SP 800-218A** extends it as the **GenAI / dual-use-foundation-model** SSDF Community Profile (model-development-specific tasks) — the relevant profile to track because gingoa is an AI harness. https://csrc.nist.gov/Projects/ssdf
- `[lit]` **BSIMM** — observed (not prescriptive) data on what real firms do across 4 domains/12 practices; complements SAMM.
- `[census]` **OpenSSF Scorecard `sc` field, derived offline (gh-API=0) over both samples** — census-governance (n=429) + census-expanded (n=938), 59% coverage, recency-weighted; methodology `_schema.md` §4 (methodology). "strong" = score ≥7/10. The checks below are the **foundation-relevant subset of Scorecard's ~20 checks** (the full set also includes **SBOM**, **Webhooks**, Vulnerabilities, Binary-Artifacts, Fuzzing, Maintained, Packaging, License, Contributors, CII-Best-Practices — full list https://github.com/ossf/scorecard/blob/main/docs/checks.md). The *non-file* security floor is **low in the wild**, which is the whole reason C3 is HIGH:
  - **SAST** strong **36%** (governance n=247) → **24%** (expanded n=609) — static analysis is middling even among top repos and thins on the wider sample.
  - **Token-Permissions** (least-priv CI) strong **26%** (governance n=225) → **24%** (expanded n=502) — least-privilege CI tokens are uncommon.
  - **Security-Policy** strong **67%** (governance n=252) → **55%** (expanded n=619) — cross-validates the file census `SECURITY.md` ≈ **56%** presence.
  - **Dangerous-Workflow** strong **91%** (governance n=226) — most repos *do* avoid the worst untrusted-input → `run:` patterns (the bright spot).
  - **Code-Review enforced ~41%** — mandatory PR review is far from universal (the [lit] basis for gingoa's ③ gate); **Pinned-Dependencies** strong 20–27%, **Signed-Releases** strong 15% (cross-ref aspect 10).
- **Read of the census:** the *practices* are senior-standard `[lit]` but **adoption is thin** — so a non-engineer harness must *supply* them by default rather than assume the ecosystem will.

## Archetype variations
<!-- How this differs across archetypes. -->

- **web / api** — Highest surface: full OWASP Top 10 + ASVS, DAST/ZAP, CSP/HSTS headers, CSRF/CORS posture, rate-limiting + abuse controls, IDOR/BOLA object-level authz. Auth is **risk-zone gated** for non-engineers.
- **cli / library** — Threat surface narrows to *supply chain* (this is gingoa's own profile): pinned actions, least-priv tokens, lockfile/dep-audit, signed releases, no DAST. Input-injection still applies (argument/path/command handling).
- **mobile** — Adds secure storage (Keychain/Keystore), cert pinning, no secrets in the bundle, platform permission model.
- **data / ML** — Adds data-poisoning, model/prompt-injection, PII handling in pipelines; supply chain extends to model + dataset provenance.
- **No archetype is exempt** — secret hygiene, dependency audit, and supply-chain hardening are cross-cutting at every stage; the *depth* scales with surface and data sensitivity.

## Tradeoffs / what's ruled out

- **Gates vs. velocity** — CI security gates add latency and false positives. Ruling: gate **new** findings (block regressions), triage/baseline existing debt; never make scanners advisory-only (they get ignored).
- **Pin vs. patch lag** — SHA-pinned actions + lockfiles trade automatic patching for reproducibility/integrity; mitigated by Dependabot raising controlled bump PRs. Net: **pin, then automate updates.**
- **Hand-rolled auth/crypto is ruled out** for non-experts — the failure modes are silent and catastrophic; delegate to vetted providers, gate the rest behind expert mode.
- **Publish split** — *Executable guardrails* (secret-scan, dep-audit, pinned actions) are census-aligned config → **published**. *Narrative artifacts* (threat model, secret-flow topology, PII/retention policy) default **local/internal** — publishing them aids attackers. Ship the guardrail, keep the playbook private.
- **Maturity-model theater** — SAMM/BSIMM scoring without acting on the weakest stream is pure ceremony; min-dimension scoring (gingoa's north star) explicitly punishes the weakest link, not the average.

## Sources

- OWASP SAMM — https://owasp.org/www-project-samm/
- OWASP ASVS — https://owasp.org/www-project-application-security-verification-standard/
- OWASP Top 10 (project) — https://owasp.org/www-project-top-ten/ · OWASP Top 10:2025 (current edition, Jan 2026; A03 Software Supply Chain Failures) — https://owasp.org/Top10/2025/
- OWASP Threat Modeling — https://owasp.org/www-community/Threat_Modeling_Process
- OWASP Proactive Controls — https://owasp.org/www-project-proactive-controls/
- NIST SP 800-218 (SSDF) — https://csrc.nist.gov/pubs/sp/800/218/final · NIST SP 800-218A (GenAI/foundation-model SSDF profile) — https://csrc.nist.gov/Projects/ssdf
- BSIMM — https://www.bsimm.com/
- OpenSSF Scorecard (~20 checks, incl. SBOM + Webhooks) — https://securityscorecards.dev/ · checks list https://github.com/ossf/scorecard/blob/main/docs/checks.md

## Sub-documents
- [`facts-2026-08-security-sdlc.md`](facts-2026-08-security-sdlc.md) — *research-log (ko)* — 2026-08 facts-only pass: OWASP Top10:2025/ASVS/SAMM · MS SDL · STRIDE · SLSA · secrets management · DBIR-2026 data · CVE-2025-48757 (Lovable) facts (supply-chain content also serves aspect-10).
