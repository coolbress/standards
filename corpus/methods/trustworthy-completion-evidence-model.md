---
id: trustworthy-completion-evidence-model
title: "Trustworthy Completion, Assurance, and Appropriate Reliance Evidence Model"
kind: reference
status: verified
last_updated: "2026-08-02"
evidence_track: lit
freshness: versioned
review_due: "2027-02-02"
sources: [NIST-SP800-160V1R1, NIST-SSDF-1.1, NIST-GAI-600-1, IUI-APPROPRIATE-RELIANCE-2023, VIRK-NONPROGRAMMER-CODE-2025, NGUYEN-CODELLM-CHI-2024, PRATHER-WIDENING-GAP-ICER-2024, CODEA11Y-CHI-2025]
---

# Trustworthy Completion, Assurance, and Appropriate Reliance Evidence Model

## Decision question and scope

What evidence supports evaluating a coding harness for a non-engineer by more than artifact quality or task
completion? This document covers software assurance, human reliance on imperfect AI advice, and empirical studies
of non-programmers or novice programmers using code-generating AI. It does **not** establish that one intervention
or numerical effect transfers to goppi, production software, all non-engineers, or every project archetype.

## Claim register

| Claim ID | Class | Claim and scope | Evidence | Confidence | Valid as of / expiry |
|---|---|---|---|---|---|
| TCM-001 | definition | NIST SP 800-160 Vol. 1 Rev. 1 defines assurance as grounds for justified confidence that a claim has been or will be achieved, obtained through techniques and methods that generate credible evidence. It defines assurance evidence as information used to substantiate decisions about assurance, trustworthiness, and risk. | `NIST-SP800-160V1R1` | high for NIST's security-engineering context | versioned; review on NIST revision |
| TCM-002 | definition | In the same NIST publication, an assurance case is a reasoned, auditable artifact linking claims, systematic argumentation, evidence, and explicit assumptions. This supports claim-to-evidence traceability; it does not make an artifact correct merely because a case was written. | `NIST-SP800-160V1R1` | high for definition; final sentence is bounded interpretation | versioned; review on NIST revision |
| TCM-003 | normative | NIST's GenAI profile recommends measuring performance or assurance under conditions similar to deployment, documenting limits of generalization, avoiding extrapolation from narrow anecdotal assessments, testing user instructions, using representative in-context user populations, and including incident response, recovery, and change management in monitoring. These are suggested actions, not universal mandatory controls. | `NIST-GAI-600-1` | high for what the profile recommends | review on profile revision |
| TCM-004 | empirical | In a 200-participant deception-detection experiment, Schemmer et al. operationalized reliance on two axes: following correct AI advice and retaining a correct initial judgment when AI advice is wrong. In that task, explanations increased relative correct AI reliance but did not significantly improve correct self-reliance; higher trust was associated with lower correct self-reliance. The task was not software development. | `IUI-APPROPRIATE-RELIANCE-2023` | medium-high within the sampled task | durable study; transfer to coding must be tested |
| TCM-005 | empirical | A 2025 preprint studied marketing/sales professionals evaluating natural-language explanations of flawed AI-generated data analyses: an initial n=10 study found no safety-critical flaw was detected consistently, and a second n=18 study found structured steps and alternatives had positive but inconsistent effects. Participants were warned, asked to restate methods, and incentivized; the small samples, preprint status, hidden code, and data-analysis domain prevent broad generalization. | `VIRK-NONPROGRAMMER-CODE-2025` | medium-low; direct target-population signal but early and narrow | review after peer review or replication |
| TCM-006 | empirical | A CHI 2024 controlled study of 120 beginning programmers across three institutions found difficulty writing and revising prompts for problems at their demonstrated skill level even with automatic correctness feedback. The reported mean eventual success was 57% and mean pass-at-first-attempt was 24%. Participants had passed an introductory course, so this is not a sample of people with no programming experience. | `NGUYEN-CODELLM-CHI-2024` | high within the study design; low for complete-novice transfer | durable study; transfer remains open |
| TCM-007 | empirical | In a one-site observational lab study of 21 novice programming students using generative-AI tools, 20 produced a working program, while the researchers observed metacognitive difficulties and an illusion of competence among some struggling participants. The small, educational, single-task study shows that output completion and calibrated understanding can diverge; it does not estimate prevalence among non-engineer project owners. | `PRATHER-WIDENING-GAP-ICER-2024` | medium within sample; low for population transfer | durable study; replication preferred |
| TCM-008 | empirical | CodeA11y used a 16-person formative study and a separate controlled evaluation with 20 novice developers. In the accessibility-specific tasks, an embedded scaffold that supplied accessible defaults, identified relevant errors, and reminded users of manual validation improved accessible UI outcomes. This supports testing risk-specific, evidence-producing scaffolds rather than assuming generic process prompts work. | `CODEA11Y-CHI-2025` | medium-high for accessibility tasks; low for broad harness transfer | durable study; test each goppi control separately |
| TCM-009 | synthesis | The evidence supports keeping at least three distinct evaluation objects: the artifact's objective result, the evidence that justifies completion claims, and the user's ability to accept correct guidance while detecting or safely deferring incorrect guidance. Recovery and burden are additional lifecycle and usability guardrails. No cited source supplies a universal weighting or worth threshold for these objects. | `NIST-SP800-160V1R1`; `NIST-GAI-600-1`; `IUI-APPROPRIATE-RELIANCE-2023`; `PRATHER-WIDENING-GAP-ICER-2024` | high for separation; no confidence claimed for weights | validate with goppi target users and tasks |
| TCM-010 | synthesis | A development activity is not assurance evidence merely because it occurred. For evaluation, it must produce information relevant to a stated claim, decision, risk, or recovery path. NIST SSDF examples such as release-integrity information, provenance, archived releases, and auditable design/risk records illustrate evidence-producing practices; their security scope must not be silently expanded into a universal software-process mandate. | `NIST-SP800-160V1R1`; `NIST-SSDF-1.1` | high for the claim/evidence distinction; medium for general process application | review with each archetype's acceptance surface |

