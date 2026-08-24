# Skill authoring — the standard for adding a goppi component (G8)

How to write a skill (and, where noted, any component: hook, checker,
reference) so it earns its context cost and can be deleted honestly. This is
the §8 component spec made concrete for the most common component kind.
Written from a 2026-07-24 research pass: both hosts' official guidance, the
open Agent Skills standard lineage, and goppi's own six shipped skills.

**Load path**: read when adding or materially revising a goppi component —
cited from AGENTS.md (repo-dev orientation) and applied by review when the
changed unit is a skill.

## The trigger contract — the description is the only always-injected surface

- The frontmatter `description` is the **only** text a host reads to decide
  when the skill fires; the body loads only after the trigger. So the
  description must carry the complete trigger contract on its own — never
  put when-to-use information *only* in the body, where it is invisible at
  trigger time. [lit: both vendors state this] (The body may still restate
  proportionality rules for judgment *after* firing — the shipped skills'
  "when to stay silent" sections do exactly that.)
- Write the description as a **trigger contract**, three parts, in this order:
  what the skill does → when to run it (concrete trigger phrases and
  situations) → **when NOT to run it**. The do-NOT clause is goppi's silence
  discipline [goppi-internal]: all six shipped skills carry one, because the
  observed failure mode of skill libraries is over-firing ceremony, not
  under-firing (§3.1 "waterfall in markdown").
- Budget the description: hosts truncate — Claude Code caps the listed
  description at 1,536 characters; Codex fits all descriptions into a ~2%
  skills context budget and shortens them when it overflows. [lit] House
  budget: all always-injected text (contract + every description) ≤2k tokens
  (§7) — measure the words when adding one.
- A side-effect skill the model must never fire on its own judgment gets
  `disable-model-invocation: true` (Claude; the description then leaves
  context entirely) — goppi's conditional-disclosure choice (§5), not the
  ambient "existence = active" style.

## The body — self-contained, thin, imperative

- **Assume the host model is already smart.** Add only what it does not have:
  procedural sequence, house policy, non-obvious domain facts. Challenge every
  paragraph: "does this justify its token cost?" [lit: Codex Skill Creator]
- **Self-contained**: the skill must work when its companion files are
  unreachable — restate the operative rules inline; a sibling reference
  carries the worked example and evidence, pointed to by path
  [goppi-internal: the review/governed pattern]. This deliberately diverges
  from the vendors' "never duplicate between body and references" rule
  [lit] — grounds: goppi skills deploy to hosts and projects where the
  sibling may not be installed, and a skill that silently degrades without
  its reference is a broken control. Keep the duplicated core small.
- Size: body ≤5k tokens (§7). The measured basis: after compaction, Claude
  re-attaches each invoked skill's first 5k tokens under a 25k combined
  budget — text beyond that can vanish mid-session [lit]. Codex guidance
  agrees (<500 lines, split beyond that). Companion references are the
  overflow, one level deep, each cited with *when* to read it.
