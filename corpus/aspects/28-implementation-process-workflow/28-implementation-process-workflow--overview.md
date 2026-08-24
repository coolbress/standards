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
- [`sdlc-models--facts-2026-08.md`](sdlc-models--facts-2026-08.md) — *research-log (ko)* — 2026-08 pass: what Royce-1970/V-model/Spiral/RUP/CMMI/CD prescribe; its ISO/IEC/IEEE 12207:2017 detail is retained as historical, review-needed evidence and separated from the 2026 public scope.
- [`agile-adoption--facts-2026-08.md`](agile-adoption--facts-2026-08.md) — *research-log (ko)* — 2026-08 facts-only pass: Manifesto/Scrum-Guide/Kanban/XP/SAFe/Shape-Up prescriptions verbatim + adoption statistics (State of Agile, PMI 2024) + attributed Scrum critiques (Jeffries/Fowler/Holub/Basecamp).
- [`agent-workflow-prescriptions--facts-2026-08.md`](agent-workflow-prescriptions--facts-2026-08.md) — *research-log (ko)* — 2026-08 facts-only pass: what agent-era workflows PRESCRIBE (Spec Kit spec→plan→tasks→implement + constitution · Kiro 3-file/EARS · Anthropic Explore→Plan→Implement→Commit + skip-planning rule · Codex guidance · Cursor/Windsurf splits) + attributed critiques (Scott Logic 10x overhead measurement); BMAD/OpenSpec 미확보 명시.

## Claim table — 벽의 근거 (배치 1 · 1차 출처 직접 확인 2026-08-24)

이 네 행은 [`direction/04`](../../../direction/04-the-plan.md) 설계 원칙 **01(집행은 에이전트 밖에서)** 과
**03(집행은 벽으로)** 을 떠받친다. 무너지면 설계를 다시 봐야 하므로 1차 출처를 직접 열었다.

| Claim ID | Class | Claim and scope | Evidence | Confidence | 재검증 |
|---|---|---|---|---|---|
| **IPW-001** | empirical | **외부 피드백 없는 자기교정은 성공 사례가 없다.** 서베이 결론 (1): *"no prior work demonstrates successful self-correction with feedback from prompted LLMs, except for studies in tasks that are exceptionally suited for self-correction."* | `SELFCORRECT-SURVEY-2024` | high | 2026-08-24 |
| **IPW-002** | empirical | ⭐ **그러나 신뢰할 만한 외부 피드백이 있으면 자기교정은 잘 작동한다.** 같은 서베이 결론 (2): *"self-correction works well in tasks that can use **reliable external feedback**."* **이것이 이 프로젝트 설계의 가장 직접적인 근거다** — 테스트·CI·타입체커가 곧 그 외부 피드백이다. ⚠️ 이전 판의 인용에서 **이 절반이 빠져 있었다** | `SELFCORRECT-SURVEY-2024` | high | 2026-08-24 **신규** |
| **IPW-003** | empirical | **내재적 자기교정은 성능을 떨어뜨리기도 한다** — *"LLMs struggle to self-correct their responses without external feedback, and at times, their performance even degrades after self-correction."* ⚠️ **범위 한정: 추론 과제**(GSM8K·CommonSenseQA·HotpotQA, GPT-3.5/4)다. 코딩 일반이 아니다 | `NO-SELFCORRECT-REASONING-2023` | high | 2026-08-24 **출처 정정** |
| **IPW-004** | empirical | **LLM 심판은 자기 출력을 알아보고 선호한다.** GPT-4·Llama-2 가 자기 생성물을 식별하는 정확도가 유의하고, 파인튜닝 실험에서 **자기인식 능력과 자기선호 강도가 선형으로 동행**했다. ⚠️ 저자 표현이 *"initial evidence"* 이므로 **개별 판단 수준의 인과로 확정하지 않는다** | `SELF-PREFERENCE-2024` | medium-high | 2026-08-24 |
| **IPW-005** | vendor-behavior | **pre-commit 훅은 게이트가 될 수 없다.** git 자체 문서: `--no-verify` 는 *"bypasses the pre-commit and commit-msg hooks"*, `git push --no-verify` 는 *"the hook is bypassed completely"*. **로컬 훅은 커밋하는 사람이 끌 수 있다** | `GIT-COMMIT-DOC` | high | 2026-08-24 |

> **배치 1 의 결론: 벽의 근거는 무너지지 않았다. 오히려 강해졌다.**
> 다만 **인용 구조가 틀려 있었다** — ⓐ *"출력을 악화시킬 수 있다"* 의 출처가 서베이(`2406.01297`)로 적혀 있었으나
> 실제로는 Huang et al.(`2310.01798`)이고 **추론 과제 한정**이다. ⓑ Reflexion 을 *"자기교정은 신뢰할 수 없다"* 의
> 근거로 든 것은 **방향이 반대**다 — Reflexion 은 **피드백 기반 반복이 성공한다**는 논문이고, HumanEval 91% 는
> **자체 생성 단위시험을 실제 실행한 신호**로 구동된다(`REFLEXION-2023`). ⓒ 그리고 **IPW-002 가 통째로 빠져 있었다.**

