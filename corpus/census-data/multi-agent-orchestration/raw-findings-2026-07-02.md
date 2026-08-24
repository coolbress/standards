# Raw findings — multi-agent orchestration + CC/Codex dispatch parity (2026-07-02)

Raw research originals behind
`aspects/27-ai-harness-archetype/multi-agent-orchestration-standard.md`.
Two web-research passes (deposit-rule: raw here, learnings in the aspect sub-doc).

## Pass 1 — Codex vs Claude Code dispatch capability (web-verified)

**Bottom line:** As of **2026-06**, Codex DOES have subagents/delegation (Codex CLI **v0.142.0, 2026-06-22**) — this corrects a stale prior that "Codex has no in-session dispatch."

Codex:
- Explicit-spawn subagents: built-ins `default`/`worker`/`explorer` + custom via `name`/`description`/`developer_instructions` (+ optional `model`/`sandbox`/`tool`). Parent waits for all results, then consolidates.
- **Explicit-request-only by default**; proactive delegation is an opt-in thread/turn-level setting (disabled | explicit-request-only | proactive).
- Parallel execution: "spawns specialized agents in parallel and collects results in one response" (batch CSV, multi-aspect security+perf+testing).
- **`codex mcp-server`** exposes Codex itself as an MCP server (tools `codex()` create-session, `codex-reply()` continue) → external orchestrators call Codex as a subprocess; integrates with OpenAI Agents-SDK handoffs.
- Customization surface = `developer_instructions` (no AGENTS.md-style declarative subagent file).

Claude Code:
- Proactive **+** explicit delegation (decides from subagent `description`↔task match).
- Each subagent = **isolated fresh context window; only final message returns**; parent conversation history not shared (unless a "fork").
- Definitions: built-in (Explore/Plan/general-purpose) + custom `.claude/agents/*.md` (frontmatter `description`/`prompt`/`tools`/`model`/`permissionMode`/`hooks`/`skills`/`memory`/`isolation`/`background`/`maxTurns`).
- Parallel (fg/bg); **nesting up to 5 levels** (v2.1.172); per-subagent `model` override.
- Not itself an MCP server; Agent-SDK for programmatic invocation.

Sources: developers.openai.com/codex/changelog · /codex/subagents · /codex/guides/agents-sdk · code.claude.com/docs/en/sub-agents · /agent-sdk/subagents.
Caveat: single web-research pass; specific Codex version/date figures should be re-verified if load-bearing.

## Pass 2 — industry multi-agent orchestration (see aspect sub-doc for the distilled tables)

Key primary sources captured:
- **Anthropic multi-agent research system** (2025-06-13): orchestrator-worker (Opus lead + Sonnet workers); ~4× (single) / ~15× (multi) chat tokens; tokens explain 80% of perf variance; +90.2% vs single-agent Opus on internal research eval; wins on breadth-first/parallel/large-context, loses on shared-context/dependency/most-coding. https://www.anthropic.com/engineering/built-multi-agent-research-system
- **Cognition — Don't Build Multi-Agents** (2024) + **What's Actually Working** (2025): context fragmentation → conflicting implicit decisions; **single-writer principle**; endorsed = generator-verifier (read-only reviewer, limited context = ~2 more bugs/PR) + cross-frontier routing + hierarchical delegation; "reliability is context engineering". https://cognition.com/blog/dont-build-multi-agents · https://cognition.com/blog/multi-agents-working · https://jxnl.co/writing/2025/09/11/why-cognition-does-not-use-multi-agent-systems/
- **OpenAI Agents SDK / Swarm**: handoffs (control transfer, shared history) vs agents-as-tools (manager retains control, isolated calls); "routines"; warns against premature splitting. https://openai.github.io/openai-agents-python/ · https://cookbook.openai.com/examples/orchestrating_agents · https://github.com/openai/swarm
- **LangGraph**: graph + shared state (blackboard-like); supervisor (control returns, accurate routing) vs swarm (peer handoff, lower latency, harder debug). https://dev.to/focused_dot_io/multi-agent-orchestration-in-langgraph-supervisor-vs-swarm-tradeoffs-and-architecture-1b7e · https://aws.amazon.com/blogs/machine-learning/build-multi-agent-systems-with-langgraph-and-amazon-bedrock/
- **CrewAI**: role-based; process types sequential / hierarchical (manager coordinates, doesn't execute) / consensual. https://docs.crewai.com/en/concepts/tasks · https://github.com/crewAIInc/crewAI
- **AutoGen**: conversable agents; GroupChatManager turn-taking/broadcast; fully-shared transcript (highest coupling). https://microsoft.github.io/autogen/0.2/docs/tutorial/conversation-patterns/
- **Model routing / MoA**: arXiv 2509.07571 (generalized routing) · 2602.16873 (AdaptOrch — composition dominates as capability converges) · 2506.00051 (Expert Orchestration). Production = static role assignment; dynamic per-query routing still mostly research.
