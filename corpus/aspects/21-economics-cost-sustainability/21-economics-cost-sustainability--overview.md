---
id: aspect-21-economics-cost-sustainability
title: "Software Economics, Cost & Sustainability"
group: "R — Release & Operate"
kind: gated
gated_archetypes: ["cloud", "published"]
cross_cutting: false
lifecycle_stages: ["④"]
anchors: ["SWEBOK-KA15", "FinOps-Framework", "GSF-SCI", "CSRD"]
evidence_track: lit
status: review-needed
last_updated: "2026-06-25"
sources:
  - "https://www.computer.org/education/bodies-of-knowledge/software-engineering"
  - "https://www.finops.org/framework/"
  - "https://greensoftware.foundation/standards/sci/"
  - "https://www.iso.org/standard/86612.html"
  - "https://finance.ec.europa.eu/capital-markets-union-and-financial-markets/company-reporting-and-auditing/company-reporting/corporate-sustainability-reporting_en"
claim: "Senior teams treat run-cost and carbon as first-class engineering metrics — FinOps cost visibility/allocation/optimization for any metered-cloud system, SWEBOK-KA15 ROI/make-or-buy for technical decisions, and (for in-scope orgs) GSF-SCI carbon-per-functional-unit and CSRD/ESRS disclosure — but the cloud cost loop fires only for metered deployments and the sustainability/disclosure loop only above regulatory thresholds."
maps_from: []
---

> **Standard (claim):** _Treat run-cost and carbon as first-class engineering metrics: FinOps for metered-cloud cost visibility/optimization, SWEBOK-KA15 for ROI/make-or-buy decisions, and GSF-SCI + CSRD/ESRS for the in-scope sustainability/disclosure loop — each gated to where it actually applies._
> **Evidence:** [lit] 4 named standards (FinOps Framework, SWEBOK-KA15, ISO/IEC 21031, CSRD) · **Confidence:** med-high (lit-grounded; no census) · **Kind:** gated[cloud/published] · **Stage:** ④

**Seed sub-aspects:** `cost visibility / tagging` · `budget alerts` · `rightsizing / commitments` · `unit economics` · `ROI / make-or-buy (KA15)` · `sustainability / Scope-3 / SCI (emerging)`

## What professional engineers do

- **Cost visibility / tagging** [lit] — Every billable resource carries allocation metadata (tags/labels/account structure) so 100% of spend maps to a team, service, or feature. FinOps calls this *cost allocation*; it is the precondition for the whole loop — you cannot optimize or chargeback what you cannot attribute. Senior practice: a tagging policy enforced at provision time (IaC, not after the fact), plus showback/chargeback so each team sees its own bill.
- **Budget alerts / anomaly management** [lit] — Set budgets with thresholded alerts and automated anomaly detection on the daily cost feed, so a runaway resource or a misconfigured loop is caught in hours, not at month-end invoice. FinOps puts this in the *Understanding Costs* domain (reporting/analytics + anomaly detection) — data must be *accessible, timely, and accurate* (FinOps Principle 4).
- **Rightsizing / commitments** [lit] — Continuously match provisioned capacity to real utilization (rightsizing), then buy down the steady-state baseline with rate optimization (committed-use discounts / reserved instances / savings plans). FinOps *Optimizing Spend* = workload-architecture decisions + usage optimization + rate negotiation; it explicitly exploits *the variable cost model of the cloud* (Principle 6).
- **Unit economics** [lit] — Convert raw spend into a per-unit metric (cost per order, per active user, per inference) so cost is read against business value, not in isolation. FinOps *Quantifying Value* names unit-economics measurement and KPI analysis as distinct capabilities; this is what lets engineering reason about margin and scaling, not just total bill.
- **ROI / make-or-buy (SWEBOK-KA15)** [lit] — Technical decisions (build-vs-buy, adopt-a-framework, refactor-vs-rewrite) are justified with applied microeconomics: cash flow, time-value of money, equivalence, and explicit selection criteria over technically-feasible alternatives. KA15's *Engineering Decision-Making Process* makes "why this technology / what is the ROI" a numerical argument, including intangible assets and the business model — and mandates *monitoring the performance of the selected alternative* after the fact.
- **Sustainability / SCI (emerging, gated)** [lit] — For orgs that measure or must disclose carbon, software emissions are reported as a *rate*, not a total: SCI = (O + M) per R — operational energy×carbon-intensity plus embodied hardware emissions, per functional unit. Critically, *only actions that eliminate emissions reduce the score* — offsets do not count. SCI is now ISO/IEC 21031:2024.
- **Disclosure / Scope-3 (CSRD/ESRS, gated by threshold)** [lit] — Large/listed EU-in-scope orgs report sustainability under ESRS with double materiality, including value-chain (Scope-3) emissions, with external assurance. The 2025 Omnibus narrowed scope toward the largest companies (~1000+ employees) and used a "stop-the-clock" delay — so this fires only above a moving regulatory threshold.

## Evidence (lit + census)

