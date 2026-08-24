---
id: aspect-16-privacy-data-protection
title: "Privacy & Data Protection"
group: "Q — Quality Attributes"
kind: gated
gated_archetypes: ["handles-user-data"]
cross_cutting: false
lifecycle_stages: ["③"]
anchors: ["GDPR-Art-25", "ISO-25010-Security", "NIST-Privacy"]
evidence_track: lit
status: review-needed
last_updated: "2026-06-25"
sources:
  - "https://gdpr-info.eu/art-25-gdpr/"
  - "https://gdpr-info.eu/chapter-3/"
  - "https://gdpr-info.eu/art-33-gdpr/"
  - "https://www.nist.gov/privacy-framework"
  - "https://www.nist.gov/privacy-framework/privacy-framework"
claim: "When a system handles personal data, senior engineers bake privacy in by design and by default (GDPR Art.25) — minimize collection, build erasure/access/portability (DSAR) as first-class data-model operations, log lawful basis/consent, and pre-wire a 72-hour breach-notification path — rather than bolting privacy on after launch."
maps_from: []
---

> **Standard (claim):** When a system handles personal data, privacy is designed in **by default** (GDPR Art.25) — minimize collection, treat erasure/access/portability as first-class data operations, record lawful basis, and pre-wire a 72-hour breach path — not bolted on after launch.
> **Evidence:** [lit] (named standards: GDPR, NIST Privacy Framework, ISO/IEC 25010) · **Confidence:** high (regulatory, not stylistic) · **Kind:** gated[handles-user-data] · **Stage:** ③

**Seed sub-aspects:** `privacy-by-design` · `data minimization` · `DSAR / erasure / portability` · `consent / cookies` · `DPIA` · `anonymization / pseudonymization` · `breach notification`

## What professional engineers do

