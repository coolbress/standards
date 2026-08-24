# result — clear-request-silence pair, Codex, 2026-07-24 (n=1)
<!-- genre: pair -->

The first controlled harness-vs-vanilla comparison pair executed on Codex.

| | |
|---|---|
| Task | `tasks/clear-request-silence/` |
| Host | Codex CLI 0.144.1 |
| Model | `gpt-5.6-sol`, pinned for probes and both arms |
| Arms | `--ephemeral --ignore-user-config --ignore-rules --skip-git-repo-check --dangerously-bypass-approvals-and-sandbox` |
| Harness material | project `AGENTS.md` = generated goppi contract + inlined `kickoff` skill |
| n | **1 pair.** pass@1 = pass^1; no reliability claim beyond this run |

## Probe verdict: PASS

Vanilla isolation probe (session
`019f91b3-ed4b-7ed0-938e-171f91486127`) reported:

```text
No actual AGENTS.md or similar instruction file was loaded from the filesystem.
No goppi material is loaded.
No skills named kickoff, scaffold, ship, governed, review, or harness-eval are loaded.
```

This is the important installed-plugin test: `--ignore-user-config` excluded
both the global contract and installed goppi/codex-native skills from the
vanilla arm.

Harness discovery probe (session
`019f91b4-2d97-7443-91fe-046ebbbf977e`) reported:

```text
Yes. This project loaded an AGENTS.md containing the five-clause goppi contract
and the inlined kickoff skill.
Contract verification rule: claim done only after running verification and
reading its output.
Kickoff rule for a clear, small request: stay silent and proceed without an
interview or kickoff ceremony.
```

The probe also correctly distinguished inlined project instructions from
natively discoverable skill packages.

## Pair verdict: no scored difference — both arms pass

| Criterion | Vanilla | Harness |
|---|---:|---:|
| `./longest-line.sh sample.txt` | `23` (exit 0) | `23` (exit 0) |
| Verification actually executed and output read | PASS | PASS |
| Clarifying questions before delivery | 0 | 0 |
| spec/plan/interview artifacts | none | none |
| **Task verdict** | **PASS** | **PASS** |

Real vanilla output (session
`019f91b4-4c14-7a00-9539-3bd26602119c`):

```text
$ ./longest-line.sh sample.txt
23
```

Real harness output (session
`019f91b4-968f-7352-9b7a-402902ecd033`):

```text
$ ./longest-line.sh sample.txt
23
```

The post-run driver independently executed both scripts and recorded:

```text
isolation_rc=0
discovery_rc=0
vanilla_rc=0
harness_rc=0
vanilla result=23 rc=0 ceremony_artifacts=none
harness result=23 rc=0 ceremony_artifacts=none
```

Raw run evidence was inspected at
`/private/tmp/goppi-codex-pair.PuB2b6/` before this record was written.

## Honest reading

On this task, model, host version, and day, vanilla Codex already showed the
desired clear-request silence and correct verification. The measured scored
worth of the inlined goppi advisory layer is therefore **zero at n=1**. This
validates the adapter and closes the first-Codex-pair blocker; it does not show
that kickoff improves reliability. Repetition is required to measure pass^k.

The harness script was marginally shorter while the vanilla script added an
argument-count guard. That is an unscored implementation difference and does
not change the task verdict.
