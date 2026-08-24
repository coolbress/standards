# Retrieval model A/B raw result

- arm: before
- repetition: 2
- agent task: retrieval_before_2
- host: Codex
- exact model/version/config: `UNAVAILABLE — collaboration runtime does not expose it`
- prompt reference: `../RETRIEVAL-MODEL-AB-PROTOCOL.md#exact-trial-prompt`

ARM=before | REP=2

Q1 | Minimum-permission CI is stated as least-privilege token permissions, with a default read-only `GITHUB_TOKEN`; immutable action pinning is stated as pinning GitHub Actions to a commit SHA. OpenSSF Scorecard provides the direct evidence categories (`Token-Permissions`, `Pinned-Dependencies`), with observed strong adoption only 24–26% and 20–27%, respectively; NIST SSDF supplies the broader supply-chain posture. | `aspects/04-build-ci-engineering/04-build-ci-engineering--overview.md`; `aspects/09-application-security/09-application-security--overview.md` | both `verified`; updated 2026-07-05 and 2026-06-27 | https://securityscorecards.dev/ ; https://github.com/ossf/scorecard/blob/main/docs/checks.md ; https://csrc.nist.gov/pubs/sp/800/218/final | The corpus supports the controls and prevalence gap, but does not present causal evidence that these two GitHub-specific practices improve outcomes.

Q2 | Yes, as corpus-native verified evidence: the top-level Requirements & Planning document is marked `status: verified`, carries literature sources, and states high confidence. Its census support is explicitly bounded to planning-artifact presence; content rigor remains literature-grounded. | `aspects/01-requirements-planning/01-requirements-planning--overview.md`; `_schema.md` | `verified`; updated 2026-06-25. Schema defines verified as cited and cross-checked. | https://www.iso.org/standard/72089.html ; https://www.computer.org/education/bodies-of-knowledge/software-engineering ; https://arxiv.org/abs/1611.10288 | “Current” is supported only to the document’s 2026-06-25 freshness; artifact-presence census does not verify planning quality.

Q3 | The map is: normal-software floor, plus orchestration; prompt source/versioning; eval harness; MCP Tools/Resources/Prompts; skills/hooks/plugins/marketplace packaging; context and file-backed memory; cross-host adapters with schema validation; and prompt-injection/tool-sandbox security. | `aspects/27-ai-harness-archetype/27-ai-harness-archetype--overview.md` | `verified`, `census+lit`, high confidence; updated 2026-07-05; cites MCP spec revision 2025-11-25 and 200-repo/36-canonical census | https://modelcontextprotocol.io/specification ; https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills ; https://agents.md ; https://www.swebench.com/ | The component map is supported; no claim is made that one agent architecture is universally dominant.

Q4 | NOT FOUND as one integrated threat path. The corpus separately states: treat tool descriptions/annotations and inputs as untrusted; require consent before tool invocation or exposing user data; sandbox tool execution; keep secrets in a manager, never source, and rotate them; use least-privilege tokens and server-side deny-by-default authorization; gate scans in CI. | `aspects/27-ai-harness-archetype/27-ai-harness-archetype--overview.md`; `aspects/09-application-security/09-application-security--overview.md` | both `verified`; updated 2026-07-05 and 2026-06-27 | https://modelcontextprotocol.io/specification ; https://owasp.org/www-community/Threat_Modeling_Process ; https://csrc.nist.gov/pubs/sp/800/218/final | No opened document joins untrusted content → credential access → egress → filesystem/production authority → recovery into one modeled chain. Egress boundaries, filesystem authority, production blast radius, and recovery validation are therefore unsupported as an integrated control story.

Q5 | No. The locked taxonomy anchors SWEBOK v4, ISO/IEC/IEEE 12207:2017, and ISO/IEC 25010:2023—not SWEBOK V4.0a × 12207:2026 × 25010:2023. A newer draft fact log merely says a 2026 edition exists and summarizes it through secondary sources; it does not provide a 28-aspect crosswalk. | `TAXONOMY.md`; `aspects/28-implementation-process-workflow/sdlc-models--facts-2026-08.md` | taxonomy `locked`, updated 2026-06-27; fact log `draft`, updated 2026-08-02 | https://quality.arc42.org/standards/iso12207 ; https://blog.pacificcert.com/iso-iec-ieee-12207-standardizing-software-lifecycle-processes/ | No V4.0a mapping, no 12207:2026 clause-level mapping, and no licensed full-standard text is present. Complete clause-by-clause coverage cannot be verified from public/secondary summaries.

Q6 | The target-user model is stated as: a non-engineer may not know NFRs or acceptance criteria are askable, may be unable to articulate requirements, and needs a structured interview to supply that missing scaffolding. The corpus also says shipped spec-driven tools are predominantly engineer-facing and that true interview-first stopping systems are academic. | `aspects/01-requirements-planning/01-requirements-planning--overview.md`; `aspects/27-ai-harness-archetype/27-ai-harness-archetype--overview.md` | both `verified`; updated 2026-06-25 and 2026-07-05 | https://github.com/github/spec-kit ; https://kiro.dev/ ; https://arxiv.org/html/2605.16701 | These are literature/prior-art observations, not direct user research defining the intended user’s measured abilities. Transfer from RE studies/tool convergence to non-engineer coding-agent users is not established.

