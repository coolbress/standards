---
id: aspect-27-ai-harness-archetype--plugin-marketplace-memory-standard
title: "Plugin · Marketplace · Memory build standard (the packaging + memory layer — the frontier-AI standard)"
parent: aspect-27-ai-harness-archetype
kind: reference
evidence_track: census+lit
status: review-needed
last_updated: "2026-06-27"
sources:
  - "https://code.claude.com/docs/en/plugins"
  - "https://code.claude.com/docs/en/plugins-reference"
  - "https://code.claude.com/docs/en/plugin-marketplaces"
  - "https://code.claude.com/docs/en/discover-plugins"
  - "https://code.claude.com/docs/en/memory"
  - "https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool"
  - "https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents"
  - "https://claude.com/blog/context-management"
  - "https://developers.openai.com/codex/memories"
  - "https://developers.openai.com/codex/guides/agents-md"
  - "https://developers.openai.com/api/docs/guides/conversation-state"
  - "https://openai.github.io/openai-agents-python/sessions/"
method: "lit — read the Claude Code plugins / plugins-reference / plugin-marketplaces / discover-plugins / memory docs IN FULL, the Anthropic API memory-tool page, the 'effective context engineering for AI agents' engineering post, and the 'context management' (memory tool + context editing) announcement; plus the OpenAI Codex memories + AGENTS.md docs, the Responses-API conversation-state guide, and the Agents-SDK sessions page (cross-vendor convergence check). census — harvested verbatim plugin.json / marketplace.json schemas, the `claude plugin` + `claude plugin marketplace` CLI tables, the memory-tool command set, and the gingoa-shipped manifests (`.claude-plugin/marketplace.json`, `adapters/gingoa/.{claude,codex}-plugin/plugin.json`). Raw shapes + verbatim quotes deposited at census-data/frontier-ai-components/plugins-marketplace-memory/."
---