**재검증 기록 (배치 1)** — 검증일 `2026-08-24` · 검증자 `Claude Opus 5` + `codex-cli 0.145.0`(독립 질의, 결론 비공개) · **판정: 유지 3 · 출처 정정 1 · 신규 추가 1** · **불일치 없음**(4개 항목 전부 일치. Codex 가 IPW-003 의 과제 범위와 IPW-004 의 *"initial evidence"* 한정을 추가로 짚었다) · 절차 [`reverification-protocol`](../../methods/reverification-protocol.md)

## Claim table — 독립 리뷰어의 근거 (배치 2 · 1차 출처 직접 확인 2026-08-24)

이 행들은 [`direction/04`](../../../direction/04-the-plan.md) **만들 것 ⑥(`@claude` PR 리뷰어 — diff 만 보는 제3자)** 를 떠받친다.

| Claim ID | Class | Claim and scope | Evidence | Confidence | 재검증 |
|---|---|---|---|---|---|
| **IPW-006** | empirical | **컨텍스트를 분리한 리뷰가 같은 세션 자기리뷰보다 낫다 — 통제실험.** 30개 산출물 · 150개 주입 오류 · **360 리뷰** · 4개 조건. **CCR F1 28.6%** vs 같은세션 자기리뷰 **24.6%**(p=0.008, d=0.52) · 반복 자기리뷰 21.7%(p<0.001) · 컨텍스트 있는 서브에이전트 23.8%(p=0.004). ⭐ **SR2 대조가 결정적** — 같은 세션에서 두 번 리뷰해도 한 번보다 낫지 않았다(p=0.11). **반복이 아니라 컨텍스트 분리 자체가 원인**이다 | `CROSS-CONTEXT-REVIEW-2026` | high | 2026-08-24 |
| **IPW-007** | synthesis | ⚠️ **그러나 절대 성능은 낮다.** 최선 조건(CCR)에서도 **F1 28.6%** — 주입된 오류의 **약 71%를 놓친다.** *"+16%"* 는 **상대 개선**(28.6/24.6)이지 절대 수준이 아니다. → **독립 리뷰어는 갖출 값이 있지만 안전망으로 취급하면 안 된다.** 게이트는 여전히 CI 다 | `CROSS-CONTEXT-REVIEW-2026` | high | 2026-08-24 **신규** |
| **IPW-008** | vendor-behavior | Cognition 은 자사 Devin Review 가 *"catches an **average of 2 bugs per PR**, of which roughly 58% are severe"* 라고 보고한다. ⚠️ **절대 평균값이지 다른 방식 대비 증분이 아니다.** 표본·대조군·심각도 판정 절차 **미제시**. 벤더의 자기 제품 보고다 | `COGNITION-MULTIAGENT-2025` | medium | 2026-08-24 **수치 재해석** |
| **IPW-009** | vendor-behavior | **교차벤더 라우팅은 비용이 아니라 역량 최적화다** — *"Cross-frontier communication is less about a weaker model knowing when to ask a stronger one, and more about routing to whichever model is best at the specific sub-task… The delegation logic becomes a **capability router** rather than a difficulty escalator."* | `COGNITION-MULTIAGENT-2025` | medium-high | 2026-08-24 |
| **IPW-010** | synthesis | ❌ ***"정적 역할 배정이 프로덕션 표준이고 동적 per-query 라우팅은 아직 연구 단계"* 는 받쳐지지 않는다.** 배포 통계가 없고, **같은 출처(Cognition)가 동적 교차벤더 라우팅을 *"in production for a meaningful stretch"* 로 돌렸다고 밝힌다** — 자기모순이다. MasRouter 도 선행연구를 Fixed·Dynamic 양쪽으로 분류할 뿐이다 | `COGNITION-MULTIAGENT-2025` | high (반증) | 2026-08-24 **삭제 권고** |

> **배치 2 의 요점: 결론은 맞는데 근거가 뒤바뀌어 있었다.**
> *"작성자 컨텍스트가 없는 리뷰어가 더 찾는다"* 는 **통제실험(IPW-006)이 받친다.** 그런데 이전 판은
> 그 문장에 **Cognition 의 *"2건/PR"* 을 근거로 붙였다** — 그건 **절대값이고 대조군이 없어** 비교 주장을
> 받칠 수 없다. 강한 근거와 약한 근거가 한 문장에 섞여 **약한 쪽이 하중을 지고 있었다.**

**재검증 기록 (배치 2)** — 검증일 `2026-08-24` · 검증자 `Claude Opus 5` + `codex-cli 0.145.0`(독립 질의) · **판정: 유지 2 · 한정 추가 1 · 수치 재해석 1 · 삭제 1** · **불일치 없음**(Codex 가 IPW-010 의 자기모순을 독립적으로 짚었다) · 절차 [`reverification-protocol`](../../methods/reverification-protocol.md)
