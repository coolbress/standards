---
name: github-workflow
description: Inspect, establish, and execute an evidence-aware Git and GitHub delivery workflow while complementing Codex's native Git, diff, review, branch, and worktree UX. Automatically use for repository GitHub delivery or governance work involving issues, branches, worktrees, commits, pull requests, CI, review, merge, rulesets, templates, or safe bootstrap. Do not use for generic local coding questions or a read-only diff review that Codex's native review workflow already covers.
---

# GitHub Workflow

Use Codex's native Git diff, staging, commit, branch, worktree, push, PR, and review affordances whenever they cover the operation. Respect the app's configured branch naming, force-push policy, commit prompt, PR-description prompt, and review delivery mode. Add judgment, repository policy, remote governance, and reproducible checks with this skill; do not recreate native UI.

Invoke this workflow implicitly when the user's repository task enters GitHub delivery or governance scope; the user does not need to name the skill. Read-only inspection is safe to perform automatically. Do not treat implicit invocation as authorization to create or change issues, branches, worktrees, commits, pushes, PRs, rulesets, templates, CI, or merge settings: make those mutations only when the user's setup, configuration, or delivery request authorizes them. Report every material external change and its resulting URL or state.

## Inspect before prescribing

1. Run `python3 scripts/inspect_repo.py <repo>` for a read-only local inventory.
2. Read the nearest applicable `AGENTS.md`, repository constitution, contribution guide, issue/PR templates, CI workflows, and release policy. Repository and explicit user rules override this skill.
3. Inspect status, current branch, remotes, history, worktrees, and existing user changes. Never reset, delete, clean, or rewrite work merely to obtain a clean tree.
4. Inspect GitHub repository, issue, PR, checks, rulesets, and merge settings through the connected GitHub capability. Use `git` for local state and `gh` when native/connected coverage is insufficient, especially for push and Actions logs.
5. Classify the context before selecting controls:
   - lifecycle: no history, established, or migration;
   - collaboration: solo, team, or external contributors;
   - visibility: private, internal, or public;
   - archetype: library, CLI, service, application, monorepo, infrastructure, or data/ML;
   - risk: reversible/local, compatibility/data, security/compliance, deployment, or irreversible.

If evidence or configuration may have changed, verify it rather than relying on this skill's snapshot.

## Separate evidence from policy

Label material recommendations in audits and PR rationale:

- `[lit]`: an official standard, product document, or peer-reviewed source;
- `[census]`: an observed repository-survey result;
- `[inferred]`: a context-specific decision or synthesis.

Never convert adoption frequency directly into a mandate. Use census data to describe prevalence and compatibility, literature to establish sound practice, and project risk/context to decide. Read [references/evidence-baseline.md](references/evidence-baseline.md) when setting or auditing conventions. Read [references/codex-native-settings.md](references/codex-native-settings.md) when configuring the Codex app's Git and review settings.

## Choose the delivery path

### Existing issue workflow

Treat the GitHub Issue as the authoritative unit when the repository or user requires issue-based work.

1. Confirm one primary responsibility, acceptance criteria, risks, and verification evidence in the issue.
2. Use `codex/<issue-number>-<short-slug>` unless repository instructions specify another pattern.
3. Create an independent worktree for the issue. In a Codex-managed worktree, create the branch before committing because managed worktrees begin on detached `HEAD`. Assign only one writer per worktree; parallel agents receive separate worktrees and non-overlapping scopes. Remember that one branch cannot be checked out in two worktrees and ignored files move only through an intentional `.worktreeinclude` rule.
4. Open a Draft PR early after the branch exists remotely and the proposed scope is coherent. Link the issue with GitHub closing syntax when merge should close it.
5. Keep commits intentional and the PR single-purpose. Update the issue or split work when scope materially expands.

### Authorized issue creation

