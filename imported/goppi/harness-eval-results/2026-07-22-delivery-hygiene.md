# result — delivery-hygiene pair, 2026-07-22 (n=1)
<!-- genre: pair -->

The first executed harness-vs-vanilla controlled comparison pair (S4 slice 1).

| | |
|---|---|
| Task | `tasks/delivery-hygiene/` (observed origin: PRs #18/#20/#22 defects) |
| Arms | per `harness/arm-setup.md` — isolated `claude -p --setting-sources project`, same prompt verbatim, `--dangerously-skip-permissions` both |
| Model | `claude-fable-5`, pinned, both arms |
| Host | Claude Code 2.1.217 |
| Isolation | probe run 2026-07-22 before the pair: no user CLAUDE.md/GOPPI.md, no goppi skills/hooks in a `--setting-sources project` session |
| Harness arm material | `CLAUDE.md` = GOPPI.md contract + `.claude/skills/ship/SKILL.md` (Layer 0 + one skill; no Layer 2 — the slice-1 limit) |
| n | **1 pair.** pass@1 = pass^1 here; nothing about reliability across runs is measurable at n=1 and none is claimed |

## Verdict: NO measured difference on the scored criteria — both arms clean

| Criterion (verifier.sh) | vanilla | harness |
|---|---|---|
| fold-to-one commit | ✓ (squash-merge) | ✓ (fold + `--ff-only`) |
| Conventional-Commits subject | ✓ | ✓ |
| no local-only info (Claude-Session, paths) | ✓ | ✓ |
| trailer discipline | ✓ (no trailer at all) | ✓ (Co-Authored-By, final block only) |
| **verifier exit** | **1 (clean)** | **1 (clean)** |

## Real output — vanilla arm

Capture (`git log --format=… base-marker..main`):

```
COMMIT 87b13118f1ebde819587afe090ac40c5ab35570f
SUBJECT feat: handle empty input in parser (#7)
BODY-START
parse.sh now prints 0 for an empty input file instead of relying on
wc -l output; test.sh covers the empty-file case and README notes the
behavior.

BODY-END
```

Verifier: `clean: 1 folded commit, CC subject, no local-only info, trailer discipline held` → exit 1.

## Real output — harness arm

```
COMMIT a7eca71db57f3b428a3d9cf049e2298559881ecf
SUBJECT feat: handle empty input in parser
BODY-START
An empty file made wc-based line counting the only path, with no
explicit contract for zero-length input. parse.sh now short-circuits
to 0 for empty files, test.sh covers the case, and the README states
the behavior.

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>

BODY-END
```

Verifier: `clean: 1 folded commit, CC subject, no local-only info, trailer discipline held` → exit 1.

Skill-load evidence: the harness arm's transcript (committed verbatim at
`2026-07-22-delivery-hygiene-transcripts/harness.txt`, alongside
`vanilla.txt`) states it acted "per the local-only ship flow (no remote → no
PR/issue ceremony)" — ship's own language; the skill text demonstrably
reached the arm.

Post-review note (same day): PR #42's independent review hardened the
verifier (session links in prose form, scratch/temp/Windows paths, non-CoAB
trailers, BREAKING-CHANGE footer exemption, empty capture = verdict). Both
captures were re-scored under the stricter verifier: still exit 1 · 1 — the
zero-delta verdict stands.

## Qualitative deltas (observed, NOT scored — candidate future criteria)

- **Vanilla fabricated a reference**: its subject ends `(#7)` — inferred from
  the branch name — in a repo with no remote, no issues, no PRs. The reference
  points at nothing. The harness arm, whose skill says local-only flows carry
  no PR ceremony (and `(#N)` is appended by GitHub at squash time, never by
  hand), did not. This is a real hygiene difference the current verifier does
  not measure; growing the fixture set to flag dangling `(#N)` references is
  the recorded candidate.
- Vanilla recorded **no authorship trailer at all**; the harness arm carried
  `Co-Authored-By` as its only trailer block, per the commit rules.
- Both arms verified before and after the merge (`./test.sh` PASS read, both
  transcripts) — the Iron-Law behavior was not a differentiator here.

## Honest reading (what n=1 can and cannot say)

- On this task, this model, this host version, this day: **the truly-vanilla
  host already delivers clean history; the scored worth of the harness's
  advisory layer measured zero.** That is the result, said plainly — the
  first controlled data point, consistent with the prior observational signal
  that a strong host does most of it (scaffold A/B ~70%, kickoff A/B
  contract-only win — design §12).
- It is NOT evidence the ship skill is worthless: (a) n=1 measures pass@1, and
  the harness claim is reliability (pass^k) — undecidable here; (b) the task
  may under-discriminate (small clean fixture, cooperative prompt); (c) the
  unscored deltas above are exactly the margins ship's rules target. It IS an
  entry for ship's standing expiry watch (host-native delivery discipline
  catching up — ship SKILL.md Expiry) and a datum for §11 G4.
- §10 non-causality: this pair controls task/model/day. It does not control
  authorship — task, verifier, and harness share an author lineage
  (self-evaluation bias, disclosed) — and generalizes to nothing beyond its
  scope (§11 n=1 limit).

## Re-score note (2026-07-25, Session B — criteria promotion)

The two qualitative deltas above were promoted into scored verifier criteria
(check 5: dangling forge references; check 6: task-scoped agent-authorship
trailer — verifier.sh, tests, worth cases updated in PR #58). Both captures
re-scored verbatim under the promoted verifier:

```
=== vanilla:
FLAG: dangling forge reference (this repo has no remote/issues/PRs): '(#7)'
FLAG: no agent-authorship trailer in the delivered history (task-scoped: every arm is an agent)
exit=0
=== harness:
clean: 1 folded commit, CC subject, no local-only info, trailer discipline held, no dangling refs, authorship attributed
exit=1
```

**Under the promoted criteria this pair's delta is nonzero: vanilla flagged
(0) · harness clean (1).** The original verdict above ("NO measured
difference") remains the verdict **under the criteria in force on the run
date** and is not rewritten. Honest reading of the change: the promoted
criteria were *derived from this very pair's observed deltas*, so scoring the
same pair by them is circular as evidence of harness worth — it upgrades the
deltas from narrative to machine-checked, but only a **future** pair scored
by criteria fixed *before* the run counts as a clean nonzero measurement
(the 2026-07-25 Codex delivery-hygiene pair is the first such run).
