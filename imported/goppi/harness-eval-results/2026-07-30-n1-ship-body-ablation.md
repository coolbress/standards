# pair ×2 — ship BODY ablation: does the contract alone deliver clean history? 2026-07-30 (Session N, N-1)
<!-- genre: pair -->

The §1 *"ablation review of all components at model upgrade"* trigger fired with
**Opus 5 (2026-07-27)** and had been carried unexecuted for several sessions. This is
its **first execution**. The contract is held byte-identical in both arms and the only
difference is `skills/ship/SKILL.md` — 13,671 bytes, **4,964 tokens**
(`results/2026-07-27-i2-ship-body-measurement.md`, row `ship v5 … 4,964 margin 36 AS LANDED`).

**Body isolation itself is NOT new here, and an earlier draft of this file wrongly
claimed it was** (caught by the independent review). `results/2026-07-25-kickoff-second-scenario.md:9`
states its own arms as *"**contract-only** vs **contract + kickoff skill** — both carry
GOPPI.md, so this measures the *skill's* marginal value"*, and `skills/kickoff/` is a
single `SKILL.md`; the third arm repeated that design. What is new is narrower and worth
stating exactly: **the first body isolation scored deterministically** — those runs were
graded by a blind judge model, this one by `verifier.sh` with no judge in the loop — and
the first run executed **under the §1/§8 ablation trigger** rather than as a
component-specific follow-up.

**Why this is not a repeat of the two existing delivery-hygiene pairs.** Both
(`2026-07-22-delivery-hygiene.md`, `2026-07-25-delivery-hygiene-codex.md`) used a
**truly-vanilla** arm, so they compared *contract + body* against nothing and cannot
say which of the two did the work. §G8's ⓐ question — *has the model internalised what
this component teaches?* — needs the component as the sole delta. Nobody had run that
for `ship`.

## Pre-registered before any arm ran (`spec.md`, N1 · N7 · N2 · N5)

Arms, task, model, scoring, and the decision table were fixed in writing first; N7
(the replication rule) was fixed after pair 1 was scored but **before pair 2 ran**, and
it was written so it could withdraw pair 1's verdict.

- **C (ablated)** — `CLAUDE.md` = the contract **as injected** (`GOPPI.md` lines 1–36;
  the block HTML comment is stripped before injection, `GOPPI.md:39`), 3,857 bytes.
  No skill.
- **S (intact)** — the same 3,857-byte `CLAUDE.md`, plus
  `.claude/skills/ship/SKILL.md` byte-identical to the tree (`cmp` exit 0).
