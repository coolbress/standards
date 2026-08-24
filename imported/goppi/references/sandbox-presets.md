# Sandbox presets — Governed mode & untrusted input (Layer 2, design §4.3)

Two triggers, one mechanism. Turn the sandbox on when **either** holds:

1. **Governed mode** — the task touches a Governed trigger (GOPPI.md clause 3).
2. **Untrusted input** — the session processes web pages, external documents, or
   third-party code, *regardless of mode*. The 24/25 credential-theft evidence
   attaches to the input's nature, not the task's ceremony (design §3).

The host sandbox is session-level, OS-enforced (macOS Seatbelt / Linux+WSL2
bubblewrap), and applies to shell commands and their children. It is the real
isolation layer; permission rules are friction, contract text is advice (§4.3).

## Preset G — Governed

Merge into the project's `.claude/settings.local.json` (or apply via the host's
sandbox panel). Key intent: **credentials never enter the sandbox**, network is
allowlist-by-approval, and if the sandbox cannot start we stop rather than
silently fall back (fail-closed: this is a security control).

```jsonc
{
  "sandbox": {
    "enabled": true,
    "failIfUnavailable": true,          // no silent unsandboxed fallback
    "autoAllowBashIfSandboxed": true,   // friction goes down inside the fence
    "filesystem": {
      // default read is the WHOLE filesystem and the host ships NO built-in
      // credential deny list — so goppi declares one explicitly:
      "denyRead": [
        "~/.ssh", "~/.gnupg", "~/.aws", "~/.kube", "~/.docker/config.json",
        "~/.netrc", "~/.npmrc", "~/.pypirc", "~/.config/gh",
        "~/.claude/.credentials.json",
        // workspace secrets — parity with the Codex profile's in-workspace
        // denies (.codex/config.toml): the workspace being writable must not
        // make its OWN secrets readable. OS-enforced ONLY while this sandbox
        // is on (§4.3 conditional); off-sandbox, the same paths are covered
        // only by Read()-rule + hook friction, which Bash subprocesses bypass.
        "./.env", "./.env.*", "**/*.pem", "**/*.key",
        "**/id_rsa", "**/id_ed25519", "./secrets/**", "./.git/config"
      ]
    },
    "network": {
      // intentionally empty allowlist: every new domain prompts the user once
      // per session. Broad domains (e.g. github.com) are exfil surface — add
      // the narrowest host that works, per task, when prompted.
      "allowedDomains": []
    },
    "credentials": {
      "envVars": [
        { "name": "AWS_ACCESS_KEY_ID", "mode": "deny" },
        { "name": "AWS_SECRET_ACCESS_KEY", "mode": "deny" },
        { "name": "AWS_SESSION_TOKEN", "mode": "deny" },
        { "name": "GITHUB_TOKEN", "mode": "deny" },
        { "name": "GH_TOKEN", "mode": "deny" },
        { "name": "ANTHROPIC_API_KEY", "mode": "deny" },
        { "name": "OPENAI_API_KEY", "mode": "deny" },
        { "name": "NPM_TOKEN", "mode": "deny" }
      ]
    }
  }
}
```

## Preset U — Untrusted input

Preset G, plus two hardenings for sessions that chew on external content:

```jsonc
{
  "sandbox": {
    /* ...everything from Preset G, and: */
    "allowUnsandboxedCommands": false   // strict mode: no unsandboxed retry escape hatch
  }
}
```

- Also export `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB=1` for the session — strips
  Anthropic + cloud credentials from **all** subprocesses, sandboxed or not.
- If a task genuinely needs a credential (e.g. `gh` for a PR), prefer doing that
  step in a separate non-untrusted session, or use `credentials.envVars` `mask`
  mode (v2.1.199+, requires `network.tlsTerminate`) so the real value only
  exists in the proxy, never inside the sandbox.

## Codex — the equivalent is a **permission profile**, not `sandbox_mode`

On Codex the credential-read boundary is NOT `sandbox_mode`: legacy
`sandbox_mode = "workspace-write"` grants **whole-filesystem read** (`:root = read`)
and only scopes writes (verified in openai/codex `rust-v0.144.0`). The real boundary
is a **permission profile** in `<repo>/.codex/config.toml` — goppi ships
[`goppi-guarded`](../.codex/config.toml):