- **Privacy by design & by default** [lit] — GDPR Art.25 makes this a legal obligation, not a nicety: implement technical/organizational measures (it names pseudonymisation) at design time, and ship defaults where *only data necessary for each specific purpose* is processed — covering amount collected, extent of processing, retention period, and accessibility. Personal data must not be made accessible "to an indefinite number of natural persons" without the subject's intervention. Concretely: opt-in not opt-out defaults, no public-by-default profiles, no "collect now, decide later" telemetry.
- **Data minimization** [lit] — collect the smallest field set that serves a declared purpose; map each stored field to a purpose and a retention TTL. Drop/aggregate logs and analytics that carry identifiers. Enforce with a data inventory (record of processing, GDPR Art.30) so every field has a known owner, purpose, and lawful basis.
- **DSAR: access / erasure / portability** [lit] — Chapter 3 rights become engineering work: Art.15 (access — confirm + export what's held), Art.16 (rectification), Art.17 (erasure / "right to be forgotten"), Art.20 (portability — machine-readable export). Seniors build these as queryable data-model operations: a stable subject key threaded through every store (DB, cache, search index, backups, third-party processors, log pipeline) so "delete user X everywhere" is a real, testable operation rather than a manual scramble. Soft-delete + scheduled hard-delete + processor cascade is the common pattern.
- **Consent / cookies** [lit] — consent must be specific, informed, and revocable, recorded with timestamp + scope + version of the notice; no pre-ticked boxes. Cookie/tracker consent gates non-essential scripts until granted. Withdrawal must be as easy as granting and must propagate to downstream processing.
- **DPIA (Data Protection Impact Assessment)** [lit] — for high-risk processing (large-scale, special-category, profiling, monitoring), run a DPIA before building: describe the processing, assess necessity/proportionality, identify risks to subjects, and document mitigations. It is the privacy analogue of a threat model and is a gating artifact, not a retrospective.
- **Anonymization / pseudonymization** [lit] — pseudonymization (reversible with a separately held key — Art.25/Art.4) reduces risk while keeping data useful; true anonymization (irreversible) takes data out of GDPR scope entirely. Seniors separate the re-identification key store, and for analytics prefer aggregation / k-anonymity / differential-privacy techniques over raw identifiers.
- **Breach notification** [lit] — pre-wire the response path: GDPR Art.33 requires notifying the supervisory authority "without undue delay and, where feasible, not later than **72 hours**" after becoming aware of a breach; Art.34 requires notifying affected individuals when risk is high. Engineering enablers: tamper-evident audit logs, detection/alerting, an incident runbook, and a maintained contact/processor list — so the clock is meetable.
- **Risk-management spine** [lit] — the NIST Privacy Framework gives the org-level structure (voluntary, risk-based): its Core functions — **Identify-P, Govern-P, Control-P, Communicate-P, Protect-P** — map to inventorying data, setting policy, giving subjects control, transparency, and securing data. ISO/IEC 25010 frames privacy under the **Security** quality characteristic (confidentiality), tying it to the broader quality model so it is measured, not assumed.

## Evidence (lit + census)

- [lit] **GDPR Art.25 — Data protection by design and by default.** Mandates appropriate technical/organizational measures (e.g. pseudonymisation) at design time and defaults that process only data necessary per purpose; bars indefinite accessibility without subject intervention. https://gdpr-info.eu/art-25-gdpr/
- [lit] **GDPR Chapter 3 — data subject rights** (Art.15 access, 16 rectification, 17 erasure, 20 portability). https://gdpr-info.eu/chapter-3/
- [lit] **GDPR Art.33 — breach notification within 72 hours** to the supervisory authority "without undue delay and, where feasible, not later than 72 hours"; delays must be justified. https://gdpr-info.eu/art-33-gdpr/
- [lit] **NIST Privacy Framework** — voluntary risk-management tool to identify and manage privacy risk; Core / Profiles / crosswalks structure. https://www.nist.gov/privacy-framework · https://www.nist.gov/privacy-framework/privacy-framework
- [lit] **ISO/IEC 25010** — places privacy/confidentiality under the Security quality characteristic (anchor; ties privacy to the product-quality model).
- [census] **Not censusable.** Privacy controls (DSAR endpoints, consent records, DPIAs) are rarely visible in public OSS repos — they are deployment/operational artifacts. This aspect is literature-grounded (regulatory). No fabricated adoption %.

## Archetype variations

This aspect is **gated** — it fires only for **`handles-user-data`** archetypes (anything storing/processing personal data: SaaS web apps with accounts, mobile apps, anything with PII, health, payment, or behavioral data).

- **Web / SaaS with accounts** — full surface: consent banner + record, account-data export & delete, processor cascade (analytics, email, payment), audit logging.
- **Mobile** — adds platform privacy manifests (Apple privacy nutrition labels, Android Data Safety), on-device vs server data choices, OS permission prompts.
- **Health / fintech / EU-facing** — escalates: DPIA effectively mandatory, special-category data handling, often sector overlays (HIPAA, PCI-DSS) layered on the GDPR baseline.
- **Pure-tool / no-PII archetypes** (CLI, library, dev-harness, static site with no accounts) — **does not fire**: no personal data, no DSAR, no consent. Forcing privacy scaffolding here is over-engineering.

## Tradeoffs / what's ruled out

- **Privacy vs. data-hungry analytics** — minimization and short retention cost some product/ML insight; the ruling: declare purpose first, collect to it, aggregate the rest. "Collect everything, decide later" is ruled out (violates Art.25 default).
- **Erasure vs. immutable/audit stores** — true hard-delete conflicts with append-only ledgers and backups; resolved via crypto-shredding (delete the key) or documented backup-rotation windows, not by skipping erasure.
- **Pseudonymization is not anonymization** — reversible pseudonymized data stays in regulatory scope; don't claim "anonymized" for hashed-but-linkable IDs.
- **Don't gate non-handlers** — applying this aspect to a CLI/library/harness with no PII adds compliance theater with zero subjects to protect; explicitly ruled out by the gate.

## Sources

- https://gdpr-info.eu/art-25-gdpr/ — GDPR Art.25, data protection by design & by default
- https://gdpr-info.eu/chapter-3/ — GDPR Chapter 3, data subject rights (Art.15/16/17/20)
- https://gdpr-info.eu/art-33-gdpr/ — GDPR Art.33, 72-hour breach notification
- https://www.nist.gov/privacy-framework — NIST Privacy Framework (overview)
- https://www.nist.gov/privacy-framework/privacy-framework — NIST Privacy Framework v1.0 (Core / Profiles)

## Sub-documents
- [`privacy-statutory-duties--facts-2026-08.md`](privacy-statutory-duties--facts-2026-08.md) — *research-log (ko)* — 2026-08 facts-only pass (R3-2): **개인정보 보호법 제30조 제1항 각 호 원문 확보**(처리방침 필수 기재 11항목, 시행일 2025-10-02, 법률 제20897호) + 제15·16·22조(만 14세 미만 포함) · GDPR Art.13 vs 14 차이표(**요약본 기반 — EUR-Lex 원문 미대조**) · 쿠키 동의의 근거 조문. R1-10b의 최대 미해결을 종결.