- [lit] **FinOps Framework** — six principles; capability domains *Understanding Costs* (ingestion, allocation, reporting/analytics, anomaly detection), *Quantifying Value* (planning, forecasting, budgeting, KPI, unit economics), *Optimizing Spend* (architecture, usage optimization, rate negotiation, sustainability), *Practice Management* (governance, chargeback, tooling); lifecycle Inform → Optimize → Operate, "Crawl/Walk/Run." https://www.finops.org/framework/
- [lit] **SWEBOK-KA15 (Guide v4.0, IEEE Computer Society)** — Software Engineering Economics: proposals, cash flow, time-value of money, equivalence, bases for comparison, intangible assets, business model; the engineering decision-making process incl. selection criteria and post-decision monitoring. https://www.computer.org/education/bodies-of-knowledge/software-engineering
- [lit] **GSF SCI / ISO/IEC 21031:2024** — `SCI = (O + M) per R`; a *rate* (per user / transaction / API call); offsets excluded; ratified as the first ISO standard for software carbon measurement. https://greensoftware.foundation/standards/sci/ · https://www.iso.org/standard/86612.html
- [lit] **CSRD / ESRS (EU)** — ESRS-based reporting, double materiality, value-chain (Scope-3) emissions, external assurance; 2025 Omnibus "stop-the-clock" + 1000-employee scope narrowing. https://finance.ec.europa.eu/capital-markets-union-and-financial-markets/company-reporting-and-auditing/company-reporting/corporate-sustainability-reporting_en
- [census] — none. This aspect is literature-grounded; cost/carbon practices live in billing dashboards and corporate filings, not in public repos, so a repo census does not surface adoption. See `census_todo`.

## Archetype variations

- **`cloud` (gates the FinOps/cost loop)** — The full cost-visibility → budget-alert → rightsizing/commitments → unit-economics loop fires only when deployment is *metered*: a per-resource billing API exists to tag, alert on, and optimize. A single-tenant VM or a fixed-price PaaS gets a degraded subset (mostly budget alerts); a multi-service autoscaling estate gets the whole framework and chargeback.
- **`published` (gates the disclosure/sustainability loop)** — Carbon/SCI reporting and CSRD/ESRS disclosure attach to the *organization that ships/operates at scale*, not to the code. SCI is opt-in and applies to any operator that wants a carbon metric; CSRD/ESRS is mandatory only above the (currently 1000-employee) threshold. Most published artifacts (an OSS library, a small SaaS) carry neither.
- **Cross-cutting note** — SWEBOK-KA15 ROI/make-or-buy is the one sub-aspect that is *archetype-agnostic in spirit* (any team should justify build-vs-buy), but it is parked here under the gated aspect because the numerical run-cost inputs only become real once a metered deployment exists.

## Tradeoffs / what's ruled out

- **Don't scaffold FinOps for non-metered targets.** A CLI, a library, or a fixed-price host has no per-resource billing feed — cost tagging/anomaly tooling is pure overhead. Ruled out unless a metered cloud deployment is in the contract.
- **Don't mandate SCI/CSRD by default.** Carbon measurement is real engineering work (energy + embodied-emissions modeling) and CSRD is a legal regime with thresholds; forcing either on a small project is gold-plating. Offer SCI as opt-in; trigger CSRD only when org-scale/jurisdiction thresholds are declared.
- **Cost ≠ the only axis.** FinOps optimizes spend *against business value* (unit economics), not toward minimum bill — over-aggressive rightsizing/commitment buying trades reliability headroom for savings. The standard is value-based, not cheapest-possible.
- **Offsets are out (for SCI).** ISO/IEC 21031 deliberately excludes carbon offsets from the score — a project cannot "buy down" its SCI; only genuine energy/hardware/intensity reductions count.

## Sources

- FinOps Framework — https://www.finops.org/framework/
- SWEBOK Guide v4.0 (IEEE Computer Society), KA15 Software Engineering Economics — https://www.computer.org/education/bodies-of-knowledge/software-engineering
- Green Software Foundation — Software Carbon Intensity (SCI) — https://greensoftware.foundation/standards/sci/
- ISO/IEC 21031:2024 — Software Carbon Intensity (SCI) specification — https://www.iso.org/standard/86612.html
- EU Corporate Sustainability Reporting Directive (CSRD) / ESRS — https://finance.ec.europa.eu/capital-markets-union-and-financial-markets/company-reporting-and-auditing/company-reporting/corporate-sustainability-reporting_en

## Sub-documents
- [`serverless-cost-model--facts-2026-08.md`](serverless-cost-model--facts-2026-08.md) — *research-log (ko)* — 2026-08 facts-only pass (R3-3): **과금 단위 표** — AWS Lambda(GB-s: 실행시간이 곧 비용) vs Vercel(부분) vs Cloudflare(CPU-ms: 아님). **어느 플랫폼도 "성능=비용"을 공식 원칙으로 규정하지 않는다** · FinOps는 재단의 처방.
