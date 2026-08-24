# Coverage report — frontier-AI component build-standards vs official Anthropic + OpenAI publications

**Run date:** 2026-06-27
**Question:** Did the 5 sub-docs (skills · MCP · hooks-commands-subagents · plugins-marketplace-memory ·
prompts-evals) cite the load-bearing official Anthropic + OpenAI publications, or did we miss relevant ones?
**Method:** grep'd all ~71 cited URLs (frontmatter `sources:` + inline + `## Sources`) → the already-covered
set; enumerated the publication surfaces (`anthropic.md`, `openai.md`); diffed. **Phase A only — no sub-doc edits.**

---

## 1. Coverage statistic

Counting only items judged **RELEVANT to one of the 5 component build-standards** (excludes the NOT-RELEVANT list
in §5 — incident postmortems, alignment/interpretability research, model-release notes, RAG, host permission-UX):

- **Relevant items enumerated:** **31**
- **Already cited:** **17** → **~55%**
- **Missing-but-relevant (the gap list):** **14**

By surface, the already-cited 17 are dense exactly where the build rules live: the **MCP spec** (7 pages) + MCP
engineering posts (writing-tools, code-execution) ✓; the **skills** engineering+best-practices+docs ✓; the
**multi-agent** post ✓; **context-engineering** + **memory-tool** + **context-management** ✓; the **prompt + eval +
grader + agent-eval** docs ✓ + the **statistical-evals** paper ✓; and the full **Codex** convergence surface ✓.
The misses cluster in **(a) cross-cutting Claude-Code "how to build/run the harness" guidance** (best-practices,
features-overview, building-effective-agents, agent-SDK post) and **(b) newer/sibling model-prompting + eval-stats
posts** — load-bearing for completeness, but mostly *corroborating or nuance-adding* rather than *rule-overturning*.

---

## 2. GAP TABLE (missing-but-relevant only — not padded)

Priority = how load-bearing for the **build standard**. HIGH = adds/changes a rule or a primary source the standard
leans on · MED = adds a number/nuance/divergence · LOW = corroborates an already-cited rule.