> **Standard (claim):** The packaging + memory layer is **three artifacts with three jobs**. (1) A **plugin** is
> the **distribution unit** for the whole capability layer — a self-contained directory whose only required
> manifest field is `name` (`.claude-plugin/plugin.json`), bundling skills · agents · hooks · MCP/LSP servers ·
> monitors that **auto-discover** from fixed root folders (`skills/`, `agents/`, `hooks/hooks.json`, `.mcp.json`)
> — `${CLAUDE_PLUGIN_ROOT}`-relative, namespaced, versioned by explicit `version` or git SHA. (2) A
> **marketplace** is a **git-hosted catalog** (`.claude-plugin/marketplace.json`: required `name`/`owner`/
> `plugins[]`; each plugin = `name` + a `source` discriminator — relative-path · `github` · `url` · `git-subdir`
> · `npm`) that users `add` then `install` from; there is **no central registry** — trust is per-source, curation
> is "open marketplace + review gate". (3) **Memory = explicit files, not chat state**: a static instruction
> hierarchy (`CLAUDE.md`/`AGENTS.md` + `@`-imports ≤4 hops + `.claude/rules/`) carries durable rules, a
> generated layer (Claude Code **auto-memory** `MEMORY.md`-indexed dir / the API **memory tool**'s `/memories` /
> Codex **Memories** `~/.codex/memories/`) accumulates learnings, and **context engineering** (finite context →
> smallest high-signal set · progressive disclosure · compaction · context-editing · structured note-taking)
> governs the window. Plugins/marketplaces "can execute arbitrary code … with your user privileges"; memory is
> poisonable — both are **untrusted-by-default**. OpenAI converges on every axis (Codex AGENTS.md+Memories,
> Responses/Conversations state, Agents-SDK Sessions).
> **Evidence:** lit (Claude Code docs + Anthropic memory-tool/context-engineering + OpenAI Codex/Responses/
> Agents-SDK) · census (plugin.json + marketplace.json schemas, CLI tables, gingoa's shipped manifests) ·
> **Confidence:** high

This sub-doc is the concrete build spec behind aspect-27's "skill / hook packaging + marketplace" and "context /
memory management" bullets — the **packaging** half (how the capability layer is bundled + distributed) and the
**memory** half (how durable state lives across the fresh-context-per-session boundary). The *capability* units
themselves are [`skill-authoring-standard.md`](skill-authoring-standard.md),
[`mcp-server-standard.md`](mcp-server-standard.md), and
[`hooks-commands-subagents-standard.md`](hooks-commands-subagents-standard.md); the cross-host config wiring is
[`host-config-schemas.md`](host-config-schemas.md). gingoa **scaffolds and distributes** plugins + a marketplace,
and scaffolds memory files for user projects, so this is the standard those features must emit to. Facts are
pinned to the Claude Code docs + Anthropic/OpenAI material current at capture (2026-06-27).

## Why this is one layer (and where it sits)

The five capability components (skill · hook · command · subagent · MCP server) are *what the harness can do*.
This layer is *how that gets packaged, shipped, and remembered*:

| Artifact | Job | Trigger to build it | Standard |
|---|---|---|---|
| **Plugin** (`plugin.json`) | bundle the capability layer into one installable, shareable, versioned unit | you want to share components across projects/teams | §1 |
| **Marketplace** (`marketplace.json`) | a catalog that lists plugins + where to fetch each | you want others to discover + install your plugin(s) | §2 |
| **Memory** (CLAUDE.md/AGENTS.md · memory tool · auto-memory · context engineering) | carry durable state across the per-session fresh-context boundary | the agent must remember rules/learnings beyond one window | §3–§4 |

The load-bearing relationship: a **plugin is the unit of *distribution*** (the constitution+skill+hook+MCP bundle
becomes one `@plugin:thing`), a **marketplace is the unit of *discovery*** (an app-store of plugins), and
**memory is the unit of *persistence*** (because "Each Claude Code session begins with a fresh context window"
[lit, memory], durable knowledge MUST live in explicit files, not the chat transcript). Get the boundary wrong
and you ship a skill that should have been a plugin, a one-off path where a marketplace belonged, or a rule pasted
into chat that evaporates at the next session.

---

# Part A — Plugins (the distribution unit)

## 1. plugin.json — the manifest contract

A **plugin** is "a self-contained directory of components that extends Claude Code with custom functionality.
Plugin components include skills, agents, hooks, MCP servers, LSP servers, and monitors" [lit, plugins-reference].
It is the packaging boundary for the *entire* capability layer — install one plugin, get its skills + agents +
hooks + MCP servers at once.

**The manifest is optional, and `name` is the only required field** [lit, verbatim]: "If you include a manifest,
`name` is the only required field." If omitted entirely, Claude Code auto-discovers components from default
folders and derives the name from the directory. So the *minimal* plugin is a directory of folders; the manifest
adds metadata + custom paths. The full schema [lit, plugins-reference]:

| Field | Required | Shape / note |
|---|---|---|
| `name` | **Yes** | unique id, **kebab-case, no spaces**; the **namespace** (`/<plugin>:<skill>`, `<plugin>:<agent>`) |
| `version` | No | semver; **pins the cache** — bump it or users don't get updates. Omit → git commit SHA = version (every commit = new version) |
| `description` | No | shown in `/plugin` |
| `author` | No | **object** `{name, email?, url?}` (not a string) |
| `displayName`/`homepage`/`repository`/`license`/`keywords` | No | metadata; `license` = SPDX id |
| `skills`/`commands`/`agents`/`hooks`/`mcpServers`/`lspServers`/`outputStyles` | No | custom component paths (string\|array\|object), all relative + `./`-prefixed |
| `experimental.{themes,monitors}` · `userConfig` · `channels` · `dependencies` | No | newer/experimental surfaces |

Two rules matter for a *portable* artifact: `author` is an **object** (gingoa ships `{ "name": "coolbress" }`,
correct), and **unrecognized top-level fields are ignored** — "You can keep metadata from another ecosystem in
`plugin.json` and the plugin still loads" (one manifest can double as a `package.json`/VS-Code/DXT manifest)
[lit]. `claude plugin validate` flags unknowns as **warnings**; `--strict` promotes them to errors (use in CI). A
wrong *type* (e.g. `keywords` as a string) is a hard **load error**.

## 2. The `.claude-plugin/` layout + auto-discovery (the #1 footgun)

**Only `plugin.json` goes in `.claude-plugin/`; every component folder is at the plugin root.** This is the most
repeated warning in the docs [lit, verbatim]:

> "Don't put `commands/`, `agents/`, `skills/`, or `hooks/` inside the `.claude-plugin/` directory. Only
> `plugin.json` goes inside `.claude-plugin/`. All other directories must be at the plugin root level."

When a component path is **omitted** from the manifest, it **auto-discovers** from a fixed default location
[lit, file-locations reference]:

```
my-plugin/
├── .claude-plugin/plugin.json   # the ONLY thing in .claude-plugin/
├── skills/<name>/SKILL.md       # skills (auto-discovered, namespaced /<plugin>:<name>)
├── agents/<name>.md             # subagents
├── commands/<name>.md           # flat-file commands (legacy form; "Use skills/ for new plugins")
├── hooks/hooks.json             # hooks (same shape as settings.json `hooks`)
├── .mcp.json                    # MCP servers ({"mcpServers": {...}})
├── .lsp.json                    # LSP servers
├── monitors/monitors.json       # background monitors
├── bin/                         # executables added to the Bash PATH while enabled
└── settings.json                # default settings (only `agent` + `subagentStatusLine` keys honored)
```

Path-behavior rule: `commands`/`agents`/`outputStyles`/`themes`/`monitors` manifest keys **replace** the default
dir; **`skills` *adds to* the default `skills/` scan**. A `SKILL.md` at the plugin *root* (no `skills/`, no
`skills` field) loads as a single-skill plugin (CC v2.1.142+) — but gingoa uses the `skills/<name>/SKILL.md`
layout (good: stable name, room to grow). **`CLAUDE.md` at a plugin root is NOT loaded as project context** —
"Plugins contribute context through skills, agents, and hooks rather than CLAUDE.md" [lit]; ship instructions as a
skill, not a bundled constitution.

**`${CLAUDE_PLUGIN_ROOT}`** resolves to the install dir and is the *only* reliable way for a bundled hook/MCP
command to reference its own scripts (the plugin is **copied** to `~/.claude/plugins/cache`, and **paths can't
traverse outside the plugin root** — `../shared-utils` won't resolve after install) [lit]. Note it **changes on
update** ("do not write state here") — durable state goes in `${CLAUDE_PLUGIN_DATA}`.

## 3. Install / enable / version (config, not code)

A plugin is registered in `settings.json`, scoped like every other config [lit]: `enabledPlugins:
{"<plugin>@<marketplace>": true}` across **user** (`~/.claude/settings.json`, default) · **project**
(`.claude/settings.json`, team-shared) · **local** (`.claude/settings.local.json`, gitignored) · **managed**
(read-only). The CLI surface (verbatim subcommands): `claude plugin {install, uninstall, enable, disable, update,
list, details, validate, tag, init}` and `claude plugin marketplace {add, list, remove, update}`; interactive
`/plugin` (Discover/Installed/Marketplaces/Errors tabs); dev-test with `claude --plugin-dir ./x` (no install) +
`/reload-plugins`. `claude plugin details` even prints a **projected token cost** (always-on vs on-invoke) — a
reminder that every bundled component's listing text is a *recurring* context cost (the same budget discipline as
skills/MCP). **Version resolution order:** `plugin.json` version → marketplace-entry version → git SHA →
`unknown`; explicit `version` *pins the cache* (bump on every release or users never update) — omit it for
fast-iterating internal plugins so each commit ships.

## 4. What belongs in a plugin vs standalone (the boundary)

The docs draw the line explicitly [lit, plugins]: **standalone `.claude/`** for "personal workflows,
project-specific customizations, quick experiments" (short names `/hello`); **plugin** when you "want to share
functionality with your team or community … the same skills/agents across multiple projects … version control and
easy updates … distributing through a marketplace" (namespaced `/<plugin>:hello`). So: a component you keep
re-copying between projects → promote to a plugin; a one-project tweak → leave it standalone. Inside a plugin,
the *capability units* still follow their own standards (skills §`skill-authoring-standard`, MCP
§`mcp-server-standard`, hooks/agents §`hooks-commands-subagents-standard`) — the plugin only *packages* them.

---

# Part B — Marketplaces (the distribution catalog)

## 5. marketplace.json — the catalog contract

A marketplace is "a catalog that lets you distribute plugins to others" with "centralized discovery, version
tracking, automatic updates" — in practice **just a git repo with `.claude-plugin/marketplace.json` at its root**
[lit, plugin-marketplaces]. There is **no central package registry**; a marketplace is added by URL/repo/path.
Schema:

| Field | Required | Shape |
|---|---|---|
| `name` | **Yes** | kebab-case marketplace id; **public-facing** (`/plugin install x@<name>`); one marketplace per name per user |
| `owner` | **Yes** | object `{ name (req), email? }` |
| `plugins` | **Yes** | array of plugin entries |
| `metadata`/`description`/`version`/`$schema`/`metadata.pluginRoot`/`allowCrossMarketplaceDependenciesOn` | No | catalog metadata (`pluginRoot` prefixes relative sources) |

Each **plugin entry** requires `name` + `source`, and may carry any plugin.json field plus marketplace-only
`category`/`tags`/`strict`/`relevance`/`defaultEnabled`. The **`source` discriminator** is the heart of the
catalog [lit, verbatim table]:

| `source` | Shape | Use |
|---|---|---|
| relative path | `"./plugins/x"` (string, `./`-prefixed, no `../`) | plugin lives in the *same* repo as the marketplace |
| `github` | `{ "source":"github", "repo":"owner/repo", "ref"?, "sha"? }` | plugin in a separate GitHub repo |
| `url` | `{ "source":"url", "url":"https://github.com/git/git.git", "ref"?, "sha"? }` | any git host (GitLab/Bitbucket/self-hosted) |
| `git-subdir` | `{ "source":"git-subdir", "url", "path", "ref"?, "sha"? }` | plugin in a monorepo subdir (sparse clone) |
| `npm` | `{ "source":"npm", "package":"@org/x", "version"?, "registry"? }` | plugin published to npm |

`sha` pins an exact commit (when both `ref`+`sha` set, `sha` wins). **Relative paths only work when the user adds
the marketplace as a *git/local source* (the whole repo is cloned); a bare URL to `marketplace.json` downloads
only that file** → use `github`/`npm`/`url` sources for URL-distributed marketplaces [lit]. **`strict`** (default
`true`) = `plugin.json` is the component authority; `strict:false` = the marketplace entry *is* the whole
definition (the plugin needs no `plugin.json`) — for a curating operator who restructures a plugin's components.

This matches gingoa's shipped `.claude-plugin/marketplace.json` exactly: `name:"gingoa"`,
`owner:{name:"coolbress"}`, `metadata.description`, one plugin `{ name:"gingoa", source:"./adapters/gingoa",
description }` — required keys present, `owner` as an object, a `./`-relative same-repo source.

## 6. Publish · host · curate · trust

**Host = push a git repo** (GitHub recommended; any git host works; private repos via git credential helpers +
`GITHUB_TOKEN`/`GITLAB_TOKEN` for background auto-update) [lit]. **Add** = `claude plugin marketplace add
<owner/repo | git-url | url-to-marketplace.json | local-path>` (pin via `@ref` on the GH shorthand / `#ref` on a
git URL); **install** = `claude plugin install <plugin>@<marketplace>`. A team auto-prompts installs by declaring
`extraKnownMarketplaces` in the project `.claude/settings.json` (fires on workspace-trust). Container/CI
pre-population: `CLAUDE_CODE_PLUGIN_SEED_DIR`.

**Curation is the open-marketplace-+-review-gate model**, exactly aspect-27's ADR-0010 tradeoff resolved by
Anthropic itself [lit, plugins + discover-plugins]:

- **`claude-plugins-official`** — "curated by Anthropic, and inclusion is at Anthropic's discretion" (no
  application process).
- **`claude-plugins-community` / `claude-community`** — third-party submissions that "passed Anthropic's
  automated validation and safety screening," each **pinned to a specific commit SHA**. Submit via an in-app form;
  "Run `claude plugin validate` locally before you submit. The review pipeline runs the same check on every
  submission, along with automated safety screening." → a public marketplace with a **validate + safety-screen +
  SHA-pin** gate. Reserved names (`anthropic-*`, `claude-plugins-*`, `agent-skills`, …) block impersonation.
- **Validation** (the publishable floor): "the validator checks `marketplace.json` only: schema, duplicate plugin
  names, source path traversal, and version mismatches against each referenced `plugin.json`"; run against a
  *plugin* dir to also check SKILL/agent/command frontmatter + `hooks/hooks.json` JSON.
- **Managed lockdown:** `strictKnownMarketplaces` — `[]` = no marketplaces addable; a list = exact-match
  allowlist (+ `hostPattern`/`pathPattern` regex); "checked before any network or filesystem operation."

## 7. Marketplace + plugin security (untrusted code, verbatim)

This is the same first-class concern as hooks/MCP, stated bluntly [lit, discover-plugins, verbatim]:

> "Plugins and marketplaces are **highly trusted components that can execute arbitrary code on your machine with
> your user privileges**. Only install plugins and add marketplaces from sources you trust."

and per-install:

> "Make sure you trust a plugin before installing it. **Anthropic doesn't control what MCP servers, files, or
> other software are included in plugins** and can't verify that they work as intended."

The consequence: a plugin bundles **hooks** (arbitrary shell on lifecycle events, no per-run consent —
§`hooks-commands-subagents-standard`) and **MCP servers** (arbitrary processes — §`mcp-server-standard`), so
**adding a marketplace + installing a plugin is a code-trust decision, made at install time**. Mitigations the
platform builds in: plugins are **copied to a cache** (not run in place) and **can't path-traverse** outside their
root; symlinks outside the marketplace are **skipped for security**; project `@skills-dir` plugins load only after
the **workspace-trust dialog** (and their MCP servers re-prompt per server, monitors don't load); the `/plugin`
detail view shows a **"Will install" component inventory + token cost** before you commit. A marketplace operator
inherits the trust of every plugin it lists — curation is a security duty, not just taste.

---

# Part C — Memory & context management (the persistence layer)

The governing fact: "Each Claude Code session begins with a fresh context window" [lit, memory]. Everything below
exists to carry state across that boundary **as explicit, inspectable files** — not as implicit chat history.
There are three tiers: a **static instruction hierarchy** (§8), a **generated/agentic memory layer** (§9), and
the **context-engineering discipline** that governs the window itself (§10).

## 8. The static instruction hierarchy (CLAUDE.md / AGENTS.md)

CLAUDE.md files are "instructions you write to give Claude persistent context," **loaded into context at the
start of every session** [lit, memory]. The hierarchy, in load order **broad → specific** (all *concatenated*,
not overriding) [lit, verbatim table]:

| Scope | Location | Notes |
|---|---|---|
| Managed policy | `/Library/Application Support/ClaudeCode/CLAUDE.md` · `/etc/claude-code/CLAUDE.md` · `…\ClaudeCode\CLAUDE.md` | org-wide; **cannot be excluded** by users |
| User | `~/.claude/CLAUDE.md` | personal, all projects |
| Project | `./CLAUDE.md` or `./.claude/CLAUDE.md` | team-shared via VCS |
| Local | `./CLAUDE.local.md` | personal per-project; gitignore it |

Claude **walks up the directory tree** concatenating each `CLAUDE.md`/`CLAUDE.local.md`; subdir files load **on
demand** when Claude reads files there. **`@`-imports** pull in extra files: "`@path/to/import` … Both relative
and absolute paths are allowed. … Imported files can recursively import other files, with a **maximum depth of
four hops**" [lit, verbatim] (code-span `` `@x` `` is skipped; the first external import shows an **approval
dialog**). **`.claude/rules/`** holds modular per-topic rule files; a `paths:` frontmatter glob scopes a rule so
it loads only when matching files are touched (progressive disclosure for rules). Bootstrap with **`/init`**;
inspect with **`/memory`**.

**The cross-vendor split is identical** [lit]: Claude Code reads **CLAUDE.md** (`@AGENTS.md`-import to reuse an
existing one); OpenAI Codex reads **AGENTS.md**. Both vendors say the same thing — *a fact/rule that always
applies → the constitution; a procedure → a skill*. CLAUDE.md best practices: **"target under 200 lines"** ("Longer
files consume more context and reduce adherence"), be **specific** ("Use 2-space indentation" not "format code
properly"), avoid **contradictions** ("Claude may pick one arbitrarily"). Critically (verbatim): memory is
**"context, not enforced configuration. To block an action regardless of what Claude decides, use a PreToolUse
hook instead."** — a rule that *must* hold is a hook, not a CLAUDE.md line (the same hook-vs-prose boundary
aspect-27 draws everywhere).

## 9. The generated / agentic-memory layer (memory tool · auto-memory · Codex Memories)

Beyond what you write, the agent maintains its own memory — the realization of Anthropic's **structured
note-taking** principle: "the agent regularly writes notes persisted to memory outside of the context window.
These notes get pulled back into the context window at later times" [lit, context-engineering]. Three concrete
implementations:

- **Claude Code auto-memory** (CC v2.1.59+) — per-project `~/.claude/projects/<project>/memory/` with a
  **`MEMORY.md` index** + topic files. "The first 200 lines of `MEMORY.md`, or the first 25KB, whichever comes
  first, are loaded at the start of every conversation"; topic files load **on demand** [lit]. Claude writes its
  own learnings (build commands, debugging insights, preferences) — plain markdown the user can `/memory`-audit
  and edit. *(This is exactly the `MEMORY.md`-indexed auto-memory backing this very research session.)*
- **The API memory tool** (`memory_20250818`) — a **client-side, file-based** store: "Claude makes tool calls to
  perform memory operations, and **your application executes those operations locally**" [lit, verbatim]. Command
  set: **`view` · `create` · `str_replace` · `insert` · `delete` · `rename`**, all under the **`/memories`**
  directory; the auto-injected system prompt is emphatic — **"ALWAYS VIEW YOUR MEMORY DIRECTORY BEFORE DOING
  ANYTHING ELSE … ASSUME INTERRUPTION: Your context window might be reset at any moment, so you risk losing any
  progress that is not recorded in your memory directory."** Anthropic's **multi-session SW-dev pattern**: an
  initializer session bootstraps a **progress log + feature checklist + init-script reference**; each session
  reads them on open and updates the progress log on close — "Work on one feature at a time. Only mark a feature
  complete after end-to-end verification."
- **OpenAI Codex Memories** — the same two-layer model on the other host: **AGENTS.md** (static) + **Memories**
  (Codex-generated session summaries in **`~/.codex/memories/`**), enabled via `[features] memories = true` in
  `~/.codex/config.toml`. The guidance is the explicit-files-win stance verbatim [lit]: **"Keep required team
  guidance in `AGENTS.md` or checked-in documentation. Treat memories as a helpful local recall layer, not as the
  only source for rules that must always apply."**

**The principle across all three: memory = explicit files, not chat state.** A static file holds rules-that-must-
hold; a generated memory dir holds learnings; both are **inspectable, editable, version-control-able artifacts**,
not opaque transcript. (Contrast OpenAI's **Responses/Conversations API**, where state is **server-side** —
`previous_response_id` chains stored responses, the Conversations API is a durable object "reusable across
sessions, devices, or jobs," `store:false` to opt out — and the **Agents-SDK Sessions** client store (`SQLiteSession`
file/db, `OpenAIResponsesCompactionSession` for auto-compaction). The "explicit local files" stance is strongest
on the Anthropic/Claude-Code side, and is the one gingoa scaffolds to.)

