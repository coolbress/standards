# t2 — the eight the instrument could not see, and the defect that was only half closed (2026-08-01, Session T2)
<!-- genre: measurement -->

**What was measured**: whether the 8 suites `2026-08-01-t1-harness-coverage.md` recorded
as *"not measured, not clean"* were blocked by anything about **themselves** — and what
`additive-only.sh`'s **multiset count** actually does, a property t1 recorded as
unmeasured rather than resolved.

**Both answers were no and worse-than-unmeasured.** The 8 were blocked by the
instrument. The count was reachable, and wrong where it fires.

**Instrument**: `evals/mutation-harness.sh` + `evals/mutations.tsv`. Machine: darwin
25.5.0, arm64, bash 3.2.57, gitleaks 8.30.1 present. Every hand-run wrapped in
`bash -c`. Every claim below names a command whose output was read.

---

## ① The instrument's two blind spots, each with its before-state

| | before | after |
|---|---|---|
| **Dialect** — the reader took `PASS: `/`FAIL: ` at column 0; six suites print `  ok: `/`  FAIL: ` at two | a real mutation of `adr-index.sh`: **BLOCKED, exit 3**, *"expected case is 'ABSENT' in the UNMUTATED baseline"* | **KILLED, exit 0** |
| **Relocation** — the mutant ran from a temp dir, where a `$0`-relative lookup cannot resolve | `goppi-doctor`'s suite under an **unmutated** temp-dir copy: **49 pass / 26 FAIL** | beside its original: **75 / 0** |

**Each fix carries a false-kill path, and each path is refused by a fixture rather than
by an assertion.** These are in `evals/mutation-harness.test.sh` and fail without the
change:

- Both dialects print a failing case's **captured output** — the mutant's own stdout,
  which for these gates routinely contains the literal `FAIL:` — indented by six. A
  fixture emitting exactly that and nothing else must come out **BLOCKED**, not
  KILLED. The indent bound (0 or 2 spaces, never 3+) is the whole safety property.
- Cleanup is proved on **success**, on **ERROR** (which `continue`s past the inline
  removal, so only the trap can run), and on **SIGTERM** — with the mutant asserted
  **present at the moment of the kill**, so "nothing left behind" cannot pass
  vacuously.
- The switch value must be **absolute**. This one was found by the relocation control,
  not by design: the first version of the new placement produced a *relative* path, a
  `cd`-ing suite got **exit 127**, and the harness would have read that as a case going
  red — a kill. Second session running in which that control paid on first use.

## ② The census, closed to its floor

