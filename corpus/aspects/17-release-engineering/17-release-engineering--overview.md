---
id: aspect-17-release-engineering
title: "Release Engineering"
group: "R — Release & Operate"
kind: universal
gated_archetypes: []
cross_cutting: false
lifecycle_stages: ["④"]
anchors: ["SemVer-2.0", "Conventional-Commits", "Keep-a-Changelog", "DORA"]
evidence_track: census+lit
status: review-needed
last_updated: "2026-06-25"
sources:
  - "https://semver.org/"
  - "https://www.conventionalcommits.org/en/v1.0.0/"
  - "https://keepachangelog.com/en/1.1.0/"
  - "https://dora.dev/guides/dora-metrics-four-keys/"
  - "https://cloud.google.com/devops"
  - "https://getdx.com/blog/2024-dora-report/"
claim: "Senior teams ship via automated, SemVer-tagged releases driven from Conventional-Commits history (release-notes + CHANGELOG generated, not hand-written), with deployment/rollback rigor scaled to the archetype and delivery health tracked against DORA — release discipline is near-universal, operational depth is archetype-conditional."
maps_from: ["census-data/census-release-ops"]
---

> **Standard (claim):** Senior teams ship via **automated, SemVer-tagged releases driven from Conventional-Commits history** (notes + CHANGELOG generated, not hand-written); deployment/rollback rigor scales to the **archetype**, and delivery health is tracked against **DORA** — release discipline is near-universal, operational depth is archetype-conditional.
> **Evidence:** 429-repo census (Releases/Tags API + commit sampling + tree flags) + DORA/SemVer/CC/Keep-a-Changelog `[lit]` · **Confidence:** high (release half hard-measured; ops half cross-validated against surveys) · **Kind:** universal · **Stage:** ④

**Seed sub-aspects:** `SemVer` · `changelog automation` · `CI/CD gates` · `deployment strategies (blue-green / canary)` · `progressive delivery & feature-flag lifecycle` · `rollback` · `env promotion` · `PRRs`

## What professional engineers do

- **SemVer versioning** `[lit][census]`. Every release is a `vMAJOR.MINOR.PATCH` tag; major = breaking, minor = additive, patch = fixes. Near-mandatory: **86% (uniform) / 80% (weighted)** of repos tag SemVer, tag-level conformance `semver_ratio` weighted-mean **0.72**. The harness SemVer-tags every release by default.
- **Release automation + notes** `[lit][census]`. A release workflow cuts a **tagged GitHub Release with notes** — not a manual upload. **89/86%** publish tagged releases, **88/85%** ship notes alongside. Tooling (semantic-release / release-please / changesets / goreleaser) is a `[lit]` default — the census measured the *outcome* (a published release), not which tool.
- **Conventional Commits as the engine** `[lit][census]`. Commit history (`feat:`, `fix:`, `BREAKING CHANGE:`) is the single source that *derives* the next SemVer bump, the changelog, and the release notes — no hand-curation. Behavioral commit-sampling shows **45% uniform / 67% weighted** actually follow CC (vs only 14% that merely *install* commitlint-style tooling) — the **fastest-rising ④ signal (+22 weighted)**.
- **Changelog (Keep a Changelog)** `[lit][census]`. A human-readable `CHANGELOG.md` (Added/Changed/Fixed/Removed, newest-first, "Unreleased" section) — ideally generated from CC history. **55% uniform / 52% weighted**(n=429) maintain one; strongest for library/cli/published artifacts, optional for internal services.
- **Release cadence** `[census]`. Median **7 days** between releases (n=378 with ≥2 releases) — a proxy for DORA *deployment frequency*; mature OSS releases roughly **weekly**.
- **CI/CD gates + deployment** `[lit][census]`. Release candidates are green increments; CD/publish workflows promote them. **64/68%** run a CD/deploy-or-publish workflow; **53/62%** containerize. Progressive-delivery patterns (blue-green, canary, feature-flag-gated rollout) and **environment promotion** (dev→staging→prod) apply where a live service exists `[lit]`.
- **Rollback / recoverability** `[lit]`. A defined revert path (`git revert`, redeploy-previous-tag, flag-kill) so a bad release is reversible without history rewrite — a DORA *failed-deployment-recovery* lever; `[lit]` posture (rarely a repo file).
- **IaC + observability-as-code** `[census]`. Infra-as-code (Terraform/k8s/helm) at **28/29%** and observability-as-code (otel/prometheus/SLO yaml) at **18/17%** — a sparse, archetype-driven tail; real monitoring/SLOs live outside the repo (Grafana/Datadog/PagerDuty).
- **Delivery-health measurement (DORA / PRRs)** `[lit]`. Teams track the **Four Keys** (deploy frequency, change lead time, change-failure rate, recovery time) + reliability; production-readiness reviews (PRRs) gate a service's first ship. These are *achievement* metrics measured by survey, not repo census.

