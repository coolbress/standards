---
id: aspect-15-accessibility-ux
title: "Accessibility & UX / Interaction Capability"
group: "Q — Quality Attributes"
kind: gated
gated_archetypes: ["web", "mobile"]
cross_cutting: false
lifecycle_stages: ["③"]
anchors: ["ISO-25010-Interaction-Capability", "WCAG-2.2", "EN-301-549"]
evidence_track: lit
status: review-needed
last_updated: "2026-06-25"
census_todo: "Literature-grounded (WCAG 2.2 / ISO 25010 / EN 301 549). A11y conformance is not a measurable repo-survey field, so no census % is claimed; revisit only if a future census adds an a11y-CI-presence signal for web/mobile repos."
sources:
  - "https://www.w3.org/TR/WCAG22/"
  - "https://iso25000.com/index.php/en/iso-25000-standards/iso-25010"
  - "https://www.etsi.org/deliver/etsi_en/301500_301599/301549/03.02.01_60/en_301549v030201p.pdf"
  - "https://digital-strategy.ec.europa.eu/en/policies/web-accessibility-directive-standards-and-harmonisation"
claim: "For web/mobile user products, senior engineers build to WCAG 2.2 Level AA as the floor — semantic markup, full keyboard/screen-reader operability, ≥4.5:1 text contrast, 24px targets, visible focus — and gate it in CI with axe; for the EU market EN 301 549 makes WCAG AA a legal requirement, and ISO/IEC 25010 frames a11y as the broader Interaction Capability quality (learnability, operability, user-error protection, inclusivity)."
maps_from: []
---

> **Standard (claim):** WCAG 2.2 **Level AA** is the production floor for any user-facing web/mobile UI — semantic HTML + ARIA, keyboard + screen-reader operability, ≥4.5:1 contrast, ≥24px targets, visible non-obscured focus — enforced by automated a11y CI (axe) plus manual AT testing, and framed by ISO/IEC 25010 **Interaction Capability**; EN 301 549 makes WCAG AA *legally required* for the EU.
> **Evidence:** [lit] WCAG 2.2 · ISO/IEC 25010:2023 · EN 301 549 v3.2.1 · **Confidence:** high (named standards, two legally binding) · **Kind:** gated[web/mobile] · **Stage:** ③

**Seed sub-aspects:** `WCAG POUR / AA` · `semantic HTML / ARIA` · `keyboard / screen-reader` · `contrast` · `broader UX (learnability/operability/error-protection)` · `a11y CI (axe)`

## What professional engineers do

- **WCAG POUR / AA as the floor** `[lit]` — Build to the four W3C principles: **P**erceivable, **O**perable, **U**nderstandable, **R**obust, at the **Level AA** conformance tier (Level A = baseline, AAA = aspirational, not a blanket target). AA is the universally cited contractual/legal bar; senior teams treat it as the *minimum*, not the goal. WCAG 2.2 (Oct 2023) is the current rec — it is backward-compatible with 2.1 and adds 9 criteria (below).
- **Semantic HTML / ARIA** `[lit]` — Use native semantic elements first (`<button>`, `<nav>`, `<main>`, `<label>`-bound inputs, heading hierarchy); reach for ARIA only to fill gaps native HTML can't express ("no ARIA is better than bad ARIA"). Names, roles, and values must be programmatically determinable (WCAG 4.1.2 Robust) so assistive tech can expose them.
- **Keyboard / screen-reader operability** `[lit]` — Every interactive path must be fully operable by keyboard with no traps (WCAG 2.1.1/2.1.2), a logical focus order (2.4.3), and a **visible focus indicator** that 2.2 strengthens via *Focus Not Obscured (2.4.11, AA)*. Manual testing with real screen readers (NVDA, VoiceOver, JAWS) is non-negotiable — automation alone can't verify the AT experience.
- **Contrast** `[lit]` — Text/images-of-text ≥ **4.5:1** (large text ≥ 3:1) for AA (WCAG 1.4.3); non-text UI components and graphics ≥ 3:1 (1.4.11). Don't rely on color alone to convey meaning (1.4.1).
- **WCAG 2.2 new criteria** `[lit]` — Notably **Target Size (Minimum) 2.5.8 (AA, ≥24×24 CSS px)**, **Dragging Movements 2.5.7 (AA, a single-pointer alternative)**, **Accessible Authentication 3.3.8 (AA, no cognitive-function test like solving a puzzle)**, plus *Consistent Help (3.2.6)* and *Redundant Entry (3.3.7)*.
- **Broader UX / Interaction Capability** `[lit]` — ISO/IEC 25010:2023 elevates this beyond a11y compliance into a product-quality characteristic: **learnability, operability, user-error protection, appropriateness recognizability, user engagement, inclusivity, user assistance, self-descriptiveness**. Senior practice: error prevention/recovery (clear inline validation, undo, confirmation on destructive actions), consistent affordances, and inclusive design that widens the usable population — a11y is the floor of inclusivity, not the ceiling of UX.
- **A11y CI (axe)** `[lit]` — Wire automated checks into CI: `axe-core` via `jest-axe`/`@axe-core/playwright`, Lighthouse a11y audits, `eslint-plugin-jsx-a11y` at lint time. Automation catches ~30-50% of issues (contrast, missing alt/labels, ARIA misuse) and prevents regressions; the rest needs manual + AT review. Gate the build on zero new violations.

