# Independent Review

Use review to find defects the authoring context is likely to rationalize or overlook. Tests remain the primary proof for deterministic behavior; review covers assumptions, omissions, risk, maintainability, and qualities that tests do not fully grade.

## Select the gate

- Skip a separate reviewer for routine Direct work after focused tests and diff inspection.
- Require one independent pass for material Structured work, public contracts, broad regressions, auth or permission logic, money, data integrity, migrations, security, concurrency, or subjective user-facing quality.
- Require independent review for Governed completion and before a GitHub merge when the repository workflow applies.

## Preserve independence

Give the reviewer the requested outcome, acceptance criteria, actual diff or artifact, and verification results. Do not provide the author's conclusion that the work is correct or ask the reviewer to confirm it.

Use a fresh context that did not author the change. The reviewer may be another Codex agent, a detached Codex review, a qualified human, or a different frontier model. Cross-model review adds diversity; it is optional unless the user or repository policy requires it.

Run the first review read-only. Require file-and-line or artifact evidence for actionable findings. Reject unsupported style preferences and praise-only reviews.

## Close the loop

1. Triage each finding against the actual artifact.
2. Fix only evidence-backed issues within scope.
3. Rerun affected checks.
4. Re-review changed high-risk surfaces when the fix materially altered them.
5. Report unresolved findings and missing reviewer coverage; never claim independent review when only self-review ran.

Do not create an unlimited reviewer loop. One pass is normally enough for Structured work. Governed work may iterate until acceptance-critical findings are resolved or a blocker is explicit.
