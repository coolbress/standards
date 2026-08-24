# measurement — G5 token calibration, 2026-07-25 (NOT a pair)
<!-- genre: measurement -->

Session B item 4: put real numbers behind design §7's token budgets and the
§11 G5 "<5%" draft threshold. This is a **host token measurement**, not a
harness-vs-vanilla pair — recorded here because it shares the results
convention (real outputs, honest scope).

## Method (disclosed)

Four 1-turn headless runs, identical trivial prompt ("Reply with exactly:
OK"), `claude -p --setting-sources project --output-format json`, model
`claude-fable-5` pinned, Claude Code 2.1.220, isolated scratch dirs. The
injected-context size is read from the host's own `usage` fields;
`cache_read_input_tokens` was **identical (15,251) across all four runs**
(the shared system+tools layer), so deltas ride purely on
`cache_creation_input_tokens`. M4 measures the review skill body by
injecting it as the project CLAUDE.md — a host-tokenizer count of those
bytes as context; the on-trigger skill-load wrapper may differ slightly.

## Raw results

```
m1 result='OK' in=2 cc=6000  cr=15251 TOTAL_CTX=21253 out=4  cost=0.1355 turns=1
m2 result='OK' in=2 cc=7209  cr=15251 TOTAL_CTX=22462 out=15 cost=0.1602 turns=1
m3 result='OK' in=2 cc=8227  cr=15251 TOTAL_CTX=23480 out=4  cost=0.1800 turns=1
m4 result='OK' in=2 cc=11837 cr=15251 TOTAL_CTX=27090 out=16 cost=0.2528 turns=1
```

- m1 = empty dir (baseline) · m2 = + `CLAUDE.md` = GOPPI.md contract ·
  m3 = m2 + all 6 goppi skills under `.claude/skills/` · m4 = `CLAUDE.md` =
  review SKILL.md body only (772 / 2,302 words for contract / review body).

## Findings vs the recorded budgets

| Claim (design §7) | Measured (this host/model/day) | Verdict |
|---|---|---|
| always-injected ≤ 2k tokens | contract 1,209 + 6 skill descriptions 1,018 = **2,227** | **over target by ~11%** |
| ≤ 5k tokens per skill body | review body as-injected = **5,837** (2,302 words × ~2.5 t/w — template blocks tokenize heavily) | **over cap** (P2-1 suspicion quantified) |
| harness overhead < 5% of work tokens (draft) | small-task pairs, same day: Claude false-completion contract-only **+13.8% cost**; Codex false-completion **−0.4%** (noise); Codex delivery-hygiene contract+ship **+169% tokens** | **decisively exceeded at small-task scale** — the only scale measured; review #2 #17's "a ratio hides a small task's large overhead" now has numbers |

## Honest scope

- One host (Claude) for the injection measurements; Codex reports only
  per-run totals (no cache split), so its always-injected surface is not
  separable this way. Overhead ratios cover both hosts via the pairs.
- The skills-description injection (m3−m2 = 1,018) measures **project-level**
  `.claude/skills/` deployment; the plugin path injects the same description
  text but was not separately measured.
- Hook notices (deploy-check etc.) are part of the real deployed
  always-injected surface and are NOT in these numbers — the deployed total
  is ≥ 2,227, not exactly it.
- Single measurement per point (deltas are exact host-reported integers, but
  day/version variance is unmeasured). Numbers feed §7 + §11 G5; the "<5%"
  draft threshold is retired by this measurement (see design §7/§11 edits,
  Session B).
