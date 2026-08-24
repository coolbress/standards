# Anthropic — publication-surface enumeration (frontier-AI components coverage census)

**Run date:** 2026-06-27
**Purpose:** Phase A coverage census — enumerate Anthropic's official publication surfaces relevant to the
5 component build-standards (skills · MCP · hooks/commands/subagents · plugins/marketplace/memory · prompts/evals),
to diff against what those sub-docs already cite. See `coverage-report.md` for the diff + gap list.
**Append-only** (research-deposit-rule). Companion: `openai.md`.

## ENUMERATION LIMITS (be honest — the census's value is its calibration)

- **`anthropic.com/engineering`** — **fully walked.** The listing page rendered a complete, non-paginated
  chronological archive of **25 posts** (Sep-2024 → Apr-2026). High confidence this is the full engineering archive
  at capture. (One title redirect: `engineering/claude-code-best-practices` → `code.claude.com/docs/en/best-practices`;
  `engineering/building-agents-with-the-claude-agent-sdk` → `claude.com/blog/...`.)
- **`anthropic.com/research`** — **PARTIALLY walked.** The index is JS-rendered with a "See more" control I could
  not paginate via fetch; I captured the featured set + the first listing band (~13 items) and supplemented with
  targeted web/arXiv search. The research surface is therefore **enumerated by topic-search, not exhaustively** —
  this is the census's known-weakest axis (see coverage-report PAPERS axis). I am confident about the
  *build-standard-relevant* research items (evals), less confident the list of *all* recent papers is complete.
- **`anthropic.com/news`** — **NOT walked as an index** (JS-rendered, no stable paginated archive via fetch);
  enumerated by targeted search for the agent/tooling/model-release announcements that map to the 5 components.
  Model-release posts (Sonnet/Opus 4.x) were sampled, not exhaustively listed, since most are not build-standard
  load-bearing (the prompting-relevant deltas live in the docs, already cited).
- **`docs.claude.com` / `platform.claude.com` / `code.claude.com` / `modelcontextprotocol.io`** — these are the
  primary spec/docs surfaces already cited heavily by the sub-docs; here I enumerated only the **net-new
  build-standard pages** the sub-docs missed (best-practices, features-overview, MCP changelog), not the full doc
  tree (which the sub-docs already cover page-by-page).

---

## Surface 1 — anthropic.com/engineering (FULL archive, 25 posts)

`✓ = already cited in a sub-doc · ✗ = not cited`

