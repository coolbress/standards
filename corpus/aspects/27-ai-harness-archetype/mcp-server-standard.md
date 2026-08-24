---
id: aspect-27-ai-harness-archetype--mcp-server-standard
title: "MCP server build standard (Tools · Resources · Prompts — the frontier-AI standard)"
parent: aspect-27-ai-harness-archetype
kind: reference
evidence_track: census+lit
status: review-needed
last_updated: "2026-06-27"
sources:
  - "https://modelcontextprotocol.io/specification/2025-11-25"
  - "https://modelcontextprotocol.io/specification/2025-11-25/changelog"
  - "https://modelcontextprotocol.io/specification/2025-11-25/server/tools"
  - "https://modelcontextprotocol.io/specification/2025-11-25/server/resources"
  - "https://modelcontextprotocol.io/specification/2025-11-25/server/prompts"
  - "https://modelcontextprotocol.io/specification/2025-11-25/basic/transports"
  - "https://modelcontextprotocol.io/specification/2025-11-25/basic/lifecycle"
  - "https://modelcontextprotocol.io/specification/2025-11-25/basic/security_best_practices"
  - "https://modelcontextprotocol.io/docs/sdk"
  - "https://www.anthropic.com/news/model-context-protocol"
  - "https://www.anthropic.com/engineering/writing-tools-for-agents"
  - "https://www.anthropic.com/engineering/advanced-tool-use"
  - "https://www.anthropic.com/engineering/code-execution-with-mcp"
  - "https://code.claude.com/docs/en/mcp"
  - "https://developers.openai.com/apps-sdk"
  - "https://developers.openai.com/api/docs/guides/function-calling"
  - "https://openai.github.io/openai-agents-python/mcp/"
  - "https://github.com/modelcontextprotocol/inspector"
  - "https://github.com/modelcontextprotocol/typescript-sdk"
  - "https://github.com/modelcontextprotocol/python-sdk"
  - "https://github.com/github/github-mcp-server"
method: "lit — read the MCP spec rev 2025-11-25 IN FULL (overview/security principles, lifecycle, transports, server/{tools,resources,prompts}, security_best_practices, docs/sdk) + the schema TypeScript source for the ToolAnnotations defaults + Anthropic's MCP announcement, 'Writing tools for agents', and 'Code execution with MCP' + the Claude Code MCP docs + OpenAI's function-calling, Apps SDK, Responses-API-MCP, and Agents-SDK-MCP docs + the MCP Inspector. census — harvested the TS-SDK (registerTool/registerResource/registerPrompt + transports) and Python-SDK (FastMCP decorators) API surfaces and the structure of real servers (modelcontextprotocol/servers, github/github-mcp-server). Raw shapes deposited at census-data/frontier-ai-components/mcp/."
---

> **Standard (claim):** A frontier-grade MCP server is a **capability-negotiated JSON-RPC 2.0 service** that
> exposes three primitives — **Tools** (model-controlled functions: JSON-Schema `inputSchema`, optional
> `outputSchema`+`structuredContent`, and safety **annotations** — `readOnlyHint`/`destructiveHint`/
> `idempotentHint`/`openWorldHint`), **Resources** (application-driven, URI-addressed context; RFC-6570
> templates), and **Prompts** (user-controlled templated workflows, surfaced as slash commands) — over a
> **transport** (`stdio` for local, **Streamable HTTP** for remote), built **untrusted-by-default** (explicit
> human consent before every tool call and before exposing data to a server; annotations are untrusted unless
> from a trusted server; local servers sandboxed). Good tools are designed for the **agent-computer interface**
> (few high-impact consolidated tools, token-efficient high-signal responses, error messages that steer the
> model), built **evaluation-first**, and tested with the **MCP Inspector**. OpenAI converges on the same wire
> (its Apps SDK builds ChatGPT apps *as MCP servers*; its Responses/Agents APIs *consume* MCP servers).
> **Evidence:** lit (MCP spec rev 2025-11-25 + Anthropic engineering + OpenAI Apps/Agents docs) · census (TS/
> Python SDK API surface, modelcontextprotocol/servers, github-mcp-server) · **Confidence:** high