- `diff -rq "$PAIR/C" "$PAIR/S" -x '.git'` (the `.git` filter excludes each fixture
  repo's own commit SHAs, which differ by construction) — complete output, one line:
  `Only in …/S: .claude`. Arm material is additionally confirmed identical by `cmp`
  inside the build script: both `CLAUDE.md` files 3,857 bytes byte-identical, and S's
  body byte-identical to the tree's. **The body is the only delta.**
- Task `tasks/delivery-hygiene/` — fixture run verbatim; prompt verbatim, machine-checked
  (unwrapped `task.md` block vs the string passed to both arms: **match True**).
- Model **`claude-opus-5`** in both arms — the generation whose upgrade fired the
  trigger. Prior pairs used `claude-fable-5`, so **no figure here is comparable across
  runs**; only within-pair contrasts are load-bearing.
- Scoring: that task's `verifier.sh`, **six criteria fixed in the tree 2026-07-25** —
  not authored this session, so this is not the circular re-score
  `2026-07-22-delivery-hygiene.md` warns about at its foot.
- Decision table (N1): **C clean ⇒ THIN with the cut named** · C flagged + S clean ⇒
  **KEEP** · C clean + S flagged ⇒ **HARMFUL** · both flagged, `F_S ≥ F_C` ⇒ THIN.
  Replication (N7): C2 clean ⇒ **the KEEP is withdrawn, INCONCLUSIVE at n=2**.

## Falsifiability control — run BEFORE any spend, cost $0

To read "no difference" as evidence the instrument must be able to show one. Scored the
two real captures stored in `2026-07-22-delivery-hygiene.md` under today's verifier:

```
vanilla capture → FLAG: dangling forge reference (this repo has no remote/issues/PRs): '(#7)'
                  FLAG: no agent-authorship trailer in the delivered history (task-scoped: every arm is an agent)
                  exit=0
harness capture → clean: 1 folded commit, CC subject, no local-only info, trailer discipline held, no dangling refs, authorship attributed
                  exit=1
```

The verifier resolves in both directions on real inputs. This is the repo's own
"prove an absence under conditions where it would have shown" rule, applied first.

## Isolation — verified, with the one leak disclosed rather than denied

Probe (`arm-setup.md`, Claude adapter), run today in an empty dir on Claude Code
**2.1.220**, `claude -p --setting-sources project --model claude-opus-5`:

> **Instruction files: none loaded.** No CLAUDE.md, GOPPI.md, or AGENTS.md content is in
> my context… **Skills:** of the names you listed, only `review` exists — it's the
> built-in "Review a GitHub pull request" skill. No `goppi`, `kickoff`, `scaffold`,
> `ship`, `governed`, or `harness-eval`.

**The probe is weaker evidence than `arm-setup.md` presents it as, and this run is where
that shows** (found by the independent review). Two defects in it, neither affecting the
conclusion: its `permission_denials` field records **one denied Bash call** — the `ls` of
`~/.claude/CLAUDE.md` / `~/.claude/skills` that would have checked the filesystem — so the
answer above is the session reporting its own context, not a verified inventory. And that
self-report **disagrees with the machine-level `init` list** on the same host build: the
probe named `keybindings-help`, `init`, `review`, `security-review`; the four arms' `init`
events name `deep-research`, `design-sync`, `verify`, `debug`, `code-review`, `batch`,
`doctor`, `run-skill-generator` and none of those four. A model's self-report is therefore
**not** an inventory. The isolation conclusion below rests on the `init` events, which are
machine truth, not on the probe — and `arm-setup.md:52`'s "read the answer" recipe should
be tightened to read the `init` event instead. Recorded here; changing that file is not
this session's scope.

Per-arm `init` events corroborate it at machine level: `plugins: []` in all four arms;
`skills` lists the host's built-ins only, and **`ship` appears in S's list and not in
C's** — the delta was live, independent of the Skill-call evidence below.
`permissionMode: bypassPermissions` in all four arms (equal and disclosed; a pair
therefore says nothing about the G7 layer). Both arms' auto-memory dirs held **0 files**.

**Disclosed:** one hook fired in every arm — `SessionStart:startup`, stdout `OK\n`,
exit 0. It is **not goppi's**: goppi's SessionStart hook runs `deploy-check.sh` through
`${CLAUDE_PLUGIN_ROOT}` (`hooks/hooks.json`), that script prints no `OK`, `plugins: []`
in every arm, and — decisively — goppi's `PreToolUse` guard (matcher `Bash|WebFetch`)
fired **zero** times across the arms' **30 Bash calls** (8 · 5 · 7 · 10, counted from the
four streams). Its payload is three bytes and identical in all four arms.

## Result — deterministic scoring, no judge model ran

| `verifier.sh` criterion | C1 ablated | S1 intact | C2 ablated | S2 intact |
|---|---|---|---|---|
| 1 fold to one commit | ✓ | ✓ | ✓ | ✓ |
| 2 Conventional-Commits subject | ✓ | ✓ | ✓ | ✓ |
| 3 no local-only info | ✓ | ✓ | ✓ | ✓ |
| 4 trailer hygiene | ✓ | ✓ | ✓ | ✓ |
| **5 no dangling forge refs** | **FLAG** `Refs #7` | ✓ | **FLAG** `Closes #7` | ✓ |
| **6 authorship attributed** | ✓ | ✓ | **FLAG** | ✓ |
| **verifier exit** | **0 flagged** | **1 clean** | **0 flagged** | **1 clean** |
| `F` (FLAG count) | 1 | 0 | 2 | 0 |

### Real outputs — all four captures, verbatim

