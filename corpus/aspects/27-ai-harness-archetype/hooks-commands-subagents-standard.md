---
id: aspect-27-ai-harness-archetype--hooks-commands-subagents-standard
title: "Hooks · Slash-commands · Subagents build standard (the orchestration/lifecycle layer — the frontier-AI standard)"
parent: aspect-27-ai-harness-archetype
kind: reference
evidence_track: census+lit
status: review-needed
last_updated: "2026-06-27"
sources:
  - "https://code.claude.com/docs/en/hooks"
  - "https://code.claude.com/docs/en/sub-agents"
  - "https://code.claude.com/docs/en/skills"
  - "https://code.claude.com/docs/en/slash-commands"
  - "https://code.claude.com/docs/en/best-practices"
  - "https://code.claude.com/docs/en/features-overview"
  - "https://www.anthropic.com/engineering/building-effective-agents"
  - "https://www.anthropic.com/engineering/multi-agent-research-system"
  - "https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents"
  - "https://claude.com/blog/building-agents-with-the-claude-agent-sdk"
  - "https://claude.com/blog/lessons-from-building-claude-code-how-we-use-skills"
  - "https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf"
  - "https://developers.openai.com/codex/hooks"
  - "https://developers.openai.com/codex/custom-prompts"
  - "https://developers.openai.com/codex/cli/slash-commands"
  - "https://developers.openai.com/codex/guides/agents-md"
  - "https://openai.github.io/openai-agents-python/"
  - "https://openai.github.io/openai-agents-python/handoffs/"
  - "https://github.com/ChrisWiles/claude-code-showcase"
  - "https://github.com/disler/claude-code-hooks-mastery"
  - "https://github.com/VoltAgent/awesome-claude-code-subagents"
  - "https://github.com/hesreallyhim/awesome-claude-code"
method: "lit — read the Claude Code hooks / sub-agents / skills(+commands) docs IN FULL, Anthropic's multi-agent-research-system engineering post and the 'how we use skills' blog, the OpenAI Codex hooks / custom-prompts / slash-commands / AGENTS.md docs, and the OpenAI Agents SDK overview + handoffs pages; census — harvested verbatim event tables, exit-code/JSON I/O contracts, frontmatter schemas, and real `.claude/{agents,commands,hooks}` layouts from claude-code-showcase, claude-code-hooks-mastery, awesome-claude-code-subagents (154+ subagents), and the awesome-claude-code index. Raw blocks deposited at census-data/frontier-ai-components/hooks-commands-subagents/."
---

> ⚠️ **2026-08-24 확인**: 이 문서의 frontmatter 목록은 현행과 일치한다(`fable`·`disallowedTools`·`permissionMode`·`mcpServers`·`memory`·`maxTurns`·`isolation: worktree`·`background`·`color` 포함). 현행에서 추가로 확인된 것은 **`initialPrompt` 필드**와 **중첩 기본 3단 / 동시 실행 최대 20**뿐이며 후자는 이 문서가 다루지 않는다 → [`claude-code-agent-surface--facts-2026-08`](claude-code-agent-surface--facts-2026-08.md) CAS-002.
> **Standard (claim):** The orchestration/lifecycle layer is **three distinct components with three distinct
> trigger models**, and choosing the right one is the whole skill: a **Hook** = *deterministic, event-triggered
> shell* that fires on a lifecycle event (`PreToolUse`/`PostToolUse`/`UserPromptSubmit`/`SessionStart`/`Stop`/…)
> over a **JSON-stdin → exit-code/JSON-stdout** contract (exit 0 ok · **exit 2 blocks** · stderr steers the model)
> — it runs **arbitrary, untrusted shell with the user's credentials**, so consent + review are mandatory. A
> **Slash-command** = a *manually-invoked prompt* (`.claude/commands/*.md`, `$ARGUMENTS`/`$N`, ``!`bash` ``/`@file`)
> that has **merged into Skills** on both Claude Code and Codex — a command is just a skill with
> `disable-model-invocation: true`. A **Subagent** = an *isolated execution context* (`.claude/agents/*.md`:
> `name`/`description`/`tools`/`model` + a system-prompt body) that the lead **dispatches** via the Agent tool and
> that returns **only a summary** to the main thread — the orchestrator-worker pattern that beat single-agent by
> **+90.2%** on Anthropic's research eval but burns **~15×** the tokens and **helps breadth-first research / hurts
> tightly-coupled coding**. OpenAI converges on every axis (identical hook events + I/O, prompts→skills
> deprecation, Agents-SDK handoffs as the sub-agent primitive).
> **Evidence:** lit (Claude Code docs + Anthropic multi-agent post + OpenAI Codex/Agents-SDK docs) · census
> (hook/frontmatter shapes + 4 OSS repos, incl. a 154-subagent library) · **Confidence:** high

