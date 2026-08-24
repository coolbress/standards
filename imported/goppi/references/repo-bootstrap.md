# repo-bootstrap — git & GitHub setup for non-engineers (v0.2)

> Status: **active reference, setup-time half** — the GitHub-setup knowledge the
> `scaffold` skill uses (Phases 0–3 + settings/protection); `kickoff` asks the
> interview questions. The **daily flow** (formerly Phase 4) now lives in
> `skills/ship/SKILL.md` (S3, ADR-0021) — Phase 4 below is a pointer, not a copy.
> First customer: the goppi repo itself — an explicit, user-approved genesis
> re-initialization (the sole history-rewrite exception; it happens before any
> collaboration exists and is recorded in the design doc §12).
> v0.2: revised after independent cross-vendor review (gpt-5.6-sol, high;
> 22 findings triaged — see design doc §12, 2026-07-14).

## Problem

A non-engineer cannot set up version control, a remote, CI, or merge gates — and
does not know these exist. Without them, `ship` has no rails to run on and the
G2/G3 guarantees (resumable history, evidence-gated merges) silently degrade.
goppi therefore owns the setup, under strict disclosure rules. **Honesty about
enforcement**: on a Free-plan private repo the merge gate binds the agent (which
always obeys this flow) but is only advisory for humans and other tools; that
residual risk is disclosed, not papered over.

## Five principles

1. **Existing policy wins.** Brownfield repos keep their conventions; detect,
   never overwrite. (goppi's own genesis re-init is the documented, user-approved
   exception, not a precedent.)
2. **One bundled confirm for external/irreversible acts.** Remote creation,
   visibility, protection: explained in plain language, approved once as a
   bundle — never silently, never nagging per item.
3. **Defaults point in the reversible direction.** Private before public.
4. **Transparency manifest after setup.** What was set, why, how to undo — in
   plain language, recorded in the repo. "Automatic" must never mean "hidden".
5. **Never force ceremony.** Local-only projects get no issues/PRs; conditional
   items (releases, Dependabot, LFS) activate on detected need, not by default.

## Phase 0 — Detect (no questions asked)

- git / remote / existing `.github/`, CI, protection, templates → brownfield
  with policy: record findings, honor them, skip to Phase 4.
- `gh` auth; **owner context** (personal account vs organizations available);
  protection capability probe — on 403, distinguish plan limits from token
  scope/SSO/rate-limit via the API error body; **ambiguity → report "cannot
  verify protection", never silently degrade**.
- Project type → .gitignore, test/lint commands (CI candidates).
- **Publication-safety scan**: secret patterns across all files AND history-to-be
  (secret-guard pattern set + gitleaks if present); oversized files (>50MB warn,
  >100MB block → LFS/`.gitattributes` proposal); dependency manifests (→
  Dependabot candidate); distributable signals (package manifest, Dockerfile →
  release/tag convention candidate).

## Phase 1 — Interview (user decisions only; asked inside kickoff)

| # | Question (plain language) | Default |
|---|---|---|
| 1 | Put this project on GitHub? — benefits: backup, history, automatic checks; local-only is fine (then no issues/PRs) | yes, if `gh` ready |
| 2 | **Where and under what name?** — owner (personal / listed orgs) + repo name confirmed, not inferred | personal / directory name |
| 3 | Private or public? — private = only you. If **public**: explicit publication-authority confirmation ("this is yours to publish; no employer/client/third-party data") + license chosen from plain-language options, where "no license = all rights reserved" is a valid, explained choice. No silent license default. | **private** |

Not asked (standard setup, disclosed afterward): merge policy, templates, CI,
protection. Not asked but **recorded as triggers** (re-raised when detected):
collaborator added → require approvals & revisit CODEOWNERS; deploy/consumers
detected → release/tag convention; dependencies detected → Dependabot.

## Phase 2 — Standard setup (after one bundled confirm)

0. **Secret preflight gate** (from Phase 0 scan) — a finding blocks remote
   creation until resolved (fail-closed; same posture as the secret-guard hook).
   Enable GitHub push protection / secret scanning where the plan allows.
1. `git init` (branch `main`) + `.gitignore` + genesis commit naming the bootstrap.
2. Remote at chosen owner/name/visibility.
3. Merge policy: **squash-only** (simplest history for a non-engineer to read;
   rebase-merge is also linear but loses the PR-unit grouping), auto-delete
   merged branches, and **explicitly set BOTH squash-source settings**
   (`squash_merge_commit_title = PR_TITLE`,
   `squash_merge_commit_message = COMMIT_MESSAGES`) — linting the title alone
   doesn't control what lands on `main`, and an explicit message source makes
   the squash body deterministic: it comes from the branch commit you authored,
   not from title-derived or PR-body defaults. Note the setting alone does NOT
   prevent a multi-commit PR from squashing into a bulleted commit-list body —
   that is what Phase 4's one-commit-at-merge rule is for.