## What this closes—and what it does not

The old output-only comparison is construct-incomplete: a correct artifact without inspectable completion evidence
can still leave a target user unable to distinguish success from a false done-claim. Conversely, an agent that stops
at `UNVERIFIED` or `BLOCKED` before causing harm may be more trustworthy than one that produces more files and
declares success.

This evidence does **not** prove that goppi works. It justifies a testable model in which:

1. objective result quality remains necessary;
2. completion claims require claim-linked evidence and explicit unknowns;
3. reliance is tested with both correct and deliberately incorrect agent guidance;
4. failure detection and recovery are scored separately from task completion; and
5. every process component must demonstrate an observable contribution or be narrowed/deleted.

## Search and selection record

- Search date: 2026-08-02.
- Query clusters: `NIST software assurance justified confidence evidence`; `NIST AI RMF human-AI
  configuration over-reliance representative users`; `appropriate reliance AI advice explanations empirical`;
  `non-programmers assessing AI-generated code`; `beginning programmers code LLM controlled study`;
  `novice generative AI programming metacognition`; `coding assistant scaffold controlled study`.
- Included: current government publications; peer-reviewed original studies with described samples and tasks;
  one directly relevant preprint retained with an explicit evidence downgrade.
- Excluded from load-bearing claims: news summaries, individual vibe-coding incidents, vendor outcome marketing,
  Reddit anecdotes, and papers without a target-user, reliance, or assurance connection.
- Negative evidence: no retrieved study directly tests a full lifecycle harness with people who have never run a
  software project. There is therefore no empirical basis here for a universal 50%/30% worth threshold or for
  claiming that professional-process conformance alone creates value.

## Sources

- `NIST-SP800-160V1R1` — https://doi.org/10.6028/NIST.SP.800-160v1r1
- `NIST-SSDF-1.1` — https://doi.org/10.6028/NIST.SP.800-218
- `NIST-GAI-600-1` — https://doi.org/10.6028/NIST.AI.600-1
- `IUI-APPROPRIATE-RELIANCE-2023` — https://doi.org/10.1145/3581641.3584066
- `VIRK-NONPROGRAMMER-CODE-2025` — https://arxiv.org/abs/2508.06484
- `NGUYEN-CODELLM-CHI-2024` — https://doi.org/10.1145/3613904.3642706
- `PRATHER-WIDENING-GAP-ICER-2024` — https://arxiv.org/abs/2405.17739
- `CODEA11Y-CHI-2025` — https://doi.org/10.1145/3706598.3713335
