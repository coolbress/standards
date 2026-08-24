# measurement — the four unmeasured skill bodies + the scaffold restructure, 2026-07-25 (Session G, G-1)
<!-- genre: measurement -->

The remaining four skill bodies (`kickoff`, `scaffold`, `harness-eval`,
`governed`) had never been measured against design §7's ≤5k per-skill cap, and
the six-body suite had never been measured against §7's 25k re-attachment
budget. Same genre as the three prior measurements: **host token measurements,
not pairs** (`results/2026-07-25-c1-review-slim-remeasure.md`,
`results/2026-07-25-ship-body-measurement.md`).

A word-count **projection** written 2026-07-25 (`.scratch/next-session-tasks.md`)
aimed this session at `scaffold`. It was recorded explicitly as a projection, not
a measurement. Testing it against real numbers is one of this file's results.

## Method

B's M4, unchanged: 1-turn headless runs, prompt "Reply with exactly: OK",
`claude -p --setting-sources project --output-format json`, model
`claude-fable-5`, **Claude Code 2.1.220** (the same CLI build as every prior
measurement in this directory), isolated scratch dirs outside any repo. The
artifact is the SKILL.md body with YAML frontmatter stripped (`awk 'NR>4'` —
verified correct for all six bodies, each closing its frontmatter on line 4); the
frontmatter description belongs to the always-injected budget, not the body cap.

Baseline (empty dir) `cc=5996`; `cache_read` 15,251 identical on all six runs.
Baseline reproducibility across sessions on this CLI build: 6000 (Session B) →
5994 (Session C) → **5996** (here) — a 6-token spread, so the three sessions'
numbers are directly comparable.

## Raw results

```
baseline     result='OK' cc=5996  cr=15251 cost=$0.1366 ms=2831
scaffold     result='OK' cc=14076 cr=15251 cost=$0.2979 ms=2217
kickoff      result='OK' cc=9939  cr=15251 cost=$0.2143 ms=2378
harness-eval result='OK' cc=9462  cr=15251 cost=$0.2058 ms=2801
governed     result='OK' cc=7881  cr=15251 cost=$0.1737 ms=2198
scaffold-rev result='OK' cc=10803 cr=15251 cost=$0.2315 ms=2501
```

| body | words | **measured** | vs cap 5,000 | projected band | projection error |
|---|---|---|---|---|---|
| **`scaffold`** | 2,902 | **8,080** | **+3,080** | 7,177–7,473 | **+607 above band** |
| `kickoff` | 1,596 | **3,943** | −1,057 | 3,946–4,109 | −3 (just **below** the band) |
| `harness-eval` | 1,229 | **3,466** | −1,534 | 3,039–3,164 | **+302 above band** |
| `governed` | 715 | **1,885** | −3,115 | 1,768–1,841 | **+44 above band** |

**Suite, as found**: 8,080 + 3,943 + 3,466 + 1,885 + review 4,972 + ship 4,962 =
**27,308 against §7's 25,000 re-attachment budget — over by 2,308**, entirely
`scaffold`'s doing. The projection's "over that too" call was right, and its
reasoning ("entirely because of scaffold") was right; only the size was wrong,
and wrong in the dangerous direction.

## Finding 1 — the projection erred, and erred low

**All four missed the band** — three above the top, and `kickoff` 3 tokens below
the floor (0.08%, near-exact but still outside). The projection multiplied word counts by the two
observed tokens-per-word ratios (review 2.473, ship 2.575), assuming a 2.47–2.58
band. The real range across six measured bodies is **2.471–2.820** — more than
twice as wide, and open on the high side, which is exactly where a budget check
must not be optimistic.

For `scaffold` this was not a rounding difference: the body was **62% over the
cap**, not the 44–49% the projection implied.

## Finding 2 — characters predict tokens about twice as well as words do

Same six measured bodies, two candidate predictors:

| predictor | range | spread |
|---|---|---|
| tokens per **word** | 2.471 – 2.820 | 14.1% |
| **characters** per token | 2.485 – 2.686 | 8.1% |

The restructure below was sized with the character ratio and landed **11 tokens
from prediction** (predicted 4,818 at 2.680 ch/tok; measured 4,807 at an actual
2.686). The same cut sized by words would have been predicted anywhere from
4,522 to 5,160 (1,830 words × the measured 2.471–2.820 t/w range) — a band that straddles the cap and would have decided nothing.

This matters because the cheap pre-run estimate is what makes "over-cut, then
measure once" affordable. **Word count answers *direction*; character count
answers *how much*.** Neither replaces a measurement, and no claim in this repo
is made on either.

## Finding 3 — the scaffold restructure: 8,080 → 4,807, in one measurement

