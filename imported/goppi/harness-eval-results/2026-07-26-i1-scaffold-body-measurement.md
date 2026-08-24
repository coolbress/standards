# measurement — `scaffold` after Session I's gate pointer, 2026-07-26 (I, item ⑤)
<!-- genre: measurement -->

Session I adds a pointer to `evals/additive-only.sh` in `skills/scaffold/SKILL.md`
Path B. `scaffold` was the second-tightest body in the repo (**4,972**, margin 28
after Session H), so §7's rule that "the cap now binds the *next* edit to this body,
and re-measurement is part of making one" bound this change directly. Genre:
**host token measurement, not a pair.**

This file exists because the session first reported a **prediction** in place of a
measurement, and the prediction was wrong in the dangerous direction twice.

## Method

B's M4, unchanged: 1-turn headless runs, prompt `Reply with exactly: OK`,
`claude -p --setting-sources project --output-format json`, model
`claude-fable-5`, isolated scratch dirs **outside any repo**. Artifact = the
SKILL.md body with frontmatter stripped (`awk 'NR>4'`), placed as the project's
`CLAUDE.md`. Body tokens = `cache_creation(body run) − cache_creation(baseline)`.

**Protocol guard added this session**: every valid run must report
`cache_read = 15251`. See finding 3 — a run that reuses a directory reports a
warm-cache figure that looks like a spectacular result.

Baseline (empty dir) **cc=6002**, `cr=15251`. Cross-session baseline on this CLI
line: 6000 (B) → 5994 (C) → 5996 (G) → 6006 (H) → **6002 (here)**. The spread is
now **12 tokens across five sessions**, unchanged by this run.

## Raw results

```
baseline      result='OK' cc=6002  cr=15251  cost=$0.1355          [valid]
scaffold-1    result='OK' cc=10981 cr=15251  cost=$0.2351          [valid]   13,252 chars → 4,979
scaffold-2    result='OK' cc=7724  cr=18486  cost=$0.1737          [INVALID — warm cache, see finding 3]
scaffold-2'   result='OK' cc=10992 cr=15251  cost=$0.2353          [valid]   13,198 chars → 4,990
```

| body | prior (H) | chars | **measured** | vs cap 5,000 |
|---|---|---|---|---|
| `scaffold` on `main` | — | 13,300 | 4,972 (Session H) | −28 |
| `scaffold` **as landed** | 4,972 | 13,252 | **4,979** | **−21** |
| `scaffold` (further compressed — **rejected**) | — | 13,198 | 4,990 | −10 |

**Suite**: substituting into Session H's landed suite gives
4,979 + kickoff 4,591 + harness-eval 3,466 + governed 1,885 + review 4,972 +
ship 4,984 = **24,877 against §7's 25,000 — under by 123.** Stated with its
caveat: the five other bodies were measured against a 6006 baseline and this one
against 6002, a 4-token difference that is inside the 12-token cross-session
spread and is **not** re-measured here (that would cost five more runs to move a
number by less than its own noise).

**Spend: $0.7796 of an approved $1 band**, across 4 runs of which **3 were valid**.

## Finding 1 — the character-based prediction failed, and in the dangerous direction

The session first reported "+60 characters ≈ **+17 tokens**, margin 26" using a
**3.6 ch/tok** ratio that appears in no prior result file. The repo's recorded
method is `prior measured tokens + (Δchars ÷ ratio)` with the **worst observed
ratio, 2.516**. Redone correctly, the same edit predicted **~4,997, margin 3** —
still a prediction, but one that says "this may be over the cap", which is the
opposite decision.

**A ratio invented at the moment of use is not a method.** The number to apply is
the worst ratio *this repo has actually observed*, and it lives in
`2026-07-25-g1-skill-body-sweep.md`.

## Finding 2 — at this granularity, characters do not predict tokens at all

The compression pass removed **54 characters** of ordinary prose and the body got
**11 tokens larger** (4,979 → 4,990). Both edits changed where lines wrap, and
token boundaries move with them; the added text was **code-span-dense**
(`` `evals/additive-only.sh` ``, `(ADR-0030)`) while the removed text was plain
prose, and the two tokenize nothing alike.

This does **not** overturn G-1's "characters predict tokens about twice as well as
words" — it bounds it. That finding came from **restructures of thousands of
characters**, where the composition of added and removed text averages out. For a
**small edit (tens of characters) that also re-wraps lines**, the character delta
carries no signal: here it pointed the wrong way entirely.

Operational rule this session followed: **when a body is within ~50 tokens of its
cap, measure — do not predict.** The measurement costs $0.24 and one run.

## Finding 3 — a fixed-path measurement dir gave a spectacular, meaningless number

`scaffold-2` reported **1,722 tokens** — a 3,268-token improvement — because it
reran in the directory the previous run had already warmed. The tell is in the
output: `cache_read` was **18,486** instead of the 15,251 every valid run reports,
so the "cache creation" being measured was only the delta the cache did not
already hold.

This is precisely the trap `CONTRIBUTING.md` records as *"never write a generated
payload to a fixed path and read it back later"* — reproduced here on the
measurement harness itself, by the session that had just re-read that file.
**The protocol now requires asserting `cr = 15251`**, so an invalid run announces
itself instead of reading as a triumph.

## What landed, and the honest residual

The **4,979** version is what ships. The compressed 4,990 version was reverted by
applying the exact inverse of both edits; the body returned to **13,252
characters**, matching the measured artifact byte-for-byte in length. The residual
is stated rather than hidden: the measured artifact file itself was overwritten by
the later run, so byte-identity rests on the edits being exact-string inverses plus
the character count matching — not on a stored hash. A future measurement should
**keep each run's artifact** for exactly this reason.
