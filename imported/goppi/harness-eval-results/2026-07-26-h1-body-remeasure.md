# measurement — the three bodies Session H edited, 2026-07-26 (H, item ①-6)
<!-- genre: measurement -->

Session H's F-1 long tail adds rules to `ship`, `scaffold` and `kickoff`. Two of
those three were the tightest bodies in the repo — `ship` at 4,962 (margin 38)
and `scaffold` at 4,911 (margin 89) — so §7's rule that "the cap now binds the
*next* edit to this body, and re-measurement is part of making one" bound this
session directly. This file is that re-measurement. Genre: **host token
measurement, not a pair** (same as `2026-07-25-g1-skill-body-sweep.md`).

## Method

B's M4, unchanged and matching every prior measurement in this directory:
1-turn headless runs, prompt `Reply with exactly: OK`,
`claude -p --setting-sources project --output-format json`, model
`claude-fable-5`, **Claude Code 2.1.220**, isolated scratch dirs outside any
repo. Artifact = the SKILL.md body with frontmatter stripped (`awk 'NR>4'`); the
frontmatter description belongs to the always-injected budget, not the body cap.

Baseline (empty dir) **cc=6006**, reproduced exactly on all three baseline runs
this session; `cache_read` 15,251 identical across all nine runs.
Cross-session baseline reproducibility on this CLI build: 6000 (B) → 5994 (C) →
5996 (G) → **6006** (here). That is a **12-token spread across four sessions**,
wider than the 6 recorded in §7 — worth stating, because one result below has a
margin of the same order.

## Raw results

```
baseline     result='OK' cc=6006  cr=15251 cost=$0.1362 ms=3764
ship         result='OK' cc=10990 cr=15251 cost=$0.2362 ms=2144
scaffold     result='OK' cc=10963 cr=15251 cost=$0.2354 ms=2992
kickoff      result='OK' cc=10716 cr=15251 cost=$0.2304 ms=2298
kickoff-rev  result='OK' cc=10583 cr=15251 cost=$0.2278 ms=—
--- after the independent review's accepted findings ---
baseline     result='OK' cc=6006  cr=15251 cost=$0.1377
scaffold-2   result='OK' cc=11018 cr=15251 cost=$0.2363   (5,012 — OVER cap)
kickoff-2    result='OK' cc=10597 cr=15251 cost=$0.2306
scaffold-3   result='OK' cc=10978 cr=15251 cost=$0.2350   (4,972 — as landed)
```

| body | before | chars | **measured** | vs cap 5,000 |
|---|---|---|---|---|
| `ship` | 4,962 | 13,257 | **4,984** | −16 |
| `scaffold` (pre-review) | 4,911 | 13,362 | 4,957 | −43 |
| `scaffold` (review fixes, over) | — | 13,418 | 5,012 | **+12 — rejected** |
| **`scaffold` (as landed)** | 4,911 | 13,300 | **4,972** | −28 |
| `kickoff` (first cut) | 4,284 | 12,679 | 4,710 | −290 |
| `kickoff` (retighten) | — | 12,282 | 4,577 | −423 |
| **`kickoff` (as landed)** | 4,284 | 12,316 | **4,591** | −409 |

**Suite as landed**: scaffold 4,972 + kickoff 4,591 + harness-eval 3,466 +
governed 1,885 + review 4,972 + ship 4,984 = **24,870 against §7's 25,000
re-attachment budget — under by 130.**

The two extra `scaffold` rows are the honest record of the review loop: an
accepted finding required the destructive-accident set to be **fully enumerated
inline** (the reachability precedent Session G set), which pushed the body **12
tokens over cap**. Over-cap is not a rounding error to wave through, so four
duplicate-removing compressions were made and the body re-measured once more.
Baseline `cc=6006` reproduced **exactly** on all three of this session's baseline
runs, which is what makes the single-body final measurement legitimate rather
than a shortcut.

## Finding 1 — a character-based prediction held, and the method is worth stating exactly

**The method, corrected in review** — the first draft of this section described it
loosely enough to be unreproducible, and the reviewer's literal reading of that
description produced predictions ~300 tokens off. What was actually done:

