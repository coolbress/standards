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

## Claim table — `direction` 이 기대는 규칙 (2026-08-28 앵커 신설)

[`direction/05`](../../../direction/05-the-output-floor.md) 이 `AGENTS.md` 를 **어떻게 쓰는지**의 근거로 이 문서를
가리키면서 **이름으로만** 적었다 — claim table 이 없어 경로 인용이 `RESULT FAIL` 을 냈다(`GAPS` R5-29).
보급률은 [`planning-output-census`](planning-output-census.md) 가 답하고(`POC-001`), **여기는 내용**을 답한다.

| Claim ID | Class | Claim and scope | Evidence | Confidence | 재검증 |
|---|---|---|---|---|---|
| CAS-001 | normative | **하나만 정본이고 나머지는 거울이다.** 독립된 두 파일은 갈린다 — 심볼릭 링크(드리프트 0)거나 유지되는 축약본이거나 둘 중 하나이고, **둘 다 맨 위에 어느 쪽이 정본인지 적는다.** 우리 저장소들은 `AGENTS.md` 를 정본으로, `CLAUDE.md` 를 **링크**로 둔다 | `AGENTSMD-SPEC` · `CLAUDE-CODE-BEST-PRACTICES-DOC` | high | 2027-02-28 |
| CAS-002 | empirical | 🔴 **저장소 개요 산문은 넣지 마라 — 값을 치르고 아무것도 안 산다.** ETH Zürich 가 여러 LLM·에이전트에 걸쳐 재니 컨텍스트 파일이 **과제 성공률을 일반적으로 올리지 않으면서 추론 비용을 평균 20% 넘게** 올렸고, *"repository overviews, although popular and **recommended by model providers**, are not helpful"* 로 못박았다. **다만 지시(instructions)는 따라진다** — 그래서 이 문서의 §절 골격이 명령형인 것이다 | `AGENTS-CONTEXT-EVAL-2026` | medium-high | 2027-02-28 |
| CAS-003 | empirical | **좋은 파일은 효율을 올린다 — 성공률이 아니라.** 중앙값 **런타임 −28.64% · 출력 토큰 −16.58%**, 과제 완수는 비슷했다. 🔶 **표본이 작다: 저장소 10개 · PR 124건.** `CAS-002` 와 **모순이 아니다** — 저 쪽은 *개요를 넣으면* 손해라 하고 이 쪽은 *지시가 있으면* 싸진다 한다. 갈림길은 **무엇이 적혀 있는가**이지 파일의 유무가 아니다(`C50-14` *presence ≠ adequacy*) | `AGENTS-EFFICIENCY-2026` | medium | 2027-02-28 |
| CAS-004 | vendor-behavior | **짧게 써라 — 벤더 권고는 200줄 미만이고 이유는 준수율이다**(*"performance degrades as context fills"*). 가지치기 시험: 한 줄씩 *"이걸 지우면 실수가 나나"* 를 묻고 아니면 자른다. ⚠️ **권고이지 측정이 아니다** — 200 이라는 수의 근거는 벤더가 제시하지 않는다. 측정 쪽은 `CAS-002` 다 | `CLAUDE-CODE-BEST-PRACTICES-DOC` | medium | 2027-02-28 |
| CAS-005 | normative | **가장 많이 빠지는 두 절이 가장 값어치가 크다** — ① 플래그까지 붙은 **정확한 명령**(에이전트는 비표준 스크립트 이름을 추측할 수 없다) ② **경계** 3단(ALWAYS · ASK FIRST · NEVER). GitHub 이 약 2,500 저장소를 훑어 정리한 지침과 같은 방향이다. ⚠️ 벤더가 **자기 사용자**를 분석한 것이라 독립 재현이 안 된다 | `GITHUB-AGENTS-2500-REPOS` · `AGENTSMD-SPEC` | medium | 2027-02-28 |
| CAS-006 | local-census | **양쪽 형식이 야생에 다 있다** — 공개 GitHub 에 `AGENTS.md` **129,696** · `CLAUDE.md` **40,200** 개. 🔴 **이건 파일 수이지 저장소 비율이 아니다** — 비율은 `POC-001`(34.8% / 28.8%)이 답한다. 두 수를 같은 문장에 섞어 쓰지 마라 | `DOC-CONVENTIONS-CENSUS-2026` | medium | 2026-12-28 |

## Sources
agents.md spec https://agentsmd.net/ · OpenAI Codex AGENTS.md https://developers.openai.com/codex/guides/agents-md ·
openai/codex AGENTS.md https://github.com/openai/codex/blob/main/AGENTS.md · Claude Code best practices
https://code.claude.com/docs/en/best-practices · CLAUDE.md placement/200-line https://code.claude.com/docs/en/claude-directory ·
GitHub 2,500-repo analysis https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/ ·
Augment Code AGENTS.md guide https://www.augmentcode.com/guides/how-to-build-agents-md · InfoQ AGENTS.md standard
https://www.infoq.com/news/2025/08/agents-md/ · arXiv 2602.11988 (repo-overviews not helpful) https://arxiv.org/abs/2602.11988 ·
arXiv 2601.20404 (efficiency impact) https://arxiv.org/abs/2601.20404 · adoption census: `census-data/census-doc-conventions/`.
