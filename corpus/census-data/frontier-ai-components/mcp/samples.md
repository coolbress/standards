# MCP raw samples (verbatim shapes + SDK surface + OSS census)

Captured 2026-06-27 from the sources in `README.md`. Append-only.

---

## 1. Tool definition + annotations (spec rev 2025-11-25)

`tools/list` entry (from spec `server/tools`):

```json
{
  "name": "get_weather",
  "title": "Weather Information Provider",
  "description": "Get current weather information for a location",
  "inputSchema": {
    "type": "object",
    "properties": { "location": { "type": "string", "description": "City name or zip code" } },
    "required": ["location"]
  },
  "outputSchema": { "type": "object", "properties": { "temperature": { "type": "number" } }, "required": ["temperature"] },
  "annotations": { "title": "...", "readOnlyHint": false, "destructiveHint": true, "idempotentHint": false, "openWorldHint": true }
}
```

`tools/call` result — unstructured `content[]` + optional `structuredContent` (must conform to `outputSchema`);
`isError: true` carries a *tool execution error* the model can self-correct from.

**ToolAnnotations defaults — verbatim from `schema/2025-11-25/schema.ts` JSDoc:**

| hint | JSDoc | default |
|---|---|---|
| `readOnlyHint` | "If true, the tool does not modify its environment." | `false` |
| `destructiveHint` | "If true, the tool may perform destructive updates… If false, the tool performs only additive updates. (meaningful only when `readOnlyHint == false`)" | `true` |
| `idempotentHint` | "If true, calling the tool repeatedly with the same arguments will have no additional effect… (meaningful only when `readOnlyHint == false`)" | `false` |
| `openWorldHint` | "If true, this tool may interact with an 'open world' of external entities. If false, the tool's domain of interaction is closed." | `true` |

Spec WARNING (verbatim): "For trust & safety and security, clients **MUST** consider tool annotations to be
untrusted unless they come from trusted servers." Tools are **model-controlled**; "there **SHOULD** always be a
human in the loop with the ability to deny tool invocations." Tool names: 1–128 chars, `[A-Za-z0-9_.-]`,
case-sensitive, unique per server. `inputSchema` MUST be a valid JSON Schema object (defaults to 2020-12).

---

## 2. Resource + template + prompt (spec rev 2025-11-25)

Resource (from `server/resources`): `{ uri, name, title?, description?, mimeType?, size? }`; contents are `text`
OR `blob` (base64). Resources are **application-driven** (host decides how to surface — picker, search, auto).
Resource template: `{ "uriTemplate": "file:///{path}", "name", ... }` — RFC 6570. Capability:
`{ "resources": { "subscribe": true, "listChanged": true } }` (both optional). Methods: `resources/list`,
`resources/read`, `resources/templates/list`, `resources/subscribe`, `notifications/resources/updated`,
`notifications/resources/list_changed`. URI schemes: HTTPS (client fetches directly), `file://`, `git://`,
custom. Annotations on resources/content: `audience` (`["user","assistant"]`), `priority` (0–1), `lastModified`.

Prompt (from `server/prompts`): `{ name, title?, description?, arguments: [{ name, description?, required? }] }`.
Prompts are **user-controlled** — "exposed from servers to clients with the intention of the user being able to
explicitly select them… Typically… triggered through user-initiated commands… For example, as slash commands."
`prompts/get` returns `{ description, messages: [{ role: "user"|"assistant", content: {type, ...} }] }`.

---

## 3. Lifecycle + transports (spec rev 2025-11-25)

Lifecycle: `initialize` (client→server: `protocolVersion`, `capabilities`, `clientInfo`) → `initialize` result
(`protocolVersion`, server `capabilities`, `serverInfo`, optional `instructions`) → `notifications/initialized`.
Capability negotiation: both sides declare capabilities; "Both parties MUST… Only use capabilities that were
successfully negotiated." Version negotiation: client sends latest; server echoes if supported, else returns its
latest; client disconnects if unsupported.

**stdio** (verbatim MUST/MUST NOT): messages newline-delimited, **MUST NOT** contain embedded newlines; server
**MAY** write logs to `stderr`; server **MUST NOT** write anything to `stdout` that is not a valid MCP message;
client **MUST NOT** write anything to `stdin` that is not a valid MCP message. "Clients **SHOULD** support stdio
whenever possible."