- Imperative form throughout [lit: Codex]. Vendor-neutral wording (§5): no
  host-specific tool names or slash commands in the policy prose; where
  execution genuinely differs per host, use a host-conditional table
  [goppi-internal: the review skill's executor table is the precedent].
- No extraneous files in a skill directory (no README, CHANGELOG,
  installation guide) [lit: Codex] — a skill carries only what the agent
  needs to do the job.

## The gate — what earns a build, what earns a delete

- **Need proven, not "well-designed"** (§2 value 6): a skill is built on an
  observed gap or an explicit §8 trigger, never because it would be elegant.
  Rule-adds require the same failure twice + reproduction.
- **Evidence + Expiry are mandatory sections** (§8 component spec): `[lit]`
  justifies only that the mechanism class is useful — the specific
  implementation stays `[inferred]` until measured. A component without an
  expiry condition is rejected in review.
- **Deterministic parts get machine verification**: any script a skill ships
  gets a sibling `*.test.sh` wired into the check gate, plus
  `evals/worth/` fixtures where a WITH-vs-WITHOUT delta is expressible
  [goppi-internal]. Scripts are tested by running them, not by reading them
  [lit: Codex].
- **Validate in a fresh context**: forward-test with an agent that does not
  know it is testing — pass the task and raw artifacts, never your
  conclusions or the expected answer; authoring-session context masks gaps
  in the written instructions [lit: both vendors]. Trigger accuracy and
  output quality are measured separately [lit: Claude docs]; the controlled
  with-vs-without pair is goppi's `harness-eval` skill — use it, don't
  rebuild it.

## Dual-host notes

- **Claude Code**: fires on description matching or explicit `/name`;
  plugin skills are namespaced `/plugin:name`. `disable-model-invocation`
  and per-skill `allowed-tools` exist here only.
- **Codex**: fires when the user names the skill (`$SkillName` or plain
  text) or the task clearly matches the description — **for that turn only;
  a skill is not carried across turns unless re-mentioned**. The main agent
  must read the whole SKILL.md itself (delegating skill-reading to a
  subagent is forbidden by the host protocol). Plugin skills are prefixed
  `plugin_name:`. [lit: binary-embedded protocol, re-derived 2026-07-24]
- Both hosts (and Hermes-Agent) follow the Agent Skills open standard
  (agentskills.io) — SKILL.md + frontmatter is a 3-vendor convergence, so
  the format itself is stable ground [census].

## Evidence

- [lit] Codex Skill Creator (embedded in codex-cli 0.145.x, re-derived via
  `strings` 2026-07-24): concise-is-key, degrees of freedom, description as
  primary trigger, no-extraneous-files, <500-line body, script testing,
  forward-testing protocol. In-session skills protocol (same binary):
  `$SkillName` turn-scoped mention semantics, 2% description budget,
  read-SKILL.md-completely rule.
- [lit] code.claude.com/docs skills (fetched 2026-07-24): frontmatter
  reference, 1,536-char description cap, `disable-model-invocation` matrix,
  compaction re-attach 5k/25k budgets, evaluate-and-iterate (trigger accuracy
  vs output quality, fresh-session baseline comparison). Anthropic
  engineering "Agent Skills" post: progressive-disclosure levels,
  start-with-evaluation, name/description emphasis.
- [census] agentskills.io convergence: Anthropic + OpenAI + Nous
  Hermes-Agent all cite the standard (2026-07-24). Hermes's
  "autonomous skill creation" (workflow→skill promotion after complex
  tasks, verified at the repo 2026-07-24) and Anthropic's "ask Claude to
  capture its successful approaches into a skill" are the same
  capture-experience pattern — goppi keeps that promotion **human-gated**
  (§2 value 6: need proven, harness-eval recommends, human applies).
  Dated fact: the openai/skills curated repo is deprecated in favor of
  openai/plugins (2026-07-24) — cite the plugins guide, not the repo.
- [census] superpowers / writing-skills lineage: markdown skill library as
  the winning shape; two-stage review order precedent (design §3).
- [goppi-internal] The six shipped skills as precedents: every description
  carries a do-NOT clause; review/governed's self-contained-plus-sibling
  pattern; kickoff's trigger audit line + ceremony cap; §7 budgets; §8
  component spec (Evidence/Expiry, [lit]-scope discipline).

## Expiry conditions

- A host ships native skill-authoring guidance covering the trigger
  contract, budgets, and validation (e.g. a built-in skill-creator on the
  deployed host) → shrink this to the goppi-only deltas (silence discipline,
  Evidence/Expiry gate, worth fixtures).
- The §7 budgets or host truncation limits change on a host upgrade → the
  numbers here are stale; re-measure before trusting them (they are
  2026-07-24 values).
- Two review cycles where no component addition ever consults this file
  (no citation in any ADR or review record) → it is shelf documentation;
  fold the gate rules back into design §8 and delete.
