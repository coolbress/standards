# q5 — the security hook's 40 unpinned cases, the three rules that had no case at all, and the report that could not count (2026-08-02, Session Q)

<!-- genre: measurement -->

**What was measured**: whether the cases `2026-08-01-t2-harness-coverage-closed.md`
reported as unpinned in `hooks/scripts/secret-guard.test.sh` — **6 of 46 pinned**, the
emptiest and highest-value entry on that list — can be pinned by mutating the script
under test, which is the only method ADR-0040's report licenses.

**They can, all of them.** But the rows were the cheap part. Four things the report could
not have told anyone about came out of the probe that had to run first: a case that
**passed vacuously**, three documented rules with **no case at all**, a property whose
two halves are **redundant** so neither is individually measurable, and — the one that
matters beyond this suite — **the report itself was under-counting every suite in the
tree**.

**Instrument**: `evals/mutation-harness.sh` + `evals/mutations.tsv`. The harness **was
changed** partway through, on the user's instruction, once ⑥ established it was
mis-crediting; everything measured before that point is labelled with which side of the
fix it came from. Machine: darwin 25.5.0, arm64, bash 3.2.57. Every claim names a command
whose output was read — including the one claim in this session that turned out to rest
on a check that could not fail (⑩).

---

## ① The starting state, re-measured rather than quoted

`./evals/mutation-harness.sh --only 'secretguard-*'` on `main` `00c2498`:

> `hooks/scripts/secret-guard.test.sh: 40 of 46 case(s) unpinned`
> `----- mutation-harness: 3 run · 3 killed · 0 survived · 0 error · 0 blocked`

Matching the handoff, which is what licensed reading its other figures (checklist §1).

## ② Result

| | before | after |
|---|---|---|
| cases pinned | **6 of 46** | **50 of 50** |
| registry rows for this suite | 3 | **31** |
| suite cases | 46 | 50 (+4 new, 1 fixture replaced) |
| `--only 'secretguard-*'` | 3 run · 3 killed | **31 run · 31 killed · 0 survived · 0 error · 0 blocked** |

Every mutation is drawn from a property **the script's own header calls load-bearing**
— the FAIL-CLOSED posture, the eleven secret formats, the removed in-band override, and
each clause of the "precision-first" paragraph — as `session-Q-prompt.md` ⑤ step 2
requires. Nothing was invented to make a number move.

## ③ The case that could not fail

`non-Bash payload skips the path scan` asserted that a WebFetch payload is never
path-scanned. Its fixture was:

```
{"tool_name":"WebFetch","tool_input":{"url":"https://ex.com/docs?q=cat%20.env"}}
```

The space is **percent-encoded**, and every path pattern requires `verb` + literal
whitespace. So the payload matched nothing **whether or not the scope existed** — the
case passed for a reason unrelated to its name. Measured, not inferred: mutating the
scope to `if true; then` (scan *everything*) reddened **zero** cases.

Fixed by giving it a payload the scan **would** catch (a `prompt` field containing
`cat .env`). The same mutation now reddens exactly that one case.

Sessions T and T2 each found cases of this class by mutating suites nothing had touched
before. This one is different in **how it surfaced**: the coverage report **named the
case**, and the probe then proved it could not fail. That is the report being used the
way ADR-0040 argued for — as a worklist, not a disclaimer.

## ④ Three documented rules with no case at all

Each is named in `secret-guard.sh`'s own comments as the reason a false positive does
not happen. None had a test. All three probes reddened **nothing** before the cases
existed, which is how they were found:

