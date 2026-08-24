---
id: evidence-policy
title: "Evidence Review and AI-Readable Corpus Policy"
kind: method
status: verified
last_updated: "2026-08-02"
evidence_track: lit
freshness: versioned
review_due: "2027-02-02"
sources: [FAIR-2016, W3C-PROV-O, RO-CRATE-1.2, NIST-RDAF-2.0, PRISMA-2020, KITCHENHAM-2007, AGENT-SKILLS-SPEC]
---

# Evidence Review and AI-Readable Corpus Policy

## Finding: there is no single AI-corpus standard

No ratified standard defines the best on-disk research architecture for coding agents. The defensible design is
a small synthesis of established practices rather than a new “perfect” format:

- FAIR supplies machine-actionable findability, explicit identifiers, provenance, and reuse principles.
- W3C PROV supplies a formal provenance vocabulary.
- RO-Crate supplies a JSON-LD packaging format for a research object and its related files and sources.
- NIST RDaF supplies research-data lifecycle coverage.
- PRISMA and software-engineering systematic-review guidance supply transparent question, search, selection,
  appraisal, and synthesis records.
- Agent Skills provides directly relevant evidence for progressive disclosure: compact metadata first,
  instructions second, and focused references only on demand.

`llms.txt` is an emerging website-orientation convention, not a ratified local-corpus standard. It is useful as
a curated web index when publishing documentation, but it neither controls access nor proves that general AI
systems use it. This local corpus therefore uses the existing `INDEX.md` role and does not add `llms.txt`.

## Evidence hierarchy is claim-relative

Do not use one global source ranking. Use the source that can actually establish the claim:

| Claim | Preferred evidence | Common category error |
|---|---|---|
| Standard requirement | current standards body specification/catalog | turning SHOULD into universal MUST |
| Product behavior/schema | current first-party docs + version | treating vendor docs as proof of effectiveness |
| Effectiveness/causality | replicated primary studies or systematic review | inferring causality from adoption |
| Industry prevalence | reproducible, representative census | calling common practice “best practice” |
| Operational lesson | scoped first-party postmortem/report | generalizing one organization to all teams |
| Design recommendation | explicit cross-source synthesis + tradeoffs | disguising author judgment as fact |

Secondary sources are discovery aids. They may remain when they add analysis unavailable in primary material,
but the document must label them and avoid routing an important factual claim through them when the primary
source is available.

## Review protocol

Each new research pass records:

1. Decision question and why it matters.
2. Scope, exclusions, and freshness horizon.
3. Search locations, query strings, and search date.
4. Inclusion/exclusion criteria and source-type target.
5. Extracted claim rows with source IDs and limitations.
6. Conflicts and negative evidence.
7. Synthesis, clearly labeled as synthesis.
8. Expiry trigger and next review date.

This is a pragmatic evidence review, not a “systematic review,” unless its search coverage and reporting really
meet the chosen systematic-review protocol. PRISMA is used as a transparency checklist, not as a quality score.

## AI-readable authoring rules

- One stable ID per document and per load-bearing claim.
- One topic/purpose per document; keep aspect sub-documents flat and directly linked.
- Put a concise scope statement before detail.
- Use descriptive headings and explicit tables for repeated fields.
- Keep source identity in structured JSONL and citations near claims.
- Separate raw evidence, evidence synthesis, and project decisions physically.
- Preserve contradictions; never ask a model to infer which number silently “wins.”
- Make volatile product claims carry `review_due` and an expiry trigger.
- Prefer deterministic indexes generated from metadata over hand-copied rosters.
- Validate structure mechanically; evaluate retrieval quality with representative questions before adding RAG,
  embeddings, or a knowledge graph.

## Search craft (absorbed 2026-08-02 from claudeck-v1 `researcher.md`)

Three collection rules from the claudeck-v1 researcher agent that this policy previously lacked. Provenance:
`legacy/sources/claudeck-v1/researcher.md`; the first rule is recorded as A/B-verified in that harness's own local
records (goppi design §8 cites it) — a local record, not independently replicated.

1. **Domain-scope the query when the term is also a product category.** When a technique's name doubles as a
   marketing category (rate limiting, caching, feature flags, message queues), unscoped web search returns the
   vendor layer and buries the primary source. Re-scope to the academic/primary domain (e.g. arxiv.org,
   dl.acm.org, standards bodies, first-party design docs); when the term is academia-owned the scoping is a
   harmless no-op, so the rule is no-regret.
2. **Budget ceilings per question — stop and report, don't grind.** Default ≤6 searches and ≤8 fetches per
   research question. Hitting the cap without convergence is itself a finding ("the answer is not cheaply
   available"), reported as such — never a license to keep fetching marginal pages.
3. **No-web fallback must be labeled, not silent.** If web tools are unavailable, answer from prior knowledge
   only under an explicit "unverified — no external sources" banner, marking individual uncertain claims;
   never present training-data recall as verified research.

Tool-specific mechanics in the original (context7-first, reader-proxy retry) are harness implementation
choices, out of scope for this policy; re-evaluate them at harness design time.

## Why Markdown + JSONL, with optional RO-Crate

Markdown is reviewable, diffable, and directly consumable by current coding agents. YAML frontmatter makes each
document self-describing. JSONL keeps source and claim records streamable and easy to validate. RO-Crate is kept
as an export boundary because its JSON-LD graph is strong for portable research packaging but costly to maintain
by hand. Contextual retrieval or embeddings are an optimization to test later, not a prerequisite for corpus
correctness.

## Sources

- `FAIR-2016` — https://www.go-fair.org/fair-principles/
- `W3C-PROV-O` — https://www.w3.org/TR/prov-o/
- `RO-CRATE-1.2` — https://www.researchobject.org/ro-crate/specification/1.2/
- `NIST-RDAF-2.0` — https://doi.org/10.6028/NIST.SP.1500-18r2
- `PRISMA-2020` — https://www.prisma-statement.org/prisma-2020
- `KITCHENHAM-2007` — https://madeyski.e-informatyka.pl/download/Kitchenham07.pdf
- `AGENT-SKILLS-SPEC` — https://agentskills.io/specification

