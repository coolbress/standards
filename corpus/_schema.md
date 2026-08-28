---
id: corpus-schema
title: "Evidence Corpus Schema"
kind: method
status: verified
last_updated: "2026-08-02"
evidence_track: lit
freshness: durable
sources: [FAIR-2016, W3C-PROV-O, RO-CRATE-1.2]
---

# Evidence Corpus Schema

This schema governs the active corpus. The inherited gingoa schema is preserved at
`../legacy/judgments/gingoa/schema.md`; it no longer governs because it mixed evidence, project
application, and retrieval rules.

> ⚠️ **2026-08-24 층 개편**: `imported/` + `interpretation/` → **`legacy/`** 로 통합됐고,
> **`direction/`**(결론 층)이 신설됐다. 아래 표는 그 개편을 반영한다.

## 1. Layers and authority

| Layer | Purpose | May contain goppi decisions? | Mutable? |
|---|---|---:|---:|
| `corpus/methods/` | evidence and curation rules | no | yes, reviewed |
| `corpus/aspects/` | topic synthesis and claim registers | no | yes, reviewed |
| `corpus/census-data/` | raw or derived local empirical evidence | no | append-only |
| `legacy/sources/` | immutable historical source copies (구 `imported/`) | historical content only | no |
| `legacy/judgments/` | 폐기된 하네스의 결론·비교·결정 (구 `interpretation/`) | historical | reviewed |
| `direction/` | **현행 방향과 계획** — 이 저장소의 결론 층 (2026-08-24 신설) | yes | yes |
| `audit/` | manifests, findings, dispositions, validation reports | no | append-only per audit |
| `archive/` | recoverable material removed from active retrieval | historical content only | no |

The active corpus is an **evidence base**, not a bag of “objective truth.” A claim is acceptable only when its
source, scope, evidence class, and uncertainty are visible. Source authority is always relative to the claim:
official product documentation is authoritative for a product's interface, not for the product's effectiveness.

## 2. Document types

- `<topic>--overview.md`: bounded topic synthesis. It is not automatically normative and must not contain project-specific
  application decisions.
- `reference`: a focused, source-backed build or interface reference.
- `research-log`: search and extraction record; may contain unresolved conflicts.
- `evidence`: local empirical result or a stable pointer to raw data.
- `method`: corpus-wide research or curation rule.
- `navigation`: non-evidentiary index or crosswalk.

### 2.1 File naming — new files only (added 2026-08-08)

**Question first, date last.** `<question-topic>--<artifact>-<YYYY-MM>.md`
— e.g. `accessibility-obligations--facts-2026-08.md`, not `facts-2026-08-accessibility.md`.

Rationale: a filename is a retrieval surface. Front-loading `facts-2026-08-` spends the first 16 characters
on metadata that belongs in front matter, pushing the actual question past where a file-selection step reads.
Dates stay in the name **only** for append-only records (evaluation runs, incidents, snapshots), where the
date *is* the identity.

### 2.2 The one rename that was executed — `_aspect.md` → `<topic>--overview.md` (2026-08-08)

The per-topic overview file used to be named `_aspect.md` in all 28 directories. **The same basename 28 times
meant any filename-level search returned 28 indistinguishable hits** — 28 of the 41 non-unique basenames in the
tree. It was renamed to `<topic>--overview.md` (e.g. `08-software-testing--overview.md`).

This was executed only after the blockers were removed, in this order:

1. **Stable ids** were emitted into `ROUTES.jsonl` (183 unique, zero collisions) with an `aliases` field, so a
   rename no longer severs document identity.
2. **`validate_corpus.py`** stopped branching on a hardcoded basename; it now derives the overview name from the
   directory (`aspect_overview_path` / `is_aspect_overview`), and a regression test asserts that a stale
   `_aspect.md` **does not** satisfy the check — otherwise a half-landed rename would report green.
3. **Path-carrying ledgers** were updated: `audit/after-manifest.tsv` regenerated, `audit/retrieval-cases.jsonl`
   30 `expected_path` values rewritten, plus in-document links.
4. **Deliberately not touched** — historical records: `audit/before-manifest.tsv` (pre-curation state),
   the `arm == "before"` branch in `tools/evaluate_retrieval_before_after.py`, `legacy/judgments/`,
   and `audit/ARCHIVE-LEDGER.md`. Rewriting those would falsify history.
5. **Safeguard**: `archive/2026-08-08/pre-rename-snapshot.tar.gz` (323 files, SHA-256 in the ledger). The tree is
   not under version control, so the snapshot is the only rollback path.
6. **Regression gate**: the retrieval contract must still pass 30/30. A rename that breaks retrieval is reverted.

The rename map is recorded at `audit/rename-map-2026-08-08.json`.

⚠️ **Still do NOT bulk-rename anything else without repeating steps 1–6.** The naming rule in §2.1 applies to
new and substantially-rewritten files; it is not a licence to sweep the tree.

## 3. Required metadata

Every new curated Markdown document starts with YAML frontmatter containing:

