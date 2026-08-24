# Verification ladder — what "verified" means, rung by rung (G3)

The Iron Law (contract clause 4) says a done-claim needs an executed command and
its read output. This reference answers the next question: **which** command is
enough evidence for **which** claim. Verification is a ladder — pick the rung
the acceptance criterion actually requires, never a cheaper one that merely
looks green.

**Load path**: consumed at the moments verification is chosen or judged — the
`ship` skill's `## Verification` reporting (status vocabulary, rung choice),
the `review` skill's stage-2 rung audit, and the `governed` skill's standing
rules all restate the core inline and point here for the full version.

## Baseline before change

For a **material change** (touches a public interface, data flow, or an
irreversible surface — design §8 terminology), run the **narrowest existing
relevant check before editing**, when one exists and running it is affordable.
Record what already fails, so the final result neither blames pre-existing
failures on the change nor hides a regression behind them ("it was already
red"). Skip the baseline for trivial edits or when it costs more than the
change itself — and say so when the distinction matters.

## The five rungs

1. **Static** — syntax, formatting, types, schema/config validity.
2. **Focused** — the test(s) for the changed behavior specifically.
3. **Integration** — checks at the boundaries the change touches.
4. **End-to-end / visual** — user-visible critical paths, seen working.
5. **Broad regression** — full suites, only when the change radius or the
   project's policy justifies the spend.

**Anti-substitution (the rule with teeth)**: never substitute a lower rung when
the acceptance criterion requires a higher one — a passing type-check is not
evidence that behavior changed correctly. The converse holds too: do not run
every rung by default; ceremony is proportional (§2 value 3).

## Reading a result honestly

- A green command is evidence **only for the paths it actually executed**:
  inspect skipped, deselected, quarantined, and conditional tests before
  counting a suite as coverage. Presence of a check is not adequacy of a check.
- Status vocabulary — report each check as exactly one of **passing** (ran,
  green), **failing** (ran, red — with output), **skipped** (deliberately not
  run, with reason), **unavailable** (the environment cannot run it — a
  blocker, not a failure), or **not-applicable** (the criterion doesn't apply).
  Conflating "unavailable" with "passing" is a false completion; conflating it
  with "failing" manufactures a fake product defect (the same rule
  `hosts/codex/smoke-test.sh` applies to its own prerequisites).
- Failures are inspected, not re-run blindly; the diff/artifact is checked for
  unintended changes before claiming the change is what was intended. (When
  the failure becomes a fix, the full discipline is `references/debugging.md`:
  trace → hypothesis → fix → verify — no fix without a trace.)
- **No automated check exists?** Build the smallest reproducible manual or
  artifact-based verification — and state plainly that it is not equivalent to
  an automated regression test.
- **`cmd 2>&1 | tail` reports the wrong exit code.** In a pipeline the shell
  returns the *last* command's status, so `tail`'s success masks `cmd`'s
  failure — and the check that was supposed to gate the claim silently passes.
  Capture the status of the command itself (`cmd > out 2>&1; rc=$?`, or
  `set -o pipefail`) before reading the tail. Any "it printed fine so it
  passed" reading of a piped command is a rung-0 verification wearing rung-2
  clothes.
- **Remedy discipline — a failing check names {what · why · one-line remedy}.**
  A red result that says only *what* broke hands the reader a search problem on
  top of the defect; the *why* is what lets them judge whether it matters here,
  and the remedy is what makes the check actionable by someone who did not write
  it. goppi holds its own deterministic layer to this — `evals/*.sh`,
  `hosts/goppi-doctor.sh`, `deploy-check`, `run-pair.sh`. The rule is kept from
  rotting into a claim by `evals/remedy-discipline.test.sh`, which drives **17
  real failure paths** and reads their real output rather than grepping source
  text. Coverage is a sample, not a proof — `deploy-check`'s two advisories are
  still undriven (they were audited by hand and do comply). Adding a checker
  means adding its failure path there too.

## The circuit breaker — three strikes, then stop

**When the same task has failed its verification three times, stop and report.**
Not a fourth attempt, not a different phrasing of the third: hand the problem
back with four things, and wait.

1. **The exact command** — verbatim, as run, with its working directory.
2. **Its full output** — not a summary, not the last line. The reader cannot
   re-derive what you elided.
3. **What you already tried** — each attempt and what changed between them, so
   nobody repeats a dead end you have already paid for.
4. **The suspected root cause** — your best current hypothesis, explicitly
   labelled as a hypothesis. "I don't have one" is a legitimate answer and is
   more useful than a guess dressed as a finding.

The rule exists because the failure mode it stops is expensive and quiet: a
model that keeps re-running a failing check accumulates plausible-looking edits
against a cause it never traced, and each one widens the diff a human will later
have to unpick. Three failures is evidence the *model* of the problem is wrong,
not that the fix needs another coat of paint — and a wrong model is exactly the
thing more attempts cannot fix. This is `references/debugging.md`'s "no fix
without a trace" with a counter attached: the trace requirement says *how* to
fix; the breaker says *when to stop trying to*.

Two boundaries keep it from becoming an excuse to quit early:

- **It counts failures of the same task, not of the session.** Three unrelated
  checks failing once each is an ordinary day; the same check failing three
  times is the signal.
- **Stopping is a report, not a silent abandonment.** `BLOCKED` and
  `INCONCLUSIVE` are correct outcomes (contract clause 4) — a completion claim
  padded over three failures is not.

## Evidence

- [census] claudeck v1 — the three-strike breaker and its four-field report are
  ported from that harness's rule set. goppi's addition is the same-task scoping
  and the tie into the clause-4 status vocabulary; the count (three) is
  inherited, not independently derived, and nothing here has yet measured
  whether three is the right number.
- [census] codex-native-harness `references/verification.md` (v0.3.1) — the
  ladder shape, baseline-before-change, anti-substitution, and the
  passing/skipped/unavailable/not-applicable vocabulary are ported from its
  field-tested rules (the prose was exercised in daily use; its eval matrix
  never was — ADR-0023). The "green ≠ executed-path evidence" rule is the same
  lineage (github-workflow SKILL test-adequacy rule).
- [goppi-internal] The measured G3 incidents (design §11: the S1 "23/23
  passing" false completion; the NPV-ranking and special-dividend bugs caught
  only by rung-2 execution) — the ladder exists because rung confusion was
  goppi's own observed failure mode.
- [lit-internal] design §4.2 references target set names this file; contract
  clause 4 is the always-on summary this reference expands.

## Expiry conditions

- Host ships a native verification policy (baseline capture, rung selection,
  or skipped-check disclosure) → keep only the anti-substitution rule and the
  status vocabulary if the native flow lacks them.
- Two review cycles where no finding ever cites a rung distinction → this
  reference is restating the contract; fold the ladder into clause 4's line
  and delete the file.
