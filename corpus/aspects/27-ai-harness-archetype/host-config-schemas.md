---
id: aspect-27-ai-harness-archetype--host-config-schemas
title: "Host config-integration schemas (cross-host adapter evidence)"
parent: aspect-27-ai-harness-archetype
kind: evidence
evidence_track: lit
status: review-needed
last_updated: "2026-06-26"
method: "empirical — Claude Code docs + `claude plugin validate`; Codex via `codex plugin marketplace add` against a sandboxed CODEX_HOME (codex-cli 0.125.0)"
---

# Host config-integration schemas (verified facts)

Gingoa attaches to each host by editing that host's config file. These are the **verified** shapes the
install/doctor/uninstall code depends on. Re-verify before assuming on a new host version.

## Claude Code — `~/.claude/settings.json` (JSON)
Verified against current Claude Code docs (code.claude.com/docs settings + plugins-reference), 2026-06-26.

- Register a local directory marketplace:
  ```json
  "extraKnownMarketplaces": { "<name>": { "source": { "source": "directory", "path": "<abs>" } } }
  ```
  (the doubled `source` nesting is correct — outer key `source`, inner discriminator `source:"directory"`)
- Enable a plugin: `"enabledPlugins": { "<plugin>@<marketplace>": true }`
- Marketplace manifest: `<root>/.claude-plugin/marketplace.json`; plugin manifest:
  `<plugin>/.claude-plugin/plugin.json`. `owner`/`author` are OBJECTS `{name, email?, url?}`.
  Component-path fields (skills/commands/agents/hooks) are OMITTED → auto-discovery at the plugin root.
  Skills auto-discover from `skills/<name>/SKILL.md` (frontmatter `name`/`description`); no plugin.json entry.
- Tooling: `claude plugin validate <root>` — gingoa passes clean (marketplace needs `metadata.description`
  to avoid a warning).

## Codex — `~/.codex/config.toml` (TOML)
**Empirically verified** with `codex-cli 0.125.0`, 2026-06-26, by running
`CODEX_HOME=<tmp> codex plugin marketplace add <local repo>` and inspecting the written `config.toml`.

- `codex plugin` has exactly: `marketplace {add, upgrade, remove}`. **No `list`, no separate
  `enable`/`install`** — registering the marketplace IS the enablement (unlike CC's `enabledPlugins`).
- `marketplace add <local dir>` writes EXACTLY this table (and nothing else) to `config.toml`:
  ```toml
  [marketplaces.<name>]
  last_updated = "<ISO-8601 Z>"
  source_type = "local"
  source = "<abs path>"
  ```
- Codex reads the SAME shared `.claude-plugin/marketplace.json` at the root (it reported
  `Added marketplace 'gingoa'` from our repo, which ships only `.claude-plugin/marketplace.json`). The
  marketplace root is referenced by path — NOT copied into `CODEX_HOME` (only `config.toml` is written).
- `marketplace add` does **not** validate the plugin manifest at add time: it succeeded against fixtures
  with no plugin.json, with only `.codex-plugin/plugin.json`, and with only `.claude-plugin/plugin.json`.
  So whether Codex requires `.codex-plugin/plugin.json` is a LOAD-time question not observable headlessly.
  Decision: gingoa ships `.codex-plugin/plugin.json` (matches the per-host plugin-manifest design in
  `src/hosts.ts`; harmless + future-proof if Codex reads `.claude-plugin/` instead). doctor checks it.

### Implication for gingoa
- Codex install = upsert the single `[marketplaces.gingoa]` table (managed key = `marketplaces.gingoa`),
  preserving the user's comments/formatting (line-oriented `toml-edit`, smol-toml round-trip fallback).
- Codex uninstall = remove that one table block. doctor = table registered + `source_type="local"` +
  source path valid (has `.claude-plugin/marketplace.json`) + `.codex-plugin/plugin.json` + bundled skill.
