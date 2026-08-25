---
id: aspect-27-ai-harness-archetype--multi-agent-orchestration-standard
title: "Multi-agent orchestration — the topology/when-to-dispatch standard (orchestrator-worker, single-writer, model-routing)"
parent: aspect-27-ai-harness-archetype
kind: reference
evidence_track: census+lit
status: review-needed
last_updated: "2026-07-02"
sources:
  - "https://www.anthropic.com/engineering/built-multi-agent-research-system"
  - "https://code.claude.com/docs/en/agent-sdk/subagents"
  - "https://cognition.com/blog/dont-build-multi-agents"
  - "https://cognition.com/blog/multi-agents-working"
  - "https://openai.github.io/openai-agents-python/"
  - "https://developers.openai.com/codex/subagents"
  - "https://developers.openai.com/codex/changelog"
  - "https://arxiv.org/html/2602.16873v1"
  - "https://arxiv.org/html/2509.07571v1"
---

> ⚠️ **2026-08-25 배치 5 재검증 — *"지배적(dominant)"* 은 내려야 한다.** 아래 claim table **MAO-003** 참조:
> 세 출처 중 어느 것도 토폴로지 채택률의 모집단 조사·설문·배포 통계를 제시하지 않고,
> **Cognition 은 정반대를 명시한다** — *"No single approach to building agents has become the standard yet."*
> 아래 문장의 *"dominant"* 는 **관측이 아니라 이 코퍼스의 판단**이다.
>
> **Standard (claim):** ~~The dominant production multi-agent topology is~~ **A widely-described production multi-agent topology is** **orchestrator-worker with context isolation** — a capable lead decomposes a task, dispatches specialized workers in parallel that each run in their **own context window** and return only a condensed result, and the lead synthesizes. It delivers a large quality lift on the right tasks (Anthropic: **+90.2%** on a research eval) at a **~15× token cost**, so it is justified only for **high-value, read-heavy, genuinely-decomposable** work. The hard boundary is **Cognition's single-writer principle**: parallel workers may *contribute intelligence* but **writes stay single-threaded** — parallel writers to shared state produce conflicting *implicit* decisions and incoherent output.
> **Evidence:** lit (Anthropic eng, Cognition, OpenAI/Claude Code docs, MoA arXiv) + the cross-vendor convergence of Claude Code + Codex on the same subagent primitive. **Confidence:** high. **Kind:** reference / gated[ai-harness]. **Complements** [`hooks-commands-subagents-standard.md`](hooks-commands-subagents-standard.md) (how to author *one* subagent) with *how to compose many / when to dispatch at all*.

## Why this sub-doc (vs the component standard)
`hooks-commands-subagents-standard.md` covers the *component* — authoring a single subagent (`.claude/agents/*.md`, context isolation, the when-to-use-a-subagent matrix). This sub-doc is the *strategy* layer above it: the named orchestration **topologies**, the **decision rule** for when an orchestrator + parallel workers actually helps vs hurts, the **token-cost reality**, **heterogeneous model routing**, and the **cross-host (CC/Codex) dispatch parity** as of mid-2026.

## Named topologies (comparison)

| Pattern | Coordination primitive | Context model | Coupling | Parallel? | Representative impl |
|---|---|---|---|---|---|
| **Orchestrator-worker** | lead dispatches + synthesizes | isolated windows, summary return | low | yes | Anthropic Research; Claude Code subagents; OpenAI "agents-as-tools" |
| **Supervisor** | central router, control always returns | shared state or per-call | medium | partial | LangGraph Supervisor |
| **Handoff / swarm** | peer-to-peer control transfer | history passed on handoff | variable | no | OpenAI Agents-SDK handoffs; LangGraph Swarm |
| **Group-chat** | turn-taking broadcast, all see all | fully shared transcript | high | no | AutoGen GroupChat |
| **Hierarchical** | multi-level manager chains | manager sees all; workers bounded | medium | partial | CrewAI hierarchical |
| **Generator-verifier** | write, then **read-only** independent review | reviewer context *intentionally limited* | low (by design) | no | **Cognition's endorsed pattern** |
| **Blackboard** | shared data structure, any agent r/w | fully shared persistent state | high | yes (locks) | LangGraph state |
| **Model-routing / MoA** | orchestrator routes to a specialist *model* | query + result only | very low | yes | Anthropic Opus→Sonnet; per-task model |