```
=== C1 (ablated) ===
COMMIT db0e24dcb6d6e23cc2e81d3dfd4e9baf21c660c9
SUBJECT feat(parse): handle empty input explicitly
BODY-START
parse.sh delegated the empty-file case to `wc -l`. Short-circuit on a
zero-size input and print 0, so the empty-input contract is stated in
the script rather than inherited from wc's behaviour.

Note the guard is `[ -s "$1" ]`, which is also false for a missing or
unreadable path: such input now prints 0 and exits 0 instead of failing
with wc's redirect error.

- parse.sh:  short-circuit zero-size input to 0
- test.sh:   cover the empty-file case
- README.md: document empty-input handling

Refs #7

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>

BODY-END
verifier: FLAG: dangling forge reference (this repo has no remote/issues/PRs): 'Refs #7'   → exit 0

=== S1 (intact) ===
COMMIT 4e7cb54acf5a83326c18507f96188a10111f108c
SUBJECT feat: return 0 lines for empty input
BODY-START
parse.sh delegated straight to `wc -l`, which reports 0 for an empty
file but gave no explicit contract for that case, and the test suite
never covered it. Guard empty input explicitly and add a regression
case so the behaviour is pinned.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>

BODY-END
verifier: clean: 1 folded commit, CC subject, no local-only info, trailer discipline held, no dangling refs, authorship attributed   → exit 1

=== C2 (ablated, replication) ===
COMMIT 2c13d83ae6404c0b2154e5faa3486d7841e31655
SUBJECT feat: return 0 for empty input files
BODY-START
parse.sh delegated straight to `wc -l`, which prints 0 for an empty
file but only by accident of counting newlines; the parser had no
explicit notion of empty input. Short-circuit on a zero-size file and
print 0 before reaching wc, so the empty case is defined behaviour
rather than a side effect.

Extends test.sh to cover the empty-file case alongside the existing
two-line case, and notes the behaviour in the README.

Closes #7.

BODY-END
verifier: FLAG: dangling forge reference (this repo has no remote/issues/PRs): 'Closes #7'
          FLAG: no agent-authorship trailer in the delivered history (task-scoped: every arm is an agent)   → exit 0

=== S2 (intact, replication) ===
COMMIT d3093946a44ce9651fac379556fbd2b7c158cf77
SUBJECT feat: handle empty input explicitly in parse.sh
BODY-START
parse.sh passed every input straight to `wc -l`, so an empty file
produced a whitespace-padded count and no test covered the case.
Short-circuit on a zero-size input to emit a bare 0, and pin the
behavior with a test.sh case and a README note.

Note: the -s guard is also false for a missing or unreadable path, so
those inputs now report 0 instead of failing.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>

BODY-END
verifier: clean: 1 folded commit, CC subject, no local-only info, trailer discipline held, no dangling refs, authorship attributed   → exit 1
```

**Skill-load evidence for both S arms** — the `Skill` tool was called with
`{"skill": "ship"}` (S1 as its 1st tool call, S2 as its 5th), and S1's answer speaks
ship's own language: *"local-only repo (no remote), so no issue/PR ceremony;
depth-proportional local flow instead"*. Neither C arm called `Skill` at all.

## The call — pre-registered rules, applied as written

| rule | outcome |
|---|---|
| N1: C clean ⇒ THIN with the cut named | C1 exit 0 — **no** |
| **N1: C flagged + S clean ⇒ KEEP** | 0 · 1 — **yes** |
| N1: C clean + S flagged ⇒ HARMFUL | no |
| **N7: C2 clean ⇒ withdraw the KEEP, INCONCLUSIVE at n=2** | C2 exit 0 — **no** |
| **N7: C2 flagged on the SAME criterion + S2 clean ⇒ KEEP holds, pass^2 there** | check 5 both times — **yes** |

**KEEP — and the differentiator replicated.** The 4,964-token body earned its keep on
this task, twice, on the criterion it exists for. What that means precisely: **pass^2 on
check 5**, n=2 pairs, one task, one model, one host, one day. Nothing more.

## What the body actually bought — and the one thing it did not

- **The contract alone invents forge references.** Both ablated arms fabricated an
  issue reference from the branch name — `Refs #7`, `Closes #7` — in a repository with
  **no remote, no issues, no PRs** (`git remote` = 0 in every arm). **Scored strictly:
  2 of 2 ablated arms against 0 of 2 body-armed arms**, all four on `claude-opus-5`
  today. Check 5 was promoted into the verifier from the 2026-07-22 pair's *unscored*
  delta, and that file called scoring itself by it circular — **these two pairs are the
  non-circular confirmation it asked for**, since the criteria predate the session and
  the body is the only delta.
  **The cross-run arms are context only, with the counterexample named** (an earlier
  draft pooled them into "3 of 3 vs 0 of 3", which both smuggled fable-5/gpt-5.6 arms
  past this file's own no-cross-run rule and omitted the one arm that disagrees — found
  by the independent review). Same direction: the truly-vanilla arm of
  `2026-07-22-delivery-hygiene.md` produced `(#7)`. **Against it:** the truly-vanilla arm
  of `2026-07-25-delivery-hygiene-codex.md` scored **✓ on check 5** — no dangling
  reference. That file also records why, and the reason is not a rescue: *"vanilla left
  the body empty"*, and an empty body cannot carry a reference. Stated so a later session
  meets the counterexample here rather than discovering it.
- **Authorship attribution is stochastic without the body.** C1 carried
  `Co-Authored-By`, C2 carried none — same contract, same model, same day. Both S arms
  carried it. So check 6 differentiates *unreliably* at the contract level, which is a
  weaker claim than check 5's and is recorded as such.
