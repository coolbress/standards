---
id: aspect-20-operations-incident-reliability
title: "Operations, Incident & Reliability"
group: "R — Release & Operate"
kind: gated
gated_archetypes: ["web", "backend", "data-ml"]
cross_cutting: false
lifecycle_stages: ["④"]
anchors: ["Google-SRE", "ITIL-4", "DORA", "NIST-SP-800-34"]
evidence_track: lit
status: review-needed
last_updated: "2026-06-25"
sources:
  - "https://sre.google/sre-book/embracing-risk/"
  - "https://sre.google/sre-book/postmortem-culture/"
  - "https://dora.dev/guides/dora-metrics-four-keys/"
  - "https://cloud.google.com/devops"
  - "https://getdx.com/blog/2024-dora-report/"
  - "https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final"
  - "https://www.atlassian.com/incident-management/devops/incident-vs-problem-management"
  - "https://grafana.com/observability-survey/2024/"
claim: "Senior teams operate a running service against explicit SLOs with an error-budget policy, escalate via on-call to a defined incident-response flow, learn through blameless postmortems and problem-management RCA, and prove resilience with tested DR (RTO/RPO) — measuring delivery health by the DORA four keys; these live outside the repo (Grafana/PagerDuty/runbooks), so they are a [lit] posture, not a file census."
maps_from: []
---

> 🔄 **분류 정정 2026-08-28** (`GAPS` R5-16 ②ⓐ): `kind: universal` · `gated_archetypes: []` → **`kind: gated` · `["web", "backend", "data-ml"]`**. claim 이 *"operate a **running service** against explicit SLOs"* + on-call 이다. 돌고 있는 것이 없으면 error budget 도 incident 도 성립하지 않는다.
>
> `[]` 는 *universal* 을 뜻하므로(`_schema.md` §3.1) 그대로 두면 **바닥이 로컬 CLI 스크립트에도 이걸 요구한다.** claim 본문과 분류가 어긋나 있었다.

> **Standard (claim):** Senior teams run a service against explicit **SLOs + error-budget policy**, route alerts through **on-call → incident response → blameless postmortem → problem RCA**, prove recovery with tested **DR (RTO/RPO)**, and gauge delivery by the **DORA four keys** — an operational posture that lives outside the repo, hence [lit], not file-censusable.
> **Evidence:** lit (Google SRE · ITIL-4 · DORA · NIST 800-34) + the 429-repo release-ops census tier-C frame · **Confidence:** high · **Kind:** universal · **Stage:** ④

**Seed sub-aspects:** `SLO + error-budget policy` · `on-call / escalation` · `incident response` · `blameless postmortems` · `problem management (RCA)` · `DR / backup / BCP (RTO/RPO)` · `toil reduction` · `chaos engineering` · `IaC / GitOps` · `delivery metrics (DORA)`

## What professional engineers do

