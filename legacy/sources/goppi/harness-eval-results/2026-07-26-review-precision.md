# pair — review precision: harness vs vanilla on a seeded-bug corpus, 2026-07-26 (Session F, F-d)
<!-- genre: pair -->

The run `skills/review/SKILL.md`'s expiry condition asks for: *"S4 eval shows
same-vendor fresh-context reviews catch ≈nothing beyond `./check.sh`…"*. Until
now the review layer's evidence was anecdote — a strong one (Session G's review
found 11 findings and failed stage 1) but unscored and graded by the same driver
whose work it reviewed.

Scoring, arms, and **what would count as evidence against the layer** were fixed
in `tasks/review-precision/task.md` **before any spend**.

## Result

| | recall (seeded bugs caught) | false positives (HIGH/MED on a non-defective file) | cost | host time |
|---|---|---|---|---|
| **vanilla** | **8 / 8** | **0 / 14** | $0.8867 | 125.9 s |
| **harness** (contract + review skill) | **8 / 8** | **1 / 14** | $0.6997 | 98.0 s |

Per-arm tokens (host-reported): vanilla in 10 · out 9,428 · cache-create 13,986 ·
cache-read 135,476 — harness in 8 · out 7,006 · cache-create 13,020 · cache-read
88,915. Driver wall time 130.7 s / 102.6 s. **Pair total $1.5864**, inside the
approved $5 band. Scoring is deterministic (`verifier.sh`); no judge model ran.

The single false positive: the **harness** arm flagged
`adversarial-fixtures/a05-import-in-string.py:3` under its `### MEDIUM` section.
Vanilla made the *same observation* about the same line and filed it under
`### LOW`, where the rule does not count it.

## The pre-registered rule fired — and it is the bad one

task.md, written before the run:

> **The layer looks harmful** if the harness arm's FP count is *higher* than
> vanilla's. The demotion ladder's whole purpose is the opposite; a reviewer that
> over-flags *more* because it read our skill is a defect in the skill.

**1 > 0. That condition is met.** Recall is identical, so the "looks unnecessary"
condition (recall within 1 *and* FP not lower) also holds on its first clause and
fails only because the FP count moved — in the wrong direction.

The sharper sub-test fired the same way: the two project-invariant fixtures
(`06-memsafe-select-star`, `07-arch-import-isolation`) were included because only
a reviewer that read the project's instructions should catch them. **Vanilla
caught both.**

## What the one false positive actually was — recorded, not used as a defence

By the written rule this is a false positive, and it is scored as one. The rule is
anchor-based and was fixed before the run: *"Any HIGH/MEDIUM finding anchored to
one of these is a FALSE POSITIVE"* (claudeck's own wording in `GROUND-TRUTH.md`).

What the harness arm actually wrote is worth reading, because it is **not** the
baited misreading. The bait for `a05` is "grep sees `import heavyengine` → flag an
import-isolation violation". The harness arm did not claim that. It said the
*guard itself* is unreliable in both directions — a `from heavyengine.api import
run` form would slip past the substring check, and a comment mentioning the module
would trip it. That is a true statement about the code.

So the honest reading is two-sided and neither side cancels the other:

- **The rule fired and stands.** A MEDIUM anchored to a file the corpus defines as
  non-defective is what the pre-registration said it would count, and re-reading
  the finding after seeing the outcome is exactly the move the pre-registration
  exists to prevent. It is scored as a false positive.
- **The rule cannot tell "over-flagged the bait" from "found something real on a
  file that has no seeded bug".** That is a limitation of *this bench*, now
  documented, and the next iteration should score the *claim* against the ground
  truth rather than the anchor alone. Recording it here is not a re-score.

The one genuine asymmetry the run does show: on the identical observation, the
harness arm chose MEDIUM and vanilla chose LOW. The review skill carries a
demotion ladder whose stated purpose is to push exactly this kind of
unsupported-severity claim downward. On this datum it did not.

