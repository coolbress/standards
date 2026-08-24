# measurement — where the secret-scan gate should sit, 2026-07-28 (issue #89, Session L)
<!-- genre: measurement -->

ADR-0032 decided goppi's secret-scan gate on three axes and **never compared where in
the lifecycle it sits** — recorded as option ⓛ, explicitly not rejected, because it was
never weighed. This is the weighing. It ran **before** any hook was written and it
changed what the issue was about.
Genre: **deterministic tool measurement, not a pair.** No model runs, no spend.
Environment: `gitleaks 8.30.1`, macOS, bash 3.2, `git` 2.x. Every table below is a
recorded run, not an estimate.

## The finding that reframed the issue

#89 was titled *"detects but does not prevent"*. That is too kind to what shipped.

| fixture | local `check.sh` | CI (fresh clone of the pushed head) | present in pushed history? |
|---|---|---|---|
| secret added in commit A, removed in commit B, branch pushed | `clean` | `clean` | **yes — 1 finding** |

Run end to end: a real bare remote, a real `git push`, a real `git clone` of the result.
Both gates green; the credential in the published history the whole time. So the
accurate sentence is not "detects late" but **"does not detect, in a case reachable by
the most ordinary reaction to noticing your own mistake"** — commit, spot it, remove it,
push.

