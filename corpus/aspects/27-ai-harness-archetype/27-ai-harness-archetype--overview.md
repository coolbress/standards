---
id: aspect-27-ai-harness-archetype
title: "AI-Harness Archetype"
group: "S — Specialized Archetype"
kind: internal
gated_archetypes: ["ai-harness"]
cross_cutting: false
lifecycle_stages: ["all"]
anchors: ["Anthropic-MCP", "Agent-Skills", "AGENTS.md", "evals-SWE-bench"]
evidence_track: census+lit
status: review-needed
last_updated: "2026-07-05"
sources:
  - "https://modelcontextprotocol.io/specification"
  - "https://agents.md"
  - "https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills"
  - "https://www.swebench.com/"
  - "https://arxiv.org/abs/2310.06770"
claim: "A mature AI-harness ships the full normal-software floor PLUS an additive capability layer — skills/commands/hooks/prompts, an MCP tool/resource surface, a config-schema'd plugin+marketplace manifest, an agent constitution, examples, and templates — version-controlled, eval-gated, and packaged for cross-host reuse."
maps_from: ["census-data/harness-census", "docs/adr"]
census_todo: ""
---

> **Standard (claim):** A mature AI-harness ships the full normal-software floor **plus** an *additive capability layer* — skills · commands · hooks · prompts · an MCP tool/resource surface · a config-schema'd plugin+marketplace manifest · an agent constitution · examples · templates — version-controlled, eval-gated, and packaged for cross-host reuse.
> **Evidence:** census+lit (200-repo + 36-canonical harness census; MCP/Agent-Skills/AGENTS.md/SWE-bench standards) · **Confidence:** high · **Kind:** internal / gated[ai-harness] · **Stage:** all

**Seed sub-aspects:** `agent orchestration (planner / impl / review)` · `prompt engineering + versioning` · `evals / eval-harness` · `MCP tool / resource design` · `skill / hook packaging + marketplace` · `context / memory management` · `cross-host adapters` · `prompt-injection / tool-sandbox security`

## What professional engineers do

The defining move: an AI-harness is **a normal software project + an extension layer**. The floor (README/LICENSE/CI/tests/manifest/lockfile) is non-negotiable and identical to any application archetype; the harness identity is the *additive* capability layer. Treat the two as orthogonal — never let the novelty of the layer excuse a missing floor.

