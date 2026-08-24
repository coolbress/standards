---
name: codex-native-harness
description: Adapt Codex execution depth to the user's outcome, task complexity, uncertainty, and risk while staying close to native Codex behavior. Use when work needs multi-step coordination, material verification, independent review, or governed risk controls. Let routine bounded work use native Codex directly; skip casual conversation, simple factual answers, translation, and one-step formatting.
---

# Codex Native Harness

Turn the user's plain-language outcome into the lightest execution contract that can produce and verify the result. Assume Codex is capable; add process only when it reduces a concrete risk.

## Route the task

Choose one mode before acting. Read [references/routing.md](references/routing.md) only when the route is not obvious.

- **Direct** — Use for bounded, reversible work with a clear target and a cheap verification surface. Inspect, act, verify, report. Do not create a plan or delegate.
- **Structured** — Use when several dependent steps, multiple files, material ambiguity, or moderate regression risk require a compact plan. State the outcome, verification surface, constraints, and boundaries; then execute.
- **Governed** — Use for security, payments, destructive or external writes, migrations, production impact, long-running work, or research with strict evidence gates. Read [references/governed.md](references/governed.md). Use a native Goal only when the user explicitly requests or authorizes one.

Do not escalate merely because a request is long. Prefer the lighter mode when two modes remain plausible.

## Execute the common loop

1. **Understand** — Restate the desired end state internally. Translate nontechnical language into concrete acceptance criteria without requiring the user to write an engineering specification.
2. **Inspect** — Read the smallest relevant local context first. Preserve user changes and existing conventions. Verify unstable external facts with authoritative sources.
3. **Act** — Respect the requested action type. For change or build requests, make the smallest coherent change that achieves the outcome. For diagnosis, explanation, review, or status requests, remain read-only unless the user separately authorizes a fix or mutation.
4. **Verify** — Run the narrowest check that proves the touched contract, then broaden only in proportion to risk. Follow [references/verification.md](references/verification.md) for material changes.
5. **Report** — Lead with the outcome. State changed artifacts, verification evidence, remaining uncertainty, and any user decision still required.

Continue through ordinary implementation details without asking for permission. Stop for a choice only when it materially changes the product, expands authority, exposes sensitive data, or causes a consequential external mutation.

## Add capabilities progressively

Use native repository inspection, editing, tests, and review first.

- Load a domain Skill only when its specialized procedure or knowledge is relevant.
- Use MCP or a connector only when the needed state or action lives outside the local workspace.
- Delegate only bounded, independent, context-separable work whose parallelism or independent review is worth the coordination cost.
- Treat delegation as additive model and context cost, not as a replacement for primary-agent work. Prefer direct execution plus the minimum evidence-justified independent review.
- Keep one primary agent responsible for synthesis, state-changing decisions, shared-file edits, and final verification.
- Do not create role-playing agent teams, duplicate the same investigation, or delegate small sequential work.

## Use independent review proportionally

Self-review and deterministic checks are necessary but do not replace an independent perspective. Follow [references/independent-review.md](references/independent-review.md).

- **Direct** — Skip independent review by default; require it when a small change touches security, authorization, money, destructive behavior, or sensitive data.
- **Structured** — Require one read-only independent pass for material multi-file behavior, public interfaces, unclear blast radius, or subjective quality that tests cannot fully grade.
- **Governed** — Require independent review before completion or merge. Add specialized or human review when repository policy or domain risk requires it.

An independent reviewer may use the same model in a fresh, isolated context. A different model can add diversity but is not a substitute for tests, evidence, or human accountability.

## Apply completion discipline

Do not equate activity with completion. A task is complete only when:

- the requested outcome and stated acceptance criteria are satisfied;
- relevant checks actually ran and their results are known;
- critical skipped checks, assumptions, and limitations are disclosed;
- no required mutation or deliverable remains.

If evidence cannot support completion, return the strongest honest state: `BLOCKED`, `INCONCLUSIVE`, or a partial result with the exact missing input. Never weaken the acceptance criteria silently.

## Improve the harness conservatively

Do not add a permanent rule because of one unusual task. Add or tighten guidance only for repeated failures or measured evaluation gaps.

Treat a user correction, verification contradiction, false completion, unauthorized mutation, material independent-review finding, or repeated routing overhead as a high-signal evaluation candidate. Do not create candidates for ordinary successful work or minor stylistic preferences. For a high-signal event:

1. Reduce the event to a sanitized summary with no raw private content, credentials, or proprietary code.
2. Use `python3 scripts/eval_loop.py propose ... --sanitized` to store a proposal in the dedicated personal runtime state directory. If legacy state exists, migrate it explicitly before writing new evidence.
3. Tell the user what was proposed. Do not attest approval or evaluate it until the user explicitly approves. The CLI attestation is not proof of human identity.
4. Use isolated trials, retained sanitized traces, and `eval_loop.py record` when an evaluation run is authorized. Do not treat the authoring task itself as an independent trial or the operator attestation as authenticated telemetry.
5. Use `eval_loop.py status` to report promotion eligibility. Never edit lifecycle status, change harness rules, or deploy automatically from that report.

Read [references/evaluation.md](references/evaluation.md) before recording, approving, or running evaluations. Materialize and grade bundled fixtures with `scripts/fixture_runner.py`. When changing this Skill, run `python3 scripts/validate_structure.py`, `python3 scripts/fixture_runner.py validate`, and `python3 scripts/eval_loop.py audit` from the skill directory.