## Evidence (lit + census)

- **SemVer 2.0.0** — `vMAJOR.MINOR.PATCH` contract `[lit]` (https://semver.org/). Census: `semver_any` **86/80**, `semver_ratio` wmean **0.72** `[census]`.
- **Conventional Commits 1.0.0** `[lit]` (https://www.conventionalcommits.org/en/v1.0.0/). Census: `cc_adopted` **45/67** (behavioral commit sampling), `cc_ratio` wmean **0.60**, **+22** weighted-vs-uniform — fastest-rising ④ signal `[census]`. Independently re-validates the T1 (Conventional-Commits adoption) call on fresh evidence, not taste.
- **Keep a Changelog 1.1.0** `[lit]` (https://keepachangelog.com/en/1.1.0/). Census: `changelog` **55/52** `[census]`.
- **Releases / notes** `[census]`: `has_releases` **89/86** (coverage 100%), `has_release_notes` **88/85**. **Cadence** median **7 days** (n=378).
- **Deployment/ops half** `[census]`: `cd_deploy` **64/68**, `container` **53/62**, `iac` **28/29**, `observability` **18/17**.
- **DORA Four Keys + reliability** `[lit, empirical]` (https://dora.dev/guides/dora-metrics-four-keys/; https://cloud.google.com/devops). **State of DevOps 2024** cluster split: Elite **19%**, High **22%** (↓ from 31%), Low **25%** (↑ from 17%) (https://getdx.com/blog/2024-dora-report/); foundations: *Accelerate* (Forsgren et al. 2018), *Google SRE* (Beyer et al. 2016).
- **Observability/SLO surveys** `[lit, empirical]`: SLOs in production **~26%** (Grafana Observability Survey 2024, https://grafana.com/observability-survey/2024/); OpenTelemetry 58–85% — cross-validates the **17% observability-as-code** census (both: "monitoring/SLO maturity is a minority").
- **Census provenance** `[census]`: same 429-repo set as ② foundation, collected via GitHub Releases/Tags API + commit-message sampling + file-tree flags (mechanical, no LLM judgment); recency-weighted `w = 0.5^(age/2yr)`, ref 2026-06-24; 0 fetch failures, 5 tree truncations. Source `census-data/census-release-ops/`.

## Archetype variations

**Release discipline is universal; operational depth tracks "is there a running service?"** (per-archetype uniform %, `census-release-ops/stats.json`):

- **library** (n=93): releases/notes/SemVer **91/90/92**, but container **24**, iac **16**, obs **10**. ④ = "publish a versioned release." CC only 37.
- **cli** (n=77): **95/95/88** release, container 53, obs **8**. Like library + a binary publish step (e.g. goreleaser).
- **backend-service** (n=67): container **79**, cd 67, iac **42**, obs **31**, CC **54**. ④ = release **+** containerize **+** deploy **+** observe; PRRs/SLOs apply.
- **monorepo** (n=90): highest across the board — CC **71**, changelog **77**, container 68, iac **48**, obs **36**. Per-package versioning (changesets-style) + service-grade ops.
- **web-app** (n=33): release ~88, cd **70**, container 52, obs 9 — deploy-heavy, light on infra monitoring.
- **data-ml** (n=23): weakest release discipline (releases **65**, SemVer **43**, CC 17) — many are research repos, not shipped products; container 57 but obs 9.
- **mobile** (n=11): strong release/SemVer (91/82) but container 27, **obs 0** — store-submission pipeline, not server ops.

→ No archetype is *gated out* of release engineering, but the **operational half (container/CD/IaC/observability) is archetype-conditional** — selected by contract field **C5**. Mandating IaC/observability on a library is cargo-cult.

## Tradeoffs / what's ruled out

- **Behavioral sampling beats file-presence.** ②'s file proxy under-counted commit convention at 14% (commitlint *config* exists); commit-message sampling shows **45% uniform / 67% weighted**(n=429) real practice. Evidence > proxy — but it costs an API sampling pass.
- **Observability stays literature-backed, not a census gap.** Even in repos that *should* have it, observability-as-code is sparse (17%) because real monitoring/SLOs live in Datadog/Grafana/PagerDuty, not the tree. Don't try to "fill" it with a wider census — it's an honest literature-backed posture line.
- **Operational *achievement* (SLO attainment, MTTR, change-failure rate) is irreducibly `[lit]`** — exists outside any repo; population numbers come from DORA-style **surveys**, not repo census. The harness *instruments toward* the Four Keys (release automation→frequency, CI+tests→low failure rate) but cannot census others' attainment.
- **Tool choice is `[lit]` default, not censused.** The census saw the *outcome* (a published GitHub Release), not whether it came from semantic-release / release-please / changesets / goreleaser; pick per ecosystem.
- **Ruled out:** manual version bumps, hand-written changelogs, manual release uploads, mandatory IaC/observability for non-service archetypes.

## Sources

- SemVer 2.0.0 — https://semver.org/
- Conventional Commits 1.0.0 — https://www.conventionalcommits.org/en/v1.0.0/
- Keep a Changelog 1.1.0 — https://keepachangelog.com/en/1.1.0/
- DORA Four Keys — https://dora.dev/guides/dora-metrics-four-keys/
- DORA / DevOps research — https://cloud.google.com/devops
- State of DevOps 2024 analysis — https://getdx.com/blog/2024-dora-report/
- Grafana Observability Survey 2024 (SLO ~26%) — https://grafana.com/observability-survey/2024/
- Census: 429-repo Release/Tags-API + commit sampling — `census-data/census-release-ops/`
- *Accelerate* (Forsgren, Humble, Kim 2018) · *Site Reliability Engineering* (Beyer et al., Google 2016)

## Sub-documents
- [`last-mile-domain-hosting--facts-2026-08.md`](last-mile-domain-hosting--facts-2026-08.md) — *research-log (ko)* — 2026-08 facts-only pass (GAPS R1-10 전반): 코드 완성 이후 공개까지의 도메인 등록(ICANN 연락처 검증·갱신/만료 유예) · DNS 연결과 TLS 자동 발급 · PaaS 프로덕션 배포와 롤백 · 무료→유료 과금 전환 트리거, 그리고 **과금·외부 노출·자격증명이 발생하는 정확한 단계**. 본문 미확인 claim은 `[미확인]`으로 강등 표기됨.
- [`last-mile-payments-privacy--facts-2026-08.md`](last-mile-payments-privacy--facts-2026-08.md) — *research-log (ko)* — 2026-08 facts-only pass (GAPS R1-10 후반): PSP 온보딩 요건(신원·UBO·은행계좌) · PCI DSS SAQ 범위와 6.4.3/11.6.1 · PIPA 제30조 · GDPR Art.13/14 정보 제공 의무, 그리고 **신원·계약·법적 책임 때문에 사람만 할 수 있는 단계**. PIPA 조문 각 호는 1차 미확보로 `미해결`.
- [`release-operate-artifact-checklist.md`](release-operate-artifact-checklist.md) — *research-log* — the ④ release+operate artifact checklist: supply-chain provenance (SBOM/SLSA/cosign/checksum) + the SRE/operate half (SLO/error-budget/runbook/postmortem/OTel/DORA); also grounds aspects 18 & 20.

## Claim table — feature toggle 의 비용 (R5-1 배치 C · 1차 출처 직접 확인)

| Claim ID | Class | Claim and scope | Evidence | Confidence | 재검증 |
|---|---|---|---|---|---|
| REL-001 | definition | 원문은 feature toggle 을 **"technical debt(기술 부채)"** 라고 부르지 **않는다.** 쓰는 표현은 ***"inventory which comes with a carrying cost"*** 다: *"Savvy teams view their Feature Toggles as inventory which comes with a carrying cost, and work to keep that inventory as low as possible."* | `FOWLER-FEATURE-TOGGLES` | high | 2026-08-24 |
| REL-002 | synthesis | ⚠️ ***"feature flag 는 부채"* 는 과일반화다.** 원문은 토글을 **수명별로 구분**한다 — Release(며칠~주) · Experiment(시간~주) · Ops(가변) · **Permissioning(수년)**. Permissioning 토글은 *"multiple years"* 존속이 **설계 의도**이고 부채로 취급되지 않으며, 원문의 처방은 *"different toggles [should be] managed in different ways"* 다. **비용은 개수를 줄여 관리할 대상이지 토글 자체가 부채인 것이 아니다** | `FOWLER-FEATURE-TOGGLES` | high | 2026-08-24 |

**재검증 기록 (배치 C)** — 검증일 `2026-08-24` · 검증자 `Claude Opus 5` + `codex-cli 0.145.0`(독립 질의) · **판정: 한정 추가** · **불일치 없음**(Codex 가 *"원문이 유형별 비용 차이를 명시적으로 단정하지는 않는다"* 를 더 정밀하게 짚었다) · 절차 [`reverification-protocol`](../../methods/reverification-protocol.md)


## Claim table — Conventional Commits 의 가치 조건 (`03` 미검증 해소 · 2026-08-26)

| Claim ID | Class | Claim and scope | Evidence | Confidence | 재검증 |
|---|---|---|---|---|---|
| REL-003 | vendor-behavior | ✅ **자동화가 CC 에 의존하는 것은 도구 사실이다.** `semantic-release` 는 구조화된 커밋 메시지 없이 동작하지 않고 **Conventional Commits 명세에 전적으로 의존**해 변경을 SemVer 로 매핑한다. → *"자동화가 소비할 때 가치가 있다"* 의 **앞 절반은 사실**이다 | `SEMANTIC-RELEASE-DOC` | high | 2026-08-26 **신규** |
| REL-004 | synthesis | 🔵 ***"아니면 cargo cult"* 는 판단이다.** CC 채택이 **자동화 없이도** 성과에 영향을 주는지 잰 실증 연구를 찾지 못했다 — 나온 것은 실무 문서와 도구 문서뿐이다. **탐색 범위**: CC 채택 효과 · semantic-release 영향 · 저장소 단위 실증. → **뒷 절반은 프로젝트 판단으로 표시**한다 | `SEMANTIC-RELEASE-DOC` (부재 확인 대상) | medium (공백 확인) | 2026-08-26 **판단으로 분류** |

**재검증 기록 (`03` ⚪ 해소 · Conventional Commits)** — 검증일 `2026-08-26` · 검증자 `Claude Opus 5` · **판정: 사실 1 · 판단 1** · **한 문장을 둘로 갈랐다** — *"자동화가 소비할 때만 가치"* 에서 **앞은 도구 사실, 뒤는 판단**이다 · 절차 [`reverification-protocol`](../../methods/reverification-protocol.md)