This sub-doc is the concrete build spec behind aspect-27's "MCP tool / resource design" and "prompt-injection /
tool-sandbox security" bullets. gingoa scaffolds MCP servers and tools for user projects, so this is the standard
the scaffold must emit to. All facts are pinned to the **2025-11-25** revision (the current spec at capture); the
deltas this doc relies on are itemized in the spec's own **Key Changes** changelog, which establishes — among
others — **JSON Schema 2020-12 as the default dialect**, stderr-for-all-logging, HTTP-403-on-bad-Origin,
input-validation-errors-as-Tool-Execution-Errors, **tool-name guidance**, and experimental **tasks** (durable
requests with polling) / **icons** / richer **elicitation** [lit, spec/changelog].

## Why a single cross-vendor wire exists

Anthropic announced MCP on **2024-11-25** as "a universal, open standard for connecting AI systems with data
sources, replacing fragmented integrations with a single protocol" — solving the **N×M** problem where "every new
data source requires its own custom implementation" [lit, anthropic.com/news]. The spec explicitly frames MCP as
**LSP-for-AI**: "MCP takes some inspiration from the Language Server Protocol… In a similar way, MCP standardizes
how to integrate additional context and tools into the ecosystem of AI applications" [lit, spec]. The payoff is
write-once-consume-everywhere, and it is real across vendors: **OpenAI's Apps SDK builds ChatGPT apps as MCP
servers**, and **OpenAI's Responses API + Agents SDK consume remote MCP servers** [lit, developers.openai.com].
So an MCP server is a genuinely portable artifact — the same server lights up Claude Code, ChatGPT, and any
MCP-speaking host.

The protocol is **JSON-RPC 2.0** over **stateful** connections with **capability negotiation**. Three roles:
**Hosts** (LLM apps that initiate), **Clients** (connectors inside the host, one per server), **Servers** (what
you build) [lit, spec]. Servers offer up to three features — **Resources**, **Prompts**, **Tools**; clients may
offer **Sampling**, **Roots**, **Elicitation** back to the server.

## 1. Tools — the model-controlled surface (the contract that matters most)

Tools are **model-controlled**: "the language model can discover and invoke tools automatically." The host
**SHOULD** keep "a human in the loop with the ability to deny tool invocations" with clear UI + confirmation
prompts [lit, spec/tools]. Discovery is `tools/list` (paginated); invocation is `tools/call`. Declare the
capability `{"tools":{"listChanged":true}}` and emit `notifications/tools/list_changed` when the set changes.

A **Tool definition** is:
- `name` — unique id, 1–128 chars, `[A-Za-z0-9_.-]`, case-sensitive, unique within the server.
- `title` — optional human display name. `description` — what it does (the model reads this to choose).
- `inputSchema` — a **valid JSON Schema object** (not `null`; defaults to draft 2020-12, which rev 2025-11-25
  "establish[ed] … as the default dialect for MCP schema definitions" [lit, spec/changelog]). For no-param tools
  use `{ "type": "object", "additionalProperties": false }`.
- `outputSchema` — optional JSON Schema for structured results. If present, the server **MUST** return
  conforming `structuredContent` and the client **SHOULD** validate it.
- `annotations` — optional behavioral hints (below).

A **tool result** carries unstructured `content[]` (text / image / audio / `resource_link` / embedded
`resource`) and/or a `structuredContent` JSON object (for back-compat, also serialize it into a text block).
Errors split two ways [lit, spec/tools]: **protocol errors** (JSON-RPC, e.g. unknown tool) the model can't fix,
vs **tool execution errors** (`isError: true` in the result) which "contain actionable feedback that language
models can use to self-correct and retry" — clients **SHOULD** feed these back to the model. Rev 2025-11-25
sharpened this split: even **input-validation errors should be returned as Tool Execution Errors rather than
Protocol Errors** specifically "to enable model self-correction" [lit, spec/changelog] — so a server validating a
bad argument returns `isError:true` with a steering message, not a JSON-RPC error.

### 1a. Annotations — idempotency / safety / read-only hints (and the default trap)

The `annotations` object carries four behavioral hints. **Their defaults are non-obvious — get them wrong and a
safe tool reads as dangerous (or vice-versa)** [lit, schema.ts JSDoc, verbatim]:

