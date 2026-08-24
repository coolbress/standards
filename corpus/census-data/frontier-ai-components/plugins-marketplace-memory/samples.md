# plugins · marketplace · memory — raw samples (verbatim schemas + quotes)

Captured 2026-06-27 from the sources in `README.md`. Append-only.

---

## 1. plugin.json — Claude Code manifest (verbatim, plugins-reference)

A **plugin** = "a self-contained directory of components that extends Claude Code with custom functionality.
Plugin components include skills, agents, hooks, MCP servers, LSP servers, and monitors."

**Complete schema** (verbatim):
```json
{
  "name": "plugin-name",
  "displayName": "Plugin Name",
  "version": "1.2.0",
  "description": "Brief plugin description",
  "author": { "name": "Author Name", "email": "author@example.com", "url": "https://github.com/author" },
  "homepage": "https://example.com/",
  "repository": "https://github.com/git/git",
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"],
  "skills": "./custom/skills/",
  "commands": ["./custom/commands/special.md"],
  "agents": ["./custom/agents/reviewer.md"],
  "hooks": "./config/hooks.json",
  "mcpServers": "./mcp-config.json",
  "outputStyles": "./styles/",
  "lspServers": "./.lsp.json",
  "experimental": { "themes": "./themes/", "monitors": "./monitors.json" },
  "dependencies": ["helper-lib", { "name": "secrets-vault", "version": "~2.1.0" }]
}
```

**Required fields (verbatim):** "The manifest is optional. If omitted, Claude Code auto-discovers components in
default locations and derives the plugin name from the directory name." — **"If you include a manifest, `name`
is the only required field."** `name` = unique identifier (kebab-case, no spaces), used for namespacing.

**`author`** is an **object** `{name, email?, url?}`. **`version`** optional: "If omitted … the git commit SHA
is used and every commit counts as a new version."

**Unrecognized fields:** "Claude Code ignores top-level fields it does not recognize" (so one manifest can double
as a VS Code / Cursor / package.json / MCPB-DXT manifest). `claude plugin validate` reports them as **warnings**;
`--strict` treats warnings as errors. A `keywords` string-instead-of-array is a **load error**.

**Component path behavior:** `commands`/`agents`/`outputStyles`/`themes`/`monitors` **replace** the default
dir; `skills` **adds to** the default `skills/` scan. All custom paths must be relative + start with `./`.

**Default auto-discovery layout (File locations reference, verbatim):**
| Component | Default Location |
|---|---|
| Manifest | `.claude-plugin/plugin.json` |
| Skills | `skills/` (`<name>/SKILL.md`) |
| Commands | `commands/` (flat `.md`; "Use `skills/` for new plugins") |
| Agents | `agents/` |
| Hooks | `hooks/hooks.json` |
| MCP servers | `.mcp.json` |
| LSP servers | `.lsp.json` |
| Monitors | `monitors/monitors.json` |
| Executables | `bin/` (added to Bash `PATH`) |
| Settings | `settings.json` (only `agent` + `subagentStatusLine` keys) |

**Layout WARNING (verbatim):** "Don't put `commands/`, `agents/`, `skills/`, or `hooks/` inside the
`.claude-plugin/` directory. Only `plugin.json` goes inside `.claude-plugin/`. All other directories must be at
the plugin root level."

**Single-skill plugin:** a `SKILL.md` at the plugin root (no `skills/` dir, no `skills` field) loads as one
skill (CC v2.1.142+); the frontmatter `name` is the invocation name. ← gingoa's `adapters/gingoa` uses the
`skills/<name>/SKILL.md` layout.

**`CLAUDE.md` at plugin root is NOT loaded as project context** (verbatim): "Plugins contribute context through
skills, agents, and hooks rather than CLAUDE.md."

**Env vars:** `${CLAUDE_PLUGIN_ROOT}` (abs install dir, changes on update — "do not write state here"),
`${CLAUDE_PLUGIN_DATA}` (persistent state dir surviving updates, `~/.claude/plugins/data/{id}/`),
`${CLAUDE_PROJECT_DIR}` (project root).