## The bench also has a ceiling, and that limits what any of this means

Both arms scored 8/8 recall and 13/14 or 14/14 precision. On the recall axis the
bench has **no resolving power at all** — it could not have shown a difference in
either direction. The fixtures were authored for claudeck v1's pipeline against
that era's models; against `claude-fable-5` they are not hard, and 15 of the 16
non-defective files drew nothing from either arm.

So: the precision axis produced a real, adverse signal at n=1; the recall axis
produced nothing usable. Neither supports a decision on its own.

## What this changes

- `skills/review/SKILL.md`'s expiry condition gets its **first data point, and it
  is unfavourable** — on this corpus the layer added no recall and one extra
  MEDIUM. It is n=1 on inputs unlike goppi's own review surface, so it is recorded,
  not acted on.
- **The skill body could not absorb this datum.** `skills/review/SKILL.md` sits at
  4,972 tokens against §7's 5,000 cap — a 28-token margin (ADR-0027: "a pass, not
  headroom"). A two-sentence Evidence addition would breach the cap, so the record
  lives here and in design §11. The thin margin becoming operational for the first
  time.
- **The next bench must be built on goppi-shaped inputs** — markdown, shell and
  workflow changes with real cross-file obligations, where Session G's failure mode
  (a rule silently dropped from a restructure, every gate green) is the seeded
  defect — and it must score the claim, not just the anchor.

## Three defects in the scorer, and how each was caught

This section is longer than the result because the instrument was wrong three
times, and each was caught by a different mechanism.

1. **A severity leaking from an adjacent paragraph** (caught by the driver reading
   the raw output). The first run reported vanilla FP = 1 on
   `p06-test-with-assert.py`; the arm had listed that file under *found sound*, and
   the summary paragraph two lines below ("9 findings — 4 HIGH … 4 MEDIUM") leaked
   onto it. Fixed: severity attaches only within the same item.
2. **Blind to section headings** (caught by the independent review). Both arms
   grouped findings under `### HIGH` / `### MEDIUM` / `### LOW`. The scorer read
   only *inline* severities, so **every mention in both arms scored severity=None**
   and the false-positive axis was **0 by construction, not by measurement** — the
   number this file originally reported as a tie. Fixed: severity is inherited
   from the nearest preceding severity heading, and **any** other heading (e.g.
   "## Files examined and found sound") closes that scope.
3. **Scoring every file named in an item** (surfaced while fixing 2). Vanilla's
   real finding on `fixtures/07` *cites* `p05-isolation-seam.py` as the correct
   example; the scorer counted p05 as a MEDIUM false positive. The same flaw let a
   neighbouring file's line number land inside another file's tolerance and
   manufacture a catch. Fixed: a line number must be adjacent to *its own*
   filename, and a file named without its own anchor is neither a finding nor a
   false positive.

Regression cases for all three, suite **18 → 26**. Every number in this file is
from the corrected scorer, re-run over the unchanged arm outputs — **the arms were
not re-run, and the raw `*.findings.txt` are untouched.**

The pattern is the session's own subject: three green-and-wrong instruments in a
row, none of them caught by a gate.

## Honest scope

- **n=1 per arm**, one corpus, one model (`claude-fable-5`), one day, one host.
- Slice-1 limit: Layer 2 (hooks, deny/ask, sandbox) is not deployed, so this
  compares *contract + skill text* against vanilla, not a full installation.
- Prompts bypassed equally in both arms — says nothing about the G7 layer.
- Recall is a **lower bound**: anchoring is matched by file and line, so a real bug
  described at the wrong location scores as a miss. It did not bind here (both
  arms anchored everything correctly).
- The corpus is Python; goppi's own review surface is markdown, shell and YAML.
  The transfer was flagged as an assumption in task.md before the run, and this
  result is the reason it now looks like the load-bearing one.
- Ground truth never reached either arm (verified: no `GROUND-TRUTH.md` or
  `bugs.jsonl` under either arm dir).
