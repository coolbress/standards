---
id: aspect-05-scm-workflow
title: "SCM & Development Workflow"
group: "F — Foundation & Build"
kind: cross-cutting
gated_archetypes: []
cross_cutting: true
lifecycle_stages: ["all"]
anchors: ["SWEBOK-KA8", "DORA-trunk", "Conventional-Commits"]
evidence_track: census+lit
status: review-needed
last_updated: "2026-07-05"
sources:
  - "https://dora.dev/capabilities/trunk-based-development/"
  - "https://www.conventionalcommits.org/en/v1.0.0/"
  - "https://itrevolution.com/product/accelerate/"
  - "https://scorecard.dev/"
  - "https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches"
  - "https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners"
  - "https://semver.org/"
claim: "Senior teams work on short-lived branches off trunk (≤3 active, merged daily) protected by required PR review + green CI, with Conventional Commits feeding automated versioning/changelog and CODEOWNERS gating ownership — a workflow whose protective half (review-before-merge, branch protection) is rare in the wild and so is exactly what a non-engineer harness must default-on."
maps_from: ["census-data/census-governance"]
census_todo: "RESOLVED offline (gh-API=0): branch-protection + review-enforcement now census-backed from the Scorecard `sc` field in census-governance (n=118/252) + census-expanded (n=313/619) — Branch-Protection strong 10-13% / present 47-62%, Code-Review-enforced strong 41%. Still deferred (low priority): tree census cannot see branch lifetime / merge cadence (trunk-based signal) or merge_method config — converting the [lit] DORA trunk claims into [census] adoption % needs a targeted workflow/API survey of branch-age distribution + merge-method."
---

> **Standard (claim):** Senior teams integrate to **trunk on short-lived branches** (≤3 active, merged ≥daily), guarded by **required PR review + green CI** on a protected default branch, with **Conventional Commits** driving automated semver/changelog and **CODEOWNERS** gating ownership.
> **Evidence:** [lit] DORA/Accelerate, Conventional Commits, SemVer, GitHub branch-protection · [census] 429-repo governance survey + OpenSSF Scorecard · **Confidence:** high (workflow shape) / medium (trunk cadence is [lit]-only, not tree-censusable) · **Kind:** cross-cutting · **Stage:** all

**Seed sub-aspects:** `branching (trunk / GitHub-flow)` · `Conventional Commits` · `CODEOWNERS` · `PR workflow` · `merge / branch-protection` · `monorepo vs poly-repo` · `release-train cadence`

## What professional engineers do
<!-- The reference: how senior engineers handle SCM & Development Workflow. One pass per seed sub-aspect, evidence-tagged. -->

