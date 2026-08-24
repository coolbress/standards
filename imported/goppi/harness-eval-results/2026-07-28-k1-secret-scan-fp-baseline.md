# measurement — secret-scanner false positives on goppi, 2026-07-28 (issue #85, G5)
<!-- genre: measurement -->

Threat-model **G5** was deferred twice (Session H, Session I) with the same stated
reason both times: a new blocking gate's false-positive behavior must be measured
before it blocks merges, because §11's zero-false-block goal binds goppi's own gates
too. This is that measurement. It ran **before** anything was wired, and it decided
the design (**ADR-0032**) rather than confirming one.
Genre: **deterministic tool measurement, not a pair.** No model runs, no spend.

## Why the measurement was expected to be the hard part

goppi's repository is deliberately full of credential-shaped material: `secret-guard`
has a fixture per pattern it matches, `evals/worth/cases/secret-guard/must-flag/`
carries nine more, and `evals/worth/README.md` states outright that every fixture key
is synthetic. The working assumption entering the session — recorded in the session
brief as **confirmed, with 24 files named** — was that any scanner would light up on
day one, making the *allowlist* the real design surface and its width the real risk.

The assumption was tested rather than inherited. **It did not hold.**

## Method

`gitleaks 8.30.1` (homebrew, darwin_arm64), **default rules, no config file, no
`.gitleaksignore`** — deliberately the out-of-the-box behavior, since that is what a
first-day adopter gets. Repository at `269fffa` (main, v0.16.2 + the ADR-0031
correction). Commands as run:

```
gitleaks dir . --no-banner --report-format json --report-path <tmp> --exit-code 0
gitleaks git . --no-banner --report-format json --report-path <tmp> --exit-code 0
```

## Raw results

| scan | clone | bytes | findings |
|---|---|---|---|
| working tree | either | 1.46 MB | **1** |
| full history | **fresh clone from origin** at `269fffa` — 55 commits | 1.36 MB | **1** (`2efd16f`) |
| full history | the author's local clone — 137 commits reported | 3.41 MB | 4 |

**Corrected twice, and the second correction is the one that matters.**

