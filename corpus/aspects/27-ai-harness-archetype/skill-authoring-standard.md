---
id: aspect-27-ai-harness-archetype--skill-authoring-standard
title: "Agent Skill authoring standard (SKILL.md — the frontier-AI build standard)"
parent: aspect-27-ai-harness-archetype
kind: reference
evidence_track: census+lit
status: review-needed
last_updated: "2026-06-27"
sources:
  - "https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills"
  - "https://claude.com/blog/lessons-from-building-claude-code-how-we-use-skills"
  - "https://code.claude.com/docs/en/skills"
  - "https://agentskills.io/specification"
  - "https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices"
  - "https://github.com/anthropics/skills"
  - "https://developers.openai.com/codex/skills"
  - "https://github.com/obra/superpowers"
method: "lit — read the Anthropic engineering post, the Claude Code 'how we use skills' blog, the Claude Code skills docs, the agentskills.io open spec, and the official best-practices page IN FULL; census — harvested verbatim SKILL.md frontmatter + folder layouts from anthropics/skills (template + skill-creator/pdf/mcp-builder), obra/superpowers, and the OpenAI Codex skills docs (cross-vendor adoption check). Raw blocks deposited at census-data/frontier-ai-components/skills/."
---

> **Standard (claim):** A frontier-grade Agent Skill is a **directory whose entrypoint is a `SKILL.md`** —
> YAML frontmatter (`name` + `description` required; small optional set) over a Markdown body — built for
> **progressive disclosure** (metadata always loaded → body on activation → bundled files on demand), kept
> **concise** (body < 500 lines / < ~5k tokens), with a **third-person, trigger-keyword description**, optional
> `scripts/`·`references/`·`assets/` referenced one level deep, and **eval-tested before ship**. It is the
> *procedure/capability* layer, distinct from the always-on constitution (CLAUDE.md/AGENTS.md), the MCP
> tool surface, and subagents.
> **Evidence:** lit (Anthropic engineering + best-practices + Claude Code docs + open spec) · census (anthropics/skills, obra/superpowers, OpenAI Codex adoption) · **Confidence:** high

This sub-doc is the concrete build spec behind aspect-27's "skill / hook packaging" bullet. gingoa scaffolds
skills for every user project, so this is the standard the scaffold must emit to.

## Why a cross-vendor standard exists