**Version resolution order:** `plugin.json` version → marketplace-entry version → git commit SHA → `unknown`.

---

## 2. plugin CLI (verbatim subcommands, plugins-reference)

- `claude plugin init <name> [--with skills agents hooks mcp lsp output-style channel] [--force]` — scaffold a
  `@skills-dir` plugin at `~/.claude/skills/<name>/`.
- `claude plugin install <plugin>[@marketplace] [--scope user|project|local]`
- `claude plugin uninstall <plugin> [--scope] [--keep-data] [--prune]` (aliases `remove`, `rm`)
- `claude plugin enable|disable <plugin> [--scope]`
- `claude plugin update <plugin> [--scope user|project|local|managed]`
- `claude plugin list [--json] [--available]`
- `claude plugin details <name>` — component inventory + projected **token cost** (always-on vs on-invoke)
- `claude plugin validate <root> [--strict]`
- `claude plugin tag [--push]` — release git tag
- `claude plugin marketplace {add,list,remove,update}` (see §4)
- Test without install: `claude --plugin-dir ./my-plugin` (or `.zip`), `claude --plugin-url <url>`;
  `/reload-plugins` to hot-reload. Interactive: `/plugin` (Discover/Installed/Marketplaces/Errors tabs).

**Install scopes:** `user` (`~/.claude/settings.json`, default) · `project` (`.claude/settings.json`, team) ·
`local` (`.claude/settings.local.json`, gitignored) · `managed` (read-only).

**settings.json keys:** `enabledPlugins: { "<plugin>@<marketplace>": true }` ·
`extraKnownMarketplaces: { "<name>": { "source": {...}, "autoUpdate"? } }` ·
`strictKnownMarketplaces` / `blockedMarketplaces` (managed-only allow/deny).

---

## 3. plugin SECURITY (verbatim, discover-plugins)

**Top-level Security section (verbatim):**
> "Plugins and marketplaces are highly trusted components that can execute arbitrary code on your machine with
> your user privileges. Only install plugins and add marketplaces from sources you trust. Organizations can
> restrict which marketplaces users are allowed to add using managed marketplace restrictions."

**Per-install warning (verbatim):**
> "Make sure you trust a plugin before installing it. Anthropic doesn't control what MCP servers, files, or other
> software are included in plugins and can't verify that they work as intended. Check each plugin's homepage for
> more information."

**External-imports warning (memory, verbatim):** "The first time Claude Code encounters external imports in a
project, it shows an approval dialog listing the files. If you decline, the imports stay disabled…"

**Plugin caching:** marketplace plugins are **copied** to `~/.claude/plugins/cache` (not used in place); paths
can't traverse outside the plugin root (`../shared-utils` won't resolve); symlinks outside the marketplace are
**skipped for security**. Project `@skills-dir` plugins load only after the **workspace-trust dialog**; their
MCP servers go through per-server approval, LSP only after trust, monitors don't load at all.

---

## 4. marketplace.json — Claude Code catalog (verbatim, plugin-marketplaces)

A marketplace = "a catalog that lets you distribute plugins to others … centralized discovery, version tracking,
automatic updates, and support for multiple source types."

**Required top-level fields (verbatim table):** `name` (kebab-case identifier; public-facing; one marketplace
per name per user) · `owner` (object) · `plugins` (array). Optional: `$schema`, `description`, `version`,
`metadata.pluginRoot`, `allowCrossMarketplaceDependenciesOn`. (`description`/`version` also accepted under
`metadata`.)

**Owner fields:** `name` (Yes) · `email` (No).

**Per-plugin entry — required:** `name`, `source`. Optional: any plugin.json field (`description`, `version`,
`author`, `homepage`, `repository`, `license`, `keywords`, component paths…) **plus** marketplace-specific
`category`, `tags`, `strict`, `relevance`, `defaultEnabled`.

