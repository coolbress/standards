---
title: "Corpus Schema & Conventions"
status: verified
last_updated: "2026-06-25"
---

> ⚠️ **아카이브 (2026-08-02 감사)** — gingoa 시절 원문 보존본. 내부 상대 링크는 원 위치 기준이라 깨져 있을 수 있다. 활성 문서는 `../../corpus/`를 보라.

# Corpus Schema & Conventions

How this research corpus is structured, written, and maintained. Read once; it is the corpus's own
constitution (what `CLAUDE.md` is to the repo). Machine + human readable.

## 1. What this corpus is (and is not)
- **Is:** the general, evidence-based **"how do senior engineers do it"** reference. Aspect-organized
  (the [`TAXONOMY.md`](TAXONOMY.md) 28 aspects). gingoa consults it continuously while building.
- **Is not:** gingoa's own applied decisions. Those live in `docs/internal/` (prd.yml, PRD.md,
  ADRs) = gingoa's *application* of this reference to itself. Link the two via each aspect's
  `gingoa_applied:` frontmatter field. **Corpus = standard; `docs/internal/` = application.**
- **Axis:** aspect-primary (knowledge stored once per aspect) + **lifecycle overlay** ([`lifecycle.md`](lifecycle.md)):
  gingoa drives the user ①→②→③→④ and activates the relevant aspects at each stage gate.

## 2. Layout
```
research/
├── INDEX.md            # agent entry point — catalog of all aspects (GENERATED)
├── _schema.md          # this file — conventions
├── GUIDE.ko.md         # Korean reader's guide for the owner (the ONLY Korean corpus file)
├── TAXONOMY.md         # the locked 28-aspect set + anchoring + rationale
├── lifecycle.md        # stage → aspects activation overlay (hand-maintained)
├── aspects/NN-slug/    # one directory per aspect
│   └── _aspect.md      # the aspect's standard doc (split into more docs on growth)
└── census-data/        # immutable raw evidence (repo surveys, JSON) — never edited, only appended
```
**Language:** corpus is **English** (LLM-consumed). The single exception is `GUIDE.ko.md` (owner-facing).

## 3. Per-aspect document anatomy
Frontmatter (YAML) + a situating blockquote + fixed sections:

| Frontmatter field | Meaning |
|---|---|
| `id` | stable `aspect-NN-slug` |
| `title` · `group` | display name · taxonomy group (P/F/C/Q/R/G/S) |
| `kind` | `universal` \| `cross-cutting` \| `gated` \| `internal` |
| `gated_archetypes` | archetypes that activate a gated aspect (e.g. `["web","mobile"]`) |
| `cross_cutting` | `true` ⇒ fires at every lifecycle stage |
| `lifecycle_stages` | primary stage(s): `①②③④` or `all` |
| `anchors` | authoritative standards this aspect maps to (SWEBOK KA, ISO, etc.) |
| `evidence_track` | `census` \| `lit` \| `census+lit` — how this aspect is grounded (§4) |
| `status` | `stub` → `draft` → `verified` → `superseded` |
| `sources` | list of cited URLs |
| `claim` | one-sentence standard the doc establishes |
| `gingoa_applied` | path into `docs/internal/` where gingoa applied this (or empty) |
| `maps_from` | `census-data/` + `docs/internal/` source(s) that fed this aspect (collection scaffolding) |

Body sections (keep the headers stable so the agent can navigate):
`What professional engineers do` (the reference) → `Evidence (lit + census)` → `Archetype variations`
→ `Tradeoffs / what's ruled out` → `Implications for gingoa` → `Sources`.

**One doc = one purpose** (Diátaxis discipline). When an `_aspect.md` outgrows comfortable reading, split a
sub-aspect into its own `NN-slug/<subtopic>.md` and link it from `_aspect.md`.

### 3a. Sub-doc convention (consistency for everything that is NOT `_aspect.md`)
Any non-`_aspect.md` file under an aspect dir is a **sub-doc** and MUST carry this light frontmatter, so the
folder stays uniform and every file is self-describing + navigable back to its parent:

| field | meaning |
|---|---|
| `id` | `aspect-NN-slug--<subtopic-slug>` (parent id + `--` + slug) |
| `title` | display name |
| `parent` | the owning `aspect-NN-slug` (the discriminator: sub-docs have it, `_aspect.md` does not) |
| `kind` | `sub-aspect` (a split-out part of the standard) \| `evidence` (verified raw data backing the aspect) \| `research-log` (citation-dense research appendix) |
| `evidence_track` · `status` · `last_updated` | as for an aspect; `evidence`/`research-log` may add a `method:` line |

