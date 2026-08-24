# Raw harvested shapes — hooks · slash-commands · subagents (captured 2026-06-27)

Verbatim/near-verbatim from the sources in `README.md`. Provenance for the standard doc; never edited.

---

## A. HOOKS (Claude Code) — `code.claude.com/docs/en/hooks`

### A1. Lifecycle events (the core set, + can-block)
| Event | Fires when | Can block? |
|---|---|---|
| `SessionStart` | new session starts or resumes (matcher source: `startup`/`resume`/`clear`/`compact`) | No (injects context) |
| `UserPromptSubmit` | user submits a prompt, before Claude processes it | **Yes** (exit 2 blocks + erases prompt) |
| `PreToolUse` | before a tool call executes (matcher = tool name) | **Yes** (exit 2 / `permissionDecision:"deny"` blocks) |
| `PostToolUse` | after a tool call succeeds (matcher = tool name) | No (tool already ran; can feed context / `decision:"block"`) |
| `Notification` | Claude Code sends a notification | No |
| `Stop` | Claude finishes responding | **Yes** (exit 2 / `decision:"block"` forces continue) |
| `SubagentStop` | a subagent finishes | **Yes** |
| `SubagentStart` | a subagent is spawned (matcher = agent type) | No |
| `PreCompact` | before context compaction (matcher `manual`/`auto`) | **Yes** |
| `SessionEnd` | session terminates | No |

> Newer CC builds add many more (`PostToolUseFailure`, `PermissionRequest`, `PostToolBatch`, `InstructionsLoaded`,
> `Elicitation`, `WorktreeCreate`, …) — the 10 above are the stable, cross-vendor-comparable core.

### A2. settings.json config skeleton (verbatim shape)
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/check.sh", "timeout": 600 }
        ]
      }
    ]
  }
}
```
- Locations + scope: `~/.claude/settings.json` (all projects, machine-local) · `.claude/settings.json` (project,
  committed) · `.claude/settings.local.json` (project, gitignored) · managed policy · plugin `hooks/hooks.json` ·
  skill/agent frontmatter. Enterprise: `"allowManagedHooksOnly": true`; kill switch `"disableAllHooks": true`.
- Matcher rules (verbatim): `"*"`/`""`/omitted = match all; only `[A-Za-z0-9_ ,|]` = exact or `|`/`,`-separated
  list (`Edit|Write`); anything else = JS regex (`mcp__memory__.*`). MCP tools are `mcp__<server>__<tool>`.

### A3. STDIN to a hook (common fields, verbatim)
```json
{ "session_id":"abc123", "transcript_path":"…/transcript.jsonl", "cwd":"…",
  "hook_event_name":"PreToolUse", "permission_mode":"default",
  "tool_name":"Bash", "tool_input":{ "command":"npm test" } }
```
Event-specific: `tool_response` (PostToolUse), `prompt` (UserPromptSubmit), `source`+`model` (SessionStart).

### A4. Exit-code semantics (verbatim)
- **Exit 0 — success.** stdout parsed for JSON output. For most events stdout → debug log; **exception:
  `UserPromptSubmit` / `SessionStart` stdout is visible to Claude** (injected as context).
- **Exit 2 — BLOCKING error.** JSON in stdout **ignored**; **stderr fed back to Claude**. Effect per event:
  PreToolUse=blocks the tool call · UserPromptSubmit=blocks+erases the prompt · Stop/SubagentStop=prevents
  stopping (continue) · PostToolUse=shows stderr to Claude (tool already ran) · PreCompact=blocks compaction.
- **Other non-zero (1, 3+) — non-blocking error.** Execution continues; transcript shows `<hook> hook error` + first stderr line.

### A5. Advanced JSON stdout (exit 0) — verbatim field names
Universal: `continue` (default `true`; `false` → Claude stops entirely), `stopReason` (shown to user when
`continue:false`), `suppressOutput` (`false`), `systemMessage` (warning to user).
Decision control: top-level `{ "decision":"block", "reason":"…" }` (UserPromptSubmit/PostToolUse/Stop/…).
PreToolUse uses `hookSpecificOutput`:
```json
{ "hookSpecificOutput": {
    "hookEventName":"PreToolUse",
    "permissionDecision":"allow|deny|ask",
    "permissionDecisionReason":"…",
    "additionalContext":"…" } }
