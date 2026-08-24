# Verification

Match evidence to the contract that changed.

For a material code change, run the narrowest existing relevant check before editing when it is affordable and useful. Record pre-existing failures so the final result does not attribute them to the change or hide a regression. Skip the baseline for trivial edits or when it would be disproportionately expensive, and say so when the distinction matters.

## Evidence ladder

1. Static checks for syntax, formatting, types, schemas, or configuration validity.
2. Focused tests for the changed behavior.
3. Integration checks at affected boundaries.
4. End-to-end or visual checks for user-visible critical paths.
5. Broader regression suites only when the change radius or repository policy justifies them.

Do not substitute a lower rung when the acceptance criterion requires a higher one. Do not run every rung by default.

## Before declaring completion

- Confirm the command actually executed the intended path.
- Inspect failures rather than rerunning blindly.
- Check the resulting diff or artifact for unintended changes.
- Record exact checks and outcomes.
- Distinguish passing, skipped, unavailable, and not applicable checks.
- For research, separate source evidence, calculation, inference, and unresolved uncertainty.

When no automated check exists, create the smallest reproducible manual or artifact-based verification available. State clearly that it is not equivalent to an automated regression test.
