---
id: aspect-12-performance-scalability
title: "Performance & Scalability"
group: "Q — Quality Attributes"
kind: gated
gated_archetypes: ["web", "backend", "data-ml", "mobile", "library"]
cross_cutting: false
lifecycle_stages: ["③", "④"]
anchors: ["ISO-25010-Performance", "ISO-25010-Flexibility", "SRE-capacity"]
evidence_track: lit
status: review-needed
last_updated: "2026-06-25"
sources:
  - "https://iso25000.com/index.php/en/iso-25000-standards/iso-25010"
  - "https://quality.arc42.org/standards/iso-25010"
  - "https://sre.google/sre-book/software-engineering-in-sre/"
  - "https://sre.google/sre-book/handling-overload/"
claim: "Senior engineers treat performance as a budgeted, measured quality attribute — set explicit time/throughput/resource targets (ISO 25010 performance efficiency), defend them with profiling + load tests + a perf-regression CI gate, and design for scale via statelessness, caching, capacity planning and graceful load shedding (SRE) — and this fires only for the runtime/data-heavy archetypes."
maps_from: []
census_todo: "Literature-grounded aspect (lit track): ISO 25010 + Google SRE are normative, not census-derived. No repo-survey % collected; perf-gate adoption could be censused later from CI configs but is not fabricated here."
---

> **Standard (claim):** Performance is a budgeted, measured quality attribute — explicit time/throughput/resource targets (ISO 25010 *performance efficiency*), defended by profiling + load tests + a perf-regression CI gate, with scale designed in via statelessness, caching, capacity planning and graceful load shedding (SRE).
> **Evidence:** [lit] ISO/IEC 25010:2023 · Google SRE Book · **Confidence:** High (normative standards) · **Kind:** gated[web/backend/data-ml/mobile/library] · **Stage:** ③, ④

**Seed sub-aspects:** `perf budgets / benchmark` · `profiling` · `load / stress` · `caching` · `DB / query optimization` · `horizontal scale / statelessness` · `perf-regression CI gate`

## What professional engineers do

- **Perf budgets / benchmark** [lit] — Turn performance into *requirements*, not vibes. ISO/IEC 25010 *Performance efficiency* decomposes into **time behaviour** (response time + throughput meet a stated requirement), **resource utilization** (CPU/memory/IO bounded), and **capacity** (the max limit a parameter must sustain). Seniors write these as numbers up front: p95/p99 latency targets, throughput floors, a per-request resource ceiling, and a defined peak load the system must hold. Benchmarks are repeatable harnesses (e.g. criterion/JMH/pytest-benchmark/k6) producing comparable numbers, not one-off timings.
- **Profiling** [lit] — Measure before optimizing; locate the actual hot path (CPU flamegraphs, allocation profiles, query traces, OpenTelemetry spans) rather than guessing. Optimization targets the dominant cost, and is re-profiled to confirm the win — resource-utilization claims (ISO 25010) are only credible when measured.
- **Load / stress** [lit] — Validate the *capacity* sub-characteristic with load tests at expected peak and stress tests past it to find the knee/breaking point. The SRE practice: some services are load-tested explicitly, others infer scaling from historical performance — but the capacity number is always backed by a curve, not an assumption.
- **Caching** [lit] — Reduce work and latency by serving cached/derived results instead of recomputing or re-fetching canonical storage. SRE's graceful-degradation pattern explicitly trades freshness for cost: serve a cached or partial answer that is "easier to compute" under load. Cache layers (CDN, in-memory, query cache) are a primary lever for time-behaviour and resource-utilization.
- **DB / query optimization** [lit] — A dominant latency/resource source for web+backend+data archetypes. Index for the access pattern, kill N+1 queries, bound result sets, and profile slow queries — this is the concrete face of *time behaviour* + *resource utilization* for data-backed systems.
- **Horizontal scale / statelessness** [lit] — Design for *scalability*, a first-class ISO/IEC 25010:2023 sub-characteristic of the new **Flexibility** characteristic ("adapted for different or evolving … environments"). The mechanism: keep request handlers stateless so load spreads across replicas; push state to shared stores. Capacity planning (SRE) shifts from hand-bin-packed resource plans to **intent-based** provisioning — "specify the requirements, not the implementation" — using dependencies, performance metrics, and prioritization to forecast demand.
- **Perf-regression CI gate** [lit] — Make the budget enforceable: run the benchmark/load harness in CI and fail (or flag) when a metric regresses past threshold. Without a gate, performance silently rots; the gate is what converts a one-time tuning into a durable guarantee.
- **Overload behaviour** [lit, normative] — At ④ operate-time, plan for *more* than peak. SRE techniques: criticality tiers (CRITICAL_PLUS → SHEDDABLE) so low-value work sheds first; client-side throttling + bounded retry budgets (cap retries, ~10% retry ratio) to stop retry storms; per-customer quotas; and load shedding keyed on CPU/memory utilization signals. The goal is graceful degradation under overload, not collapse.

