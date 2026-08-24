# u1 — how many "it cannot be done" claims are actually claims (2026-08-01, Session U ①②③)

<!-- genre: measurement -->

**What was measured**: whether a machine check on absence/impossibility claims is worth
building — by counting the population and classifying every hit by hand, **before**
anything is wired. That order is this repository's own precedent (ADR-0032 / G5, whose
false-positive baseline *"ran before anything was wired, and decided the design"*), and
`session-U-prompt.md` fixed it in advance: *"게이트부터 만들면 안 된다 … '만들지 않는다'가
1급 결과"* — **"we don't build it" is a first-class outcome.**

**Why now**: `spec.md`'s **O4** — *no number from prose, no absence claim from a
capped or filtered search* — is a standing rule that **nothing checks**. Session O broke
it three times in one day. Session T2 broke a **second, adjacent class** three more
times: not *"the tree contains no X"* but *"this cannot be done"*, all three written
into durable artifacts, all three refuted by measurement within hours, none caught by
their author.

## The population, re-counted (U ①)

Patterns broadened first, since the prior list was a session's off-the-cuff product.
**Anchored, because this population moves with every commit** — class B alone went
74 → 105 across six commits on 2026-08-01, and this file adds hits of its own:

```
REF=54dc397                       # the tree this measurement describes
git archive $REF | tar -x -C <dir> && cd <dir>
grep -rIn -E "<class pattern>" --include='*.md' --include='*.sh' .
```

| class | patterns | hits | files |
|---|---|---|---|
| **A — absence of fact** | `nowhere in` · `no artifact` · `nothing in the repo` · `nothing in this tree` · `nothing enumerates` · `there is no` · `no such` · `never enumerated` · `absent from the tree` | **58** | 33 |
| **B — impossibility of capability** | `cannot be` · `not solvable` · `impossible` · `no way to` · `does not fit` · `구조적으로` · `못 한다` · `unmeasurable` · `cannot carry/run/be measured` | **105** | 51 |
| | **union (distinct lines)** | **160** | **67** |

**163 classified rows over 160 distinct lines**: 3 lines match both class patterns and
were read once per class. Two further reproduction facts, both found in review of this
file and both worth more than the numbers they correct:

- **A working tree gives different figures than the archived tree.** `spec.md` (5 hits)
  and `progress.md` (3) are gitignored, present locally, absent from `git archive`. A
  measurement of "the repo" must say which.
- **The first version of this file reported the sum (163) as the population and gave no
  command and no commit.** Both are the defect it is about, committed inside it.

The figure in the session prompt was **23 hits / 13 files** — a third of the real
population, and **class B was not in it at all**: the class that produced the three most
recent breaches is invisible to patterns written before they happened.

## The classification (U ②)

Every hit read. Three buckets, and the axis that decides between the first two is the
one the T2 failures made obvious: **is a command, file, or measurement cited beside the
claim?**

| bucket | meaning | rows | share |
|---|---|---|---|
| **ⓐ** | it is a claim, and evidence sits beside it | **48** | 29% |
| **ⓑ** | it is a claim, and nothing sits beside it | **7 rows / 6 distinct** | **4%** |
| **ⓒ** | not a claim at all | **108** | 66% |

Per class: **A** — 24 ⓐ · 4 ⓑ · 30 ⓒ (48% are claims). **B** — 24 ⓐ · 3 ⓑ · 78 ⓒ
(26% are claims).

**The ⓑ set, named — six claims, one of them counted twice** (`t1:67` matches both class
patterns, which is where the "7" came from; there is no seventh):

| # | location | the claim | what refuted it |
|---|---|---|---|
| 1 | `…/2026-08-01-t1-harness-coverage.md:67` | `remedy-discipline` *"would not fit anyway"* — crosses many scripts | ADR-0039: the registry keys suites by **label**, so one file takes one row per script |
| 2 | `…/t1-harness-coverage.md:169` | `goppi-doctor`/`worth/run` *"unmeasurable by this instrument as built"* | ADR-0038: the mutant runs **beside its original**; both registered |
| 3 | `…/2026-08-01-t2-harness-coverage-closed.md:50` | *"there is no script under test"* | same as 1 |
| 4 | `…/t2-harness-coverage-closed.md:269` | *"structurally unmeasurable"* | same as 1 |
| 5 | `docs/decisions/0038-…:56` | *"no script under test"* | same as 1 |
| 6 | `docs/decisions/0037-…:96` | *"there is no equivalent exact instrument for TOML"* | ADR-0039: the equivalent is a **parser**, and this repo already applies one to JSON |

Naming them is what makes the re-open conditions evaluable: a future session can recount
against this list instead of re-classifying from scratch.

