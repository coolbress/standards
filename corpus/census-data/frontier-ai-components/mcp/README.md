# frontier-ai-components / mcp — raw evidence

Verbatim MCP spec shapes, SDK API surfaces, and real-server structures harvested from the MCP specification
(rev 2025-11-25), the official SDKs, Anthropic + OpenAI docs, and mature OSS MCP servers — backing
`aspects/27-ai-harness-archetype/mcp-server-standard.md`. Append-only raw provenance — never edited.

Method: WebFetch of `modelcontextprotocol.io/specification/2025-11-25/*` (overview/lifecycle/transports +
server/{tools,resources,prompts} + basic/security_best_practices + docs/sdk), the schema TypeScript source
(`schema/2025-11-25/schema.ts` for the `ToolAnnotations` defaults), the TS-SDK `docs/server.md` + Python-SDK
README (the high-level API surface), the MCP Inspector repo, Anthropic's MCP announcement + "Writing tools for
agents" + "Code execution with MCP" engineering posts, the Claude Code MCP docs, OpenAI's function-calling +
Apps-SDK + Responses-API-MCP + Agents-SDK-MCP docs, and the reference-servers / github-mcp-server repos.
Captured 2026-06-27.

See [`samples.md`](samples.md) for the harvested shapes (tool/resource/prompt JSON, annotation defaults, SDK
snippets, the OpenAI-vs-MCP schema contrast, and the OSS-server structure table).
</content>
