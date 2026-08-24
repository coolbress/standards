# Per-feature spec doc — re-validation census (2026-06-27)

> Raw deposit for an owner-requested **re-validation** of the settled per-feature-spec standard in
> [`../../aspects/01-requirements-planning/planning-document-family.md`](../../aspects/01-requirements-planning/planning-document-family.md).
> Scope = exactly four points: (1) storage location, (2) authoring/structure, (3) file naming,
> (4) publish-to-remote. Method: four parallel researchers — (A) standards+academic, (B) SDD
> frameworks, (C) top-star GitHub census, (D) practitioner articles. Question asked of each:
> *does fresh authoritative evidence SUPERSEDE the standard?* Verdict per point ∈ {CONFIRM, REFINE,
> SUPERSEDE}.

## Standard under test
- **Location:** `docs/specs/<feature-slug>/spec.md` (per-feature folder; `design.md`/`plan.md`/`tasks.md` alongside)
- **File name:** fixed `spec.md`, NO date prefix (the slug folder carries identity)
- **Sections:** Overview(→PRD) · User-stories(P1/P2/P3) · Acceptance-criteria in **EARS** · FR-NNN · feature-NFR delta · Edge-cases · Assumptions · Out-of-scope · `[NEEDS CLARIFICATION]`
- **Publish:** commit **and** push (public for OSS); volatile `plan` gitignored-local; research/internal never pushed

## Verdict matrix (4 points × 4 angles)
| Point | A. Standards/academic | B. SDD frameworks | C. Top-star census | D. Practitioner | NET |
|---|---|---|---|---|---|
| **1 — Location** | CONFIRM (silent on repo paths by construction) | REFINE (`specs/`-root) | REFINE (`specs/`-root / RFC=dedicated repo) | REFINE-med (split, no authority) | **REFINE — stands; `docs/specs/` is minority but not forbidden** |
| **2 — Structure** | CONFIRM (SWEBOK v4 §4.3 AC-spec + EARS RE'09/2019 stable; minor: 29148 §5.1 per-req rationale) | CONFIRM (matches Spec-Kit P1/P2/P3+FR-NNN, Kiro EARS; `[NEEDS CLARIFICATION]` is inline in Spec-Kit) | CONFIRM (folder-per-feature quartet = both tools) | no-evidence (LOW; blogs don't cover EARS) | **CONFIRM (+2 minor enhancements)** |
| **3 — Naming** | CONFIRM (silent; SRS=doc TYPE not filename) | CONFIRM (fixed `spec.md`+no-date; REFINE folder `NNN-`) | CONFIRM (`spec.md` census-validated; NNNN=RFC-governance only) | CONFIRM-HIGH (date-prefix = Jekyll origin, zero spec backing; MADR NNNN = ADR not spec) | **CONFIRM (strong)** |
| **4 — Publish** | CONFIRM (IEEE-830 §5.2 + 29148 §6 = configuration management) | CONFIRM (Kiro explicit "commit alongside code"; Spec-Kit branch→PR) | CONFIRM (universal; 0 counter-examples) | CONFIRM (Addy Osmani, Fowler, dein.fr) | **CONFIRM (strong)** |

**Headline: NO SUPERSESSION on any of the four points.** The standard is re-confirmed. The generic
spec-skill defaults (`docs/product-specs/YYYY-MM-DD-<slug>.md`) are NOT backed for feature specs and are
correctly overridden by the corpus.

## Key debunk — date-prefix has no authority for specs
Date-prefix (`YYYY-MM-DD-slug.md`) originates in **Jekyll `_posts/`** (a hard blog-post parsing
requirement) and chronological data-management series — neither applies to feature specs. **MADR's
`NNNN-title.md` is an ADR convention** (a monotonic decision log where the number IS the permanent
identity), not a per-feature artifact. The closest direct precedent — GitHub Spec-Kit — uses a fixed
`spec.md` with the folder carrying identity, identical to the standard under test.

## RFC/proposal cluster ≠ feature-spec cluster (do not conflate)
Top-star census splits cleanly:
- **RFC/governance** (Rust `text/NNNN-title.md`, K8s `keps/sig-x/NNNN-title/README.md`+`kep.yaml`,
  Python `peps/pep-NNNN.rst`, React/Vue/Ember/Swift `NNNN-title.md`, TC39 = one repo/proposal) — number
  prefix = citable permanent identity; lives in a **dedicated repo**. 6/7 number-prefixed.
- **In-repo feature specs** (Spec-Kit `specs/NNN-slug/spec.md`, Kiro `.kiro/specs/<slug>/requirements.md`,
  OpenSpec `openspec/specs/<domain>/spec.md`) — folder-per-feature; Kiro/OpenSpec use **bare slug**, Spec-Kit
  uses a light `NNN-` ordering prefix. gingoa = bare slug → in the Kiro mainstream.
