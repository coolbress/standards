---
id: aspect-17-release-engineering--release-operate-artifact-checklist
title: "Release + Operate artifact checklist (④) — provenance & SRE half"
parent: aspect-17-release-engineering
kind: research-log
evidence_track: lit
status: review-needed
last_updated: "2026-06-27"
method: "Independent canonical-checklist survey (2026-06-26; SLSA-v1.2 citation pass 2026-06-27) of ④ release+operate artifacts — SemVer/Keep-a-Changelog/Conventional-Commits, SLSA v1.2 + SBOM (CycloneDX/SPDX) + Sigstore, GitHub Releases, DORA, Google SRE (SLO/error-budget/runbook/postmortem), PagerDuty incident response, OpenTelemetry. Completes aspect-17's thin supply-chain-provenance + SRE half; also grounds aspect-18 (Packaging/Distribution) and aspect-20 (Operations/Incident/Reliability)."
---

# Release + Operate artifact checklist (④)

aspect-17's `<topic>--overview.md` covers the **release-discipline** half well (SemVer · Conventional-Commits engine ·
changelog · tagged Releases · cadence · rollback · DORA framing). This sub-doc adds the two parts it is THIN
on and that the ④ gap-audit (2026-06-26) flagged as missing from the ④ output enumeration:
**(A) supply-chain provenance** and **(B) the SRE/operate artifact set**. Tags: **MUST** / **REC** / **ARCH**.

## A. Release-stage artifacts (provenance focus — the gap)
*(release discipline itself — SemVer bump, CHANGELOG, tag, GitHub Release, CC-driven notes — is in the parent.)*
- **Annotated, signed git tag** (MUST) — GPG/SSH-signed; SLSA **Source L2** minimum tamper evidence (Source L2 = signed/protected history — a **v1.2** Source-track level, not present in v1.0).
- **Immutable, content-addressed build artifact** (MUST) — pinned binary/image-by-digest/package; deploying
  from a source checkout is not a release.
- **Checksum manifest** (MUST) — `checksums.txt` SHA-256 for every artifact, signed.
- **SBOM** (MUST under EO 14028 / EU CRA; else REC) — CycloneDX or SPDX inventory of direct+transitive deps
  (name/version/supplier/license/hash). NTIA/CISA minimum elements. *This is the aspect-18 grounding memory
  flagged as missing.*
- **SLSA Build provenance** (REC) — L1 = provenance exists+distributed (in-toto/DSSE: builder, source+commit,
  deps); **L2** = signed by the build platform (achievable on GitHub Actions via `slsa-github-generator`);
  L3 hardened = ARCH (critical infra).
- **Signed artifact** (MUST for public release) — **Sigstore/Cosign keyless** via Actions OIDC (Fulcio cert +
  Rekor transparency log); consumers `cosign verify`. No long-lived key. **SBOM attestation** (REC) =
  `cosign attest` the SBOM.
- **Deployment config / IaC diff** (MUST if a live service) · **rollback plan** (MUST; tested, with the
  trigger threshold) · **feature flags / dark launch** (REC) · **release-automation workflow as code** (MUST)
  · **release communication / migration guide on MAJOR** (REC).

## B. Operate-stage artifacts (the SRE half)
- **SLO document** (MUST) — SLI/SLO table + rationale + measurement caveats (Google SRE Workbook template).
- **Error-budget policy** (MUST) — *distinct from the SLO*: the rolling window + burn thresholds that trigger
  graduated response (e.g. >X% → freeze + mandatory postmortem). A policy without enforcement is decorative.
- **SLA** (ARCH: customer-facing) — external commitment, looser than the SLO.
- **Observability three pillars** (MUST) — metrics + distributed traces + structured logs via OpenTelemetry;
  the SLI measurement substrate (rate/errors/latency p50-p99/saturation).
- **Dashboards** (MUST, version-controlled) · **SLO burn-rate alerts** (MUST; multi-window multi-burn-rate,
  not raw thresholds — kills alert fatigue).
