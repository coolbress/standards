---
id: target-user-capability-model
title: "Target User Capability and Responsibility Model"
kind: reference
status: verified
last_updated: "2026-08-02"
evidence_track: lit
freshness: versioned
review_due: "2027-02-02"
sources: [EUSE-STATE-OF-ART, LCNC-ADOPTION-SLR-2024, LOVABLE-SECURE-2025, REPLIT-SECURE-2025, ANTHROPIC-CONTAINMENT-2026, IUI-APPROPRIATE-RELIANCE-2023, VIRK-NONPROGRAMMER-CODE-2025, NGUYEN-CODELLM-CHI-2024, PRATHER-WIDENING-GAP-ICER-2024, CODEA11Y-CHI-2025, NIST-GAI-600-1]
---

# Target User Capability and Responsibility Model

## Scope

“Non-engineer” is not one capability level. This model describes what a user can express, inspect, decide,
and operate. It is an applicability axis for aspects 01, 23, and 27—not a claim that users are deficient or a
29th software-engineering topic.

## Claim register

| Claim ID | Class | Claim and scope | Evidence | Confidence | Valid as of / expiry |
|---|---|---|---|---|---|
| TUC-001 | empirical | End-user software engineering studies people who create software in support of another primary job and documents reliability, testing, and debugging problems and interventions. The reviewed populations and tools predate current coding agents. | `EUSE-STATE-OF-ART` | high for field scope; medium for transfer to agents | durable field basis; refresh transfer evidence annually |
| TUC-002 | empirical | A 2024 LCNC systematic review synthesized 40 included primary studies and found a heterogeneous adoption literature; it does not establish one universal “citizen developer” capability profile. | `LCNC-ADOPTION-SLR-2024` | medium-high | review 2027-02-02 |
| TUC-003 | vendor-behavior | Lovable documents that absent or over-broad RLS can expose Supabase data; Replit reports a database-deletion incident and subsequent recovery and dev/prod-separation mitigations. These establish failure paths, not an inherent inability of non-engineers. | `LOVABLE-SECURE-2025`; `REPLIT-SECURE-2025` | high for vendor accounts; low for population generalization | review when product controls change |
| TUC-004 | synthesis | Harness behavior should be conditioned on separate capabilities: outcome expression, domain decision, evidence comprehension, technical verification, risk comprehension, and operational responsibility. Identity labels alone are insufficient. | `EUSE-STATE-OF-ART`; `LCNC-ADOPTION-SLR-2024` | medium-high | test with representative users |
| TUC-005 | empirical | Anthropic reports high permission-approval rates and declining attention under repeated prompts in its products; human approval is therefore not a complete containment boundary. | `ANTHROPIC-CONTAINMENT-2026` | medium; vendor telemetry | review 2026-11-02 |
| TUC-006 | synthesis | Transfer from end-user and LCNC populations to current coding-agent users is not established; a product must state its target capability profile as a hypothesis and validate it rather than infer capability from the label “non-engineer.” | `EUSE-STATE-OF-ART`; `LCNC-ADOPTION-SLR-2024` | high for evidence boundary; target profile remains unknown | review after representative user studies |
| TUC-007 | empirical | In a controlled CHI study, 120 beginning programmers who had passed an introductory course still struggled to prompt code LLMs on problems at their skill level despite automatic correctness feedback. This identifies outcome expression, generated-code interpretation, and iterative correction as separate barriers, but does not describe complete novices or full projects. | `NGUYEN-CODELLM-CHI-2024` | high within study; low for complete-novice transfer | durable study; validate on target tasks |
| TUC-008 | empirical | A one-site N=21 novice-programmer study observed that producing a working program could coexist with metacognitive difficulty and an illusion of competence for some participants. Output success is therefore not sufficient evidence of calibrated understanding in that setting. | `PRATHER-WIDENING-GAP-ICER-2024` | medium; small educational sample | durable study; replication and target-user transfer open |
| TUC-009 | empirical | In two small studies of marketing/sales professionals evaluating AI-generated data analyses, critical flaws were inconsistently detected even after warnings, incentives, method restatement, and structured explanations. This is direct but early preprint evidence for a particular business-analysis task, not a universal non-engineer limitation. | `VIRK-NONPROGRAMMER-CODE-2025` | medium-low | review after peer review/replication |
| TUC-010 | empirical | Appropriate reliance can be measured separately as accepting correct AI advice and retaining or escalating a correct judgment when AI advice is wrong. A 200-participant non-coding experiment found that explanations did not uniformly improve both axes, so explanation presence or stated trust alone is not a sufficient comprehension measure. | `IUI-APPROPRIATE-RELIANCE-2023` | medium-high for construct; coding transfer open | validate with seeded coding decisions |
| TUC-011 | empirical | In accessibility-specific novice-developer studies, an embedded scaffold that supplied safe defaults, identified relevant errors, and reminded users of manual validation improved accessible UI outcomes. This supports testing task-specific scaffolds and their resulting evidence rather than assuming all procedural guidance helps. | `CODEA11Y-CHI-2025` | medium-high in domain; low for general harness transfer | durable study; component-level replication required |
| TUC-012 | normative | NIST's GenAI profile recommends representative in-context user populations for risk evaluation, separating human proficiency tests from GAI capability tests, user-testing instructions, and avoiding extrapolation from narrow anecdotal assessments. These are suggested risk-management actions and support measuring the user and agent separately. | `NIST-GAI-600-1` | high for profile guidance | review on profile revision |

