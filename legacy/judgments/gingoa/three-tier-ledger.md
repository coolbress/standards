---
id: three-tier-ledger
title: "gingoa's 3-tier governance/quality LEDGER — every scaffoldable item → tier → gate → condition → dogfood"
kind: synthesis-decision-ledger
status: VALIDATED (owner-locked 2026-07-07; tier calls + build sequence + the cost-of-wrong-default veto refinement confirmed — see Decisions D1–D6)
last_updated: "2026-07-07"
grounds_in:
  - "aspects/24-governance-collaboration-compliance/24-governance-collaboration-compliance--overview.md + issue-pr-writing-conventions.md"
  - "aspects/25-licensing-foss-compliance (license)"
  - "aspects/04-build-ci-engineering (CI floor)"
  - "aspects/05-scm-workflow (branch-protection / PR-first / merge policy)"
  - "census-data/census-governance-floor (N=6,582) · census-issue-pr (N=2000 + conventions N=1104)"
maps_to_memory: "governance-tier-model · census-governance-floor · template-standard-dogfood-gap"
---

> ⚠️ **아카이브 (2026-08-02 감사)** — gingoa 시절 원문 보존본. 내부 상대 링크는 원 위치 기준이라 깨져 있을 수 있다. 활성 문서는 `../../corpus/`를 보라.

# gingoa's 3-tier governance/quality LEDGER

The single "정확히 뭘 할지" lock: every scaffoldable governance/quality item, across all User Stories, placed
into a tier with its gate/locus, its archetype/audience condition, and its dogfood target. Grounded in the
census evidence — NOT re-derived from opinion. This is the deliverable that drives the per-US build; the build
is still sliced (evidence-ordered), but WHAT to build is fixed here.

## The discriminator (from [[governance-tier-model]])

Not majority-vs-minority, but **"can the non-engineer judge it, AND is it their context?"**

- **① AUTO (essential)** — census-standard OR minority-but-senior-craft the non-engineer can't judge → set
  automatically, with an honest "above-census enabler" label + an expert-mode opt-out (ADR-0012).
- **② SENIOR-DEFAULT** — protective craft, weak-in-the-wild, that a peerless non-engineer would never think
  to demand → default ON, escape-hatch available.
- **③ CONTEXT-CONFIRM** — genuinely the builder's project context (audience/archetype-dependent) → gingoa
  PROPOSES and the builder CONFIRMS; gated on a context signal that US-2 Elicit must ask.

### Tie-breaker & facets (refinement — owner-folded 2026-07-07 after a premium-model adversarial eval; cause = the verified LICENSE gap)

The two-part discriminator is **sound-but-needs-a-tie-breaker**:

