---
id: aspect-28-implementation-process-workflow
title: "Implementation Process & Agentic Workflow"
group: "C — Construct & Verify"
kind: universal
gated_archetypes: []
cross_cutting: false
lifecycle_stages: ["③"]
anchors: ["SWEBOK-Process-KA", "SWEBOK-Management-KA", "ISO-12207-2026-catalog-scope", "Boehm-Turner", "agentic-workflow-lit"]
evidence_track: lit
status: review-needed
last_updated: "2026-06-26"
sources:
  - "https://www.computer.org/education/bodies-of-knowledge/software-engineering/v4"
  - "https://dl.acm.org/doi/10.5555/861419"
  - "https://arxiv.org/abs/2605.30208"
  - "https://dora.dev/devops-capabilities/process/working-in-small-batches/"
  - "https://aclanthology.org/2023.acl-long.147/"
  - "https://www.anthropic.com/engineering/multi-agent-research-system"
  - "https://arxiv.org/abs/2307.03172"
  - "https://arxiv.org/abs/2303.11366"
  - "https://arxiv.org/abs/2406.01297"
  - "https://arxiv.org/abs/2506.12469"
  - "https://arxiv.org/abs/2404.13076"
  - "https://arxiv.org/abs/2404.18796"
  - "https://arxiv.org/abs/2510.11822"
  - "https://arxiv.org/abs/2603.12123"
claim: "Implementation is driven by process tailored to each change's risk — light gates for trivial/low-risk changes, full gates for risky/novel ones — executed by a plan-first coordinator that delegates to context-isolated workers, verifies against objective signals, bounds retries, checkpoints with the human before irreversible actions, and gates merges behind an adversarial cross-vendor review."
maps_from: ["docs/adr", "aspects/28-implementation-process-workflow/research-log.md"]
census_todo: "none — [lit] by nature: how work is ROUTED/MANAGED is not observable from a repo census (a repo shows artifacts, not the decision process). Census-grounding does not apply; literature is the only valid track."
---

> **Standard (claim):** Implementation is driven by process **tailored to each change's risk** — light gates for trivial/low-risk changes, full gates for risky/novel ones — executed by a **plan-first coordinator** that delegates to **context-isolated workers**, verifies against **objective signals**, **bounds retries**, **checkpoints with the human before irreversible actions**, and gates merges behind an **adversarial cross-vendor review**.
> **Evidence:** lit (SWEBOK Process/Mgmt KA · Boehm-Turner · DORA · Meta RADAR · agentic-coding + LLM-as-judge literature) · **Confidence:** high (principles); calibrate (no single agent architecture dominates; LLM review augments, never replaces) · **Kind:** universal · **Stage:** ③

**Seed sub-aspects:** `risk/size process tailoring (tiering)` · `plan-then-act (plan as artifact)` · `lead-coordinator + context-isolated subagents` · `objective-signal verification (TDD / lint / types)` · `failure handling (circuit-breaker / oscillation)` · `human-in-the-loop on irreversible actions` · `adversarial cross-vendor review (judge-bias mitigation)`

This is the **meta-layer over aspect-07** (construction practices) and aspect-08 (testing): not *how to write a unit of code*, but *how the construction work is routed, executed, and gated* — the SWEBOK **Software Engineering Process** + **Management** KAs, applied in the AI-agent era.

## What professional engineers do

