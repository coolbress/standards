<div align="center">

# ⎈ claudeck

### Your command deck for vibe-coding with Claude Code.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE) &nbsp;
![for Claude Code](https://img.shields.io/badge/for-Claude%20Code-d97757) &nbsp;
![bash + python3](https://img.shields.io/badge/bash%20%2B%20python3-555)

<br>

![claudeck in action](docs/demo.gif)

*One plain-language ask becomes a classified, gated, test-driven, dual-model-reviewed change, held at the PR for your call.*

</div>

> **Speak → Align → Persist → Verify → Protect → Extend**

- **Speak** — one ask, full pipeline. Say it in plain language; the harness sizes the work and runs the
  right plan → TDD → review → ship flow on its own — pausing only for the decisions that are yours.
- **Align** — asks before it assumes. Vague or high-stakes work triggers a spec interview, and it
  respects your project's existing boundaries before writing a line.
- **Persist** — never loses the thread. Survives `/compact`, restarts, and parallel work via state
  snapshots, durable plans, persistent memory, and isolated worktrees — no lost work.
- **Verify** — reviewed in depth. Every change is checked by a top-tier model *and* an external one
  (Codex); an optional `/audit` pass hardens critical code to a LOCKed bar.
- **Protect** — guardrails on by default. Blocks dangerous commands, secret leaks, and prompt-injection
  — and tests itself on every change, so you know it isn't broken.
- **Extend** — grows with you. Add your own skills, bootstrap onto a new machine or repo, and see every
  component at a glance.

`Inside: 34 skills · 8 specialized agents · 24 safety & lifecycle hooks · 17 scripts · 2 MCP servers — all self-tested.`

---

## What is it?

**Vibe coding with agents is fast** — you describe, the model builds, subagents fan out. Raw, it's also
easy to ship a mess. **claudeck is the harness that makes it shippable**: one git repo you clone _to_
`~/.claude` that turns a plain-language ask into a full, gated pipeline — *plan → TDD → multi-model
review → ship* — wrapping every session in just-enough process, always-on guardrails, and multi-agent
orchestration.

**It is _not_** a public framework, a plugin marketplace, or a multi-tenant product — it's a personal /
small-team (≤5) harness, versioned by `git log`, with no CI or release pipeline by design.

## Features at a glance

| Area | What you get |
|---|---|
| **Routing & gates** | every request graded Tier 0–3 → *just-enough* process; three gates keep you in the loop on anything outward-facing |
| **Workflow pipeline** | `spec → plan → TDD → verify → review → PR → cleanup`, fired as skills only when the tier needs them |
| **Subagent orchestration** | the lead plans & reviews; isolated-worktree agents write + commit; parallelism capped by RAM so a fan-out can't OOM you |
| **Spec & constraints** | vague or high-stakes work runs a **spec interview** first; `respecting-constraints` checks architecture boundaries + patterns *before the first line is written* |
| **Memory & sessions** | file-based memory + `learn`/`remember`; session hooks inject routing, git context, and compaction snapshots |
| **Code intelligence** | a local GitNexus blast-radius graph + live library docs (context7), fed to otherwise graph-blind agents |
| **Vendor-diverse review** | the pre-PR gate built into every Tier 2/3 run — **best (Fable 5/Opus)** proposes ▸ **Codex** adjudicates (Sonnet fallback) |
| **Convergent `/audit`** | *separate, on demand:* drives already-finished code to a **LOCKed** bar over unbounded **best (Fable 5/Opus)**+**Codex** rounds |
| **Always-on guardrails** | block a destructive command, a leaking secret, or an OOM *before* the tool runs, and flag a web-page prompt-injection *after* a fetch (+ gitleaks & health git gates) |
| **Health & SSOT** | `harness-doctor` gates every push · `harness-meta` is the single source for counts/models · `/dashboard` renders it live |
| **Self-versioning** | the repo *is* the harness — `git log` is the changelog, freshness auto-derived from `HEAD` |
| **Extensibility & portability** | add your own skills (`writing-skills`), bootstrap onto a new machine or repo (`harness-init`), and see every component live (`/dashboard`) |

→ Run **`/dashboard`** for the full, live component map — every command, agent, hook, and skill.

## Why it exists

Each row is concrete value to **you** — the pain you'd hit without a harness, and what claudeck does instead:

| Without a harness | What you get with claudeck |
|---|---|
| You hand-hold the agent through plan, tests, review, and PR | **one ask runs the whole pipeline** — claudeck right-sizes the work and drives plan → TDD → review → PR itself, pausing only for the calls that are yours |
| A vague ask sends the agent off building the wrong thing | **it asks before it assumes** — vague or high-stakes work triggers a spec interview, and respects your project's existing patterns before writing a line |
| A `/compact`, a crash, or a parallel task loses your place | **you never lose the thread** — state snapshots, durable plans, persistent memory, and isolated worktrees let you resume exactly where you were |
| A big change lands on one model's blind spot | **every change gets a two-vendor review** — best (Fable 5/Opus) proposes, Codex adjudicates |
| `rm -rf`, a leaked secret, or an OOM fan-out fires before you blink | **guardrails stop it first** — destructive commands, secrets, and memory-blowing spawns are blocked *before* they run (a RAM-weighted semaphore keeps a fan-out from crashing your box) |
| Your setup drifts between machines & teammates | **the same, always-current workflow everywhere** — `~/.claude` is a git repo; one `git pull` updates it |

<div align="center">

![a guardrail catching a footgun](docs/demo-guard.gif)

*A footgun stopped before it runs — `rm -rf` waits for your explicit override.*

</div>

## Quickstart

**Prerequisites** — Claude Code, plus `node` + `gitleaks`. `bootstrap.sh` installs the rest
(`gh`·`jq`·`shellcheck`·`gitnexus`·`codex`) and prints a flutter-doctor-style status of what's missing.

**1 — Install.** claudeck *is* your `~/.claude`, so the path depends on whether you already have one.

*Fresh* — never ran Claude Code (no `~/.claude` yet):
```bash
git clone https://github.com/coolbress/claudeck.git ~/.claude
```

*Adopt an existing `~/.claude` in place* — nothing personal is lost: your sessions, login,
`~/.claude.json`, caches, and plugins are all gitignored; only `settings.json` + `CLAUDE.md` are
replaced, so back those two up first:
```bash
cd ~/.claude
mkdir -p ~/.claude.pre-harness && cp -p settings.json CLAUDE.md ~/.claude.pre-harness/ 2>/dev/null || true
git init -q && git remote add origin https://github.com/coolbress/claudeck.git
git fetch -q origin && git checkout -f -b main --track origin/main
```
> Re-enable any plugins you had from the backed-up `settings.json` (`enabledPlugins`) — the plugin
> files themselves never moved.

**2 — Wire + verify.**
```bash
~/.claude/bootstrap.sh                          # git gates · exec bits · deps
python3 ~/.claude/scripts/harness-doctor.py     # expect: HARNESS HEALTHY   (or /harness-doctor in-session)
```

**3 — Open a project.** Per-project onboarding happens **in-session**: the first time you open a repo,
claudeck proposes a build/test command + the docs to track; you confirm or edit, and it writes
`<repo>/.claude/harness.conf`. Re-run `/harness-init` anytime. Full walkthrough →
[`docs/getting-started.md`](docs/getting-started.md).

> [!IMPORTANT]
> The repo must live **at** `~/.claude` itself — don't clone it elsewhere and symlink, and don't
> hand-edit a running `~/.claude` out of band. It's the source of truth: edit it here and commit.

## What's inside

```
~/.claude/                  ← this repo, cloned into place
├── CLAUDE.md               global instructions Claude Code reads natively every session
├── settings.json           the ONLY place hooks/permissions/models are wired
├── VERSION                 coarse semver marker (freshness auto-derived from git HEAD)
├── bootstrap.sh            per-machine installer (git gates · exec bits · deps)
├── agents/                 subagent roles: code-reviewer (best: Fable 5/Opus) · cross-checker (Codex) · implementer · …
├── skills/                 behavior layer — routing · the pipeline (spec/tdd/pr/cleanup…) · /audit · /dashboard
├── hooks/                  entry hooks (session-start · prompt-context)
│   ├── scripts/            the guardrail/gate handlers (each with a co-located *.test.sh)
│   └── gitnexus/           code-graph enrichment hook
├── scripts/                deterministic tooling — harness-doctor · harness-meta · selfwire · init · review-render · …
├── githooks/ · templates/ · bootstrap-assets/   scaffolding the installer uses
├── eval/                   routing-bench — tier-classification accuracy fixtures
└── docs/                   the handbook (you are at its front door)
```

## How it works

Every message is silently graded into a **Tier**, and only as much process as that tier needs runs:

```
Tier 0   docs / chat / "explain X"      → answered directly. No pipeline, no gate.
Tier 1   one-line code edit             → Edit → Commit+PR → Cleanup
Tier 2   bug fix / small refactor       → Issue → Plan → TDD → Verify → review-round → PR → Cleanup
Tier 3   new feature / multi-layer      → Spec → Issue → Plan → TDD → Verify → review-round → PR → Cleanup
```

(Korean verbs count too: 설명=0 · 고쳐=2 · 만들어=3.) Isolation (branch/worktree) is *not* a pipeline
step — it's a tier-agnostic precondition (**Rule 5a**, the Locate ladder) run before the first code edit:
silent when you're already in the right worktree, STOP/ask only when it must create or relocate. Around it all: `SessionStart` injects routing +
memory, `UserPromptSubmit` adds git context, and every tool call passes the always-on Pre/PostToolUse
guardrails (guards · gates · code-graph · semaphore). The full model + the *why* →
[`docs/architecture.md`](docs/architecture.md).

## Key concepts

<details>
<summary><b>Hooks vs skills — enforce vs guide</b></summary>

<br>

A **hook** is deterministic and fires on a tool/lifecycle event; it can block with a non-zero exit. Hooks
are the guardrails that must *always* run, wired in `settings.json`. A **skill** is prompt-based behavior
Claude invokes by relevance or `/name`; skills are the *workflow*. **Hooks enforce; skills guide.**
</details>

<details>
<summary><b>The three gates — control without nagging</b></summary>

<br>

The harness is global, but not every project uses GitHub / branches / PRs — so gating is graduated:

- **Gate 1** (once, after a Tier 1/2/3 request): it proposes the pipeline as a checklist; you confirm or
  trim steps that don't apply (no remote → drop Issue/PR). It won't silently re-add a dropped step.
- **Gate 2** (auto): cheap, local, reversible steps run hands-free — plan · TDD · verify · spec.
- **Gate 3** (re-confirm): it stops before anything **outward-facing** (issue/branch/commit/push/PR) or
  **resource-intensive** (the review-round, an ad-hoc Opus dispatch) — `▶ <step> 진행할까요? (yes/skip/stop)`.
</details>

<details>
<summary><b>OOM guard — how parallel agents are throttled</b></summary>

<br>

Two fail-open `PreToolUse` hooks keep a parallel spawn from crashing a small host:

- `memory-gate.sh` — blocks Agent / heavy-bash at macOS memory-pressure level 4.
- `agent-semaphore.sh` — an atomic `mkdir` lock with a RAM-derived **weighted budget** (`Σweight ≤ RAM−reserve`; light agents 1 GB / heavy 4 GB) → 8 GB: BUDGET 3 (1 heavy or 3 light at once) · 16 GB: 11 · 32 GB+: cap_max-bound; live memory-pressure throttles it down.

Both **fail open** by construction — if the guard itself errors, your work is never blocked. Knobs:
`HARNESS_AGENT_CAP` · `HARNESS_SEMAPHORE_DISABLE` · `HARNESS_MEM_GATE_DISABLE`.
</details>

<details>
<summary><b>Engine ⊥ personal state — what a clone carries (and what it doesn't)</b></summary>

<br>

`.gitignore` is **fail-closed**: it ignores everything (`/*`), then re-includes only the engine (a short
allowlist of dirs + top-level files). Any new ephemeral/secret dir Claude Code adds is excluded **by
default** — so a clone carries the shared tooling only, never your memory, sessions, caches, or secrets.
Add a new top-level engine file? You must allowlist it, or git won't see it.
</details>

## Documentation

[`docs/index.md`](docs/index.md) is the hub — organized by the same six dimensions as the pitch above,
so you can navigate by *what you want*, not by filename. The highlights:

| | Doc |
|---|---|
| **Start** — install · run · how it's built | [`getting-started.md`](docs/getting-started.md) · [`install.md`](docs/install.md) · [`architecture.md`](docs/architecture.md) |
| **Speak** — the feature pipeline | [`workflows/tier3-feature.md`](docs/workflows/tier3-feature.md) · [`parallel-dispatch.md`](docs/workflows/parallel-dispatch.md) · [`gitnexus.md`](docs/workflows/gitnexus.md) |
| **Align** — asks before it assumes | [`spec-and-constraints.md`](docs/spec-and-constraints.md) |
| **Persist** — never loses the thread | [`memory-and-sessions.md`](docs/memory-and-sessions.md) |
| **Verify** — reviewed in depth | [`workflows/review-round.md`](docs/workflows/review-round.md) · [`audit.md`](docs/workflows/audit.md) |
| **Protect** — guardrails on by default | [`safety-model.md`](docs/safety-model.md) · [`concurrency-model.md`](docs/concurrency-model.md) |
| **Extend** — grows with you | [`extending.md`](docs/extending.md) · [`distribution-model.md`](docs/distribution-model.md) |
| **Reference** — internals · deps · live map | [`harness-notes.md`](docs/harness-notes.md) · [`dependencies.md`](docs/dependencies.md) · run `/dashboard` · `/harness-doctor` |

## Updating

```bash
cd ~/.claude && git pull            # the repo IS the harness, so pull = update
~/.claude/bootstrap.sh              # re-run only if deps/gates changed (idempotent)
python3 ~/.claude/scripts/harness-doctor.py
```

There is no `CHANGELOG.md` or release CI by design — `git log` (Conventional Commits) is the
authoritative change history for this clone-HEAD repo. `VERSION` is a coarse, hand-set semver bumped at
milestones; the "how current is this" signal (`head_sha` / `head_date`) is auto-derived from git HEAD, so
the displayed version never goes stale.

## Contributing

One contributor + a few trusted teammates, so the house rules are short:

1. **Edit the tracked files, then commit** — never hand-edit a running `~/.claude` out of band.
2. **Keep `harness-doctor.py` green** — it gates every push (pre-commit gitleaks + pre-push health).
3. **Don't hand-count** — counts/models/version come from `harness-meta.py`. The one sanctioned hand-count
   is the README `Inside:` line, which the doctor drift-checks against source; any other hardcoded count is
   a drift bug the doctor catches.
4. **Record durable decisions** in [`docs/harness-notes.md`](docs/harness-notes.md), not in commit
   messages alone.

See [`docs/architecture.md`](docs/architecture.md) for boundaries and [`docs/index.md`](docs/index.md)
for the full handbook.

## License

[MIT](LICENSE) © 2026 coolbress