## Evidence (lit + census)

- `[lit]` **WCAG 2.2** (W3C Recommendation, 2023-10-05) — POUR principles; Levels A/AA/AAA; SC 1.4.3 contrast 4.5:1 (3:1 large); 2.4.11 Focus Not Obscured (AA); 2.5.7 Dragging Movements (AA); 2.5.8 Target Size Minimum 24×24px (AA); 3.3.8 Accessible Authentication (AA). https://www.w3.org/TR/WCAG22/
- `[lit]` **ISO/IEC 25010:2023** — *Interaction Capability* product-quality characteristic and its sub-characteristics (appropriateness recognizability, learnability, operability, user-error protection, user engagement, inclusivity, user assistance, self-descriptiveness). https://iso25000.com/index.php/en/iso-25000-standards/iso-25010
- `[lit]` **EN 301 549 v3.2.1** (ETSI/CEN/CENELEC harmonised European Standard) — Clause 9 references WCAG 2.1 Level A+AA for web; Clause 11 adds native-mobile requirements (gesture alternatives, orientation). It is the standard backing the EU Web Accessibility Directive and European Accessibility Act, so WCAG AA is *legally binding*, not optional. v3.2.1 is the current harmonised version; a v4 revision aligning to WCAG 2.2 AA is in progress (the EC confirms the update process has started but is not yet harmonised). https://www.etsi.org/deliver/etsi_en/301500_301599/301549/03.02.01_60/en_301549v030201p.pdf · https://digital-strategy.ec.europa.eu/en/policies/web-accessibility-directive-standards-and-harmonisation
- `[census]` — Literature-grounded aspect; a11y conformance is rarely a measurable repo-survey field, so no census % is claimed (see `census_todo`).

## Archetype variations

This aspect is **gated** — it fires only for the `web` and `mobile` archetypes (user-facing UIs).

- **web** — Full WCAG 2.2 AA: semantic HTML, ARIA, focus management, contrast, responsive/zoom (1.4.4/1.4.10), reduced-motion. axe/Lighthouse/jsx-a11y in CI. EN 301 549 Clause 9 applies for EU.
- **mobile** — WCAG principles apply but via platform AT (iOS VoiceOver + accessibilityLabel/traits; Android TalkBack + content descriptions); touch-target sizing (44pt Apple HIG / 48dp Material — both ≥ WCAG's 24px), gesture alternatives, dynamic-type/font-scaling, orientation support. EN 301 549 **Clause 11** governs native apps in the EU.
- **Non-gated archetypes** (cli, library, service/API, data-pipeline, ai-harness) — **no UI surface, so this aspect does not activate.** CLIs have their own usability conventions (clear help, exit codes, machine-readable output) but those live under UX/operability of the CLI aspect, not WCAG.

## Tradeoffs / what's ruled out

- **AA, not AAA, as the default** — AAA is not achievable or appropriate for whole sites (W3C itself says so); chasing it everywhere wastes effort. Ruled out as a blanket target.
- **Automated-only a11y is a false sense of safety** — axe/Lighthouse cover a minority of criteria; shipping on a green CI without manual AT testing is ruled out for production claims of conformance.
- **ARIA-first markup** — Heavy ARIA over native semantics increases bugs and AT breakage; ruled out in favor of native-HTML-first.
- **Cost/scope** — Retrofitting a11y is expensive; the tradeoff is paid down by building it in from the first component (design tokens for contrast, an accessible component library) rather than as a late audit.

## Sources

- WCAG 2.2 (W3C Recommendation) — https://www.w3.org/TR/WCAG22/
- ISO/IEC 25010:2023 Interaction Capability — https://iso25000.com/index.php/en/iso-25000-standards/iso-25010
- EN 301 549 v3.2.1 (ETSI harmonised standard) — https://www.etsi.org/deliver/etsi_en/301500_301599/301549/03.02.01_60/en_301549v030201p.pdf

## Sub-documents
- [`accessibility-legal-sources--facts-2026-08.md`](accessibility-legal-sources--facts-2026-08.md) — *research-log (ko)* — 2026-08-05 **법령 원문 재시도 패스(R4)**: 장차법 제20·21조(위키문헌 경유 — 국가법령정보센터 원문 미대조) · EAA 전자상거래 포함·미소기업 예외(**복수 2차 일치, Directive 원문 미확인**) · GDPR Art.13/14(요약본). ⚠️ **이 패스의 1차 확보는 0건**이며, 시행령 별표3(단계적 적용 대상)은 404로 미확보다. EUR-Lex는 3가지 URL 형식 모두 동적 로딩으로 실패 — **도구 환경 제약**으로 기록. 따라서 이 문서는 **"확인이 필요하다"는 신호까지만** 뒷받침하고 법적 의무 판정의 근거로 쓰지 않는다.
- [`accessibility-obligations--facts-2026-08.md`](accessibility-obligations--facts-2026-08.md) — *research-log (ko)* — 2026-08 facts-only pass (R3-1): WCAG 2.2 적합성 정의와 레벨 · **법적 의무 발생 조건 표**(유럽 접근성법 2019/882 · EN 301 549 · 한국 장차법/KWCAG · 미국 ADA Title II 최종규칙) · **자동 검사가 잡지 못하는 것**. ⚠️ EAA 조문 원문과 한국 법령 조항은 fetch 실패로 **미확보**(미해결 절 참조).