```yaml
id: stable-kebab-id
title: "Human-readable title"
kind: reference              # aspect | reference | research-log | evidence | method | navigation
status: draft                # imported | draft | review-needed | verified | superseded | retracted
last_updated: "YYYY-MM-DD"
evidence_track: lit          # lit | census | census+lit | none
freshness: versioned         # durable | versioned | volatile
review_due: "YYYY-MM-DD"     # required for versioned/volatile material
sources: [SRC-ID]
```

Aspect documents keep their stable `aspect-NN-slug` ID plus `group`, `kind` (applicability),
`lifecycle_stages`, `anchors`, and `claim`. During the 2026-08 audit, inherited documents use
`status: review-needed` until their individual claims meet this schema.

### 3.1 `gated_archetypes` — who owes this aspect (added 2026-08-28, `GAPS` R5-16)

Every aspect overview carries `gated_archetypes`. `direction/05` builds its whole archetype layer on
this field, **yet it had no definition here and no check** — the field appeared 0 times in this schema
and 0 times in `validate_corpus.py`. This section is that definition.

```yaml
gated_archetypes: []                      # universal — every project owes this aspect
gated_archetypes: ["backend", "data-ml"]  # gated — only these owe it
```

**`[]` means universal, not "unspecified".** A missing key is an error; an empty list is a claim.

🔴 **The field carries two different things and that is deliberate.** Both are *gates*, but they are
answered differently:

| axis | values | answered by |
|---|---|---|
| **project kind** — what the thing is | `cli` `library` `web` `backend` `mobile` `data-ml` | one choice at creation |
| **condition** — a property the project has | `published` `cloud` `handles-user-data` `ai-harness` | yes/no, can change later |

A project matches an aspect if it matches **any** listed value. `handles-user-data` is one of the
three questions `/kickoff` asks, so a condition gate is answerable without inventing a questionnaire.

⚠️ **`[]` must not be used to mean "we did not decide."** If an aspect's own claim presupposes a
condition — *"instrument **services**"*, *"operate a **running service** against SLOs"*,
*"publishes to the **canonical channel**"* — then it is gated, and writing `[]` makes the floor
demand SLOs and on-call from a local CLI script. `validate_corpus.py` cannot read intent, so this
one stays a human rule; what it does check is that every aspect **has** the key and that every value
is from the closed set above.

## 4. Claim record

New or materially refreshed syntheses use a claim table:

| Claim ID | Class | Claim and scope | Evidence | Confidence | Valid as of / expiry |
|---|---|---|---|---|---|

Allowed classes:

- `definition`: a source's definition, attributed to it.
- `normative`: a requirement from a named standard or official specification; preserve MUST/SHOULD strength.
- `empirical`: an observation with population, sample, method, and limitations.
- `vendor-behavior`: current documented behavior of a named product/version.
- `synthesis`: a conclusion derived across sources; never presented as source text.
- `local-census`: a result from this corpus's data and code; prevalence is not quality.

Every claim cites one or more source IDs or a corpus evidence path. Conflicting results remain separate; they
are not averaged or silently reconciled. Exact quotations are exceptional and short.

## 5. Status semantics

- `imported`: immutable source copy, not endorsed.
- `draft`: incomplete collection or extraction.
- `review-needed`: inherited or changed synthesis whose claim-level support has not passed the current policy.
- `verified`: required metadata complete; each material claim traceable; source scope checked; conflicts and
  limitations stated; relevant validator checks pass; reviewer recorded.
- `superseded`: retained for history and linked to its replacement.
- `retracted`: known incorrect or unsafe to rely on; reason required.

`verified` is not permanent. A versioned source update, expiry trigger, contradicted claim, or material method
defect returns the document to `review-needed`.

## 6. Retrieval contract

Agents load progressively:

1. `INDEX.md` and its audit banner.
2. The relevant aspect's frontmatter, summary, and sub-document index.
3. Claim rows needed for the question.
4. Source-registry records and raw evidence only when validating or resolving a conflict.

Agents must not treat `review-needed`, `draft`, `legacy/`, or `archive/` as verified general
evidence. Retrieval status and evidence strength are filters, not prose hints.

## 7. Source registry and provenance

Canonical sources used by newly curated documents are registered in `_meta/sources.jsonl`. Each record includes
an ID, URL, publisher, source type, what it is authoritative for, access date, and freshness class. The registry
does not replace nearby citations; it prevents identity and version drift.

The optional export `ro-crate-metadata.json` may be generated when the research package is shared or archived.
RO-Crate is useful for packaging and provenance, but is not required for day-to-day Markdown authoring.

## 8. Mechanical validation

Run:

```sh
python3 .scratch/research/tools/validate_corpus.py
```

The validator checks active-file inventory, non-empty exact file and substantial-section repeats,
generated/dead artifacts, required aspect files, all `verified` frontmatter, registered source references,
claim rows in verified references, internal links, and legacy gingoa markers. The separate retrieval-contract
check verifies 30 pre-registered routes and bounded read surfaces. External-link reachability, semantic
duplication, model behavior, and claim truth require separate checks and are never inferred from a green
structural result.