- **Right-size process to the change (tiering).** Mature teams do NOT run one heavyweight pipeline on every change; they tailor process to risk/scope. Standard/low-risk changes ride a light, pre-approved track; novel/high-blast-radius changes get full gates. The classifier keys on four convergent dimensions: **blast-radius · novelty · criticality · reversibility**. [lit] SWEBOK + CMMI process tailoring; Boehm-Turner 5-factor model (criticality sets the floor); ITIL standard/normal/emergency; Meta RADAR auto-routes diffs by risk score.
- **Smaller change → lighter process → faster merge.** Small batches simultaneously raise delivery throughput and *lower* change-failure rate (it is not a speed/quality tradeoff). ~100-line CLs are reviewed more thoroughly; tool-generated/mechanical changes get a verify-only bypass lane. [lit] DORA/Accelerate small-batches; Reinertsen batch economics; Google small-CLs.
- **Plan before acting — and the plan is an artifact.** Decompose and write a plan before executing; persist it (file/state), don't keep it only in context. Explicit planning removes calculation / missing-step / misread error classes; the persisted plan is also the human-checkpoint and crash-resume unit. [lit] Plan-and-Solve (ACL 2023); ReAct.
- **Coordinator + context-isolated workers.** A lead plans/dispatches/reviews and stays out of the weeds; heavy work goes to sub-agents in isolated workspaces (e.g. git worktrees), each handed the *full decision context* (plan + constraints + prior decisions), not a bare task string. Keeps the coordinator's context lean — attention degrades for mid-context information ("lost in the middle"), an architectural property no prompt fixes. [lit] Anthropic multi-agent system (+90% on a research eval); CAID (+26.7pp, worktree isolation); Lost-in-the-Middle. Calibrate: multi-agent helps for parallelizable/isolatable work, adds coordination-failure risk otherwise (Cognition's caution; MAST failure taxonomy).
- **Verify against objective signals, not self-assessment.** Verification uses the compiler, test runner, linter, type-checker — external truth. Intrinsic self-correction (a model critiquing itself with no external feedback) is unreliable and can degrade output. Test-driven agent loops (RED→GREEN) are the strongest coding-specific pattern. [lit] Reflexion (test-signal-driven); "when can LLMs correct their own mistakes" (self-correction limits); SELF-[IN]CORRECT.
- **Bound failure: circuit-breakers + oscillation detection.** Agent loops spiral and retry unboundedly; cap attempts (stop after N failures → escalate/HITL) and detect oscillation (same action without state change). Persist checkpoints so a crashed run resumes from the last verified state. [lit] MAST failure modes; AgentFixer; SHIELDA structured exception handling.
- **Human-in-the-loop before irreversible/outward actions.** Autonomy is a deliberate design choice separate from capability; the practical standard for coding agents is to confirm before commit / push / PR / merge / delete / destructive commands. "Write-staging" (draft → human approval → promote) converts an irreversible action into a reversible one. [lit] Levels-of-Autonomy taxonomy; write-staging; OpenAI Model Spec (minimize irreversible side-effects).
- **Gate merges behind adversarial, cross-vendor review.** LLM-as-judge agrees with humans ~80% of the time but carries a causal **self-preference bias** (a model favors its own lower-perplexity outputs) — so a model is a weak judge of its *own* work. The fixes, all literature-backed: (1) **vendor/model diversity** (a panel of disjoint-family models beats a single judge and reduces correlated blind spots); (2) an **adversarial second pass** (a challenger that confirms/adjusts/drops the first reviewer's findings — proven to raise defect detection when detection patterns are diverse); (3) an **evidence bar** to defeat agreeableness bias (without it, the adjudicator rubber-stamps the proposer's hallucinations); (4) **context isolation** (review in a fresh session, not the generation context — measured +16% F1). [lit] Zheng MT-Bench; Panickssery (self-preference, NeurIPS'24 oral); Verga PoLL; CodeX-Verify; agreeableness-bias; cross-context-review.

## Evidence (lit + census)

- [lit] **SWEBOK v4 — Software Engineering Process + Management KAs.** "A well-defined, optimized and automated life cycle tailored to product/project characteristics is key"; risk-based rigor + tailoring are listed principles. https://www.computer.org/education/bodies-of-knowledge/software-engineering/v4
- [lit] **ISO/IEC/IEEE 12207:2026** — the public ISO catalog supports a methodology-neutral common
  life-cycle-process framework and says its processes can be applied concurrently, iteratively, recursively,
  and incrementally. It does **not** support this document's risk-tier classifier; that support comes from
  SWEBOK, CMMI, Boehm–Turner, ITIL, and Meta RADAR. Clause-level mapping remains **INCONCLUSIVE**.
  https://www.iso.org/standard/90219.html
- [lit] **Boehm & Turner, *Balancing Agility and Discipline* (2004)** — the canonical "how much process" model: criticality · size · dynamism · personnel · culture. https://dl.acm.org/doi/10.5555/861419
- [lit] **Meta RADAR (arXiv:2605.30208, 2026)** — automated risk-tiered code review: deterministic codemod → auto-accept; AI codemod → reduced; human → full. 60% auto-approval, **1/50 the production-incident rate** of full-human review. The strongest contemporary prior art for tiering changes by risk. https://arxiv.org/abs/2605.30208
- [lit] **DORA / Accelerate** — small batches predict higher throughput AND lower change-failure rate. https://dora.dev/devops-capabilities/process/working-in-small-batches/
- [lit] **Plan-and-Solve (ACL 2023)**; **ReAct (ICLR 2023)** — plan-before-act reduces error classes. https://aclanthology.org/2023.acl-long.147/
- [lit] **Anthropic multi-agent research system** — lead + isolated subagents, +90.2% vs single-agent on a research eval; **CAID (arXiv:2603.21489)** — worktree-isolated delegation +26.7pp. https://www.anthropic.com/engineering/multi-agent-research-system
- [lit] **Lost in the Middle (arXiv:2307.03172)** — U-shaped context attention; mid-context info is under-weighted (architectural). https://arxiv.org/abs/2307.03172
- [lit] **Reflexion (arXiv:2303.11366)** (91% HumanEval, test-signal-driven); **self-correction limits (arXiv:2406.01297)** (intrinsic self-correction unreliable). https://arxiv.org/abs/2406.01297
- [lit] **Levels of Autonomy for AI Agents (arXiv:2506.12469)**; **write-staging (arXiv:2605.12105)**; OpenAI Model Spec — HITL before irreversible actions. https://arxiv.org/abs/2506.12469
- [lit] **LLM-as-judge:** Zheng MT-Bench (2306.05685); **self-preference bias** Panickssery NeurIPS'24 oral (2404.13076); **PoLL diverse-jury** (2404.18796); **CodeX-Verify** multi-agent (2511.16708); **agreeableness bias** (2510.11822); **cross-context review** (2603.12123).
- [census] **N/A by design** — see `census_todo`. (A repo census measures artifacts; the *process that produced them* is not file-detectable. This is the corpus's clearest `[lit]`-only aspect — and the reason the original 27-aspect, census-weighted taxonomy under-covered it.)

## Archetype variations

- **Universal principle, agentic-era instantiation.** Pillar A (risk-tiered process) is classic universal SWE — it applies to any team/project. Pillars B (coordinator/worker workflow) and C (adversarial review) are the **AI-agent instantiation**: how a team building *with* coding agents executes ③. As agentic coding becomes default practice, this is universal-modern, not a niche.
- **AI-harness archetype (the heaviest user).** A harness like gingoa (aspect-27) *is* an agent that drives ③, so it implements this aspect as machinery (a routing skill, planner/implementer/reviewer agents, gates). Non-agentic projects still use Pillar A (tier your changes; small CLs) and the human forms of B/C (plan-first; peer review).
- **Solo vs team.** Solo/low-criticality work compresses tiers (more Tier-0/1); team/high-criticality work widens gates (mandatory review, branch protection). Boehm-Turner's criticality factor sets the floor either way.

## Tradeoffs / what's ruled out

- **Ruled out: one pipeline for everything.** Running full ceremony on a typo wastes effort (Lean "extra processing"); running no process on a risky change is the defect vector. Tier by risk. [lit] Lean; Boehm-Turner.
- **Ruled out: same-model self-review as the merge gate.** Self-preference bias is *causal* (NeurIPS'24 oral) — a model rubber-stamps its own work. The review gate needs a *different* vendor + an evidence bar. Same-vendor self-adjudication is at best a labeled, degraded fallback.
- **Ruled out: intrinsic self-correction as verification.** Model self-assessment without external signals is unreliable; verification must be compiler/test/lint/type output. [lit] arXiv:2406.01297.
- **Ruled out: unbounded agent autonomy on irreversible actions.** Commit/push/PR/merge/delete are gated by default; autonomy is granted deliberately, not assumed. [lit] autonomy-levels; Model Spec.
- **Tradeoff: multi-agent power vs coordination cost.** Isolated sub-agents parallelize and keep context clean, but add hand-off/alignment failure modes (MAST). Use them for isolatable work with full-context hand-off; don't fragment a single coherent design decision across agents. [lit] Anthropic (for) vs Cognition (against) — resolved: isolation is the mechanism, full-context hand-off is the fix.
- **Tradeoff: review thoroughness vs false-positive burden.** Production LLM review precision is ~65–75% — it never reaches zero false positives; the dimension anchoring + evidence bar bound the noise, humans still adjudicate. [lit] BitsAI-CR.
- **Calibration: no dominant agent architecture.** SWE-bench leaderboards show high performers use varied designs — don't over-fit to one shape; the *principles* above are the durable part, the specific topology is replaceable. [lit] Dissecting-SWE-bench.

## Sources

- SWEBOK v4 (Process + Management KAs) — https://www.computer.org/education/bodies-of-knowledge/software-engineering/v4
- Boehm & Turner, *Balancing Agility and Discipline* (2004) — https://dl.acm.org/doi/10.5555/861419
- Meta RADAR (risk-tiered code review, 2026) — https://arxiv.org/abs/2605.30208
- DORA — Working in Small Batches — https://dora.dev/devops-capabilities/process/working-in-small-batches/
- Plan-and-Solve (ACL 2023) — https://aclanthology.org/2023.acl-long.147/
- Anthropic — multi-agent research system — https://www.anthropic.com/engineering/multi-agent-research-system
- CAID (async SE agents) — https://arxiv.org/abs/2603.21489
- Lost in the Middle — https://arxiv.org/abs/2307.03172
- Reflexion — https://arxiv.org/abs/2303.11366 · self-correction limits — https://arxiv.org/abs/2406.01297
- Levels of Autonomy — https://arxiv.org/abs/2506.12469 · write-staging — https://arxiv.org/abs/2605.12105
- LLM-as-judge / bias: Zheng MT-Bench https://arxiv.org/abs/2306.05685 · Panickssery (self-preference, NeurIPS'24 oral) https://arxiv.org/abs/2404.13076 · PoLL https://arxiv.org/abs/2404.18796 · CodeX-Verify https://arxiv.org/abs/2511.16708 · agreeableness bias https://arxiv.org/abs/2510.11822 · cross-context review https://arxiv.org/abs/2603.12123
- Modern code review baseline: Bacchelli & Bird ICSE'13 · Sadowski et al. ICSE-SEIP'18
- Full research log with all citations — [`research-log.md`](research-log.md) (co-located with this aspect)

## Sub-documents
- [`research-log.md`](research-log.md) — *research-log* — the full implementation-process & agentic-workflow research dig with all citations (the raw evidence behind this aspect's claims).
- [`facts-2026-08-sdlc-models.md`](facts-2026-08-sdlc-models.md) — *research-log (ko)* — 2026-08 pass: what Royce-1970/V-model/Spiral/RUP/CMMI/CD prescribe; its ISO/IEC/IEEE 12207:2017 detail is retained as historical, review-needed evidence and separated from the 2026 public scope.
- [`facts-2026-08-agile-adoption.md`](facts-2026-08-agile-adoption.md) — *research-log (ko)* — 2026-08 facts-only pass: Manifesto/Scrum-Guide/Kanban/XP/SAFe/Shape-Up prescriptions verbatim + adoption statistics (State of Agile, PMI 2024) + attributed Scrum critiques (Jeffries/Fowler/Holub/Basecamp).
- [`facts-2026-08-agent-workflow-prescriptions.md`](facts-2026-08-agent-workflow-prescriptions.md) — *research-log (ko)* — 2026-08 facts-only pass: what agent-era workflows PRESCRIBE (Spec Kit spec→plan→tasks→implement + constitution · Kiro 3-file/EARS · Anthropic Explore→Plan→Implement→Commit + skip-planning rule · Codex guidance · Cursor/Windsurf splits) + attributed critiques (Scott Logic 10x overhead measurement); BMAD/OpenSpec 미확보 명시.
