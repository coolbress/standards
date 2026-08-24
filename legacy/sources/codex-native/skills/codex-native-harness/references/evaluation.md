# Harness Evaluation

Evaluate the harness on real tasks before adding complexity.

## Semi-automatic improvement loop

Use this loop to preserve high-signal learning without allowing the harness to rewrite itself:

1. **Observe** — Detect a user correction, verification contradiction, false completion, unauthorized mutation, material independent-review finding, or repeated routing overhead.
2. **Propose** — Convert the event into a minimal sanitized summary. Store no raw proprietary code, private documents, credentials, or full conversation trace. Run `python3 scripts/eval_loop.py propose --help` for the proposal schema.
3. **Approve** — A proposal remains non-binding until the user explicitly approves evaluation. The CLI records an operator attestation; it cannot authenticate that a human spoke, so invoke `approve` only after explicit user approval. Attestation makes the proposed case evaluable but does not edit `evals/cases.json` or the harness.
4. **Reproduce** — Run approval-attested cases in fresh isolated contexts. Keep the author and evaluator contexts separate. An operator-attested trial record requires a unique session identifier, exact model and configuration fingerprint, a comparison-group key shared only by matched harness/native conditions, a sanitized UTF-8 outcome artifact, the sanitized trace artifact, and grader JSON that covers every applicable variant criterion. The private runtime ledger retains permission-restricted copies and revalidates their hashes, sizes, grader schema, trace linkage, and expected-criteria coverage on every status check. This preserves evidence but does not authenticate the claimed Codex session; do not call it trusted telemetry without a trusted adapter.
5. **Compare** — Evaluate both the current harness and native Codex baseline on the same acceptance criteria. Use deterministic checks first and calibrated human or model judgment only where needed.
6. **Recommend** — Report evidence, regressions, overhead, and eligibility. Require a reviewed plugin change for any instruction, script, routing, or lifecycle update.

The default runtime directory is `$CODEX_NATIVE_EVAL_DIR` when set. Otherwise use `$CODEX_HOME/state/codex-native/evals`, falling back to `~/.codex/state/codex-native/evals`. Keep mutable evidence outside Skill and plugin package trees. Override it with `--data-dir` for repository-specific or temporary evaluation work. If the sandbox does not allow the dedicated state directory, request the narrow write permission instead of silently falling back into the Skill tree.

Older versions stored state under `$CODEX_HOME/skills/.state/codex-native/evals`. Run `python3 scripts/eval_loop.py migrate-state` once to copy legacy state into the dedicated directory. Migration refuses conflicts and never deletes the legacy copy automatically.

Secret scanning is defense in depth, not a complete DLP system. Summarize before invoking the CLI; never rely on `--sanitized` or pattern matching to make raw private content safe.

Fixture command assertions execute subprocesses without a shell. Bundled fixtures are reviewed plugin code. Treat any custom `--cases` or `--fixtures` file as executable code; the runner refuses custom files unless `--allow-custom-fixtures` is explicitly supplied after review.

The loop must never automatically:

- capture raw task content or secrets;
- promote a proposal into the bundled regression suite;
- modify this Skill or its plugin;
- change `evals/manifest.json` lifecycle status;
- merge, deploy, or broaden external authority.

Useful commands:

```bash
python3 scripts/eval_loop.py audit
python3 scripts/fixture_runner.py validate
python3 scripts/fixture_runner.py materialize --case-id direct-local-fix --output /tmp/codex-native-eval
python3 scripts/fixture_runner.py grade --case-id direct-local-fix --variant harness --workspace /tmp/codex-native-eval --trace /tmp/trace.json
python3 scripts/eval_loop.py propose --help
python3 scripts/eval_loop.py approve --help
python3 scripts/eval_loop.py plan --variant harness
python3 scripts/eval_loop.py record --help
python3 scripts/eval_loop.py status
python3 scripts/test_eval_loop.py
```

## Task set

Maintain representative cases for:

- a trivial request that must not trigger process overhead;
- a localized code change;
- an ambiguous multi-file feature;
- diagnosis without unauthorized fixing;
- a high-risk or destructive request;
- research with evidence and source-quality requirements;
- a genuinely parallel task and a falsely parallel task;
- a blocked task that must stop honestly.

## Measures

Track:

- outcome success and acceptance-criteria coverage;
- verification quality and false completion rate;
- regressions or unintended mutations;
- unnecessary plans, questions, tools, Skills, and subagents;
- user intervention count;
- elapsed time, tool calls, and token cost;
- clarity for a nontechnical user.

Grade the observable end state and acceptance criteria rather than requiring one exact tool trajectory. Use deterministic graders where possible, human review for subjective quality and safety, and model graders only after calibration against human judgments.

Run multiple trials for nondeterministic behaviors before treating a change as an improvement. Retain traces when diagnosing failures, but do not optimize for attractive traces at the expense of the outcome.

Start error analysis from real failures and user corrections. Use synthetic cases to fill known coverage gaps, not as a substitute for observing actual use. Every bundled case must reference a reproducible fixture with exact seed files, observable assertions, and deterministic checks where possible. Test tool removal as well as tool addition; remove a capability when ablation shows no meaningful outcome loss.

When a case fails, grade the end state first, identify the earliest upstream decision or tool/context failure that made success unlikely, and only then analyze downstream symptoms. Turn repeated failure categories into focused regression cases.

## Change gate

Compare the current version against the proposed change on the same cases. Grade shared outcome and safety criteria for both native and harness variants; grade trigger and routing criteria only for the harness. Require the manifest's minimum number of distinct model/configuration combinations and matched harness/native comparison groups before evidence can be considered complete. Adopt added instructions, scripts, or routing only when they improve important outcomes without creating disproportionate overhead or new failure modes. Prefer simplifying or deleting guidance when stronger models make it redundant.

Keep lifecycle state in `evals/manifest.json`, representative prompts in `evals/cases.json`, reproducible fixture contracts in `evals/fixtures.json`, and dated historical evidence under `evals/results/`. Treat a partial run as partial evidence, not a release-grade regression result.

Treat `status` as advisory. Promotion requires full gate satisfaction plus human review of the evidence and the proposed diff. A passing report never grants authority to update the manifest automatically.