```
SessionStart/UserPromptSubmit can return `hookSpecificOutput.additionalContext` (injected into context).

### A6. Security warning (verbatim)
> "Hooks are powerful and can execute arbitrary code. Always review hook configurations before enabling them,
> especially those from untrusted sources or plugins. Malicious hooks can read sensitive files, execute commands,
> or exfiltrate data."

### A7. Env vars / placeholders
`$CLAUDE_PROJECT_DIR` (project root), `${CLAUDE_PLUGIN_ROOT}` (plugin dir; command hooks), `${CLAUDE_PLUGIN_DATA}`,
`$CLAUDE_ENV_FILE` (SessionStart persistence). Plugin hooks live in `hooks/hooks.json` and reference `${CLAUDE_PLUGIN_ROOT}`.

---

## B. SLASH-COMMANDS → merged into SKILLS (Claude Code) — `/skills` doc

> **Verbatim, the convergence:** *"**Custom commands have been merged into skills.** A file at
> `.claude/commands/deploy.md` and a skill at `.claude/skills/deploy/SKILL.md` both create `/deploy` and work the
> same way. Your existing `.claude/commands/` files keep working. Skills add optional features: a directory for
> supporting files, frontmatter to control whether you or Claude invokes them, and the ability for Claude to load
> them automatically when relevant."*

- Classic command file: `.claude/commands/<name>.md` (project) / `~/.claude/commands/<name>.md` (personal); the
  Markdown body is the prompt. **The command name = the file/dir name**, not frontmatter. Subdir = namespace
  qualifier (`apps/web/.claude/skills/deploy` → `/apps/web:deploy`); plugin → `/<plugin>:<name>`.
- Substitutions (verbatim): `$ARGUMENTS` (all args; if absent, args appended as `ARGUMENTS: <value>`) ·
  `$ARGUMENTS[N]` / `$N` (0-based positional, shell-quoted) · `$name` (named, via `arguments:` frontmatter) ·
  `${CLAUDE_SKILL_DIR}` / `${CLAUDE_SESSION_ID}`. Escape literal with `\$`.
- Dynamic context: ``!`<command>` `` runs bash and **inlines the output before Claude sees it** (preprocessing,
  recognized only at line-start/after-whitespace; needs `allowed-tools: Bash(…)`); fenced ` ```! ` for multi-line;
  `@file` inlines a file. Kill switch `"disableSkillShellExecution": true`.
- Invocation control (the command↔skill knob, verbatim): `disable-model-invocation: true` → "Only you can invoke
  the skill. Use this for workflows with side effects … like `/commit`, `/deploy` … You don't want Claude deciding
  to deploy because your code looks ready." `user-invocable: false` → only Claude can invoke (background knowledge).
- Frontmatter superset: `name`, `description`, `when_to_use`, `argument-hint`, `arguments`, `allowed-tools`,
  `disallowed-tools`, `model`, `effort`, `context: fork`, `agent`, `hooks`, `paths`, `shell`.
- MCP prompts surface as `/mcp__<server>__<prompt>`. Permission rules: `Skill(name)` / `Skill(name *)`.

---

## C. SUBAGENTS (Claude Code) — `code.claude.com/docs/en/sub-agents`

### C1. File + frontmatter (verbatim example)
```markdown
---
name: code-reviewer
description: Expert code review specialist. Proactively reviews code … Use immediately after writing or modifying code.
tools: Read, Grep, Glob, Bash
model: inherit
---
You are a senior code reviewer …  (the body IS the system prompt)
```
- Locations + precedence: managed (1, highest) > `--agents` CLI (2) > `.claude/agents/` project (3) >
  `~/.claude/agents/` user (4) > plugin `agents/` (5). Loaded at session start (restart to pick up edits;
  `/agents` UI is live).