## Capability axes

| Axis | C0 — needs translation | C1 — can choose with plain evidence | C2 — can independently verify |
|---|---|---|---|
| Outcome expression | goal/examples only | acceptance outcomes and priorities | formal requirements/tradeoffs |
| Domain decision | cannot decide | owns business/content decision | can model edge cases and policy |
| Evidence comprehension | pass/fail only | understands what ran, failed, and remains unknown | audits tests, logs, and source scope |
| Technical verification | cannot inspect code/shell | can reproduce guided checks | independently reviews implementation |
| Risk comprehension | needs consequence translation | can choose after concrete impact/recovery preview | can threat-model controls |
| Operational responsibility | cannot monitor/respond | can act on plain alerts/runbooks | can diagnose and operate systems |

Capability is task-specific: one person can be C2 in domain decisions and C0 in security. A harness should record
the relevant axis rather than assign one global “beginner/expert” label.

## Harness consequences

- Ask the user for outcomes, irreversible preferences, business rules, and values—not implementation trivia.
- Convert technical alternatives into consequence, evidence, reversibility, and cost.
- Never treat approval as informed when the user cannot explain the consequence being approved.
- Do not infer calibrated reliance from satisfaction, trust ratings, or successful output. Test both correct agent
  guidance and seeded incorrect guidance at decision points with an objective oracle.
- Replace unavailable human technical review with stronger isolation and tests, while stating that they are not
  equivalent to accountable expert review.
- Default production, credentials, money, publishing, and destructive actions to bounded execution plus a human
  decision; do not hand raw technical commands to C0/C1 users as the explanation.

## Research still required

Run formative observation and task tests across at least three target profiles, then a separate pilot and
confirmatory study. Measure whether users can state acceptance outcomes, distinguish passed from unverified work,
accept correct guidance, reject or escalate seeded incorrect guidance, understand a risk preview, and execute a
recovery path. Determine confirmatory sample size and numerical thresholds from the pilot's baseline incidence and
precision target; do not reuse pilot participants or task instances to claim confirmation. This document defines
the axes; it does not claim population prevalence or prescribe a fixed sample size.

## Sources

- `EUSE-STATE-OF-ART` — https://www.cs.cmu.edu/~cscaffid/old/papers/Ko2009EndUserSoftwareEngineering.pdf
- `LCNC-ADOPTION-SLR-2024` — https://www.sciencedirect.com/science/article/pii/S0164121224003443
- `LOVABLE-SECURE-2025` — https://lovable.dev/blog/secure-vibe-coding
- `REPLIT-SECURE-2025` — https://replit.com/blog/doubling-down-on-our-commitment-to-secure-vibe-coding
- `ANTHROPIC-CONTAINMENT-2026` — https://www.anthropic.com/engineering/how-we-contain-claude
- `IUI-APPROPRIATE-RELIANCE-2023` — https://doi.org/10.1145/3581641.3584066
- `VIRK-NONPROGRAMMER-CODE-2025` — https://arxiv.org/abs/2508.06484
- `NGUYEN-CODELLM-CHI-2024` — https://doi.org/10.1145/3613904.3642706
- `PRATHER-WIDENING-GAP-ICER-2024` — https://arxiv.org/abs/2405.17739
- `CODEA11Y-CHI-2025` — https://doi.org/10.1145/3706598.3713335
- `NIST-GAI-600-1` — https://doi.org/10.6028/NIST.AI.600-1