*First correction (2026-07-28, from #86's independent review):* the original file
recorded only the bottom row — 137 commits, 4 findings — as if it were a property of
the repository. It is not; a fresh clone reports **one**. Re-verified by cloning
`https://github.com/coolbress/goppi.git`, checking out `269fffa`, and re-running the
recorded command.

*Second correction (2026-07-28, #88): the **mechanism** given for that gap was wrong,
and wrong in a way that would mislead the next auditor.* The file said the extra
commits were "dangling objects left by squashed and deleted branches, and `gitleaks
git` walks them". **`gitleaks git` does not walk dangling objects — it follows refs.**
What actually happened: at scan time this clone still carried **~30 stale
remote-tracking refs** (`origin/feat/8-layer-2` → `f120ab6`, `origin/unit/*`, and the
rest — branches long since merged and deleted on origin), and those refs made the
commits reachable. A `git fetch --prune` run later in the same session removed them,
which is what turned the same objects into the unreachable ones a subsequent check
found. Verified: all three still exist as objects, `git branch -a --contains` now
returns nothing for each, and only `origin/main` plus the release branch remain.

The practical form of the lesson is better than the original wording, too:
**`git fetch --prune` changes the result of this audit.** A count from a long-lived
working clone is not comparable to one from a fresh checkout, and neither is wrong —
they are answering "what does *this clone* contain".

**The correction is worth more than the number.** A history scan's result is a
property of the **clone**, not of the repository — so a history *gate* would give
different verdicts to the maintainer, a CI runner and a fresh contributor, on
identical code. That is an independent reason for ADR-0032's ⓖ rejection, stronger
than the "four immutable hits" argument the first version rested on.

The one reachable finding is the same line the tree scan finds, so the entire
false-positive surface of this repository is **one line**:

```
hooks/scripts/secret-guard.test.sh:31   rule gcp-api-key   entropy 5.18
```

Every other fixture — the AWS example key, the all-`A` GitHub token, all nine
`must-flag` cases — produced nothing.

## Why the other fixtures do not fire (probed, not assumed)

A non-finding is only evidence if you know *why* it did not fire; "it happened to pass"
is not a property you can depend on. Four probes, each value assembled at runtime:

| probe | result |
|---|---|
| the AWS-documentation example access key (the exact fixture string) | **not flagged** |
| the same key with **one character changed** | **CAUGHT** (`aws-access-token`) |
| `ghp_` + 36 repeated `A` (the repo's synthetic-token convention) | **not flagged** |
| `ghp_` + 36 characters of real entropy, identical shape | **CAUGHT** (`github-pat`) |

So two different mechanisms are at work, and neither is luck: the AWS example key is
**stopword-allowlisted inside gitleaks itself** (mutating one character defeats the
stopword and the rule fires), and the synthetic token fails an **entropy filter**. The
repo's existing fixture convention — obviously-repetitive values — was already doing
the job an allowlist would have been built to do.

## Detection power, measured in the same session

A gate with no false positives is trivial to build by detecting nothing, so the
opposite direction was measured too. Six real-shaped credentials, generated at runtime
from a seeded PRNG (no literal in any file):

**5 of 6 caught** — `aws-access-token`, `github-pat`, `slack-bot-token`, `private-key`,
`generic-api-key`. The miss was a bare 40-character base64-ish AWS *secret* key with no
adjacent keyword, which is the known weak case for context-free secret detection and is
recorded here rather than papered over.

## The finding that changed the design

`gitleaks dir .` scans the **filesystem, not the repository**. Verified by planting a
canary under `GOPPI_state/` — gitignored, PreCompact session state, never committable —
and watching all five of its credentials get flagged. That would have been a
**local-only false block**: the maintainer's `check.sh` failing on session scratch that
CI, with a clean checkout, never sees. `.github/workflows/ci.yml` exists precisely so
CI and local cannot drift; a gate whose verdict depends on untracked scratch is that
drift. The landed gate therefore scans
`git ls-files --cached --others --exclude-standard` — what git would let you commit.

## What was done with the one finding

It was **corrected at the source, not exempted**. The fixture value became
`AIzaSyNOT_A_REAL_KEY_NOT_A_REAL_KEY_NOT`: still matching `secret-guard`'s
`AIza[0-9A-Za-z_-]{35}`, which is the entire thing that test case proves, but too
repetitive for a repository scanner to mistake for a live credential. `secret-guard` is
a regex matcher, so entropy is irrelevant to its fixtures and the fidelity cost is
**zero** — verified: the corrected value is still blocked with the same
`google-api-key` label, and secret-guard's 46 tests still pass.

**Allowlist entries in the landed configuration: 0.** No `.gitleaksignore`, no
`[allowlist]` block, no path exclusion. Grounds, and the five alternatives rejected to
get there, are in **ADR-0032**.

## The history residue, stated rather than hidden

Existing commits cannot be edited, so the pre-correction occurrence remains in goppi's
history forever. This is why the full-history scan is **an audit
(`evals/secret-scan.sh --history`), deliberately not a gate**: wiring it would force
exactly the permanent allowlist this design refuses.

**What a re-run should expect, by clone:** a **fresh clone from origin** reports
**exactly 1** finding — `gcp-api-key`, `hooks/scripts/secret-guard.test.sh:31`, commit
`2efd16f` — so on a fresh clone a **second** finding is new and must be treated as
real. A long-lived working clone reports **more**, and the excess is not a signal about
the repository: it is **every commit reachable from a ref a fresh clone does not have.**
Two sources, and the prescribed diagnostic must cover both — `git fetch --prune`
addresses only the first:

1. **Stale remote-tracking refs** for branches merged and deleted on origin. This was
   the dominant term at scan time (~30 refs), and pruning removes them.
2. **Local topic branches** for squash-merged PRs. `prune` never touches these. Measured
   on this repository after pruning: `git remote prune origin --dry-run` is **empty**,
   yet `git rev-list --count --all` = 65 against `--remotes` = 58 — **7 commits** still
   reachable only from seven local branches whose PRs were squashed long ago.

So the diagnostic is `git rev-list --count --all --not --remotes` (what only your local
refs hold) **plus** `git remote prune origin --dry-run` (what only your stale remote
refs hold). Or simply **re-run the audit on a fresh clone**, which is how every
correction to this file was made and is the only form that needs no interpretation.

## Ceiling

Detection is gitleaks' rule set, pinned by version in `.github/workflows/ci.yml`. Rules
do not improve on their own and the pin does not auto-update (dependabot covers the
`github-actions` ecosystem, and this is deliberately not an action). Version currency
is a maintenance item, named here so it is not discovered as a surprise.
