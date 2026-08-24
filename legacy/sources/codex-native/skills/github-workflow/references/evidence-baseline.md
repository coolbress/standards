# Evidence baseline

Use this snapshot as orientation, not as a universal policy. Refresh material claims from the source artifacts or current official documentation when they affect a decision.

## Gingoa repository census snapshot

Source corpus: `/Users/coolbress/gingoa/docs/research/`, reviewed 2026-07-11. Primary local sources:

- `census-data/README.md` documents the sampling and raw-evidence layout.
- `three-tier-ledger.md` synthesizes governance and issue/PR decisions.
- `_schema.md` defines the `[lit]`, `[census]`, and `[inferred]` evidence tracks and warns that publication frequency and sound engineering practice answer different questions.

Observed signals:

- `[census]` The governance-floor survey covers 6,582 public repositories with a star floor of 29 and archetype/ecosystem strata. Its own caveat reports ecosystem skew, including Java over-representation and Python under-counting; Gingoa therefore uses Node/Go/Rust as a closer reference class for its product decisions.
- `[census]` The widened issue/PR convention pass covers the 2,425 **template-bearing** repositories found in that pool: 3,248 issue forms, 20,837 fields, and 1,077 PR templates. Within that conditional subset, help text appears on **87.20% of input-like issue-form fields** (owner-cluster 95% interval **86.09–88.31%**) and textarea is the dominant prose control at about 53%; a "type of change" section appears in about 12% of sampled PR templates. These are not population-wide repository rates and do not require copying every common form. Updated sources: `census-data/census-issue-pr/robustness.json` and `census-data/census-issue-pr/robustness-report.md`.
- `[census]` Gingoa's synthesis reports CI as common, while strong branch protection and required review are materially less prevalent. This is evidence that repository presence is not the same as control adequacy.
- `[census]` Gingoa reports squash merge as highly prevalent in its sampled governance data, but merge policy remains repository-specific and history-sensitive.
- `[inferred]` An issue-authoritative, one-responsibility branch/worktree, early Draft PR, selective staging, CI/review gate, and squash-by-default flow is a coherent professional baseline for scoped Codex work. It is a synthesis, not a direct census statistic.

## Interpretation rules

1. Do not infer causality or quality from prevalence.
2. Do not generalize a public, star-filtered OSS sample to private, regulated, enterprise, or solo repositories without qualification.
3. Prefer stratified/archetype results over the pooled percentage when they conflict.
4. Treat repository observations as clustered by owner/organization and ecosystem. Do not present naive field-level or repository-level intervals as independent population certainty; seek owner-cluster sensitivity and correct denominators for material claims.
5. Treat irreversible or commitment-bearing choices—licensing, disclosure promises, destructive history changes, production deployment—as explicit user decisions regardless of popularity.
6. Distinguish an artifact's presence from its adequacy and enforcement. Likewise, distinguish a green CI job from acceptance-critical tests that actually ran; inspect skips and conditional dependencies.
7. Use current `[lit]` official GitHub and Codex documentation for product capabilities, permission behavior, rulesets, and merge semantics; those are temporally unstable.

## Native Codex boundary

`[lit]` Current official Codex documentation describes these native surfaces:

- Settings > Git controls branch naming, force-push policy, commit-message prompting, and PR-description prompting; review delivery can be inline or detached.
- The review pane covers unstaged, staged, commit, branch, and last-turn diffs, including per-hunk/file staging and inline comments.
- Built-in Git tools can stage/revert chunks or files, commit, push, and create a PR; use the integrated terminal for gaps.
- Managed worktrees isolate tasks, start on detached `HEAD`, allow "Create branch here" and local/worktree handoff, and cannot share one checked-out branch. Ignored files transfer only through `.worktreeinclude`; the app manages worktree cleanup.

Sources (verify current behavior before relying on it):

- <https://learn.chatgpt.com/docs/developer-settings#git>
- <https://learn.chatgpt.com/docs/code-review>
- <https://learn.chatgpt.com/docs/environments/local-environment#use-built-in-git-tools>
- <https://learn.chatgpt.com/docs/environments/git-worktrees>

Use this skill for classification, evidence discipline, sequencing, GitHub governance, and verification. If the app does not expose a required setting or remote operation, use the connected GitHub capability or `git`/`gh` and report the fallback.