| hint | meaning | **default** |
|---|---|---|
| `readOnlyHint` | "If true, the tool does not modify its environment." | **`false`** |
| `destructiveHint` | "may perform destructive updates… If false… only additive updates." *(meaningful only when `readOnlyHint == false`)* | **`true`** |
| `idempotentHint` | "calling the tool repeatedly with the same arguments will have no additional effect" *(meaningful only when `readOnlyHint == false`)* | **`false`** |
| `openWorldHint` | "may interact with an 'open world' of external entities" | **`true`** |

So a tool with **no** annotations defaults to *write, destructive, non-idempotent, open-world* — the most
cautious reading. A genuine read-only query (a search, a fetch, a `get_`) **MUST** set `readOnlyHint: true`
explicitly, or hosts will gate it like a deletion. A purely additive create should set `destructiveHint: false`;
a `put`-style upsert should set `idempotentHint: true`.

**Annotations are advisory, not enforcement, and untrusted.** The spec is emphatic: "clients **MUST** consider
tool annotations to be untrusted unless they come from trusted servers" [lit, spec/tools]. They steer host UX
(which tools to auto-approve, which to confirm); they do **not** replace server-side authorization. The server
itself **MUST** validate all inputs, enforce access control, rate-limit, and sanitize outputs regardless of any
hint.

### 1b. Anthropic's own rules for *good* tool design (the ACI)

The spec defines the wire; Anthropic's "Writing tools for agents" post defines the *craft* [lit]. Tools are an
**agent-computer interface (ACI)** — "a new kind of software which reflects a contract between deterministic
systems and non-deterministic agents." Concrete rules:

- **Few high-impact, consolidated tools — not API-endpoint wrappers.** "A common error… is tools that merely wrap
  existing software functionality or API endpoints." Build for *workflows*: a single `schedule_event` over
  `list_users`+`list_events`+`create_event`; `get_customer_context` returning everything relevant at once.
  Agents have scarce context — don't make them stitch many calls.