Always link a sub-doc from its `_aspect.md` (Sources or the relevant section). The generator only manages
`_aspect.md`; sub-docs are hand-authored and never clobbered.

**Per-aspect folder layout (standardized — follow for every aspect):**
```
aspects/NN-slug/
├── _aspect.md          # the standard doc — ALWAYS present; ends with a ## Sub-documents index IF any exist
└── <subtopic-slug>.md  # 0+ sub-docs — FLAT (no subdirs), §3a frontmatter, filename = the id's `--<slug>` suffix
```
- **Flat:** sub-docs sit next to `_aspect.md`; no nested folders inside an aspect.
- **Filename:** descriptive kebab `<subtopic-slug>.md` matching the sub-doc's `id` suffix (after `--`).
- **Index:** every `_aspect.md` that HAS sub-docs MUST end with a `## Sub-documents` section listing each as
  `- [`file.md`](file.md) — *kind* — one-line` (so the folder's contents are discoverable without grepping the
  body). Aspects with no sub-docs omit the section.
- **Raw evidence** (census records, gh counts) lives in `census-data/` (§4 / `census-data/README.md`), NEVER in
  an aspect folder — aspect dirs hold only the standard doc + its sub-docs.

### 3b. STANDING RULE — fold every new research INTO the corpus (don't leave it loose)
After ANY research pass (a survey, a [lit] dig, a tool comparison), **fold it into the corpus where it
belongs** — never leave it as a loose note at the root or only in chat:
1. Pick the **most-relevant aspect** (by SWEBOK KA / lifecycle stage). Add a concise paragraph to its
   `_aspect.md` "What professional engineers do" (or "Implications for gingoa") + add the new source URLs
   to its frontmatter `sources:`.
2. Drop the **citation-dense log as a sub-doc** under that aspect (`NN-slug/<topic>.md`, §3a frontmatter,
   `kind: research-log` | `evidence`) and link it from the `_aspect.md`.
3. If the research reveals a corpus GAP (a missing KA), that's a new-aspect decision (owner call) — see §2.
Example (2026-06-26): the AI-agentic-elicitation survey → enriched `aspect-01` + sub-doc
`01-requirements-planning/elicitation-prior-art.md`.

## 4. Evidence discipline (the two axes)
Every claim carries an evidence tag:
- `[lit]` — published, WebSearch-verified literature/standard. Used for *do-we-do-it?* (a senior practice,
  however rare in the wild). No fabricated citations.
- `[census]` — repo-survey adoption %, archetype-split, **recency-weighted where the preserved records contain
  `createdAt`** (`w = 0.5^(age/2yr)`, so trend beats survivorship bias). Legacy censuses without `createdAt`
  remain explicitly unweighted; their age cannot be reconstructed from star counts or current API state.
  Used for *do real repos expose it?* — the publish/default decision.
- `[inferred]` — our own routing logic (e.g. how the contract selects a conditional set).

Two independent questions: **do-it → `[lit]`** · **publish-to-remote → `[census]`**. An aspect's
`evidence_track` says which sources ground it; censusable aspects widen the census, practice/lit aspects
lean on literature.

**Publish-axis partition:** product code · README · LICENSE · CI · tests · manifest (census 86–99%) → published;
contract · specs · design docs · ADRs · planning/research notes · runbooks · threat models (census 13–19%) →
local/team (opt-in to publish ⚖️). Non-file foundation (branch-protection, review-enforcement, token-perms,
signed-releases) is judged **default-on vs opt-in** (also census-informed), not "publish".

**Reference-class caveat (2026-06-26):** the 13–19% planning-doc figure is a *broad-OSS* aggregate dominated by
solo hobby repos with no requirements process (selection bias) — it is the **wrong reference class** for deciding
where a *structured project's* spec/ADR output should live. The right cohort (spec-driven AI tools + the ADR/
docs-as-code community) is **unanimous: commit specs + ADRs to the repo and push** (Spec Kit/Kiro/BMAD/OpenSpec;
Nygard/Fowler/GDS/adr-tools). So for **gingoa's emitted ①-output in an end-user project, default = committed dir
(pushed)**, override-to-local for private/NDA concepts — NOT default-local. The local-default still applies to a
harness's *own internal* dogfood scratch (`docs/internal/`). Survey: `aspects/01-requirements-planning/elicitation-prior-art.md` §Naming & publish.

