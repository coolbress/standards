---
id: aspect-13-api-interface-design
title: "API & Interface Design"
group: "Q — Quality Attributes"
kind: gated
gated_archetypes: ["library", "cli", "backend"]
cross_cutting: false
lifecycle_stages: ["③"]
anchors: ["SWEBOK-KA2", "SWEBOK-KA3", "OpenAPI", "AsyncAPI"]
evidence_track: lit
status: review-needed
last_updated: "2026-06-25"
sources:
  - "https://ieeecs-media.computer.org/media/education/swebok/swebok-v4.pdf"
  - "https://spec.openapis.org/oas/latest.html"
  - "https://www.asyncapi.com/docs/reference/specification/latest"
  - "https://www.rfc-editor.org/rfc/rfc9110.html"
claim: "Design the interface contract first and version it: a stable, machine-described surface (OpenAPI for HTTP, AsyncAPI for event-driven, signature+semantics for libraries/CLI) with explicit pre/postconditions, idempotency where HTTP requires it, and a breaking-change gate — never an ad-hoc surface that leaks implementation."
maps_from: []
census_todo: "Literature-grounded (lit-track gated aspect): no fabricated census %. If a future repo survey measures OpenAPI/AsyncAPI adoption or CLI --json/exit-code conventions per archetype, append to census-data/ and widen here."
---

> **Standard (claim):** Design the interface contract first and version it — a stable, machine-described surface (OpenAPI / AsyncAPI / signature+semantics) with explicit pre/postconditions, HTTP-correct idempotency, and a breaking-change gate; never an ad-hoc surface that leaks implementation.
> **Evidence:** [lit, normative] SWEBOK v4 KA2/KA3, OpenAPI 3.2, AsyncAPI 3.1, RFC 9110 · **Confidence:** High (named standards) · **Kind:** gated[library/cli/backend] · **Stage:** ③

**Seed sub-aspects:** `REST / GraphQL / gRPC design` · `versioning & breaking-change gate` · `idempotency` · `rate-limit` · `OpenAPI contract` · `CLI UX (POSIX flags / exit codes / --json)` · `SDK / webhook`

## What professional engineers do

- **Contract before code (SWEBOK KA2 — Software Design).** An API is "the set of signatures exported and available to the users of a library or framework," and a signature alone is insufficient: it "should always include statements about the program's effects and/or behaviors (i.e., its semantics)." [lit, normative] Seniors design the interface — signatures + documented semantics — as the design artifact, then construct against it, applying **Design by Contract**: explicit pre/postconditions per routine/class so each forms a contract with its callers. [lit, normative]
- **HTTP / REST design.** Use the HTTP method whose defined semantics match the intent (RFC 9110). GET/HEAD/OPTIONS/TRACE are *safe* (read-only, no expected state change); GET/HEAD/OPTIONS/TRACE + PUT + DELETE are *idempotent* (N identical requests ≡ 1). [lit, normative] POST is neither — so create/charge-style POSTs that must tolerate client retries get an **idempotency key** to fold duplicates. Resource-oriented URLs, status codes that mean what they say, and content negotiation are the baseline.
- **OpenAPI contract (HTTP).** Describe the surface in OpenAPI — "a standard, programming-language-agnostic interface description for HTTP APIs" that humans and machines read without source access. [lit] A valid document needs `openapi`, an `info` (title+version), and at least one of `paths`/`components`/`webhooks`; schemas use JSON Schema 2020-12; reusable schemas/params/responses/security live in `components`. This drives codegen, mock servers, contract tests, and docs from one source of truth.
- **Event-driven / async (AsyncAPI).** For message/event APIs (Kafka, MQTT, AMQP, WebSockets, webhooks), describe the surface in AsyncAPI — "describe message-driven APIs in a machine-readable format," protocol-agnostic, modeling **channels** (where messages flow), **messages** (payload+headers), **operations** (send/receive), and **servers/bindings**. [lit] Webhooks are a published, versioned, signed contract — not an undocumented callback.
- **Versioning & the breaking-change gate.** OpenAPI/AsyncAPI/SemVer all encode the same rule: a backward-incompatible change to the surface is a MAJOR event. Removing/renaming a field, tightening a type, changing required-ness, or altering semantics is breaking; additive changes are not. Seniors gate this in CI (spec-diff / linter) and choose a versioning strategy (URL `/v2`, media-type, or header) plus a deprecation window before removal.
- **Rate-limit & robustness.** Public/backend surfaces advertise limits (`429` + `Retry-After` / `RateLimit-*` headers) and document error shapes as part of the contract, so clients can back off deterministically rather than guess.
- **CLI UX as an interface.** A CLI is an API for humans + scripts: POSIX/GNU flag conventions (`-v`/`--verbose`, `--` terminator), meaningful **exit codes** (0 success, non-zero categorized failure), stdout-for-data / stderr-for-diagnostics separation, and a `--json` (or `--format`) machine mode so the tool composes in pipelines. Stable flags + stable exit codes = the CLI's backward-compatibility contract.
- **Library/SDK surface.** Minimize and stabilize the public surface; everything else is internal. Hand-written or generated SDKs track the spec version; deprecations are announced, typed, and removed only on a MAJOR bump.

