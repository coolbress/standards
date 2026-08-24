---
id: aspect-27-ai-harness-archetype--harness-control-plane
title: "Agent Harness Control Plane, Execution Boundary, and Lifecycle"
parent: aspect-27-ai-harness-archetype
kind: reference
status: verified
last_updated: "2026-08-02"
evidence_track: lit
freshness: volatile
review_due: "2026-11-02"
sources: [OPENAI-CODEX-CUSTOMIZATION, OPENAI-SANDBOX-AGENTS, MCP-2025-11-25, AGENT-SKILLS-SPEC, ANTHROPIC-AGENT-EVALS-2026, ANTHROPIC-LONG-HARNESS-2025, ANTHROPIC-CONTAINMENT-2026, ANTHROPIC-MULTIAGENT-2025]
---

# Agent Harness Control Plane, Execution Boundary, and Lifecycle

> Scope: a component map grounded in current first-party specifications and engineering reports. Product-specific
> behavior is labeled as such; the cross-source component model is corpus synthesis, not a universal standard.

## Claim register

| Claim ID | Class | Claim and scope | Evidence | Confidence | Valid as of / expiry |
|---|---|---|---|---|---|
| HCP-001 | definition | An agent harness is the system around a model that runs the agent loop, supplies tools and environment, and returns or persists outcomes; evaluating an “agent” evaluates model and harness together. | `ANTHROPIC-AGENT-EVALS-2026`; `OPENAI-SANDBOX-AGENTS` | high for cited vendors | 2026-08-02; terminology may evolve |
| HCP-002 | vendor-behavior | OpenAI's current Agents SDK documentation assigns model calls, tool routing, handoffs, approvals, tracing, recovery, and run state to the harness control plane, while files, commands, packages, mounts, ports, and snapshots belong to the sandbox execution plane. | `OPENAI-SANDBOX-AGENTS` | high | 2026-08-02; beta API, review 2026-11-02 |
| HCP-003 | synthesis | A complete harness component census must cover control, capability, execution, state, assurance, and distribution planes; counting only prompts, skills, hooks, MCP, and subagents misses approvals, recovery, run state, isolation, observability, and update/rollback. | HCP-001/002; `OPENAI-CODEX-CUSTOMIZATION`; `MCP-2025-11-25` | medium-high | review when major host surfaces change |
| HCP-004 | normative | MCP standardizes host/client/server integration and exposes server Resources, Prompts, and Tools plus client Roots, Sampling, and Elicitation, with progress, cancellation, errors, and logging as utilities. Consent and tool descriptions remain trust boundaries. | `MCP-2025-11-25` | high | protocol revision 2025-11-25 |
| HCP-005 | vendor-behavior | Current Codex customization separates persistent `AGENTS.md`, learned memories, reusable Skills, external MCP connections, and Subagents; Skills use progressive disclosure. | `OPENAI-CODEX-CUSTOMIZATION`; `AGENT-SKILLS-SPEC` | high | 2026-08-02; volatile |
| HCP-006 | empirical | Anthropic reports that multi-agent research helped breadth-first, decomposable research in its internal eval but used substantially more tokens; it also reports coding as less parallelizable. This is scoped first-party evidence, not a universal dispatch rule. | `ANTHROPIC-MULTIAGENT-2025` | medium | Anthropic system/eval, published 2025 |
| HCP-007 | empirical | Anthropic's long-running coding experiments found that compaction alone was insufficient and used initializer/incremental agents plus durable handoff artifacts to bridge sessions. | `ANTHROPIC-LONG-HARNESS-2025` | medium | Anthropic experimental setup, published 2025 |
| HCP-008 | synthesis | Safety should cap capability with filesystem, network, credential, authority, and state boundaries; repeated per-action approval is not a sufficient containment strategy. | `OPENAI-SANDBOX-AGENTS`; `ANTHROPIC-CONTAINMENT-2026`; `MCP-2025-11-25` | high for boundary need; implementation context-dependent | review quarterly |
| HCP-009 | synthesis | Harness evaluation needs outcome/end-state checks, trace/process diagnostics, source-quality or policy checks where relevant, and human review of the eval itself. One happy-path demonstration is not evidence of harness worth. | `ANTHROPIC-AGENT-EVALS-2026`; `ANTHROPIC-MULTIAGENT-2025` | high | review annually |

## Component planes

| Plane | Components | Primary verification surface |
|---|---|---|
| Control | agent loop; task/depth routing; model/provider choice; tool routing; orchestration/handoffs; approvals/guardrails; cancellation; recovery | deterministic state transitions, policy tests, failure injection |
| Capability | instructions/constitution; skills; prompts; tools; MCP resources/prompts/tools; hooks; subagents | schema validation, discovery/trigger evals, contract tests |
| Execution | filesystem/shell/browser/code execution; mounts; packages; ports; sandbox provider | isolation tests, allow/deny tests, clean-environment run |
| State and context | working context; compaction; run state; workspace snapshot; session resume; durable memory; handoff artifacts | resume/replay tests, corruption/staleness tests |
| Assurance | traces; logs; metrics; eval tasks; graders; human review; security red-team; cost/latency budgets | end-state grading, trace review, calibrated evals, audit evidence |
| Distribution | plugin/package manifest; installation; host adapters; config schema; version compatibility; update; rollback; deprecation | install/upgrade/rollback matrix across supported hosts |

## Build standard

1. Define the outcome and end-state verifier before choosing components.
2. Draw the control-plane/execution-plane boundary and keep credentials and approval state outside model-directed
   execution where feasible.
3. Grant the smallest capabilities needed for the task; treat retrieved content and tool metadata as untrusted.
4. Make run, workspace, and memory state distinct; define which one survives a pause, restart, update, or failure.
5. Add one component only with a representative eval and an expiry/removal condition.
6. Test fresh install, upgrade, host compatibility, failure recovery, and rollback—not only the happy path.
7. Evaluate the result/end state first, then use traces to diagnose why it passed or failed.

## What this changes in the inherited corpus

The earlier aspect-27 component set was strong on Skills, MCP, hooks, commands, subagents, plugins, memory,
prompts, and evals. It was incomplete as a full harness taxonomy because isolation, approvals, recovery, run
state, observability, lifecycle compatibility, and rollback were not first-class peers. This document fills the
map; each plane still needs a focused implementation standard before goppi-final is built.

## Sources

- `OPENAI-CODEX-CUSTOMIZATION` — https://learn.chatgpt.com/docs/customization/overview
- `OPENAI-SANDBOX-AGENTS` — https://developers.openai.com/api/docs/guides/agents/sandboxes
- `MCP-2025-11-25` — https://modelcontextprotocol.io/specification/2025-11-25
- `AGENT-SKILLS-SPEC` — https://agentskills.io/specification
- `ANTHROPIC-AGENT-EVALS-2026` — https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- `ANTHROPIC-LONG-HARNESS-2025` — https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- `ANTHROPIC-CONTAINMENT-2026` — https://www.anthropic.com/engineering/how-we-contain-claude
- `ANTHROPIC-MULTIAGENT-2025` — https://www.anthropic.com/engineering/multi-agent-research-system