**Streamable HTTP** (replaced HTTP+SSE from rev **2024-11-05**): single MCP endpoint, POST + GET; POST a JSON-RPC
message, server returns `application/json` (one object) OR `text/event-stream` (SSE stream); GET opens a
server→client SSE stream; `Mcp-Session-Id` header for sessions (cryptographically-secure, visible ASCII);
`MCP-Protocol-Version` header on all subsequent HTTP requests. Security MUST/SHOULD: validate `Origin` (403 on
invalid — DNS-rebinding defense); bind to `127.0.0.1` when local; implement auth.

---

## 4. Security best-practices attack classes (spec `basic/security_best_practices`)

- **Confused deputy** — proxy + static client_id + dynamic registration + consent cookie → MCP proxy servers
  **MUST** implement per-client consent before forwarding to third-party authz.
- **Token passthrough** — "MCP servers **MUST NOT** accept any tokens that were not explicitly issued for the MCP
  server."
- **SSRF** — clients fetching OAuth metadata URLs **SHOULD** enforce HTTPS + block private IP ranges
  (`169.254.169.254`, `10/8`, etc.).
- **Session hijacking** — "MCP Servers **MUST NOT** use sessions for authentication"; use secure non-deterministic
  session IDs; bind session to user (`<user_id>:<session_id>`).
- **Local server compromise** — one-click local-server config **MUST** show the exact command + require explicit
  consent; clients **SHOULD** sandbox spawned servers (containers/chroot, restricted fs/network); local servers
  **SHOULD** use `stdio` to limit access.
- **Scope minimization** — least-privilege scopes; no wildcard/omnibus scopes.

---

## 5. Official SDKs (docs/sdk, tiered)

Tier 1: TypeScript, Python, C#, Go. Tier 2: Java, Rust. Tier 3: Swift, Ruby, PHP, Kotlin.
All "support creating MCP servers that expose tools, resources, and prompts" + clients + local/remote transports.

### TS-SDK high-level API (`McpServer`, from docs/server.md — verbatim)

```typescript
const server = new McpServer({ name: 'my-server', version: '1.0.0' });

server.registerTool('calculate-bmi',
  { title: 'BMI Calculator', description: 'Calculate Body Mass Index',
    inputSchema: z.object({ weightKg: z.number(), heightM: z.number() }),
    outputSchema: z.object({ bmi: z.number() }) },
  async ({ weightKg, heightM }) => {
    const output = { bmi: weightKg / (heightM * heightM) };
    return { content: [{ type: 'text', text: JSON.stringify(output) }], structuredContent: output };
  });

// annotations example
{ title: 'Delete File', description: 'Delete a file from the project',
  inputSchema: z.object({ path: z.string() }),
  annotations: { destructiveHint: true, idempotentHint: true } }

server.registerResource('user-profile',
  new ResourceTemplate('user://{userId}/profile', { list: async () => ({ resources: [...] }) }),
  { title: 'User Profile', description: 'User profile data', mimeType: 'application/json' },
  async (uri, { userId }) => ({ contents: [{ uri: uri.href, text: JSON.stringify({ userId }) }] }));

server.registerPrompt('review-code',
  { title: 'Code Review', description: 'Review code for best practices',
    argsSchema: z.object({ language: completable(z.string(), v => [...].filter(l => l.startsWith(v))) }) },
  ({ language }) => ({ messages: [{ role: 'user', content: { type: 'text', text: `Review this ${language} code.` } }] }));

// transports
await server.connect(new StdioServerTransport());
const transport = new StreamableHTTPServerTransport({ sessionIdGenerator: () => randomUUID() });
```

### Python-SDK high-level API (`FastMCP`, from README — verbatim)

```python
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("My Server Name")

@mcp.tool()                                  # input schema inferred from type hints + docstring
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.resource("file://documents/{name}")     # RFC-6570 template param → fn arg
def read_document(name: str) -> str: ...

@mcp.prompt(title="Code Review")
def review_code(code: str) -> str: ...

class WeatherData(BaseModel): temperature: float; ...   # return → structuredContent via outputSchema
@mcp.tool()
def get_weather(city: str) -> WeatherData: ...

mcp.run()  # or mcp.run(transport="stdio") / mcp.run(transport="streamable-http"); `uv run mcp dev server.py`
```