| # | Title | URL | Date | Component (sub-doc) | Prio | What NEW load-bearing fact it adds |
|---|---|---|---|---|---|---|
| 1 | Building effective agents | anthropic.com/engineering/building-effective-agents | 2024-12-19 | hooks-commands-subagents (+ prompts-evals) | **HIGH** | The canonical 5 agent **workflow patterns** (prompt-chaining · routing · parallelization · orchestrator-workers · evaluator-optimizer) + the **"workflows vs agents, use the simplest thing"** rule. The subagent doc cites the *multi-agent research* post but not this foundational pattern taxonomy that the planner→impl→review loop derives from. |
| 2 | Best practices for Claude Code | code.claude.com/docs/en/best-practices | 2025-04-18 | ALL 5 (cross-cutting) | **HIGH** | The primary CC build-practice page: CLAUDE.md tuning table (✅/❌ include), skills-vs-CLAUDE.md, **Stop-hook as a deterministic gate**, Writer/Reviewer + adversarial-review-subagent, /goal evaluator, plan-then-code, `claude -p` headless/fan-out. The standards state many of these but never cite this source. |
| 3 | Extend Claude Code (features-overview) | code.claude.com/docs/en/features-overview | — | hooks-commands-subagents | **HIGH** | The **official "match features to your goal"** decision matrix (skill vs subagent vs hook vs MCP vs plugin) — the *exact* deliverable of hooks-commands-subagents §4. The sub-doc built its matrix without citing the vendor's own. |
| 4 | Building agents with the Claude Agent SDK | claude.com/blog/building-agents-with-the-claude-agent-sdk | 2025-09-29 | hooks-commands-subagents (+ plugins-memory, prompts-evals) | **HIGH** | The **agent feedback loop** standard: *gather context → take action → verify work → repeat*; subagents for parallel context; compaction; tool design. This is the harness-design backbone aspect-27 is about; uncited. |
| 5 | MCP spec — Key Changes (changelog, 2025-11-25) | modelcontextprotocol.io/specification/2025-11-25/changelog | 2025-11-25 | mcp | **MED** | Pins the deltas the standard relies on: **stderr may carry ALL logging** (not just errors), **HTTP 403 on bad Origin**, **input-validation errors → Tool Execution Errors (not Protocol) for self-correction**, **JSON-Schema-2020-12 as default dialect**, tool-name guidance, tasks/icons/elicitation. The sub-doc asserts several of these; the changelog is their provenance. |
| 6 | GPT-5.1 prompting guide | developers.openai.com/cookbook/examples/gpt-5/gpt-5-1_prompting_guide | 2025-11-13 | prompts-evals | **MED** | Updates the cited GPT-5 guide: new **`none` reasoning tier**, sharper **agentic-persistence** prompt ("end-to-end within the turn"), **user-update preambles every 6–8 tool calls**, apply_patch/shell tools. The model-tuning §3 pins to GPT-5; this is the current sibling. |
| 7 | GPT-4.1 prompting guide | cookbook.openai.com/examples/gpt4-1_prompting_guide | 2025-04 | prompts-evals | **MED** | The three **agentic prompt reminders** (persistence · tool-calling · planning) + "use the `tools` field, never inject tool descriptions into the prompt" — a concrete authoring rule absent from §3. |
| 8 | A practical guide to building agents (PDF) | cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf | 2025 | hooks-commands-subagents (+ prompts-evals) | **MED** | OpenAI's official agent-build guide: **Model + Tools + Instructions** decomposition; **single vs multi-agent (manager vs decentralized/handoffs)**; **guardrails**. The cross-vendor twin of "building effective agents"; corroborates+sharpens the orchestration matrix. |
| 9 | Introducing advanced tool use (Claude Developer Platform) | anthropic.com/engineering/advanced-tool-use | 2025-11-24 | mcp (+ prompts-evals) | **MED** | Anthropic's advanced tool-use surface (tool-use API features the ACI guidance now assumes) — adds platform-side nuance to the tool-design rules beyond writing-tools/code-execution. |
| 10 | Effective harnesses for long-running agents | anthropic.com/engineering/effective-harnesses-for-long-running-agents | 2025-11-26 | hooks-commands-subagents / plugins-memory | **MED** | Long-running harness design: durable execution, resume-from-failure, context across a long run — corroborates+extends the subagent reliability ("resume, not restart") and memory persistence rules with a dedicated source. |
| 11 | Harness design for long-running application development | anthropic.com/engineering/harness-design-long-running-apps | 2026-03-24 | plugins-memory / hooks-commands-subagents | LOW | Harness/context patterns for long app builds; corroborates the context-engineering + multi-session memory pattern. |
| 12 | Quantifying infrastructure noise in agentic coding evals | anthropic.com/engineering/infrastructure-noise | 2026-02-05 | prompts-evals | LOW | Empirical eval-variance/noise — corroborates the §6 "put error bars on the number / variance" statistics rule with a concrete agentic-coding example. |
| 13 | Optimize Prompts (cookbook) | cookbook.openai.com/examples/optimize_prompts | — | prompts-evals | LOW | OpenAI's prompt-optimizer (contradiction/format/example fixes via Agents-SDK+Evals) — corroborates §4 authoring-tooling (Anthropic generator/improver twin). |
| 14 | Desktop Extensions: one-click MCP install (.dxt) | anthropic.com/engineering/desktop-extensions | 2025-06-26 | mcp / plugins (distribution) | LOW | MCP-server packaging/distribution as one-click extensions — corroborates the mcp §7 packaging + plugins distribution story with an Anthropic distribution mechanism. |

**Counts:** HIGH = **4** · MED = **6** · LOW = **4** · total **14**.

---

