---
id: aspect-04-build-ci-engineering--visibility-provision-matrix
title: "Provision-by-visibility matrix — what the ② floor can/can't do on private vs public"
parent: aspect-04-build-ci-engineering
kind: research-log
evidence_track: lit
status: review-needed
last_updated: "2026-06-26"
method: "Authoritative GitHub-Docs survey (2026-06-26) of which security/foundation features are gated by repo VISIBILITY × PLAN, + the free/OSS alternative for each gated feature. Built so the ② foundation build can DETERMINISTICALLY provision a floor from the user's private/public choice (the elicit ① contract sets it)."
---

# Provision-by-visibility matrix (②)

Why this exists: the ② floor is **not visibility-neutral**. Several "must-have" GitHub-native features are
gated behind repo visibility + plan, so the ② build MUST branch on the user's `private`/`public` choice (a ①
contract field) and emit the right floor + an OSS substitute when a native feature is blocked. This is the
machine-actionable form of the repo-context conditioning rule (`_schema.md §4`).

## Feature availability (verified against GitHub Docs, 2026-06-26)
Columns: **PUB** = public (free) · **PRIV-free** = private, Free plan · **PRIV-paid** = private, Pro/Team +
GitHub Code Security / Secret Protection add-on (Team is the min base to *buy* the add-ons; Pro-personal
cannot).

| Feature | PUB | PRIV-free | PRIV-paid | Gated by |
|---|---|---|---|---|
| CodeQL code scanning | ✅ | ⛔ | ✅ (Code Security) | GHAS/Code-Security on private |
| Secret scanning + push protection | ✅ | ⛔ | ✅ (Secret Protection) | GHAS/Secret-Protection on private |
| **Dependabot alerts** | ✅ | **✅ free** | ✅ | — (free on private!) |
| Dependabot security updates | ✅ | ✅ | ✅ | needs dep-graph + alerts (both free) |
| Dependabot **version** updates | ✅ | ✅ | ✅ | works; **caveat** ↓ (GitHub-Packages npm) |
| Branch protection / rulesets | ✅ | ⛔ | ✅ | Pro/Team for private |
| Required PR reviews + CODEOWNERS *enforcement* | ✅ | ⛔ | ✅ | rides branch protection |
| Private vulnerability reporting | ✅ | ⛔ | ⛔ | **public-only by design** |
| Environments + required reviewers | ✅ | ⛔ | ✅ | Pro/Team for private |
| Actions minutes | ✅ unmetered | ⚠️ 2,000/mo | ⚠️ 3,000/mo | metered on private |
| OpenSSF Scorecard (publish + SARIF) | ✅ | ⚠️ partial | ⚠️ partial | publish_results = public-only; SARIF needs Code-Security |

**npm version-update caveat (all private repos):** Dependabot version updates work for **public-registry**
deps on a private repo. The footgun is only when the repo hosts/consumes packages on **GitHub Packages /
a private registry** — then `GITHUB_TOKEN` is insufficient and you need a checked-in `.npmrc` (URL only) +
a `registries:` block with a PAT (`read:packages`). *(gingoa's earlier "npm auto-routes to GitHub Packages"
deferral may be over-stated — gingoa's deps are all public-registry; **revisit: re-test Dependabot-npm, or
adopt Renovate** which handles private registries natively without the PAT footgun.)*

## Free / OSS substitute for each gated feature (works regardless of visibility)
| Gated native feature | OSS substitute | Note |
|---|---|---|
| CodeQL | **Semgrep OSS** (`semgrep scan --config p/…`) | SARIF as Actions artifact; no Security tab without Code-Security |
| Secret scanning + push protection | **gitleaks** (CI + pre-commit) · TruffleHog (adds live-credential verify) | pre-commit gitleaks is *better* than push-protection — blocks before the push |
| Dependabot alerts | (already free on private) `pnpm audit` + **OSV-Scanner** | OSV.dev = same advisory DB |
| Dependabot security/version updates | **Renovate** (`vulnerabilityAlerts.enabled`) | more capable; native private-registry support; no `.npmrc`/PAT footgun |
| Branch protection / required review | **no true substitute** — CI-block-on-PR (required status via `pull_request` trigger) | force-push bypass still possible; document the gap |
| Environments + required reviewers | manual `workflow_dispatch` approval gate | not equivalent |

## Provision decision table (what ② emits)
**PRIVATE-default floor (Free plan):** Semgrep SAST job · gitleaks (CI + pre-commit) · `pnpm audit` + OSV-Scanner ·
Renovate (or re-tested Dependabot) · CI four-check gate (note 2,000-min/mo budget) · Scorecard with
`publish_results:false` + JSON artifact · **SKIP w/ a logged NOTICE:** branch protection, required-review,
environments, private-vuln-reporting (— "requires Pro/Team or public; tracked as a launch deferral").

**PUBLIC-default floor (Free plan):** CodeQL default-setup · enable secret-scanning + push-protection · Dependabot
(or Renovate) · **branch-protection ruleset** + `required_approving_review_count:1` + CODEOWNERS · environments
w/ required reviewers · enable private-vulnerability-reporting · Scorecard `publish_results:true` (+`id-token:write`,
use *rulesets* not classic protection to avoid the admin-PAT Branch-Protection check) · unmetered CI.

## What FLIPS when a private repo goes public (the ②→launch mutation)
1. Semgrep → **CodeQL** (swap the SAST job). 2. enable **secret-scanning + push-protection**. 3. **branch
protection ruleset** on. 4. **required PR review + CODEOWNERS** enforced. 5. **environments + required
reviewers**. 6. enable **private-vulnerability-reporting**. 7. Scorecard → `publish_results:true` (+badge).
8. drop the Actions-minutes notice (now unmetered). 9. (optional) Dependabot-npm PAT may become unnecessary
for public-registry deps. → This is the `--make-public` codemod the ②/launch tooling should encode.

## Sources
GHAS overview https://docs.github.com/en/get-started/learning-about-github/about-github-advanced-security ·
GitHub plans https://docs.github.com/get-started/learning-about-github/githubs-products · CodeQL private-repo
gate https://docs.github.com/en/code-security/code-scanning/troubleshooting-code-scanning/cannot-enable-codeql-in-a-private-repository ·
push protection https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection ·
protected branches https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches ·
rulesets https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets ·
environments https://docs.github.com/actions/deployment/targeting-different-environments/using-environments-for-deployment ·
Actions billing https://docs.github.com/en/billing/concepts/product-billing/github-actions · private vuln reporting
https://docs.github.com/en/code-security/security-advisories/working-with-repository-security-advisories/configuring-private-vulnerability-reporting-for-a-repository ·
Dependabot private registries https://docs.github.com/en/code-security/dependabot/working-with-dependabot/guidance-for-the-configuration-of-private-registries-for-dependabot ·
Renovate bot comparison https://docs.renovatebot.com/bot-comparison/ · Scorecard action https://github.com/ossf/scorecard-action/blob/main/README.md