When issue creation is authorized, search open and recently closed issues for duplicates, select the repository's template, and confirm title, labels/milestone/assignee only from known metadata. Record one responsibility, context and rationale, acceptance criteria, risks, and verification plan. After merge, verify the linked issue actually closed; close or update it only when authorized and the acceptance criteria are satisfied.

### Small or local-only work

Do not create GitHub objects merely because they are available. For a read-only audit, experiment, or explicitly local change, stop at the requested boundary. Propose an issue/PR transition before making an external representational change when authorization is absent.

### No-history bootstrap

Preserve all existing files. Inventory and test the working tree, then form logical commits without pretending there is a mergeable branch history. Establish the remote/default branch and initial baseline before creating dependent worktrees or PRs. Do not use checkout/reset as a migration shortcut.

### Non-repository path

If inspection reports no Git repository, inventory the files and stop for direction. Do not run `git init`, add a remote, or publish anything without authorization.

## Implement and stage safely

1. Re-read status immediately before editing and staging.
2. Change only issue-scoped files. Preserve unrelated tracked, untracked, and ignored user work.
3. Prefer native diff review and selective staging. Inspect the staged diff separately; never rely on `git add .` in a mixed tree.
4. Run focused tests during implementation, then repository-required gates. Record exact commands and outcomes.
5. Inspect skipped, deselected, quarantined, and conditional tests plus missing optional dependencies. A green command is not evidence for a critical path that did not execute.
6. Review dependency, generated-file, schema, migration, security, and compatibility effects in proportion to risk.
7. Use Conventional Commits for commit subjects unless a stricter repository convention applies: `type(scope): imperative summary`. Keep each commit to one logical change. Do not amend, force-push, or rewrite shared history unless explicitly authorized and safe.

## Prepare the PR

Write a precise title and body using the repository template. If no template exists, include:

- purpose and linked issue;
- technical and, where relevant, economic rationale;
- acceptance criteria mapping;
- changes made and intentionally excluded;
- exact test/CI evidence;
- risks, migration or rollback notes, and remaining follow-ups.

Use a Conventional Commit PR title unless a stricter repository policy applies: `type(scope): imperative summary`. Do not manually append `(#<PR-number>)` to the PR title; reserve that suffix for the final squash commit on the default branch.

Keep the PR Draft until its acceptance criteria and local gates are satisfied. Mark it ready only when reviewable as a complete unit.

## Gate and merge

1. Require repository CI and applicable independent review before merge. Verify required checks exercise the acceptance-critical paths and that rulesets enforce the intended gate; presence alone is not adequacy. Do not bypass a failed, skipped-critical, or missing required check.
2. Resolve actionable review threads and rerun affected checks. Keep scientific, engineering, security, and deployment approvals distinct when the project does.
3. Use squash merge by default for a single-purpose PR only when repository policy permits it. Preserve commits when they carry meaningful independent history or the repository mandates another method.
4. Immediately before merge, verify the exact PR number, target branch, head commit OID, title, checks, review state, and final diff. Never push directly to the default branch when the selected workflow requires PRs.
5. Derive the final merge method, commit title, body, and safety flags from verified repository policy and current tool capabilities. When squash is selected and no stricter convention exists, use a Conventional Commit subject and preserve PR traceability. Read [references/merge-execution.md](references/merge-execution.md) only when an authorized merge is actually being prepared.
6. Never rewrite already-merged default-branch history merely to add or repair the PR-number suffix; apply the rule prospectively.
7. After merge, verify the resulting checks/state and report issue, branch, PR, and merge URLs plus status. Delete branches/worktrees only when requested or clearly safe and no work would be lost.
8. Treat a verified merge and linked-issue closure as the default task boundary. Unless the user explicitly requested continuous roadmap execution, do not start a materially separate next issue in the same thread; report the candidate and recommend a fresh task with a concise handoff instead.

## Report uncertainty

Distinguish confirmed configuration from recommendation. State when rulesets, permissions, authentication, CI logs, or native Codex app settings could not be inspected. Never imply an external object or app setting was changed unless the operation succeeded.