- **Agent orchestration (planner / impl / review).** Decompose work into a planner → implementer → reviewer loop rather than one mega-prompt; isolate each role's context. Canonical harnesses (codex, opencode, goose, claude-flow, crewai) expose this as `commands/` (slash-command entry points, canon 50%) over a shared core. Each role runs in a bounded context with explicit handoff artifacts (a plan file, a diff, a review verdict) so failures are localizable. [census][inferred]
- **Prompt engineering + versioning.** Prompts are **source code**: stored in `prompts/` (canon 67%), reviewed in PRs, diffed, and pinned to a model id — not pasted into chat. Use progressive disclosure (load instructions only when relevant) so the system prompt stays small. [lit][census]
- **Evals / eval-harness.** Gate behavior with a reproducible eval suite, not vibes. SWE-bench is the field-standard benchmark for agentic code edits (real GitHub issue→patch, run the repo's own tests as the oracle). Mature harnesses keep tests at near-100% and wire an eval/CI gate so prompt or tool changes can't silently regress. [lit][census]
- **MCP tool / resource design.** Expose capabilities through the **Model Context Protocol** — a JSON-RPC 2.0, capability-negotiated surface of **Tools** (model-callable functions), **Resources** (context/data), and **Prompts** (templated workflows). MCP is the LSP-for-AI: write the integration once, every host consumes it. Design tools with untrusted-by-default annotations and explicit user-consent gates. [lit][census]
- **Skill / hook packaging + marketplace.** Package reusable behavior as **Agent Skills** — `SKILL.md` (YAML frontmatter `name`/`description` preloaded; body + bundled files loaded on demand) — plus `hooks/` (lifecycle event handlers, canon 72%) and a **plugin + marketplace/registry manifest** (canon 64%) so third parties can author and distribute extensions. [lit][census]
- **Context / memory management.** Progressive disclosure + a persistent agent constitution (`CLAUDE.md`/`AGENTS.md`, canon 75%) carry durable conventions; per-run context stays minimal. Memory is explicit files, not implicit chat state. [lit][census]
- **Cross-host adapters.** Avoid lock-in to a single host's panel/config API by keeping a shared core and projecting it into per-host adapters; a config/manifest **JSON Schema** (canon 64%) makes the contract machine-checkable across hosts. **The schema must be CI-VALIDATED, not just present** (ADR-0014 evidence≠presence): wire a test that validates every shipped manifest (`marketplace.json` / per-host `plugin.json` / `SKILL.md` frontmatter) against the schema — a **`vitest` test** (a few `expect` assertions on required keys + that plugin `source` paths resolve) is the minimal-viable; **`ajv`** + the JSON Schema is the fuller form when the manifest grows. Mirror the executable module-boundary test (`tests/architecture.test.ts`) — assert the contract, don't document it. A manifest that only `claude plugin validate`s locally is not CI-enforced. [census][inferred][added 2026-06-27 — audit gap fill]
- **Prompt-injection / tool-sandbox security.** Tools = arbitrary code execution: treat tool descriptions/annotations as untrusted, require explicit consent before tool invocation and before exposing user data to a server, and sandbox execution. This is a first-class MCP principle, not an afterthought. [lit]

## Evidence (lit + census)

- [lit] **MCP** standardizes LLM↔tool/data integration over JSON-RPC 2.0 with Tools/Resources/Prompts and explicit user-consent + tool-safety principles (spec rev 2025-11-25). https://modelcontextprotocol.io/specification
- [lit] **Agent Skills** = "organized folders of instructions, scripts, and resources that agents discover and load dynamically," packaged as `SKILL.md` with progressive disclosure (metadata → body → bundled files). https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- [lit] **AGENTS.md** = standardized agent-instruction file (build/test/conventions), adopted by **60,000+** open-source projects. https://agents.md
- [lit] **SWE-bench** = field-standard agentic-coding eval: real GitHub issue → patch, repo's own tests as oracle. https://www.swebench.com/ · https://arxiv.org/abs/2310.06770
- [census] **Stack mix (top-200):** TS 69 · Python 54 · JS 19 · Go 14 · Rust 12 → TS+JS ≈ 44%, Python 27% (gingoa's TS/Node = the plurality).
- [census] **Floor confirmed (canonical-36):** README/LICENSE/.gitignore/CI 100% · tests 92% · pkg manifest 72% (100% of APP harnesses) · committed lockfile 56% (below census norm — gingoa's commit-it call is a deliberate [lit] choice).
- [census] **Capability layer (canonical-36):** examples/ 78% · agent constitution 75% · hooks/ 72% · skills/ 67% · prompts/ 67% · config JSON Schema 64% · mcp config 64% · marketplace/registry 64% · templates/ 56% · slash-commands 50% · plugins/ 42%.
- [census] **Bimodal split:** 200 repos = 142 application + 58 content; canonical 36 = 26 application + 10 content. Content harnesses = manifest 0% / lockfile 0% (markdown+manifest, not built software).
- [census] **Agent-constitution file = rising, tooling-concentrated convention (N=6,582 governance-floor, star floor 29, archetype-stratified):** at repo root **AGENTS.md 13% · CLAUDE.md 11%** overall, but strongly monorepo/tooling-skewed — AGENTS.md 10%→**42% in monorepos** / 30% in cli-tooling; CLAUDE.md 9%→35% mono / 26% cli. This governance-FLOOR census detects the root files (distinct from the canonical-36 harness-capability census's `constitution 75%`): the agent-instructions file has crossed from novelty into an *emerging norm* among developer-tooling/monorepo projects — a rising, context-concentrated convention, not yet a universal floor, consistent with shipping a generic constitution as an above-census senior default. `census-data/census-governance-floor/` (2026-07-05).

## Archetype variations

This aspect is **gated to `ai-harness`** — the 8th archetype, an L2′ capability module layered atop the L0 software floor (gingoa's ADR-0009). It does not activate for the other 7 archetypes; a normal library/cli/web-app ships the floor only. Within the harness archetype it is **bimodal**:

- **Application harness** (codex, cline, opencode, goose…): full software floor **+** capability layer. The agent/CLI is real software — all four build/test/lint/typecheck gates apply.
- **Content harness** (skill/plugin/prompt packs): capability layer with a *lighter* floor — manifest 0%, lockfile 0%, CI ~59%, tests ~45%. The floor gate relaxes to "valid manifest + schema-valid skills," not "green build."
- Pure agent **libraries** (aider, langchain) have the floor but little of the layer; marquee coding agents light up nearly all of it. The layer's depth scales with how much of an end-user product the harness is.

## Tradeoffs / what's ruled out

- **Ruled out: layer-without-floor.** Shipping skills/prompts while skipping CI/tests/lockfile fails the min-dimension bar. The census shows mature application harnesses do *both* (floor at ~100% canonical); the layer is additive, never a substitute.
- **Ruled out: prompts-as-chat-state.** Unversioned, unreviewed prompts pasted into a session are non-reproducible and uneval-able — they violate prompt-as-source.
- **Tradeoff: open marketplace vs. quality floor.** A fully-open extension ecosystem maximizes breadth but admits low-quality listings; a closed core preserves quality but can't scale breadth. Resolved (ADR-0010) via an **open marketplace + curation-review gate** (App-Store model).
- **Tradeoff: host-native panel vs. cross-host neutrality.** A single-host UI/API is cheaper but locks in; a shared-core + per-host-adapter (+ MCP surface) costs more authoring but preserves breadth (ADR-0011 builds the GUI as a local web app over MCP).
- **Tradeoff: MCP power vs. attack surface.** Tools are arbitrary code execution; the consent/sandbox/untrusted-annotation discipline is mandatory overhead, not optional.

## Sources

- MCP specification (rev 2025-11-25) — https://modelcontextprotocol.io/specification
- Agent Skills (Anthropic engineering) — https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- AGENTS.md — https://agents.md
- SWE-bench — https://www.swebench.com/ · https://arxiv.org/abs/2310.06770
- gingoa harness census — `census-data/harness-census/SUMMARY.md`
- gingoa ADR-0009 (AI-harness archetype), ADR-0010 (open marketplace), ADR-0011 (GUI over MCP) — `docs/adr/`

## Sub-documents
- **호스트 동작 1차 실측 5건** (2026-08 · `*--measured-2026-08.md`) — [`hook-output-surfaces`](hook-output-surfaces--measured-2026-08.md) · [`user-channel-rendering`](user-channel-rendering--measured-2026-08.md) · [`pretool-ask-exit-codes`](pretool-ask-exit-codes--measured-2026-08.md) · [`approval-attribution-channels`](approval-attribution-channels--measured-2026-08.md) · [`stop-event-rendering`](stop-event-rendering--measured-2026-08.md). **공식 문서가 틀리게 적은 항목을 실행으로 뒤집은 기록을 포함한다** — `corpus/methods/evidence-durability--grading-model.md` §0이 이 코퍼스의 존재 이유로 인용하는 사례다.
- [`host-component-ecosystem--facts-2026-08.md`](host-component-ecosystem--facts-2026-08.md) — *research-log (ko)* — 2026-08-08 호스트 표면·플러그인 규격·Skills·마켓플레이스·생태계 보안 지형 최신화. `corpus/methods/evidence-durability--grading-model.md` §3의 🟡 항목이 인용하는 원문.
- [`claude-code-agent-surface--facts-2026-08.md`](claude-code-agent-surface--facts-2026-08.md) — *research-log (ko)* — 2026-08 호스트 표면 갱신: 서브에이전트 중첩 **기본 3단**(기존 기술 "5단" 정정)·동시 최대 20·`initialPrompt`·컨텍스트 격리 포함/제외 전수·MCP 등록과 `.mcp.json` 승인 제약. 외부 모델 경로는 MCP 또는 셸아웃 둘뿐임을 확정. 2026-08 모델 지형은 2차 출처 부록으로 격리.
- [`agent-threat-model.md`](agent-threat-model.md) — *reference* — **current verified integrated threat map**
  across prompt injection, authority, identity/credential, filesystem, egress, durable state, production,
  approvals, supply chain, cost, and false completion; defines system-enforced invariants and red-team cases.
- [`harness-control-plane-standard.md`](harness-control-plane-standard.md) — *reference* — **current verified
  component map** across control, capability, execution, state/context, assurance, and distribution; adds the
  previously underrepresented approval, isolation, recovery, run-state, observability, lifecycle, and rollback
  surfaces. `[lit]` current OpenAI/Codex, MCP, Agent Skills, and Anthropic first-party sources.
- [`host-config-schemas.md`](host-config-schemas.md) — *evidence* — empirically-verified cross-host adapter config schemas (Claude Code `settings.json` marketplace/plugin keys; Codex `config.toml` `[marketplaces.*]`, verified vs codex-cli 0.125.0) — concrete grounding for the cross-host-adapters sub-aspect.
- [`skill-authoring-standard.md`](skill-authoring-standard.md) — *reference* — frontier-AI **Agent Skills** build standard: `SKILL.md` frontmatter contract (name/description rules, host extensions) · progressive disclosure (metadata→body→bundled) · &lt;500-line sizing · when-to-use vs command/subagent/MCP · eval-driven authoring · untrusted-code security — what gingoa's scaffold feature must emit. `[lit]` Anthropic skills posts + agentskills.io open spec (Codex builds on it) + OSS.
- [`mcp-server-standard.md`](mcp-server-standard.md) — *reference* — frontier-AI **MCP** build standard (spec rev 2025-11-25): Tools/Resources/Prompts shapes + annotation defaults (un-annotated = write/destructive) · transports (stdio · Streamable-HTTP) · capability negotiation/lifecycle · 4-principle security model (consent + tool-safety, token-passthrough/confused-deputy/SSRF) · Anthropic ACI tool-design craft (few workflow tools · token-efficient · code-execution-with-MCP 98.7% token cut) · SDK conventions + Inspector testing · OpenAI Apps-SDK convergence (ChatGPT app = MCP server). `[lit]` MCP spec + Anthropic eng + OpenAI Apps/Agents-SDK + OSS servers.
- [`hooks-commands-subagents-standard.md`](hooks-commands-subagents-standard.md) — *reference* — the orchestration/lifecycle layer: **Hooks** (10-event core · `settings.json` matcher shape · JSON-stdin + exit-code 0/2/other contract · arbitrary-shell security) · **Slash-commands** (now *merged into Skills* — a command = a skill with `disable-model-invocation`) · **Subagents** (`.claude/agents/*.md` · context isolation · Anthropic multi-agent eval +90% / ~15× tokens) + a **when-to-use decision matrix** (hook/command/subagent/skill/MCP/constitution). `[lit]` Claude Code docs + Anthropic multi-agent post + OpenAI Agents-SDK (cross-vendor *converged*).
- [`plugin-marketplace-memory-standard.md`](plugin-marketplace-memory-standard.md) — *reference* — the packaging + memory layer: **Plugins** (`.claude-plugin/plugin.json`, `name`-only-required, object `author`, root-level component auto-discovery, the "nothing-but-plugin.json-in-`.claude-plugin/`" footgun, `${CLAUDE_PLUGIN_ROOT}`) · **Marketplace** (`marketplace.json` `source` discriminator table · no central registry · open-marketplace + review-gate curation · `strictKnownMarketplaces`) · **Memory** (the "memory = explicit files not chat state" thesis: CLAUDE.md/AGENTS.md hierarchy + `@`-imports ≤4 hops; the generated layer = Claude Code auto-memory `MEMORY.md` + API memory-tool over `/memories` + Codex `~/.codex/memories/`; context-engineering principles + context-editing 39%/29%/84%) · path-traversal + memory-poisoning security. `[lit]` Claude Code plugin/marketplace/memory docs + Anthropic context-engineering posts + OpenAI Codex Memories/Conversations.
- [`prompts-and-evals-standard.md`](prompts-and-evals-standard.md) — *reference* — the prompt-authoring + eval-harness layer: **Prompts** (the technique ladder — clear&direct · 3–5 examples · CoT/let-think · XML structure · system/role · queries-at-end +30%; Claude 4.x specifics — **prefill deprecated** (400 on 4.6+) · adaptive `effort` thinking · over-trigger fix · parallel-tool-calls; GPT-5 `reasoning_effort`+minimal · preambles · contradiction-trap; **prompts-as-source-code** — OpenAI deprecating managed `v1/prompts` (shutdown 2026-11-30) → keep prompts in a versioned `prompts/` module) · **Evals** (Anthropic 3 eval-design principles "volume over quality" · 3 grader classes + LLM-judge "encourage reasoning then discard" · 20–50 real-failure tasks · pass@k/pass^k · "grade the output not the path" · 5 statistical recs — clustered SEs/paired-diffs/power; OpenAI grader menu `string_check`/`text_similarity`/`score_model`/`label_model`/`python`/`multigrader` + trace grading) · the prompt↔eval test-and-iterate loop wired as a CI regression gate. `[lit]` Anthropic prompt-eng + eval docs + OpenAI GPT-5/Evals guides (cross-vendor *converged* on prompts-as-source). Connects to aspect-08 (testing) + skill-authoring's eval-driven authoring; gingoa's PRD/EARS acceptance = its first golden eval set.

- [`multi-agent-orchestration-standard.md`](multi-agent-orchestration-standard.md) — *reference* — the orchestration **topology / when-to-dispatch** layer above the component standard: named topologies (orchestrator-worker · supervisor · handoff/swarm · group-chat · hierarchical · **generator-verifier** · blackboard · model-routing/MoA) · the **decision rule** (dispatch only for high-value, read-heavy, decomposable work) · **Cognition's single-writer principle** (parallel workers contribute *intelligence* not *actions*; writes stay single-threaded) · the **~15× token / +90.2%** Anthropic reality · **heterogeneous model routing** (large-lead/small-workers; MoA arXiv) · **CC↔Codex dispatch parity VERIFIED mid-2026** (Codex added subagents 2026-06 — corrects the stale "Codex has no dispatch" prior). Grounds ADR-0013's `S(lead→sub-agent)`; the adversarial reviewer = generator-verifier. `[lit]` Anthropic eng + Cognition + OpenAI/Claude Code docs + MoA arXiv.

- [`facts-2026-08-steering-mechanisms.md`](facts-2026-08-steering-mechanisms.md) — *research-log (ko)* — 2026-08 facts-only pass: 조향 표면의 공식 문서 기록 — Claude Code(CLAUDE.md advisory · PreToolUse exit-2 차단 · permission deny-우선), OpenAI Model Spec 지시 위계, MCP tool 실행의 advisory 성격, Cursor rules 우선순위; Codex/Gemini 표면은 예산 소진 INCONCLUSIVE (기존 `host-config-schemas.md`가 Codex config를 부분 커버).
- [`facts-2026-08-instruction-adherence.md`](facts-2026-08-instruction-adherence.md) — *research-log (ko)* — 2026-08 facts-only pass: 지시 준수 실증 — IFEval, 지시 개수별 붕괴(N=10 58.8–93.8% → N=80 ~0%, arXiv), Lost-in-the-Middle U-곡선, 맥락 한계 근처 거부율 79–90%(환각 아님), METR 장기작업 상태 관리 붕괴, Anthropic 공식 저하 입장; **미측정 명시**: 시스템프롬프트 크기 임계·스킬 발화 신뢰율·단계 이탈률.
- [`facts-2026-08-compliance-verification.md`](facts-2026-08-compliance-verification.md) — *research-log (ko)* — 2026-08 facts-only pass: 준수 검증 방법 — OpenAI Evals grader 4종, τ-bench pass^k·policy-pass, LLM-judge 편향 3종(위치/장황/자기선호)과 보정, Claude Code Stop/PreToolUse 결정적 게이트, OTel GenAI 시맨틱 컨벤션 span; **표준 부재 명시**: 스킬 발화 준수 지표·크로스 프레임워크 준수 감사.

<!-- frontier-AI component build-standards (aspect-27 augmentation, 2026-06-27) — COMPLETE (5/5): skill · mcp-server · hooks-commands-subagents · plugin-marketplace-memory · prompts-and-evals. -->
<!-- orchestration topology/strategy layer added 2026-07-02: multi-agent-orchestration-standard (complements hooks-commands-subagents at the compose-many/when-to-dispatch level). -->
