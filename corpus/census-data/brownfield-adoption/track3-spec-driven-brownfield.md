# Track 3 (raw) — Spec-driven / AI-agent tools: attaching a planning layer to an EXISTING codebase

Research thread for gingoa's brownfield **①-plan mode**: an existing project's planning docs may be PRESENT / ABSENT /
DIFFERENT-FORMAT. How spec-driven & AI-agent tools bootstrap their planning layer onto existing code.

## Per-tool table
| Tool | Brownfield | Mechanism | Artifacts |
|---|---|---|---|
| **BMAD-METHOD** | EXPLICIT, first-class | Phase 0 `document-project` (flatten whole codebase) → `create-brownfield-prd` → `create-brownfield-architecture` → QA risk suite | flattened codebase doc; enhancement PRD; integration architecture; QA regression plan |
| **GitHub Spec Kit (`specify`)** | PARTIAL — `init --here` inits in existing repo but doesn't auto-ingest; Brownfield Bootstrap ext (#1436) scans stack+patterns | `.specify/memory/constitution.md`, `.specify/templates/{spec,plan,tasks}` — no PRD-equivalent |
| **Kiro** | PARTIAL — "Generate Steering Docs" auto-examines project; spec workflow itself greenfield-focused | `product.md`/`tech.md`/`structure.md` steering; live-file refs `#[[file:...]]` |
| **OpenSpec (Fission AI)** | BROWNFIELD-FIRST by design — delta specs on evolving code; `spec-gen` for cold-start | change folder (proposal/specs/design/tasks); `spec-gen` → `openspec/specs/*/spec.md` |
| **Tessl** | EXPLICIT reverse-engineering — `tessl document --code`, `@describe` | spec markdown w/ `@generate`/`@test`; codegen marked `// GENERATED FROM SPEC` |
| **Sourcegraph Cody** | CONTEXT ONLY — RAG over ≤10 repos; no spec/PRD gen | none (assistant) — brownfield value = contextual grounding |
| **Aider** | CONTEXT ONLY — graph-ranked repo-map; `/architect` mode | none persistent — conversational plans |
| **Continue.dev** | CONTEXT ONLY via Repomix MCP | Repomix flattened digest for context |
| **Copilot Workspace** | PARTIAL — task-scoped understanding; no PRD-level bootstrap | current/desired-state task docs; per-file plans |

## Key findings
1. **Three mechanisms, all tools use ≥1:** (A) FULL upfront reverse-engineer (BMAD, Tessl, spec-gen) — always
   "flatten/summarize the codebase FIRST", never code→PRD directly; PRD derived from the digest. (B) INCREMENTAL /
   change-level (OpenSpec official stance) — do NOT reverse-engineer the whole codebase upfront; write a narrow spec per
   change (current behavior · target · invariants · scope). (C) CONTEXT provision + fresh elicitation (Kiro/Aider/Cody/
   Continue) — existing code as context for human-directed AI; no PRD generated.
2. **Existing-doc handling (all treat as special case):** same-format present → REFERENCE directly (Kiro `#[[file:]]`,
   spec-kit constitution); different-format → manual convert + agent pass (no tool has explicit "format X→Y" pipeline;
   closest = spec-kit Brownfield Bootstrap regenerating from code); absent → REVERSE-ENGINEER from code+README (BMAD
   `document-project` most structured).
3. **BMAD's two-mode distinction = most transferable:** PRD-First (scoped PRD → document only relevant subsystems;
   large monorepos/known reqs) vs Document-First (flatten entire codebase → then PRD; small/med, unknown system).
4. **"Flatten/document-project" digest = the universal INPUT:** BMAD flatten, Aider repo-map, Repomix, Cody code-graph —
   all downstream spec/PRD generation draws from the structured digest, NOT raw source.
5. **Format-reconciliation is a real GAP:** no tool has an explicit "existing PRD format X → convert to Y" pipeline.

## Transferable to gingoa ①-plan brownfield — decision map
```
existing planning doc?
├── YES, same format (valid prd.yml/PRD.md)  → IMPORT: validate EARS, fill gaps via targeted elicitation
│                                               (Kiro reference-live-file + spec-kit research-doc)
├── YES, different format (Confluence/JIRA/README) → CONVERT: agent ingest → map to prd.yml schema, flag no-source fields
│                                               (BMAD document-first treats existing doc as the "digest")
└── NO (absent / code-only)                   → REVERSE-ENGINEER: flatten codebase → derive prd.yml from digest
                                                (BMAD document-project: flatten → PRD; mark INFERRED vs CONFIRMED; require user confirm)
```
**De-facto standard convergence:** (1) FLATTEN FIRST — structured digest before any PRD work; (2) SCOPE NARROWLY for
active dev (don't retro-spec the whole codebase); (3) NEVER trust AI-generated specs as authoritative — mark inferred
fields, require human confirmation; (4) REFERENCE over regenerate when a doc exists. BMAD `document-project →
brownfield-prd` = most adoptable for gingoa `elicit --mode=adopt` (absent-doc case); OpenSpec incremental = the
complement for ongoing brownfield work after the bootstrap.

## Sources
BMAD working-in-the-brownfield + DeepWiki brownfield-workflow + #563 · spec-kit #1436 Brownfield Bootstrap / #331 / #1285 ·
Kiro steering docs / Kiro-vs-OpenSpec · OpenSpec repo / #634 spec-gen / getting-started · Tessl blog + Fowler SDD-3-tools ·
Aider repomap docs+blog · Sourcegraph Cody context · intent-driven.dev brownfield · Augment Code brownfield guides · Copilot Workspace.
