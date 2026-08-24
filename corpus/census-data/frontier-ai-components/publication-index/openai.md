# OpenAI — publication-surface enumeration (frontier-AI components coverage census)

**Run date:** 2026-06-27
**Purpose:** Phase A coverage census — enumerate OpenAI's official publication surfaces relevant to the
5 component build-standards (skills · MCP · hooks/commands/subagents · plugins/marketplace/memory · prompts/evals),
to diff against what those sub-docs already cite. See `coverage-report.md` for the diff + gap list.
**Append-only** (research-deposit-rule). Companion: `anthropic.md`.

> Note on scope: gingoa's 5 sub-docs treat OpenAI as the **cross-vendor convergence/divergence check** (the
> primary host is Claude Code; Codex is the second host). So the OpenAI bar for "load-bearing" is *does it change
> a build rule or add a divergence the portable artifact must respect* — not "every OpenAI doc". Most OpenAI
> agent-infra docs corroborate the Anthropic-primary rules; the gaps below are the few that add a rule/number.

## ENUMERATION LIMITS

- **`developers.openai.com` / `platform.openai.com` docs** — these are the surfaces the sub-docs already cite
  heavily (prompt-engineering, reasoning, evals, graders, agent-evals, function-calling, conversation-state,
  apps-sdk, codex/*). I enumerated the **net-new pages** the sub-docs missed (structured-outputs, prompt-caching,
  building-agents track) rather than re-walking the full doc tree. Not exhaustively paginated — topic-searched.
- **`cookbook.openai.com` / `developers.openai.com/cookbook`** — **PARTIALLY walked.** The index is topic-bucketed
  (Agents / Evals / Optimization / Text / Codex) and JS-rendered; I could not paginate each bucket fully via fetch.
  Enumerated the high-relevance recipes via topic + targeted search (GPT-4.1, GPT-5.1, Optimize Prompts, agent
  improvement loop, prompt-caching). Other cookbook recipes likely exist but are not build-standard load-bearing.
- **`openai.com/research` / `openai.com/index`** — **NOT walked as an index** (JS-rendered). Enumerated by
  targeted search for the agent/tool/eval-relevant announcements ("A practical guide to building agents",
  "New tools for building agents"). OpenAI's pure ML research papers (GPT-x system cards, o-series) were judged
  not-relevant to a *component build standard* and not enumerated exhaustively.
- **`openai.github.io` (Agents SDK)** — the Python SDK overview/handoffs/sessions/mcp pages are already cited;
  I enumerated the remaining doc pages (tools, guardrails, tracing, running_agents) — they corroborate, see below.
- **`github.com/openai`** — openai-cookbook, openai-evals, openai-agents-python/js are the relevant repos; the
  sub-docs cite the Agents-SDK docs site rather than the repo. Not re-walked file-by-file.

---

## Surface 1 — developers.openai.com / platform docs

`✓ = already cited · ✗ = not cited`

| Title | URL | Topic | Component | Cited |
|---|---|---|---|---|
| Prompt engineering | /api/docs/guides/prompt-engineering | developer/user/assistant authority hierarchy; caching order | prompts-evals | ✓ |
| Prompt guidance | /api/docs/guides/prompt-guidance | outcome-first; prompts-in-code; objects deprecation | prompts-evals | ✓ |
| Migrate from prompt objects | /api/docs/guides/prompting/migrate-from-prompt-object | the `prompts/` module rule + sunset dates | prompts-evals | ✓ |
| Reasoning best practices | /api/docs/guides/reasoning-best-practices | keep-it-simple, avoid-CoT, developer-msgs, zero-shot | prompts-evals | ✓ |
| Evals | /api/docs/guides/evals | behavior-driven; datasets/JSONL; templating | prompts-evals | ✓ |
| Graders | /api/docs/guides/graders | string_check/text_similarity/score_model/label_model/python/multigrader | prompts-evals | ✓ |
| Evaluate agent workflows / trace grading | /api/docs/guides/agent-evals | trace = model+tool+guardrail+handoff record | prompts-evals | ✓ |
| Function calling | /api/docs/guides/function-calling | native function-tool schema (contrast vs MCP) | mcp | ✓ |
| Conversation state | /api/docs/guides/conversation-state | Responses `previous_response_id` + Conversations API; `store:false` | plugins-marketplace-memory | ✓ |
| Apps SDK | /apps-sdk | build a ChatGPT app *as* an MCP server | mcp | ✓ |
| Structured model outputs | /api/docs/guides/structured-outputs | schema-adherent outputs (the prefill-replacement on the OpenAI side) | prompts-evals (peripheral) | ✗ |
| Prompt caching | /api/docs/guides/prompt-caching | automatic caching; static-prefix-first ordering (80%/90%) | prompts-evals (corroborates §2 caching) | ✗ |
| Building agents (track) | /tracks/building-agents | reasoning models + Responses API agent-building track | hooks-commands-subagents (peripheral) | ✗ |

## Surface 2 — Codex docs (the second-host convergence surface)

| Title | URL | Topic | Component | Cited |
|---|---|---|---|---|
| Codex — Agent Skills | /codex/skills | Codex builds on the open Agent Skills standard | skills | ✓ |
| Codex — Hooks | /codex/hooks | same hook events + JSON I/O; hash-trust | hooks-commands-subagents | ✓ |
| Codex — Custom prompts (deprecated→skills) | /codex/custom-prompts | prompts→skills convergence | hooks-commands-subagents | ✓ |
| Codex — Slash commands | /codex/cli/slash-commands | Codex CLI slash commands | hooks-commands-subagents | ✓ |
| Codex — AGENTS.md | /codex/guides/agents-md | static instruction file (cross-host CLAUDE.md twin) | plugins-memory + hooks-commands-subagents | ✓ |
| Codex — Memories | /codex/memories | AGENTS.md static + ~/.codex/memories generated | plugins-marketplace-memory | ✓ |

## Surface 3 — cookbook.openai.com (PARTIAL — high-relevance recipes)

| Title | URL | Date | Topic | Component | Cited |
|---|---|---|---|---|---|
| GPT-5 prompting guide | /cookbook/examples/gpt-5/gpt-5_prompting_guide | 2025-08 | reasoning_effort, eagerness, tool preambles, contradiction trap, metaprompting | prompts-evals | ✓ |
| GPT-5.1 prompting guide | /cookbook/examples/gpt-5/gpt-5-1_prompting_guide | 2025-11-13 | NEW `none` reasoning tier; persistence ("end-to-end within the turn"); user-update preambles (every 6–8 tool calls); apply_patch/shell tools | prompts-evals | ✗ |
| GPT-4.1 prompting guide | /cookbook/examples/gpt4-1_prompting_guide | 2025-04 | agentic prompt reminders (persistence/tool-calling/planning); use `tools` field not injected descriptions | prompts-evals | ✗ |
| Optimize Prompts | /cookbook/examples/optimize_prompts | — | the prompt-optimizer system (Agents-SDK + Evals; contradiction/format/example checks) | prompts-evals (authoring tooling) | ✗ |
| Build an Agent Improvement Loop with Traces, Evals, and Codex | /cookbook/examples/agents_sdk/agent_improvement_loop | — | traces→reviewer→generated-evals→optimize→implement loop | prompts-evals (§7 lifecycle) | ✗ (named in §7 prose, not URL-cited) |
| Prompt Caching 101 / 201 | /cookbook/examples/prompt_caching101 (/201) | — | caching mechanics | prompts-evals (peripheral) | ✗ |

## Surface 4 — openai.com/index + business guides (announcements / guides)

| Title | URL | Topic | Component | Cited |
|---|---|---|---|---|
| A practical guide to building agents | openai.com/.../a-practical-guide-to-building-ai-agents/ (PDF: cdn.openai.com/.../a-practical-guide-to-building-agents.pdf) | OpenAI's official agent-build guide: Model+Tools+Instructions; single vs multi-agent (manager vs decentralized/handoffs); guardrails | hooks-commands-subagents + prompts-evals | ✗ |
| New tools for building agents | openai.com/index/new-tools-for-building-agents/ | 2025-03 launch: Responses API + Agents SDK + built-in tools | hooks-commands-subagents / mcp (peripheral) | ✗ |

## Surface 5 — openai.github.io (Agents SDK — Python)

| Title | URL | Topic | Component | Cited |
|---|---|---|---|---|
| Agents SDK overview | /openai-agents-python/ | Agents·Handoffs·Guardrails·Sessions·Runner·Tracing | hooks-commands-subagents | ✓ |
| Handoffs | /openai-agents-python/handoffs/ | delegate-to-agent-as-tool; input_filter | hooks-commands-subagents | ✓ |
| Sessions | /openai-agents-python/sessions/ | SQLiteSession; compaction session | plugins-marketplace-memory | ✓ |
| MCP | /openai-agents-python/mcp/ | consume MCP via MCPServerStdio/StreamableHttp/Sse | mcp | ✓ |
| Tools | /openai-agents-python/tools/ | function-tool auto-schema; hosted tools | mcp/prompts-evals (corroborates) | ✗ |
| Guardrails | /openai-agents-python/guardrails/ | input/output guardrails run in parallel; fail-fast | hooks-commands-subagents (corroborates hook-as-guardrail) | ✗ |
| Tracing | /openai-agents-python/tracing/ | built-in trace of LLM/tool/handoff/guardrail events | prompts-evals (corroborates trace-grading) | ✗ |
| Running agents | /openai-agents-python/running_agents/ | runner loop, max_turns | hooks-commands-subagents (corroborates) | ✗ |
