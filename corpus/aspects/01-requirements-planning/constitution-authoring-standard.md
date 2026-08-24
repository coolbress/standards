---
id: aspect-01-requirements-planning--constitution-authoring-standard
title: "Agent-constitution authoring standard — AGENTS.md / CLAUDE.md (how to write a good one)"
parent: aspect-01-requirements-planning
kind: research-log
evidence_track: census+lit
status: review-needed
last_updated: "2026-06-27"
method: "Survey (2026-06-27) of the agents.md open spec + OpenAI/Codex docs + Anthropic Claude Code best-practices + GitHub 2,500-repo analysis + arXiv empirical studies (2602.11988, 2601.20404) + named repos. The constitution kind is a MANDATORY ① artifact for any AI-agent-driven project (e.g. gingoa); this is HOW to author it. Adoption census in census-doc-conventions (AGENTS 129,696 / CLAUDE 40,200)."
---

# Agent-constitution authoring standard (AGENTS.md / CLAUDE.md)

The constitution/steering kind ([`planning-document-family.md`](planning-document-family.md)) is **mandatory**
for any project an AI agent must operate to build — it is the per-session instruction file the agent reads
every run. This is the *how-to-write* standard (the family doc says *what kind*; this says *how*).

## Discovery + dual-file (CLAUDE.md vs AGENTS.md)
- **CLAUDE.md** — Claude Code reads it at session start, **loaded unconditionally every run** (every token
  competes for context). Hierarchy: `~/.claude/CLAUDE.md` (global) → `./CLAUDE.md` (project, committed) →
  `./CLAUDE.local.md` (personal, gitignored) → parent/child dirs (monorepo). `@path` **imports** another file.
- **AGENTS.md** — the open cross-vendor standard (Codex, Cursor, Aider, Jules, Copilot, Zed, RooCode; formalized
  2025). Codex walks root→cwd, `AGENTS.override.md` wins per level, **32 KiB** merged cap, no import syntax.
- **Dual-file rule:** keep **ONE source of truth (CLAUDE.md)** + **AGENTS.md = a mirror** (symlink for zero
  drift, or a maintained condensed subset). State "X is SSOT; Y mirrors it" at the top of both. Two independent
  files drift. gingoa keeps CLAUDE.md = SSOT + a condensed AGENTS.md mirror (both hosts have slightly different
  reading limits → maintained mirror, not symlink).

## Section skeleton (high-value first)
1. **One-line header** — what the repo is + the SSOT/mirror note.
2. **Build & verify** — EXACT commands (install/lint/typecheck/test/build) WITH flags; the single highest-value
   content (the agent can't guess non-standard script names). Include a **single-test** invocation.
3. **Code style** — rules that DIFFER from language defaults, as code snippets (not prose); naming/import conventions.
4. **Architecture** — 2–3 bullets of non-obvious structure only; link out, don't repeat.
5. **Git / PR / commit etiquette** — commit + PR-title format, branch rules, "never `--no-verify`".
6. **Boundaries** — three tiers: **ALWAYS** do X · **ASK FIRST** before Y · **NEVER** do Z (the guardrails that
   stop destructive agent actions). The most-skipped, highest-leverage section.
*(Optional, only if non-obvious: project-structure, testing rules, compaction "always preserve" instructions.)*

## Length + authoring principles
- **Keep it short — Anthropic says <200 lines** for adherence; "performance degrades as context fills."
  **Pruning test:** for each line, "would removing this cause a mistake?" — if not, cut. A bloated file makes
  the agent IGNORE the rules that matter.
- **Commands > explanations · code snippets > prose · front-load** critical rules (lost-in-the-middle).
- **`IMPORTANT:`/`YOU MUST:`** sparingly (2–3×) on rules that get violated despite being present.
- **Commit it** (team artifact, compounds); personal overrides → `CLAUDE.local.md` (gitignored). Use `@`-imports
  to reference README/package.json rather than duplicating.

## Anti-patterns (several empirically confirmed)
- **Kitchen-sink** file (critical rules drowned). · **Repository-overview prose** — arXiv 2602.11988: repo
  overviews add **+20% inference cost with NO task-success gain**. · **Auto-generated** content (+20–23% cost,
  −0.5–2% perf; human-curated ≈ +4% success). · Duplicating README/package.json/inferrable conventions. ·
  **Missing exact commands** (the #1 omission). · **No boundaries** section. · Volatile facts (keys/URLs/versions)
  that age poorly. · Stray `AGENTS.override.md` silently suppressing the base.
- *Upside, empirical:* a good AGENTS.md cut agent **runtime −28.6% / tokens −16.6%** (arXiv 2601.20404).

## Sources
agents.md spec https://agentsmd.net/ · OpenAI Codex AGENTS.md https://developers.openai.com/codex/guides/agents-md ·
openai/codex AGENTS.md https://github.com/openai/codex/blob/main/AGENTS.md · Claude Code best practices
https://code.claude.com/docs/en/best-practices · CLAUDE.md placement/200-line https://code.claude.com/docs/en/claude-directory ·
GitHub 2,500-repo analysis https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/ ·
Augment Code AGENTS.md guide https://www.augmentcode.com/guides/how-to-build-agents-md · InfoQ AGENTS.md standard
https://www.infoq.com/news/2025/08/agents-md/ · arXiv 2602.11988 (repo-overviews not helpful) https://arxiv.org/abs/2602.11988 ·
arXiv 2601.20404 (efficiency impact) https://arxiv.org/abs/2601.20404 · adoption census: `census-data/census-doc-conventions/`.
