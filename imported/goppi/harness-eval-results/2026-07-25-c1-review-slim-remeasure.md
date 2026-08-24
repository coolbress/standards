# measurement — review skill body after the C-1 slim, 2026-07-25 (NOT a pair)
<!-- genre: measurement -->

Session C item 1's acceptance gate: the slimmed `skills/review/SKILL.md` must
land **≤5,000 tokens** as injected, measured — not estimated. Same genre as the
Session B G5 calibration: a **host token measurement**, not a harness-vs-vanilla
pair, recorded here because it shares the results convention (real outputs,
honest scope).

Why a measurement and not a word count: the 2026-07-25 datum (5,837 tokens for
2,302 words = 2.54 t/w) is high for prose because template blocks and
markdown/symbol density tokenize heavily. The C-1 restructuring moved the
heaviest such block out of the body, so the words→tokens ratio moves exactly
where the change cut — a word-count projection would be least reliable at the
one point the decision turns on.

## Method (disclosed — B's M4, re-run)

Two 1-turn headless runs, identical trivial prompt ("Reply with exactly: OK"),
`claude -p --setting-sources project --output-format json`, model
`claude-fable-5` pinned, **Claude Code 2.1.220** (the same CLI build as the
Session B measurement), isolated scratch dirs outside any repo. The injected
context size is read from the host's own `usage` fields; `cache_read_input_tokens`
was **identical (15,251) across both runs** — the same shared system+tools layer
Session B saw — so the delta rides purely on `cache_creation_input_tokens`.

The measured artifact is the SKILL.md **body with the YAML frontmatter stripped**
(`awk 'NR>4'`), matching how Session B measured its 2,302-word figure. The
frontmatter `description` is a separate surface: it belongs to the always-injected
budget (§7's ≤2k), not to the per-skill body cap, and it was deliberately left
unchanged by C-1 — it is the skill's trigger contract, and a trigger/body
mismatch is a defect this repo has already had once (PR #45 review).

## Raw results

```
base result='OK' in=2 cc=5994  cr=15251 out=43 cost=$0.1373 ms=2655
rev  result='OK' in=2 cc=10938 cr=15251 out=14 cost=$0.2347 ms=2381
```

- `base` = empty dir (baseline) · `rev` = `CLAUDE.md` = the slimmed review body
  (2,002 words).
- **Review body as-injected = 10,938 − 5,994 = 4,944 tokens.**

Baseline reproducibility: Session B's empty-dir baseline on the same CLI build
was `cc=6000`; this run reads `cc=5994` (−6 tokens, ~0.1%) with an identical
`cache_read` of 15,251. The two measurements are directly comparable.

## Findings vs the recorded budget

| Claim (design §7) | Before (Session B) | After (this measurement) | Verdict |
|---|---|---|---|
| ≤ 5k tokens per skill body | **5,837** (2,302 words) | **4,944** (2,002 words) | **under the cap** — −893 tokens, −15.3% |

The reduction was achieved **while adding** three components (Stage-0
deterministic pre-pass · auto-demotion ladder + banned-hedge list ·
regression-test-on-finding), so it is not a like-for-like shrink: content moved
out (report format → `references/review-report.md`; the duplicated per-host
executor table → deferred to `references/model-roster.md`, which already owned
it) and new content moved in.

Implied ratios: 2.535 t/w before, 2.469 t/w after. The ratio barely moved, so
the saving came from **fewer words on the load path**, not from a genre change
as large as expected — the pre-slim decomposition guess (prose ≈2.2 t/w, fenced
template ≈4.0 t/w) over-attributed the cost to the template block.

## Re-measured after the independent review (same day, appended not rewritten)

The review of PR #61 raised a finding this file's own "the cap binds the next
edit" warning had predicted: the restructuring created a hard dependency on
`references/review-report.md` with **no degrade rule**, while keeping one for a
different sibling — so in a deployment where `references/` does not resolve, the
driver would write the report from memory and the rows the G3 evidence contract
depends on could silently go missing. Accepted and fixed by adding an
unreachable-sibling rule to the body.

That edit had to pay for itself out of a 56-token margin. It was offset by
trimming two Evidence/intro passages, and then **re-measured rather than
assumed** — the discipline this file exists to enforce:

```
base result='OK' cc=5994  cr=15251
rev2 result='OK' cc=10966 cr=15251   → body = 4,972 tokens   cost $0.2354
```

| | words | as-injected | margin under 5k |
|---|---|---|---|
| pre-slim (Session B) | 2,302 | 5,837 | **over by 837** |
| post-slim (above) | 2,002 | 4,944 | 56 |
| **post-review, as landed** | 2,011 | **4,972** | **28** |

**The landed number is 4,972.** One review finding consumed half the remaining
margin, which is the concrete form of "this is a pass, not headroom": the next
edit to this body has roughly 11 words of room before something else must leave.

## Honest scope

- **The margin is 56 tokens (1.1%).** This is a pass, not headroom: any
  future addition to the review body lands over the cap unless something else
  leaves. Treat the cap as binding on the next edit, and re-measure it —
  a body that grows back is the failure mode this measurement exists to catch.
- One host (Claude), one model, one CLI build, one run per point. The deltas are
  exact host-reported integers, but day/version variance is unmeasured — same
  limit Session B recorded.
- M4 measures the body by injecting it as the project `CLAUDE.md` — a
  host-tokenizer count of those bytes as context. The on-trigger skill-load
  wrapper may differ slightly; the comparison to 5,837 is what this run is for,
  and both sides used the identical method.
- Cost of this measurement: **$0.372** total ($0.1373 + $0.2347), 5.0s of host
  time. Recorded per the Session B per-arm format even though this is not a pair.
- Not measured here: the always-injected surface (§7's ≤2k), which the
  frontmatter description feeds. `GOPPI.md` is touched elsewhere in this session,
  so that budget is re-measured separately.
