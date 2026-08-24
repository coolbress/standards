---
id: aspect-28-implementation-process-workflow--research-log
title: "③ Implementation methodology — process tailoring + agentic workflow + adversarial review"
parent: aspect-28-implementation-process-workflow
kind: research-log
evidence_track: lit
status: review-needed
last_updated: "2026-06-26"
why_lit_not_census: "How to ROUTE/MANAGE construction work is a process/method question — not observable from a repo census (a repo shows artifacts, not the decision process that produced them). The SWEBOK 'Software Engineering Process' + 'Software Engineering Management' KAs cover this; the 27-aspect corpus (domain-organized) never carved one out. claudeck v1's routing is an instance of this methodology, so far adopted on 'it's well-built' trust rather than [lit] grounding. This note supplies the grounding."
---

# ③ Implementation methodology — the [lit] backbone for claudeck v1's routing

**The gap:** gingoa's 27 aspects are domain-organized (testing, security, scm…) and contain the ③
**construction practices** (aspect-07: TDD, code review, small CLs, defensive coding — SWEBOK KA4). They
do NOT contain the **meta/orchestration layer**: how an (AI) agent *routes, plans, delegates, verifies,
and is reviewed* when doing construction. That layer is exactly SWEBOK's **Software Engineering Process**
+ **Management** KAs, and it is `[lit]` (not census-able). Three pillars, all now grounded:

---

## Pillar A — Risk/size-tiered process selection  (claudeck's Tier 0/1/2/3)

> **Standard:** Match process weight to a change's risk/scope; well-understood low-risk changes ride a
> lighter pre-approved track, risky/novel changes get full gates. Multiply codified; **confidence: high.**

- **Process tailoring is a mandated discipline in the cited historical/adjacent sources.** The withdrawn
  ISO/IEC/IEEE 12207:2017 and 15288 material was originally used here; CMMI L3 requires each
  project's "defined process" to be a documented tailoring of the org standard. SWEBOK v4 SE-Process KA
  lists **risk-based rigor + lifecycle tailoring** as key principles. The current ISO/IEC/IEEE 12207:2026
  public catalog confirms a methodology-neutral life-cycle framework, but not this clause-level tailoring
  detail; current-edition mapping is **INCONCLUSIVE**. `[lit]` historical ISO 12207:2017 ·
  CMU/SEI-94-TR-024 · SWEBOK v4.
- **The canonical "how much process" model** = Boehm & Turner, *Balancing Agility and Discipline* (2004):
  five risk factors — **criticality, size, dynamism, personnel, culture**; criticality sets the minimum
  process floor. `[lit]` Boehm & Turner; IEEE Computer 2003.
- **"Just enough" lineage:** XP/YAGNI ("simplest thing that could work"), Lean's "extra processing" =
  waste. `[lit]` Fowler/Beck · Poppendieck 2003.
- **Small-batch economics** (why small changes warrant lighter process + merge fast): DORA/Accelerate
  (small batches → simultaneously higher deploy freq + lower change-fail rate), Reinertsen flow
  (queueing-theory batch-size cost), Google "small CLs ~100 LOC" + **tool-generated changes get a bypass
  lane**, trunk-based dev. `[lit]` DORA · Reinertsen 2009 · google/eng-practices.
- **Discrete change-tier prior art:** ITIL **standard / normal / emergency** (pre-approved vs CAB vs
  ECAB) — the clearest precedent for differentiated process lanes. **Meta RADAR (2026, arXiv:2605.30208)**
  = strongest contemporary prior art: auto-classifies diffs by risk (deterministic codemod → auto-accept;
  AI codemod → reduced; human → full review), **60% auto-approval, 1/50 the production-incident rate** of
  full-human review. Almost exactly claudeck's tier model applied to review.
- **Honest scope:** tiering by **risk** is codified; tiering by **task TYPE** within a repo (doc / one-liner
  / bug / feature) is a *novel application* of established principles, not a named standard. The four
  convergent tailoring dimensions to classify on: **blast-radius · novelty · criticality · reversibility.**

Sources: withdrawn ISO/IEC/IEEE 12207:2017 (ieeexplore 8100771; historical only) · current
ISO/IEC/IEEE 12207:2026 catalog https://www.iso.org/standard/90219.html · SWEBOK v4 (computer.org) · CMU/SEI-94-TR-024 · Boehm&Turner
2004 (ACM 861419) · Felderer risk-based-testing taxonomy (arXiv:1912.11519) · DORA small-batches/trunk
(dora.dev) · Reinertsen *Flow* 2009 · google.github.io/eng-practices small-CLs · trunkbaseddevelopment.com
· ITIL change types (it-processmaps) · Meta RADAR (arXiv:2605.30208).