**7 of the 8 registered** (plus the harness's own suite, which review found unnamed): `adr-index` · `reference-wiring` · `hosts/smoke-test` ·
`run-pair` · `review-precision/verifier` · `goppi-doctor` · `worth/run`. Every one
passed the relocation control **under the new placement** before any mutation was
written for it.

**`evals/remedy-discipline.test.sh` is still out, and nothing here changes its
reason**: it drives **twelve** different scripts, so there is no script under test.
That is the floor of this census, not an item of unfinished business.

Registry: **15 → 23 suites, 52 → 70 mutations.**

## ③ Three more cases that could not fail for the reason their names gave

Found on first contact with suites nothing had ever mutated:

| case | why it could not fail | fix |
|---|---|---|
| `AGENTS.md-cited reference passes (exit 0)` | hand-rolled if/else — the FAIL line reads `agents-cited: rc=1`, so a PASS-text matcher never sees the kill | registry expectation moved to the documented `<green>>><red>` form |
| `substring collision: ladder.md flagged…` | same shape (`substring: rc=0 out=…`) | same |
| `an item declaring the file sound is not a finding even with a severity word in it` | its fixture named a file with **no line anchor**, so the item was dropped by *"named but not anchored"* one rule earlier and the sound-listing rule never ran | line anchor added to the fixture; the case can now fail for its named reason |

The first two are the trap `evals/mutations.tsv`'s own header documents, walked into
because dialect-B suites use hand-rolled if/else far more. The third is the **same
shape** as the fence fixture t1 fixed — three in two sessions.

## ④ `additive-only`'s count: reachable, and wrong where it fires

t1 recorded the multiset count as **unmeasured**. Measured here, one probe per text
mode, **before any change**:

| probe | verdict | was a control actually lost? |
|---|---|---|
| `.gitignore` lists `.env` twice, one copy removed | **CLOBBER, exit 1** | **No** — `git check-ignore .env` → **still ignored** |
| `.codex/config.toml`, a key repeated in one table | CLOBBER, exit 1 | before-state is **invalid TOML** |
| `.codex/rules/*.rules`, a line repeated in one rule block | CLOBBER, exit 1 | before-state is **malformed** |
| `.codex/config.toml`, an element repeated in a multi-line **array** | CLOBBER, exit 1 | **both states are valid TOML** — a real false block, added by the review, not by these probes |

So two of the four firings are **false blocks**. The `.gitignore` one is the one acted on, because it is the file for which this
script already owns an exact instrument (`gitignore_control_loss()` asks git itself),
and on a gate whose false blocks land on **a repository goppi does not own**.

**ADR-0037**: the count stays strict everywhere except `.gitignore`; a line that
disappears **entirely** is still a loss in both modes. Both edges are now cases —
including one asserting **git agrees**, so the pair cannot pass over a check that
stopped looking — and both are held by registry rows.

**The option not taken is the one worth recording**: pinning the current behaviour with
a fixture would have "measured" the count and blessed the false block in the suite,
permanently. Measured is not the goal; correct is.

## ④b What the independent review found — including in this session's own proofs

Stage 1 came back **FAIL**, and the two HIGH findings were both reproduced by hand
before anything was changed:

1. **The `.gitignore` relaxation dropped a true positive.** gitignore is
   last-match-wins, so duplicate patterns straddling a `!` are **order-sensitive**:
   `*.pem` / `!ca-bundle.pem` / `*.pem`, de-duplicated, **stops ignoring
   `ca-bundle.pem`**. Measured: `main` blocked it (rc=1); this branch waved it through
   (`additive ✓`, rc=0). The "exact instrument" the relaxation deferred to was not
   exact — `gitignore_control_loss()` **skipped negations entirely**, so the one path
   whose semantics changed was never probed. Fixed by probing negations too, and by
   licensing the relaxation on the probe being available at all rather than on the
   filename. A false PASS on a gate that protects someone else's repository, shipped by
   me, caught by the review — which is exactly the asymmetry ADR-0031 records.
2. **The cleanup was defeated by a signal on any multi-mutation run.** `trap cleanup
   EXIT INT TERM HUP` with a handler that returns lets the loop continue with `$TMP`
   already gone: the next mutant is written, never logged, never removed. Reproduced
   against the shipped registry — TERM → 2 leftovers, HUP → 2. **The self-test could
   not see it because its registry declared exactly one mutation.**

And the finding that matters most for method: **two of this change's own proofs could
not fail.** The captured-output fixture emitted its `FAIL:` before its `PASS:`, so an
unbounded matcher returned BLOCKED — the same verdict as the bounded one. The
absoluteness case ran against an already-absolute target. Both are rebuilt, and all
three properties are now verified by **perturbation**: restore the regression, run the
suite, watch the named case go red.

| perturbation | case that goes red |
|---|---|
| matcher strips all leading whitespace | *"a 6-space-indented `FAIL:` … is NOT read as a case line"* |
| mutant path made relative again | *"the switch value handed to the suite is ABSOLUTE"* |
| signal handlers no longer exit | *"nothing is left behind when the harness is KILLED mid-run"* |

Four more, all accepted and reproduced: the drift guard named **15 of 22** suites
(deleting every `adrindex` row left `check.sh` green); `evals/mutation-harness.test.sh`
was itself **unregistered and unnamed** — the census that claimed to be closed was 22
of 24, not 23, and it is now registered; ADR-0037's *"malformed input only"* was
**refuted by valid TOML** (a repeated element in a multi-line array), so the residual
false-block class is now named rather than denied; and `hosts/smoke-test.test.sh`
leaked the product's own `FAIL:` lines at **column 0**, below the indent bound, which a
future registry row could read as a case of that suite — indented at the source.

## ④c The three "not solvable here" items, re-checked on request — two reasons were wrong

The delivery record carried three items forward. Asked to re-check them, **two of the
three deferrals turned out to rest on claims that had never been tested**:

| item | the reason given | what measuring it showed |
|---|---|---|
| register `remedy-discipline` | *"drives many scripts, so there is no single script under test"* | wrong about the **registry**: `suite_index()` keys on the **label**, so one test file takes one row per collaborator. Registered, two rows, both mutations killed |
| make the relocation control standing | *"a manual registration-time gate"* | avoidable at **zero cost** — the baseline run already happens; pointing it at an unmutated copy in the mutant's place makes it the control |
| the valid-TOML false block | *"relaxing it would have nothing behind it — no TOML equivalent of `git check-ignore`"* | the equivalent is a **parser**, and this repo already applies one to JSON. `toml_subset()` mirrors `json_subset()` |

**The census now closes at 24 of 24 suites** (25 rows, **74 mutations, 74 killed**, 547.1 s against a `check.sh` of 156.3 s). The structural
TOML comparison is not merely a relaxation: it is **strictly stronger** on the attack
the text path existed for — a `":root"` swapped between two profiles is a value change
at a keyed path, named rather than inferred from line bookkeeping — and both directions
are pinned by cases plus a registry row.

**And the baseline-as-control found something on its first run**: the five suites that
predate the control (`prepush`, `secretscan`, `pincurrency`, `pinbump`, `pairtally`) had
**never been checked against it**. All five pass — measured, for the first time.

**The registry caught the refactor moving a property.** Routing `.toml` to a parser
moved the `":root"`-swap case from the text context key to the structural comparison,
and the next full run reported `additiveonly-context-key-removed` as a **SURVIVOR** —
its expectation named a case the text path no longer decides. Re-pointed, and the new
mechanism given its own row. A property silently losing its pin during an improvement
is exactly what this machinery is for, and this is the first time it caught one here.

The transferable lesson is not "try harder". It is that **a claim that something is
impossible needs the same evidence as a claim that it works**, and neither of these two
had any. That is the same defect this whole session has been finding in tests, stated
one level up: an assertion nothing exercised.

## ④d The second review, and what it found in the third pass

Stage 1 **PASS**, 7 findings (4 MED · 3 LOW), **all accepted, each reproduced first**.
The two that matter both landed inside the fix, not around it:

- **The structural TOML comparison bought its relaxation with three regressions.** A key
  added inside an array-of-tables element read as **a loss** (a false block on an
  *addition*, in the change whose purpose was removing a false block), and argv
  **reordering** and **type changes** stopped being seen — Python makes `False == 0` and
  `1 == 1.0` true. Six probes against `main`, before and after the fix: the only
  behavioural difference that now remains is the single relaxation ADR-0039 argues for.
- **The same move made an existing case vacuous, and no registry row could see it.**
  Case 23's fixture was `.codex/config.toml`; once that path went structural, its
  trailing-comment property stopped being exercised — proved by disabling comment
  stripping and watching the suite stay green. Moved to a `.rules` fixture, and the
  perturbation now reddens it. The registry caught the `":root"` swap changing hands and
  **could not** catch this one, which is the honest bound on the machinery: it works as
  far as the rows reach.

Also fixed: the drift guard had not been extended to the two new rows (deleting them
left `check.sh` green); the standing control is **expectation-scoped**, so the baseline
now reports how many cases are red and `CONTRIBUTING.md` keeps the manual whole-suite
control for when a suite gains a case; *"one row per collaborator"* overstated a suite
where **2 of 14** scripts are measured, now said plainly; the kill-moment assertion is
back to an exact count; and the BLOCKED remedy no longer says *"usually a missing tool"*
when placement is now a first-class cause.

## ④e The limitation that was recorded as a limitation — and then measured

The previous section ends with *"the machinery works as far as the rows reach"*, written
after a case went **vacuous** during a refactor with every gate green and no row able to
notice. That was accepted as a bound. It did not have to be.

**The data was already in every run**: the baseline holds every case a suite prints, and
each mutant run holds the ones that went red. Nothing was computing the complement. Now
each run ends by **naming, per suite, the cases no mutation reddens** (ADR-0040) — a
report, not a gate, because some cases legitimately cannot be pinned by mutating the
script under test, and failing on them would reward deleting honest cases.

First correct full run, keyed by **suite file** (two registry rows over one file are two
views of the same cases, not two suites):

| suite file | pinned | suite file | pinned |
|---|---|---|---|
| `pre-push` | 11 of 19 | `secret-scan` | 7 of 47 |
| `pin-currency` | 6 of 18 | `pin-bump` | 5 of 26 |
| `pair-tally` | 8 of 38 | `secret-guard` | **6 of 46** |
| `deploy-check` | 3 of 9 | `precompact-snapshot` | 2 of 5 |
| `workflow-hygiene` | 4 of 11 | `spec-accounting` | 3 of 13 |
| `floor-accounting` | 3 of 21 | `issue-body-hygiene` | 3 of 15 |
| `pr-body-hygiene` | 5 of 43 | `delivery-hygiene/verifier` | 3 of 22 |
| `additive-only` | 9 of 64 | `adr-index` | 3 of 10 |
| `reference-wiring` | 2 of 11 | `smoke-test` | 1 of 6 |
| `run-pair` | 1 of 21 | `review-precision/verifier` | 2 of 26 |
| `goppi-doctor` | 2 of 75 | `worth/run` | 2 of 8 |
| `mutation-harness` | 2 of 76 | `remedy-discipline` | 2 of 47 |

**74 mutations pin 95 of 677 cases.** That number was always true; it was never visible.
`secret-guard` — a security control — has **6 of 46** pinned, and that is a worklist now
rather than a feeling.

**The report found four defects in itself across its first runs**, which is the shape of
thing it exists to reveal, and the last three were found by the independent review of the
change that introduced it:
① comparing case names by **equality** reported *every* case as unpinned (a `FAIL:` line
carries its diagnosis after the name, so red text is never byte-equal to green);
② crediting only red lines reported `reference-wiring` as 11 of 11 unpinned while two of
its cases were demonstrably killed — the `<green>>><red>` form must be credited from the
baseline, not the red line;
③ recording the **expectation's text** instead of the full case name credited nothing
whenever the two differed by so much as an indent, so `pre-push`'s
`  ...and it says WHY…` was listed as unpinned in the same run that killed a mutation
over it;
④ crediting **before** reading the verdict marked a **SURVIVOR's** case as pinned, one
line below the harness saying the suite did not notice — blind exactly where it earns
its keep. Keyed by file, matched whole-line, credited from the baseline and only on a
found red text; each of the four is pinned by a self-test case.

## ⑤ Cost, re-measured

| figure | measured, sequentially, nothing else running |
|---|---|
| `./check.sh` | **127.3 s**, rc=0 ALL GREEN |
| full mutation run | **448.6 s** — 70 mutations over 23 suites, **70 killed** |
| ratio | **3.52×** |

Per-suite `--only`, this round: `referencewiring` 2.3 s · `adrindex` 2.4 s ·
`reviewprecision` 4.8 s · `runpair` 6.3 s · `goppidoctor` 10.9 s · `worthrun` 23.4 s ·
`codexsmoke` 26.1 s · **`additiveonly` 63.3 s (48.7%)** · **`secretscan` 71.4 s
(54.9%)** · **`prepush` 79.3 s (61.1%)**.

ADR-0036's rule holds through a registry that grew by half: every suite is in its
**first or second bucket, never its third**. The heaviest per-change trigger is no
longer `prepush` but `additiveonly` — it went from one mutation to three, and cost here
is **mutations × suite runtime**, so a third mutation on a 16-second suite costs more
than an entire cheap suite.

## ⑥ What this run does NOT show

- **Nothing about `remedy-discipline`.** Not measured, and structurally unmeasurable by
  this instrument as built.
- **Nothing about properties with no mutation.** 15 new mutations cover 15 properties,
  not 7 suites. The registry is still a floor.
- **Nothing about whether these suites test the right things** — only that they *can*
  fail. The harness's own header says so, and it is worth repeating twice in two
  sessions of headline all-killed numbers.
- **The relocation control remains a registration-time gate**, run by hand, with no
  standing enforcement. t1 named that gap; it is still open, and `floor-accounting`
  is still the live example (resolves through `$0`, passes 21/21 because no case
  reaches that branch).