- **SLO + error-budget policy** — Define availability/latency **SLOs** (per quarter) from user-meaningful SLIs; the gap between SLO target and 100% is the **error budget**. A written **error-budget policy** makes reliability self-enforcing: budget remaining ⇒ ship features freely; **budget exhausted ⇒ freeze launches** and spend the next cycle on resilience/testing — aligning product and SRE incentives instead of litigating them. [lit, normative]
- **On-call / escalation** — A named rotation with a paging tool (PagerDuty/Opsgenie), tuned **alert thresholds** tied to SLO burn (multi-window burn-rate alerts, not raw-metric noise), an escalation ladder (primary → secondary → IC), and humane practices (compensated, bounded shift length, follow-the-sun for large teams). [lit]
- **Incident response** — A defined flow: **detect → triage/severity → declare → coordinate (Incident Commander, comms lead, ops lead) → mitigate → resolve → review**. Severity levels (Sev1–3) drive who's paged and how fast. Goal of the live phase is **restore service**, not find root cause (that's deferred to the postmortem). [lit ITIL-4 incident management]
- **Blameless postmortems** — Every significant incident gets a written postmortem within days: timeline, impact, contributing causes, what went well, action items with owners. **Blameless** = focus on systems/process, not individuals, so engineers report honestly; the postmortem is the unit of organizational learning. [lit Google SRE]
- **Problem management (RCA)** — ITIL separates **incident** (restore service fast) from **problem** (the underlying cause). Problem management does **root-cause analysis** on recurring/severe incidents and drives permanent fixes (and known-error records), closing the loop so the same outage doesn't recur. [lit ITIL-4]
- **DR / backup / BCP (RTO/RPO)** — Per NIST SP 800-34: a **Business Impact Analysis** sets recovery priorities and the targets **RTO** (max tolerable downtime) and **RPO** (max tolerable data loss). Backups follow 3-2-1; **restores are tested** (an untested backup is a hope, not a plan). Tiered by system criticality. [lit NIST 800-34]
- **Toil reduction** — SRE caps manual, repetitive, automatable operational work (target ≤ ~50% of an SRE's time) and reinvests in automation; toil that scales linearly with service growth is a backlog signal. [lit, normative]
- **Chaos engineering** — Mature orgs inject controlled failure (latency, instance kill, dependency outage) in a blast-radius-bounded way to validate that SLOs and runbooks hold under real failure — a hypothesis-driven discipline (Netflix Chaos Monkey lineage), not random breakage. [lit]
- **IaC / GitOps** — Infra and deploy state declared as code (Terraform/Helm/k8s) and reconciled from git as the source of truth (Argo/Flux), giving reviewable, auditable, reproducible, rollback-able operations. Repo-censusable for service archetypes (see Evidence). [lit + census]
- **Delivery metrics (DORA)** — The **four keys** measure delivery health: **deployment frequency** + **change lead time** (velocity) and **change-failure rate** + **time-to-restore** (stability), plus a 5th **reliability** key. Elite ≠ slow-but-safe — top teams are fast *and* stable; the keys are leading indicators wired from release automation, CI/tests, and observability. [lit DORA]

## Evidence (lit + census)

- [lit] **Google SRE — Embracing Risk** (SLO, error budget, freeze-on-exhaustion policy): https://sre.google/sre-book/embracing-risk/ ; **Postmortem Culture** (blameless): https://sre.google/sre-book/postmortem-culture/
- [lit] **ITIL-4** incident vs problem management (restore-fast vs RCA): https://www.atlassian.com/incident-management/devops/incident-vs-problem-management
- [lit, normative] **NIST SP 800-34 Rev.1** "Contingency Planning Guide for Federal Information Systems" — BIA, RTO/RPO, backup/DR/BCP tiers: https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final
- [lit, empirical] **DORA four keys + reliability**: https://dora.dev/guides/dora-metrics-four-keys/ ; **State of DevOps 2024** clusters — Elite **19%** / High **22%** (was 31%) / Low **25%** (was 17%): https://cloud.google.com/devops · analysis https://getdx.com/blog/2024-dora-report/
- [census] 429-repo release-ops survey (recency-weighted `w=0.5^(age/2yr)`): **observability-as-code 18→17%** — the operations achievement layer is a sparse, archetype-skewed tail because real monitoring/SLOs live outside the repo (Datadog/Grafana/PagerDuty). `iac 28→29%` (backend 42 / monorepo 48 vs library 16). `cd_deploy 64→68%`, `container 53→62%`. **Median release cadence 7 days** (n=378) = DORA *deployment-frequency* proxy: typical top OSS ships weekly.
- [census→lit cross-check] **Grafana Observability Survey 2024**: SLOs in production **26%** (large orgs 55% vs small 28%), OpenTelemetry 58–85% — independently matches the repo census (obs-as-code 17%): both say "monitoring/SLO maturity is a minority, archetype-driven posture." https://grafana.com/observability-survey/2024/

## Archetype variations

- **backend-service** (gated-on: "is there a running service") — full posture: SLOs, on-call, incident flow, IaC, observability-as-code. Census: container **79%**, IaC **42%**, observability **31%** (the high end). The archetype where the whole aspect activates.
- **monorepo** — typically wraps services: container **68%**, IaC **48%**, observability **36%** (highest obs). Same full posture, often multi-service.
- **web-app** — deploy + uptime/error monitoring (often a managed platform), lighter SLO/on-call than backend (observability **9%**).
- **data-ml** — pipeline/job reliability (freshness/SLAs, retries, lineage) over request-latency SLOs; many are research repos (releases 65% only).
- **library / cli** — **no live operations to run**; this aspect is largely **N/A** beyond release hygiene (observability **10% uniform / 8% weighted** · n=429, mobile **0%**). Forcing SLOs/IaC/on-call here is cargo-cult. Operations scales with "is there a service that runs," not universally.
- **mobile** — crash reporting + staged rollout + remote config + app-store ops, not server SLOs (observability 0% in census).

## Tradeoffs / what's ruled out

- **Achievement metrics (SLO attainment, MTTR, change-failure rate) are not file-censusable** — they live in monitoring/paging/incident tools, not the tree. Honest [lit] (DORA survey, Grafana survey) supplies population numbers; we instrument *toward* them (release automation → frequency; CI/tests → low CFR; observability → fast restore) but cannot census *attainment* in others' repos.
- **Operations is archetype-conditional, not universal** — mandating IaC/SLO/on-call on a library is a weak-link inversion. The standard branches by archetype.
- **Public-axis exclusion** — SLO targets, runbooks, incident retros, on-call config, DORA dashboards, threat models are **built (per literature) but kept off the public remote**: intrinsically off-repo (Grafana/PagerDuty/internal wiki) and some leak attacker advantage. Observability-as-code (prometheus/otel) *is* a public config when the archetype applies; SLO **targets** and **retros** stay internal.
- **Chaos engineering & strict error-budget freezes are maturity practices**, not day-one defaults — valuable but ruled out of the birth baseline; surfaced as posture, adopted as the service matures.

## Sources
- https://sre.google/sre-book/embracing-risk/
- https://sre.google/sre-book/postmortem-culture/
- https://www.atlassian.com/incident-management/devops/incident-vs-problem-management
- https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final
- https://dora.dev/guides/dora-metrics-four-keys/
- https://cloud.google.com/devops
- https://getdx.com/blog/2024-dora-report/
- https://grafana.com/observability-survey/2024/

## Sub-documents
- [`solo-operations-minimum--facts-2026-08.md`](solo-operations-minimum--facts-2026-08.md) — *research-log (ko)* — 2026-08 facts-only pass (GAPS R1-9): managed 플랫폼(AWS·Vercel·Render·Fly.io·Supabase)의 shared-responsibility 서술에서 **1인 소유자에게 남는 운영 책임** — 알림 표면 · 백업/복원과 복원 책임 소재 · spend cap(hard vs alert-only) · 런타임 EOL과 인시던트 오너십. 미조사 플랫폼과 미명시 항목은 문서의 `미해결` 절에 명시.
- [`operations-sre--facts-2026-08.md`](operations-sre--facts-2026-08.md) — *research-log (ko)* — 2026-08 facts-only pass: SLI/SLO/error-budget · toil · IMAG roles · blameless postmortem · on-call rules · golden signals · observability pillars · DevOps origins (telemetry content also serves aspect-19).