- **Branching = trunk-based / GitHub Flow.** One long-lived `main`; all work on **short-lived feature branches** (hours, not weeks) merged back continuously. DORA's ~~measured~~ **survey-derived** rule: **≤3 active branches**, **merge to trunk ≥ once/day**, **no code freezes / integration phases** — these correlate with elite delivery performance. [lit] ⚠️ **2026-08-25 한정 병기 (배치 5)** — 세 수치는 dora.dev 원문 그대로이나, 근거는 페이지 자신이 밝히듯 *"Analysis of DORA data from **2016** and **2017**"*, 즉 **State of DevOps 설문 분석**이다. 저장소 계측도 무작위 배정도 아니므로 ***"measured"* 라는 표현을 내렸다** — [`github-workflow-current`](github-workflow-current.md) **GHW-009·010**. 같은 페이지가 *"requires multiple approvals"* 인 무거운 리뷰를 **trunk-based development 채택의 장애물**로 든다(**GHW-011**). GitHub Flow is the lightweight default; heavyweight GitFlow (long release/develop branches) is now an anti-pattern for continuously-deployed software. [inferred]
- **Conventional Commits.** Structured commit subjects (`type(scope): summary`, e.g. `feat:`, `fix:`, `feat!:`) so tooling can derive **SemVer bumps + changelogs** mechanically. [lit] In a squash-merge model the **PR title** (not every WIP commit) becomes the conventional commit — enforced by a `pr-title` CI check. [inferred] **[census]** (500 top-starred, `census-data/census-issue-pr/`, 2026-06-26): enforcing CC *PR titles* is **substantial-but-minority** — strict (≥70% of titles) **34%**, partial 57%, mean 0.45 — so it is an **⚖️ above-strict-census** choice, justified where the repo **squash-merges** (PR title = the landed commit → changelog/semver automation). *Issue* titles stay **plain** (CC ≈ 2% in the wild) — never force a type prefix on issues. **[census — widened N=2000, 2026-07-05 (`census2k.py`, top-2000-by-stars software)]** the minority read *strengthens* at 4× the sample: CC PR-titles strict **21%**, partial **41%**, mean **0.33**; issue-title CC ≈**1%**. So "PR title = Conventional Commits" is confirmed an **above-census senior opinion** (an automation *enabler*, not an industry baseline — tension T1), and "issue title = plain summary" is confirmed near-universal.
- **PR workflow + branch protection.** Change lands only via PR; the protected default branch **requires ≥1 review and passing status checks** before merge, blocks direct pushes, and disallows force-push/history rewrite. This is the non-bypassable gate (vs. local pre-commit hooks, which `--no-verify` can skip). [lit]
- **Issue-before-PR is size-conditional, NOT universal.** The dominant norm (and GitHub Flow itself) lets **trivial / small / follow-up changes go straight to a PR**; an **issue first is expected only for non-trivial** work (new feature / API / architecture / breaking) where a maintainer could reject the whole *direction* and waste the implementation. The test is "non-trivial," not a line count. A strict *issue-required-for-every-non-trivial-PR* minority (~20–25%) exists (Django "non-typo PR without a ticket is closed", Go "excluding very trivial, connect to an issue", TypeScript approved-issues-only) — correlated with language-core / scarce-maintainer projects; Homebrew is the opposite (PR-preferred, "do not open both"). [lit, normative] (11-project + GitHub-flow sample, `census-data/issue-vs-pr-norm/`, 2026-06-28). For gingoa: small docs/spec-clarification/follow-up PRs need **no preceding issue**; the issue-first gate is reserved for direction-uncertain / API / architecture changes (already served by the ADR + spec process).
- **Merge strategy.** Teams pick one canonical strategy — **squash-merge** (clean linear history, one commit per PR, pairs with PR-title convention) is the common modern default; rebase-merge for strict linearity; merge-commits where preserving branch topology matters. [inferred] **[census]** (250 repos, 4041 squash commits, `census-data/census-commit-body/`): **76% squash-merge**; the landed commit standardly carries a **summary body (73%**, median ~475 chars), a **CC subject (48%)**, and a **`Co-Authored-By` trailer (36%** — pair/bot/AI-assisted; the de-facto attribution trailer, gingoa mandates it on *every* commit incl. the squash body). Issue-closing keywords sit in only **7% of commit bodies** — issues are usually linked via the PR (description/sidebar), not the squash body, so `Closes #N` in the body is correct-but-above-census (harmless double-link).
- **CODEOWNERS.** A `.github/CODEOWNERS` file maps paths → reviewers so the right owners are auto-requested and (with "require review from code owners") **gate** merges to their area. Primarily a **monorepo / multi-team** tool. [lit][census]
- **Monorepo vs poly-repo.** Monorepos add **workspace config** (pnpm-workspace/turbo/nx), path-scoped CODEOWNERS, and selective/affected-build CI; poly-repos keep per-service isolation. Either is senior-valid; the choice is an explicit foundation decision, not a default. [inferred]
- **Release-train cadence.** Versioning is **SemVer**; releases are tag-driven and (ideally) automated from the Conventional-Commits history. Cadence ranges from continuous (per-merge) to scheduled trains — see aspect 04 release-ops. [lit]

## Evidence (lit + census)
<!-- [lit] named papers/standards (cite URL) · [census] repo-survey numbers. Track: census+lit. -->

- **[lit] DORA — trunk-based development.** Branches "last no more than a few hours"; ≤3 active branches + daily merge + no code freezes predict higher delivery/operational performance; trunk-based is a *required practice for CI*. (DORA capabilities; rooted in Accelerate, Forsgren/Humble/Kim 2018.)
- **[lit] Conventional Commits 1.0.0** — the structured-commit spec enabling automated SemVer + changelog. **[lit] SemVer 2.0.0** — the version-contract it feeds.
- **[lit] OpenSSF Scorecard** — supplies the non-file evidence below via its public API (`api.securityscorecards.dev`).
- **[census] 429-repo governance survey** (top-star GitHub, recency-weighted `w=0.5^(age/2yr)`, Scorecard coverage 59%):
  - **Code-Review enforced ≈ 41%** strong (mean 5.3/10) — *required PR review is the minority, not the norm.* This is the non-file basis for gingoa's ③ review gate.
  - **Branch-Protection ≈ 13%** strong (mean 2.9/10; only n=118 judgeable without admin token) — protected `main` is **rare** even among elite repos.
  - **CI-Tests 100%** strong (mean 9.8, small n=31) and **Dangerous-Workflow 91%** — where CI exists it is taken seriously; CI itself sits at **92%/91%** (simple/weighted) adoption in the file census.