**What ⓒ is made of**, because 66% is the number that decides this: ordinary technical
prose. `cannot be fetched` in a URL-validation comment · `cannot be edited` about git
history · `cannot be auto-approved` about a sandbox rule · `there is no engine` as a
statement of what `scaffold` deliberately is · runtime `why:`/`remedy:` lines emitted at
failure time · SKIP messages for a macOS-shaped guard · test assertions comparing
strings. None of these is an assertion about this repository that a search or a run
could settle. A checker cannot tell them apart from the 7 without reading them.

## The verdict (U ③): **do not build a tree-wide gate on these patterns**

**A tree-wide gate on these patterns fires 160 times to find 6 — a 96% false-positive
rate.** §11's zero-false-block goal and the ADR-0032/G5 precedent both make that
disqualifying, and this is the outcome the session was told to be willing to reach.

**The verdict is scoped to that design, and the scope is the point.** An earlier draft of
this section concluded that *"the machine cannot be built at acceptable precision on this
tree"* — an impossibility claim about a design space, resting on a measurement of one
point in it, **in the file whose subject is impossibility claims that outrun their
evidence.** Caught in review. What is measured is one design; what is unmeasured is
named below.

Three further facts, each of which independently weakens the case for a machine:

1. **The debt is tiny and concentrated.** All 6 sit in **4 files**, in
   `evals/harness-eval/results/*.md` and the ADRs restating them.
2. **All 6 were refuted within hours, by measurement.** Commit timestamps: `t1` landed
   11:17 (`64d8b7b`), the dialect/relocation exclusions closed 15:21 (`718f264`,
   ADR-0038), the TOML one landed 15:21 and closed 17:54 (`4546f59`, ADR-0039). Stated
   with the caveat review added: those 6 claim-instances are **~3 distinct incidents**
   closed in 2 commits on 1 day, so the evidence is thinner than "6 of 6" sounds.
3. **What caught them was a person asking.** Three of three in one session, and the
   author caught none. That control already exists, costs nothing, and no grep in this
   population would have fired on the right 6 without also firing on 154 others.

### The narrow design, measured rather than dismissed

The obvious alternative anchor is *"an exclusion row in a census table under
`evals/harness-eval/results/`"*, which is where the debt lives. Measured at the same
commit: **22 hits in that directory, 10 of them table rows** — `t1:63-70`, `t2:144`,
`l1:116`. Of the 6 ⓑ claims, **2 are in those 10 rows**; the other 4 are prose in result
files and ADRs, which the anchor does not reach.

So the narrow gate costs **8 false fires to catch 2**, and misses 4 of 6. That is 80% FP
on the anchor and 33% recall — better than 96% and still not good, and it is now a
number rather than an intuition. **It is not built either**, on those figures.

**What is worth doing instead, and is already done**: the discriminator is not the
sentence, it is what sits beside it. `.scratch/session-start-checklist.md` item 4b states
it as a writing rule — *before writing "cannot", run the thing that would show it and
cite the command; if you cannot run it, write "not tried", which is a different claim.*

⚠️ **That rule does not cover 2 of the 3 incidents it was written for, and review found
it.** `goppi-doctor` and `worth/run` were excluded **with** a populated evidence column
and a real measurement (`49/26` red under relocation) — the measurement was correct and
the **conclusion drawn from it** was wrong: a property of *the instrument as built* was
written as a property of *the suites*. Citing a command is necessary and not sufficient.
The rule's exemplar has been corrected to say so.

## Re-open conditions

- **The ⓑ set grows past ~20, or its recall under the narrow anchor rises above ~70%** →
  the narrow gate's 80%-FP / 33%-recall arithmetic changes and it becomes worth its cost.
  Measured today at `54dc397`: **6 claims, 4 files, 2 of them inside the anchor.** Recount
  against the named list above, not by re-classifying from scratch.
- **A ⓑ claim survives more than one session unrefuted** → the human control that caught
  all 6 has stopped working, which is the premise this verdict rests on.
- **The pattern list is broadened again and the ⓒ share drops below ~40%** → precision
  was a function of the patterns, not of the tree, and the question re-opens.

## What this run does NOT show

- **Nothing about whether the 6 were harmful.** All were refuted within hours; the cost
  was a detour, not a shipped defect. This file counts claims, not damage.
- **The axis scores citation PRESENCE, not citation correctness** — and that runs in the
  direction of understating the debt. A claim that cites a file and is **wrong** scores
  ⓐ. Review found live examples: `docs/decisions/0034-…:11` still says `goppi-doctor` and
  `worth/run` *"cannot be run relocated"*, and `:90` still says *"Nineteen of the 23
  suites … cannot be measured this way at all"*. Both were overturned; the census closed
  at 24 of 24. They are cited, so this measurement counts them as sound. **A dated
  superseding note has been added to ADR-0034**, but the limitation stands: any check
  built on this axis would inherit it.
- **Nothing about classes the patterns do not name.** A claim phrased *"we deliberately
  did not"* is invisible here, and that phrasing is the obvious way to evade a check —
  which is a further argument against building one.
- **Nothing about other repositories.** 96% is this tree's number, on these patterns,
  today.