- **On-call rotation + escalation policy** (MUST) · **runbook per alert** (MUST — the "2am, know nothing, do
  this" artifact; most teams have alerts but no runbooks) · **incident severity matrix** (MUST) · **comms
  templates** (REC).
- **Blameless postmortem template + process** (MUST) — overview/contributing-factors/impact/timeline/action
  items; SEV-1 within ~3 days. **Action-item tracking → backlog** (MUST) — the loop-closing artifact.
- **Threat model** (MUST, **internal only**) · **vulnerability-management process** (MUST — triage SBOM CVEs
  via CVSS/VEX with remediation SLAs) · **access-control + secret-rotation policy** (MUST, **internal only**).
- **DORA metrics instrumentation** (MUST) — the 5 keys (deploy freq · lead time · recovery time · change-fail
  rate · rework). **Reliability/SLO retrospective** (MUST) — the recurring meeting that converts ops evidence
  into plan-stage prioritization. **Status page** (REC; customer-facing).

## Publish-vs-internal (confirms `_schema.md §4` publish-axis)
- **Publish with the artifact:** signed tag · GitHub Release + notes · CHANGELOG · build artifact + checksums ·
  **SBOM · SLSA provenance · Cosign signature/Rekor entry** (public verifiability is the point) · release CI yaml.
- **Internal by default:** deployment config (network topology) · rollback triggers (timing-attack aid) · SLO
  targets · error-budget policy · dashboards · runbooks · **threat model** · access/secret-rotation policy ·
  vuln-management SLAs. Postmortems: internal full + optional public summary. DORA results: shareable.

## Most-commonly-missed (senior-flags)
No SBOM · no signed artifact/provenance (Cosign is a one-line CI step) · no tested rollback (roll-forward
assumption → indefinite outage) · no runbooks · error-budget policy without enforcement · no postmortem
culture · no DORA measurement · unsigned/mutable version tags.

## gingoa ④ gap-closure (audit 2026-06-26)
gingoa's ④ (deferred, not yet built) enumerated release-workflow/CHANGELOG/runbooks/SLO/postmortem/threat-model/
rollback. This checklist is its **build-time spec**; the MUST-adds to bake in are: **SBOM · SLSA provenance ·
Cosign signing + checksum manifest · DORA instrumentation · error-budget policy · OTel three-pillars +
burn-rate alerts · vuln-management (SBOM→VEX)**. These also ground aspect-18 (packaging/provenance) and
aspect-20 (operate) — the ④ items memory flagged as not yet grounded in a mechanism.

## Sources
SemVer https://semver.org/ · Keep a Changelog https://keepachangelog.com/en/1.1.0/ · Conventional Commits
https://www.conventionalcommits.org/en/v1.0.0/ · SLSA v1.2 Build track https://slsa.dev/spec/v1.2/build-requirements ·
SLSA v1.2 Source track (new in v1.2; Source L2 = signed/protected history) https://slsa.dev/spec/v1.2/source-requirements ·
SLSA distributing provenance https://slsa.dev/spec/v1.2/distributing-provenance · Sigstore Cosign
https://docs.sigstore.dev/cosign/signing/overview/ · CycloneDX https://cyclonedx.org/capabilities/sbom/ ·
CISA SBOM framing 2024 https://www.cisa.gov/sites/default/files/2024-10/SBOM%20Framing%20Software%20Component%20Transparency%202024.pdf ·
NTIA minimum elements https://www.ntia.gov/files/ntia/publications/sbom_minimum_elements_report.pdf ·
GitHub Releases https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases ·
Google SRE Workbook (SLO/error-budget/alerting) https://sre.google/workbook/implementing-slos/ ·
DORA metrics https://dora.dev/guides/dora-metrics/ · PagerDuty incident response https://response.pagerduty.com/ ·
PagerDuty postmortems https://postmortems.pagerduty.com/ · OpenTelemetry https://opentelemetry.io/docs/concepts/observability-primer/ ·
OWASP threat modeling https://owasp.org/www-project-threat-modeling/