- `filesystem.":root" = "deny"` + `":minimal" = "read"` → no reads of `~/.ssh`,
  `~/.aws`, `~/.config/gh`, etc. (the Codex analogue of Preset G's `denyRead`);
- in-workspace `.env`/`*.pem`/`*.key`/`secrets/**` denies (`deny` beats `write`);
- `network.enabled = false` (allowlist-by-approval, matching Preset G).

Requires **Codex ≥ 0.138** and a **trusted** project folder — an untrusted `.codex/`
layer is ignored entirely, so the profile silently does nothing until the user trusts
it (`hosts/goppi-doctor.sh` flags presence; for un-bypassable enforcement use a
managed `requirements.toml`). It does **not** compose with `sandbox_mode` — ship one
or the other. Deny-read globs expand up to `glob_scan_max_depth`; deeply-nested
secrets need a higher depth or exact-path denies.

**Why the two hosts differ here (intentional, not a gap):** Codex keeps the
credential boundary in this committed, trust-gated profile file because it has no
mid-session sandbox toggle; the Claude boundary above is the *session* sandbox, which
goppi keeps **conditional** (§4.3 — activated for Governed / untrusted sessions, not
force-committed always-on). Both are the same OS-enforced deny; only their home
differs. Full parity table: `hosts/codex/README.md` → "Host parity".

## The destructive-accident ask set (both hosts)

Beyond G7's external/irreversible list, both hosts carry a second `ask`/`prompt`
set aimed at **local, silent, unrecoverable loss** — the class where the damage is
done before anyone sees a diff.

**Threat model, stated so nobody upgrades it in their head** (claudeck v1,
`harness-notes.md:383`, ported unchanged): this is a **backstop against a plausible
accident, not adversarial coverage**. A prefix/glob match is trivially evaded —
flag permutations, absolute paths, `$VAR` indirection, shell chaining. The real
isolation is the sandbox above. What this set buys is one confirmation prompt
between a mis-aimed command and an unrecoverable outcome.

**`ask`, never `deny`** — and the reason is mechanical, not stylistic: every verb
here has ordinary legitimate uses, and a deny rule *cannot carry an exception*
(a broad `Bash(git clean *)` deny blocks every matching call, including one a
narrower allow rule also matches — [lit] permissions doc, "Manage permissions").
So a deny would convert routine work into a hard block, which is the false-block
§11 forbids. A user who wants deny promotes it locally; the shipped default asks.

| Loss | Claude `permissions.ask` | Codex `prefix_rule` (prompt) |
|---|---|---|
| remote history rewritten | `Bash(git push *--force*)` · `Bash(git push *--mirror*)` | `["git","push"]` (whole verb — flag position is not fixed) |
| untracked files gone | `Bash(git clean *)` † | `["git","clean"]` † |
| unmerged branch gone | `Bash(git branch -D*)` | `["git","branch","-D"]` |
| stash gone | `Bash(git stash drop*)` · `Bash(git stash clear*)` | `["git","stash","drop"]` · `["git","stash","clear"]` |
| recovery path gone | `Bash(git reflog expire*)` · `Bash(git gc *--prune*)` | `["git","reflog","expire"]` · `["git","gc"]` |
| files deleted in bulk | `Bash(find * -delete*)` · `Bash(find * -exec rm*)` | **not expressible — see below** |
| file contents destroyed | `Bash(truncate *)` · `Bash(shred *)` · `Bash(dd *of=*)` | `["truncate"]` · `["shred"]` · `["dd"]` |
| process killed uncleanly | `Bash(kill -9*)` · `Bash(pkill -9*)` | `["kill","-9"]` · `["pkill","-9"]` |

**† `git clean` is deliberately broader than the destructive flags.** The ported
row was `git clean -fd*`; both hosts prompt on the **whole verb** instead, so
`git clean -n` and `-i` — the read-only previews — prompt too. That is a widening
past the ported set, disclosed here rather than left for someone to find: matching
flag spellings (`-fd`, `-df`, `-fdx`, `--force`) exhaustively is the arms race the
threat-model note above says this set does not fight, and one extra prompt on a
command nobody runs in a loop is the cheaper error. It is an `ask`, not a block.

**The one real asymmetry, named rather than papered over**: Codex's engine matches
**argv prefixes only**, and `find`'s destructive flag sits at the *end* of argv
after a variable-length path list, so no prefix rule can reach `find … -delete` or
`find … -exec rm`. Writing `["find"]` instead would prompt on every read-only
`find` — a false-ask on one of the most-used commands there is, worse than the gap.
So Codex is **uncovered** for that row; it is printed in `hosts/codex/smoke-test.sh`'s
known-uncovered list rather than asserted. Elsewhere Codex is *coarser* (whole verb)
where Claude can target the exact flag — coarser, never narrower.

**Two Claude-side notes worth keeping** ([lit] permissions doc, 2026-07-26):
`find` with `-delete`/`-exec` already always prompts and cannot be auto-approved by
a `Bash(find *)` prefix rule, so those two rows are belt-and-braces; and rules
evaluate **deny → ask → allow, with the first match winning and specificity never
reordering them**, so any `ask` row here keeps prompting even if a project later
allowlists the same verb.

**What the two push rows are, and are not** (corrected in review, 2026-07-26):
under the set as shipped they are **inert**, because `Bash(git push*)` is already
in `ask` and matches everything they match — and the precedence note above means
that blanket row, on its own, already survives an allowlist. So they buy nothing
against `allow`. What they do buy is narrower and worth one line: they survive the
**blanket row being removed or narrowed**, which is the realistic edit — someone
silencing a noisy prompt on every ordinary `git push` has no reason to think about
force-push, and these rows mean they keep the protection they were not thinking
about. Stated because the first draft of this file claimed the allowlist property
for them, which is false.

## Honest limits (do not claim more than this buys)

- Sandbox covers **shell commands only**. The host's file tools (read/edit) are
  governed by permission rules, not the sandbox — the G7 `Read(...)` deny set
  in `settings.json` stays load-bearing.
- The converse also binds: **`settings.json` `Read(...)` denies govern the file
  tools only — they do not reach Bash subprocesses** (`cat ./.env` passes every
  permission rule). On Claude, Bash-level blocking of secret reads is
  OS-enforced **only while this sandbox is on**; off-sandbox, the PreToolUse
  secret-path friction (hooks/README.md) is pattern-level friction, not a
  boundary. Codex differs: its committed profile denies are always-on once the
  folder is trusted.
- The network proxy matches the client-supplied hostname and does **not**
  inspect TLS by default → domain-fronting exfiltration remains possible
  against allowed domains. Mitigation: keep `allowedDomains` empty/narrow.
- An unsandboxed-retry approval (`dangerouslyDisableSandbox`) goes through the
  regular permission prompt — in Governed sessions, treat that prompt itself as
  a Governed trigger and decline unless the command was reviewed.
- Git worktrees share `.git` writable (except `hooks/`, `config`).

## Evidence
- [lit] https://code.claude.com/docs/en/sandboxing (2026-07-14) — schema (`sandbox.enabled/failIfUnavailable/allowUnsandboxedCommands/filesystem/network/credentials`), default read = entire filesystem, "There is no built-in credential deny list", no pre-allowed domains, per-session domain approval, TLS-not-terminated caveat, worktree note, Seatbelt/bubblewrap platforms, `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB`.
- [lit] https://code.claude.com/docs/en/settings (2026-07-14) — full `sandbox` key table incl. `credentials.envVars` deny/mask semantics (mask v2.1.199+, needs `tlsTerminate`), `failIfUnavailable` fallback behavior.
- [lit] https://code.claude.com/docs/en/permissions (2026-07-14) — Bash patterns are fragile/bypassable; OS-level enforcement is the sandbox; Read/Edit deny rules don't reach arbitrary subprocesses (→ sandbox `denyRead` complements them).
- [lit] https://www.anthropic.com/engineering/how-we-contain-claude (2026-07-14) — "If credentials never enter the sandbox, they can't be exfiltrated"; allowlists are capability grants; model-layer-only defense lost credentials 24/25 (design §3) → untrusted-input trigger is input-property-based.
- [inferred] The specific credential path/env-var lists — union of common credential locations on this machine's ecosystem (git/gh/aws/npm/pypi/k8s/docker/LLM keys). Eval target: S4 checks for both misses and false friction.
- [goppi-internal] The workspace `denyRead` patterns (v0.9.1, #48 P0-1a) — 1:1 parity with the in-workspace deny list already shipped in `.codex/config.toml`; the gap (Claude preset lacked them while the Codex profile had them, so `cat ./.env` passed every Claude layer) was reproduced by the external Codex critique, 2026-07-24. Live Bash-block verification is per-deployment (sandbox-on session) and stays BLOCKED from off-sandbox runs.

## Expiry conditions
- Host ships a built-in credential deny list or named sandbox presets → delete the overlapping lists here, keep only deltas.
- Host extends sandbox coverage to its file tools → drop the "permission rules stay load-bearing" caveat and revisit the G7 deny set.
- Host isolates untrusted web/file content natively end-to-end (beyond the current isolated WebFetch context) → Preset U shrinks to Preset G.
