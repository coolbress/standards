---
title: "Gingoa Engineering-Standard Aspect Taxonomy"
status: locked
last_updated: "2026-06-27"
provenance: "4-angle deep research (foundational-frameworks + cross-framework + archetype + adversarial), synthesized & adjudicated"
anchors: [SWEBOK-v4, ISO-IEC-IEEE-12207-2017, ISO-IEC-25010-2023, ISO-IEC-25019-2023, ISO-IEC-IEEE-29148-2018, PMBOK-7, ITIL-4, OWASP-SAMM, BSIMM, NIST-SSDF-800-218, SLSA-v1.0, OpenSSF, DORA-2024, Google-SRE, 12-Factor, CNCF, Diataxis, WCAG-2.2, GDPR, FinOps-Framework]
---

> ⚠️ **아카이브 (2026-08-02 감사)** — gingoa 시절 원문 보존본. 내부 상대 링크는 원 위치 기준이라 깨져 있을 수 있다. 활성 문서는 `../../corpus/`를 보라.

# Gingoa Engineering-Standard Aspect Taxonomy (LOCKED)

> The definitive set of engineering **aspects** ("how senior engineers do it") the gingoa corpus must cover.
> **aspect = the standard (WHAT)** · the lifecycle (①기획→②포석→③구현→④릴리스·운영) is gingoa's **activation
> layer (WHEN gingoa applies it)**. Knowledge stored once, per aspect; the lifecycle map (`lifecycle.md`)
> inverts this into a `stage → aspects` activation matrix the harness pipeline consumes.
> North star: **no senior engineer can say "engineers don't do it this way"** — for ANY scaffolded archetype.

## How this was locked (provenance)
Validated against the authoritative frameworks (anchors above) via four independent research angles that
**converged**: (A) exhaustive coverage vs SWEBOK v4 / 12207 / 25010 / 25019 / 29148; (B) cross-framework
triangulation (PMBOK, ITIL, OWASP SAMM/BSIMM, NIST SSDF, SLSA, DORA/SRE, 12-Factor, CNCF, FinOps); (C) per-
archetype completeness (library·cli·web·backend·mobile·data-ml·monorepo·ai-harness); (D) adversarial
staff-engineer attack. Coverage check: every SWEBOK KA (except CS/Math foundations), every 12207 process
(incl. the previously-missing **Disposal**), and every 25010 characteristic is mapped to an aspect or
**consciously excluded with grounds** (see §Out-of-scope). Evidence-tag convention: `[lit]` literature ·
`[census]` repo survey · `[inferred]` our routing logic (see `00-project-lifecycle.md §7`).

## Adjudicated conflicts (where the 4 angles disagreed)
- **Architecture vs Design** — SWEBOK separates KA2/KA3; we **keep one aspect** (`02`) with explicit
  architecture vs detailed-design sub-groups. Detailed design folds into Construction in practice; splitting
  adds fragmentation without senior-objection risk. `[inferred]`
- **Security split** — NIST SSDF separates PW (produce secure) / PS (protect artifact) / RV (respond); SLSA +
  EO 14028 + EU CRA make supply chain a distinct regulated domain. **We split** into `09 Application Security`
  and `10 Software Supply Chain Security`. `Licensing` (`25`) stays separate (legal/SPDX ≠ SBOM-as-security).
- **Dev-Env vs Build/CI** — different owners, tooling, lifecycle, failure modes (D). **We split** into `03 Dev
  Environment` and `04 Build & CI Engineering`.
- **Observability vs Operations** — SWEBOK KA6 + SRE chapters + D's grab-bag critique. **We split** into `19
  Observability & Telemetry` and `20 Operations, Incident & Reliability` (DR/BCP, SLO/error-budget, on-call,
  problem-mgmt land in 20).
- **Platform Engineering** — B (DORA-2024/CNCF cert → first-class) vs D (premature for solo non-engineer).
  **Resolution: fold into `23 Developer Experience` as a team-scale-gated sub-aspect** (activates at multi-team).
- **Risk Management** — PMBOK Uncertainty + 12207 Risk process (currently only security-risk). **Fold into `01`**
  as an explicit non-security risk sub-aspect (avoid standalone PM-tool bloat).
- **Estimation / IDP-portal / Conway** — kept as **scale-gated sub-aspects** (01, 23, 24), not standalone.

---

## The locked set — 28 aspects (roster lives in INDEX)
The 28-aspect **roster** + its live per-aspect classification (Kind · Stage · anchors · key sub-aspects) lives in
[`INDEX.md`](INDEX.md) (the navigation entry point) + each aspect's own frontmatter (`kind` / `lifecycle_stages` /
`anchors`); the stage→aspect activation overlay is [`lifecycle.md`](lifecycle.md). **This file is the design
rationale** for that set — its provenance (above), the conflict adjudications (above), and the out-of-scope calls
(below) — not a second, drift-prone copy of the roster. Group structure: **P** Plan&Design · **F** Foundation&Build ·
**C** Construct&Verify · **Q** Quality attrs · **R** Release&Operate · **G** Cross-cutting · **S** Specialized.

## Out-of-scope (consciously excluded, with grounds)
| Excluded | Why | Re-entry condition |
|---|---|---|
| **Safety Engineering** (25010 char.9 / IEC 61508 · ISO 26262 · DO-178C) | safety-critical embedded/medical/automotive — none of gingoa's target archetypes | future gated aspect `G[embedded/iot/medical]` — stub kept |
| **Internationalization (i18n)** | a design constraint, not a SWEBOK KA / 12207 process / 25010 char; gingoa repo is English-only | note inside `13 API/UX` for consumer-web archetypes |
| **SWEBOK KA16 Computing Foundations / KA17 Mathematical Foundations** | university CS prerequisites, not "how to build production software" procedural guidance | never (assumed knowledge) |
| **Full Estimation / IDP-portal / PMO** | PM-tool territory; estimation is unreliable & context-bound (D) | scale-gated sub-aspects in 01/23/24 at team scale |

## Notes for corpus build
- Each aspect → directory `aspects/NN-<slug>/` with `_aspect.md` (frontmatter + "what engineers do" + evidence
  + archetype variations + implications-for-gingoa + sources). Split into multiple docs on growth (1 doc = 1 purpose).
- Sub-aspects are seeded per aspect (each `_aspect.md` "Seed sub-aspects" line); per-aspect collection expands them with `[lit]`/`[census]`.
- Censusable aspects (file-detectable: 03/04/05/08/10/15/18/19/22 + parts) → widen census; practice/lit aspects
  (01/02/07/11/20/24/26/27/**28**) → literature track. **28 is [lit]-ONLY by nature** — how work is
  routed/managed is not observable from a repo census. Per the two-axis methodology (`00 §7`).