| rule (script's words) | case added | pinned by |
|---|---|---|
| alnum-starting names "need an explicit left boundary or they'd match inside `myid_rsa` / `mysecrets/`" | `myid_rsa does not read id_rsa — allowed`, `mysecrets/ is not secrets/ — allowed` | `secretguard-sshkey-left-boundary-removed`, `secretguard-secrets-left-boundary-removed` |
| "a write-redirect (`>`, heredocs) between verb and path never matches" | `write redirect TO .env allowed (path is the output)` | `secretguard-write-redirect-exclusion-removed` |
| RD is an "input redirect (not heredoc `<<`)" | `herestring feeds text, does not read .env — allowed` | `secretguard-redirect-heredoc-guard-removed` |

Each new case was verified **non-vacuous before being kept**: it goes red under its own
property's mutation and under nothing else. Four cases, four one-to-one pins.

## ⑤ The property whose halves are redundant

`broken grep fails closed` is the suite's only fail-closed fixture, and the script has
**two** independent guards that catch it — the up-front `grep` self-test, and the
`rc >= 2` inspection at every call site. Measured separately:

| mutation | cases reddened |
|---|---|
| self-test removed only | **0** |
| every `rc >= 2` inspection removed only | **0** |
| **both** (the posture as the header describes it) | **1** — `broken grep fails closed` |

So it is registered as one row, `secretguard-fail-closed-spine-removed`, because one
property is what the header claims it is. **This is defence-in-depth working, not a
defect** — but it does mean the suite cannot tell you *which* half is load-bearing, and
a session that deleted either one would see green.

The third guard, `command -v grep`, is **not separately pinnable by construction**: any
scenario where grep is absent also fails the self-test, which invokes grep. That is a
statement about the guards, not about the instrument.

## ⑥ What the coverage report does not credit

`secretguard-path-scan-never-runs` demonstrably reddens **15** cases (measured directly
against a mutated copy). The registry row named **7**. The report then listed the other
**8 as unpinned** — "nothing here would notice if the property each names stopped being
exercised" — while a registered, killed mutation in the same run had just reddened them.

The cause is in `evals/mutation-harness.sh`. Its comment says red lines are credited
whatever the verdict:

> *"Red lines are credited whatever the verdict: a case that went red under a mutation
> is pinned by it even if some other expectation of that mutation survived."*

`list_fail_cases` writes the name **as it appears on the FAIL line**, which in this
suite carries a diagnosis suffix (`... (exit=0 want=2 stderr-miss=1)`). Crediting is a
whole-line match (`grep -Fxq`) against the baseline name, so those entries never match.
Only cases **named in an expectation** are credited — via the second loop, which
resolves the name against the baseline first. For any suite whose FAIL line carries a
suffix, that first contribution is dead.

**Fixed, on the user's instruction, in this same change.** `credit_red_cases` resolves
each red case back to **the longest baseline name that prefixes it** before crediting:

- **Prefix**, not substring — the case name always starts the line, so everything after
  it is diagnosis, and a substring test would match a name appearing inside that
  diagnosis.
- **Longest**, because this repo grows case names by appending qualifiers. A plain
  prefix test also credits the shorter case the red one merely extends — the exact
  ambiguity PR #147's review refused when it introduced the whole-line match. Longest-wins
  keeps that guarantee and restores the credit the comment always claimed.

A hand-rolled case whose FAIL text differs from its PASS text prefixes nothing and is
still credited by its expectation's `<green>>><red>` form, unchanged.

**Proved by perturbation (R1), not by assertion.** A new case in
`evals/mutation-harness.test.sh` uses a fixture mutation that reddens **two** cases while
the registry names **one**, and asserts the unnamed one is not on the unpinned list —
plus a positive assertion that the report ran at all, because a bare absence assertion
passes over a run that reported nothing (the correction PR #147's review made). Measured
both ways on the shipped harness:

| | `--registry` naming 1 of the 15 reddened cases |
|---|---|
| before the fix | `49 of 50 case(s) unpinned` |
| after the fix | `35 of 50 case(s) unpinned` |

and the self-test itself: **78 passed / 0 failed** against the fixed harness,
**77 / 1** against a reverted copy — the new case is the one that goes red. Registered as
`mutationharness-red-cases-credited-raw`, KILLED.

The 8 secret-guard cases were still closed the honest way rather than left to the fix —
not by naming them on the coarse row, but with **six more mutations**, each pinning the
clause it actually tests (the quoted-path alternate, the `source` verb, the path
terminator's dot, the `*.env` left boundary, and the two copy patterns). A case pinned
only by *"the whole scan is gone"* would not notice its own rule being deleted.

## ⑦ Cost — the bucket is robust, the percentage is not

The machine would not stay quiet (see ⑧), so this is reported as **two pairs**, each
measured back-to-back, rather than as one figure pretending to be clean:

| pair | `--only 'secretguard-*'` | `./check.sh` | ratio | load |
|---|---|---|---|---|
| pre-fix, quiet-ish (11:17–11:19) | **128 s** | **139 s** | **92.1%** | low |
| post-fix, busy (14:00–14:07) | **262 s** | **172 s** | **152%** | 13.6 falling to 4.2 |

Both are inflated and the second pair is not even internally load-matched — the load fell
*during* `check.sh`. **What survives both is the only thing ADR-0036 actually consumes:**
`secretguard` is in the **second bucket** (20% – 2×) either way, and **nowhere near the
third** (>2×) under either measurement. The decision does not depend on which number is
right.

**The move is real regardless**: 12.4% → at least 92.1%. It was 14.3 s with 3 mutations,
and every one of the 31 re-runs all 50 cases. This suite is now second only to `prepush`,
and the next session adding rows here should measure before adding, not after
(`session-V-prompt.md` ③). The crediting fix is not what costs this — it is O(red × baseline)
in bash, a few hundred iterations per mutation.

## ⑧ Full runs — two of them, because the instrument changed mid-session

ADR-0036 names a registry change as the event that owes a full run; the harness change
owed a second one.

| | run A (registry only) | run B (after the crediting fix) |
|---|---|---|
| verdict | `102 run · 102 killed · 0 survived · 0 error · 0 blocked`, exit 0 | `103 run · 103 killed · 0 survived · 0 error · 0 blocked`, exit 0 |
| wall clock | **5332 s — discarded** | 1082 s, under load |

**Run A's wall clock is discarded and the discard is the record.** 5332 s is **9.5× the
~562 s** the isolated per-suite measurements predict. Checked immediately on completion:
load average **6.35**, `Spotlight` at **73.5%**, `syspolicyd` at **67.3%** — Gatekeeper
evaluation and indexing of the thousands of freshly written mutant copies the harness
execs. Checklist §3's exact failure mode; Session T hit it and set the precedent of
recording the discard rather than publishing the number. Run B's 1082 s is closer but
still ran at load 8–18, so it is reported as a bound, not a cost.

Nothing about either verdict is timing-sensitive, so both obligations are met — and
ADR-0036's own decision is that the full-registry number **is not the cost of any event a
gate change triggers**. The figure the rule consumes is ⑦'s.

## ⑨ What the whole registry now reaches — and how much of it was already there

| | session start (T2, `00c2498`) | after the rows | after the crediting fix |
|---|---|---|---|
| cases pinned | **95 of 677** | 139 of 681 | **178 of 683** |
| mutations | 74 | 102 | **103** |

Read the last column against ④. Between the middle and right columns the registry gained
**one** mutation and the suites gained **two** cases, yet the pinned count rose by **39**.
**About 38 of those were already pinned and simply not counted** — the report had been
under-stating its own coverage by roughly a fifth of the true figure, in every suite, for
as long as the report has existed.

It shows up per-suite with no new rows anywhere but `secret-guard`:

| suite | before the fix | after |
|---|---|---|
| `hosts/goppi-doctor.test.sh` | 73 of 75 unpinned | **63 of 75** |
| `evals/additive-only.test.sh` | 55 of 64 | **51 of 64** |
| `evals/pair-tally.test.sh` | 30 of 38 | **24 of 38** |
| `hooks/git/pre-push.test.sh` | 8 of 19 | **5 of 19** |
| `evals/pr-body-hygiene.test.sh` | 38 of 43 | **36 of 43** |
| `evals/secret-scan.test.sh` | 40 of 47 | **38 of 47** |

Eleven suites moved; twelve did not. **`hooks/scripts/secret-guard.test.sh` is absent from
the list entirely — 0 of 50 unpinned.** The four suites `session-Q-prompt.md` ⑤ handed
forward stay untouched by design, and their figures above are what `session-V-prompt.md`
tells the next session to re-measure rather than quote.

One thing checked rather than assumed: the credit cache is keyed per **test file**, and
`remedy-discipline` is the one file two labels share. Running its suite under each label's
switch var gives **47 PASS case names, identical both ways** — so the shared key is safe.

## ⑩ A claim of mine that rested on a check incapable of failing

The first full-run attempt was killed at a 10-minute tool cap. I checked the tree and
reported it clean. **It was not, and neither half of my check could have found anything:**

- `git status` **cannot** show these files — `.gitignore:19` is `.goppi-mutant.*`.
- my `find` searched for `.mutant-*`, which **cannot match** `.goppi-mutant.*`.

A real leftover was sitting in `evals/`, timestamped 11:29, owned by a **dead** PID,
inside the killed run's window. Found only later, by an unrelated `find` with the right
glob. Removed by hand; `evals/additive-only.sh` verified unmodified.

**This is the session's own subject matter, committed while writing the session up** —
a proof that could not fail, inside a report about cases that cannot fail. Sessions T and
T2 each shipped one of these and a reviewer caught it. This one the author caught, but by
accident and hours late, which is the same thing as not catching it.

**On the leftover itself: expected, not a defect.** The harness traps EXIT/INT/TERM/HUP
and its own suite proves the SIGTERM path clean (`nothing is left behind when the harness
is KILLED mid-run (SIGTERM)`, green). But bash defers a trap until the running foreground
child returns, so a SIGTERM delivered while a suite is executing cannot be serviced until
that suite finishes — and a tool timeout that escalates to SIGKILL never lets it. The
harness already says so at line 115: the mutants are dot-prefixed and gitignored
*precisely* "so a run that dies in a way no trap can catch (SIGKILL, …)" leaves something
inert. The design anticipated this. **My check did not.**

---

## Method note

**Every property that nothing had ever exercised turned out to be either unmeasurable,
unpinned, or wrong.** Three sessions running. This time the split was: 40 pinnable, 1
vacuous, 3 documented-but-untested, 1 redundant-by-design, and 1 defect in the
instrument doing the reporting.

The cheap part was the mutations. The part that needed a probe — applying a candidate to
a copy and reading which case names went red, before writing any registry row — is what
caught the vacuous case and the three missing ones. **Registering a mutation without
first watching which cases it reddens is how a row gets written against a case that
cannot fail.**