The NNNN-prefix is an RFC pattern; applying it to feature specs is a category error.

## REFINE signals (enhancements, not supersessions)
1. **Location** — external mainstream is `specs/`-at-root (Spec-Kit) or tool-namespaced (`.kiro/`,
   `openspec/`); none use `docs/`. `docs/specs/` is minority BUT internally consistent with gingoa's
   already-locked `docs/adr/` (census 5,088) + `docs/PRD.md`. **Keep gingoa's OWN spec at `docs/specs/`**;
   the **emit-side** (the elicit feature writing specs into a *user's* repo) should consider matching the
   `specs/`-root tooling default or being configurable — a US-3 / elicit-Slice-2+ decision, NOT this slice.
2. **Per-requirement rationale** — 29148 §5.1 lists a rationale attribute per requirement. gingoa carries
   a doc-level `Decisions & Rationale` nucleus (coarser). Per-req rationale is optional finer-grain.
3. **Inline `[NEEDS CLARIFICATION]`** — Spec-Kit embeds the marker INLINE at the point of ambiguity (agents
   scan for it to detect incomplete specs), vs a standalone appendix section. The inline form directly
   strengthens gingoa's elicit **lock-gate** (lock requires 0 markers — easier to detect inline). **Adopt
   inline markers** (optionally + a rollup). Relevant to US-2 Slice 1.
4. **Folder `NNN-` numbering** (Spec-Kit) — defer; bare slug matches Kiro/OpenSpec and gingoa has no
   branch-per-spec / Spec-Kit-CLI 1:1 traceability need today.

## Quantitative census — top-453 repos (stars > 50000), 2026-06-27
Owner-requested hard numbers. Population = the 453 most-starred public repos (`gh search/repositories
q=stars:>50000`); each repo's default-branch tree fetched recursively and classified. Raw:
[`spec-revalidation-top453-rows.tsv`](spec-revalidation-top453-rows.tsv) · repo list
[`spec-revalidation-top453-repos.txt`](spec-revalidation-top453-repos.txt) · script
[`spec-revalidation-census.sh`](spec-revalidation-census.sh). (6/453 trees truncated → tiny undercount.)

| Convention (dir present) | count / 453 | % | example repos |
|---|---|---|---|
| `docs/specs/` | 3 | 0.7% | openclaw, appwrite, paperclip |
| root `specs/` | 5 | 1.1% | opencode, warp, realworld, open-design |
| `.kiro/specs/` | 0 | 0.0% | — |
| `openspec/` | 1 | 0.2% | Fission-AI/OpenSpec (the tool itself) |
| `rfcs/` (anywhere) | 6 | 1.3% | torvalds/linux, rust-lang/rust, moby, strapi, atom |
| `proposals/` | 5 | 1.1% | nodejs/node, swiftlang/swift, rust, 996.ICU |
| `adr`/`adrs`/`docs/decisions` | 6 | 1.3% | TryGhost/Ghost, mattpocock/skills |
| any `spec.md` file | 11 | 2.4% | — |
| has `docs/` at all | 200 | 44.2% | — |
| **ANY structured spec/RFC/ADR dir** | **24** | **5.3%** | — |

**Global code-search (all GitHub, `search/code` total_count — selection-biased, complements the top-N):**
`path:docs/specs filename:spec.md` = **3,632** · `path:specs filename:spec.md` = **2,976** · `filename:spec.md`
= **41,696** · `.kiro/…/requirements.md` = 1,904.

### What the numbers say (the two points the owner asked)
- **LOCATION — no dominant convention; `docs/specs/` is NOT a minority outlier.** In the top-453, `docs/specs/`
  (0.7%) and root `specs/` (1.1%) are statistically tied — both ~1%, neither dominates. But GLOBALLY (all of
  GitHub) `docs/specs/spec.md` (**3,632**) actually **exceeds** `specs/spec.md` (**2,976**) — so once the
  spec-driven long tail is included, `docs/specs/` is the *marginally more common* home for a `spec.md`. The
  framework DEFAULTS differ (Spec-Kit root `specs/`, Kiro `.kiro/`) but the file population favors `docs/specs/`.
  → gingoa's `docs/specs/` is **CONFIRMED**, not a deviation (and it's internally consistent with `docs/adr/`).