**Repo-context conditioning of "must-have" (2026-06-26):** a generic, public-repo/team standard checklist
**over-flags** for a real project's context. Before calling an absent floor item a *gap*, condition it on
three axes — **visibility** (public vs private), **plan** (free vs paid/GitHub Advanced Security), **team
size** (solo vs team). Examples that are context-*blocked*, not oversights: CodeQL code-scanning needs GHAS on
a private repo (→ Semgrep OSS instead); branch protection 403s on a private free plan; Dependabot-npm can't
scope the public registry on a private repo (→ `pnpm audit` compensates); CODEOWNERS/GOVERNANCE are
team-load-bearing. **Rule:** a context-blocked item is a *documented, condition-bound deferral with a
compensating control*, not a silent gap — the inverse of *presence≠adequacy* (here **absence can be
adequacy**, given context). When auditing artifact coverage, run the checklist THEN subtract context-blocked
items; never force-add a thing that cannot run. Full per-stage checklists: aspect-04 (② floor), aspect-17 (④).
The **machine-actionable** form — which GitHub features are gated by visibility×plan + the OSS substitute for
each + the private-default vs public-default floor + the `--make-public` flip list — is
`aspects/04-build-ci-engineering/visibility-provision-matrix.md` (the ② build branches on the ① `visibility` field).

**Census methodology (the corpus's own provenance — self-contained here, formerly in the legacy notes):**
- Sample: top-starred GitHub repos, **manifest-filtered** to real software (non-software excluded per Munaiah 2017,
  EMSE 2017). Sizes: dev-environment 429→**938** (deterministic re-census), governance/release-ops 429, harness 200.
- **Sample-expansion lesson:** the universal core (manifest/readme/gitignore/ci/license/test) is rock-stable across
  429→938 (±0–3pp); recommended/maturity tiers are *over-represented* in the top-429 and fall when widened (det-938
  is the more honest baseline for a new project). Naive top-N expansion pulls in non-software → always manifest-filter.
- **Non-file foundation** is measured via the **OpenSSF Scorecard public API** (per-check 0–10 scores), at **~59%
  scan coverage** (some checks — e.g. Branch-Protection — need admin/visibility → lower n). Raw `sc` scores per repo
  live in `census-data/census-governance` + `census-data/census-expanded`.
- **Raw-evidence layout is normalized** in [`census-data/README.md`](census-data/README.md): every census is a
  `census-<name>/` dir = `census.{py,sh}` collector + `records.json` (Mode A, per-repo) + `stats.json` (aggregates).
  Two modes: **A** per-repo record census, **B** aggregate `search/code` count census (`stats.json`-only, e.g.
  `census-doc-conventions` = the planning/spec/ADR naming·location·publish counts). Synthesis → aspect docs; this
  dir = immutable provenance (append-only).
- **Operate-attainment** (SLO/MTTR/incident) is not repo-censusable → `[lit]` + industry surveys (DORA, Grafana/Splunk).

## 5. Status lifecycle
`stub` (skeleton, no content) → `draft` (collected, unreviewed) → `verified` (cited + cross-checked) →
`superseded` (kept for history; points to its replacement). Agents should skip `superseded` and treat
`stub`/`draft` as incomplete.

## 6. Update protocol
- **Structure** (the 28 aspects, INDEX, lifecycle-map) was originally scaffolded from `TAXONOMY.md`, but the
  corpus is now **fully hand-curated** — edit `INDEX.md` / `lifecycle.md` / the aspect docs directly. To
  add/rename/split an aspect: edit `TAXONOMY.md` (the locked set), then add the aspect dir + INDEX/lifecycle
  entries by hand. (The one-time scaffolder was removed; do not regenerate over curated content.)
- **Content** (the prose inside each `_aspect.md`) is hand/collection-written and never overwritten by the
  generator — it skips any existing `_aspect.md` and only scaffolds a missing stub; `INDEX.md` and
  `lifecycle.md` are always refreshed. Safe to re-run anytime.
- **Census data** in `census-data/` is immutable raw evidence — append new surveys, never rewrite.
- `_legacy/` (pre-restructure Korean research) and `.scratch/template-direction.md` were **absorbed and removed**
  (2026-06-25): their methodology is now self-contained in §4 above; their decisions live in the aspects +
  ADR-0013/0014. Provenance for any claim is each aspect's own `## Sources`.

## 7. Provenance
Aspect set locked 2026-06-25 via four converging deep-research angles (foundational frameworks · cross-
framework · per-archetype · adversarial). See [`TAXONOMY.md`](TAXONOMY.md) for the full coverage check and
adjudicated decisions.
