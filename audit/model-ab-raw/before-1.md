---
arm: before
repetition: 1
agent_task: retrieval_before_1
host: Codex
model_version_config: "UNAVAILABLE — collaboration runtime does not expose it"
prompt_reference: ../RETRIEVAL-MODEL-AB-PROTOCOL.md#exact-trial-prompt
---

ARM=before | REP=1

Q1 | The corpus requires GitHub Actions pinned to full commit SHAs because tags are mutable, plus workflow-level minimal/`read-all` permissions. Supporting evidence is OpenSSF Scorecard’s Pinned-Dependencies and Token-Permissions checks; the parent synthesis reports pinning at 3.1/10 and treats both controls as the practical supply-chain floor. | `aspects/04-build-ci-engineering/04-build-ci-engineering--overview.md`; `aspects/04-build-ci-engineering/foundation-floor-artifact-checklist.md` | both `verified`; updated 2026-07-05 and 2026-06-27 respectively | OpenSSF Scorecard: https://github.com/ossf/scorecard/blob/main/docs/checks.md ; https://scorecard.dev/ ; SLSA v1.2: https://slsa.dev/spec/v1.2/build-track-basics | The opened documents assert tag mutability and default-token breadth but do not provide a direct GitHub Actions documentation citation for either detail.

Q2 | Yes, under the corpus’s own status rules, the top-level Requirements & Planning claim is verified evidence as of 2026-06-25. Its frontmatter says `status: verified`, and `_schema.md` defines verified as “cited + cross-checked”; the body describes it as literature-anchored and only partially censused. | `aspects/01-requirements-planning/01-requirements-planning--overview.md`; `_schema.md` | `verified`, last updated 2026-06-25 | SWEBOK v4: https://ieeecs-media.computer.org/media/education/swebok/swebok-v4.pdf ; ISO/IEC/IEEE 29148:2018: https://www.iso.org/standard/72089.html ; ISO/IEC 25010:2023: https://www.iso.org/standard/78176.html | “Current” is bounded to its 2026-06-25 update: the corpus states no expiry policy and the opened top-level document has no August 2026 re-verification.

Q3 | The map has two major planes: the normal-software floor—README, license, CI, tests, manifest and lockfile—and an additive harness-capability plane. The latter contains orchestration; versioned prompts and evals; MCP Tools/Resources/Prompts; skills, hooks, plugins and marketplace packaging; explicit context/memory; cross-host adapters and schemas; and prompt-injection/tool-sandbox security. | `aspects/27-ai-harness-archetype/27-ai-harness-archetype--overview.md` | `verified`, updated 2026-07-05; `census+lit`, based on a 200-repository plus 36-canonical-harness census | MCP: https://modelcontextprotocol.io/specification ; Agent Skills: https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills ; AGENTS.md: https://agents.md ; SWE-bench: https://www.swebench.com/ | Census supports component prevalence, not the effectiveness of the complete plane architecture as an integrated system.

Q4 | No complete integrated threat path is documented. A partial chain is supported: untrusted input/tool metadata can reach arbitrary-code-capable tools; controls include validation at trust boundaries, avoiding dangerous workflow patterns, secrets in a manager rather than source, rotation, least-privilege CI tokens, explicit consent before tool invocation or exposing user data, and sandboxing. | `aspects/09-application-security/09-application-security--overview.md`; `aspects/27-ai-harness-archetype/27-ai-harness-archetype--overview.md` | both `verified`; updated 2026-06-27 and 2026-07-05 | OWASP Threat Modeling: https://owasp.org/www-community/Threat_Modeling_Process ; NIST SSDF: https://csrc.nist.gov/pubs/sp/800/218/final ; MCP: https://modelcontextprotocol.io/specification | Unsupported: one evidence-backed end-to-end chain covering content → credential theft → network egress → filesystem/production authority → recovery; explicit egress-deny controls; concrete filesystem/production capability boundaries; and tested recovery for this threat.

Q5 | No. The locked taxonomy claims broad convergence, but its frontmatter anchors SWEBOK v4, ISO/IEC/IEEE 12207:2017 and ISO/IEC 25010:2023—not SWEBOK V4.0a × 12207:2026 × 25010:2023. The August SDLC note says a 2026 edition was announced and summarizes four process categories, but supplies no 28-aspect crosswalk. | `TAXONOMY.md`; `aspects/28-implementation-process-workflow/sdlc-models--facts-2026-08.md` | taxonomy `locked`, updated 2026-06-27; SDLC note `draft`, updated 2026-08-02 | ISO 12207 summaries: https://quality.arc42.org/standards/iso12207 and https://blog.pacificcert.com/iso-iec-ieee-12207-standardizing-software-lifecycle-processes/ | Licensed-standard limitation: the opened corpus contains no licensed normative ISO 12207:2026 text and relies on secondary summaries. V4.0a-specific mapping is NOT FOUND.