This sub-doc is the concrete build spec behind aspect-27's "agent orchestration (planner/impl/review)" and
"skill / hook packaging" bullets — the *lifecycle/dispatch* half of the capability layer (the *capability* half is
[`skill-authoring-standard.md`](skill-authoring-standard.md) and [`mcp-server-standard.md`](mcp-server-standard.md)).
gingoa scaffolds hooks, commands, and subagents for every user project, so this is the standard the scaffold must
emit to. Facts are pinned to the Claude Code docs + Codex docs current at capture (2026-06-27).

## Why these three are one layer (and how they differ from skills/MCP)

The five components of the capability layer split cleanly by **who/what triggers them and where they run**:

| Component | Trigger | Runs in | Returns | Standard |
|---|---|---|---|---|
| **Hook** | a **lifecycle event** (deterministic) | a shell process / HTTP / MCP-tool | exit code + optional JSON that *blocks or steers* | this doc §1 |
| **Slash-command** | the **user** types `/x` (now = a skill) | the main conversation | a rendered prompt | this doc §2 |
| **Subagent** | the **lead model dispatches** (or user `@`-mentions) | its **own isolated context window** | a summary | this doc §3 |
| **Skill** | the **model** loads it when relevant (or user `/x`) | the main conversation (or a fork) | applied procedure | `skill-authoring-standard.md` |
| **MCP server** | the **model** calls a tool / user picks a resource | an external process/service | tool result / context | `mcp-server-standard.md` |

The load-bearing distinction: a **hook is the only deterministic, non-LLM control point** — it fires whether or not
the model wants it to, and it can *force* behaviour (block a tool, inject context, refuse to stop). Commands and
skills are *prompts the model reads*; subagents are *contexts the model spawns*. Get this mapping wrong and you
ship a fragile LLM-judged guardrail where a hook belonged, or a context-bloating subagent where a skill belonged.

## 1. Hooks — the deterministic lifecycle-event layer

### 1a. Lifecycle events (when each fires, whether it can block)
A hook is "a shell command that runs in response to events in Claude Code's lifecycle." The stable, cross-vendor
core [lit, code.claude.com/hooks]:

| Event | Fires | Can block / influence |
|---|---|---|
| `SessionStart` | session starts/resumes (source `startup`/`resume`/`clear`/`compact`) | injects context (stdout → Claude) |
| `UserPromptSubmit` | user submits a prompt, **before** the model sees it | **blocks** (exit 2 erases prompt); stdout → context |
| `PreToolUse` | **before** a tool call runs (matcher = tool name) | **blocks** the call (exit 2 / `permissionDecision:"deny"`) |
| `PostToolUse` | **after** a tool succeeds (matcher = tool name) | can't stop the tool; can feed context / `decision:"block"` next turn |
| `Notification` | Claude Code sends a notification | no |
| `Stop` | the model finishes responding | **blocks stopping** (exit 2 / `decision:"block"` → forces continue) |
| `SubagentStop` | a subagent finishes | **blocks** the subagent stopping |
| `SubagentStart` | a subagent is spawned (matcher = agent type) | no |
| `PreCompact` | before context compaction (matcher `manual`/`auto`) | **blocks** compaction |
| `SessionEnd` | session terminates | no (cleanup only) |

(CC ships many more — `PostToolUseFailure`, `PermissionRequest`, `PostToolBatch`, `InstructionsLoaded`,
`Elicitation`, `WorktreeCreate`, … — but the 10 above are the portable, Codex-shared core.)

### 1b. The config shape + matchers
Hooks are configured in `settings.json` (`~/.claude/` machine · `.claude/` committed · `.claude/settings.local.json`
gitignored · managed policy · plugin `hooks/hooks.json` · skill/agent frontmatter). The shape is
`hooks → EventName → [{ matcher, hooks:[{ type:"command", command, timeout }] }]` [lit]:
```json
{ "hooks": { "PreToolUse": [
  { "matcher": "Edit|Write",
    "hooks": [ { "type": "command",
                 "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/guard.sh",
                 "timeout": 600 } ] } ] } }
```
**Matcher rules** [lit, verbatim]: `"*"`/`""`/omitted = match all; `[A-Za-z0-9_ ,|]`-only = exact or `|`/`,`-list
(`Edit|Write`); anything else = a **JS regex** (`mcp__memory__.*`). Tool-name events (`PreToolUse`/`PostToolUse`)
take a tool-name matcher; `SessionStart`/`PreCompact` take a *source/trigger* matcher; `Stop`/`UserPromptSubmit`
take none. Plugins ship hooks via `hooks/hooks.json` and reference `${CLAUDE_PLUGIN_ROOT}`.

