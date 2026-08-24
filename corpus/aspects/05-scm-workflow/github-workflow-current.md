---
id: aspect-05-scm-workflow--github-workflow-current
title: Current GitHub workflow — evidence and bounded defaults
parent: aspect-05-scm-workflow
kind: reference
status: verified
last_updated: 2026-08-02
evidence_track: lit
freshness: volatile
review_due: 2026-11-02
sources:
  - GITHUB-FLOW
  - GITHUB-PR
  - GITHUB-DEPLOY
  - GITHUB-ACTIONS-SECURE
---

# Current GitHub workflow — evidence and bounded defaults

This note separates GitHub's current product facts from a recommended workflow. GitHub
documents mechanisms; it does not prescribe one universal issue, branch, review, merge,
or deployment policy for every project.

## Claim table

| Claim ID | Class | Claim and scope | Evidence | Confidence | Valid as of / expiry |
|---|---|---|---|---|---|
| GHW-001 | vendor-behavior | GitHub Flow is a branch-based workflow: create a branch, make and commit changes, open a pull request, address review, merge, then delete the branch. | `GITHUB-FLOW` | high | 2026-08-02; review 2026-11-02 |
| GHW-002 | vendor-behavior | A pull request brings conversation, commits, checks, and file changes together and exposes merge readiness; repository settings determine mandatory gates. | `GITHUB-PR` | high | 2026-08-02; review 2026-11-02 |
| GHW-003 | vendor-behavior | Branch protections or rulesets can require reviews and checks; environments can add reviewers, waits, and branch restrictions; merge queues retest queued changes against the current base. Availability varies by configuration and plan. **구체 경계(Free+비공개=불가)는 [`github-enforcement-boundaries--facts-2026-08`](github-enforcement-boundaries--facts-2026-08.md) GEB-001·002 · 2026-08-24 실측.** | `GITHUB-DEPLOY` | high | 2026-08-02; review 2026-11-02 |
| GHW-004 | vendor-behavior | Reverting a merged pull request creates a new pull request that reverses the merge; complex or conflicting changes can require a manual revert. | `GITHUB-DEPLOY` | high | 2026-08-02; review 2026-11-02 |
| GHW-005 | vendor-behavior | GitHub recommends minimum necessary `GITHUB_TOKEN` permissions and says only a full-length commit SHA is immutable when pinning an action. | `GITHUB-ACTIONS-SECURE` | high | 2026-08-02; review 2026-11-02 |
| GHW-006 | synthesis | GitHub Flow does not itself require an issue, a commit-message convention, squash merging, a particular reviewer count, or a deployment strategy. These are project policy choices. | `GITHUB-FLOW`; `GITHUB-PR` | medium-high | review when GitHub Flow changes |
| GHW-007 | synthesis | A defensible default path is isolate change → automated verification → risk/ownership-proportional review → protected merge → observable deployment → recoverable rollback. This is a recommended control chain, not a GitHub-mandated standard. | `GITHUB-FLOW`; `GITHUB-PR`; `GITHUB-DEPLOY`; `GITHUB-ACTIONS-SECURE` | medium | review 2026-11-02 |

## Risk-scaled application

| Context | Minimum defensible controls |
|---|---|
| Solo, local-only experiment | Small branch or isolated worktree; local checks; reversible commits. |
| Solo, remotely published repository | Required automated checks; protected default branch where practical; explicit self-review evidence. |
| Team repository | Checks plus ownership-aware review; branch protection/rulesets; clear merge policy. |
| Production deployment | Environment protection, least-privilege workflow permissions, pinned dependencies/actions, observable rollout, and tested rollback. |

Independent human approval may be impossible in a one-person project. That limitation
must be stated rather than simulated; automated checks, protected merges, and an
independent model review can reduce risk but are not equivalent to accountable peer review.

## Do not infer

- Repository prevalence is not proof that a practice is effective.
- A green check is not proof that requirements are satisfied; it proves only the configured checks passed.
- A pull request is not automatically an independent review.
- A squash-first or Conventional Commits policy can be useful, but neither is imposed by GitHub Flow.

## Sources

- [GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow)
- [About pull requests](https://docs.github.com/en/pull-requests/get-started/about-pull-requests)
- [Deploying code](https://docs.github.com/en/pull-requests/concepts/deploying-code)
- [Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use)
