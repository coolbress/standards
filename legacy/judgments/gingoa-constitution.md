> ## ⚠️ 이관 (2026-08-24) — gingoa의 헌법
>
> 원본 `gingoa/CLAUDE.md` (세션 시작 시 읽히던 상시 계약 · Codex용 `AGENTS.md`는 그 사본).
> **폐기된 하네스의 판단**이며 현행 방향은 [`direction/`](../../direction/)이다.
>
> **왜 남기나**: 이 54줄이 gingoa가 *에이전트에게 무엇을 시키려 했는가*의 전문이다.
> [`LINEAGE.md`](../LINEAGE.md)가 서술하는 "상시 계약" 방식의 **실물**이고,
> `direction/04`가 *"CLAUDE.md는 20줄이면 된다"* 고 정한 것의 **비교 대상**이다.

---

# Gingoa — Constitution (Claude Code)

> Read by **Claude Code** at session start. Codex reads `AGENTS.md` (a mirror of this file — keep them in
> sync). **English only** in this repo.

## North star
A non-engineer + AI agent → **production-grade** software a senior engineer calls "well built." The harness
fills the craft · operability · sound-process gap the non-engineer doesn't know to ask for. Scored by the
**minimum** dimension (no weak link), not the average.

## Build & verify
- `pnpm lint` (Biome) · `pnpm typecheck` (tsc) · `pnpm test` (Vitest) · `pnpm build` (tsc).
- Single test while iterating: `pnpm vitest run tests/<file>.test.ts` (or `pnpm vitest run -t "<name>"`).
- CI gates all four on every push / PR.

## Code style
- **TypeScript, ESM** (`"type": "module"`; `import`/`export`; use `.js` extensions in relative imports).
- Strict TS incl. `noUncheckedIndexedAccess` — guard indexed access (`?? …` or an explicit `=== undefined`).
- Lint + format = **Biome** (LF · 2-space · width 100); run it, don't hand-format.
- Typed, composable modules; tests in `tests/` (Vitest) are **hermetic** — temp homes, never real ones.

## Architecture
A cross-host (Claude Code + Codex) harness: a **host-neutral core** (`src/core/`) projected onto each host by
thin **adapters** (`src/adapters/{cc,codex}.ts`), composed by an install **CLI** (`src/cli/`). Dependencies
flow one way — `cli → adapters → core`; the **core MUST NOT import an adapter** (a CI fitness-function
enforces it). Design docs land in `docs/` as the components are built.

## Build to the spec
Implement against the **feature's spec** — its per-feature `docs/specs/<slug>/spec.md` (written when a feature's
implementation starts), which derives from the **project requirements** (the user story in `docs/prd.yml` /
`docs/PRD.md`) and the story's governing `docs/adr/` decisions. The **EARS acceptance criteria are the tests** to
satisfy. Read them before implementing and build to them; if the spec or the PRD is wrong or missing, **fix it
first** — never drift silently.

## Commits & PRs
- **Conventional Commits**; reference the issue; never `--no-verify`.
- **PR title** = Conventional Commits (it becomes the squash-merge commit; enforced by the `pr-title`
  workflow). **Issue title** = a plain one-line summary.
- **The landed squash commit** (`gh pr merge --squash`): the **subject keeps the `(#N)` PR tag** (GitHub's
  default — a hand-set `--subject` must not strip it), the **body carries no `Closes`/`Refs` tag** (issue
  linkage rides the PR description's `Closes #N`), and the **body ends with the `Co-Authored-By` trailer**.
  Prefer the platform default; if you set `--subject`/`--body`, verify the merged commit.
- **The squash body is a concise summary, not a WIP-commit dump.** The repo squash config builds the body from
  the branch's commit messages, so land each change as **one squash-ready commit** — a `type(scope): …` subject
  plus a short what/why body ending in the `Co-Authored-By` trailer. A many-commit branch concatenates into a
  verbose body; the detailed step history belongs in the PR description and design docs, not the commit body.
  (A genuinely multi-commit change: curate the squash `--body` to a summary at merge, preserving the rules above.)

## Boundaries
- **NEVER** read or write a live `~/.claude` / `~/.codex` — install + tests use `GINGOA_CLAUDE_HOME` /
  `GINGOA_CODEX_HOME` overrides; touch a real home only via explicit, backed-up, surgical edits.
- **NEVER** commit a secret, bypass CI, or push directly to `main`.
- **ASK FIRST** before any outward or hard-to-reverse action (create/push a branch, open/merge a PR, delete).
- **ALWAYS** run lint + typecheck after changing code, and keep every shipped guardrail itself tested.
