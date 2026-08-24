---
id: lifecycle-crosswalk
title: "Lifecycle Navigation Crosswalk"
kind: navigation
status: review-needed
last_updated: "2026-08-02"
evidence_track: lit
freshness: versioned
review_due: "2026-10-02"
sources: [ISO-12207-2026, SWEBOK-4.0A]
---

# Lifecycle Navigation Crosswalk

This file is a **local navigation overlay**, not an industry-mandated process. ISO/IEC/IEEE 12207:2026 provides
a common life-cycle process framework but does not require one specific life-cycle model or methodology. The
four stages below are a compact way to retrieve evidence; activities may be concurrent, iterative, and recursive.

| Local navigation stage | Primary aspects | Always consider |
|---|---|---|
| 1. Discover and plan | 01, 02, 21, 24, 25 | risk, security, privacy, evidence, stakeholder needs |
| 2. Establish the delivery system | 03, 04, 05, 06, 10, 22, 23 | reproducibility, permissions, supply chain, recovery |
| 3. Implement and verify | 07, 08, 11–16, 19, 28 | architecture, security, documentation, traceability |
| 4. Release, operate, maintain, retire | 17–21, 24, 25 | observability, rollback, incident learning, disposal |

Greenfield and brownfield are applicability modes, not separate life cycles. Brownfield work adds discovery,
compatibility, non-clobbering, incremental adoption, and rollback constraints. Detailed gingoa-era activation
decisions are preserved at `../interpretation/legacy/gingoa-lifecycle.md` and are not evidence.

## Sources

- `ISO-12207-2026` — https://www.iso.org/standard/90219.html
- `SWEBOK-4.0A` — https://www.computer.org/education/bodies-of-knowledge/software-engineering

