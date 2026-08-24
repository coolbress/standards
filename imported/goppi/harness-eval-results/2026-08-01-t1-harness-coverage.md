# t1 — eyes on the suites the harness could not see (2026-08-01, Session T)
<!-- genre: measurement -->

**What was measured**: for each of the 18 `*.test.sh` suites carrying **no**
falsifiability switch, whether one belongs there at all — and, where it does,
whether the suite actually goes red when a property its own script calls
load-bearing is removed. The starting claim about those 18 was never "no defect".
It was **"never looked"**, and this file is the looking.

**Instrument**: `evals/mutation-harness.sh` + `evals/mutations.tsv`. Machine: darwin
25.5.0, arm64, bash 3.2.57, gitleaks 8.30.1 present. Every suite run from the
repository root; every hand-run wrapped in `bash -c`, because these suites are
`#!/bin/bash` and Session R nearly published a false finding out of a zsh
word-splitting difference.

**Census, re-counted from the tree rather than quoted** (uncapped `find` for the
suites, and a sweep of the **prefix** `GOPPI_` rather than a list of switch names —
Session R's review found a missed occurrence precisely because a phrase search cannot
see a line-wrapped phrase): **24 suites · 6 with a switch · 18 without**. That
matches the handoff's figures, which is a result and not a formality: it is what
licensed reading the rest of the handoff's numbers as still current.

---

## ① The adjudication — all 18, each with its reason

Two criteria decided this, and **both were discovered by measurement during the
session**, before any mutation result was read:

- **DIALECT.** The harness reads verdicts off lines beginning `PASS: ` / `FAIL: `.
  Six suites speak a second dialect — `  ok: ` / `  FAIL: `, two-space indented —
  which its matcher never sees. A switch there buys nothing: every expectation is
  `ABSENT` in the baseline, so the harness reports **BLOCKED** and measures nothing.
  This is a property of the instrument, not of those suites.
- **RELOCATION.** The harness runs the mutant from a temp directory. A script that
  reaches for anything through `$0` behaves differently there for a reason that has
  nothing to do with the mutation — and **the harness's own guards do not catch
  that**: a case reddened by relocation reads as a **kill**. So before registering
  anything, each candidate's switch was pointed at an **unmutated copy** in a temp
  dir and the suite required to be exactly as green as in place.
  **The discriminator is the control, not the presence of `$0`** — a distinction the
  independent review had to supply, with a counterexample from inside the registry:
  `evals/floor-accounting.sh:103-106` resolves `../references/production-floor.md`
  through `$0` and passes the control **21/21**, because every case supplies the
  version through `$2`/`GOPPI_FLOOR_VERSION` and leaves that branch dead. It follows
  that **the control is a registration-time gate with no standing enforcement**: the
  natural next case for that suite — reading the current floor from the reference —
  would be green in place, red relocated, and read as a KILL. Named as a live residual
  risk rather than fixed here; re-run the control whenever a suite gains a case.

| suite | verdict | reason |
|---|---|---|
| `evals/additive-only` | **switch added** | control clean, 50/50 |
| `evals/floor-accounting` | **switch added** | control clean, 21/21 |
| `evals/issue-body-hygiene` | **switch added** | control clean, 14/14 (15/15 after the case §③ adds) |
| `evals/pr-body-hygiene` | **switch added** | control clean, 43/43 |
| `evals/spec-accounting` | **switch added** | control clean, 13/13 |
| `evals/workflow-hygiene` | **switch added** | control clean, 11/11 |
| `hooks/scripts/deploy-check` | **switch added** | control clean, 9/9 |
| `hooks/scripts/precompact-snapshot` | **switch added** | control clean, 5/5 |
| `hooks/scripts/secret-guard` | **switch added** | control clean, 46/46 |
| `evals/harness-eval/tasks/delivery-hygiene/verifier` | **switch added** | control clean, 22/22 |
| `hosts/goppi-doctor` | **does not fit — relocation** | resolves `SELF_DIR/../.codex/rules/goppi.rules`, `../evals/codex-rules-lint.py` and `../.claude/settings.json` through `$0`. Relocation alone reddens **26 of 75** cases. The switch was added, measured, and **removed again** |
| `evals/worth/run` | **does not fit — relocation** | `cd "$(dirname "$0")"` then requires sibling `cases/` + `verifiers/`; a relocated copy exits 2 with *"cases/ or verifiers/ missing next to run.sh"* before doing anything |
| `evals/adr-index` | **does not fit — dialect** | `  ok:` / `  FAIL:` |
| `evals/reference-wiring` | **does not fit — dialect** | `  ok:` / `  FAIL:` |
| `evals/remedy-discipline` | **does not fit — dialect**, and would not fit anyway | crosses many scripts by design (`secret-scan.sh`, `pre-push.sh`, `run-pair.sh`, …): there is no single script under test |
| `hosts/smoke-test` | **does not fit — dialect** | `  ok:` / `  FAIL:` |
| `evals/harness-eval/harness/run-pair` | **does not fit — dialect** | `  ok:` / `  FAIL:`. (ADR-0034 already recorded the separate reason that `GOPPI_PAIR_CLI` injects a *collaborator*, not the script under test) |
| `evals/harness-eval/tasks/review-precision/verifier` | **does not fit — dialect** | `  ok:` / `  FAIL:` |

**The relocation control earned its place on its first use.** `goppi-doctor` is the
suite a coverage-minded session would reach for first — 75 cases, a security audit,
an obvious switch point. Registering a mutation there would have produced a **false
KILL** off any of 26 cases that go red with no mutation present at all.