## The decision rule (when orchestrator+parallel-workers helps)
**Use it only when ALL hold** (else prefer a single-threaded agent with good context):
1. Task **decomposes into independent sub-problems** that don't need each other's *intermediate* decisions (research: explore A vs B ✅; edit one shared codebase ❌).
2. Sub-problems are **read/analysis-heavy** (gather, review, validate, summarize). **Writing to shared state is the danger zone.**
3. Total information **exceeds one context window**, or sequential traversal is prohibitively slow (multi-agent buys parallelism *and* context capacity).
4. Task value **justifies the ~15× token cost** (Anthropic states this explicitly; not economically rational for cheap tasks).
5. You accept workers make **implicit decisions**; if those can conflict, you need the single-writer constraint or scoping that prevents conflict.

**Do NOT use it when:** tasks share mutable state · the task needs tight real-time coordination ("LLM agents are not yet great at coordinating/delegating in real time" — Anthropic) · a finding from A must reshape B mid-flight (isolation defeats it) · token budget is tight · the task is simple/fast (coordination overhead not repaid).

## The single-writer principle (Cognition — the load-bearing caveat)
Cognition ("Don't Build Multi-Agents", 2024 → "Multi-Agents: What's Actually Working", 2025), from production coding: **"actions carry implicit decisions, and conflicting decisions carry bad results."** Two parallel agents editing shared code each make micro-decisions invisible to the peer → incoherent result (the Flappy-Bird example). Revised rule: **multi-agent works when writes stay single-threaded and extra agents contribute *intelligence*, not *actions*.** Three patterns they endorse in production:
1. **Generator-verifier loop** — a coding agent produces; a **separate read-only reviewer** audits *without* the author's context. Counterintuitively the reviewer's *shorter/limited* context **improves** bug detection by cutting "context rot". Read-only multi-agent. ⚠️ **2026-08-25 정정 (배치 5 · MAO-006)** — 이 문장에 붙어 있던 *"~2 more bugs/PR, 58% severe"* 는 **비교 증분이 아니다.** 원문은 Devin Review 가 *"catches an **average of** 2 bugs per PR, of which roughly 58% are severe"* 라는 **절대값**이고 대조군이 없다. *"더 찾는다"* 를 받치는 것은 이 수치가 아니라 통제실험이다 ([`28 overview`](../28-implementation-process-workflow/28-implementation-process-workflow--overview.md) **IPW-006·008**).
2. **Cross-frontier model routing** — pair e.g. Claude + a GPT-class model as peer specialists (capability optimization, not cost).
3. **Hierarchical delegation** — manager coordinates, children execute bounded scopes, manager synthesizes.
Core principle: **"reliability is context engineering"** — what each agent *knows* matters more than the infrastructure pattern.

## Token / performance reality (Anthropic, 2025-06)
- Single agent ≈ **4×** a chat's tokens; multi-agent ≈ **15×**.
- "Token usage by itself explains **80%** of the [performance] variance"; three factors explain 95%.
- Multi-agent (Opus lead + Sonnet workers) beat single-agent Opus by **+90.2%** on their internal research eval.
- Wins: breadth-first, parallelizable, info-exceeds-one-window, many complex tools. Loses: shared-context / many inter-agent dependencies / most coding (fewer truly parallel subtasks).