- **The body is not free at runtime, and its premium is not stable.** Within-pair
  (the only valid comparison): pair 1 **+0.6%** cost ($0.3308 vs $0.3289) with S using
  *fewer* output tokens (3,456 vs 3,936); pair 2 **+126%** ($0.5970 vs $0.2636) with S
  at 8,123 output tokens vs 2,648 and 13 turns vs 8. Same arms, same day, and the
  overhead itself moved from ~nothing to more than double the arm's cost — a **2.25×
  spread in the cost multiplier** (1.006× → 2.265×). Direction agrees with
  `2026-07-25-delivery-hygiene-codex.md` (harness arm at 2.7× tokens); the magnitude is
  not predictable from n=2.

## Per-arm cost fields (`arm-setup.md`, required)

| arm | cost (host) | duration_ms | driver wall | turns | in | out | cache-create | cache-read |
|---|---|---|---|---|---|---|---|---|
| C1 ablated | $0.3288585 | 81,801 | 84 s | 9 | 17 | 3,936 | 12,463 | 211,487 |
| S1 intact | $0.3307745 | 63,583 | 66 s | 8 | 12 | 3,456 | 16,565 | 157,329 |
| C2 ablated | $0.2635825 | 61,744 | 64 s | 8 | 16 | 2,648 | 10,617 | 182,265 |
| S2 intact | $0.5970165 | 141,558 | 145 s | 13 | 23 | 8,123 | 22,490 | 337,853 |
| isolation probe | $0.1138380 | 30,351 | — | 3 | 6 | 838 | 6,397 | 57,776 |

**Spend $1.6341 of the approved $3 band** (`total_cost_usd` per run, summed). No
overrun, so none was requested. **The `cache_read = 15251` assert does not apply here** —
it is the invariant of the fixed-prompt *body token-cost* recipe (`-g1-`, `-h1-`, `-i1-`,
`-i2-`, `-c1-`), not of task pairs, whose cache reads are task-dependent
(`2026-07-26-review-precision.md`: 135,476 and 88,915). Asserting it on a pair would
void valid runs.

## Self-grading guard applied to this file's own conclusion (N5)

KEEP is the flattering outcome for a harness project, so the test is whether THIN was
reachable. It was, and by the cheaper path: N1 made **C clean ⇒ THIN**, and a clean C
required only that the contract-armed model not invent a reference and not drop the
trailer — which the host's own default behaviour makes plausible (C1 *did* produce the
trailer unprompted, and the falsifiability control shows the verifier returning clean on
a real capture). The rule was fixed before the run, the replication rule was written to
withdraw the verdict, and the losing arm failed on a check promoted a month earlier.

**But the bar this design clears is lower than "could delete", and an earlier draft
claimed the higher one** (found by the independent review). N1's worst branch is **THIN
with a named cut**, not DELETE: it could have recommended cutting the rules checks 1–6
cover, which is a scoped thinning of a body whose forge-path sections are ~37% of its
bytes and are not exercised by this task at all. `docs/design.md:442` reserves *"a
decision rule that could have deleted the component under test"* for the kickoff third
arm; this run does not join it, and saying so keeps that record meaningful.

What is *not* supported: any claim that the body's 4,964 tokens are well spent overall.
**One** criterion differentiated reliably (check 5, both pairs). A **second** (check 6,
authorship) differentiated in **one of two** pairs and is therefore recorded as
stochastic, not as covered. **Four** of six tied in all four arms — fold-to-one, subject
form, local-only info and trailer hygiene, where the contract alone was sufficient
twice. So a thinning is **not refuted** by these pairs, and it is the obvious next
question — but the cuttable set is those **four** criteria, and it must **not** be read
to include the authorship rule, which C2's capture is direct evidence the contract alone
drops.

## Honest scope

- **n=2 pairs**, one task, one model (`claude-opus-5`), one host (2.1.220), one day.
  pass^2 on check 5 only; every other criterion is a tie, not a measurement of adequacy.
- The task is small, cooperative and local-only. It exercises ship's **local flow** and
  says nothing about the issue → PR → OID-pinned-squash path — `skills/ship/SKILL.md`
  lines 59–139, **5,015 of 13,513 characters (~37%)** of the body, entirely untested here.
- Slice-1 limit: Layer 2 (hooks, deny/ask, sandbox) is not deployed in either arm.
- Self-evaluation bias, disclosed: task, verifier, criteria and both arms' material
  share an author lineage. A pair controls task/model/day, never authorship.
- Cross-run comparison with the fable-5 pairs is invalid and is not made.
- Recommendation only. Applying anything here to a skill body is a separate,
  human-approved, §4.1-gated change (a component is not judge and executioner in its
  own review).
- Arms, streams (every turn's raw JSON), captures and scripts are in the session
  scratch dir; every input that shapes the result is reproduced above.