- **Return high-signal, token-efficient context.** Prioritize "contextual relevance over flexibility"; resolve
  opaque ids ("merely resolving arbitrary alphanumeric UUIDs to more semantically meaningful… language…
  significantly improves Claude's precision") and avoid `uuid`/`256px_image_url`/`mime_type` noise. Offer a
  `response_format` ("concise" vs "detailed") + pagination/filtering/truncation with sensible defaults.
- **Namespace** related tools under a prefix (`asana_projects_search`, `asana_users_search`) so the model picks
  cleanly among dozens.
- **Prompt-engineer the description + schema.** Unambiguous parameter names (`user_id` over `user`); "write
  descriptions as if onboarding a new hire"; "even small refinements to tool descriptions can yield dramatic
  improvements."
- **Error messages that steer the agent** toward the fix (the right format, a narrower search) — not opaque
  tracebacks.
- **Build evaluation-first.** Prototype → generate real tasks → run agents → read transcripts for failure modes →
  let Claude refactor the tools → validate on a held-out set. This mirrors the eval-driven discipline aspect-27
  demands for skills.

Anthropic's "Advanced tool use" post is the platform-side complement these ACI rules now assume — three features
that make a large tool surface tractable: a **Tool Search Tool** (Claude discovers tools on-demand, `defer_loading:
true` keeps them out of context until needed — Anthropic reports an "85% reduction in token usage"), **programmatic
tool calling** (Claude orchestrates tools from a code-execution environment so intermediate results don't all enter
context), and **tool-use examples** (`input_examples` in a tool definition lifting complex-parameter accuracy "from
72% to 90%") [lit, advanced-tool-use]. For a server author the implication is concrete: a well-described,
example-bearing tool is found and called correctly even when its full schema isn't preloaded — the host-side
counterpart to the §1c "defer, don't dump" discipline.

### 1c. Tool sprawl at scale — defer, don't dump

As servers multiply, loading every tool definition up front bloats context: Anthropic measured a 5-server / 58-
tool setup at ~55K tokens *before the conversation starts*, and a workflow that cost ~150K tokens dropping to
~2K (a **98.7%** reduction) by presenting MCP servers as **on-demand code APIs** rather than always-loaded tool
calls [lit, code-execution-with-mcp]. Claude Code ships the host-side version of this — **tool search** is on by
default: only tool names + server `instructions` load at start, full schemas load when the model searches for
them [lit, code.claude.com]. **Server-author implication:** write a tight `instructions` string and per-tool
descriptions (Claude Code truncates each at ~2KB) so the model can find your tools without their full schemas in
context.

## 2. Resources — the application-driven context surface

Resources expose data ("files, database schemas, or application-specific information"), each identified by a
**URI**, and are **application-driven**: "host applications determine how to incorporate context" — a picker,
search, or automatic inclusion [lit, spec/resources]. They are *not* model-invoked like tools; the user or host
selects them. Methods: `resources/list`, `resources/read`, `resources/templates/list`; capability
`{"resources":{"subscribe":?,"listChanged":?}}` (both optional). A resource is `{ uri, name, title?,
description?, mimeType?, size? }`; contents are `text` **or** `blob` (base64).

- **Resource templates** parameterize URIs with **RFC 6570** (`"uriTemplate": "file:///{path}"`); arguments can
  autocomplete via the completion API.
- **Subscriptions** (`resources/subscribe` → `notifications/resources/updated`) and `list_changed` let a server
  push freshness.
- **URI schemes:** HTTPS only when the *client* can fetch it directly; otherwise `file://`, `git://`, or a
  custom RFC-3986 scheme.
- **Annotations** (`audience: ["user"|"assistant"]`, `priority: 0–1`, `lastModified`) help the host filter/rank.

Host consumption is concrete: Claude Code surfaces resources as **`@server:protocol://resource/path` mentions**
(e.g. `@github:issue://123`), fuzzy-searchable in the `@` autocomplete [lit, code.claude.com]. Reach for a
resource when the data is *context to read*; reach for a tool when the model needs to *act*.

## 3. Prompts — the user-controlled workflow surface

Prompts are **user-controlled** templated messages: "exposed from servers to clients with the intention of the
user being able to explicitly select them… Typically… triggered through user-initiated commands… For example, as
slash commands" [lit, spec/prompts]. Methods: `prompts/list`, `prompts/get`; capability
`{"prompts":{"listChanged":true}}`. A prompt is `{ name, title?, description?, arguments: [{ name, description?,
required? }] }`; `prompts/get` returns `{ description, messages: [{ role: "user"|"assistant", content }] }` with
arguments interpolated. Arguments can autocomplete via the completion API.

Host consumption: Claude Code exposes each prompt as a slash command **`/mcp__servername__promptname`**, with
space-separated args [lit, code.claude.com]. Use a prompt for a *reusable, user-initiated* workflow (a code
review, a triage); use a tool for *model-initiated* action.

## 4. Capability negotiation + lifecycle

Every connection opens with a **rigorous lifecycle** [lit, spec/lifecycle]: client sends `initialize`
(`protocolVersion`, its `capabilities`, `clientInfo`) → server replies (`protocolVersion`, its `capabilities`,
`serverInfo`, optional `instructions`) → client sends `notifications/initialized`. **Both parties MUST "only use
capabilities that were successfully negotiated."** Version negotiation: client sends its latest; if the server
supports it the server echoes it, else returns its own latest; the client disconnects if it can't match. A
feature that isn't declared isn't available — so declare exactly the capabilities you implement
(`tools`/`resources`/`prompts` and their `listChanged`/`subscribe` sub-flags), no more.

## 5. Transports — stdio vs Streamable HTTP (and when)

Two standard transports [lit, spec/transports]; "Clients **SHOULD** support stdio whenever possible."

- **stdio** (local): the client launches the server as a subprocess; JSON-RPC over `stdin`/`stdout`, **newline-
  delimited**, messages **MUST NOT contain embedded newlines**. The server **MAY** use `stderr` for **all types
  of logging, not just error messages** (clarified in rev 2025-11-25 [lit, spec/changelog]), and **MUST NOT**
  write anything to `stdout` that is not a valid MCP message (a stray `console.log` to stdout corrupts the
  stream — the #1 stdio bug). **Choose stdio** for a server that runs on the user's machine with local
  filesystem/process access — it's the default and the most secure (access is limited to the launching client).
- **Streamable HTTP** (remote; **replaced** the old HTTP+SSE transport from rev **2024-11-05**): one **MCP
  endpoint** serving POST + GET. The client POSTs a JSON-RPC message; the server replies with `application/json`
  (one object) or opens a `text/event-stream` **SSE** stream; the client may GET to open a server→client SSE
  stream. Sessions use an `Mcp-Session-Id` header (cryptographically-secure, visible-ASCII); all subsequent HTTP
  requests carry `MCP-Protocol-Version`. **Choose Streamable HTTP** for a cloud/multi-client server, OAuth, or
  push. Its **security MUSTs**: validate the `Origin` header (rev 2025-11-25 clarified the server "must respond
  with **HTTP 403 Forbidden for invalid Origin headers**" — the DNS-rebinding defense [lit, spec/changelog]), bind
  to `127.0.0.1` when local, and implement auth — without these "attackers could use DNS rebinding to interact
  with local MCP servers from remote websites."

(SSE-only and WebSocket exist as host extensions, but SSE is **deprecated** in favor of Streamable HTTP [lit,
code.claude.com].)

## 6. Security & consent model — first-class, not an afterthought

The spec's top-level principles are non-negotiable [lit, spec — verbatim]:

1. **User Consent and Control** — "Users must explicitly consent to and understand all data access and
   operations… retain control over what data is shared and what actions are taken."
2. **Data Privacy** — "Hosts must obtain explicit user consent before exposing user data to servers" and "must
   not transmit resource data elsewhere without user consent."
3. **Tool Safety** — "Tools represent arbitrary code execution and must be treated with appropriate caution…
   descriptions of tool behavior such as annotations should be considered untrusted, unless obtained from a
   trusted server. Hosts must obtain explicit user consent before invoking any tool."
4. **LLM Sampling Controls** — users approve sampling; the protocol limits server visibility into prompts.

These are *host* obligations the protocol can't enforce — but a **server** is the other half of the trust
boundary and must be built defensively. The **Security Best Practices** page names the attack classes a server
**MUST** defend [lit, spec/security_best_practices]:

- **Token passthrough** — "MCP servers **MUST NOT** accept any tokens that were not explicitly issued for the MCP
  server." Validate the token audience; never forward a client's upstream token downstream.
- **Confused deputy** — an OAuth-proxy server **MUST** implement **per-client consent** (registered `client_id`
  registry, checked *before* forwarding to a third-party authz) + exact `redirect_uri` matching + single-use
  `state`.
- **Session hijacking** — "MCP Servers **MUST NOT** use sessions for authentication"; use secure, non-
  deterministic session IDs (UUIDs from a CSPRNG) and bind them to the user (`<user_id>:<session_id>`).
- **SSRF** — a server (or client) fetching URLs **SHOULD** enforce HTTPS and block private IP ranges
  (`169.254.169.254`, `10/8`, `127/8`, …).
- **Local server compromise / sandboxing** — local servers are arbitrary code execution. A one-click installer
  **MUST** show the exact command and require explicit consent; hosts **SHOULD** sandbox spawned servers
  (containers/chroot, restricted fs+network, least privilege); local servers **SHOULD** use `stdio` to limit
  access to just the launching client, and restrict any HTTP transport (auth token or unix-domain socket).
- **Scope minimization** — least-privilege OAuth scopes; no wildcard/omnibus scopes; incremental elevation.

Per-feature server duties: validate every tool input + access-control + rate-limit + sanitize output (tools);
validate all resource URIs + access controls (resources); validate prompt inputs against injection (prompts).

## 7. SDK conventions — build with the high-level API

Ten **official SDKs** ship, tiered [lit, docs/sdk]: **Tier 1** TypeScript · Python · C# · Go; **Tier 2** Java ·
Rust; **Tier 3** Swift · Ruby · PHP · Kotlin. All "support creating MCP servers that expose tools, resources, and
prompts," clients, and local+remote transports. Prefer each SDK's **high-level** API — it derives the JSON-Schema
+ wire plumbing from your types so you write a function, not a protocol.

- **TypeScript** — `new McpServer({name,version})` then `registerTool(name, { title, description, inputSchema
  (zod shape), outputSchema?, annotations? }, handler)` (handler returns `{ content:[…], structuredContent? }`);
  `registerResource(name, new ResourceTemplate("scheme://{p}", {list}), {title,mimeType}, readCb)`;
  `registerPrompt(name, { argsSchema (zod, `completable()` for autocomplete) }, cb)`. Connect a transport:
  `server.connect(new StdioServerTransport())` or `new StreamableHTTPServerTransport({ sessionIdGenerator })`
  [census, ts-sdk docs/server.md].
- **Python (FastMCP)** — `mcp = FastMCP("name")` then decorate: `@mcp.tool()` (infers `inputSchema` from type
  hints + docstring; return a Pydantic model → `outputSchema`+`structuredContent`), `@mcp.resource("scheme://
  {p}")`, `@mcp.prompt()`. Run: `mcp.run()` / `mcp.run(transport="stdio")` / `mcp.run(transport="streamable-
  http")`; iterate with `uv run mcp dev server.py` [census, python-sdk README].

**Packaging** follows the language's norm so a host can launch the server with one command: a `bin` in
`package.json` runnable as **`npx -y <pkg>`** (TS) or a console-script runnable as **`uvx <pkg>`** (Python), or a
container (Go's `github-mcp-server` ships `ghcr.io/github/github-mcp-server` + a `stdio` subcommand). Real servers
group a large surface into **toolsets** with a **read-only mode** (github-mcp-server: `--toolsets`
repos/issues/pull_requests/actions/code_security; `--read-only` skips write tools) [census].

**Host registration** is config, not code. Claude Code: `claude mcp add --transport {stdio|http|sse} <name> …`
across three scopes — **local** (`~/.claude.json`, default), **project** (`.mcp.json`, committed + team-shared,
approval-gated), **user** (all projects) — or a plugin bundles a server in its `.mcp.json`/`plugin.json`
(`${CLAUDE_PLUGIN_ROOT}`) [lit, code.claude.com]. The `.mcp.json` shape is the cross-host de-facto:
`{"mcpServers":{"<name>":{"command":"…","args":[…],"env":{…}}}}` (or `{"type":"http","url":…,"headers":…}`).

## 8. Testing an MCP server

- **MCP Inspector** — the official interactive test/debug tool: `npx @modelcontextprotocol/inspector <command>`
  (e.g. `… node build/index.js`), UI at `localhost:6274` (token-auth, localhost-bound). Browse + call tools with
  form inputs, read resources, get prompts, watch notifications; a **CLI mode** drives it from scripts/CI with
  JSON output [lit, inspector repo]. This is the manual smoke test before wiring a server into a host.
- **In-memory transport** — the SDKs ship an in-memory client↔server pair so unit tests exercise `tools/call` /
  `resources/read` / `prompts/get` without a subprocess. Assert schema-conformant results + `isError` paths
  + that `outputSchema` validates the `structuredContent`.
- **Eval the tools** (§1b) — beyond unit tests, run an agent through representative tasks and read the transcripts;
  this is what catches an ambiguous description or a token-bloated response.

## 9. OpenAI's framing — same wire, two directions

OpenAI both **builds** and **consumes** MCP, which is strong evidence the standard is genuinely cross-vendor:

- **Apps SDK = build a ChatGPT app *as an MCP server*** [lit, developers.openai.com/apps-sdk]. The app's backend
  "functions as an MCP server that exposes tools." A tool returns `structuredContent`, and `_meta["openai/
  outputTemplate"]` links it to a **widget** registered as an MCP **resource** (`ui://` scheme, `text/
  html+skybridge` mimeType) — extra `_meta` keys `openai/widgetAccessible`, `openai/toolInvocation/invoking`.
  This is OpenAI's official "how to build an MCP server" and it layers UI on the *same* Tools/Resources model.
- **Responses API consumes a remote MCP server** [lit] as a tool: `{ "type":"mcp", "server_label",
  "server_url", "authorization", "require_approval":"never|always|{never:{tool_names:[…]}}", "allowed_tools":[…]
  }`; an approval-required call emits `mcp_approval_request` answered by `mcp_approval_response`. Note
  `require_approval` is OpenAI's host-side encoding of the **explicit-consent-before-tool-call** principle.
- **Agents SDK consumes MCP** via `MCPServerStdio` / `MCPServerStreamableHttp` / `MCPServerSse` / `HostedMCPTool`,
  passed as `Agent(mcp_servers=[…])`, with static/dynamic **tool filtering** and `cache_tools_list=True` [lit].

**Schema contrast (MCP vs OpenAI function calling).** OpenAI's native function tool is `{ "type":"function",
"name", "description", "parameters" (JSON Schema), "strict":true }` [lit, function-calling]. MCP's Tool is the
superset relevant to a server author: it adds `title`, `outputSchema`, `annotations` (the safety hints), `_meta`,
and ships over a **capability-negotiated, `listChanged`-aware** `tools/list` rather than inline in one request.
For gingoa, the takeaway: **build to the MCP Tool shape** (it's the portable, richer contract); the OpenAI
function shape is what a host *projects MCP into* when it calls the model, not what you author.

## Anti-patterns (each cited)

- **Writing to `stdout` on a stdio server** (a logging call, a banner) — corrupts the JSON-RPC stream; log to
  `stderr` only [lit, spec/transports].
- **Omitting `readOnlyHint` on a read-only tool** — it defaults to *write/destructive*, so hosts gate a harmless
  query like a deletion [lit, schema.ts].
- **Trusting annotations / descriptions as enforcement** — they're untrusted hints; the server still MUST
  authorize + validate [lit, spec].
- **One tool per API endpoint** — "tools that merely wrap existing… API endpoints"; build workflow tools instead
  [lit, writing-tools].
- **Dumping low-signal context** (raw UUIDs, `mime_type`, unpaginated blobs) — wastes the agent's scarce context;
  return high-signal, resolved, paginated results [lit, writing-tools].
- **Loading every tool up front at scale** — 58 tools ≈ 55K tokens before the first turn; lean on tight
  `instructions` + host tool-search/deferral [lit, code-execution-with-mcp].
- **Token passthrough / session-as-auth / unvalidated `Origin`** — the named spec attack classes [lit,
  security_best_practices].
- **Skipping consent on a one-click local install** — must show the exact command + require approval; sandbox the
  process [lit, security_best_practices].
- **Resource-vs-tool confusion** — using a model-callable *tool* for static read-context (should be a *resource*),
  or a *resource* for an action (should be a *tool*); and using a *tool* where a user-initiated *prompt* fits.

## How gingoa should scaffold an MCP server

gingoa scaffolds MCP servers/tools for user projects. The scaffold MUST emit, to match this standard:

1. **A high-level SDK server** in the project's plurality language — **TypeScript `McpServer`** (gingoa's TS/Node
   plurality) or **Python `FastMCP`** — with a `bin`/console-script runnable as **`npx -y <pkg>`** / **`uvx
   <pkg>`**, plus a `.mcp.json` snippet (`{"mcpServers":{"<name>":{"command":…,"args":[…]}}}`) for one-command
   host registration. **stdio is the default transport**; offer **Streamable HTTP** as the opt-in for a remote/
   multi-client server (and when chosen, bake in `Origin` validation + `127.0.0.1` binding + a session id).
2. **Tools authored to the ACI bar** — `registerTool`/`@mcp.tool()` with a clear `name`, a *new-hire-grade*
   `description`, an unambiguous JSON-Schema `inputSchema`, and an **`outputSchema`+`structuredContent`** when the
   result is structured. Emit **explicit annotations** — the scaffold MUST set `readOnlyHint: true` on generated
   read/`get_`/`search_` tools and surface `destructiveHint`/`idempotentHint` as prompts for write tools (never
   rely on the dangerous defaults). Default to **few consolidated workflow tools**, **namespaced** under the
   server name, returning **high-signal, paginated** responses with **steering error messages** (`isError:true`).
3. **Resources + prompts only when they fit** — a `registerResource`/`@mcp.resource("scheme://{id}")` for
   read-context (RFC-6570 template + `list`), a `registerPrompt`/`@mcp.prompt()` for a user-initiated workflow
   (surfaced as `/mcp__server__prompt`). Declare exactly the capabilities implemented (`tools`/`resources`/
   `prompts` + their `listChanged`/`subscribe`).
4. **Security-by-default** — input validation + access control + rate-limit + output sanitization in every tool
   handler; never accept a token not issued to the server (no passthrough); non-deterministic session ids bound
   to the user for any HTTP transport; a `stderr`-only logging helper so the scaffold can't corrupt stdout. For a
   write/destructive tool, scaffold a server-side confirmation/consent affordance, not just the annotation.
5. **An eval + Inspector test harness** — an in-memory-transport unit test that asserts each tool's schema-
   conformant result + `isError` path + `outputSchema` validation; **≥3 eval scenarios** (query → expected tool +
   behavior) so the user inherits evaluation-driven tool development; and a one-line `npx @modelcontextprotocol/
   inspector <cmd>` smoke-test note.
6. **A schema/manifest validation gate** — mirror aspect-27's "presence ≠ adequacy" rule: a vitest test asserting
   the server's `tools/list` is well-formed (each `inputSchema` is a valid JSON Schema object, names match
   `[A-Za-z0-9_.-]{1,128}`, read-only tools carry `readOnlyHint`), and that the emitted `.mcp.json` parses. A
   scaffolded server that doesn't pass the Inspector + the test is a bug, not a deliverable.

This makes the gingoa MCP scaffold emit the **portable, cross-host artifact** (one server → Claude Code, ChatGPT
via the Apps/Responses/Agents path, any MCP host) at the Anthropic-tool-design quality bar, with the spec's
untrusted-by-default security model and eval discipline built in — gated like every other shipped guardrail.

## Sources

- MCP specification — overview + security/trust principles (rev 2025-11-25) — https://modelcontextprotocol.io/specification/2025-11-25
- MCP — Key Changes / changelog (rev 2025-11-25 deltas: stderr-for-all-logging, HTTP-403-on-bad-Origin, input-validation→Tool-Execution-Errors, JSON-Schema-2020-12 default, tool-name guidance, tasks/icons/elicitation) — https://modelcontextprotocol.io/specification/2025-11-25/changelog
- MCP — Tools — https://modelcontextprotocol.io/specification/2025-11-25/server/tools
- MCP — Resources — https://modelcontextprotocol.io/specification/2025-11-25/server/resources
- MCP — Prompts — https://modelcontextprotocol.io/specification/2025-11-25/server/prompts
- MCP — Transports (stdio + Streamable HTTP) — https://modelcontextprotocol.io/specification/2025-11-25/basic/transports
- MCP — Lifecycle + capability negotiation — https://modelcontextprotocol.io/specification/2025-11-25/basic/lifecycle
- MCP — Security Best Practices — https://modelcontextprotocol.io/specification/2025-11-25/basic/security_best_practices
- MCP — ToolAnnotations defaults (schema TypeScript source) — https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/schema/2025-11-25/schema.ts
- MCP — official SDKs (tiers) — https://modelcontextprotocol.io/docs/sdk
- MCP Inspector — https://github.com/modelcontextprotocol/inspector
- MCP TypeScript SDK (McpServer high-level API) — https://github.com/modelcontextprotocol/typescript-sdk
- MCP Python SDK (FastMCP) — https://github.com/modelcontextprotocol/python-sdk
- MCP reference servers — https://github.com/modelcontextprotocol/servers
- GitHub MCP server (Go; toolsets + read-only) — https://github.com/github/github-mcp-server
- Anthropic — Introducing the Model Context Protocol — https://www.anthropic.com/news/model-context-protocol
- Anthropic — Writing effective tools for agents (the ACI) — https://www.anthropic.com/engineering/writing-tools-for-agents
- Anthropic — Introducing advanced tool use (Tool Search Tool + `defer_loading`; programmatic tool calling; tool-use `input_examples`) — https://www.anthropic.com/engineering/advanced-tool-use
- Anthropic — Code execution with MCP (tool-loading at scale) — https://www.anthropic.com/engineering/code-execution-with-mcp
- Claude Code — Connect Claude Code to tools via MCP — https://code.claude.com/docs/en/mcp
- OpenAI — Apps SDK (build a ChatGPT app as an MCP server) — https://developers.openai.com/apps-sdk
- OpenAI — Function calling (schema contrast) — https://developers.openai.com/api/docs/guides/function-calling
- OpenAI Agents SDK — MCP — https://openai.github.io/openai-agents-python/mcp/
- Raw harvested shapes + OSS structure census — `census-data/frontier-ai-components/mcp/samples.md`
</content>