## 10. Context engineering — the discipline that governs the window

Memory files exist *because* context is scarce. Anthropic's framing [lit, context-engineering, verbatim]:
"Context engineering refers to the set of strategies for curating and maintaining the optimal set of tokens
(information) during LLM inference," and **"Context, therefore, must be treated as a finite resource with
diminishing marginal returns"** ("context rot"; each token spends an "attention budget"). The operating rules:

- **Right altitude / smallest high-signal set** — aim for the **"smallest possible set of high-signal tokens that
  maximize the likelihood of some desired outcome."** Every CLAUDE.md line, skill description, and bundled MCP
  tool is a *recurring* cost (hence the <200-line CLAUDE.md, the `claude plugin details` token meter).
- **Just-in-time / progressive disclosure** — "agents built with the 'just in time' approach maintain lightweight
  identifiers (file paths, stored queries, web links, etc.)" and load context on demand. This is the *same*
  progressive-disclosure model as skills (metadata→body→files), auto-memory (`MEMORY.md` index → topic files on
  demand), and `.claude/rules/` (`paths`-scoped).
- **Compaction** — summarize the conversation at the limit and restart from the compressed summary (project-root
  CLAUDE.md is re-read from disk and survives `/compact`). OpenAI's `responses.compact` /
  `OpenAIResponsesCompactionSession` is the mirror.