## Evidence (lit + census)

- **[lit] ISO/IEC 25010:2023 — Performance efficiency.** Sub-characteristics: *time behaviour* (response time + throughput meet requirements), *resource utilization* (amounts/types of resources used meet requirements), *capacity* (maximum limits of a parameter meet requirements). This is the normative source for "performance as a stated, measurable requirement." (iso25000.com)
- **[lit] ISO/IEC 25010:2023 — Flexibility / Scalability.** The 2023 revision renames *Portability* to **Flexibility** and adds **Scalability** as a sub-characteristic (alongside adaptability, installability, replaceability) — making "scale to expanded load/environments" a first-class quality attribute. (quality.arc42.org)
- **[lit] Google SRE Book — Capacity planning.** Intent-based capacity: "Specify the requirements, not the implementation"; demand forecasting from dependencies + performance metrics + prioritization; some services load-tested, others inferred from past performance. (sre.google, "Software Engineering in SRE")
- **[lit, normative] Google SRE Book — Handling overload (Ch. 21).** Criticality tiers (CRITICAL_PLUS/CRITICAL/SHEDDABLE_PLUS/SHEDDABLE), client-side throttling, retry budgets (≤3 attempts, ~10% retry ratio), per-customer quotas, utilization-signal-based load shedding, and graceful degradation (cached/partial results). (sre.google, "Handling Overload")
- **[census] — none.** This aspect is literature-grounded (see `census_todo`); no repo-survey % is asserted. Perf-gate CI adoption is censusable later but not fabricated here.

## Archetype variations

This aspect is **gated** — it activates only for `web`, `backend`, `data-ml`, `mobile`, `library`:

- **web** — Front-end performance budgets (TTFB, LCP, bundle size, Core Web Vitals), CDN/edge caching, and a Lighthouse/bundle-size CI gate dominate; statelessness matters for SSR/serverless scale-out.
- **backend** — The canonical case: latency SLOs, load tests, DB/query optimization, stateless replicas behind a load balancer, capacity planning, and SRE overload handling (load shedding, retry budgets) all apply directly.
- **data-ml** — Throughput + resource-utilization on large datasets (batch + streaming), pipeline/job profiling, partitioning/sharding for horizontal scale, and inference latency/cost budgets; capacity is about data volume and model serving QPS.
- **mobile** — Device-bound resource utilization (battery, memory, jank/frame budgets, startup time, app size) plus network efficiency; "scale" is per-device and offline-tolerant, not server replicas.
- **library** — No runtime to operate, but **micro-benchmarks + a benchmark-regression gate** and documented algorithmic complexity are the seniors' standard; consumers inherit the library's hot-path cost.

Outside these archetypes the aspect does **not** fire.

## Tradeoffs / what's ruled out

- **Premature optimization is ruled out** — profile first; optimize the measured hot path only. Untargeted tuning costs craft budget without moving the dominant cost.
- **Caching trades freshness/consistency for latency/cost** — acceptable for degradation paths and read-heavy data; invalidation complexity is the price. Not a substitute for fixing a slow query.
- **Horizontal scale demands statelessness** — sticky session/in-process state is ruled out for scalable handlers; the cost is an external state store + its own latency.
- **A perf budget without a CI gate decays** — a number nobody enforces is documentation, not a guarantee. Conversely, an over-tight gate becomes flaky (perf tests are noisy), so thresholds carry tolerance bands.
- **Not every project pays this tax** — for non-gated archetypes (e.g. a CLI/harness) a full load-test + capacity-planning rig is over-engineering and explicitly *not* required.

## Sources

- ISO/IEC 25010 — Performance efficiency (time behaviour, resource utilization, capacity): https://iso25000.com/index.php/en/iso-25000-standards/iso-25010
- ISO/IEC 25010:2023 — Flexibility characteristic + Scalability sub-characteristic: https://quality.arc42.org/standards/iso-25010
- Google SRE Book — Software Engineering in SRE (intent-based capacity planning): https://sre.google/sre-book/software-engineering-in-sre/
- Google SRE Book — Handling Overload (criticality, throttling, retry budgets, load shedding): https://sre.google/sre-book/handling-overload/

## Sub-documents
- [`web-performance-thresholds--facts-2026-08.md`](web-performance-thresholds--facts-2026-08.md) — *research-log (ko)* — 2026-08 facts-only pass (R3-3): Core Web Vitals 임계값과 **그 지위 — Google의 정책이지 표준 기관 산출물 아님** · 성능 예산은 처방 · Lighthouse의 임계값 강제 방식. 표준 §6의 aspect 12 기각 사유 교정의 근거.
