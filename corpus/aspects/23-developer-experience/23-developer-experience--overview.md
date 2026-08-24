---
id: aspect-23-developer-experience
title: "Developer Experience & Onboarding"
group: "G — Cross-cutting Practice & Governance"
kind: universal
gated_archetypes: []
cross_cutting: true
lifecycle_stages: ["②"]
anchors: ["CNCF-Platform-Eng-MM", "DORA-platform", "SPACE"]
evidence_track: lit
status: review-needed
last_updated: "2026-06-25"
sources:
  - "https://tag-app-delivery.cncf.io/whitepapers/platform-eng-maturity-model/"
  - "https://dora.dev/capabilities/platform-engineering/"
  - "https://www.microsoft.com/en-us/research/publication/the-space-of-developer-productivity-theres-more-to-it-than-you-think/"
claim: "A new contributor reaches a first green build/PR through a documented golden path and self-service scaffolding, and DX is steered by multi-dimensional signals (SPACE) rather than a single output metric — escalating to a platform/IDP only at multi-team scale."
maps_from: []
census_todo: "Literature-grounded aspect (CNCF PE-MM / DORA platform-engineering / SPACE). Platform/IDP maturity is rarely visible in a single-repo census; no adoption % fabricated. A future census could measure the shallower signals: presence of an onboarding/CONTRIBUTING runbook, a scaffolder (Copier/cookiecutter), and a one-command bootstrap."
---

> **Standard (claim):** A new contributor reaches a first green build/PR through a documented golden path and self-service scaffolding, and DX is steered by multi-dimensional signals (SPACE) rather than a single output metric — escalating to a platform/IDP only at multi-team scale.
> **Evidence:** [lit] CNCF Platform-Eng Maturity Model · DORA platform-engineering capability · SPACE framework · **Confidence:** High (named standards) · **Kind:** universal · cross-cutting · **Stage:** ②

**Seed sub-aspects:** `onboarding runbook` · `time-to-first-PR` · `golden paths / paved road` · `scaffolding (Copier)` · `DX metrics (DORA / SPACE)` · `platform-engineering / IDP (team-gated)`

## What professional engineers do

- **Onboarding runbook → time-to-first-PR.** [lit] The headline DX metric is *time-to-first-meaningful-contribution*: a `CONTRIBUTING.md` / dev-setup runbook plus a **one-command bootstrap** (`make setup`, devcontainer, `npm run dev`) so a new contributor clones, builds green, and lands a first PR the same day. The runbook is treated as code — kept in-repo, tested in CI — because a stale setup doc is the most common cause of multi-day onboarding stalls.
- **Golden paths / paved road.** [lit] A *golden path* is the opinionated, supported, "happy" route for the most common workflow — pre-wired with the org's testing, security, and deploy defaults so the easy way is also the correct way. DORA's guidance: *identify the golden path for the most common workflow and build just enough to make that specific journey demonstrably better*, then iterate. The paved road reduces **cognitive load** by abstracting underlying complexity rather than forcing every developer to master Kubernetes/cloud/security details.
- **Scaffolding (Copier/cookiecutter).** [lit] Golden paths are made *self-service* through templated scaffolding: a new service/module is generated from a template that bakes in the linter, test harness, CI, and directory layout. In the CNCF maturity model this is the Operational level (templates + docs) maturing toward Scalable "one-click" provisioning where teams benefit *without needing to understand how it is provisioned*.
- **DX metrics (SPACE, not a single number).** [lit] Productivity *cannot be measured by a single metric or dimension*. The SPACE framework prescribes capturing **at least two or three** of its five dimensions: **S**atisfaction & wellbeing, **P**erformance, **A**ctivity, **C**ommunication & collaboration, **E**fficiency & flow — deliberately mixing perceptual (survey) and system signals to avoid gaming. DORA's four keys (lead time, deploy frequency, change-fail rate, MTTR) supply the delivery-throughput slice; SPACE keeps the human/flow slice in the picture.
- **Platform engineering / IDP (team-gated).** [lit] At multi-team scale the golden path is productized into an **Internal Developer Platform** — the platform is treated as an internal *product* for developers, with self-service interfaces, a measurement/feedback loop, and dedicated investment. The CNCF PE Maturity Model scores this across five aspects (Investment, Adoption, Interfaces, Operations, Measurement) over four levels (Provisional → Operational → Scalable → Optimizing). This is a deliberate organizational investment, **not** a default for small projects.