Q7 | The corpus does not present a validated solo scaling recipe. Google SRE guidance says humane 24/7 coverage under its 25% on-call rule needs at least eight people at one site; therefore the team rotation cannot literally scale to one operator. For a non-engineer, the synthesis says to surface the irreducible operational advisory and templates rather than fabricate live SLOs, on-call, or MTTR. | `aspects/20-operations-incident-reliability/20-operations-incident-reliability--overview.md`; `aspects/20-operations-incident-reliability/operations-sre--facts-2026-08.md` | aspect `verified`, updated 2026-06-25; facts log `draft`, updated 2026-08-02 | https://sre.google/sre-book/being-on-call/ ; https://sre.google/sre-book/service-level-objectives/ ; https://sre.google/sre-book/managing-incidents/ | Unsupported: a tested adaptation of escalation roles, paging burden, compensation, or 24/7 availability for a solo non-engineer.

Q8 | The inherited top-level Software Testing synthesis may be cited as corpus-verified; the newer 2026-08 facts appendix may not be represented as verified because its frontmatter remains `draft`, despite saying “session-lead verified” in its method. Strongest bounded conclusion: a test harness and CI test gate are a durable floor; use many lower-level tests and few E2E tests, coverage as a regression floor rather than a target, contract tests at independent boundaries, and quarantine flaky tests. | `aspects/08-software-testing/08-software-testing--overview.md`; `aspects/08-software-testing/testing--facts-2026-08.md` | aspect `verified`, updated 2026-06-25; facts log `draft`, updated 2026-08-02 | https://martinfowler.com/articles/practical-test-pyramid.html ; https://docs.pact.io/ ; https://testing.googleblog.com/2020/12/test-flakiness-one-of-main-challenges.html | Numerical claims unique to the draft facts log should not be promoted to verified synthesis without review.

Q9 | The corpus’s strongest rule is: official product documentation is authoritative for what a product exposes, configures, or prescribes; it is not by itself evidence that the practice is effective. Effectiveness requires outcome-bearing empirical literature or measurements, with objective signals and calibration. | `_schema.md`; `aspects/28-implementation-process-workflow/research-log.md` | both `verified`; updated 2026-06-25 and 2026-06-26 | https://dora.dev/devops-capabilities/process/working-in-small-batches/ ; https://arxiv.org/abs/2406.01297 | This product-doc-versus-efficacy distinction is not explicitly codified as a named rule; it is the bounded inference supported by the schema’s evidence discipline and the research log’s empirical-evidence practice.

Q10 | `lifecycle.md` is the navigation document connecting planning, foundation/build, implementation/verification, and release/operations through stage-to-aspect activation. Retirement is not explicit there; `TAXONOMY.md` only asserts that ISO 12207 Disposal was covered. For this answer I needed `INDEX.md` + `lifecycle.md` + `TAXONOMY.md`: 3 files, 22,674 bytes. | `INDEX.md`; `lifecycle.md`; `TAXONOMY.md` | `TAXONOMY.md` is `locked`, updated 2026-06-27; `lifecycle.md` is hand-maintained and notes its mode overlay was added 2026-07-02; INDEX has no status frontmatter | no external URL needed; internal navigation | No single opened navigation document explicitly maps retirement/disposal to an aspect, so the full six-part connection is only partially supported.

Files opened and exact `wc -c`:

```text
 11521 INDEX.md
 13639 matrix--facts-2026-08.md
 10023 aspects/04-build-ci-engineering/cicd-release--facts-2026-08.md
 15833 aspects/04-build-ci-engineering/04-build-ci-engineering--overview.md
 22691 aspects/01-requirements-planning/01-requirements-planning--overview.md
 11610 aspects/08-software-testing/08-software-testing--overview.md
 10490 aspects/08-software-testing/testing--facts-2026-08.md
 18082 aspects/27-ai-harness-archetype/27-ai-harness-archetype--overview.md
 13741 aspects/09-application-security/09-application-security--overview.md
  5943 TAXONOMY.md
  5210 lifecycle.md
 11650 aspects/20-operations-incident-reliability/20-operations-incident-reliability--overview.md
 12555 aspects/20-operations-incident-reliability/operations-sre--facts-2026-08.md
 19909 aspects/28-implementation-process-workflow/28-implementation-process-workflow--overview.md
 13178 _schema.md
 12549 aspects/28-implementation-process-workflow/sdlc-models--facts-2026-08.md
 13134 aspects/28-implementation-process-workflow/research-log.md
221758 total
```

Context-cost proxy: 17 files, 221,758 bytes. No files modified.