### 1c. The I/O contract (the part that actually matters)
A hook receives **JSON on stdin** — common fields `session_id`, `transcript_path`, `cwd`, `hook_event_name`,
`permission_mode`, plus event-specific `tool_name`/`tool_input` (PreToolUse), `tool_response` (PostToolUse),
`prompt` (UserPromptSubmit), `source` (SessionStart). It communicates back **two ways — pick one** [lit]:

- **Exit codes (simple):** **`0`** = success (stdout → debug log; **except `UserPromptSubmit`/`SessionStart`,
  whose stdout is injected as context to Claude**). **`2`** = **BLOCKING error** — stdout JSON is *ignored* and
  **stderr is fed back to Claude**; the effect is per-event (PreToolUse blocks the call · UserPromptSubmit
  blocks+erases · Stop/SubagentStop force-continue · PostToolUse just surfaces stderr since the tool already ran ·
  PreCompact blocks compaction). **Any other non-zero** = non-blocking error (logged, execution continues).
- **JSON on stdout (rich, exit 0):** universal `continue` (default `true`; `false` → Claude stops entirely),
  `stopReason`, `suppressOutput`, `systemMessage`; decision control `{"decision":"block","reason":…}`
  (UserPromptSubmit/PostToolUse/Stop); and for PreToolUse `hookSpecificOutput.permissionDecision`
  (`allow`/`deny`/`ask`) + `permissionDecisionReason` + `additionalContext`. **`exit 2` and JSON are mutually
  exclusive** — exit 2 discards stdout.

The canonical guardrail pattern (verbatim from the docs): a `PreToolUse`/`Bash` hook reads
`jq -r '.tool_input.command'`, and on a match emits `permissionDecision:"deny"` (or `exit 2`) to block a
destructive command before it runs. This is the deterministic floor a skill's prose can't provide. The same
determinism powers the **Stop hook as a verification gate**: Claude Code's best-practices page lists, as the
hardest of four ways to gate a turn, "**As a deterministic gate**: a Stop hook runs your check as a script and
blocks the turn from ending until it passes" — softer rungs being a one-prompt check, a `/goal` evaluator that
"re-checks it after every turn", and a "verification subagent … so the agent doing the work isn't the one grading
it" (Claude Code overrides the Stop hook after 8 consecutive blocks, so the gate can't loop forever)
[lit, best-practices].

### 1d. Security — hooks are arbitrary, untrusted shell (the first-class concern)
The docs' warning is the whole point [lit, verbatim]:
> "Hooks are powerful and **can execute arbitrary code**. Always review hook configurations before enabling them,
> especially those from untrusted sources or plugins. Malicious hooks can read sensitive files, execute commands,
> or exfiltrate data."