- **Context editing** — Anthropic's automatic clearing of "stale tool calls and results from within the context
  window when approaching token limits." Measured (verbatim): **memory tool + context editing = 39%** improvement
  on agentic-search evals; **context editing alone = 29%**; in a 100-turn web-search eval it completed
  otherwise-failing workflows "while reducing token consumption by **84%**."
- **Sub-agent isolation** — verbose work in a clean-context worker returning a 1–2K-token summary
  (§`hooks-commands-subagents-standard`).

## 11. Memory security — poisoning + path traversal

Memory is an attack surface, two ways:

- **Path traversal (memory tool)** — the model controls the paths it writes; the *client* executes them. Verbatim
  WARNING [lit]: "Malicious path inputs could attempt to access files outside the `/memories` directory. Your
  implementation **MUST** validate all paths to prevent directory traversal attacks." Safeguards: enforce paths
  start with `/memories`, canonicalize + `relative_to`, reject `../`/`..\`/`%2e%2e%2f`. Plus: refuse/strip
  sensitive data (Codex "redacts secrets from generated memory fields"; the memory tool "will usually refuse to
  write … sensitive information," but harden it), cap file size + paginate, expire stale files.
- **Memory poisoning (instruction injection via a memory/import)** — because CLAUDE.md, `@`-imports, and generated
  memory files all flow into context, a malicious imported file or a poisoned auto-memory note is a prompt-
  injection vector. Hence the **first-external-import approval dialog**, the **workspace-trust gate** before a
  project's memory/rules load, and the **auditability** of memory as plain editable markdown. Treat any
  memory/import from an untrusted source the way you'd treat an untrusted skill or marketplace plugin.

---

## Anti-patterns (each cited)

- **Components inside `.claude-plugin/`** — the #1 plugin bug; only `plugin.json` lives there, every component
  folder is at the plugin root [lit].
- **`version` set but never bumped** — Claude Code keeps the cached copy, so users never see your changes; bump on
  every release or omit `version` to use the git SHA [lit].
- **`../` / out-of-root paths in a plugin** — won't resolve after the plugin is copied to the cache; use
  `${CLAUDE_PLUGIN_ROOT}` and in-marketplace symlinks [lit].
- **Relative `source` in a URL-distributed marketplace** — only `marketplace.json` is downloaded, so `./plugins/x`
  fails; use `github`/`npm`/`url` sources for URL distribution [lit].
- **`author`/`owner` as a string** — both are **objects** `{name,…}`; a string is wrong shape [lit].
- **Adding an untrusted marketplace / installing an unaudited plugin** — "arbitrary code … with your user
  privileges"; a plugin's bundled hooks + MCP run as you [lit].
- **A constitution bundled as a plugin-root `CLAUDE.md`** — not loaded as context; ship instructions as a skill
  [lit].
- **A rule-that-must-hold written in CLAUDE.md** — it's advisory "context, not enforced configuration"; a hard
  rule is a `PreToolUse` hook [lit].
- **CLAUDE.md > 200 lines / dumping reference into the constitution** — "consumes more context and reduces
  adherence"; move procedures to skills, scope rules with `.claude/rules/` `paths`, push reference to
  on-demand files [lit].
- **Contradictory instructions across CLAUDE.md levels** — "Claude may pick one arbitrarily"; reconcile them
  [lit].
- **Memory = chat state** — relying on transcript history for durable knowledge; it dies at the fresh-context
  boundary. Persist to explicit files (auto-memory / `/memories` / a committed CLAUDE.md) [lit].
- **Unvalidated memory-tool paths / un-redacted secrets / unbounded memory growth** — the named memory-tool
  security gaps [lit].
- **`@`-import chains deeper than needed** — the import depth caps at 4 hops; over-nesting silently drops content
  [lit].

## How gingoa should scaffold/publish each

gingoa **scaffolds + distributes** this layer (and dogfoods it: it already ships `.claude-plugin/marketplace.json`
+ `adapters/gingoa/.{claude,codex}-plugin/plugin.json` + a bundled skill, and its own auto-memory uses a
`MEMORY.md` index). To match this standard:

1. **Plugin scaffold** — emit a directory with `.claude-plugin/plugin.json` carrying **`name` (required, kebab)**
   + an **object `author`** + an explicit **`version`** (or a documented "omit to use git SHA" choice), and
   **auto-discovered component folders at the root** (`skills/<name>/SKILL.md`, `agents/`, `hooks/hooks.json`,
   `.mcp.json`) — **never inside `.claude-plugin/`**. Bundled hook/MCP commands MUST use **`${CLAUDE_PLUGIN_ROOT}`**
   (and `${CLAUDE_PLUGIN_DATA}` for state). Cross-host: ship **both** `.claude-plugin/plugin.json` and
   `.codex-plugin/plugin.json` (per `host-config-schemas.md`).
2. **Marketplace scaffold + publish** — emit a root `.claude-plugin/marketplace.json` with **`name`/`owner`(obj)/
   `plugins[]`** (each `name`+`source`); default `source` = a **`./`-relative same-repo path** (correct for
   gingoa's monorepo), and offer `github`/`git-subdir`/`npm` for split-repo distribution. Publish = a git push;
   add `metadata.description` (validator warns without it). Curate via the **open-marketplace + review-gate**
   model (ADR-0010): run `claude plugin validate --strict` in CI on every shipped manifest, and **SHA-pin** listed
   third-party plugins.
3. **Memory scaffold** — emit a **`CLAUDE.md` (or `@AGENTS.md`-importing CLAUDE.md for cross-host)** under 200
   lines, specific + non-contradictory, with **procedures pushed to skills** and **path-scoped rules in
   `.claude/rules/`**; surface the *fact→constitution / procedure→skill / hard-rule→hook* boundary at scaffold
   time. For an agent that runs the API, scaffold the **memory tool with a `/memories`-jail path validator**
   (reject `../`, canonicalize, `relative_to`) + size/secret guards, and the **progress-log + feature-checklist**
   bootstrap pattern. Frame durable state as **explicit files, not chat history**.
4. **A validation gate (presence ≠ adequacy)** — mirror aspect-27's manifest-schema rule (already in `<topic>--overview.md`):
   a **vitest test** asserting every shipped `plugin.json`/`marketplace.json` has its required keys
   (`name`; marketplace `name`+`owner`+`plugins[]`), `author`/`owner` are **objects**, each plugin `source`
   resolves, no component dirs sit inside `.claude-plugin/`, and `claude plugin validate` passes clean; plus a
   check that a scaffolded `CLAUDE.md` is ≤200 lines and `@`-imports stay ≤4 hops, and that the memory-tool path
   validator rejects traversal fixtures. A manifest/memory file that only "looks right" but doesn't validate is a
   bug, not a deliverable.

This makes the gingoa packaging+memory scaffold emit the **portable, cross-host artifacts** (one plugin →
Claude Code + Codex; one marketplace both hosts read; a CLAUDE.md/AGENTS.md + explicit memory files) at the
Anthropic/OpenAI quality bar, with the untrusted-by-default trust model and the context-engineering discipline
built in — gated like every other shipped guardrail.

## Sources

- Claude Code — Create plugins (what a plugin bundles, standalone-vs-plugin, layout) — https://code.claude.com/docs/en/plugins
- Claude Code — Plugins reference (full `plugin.json` schema, required `name`, auto-discovery, CLI, `${CLAUDE_PLUGIN_ROOT}`, caching, versioning) — https://code.claude.com/docs/en/plugins-reference
- Claude Code — Create and distribute a plugin marketplace (`marketplace.json` schema, `source` forms, hosting, curation, `strictKnownMarketplaces`) — https://code.claude.com/docs/en/plugin-marketplaces
- Claude Code — Discover and install plugins (install flow, official/community curation, the verbatim security/trust warnings) — https://code.claude.com/docs/en/discover-plugins
- Claude Code — How Claude remembers your project (CLAUDE.md hierarchy + `@`-imports ≤4 hops + `.claude/rules/` + auto-memory `MEMORY.md`) — https://code.claude.com/docs/en/memory
- Anthropic API — Memory tool (`memory_20250818`: client-side file store, `view/create/str_replace/insert/delete/rename`, `/memories`, path-traversal MUST-validate) — https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool
- Anthropic — Effective context engineering for AI agents (finite resource · smallest high-signal set · just-in-time · compaction · structured note-taking · sub-agents) — https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- Anthropic — Managing context on the Claude Developer Platform (memory tool + context editing; 39% / 29% / 84% numbers) — https://claude.com/blog/context-management
- OpenAI Codex — Memories (AGENTS.md static + `~/.codex/memories/` generated; "keep required guidance in AGENTS.md") — https://developers.openai.com/codex/memories
- OpenAI Codex — Custom instructions with AGENTS.md — https://developers.openai.com/codex/guides/agents-md
- OpenAI — Conversation state (Responses API `previous_response_id` + Conversations API; `store:false`) — https://developers.openai.com/api/docs/guides/conversation-state
- OpenAI Agents SDK — Sessions (`SQLiteSession`, compaction session, automatic history) — https://openai.github.io/openai-agents-python/sessions/
- gingoa shipped manifests — `adapters/gingoa/.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, root `.claude-plugin/marketplace.json`; cross-host wiring — `host-config-schemas.md`
- Raw harvested schemas + verbatim quotes — `census-data/frontier-ai-components/plugins-marketplace-memory/samples.md`
