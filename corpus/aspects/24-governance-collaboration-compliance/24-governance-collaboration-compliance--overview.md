---
id: aspect-24-governance-collaboration-compliance
title: "Governance, Collaboration & Compliance"
group: "G — Cross-cutting Practice & Governance"
kind: cross-cutting
gated_archetypes: []
cross_cutting: true
lifecycle_stages: ["all"]
anchors: ["ISO-12207-2026-catalog-scope", "SWEBOK-KA9", "SWEBOK-KA14", "Team-Topologies"]
evidence_track: census+lit
status: review-needed
last_updated: "2026-07-07"
sources:
  - "https://www.contributor-covenant.org/version/2/1/code_of_conduct/"
  - "https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners"
  - "https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions"
  - "https://adr.github.io/madr/"
  - "https://scorecard.dev/"
  - "https://teamtopologies.com/key-concepts"
  - "https://www.computer.org/education/bodies-of-knowledge/software-engineering"
  - "https://www.iso.org/standard/90219.html"
claim: "Senior teams make collaboration legible — decision rights recorded as ADRs, review/ownership enforced by branch protection + CODEOWNERS, a CoC/license/security posture set day-one — and treat org structure (Conway/Team Topologies) and compliance (SOC2/ISO27001) as design inputs, not afterthoughts; gingoa scaffolds the team-collaboration file set and records its own decisions as MADR ADRs."
maps_from: ["census-data/census-governance", "census-data/census-governance-floor"]
---

> **Standard (claim):** Senior teams make collaboration **legible** — decision rights recorded (ADRs), review + ownership **enforced** (branch protection + CODEOWNERS), CoC/license/security posture set day-one — and treat org structure (Conway/Team Topologies) and compliance (SOC2/ISO27001) as design inputs, not afterthoughts.
> **Evidence:** census+lit · **Confidence:** high (governance file set, review) / medium (compliance — context-gated) · **Kind:** cross-cutting · **Stage:** all

**Seed sub-aspects:** `issue / triage` · `contribution policy / CoC` · `decision rights (RACI/ADR)` · `ethics / legal / IP / export` · `compliance / audit (SOC2/ISO27001)` · `Conway / team-topology (team-gated)` · `quality planning (KA12)` · `internal/published boundary — self-contained remote artifacts`

## Sub-documents
- [`solo-governance-handover--facts-2026-08.md`](solo-governance-handover--facts-2026-08.md) — *research-log (ko)* — 2026-08 facts-only pass (R3-4): **개발자 인계·온보딩에 공식 표준이 팀 규모와 무관하게 존재하지 않는다**(확인된 부정 결과) · ISO/IEC/IEEE 15289 정보 항목 · GitHub 커뮤니티 항목은 전부 "권장". "1인이라 기각"이 아니라 "규범 부재"가 정확한 진술임을 확인.

- [issue-pr-writing-conventions.md](issue-pr-writing-conventions.md) — the **작성법 (how-written)** layer beneath the section/type censuses: field TYPE (textarea 54% dominant), required-by-type (dropdown 73 / input 65 / textarea 57 ↔ checkboxes 3.8), help-text near-universal (87%), preflight 22% / in-form CoC 6%, PR checklist **empty `- [ ]` 62%** + HTML-comment guidance 70% + **type-of-change minority 12% (85% checkbox when present, free-text 1.7%)**. The writing-method inputs to the tiered template standard.
- [`roles-teams--facts-2026-08.md`](roles-teams--facts-2026-08.md) — *research-log (ko)* — 2026-08 facts-only pass: PM/PO/ProjM role definitions · public career ladders (Dropbox/GitLab) · Team Topologies · Conway 1968 · two-pizza · Spotify-model authors' caveat · QSM team-size data · dual-track (also serves aspect-23).

## What professional engineers do