Q6 | The corpus characterizes the target user as someone with a vague idea who may not know that NFRs or acceptance criteria are askable and cannot precisely articulate requirements. Evidence instead concentrates on the deficiencies of shipped spec tools and on academic interview systems: adaptive questioning, ≤2 questions per turn, serial context and ISO-29148 completeness checks. | `aspects/01-requirements-planning/01-requirements-planning--overview.md`; `aspects/01-requirements-planning/elicitation-prior-art.md` | both `verified`; updated 2026-06-25 and 2026-06-26 | iReDev: https://arxiv.org/abs/2507.13081 ; LLMREI: https://arxiv.org/abs/2507.02564 ; Elicitron: https://arxiv.org/abs/2404.16045 | No direct target-user capability study was found. Transfer from academic requirements-elicitation results to non-engineers using coding agents—or to downstream coding quality—is not established.

Q7 | The corpus imports team-scale SRE practice, not a validated solo adaptation. It states that humane 24/7 coverage under Google’s ≤25%-on-call rule requires at least eight people at one site. For a non-engineer, the top-level synthesis says to scaffold runbook/postmortem templates and surface the irreducible advisory about SLOs, incident response and DR, but not fabricate live SLO/on-call/MTTR capability. | `aspects/20-operations-incident-reliability/20-operations-incident-reliability--overview.md`; `aspects/20-operations-incident-reliability/operations-sre--facts-2026-08.md` | top-level `verified`, updated 2026-06-25; facts log `draft`, updated 2026-08-02 | Google SRE on-call: https://sre.google/sre-book/being-on-call/ ; incident management: https://sre.google/sre-book/managing-incidents/ ; postmortems: https://sre.google/sre-book/postmortem-culture/ | A safe, humane and effective solo non-engineer on-call model is NOT FOUND/UNSUPPORTED.

Q8 | Yes, the inherited top-level Software Testing synthesis may be cited as corpus-labeled verified evidence as of 2026-06-25. The strongest bounded conclusion is that an automated test harness and server-side CI test gate are a durable floor, with many lower-level tests and few high-cost E2E tests; the corpus reports test-framework presence at 90% in its N=938 census. | `aspects/08-software-testing/08-software-testing--overview.md`; `aspects/08-software-testing/testing--facts-2026-08.md` | top-level `verified`, updated 2026-06-25; newer facts log `draft`, updated 2026-08-02 | Fowler test pyramid: https://martinfowler.com/articles/practical-test-pyramid.html ; Google E2E guidance: https://testing.googleblog.com/2015/04/just-say-no-to-more-end-to-end-tests.html | The August refresh is not verified. Exact layer ratios, universal coverage thresholds, TDD effectiveness and retry-versus-quarantine policy should not be presented as a refreshed verified synthesis.

Q9 | Source authority and claim type are separate. Official/first-party product documentation can establish what a product defines, exposes or recommends; it does not by itself establish that the practice improves outcomes. Effectiveness requires empirical `[data]`, independently cross-checked literature, or census evidence rather than a vendor/product `[claim]`. | `_schema.md`; `aspects/08-software-testing/testing--facts-2026-08.md` | `_schema.md` `verified`, updated 2026-06-25; testing facts `draft`, updated 2026-08-02 | Example empirical source: Rafique & Mišić meta-analysis, https://link.springer.com/article/10.1007/s10664-016-9490-0 ; example first-party guidance: https://testing.googleblog.com/2020/08/code-coverage-best-practices.html | No single sentence in the opened files states this generalized rule verbatim; it follows directly from the corpus’s separate evidence tags and the facts log’s `[definition/regulation]` / `[data]` / `[claim]` classification.

Q10 | `lifecycle.md` is the navigation overlay connecting Planning, Foundation/Build, Implementation/Verification, and Release & Operations, while firing cross-cutting disciplines at every stage. Retirement is not an explicit lifecycle stage there; only `TAXONOMY.md` says ISO 12207 Disposal was mapped somewhere in the 28-aspect set. For this answer I needed INDEX plus two documents: `lifecycle.md` and `TAXONOMY.md`. | `lifecycle.md`; `TAXONOMY.md` | lifecycle has no frontmatter status/date; footer says the mode overlay was added 2026-07-02. Taxonomy `locked`, updated 2026-06-27 | No external URL needed for the navigation finding | A navigation path explicitly naming retirement/disposal is NOT FOUND.

Files opened and byte counts:

```text
 11521 INDEX.md
 13178 _schema.md
  5943 TAXONOMY.md
  5210 lifecycle.md
 13639 matrix--facts-2026-08.md
 22691 aspects/01-requirements-planning/01-requirements-planning--overview.md
 16462 aspects/01-requirements-planning/elicitation-prior-art.md
 15833 aspects/04-build-ci-engineering/04-build-ci-engineering--overview.md
 12611 aspects/04-build-ci-engineering/foundation-floor-artifact-checklist.md
 11610 aspects/08-software-testing/08-software-testing--overview.md
 10490 aspects/08-software-testing/testing--facts-2026-08.md
 13741 aspects/09-application-security/09-application-security--overview.md
 11650 aspects/20-operations-incident-reliability/20-operations-incident-reliability--overview.md
 12555 aspects/20-operations-incident-reliability/operations-sre--facts-2026-08.md
 18082 aspects/27-ai-harness-archetype/27-ai-harness-archetype--overview.md
 12549 aspects/28-implementation-process-workflow/sdlc-models--facts-2026-08.md
207765 total
```

Context-cost proxy: 16 files, 207,765 bytes. No files were modified.