## 3. PAPERS / RESEARCH AXIS (our known-weakest axis — called out)

The audit confirms the weakness is **calibration, not omission of a load-bearing paper**:

- **The one build-standard-load-bearing research paper is already cited:** *A statistical approach to model evals*
  (anthropic.com/research/statistical-approach-to-model-evals, **arXiv:2411.00640**) ✓ — it is the source for the
  prompts-evals §6 statistics rules (SEM, clustered SEs, paired-differences, power analysis).
- **No *uncited* pure-research paper was found that adds a load-bearing build rule** for any of the 5 components.
  The eval/agent guidance that *is* load-bearing lives in **engineering posts + docs**, not standalone papers —
  and those are the gaps (#1, #4, #9, #10, #12), already captured above. So the "papers axis" gap is really an
  "engineering-blog + docs axis" gap.
- **Relevant research found but correctly NOT cited (not-relevant to a build standard):** `claude-code-expertise`
  (economic study of ~400k sessions), `teaching-claude-why` (alignment), `natural-language-autoencoders`
  (interpretability), and the foundational Constitutional-AI / extended-thinking / computer-use papers — these are
  model-behaviour/training research, not component build rules.
- **Calibration caveat:** `anthropic.com/research` is JS-rendered and I could not fully paginate it (see
  `anthropic.md` LIMITS), so I enumerated it by topic-search. I am confident on the **evals** sub-axis (the only
  build-relevant one); I cannot 100% rule out an obscure recent paper, but none surfaced under targeted search for
  agents/tools/eval/context/memory/prompting. The honest statement: **the research-paper axis is sound for the
  build standard, and its weakness is enumeration-completeness of irrelevant papers, not a missed rule.**

---

## 4. (folded into §2 — no separate section)

---

## 5. NOT-RELEVANT (deliberately excluded — auditable, not silent)

| Item | Why excluded |
|---|---|
| how-we-contain-claude · claude-code-sandboxing · claude-code-auto-mode · enabling-claude-code-to-work-more-autonomously | Host permission/containment UX — a real topic, but not a rule for the 5 *scaffolded components* (the skills/MCP security §§ already cover the component-side trust model). |
| april-23-postmortem · a-postmortem-of-three-recent-issues | Incident reports — no build rule. |
| claude-code-expertise · teaching-claude-why · natural-language-autoencoders · Project Deal/Fetch/Glasswing · economic-index | Economic / alignment / interpretability / red-team research — not component build standards. |
| Contextual Retrieval | RAG technique — not one of the 5 components (gingoa scaffolds skills/MCP/hooks/etc., not a RAG pipeline). |
| Sonnet 4.5 / Opus 4.x release notes | The *prompting-relevant* deltas (prefill deprecation, adaptive thinking, over-trigger) are already captured from the **docs** (claude-prompting-best-practices ✓); the release posts add no build rule beyond that. |
| swe-bench-sonnet · eval-awareness-browsecomp · AI-resistant-technical-evaluations · building-c-compiler · managed-agents | Benchmark/eval-methodology + multi-agent demos that *corroborate* without changing a rule; the load-bearing eval+multi-agent sources (demystifying-evals ✓, multi-agent-research-system ✓) are already cited. (infrastructure-noise was kept as LOW #12 because it specifically backs the error-bar rule.) |
| claude-think-tool | The "think" tool is a narrow tool-use technique; the ACI/tool-design rules are already covered by writing-tools ✓. Borderline; excluded as non-load-bearing for the 5 build standards. |
| OpenAI structured-outputs · prompt-caching · building-agents track · Agents-SDK tools/guardrails/tracing/running_agents · prompt_caching 101/201 · new-tools-for-building-agents | OpenAI corroborating docs — the convergence they show is already cited via the primary OpenAI pages (prompt-engineering, agent-evals, apps-sdk, agents-SDK overview/handoffs/sessions/mcp). Kept only #6/#7/#8/#13 from the OpenAI side as genuine rule/number adds. |

---

## 6. VERDICT

**The existing coverage of the *build standard* is sound: every load-bearing standard was cited from a primary
source.** The MCP wire (spec rev 2025-11-25, all primitives + transports + security + SDKs), the Agent-Skills
open-spec + best-practices, the hooks/subagents/commands contracts, the plugin/marketplace manifests, the
memory/context-engineering model, and the prompt-ladder + eval-grader + eval-statistics rules are all anchored to
the authoritative Anthropic/OpenAI/MCP pages — and the cross-vendor convergence is verified against the full Codex
+ Agents-SDK surface. The ~55% relevant-item coverage is **not** a hole in the *rules*; it is missing **secondary
and cross-cutting sources** — and the audit found **zero uncited publication that overturns a stated rule**.

**What Phase B should fold to make it defensibly exhaustive (4 HIGH, then the MEDs):** add the four HIGH sources —
**building-effective-agents** (the workflow-pattern taxonomy under the orchestration matrix), **best-practices**
(the CC build-practice page the standards paraphrase uncited), **features-overview** (the vendor's own
component-decision matrix, which the hooks-commands-subagents §4 matrix should cite), and **building-agents-with-
the-claude-agent-sdk** (the gather→act→verify feedback-loop backbone) — into the relevant sub-docs' `sources:` and
the bodies where each rule already appears. Then fold the MEDs as nuance: the **MCP changelog** (provenance for the
2025-11-25 deltas), the **GPT-5.1 + GPT-4.1 guides** (current/sibling model-tuning in prompts-evals §3), the
**practical-guide-to-building-agents** PDF + **advanced-tool-use** + **effective-harnesses-for-long-running-agents**.
The LOW items are optional corroboration. With the 4 HIGH + 6 MED folded, the 5 sub-docs would cite every
load-bearing official publication on these topics with no rule resting on an uncited source — defensibly exhaustive.

---

## 7. Phase B — folded (2026-06-27)

The 4 HIGH + 6 MED items from §2 were folded as **surgical provenance** (citation added at the rule's existing
appearance + the small specific fact each source adds); no rule was changed. Each URL was **WebFetch-verified**
before citing (the OpenAI PDF #8 binary did not render through WebFetch; its facts were verified via web search of
the official guide). The LOW items (#11–#14) were left as optional corroboration, per the §6 verdict.

| # | Source | Folded into | Where / what was added |
|---|---|---|---|
| 1 | Building effective agents | `hooks-commands-subagents-standard.md` | §3d — the 5 workflow patterns + workflows-vs-agents + "add complexity only when it demonstrably improves outcomes"; the planner→impl→review loop framed as orchestrator-workers + evaluator-optimizer |
| 2 | Best practices for Claude Code | `hooks-commands-subagents-standard.md` | §1c (Stop-hook-as-deterministic-gate + `/goal` evaluator + verification subagent), §5 (Writer/Reviewer + adversarial review + explore→plan→code + `claude -p` fan-out) |
| 3 | Extend Claude Code / features-overview | `hooks-commands-subagents-standard.md` | §4 — cited the vendor's own "match features to your goal" matrix + "put guardrails in hooks" as the official origin our matrix aligns with |
| 4 | Building agents with the Claude Agent SDK | `hooks-commands-subagents-standard.md` | §3b — the gather→act→verify→repeat loop; subagents for parallel context/isolation; compaction |
| 8 | A practical guide to building agents (OpenAI PDF) | `hooks-commands-subagents-standard.md` | §3d — Model + Tools + Instructions; single vs multi-agent (manager vs decentralized/handoffs); guardrails (cross-vendor twin) |
| 10 | Effective harnesses for long-running agents | `hooks-commands-subagents-standard.md` | §3c reliability — resume-not-restart via init.sh + progress log + feature list + git baseline |
| 5 | MCP spec — Key Changes (changelog) | `mcp-server-standard.md` | intro pin + §1 (JSON-Schema-2020-12 default; input-validation→Tool-Execution-Errors) + §5 (stderr-all-logging; HTTP-403-on-bad-Origin) — provenance for the rev-2025-11-25 deltas |
| 9 | Introducing advanced tool use | `mcp-server-standard.md` | §1b — Tool Search Tool + `defer_loading`; programmatic tool calling; tool-use `input_examples` (platform-side complement to the ACI rules) |
| 6 | GPT-5.1 prompting guide | `prompts-and-evals-standard.md` | §3 — new `none` reasoning tier; end-to-end-within-the-turn persistence; update-preamble cadence (6–8 tool calls); apply_patch/shell (current sibling of GPT-5) |
| 7 | GPT-4.1 prompting guide | `prompts-and-evals-standard.md` | §3 — the three agentic reminders (persistence · tool-calling · planning) + "use the API `tools` field, don't inject tool descriptions into the prompt" |

**Files edited:** `hooks-commands-subagents-standard.md` (6 folds), `mcp-server-standard.md` (2), `prompts-and-evals-standard.md` (2). `skill-authoring-standard.md` and `plugin-marketplace-memory-standard.md` received no folds (none assigned in the work-list); `<topic>--overview.md` not touched. All three edited docs keep `last_updated: "2026-06-27"`.

---

## 8. Deterministic enumeration (sitemap + arXiv, 2026-06-27)

**Why this section exists.** Phase A flagged one residual it could not *prove*: `anthropic.com/research` + `/news`
and `openai.com/research` + `/index` are **JS-rendered**, so Phase A enumerated them by topic-search and could
only say "confident, none surfaced" — not "provably none." Phase C closes that by harvesting the **XML sitemaps**
(which render without JS — the JS gate only ever affected the *human* index pages) + the **arXiv API**, then
1:1-classifying the result. Method = `enumerate.sh` (curl + xmllint; in this sandbox curl was permission-blocked, so
the capture was taken via WebFetch on the raw `.xml` URLs — still deterministic XML parsing, not prose reading).
Raw lists deposited alongside: `sitemap-anthropic.txt`, `sitemap-openai.txt`, `sitemap-docs-and-arxiv.txt`, `enumerate.sh`.

### 8.1 Per-surface counts (what the sitemaps mechanically expose)

| Surface | Render | Total URLs | Of which `/research` | `/engineering` | `/news` or `/index` | Notes |
|---|---|---|---|---|---|---|
| **anthropic.com/sitemap.xml** | ✅ FULL (flat sitemap, no JS) | **~460** | **~140** (+ 5 `/research/team/*`) | **25** (+ index) | **~230** `/news/*` | The exact JS-gated `/research` + `/news` surfaces — now fully enumerated. |
| **openai.com/sitemap.xml** | ⚠️ index renders; children SAMPLED by WebFetch (see caveat) | index→34 children | folded into `/index/*` | `/index/*` (eng-tagged) | **~45** `/index/*` captured (union of research/eng/publication/release/api children) | Per-child lists were sampled, not exhaustive, through WebFetch markdown conversion. |
| **developers.openai.com** (`/sitemap-0.xml`) | ✅ FULL | dev-docs + cookbook tree | — | — | — | All agent/eval/prompt/mcp guide pages rendered completely. |
| **code.claude.com/sitemap.xml** | ✅ FULL | ~150 `/docs/en/*` (×11 locales) | — | — | `whats-new/2026-w13..w26` | English doc tree fully enumerated. |
| **platform.claude.com** (= docs.claude.com 301→) | ✅ FULL | full API doc tree | — | — | — | tool-use / skills / mcp / memory pages all present. |
| **modelcontextprotocol.io/sitemap.xml** | ✅ FULL | spec revs + changelogs + ~60 SEPs | — | — | per-rev `/changelog` | rev 2025-11-25 + the SEPs that are its provenance. |

### 8.2 Reconciliation — every research/eng/news/index URL classified

The build-relevant classification universe is the `/research/ /engineering/ /news/ /index/` set + net-new doc/changelog
pages. Product / pricing / legal / careers / company / events / model-release / partnership / funding / hiring URLs are
**not classified individually** — they are trivially not a build rule for the 5 scaffolded components.

- **anthropic.com** non-research aggregate: **~40** product/legal/careers/company/events/policy URLs — not relevant.
- **anthropic.com `/news/*`**: ~230 URLs; **~215** are model-release / partnership / funding / policy / hiring /
  event announcements = not relevant (aggregated); the ~8 build-relevant ones (`/news/skills`,
  `/news/context-management`, `/news/model-context-protocol`, `/news/contextual-retrieval`,
  `/news/enabling-claude-code-to-work-more-autonomously`, `/news/prompt-engineering-for-business-performance`,
  `/news/prompting-long-context`, `/news/donating-the-model-context-protocol...`) were **all already enumerated in
  Phase A** (cited, or in the NOT-RELEVANT list).
- **anthropic.com `/research/*`** (the headline surface): ~140 papers/reports. **The only build-relevant (evals)
  item — `statistical-approach-to-model-evals` (arXiv:2411.00640) — is CITED ✓.** The remaining ~139 are
  interpretability / alignment / economic-index / cyber / model-welfare / circuits research = not a component build
  rule (the whole research surface is now visible, and it is dominated by non-build axes exactly as Phase A judged).
- **openai.com `/index/*`** + dev-docs: every agent/tool/eval/prompt/codex item maps to an already-cited or
  already-enumerated Phase-A entry (see `sitemap-openai.txt` per-line tags); the model-release / customer-story /
  alignment-research items are not relevant.

**Reconciliation result (the build-relevant `/research /eng /news /index` + net-new doc set):**

| Bucket | Count | Meaning |
|---|---|---|
| **CITED** (already in a sub-doc) | matches Phase-A's 17 | every load-bearing rule still rests on a cited primary source |
| **ENUMERATED-IN-PHASE-A** (in anthropic.md / openai.md — cited, gap-table, or NOT-RELEVANT) | the rest of the 31 relevant + the gap-14 | Phase A had already seen them |
| **NET-NEW vs Phase A** (not seen before) | **0 load-bearing** ; a handful of *sibling/doc-twin* URLs (see 8.3) | nothing that overturns or adds a rule |

### 8.3 NET-NEW table (sitemap exposed, not in Phase A's enumeration)

These URLs are discrete pages Phase A did not list as such. **None is build-relevant-and-load-bearing** — each is
either a doc-twin of an already-folded source, a provenance SEP whose *fact* is already in the sub-doc via the
changelog, or a host-runtime/product page outside the 5 scaffolded components. Itemized for auditability (no padding):

| NET-NEW URL | Relevant to the 5? | If yes: prio · sub-doc · what it'd add | If no: reason |
|---|---|---|---|
| `modelcontextprotocol.io/seps/1303-…`, `/1613-…`, `/986-…`, `/1686-…` | N (fact already in) | — | The SEPs are the *provenance* of rev-2025-11-25 rules already folded via the changelog (gap #5). Citing the changelog is the right grain; the SEPs add no new rule. |
| `modelcontextprotocol.io/community/working-groups/skills-over-mcp` | **Y — LOW (WATCH)** | LOW · skills / mcp · a *forward signal* that the skills+MCP boundary may converge upstream | Not yet a rule (working-group, not spec). FLAG for the lead to monitor, not fold. |
| `developers.openai.com/api/docs/guides/secure-mcp-tunnels/` + `platform.claude.com/.../mcp-tunnels/*` | **Y — LOW** | LOW · mcp · self-host/remote-MCP delivery (cross-vendor twins) | Distribution/ops mechanism, not a server-authoring rule; mcp §7 packaging already covers the shape. |
| `developers.openai.com/api/docs/guides/evaluation-best-practices/` + `/evaluation-getting-started/` | **Y — LOW** | LOW · prompts-evals · OpenAI-side eval best-practice corroboration | Corroborates §6/§7; the load-bearing eval rules are already cited (evals/graders/agent-evals + the stats paper). |
| `developers.openai.com/api/docs/guides/prompt-generation/` | **Y — LOW** | LOW · prompts-evals · OpenAI prompt-generation (authoring tooling twin) | Same family as the already-enumerated Optimize-Prompts / prompt-optimizer (LOW #13); no new rule. |
| `developers.openai.com/api/docs/changelog/` | N | — | API changelog index — model/param deltas, not a component build rule. |
| `developers.openai.com/api/docs/guides/agent-builder*` | N | — | No-code visual builder — not a portable-artifact rule for the 5 components. |
| `code.claude.com/docs/en/{agent-teams,agent-view,routines,scheduled-tasks}` | N | — | Host-side orchestration / UI surfaces, not one of the 5 scaffolded components. |
| `code.claude.com/docs/en/{plugin-relevance,plugin-hints,plugin-dependencies,discover-plugins,claude-directory}` | **Y — LOW** | LOW · plugins · plugin relevance/hints/deps + discovery/directory metadata | Refinements to the plugin manifest/distribution story the plugins sub-doc already covers; optional corroboration. |
| `code.claude.com/docs/en/agent-sdk/*`, `platform.claude.com/.../managed-agents/*` | N (doc-twin) | — | Doc twins of the already-folded Agent-SDK blog post (gap #4) / the `/engineering/managed-agents` post; no new rule. |
| `platform.claude.com/.../tool-use/{programmatic-tool-calling,tool-search-tool}` | N (covered) | — | Already folded via advanced-tool-use (gap #9). |
| arXiv third-party hits (Recursive Agent Harnesses, tap, Scaffold-Effects, Containment-Gap, etc.) | N | — | Third-party academic papers that merely *mention* the vendors; not official publications, not rule sources. |

### 8.4 Updated completeness verdict — papers axis now PROVABLE

The deterministic enumeration **confirms Phase A's finding and upgrades it from "confident" to "provable" on the
papers/research axis.** The exact surface Phase A could not paginate — `anthropic.com/research` — rendered
**completely** as XML via the sitemap (~140 research URLs, all now visible), and the only build-load-bearing item on
it (`statistical-approach-to-model-evals`, arXiv:2411.00640) is **cited ✓**; every other research URL is
interpretability / alignment / economic / cyber / model-welfare research that is correctly not a component build
rule. The arXiv backstop surfaced **no missed *official* Anthropic/OpenAI paper** — only third-party academics that
name the vendors. The `/news` surface (also JS-gated for humans) is now fully visible too, and its build-relevant
subset was already enumerated by Phase A with **zero net-new load-bearing items**. **So the papers axis is now
provably (not merely confidently) complete: of the URLs the official sitemaps expose, every build-relevant one is
accounted for — cited or explicitly excluded-with-reason — and 0 net-new load-bearing publications were found.**

**Residual (honest).** Two limits remain, neither affecting the papers-axis proof: (1) **`openai.com`'s per-child
sitemaps were *sampled* through WebFetch's markdown conversion, not rendered exhaustively** (the curl+xmllint path in
`enumerate.sh` would render them in full, but curl was sandbox-blocked here) — so the OpenAI `/index/*` enumeration
is *reconciliation-complete vs Phase A* but not *proven-exhaustive*; this is low-risk because OpenAI is the
cross-vendor check (Claude Code is the primary host) and its load-bearing items live in the dev-docs/cookbook, which
**did** render fully. (2) The one **forward signal** worth watching — `modelcontextprotocol.io/.../skills-over-mcp`
(a working group on skills+MCP convergence) — is FLAGGED for the lead, not folded (it is not yet a spec rule). To
fully discharge residual (1), re-run `enumerate.sh` in an environment where `curl` is permitted.

---

## 9. OpenAI residual CLOSED — full sitemap render via curl (2026-06-27)

Residual §8(1) is now discharged: the lead re-ran `enumerate.sh`'s OpenAI section with `curl` permitted
(sandbox bypass; read-only fetch of public XML). The OpenAI URL set is now **provably exhaustive**, matching the
Anthropic side.

**Full render (vs Phase C's WebFetch-sampled 105):**
- `openai.com/sitemap.xml` = a **sitemap-index of 34 children**, ALL fetched → **1,380 unique `openai.com` URLs**
  (raw: `sitemap-openai.txt`; the prior sample retained as `sitemap-openai.sampled-phaseA.txt`).
- OpenAI files virtually all news/research/announcements under the **`/index/<slug>`** path (967 URLs) — not
  `/research/` (only 7). Build-topic filter (agent·tool·eval·prompt·gpt-N·mcp·memory·reason·function·codex·
  structured-output·responses·realtime·instruct) → **155 candidate `/index/` URLs** (`sitemap-openai-build-relevant.txt`).

**Reconciliation of the 155 build-topic candidates → 0 net-new load-bearing:**
- They are all on the **`/index/` announcement stream** (OpenAI's news/blog/research-announcement + system-card
  path), NOT the `developers.openai.com` / `cookbook.openai.com` / `openai.github.io` doc surfaces where the
  *build rules* live — and those doc surfaces rendered fully and are cited (the GPT-5/5.1/4.1 prompting guides,
  evals/graders docs, Agents-SDK docs, Apps-SDK). The `/index/` posts are **announcement twins** of cited primary docs.
- Buckets: (a) model-release announcements + **system cards** (gpt-5-*, gpt-4o-*, o1/o3) = release/safety, no build
  rule; (b) **research** (instruction-hierarchy, learning-to-reason, process-supervision, emergent-tool-use,
  designing-agents-to-resist-prompt-injection) = model-behaviour research, not a component build rule; (c) **API/agent
  announcements** (structured-outputs, prompt-caching, function-calling, new-tools-and-features-in-the-responses-api,
  new-tools-for-building-agents) — Phase A already classified these as corroborating-via-the-cited-primary-pages.
- **NET-NEW build-relevant = at most LOW (forward-watch), 0 load-bearing:** the Codex agent-harness/loop posts
  (`unrolling-the-codex-agent-loop`, `unlocking-the-codex-harness`), `the-next-evolution-of-the-agents-sdk`, and
  `introducing-agentkit` are **cross-vendor corroboration** of the agent-loop convergence ALREADY folded in Phase B
  (#4 Claude Agent SDK gather→act→verify loop + #8 OpenAI *practical-guide-to-building-agents*). None is a primary
  build-standard doc; none overturns or adds a rule.

**Honest sub-residual (downgraded, low-risk):** OpenAI **bot-blocks its `/index/` article *bodies*** (WebFetch UA →
403; browser-UA curl → empty) — so the announcement posts above were classified by **URL-stream (`/index/` =
announcement, not `/docs/` = build-standard) + topic + the fact their primary-doc equivalents are cited and rendered**,
not by reading each body. This is low-risk: a build *rule* lives in the docs/cookbook (cited + fully rendered), not in
an announcement post. If maximal rigor on bodies is ever wanted, fetch via an authenticated/headless-browser tool.

**Updated verdict (both axes):** Anthropic enumeration = provably exhaustive (§8); OpenAI enumeration = **now
provably exhaustive too** (full 1,380-URL sitemap render). **Net-new load-bearing publications across BOTH companies =
0.** The 5 sub-docs cite every load-bearing official publication on the 5 components; the only un-cited build-relevant
items are LOW corroboration/forward-watch (owner-scoped out) — defensibly exhaustive, papers axis provable, OpenAI
enumeration residual closed.