---

## 6. OpenAI vs MCP — tool schema contrast

OpenAI function tool (Responses API, from function-calling docs — verbatim shape):

```json
{ "type": "function", "name": "get_weather",
  "description": "Retrieves current weather for the given location.",
  "parameters": { "type": "object", "properties": {...}, "required": [...], "additionalProperties": false },
  "strict": true }
```

| | OpenAI function tool | MCP Tool |
|---|---|---|
| fields | `type:"function"`, `name`, `description`, `parameters` (JSON Schema), `strict` | `name`, `title`, `description`, `inputSchema` (JSON Schema), `outputSchema`, `annotations`, `_meta` |
| schema-validity | `strict:true` + Structured Outputs | client SHOULD validate `structuredContent` vs `outputSchema` |
| safety hints | none in schema (instruction-level) | `readOnlyHint`/`destructiveHint`/`idempotentHint`/`openWorldHint` (untrusted unless trusted server) |
| discovery | tools sent inline in the request | `tools/list` over JSON-RPC, capability-negotiated, `listChanged` |

**OpenAI Apps SDK** = build a ChatGPT app *as an MCP server*. `_meta["openai/outputTemplate"]` on a tool points
to a widget resource (registered as an MCP resource, `text/html+skybridge` mimeType, `ui://` scheme); tool returns
`structuredContent`; extra `_meta` keys `openai/widgetAccessible`, `openai/toolInvocation/invoking`.

**OpenAI Responses API consuming a remote MCP server** — tool entry:

```json
{ "type": "mcp", "server_label": "...", "server_url": "https://example.com/", "authorization": "<oauth>",
  "require_approval": "never|always|{ \"never\": { \"tool_names\": [...] } }", "allowed_tools": ["tool_a"] }
```

Approval flow: server emits `mcp_approval_request` → caller replies `mcp_approval_response { approval_request_id,
approve }`.

**OpenAI Agents SDK** consuming MCP: `MCPServerStdio` / `MCPServerStreamableHttp` / `MCPServerSse` / `HostedMCPTool`;
`Agent(mcp_servers=[server])`; `create_static_tool_filter(allowed_tool_names=[...])` or dynamic filter;
`cache_tools_list=True` + `invalidate_tools_cache()`.

---

## 7. OSS server structure census (real repos, 2026-06-27)

| repo | lang | transport | tool defn | schema source | packaging | annotations | notes |
|---|---|---|---|---|---|---|---|
| `modelcontextprotocol/servers` (filesystem, memory, everything, sequentialthinking) | TypeScript | stdio | TS-SDK `registerTool`/low-level | zod / JSON Schema | `npx -y @modelcontextprotocol/server-X` | varies | canonical reference impls (not "production solutions") |
| `modelcontextprotocol/servers` (git) | Python | stdio | FastMCP `@mcp.tool()` | type hints + docstring | `uvx mcp-server-git` | — | Python reference impl |
| `github/github-mcp-server` | Go | stdio (Docker/binary) + remote hosted (`api.githubcopilot.com/mcp/`) | Go SDK | Go structs | `ghcr.io/github/github-mcp-server` | read-only mode skips write tools | tools grouped into **toolsets** (`repos`,`issues`,`pull_requests`,`actions`,`code_security`,`context`,`users`); `--toolsets`/`GITHUB_TOOLSETS`; `--read-only`; dynamic tool-search |

Cross-cutting de-facto structure: a manifest/`package.json`-or-`pyproject.toml` declaring the entrypoint bin;
the server file registers tools/resources/prompts via the high-level SDK; **stdio** transport as the default for
local servers (Streamable HTTP for remote); packaged to run via a single `npx -y`/`uvx`/Docker command; grouped
toolsets + a read-only mode for large surfaces; tested via the **MCP Inspector** (`npx @modelcontextprotocol/inspector
<cmd>`, UI at :6274, token-auth + localhost-bound) and the SDK's in-memory transport for unit tests.

MCP Inspector: official test/debug tool — `npx @modelcontextprotocol/inspector node build/index.js`; UI mode
(browse + call tools, read resources, get prompts, view notifications) + CLI mode (scripting/CI, JSON output).
</content>