## Heterogeneous model routing
- **Production norm = large orchestrator, small workers** (Anthropic: Opus 4 lead, Sonnet 4 workers). Claude Code exposes this via a **per-subagent `model` field**; Codex custom agents take an optional `model`.
- **Mixture-of-Agents (MoA)** formalizes routing per task type: *Towards Generalized Routing* (arXiv 2509.07571, 2025-09); *AdaptOrch* (arXiv 2602.16873, 2026-02) — as frontier-model capability converges, *composition* dominates *model choice*; *Beyond Monoliths / Expert Orchestration* (arXiv 2506.00051).
- ~~**State mid-2026:** production systems use **static role assignment**; **dynamic per-query routing** is still mostly research.~~ ❌ **2026-08-24 재검증으로 삭제** — 배포 통계가 없고, **같은 출처(Cognition)가 동적 교차벤더 라우팅을 *"in production for a meaningful stretch"* 로 돌렸다고 밝힌다** (자기모순). [`28 overview`](../28-implementation-process-workflow/28-implementation-process-workflow--overview.md) **IPW-010**. ⚠️ **이 줄은 2026-08-25 배치 5 에서야 지워졌다** — 배치 2 가 `direction/03` 만 고치고 이 문서를 두었다 (전파 누락).

## Cross-host dispatch parity (CC vs Codex, mid-2026) — VERIFIED, corrects a stale prior
Both hosts now have a first-class subagent/delegation primitive — **this is a change**: Codex added it in **June 2026** (do not assume "Codex has no subagents").

| Dimension | Codex (Codex CLI v0.142.0, 2026-06-22) | Claude Code |
|---|---|---|
| Delegation trigger | **explicit-request-only by default** (proactive is an opt-in thread/turn setting) | proactive **+** explicit |
| Built-ins | `default` / `worker` / `explorer` | Explore / Plan / general-purpose |
| Custom def | `developer_instructions` (+ optional `model`/`sandbox`/`tool`) | markdown + YAML frontmatter (`description`/`prompt`/`tools`/`model`/`hooks`/`skills`/`isolation`…) |
| Context isolation | inherits parent sandbox | **fresh window; only final message returns** |
| Parallel | yes (batch/multi-aspect) | yes (fg/bg) |
| Nesting | not documented | ~~**up to 5 levels** (v2.1.172)~~ → **기본 3단** · 동시 실행 최대 20 (2026-08-24 정정 — [`claude-code-agent-surface--facts-2026-08`](claude-code-agent-surface--facts-2026-08.md) CAS-002) |
| MCP-as-service | **`codex mcp-server`** exposes Codex as an MCP server (`codex()`/`codex-reply()`) → an outer orchestrator can call Codex as a subprocess | not a service (Agent-SDK for programmatic use) |
| Maturity | new (2026-06) | mature |