- **Decision rights are recorded, not tribal.** Real architectural decisions get a one-page ADR (status / context / decision / consequences) at a canonical path (`docs/adr/`), MADR-formatted. The point is a durable rationale future maintainers can read — decision-record only on a *real* decision, not every change. `[lit]` RACI/ownership clarifies *who decides vs is consulted*; in OSS this collapses into maintainer + CODEOWNERS. `[census]` ADR adoption is low in the wild (2–4%) but rising year-over-year.
- **Ownership + review are enforced by the platform, not by hope.** `CODEOWNERS` auto-requests the right reviewers; **branch protection** makes review + green CI a merge precondition. Mature teams gate `main` so no unreviewed code lands. `[census]` Code-Review and Branch-Protection are the *weakest* enforced controls in the wild (review 41% strong, branch-protection 13% strong) — exactly the senior practice a non-engineer would not think to demand.
- **Contribution policy is explicit.** `CONTRIBUTING.md` (how to build/test/PR), `CODE_OF_CONDUCT.md` (Contributor Covenant is the de-facto OSS standard), `SECURITY.md` (disclosure path), and issue/PR templates make collaboration onboarding deterministic. `[census]` CONTRIBUTING ~64–73%, CoC ~35–43% (public-OSS-gated), SECURITY ~54–67%.
- **Legal / IP / licensing is settled day-one.** A `LICENSE` file (SPDX-identified) is near-universal; dependency-license compatibility, IP assignment (CLA/DCO), and — for some domains — export-control posture are decided before code accrues. `[census]` License presence ~99% — the single most-universal governance artifact.
- **Compliance is treated as a design input where it applies.** SOC2 / ISO 27001 / ISO 27017 shape access control, audit logging, change-management evidence (PR + review trail *is* the change-management artifact), and dependency/supply-chain hygiene. Senior teams wire the *evidence trail* into normal flow (signed commits, immutable CI logs, pinned deps) rather than retrofitting an audit. `[lit, normative]` OpenSSF Scorecard operationalizes many of these as scored, automatable checks.
- **Org structure is an explicit lever (Conway / Team Topologies).** Conway's Law: system architecture mirrors comms structure; the **inverse Conway maneuver** designs teams to *get* the architecture you want. Team Topologies names 4 team types (stream-aligned, platform, enabling, complicated-subsystem) + 3 interaction modes (collaboration, X-as-a-Service, facilitation). `[lit]` This is *team-gated* — it activates only when there is more than one team; solo/small repos skip it but the artifact that encodes it (CODEOWNERS, module boundaries) still applies.
- **Quality planning (SWEBOK KA management).** Definition of Done, review checklists, coverage thresholds, and a defect-triage policy are *planned*, not improvised. Governance ties quality gates to merge rights.
- **The internal/published boundary is deliberate — and remote artifacts are self-contained.** Two axes: *whether to do the activity* (plan, ADRs, threat models, design notes) follows the literature; *whether it goes on the remote* follows what real repos expose — planning/design docs are **local/team by default** (census 13–19% publish them). The senior corollary teams enforce: **remote-visible collaboration artifacts — issues, PRs, commit messages, issue/PR templates, code comments — are self-contained.** They describe the change and the product so a reader with *only the remote* can follow, and never cite local-only internal docs (ADR-NNNN, the build plan, design notes) or internal-process jargon (a team's stage/pipeline shorthand) — those are **dangling references** on the remote that also **leak internal structure**. The executable projection publishes; the internal thinking stays local. `[lit]` docs-as-code + security-confidentiality (a published threat model / secret topology aids attackers) · `[census]` planning-doc publish 13–19% · `[inferred]` the self-contained-artifact corollary.

## Evidence (lit + census)

**[lit]**
- **Contributor Covenant 2.1** — de-facto OSS Code of Conduct. → contributor-covenant.org
- **ADR** (Nygard 2011) + **MADR** — one-page decision records; canonical `docs/adr/`. → cognitect.com, adr.github.io/madr
- **GitHub CODEOWNERS / branch protection** — platform-enforced review + ownership. → docs.github.com
- **OpenSSF Scorecard** — automatable governance/security checks (Branch-Protection, Code-Review, Signed-Releases…). → scorecard.dev
- **Team Topologies** (Skelton & Pais) — 4 team types + 3 interaction modes; inverse Conway maneuver. → teamtopologies.com
- **ISO/IEC/IEEE 12207:2026** — 현행 ISO catalog의 공개 범위는 조직·프로젝트가 software life-cycle
  process를 정의·통제·개선하는 데 사용할 수 있는 공통 framework임을 뒷받침한다. 세부 process 명칭과
  clause-level governance 대응은 유료 본문 미확보로 **INCONCLUSIVE**다. → iso.org/standard/90219
- **SWEBOK v4** — KA Management (quality planning, group dynamics) + KA Professional Practice (ethics, legal, professionalism). → computer.org
- **Buchgeher et al. 2023** (IEEE Access, 900+ repos) — ADR adoption low but rising; Nygard template dominant. → corroborates the 2–4% census.

**[census]** (429-repo governance survey, OpenSSF Scorecard 59% coverage, recency-weighted `w=0.5^(age/2yr)`)

| Control | n | %strong (uni/wgt) | Read |
|---|---|---|---|
| License | 252 | 99 / 100 | universal — settle day-one |
| Maintained | 252 | 84 / 83 | active-maintenance signal |
| Code-Review | 252 | 41 / 41 | **weak in the wild** — harness must lift |
| Branch-Protection | 118 | 13 / 13 | **weakest enforced control** |
| Security-Policy (SECURITY.md) | 252 | 67 / 63 | majority but not universal |
| Signed-Releases | 103 | 15 / 17 | rare; supply-chain-gated |

- Planning/decision artifacts: **ADR dir 2–4%**, RFC 1–2%, design-doc 11–16%, any-planning-artifact 13–19%. ADR is rare-but-senior (publish-axis: *not* public-default).
- Foundation files (from `census-expanded`): CONTRIBUTING 64–73%, CoC 35–43% (public-OSS-gated), CODEOWNERS 32–33% (monorepo/multi-team-gated), PR-template 53–58%.
- **Issue/PR convention census** (500 top-starred manifest-filtered repos, 2026-06-26 — `census-data/census-issue-pr/`): issue templates **78%** (YAML **forms 54%** > legacy `.md` 32%; `config.yml` 58%); **issue-title Conventional-Commits ≈ 2%** → issue titles are **plain summaries** (~31% use a `[tag]`/`word:` prefix; avg ~60 chars); **PR-title Conventional-Commits** strict (≥70% of titles) **34%** · partial (≥30%) 57% · mean 0.45 → a *substantial-but-minority* practice, **not** a census-majority. Standard **bug-form fields**: steps-to-reproduce(111) · additional-context(100) · expected-behavior(92) · description · environment/version/OS · logs. Standard **PR-body sections**: checklist(33) · description/summary · type-of-change · testing · related-issue. *(PR-template presence read 35% here but is case-sensitivity-undercounted — defer to the 53–58% above.)*
- **↑ Widened to N=2000** (2026-07-05 — `census-data/census-issue-pr/{census2k.py,records-2k.json,stats-2k.json}`, GraphQL-batched, global top-2000-by-stars *software* repos; star floor 8.2k). **The section/field rankings that ground the template standard HOLD at 4× the sample — confirmed, not revised.** Standard **bug fields**: additional-context(247, now **#1**) · steps-to-reproduce(227) · expected-behavior(210) · description(198) · describe-the-bug/version/OS · logs; **feature fields**: proposed-solution(51) · alternatives-considered(48) · additional-context. Standard **PR-body sections**: description(100) · checklist(78) · summary(39) · type-of-change(28) · testing(23) · related-issue(24). **Presence rates fall at the wider N** — *presence measured tree-based (case-insensitive recursive-tree regex, census-expanded-comparable; `repair` mode)*: issue templates 78%→**68%**, YAML forms 54%→**31%**, config 58%→**36%**, PR-template ~53%(n=938)→**44%**, PR-title-CC mean 0.45→**0.33**, issue-title-CC ≈**1%**, avg len ~54 — *expected*, since convention adoption correlates with stars and the wider net reaches less-governed repos. *(The earlier exact-case harvest read PR-template 25% — a case/location undercount that `repair` corrected to 44% over 524 fixed flags.)* **Two refinements:** (i) **YAML forms ≈ legacy `.md`** at 2000 (31% vs 34%) — forms lead only among the very-top repos, though they remain the modern GitHub-recommended direction gingoa ships; (ii) additional-context becomes the **single most-common issue field** (validates shipping it on the bug + feature forms). **Net: the census grounds a TWO-form baseline (bug + feature) + the Summary/Type-of-change/Testing/Checklist PR body as the 2000-repo standard; `task` is a deliberate gingoa add-on, NOT a census-standard form — see the form-type enrichment below.**
- **↳ Issue-FORM-TYPE enrichment** (2026-07-05 — `census-data/census-issue-pr/{taskform.py,taskform-records.json,taskform-stats.json}`; re-harvested `.github/ISSUE_TEMPLATE/` for the **629** N=2000 repos that ship ≥1 YAML form, classifying each form by filename+`name:` — since the main census kept field-labels but discarded form file-names/titles, it couldn't answer "what THIRD forms do repos ship, and is `task` one?"). **The two-form baseline is confirmed and `task` is NOT a standard form.** Of the 629 form-repos: **bug 94.4%** · **feature 72.2%** — the canonical pair (= GitHub's two built-in defaults). Everything else is a per-project add-on: **38.3% ship *some* extra form beyond bug+feature, but it fragments** — idiosyncratic 'other' **21.1%** · docs **14.6%** · question/support **9.4%** · perf 1.7% · **task-class only 4.1% (26 repos**; task·chore·maintenance·refactor·tech-debt·tracking·epic·cleanup) · security 0.5%. Auditing 'other' for missed task-ish forms (Work-in-Progress, Roadmap-Tracker, Migration, Deprecation — each n=1, idiosyncratic) lifts task-class to at most ~5%. **Key finding: the wild has NO standardized name for a non-bug/feature engineering-work form** — the 26 that exist span *Chore / Maintenance · Refactor · Tracking Issue · Work Item · Housekeeping · Repository maintenance · Task*, all low-N. **Verdict on gingoa's `task.yml`:** the census justifies (a) that adding a 3rd form is common practice (38%) and (b) that a task/chore form is an *attested-but-minority* pattern — it does **NOT** justify `task` as an industry standard. gingoa's adoption is a **principled gingoa-internal design choice** (its pr-title gate enforces 11 Conventional-Commit types + blank issues are disabled → a docs/chore/refactor/ci catch-all form is needed), correctly labelled in `docs/specs/scaffold/spec.md` as a *shipped common extra, not floor-required*. → feeds [[template-standard-dogfood-gap]].
- **Governance-floor PRESENCE vs ADEQUACY** (Tier-1 method pilot, 2026-07-05 — `census-data/census-gov-adequacy/`, same 2000-repo software set, **content-parsed** not presence-only): a presence census **overstates** the floor. **CONTRIBUTING present 62% but only 41% adequate** (67% of present — **1 in 3 is a stub** lacking build/test *and* PR-flow, e.g. a bare link to a website); **LICENSE 91%→78% recognized** (~13pp custom/stub/non-SPDX). By contrast **SECURITY 34%→31%** (92% of present adequate), **CoC 33%→27%** (83%; Contributor-Covenant = 25% of all repos), **CODEOWNERS 18%→18%** (98% adequate, median 3 rules) are *present-or-truly-absent* — little stubbing. **Takeaway:** the adequacy gap is real and **concentrated in CONTRIBUTING/LICENSE** — a presence-only check passes a third of CONTRIBUTING stubs. This is the **presence ≠ adequacy** thesis (ADR-0008/0014) measured, and it **validates gingoa's content-asserting floor**: the scaffold ships CONTRIBUTING that is *tested for* build/test + PR-flow markers (`tests/scaffold/collaboration.test.ts`), not mere presence — dogfooding exactly the gap the wild leaves open.
- **↳ Governance-FLOOR census (N=6,582, 2026-07-05 — `census-data/census-governance-floor/`)** — widened the governance-file survey 3.3× past the 2000-repo set (star floor 29) and **stratified by archetype** (ecosystem + monorepo/library/cli, from manifest text) to ground a three-tier *auto / senior-default / context-confirm* classification of the scaffoldable set. **Overall presence:** README 100 · .gitignore 99 · **LICENSE 94** (SPDX-recognized 82; MIT ≈40% / Apache-2.0 ≈26%) · CI 85 · CONTRIBUTING 48 · issue-template 48 · CHANGELOG 41 · Discussions 39 · CoC 32 · dependency-update-bot 30 · PR-template 29 · FUNDING 29 · SECURITY 21 · .editorconfig 21 · **AGENTS.md 13 · CLAUDE.md 11** · CODEOWNERS 12 · pre-commit 5 · GOVERNANCE/SUPPORT/CLA/ADR-dir ≈1–2. Merge-policy (of resolved repos): squash-merge allowed **97%** · merge-commit 74% · rebase 81%; Contributor-Covenant = 18% of all. **The archetype effect is decisive and quantifies the conditional-bundle gates: monorepos are systematically 2–3× more governed** — CODEOWNERS 11%→**31%** (the single cleanest gate, confirming its monorepo/multi-team gating), CoC 30→57, SECURITY 19→51, PR-template 26→61, issue-forms 17→52, AGENTS.md 10→42; **pre-commit is cli-gated** (3%→28%), and AGENTS.md/CLAUDE.md concentrate in cli/tooling (30/26%) — the AI-harness constitution file is a *rising, tooling-concentrated* convention, not yet a universal floor. **Reference-class caveat:** the primary-language tag is skewed — Java is over-represented (Kotlin+Groovy fold into it; JVM repos reliably carry pom/gradle) and is *low-governance* (CONTRIBUTING 33%), dragging the aggregate down, while Python is **under-counted** (requirements.txt-only projects fail the manifest software-filter). So for a node/TS harness the honest reference class is the **node/go/rust** rates, not the Java-dragged mean: CONTRIBUTING 65–70 · SECURITY 32–43 · CoC 41–49 · PR-template 39–46 · dependency-bot 34–59 (≈1.4× the aggregate). Net: re-confirms LICENSE/README/.gitignore/CI as the near-universal **① floor** and the collaboration set (CONTRIBUTING/SECURITY/CODEOWNERS/CoC/templates) as the **archetype-gated conditional bundle**, now with measured monorepo/audience gates. → grounds the 3-tier ledger this feeds.
- **↳ Issue/PR WRITING-conventions layer** (2026-07-07 — `census-data/census-issue-pr/{conventions.py,conventions-records.json,conventions-stats.json}`; re-harvested the form/PR BODIES of the **1104** template-bearing repos → 1610 forms · 10,181 fields · 503 PR templates, PyYAML field-level parse 99.8% ok). The header/label censuses said *which* sections exist; this says **how they are written** (see the [sub-doc](issue-pr-writing-conventions.md)). **Issue forms:** `textarea` is the dominant field type (**54%**; + markdown-intro 14 / input 14 / checkboxes 9 / dropdown 8.5); **required tracks load-bearing fields** (dropdown 73 / input 65 / textarea 57 ↔ **checkboxes 3.8**); **help text near-universal (87%)**; preflight-dedup checkbox **22%** (senior minority); in-form CoC **6%** (context-gated); median fields/form bug 8 ≫ feature/task 4/3. **PR templates:** checklist ships **empty `- [ ]` (62%)** median 5 items; **HTML-comment guidance 70%**; lean median 3 sections; **"type of change" only 12% present, and when present 85% is a checkbox list (free-text `feat` just 1.7%)** — a minority section that also *duplicates the enforced Conventional-Commits PR title* → a CC-enforcing repo has grounds to drop it. This is the writing-method evidence the tiered template standard conforms to. → feeds [[template-standard-dogfood-gap]].

## Archetype variations

- **library / public OSS** — full contribution-policy set (CoC + CONTRIBUTING + SECURITY + issue forms) is the norm; CoC adoption peaks here. License compatibility for downstream consumers is load-bearing.
- **monorepo / multi-team** — CODEOWNERS becomes near-mandatory (path-scoped ownership); Team Topologies / Conway is *active* (multiple teams). `[census]` CODEOWNERS ~33% overall but defined-by-archetype for monorepo.
- **backend-service / web-app** — compliance posture (SOC2/ISO27001, audit trail, access control) carries the most weight; PII/payments push into a higher governance + change-management bar. `[census]` web-app scorecard mean is lowest (4.5) — gap the harness closes.
- **cli / solo / internal** — Team Topologies + RACI collapse to one maintainer; governance reduces to LICENSE + ADR + branch protection. Compliance largely N/A.
- **data-ml** — adds data-governance, model-cards, dataset licensing, and provenance to the IP/legal sub-aspect.
- **Gated:** Conway/Team-Topologies = **team-gated** (≥2 teams). Compliance/audit = **domain-gated** (regulated data / external customers).

## Tradeoffs / what's ruled out

- **Heavy RACI / formal governance boards** — ruled out for the default (solo + AI builder); collapses to maintainer + CODEOWNERS + ADR. Re-introduce only at multi-team scale.
- **ADR-for-everything** — ruled out; census 2–4% and `[lit, normative]` warns of "settlement failure" (repos with 1–5 stale ADRs). Record *real* decisions only.
- **Public-by-default ADRs** — ruled out by the publish-axis: standard path, but kept local/opt-in (census says they are not a public norm).
- **Retrofitting compliance** — ruled out; the cheap path is wiring the evidence trail (review history, signed commits, pinned deps) into normal flow from day-one, not an audit scramble later.
- **Process theater** — a CoC/CONTRIBUTING file with no enforced review is ruled out; the *enforced* control (branch protection) is what the minimum-dimension scoring rewards.

## Sources

- https://www.contributor-covenant.org/version/2/1/code_of_conduct/
- https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners
- https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions
- https://adr.github.io/madr/
- https://scorecard.dev/
- https://teamtopologies.com/key-concepts
- https://www.computer.org/education/bodies-of-knowledge/software-engineering
- https://www.iso.org/standard/63712.html
- https://research.jku.at/en/publications/using-architecture-decision-records-in-open-source-projects-an-ms/