| # | Title | URL | Date | Topic | Component | Cited |
|---|---|---|---|---|---|---|
| 1 | How we contain Claude across products | /engineering/how-we-contain-claude | 2026 | agent containment/safety across products | not-relevant: product-safety, not a component build rule | — |
| 2 | An update on recent Claude Code quality reports | /engineering/april-23-postmortem | 2026-04-23 | CC quality postmortem | not-relevant: incident report | — |
| 3 | Scaling Managed Agents: Decoupling the brain from the hands | /engineering/managed-agents | 2026-04-08 | managed-agent / multi-agent architecture | hooks-commands-subagents (peripheral) | ✗ |
| 4 | How we built Claude Code auto mode | /engineering/claude-code-auto-mode | 2026-03-25 | CC permission/auto-mode safety | not-relevant: host permission UX, not a scaffolded component | — |
| 5 | Harness design for long-running application development | /engineering/harness-design-long-running-apps | 2026-03-24 | agent harness design patterns | hooks-commands-subagents / plugins-memory (context) | ✗ |
| 6 | Eval awareness in Claude Opus 4.6's BrowseComp performance | /engineering/eval-awareness-browsecomp | 2026-03-06 | eval methodology / eval-awareness | prompts-evals (peripheral) | ✗ |
| 7 | Quantifying infrastructure noise in agentic coding evals | /engineering/infrastructure-noise | 2026-02-05 | eval noise/variance in coding evals | prompts-evals (corroborates stats axis) | ✗ |
| 8 | Building a C compiler with a team of parallel Claudes | /engineering/building-c-compiler | 2026-02-05 | multi-agent parallel collaboration | hooks-commands-subagents (corroborates) | ✗ |
| 9 | Designing AI-resistant technical evaluations | /engineering/AI-resistant-technical-evaluations | 2026-01-21 | robust eval design | prompts-evals (peripheral) | ✗ |
| 10 | Demystifying evals for AI agents | /engineering/demystifying-evals-for-ai-agents | 2026-01-09 | agent eval frameworks | prompts-evals | ✓ |
| 11 | Effective harnesses for long-running agents | /engineering/effective-harnesses-for-long-running-agents | 2025-11-26 | agent runtime / long-running harness | hooks-commands-subagents / plugins-memory | ✗ |
| 12 | Introducing advanced tool use on the Claude Developer Platform | /engineering/advanced-tool-use | 2025-11-24 | advanced tool use (tool-use API surface) | mcp / prompts-evals (tool design) | ✗ |
| 13 | Code execution with MCP: Building more efficient agents | /engineering/code-execution-with-mcp | 2025-11-04 | MCP tool-loading at scale (98.7% reduction) | mcp | ✓ |
| 14 | Beyond permission prompts: making Claude Code more secure and autonomous | /engineering/claude-code-sandboxing | 2025-10-20 | CC sandboxing/security | not-relevant: host security UX (touched by hooks security §, but no new rule) | — |
| 15 | Equipping agents for the real world with Agent Skills | /engineering/equipping-agents-for-the-real-world-with-agent-skills | 2025-10-16 | Agent Skills framework | skills | ✓ |
| 16 | Effective context engineering for AI agents | /engineering/effective-context-engineering-for-ai-agents | 2025-09-29 | context engineering discipline | plugins-marketplace-memory | ✓ |
| 17 | A postmortem of three recent issues | /engineering/a-postmortem-of-three-recent-issues | 2025-09-17 | incident analysis | not-relevant: incident report | — |
| 18 | Writing effective tools for agents — with agents | /engineering/writing-tools-for-agents | 2025-09-11 | tool/ACI design | mcp | ✓ |
| 19 | Desktop Extensions: One-click MCP server installation | /engineering/desktop-extensions | 2025-06-26 | MCP packaging/distribution (.dxt) | mcp / plugins (distribution) | ✗ |
| 20 | How we built our multi-agent research system | /engineering/multi-agent-research-system | 2025-06-13 | orchestrator-worker, +90.2%, token econ | hooks-commands-subagents | ✓ |
| 21 | Claude Code: Best practices for agentic coding | /engineering/claude-code-best-practices → code.claude.com/docs/en/best-practices | 2025-04-18 | CC workflows: CLAUDE.md, skills, subagents, hooks, plugins, Stop-hook, Writer/Reviewer | ALL 5 (cross-cutting) | ✗ |
| 22 | The "think" tool | /engineering/claude-think-tool | 2025-03-20 | think-tool for complex tool use | prompts-evals / mcp (peripheral) | ✗ |
| 23 | Raising the bar on SWE-bench Verified | /engineering/swe-bench-sonnet | 2025-01-06 | coding-agent benchmark | prompts-evals (peripheral) | ✗ |
| 24 | Building effective agents | /engineering/building-effective-agents | 2024-12-19 | agent design patterns: prompt-chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer; workflows-vs-agents; ACI | hooks-commands-subagents + prompts-evals | ✗ |
| 25 | Introducing Contextual Retrieval | /engineering/contextual-retrieval | 2024-09-19 | retrieval/context enhancement (RAG) | not-relevant: RAG technique, not a harness component the 5 cover | — |

**Plus (engineering, redirected off the /engineering index):**

| Title | URL (canonical) | Date | Topic | Component | Cited |
|---|---|---|---|---|---|
| Building agents with the Claude Agent SDK | claude.com/blog/building-agents-with-the-claude-agent-sdk | 2025-09-29 | agent feedback loop (gather context→act→verify), subagents, harness design, compaction, tool design | hooks-commands-subagents + plugins-memory + prompts-evals | ✗ |

