# measurement — ship skill body, first measurement + the cost of this change, 2026-07-25
<!-- genre: measurement -->

`skills/ship/SKILL.md` had **never been measured** against design §7's ≤5k
per-skill cap. Issue #63 adds to it, which made measuring a precondition rather
than a nicety. Same genre as the two Session C measurements: a host token
measurement, not a pair.

## Method

B's M4, unchanged: 1-turn headless runs, prompt "Reply with exactly: OK",
`claude -p --setting-sources project --output-format json`, model
`claude-fable-5`, **Claude Code 2.1.220**, isolated scratch dirs. The artifact
is the SKILL.md body with YAML frontmatter stripped (`awk 'NR>4'`) — the
frontmatter description belongs to the always-injected budget, not the body cap.
Baseline (empty dir) `cc=5994`, `cache_read` 15,251 identical on every run.

## Results

Every row is a measured run, in the order they were made. Steps 3–7 are the
edits that paid for step 2's additions; each is named, so the arithmetic can be
followed without re-spending.

| # | Revision | words | tokens | vs cap 5,000 |
|---|---|---|---|---|
| 1 | `main`, before this change | 1,834 | **4,829** | under, margin 171 |
| 2 | + the issue-#63 additions | 1,946 | **5,088** | **over by 88** |
| 3 | + a prose tighten **and a new Evidence bullet** — net **grew** the file | 1,972 | 5,116 | over by 116 |
| 4 | − a rule the new step-3 text restated from the commit-message section | 1,957 | 5,077 | over by 77 |
| 5 | − the predecessor bibliography, collapsed to ADR pointers | 1,964 | 5,058 | over by 58 |
| 6 | − the `gh` credential rule, deduplicated into model-roster Trust rules | 1,960 | 5,017 | over by 17 |
| 7 | − session-boundary and degradation-record prose (the decisive cut) | 1,936 | **4,969** | under, margin 31 |
| 8 | **as landed** — after this PR's own review: 2 HIGH gate fixes, LOW-6 restore, LOW-8 → ADR pointer, then a deliberate over-cut | 1,927 | **4,962** | **under, margin 38** |

## Findings

- **`main` was already at 97% of the cap.** The overage was not caused by
  sloppiness in this change; the file had no room. That it went unnoticed is
  the point of measuring: a budget nobody measures is not a budget.
- **The additions cost 259 tokens** (row 1 → 2), repaid across rows 3–7. Only
  **one** of those was ordinary prose tightening (row 7); row 3 was not a cut
  at all — it net-grew the file. The other three (rows 4, 5, 6) were
  **duplication removals**: a rule restated from elsewhere in the same file, a
  bibliography whose canonical home is `docs/decisions/`, and a credential rule
  `references/model-roster.md` already owned in generalized form. **A file at
  its cap is what makes duplication visible.** Row 7 is where the file finally
  went under, and it is worth naming plainly: 48 of the 119 tokens recovered
  came from that single decisive cut, not from the itemized dedup work.
- **ship is structurally at its limit** — 38 tokens is under two lines. The
  next addition needs the treatment `skills/review/SKILL.md` got in ADR-0027
  (split a block by *when it is read*), not another round of trimming.

## Cost, recorded because most of it was avoidable

**8 runs, $1.89.** The efficient path was two: size the cut, over-cut, measure.
Instead rows 3–6 each trimmed slightly *less* than the overage and re-measured,
which is how a $0.24 check became a $1.89 one — and row 3 grew the file it was
meant to shrink. The rule that came out of it, applied on row 8 and worth
carrying forward: **estimate the required cut from word count, deliberately
over-cut past that estimate, then measure once.** Word count is a poor predictor
of absolute tokens — that is why this file exists — but at ~2.57 t/w for this
body it is a fine predictor of *direction and size*, which is all a cut needs.
Row 8 was estimated at 4,946 and measured 4,962: a 16-token error, well inside
the margin the over-cut bought.

## Honest scope

- One host, one model, one CLI build, one run per revision. Deltas are exact
  host-reported integers; day/version variance unmeasured.
- M4 injects the body as a project `CLAUDE.md`; the on-trigger skill-load
  wrapper may differ slightly. Every row above used the identical method, so
  the comparisons hold even if the absolute number shifts.
- Not measured here: the other four skill bodies (`kickoff`, `scaffold`,
  `harness-eval`, `governed`), which have also never been measured. `review`
  is measured (4,972, its own result file). On this evidence — two of two
  measured skills landing within 1% of the cap — the unmeasured four are worth
  a sweep, but this change did not touch them and did not spend on them.

> **Forward pointer (appended 2026-07-25, Session G — this file is otherwise
> unchanged).** That sweep ran: `results/2026-07-25-g1-skill-body-sweep.md`. All
> four were measured, `scaffold` came in at **8,080 — 62% over the cap** and was
> restructured to 4,807 (ADR-0028); the six-body suite is now **24,376 vs the 25k
> budget**. Two of this file's own conclusions were **not** confirmed at that
> scale: "two of two land within 1% of the cap" did not generalize (the other
> four landed 4% to 62% away from it), and the word-count sizing this file
> recommends turned out to err **low** — characters predict tokens about twice as
> well, which is what made the scaffold cut land in one run.
