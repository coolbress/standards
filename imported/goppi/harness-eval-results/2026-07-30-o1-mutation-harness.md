# o1 — the mutation harness, first run in the tree (2026-07-30, Session O)
<!-- genre: measurement -->

**What was measured**: whether the suites carrying a falsifiability switch
actually go red when the property their cases name is removed from the script under
test — and what a full run costs, so its placement is decided by a number rather
than by preference.

**Instrument**: `evals/mutation-harness.sh` + `evals/mutations.tsv`, both landed in
this change. Run from the repository root (the harness sets its own cwd). Machine:
darwin 25.5.0, arm64, bash 3.2.57, gitleaks 8.30.1 present.

**Provenance of the mutations**: rows 1–8 are transcribed from the eight recipes
recorded in the backlog's NEXT UP entry, which earned their keep in Session L. The
five `pincurrency-*` rows and the four `pinbump-*` rows are new — those suites had a
switch and no recipe — and were derived from the properties their scripts' own
comments call load-bearing ("the ONE way this check could pass over a stale version",
"which is how an alarm gets ignored and then deleted", "THE RESULT IS READ BACK, not
inferred from `sed`'s exit code").

---

## Result

| suite | switch | mutations | killed | survived | error | blocked |
|---|---|---|---|---|---|---|
| `hooks/git/pre-push.test.sh` | `GOPPI_PREPUSH_HOOK` | 4 | 4 | 0 | 0 | 0 |
| `evals/secret-scan.test.sh` | `GOPPI_SECRET_SCAN` | 5 | 5 | 0 | 0 | 0 |
| `evals/pin-currency.test.sh` | `GOPPI_PIN_CURRENCY` | 5 | 5 | 0 | 0 | 0 |
| `evals/pin-bump.test.sh` | `GOPPI_PIN_BUMP` | 4 | 4 | 0 | 0 | 0 |
| **total** | | **18** | **18** | **0** | **0** | **0** |

**That table is the state AFTER two fixes this measurement forced** — one from the
run itself, one from the independent review of it. The first run against the shipped
registry was **13 killed / 1 survived**, and the survivor was real.

**The fourth suite was missing from the first cut of this file, and the way it went
missing is the finding.** `evals/pin-bump.test.sh:11` carries `GOPPI_PIN_BUMP`, the
identical shape to the other three. It was missed because the search for switches was
**filtered to the three names a handoff happened to name**, never run as a pattern
over the tree — the same defect as the `grep … | head -5` that put a false universal
negative on `main` in #126, and the exact thing rule O4 exists to stop. Found in
independent review, not by me. It guards the SHA-256 that `pin-bump.sh`'s own comment
calls the only thing standing between CI and an unverified binary.

**The census, with its criterion, since the first cut also stated an unfounded
count.** `check.sh` runs **23** `*.test.sh` suites. **Four** resolve the script under
test through an overridable `GOPPI_*` variable and are therefore measurable here; a
fifth (`GOPPI_MUTATION_HARNESS`) is added by this change for the harness's own suite;
the remaining **19** are not measurable this way without new surface. One suite looks
like an exception and is not: `evals/harness-eval/harness/run-pair.test.sh` injects a
*collaborator* via `GOPPI_PAIR_CLI` while resolving its script under test as
`$HERE/run-pair.sh` — dependency injection, a different mechanism.

### The survivor, and why it was not a false alarm

`pincurrency-no-pin-guard-removed` deletes the guard that refuses a workflow with no
`GITLEAKS_VERSION` pin. The case named for that property —
*"no pin found → exit 2, never a silent pass over nothing"* — **stayed green**.

Reproduced by hand before it was believed, because a tool's verdict is not evidence
either:

```
--- ORIGINAL ---
pin-currency: no GITLEAKS_VERSION pin found in '…/nopin.yml'
original exit=2
--- MUTANT (guard removed) ---
pin-currency: cannot order '' against '8.30.1'
mutant exit=2
```

With the guard gone, `PINNED` is empty, falls through to the version comparison,
which cannot order `''` and exits 2 for a completely different reason. **The case
asserted only the exit code, so it passed over a script that had lost the property
its own name claims** — and the operator would have been told the versions were
uncomparable rather than that the pin had vanished.

This is the same shape as recipe #5 (`missing-gate guard removed → 127 reaches the
catch-all and passes for the wrong reason`), arrived at independently in a different
file. Two of the four switch-gated suites have now been shown to contain it.

**Fix, test-side, and verified by re-running the mutation**: the case now also
asserts that the exit **names the missing pin**. Re-run: `pincurrency-no-pin-guard-removed`
**KILLED**. The assertion was written with **one name for both branches**, because a
case whose PASS text and FAIL text differ cannot be followed by the string it is
known by — which is the next entry.

### A trap met while building the instrument, and machine-checked because of it

The handoff warned that a harness must match the suite's **FAIL** text, not its PASS
text. The first version of this registry matched PASS text anyway and reported a
working mutation as a survivor. Two suites hand-roll `if/else` cases whose PASS and
FAIL lines say **different things** (`pre-push.test.sh`'s missing-gate message is the
live example). So the registry gained a `<green-text>>><red-text>` form: the green
text proves the case ran and passed **before** mutation, the red text is what the
kill is read from. Both directions are pinned in `evals/mutation-harness.test.sh`
(`a case with different PASS and FAIL text is KILLED via the '>>' form`, and *the
same case WITHOUT `>>` is a survivor, not a false kill*).

### A performance defect the first run exposed

`ensure_baseline` was called in a **command substitution**, so its memo array was
written in a subshell and discarded — every mutation re-ran the entire unmutated
suite. Visible in the output as one baseline line per mutation instead of one per
suite; the `pincurrency` run went **8.3 s → 4.7 s** once fixed. Recorded because it
would have inflated the placement measurement below by roughly the suite count.

---

## What the independent review found in the instrument itself

Six findings (1 HIGH · 3 MED · 2 LOW), **all reproduced in the tree before being
accepted** — a reviewer is untrusted data too. Three were defects in the harness that
would have let it report a kill over an experiment that did not happen, which is the
one thing this tool must never do.

- **HIGH — `--only` matching nothing exited 0.** `./evals/mutation-harness.sh --only
  prepush` (the natural shortening of the documented `--only 'prepush-*'`) and
  `--only <renamed-id>` both ran **zero** mutations and exited **0**, which the
  script's own header defines as *"every mutation killed"*. The empty-**registry**
  path was already guarded, in these words: *"an empty experiment cannot fail, which
  is precisely the defect this harness exists to detect."* The same defect reached by
  `--only` had no guard. Now exit 2, with the remedy naming the glob.
- **MED — a kill was read off a FAIL line *containing* the text, not *naming* the
  case.** Reproduced with two fixture cases where one name is a prefix of the other:
  a mutation breaking only the **second** scored as a kill of the **first**, which
  stayed `PASS`. No live instance in the shipped registry — but this repository grows
  case names by appending qualifiers, and this very change adds one. An expectation
  matching more than one distinct baseline case is now an **ERROR**.
- **MED — the mutant was proved *applied*, never proved *runnable*.** `cmp` proves
  the bytes changed. A substitution that unbalances a block reddens **every** case,
  including the named one, so the harness scored **KILLED** over a script that never
  executed — reproduced with `s/^fi$//m`. Two shipped rows delete multi-line blocks,
  exactly that shape. The mutant now goes through `bash -n`, and a parse failure is
  an **ERROR**.
- **MED — the switch census was wrong** (above), and the "eleven suites" figure
  followed from no stated criterion.
- **LOW — `pincurrency-pin-pattern-broken` had no anchor.** `s/GITLEAKS_VERSION:/…/`
  under `-0p` rewrites the first occurrence anywhere in the file; adding a header
  comment quoting the assignment would silently retarget the mutation onto prose,
  where `cmp` still sees a diff so it is not an error, and the run reports SURVIVED.
  Safe direction, but on the one suite this change had already had to fix. Anchored
  to the `sed` expression.
- **LOW — one reading, three roundings** (`2m46s` / `165 s` / `~2m45s`). Made
  consistent.

**Each accepted finding that named a failure path got a regression test in the same
batch**, and one of those tests immediately earned its keep: the ambiguity case first
exited 2 for the *wrong reason* — an unescaped `)` made `perl` fail — and the
message assertion caught it. A case passing for the wrong reason, inside the tool
built to find cases passing for the wrong reason.

---

## Wall-clock, and the placement it decides

Rule **O1** was fixed in `spec.md` **before** these numbers existed.

| measurement | value |
|---|---|
| `./check.sh` at `71c0a33`, before this branch existed | **2m19.21s** (139.21 s) |
| `./check.sh` on this branch, **including** the new harness self-test | **2m01.51s** (121.51 s) |
| full mutation run, **18 mutations, 4 suites**, post-review code | **2m46.39s** (166.39 s) |
| ratio against the two baselines | **119.5%** / **136.9%** |

The 14-mutation run before the review's fourth suite was added measured **2m45.65s**
— so `pin-bump` cost **0.7 s** of the total, because that suite touches only files
(no scanner, no git remotes). The ratio is unchanged in the bucket that matters.

**The two `check.sh` figures are run-to-run variance, not a speed-up** — the branch
adds a self-test and cannot be faster for that reason. Both are reported rather than
the flattering one, because the decision below is a ratio and picking a denominator
after seeing the numerator is the failure this file's own rules exist to prevent.
The bucket is the same either way.

Per-suite, from separate `--only` runs: `pinbump` **9.0 s** · `pincurrency` **4.7 s** ·
`secretscan` **1m11.35s** · `prepush` **1m22.48s**. (The middle two were timed on the
harness before a cosmetic `SC2015` rewrite of one `cp` line — `A && B || C` to an
explicit `if`, the exact form `CONTRIBUTING.md` says CI's older shellcheck rejects.
The decision figure above is post-review code, re-run after every edit.)

**O1 buckets**: ≤20% of baseline → blocking gate · 20%–2× → separate target ·
>2× → scheduled job. **166.39 s is 119.5–136.9%, in the middle bucket under either
denominator, so the rule selects `separate target`.**

**The rule's own robustness, since a 4-suite registry is not the last one.** The
blocking-gate bucket ends at ~28 s and the scheduled-job bucket starts at ~243 s
(against the 121.51 s baseline). The registry would have to roughly **1.5×** in
wall-clock before the answer changes — and `pin-bump`'s 0.7 s marginal cost shows the
growth is dominated by which *suites* are touched, not by mutation count.

The decision, its two rejected alternatives and the re-open conditions are recorded
in **ADR-0034**.

---

## What this run does NOT support

- **It is not a coverage measurement.** A property with no mutation written for it is
  unmeasured here. 18 mutations over four suites is a floor, and the absence of a
  mutation is not evidence that a property is pinned. The suites contain far more
  cases than the registry names.
- **It says nothing about the 19 suites without a switch.** `pr-body-hygiene`,
  `additive-only`, `remedy-discipline` and the rest cannot be measured this way until
  they carry one, and adding switches is new surface, deliberately not taken here.
  That figure is now stated against a criterion — "resolves the script under test
  through an overridable `GOPPI_*` variable", over the 23 suites `check.sh` runs —
  because the first cut of this file gave a count that followed from no criterion.
- **A kill proves a case is sensitive to that mutation, not that it is a good test.**
  A case can go red for a reason unrelated to what it asserts — which is exactly what
  the survivor above turned out to be in reverse, and why the `>>` form and the
  baseline precondition exist.
- **n=1 machine, n=1 day.** Wall-clock is hardware-dependent; the ratio to
  `check.sh` measured on the same machine at the same time is the portable part, not
  the seconds.

## One thing deliberately not added, with the grounds

**No `evals/worth/` fixture set for the harness.** The `worth/` layer measures what a
component catches that a null verifier would not — and for this component that is
exactly what `evals/mutation-harness.test.sh` cases 1 and 3 already measure (a lethal
mutation is KILLED; a behaviourally-inert one SURVIVES), plus two verdicts a null
verifier has no analogue for. A second runner over the same fixtures would restate it.
There is precedent for a checker without a worth set — `secret-scan`, `pin-currency`,
`pin-bump` and `adr-index` all lack one, so the 10 covered components are a set with
reasons, not a rule that every checker joins. Recorded rather than skipped silently,
because `delivery-hygiene-verifier` **is** in that set on the ground that measurement
logic must prove its own worth, and this is measurement logic.
