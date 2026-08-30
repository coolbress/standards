---
id: aspect-06-config-secrets
title: "Configuration & Secrets Management"
group: "F — Foundation & Build"
kind: cross-cutting
gated_archetypes: []
cross_cutting: true
lifecycle_stages: ["all"]
anchors: ["12-Factor-III", "NIST-SP-800-53-IA"]
evidence_track: census+lit
status: review-needed
last_updated: "2026-06-25"
sources:
  - "https://12factor.net/config"
  - "https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final"
  - "https://github.com/gitleaks/gitleaks"
  - "https://openfeature.dev/specification/"
claim: "Senior engineers externalize all config to the environment (12-Factor III), keep zero secrets in source (CI secret-scanning + a managed store with rotation), validate config at startup so misconfig fails fast, and gate runtime behavior behind feature flags rather than redeploys."
census_todo: "Token-Permissions (least-priv CI) now census-backed offline (gh-API=0) from the Scorecard `sc` field — strong 24-26% across census-governance + census-expanded. Still deferred (low priority): secret-scan-TOOL share (gitleaks vs trufflehog vs GitHub secret-scanning) and feature-flag adoption (OpenFeature/LaunchDarkly) are not offline-derivable — the census records hold derived flags only, not workflow/tree contents; sharpening the publish decision needs a targeted workflow-content survey."
maps_from: []
---

> **Standard (claim):** Externalize config to the environment, hold **zero** secrets in source (CI scanning + managed store + rotation), validate config at startup (fail-fast), and flip runtime behavior with feature flags — not redeploys.
> **Evidence:** [lit] 12-Factor III + NIST SP 800-53 (IA/SC); [census] env_example 18→**36** wtd (n=429) · **Confidence:** High (config); Medium (flags/rotation, lit-led) · **Kind:** cross-cutting · **Stage:** all

**Seed sub-aspects:** `typed config + startup validation` · `feature flags` · `secret stores / rotation` · `no-secrets-in-source (gitleaks)` · `multi-env promotion` · `drift detection`

## What professional engineers do

