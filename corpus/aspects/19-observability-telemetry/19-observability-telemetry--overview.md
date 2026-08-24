---
id: aspect-19-observability-telemetry
title: "Observability & Telemetry"
group: "R — Release & Operate"
kind: universal
gated_archetypes: []
cross_cutting: false
lifecycle_stages: ["③", "④"]
anchors: ["OpenTelemetry", "SRE-golden-signals"]
evidence_track: census+lit
status: review-needed
last_updated: "2026-06-25"
sources:
  - https://opentelemetry.io/docs/
  - https://sre.google/sre-book/monitoring-distributed-systems/
  - https://sre.google/workbook/implementing-slos/
  - https://www.brendangregg.com/usemethod.html
  - https://web.dev/articles/vitals
  - https://grafana.com/observability-survey/2024/
  - https://dora.dev/guides/dora-metrics-four-keys/
claim: "Senior engineers instrument services for the three pillars (structured logs, RED/USE metrics, distributed traces) on OpenTelemetry, derive SLO-driven alerts from the SRE golden signals, and treat live monitoring/SLO targets as out-of-repo posture — but real-repo adoption is a sparse, archetype-driven tail (~17% have observability-as-code; SLOs in production ~26%)."
maps_from: ["census-data/census-release-ops/stats.json"]
---

> **Standard (claim):** Instrument services for the three pillars (structured logs · RED/USE metrics · distributed traces) on a vendor-neutral OpenTelemetry pipeline, alert on SLO burn against the four golden signals, and keep live-monitoring/SLO targets as out-of-repo operational posture.
> **Evidence:** census+lit — obs-as-code 18→17% weighted, archetype-split backend 31% / monorepo 36% / library 10% / mobile 0%; SLO-in-prod 26% (survey) · **Confidence:** high (lit), medium (census — sparse tail, real monitoring lives off-repo) · **Kind:** universal · **Stage:** ③, ④

**Seed sub-aspects** (expand during collection): `metrics (RED / USE)` · `structured logs` · `distributed tracing` · `SLI definition` · `alerting design` · `dashboards` · `RUM (web)`

## What professional engineers do

- **Three pillars on one vendor-neutral pipeline.** Emit *logs, metrics, traces* and correlate them by trace/span IDs. OpenTelemetry (OTel) is the convergent standard: instrument once with the SDK + semantic conventions, export via the OTLP protocol to any backend (Prometheus/Tempo/Loki, Datadog, Honeycomb). Decouples instrumentation from vendor lock-in. `[lit]`
- **Metrics — pick the right method per workload.** *RED* (Rate, Errors, Duration) for **request-driven** services (the user-facing view); *USE* (Utilization, Saturation, Errors) for **resources** (CPU, disk, queues — the cause-finding view). The two are complementary: RED tells you something is wrong, USE tells you why. `[lit]`
- **Golden signals frame what to watch.** Google SRE's four — *latency, traffic, errors, saturation* — are the minimal set for any user-facing system; "if you can measure only four, measure these." Alerts and dashboards derive from them. `[lit]`
- **Structured logs, not string soup.** Log as machine-parseable key/value JSON (event, level, trace_id, fields), one event per line, with a stable schema; logs become queryable/aggregatable, not just `grep`-able. Sampling + log levels control cost/cardinality. `[lit]`
- **Distributed tracing for request flows.** A trace = a tree of spans across service boundaries; context propagation (W3C `traceparent`) ties them together. Essential once a request crosses >1 service to find *where* latency/errors originate. Sampling (head/tail) trades fidelity for cost. `[lit]`
- **SLIs → SLOs → error budgets → alerts.** Define an **SLI** (a measured ratio of good events, e.g. fast & successful requests / total), set an **SLO** target (e.g. 99.9% over 28 days), and the gap is the **error budget**. Alert on **burn rate** (multi-window, multi-burn-rate) against the budget — *not* on raw thresholds — to cut alert fatigue and tie paging to user-visible harm. `[lit]`
- **Alerting design.** Page only on symptoms that threaten an SLO and need a human now; everything else is a ticket or a dashboard. Every alert has a runbook. Avoid cause-based alerting that fires on conditions invisible to users. `[lit]`
- **Dashboards.** One overview per service organized by the golden signals (the "service dashboard"); drill-downs by USE for resources. Dashboards-as-code (Grafana JSON/Jsonnet, Terraform) keeps them reviewable and versioned. `[lit][census]`
- **RUM (web/mobile).** Real-User Monitoring captures field performance — **Core Web Vitals** (LCP, INP, CLS) — from actual sessions, complementing synthetic/lab tests. The user-perceived-latency arm of the golden signals for front-ends. `[lit]`
- **Operational half lives off-repo.** Live monitoring, on-call, SLO *attainment*, MTTR, incident retros are intrinsically not repo files — they live in Grafana/Datadog/PagerDuty/internal wikis. The codebase carries *observability-as-code* (OTel config, Prometheus rules, SLO yaml, dashboards); the *targets and runbooks* are operational posture, framed by DORA + SRE. `[lit][census]`