- **PUBLISH — commit+push, unambiguous.** All 453 repos are public; 24/24 that maintain spec/RFC/ADR dirs keep
  them committed + pushed + public. **Zero** local-only counter-examples — and gitignored specs are *unobservable*
  by construction, so the census can't even attest the alternative exists. Combined with explicit tool guidance
  (Kiro "commit alongside code"), practitioner unanimity (Osmani/Fowler/dein.fr), and the standards' CM mandate
  (29148 §6 / IEEE-830 §5.2), commit+push is the only attested practice. → **CONFIRMED (strong).**

### The 5.3% rarity is selection bias, not a counter-standard
Only ~5% of even the top-453 carry ANY structured spec/RFC/ADR dir — the SAME effect this aspect's
[`planning-output-census.md`](../../aspects/01-requirements-planning/planning-output-census.md) and
`planning-document-family.md` §"Why the broad repo census shows PRD 0.4% / ADR 1.1%" already explain: top OSS
repos are libraries / learning-resources / frameworks run by **senior teams who carry requirements context
implicitly** (heads + issues + PR threads); RFC processes often live in **dedicated repos** (rust-lang/rfcs's
specs are under `text/`, not caught as `specs/`); and the structured **spec-driven cohort** (Spec-Kit/Kiro/
OpenSpec) is newer and sits in the long tail, not the legacy top-500. gingoa's user (a non-engineer + an agent
with no cross-session memory) is the **opposite** of that senior-team cohort, so the committed PRD/spec/ADR is
the scaffolding that *substitutes* for tribal knowledge. The rarity **confirms the corpus's existing reasoning**
— it is not evidence against the standard.

**Objective assessment of the write+push *direction* (folded into `planning-document-family.md` §Re-validation):**
the direction is right for a *falsifiable* reason — gingoa's user lacks the senior-tribal-knowledge precondition
the 95% rely on — but the justification is **conditional** on two disciplines (the spec is *load-bearing* per
ADR-0014, and *tier-limited* to Tier-3-equivalent changes per ADR-0019), collapsing to ceremony tax if either
fails. **push** is low-regret/net-positive (the SSOT travels across sessions/agents); **location** is data-settled
(`docs/specs/` ≈/≥ root `specs/`). The residual risk is spec **liveness (drift)**, not file location — so further
location/publish verification is exhausted; the open work is keeping specs alive while building.

## Sources (verified 2026-06-27)
**Standards/academic:** ISO/IEC/IEEE 29148:2018 (§1 scope, §5.1 traceable+rationale, §6 req-management) https://ieeexplore.ieee.org/document/8559686 · IEEE 830-1998 (§5.2 modifiable, CM) https://ieeexplore.ieee.org/document/720574 · SWEBOK v4.0 KA1 §4.3 AC-based spec https://ieeecs-media.computer.org/media/education/swebok/swebok-v4.pdf · EARS RE'09 https://dl.acm.org/doi/10.1109/RE.2009.9 + "Ten Years of EARS" IEEE Software 2019 https://dl.acm.org/doi/abs/10.1109/MS.2019.2921164 · Adv-EARS · SDD survey arXiv:2602.00180 · Spec Kit Agents arXiv:2604.05278 · GenAI-for-RE SLR arXiv:2409.06741
**SDD frameworks:** github/spec-kit (README + spec-driven.md + templates/spec-template.md) https://github.com/github/spec-kit · Kiro specs + best-practices https://kiro.dev/docs/specs/best-practices/ · OpenSpec (Fission-AI) getting-started.md + concepts.md https://github.com/Fission-AI/OpenSpec · BMAD-METHOD https://github.com/bmad-code-org/BMAD-METHOD · Tessl https://docs.tessl.io/use/spec-driven-development-with-tessl · Fowler SDD-3-tools https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html
**Top-star census:** rust-lang/rfcs `text/NNNN` · kubernetes/enhancements `keps/sig-x/NNNN-title/README.md`+`kep.yaml` · python/peps `pep-NNNN.rst` · reactjs/rfcs · vuejs/rfcs `active-rfcs/NNNN` · emberjs/rfcs · swiftlang/swift-evolution `proposals/NNNN-title.md` · tc39/template-for-proposals (repo-per-proposal, `README.md`+`spec.emu`)
**Practitioner:** MADR https://github.com/adr/madr · Jekyll posts (date-prefix origin) https://jekyllrb.com/docs/posts/ · Addy Osmani "good spec" https://addyosmani.com/blog/good-spec/ · dein.fr "move your docs in the repo" https://www.dein.fr/posts/2026-03-13-its-time-to-move-your-docs-in-the-repo · SWE-at-Google ch10 https://abseil.io/resources/swe-book/html/ch10.html · Spotify monorepo docs https://engineering.atspotify.com/2019/10/solving-documentation-for-monoliths-and-monorepos