- **[census] Protective-gate adoption (Scorecard `sc`, derived offline, gh-API=0):** the review-before-merge + branch-protection half of the claim is now census-grounded across both samples — **Branch-Protection** strong **10–13%** / present **47–62%** (governance n=118 mean 2.9; expanded n=313 mean 2.2), **Code-Review enforced** strong **41%** (governance n=252; expanded n=619). Branch-Protection's lower n reflects an honest coverage limit (the check needs admin/visibility). Read: protected `main` + required review are a *minority* even among elite repos → exactly the gate a non-engineer harness must default-ON. (Source: census-governance + census-expanded `sc`; methodology `_schema.md` §4 (methodology).)
- **[census] Conventional-Commits `pr-title` automation ≈ 8–14%** (simple/weighted) — an honest minority; adopted as an *enabler*, not claimed universal (tension T1).
- **[census] merge-method + PR-template at N=6,582** (`census-data/census-governance-floor/`, 2026-07-05; top-starred software, star-floor 29, 3.3× the prior 2000-repo set): of resolved repos **squash-merge is allowed 97%**, merge-commit 74%, rebase 81% — squash is **near-universally available**, grounding a squash-first default (note *allowed* ≠ *enforced-only*). **PR-template presence 29% overall** but **46% in the node ecosystem** (61% in monorepos) — the wider/deeper N lowers the aggregate yet the node/go/rust reference class stays substantial-minority-to-majority. Strict CC PR-titles hold at **~21%** at this N — confirming CC-title enforcement is a senior default, not a census majority (tension T1).
- **[census] CODEOWNERS ≈ 32–33%** overall, concentrated in monorepo/multi-team repos.
- **[census] planning/governance artifacts thin at birth** — any-planning-artifact 13/19/17% (simple/weighted/young), reinforcing that workflow rigor is something a harness must *add*, not inherit.

## Archetype variations
<!-- How this differs across archetypes. -->

- **Universal (all archetypes):** trunk + short-lived branches, PR-only, protected `main`, Conventional Commits / PR-title check, SemVer. No archetype is *gated out* of the core workflow.
- **monorepo / multi-team:** **CODEOWNERS** becomes load-bearing (path-scoped ownership gates); workspace config + affected/selective CI; stricter required-reviewers. (Governance survey: monorepo `adr_pct` 6%, anyplan 20% — highest planning rigor of the archetypes.)
- **library / cli / published:** release-train + SemVer discipline is tighter (a published version contract); Conventional Commits pays off most here (auto-changelog). Library lockfile is 🟨 (commit recommended but softer than apps).
- **web-app / backend:** lean toward **continuous** cadence (per-merge deploy), so short-lived branches + daily merge matter most; less ceremony around release tagging.
- **solo / non-engineer (gingoa's user):** same workflow shape, but the *protective* defaults (review-before-merge, branch protection) carry extra weight because there is no peer to catch a broken `main` push.

## Tradeoffs / what's ruled out
- **GitFlow / long-lived release+develop branches — ruled out** for continuously-delivered software: large, painful merges and stabilization phases, the opposite of DORA's ≤3-branch / daily-merge finding. Acceptable only for explicitly versioned, slow-cadence shipped products.
- **Pre-commit hooks as the *gate* — ruled out** as the sole control: locally bypassable (`--no-verify`). They are a fast-feedback *helper*; the real gate is **CI + branch protection** (tension T3).
- **Conventional Commits is an opinion, not a universal** (census 8–14%): adopted as an automation enabler with eyes open; not asserted as industry baseline. A team that hand-writes changelogs is not "wrong" (tension T1).
- **Mandating every WIP commit be conventional — ruled out** in a squash model: enforce at the **PR title**, not each intermediate commit (lower friction, same automation payoff).
- **Strict-linear (rebase) vs squash vs merge-commit:** no single winner; pick one and enforce consistency. Inconsistency is the real defect.

## Sub-documents

- [`github-enforcement-boundaries--facts-2026-08`](github-enforcement-boundaries--facts-2026-08.md) — *research-log (ko)* — 2026-08 표적 조사: 룰셋 플랜 게이트의 **API 실패 모양** 실측(403 문구·n=3)과 **이슈 폼 `required`가 REST/CLI 경로에 걸리지 않는다**는 사실. 가시성×플랜 매트릭스 본체는 04에 있다.
- [`github-workflow-current`](github-workflow-current.md) — current GitHub product facts, bounded defaults, and a risk-scaled control matrix. Prefer this verified note over inherited prescriptive claims in this file.

## Sources
- DORA — Trunk-based development: https://dora.dev/capabilities/trunk-based-development/
- Conventional Commits 1.0.0: https://www.conventionalcommits.org/en/v1.0.0/
- Accelerate (Forsgren/Humble/Kim 2018): https://itrevolution.com/product/accelerate/
- OpenSSF Scorecard: https://scorecard.dev/
- GitHub — About protected branches: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
- GitHub — About code owners (CODEOWNERS): https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners
- SemVer 2.0.0: https://semver.org/
