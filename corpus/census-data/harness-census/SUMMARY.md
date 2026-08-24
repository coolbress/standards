# OSS Coding-Harness Skeleton Census — findings (local/.scratch)

**Question (owner, 2026-06-25):** how do top-starred OSS *harnesses* structure their remote-repo
skeleton, and does that skeleton diverge from our compiled engineering standard in a way that would
block the breadth goal ("cover as many project types as possible")?

## Method
- Frame: `gh search repos` across harness-relevant topics/keywords (ai-agents, coding-agent, ai-coding,
  agent-framework, claude-code, mcp, code-generation, …) → 1,118 unique → noise-filtered (awesome-lists,
  guides, prompt-leak dumps, RAG/scraper/gateway/app repos removed) → **top 200 by stars**.
- Skeleton measured deterministically: for each repo, `gh api` repo meta + **recursive git tree**, then
  file-presence booleans (standard skeleton + harness-distinctive structure). Forks dropped.
- **Caveat:** the 2025 harness ecosystem is heavily **star-farmed / mirrored** (e.g. 221k-star unknowns,
  renamed clones). So results are reported two ways: **full top-200** (the ecosystem as it self-presents,
  noisy) and a **hand-verified canonical subset** (n=36 known-real harnesses: claude-code, codex,
  gemini-cli, opencode, cline, continue, goose, aider, OpenHands, SWE-agent, langchain, autogen, crewai,
  agno, smolagents, spec-kit, wshobson/agents, claude-flow, claude-code-router, OpenSpec, …). The canonical
  numbers are the trustworthy signal; full-200 shows the long tail.
- Type split: **APPLICATION harness** = has pkg manifest AND (CI∨tests∨lockfile) — the agent/CLI is real
  software. **CONTENT harness** = otherwise — skill/plugin/prompt packs (markdown + manifest, no build).

## Population
- Stack mix (top-200): **TypeScript 69 · Python 54 · JS 19 · Go 14 · Rust 12** → TS+JS ≈ 44%, Python 27%.
  (gingoa's TS/Node choice = the plurality.)
- 200 repos = **142 application + 58 content**. Canonical 36 = 26 application + 10 content.

## A. Standard software skeleton — CONFIRMS our compiled standard
| check | full-200 ALL | full APP | **canon ALL** | canon APP |
|---|---|---|---|---|
| README | 100% | 99% | **100%** | 100% |
| LICENSE | 94% | 96% | **100%** | 100% |
| .gitignore | 94% | 100% | **100%** | 100% |
| CI workflow | 84% | 94% | **100%** | 100% |
| tests | 76% | 89% | **92%** | 96% |
| pkg manifest | 71% | 100% | **72%** | 100% |
| committed lockfile | 58% | 82% | **56%** | 77% |
| lint/format cfg | 44% | 52% | **61%** | 73% |
| CONTRIBUTING | 59% | 65% | **61%** | 65% |
| SECURITY | 40% | 46% | **61%** | 69% |
| issue templates | 52% | 58% | **86%** | 88% |
| PR template | 42% | 46% | **67%** | 65% |
| dependabot | 22% | 27% | **64%** | 69% |
| docs/ dir | 63% | 70% | **69%** | 73% |
| CODE_OF_CONDUCT | 24% | 24% | **42%** | 38% |
| editorconfig | 10% | 13% | **28%** | 27% |
| CODEOWNERS | 15% | 18% | **47%** | 50% |
| pre-commit | 14% | 15% | **28%** | 31% |

→ **No conflict.** Application harnesses ship exactly our L0 floor (README/LICENSE/.gitignore/CI/tests/
manifest @ ~100% canonical). Recommended tier (CONTRIBUTING/SECURITY/issue+PR templates/dependabot) is
high in mature repos, sparse in the tail — matches our "non-blocking L4". Opt-in tier (editorconfig/
codeowners/pre-commit) is low — matches our "opt-in". **Committed lockfile only ~56%** → our ⚖️
above-census call (commit it) stands as a deliberate `[lit]` choice, not a census norm.

## B. Harness-DISTINCTIVE layer — what our general-repo standard does NOT model
| structural element | full-200 ALL | **canon ALL** | canon APP |
|---|---|---|---|
| `examples/` | 44% | **78%** | 77% |
| agent constitution (CLAUDE.md/AGENTS.md) | 67% | **75%** | 85% |
| `hooks/` | 52% | **72%** | 73% |
| `skills/` or SKILL.md | 68% | **67%** | 69% |
| `prompts/` | 31% | **67%** | 77% |
| config/manifest **schema** (JSON Schema) | 37% | **64%** | 62% |
| **mcp** config | 38% | **64%** | 62% |
| **marketplace/registry** manifest | 55% | **64%** | 62% |
| `templates/` or scaffold | 36% | **56%** | 58% |
| slash-`commands/` | 44% | **50%** | 54% |
| `plugins/` | 46% | **42%** | 38% |

→ **The real finding.** Mature harnesses converge on an **extra structural layer** beyond normal software:
a *capability/extension layer* — `skills/ · commands/ · hooks/ · prompts/ · mcp config · plugin +
marketplace/registry manifest · config schema · examples/ · agent constitution · templates/`. Marquee
coding agents (codex, gemini-cli, opencode, cline, goose, crewai, spec-kit, wshobson/agents, claude-flow)
light up nearly all of it; pure libraries (aider, langchain) have the floor but little of this layer;
content packs have the layer but a lighter floor.

## C. Bimodal split (matters for gingoa's identity)
- **Application harness** (codex, cline, opencode, goose…): full software floor **+** capability layer.
- **Content harness** (skill/plugin/prompt packs): capability layer, **manifest 0% / lockfile 0%**, CI 59%,
  tests 45% — they are markdown+manifest, not built software.
- **gingoa = application harness** (a CLI = real software, C5=cli) that ALSO *ships content* (adapters/,
  marketplace.json, SKILL.md). So it correctly belongs in the application column (full L0 floor — our
  FOUNDATION-PLAN already does this) **and** must ship a capability layer.

## D. Answer to the breadth concern
The harness skeleton does **not** conflict with our standard, and does **not** threaten "cover many project
types." It is strictly **ADDITIVE**: harness = (normal software project, our standard, confirmed) **+**
(capability/extension layer). And that capability layer (skills/templates/schema/mcp/commands) **is exactly
the machinery by which one harness covers many project types** — it's how gingoa projects standards onto
arbitrary user projects. Adopting it is aligned with both our min-dimension floor AND the breadth goal.

## E. Implication for gingoa
1. Keep the full L0 software floor (FOUNDATION-PLAN already correct — confirmed by canonical APP harnesses).
2. Our 7 archetypes {library, cli, web-app, backend-service, mobile, data-ml, monorepo} have **no
   "AI-harness / agent-tooling / plugin-pack" archetype** — yet that is gingoa's OWN archetype and a
   distinct, census-backed skeleton. Gap to close: model a **harness-capability layer** (skills · commands ·
   hooks · prompts · mcp · plugin+marketplace manifest · config schema · examples · agent-md · templates).
3. gingoa already seeds it (adapters/ + marketplace.json + gingoa-ping/SKILL.md). Make it first-class.
4. Publish-axis unchanged: capability layer + floor = product → **published**; planning/design stays local.
