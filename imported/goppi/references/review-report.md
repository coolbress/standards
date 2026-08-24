# Review reporting — the format a review report must take

Loaded by `skills/review/SKILL.md` at its closing loop, when a review's findings
are written up. The review skill owns *when to review and how to judge*; this
file owns *what the record looks like afterwards* — the G3 evidence contract's
visible surface. A review that happened but left no readable record is, for every
later reader, a review that did not happen.

## Where the report lives

- **With a PR**: the full report is a **PR comment** — GitHub's native home for
  review artifacts. The fresh-context reviewer has no GitHub identity, so the
  driver posts it on the reviewer's behalf. The PR body's `## Verification` then
  carries **one line** — rung · findings count · triage outcome · re-check result
  — linking that comment. Post the comment first, so there is a URL to link.
- **Without a PR**: the same report goes in `progress.md`.
- **A skipped review** (the proportional trigger said skip) is recorded in the
  same place with its reason — a skip is a visible decision, not an absence.

## Format

Verdict first, findings anchored to code, long verification detail collapsed:

```markdown
## Independent review — <✅ PASS clean / ⚠️ N findings — all resolved / ⚠️ N findings — M unresolved / ❌ SPEC FAIL (stage 1)>

| | |
|---|---|
| Rung | <base / cross-vendor (<vendor>)> · executor: <native subagent / codex review / codex exec / claude -p> — <selected / DEGRADED: reason> |
| Stage 0 · pre-pass | <command → CLEAN / N findings attached / SKIPPED: reason> |
| Stage 1 · spec conformance | <PASS / FAIL → stage 2 not run / SKIPPED — no agreement artifact: reason> |
| Stage 2 · quality | <n HIGH · n MED · n LOW> (<n demoted: from→to>) |
| Triage | <n accepted · n rejected (grounds below)> |
| Fixes | <commit sha(s), amended / none needed> · <regression tests added / none expressible: reason> |
| Re-check | <gate command → result, output read> |

### Findings
1. **<issue|suggestion|nitpick> (<blocking|non-blocking>) · <HIGH|MED|LOW>** — [`path:line`](<permalink at the reviewed sha>)
   <failure path: input → wrong output → impact>
   → **<fixed in <sha> (+ test <name>): what changed / rejected: grounds / UNRESOLVED: why + follow-up>**

<details><summary>Checked and found sound</summary>

- <what was explicitly verified OK — so silence ≠ unchecked>
</details>
```

## Labels — rule-bound, not the driver's discretion

Labels follow Conventional Comments (`issue` = defect, `suggestion` =
improvement, `nitpick` = minor; `blocking` when the merge should wait) alongside
goppi's severity. The mapping is a rule because **the reviewed party must not be
able to soften its own review**:

| Triage outcome | Label |
|---|---|
| accepted HIGH | `issue (blocking)` |
| accepted MED / LOW | `issue` or `suggestion`, `(non-blocking)`, by kind |
| taste with grounds | `nitpick` |

Other rules that bind the write-up:

- The driver resolves every `path:line` to a permalink **at the reviewed head
  SHA** — a floating link rots the moment the branch moves.
- **Unresolved findings stay in the list**, marked plainly, and flip the headline
  to the `M unresolved` variant. An unresolved finding reported beats one quietly
  dropped.
- **Demotions are shown, not silently applied** — the `(n demoted: from→to)`
  cell exists so a reader can see the severity ladder ran (review skill, stage
  2), rather than inferring that nothing was ever claimed higher.
- The `Checked and found sound` block is not optional padding: without it,
  silence in a report is ambiguous between "verified fine" and "never looked".

## Evidence

- [census] Verdict-first summary, collapsible detail, and line-anchored findings
  are the established bot-reviewer comment shape (the form GitHub review bots
  converged on); finding labels follow Conventional Comments
  (conventionalcomments.org).
- [goppi-internal] That the review **must be recorded at all**, plus the triage
  and Iron-Law re-check rows, is goppi's own G3 evidence contract (ADR-0020) —
  recording an agent reviewer's report was observed nowhere in the public-repo
  census.
- [goppi-internal] Split out of `skills/review/SKILL.md` on 2026-07-25 (Session
  C) when that body measured **5,837 tokens against the §7 ≤5k cap**: the format
  is read by the driver at write-up time, after the reviewer's work is done, so
  it is the part of the skill that loses nothing by being one hop away — while
  the reviewer brief, the staged order, and the severity ladder stayed inline
  precisely because they are needed *before* the report exists.

## Expiry conditions

- The review skill's own report table stops changing shape for 3 consecutive
  design revisions **and** the body regains headroom under the §7 cap → fold
  this back inline; a one-file skill beats a two-file one at equal size.
- A host or forge ships a native structured-review artifact (machine-readable
  findings attached to the PR) → emit that instead and keep only the goppi
  deltas (rung row, triage row, demotion visibility).