Consequences the standard demands: a hook runs **with the user's full credentials/env** the moment its event
fires, **without a per-run consent prompt** — so the consent boundary is *install/review time*, not *run time*.
Hence: review every hook (and every plugin's `hooks/hooks.json`) before enabling; prefer the `$CLAUDE_PROJECT_DIR`
prefix for reliable, non-injectable paths; gate the blast radius with `if`/matcher conditions; and note enterprise
controls (`"allowManagedHooksOnly": true`, `"disableAllHooks": true`). OpenAI Codex hardens the same boundary
differently — it **trusts a hook against its hash and re-flags any changed hook for review** until re-trusted
[lit, Codex hooks] — which is a stronger pattern gingoa should emulate when it ships hooks.

## 2. Slash-commands — the manual-prompt layer that merged into Skills

The single most important fact, verbatim from both vendors:
> "**Custom commands have been merged into skills.** A file at `.claude/commands/deploy.md` and a skill at
> `.claude/skills/deploy/SKILL.md` both create `/deploy` and work the same way." [lit, code.claude.com/skills]

So a **slash-command is now a special case of a skill**: a manually-invoked prompt. The classic format still works
and is the *minimal* command:

- **File:** `.claude/commands/<name>.md` (project) or `~/.claude/commands/<name>.md` (personal). **The command name
  comes from the file/dir name**, not frontmatter. A subdirectory becomes a **namespace qualifier**
  (`apps/web/.claude/skills/deploy` → `/apps/web:deploy`; a plugin → `/<plugin>:<name>`). The Markdown body is the prompt.
- **Frontmatter:** `description`, `argument-hint`, `allowed-tools`, `model`, `disable-model-invocation` (the
  command-vs-skill knob).
- **Substitutions** [lit]: `$ARGUMENTS` (all args; if the placeholder is absent, args are appended as
  `ARGUMENTS: <value>`) · `$ARGUMENTS[N]` / `$N` (0-based positional, shell-quoted) · `$name` (named, via
  `arguments:`). Escape a literal with `\$`.
- **Dynamic content** [lit]: ``!`<command>` `` runs bash and **inlines the output before the model sees the file**
  (pre-processing, recognized only at line-start / after-whitespace; needs `allowed-tools: Bash(…)`); a fenced
  ` ```! ` block for multi-line; `@file` inlines file contents. Kill switch `"disableSkillShellExecution": true`.
- **MCP prompts** surface as the slash command `/mcp__<server>__<prompt>` (the prompt↔command bridge — see `mcp-server-standard.md` §3).

**The command-vs-skill decision** (verbatim) [lit]: add `disable-model-invocation: true` "for workflows with side
effects or that you want to control timing, like `/commit`, `/deploy`, or `/send-slack-message`. You don't want
Claude deciding to deploy because your code looks ready." Inversely, `user-invocable: false` makes a skill
Claude-only background knowledge. So: **author a skill; set `disable-model-invocation` when you want command-like
manual-only behaviour.** OpenAI Codex made the *identical* move — "**Custom prompts are deprecated. Use skills for
reusable instructions that Codex can invoke explicitly or implicitly**" [lit, Codex custom-prompts] — confirming
this is a genuine cross-vendor convergence, not a Claude-only quirk.

## 3. Subagents — the context-isolation / orchestrator-worker layer

### 3a. File + frontmatter (the contract)
A subagent is a Markdown file whose **body is the system prompt** [lit, verbatim example]:
```markdown
---
name: code-reviewer
description: Expert code review specialist. Proactively reviews code … Use immediately after writing/modifying code.
tools: Read, Grep, Glob, Bash
model: inherit
---
You are a senior code reviewer …  (body = the subagent's system prompt)
```
- **Locations + precedence:** managed (highest) > `--agents` CLI > `.claude/agents/` (project) > `~/.claude/agents/`
  (user) > plugin `agents/` (lowest). Loaded at session start (restart to load disk edits; the `/agents` UI is live).
- **Required:** `name` (lowercase+hyphens; hooks receive it as `agent_type`; filename need not match) ·
  `description` ("When Claude should delegate to this subagent"). **Optional:** `tools` (comma-sep; **omitted =
  inherits ALL tools** — the most common footgun) · `disallowedTools` · `model` (`sonnet`/`opus`/`haiku`/`fable`/
  full-id/`inherit`, default `inherit`) · `permissionMode` · `skills` (preload full content) · `mcpServers` ·
  `hooks` · `memory` · `maxTurns` · `isolation: worktree` · `background` · `color`.
- **Plugin subagents do NOT support `hooks`/`mcpServers`/`permissionMode`** (a security restriction — ignored on load).

### 3b. Context isolation + the handoff-artifact discipline (the whole value)
The defining property, verbatim [lit, code.claude.com/sub-agents]:
> "Each subagent runs in its own context window … works independently and returns results." "Each subagent starts
> with a fresh, isolated context window. It doesn't see your conversation history, the skills you've already
> invoked, or the files Claude has already read … only the relevant summary returns to your main conversation."

So a subagent's *verbose work stays in its own window; only a summary crosses back* — this is the mechanism for the
"bounded context with explicit handoff artifacts" aspect-27 demands. This is precisely the role subagents play in
the Claude Agent SDK's feedback loop — *gather context → take action → verify work → repeat* — where subagents buy
both **parallelization** and **context isolation**, "send[ing] relevant information back to the orchestrator,
rather than their full context" while the SDK **compacts** older messages as the limit nears
[lit, building-agents-with-the-claude-agent-sdk]. The handoff is the load-bearing surface:
"Each subagent needs **an objective, an output format, guidance on the tools/sources, and clear task boundaries**"
[lit, multi-agent post]. A subagent can also `isolation: worktree` to get an isolated repo copy (so parallel
implementers never clobber each other) — the same pattern gingoa already uses for its own implementers.

**Dispatch model:** automatic delegation via the `description` (encourage with "use proactively" / "MUST BE USED")
or explicit `@agent-<name>` / session-wide `--agent`. The dispatch tool is **`Agent`** (renamed from `Task` in
v2.1.63; `Task(...)` aliases). Built-ins: **Explore** (Haiku, read-only) · **Plan** (read-only) · **general-purpose**
(all tools). A **fork** inherits the full conversation (deliberately dropping input isolation when the subagent
would need too much background).

### 3c. When multi-agent helps vs hurts (the eval, not vibes)
Anthropic's multi-agent research system is the canonical evidence [lit, verbatim]:
- **Result:** "a multi-agent system with Claude Opus 4 as the lead agent and Claude Sonnet 4 subagents
  outperformed single-agent Claude Opus 4 by **90.2%** on our internal research eval."
- **Cost:** "**token usage by itself explains 80%** of the variance"; "agents typically use about **4×** more
  tokens than chat … multi-agent systems use about **15×** more tokens than chats." Multi-agent works largely
  *because* it spends enough tokens — so it's only worth it when the task value justifies the spend.
- **Helps:** "multi-agent systems excel especially for **breadth-first queries** that involve pursuing multiple
  independent directions simultaneously."
- **Hurts:** "domains that require all agents to share the same context or involve many dependencies between
  agents are **not a good fit** … **most coding tasks** involve fewer truly parallelizable tasks than research."
- **Effort-scaling:** "Simple fact-finding requires just 1 agent with 3-10 tool calls; direct comparisons 2-4
  subagents …" — teach the lead to scale subagent count to query complexity, not spawn reflexively.
- **Reliability:** long-running stateful agents "need to durably execute code and handle errors"; build to
  **resume from the failure point**, not restart. Anthropic's "Effective harnesses for long-running agents"
  makes this concrete: because "each new session begins with no memory of what came before", a long run is
  carried by **durable handoff artifacts** — an initializer session emits an `init.sh` + a `claude-progress.txt`
  + a JSON feature list + a baseline git commit, and each subsequent session reads them, makes "incremental
  progress" on one feature, leaves "the environment in a clean state", and commits — so the harness resumes from
  recorded state rather than restarting [lit, effective-harnesses-for-long-running-agents]. (The persistence
  side of this lives in `plugin-marketplace-memory-standard.md` §9.)

### 3d. The orchestrator-worker / planner-impl-review pattern + cross-vendor
The pattern taxonomy this derives from is Anthropic's "Building effective agents", which names **five canonical
workflow patterns** — *prompt-chaining · routing · parallelization · orchestrator-workers · evaluator-optimizer* —
and draws the load-bearing **workflow-vs-agent** line: *workflows* "orchestrate LLMs and tools through predefined
code paths" while *agents* "dynamically direct their own processes and tool usage" [lit, building-effective-agents].
Its governing rule is the simplicity floor the whole when-to-use matrix (§4) rests on: start with "the simplest
solution possible" and add agentic complexity "**only when it demonstrably improves outcomes**" — "build the *right*
system for your needs", not the most sophisticated one. The planner→impl→review loop below is the
**orchestrator-workers** pattern (with an **evaluator-optimizer** review step) instantiated as Claude-Code
subagents. This is aspect-27's "planner → implementer → reviewer loop" made concrete: a **lead** decomposes and
dispatches **workers** in isolated contexts, each returning a handoff artifact (a plan, a diff, a review verdict).
OpenAI's "A practical guide to building agents" is the cross-vendor twin: it decomposes an agent into **Model +
Tools + Instructions**, and splits multi-agent into a **manager** pattern (one agent calls others as tools, keeping
control) vs a **decentralized** pattern where "agents can 'handoff' workflow execution to one another" — the same
two orchestration shapes (manager-calls-tools vs delegate-and-transfer) the Agents-SDK exposes below
[lit, practical-guide-to-building-agents]. The mature
OSS census confirms it as a first-class category — `awesome-claude-code-subagents` ships **154+ subagents across 10
domains** with a dedicated **`meta-orchestration`** family (`agent-organizer`, `multi-agent-coordinator`,
`workflow-orchestrator`) that coordinate the others [census]. OpenAI's **Agents SDK** is the same idea on the
other host: **handoffs** "allow agents to delegate to other agents for specific tasks" and are exposed to the LLM
as tools (`transfer_to_<agent>`); on handoff "the new agent … gets to see the entire previous conversation
history" unless an `input_filter` trims it — vs the **agents-as-tools** pattern where a manager keeps control
[lit, Agents-SDK]. Two orchestration shapes (delegate-and-transfer vs manager-calls-tools), one underlying
sub-agent primitive.

## 4. When-to-use decision matrix (the core deliverable)

This matrix aligns with the vendor's own — Claude Code's "Extend Claude Code" page ships a **"match features to
your goal"** decision table that distinguishes **CLAUDE.md vs Skill vs Subagent vs Hook vs MCP vs Plugin** on the
same axes used below, with the same load-bearing call: *"Put guardrails in hooks. An instruction … in CLAUDE.md or
a skill is a request, not a guarantee. A `PreToolUse` hook that blocks the edit is enforcement. If a rule must
hold every time, make it a hook rather than a prompt instruction."* [lit, features-overview]. Pick by **trigger +
determinism + isolation need**, in this order:

| If you need… | Use | Why (and not the others) |
|---|---|---|
| A rule enforced **deterministically** on every occurrence of an event (block `rm -rf`, auto-format on save, inject project state at session start, refuse-to-stop-until-tests-pass) | **Hook** | Only a hook is non-LLM and can *force* behaviour. A skill's prose is advisory; the model can ignore it. "use hooks to enforce behaviour deterministically" [lit]. |
| A **user-initiated**, manual action with side effects (`/deploy`, `/commit`, `/release`) | **Slash-command = skill + `disable-model-invocation: true`** | You control timing; the model must not fire it on its own [lit]. |
| A **reusable procedure / domain knowledge** the model should apply when relevant (a runbook, a library's gotchas, a multi-step workflow) | **Skill** | Loads on relevance via `description`; body costs nothing until used (progressive disclosure). See `skill-authoring-standard.md`. |
| **Context isolation** — a verbose side-task (run the suite, research 3 modules, audit a diff) whose output you don't want in the main window | **Subagent** | Verbose work stays in its own context; only a summary returns. "keeping exploration and implementation out of your main conversation" [lit]. |
| **Breadth-first, parallelizable** investigation across independent directions, where value > token cost | **Multiple subagents (orchestrator-worker)** | +90.2% on research eval; but ~15× tokens → only when parallel and high-value [lit]. |
| A **tightly-coupled** task needing shared context / many inter-step dependencies (most coding) | **Main conversation (or a skill)** — *not* multi-agent | "not a good fit for multi-agent systems … most coding tasks involve fewer truly parallelizable tasks" [lit]. |
| A connection to an **external system** (DB, API, SaaS) the model calls as tools | **MCP server** | Tools/resources over a protocol; see `mcp-server-standard.md`. A skill/command *uses* MCP tools; it isn't one. |
| **Always-on facts/rules** that apply to everything (build/test cmds, conventions) | **Constitution** (`CLAUDE.md` / `AGENTS.md`) | A *fact* → constitution; a *procedure* → skill; a *deterministic enforcement* → hook. |

Two recurring mistakes the matrix prevents: (1) **a skill where a hook belonged** — a "never commit secrets"
skill is advisory and skippable; the same rule as a `PreToolUse` hook is enforced. (2) **a subagent where a skill
belonged** — wrapping a reusable procedure in a subagent pays context-isolation + restart cost for knowledge that
should just load inline.

## 5. Testing & evaluation (don't ship any of the three on vibes)

- **Hooks:** unit-test the script directly — pipe a representative stdin JSON and assert the **exit code** + emitted
  JSON (`permissionDecision`/`decision`). Test the **block path** (exit 2 on the dangerous input) *and* the
  pass-through path (exit 0 otherwise), because a hook that fails open is worse than no hook. Keep hook scripts
  short, dependency-isolated (the OSS norm: **UV single-file Python** in `.claude/hooks/`, deps inline [census,
  hooks-mastery]), and bounded by `timeout`.
- **Slash-commands / skills:** the skill eval loop — `≥3` realistic prompts, run **with vs without** in fresh
  sessions, compare; for `disable-model-invocation` commands, verify the model does *not* auto-fire them. (Full
  method in `skill-authoring-standard.md` §7 + the `skill-creator` plugin.)
- **Subagents:** eval the **dispatch decision** (does the lead delegate on the right tasks? — the `description`
  is the lever) *and* the **handoff quality** (is the returned summary sufficient, in the declared output format?).
  For multi-agent, measure the +pass-rate **against the token/time overhead** before adopting it — the eval, per
  Anthropic, is dominated by token spend, so the question is always "is the parallelism worth ~15×?". The canonical
  review shape is the best-practices **Writer/Reviewer** split — one session implements, a *fresh* subagent context
  reviews "so the agent doing the work isn't the one grading it" — plus an **adversarial review** step before a task
  is called done: "have a subagent review the diff in a fresh context and report gaps", scoped to "flag only gaps
  that affect correctness or the stated requirements" (an over-eager reviewer "will usually report some, even when
  the work is sound"). The same page anchors the **explore→plan→code** discipline (plan mode separates research
  from execution) and the **`claude -p` headless / fan-out** primitive — loop `claude -p` over a task list with
  `--allowedTools` to scope a batch migration [lit, best-practices].

## 6. Anti-patterns (each cited)

- **An LLM-judged guardrail where a hook belonged** — relying on a skill/prompt to "never run destructive
  commands" instead of a deterministic `PreToolUse` block. Prose is advisory; only the hook enforces [lit].
- **A hook that fails open silently** — exits 0 on the path it was meant to block, or punts to non-blocking exit 1
  when it meant exit 2. The block path must be tested [inferred from exit-code semantics].
- **Writing to stdout from a non-injecting hook** — only `UserPromptSubmit`/`SessionStart` stdout reaches Claude;
  elsewhere stray stdout just clutters the debug log, and **exit 2 discards stdout entirely** [lit].
- **Trusting plugin/3rd-party hooks unread** — hooks run arbitrary shell with your credentials the instant their
  event fires, with no per-run prompt; review before enabling (Codex even re-flags changed hooks by hash) [lit].
- **`tools:` omitted on a subagent that shouldn't have them all** — omitting `tools` **inherits every tool**; a
  reviewer/researcher should be `tools: Read, Grep, Glob` (read-only), enforced by the field [lit].
- **A subagent for a tightly-coupled or trivial task** — pays fresh-context + latency + summary-loss cost for work
  that shares context with the main thread; "use the main conversation when multiple phases share significant
  context" [lit].
- **Reflexive multi-agent (the ~15× tax)** — fanning out subagents on a task that isn't breadth-first
  parallelizable burns tokens for no gain and risks subagents conflicting; "most coding tasks" don't qualify [lit].
- **Detailed subagent results dumped back to main** — "running many subagents that each return detailed results
  can consume significant context"; constrain the handoff to a summary in a declared format [lit].
- **A model-invocable command with side effects** — a `/deploy` the model can fire on its own; gate with
  `disable-model-invocation: true` [lit].
- **Authoring a fresh `.claude/commands/*.md` as the strategic unit** — it still works, but it's the legacy
  minimal form; the skill is the forward unit (supporting files, invocation control, auto-load) on both vendors [lit].

## How gingoa should scaffold each

gingoa scaffolds the orchestration layer for user projects (and dogfoods it — its own harness is built from hooks,
skills, and subagents). The scaffold MUST emit, to match this standard:

1. **Hooks — a tested, deterministic shell with a consent boundary.** Emit a `.claude/hooks/<name>.{sh,py}` script
   + the `settings.json` wiring (`PreToolUse`/`PostToolUse`/`SessionStart`/`Stop` as chosen), using the
   `$CLAUDE_PROJECT_DIR` path prefix, an explicit `timeout`, and the **JSON-stdin → exit-2/`permissionDecision`**
   contract. **Ship a vitest/shell test that pipes a sample stdin and asserts the block path (exit 2) AND the
   pass path (exit 0)** — a hook that only fails-open is a bug, not a guardrail (presence ≠ adequacy). Surface the
   arbitrary-shell security note at scaffold time and never auto-enable a hook the user hasn't reviewed; for
   plugin-shipped hooks, prefer a Codex-style hash-trust note.
2. **Slash-commands — scaffold a *skill*, offer the command toggle.** Default to a `.claude/skills/<name>/SKILL.md`
   (the forward, cross-host unit), and offer `disable-model-invocation: true` as the opt-in that makes it a
   manual-only command (`/deploy`, `/commit`). Wire `$ARGUMENTS`/`$N`, and ``!`bash` ``/`@file` injection only with
   the matching `allowed-tools`. (Defer to `skill-authoring-standard.md` for the body.) Keep a `.claude/commands/*.md`
   emitter only as the legacy minimal form.
3. **Subagents — focused, least-privilege, summary-returning.** Emit a `.claude/agents/<name>.md` with `name` +
   a **trigger-keyworded `description`** (incl. "use proactively" when auto-delegation is wanted), an **explicit
   `tools` allowlist** (never rely on the inherit-all default for a constrained role; read-only reviewers get
   `Read, Grep, Glob`), and a `model` (route cheap/read-heavy work to `haiku`). The body states the workflow and
   the **required output format** so the handoff artifact is bounded. Offer `isolation: worktree` for parallel
   implementers. Do **not** scaffold a subagent for tightly-coupled work — route that to a skill or the main thread.
4. **An orchestrator-worker template, gated on fit.** For breadth-first research/audit, scaffold a lead +
   worker-subagent pattern with delegation prompts that give each worker *objective + output-format + tool
   guidance + boundaries*, and a one-line note that multi-agent is **~15× tokens** and only pays off for
   parallelizable, high-value work — so the user doesn't reach for it on a coding task.
5. **A portability stance.** Hooks and the prompts→skills convergence are cross-host (Claude Code + Codex use the
   same hook event names + JSON I/O, and both deprecate custom-prompts toward skills) — so a gingoa-scaffolded hook
   and skill are near-portable; a Claude-Code subagent maps to a Codex/Agents-SDK **handoff**. Emit the portable
   core; flag host-only fields (CC's rich `hookSpecificOutput`, the subagent frontmatter superset) as host-targeted.
6. **A validation gate** — mirror aspect-27's "presence ≠ adequacy" rule: a vitest test asserting every scaffolded
   hook script returns the right exit code on its block/pass fixtures, every subagent file has `name` + non-empty
   `description` + (for constrained roles) an explicit `tools` list, and the `settings.json` hook wiring parses.
   A scaffolded guardrail that isn't tested is not a deliverable.

This makes the gingoa orchestration scaffold emit **deterministic, consent-gated hooks + forward-compatible
(skill-based) commands + isolated, least-privilege subagents** at the Anthropic/OpenAI quality bar, with the eval
discipline and the when-to-use boundaries baked in — gated like every other shipped guardrail.

## Sources

- Claude Code — Hooks reference (events, matchers, JSON I/O, exit codes, security warning, plugin hooks) — https://code.claude.com/docs/en/hooks
- Claude Code — Create custom subagents (frontmatter, context isolation, dispatch, scopes) — https://code.claude.com/docs/en/sub-agents
- Claude Code — Extend Claude with skills (the commands-merged-into-skills convergence, `disable-model-invocation`, `$ARGUMENTS`/`!bash`/`@file`) — https://code.claude.com/docs/en/skills
- Claude Code — Slash commands reference — https://code.claude.com/docs/en/slash-commands
- Claude Code — Best practices (CLAUDE.md tuning; Stop-hook-as-gate / `/goal` evaluator / verification subagent; explore→plan→code; Writer/Reviewer + adversarial review; `claude -p` headless/fan-out) — https://code.claude.com/docs/en/best-practices
- Claude Code — Extend Claude Code / features-overview (the vendor "match features to your goal" matrix: CLAUDE.md vs Skill vs Subagent vs Hook vs MCP vs Plugin; "put guardrails in hooks") — https://code.claude.com/docs/en/features-overview
- Anthropic — Building effective agents (the 5 workflow patterns; workflows-vs-agents; "add complexity only when it demonstrably improves outcomes") — https://www.anthropic.com/engineering/building-effective-agents
- Anthropic — How we built our multi-agent research system (orchestrator-worker, +90.2%, token economics, when multi-agent helps/hurts) — https://www.anthropic.com/engineering/multi-agent-research-system
- Anthropic — Effective harnesses for long-running agents (durable execution; resume-not-restart via init.sh + progress log + feature list + git baseline) — https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- Claude — Building agents with the Claude Agent SDK (the gather→act→verify→repeat loop; subagents for parallel context; compaction; tool design) — https://claude.com/blog/building-agents-with-the-claude-agent-sdk
- Claude — Lessons from building Claude Code: how we use skills (nine categories; on-demand hooks `/careful`/`/freeze`; adversarial-review subagent) — https://claude.com/blog/lessons-from-building-claude-code-how-we-use-skills
- OpenAI — A practical guide to building agents (Model + Tools + Instructions; single vs multi-agent: manager vs decentralized/handoffs; guardrails) — https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf
- OpenAI Codex — Hooks (same event names + JSON I/O; hash-trust security; command-only handlers) — https://developers.openai.com/codex/hooks
- OpenAI Codex — Custom prompts (deprecated in favor of skills) — https://developers.openai.com/codex/custom-prompts
- OpenAI Codex — Slash commands in Codex CLI — https://developers.openai.com/codex/cli/slash-commands
- OpenAI Codex — Custom instructions with AGENTS.md — https://developers.openai.com/codex/guides/agents-md
- OpenAI Agents SDK — overview (Agents · Handoffs · Guardrails · Sessions · Runner · Tracing) — https://openai.github.io/openai-agents-python/
- OpenAI Agents SDK — Handoffs (delegate-to-agent as a tool; `input_filter`; `RECOMMENDED_PROMPT_PREFIX`) — https://openai.github.io/openai-agents-python/handoffs/
- ChrisWiles/claude-code-showcase (real `.claude/{agents,commands,hooks}` + settings.json) — https://github.com/ChrisWiles/claude-code-showcase
- disler/claude-code-hooks-mastery (11-of-13 hook events; UV single-file Python hooks; exit-2/JSON patterns) — https://github.com/disler/claude-code-hooks-mastery
- VoltAgent/awesome-claude-code-subagents (154+ subagents, 10 domains, meta-orchestration family) — https://github.com/VoltAgent/awesome-claude-code-subagents
- hesreallyhim/awesome-claude-code (community index confirming the component vocabulary) — https://github.com/hesreallyhim/awesome-claude-code
- Raw harvested event tables + frontmatter + I/O contracts + OSS census — `census-data/frontier-ai-components/hooks-commands-subagents/samples.md`