## Evidence (lit + census)

- [lit, normative] **SWEBOK v4.0** (IEEE CS, Oct 2024) — KA *Software Design* (KA2): API = signatures + semantics; Design by Contract (pre/postconditions). KA *Software Construction* (KA3): constructing to documented interfaces. https://ieeecs-media.computer.org/media/education/swebok/swebok-v4.pdf
- [lit] **OpenAPI Specification 3.2.0** (2025-09-19) — language-agnostic HTTP interface description; required `openapi`/`info` + ≥1 of `paths`/`components`/`webhooks`; JSON Schema 2020-12; reusable `components`. https://spec.openapis.org/oas/latest.html
- [lit] **AsyncAPI 3.1.0** — protocol-agnostic description of message-driven APIs: channels / messages / operations / servers / bindings. https://www.asyncapi.com/docs/reference/specification/latest
- [lit, normative] **RFC 9110 — HTTP Semantics** — safe vs idempotent methods; GET/HEAD/OPTIONS/TRACE safe; +PUT/DELETE idempotent; POST neither (motivates idempotency keys). https://www.rfc-editor.org/rfc/rfc9110.html
- [census] None — this is a literature-grounded gated aspect (see `census_todo`). No adoption % fabricated.

## Archetype variations

This aspect is **gated** — it activates only for `library`, `cli`, `backend`. It does not fire for archetypes with no externally-consumed contract surface.

- **backend** — full weight: OpenAPI (HTTP) or AsyncAPI (events), RFC-9110-correct methods + idempotency keys on retryable POSTs, rate-limit headers, versioning gate, signed webhooks. Heaviest activation.
- **library** — public API surface = signatures + documented semantics (KA2); minimal stable surface; SemVer-disciplined deprecation; no transport spec, but the breaking-change gate is identical.
- **cli** — the "API" is flags + exit codes + stdout/stderr discipline + `--json`. POSIX/GNU conventions are the contract; stable flags/exit-codes are the compat guarantee. No OpenAPI/AsyncAPI.
- **Not gated** (web-only UI, mobile-only, data-pipeline-without-external-API): no published machine contract is required; do not force OpenAPI/AsyncAPI scaffolding on them.

## Tradeoffs / what's ruled out

- **Spec-first vs code-first.** Spec-first (write OpenAPI/AsyncAPI, then generate) buys a single source of truth and contract tests at the cost of upfront ceremony; code-first (annotations → generated spec) is lighter but lets the spec drift. Either is acceptable *if* the spec is the gated, CI-checked artifact; an undocumented or hand-maintained-and-stale surface is ruled out.
- **GraphQL / gRPC** are valid surfaces but trade REST's HTTP-cache/idempotency clarity for typed schemas / streaming; pick per need — not as a default.
- **Ruled out:** breaking changes without a MAJOR bump + deprecation window; POST endpoints that aren't retry-safe yet lack idempotency keys; CLIs that emit data on stderr or churn flags/exit-codes across minor releases; webhooks with no versioned, signed payload contract.

## Sources

- https://ieeecs-media.computer.org/media/education/swebok/swebok-v4.pdf
- https://spec.openapis.org/oas/latest.html
- https://www.asyncapi.com/docs/reference/specification/latest
- https://www.rfc-editor.org/rfc/rfc9110.html

## Sub-documents
- [`api-scope-boundary--facts-2026-08.md`](api-scope-boundary--facts-2026-08.md) — *research-log (ko)* — 2026-08 facts-only pass (R3-4): **RFC 9110과 OpenAPI는 공개/내부 API를 구분하지 않는다**(명시 없음 — 모든 HTTP에 균등 적용) · SemVer가 스스로 규정하는 적용 대상. 표준 §6의 "내부 API만이라 해당 없음" 기각 사유가 약함을 드러낸 근거.