Split by *when a block is read* (ADR-0027's rule), recorded in ADR-0028.

| | words | chars | as-injected | margin under 5k |
|---|---|---|---|---|
| before | 2,902 | 21,463 | **8,080** | over by 3,080 |
| **as restructured** | 1,830 | 12,911 | **4,807** | **193** |

−3,273 tokens, **−40.5%**. The reduction is **mostly** de-duplication, not
compression — but not entirely, and the review of this change set found where it
was not (see "What the restructure actually cost" below): the accounting semantics, the completion contract, the
brownfield doctrine and the release-automation mechanics all already existed, in
near-identical words, in `references/production-floor.md`; the permission-posture
mechanics already existed in `references/sandbox-presets.md` and
`hosts/codex/README.md`; and the closing "Rules that always hold" section
restated five rules the body states elsewhere (each verified present before
removal). What the reference did not already own — the update-vs-adopt test, the
ordered update steps, adopt's interview obligation — was **written into
production-floor.md** rather than deleted.

**Cost discipline, applied and worth the comparison.** The ship measurement
(`2026-07-25-ship-body-measurement.md`) spent **8 runs and $1.89** trimming
slightly less than the overage each time. Here the rule that measurement
produced — estimate the cut, deliberately over-cut, measure **once** — was
followed: **1 run, $0.2315**. Three intermediate revisions were rejected on the
*character estimate* before any run, including one that cut only 7% and would
have measured ~7,500. The estimate is free; the run is not.

**Suite, after**: 4,807 + 3,943 + 3,466 + 1,885 + 4,972 + 4,962 = **24,035
against the 25,000 budget**, the first time the suite has been measured at all.

## Finding 4 — kickoff re-measured after this session edited it: 4,284

G-3 added a paragraph to `kickoff`'s Evidence and struck an Expiry row, so the
3,943 above stopped being true of the body that actually lands. Re-measured
rather than left as an estimate, per the rule this directory enforces:

```
kickoff-rev  result='OK' cc=10280 cr=15251 cost=$0.2211
```

**4,284 tokens** (10,280 − 5,996), margin **716** — the body grew 897 chars and
341 tokens. The character predictor called it at 4,282 before the run: **2 tokens
off**, a second independent confirmation of Finding 2.

**Suite as landed: 4,807 + 4,284 + 3,466 + 1,885 + 4,972 + 4,962 = 24,376 —
under the 25,000 budget by 624.** That is the number to carry; the 24,035 above is
the mid-session figure.

## Finding 5 — what the restructure actually cost: two rules, and the honest number is 4,911

The claim above that the cut was pure de-duplication **did not survive review.**
Two rules existed in the old body and in **neither** the new body nor any
companion it names — a silent policy drop, which is the failure this kind of
restructure is most likely to cause and least likely to notice:

1. **The PR/issue body-gate filenames** (`templates/pr-body.yml`,
   `templates/issue-body.yml`) and their `.github/workflows/` destination. The new
   body deferred them to `production-floor.md`, which did not name them — so the
   pointer was broken *and* the mechanism unrecoverable, degrading the gate to
   "lay the template only", the exact state that control exists to prevent. Caught
   by an audit the driver ran only after being challenged on it.
2. **The Conventional-Commits pairing rule** for release automation — a
   release-please workflow laid onto a project with no commit convention never
   bumps past its manifest floor, while the accounting records the control
   `active`. Caught by the independent review.

A third finding was a **contradiction rather than a loss**: the Path B degrade
rule ("production-floor unreachable ⇒ treat as a first adoption") removed the
antecedent of a non-negotiable declared two paragraphs earlier ("on an update,
re-check the security floor FIRST"), so a reclassified run could skip the
same-`floor-version` regression check.

All three were fixed — the two rules written into `references/production-floor.md`
and the body respectively, the contradiction resolved so the recheck survives
reclassification — plus the Codex deny/ask command set restored **inline**, on the
same reasoning ADR-0028 used to keep the CI security invariants inline: the
degrade path is exactly when the companion is unreachable too.

**Re-measured after those fixes — the number that actually lands:**

```
scaffold-rev2 result='OK' cc=10907 cr=15251 cost=$0.2371 ms=12074
```

| | chars | as-injected | margin under 5k |
|---|---|---|---|
| before the restructure | 21,463 | 8,080 | over by 3,080 |
| after the restructure | 12,911 | 4,807 | 193 |
| **as landed, after review fixes** | **13,078** | **4,911** | **89** |

The fixes cost **104 tokens** and were paid for out of the margin by trimming
prose elsewhere; character-based sizing predicted 4,869 at the prior 2.686 ch/tok
and it measured 4,911 at an actual 2.663 — a 42-token miss, the largest of the
three predictions in this file, because the restored command list is
backtick-dense and tokenizes below the body's prose rate.

**Suite as landed: 4,911 + 4,284 + 3,466 + 1,885 + 4,972 + 4,962 = 24,480 —
under the 25,000 budget by 520.** This supersedes both 24,035 and 24,376 above.

**The method lesson, stated plainly**: the driver asserted "no rule removed" from
recollection, and it was wrong twice. A body restructure of this size needs a
**mechanical old-vs-new rule audit** before the done-claim — extract every
normative sentence from the old body, locate each in the new body or the specific
companion it names, and treat "present under different wording" as a claim to
verify, not to assume.

## Cost

**8 runs, $1.7180** total for this file's measurements — the six in the raw block
above (14.9s of host time, `duration_ms` summed), plus `kickoff-rev` (whose
`duration_ms` this run's capture did not record) and `scaffold-rev2` (12.1s).
Against the session's approved $8 band. This is a token measurement, so there is
no per-arm split to report.

## Honest scope

- One host, one model, one CLI build, **one run per point**. Deltas are exact
  host-reported integers; day-to-day and version variance is unmeasured, and the
  6-token baseline spread across three sessions is the only cross-session
  stability evidence there is.
- M4 injects the body as a project `CLAUDE.md`; the on-trigger skill-load wrapper
  may differ slightly. Every row here used the identical method, so the
  comparisons hold even if the absolute number shifts.
- The 25k suite figure assumes all six bodies re-attach together, which is the
  budget's own worst-case premise, not an observed event.
- **`scaffold`'s 193-token margin is a pass, not headroom** (4%). The next edit to
  that body must re-measure. The three other bodies have real room (`kickoff` 716
  after this session's own edit / `harness-eval` 1,534 / `governed` 3,115) and are
  **not** slimming candidates on this evidence.
- Not measured here: the always-injected surface (§7's ≤2k), which the frontmatter
  descriptions feed — that is G-2's subject and is measured separately. No
  frontmatter description was touched by this work.