- Required: `name` (lowercase+hyphens; received by hooks as `agent_type`; filename need not match),
  `description` ("When Claude should delegate to this subagent"). Optional: `tools` (comma-sep; **omitted =
  inherits ALL tools**), `disallowedTools`, `model` (`sonnet`/`opus`/`haiku`/`fable`/full-id/`inherit`; default
  `inherit`), `permissionMode`, `skills` (preload full content), `mcpServers`, `hooks`, `memory`, `maxTurns`,
  `isolation: worktree`, `background`, `effort`, `color`, `initialPrompt`.
- **Plugin subagents do NOT support `hooks`/`mcpServers`/`permissionMode`** (security; ignored when loaded from a plugin).

### C2. Context isolation (verbatim, the core property)
> "Each subagent runs in its own context window with a custom system prompt, specific tool access, and independent
> permissions. When Claude encounters a task that matches a subagent's description, it delegates to that subagent,
> which works independently and returns results."
> "Each subagent starts with a fresh, isolated context window. It doesn't see your conversation history, the
> skills you've already invoked, or the files Claude has already read … only the relevant summary returns to your
> main conversation."
- "Subagents receive only this system prompt plus basic environment details … not the full Claude Code system prompt."
- Built-ins: **Explore** (Haiku, read-only) · **Plan** (read-only, plan mode) · **general-purpose** (all tools).
  Explore/Plan skip CLAUDE.md + git status. A **fork** inherits the full conversation (drops input isolation).
- Dispatch: automatic delegation via `description` (encourage with "use proactively"/"MUST BE USED") · explicit
  natural-language / `@agent-<name>` / session-wide `--agent`. The dispatch tool is **Agent** (renamed from `Task`
  in v2.1.63; `Task(...)` still aliases). `Agent(worker, researcher)` allowlists spawnable types.
- Best practices (verbatim): "Design focused subagents — each should excel at one specific task" · "Write detailed
  descriptions — Claude uses the description to decide when to delegate" · "Limit tool access — grant only
  necessary permissions" · "Check into version control."

---

## D. MULTI-AGENT RESEARCH SYSTEM (Anthropic eng) — verbatim numbers
- "A multi-agent system with Claude Opus 4 as the lead agent and Claude Sonnet 4 subagents outperformed
  single-agent Claude Opus 4 by **90.2%** on our internal research eval."