## Surface 2 — anthropic.com/news (targeted; agent/tooling/model-release only)

| Title | URL | Date | Topic | Component | Cited |
|---|---|---|---|---|---|
| Introducing Agent Skills | /news/skills | 2025-10-16 | Skills launch (across Claude.ai/Code/SDK/platform) | skills | ✗ (engineering twin ✓) |
| Managing context on the Claude Developer Platform | /news/context-management (= claude.com/blog/context-management) | 2025 | memory tool + context editing; 39/29/84% numbers | plugins-marketplace-memory | ✓ (cited as claude.com/blog/context-management) |
| Introducing the Model Context Protocol | /news/model-context-protocol | 2024-11-25 | MCP announcement (N×M, LSP-for-AI) | mcp | ✓ |
| Introducing Claude Sonnet 4.5 / Opus 4.x releases | /news/claude-sonnet-4-5 (+ siblings) | 2025–2026 | model releases | not-relevant: prompting deltas captured in docs (already cited); release notes not a build rule | — |
| Enabling Claude Code to work more autonomously | /news/enabling-claude-code-to-work-more-autonomously | 2025 | CC autonomy | not-relevant: host UX, no new component rule | — |

## Surface 3 — anthropic.com/research (PARTIAL — see limits; topic-searched)

| Title | URL | Date | Topic | Component | Cited |
|---|---|---|---|---|---|
| A statistical approach to model evals | /research/statistical-approach-to-model-evals (arXiv:2411.00640) | 2024-11 | SEM, clustered SEs, paired-diff, power analysis | prompts-evals | ✓ |
| Agentic coding and persistent returns to expertise | /research/claude-code-expertise | 2026-06-16 | economic study of ~400k CC sessions | not-relevant: economic research, not a build rule | — |
| Teaching Claude why | /research/teaching-claude-why | 2026-05-08 | alignment / agentic-misalignment reduction | not-relevant: alignment research | — |
| Natural Language Autoencoders | /research/natural-language-autoencoders | 2026-05-07 | interpretability | not-relevant: interpretability | — |
| (Constitutional AI / extended-thinking / computer-use papers) | various | 2022–2025 | foundational model behaviour | not-relevant: model-training research, not component build rules | — |

> Build-standard-relevant research is dominated by the **evals** axis (the one paper above + the engineering
> eval posts in Surface 1: demystifying-evals ✓, infrastructure-noise ✗, AI-resistant-evals ✗, eval-awareness ✗).
> No *uncited* pure-research **paper** was found that adds a load-bearing build rule for the 5 components — the
> load-bearing eval guidance lives in the engineering posts + docs, which are enumerated above. See coverage-report.

## Surface 4 — docs / spec (net-new pages the sub-docs missed; not a full re-walk)

| Title | URL | Topic | Component | Cited |
|---|---|---|---|---|
| Best practices for Claude Code | code.claude.com/docs/en/best-practices | CLAUDE.md tuning, skills/subagents/hooks/plugins decision, Stop-hook gate, Writer/Reviewer, /goal, plan-mode | ALL 5 | ✗ |
| Extend Claude Code (features-overview) | code.claude.com/docs/en/features-overview | the canonical "match features to your goal" (skill vs subagent vs hook vs MCP vs plugin) decision matrix | hooks-commands-subagents (decision matrix) | ✗ |
| MCP spec — Key Changes / changelog (2025-11-25) | modelcontextprotocol.io/specification/2025-11-25/changelog | the 2025-11-25 deltas: stderr-for-all-logging, HTTP-403-on-bad-Origin, input-validation-errors-as-tool-exec-errors, JSON-Schema-2020-12 default, tool-name guidance, tasks, icons, elicitation | mcp | ✗ |
| MCP spec — Versioning / older revisions | modelcontextprotocol.io/specification/2025-06-18 (+ 2025-03-26) | prior revisions (back-compat context) | mcp | not-relevant: sub-doc correctly pins to current 2025-11-25 | — |
