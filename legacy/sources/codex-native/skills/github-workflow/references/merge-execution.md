# Merge execution

Use these details only after the repository policy, exact PR, target branch, head OID, checks, review state, and final diff are verified.

1. Prefer the repository's required merge method. Use squash only for a single-purpose PR when policy permits it.
2. Derive the final commit title from repository convention. If no stricter convention exists, use `type(scope): imperative summary (#<PR-number>)` for a squash commit while keeping the PR title free of the suffix.
3. Inspect the installed `gh pr merge --help` before relying on optional safety flags. When supported, pin the verified head commit and set the subject explicitly. Add the required body when repository policy calls for one.
4. Never treat an example command as authorization. Merge only within the user's established delivery request and report the resulting state.

Example shape, subject to current CLI support and repository policy:

```bash
env -u GITHUB_TOKEN gh pr merge <PR-number> --squash --subject '<verified-subject>' --match-head-commit <verified-head-oid>
```