- "**token usage by itself explains 80%** of the variance" (BrowseComp; + #tool-calls + model-choice the other two).
- "agents typically use about **4× more tokens** than chat interactions, and multi-agent systems use about
  **15× more tokens** than chats."
- Helps: "multi-agent systems excel especially for **breadth-first queries** that involve pursuing multiple
  independent directions simultaneously." Hurts: "some domains that require all agents to share the same context
  or involve many dependencies between agents are not a good fit … **most coding tasks** involve fewer truly
  parallelizable tasks than research."
- Delegation: "Each subagent needs an objective, an output format, guidance on the tools and sources to use, and
  clear task boundaries." Effort scaling: "Simple fact-finding requires just 1 agent with 3-10 tool calls, direct
  comparisons might need 2-4 subagents …" Statefulness: "we need to durably execute code and handle errors …
  built systems that can resume from where the agent was when the errors occurred."

---

## E. CROSS-VENDOR CONVERGENCE — OpenAI Codex + Agents SDK

### E1. Codex Hooks — `developers.openai.com/codex/hooks` (near-identical to CC)
- Events: `SessionStart`, `SubagentStart`/`SubagentStop`, `PreToolUse`/`PostToolUse`, `PermissionRequest`,
  `PreCompact`/`PostCompact`, `UserPromptSubmit`, `Stop` — **the same names as Claude Code**.
- Config: `hooks.json` or inline `[hooks]` in `config.toml`; event → `matcher` (regex) → `command`-type handlers.
  "Only `type: "command"` handlers run today. `prompt` and `agent` handlers are parsed but skipped."
  ```toml
  [[hooks.PreToolUse]]
  matcher = "^Bash$"
  [[hooks.PreToolUse.hooks]]
  type = "command"
  command = '/usr/bin/python3 "path/to/script.py"'
  timeout = 30
  ```
- STDIN JSON: `session_id`, `transcript_path`, `cwd`, `hook_event_name`, `model` (+ `turn_id`, `permission_mode`).
  STDOUT JSON: `continue`, `stopReason`, `systemMessage`, `hookSpecificOutput` — **the same contract as CC**.
- Security: "Codex records trust against the hook's current hash, so new or changed hooks are marked for review
  and skipped until trusted." Managed hooks (`requirements.toml`) bypass the trust flow (policy control).

### E2. Codex custom prompts → skills (the SAME deprecation as CC)
- Custom prompts = Markdown in `~/.codex/prompts/`, invoked as slash commands; substitution `$1..$9`, `$NAME`
  (`KEY=value`), `$ARGUMENTS`, `$$` literal.
- Verbatim: "**Custom prompts are deprecated. Use skills for reusable instructions that Codex can invoke
  explicitly or implicitly.**" — "If you want to share a prompt (or want Codex to implicitly invoke it), use skills."
- AGENTS.md = always-on instructions (root + nested `AGENTS.override.md`); `notify` for `agent-turn-complete`.

### E3. OpenAI Agents SDK — handoffs = the sub-agent primitive — `openai.github.io/openai-agents-python/`
- Primitives: Agents (LLM + instructions + tools) · **Handoffs** ("allow agents to delegate to other agents for
  specific tasks") · Guardrails (parallel input/output validation) · Sessions · Runner loop · Tracing.
- Handoffs = tools to the LLM: a handoff to "Refund Agent" becomes the tool `transfer_to_refund_agent`.
  `handoffs=[…]` on `Agent`; `handoff(agent, on_handoff=…, input_type=…, input_filter=…)`.
- "When a handoff occurs, it's as though the new agent takes over the conversation, and gets to see the entire
  previous conversation history." `input_filter` trims it. Use `RECOMMENDED_PROMPT_PREFIX` for handoff-aware agents.
- Two orchestration styles: **handoffs** (delegate-and-transfer, triage pattern) vs **agents-as-tools**
  (manager keeps control, calls sub-agents as tools).

---

## F. OSS LAYOUT CENSUS (4 mature repos)
| Repo | What it ships | Observed convention |
|---|---|---|
| `ChrisWiles/claude-code-showcase` | agents+commands+hooks+skills+CI | `.claude/agents/*.md` (name/description/model/tools) · `.claude/commands/*.md` ($ARGUMENTS, inline-bash) · `.claude/hooks/*` wired in `.claude/settings.json` |
| `disler/claude-code-hooks-mastery` | 11-of-13 hook events demoed | hooks = **UV single-file Python** in `.claude/hooks/`, deps inline (isolated from project) · `uv run $CLAUDE_PROJECT_DIR/.claude/hooks/x.py` · exit-2 blocking + `{decision, reason}` JSON |
| `VoltAgent/awesome-claude-code-subagents` | 154+ subagents, 10 domains | `name`/`description`/`tools`/`model` frontmatter · organized by domain (core-dev, lang, infra, qa-sec, data-ai, dx, domains, biz, **meta-orchestration**, research) · meta agents (`agent-organizer`, `multi-agent-coordinator`, `workflow-orchestrator`) coordinate others · install to `~/.claude/agents/` |
| `hesreallyhim/awesome-claude-code` | curated index | confirms the four component families as the community vocabulary: skills · hooks · slash-commands · agent-orchestrators · plugins |
