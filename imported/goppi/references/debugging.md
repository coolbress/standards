# Debugging — trace → hypothesis → fix → verify (G3)

The four-step discipline for any defect, with one rule that has teeth:
**no fix without a trace**. A code change justified only by "probably this"
is not a fix — it is a guess wearing a fix's clothes, and it passes review
only by luck.

**Load path**: consumed when a defect is being fixed or a fix is being
judged — the `review` skill's stage-2 audit (an untraced fix is a reviewable
finding) and the `governed` skill's evidence gates point here.

## The four steps

1. **Trace** — reproduce the failure and read the actual failing output
   before theorizing. The trace is concrete: the exact command, input, and
   observed wrong behavior (error text, wrong value, diff), reduced to the
   smallest reproduction that still fails. If the failure cannot be
   reproduced or observed, say so — `BLOCKED`/`INCONCLUSIVE` beats a blind
   patch (clause 4).
2. **Hypothesis** — one falsifiable cause statement tied to the trace:
   "X causes the observed Y; if true, Z will also be observable." Check Z
   before editing. Multiple candidates → order by evidence, test the top one;
   do not shotgun-edit several at once (a fix that changes five things proves
   none).
3. **Fix** — the smallest change that addresses the traced cause. A fix that
   grows beyond the cause is scope creep in a defect's clothing; split it.
4. **Verify** — re-run the exact trace from step 1 and watch it pass, then
   the rung the change's blast radius requires
   (`references/verification-ladder.md`: baseline-before-change,
   anti-substitution, failures inspected — never re-run blindly).

## The rules with teeth

- **No fix without a trace.** Applies to reported defects too: a reviewer's
  or user's claim is a hypothesis, not a trace — **reproduce before fixing**.
  Practiced precedent [goppi-internal]: all six review-#2 code defects were
  reproduced directly before being fixed, and the injection guard was deleted
  on *reproduced* false-positives and evasion, not on the reviewer's word
  (design §12, 2026-07-15).
- **An untraced fix is a reviewable finding** (review stage 2): a diff whose
  author cannot state its trace — what failed, how it was reproduced, and
  which command now shows it passing — is unverified regardless of green
  gates.
- **The trace outlives the fix**: the reproduction lands in the delivery
  artifact (test case where expressible, else the recorded before/after
  commands) so the defect cannot silently return.

## Evidence

- [census] superpowers `systematic-debugging` + claudeck v1 lineage (design
  §9 port table row: "debugging 4-stage discipline") — the four-step shape
  and the no-guess rule are the field-tested core of that lineage.
- [goppi-internal] The reproduce-before-fix practice is goppi's own record
  (§12 2026-07-15, above). Honest basis note: the baseline record contains
  **no observed fix-without-trace failure incident** — this reference exists
  on census lineage + explicit maintainer request (2026-07-24), not on a
  reproduced in-house failure; if such an incident is ever observed, add it
  here.
- [lit-internal] design §4.2 references target set names this file;
  verification-ladder is the sibling this discipline hands off to at step 4.

## Expiry conditions

- Host ships a native debugging discipline (trace-first flow, repro-required
  gating) → keep only the no-fix-without-a-trace rule if the native flow
  lacks it.
- Two review cycles where no finding ever cites the trace rule → this file is
  restating clause 4; fold the tooth into `references/verification-ladder.md`
  and delete.