**`source` forms (verbatim table):**
| Source | Shape |
|---|---|
| Relative path | `"./my-plugin"` string — must start with `./`, resolves vs marketplace root, no `../` |
| `github` | `{ "source": "github", "repo": "owner/repo", "ref"?, "sha"? }` |
| `url` (git) | `{ "source": "url", "url": "https://github.com/git/git.git", "ref"?, "sha"? }` |
| `git-subdir` | `{ "source": "git-subdir", "url", "path", "ref"?, "sha"? }` (sparse clone for monorepos) |
| `npm` | `{ "source": "npm", "package": "@org/plugin", "version"?, "registry"? }` |

**`strict`** (default `true`): plugin.json is the component authority; `false` = the marketplace entry is the
entire definition (and the plugin needs no plugin.json).

**Example (verbatim, the canonical 2-plugin marketplace):**
```json
{
  "name": "company-tools",
  "owner": { "name": "DevTools Team", "email": "devtools@example.com" },
  "plugins": [
    { "name": "code-formatter", "source": "./plugins/formatter", "description": "…", "version": "2.1.0",
      "author": { "name": "DevTools Team" } },
    { "name": "deployment-tools", "source": { "source": "github", "repo": "company/deploy-plugin" },
      "description": "…" }
  ]
}
```

**marketplace CLI:**
- `claude plugin marketplace add <owner/repo | git-url | url-to-marketplace.json | local-path> [--scope] [--sparse …]`
  (pin via `@ref` on GH shorthand or `#ref` on git URL)
- `claude plugin marketplace list [--json]`
- `claude plugin marketplace remove <name>` ("Removing a marketplace from its last remaining scope also
  uninstalls any plugins you installed from it.")
- `claude plugin marketplace update [name]`

**Hosting/curation:** GitHub recommended (just a git repo with `.claude-plugin/marketplace.json` at root); any
git host works; private repos via git credential helpers / `GITHUB_TOKEN` for background auto-update.
`extraKnownMarketplaces` in project `.claude/settings.json` prompts teammates to install on folder-trust.
**Validation (verbatim):** "When pointed at a marketplace directory, the validator checks `marketplace.json`
only: schema, duplicate plugin names, source path traversal, and version mismatches against each referenced
`plugin.json`."

**Anthropic's own marketplaces:** `claude-plugins-official` (curated by Anthropic, auto-registered, "inclusion
is at Anthropic's discretion") · `claude-plugins-community` / `claude-community` (third-party submissions that
"passed Anthropic's automated validation and safety screening", **pinned to a specific commit SHA**). Submit via
in-app forms; "Run `claude plugin validate` locally before you submit. The review pipeline runs the same check on
every submission, along with automated safety screening." **Reserved names** (cannot be used by third parties):
`claude-plugins-official`, `claude-plugins-community`, `anthropic-*`, `agent-skills`, etc.

**Managed restriction (verbatim):** `strictKnownMarketplaces` — `[]` = complete lockdown; a list = exact-match
allowlist (with `hostPattern`/`pathPattern` regex forms); "Restrictions are checked before any network or
filesystem operation."

---

## 5. Codex plugin/marketplace (cross-host, empirically verified — host-config-schemas.md)

- Codex reads the **SAME** root `.claude-plugin/marketplace.json` (`codex plugin marketplace add <repo>` reported
  `Added marketplace 'gingoa'`). `codex plugin` = only `marketplace {add, upgrade, remove}` — **no separate
  `enable`/`install`**; registering the marketplace IS enablement.
- `marketplace add <dir>` writes ONLY `[marketplaces.<name>]` `{ last_updated, source_type="local", source=<abs> }`
  to `~/.codex/config.toml`; the root is referenced by path, not copied.
- Codex did NOT validate the plugin manifest at add-time (succeeded with no plugin.json, with only
  `.codex-plugin/plugin.json`, and with only `.claude-plugin/plugin.json`). gingoa ships **both**
  `.claude-plugin/plugin.json` + `.codex-plugin/plugin.json` (harmless + future-proof).

**gingoa's shipped manifests (verbatim):**
- `.claude-plugin/marketplace.json`: `{ name:"gingoa", owner:{name:"coolbress"}, metadata:{description}, plugins:[{ name:"gingoa", source:"./adapters/gingoa", description }] }`
- `adapters/gingoa/.claude-plugin/plugin.json` == `.codex-plugin/plugin.json`:
  `{ name:"gingoa", version:"0.1.0", description, author:{name:"coolbress"} }`