## Evidence (lit + census)

- `[lit]` **OpenTelemetry** — open standard for logs/metrics/traces + OTLP. https://opentelemetry.io/docs/
- `[lit]` **Google SRE — golden signals** (latency/traffic/errors/saturation): "Monitoring Distributed Systems". https://sre.google/sre-book/monitoring-distributed-systems/
- `[lit]` **Google SRE Workbook — Implementing SLOs** (SLI/SLO/error budget, multi-burn-rate alerting). https://sre.google/workbook/implementing-slos/
- `[lit]` **RED method** (Tom Wilkie) — Rate/Errors/Duration for request services. `[lit]` **USE method** (Brendan Gregg) — Utilization/Saturation/Errors for resources. https://www.brendangregg.com/usemethod.html
- `[lit]` **Core Web Vitals** — LCP/INP/CLS field metrics for RUM. https://web.dev/articles/vitals
- `[census]` **429-repo release-ops census** (recency-weighted `w=0.5^(age/2yr)`): observability-as-code present in **18% uniform / 17% weighted** of repos — a sparse operational tail. Archetype split: **monorepo 36% · backend-service 31% · IaC-heavy** vs **library 10 · cli 8 · web-app 9 · data-ml 9 · mobile 0**. (`census-data/census-release-ops/stats.json`)
- `[lit]` (survey, cross-validates census) **Grafana Observability Survey 2024** + **Splunk State of Observability 2024**: SLOs in production **~26%** (large orgs 55% vs small 28%); OpenTelemetry adoption **58–85%**. Both agree with the repo census: observability/SLO maturity is a minority. https://grafana.com/observability-survey/2024/
- `[lit]` **DORA Four Keys** — observability is the lever for the *recovery* keys (MTTR, change-fail rate); attainment is survey-measured, not repo-censusable. https://dora.dev/guides/dora-metrics-four-keys/

## Archetype variations

- **backend-service / monorepo** — full kit expected: OTel instrumentation, RED on endpoints + USE on resources, traces across services, SLOs, dashboards-as-code. Highest real adoption (31/36%) yet still a minority — a *senior* differentiator, not a baseline most repos hit.
- **web-app** — RED + RUM (Core Web Vitals) is the user-perceived arm; front-end errors via Sentry-class tools. Obs-as-code in repo is low (9%) because much runs in the host/CDN.
- **mobile** — crash/ANR reporting + RUM via SDK (Crashlytics-class); essentially **0% repo-file** observability-as-code (lives in the app + vendor console). Tracing/Prometheus N/A.
- **library / cli** — **does NOT apply as a service.** Mandating IaC/observability here is cargo-culting (lib 10% / cli 8% is mostly the lib's *own* test infra, not service monitoring). The standard branches at the contract's service axis.
- **data-ml** — adds pipeline/job observability + data-quality/drift monitoring on top of (or instead of) request metrics; obs-as-code ~9%.

## Tradeoffs / what's ruled out

- **Not for non-services.** Forcing SLOs/dashboards on a library or CLI is anti-pattern; the aspect is gated by whether a running service exists (contract service axis).
- **Threshold alerting ruled out** in favor of SLO burn-rate alerting — static thresholds cause alert fatigue and fire on user-invisible conditions.
- **Vendor-specific-first instrumentation ruled out** — OTel-neutral instrumentation prevents lock-in; backends are swappable.
- **Cost vs fidelity** — full tracing/high-cardinality metrics are expensive; sampling and cardinality budgets are the accepted lever (no "log everything").
- **Repo census can't measure the operational half.** SLO *targets/attainment*, on-call, incident retros are honestly `[lit]`/survey, not a census gap to backfill — real monitoring lives in Datadog/Grafana/PagerDuty, off the tree.
- **Publish axis:** observability-as-code (OTel/Prometheus/dashboards) is *public config* when the archetype applies; **SLO target values + incident retros stay internal** (off-repo by nature; some carry attacker value).

## Sources
- https://opentelemetry.io/docs/
- https://sre.google/sre-book/monitoring-distributed-systems/
- https://sre.google/workbook/implementing-slos/
- https://www.brendangregg.com/usemethod.html
- https://web.dev/articles/vitals
- https://grafana.com/observability-survey/2024/
- https://dora.dev/guides/dora-metrics-four-keys/

## Sub-documents
- [`structured-logging-metrics--facts-2026-08.md`](structured-logging-metrics--facts-2026-08.md) — *research-log (ko)* — 2026-08 facts-only pass (R2-2): OpenTelemetry 로그 규약과 HTTP 서버 메트릭 semantic conventions · 로그 레벨/상관 ID/민감정보. **RED·USE는 표준이 아니라 처방**임을 분류표로 분리.