---

## Pillar B — Agentic implementation workflow  (claudeck's plan→delegate→verify, gates, circuit-breaker)

> **Standard:** A coordinator plans (as a persisted artifact), delegates to context-isolated workers,
> verifies via OBJECTIVE external signals, bounds retries, and checkpoints with the human before
> irreversible actions. **Confidence: high** for the individual practices; the field has **no single
> dominant agent architecture** (calibrate accordingly).

- **Plan-then-act.** Explicit decompose-before-act removes calculation / missing-step / misread error
  classes (Plan-and-Solve, ACL 2023); ReAct interleaves reason+act (+34% ALFWorld). → claudeck's
  **plan-file-first** matches "plan is an ARTIFACT, not a prompt" (persist it; it's the HITL + resume unit).
- **Orchestrator-worker / multi-agent.** Anthropic multi-agent research system: lead + parallel subagents
  **+90.2%** vs single-agent, via **context isolation**; CAID (arXiv:2603.21489): centralized delegation +
  **git-worktree isolation** + test verification = **+26.7pp**. Counterpoint: Cognition "Don't build
  multi-agents" (context fragmentation) — but reversed Mar-2026 ("Devin manages Devins"). **Resolution:
  isolation is the mechanism; pass FULL decision context (plan + constraints + prior decisions) to a
  subagent, not a bare task string.** → claudeck's **lead-coordinator + implementer/simple-executor in
  worktrees + cherry-pick + "## Blast-radius" handoff** is a direct match (CAID-shaped).
- **Context engineering.** "Lost in the Middle" (arXiv:2307.03172): attention degrades for mid-context
  info (architectural, not prompt-fixable). → claudeck's **"lead is coordinator ONLY, never writes
  production code, delegates heavy work"** is the right mitigation (keep coordinator context lean;
  externalize completed-step summaries).
- **Self-verification.** External signals (tests/lint/types) reliably improve; **intrinsic self-correction
  is unreliable** (arXiv:2406.01297; SELF-[IN]CORRECT). Reflexion (91% HumanEval) is driven by test
  pass/fail. → claudeck's **TDD-always + Verify + deterministic pre-pass (ruff/mypy/eslint/tsc fed to
  reviewers as facts)** is exactly the objective-signal pattern.
- **Failure handling.** Agent loops spiral / retry unboundedly (MAST 14 failure modes; AgentFixer). Need
  **attempt caps + oscillation detection + checkpoint resume.** → claudeck's **"3 TDD/Verify failures →
  stop"** circuit-breaker + **review-history oscillation check** match.
- **HITL / autonomy levels.** Confirm before irreversible/outward actions; "write-staging" turns an
  irreversible commit into a reversible draft until promoted (arXiv:2605.12105, 2506.12469); OpenAI Model
  Spec: minimize irreversible side-effects. → claudeck's **Execution Confirmation Protocol Gate 3**
  (outward-facing/hard-to-reverse: issue/commit/push/PR/merge/cleanup → re-confirm) is a point-match.
- **SWE-bench reality:** ACI (interface) design, model choice, and **multi-model + LLM-as-judge patch
  selection** are top levers; **no single architecture dominates** → don't over-fit to one shape.

Sources: Plan-and-Solve (arXiv:2305.04091) · ReAct (2210.03629) · ToT (2305.10601) · Anthropic
multi-agent-research-system + building-effective-agents · CAID (2603.21489) · Cognition don't/do
build-multi-agents · Lost-in-the-Middle (2307.03172) · Reflexion (2303.11366) · Self-Refine (2303.17651) ·
self-correction-limits (2406.01297) · MAST (2503.13657) · autonomy-levels (2506.12469) · write-staging
(2605.12105) · OpenAI Model Spec · SWE-agent (2405.15793) · Dissecting-SWE-bench (2506.17208).

---

## Pillar C — Multi-agent adversarial review  (claudeck's review-round: R1 proposer + R2 adjudicator)

> **Standard:** Two INDEPENDENT, cross-VENDOR reviewers over fixed dimensions with an EVIDENCE BAR catch
> more real defects with fewer correlated false-positives than single-model or same-context self-review.
> **Confidence: high** for the design principles; **calibrate** — LLM review augments, never replaces.

- **LLM-as-judge works but is self-biased.** ~80% human agreement (Zheng, NeurIPS 2023), but **self-
  preference bias is causal** — models favor their own (lower-perplexity) outputs (Panickssery, NeurIPS
  2024 Oral; Kim 2410.21819). → **a model is a weak judge of its OWN work.**