---

## 6. MEMORY — Claude Code (verbatim, memory docs)

**Two systems, both loaded every session:**
- **CLAUDE.md files** — you write; instructions/rules. **Auto memory** — Claude writes; learnings/patterns.
  (verbatim) "To block an action regardless of what Claude decides, use a PreToolUse hook instead." — memory is
  **context, not enforced configuration**.

**CLAUDE.md hierarchy (load order, broad→specific, verbatim table):**
| Scope | Location |
|---|---|
| Managed policy | `/Library/Application Support/ClaudeCode/CLAUDE.md` · `/etc/claude-code/CLAUDE.md` · `C:\Program Files\ClaudeCode\CLAUDE.md` (cannot be excluded) |
| User | `~/.claude/CLAUDE.md` |
| Project | `./CLAUDE.md` or `./.claude/CLAUDE.md` |
| Local | `./CLAUDE.local.md` (gitignore it) |

"All discovered files are concatenated into context rather than overriding each other." Walks UP the dir tree;
subdir CLAUDE.md load **on demand** when Claude reads files there.

**`@`-imports (verbatim):** "`@path/to/import` syntax. … Both relative and absolute paths are allowed. … Imported
files can recursively import other files, with a **maximum depth of four hops**." Code-span paths (`` `@README` ``)
are skipped. First external import shows an **approval dialog**.

**`.claude/rules/`** — modular per-topic rule files; `paths:` frontmatter scopes a rule to globs (loads only when
matching files are touched). Loaded with same priority as `.claude/CLAUDE.md`.

**Commands:** `/init` (generate/improve CLAUDE.md; `CLAUDE_CODE_NEW_INIT=1` = interactive multi-phase) · `/memory`
(list+edit loaded memory files, toggle auto-memory) · "remember that …" in chat → saved to auto memory.

**AGENTS.md interop (verbatim):** "Claude Code reads `CLAUDE.md`, not `AGENTS.md`." → import it: `@AGENTS.md` (or
symlink). `/init` reads an existing AGENTS.md + `.cursorrules`/`.windsurfrules`.

**Auto memory (the generated layer, CC v2.1.59+):** per-project dir
`~/.claude/projects/<project>/memory/` with a **`MEMORY.md` index** + topic files. "The first 200 lines of
`MEMORY.md`, or the first 25KB, whichever comes first, are loaded at the start of every conversation." Topic
files load **on demand**. Plain markdown, editable. Machine-local; shared across worktrees of one repo.
`autoMemoryEnabled` / `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` to toggle.  ← This is exactly the MEMORY.md index
gingoa's own auto-memory uses.

**Best practices (verbatim):** "target under 200 lines per CLAUDE.md file. Longer files consume more context and
reduce adherence." Specific > vague ("Use 2-space indentation" not "Format code properly"). Conflicting rules →
"Claude may pick one arbitrarily." Block-HTML comments are stripped before injection (free maintainer notes).
**Compaction:** "Project-root CLAUDE.md survives compaction: after `/compact`, Claude re-reads it from disk…"

---

## 7. MEMORY tool — Anthropic API (verbatim, memory-tool docs)

"The memory tool enables Claude to store and retrieve information across conversations through a memory file
directory." — **client-side**: "Claude makes tool calls to perform memory operations, and your application
executes those operations locally." Tool type `memory_20250818`.

**Commands (verbatim):** `view` (dir listing or file w/ optional `view_range`) · `create` (`path`, `file_text`) ·
`str_replace` (`path`, `old_str`, `new_str`) · `insert` (`path`, `insert_line`, `insert_text`) · `delete`
(`path`; recursive for dirs) · `rename` (`old_path`, `new_path`).

