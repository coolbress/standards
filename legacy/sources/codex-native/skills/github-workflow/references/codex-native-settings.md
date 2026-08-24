# Codex native Git settings baseline

These are contextual UI values, not claims that settings were applied. Repository policy overrides every default. Computer Use cannot configure the Codex app itself in this environment, so enter and verify them in the app UI.

## Suggested values

- **Branch naming:** use `codex/<issue-number>-<short-slug>` for issue-backed work. Use `codex/<short-slug>` only when repository policy allows low-risk work without an issue.
- **Force push:** Off. If an exceptional history rewrite is explicitly authorized, repository policy permits it, and no collaborator work is endangered, use `--force-with-lease` outside the app and verify the lease.
- **Commit-generation prompt:** `Describe one logical change in imperative form. State the outcome and why when useful. Do not claim tests, review, or behavior that was not verified.`
- **PR-description prompt:** `Include purpose and issue link, technical/economic rationale where relevant, acceptance-criteria mapping, changes and exclusions, exact tests including skips or missing dependencies, risks and rollback, and material [lit]/[census]/[inferred] evidence labels.`
- **Review delivery:** Detached by default for independent review. Use Inline for tight iterative fixes where immediate diff-local feedback is the goal.

## Native capability sources

- Git settings: <https://learn.chatgpt.com/docs/developer-settings#git>
- Review modes and diff scopes: <https://learn.chatgpt.com/docs/code-review>
- Managed worktrees: <https://learn.chatgpt.com/docs/environments/git-worktrees>
- Built-in Git tools: <https://learn.chatgpt.com/docs/environments/local-environment#use-built-in-git-tools>