- **Vendor diversity is the fix.** "Panel of diverse models" from **disjoint families** beats a single
  GPT-4 judge AND is 7× cheaper (Verga PoLL, arXiv:2404.18796); cross-family panels are fairest. →
  claudeck's **R1 (Claude/Fable) + R2 (Codex — different vendor)** is literature-validated; same-vendor R1+R2
  would share blind spots.
- **Adversarial second pass, proven.** CodeX-Verify (arXiv:2511.16708): information-theoretic proof that
  agents with **diverse, low-correlated detection patterns** (measured ρ≈0.05–0.25) find more bugs than
  any single agent (+39.7pp from 1→4); multi-agent **debate beats majority voting**. → claudeck's R1→R2
  adversarial structure matches.
- **THE critical calibration — agreeableness bias.** Without an evidence bar, an LLM adjudicator
  rubber-stamps R1 (confirms its hallucinations) (arXiv:2510.11822). **Cross-context review** (fresh
  session, not same-context self-review) gives +16% F1 (arXiv:2603.12123). → claudeck's R2 = **"confirms /
  adjusts / DROPS R1 findings with counter-evidence"** + **HIGH requires a code excerpt + concrete failure
  path** is *exactly* the documented mitigation; R1/R2 as separate agents = the cross-context benefit.
- **Honest limits (calibrate expectations):** production LLM-review precision is ~65–75% (BitsAI-CR,
  ByteDance arXiv:2501.15134) — false positives never hit zero; benchmark numbers inflate (F1 68%→3% on
  harder sets). Human modern review is **mostly code-health + knowledge-transfer, not defect-catching**
  (Bacchelli&Bird ICSE'13; Sadowski ICSE-SEIP'18) → AI review **augments** the defect-finding layer, it
  does not replace human review's social function. claudeck's Codex-down → Sonnet **self**-adjudication is
  a *degraded* fallback (same-vendor → agreeableness creeps back) — claudeck already labels it as such. ✓

Sources: Zheng MT-Bench (2306.05685) · Panickssery self-preference (2404.13076) · Kim (2410.21819) · Verga
PoLL (2404.18796) · CodeX-Verify (2511.16708) · multi-agent-debate (2510.12697) · agreeableness-bias
(2510.11822) · cross-context-review (2603.12123) · BitsAI-CR (2501.15134) · Bacchelli&Bird ICSE'13 ·
Sadowski ICSE-SEIP'18 · Fagan 1976.

---

## claudeck v1 routing ↔ literature — verdict

**Not "trust because well-built" — substantially [lit]-validated, often a point-for-point match:**

| claudeck routing element | Literature grounding | Verdict |
|---|---|---|
| Tier 0/1/2/3 differentiated ceremony | process tailoring · ITIL tiers · Meta RADAR | ✅ validated |
| plan-file-first (write+approve before code) | plan-as-artifact (Plan-and-Solve) | ✅ validated |
| lead-coordinator + worktree subagents + cherry-pick | CAID · Anthropic multi-agent · context isolation | ✅ validated |
| lead never writes code (lean context) | Lost-in-the-Middle | ✅ validated |
| TDD-always + Verify + deterministic pre-pass | external-signal verification · Reflexion | ✅ validated |
| 3-failure circuit-breaker + oscillation check | MAST · AgentFixer failure-handling | ✅ validated |
| Gate 3 HITL on irreversible/outward actions | autonomy-levels · write-staging · Model Spec | ✅ validated |
| review-round R1(Claude)+R2(Codex) cross-vendor | PoLL · self-preference bias | ✅ validated |
| R2 confirm/adjust/**drop** + evidence-bar (HIGH=excerpt) | agreeableness-bias mitigation · cross-context | ✅ validated (the key one) |

**Refinements the literature suggests (optional, not blockers):**
1. Tier classifier keys on task TYPE; could enrich with explicit **risk signals** (blast-radius / novelty /
   criticality / reversibility — RADAR-style) so an "edit" touching a security path or public API escalates.
2. Make coordinator context-budgeting explicit (externalize completed-step summaries — Lost-in-the-Middle).
3. Keep labeling the same-vendor self-adjudication fallback as degraded (already done). ✓

---

## Corpus recommendation (decision for the owner — touches the LOCKED 27)

The corpus genuinely lacks a **Software Engineering Process / Management** aspect (a real SWEBOK KA gap).
Options: **(a)** add a 28th aspect "Implementation Process & Agentic Workflow" (Pillars A+B+C live here as
the ③-execution methodology); **(b)** augment — fold Pillar A into a small process aspect, B+C into
aspect-27 (ai-harness-archetype) and aspect-07. Recommend **(a)** — it's a distinct, [lit]-grounded KA the
domain-organized corpus missed, and it's the canonical home for "how gingoa drives ③." Either way the
content above is the grounding; claudeck v1's routing is the *applied* form.