A real-world instance turned up during the false-positive sweep below, in an unrelated
repository (anonymised at the owner's request, and reported to them): credential
committed, containing file deleted in a later commit, tree scan clean at `HEAD`,
credential still retrievable from history. The synthetic fixture was not hypothetical.

## Coverage matrix — 5 fixtures × 4 scopes, every cell executed

| fixture | worktree (shipped) | `git archive HEAD` | `git --staged` | pushed range |
|---|---|---|---|---|
| committed secret, still in the tree | FOUND | FOUND | clean | FOUND |
| untracked new file | **FOUND** | clean | clean | clean |
| staged, worktree copy cleaned (index gap) | clean | clean | **FOUND** | clean |
| added + removed inside the branch | clean | clean | clean | **FOUND** |
| gitignored file | clean | clean | clean | clean |

- **No scope dominates.** The shipped worktree scope is the only one that catches
  untracked-but-committable files; only the range scope catches the branch-local case.
- **`git archive HEAD` is dominated** — it wins no cell the shipped scope does not
  already win, and loses three. Rejected as a candidate on that basis (ADR-0032 ⓜ).
- **The index gap is subsumed at push.** Staging a secret, cleaning the worktree copy
  and then committing produces a commit whose content carries the secret; the tree gate
  reads clean and the range scan catches it. So a pre-commit hook's unique coverage
  disappears once the question is "what is about to be published".

## Lifecycle: why push rather than commit

| property | `pre-commit` | `pre-push` |
|---|---|---|
| defeated by `--no-verify` | yes (measured, rc=0) | yes (measured, rc=0) |
| sees a commit made with `--no-verify` | **no** | **yes** |
| sees a commit built by `commit-tree` | **no** | **yes** |
| catches add-then-remove across two commits | at commit time | at push time |
| harm prevented | a local commit object — **no rotation needed** | publication — **rotation needed after** |
| cost | 0.08s | **0.13s** |

Revocability is identical, so it is not a discriminator. The two that decide it:
**publication is the harm line**, and **push is a chokepoint where commit is one of
many entry paths**.

## False-positive profile — the evidence the `scaffold` question needed

Session K deferred the `templates/` planting decision for want of exactly this number.

| | |
|---|---|
| repositories scanned | **14** |
| commits actually inside scanned ranges | **613** |
| total findings | **1** |
| false positives | **0** |
| true positives | 1 (a genuine credential, reported to its owner) |
| not counted, stated not hidden | 1 repository with a single commit — no range to resolve |

### The first version of this sweep was wrong, and how

It reported **0 findings across 14 repositories** — and was checking neither gitleaks'
exit status nor whether the range it asked for resolved. A 40-commit repository was
asked for `HEAD~40..HEAD`, which cannot resolve; the scan never ran, the report was
empty, and the empty report read as "clean" **over the one repository that actually
contained a live credential**.

That is the same fail-open the independent review of #86 found in the gate itself
(*"a missing report became `[]`, so a binary exiting 126 read as found-nothing"*),
reproduced by the person who had just read that review. It was caught by adding a
**positive control** — a planted canary that the harness must report — and by checking
`rc`. Both are now permanent: `secret-scan.sh --range` resolves its range through
`git rev-list --count` **before** scanning, and an unresolvable range is exit 2 with a
test that drives it.

## `scaffold` planting — measured, and rejected on grounds the FP profile did not supply

| question | measured result |
|---|---|
| repo already sets `core.hooksPath`, hook planted in `.git/hooks` | **only the `core.hooksPath` hook ran** — the planted one is silently inert |
| goppi sets `core.hooksPath` on a repo with existing hooks | **the user's existing `pre-commit` stopped running** — orphaned, not overwritten, no warning |
| scanner absent | gate exits 3 on every push; the hook treats that as a block |

The false-positive objection is retired (0/613). The decision is still **no**, on the
two rows above: one makes goppi ship a control that cannot fire while claiming
coverage, the other is clobbering by side effect, which is precisely what ADR-0030
forbids. Recorded because the reason a thing was deferred and the reason it is finally
declined need not be the same reason.

## Mechanism: the simplification that was tested and rejected

| | copy loop (shipped) | `gitleaks dir <276 paths>` |
|---|---|---|
| wall time | 3.3s | **0.45s** |
| argv size | — | 13,913 B against `ARG_MAX` 1,048,576 |
| unreadable file | **exit 2, `why:`/`remedy:`** | `WRN` on stderr, **exit 0, absent from findings** |
| symlink | scans the target path git stores | **not scanned** |
| case collision | detected, exit 2 | structurally impossible |

7× faster, and it trades a proven fail-closed property for that speed on a credential
surface. Rejected (ADR-0032 ⓝ), with the numbers recorded so it can be re-opened if
gitleaks ever makes unreadable inputs an error. The simplification arrived elsewhere:
`--range` reads git objects and has **no copy loop at all**.

## Mutation testing — five mutations, and two cases were passing for the wrong reason

| mutation | target case broke? |
|---|---|
| hook always exits 0 | yes (7 red) |
| hook blocks every push | yes (5 red) |
| absent scanner treated as a pass | yes |
| `</dev/null` removed (gate inherits hook stdin) | **no — initially** |
| missing-gate guard removed | **no — initially** |

- The missing-gate case passed because a missing command exits **127** into the
  catch-all branch, so the exit code was reachable two ways. It now asserts the guard's
  own message.
- The stdin case passed because the real gate happens not to read stdin — so
  `</dev/null` was a guard whose failure mode had never been demonstrated, the same
  shape as the FIFO guard deleted in #88. Tested properly against a gate that *does*
  read stdin: **the second pushed ref is swallowed and never scanned while the push
  succeeds.** The guard is load-bearing and now has a case that fails without it.

Both closed; all five mutations now break their target case.

## The independent review — 7 findings, 7 accepted, 0 rejected

Run against a suite that was green, had already survived five mutations, and had
already had two of its own cases corrected for passing on the wrong grounds.

| # | severity | defect | status |
|---|---|---|---|
| F1 | **HIGH** | `--log-opts` drives `git log -p`, which emits **no diff for a merge commit** — a credential written by a conflict *resolution* was invisible while the gate printed "no credentials" over a range containing it | fixed + 3 cases |
| F2 | MED | `--not --remotes` spans every remote, so pushing to a **second remote** reported "nothing is being published" while a whole branch went out | fixed + 1 case |
| F3 | MED | the new tests turned `./check.sh` **red** on a machine without gitleaks, converting this repo's BLOCKED-not-FAIL convention into a hard failure | fixed, verified without gitleaks |
| F4 | MED | a `remote_sha` this clone never fetched made the range unresolvable and **blocked a clean push** | fixed + 1 case |
| F5 | MED | the documented install is **silently inert** under `core.hooksPath` — the exact ground ⓛ-4 uses to refuse planting elsewhere | fixed (docs + suite) |
| F6 | LOW | the suite read the developer's global git config: under a global `core.hooksPath` it reported **6 passed / 7 failed against a hook that never ran** | fixed + positive control |
| F7 | LOW | the ⓛ-2 claim that the range "never touches the immutable fixture" is false with zero remote-tracking refs | qualified in the ADR |

### F1's fix was itself chosen by measurement, not by the first idea

| approach | merge-resolution secret | ordinary merge of an already-published branch |
|---|---|---|
| shipped (plain `--log-opts`) | **missed** | clean |
| `-m` | detected | **false block** (1 finding becomes 2) |
| `--cc` / `--diff-merges=cc` | **missed** (gitleaks does not parse combined diffs) | clean |
| `--diff-merges=first-parent` | **missed** | clean |
| **`git diff-tree --cc --name-only` → scan those blobs** | **detected** | ~~**clean**~~ → **FALSE BLOCK** (see below) |

~~The last row is the only one correct in both directions.~~ **Corrected 2026-07-29
(#97): it was not.** The right-hand column was measured with a **clean** merge, where
`--cc` names no path at all — so the cell that was supposed to prove the absence of a
false block never exercised `--cc` on a resolution. A merge resolved as the **union**
of both sides is also an "ordinary merge of an already-published branch", and there the
blob differs from every parent while every *line* came from one: scanning those blobs
whole re-reported a credential the parents already carried, giving **1 finding → 2** in
the audit and a **blocked push that published nothing new**. That is the same defect
this table credits itself with avoiding by rejecting `-m`.

The fix is to keep `--cc` as the candidate set and subtract the parents' lines, so only
content existing in no parent is scanned. Re-measured after that change: union case
`rc=1` → **`rc=0`**, true positive still `rc=1`, audit reports the credential **once**.

**The transferable part is not the flag.** The row was wrong because the column that
was supposed to falsify it used a fixture that could not — the same shape as the two
mutation-blind cases recorded further down this file. A cell proving an *absence* needs
a fixture where the thing being ruled out would actually appear.

## The cross-vendor rung — 4 findings, 3 accepted, 1 not reproduced

Run payload-only (no repo, no tools, no network: `--cd <empty dir> --sandbox read-only
--skip-git-repo-check`), and told which defects the base rung had already fixed so it
could not re-report them. It found a **disjoint class**, as it did in #86: three of its
four are fail-open paths the base rung did not reach.

| # | severity | defect | verdict |
|---|---|---|---|
| ⓧ1 | HIGH | `git push <URL>` supplies a URL, not a remote name — the scope lookup failed and **all** remote-tracking refs were excluded, publishing a credential under `0 commit(s) … nothing is being published ✓` | **confirmed**, fixed + 2 cases |
| ⓧ3 | HIGH | `\|\| : > file` turned a failing `git rev-list --merges` into an empty merge list, silently skipping the merge scan; `diff-tree \| tail` hides a failing `diff-tree` | **confirmed**, fixed + 1 case |
| ⓧ4 | MED | `remote_sha` covers only the pushed branch, so merging an already-published branch **false-blocked**; and the test for it hand-wrote a range instead of using the hook's | **confirmed**, fixed + 1 case |
| ⓧ2 | HIGH (claimed) | `diff-tree --cc --name-only` reports a top-level tree for nested paths, so `git show <merge>:<dir>` yields a tree listing | **not reproduced** |

**ⓧ2's refutation, with its own evidence.** Built correctly, `--cc` on a real merge
returns `config/prod/app.conf`, and the gate exits 1 on the nested credential. The
reviewer's observation holds for a **non-merge** commit — `diff-tree` is non-recursive by
default — and the gate only ever passes it commits from `rev-list --merges`. The first
attempt to check this had a broken fixture whose merge never happened, and it printed
`config`, which is exactly what the reviewer predicted; believing that run would have
"confirmed" the finding for the wrong reason. `-r` was added regardless, so nothing
depends on `--cc` implying recursion.

### What the review says about the process, not the code

Every finding was in code that had passed a green suite, mutation testing, and a
`check.sh` ALL GREEN. Two of them (F3, F6) were defects **in the tests
themselves** — one made the gate red for the wrong reason, the other made the
suite green over a hook that never executed. Adding the reviewer's own lesson to
this session's tally: **the measuring instruments failed three times** (the FP
harness, the two mutation-blind cases, and the suite's global-config dependence),
against **one** failure in the subject under test.

A further one surfaced while re-verifying the fixes: running the suite from a
directory outside any git repository revealed two `--range` cases that had no
repository of their own — one passing for the wrong reason ("not a git
repository" also exits 2) and one failing for an unrelated one. Both now run
inside a repository the suite owns.

## What carries forward

- **A refutation is a claim.** One prediction in this session — that stale
  remote-tracking refs narrow `--not --remotes` — failed to reproduce on the first
  construction (a delete-push prunes the local ref) and **did** reproduce with a second
  clone performing the deletion. Both the claim and its first refutation needed
  evidence.
- **A green suite written by the author of the code is the weakest evidence here.** It
  was green before mutation testing found two cases asserting nothing.
- **Measure the harness, not just the subject.** The most consequential error in this
  session was in the measuring instrument, and it hid a real credential.