- **★ Irreversibility / cost-of-wrong-default VETO over ① AUTO.** The judge-it/context test asks *who
  decides*, never *what a wrong default costs*. **A can't-judge item whose wrong default is costly ·
  irreversible · or asserts a commitment on the user's behalf MUST gate (elicit/confirm), regardless of the
  test.** LICENSE is the proof case — verified biting shipped code (`src/core/scaffold/license.ts`
  `DEFAULT_LICENSE="MIT"`, no elicit field → an irreversible legal/business pick auto-stamped un-asked). The
  cost axis is also the **objective anchor** for the otherwise-gameable "can they judge it" (which is a
  function of gingoa's *own* explanation quality — endogenous unless disciplined by cost).
- **"auto-DECIDE but must-ELICIT-data" facet (distinct from ③).** gingoa's judgment that an item belongs
  can be ①/② auto, yet it can't ACT without user-supplied content — LICENSE (holder + choice) · CODEOWNERS
  (usernames) · SECURITY (contact + the disclosure *commitment* only the user can make). Include-decided,
  **content-elicited** — the US-2→US-3 pipeline's core job (slice #2).
- **② = "applied-but-ANNOUNCED"** (① is silent). Without the visibility distinction, ②≡① (same opt-out
  mechanism; and only a judge-*capable* user opts out = not the target user). So ② = applied with a one-line
  why + an off-switch.
- **Declined ③ = accepted-risk-with-reason** (auditable), never a silent floor hole — else min-dimension
  scoring keeps a permanent weak link with no trail. Generalizes adopt's `n/a-with-reason`/`deferred`.
- **Solo-repo sub-setting gate** (design input for slice #4): branch-protection "require review" on the
  archetype **solo** user (1 non-engineer + AI) is a false-auto *deadlock* → the apply-step must gate that
  sub-setting on repo shape.
- **★ Transparency floor — no auto-set item is INVISIBLE** (owner-locked 2026-07-08; see D7). The tier controls
  *how loud the why is*, never *whether the user can see it*. This completes into ONE rule the pattern the model
  already applies piecemeal — ② = "applied-but-announced", ①-minority = "honest above-census label", declined-③
  = "accepted-risk-with-reason", skipped-② = a "logged NOTICE" (`aspects/04/visibility-provision-matrix`) — and
  extends it to **silent-①** (README / .gitignore / CI) too. Delivery = **progressive disclosure, NOT a blocking
  confirm** (confirming a craft item the non-engineer can't judge = decision-theater ≡ ③; a wall of equal-weight
  notices drowns the signal). Depth scales by tier: **silent-① = listed only · minority-①/② = listed + a one-line
  why + off-switch · ③ = recorded as "you confirmed"**. **Manifest home = the standard doc set, no new file**
  (grounds: `aspect-22` doc-roster — README ≈100% = "orientation+quickstart", CONTRIBUTING = the onboarding
  "runbook"; `aspect-23` scaffolding + "golden path ≠ golden cage" L55 / CNCF "benefit without needing to
  understand how it is provisioned" L32 = available-but-not-required; `aspect-04` L95 `.copier-answers.yml` = the
  machine ownership baseline): (1) **`.copier-answers.yml`** = machine/update provenance (exists, ADR-0003/0017);
  (2) **CONTRIBUTING.md** = the human manifest (items + tier/why + how-to-change/off), riding the ① floor file;
  (3) **README** = a one-line pointer + quickstart. **Rejected:** a novel top-level **`SCAFFOLD.md`** (absent from
  the census root roster → nonstandard clutter, competes with README for the "read-me-first" slot) and a
  **`.gingoa/` dotdir** (machine provenance already lives in `.copier-answers.yml`; a 2nd tool dir fragments the
  state + buries human prose in a dotdir nobody browses).

---

## Part A — the issue/PR template standard (grounds: conventions census N=1104, confirmed at N=6,582)

> Every convention below held within a few pp when re-harvested over the N=6,582 governance-floor pool
> (2425 template-bearing repos, star floor 29) — help-text 87.1→87.2, textarea 54→53, type-of-change 12% +
> free-text 1.6% all held. The tier calls are population-wide floors, not top-repo artifacts.
>
> A section-**roster** pass (`conventions.py roster`, 669 bug · 516 feature forms) then confirmed gingoa's
> shipped forms carry no missing floor section (bug = environment 83% / repro 74% / description 68% /
> expected 52% / logs 47% / context 41%; feature = problem 47% / proposed 51% / alternatives 27% / context),
> that the **preflight** add sits at a 24–26% senior minority, and that required-when-present tracks
> load-bearing sections (description 90% / environment 84% / repro 79% ↔ logs 22% / preflight 4% / context 3%).
> The roster *validated* the section design + the slice-#1 deltas; it surfaced no new section.

| Item | Tier | Evidence | gingoa today | Action |
|---|---|---|---|---|
| **bug + feature issue forms** | ① | bug 94% / feature 72% (the two GitHub defaults) | ships both | keep |
| **YAML forms (not legacy `.md`)** | ① | modern GitHub-recommended; forms lead top repos | ships forms | keep |
| **Writing method: textarea-for-prose · dropdown-for-enums · input-for-scalars** | ① | textarea 54% dominant | partial | conform shipped forms |
| **Required on load-bearing fields (not on checkboxes)** | ① | dropdown 73/input 65/textarea 57 ↔ checkbox 3.8 | partial | conform |
| **Help text on every field** | ① | 87% near-universal | partial | conform |
| **PR checklist ships EMPTY `- [ ]`** | ① | empty 62% (pre-checked 0.2%) | ships checklist | verify empty |
| **HTML-comment inline guidance** | ① | 70% | partial | conform |
| **Lean PR template (~3 sections: Summary/Testing/Checklist)** | ① | median 3 sections | ships 4 (incl. type-of-change) | see below |
| **"Type of change" section** | **DROP** | only 12% present; 85% checkbox not free-text; **duplicates the enforced CC PR-title** | ships it (free-text-ish) | **remove — redundant with `pr-title.yml`** |
| **`task` (3rd) issue form** | ② | task-class only 4% in wild → NOT census-standard, but a principled gingoa add (pr-title enforces 11 CC types; blank issues disabled) | ships it | keep as labelled add-on |
| **Preflight / "existing issue?" checkbox** | ② | 22% — senior dedup minority | not shipped | **add (senior-default)** |
| **In-form Code-of-Conduct checkbox** | ③ | 6% — context-gated | not in-form | leave to ③ CoC (audience-gated) |

## Part B — cross-US governance/quality items (grounds: governance-floor N=6,582)

| Item | Tier | Evidence (overall → gate) | US / locus | gingoa today |
|---|---|---|---|---|
| README · .gitignore · **LICENSE file** | ① | 100 / 99 / 94 | US-3 scaffold | ✅ (shipped #74) |
| **LICENSE *choice*** (which SPDX id) | ①-file · **must-elicit** (veto) | irreversible legal/business pick the non-engineer can't judge | US-2→US-3 | ⚠️ **`DEFAULT_LICENSE="MIT"` auto-stamped, no elicit → slice #2** |
| CI + lint/typecheck/test/build gates | ① | CI 85 | US-3/US-4 | ✅ |
| CC PR-title gate · squash-merge | ① | squash 97%; CC PR-title the enforced control | US-3/US-5 | ✅ `pr-title.yml` |
| SemVer · CHANGELOG · release notes | ① | release-ops census | US-5 release | ✅ core |
| **Branch protection** (review + green-CI merge gate) | ② | **13% strong — weakest control in the wild** | US-4 orchestrate | ⚠️ **decides, does not APPLY** |
| Code-review required | ② | 41% strong | US-4 | partial |
| Pinned GH Actions · least-priv token · secret-scan · dep-audit | ② | ~24–25% | US-3 | ✅ (floor) |
| CONTRIBUTING · SECURITY | ② | node/go/rust 65–70 / 32–43 | US-3 | ✅ (floor, content-asserted) |
| markdownlint · link-check · forbidden-terms | ② | docs-CI | US-3 | ✅ (floor) |
| **CODEOWNERS** | ③ | 12 → **31 monorepo** (cleanest gate) | US-2→US-3 | ⚠️ hardcoded `n/a` |
| **CODE_OF_CONDUCT** | ③ | 32 → 57 monorepo / public-audience | US-2→US-3 | ⚠️ `n/a` — **contradicts prd.yml:310** |
| Discussions · FUNDING · SUPPORT | ③ | 39 / 29 / 2 — community/OSS-gated | US-2→US-3 | not gated |
| CLA / DCO · GOVERNANCE · ADR-dir | ③ | 1–2% — rare, org/domain-gated | US-2→US-3 | n/a |
| Compliance (SOC2/ISO) · SLO/on-call · threat-model | ③ | `[lit]` domain-gated | off-repo | out of scope (default) |

---

## The enabling gap — why ③ is currently DOC-ONLY

Every ③ item is gated on a **project-context signal** (audience: public/private · archetype: monorepo/lib/cli/app)
that **US-2 Elicit does not ask** and the **schema does not carry**, so US-3 `cliFloorManifest()` is a zero-arg
static function that hardcodes CoC/CODEOWNERS to `n/a`. That hardcode **live-contradicts `prd.yml`** (which
says CoC `in`). ⇒ The whole ③ tier cannot function until the **US-2 → US-3 context pipeline** exists.

## Build sequence (evidence-ordered slices; each = own spec→PR)

1. **Template-standard tier-ify** (Part A) — DROP type-of-change, add preflight checkbox, conform the writing
   method (textarea/dropdown/required/help/empty-checklist/HTML-comments). **Dogfood: gingoa's own `.github/`
   AND `templates/ts-node-cli/template/.github/` identical.** Smallest, highest-clarity, already-researched.
2. **US-2 → US-3 context pipeline** (unblocks ALL ③) — add `audience` + `archetype` to the elicit schema,
   ask them in the interview, thread them to `cliFloorManifest(context)`, resolve the prd↔floor CoC
   contradiction. The structural keystone. **+ the first `must-elicit-data` case: LICENSE-choice elicitation**
   (owner-decided 2026-07-07 — the veto's proof case: ask the license, safe-default MIT + *announce* on no
   answer, per ②-applied-but-announced).
3. **③ propose+confirm set** riding the pipeline — CODEOWNERS (monorepo) · CoC (public) · Discussions/FUNDING
   (community/OSS), each gingoa-proposes / builder-confirms.
4. **Branch-protection apply-step** (②) — turn US-4's decide-only into an apply behind a human confirm
   (engine-locus: core decides, adapter applies).
5. **Expert-mode craft opt-out + transparency floor** (①) — generalise ADR-0012's danger-zone gate to a craft
   opt-out for the "above-census enabler" ① items, AND ship the transparency-floor manifest (D7): every auto-set
   item disclosed via `.copier-answers.yml` (machine) + CONTRIBUTING (items + tier/why + off-switch) + a README
   pointer, progressive-disclosure not blocking-confirm. Opt-out + disclosure are companions — an off-switch
   nobody can find isn't one.

## Decisions (owner-locked 2026-07-07)

- **D1 — DROP "Type of change"** from the shipped PR template. ✅ (grounded: 12% present + duplicates the
  enforced CC PR-title). Part of slice #1.
- **D2 — ADD a preflight "existing issue?" checkbox** to the issue forms as a ② senior-default. ✅ (22% in
  wild). Part of slice #1.
- **D2b — Conform the writing method** (textarea/dropdown + required-on-load-bearing + help-on-every-field +
  empty checklist + HTML-comment guidance). ✅ Part of slice #1.
- **D3 — Sequence: slice #1 (template tier-ify) FIRST, then slice #2 (context pipeline).** ✅ evidence/risk
  ordered — the small already-researched dogfood win before the structural keystone.
- **D4 — First ③ set = CODEOWNERS (archetype=monorepo) + CoC (audience=public).** ✅ CoC is forced (it is the
  live prd↔floor contradiction the pipeline resolves); CODEOWNERS is the cleanest-gated model ③ item.
  Discussions/FUNDING **deferred** to a later slice once the pipeline is proven.
- **D5 — Fold the irreversibility/cost-of-wrong-default VETO + 3 companion refinements** (must-elicit-data
  facet · ②=applied-but-announced · declined-③=accepted-risk-with-reason) into the tier model. ✅ owner-folded
  2026-07-07 after a premium-model adversarial eval; anti-supersede cause = the verified LICENSE gap. Does
  NOT change slice #1 (template items are all cheap + reversible).
- **D6 — LICENSE-choice elicitation → slice #2** (the first must-elicit-data case). ✅ not a fast-follow — it
  rides the context pipeline; MIT stays the safe default but is *announced*, not silently stamped.
- **D7 — Transparency floor + manifest home** (owner-locked 2026-07-08). ✅ *No auto-set item is invisible* —
  the tier controls loudness-of-why, not visibility; delivered as **progressive disclosure** (a durable manifest
  + a short scaffold-time headline), **never a blocking confirm** (a confirm on a craft item the non-engineer
  can't judge = decision-theater ≡ ③). **The manifest rides the standard doc set — no new file:**
  `.copier-answers.yml` (machine/update state, exists) + **CONTRIBUTING.md** (human: items + tier/why + off-switch)
  + a **README** one-line pointer. **Rejected** a new top-level `SCAFFOLD.md` (absent from the census root roster
  → nonstandard clutter) and a `.gingoa/` dotdir (fragments the existing copier-answers baseline; buries human
  prose). Companion to **slice #5** (an expert-mode opt-out is meaningless without the disclosure that surfaces the
  off-switch). Grounds: `aspect-22` doc-roster + `aspect-23` scaffolding/golden-path-not-cage + `aspect-04`
  copier-answers baseline. Folds from existing settled standards (synthesis, not new research). Refines
  [[governance-tier-model]].