> predicted = **the body's own prior measured token count** + (**character
> delta** ÷ a ch/tok ratio)

i.e. the ratio is applied to the **delta**, never to the whole body. That matters:
dividing a whole 13,000-character body by the worst observed ratio (2.516) predicts
5,269 for `ship` and would have condemned a compliant body. The ratio used was
**2.516** (the worst of the six observed) for `ship` and `scaffold`, and **2.600**
for `kickoff` — an inconsistency in the doing, not a method, and recorded as such:

| body | prior | Δchars | ratio used | predicted | measured | error |
|---|---|---|---|---|---|---|
| `ship` | 4,962 | +50 | 2.516 | 4,981 | 4,984 | **+3** |
| `scaffold` | 4,911 | +125 | 2.516 | 4,960 | 4,957 | **−3** |
| `kickoff` | 4,284 | +1,220 | 2.600 | 4,753 | 4,710 | −43 |

Two of three landed within 3 tokens, and the outlier is the one with the largest
delta — consistent with the delta-based method's error scaling with Δ, not with
body size. This replicates §7's G-1 finding on a different change shape (small
insertions rather than a wholesale restructure). The practical rule: **predict the
delta, not the body**; use the worst observed ratio; over-cut; measure once.

## Finding 2 — the suite budget is the binding constraint now, not the per-skill cap

The first cut of this change set measured a suite of **24,974 — 26 tokens under
25,000**, while every individual body was comfortably under its own 5,000 cap.
26 tokens is inside the 12-token baseline spread doubled; a "we are under budget"
claim at that margin is not meaningfully distinguishable from noise.

So `kickoff`'s addition was re-tightened and re-measured **once**: 4,710 →
**4,577**, restoring the suite to **24,841, margin 159**.

**The re-tighten dropped a rule, and the independent review caught it.** This
section originally claimed the re-cut was "prose only, with every ported rule
kept (risk tiers 8/12/18 …)". It was not: the **medium tier (12)** was absent
from the landed body — and, checked afterwards, absent from the *first* cut too,
so it was lost at the original port and the claim was wrong at both sites where
it appeared (here and `.scratch/next-session-tasks.md`). The tier was restored
(`distribution/supply-chain → 12`) before merge.

This is the **third** occurrence of the class ADR-0028 exists to catch — a rule
lost in a size-driven edit, with a "nothing was dropped" claim written from the
driver's recollection. The rule survives only because a fresh context diffed the
artifact against the claim. Read that as evidence about the *claim*, not about
the compression: the mechanical old-vs-new audit is what ADR-0028 requires, and
running it against a **compressed body's rule list** is easy to do and easy to
believe you did.

The generalizable point, and the reason this is written down rather than left in
a commit message: **six bodies each individually "fine" can still sum to a
breach.** Per-skill compliance is now the easy half. Any future session adding to
*any* body should read the suite number first, because 130 tokens is roughly one
paragraph — and nothing in `check.sh` measures this. It is caught by a human
choosing to spend $0.23, which is exactly the kind of control that quietly stops
happening.

## Cost

**$1.906** across 9 runs, against the **$2** band approved at session start.
Split honestly: **$1.066** for the first five (baseline + three bodies + one
re-cut), then **$0.840** for the four the independent review made necessary
(a baseline re-check, `scaffold` and `kickoff` after the accepted findings, and
`scaffold` once more after it came back 12 over cap). The review cost 44% of the
band and caught a dropped rule; that is the trade, stated rather than buried.

## Honest limits

- M4 injects the body as a project `CLAUDE.md`; the on-trigger skill-load wrapper
  may differ slightly. Every row here and in the prior four sessions used the
  identical method, so the numbers are comparable to each other — they are not a
  claim about the exact production injection path.
- `review`, `governed` and `harness-eval` were **not** re-measured: this session
  did not touch them. Their contribution to the suite total is carried forward
  from `2026-07-25-g1-skill-body-sweep.md` on this same CLI build.
- The baseline spread widened from 6 to 12 tokens across four sessions. Nothing
  here corrects for it; a body number is ±12 at the same confidence the baseline
  is, which matters only for margins under ~25 — i.e. it mattered for the
  rejected first cut, and does not for what landed.