- **Typed config + startup validation** — config is read once at boot into a typed, validated schema (zod/pydantic-settings/envconfig), and the process **refuses to start** on a missing/invalid value. Misconfig surfaces at deploy, never as a 3am runtime `undefined`. A committed `.env.example` documents every key (value-less); the real `.env` is gitignored. [lit][census]
- **No secrets in source** — secrets never enter git, not even history. Enforced two ways: a **CI secret-scanner** (gitleaks/trufflehog) on every push *and* a pre-commit hook to catch them before they land; plus GitHub **push protection / secret scanning** as a backstop. A leaked credential is treated as compromised → rotate, don't just delete the commit. [lit]
- **Secret stores + rotation** — runtime secrets live in a managed store (cloud secrets manager, Vault, or the platform's encrypted env), injected at deploy/run time, never baked into images or config files. Access is least-privilege and audited; high-value secrets **rotate** on a schedule, with short-lived/dynamic credentials (e.g. OIDC-federated cloud creds) preferred over long-lived static keys. Maps to NIST SP 800-53 **IA** (identification/authentication) + **SC-12/SC-28** (key management, protection at rest). [lit, normative]
- **Feature flags** — runtime behavior (rollouts, kill-switches, A/B, ops toggles) is gated behind flags so changes ship **decoupled from deploys** and roll back instantly without a redeploy. Vendor-neutral via the **OpenFeature** spec; flags carry an owner + expiry so they don't rot into permanent dead branches. [lit]
- **Multi-env promotion** — config differs **only by environment** (dev/staging/prod), supplied externally; the same artifact is promoted unchanged across stages — config is injected, not rebuilt. This is the operational payoff of 12-Factor III: build once, configure per-env. [lit]
- **Drift detection** — declared config/infra (IaC, declarative manifests) is reconciled against live state; drift (manual prod edits, divergent env vars) is detected and flagged rather than silently tolerated. GitOps tooling (Terraform plan, Argo/Flux) makes the desired state the source of truth. [lit]

## Evidence (lit + census)

- **[lit] 12-Factor App, factor III "Config":** "store config in the environment" — strict separation of config from code; the litmus test is whether the codebase could be open-sourced without leaking credentials. https://12factor.net/config
- **[lit, normative] NIST SP 800-53 Rev. 5** (confirmed Sep 2020, upd1 Dec 2023): credential/secret handling maps to the **IA** (Identification & Authentication), **SC-12** (cryptographic key establishment & management), and **SC-28** (protection of information at rest) control families. https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- **[lit] gitleaks** — de-facto OSS secret scanner; runs as a pre-commit hook and a CI/GitHub Action gate. https://github.com/gitleaks/gitleaks
- **[lit] OpenFeature** (CNCF) — vendor-neutral feature-flag API/SDK specification, decoupling flag evaluation from any single provider. https://openfeature.dev/specification/
- **[census] env_example** (dev-env census, n=429): uniform **18%** → recency-**weighted 36%** (young-cohort 37%, Δ+18) — the largest upward trend-mover in the foundation census, read as "modern apps externalize config (12-Factor III)."
- **[census] Token-Permissions** (OpenSSF Scorecard `sc`, derived offline gh-API=0; least-priv/CI-hardening sub-aspect): strong **26%** (governance n=225, mean 2.6/10) → **24%** (expanded n=502) — least-privilege CI `GITHUB_TOKEN` scoping is uncommon even among elite repos, so the harness must default it. (Source: census-governance + census-expanded `sc`; methodology `_schema.md` §4 (methodology).) Secret-scan TOOL share and feature-flag adoption are **not** offline-derivable (see `census_todo`).

## Archetype variations

- **web-app / backend (service archetypes):** full stack applies — `.env.example`, startup validation, managed secret store, multi-env promotion, and feature flags for safe rollout. The census surfaces `.env.example` specifically for **web-app·backend**.
- **CLI / library:** little/no runtime secret surface; config is flags/config-files, not a secrets store. Feature flags and secret stores are largely **N/A**; the live concern collapses to **no-secrets-in-source** (a published package leaking a token is catastrophic) — so secret-scanning still applies, the rest mostly doesn't.
- **Not a gated aspect** — it is cross-cutting and fires at every lifecycle stage; intensity scales with how much runtime + secret surface the archetype has.

## Tradeoffs / what's ruled out

- **Ruled out:** secrets committed to git (incl. history), secrets baked into build artifacts/images, config hard-coded per-environment forcing per-env rebuilds, and unbounded "temporary" feature flags that become permanent dead code.
- **Tradeoff — flags add complexity:** every flag is a branch in state-space and a testing/cleanup burden; justified for rollout safety/kill-switches, over-applied it rots. Mitigate with owner + expiry metadata.
- **Tradeoff — rotation vs. friction:** aggressive rotation is operationally costly; the senior move is short-lived/federated credentials (OIDC) so rotation is automatic rather than a manual chore.
- **Tradeoff — startup validation strictness:** fail-fast can block a deploy on a benign-looking missing optional var; the fix is a typed schema that distinguishes required vs. optional-with-default, not relaxing validation.

## Sources
- https://12factor.net/config
- https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- https://github.com/gitleaks/gitleaks
- https://openfeature.dev/specification/

## Sub-documents
- [`config-validation-secrets--facts-2026-08.md`](config-validation-secrets--facts-2026-08.md) — *research-log (ko)* — 2026-08 facts-only pass (R2-1): 환경변수 기반 설정 · **시작 시점 설정 검증은 국제 표준 부재, 프레임워크 기능으로만 존재**(확인된 결론) · 시크릿 저장/회전(AWS·GCP·Azure·HashiCorp — 회전 주기의 구체값은 어느 문서에도 없음) · GitHub secret scanning이 스스로 밝힌 탐지 한계.