Sources: [Codex changelog](https://developers.openai.com/codex/changelog) · [Codex subagents](https://developers.openai.com/codex/subagents) · [Codex + Agents SDK](https://developers.openai.com/codex/guides/agents-sdk) · [Claude Code subagents](https://code.claude.com/docs/en/sub-agents) · [Agent-SDK subagents](https://code.claude.com/docs/en/agent-sdk/subagents). *(Codex figures are from a single 2026-07-02 web-research pass — re-verify version/date if a decision is load-bearing on them.)*

## Sources
- Anthropic — How we built our multi-agent research system (2025-06-13) — https://www.anthropic.com/engineering/built-multi-agent-research-system
- Claude Code Agent-SDK subagents — https://code.claude.com/docs/en/agent-sdk/subagents · https://code.claude.com/docs/en/sub-agents
- Cognition — Don't Build Multi-Agents (2024) — https://cognition.com/blog/dont-build-multi-agents · Multi-Agents: What's Actually Working (2025) — https://cognition.com/blog/multi-agents-working
- OpenAI Agents SDK — https://openai.github.io/openai-agents-python/ · orchestration/handoffs — https://developers.openai.com/api/docs/guides/agents/orchestration · Swarm — https://github.com/openai/swarm
- OpenAI Codex — changelog https://developers.openai.com/codex/changelog · subagents https://developers.openai.com/codex/subagents · Agents-SDK integration https://developers.openai.com/codex/guides/agents-sdk
- LangGraph supervisor/swarm — https://dev.to/focused_dot_io/multi-agent-orchestration-in-langgraph-supervisor-vs-swarm-tradeoffs-and-architecture-1b7e · AWS+Bedrock — https://aws.amazon.com/blogs/machine-learning/build-multi-agent-systems-with-langgraph-and-amazon-bedrock/
- CrewAI — https://docs.crewai.com/en/concepts/tasks · AutoGen — https://microsoft.github.io/autogen/0.2/docs/tutorial/conversation-patterns/
- MoA / routing — Towards Generalized Routing (arXiv 2509.07571) · AdaptOrch (arXiv 2602.16873) · Beyond Monoliths / Expert Orchestration (arXiv 2506.00051)
- Simon Willison — notes on Anthropic multi-agent system — https://simonwillison.net/2025/Jun/14/multi-agent-research-system/

## Claim table — 멀티에이전트 토폴로지 (배치 5 · 1차 출처 직접 확인 2026-08-25)

이 행들은 [`direction/03`](../../../direction/03-what-research-says.md) *"여러 모델을 어떻게 쓰나"* 절을 떠받친다.

| Claim ID | Class | Claim and scope | Evidence | Confidence | 재검증 |
|---|---|---|---|---|---|
| MAO-001 | vendor-behavior | **오케스트레이터-워커가 큰 품질 향상을 낸 사례가 있다.** 원문 그대로: *"a multi-agent system with Claude Opus 4 as the lead agent and Claude Sonnet 4 subagents outperformed single-agent Claude Opus 4 by **90.2%** on our internal research eval."* ⚠️ **범위 한정 3중**: ⓐ **내부 평가**이고 표본 수·과제 구성·방법론이 **공개돼 있지 않다** ⓑ 저자가 우수 영역을 *"breadth-first queries"* 로 스스로 좁힌다 ⓒ **벤더가 자사 아키텍처를 평가한 자기보고**다 | `ANTHROPIC-MULTIAGENT-2025` | medium (벤더 내부 평가) | 2026-08-25 |
| MAO-002 | vendor-behavior | **토큰 배수와 그 설명력.** 원문 그대로: *"agents typically use about **4×** more tokens than chat interactions, and multi-agent systems use about **15×** more tokens than chats"*, 그리고 *"token usage by itself explains **80%** of the variance."* → **비용은 추정이 아니라 저자가 명시한 수치**이고, 성능 차이의 대부분이 곧 **토큰을 더 썼다는 사실**로 설명된다 | `ANTHROPIC-MULTIAGENT-2025` | high | 2026-08-25 |
| MAO-003 | synthesis | 🔴 ***"오케스트레이터-워커가 지배적(dominant) 프로덕션 토폴로지"* 는 리서치가 아니다.** 세 출처 어디에도 토폴로지 채택률의 **모집단 조사·설문·배포 통계가 없다.** Anthropic 은 **자사 아키텍처**를 서술할 뿐 업계 표준이라 하지 않는다. 그리고 **같은 근거로 인용해 온 Cognition 이 정반대를 쓴다** — *"**No single approach to building agents has become the standard yet**, besides some of the absolute basics."* → **프로젝트 판단으로 재분류**한다. ⚠️ **2026-08-25 대체 근거 탐색도 실패했다** — 나온 것은 벤더·컨설팅 설문과 콘텐츠 마케팅뿐이고 **학술 모집단 조사는 없다** ([`evidence-holes-register`](../../methods/evidence-holes-register.md) EVH-003) | `ANTHROPIC-MULTIAGENT-2025`; `COGNITION-NO-MULTIAGENT-2024` | high (반증) | 2026-08-25 **판단으로 재분류** |
| MAO-004 | vendor-behavior | **단일 작성자 원칙 — 인용은 정확하다.** *"Actions carry implicit decisions, and conflicting decisions carry bad results"* 는 2024년 글의 **Principle 2 제목 그대로**다. 2025년 후속 글이 운용 규칙을 준다 — *"multi-agent systems work best today when **writes stay single-threaded** and the additional agents contribute **intelligence rather than actions**."* ⚠️ **근거의 종류**: 통제실험이 아니라 **자사 운영 경험**이고, 예시(Flappy Bird)는 저자 스스로 *"This may seem contrived"* 라 단서를 단다. ⚠️ **용어 주의**: 원문 표현은 *"one writer"* · *"single-threaded"* 이고, *"single-**writer** principle"* 이라는 명명은 이 코퍼스의 것이다 | `COGNITION-NO-MULTIAGENT-2024`; `COGNITION-MULTIAGENT-2025` | medium-high | 2026-08-25 |
| MAO-005 | vendor-behavior | ⚠️ ***"코딩은 다중에이전트에 부적합"* 은 원문보다 센 말이다.** 원문은 **비교문**이다 — *"most coding tasks involve **fewer truly parallelizable tasks than research**."* 저자가 실제로 부적합 조건으로 든 것은 과제 종류가 아니라 **구조**다: *"Some domains that require **all agents to share the same context** or involve **many dependencies** between agents are not a good fit."* → *"코딩이라서 안 된다"* 가 아니라 *"공유 컨텍스트·상호 의존이 많으면 안 된다"* 로 쓴다 | `ANTHROPIC-MULTIAGENT-2025` | high | 2026-08-25 **한정 추가** |
| MAO-006 | vendor-behavior | **Devin Review 의 *"2 bugs per PR"* 는 절대값이다.** *"catches an **average of** 2 bugs per PR, of which roughly 58% are severe"* — 대조군·표본·심각도 판정 절차가 없다. 이 문서 본문이 이 수치를 *"~2 **more** bugs/PR"* 로 적어 **비교 증분처럼** 쓰고 있었다 (IPW-008 이 2026-08-24 에 이미 짚었으나 **이 문서에 전파되지 않았다**) | `COGNITION-MULTIAGENT-2025` | high | 2026-08-25 **전파 수정** |

> **배치 5 의 결론 — 수치는 전부 맞았고, 틀린 것은 *지위*였다.**
> 90.2%·4×·15×·80%·2 bugs/PR·58% 는 **한 자리도 어긋나지 않았다.** 어긋난 것은 그 수치에 **부여한 지위**다 —
> 벤더 내부 평가를 *"연구 평가"* 로, 자사 아키텍처 서술을 *"지배적 토폴로지"* 로, 절대값을 *"증분"* 으로 올려 읽었다.
> **가장 아픈 것은 MAO-003 이다**: *"지배적"* 의 근거로 인용한 출처 자신이 *"아직 표준이 된 접근은 없다"* 고 쓴다.
>
> 🔴 **그리고 이 문서는 배치 2(2026-08-24)의 수정을 받지 못했다.** IPW-008·010 이 `direction/03` 만 고치고
> **정작 그 근거가 사는 이 문서를 그대로 두었다.** 절차 §6(*"수정은 전파된 곳까지 간다"*)이 지켜지지 않은 것이다 —
> 하루 동안 **코퍼스는 틀린 채로, `direction` 은 고쳐진 채로** 공존했다.

**재검증 기록 (배치 5 · 멀티에이전트)** — 검증일 `2026-08-25` · 검증자 `Claude Opus 5` + `codex-cli 0.145.0`(독립 질의, 결론 비공개) · **판정: 유지 2 · 한정 추가 1 · 판단으로 재분류 1 · 전파 수정 2** · **불일치 없음**(Codex 가 MAO-003 의 결정적 반증 문장 *"No single approach… has become the standard yet"* 을 **독립적으로 먼저 찾았다**) · 절차 [`reverification-protocol`](../../methods/reverification-protocol.md)
