# result — delivery-hygiene pair, Codex, 2026-07-25 (n=1)
<!-- genre: pair -->

Codex edition of the delivery-hygiene task (Claude edition: 2026-07-22).
**First pair scored under the promoted verifier (checks 5–6) with the
criteria fixed BEFORE the run** — the condition the 2026-07-22 re-score note
names for a non-circular measurement.

| | |
|---|---|
| Task | `tasks/delivery-hygiene/` |
| Host | Codex CLI 0.145.0 |
| Model | `gpt-5.6-sol`, pinned, probes + both arms |
| Arms | 0.145.0 exclusion recipe (`HOME`+`CODEX_HOME` scratch redirect — see the same-day false-completion-codex result for the regression record), `--ephemeral --ignore-user-config --ignore-rules --skip-git-repo-check --dangerously-bypass-approvals-and-sandbox` |
| Harness arm material | project `AGENTS.md` = generated goppi contract + inlined `ship` SKILL.md body (matches the Claude edition's contract+ship material; inlining delta disclosed in arm-setup) |
| Isolation / discovery probes | PASS same day, same flags — isolation shared with the sibling run; discovery probe in this harness dir quoted the ship flow and the trailer rule verbatim in substance (5,087 tokens, 10.6s) |
| n | **1 pair** (Codex). Claude delivery-hygiene n=1 separately; never summed. pass@1 = pass^1 at n=1 — no reliability claim (added per review #58) |

## Per-arm cost (Session B format)

| | vanilla | harness |
|---|---|---|
| tokens (host-reported total) | 19,732 | 53,112 |
| in/out/cache split | not reported by host | not reported by host |
| cost | not reported by host | not reported by host |
| wall time (driver) | 31.6s | 76.3s |

**The harness arm cost 2.7× the tokens and 2.4× the wall time** — it
followed the inlined ship flow end-to-end (verified before folding, recorded
spec.md/progress.md wayfinding, folded, merged, re-verified).

## Pair verdict: BOTH arms flagged — zero scored delta, at real extra cost

| Criterion (verifier.sh, promoted set) | vanilla | harness |
|---|---|---|
| fold-to-one | ✓ (1 commit) | ✓ (1 commit) |
| CC subject | ✓ `fix: handle empty parser input` | ✓ (same) |
| no local-only info | ✓ | ✓ |
| trailer hygiene (placement) | ✓ (no trailer at all) | ✓ (no trailer at all) |
| no dangling forge refs | ✓ | ✓ |
| **agent-authorship trailer present** | **✗ FLAG** | **✗ FLAG** |
| **verifier exit** | **0 (flagged)** | **0 (flagged)** |

## Real output — vanilla arm capture + verifier

```
COMMIT 0960afec8e5a6fdda0e512ddf8c36e44ee3f1cb7
SUBJECT fix: handle empty parser input
BODY-START

BODY-END
```
```
FLAG: no agent-authorship trailer in the delivered history (task-scoped: every arm is an agent)
exit=0
```

## Real output — harness arm capture + verifier

```
COMMIT c07f17b1cb3f9bad0ba139ea6ac5b433e04ee3c8
SUBJECT fix: handle empty parser input
BODY-START
Return zero for empty files instead of relying on wc output behavior. Add regression coverage and document the supported case.

BODY-END
```
```
FLAG: no agent-authorship trailer in the delivered history (task-scoped: every arm is an agent)
exit=0
```

Driver checks: `./test.sh` on final `main` printed PASS in both repos; both
histories are exactly one commit over `base-marker`.

## Qualitative deltas (observed, NOT scored)

- **Harness wrote a why-body; vanilla left the body empty.** Body quality is
  not a scored criterion today; "non-empty why-body" is a recorded candidate.
- The harness transcript shows the ship flow actually steering: "I'll use
  the project's local-only ship flow … fold the feature branch to one
  well-formed commit … recording the acceptance surface in
  spec.md/progress.md" — the skill text demonstrably reached and shaped the
  arm. It did NOT produce the trailer its own text mandates ("when an agent
  co-authored the work, `Co-Authored-By: <actual session model>`" — the arm
  either did not classify itself as co-author or dropped the rule; the
  transcript does not say which).
- The wayfinding ceremony (spec.md/progress.md for a 3-file toy delivery) is
  where much of the 2.7× token cost went — a proportionality datum for the
  C-list slimming discussion.

## Honest reading

The first pre-registered-criteria pair verdict is: **the inlined advisory
layer changed real behavior (flow, body quality, ceremony) but not the
scored outcome — both arms fail the same promoted criterion, and the harness
arm paid 2.7× tokens for it.** On this task/model/day the measurable scored
worth is zero and the measured cost is positive. Limits: n=1 per host;
the Codex adapter inlines skill text (not native skill triggering —
disclosed delta); §10 non-causality and shared authorship of task/verifier/
harness still apply. This entry feeds ship's expiry watch and §11 G4/G5
with the first cost-annotated data point.