**The `/memories` directory** — Claude "automatically checks its memory directory before starting tasks." Auto
system-prompt instruction (verbatim): **"IMPORTANT: ALWAYS VIEW YOUR MEMORY DIRECTORY BEFORE DOING ANYTHING
ELSE."** + "ASSUME INTERRUPTION: Your context window might be reset at any moment, so you risk losing any progress
that is not recorded in your memory directory."

**Security — path traversal (verbatim WARNING):** "Malicious path inputs could attempt to access files outside
the `/memories` directory. Your implementation **MUST** validate all paths to prevent directory traversal
attacks." Safeguards: validate paths start with `/memories`; canonicalize + `relative_to`; reject `../`/`..\`/
`%2e%2e%2f`. Plus: strip sensitive info, cap file size + paginate, expire stale files.

**Multi-session SW-dev pattern:** initializer session bootstraps a **progress log + feature checklist +
init-script reference**; each session opens by reading them, closes by updating the progress log; "Work on one
feature at a time. Only mark a feature complete after end-to-end verification."

---

## 8. CONTEXT engineering — Anthropic (verbatim, eng post + announcement)

"Context engineering refers to the set of strategies for curating and maintaining the optimal set of tokens
(information) during LLM inference." Scarcity (verbatim): **"Context, therefore, must be treated as a finite
resource with diminishing marginal returns."** — "context rot", "attention budget".

**Right altitude (verbatim):** find the **"smallest possible set of high-signal tokens that maximize the
likelihood of some desired outcome."**

**Just-in-time (verbatim):** "agents built with the 'just in time' approach maintain lightweight identifiers
(file paths, stored queries, web links, etc.)" → progressive disclosure.

**Long-horizon techniques:**
- **Compaction** — summarize at the context limit + restart with the compressed summary.
- **Structured note-taking / agentic memory (verbatim):** "the agent regularly writes notes persisted to memory
  outside of the context window. These notes get pulled back into the context window at later times." (Claude
  plays Pokémon ex.)
- **Sub-agents** — focused clean-context workers returning 1–2K-token summaries.

**Context-editing announcement (verbatim numbers):** memory tool + context editing = **39%** improvement;
context editing alone = **29%**; 100-turn web-search eval — context editing completed otherwise-failing
workflows "while reducing token consumption by **84%**." Context editing "automatically clears stale tool calls
and results from within the context window when approaching token limits."

---

## 9. MEMORY — OpenAI equivalents (verbatim, Codex + Responses/Agents-SDK)

**Codex (developers.openai.com/codex/memories):** two-layer — **AGENTS.md** (static, user-written, read every
session) + **Memories** (Codex-generated session summaries in `~/.codex/memories/`). (verbatim) **"Keep required
team guidance in `AGENTS.md` or checked-in documentation. Treat memories as a helpful local recall layer, not as
the only source for rules that must always apply."** Enable: `[features] memories = true` in `~/.codex/config.toml`
(`memories.use_memories`, `memories.generate_memories`). Redacts secrets, skips short sessions, updates in
background. — DIRECTLY parallels Claude Code's CLAUDE.md + auto-memory split.

**Responses API conversation state:** server-side. `previous_response_id` chains stored responses (pass only the
new turn); **Conversations API** = a durable conversation object reusable "across sessions, devices, or jobs."
"Responses are stored by default … set `store: false`" (ZDR → encrypted reasoning items). ← state lives on
OpenAI's servers, not as explicit local files.

**Agents SDK Sessions:** client-side memory store keyed by session id; `SQLiteSession` (in-memory default; file
path = persistent); `session.get_items()` prepends history before each turn, `add_items()` after.
`OpenAIResponsesCompactionSession` wraps a session + `responses.compact` for automatic compaction;
`AdvancedSQLiteSession` adds branching/usage analytics.

**Contrast captured:** Anthropic's primary durable layer = **explicit files** (CLAUDE.md, `/memories/*`,
auto-memory `MEMORY.md`) the user can read/edit/commit; OpenAI's Responses/Conversations state is **opaque
server-side** (though Codex Memories + Agents-SDK SQLite are file/db-local). The "memory = explicit files" stance
is strongest on the Anthropic/Claude-Code side and is what gingoa scaffolds to.