Agent Skills were "originally developed by Anthropic, released as an open standard" (agentskills.io), and the
format is now adopted across vendors: **Claude Code follows the [Agent Skills](https://agentskills.io) open
standard** and extends it [lit, code.claude.com], and **OpenAI Codex "build[s] on the open agent skills
standard"** with the identical `name`+`description` SKILL.md [lit, developers.openai.com]. So `SKILL.md` is a
genuinely portable artifact (gingoa's own `gingoa-ping/SKILL.md` is "portable across both hosts via the
SKILL.md open standard"). The standard below is the **open-spec core** + the **Anthropic best-practice layer**,
with host-specific extensions flagged.

## 1. Frontmatter schema (the contract)

A skill is "a folder with a required SKILL.md and optional supporting files" [lit]. `SKILL.md` MUST be YAML
frontmatter (`---` fenced) followed by a Markdown body. **Open-spec fields** [lit, agentskills.io/specification]:

| Field | Required | Constraint |
|---|---|---|
| `name` | **Yes** | Max **64 chars**; lowercase `a-z`/`0-9`/`-` only; no leading/trailing hyphen; no `--`; **must match the parent directory name**. |
| `description` | **Yes** | **Non-empty, max 1024 chars**; states *what it does* AND *when to use it*; include trigger keywords. |
| `license` | No | License name or reference to a bundled license file. |
| `compatibility` | No | Max 500 chars — environment needs (product, system packages, network). Most skills omit it. |
| `metadata` | No | Arbitrary string→string map (e.g. `author`, `version`); keep keys unique. |
| `allowed-tools` | No | Space-separated pre-approved tools. **Experimental — support varies by agent.** |

Anthropic's best-practices page tightens two rules [lit]: `name` may **not contain XML tags or the reserved
words "anthropic"/"claude"**; `description` must be **third person** ("Processes Excel files…", never "I/You
can…") because it is injected into the system prompt and POV mixing breaks discovery.

**Host extensions are additive, not forks.** Claude Code adds optional fields over the same core
[lit, code.claude.com]: `when_to_use`, `argument-hint`, `arguments`, `disable-model-invocation`,
`user-invocable`, `disallowed-tools`, `model`, `effort`, `context: fork`, `agent`, `hooks`, `paths`, `shell`.
**A portable skill uses only the open-spec core**; CC/Codex-only fields are layered when targeting that host.
Note one CC gotcha: the **command name comes from the directory**, not frontmatter `name` (so dir == name is
doubly load-bearing). OpenAI Codex adds an optional `agents/openai.yaml` alongside the standard layout.

## 2. Progressive disclosure (the load model — the whole point)

A skill is "an organized folder of instructions, scripts, and resources that agents discover and load
dynamically" [lit, engineering post]. Three tiers [lit, spec + engineering post]:

1. **Metadata (~100 tokens), always loaded.** Claude "pre-loads the `name` and `description` of every installed
   skill into its system prompt." Only the description costs context at rest → it is the single most important
   field for *selection among 100+ skills*.
2. **Body (< ~5000 tokens recommended), on activation.** The full `SKILL.md` loads only "when Claude deems the
   skill relevant." In Claude Code it then "stays in context across turns" — so every body line is a *recurring*
   token cost; "state what to do rather than narrating how or why" [lit, code.claude.com].
3. **Bundled files, on demand.** Referenced `scripts/`/`references/`/`assets/` are read "only as needed" — a
   reference file, dataset, or doc has **zero context cost until accessed**. Scripts are *executed* (only their
   output costs tokens), not loaded.

**Listing budgets** make the description cap real: Claude Code truncates the combined `description`+`when_to_use`
at **1,536 chars** in the listing and scales the whole listing at ~1% of the context window; OpenAI Codex caps
the listing at **2% of context or 8,000 chars**. Put the key use-case first so it survives truncation [lit].

## 3. Structure & sizing rules

- **Body < 500 lines.** Repeated across the spec, the docs, and best-practices: "Keep `SKILL.md` under 500
  lines. Move detailed reference material to separate files." [lit]
- **Concise is key** — "the context window is a public good." Assume Claude is already smart; only add context
  it doesn't have; challenge each line's token cost. Cut explanations of what a PDF/library/term *is* [lit].
- **Split when it grows** — "when the `SKILL.md` becomes unwieldy, split its content into separate files and
  reference them." Organize bundled files **by domain** so an unrelated domain never loads [lit].
- **References one level deep.** All bundled files link directly from `SKILL.md`; avoid nested reference chains
  (Claude may `head -100`-preview a 2-hops-deep file and miss content). Give reference files > 100 lines a
  table of contents [lit, best-practices].
- **Naming = gerund form** (`processing-pdfs`, `analyzing-spreadsheets`) or noun/action phrases
  (`pdf-processing`); avoid vague `helper`/`utils`/`tools` and reserved words [lit]. Mature OSS (obra/
  superpowers) goes further: flat searchable namespace, getting-started skills `<150` words, frequently-loaded
  `<200` words, description starts with "**Use when…**" (problem state, not workflow) [census].
- **Set the right degree of freedom**: high freedom (prose) for open tasks with many valid paths; low freedom
  (an exact script, "do not modify the command") for fragile/destructive sequences — the "narrow bridge vs open
  field" rule [lit, best-practices].

## 4. Bundled scripts & resources

- **Folders:** `scripts/` (executable code — Python/Bash/JS), `references/` (on-demand docs like
  `REFERENCE.md`/`FORMS.md`), `assets/` (templates, images, data) [lit, spec].
- **Code is both tool and documentation.** Pre-written utility scripts beat generated code — more reliable,
  save tokens (no code in context), save time, ensure consistency. Make execution intent explicit: "**Run**
  `analyze_form.py`" (execute) vs "**See** `analyze_form.py` for the algorithm" (read) [lit, best-practices].
- **Scripts must solve, not punt** — handle errors explicitly with helpful messages; no "voodoo constants"
  (every config value justified); always **forward-slash paths** even on Windows [lit].
- **Resolve paths portably.** Reference bundled files by relative path; for host invocation Claude Code exposes
  `${CLAUDE_SKILL_DIR}` so a script path resolves at personal/project/plugin level alike [lit, code.claude.com].
- **Verifiable intermediate outputs** for batch/destructive work: analyze → plan-file → validate → execute →
  verify (the "plan-validate-execute" pattern) [lit, best-practices].

## 5. When to use a Skill vs another component

The field has converged on a clear division of labor [lit, code.claude.com + developers.openai.com + blog]:

- **Skill** — a *reusable procedure/capability* that loads only when relevant: multi-step workflows,
  domain/library reference with gotchas, scaffolding, runbooks. "Create a skill when you keep pasting the same
  instructions, checklist, or multi-step procedure, or when a section of CLAUDE.md has grown into a *procedure*
  rather than a fact" [lit].
- **Constitution (CLAUDE.md / AGENTS.md)** — *always-on facts/rules* that apply to everything (build/test cmds,
  conventions, paths to avoid). The two-place split (OpenAI): "AGENTS.md for always-on team instructions, and
  Skills for reusable task workflows." A *fact* → CLAUDE.md; a *procedure* → a skill (body loads on demand, so
  long reference costs nothing until used) [lit].
- **Slash command** — in Claude Code, **commands have merged into skills**; a command is just a manually
  invoked skill. Use `disable-model-invocation: true` for an action you want to trigger by hand (`/deploy`,
  `/commit`) and not have the model fire on its own [lit, code.claude.com].
- **Subagent** — an *isolated execution context* with its own tools/permissions. Complementary, not
  alternative: a skill can run *in* a forked subagent (`context: fork` + `agent:`), or a subagent can preload
  skills as reference. Reach for a subagent when you need context isolation; for portable knowledge/procedure,
  the skill is the unit [lit, code.claude.com].
- **MCP server** — a *connection to an external system* (tools/resources over a protocol). "Skills can
  complement MCP servers by teaching agents more complex workflows" — MCP exposes the capability, the skill
  teaches the workflow that uses it (reference MCP tools as `Server:tool_name`) [lit, engineering + best-practices].

The nine skill *categories* Anthropic's own team ships [lit, blog]: library/API reference (gotchas+footguns) ·
product verification (Playwright etc.) · data fetching/analysis · business-process automation · code scaffolding
· code quality/review · CI-CD/deployment · runbooks (symptom-driven investigation) · infra operations (with
guardrails for destructive actions).

## 6. Security & permissions

- **Skills are untrusted code.** "Malicious skills may introduce vulnerabilities … or direct Claude to
  exfiltrate data and take unintended actions." Install only from trusted sources; audit code dependencies,
  bundled resources, and any instruction telling Claude to reach untrusted network sources [lit, engineering].
- **`allowed-tools` is pre-approval, not a sandbox.** It grants the listed tools without per-use prompts while
  the skill is active; it does **not** restrict the pool — every other tool still obeys your permission
  settings. For a project `.claude/skills/` skill it takes effect only after the workspace-trust dialog, "since
  a skill can grant itself broad tool access." Use `disallowed-tools` to remove tools for a skill's duration
  [lit, code.claude.com].
- **Gate destructive/side-effecting workflows** behind manual invocation (`disable-model-invocation: true`) so
  the model can't decide to deploy/commit on its own [lit].

## 7. Evaluation (don't ship on vibes)

"**Create evaluations BEFORE writing extensive documentation**" — evaluation-driven development: identify gaps
by running representative tasks without the skill → build **≥3 eval scenarios** → baseline → write the *minimal*
instructions that pass → iterate [lit, best-practices]. **Test across models** (Haiku/Sonnet/Opus) — what an
Opus skill assumes, a Haiku skill must spell out. The Claude-A/Claude-B loop: one Claude *authors* the skill,
fresh Claude instances *use* it on real tasks; refine from observed behavior, not assumptions. Anthropic ships
this as the `skill-creator` skill/plugin (eval cases in `evals/evals.json`, with/without-skill benchmark,
description tuning) [lit, code.claude.com + repo].

## 8. Anti-patterns (each cited)

- **Over-explaining / verbose body** — restating what Claude already knows; wastes recurring context [lit].
- **Vague description** ("Helps with documents") or first-person POV — breaks discovery among many skills [lit].
- **Body > 500 lines** with no split into `references/` — defeats progressive disclosure [lit].
- **Deeply nested references** (SKILL.md → a.md → b.md) — Claude partial-reads and misses content [lit].
- **Too many options** ("use pypdf or pdfplumber or PyMuPDF or…") — give one default + an escape hatch [lit].
- **Time-sensitive content** ("before August 2025, use…") — put deprecations in an "Old patterns" section [lit].
- **Inconsistent terminology** / **Windows backslash paths** / **magic constants** / **scripts that punt
  errors to Claude** [lit, best-practices].
- **Railroading** — over-specific instructions that remove Claude's judgment; give information + flexibility,
  except where the task is genuinely fragile [lit, blog].
- **Narrative examples tied to one session** / generic file names (`doc2.md`) — name files by content [census,
  obra/superpowers + lit].
- **Naming with `helper`/`utils`/`tools` or reserved words** [lit].

## How gingoa should scaffold a skill

gingoa scaffolds skills for every user project (and dogfoods this in `adapters/gingoa/skills/gingoa-ping/`).
The scaffold feature MUST emit, to match this standard:

1. **A directory whose name == the skill `name`** (kebab, ≤64 chars, lowercase/digits/hyphens, gerund-form
   suggested, no reserved word) containing a `SKILL.md`. The directory name carries the host command, so it must
   equal the frontmatter `name`.
2. **Open-spec-core frontmatter only by default** — `name` + a generated **third-person, ≤1024-char
   `description` that leads with the trigger** ("Use when…/Use this skill whenever…") — so the artifact is
   portable across Claude Code and Codex. Host-specific fields (`disable-model-invocation`, `allowed-tools`,
   `context: fork`, …) are opt-in toggles the scaffold offers, never baked into a portable skill.
3. **A < 500-line body skeleton** with the proven sections — `## Overview` (one line) · `## When to use` ·
   `## Instructions` (numbered steps) — concise, second-person-free, no "what is X" filler. For action skills,
   emit the `## Workflow` checklist pattern.
4. **Optional bundled folders** (`scripts/` · `references/` · `assets/`) scaffolded only when requested, with
   `SKILL.md` referencing them **one level deep** (and `${CLAUDE_SKILL_DIR}`-relative script invocations for the
   CC target). Scripts ship with explicit error handling, no magic constants, forward-slash paths.
5. **An eval stub** (`evals/evals.json` with ≥3 scenarios: query + expected_behavior) so the user inherits
   eval-driven development, plus a one-line "test with/without the skill in a fresh session" note.
6. **A frontmatter validation gate** — mirror aspect-27's manifest-schema rule: a vitest test (or `skills-ref
   validate`) asserting `name` regex/length, `description` non-empty/≤1024/third-person-ish, dir==name, and
   body < 500 lines for every scaffolded skill. **Presence ≠ adequacy**: a scaffolded `SKILL.md` that doesn't
   validate is a bug, not a deliverable.

This makes the gingoa skill scaffold emit the *open-standard* artifact (works on both hosts) at the
Anthropic-best-practice quality bar, gated like every other shipped guardrail.

## Sources

- Anthropic — Equipping agents for the real world with Agent Skills — https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- Claude — Lessons from building Claude Code: how we use skills — https://claude.com/blog/lessons-from-building-claude-code-how-we-use-skills
- Claude Code — Extend Claude with skills (docs) — https://code.claude.com/docs/en/skills
- Agent Skills — open specification — https://agentskills.io/specification
- Anthropic — Skill authoring best practices — https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- anthropics/skills (spec + template + example skills) — https://github.com/anthropics/skills
- OpenAI Codex — Agent Skills — https://developers.openai.com/codex/skills
- obra/superpowers (mature OSS skill pack) — https://github.com/obra/superpowers
- Raw harvested frontmatter + limits — `census-data/frontier-ai-components/skills/samples.md`
