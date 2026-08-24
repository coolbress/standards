# measurement — `ship` after the local-validation step, 2026-07-27 (issue #78)
<!-- genre: measurement -->

Issue #78 adds one instruction to `skills/ship/SKILL.md`: prove the PR body with
`evals/pr-body-hygiene.sh` **before** creating the PR. `ship` was the tightest body
in the repo — **4,984, margin 16** (Session H) — so §7 bound this edit from the start.
Genre: **host token measurement, not a pair.**

## Method

B's M4, unchanged: 1-turn headless runs, prompt `Reply with exactly: OK`,
`claude -p --setting-sources project --output-format json`, model `claude-fable-5`,
**a fresh isolated dir per run** outside any repo. Artifact = the SKILL.md body with
frontmatter stripped (`awk 'NR>4'`), placed as the project `CLAUDE.md`.
Protocol guard (added in the previous measurement, #75): a valid run reports
`cache_read = 15251` — every run below did. **Each artifact was kept this time**,
which the previous result file recorded as the thing to fix.

Baseline (empty dir) **cc=6010**, `cr=15251`. Cross-session baseline: 6000 (B) →
5994 (C) → 5996 (G) → 6006 (H) → 6002 (I/#75) → **6010 (here)**: a **16-token spread
across six sessions**, slightly wider than the 12 recorded last time. That number is
why "margin 6" below is treated as a failure to land, not a pass.

## Raw results

```
baseline    cc=6010  cr=15251  cost=$0.1365   [valid]
ship v1     cc=11004 cr=15251  cost=$0.2362   [valid]   4,994  margin 6    rejected
ship v2     cc=10957 cr=15251  cost=$0.2351   [valid]   4,947  margin 53   (PR side only)
ship v3     cc=11005 cr=15251  cost=$0.2361   [valid]   4,995  margin 5    rejected
ship v4     cc=10991 cr=15251  cost=$0.2365   [valid]   4,981  margin 19   rejected
ship v5     cc=10974 cr=15251  cost=$0.2350   [valid]   4,964  margin 36   AS LANDED
```

v3–v5 exist because the 2026-07-27 independent review found the instruction had
landed for the PR body only (`ship` step 3) and not the issue body (step 1) — and the
issue gate is the advisory-only one, so it is the half nothing forces you to notice.

| body | Δchars vs `main` | **measured** | vs cap 5,000 |
|---|---|---|---|
| v1 — instruction + prose trims | **−48** | 4,994 | **+10 tokens — rejected** |
| v2 — one code span removed | **−138** | 4,947 | −53 |
| v3 — issue side, as its own sentence | −14 | 4,995 | **margin 5 — rejected** |
| v4 — issue side folded in, two spans | −65 | 4,981 | **margin 19 — rejected** |
| **v5 — issue side folded in, one glob span — AS LANDED** | **−90** | **4,964** | **−36** |

**Rejection rule applied**: margin must clear **twice** the baseline's own
cross-session spread (16 → 32), the standard Session H used when it refused a
26-token suite margin against a 12-token spread. v4's margin of 19 is inside that
band, so it was not landed even though it is under the cap.

**Suite**: substituting into the current set — 4,964 + `scaffold` 4,979 + `kickoff`
4,591 + `harness-eval` 3,466 + `governed` 1,885 + `review` 4,972 = **24,857 / 25,000,
margin 143.** Caveat carried, not hidden: the six bodies were measured against
baselines of 6002–6010, a spread inside the 16-token cross-session band, and they are
**not** re-measured here to chase a difference smaller than that band.

**Spend: $1.3154 of an approved $1 + $0.5 band**, 6 valid runs — the extension was
asked for and granted rather than quietly exceeded. One earlier attempt produced
no parseable output and its cost is **unaccounted** — recorded rather than rounded away;
even counting it as a full run the band holds.

## Finding — the second replication, and now the mechanism is quantified

`2026-07-26-i1` recorded that a **54-character cut made a body 11 tokens larger** and
concluded that character delta carries no signal for small edits. This measurement
replicates that and explains it:

| edit | Δchars | Δtokens | what moved |
|---|---|---|---|
| v1 — added one code span, trimmed plain prose | **−48** | **+10** | prose out, `` `evals/pr-body-hygiene.sh` `` in |
| v2 — removed one code span + illustrative clause | **−90** | **−47** | `` `feat/38-ship-skill` `` out |

**Plain prose is nearly free; code spans and dense punctuation are not.** Ninety
characters containing one backticked path bought back **47 tokens**, while forty-eight
characters of ordinary sentence bought back **nothing** — it went the other way.

**The sharpest datum is the accident at the end.** The review's finding forced the
same instruction to be written three ways, which turns the mechanism from an inference
into a controlled comparison — identical meaning, identical placement, three phrasings:

| phrasing of the SAME instruction | Δtokens vs v2 |
|---|---|
| its own sentence, its own `evals/…` span | **+48** |
| folded into the existing sentence, two spans | **+34** |
| folded in, **one** `evals/*-body-hygiene.sh` glob span | **+17** |

Collapsing two code spans into one glob cost **17 tokens instead of 48 — a 2.8×
difference for the same rule.** Character count moved by 90 across that range and
predicted none of it.

The operational rule, now with three data points behind it: **when a body is near its
cap, do not budget in characters. Budget in code spans and sentences.** Adding one backticked
identifier costs on the order of ten tokens; removing one returns about the same.
Prose edits of this size are noise. And measure — this session's first cut would have
shipped at margin 6, inside the baseline's own spread, on a prediction that said 4,965.

## Rule audit (ADR-0028's recorded obligation)

Mechanical old-vs-new comparison of every bolded phrase and code span against `main`:

- **Bold lost (1)**: `Read .github/PULL_REQUEST_TEMPLATE.md and fill it in — never
  reconstruct it from memory` — rewritten in place; its replacement carries the same
  rule **plus** the new one, so no rule was dropped.
- **Code span lost (1)**: `feat/38-ship-skill` — an example, deliberately removed; the
  pattern it illustrated (`type/<issue>-<slug>`) is still stated immediately above it.
- **Code span added (1)**: `evals/pr-body-hygiene.sh` — the point of the change.

**Prose fragments removed — all five, from a word-level diff.** The 2026-07-27
review pointed out that this list originally had two; it named two more, and running
`git diff --word-diff` rather than a bold/code-span sweep surfaces a fifth. That is
the point worth keeping: **a bold/code-span audit cannot see plain prose**, which is
the failure ADR-0028 exists to catch, so the audit is now anchored on a word diff.

1. `The flow above is the policy on every host.` — restates the section heading
   directly above it.
2. `— the Codex app's GitHub connector, or a host-native PR flow —` — illustration;
   the rule ("prefer the host's native integration") stays, and the pointer survives
   in `hosts/codex/operations.md`.
3. `entirely` — intensifier.
4. `the PR body's` (qualifying `## Verification`) — unambiguous by the time step 5
   uses it, since step 3 establishes it.
5. `— a visible decision` — rationale after a rule that already says what to record.

None is a rule. The conclusion is unchanged; it now rests on a complete enumeration
rather than a partial one.