**The dialect finding is about the instrument, and it is not fixed here.** Teaching
the harness the second dialect would unlock six suites at once, but it changes the
tool whose whole worth is that its verdicts are trustworthy, and it needs its own
cases in `mutation-harness.test.sh` (including the one that makes it dangerous: those
suites print captured output indented, so a widened matcher can read a `FAIL:` line
out of a mutant's own stdout). Recorded as a separate unit of work, not slipped in.

## ② The mutations — 26 new, over 10 suites

Each breaks a property the target's **own comments** call load-bearing. Full run
after the two survivors below were resolved:

```
----- mutation-harness: 52 run · 52 killed · 0 survived · 0 error · 0 blocked
```

Registry: **15 suites · 52 mutations** (was 5 · 26). The registry remains a **floor**,
not a coverage claim — a property with no mutation written for it is unmeasured, and
§③ names one this session deliberately left that way.

## ③ Two survivors, both real, both reproduced by hand before being touched

**1. `issuebody-fence-strip-removed` — the fixture could not see its own property.**
`issue-body-hygiene.sh` scans a fence-stripped view so a body *quoting* a task
template neither satisfies nor trips the checks. Deleting the strip left the case
named *"fenced task-shape quote does not trigger task rule"* **green**. Reason: that
fixture's fence contains the trigger (`### Objective`) **and** a checkbox, so
un-stripping makes both visible and the two halves cancel — the body is judged
task-shaped and then found to have a checkbox. The case cannot fail for the reason it
names. Fixed **test-side and additively**: a new case whose fence carries the heading
**alone**, so the trigger is isolated. Re-ran the same mutation → **KILLED**.

**2. `additiveonly-multiset-becomes-set` — the property is not the one doing the
work, and the case named for it asserts nothing.** `additive-only.sh` says text is
compared as a **multiset** of meaningful lines, and fixture 12 is commented as the
regression that proved it (a `decision = "forbidden"` flipped to `"allow"` while a
sibling rule still carries that line). Replacing `have >= b[rec]` with `have >= 1`
left **both** its cases green. Reproduced by hand, and the reproduction is the
finding:

- Fixture 12 writes **one rule per line**, so the flipped rule's whole line vanishes.
  `have` is **0**, and plain set membership catches it too. The count decides nothing.
- Records are keyed by their enclosing `pattern = [...]`, added later against the
  swap attack — which makes the count redundant for **every** fixture in the suite.
- The case named *"the multiset count is shown"* asserted the substring `before`.
  The output carries `before` **three times** for unrelated reasons — *"present
  before, absent now"*, *"lost content that existed before"*, and the remedy line's
  *"restore the listed entries from the before-state"* — while the
  `(present N× before, M× now)` line is **never printed** for this fixture. It was
  green over nothing. (The third quote first shipped here as *"NO before-state"*,
  which comes from a different code path this fixture never reaches; corrected in
  review, and worth a line because a record whose authority is that its quotes are
  checkable must have checkable quotes.)

Resolved by registering the property that **is** load-bearing — the context key, which
the script's own comment calls *"association is what the swap attacks"* — and by
replacing the empty assertion with one that names the rule block the lost line sat
under. Re-ran → **KILLED (3/3)**. The multiset **count** stays **unmeasured**, and is
recorded as unmeasured in both the registry and the suite, rather than pinned by a
fixture invented to make it fire.

## ④ Cost, and the rule it crossed

| figure | measured, sequentially, nothing else running |
|---|---|
| `./check.sh` | **115.9 s** · **118.7 s** (two runs) |
| full mutation run | **269.9 s** |
| ratio | **2.27–2.33×** |

Per-suite, **all 15 measured** (% of 115.9 s): `issuebody` 2.0 s / 1.7% · `workflowhygiene`
2.7 s / 2.3% · `specaccounting` 2.8 s / 2.4% · `deploycheck` 4.1 s / 3.5% · `pincurrency`
4.5 s / 3.9% · `deliveryhygiene` 5.2 s / 4.5% · `flooraccounting` 6.6 s / 5.7% · `pinbump`
7.7 s / 6.7% · `prbody` 8.4 s / 7.3% · `secretguard` 14.3 s / 12.4% · `pairtally` 19.7 s /
17.0% · **`precompact` 24.8 s / 21.4%** · **`additiveonly` 27.8 s / 24.0%** · **`secretscan`
73.7 s / 63.6%** · **`prepush` 82.2 s / 70.9%**.

**Eleven of fifteen are under 20%, four are not, and the two heaviest are the two that
were already in the registry** — `prepush` and `secretscan`, not anything this session
added. ADR-0034's placement rule selects **"scheduled job"** above 2×; that firing is
executed, not noted, by **ADR-0036**, which applies the rule to the run a gate change
actually triggers and gives the full run its own trigger.

**The first version of this section reported three of the fifteen and ADR-0036 turned
them into "every suite sits in the first bucket".** The independent review measured a
fourth and refuted it. The fix was to measure all fifteen — not to soften the sentence
— and the failure is left recorded here because it is the same shape (a universal from
a filtered sample) this session spent its day finding in other people's tests.

## ⑤ What this run does NOT show

- **Nothing about the 6 dialect suites.** Not "no defect" — not measured. The same
  distinction this session exists to keep.
- **Nothing about `goppi-doctor` or `worth/run`.** Both are unmeasurable by this
  instrument as built, for reasons named above, and both are real gates.
- **Nothing about properties with no mutation.** 26 mutations over 10 suites cover
  26 properties, not 10 suites.
- **Nothing about whether these suites test the right things.** The harness measures
  whether a suite *can* fail. Its own header says so, and it is worth repeating on a
  session whose headline number is 52/52.