## Evidence (lit + census)

- [lit] **CNCF Platform Engineering Maturity Model** — five aspects (Investment, Adoption, Interfaces, Operations, Measurement) × four levels (Provisional, Operational, Scalable, Optimizing). "Paved roads/golden paths, in the form of documentation and templates" appear at the Operational level; Scalable adds "one-click" self-service where teams benefit without understanding provisioning; the Measurement aspect requires standard outcome metrics gathered "from multiple angles."
- [lit] **DORA — Platform engineering capability** — a platform is an internal product offering simple, self-service golden paths so developers focus on user value; primary goal is to **reduce cognitive load** by abstracting complexity; recommended adoption is to make one common journey "demonstrably better" first and iterate.
- [lit] **SPACE framework** (Forsgren, Storey, et al., ACM Queue / Microsoft Research, 2021) — developer productivity "cannot be measured by a single metric or dimension"; five dimensions (Satisfaction, Performance, Activity, Communication & collaboration, Efficiency & flow); capture multiple, mixing perceptual and telemetry signals.
- [census] No fabricated adoption %. This is a literature-track aspect; platform/IDP maturity is an org-level property not readable from a single repo. See `census_todo` for the shallow proxies a future census could count (runbook present, scaffolder present, one-command bootstrap).

## Archetype variations

This aspect is `kind: universal` and **not gated** (`gated_archetypes: []`): every archetype owes its contributors a fast, documented path to a first green build. What *scales* with the project is the depth:

- **Library / CLI / small service** — DX is a good `CONTRIBUTING.md`, a one-command bootstrap, fast local tests, and (optionally) a scaffolder for new modules. A full IDP would be over-engineering.
- **Web / mobile / multi-service org** — golden paths get productized: shared generators, preview environments, self-service deploy. Here the platform-engineering / IDP sub-aspect activates and the CNCF maturity model becomes the yardstick.
- **AI/ML** — onboarding additionally must reproduce data + environment (pinned deps, seeds, sample datasets); "first green run" includes a reproducible training/eval, raising the bar on the bootstrap step.

The **IDP / platform-engineering** sub-aspect is effectively *team-size-gated*: it fires only at multi-team scale, where the cost of building and operating the platform is repaid across many consumers.

## Tradeoffs / what's ruled out

- **Golden path ≠ golden cage.** A paved road must stay opt-out-able; mandating it for every edge case turns enablement into a bottleneck. Provide the supported path *and* an escape hatch.
- **Single-metric DX is ruled out.** Lines-of-code, commit counts, or "velocity" alone are explicitly rejected by SPACE — they are gameable and ignore satisfaction/flow. Always pair a system metric with a perceptual one.
- **Premature platform.** Standing up an IDP for one or two teams costs more than it saves; the maturity model's Provisional/Operational levels are the *correct* stopping point for small orgs. Don't buy/build a platform to solve a runbook problem.
- **Onboarding docs rot.** A runbook that isn't exercised by CI (or by the bootstrap script itself) silently drifts; "documentation as the interface" only works when the docs are executable/tested.

## Sources

- CNCF Platform Engineering Maturity Model — https://tag-app-delivery.cncf.io/whitepapers/platform-eng-maturity-model/
- DORA — Platform engineering capability — https://dora.dev/capabilities/platform-engineering/
- SPACE of Developer Productivity (Forsgren et al., 2021) — https://www.microsoft.com/en-us/research/publication/the-space-of-developer-productivity-theres-more-to-it-than-you-think/
