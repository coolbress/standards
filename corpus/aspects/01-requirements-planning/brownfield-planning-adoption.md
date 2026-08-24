---
id: aspect-01-requirements-planning--brownfield-planning-adoption
title: "Brownfield ①-plan adoption — importing / converting / reverse-engineering an existing project's requirements"
parent: aspect-01-requirements-planning
kind: research-log
evidence_track: lit
status: review-needed
last_updated: "2026-07-02"
method: "OSS + AI-agent-tool survey (2026-07-02) of how spec-driven & agentic tools attach a planning layer to an EXISTING codebase — BMAD, GitHub Spec Kit, Kiro, OpenSpec, Tessl, Aider, Repomix, Cody, Continue, Copilot Workspace. Raw thread: census-data/brownfield-adoption/track3-spec-driven-brownfield.md (+ track5 census). Grounds the ①-plan behaviour of a future `adopt` mode; the cross-stage spine is lifecycle.md §New vs Adopt."
---

# Brownfield ①-plan adoption — the requirements doc may be PRESENT / ABSENT / DIFFERENT-FORMAT

Why this exists: aspect-01's standard assumes gingoa **elicits** a requirements doc from a non-engineer at
maximum ignorance (greenfield). When gingoa is instead pointed at an **existing** project, the ①-plan input
already partially exists — as a valid doc, a different-format doc, or only as code. This logs how the field
bootstraps a planning layer onto existing code, and derives gingoa's ①-plan adoption behaviour. It is the
①-plan slice of the cross-stage `adopt` model (spine in [`lifecycle.md`](../../lifecycle.md) §New vs Adopt;
the ② foundation slice is [`../04-build-ci-engineering/brownfield-adoption-floor.md`](../04-build-ci-engineering/brownfield-adoption-floor.md)).

## The decision map (de-facto standard)

```
existing planning doc?
├── YES, same format (a valid prd.yml / PRD.md)          → IMPORT
│      validate EARS + 29148 well-formedness, gap-fill via targeted elicitation only.
├── YES, different format (Confluence / JIRA / README)   → CONVERT
│      agent ingests the source, maps to the prd.yml schema, FLAGS every field with no source.
└── NO (absent / code-only)                              → REVERSE-ENGINEER
       flatten the codebase into a structured digest FIRST, then derive prd.yml from the digest.
```

## What the field does (evidence)

- **Flatten-first is universal.** No tool derives a spec directly from raw source — they all build a *structured
  digest* of the codebase first, then generate requirements from the digest: BMAD Phase-0 `document-project`,
  Aider's graph-ranked repo-map, Repomix's single-file digest, Sourcegraph Cody's code-graph. `[lit]` The digest
  is the real input to ①-plan reverse-engineering; treating raw code as the input is the naive mistake.
- **Never trust an AI-generated spec as authoritative.** The load-bearing invariant across the mature tools:
  a reverse-engineered PRD is a *draft to confirm*, not truth. BMAD marks **INFERRED vs CONFIRMED** and requires
  human confirmation; this is exactly the input to gingoa's existing lock/seal gate (a doc cannot lock until the
  user confirms). `[lit]`
- **Existing doc → reference, don't regenerate.** When a same-format doc exists, tools reference it live rather
  than re-deriving (Kiro `#[[file:…]]` steering refs, Spec Kit's constitution/research docs). Regeneration is
  reserved for the absent case. `[lit]`
- **Two reverse-engineering depths (BMAD's split = most transferable).** *PRD-first* (scope a target PRD, then
  document only the relevant subsystems — for large/known systems) vs *document-first* (flatten the whole
  codebase, then derive the PRD — for small/unknown systems). gingoa's non-engineer + unknown-inherited-project
  case maps to document-first. `[lit]`
- **Format-reconciliation is a real gap.** No surveyed tool ships an explicit "existing PRD format X → prd.yml"
  pipeline; the closest is treating the foreign doc as the "digest" and running a conversion pass over it
  (BMAD document-first). So gingoa's CONVERT path is a genuine contribution, not a copy. `[lit]`
- **Incremental delta-specs complement the bootstrap.** OpenSpec's stance — do *not* retro-spec the whole
  codebase; write a narrow spec per change (current behaviour · target · invariants · scope) — is the right
  posture for ongoing brownfield work *after* the one-time import/convert/reverse-engineer bootstrap. `[lit]`

## Tool positions (survey)

| Tool | Brownfield ①-plan | Mechanism |
|---|---|---|
| **BMAD-METHOD** | first-class | `document-project` (flatten) → `create-brownfield-prd` → brownfield-architecture; INFERRED vs CONFIRMED |
| **GitHub Spec Kit** | partial | `specify init --here` in an existing repo; Brownfield-Bootstrap ext scans stack; no PRD-equivalent |
| **Kiro** | partial | "Generate Steering Docs" auto-examines the project; live-file refs `#[[file:…]]` |
| **OpenSpec** | brownfield-first | delta specs per change; `spec-gen` for cold-start |
| **Tessl** | explicit reverse-eng | `tessl document --code`; codegen marked `// GENERATED FROM SPEC` |
| **Aider / Cody / Continue** | context only | repo-map / code-graph / Repomix digest — grounding, no PRD generated |
| **Copilot Workspace** | partial | task-scoped current/desired-state docs; no PRD-level bootstrap |

## Implications for gingoa (①-plan adoption)

1. `adopt` ①-plan branches on **present-same → IMPORT · present-different → CONVERT · absent → REVERSE-ENGINEER**;
   the greenfield elicit engine (US-2) is reused for gap-fill and confirmation in all three.
2. **Reverse-engineer = flatten → digest → derive**, never code → PRD directly. The flatten step is a distinct
   capability to build (or shell out to Repomix-class tooling).
3. Every reverse-engineered / converted field is **INFERRED until the user confirms** — this rides gingoa's
   existing lock/seal gate: the carried prd.yml cannot become seal-valid on inference alone.
4. This ①-plan slice depends on a mature elicit engine (incl. the adversarial requirements review); sequence it
   *after* the elicit widening so the skeptic/confirmation machinery is reusable rather than re-built.

## Sources

- BMAD-METHOD — working-in-the-brownfield · `document-project` · brownfield-workflow (DeepWiki) · issue #563 — <https://github.com/bmad-code-org/BMAD-METHOD>
- GitHub Spec Kit — Brownfield Bootstrap #1436 / #331 / #1285 — <https://github.com/github/spec-kit>
- Kiro — steering docs — <https://kiro.dev/>
- OpenSpec (Fission AI) — delta specs · `spec-gen` #634 — <https://github.com/Fission-AI/OpenSpec>
- Tessl / Fowler "SDD — 3 tools" — <https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html>
- Aider repo-map — <https://aider.chat/docs/repomap.html> · Repomix — <https://repomix.com/> · Sourcegraph Cody context
- Raw threads: `census-data/brownfield-adoption/track3-spec-driven-brownfield.md`, `…/track5-census-existing-repo-mode.md`