4. Templates: PR (verification section — Iron Law), issue forms — **Task/Bug
   always** (Task = internal build unit, subsumes internal feature work; Bug =
   behaves-vs-contract). **When going public or expecting external contributors**
   (community axis), add a **Feature/enhancement** form (problem-first, external
   users) **and `ISSUE_TEMPLATE/config.yml`** (blank-issues policy + security /
   discussion contact links). config.yml's contact URLs need the created repo, so
   lay it at repo-creation, not before (avoid an unresolved `OWNER` placeholder).
5. CI: narrowest real checks from Phase 0, **with a security baseline**:
   `permissions: contents: read` unless a job proves need, third-party actions
   pinned to full commit SHAs, no `pull_request_target` in generated workflows.
6. PR-title lint (Conventional Commits).
7. Protection, capability-dependent:
   - available → **solo ruleset**: PR required, 0 approvals (no one-person
     deadlock; approvals raised on the collaborator trigger), block force-push
     & deletion, linear history, **strict up-to-date base**, and required
     checks bound **only after verifying the check context reports on a probe
     PR** (locally-passing is necessary, not sufficient; no path-filtered
     required checks).
   - unavailable → convention level (CONTRIBUTING) + recorded trigger to apply
     the ruleset when visibility/plan allows, **stated as advisory, not protection**.
8. If public: README stub (what/how to run) + private vulnerability-reporting
   note (SECURITY.md) — community-profile table stakes.

## Phase 3 — Transparency manifest

Immediately after setup, report in the user's language: each item, why, one-line
undo. Recorded in the repo so any future session — or the user — can audit it.

## Phase 4 — Daily flow → owned by `skills/ship/SKILL.md` (ADR-0021)

Setup ends here; delivery begins. The depth-proportional daily flow that used
to be spelled out in this section — Direct-by-surface tiers, the Structured+
path (issue → branch → Draft PR → CI green → review before merge → fold to ONE
commit → OID-pinned squash), commit-message hygiene (no local-only info;
`Co-Authored-By` as the only trailer), session boundary, and the never-rules —
is encoded in **`skills/ship/SKILL.md`**, the single authoritative home of the
daily flow (one home, no drifting copies; sync direction reference → skill).
Setup hands off to it: once Phases 0–3 are done, deliver via ship.

## Evidence
- [census] Lineage audit 2026-07-14 (design doc §12; archives are private — cited as internal evidence): claudeck-v1 0 PRs by design → v2 5/5 → gingoa 54/37 with elicit-visibility, scaffold transparency manifest, confirm-gated solo ruleset with green-CI binding — every element here has a field-tested ancestor.
- [lit-internal] codex-native github-workflow + merge-execution (Draft-PR-early, squash-by-policy, OID pin, no-issue path for small low-risk changes); the precursor constitution §12·§13 (archived locally; captured in `docs/decisions/0010-delivery-workflow.md`).
- [lit] Independent review 2026-07-14 (gpt-5.6-sol, high): 22 findings; accepted items folded into v0.2 — secret preflight (GitHub push-protection docs), Actions least-privilege + SHA pinning (GitHub secure-use, OpenSSF Scorecard), required-check context verification & strict checks (GitHub protected-branches docs), owner/name + publication-authority as user decisions (GitHub repo-creation/visibility docs), surface-based Direct tier, squash-message source setting, 403 disambiguation (GitHub REST troubleshooting), public community-profile items. Triage record in design doc §12.
- [lit] GitHub REST tested 2026-07-14: rulesets/protection 403 on Free private.
- [lit] code.claude.com/docs/en/permissions (2026-07-14): Bash patterns fragile → merge gates live in host/remote, not contract text.
- [lit-internal] Observed failures 2026-07-21/22 in goppi's own history: multi-commit PRs #20/#22 squashed under `COMMIT_MESSAGES` into bulleted bodies with mid-body trailer blocks; host-injected `Claude-Session:` trailers reached the repo's permanent history in #18/#20/#22. Rules codified in ADR-0017 addendum; carried here only until `ship` existed — migrated to `skills/ship/SKILL.md` Evidence 2026-07-22 (ADR-0021).

## Expiry conditions
- ~~Built into a `ship` skill (S3) → this becomes that skill's reference.~~ **Fired 2026-07-22 for the daily-flow half** (Phase 4 → `skills/ship/SKILL.md`, ADR-0021); the setup half (Phases 0–3 + settings/protection) remains this document, used by `scaffold` (the interview half already lives in `kickoff`).
- Host or `gh` ships an equivalent guided bootstrap for non-engineers → keep only goppi deltas (transparency manifest, depth tiers, secret preflight posture).
- GitHub extends rulesets to Free private repos → delete the degradation row and its trigger machinery.
