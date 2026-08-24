# SKILL.md samples — verbatim frontmatter + layouts (raw evidence)

Captured 2026-06-27. Immutable provenance for the skill-authoring standard.

## A. The open-spec frontmatter table (agentskills.io/specification)

| Field | Required | Constraints (verbatim) |
|---|---|---|
| `name` | Yes | Max 64 chars. Lowercase letters, numbers, hyphens only. No leading/trailing hyphen; no consecutive `--`. **Must match the parent directory name.** |
| `description` | Yes | Max 1024 chars. Non-empty. What the skill does AND when to use it; include trigger keywords. |
| `license` | No | License name or reference to a bundled license file. |
| `compatibility` | No | Max 500 chars. Environment requirements (intended product, system packages, network). |
| `metadata` | No | Arbitrary string→string key-value map. Recommend unique key names. |
| `allowed-tools` | No | Space-separated string of pre-approved tools. **Experimental** — support varies by agent. |

Progressive-disclosure budget (spec, verbatim): Metadata `~100 tokens` (name+description, loaded at
startup for ALL skills) → Instructions `< 5000 tokens recommended` (full SKILL.md body, on activation) →
Resources `as needed`. "Keep your main `SKILL.md` under 500 lines." "Keep file references one level deep."

Directory: `scripts/` (executable code) · `references/` (docs, e.g. `REFERENCE.md`/`FORMS.md`) · `assets/`
(templates/images/data). Validator: `skills-ref validate ./my-skill` (agentskills/agentskills).

## B. Claude Code extension fields (code.claude.com/docs/en/skills)

CC follows the open standard, then ADDS host-specific frontmatter (all optional; only `description` recommended):
`name` (defaults to dir name) · `description` (+`when_to_use`; combined text truncated at **1,536 chars** in
the listing) · `argument-hint` · `arguments` · `disable-model-invocation` · `user-invocable` · `allowed-tools` ·
`disallowed-tools` · `model` · `effort` · `context: fork` · `agent` · `hooks` · `paths` · `shell`.

- Command name = the **directory** name (`.claude/skills/deploy/SKILL.md` → `/deploy`), NOT frontmatter `name`
  (except a plugin-root SKILL.md). Plugin skills namespace as `plugin:skill`.
- Locations: enterprise > personal (`~/.claude/skills/`) > project (`.claude/skills/`) > plugin > bundled.
- `<Tip>Keep SKILL.md under 500 lines. Move detailed reference material to separate files.</Tip>`
- Invoked SKILL.md content enters context as one message and stays for the session (recurring token cost).
- Description-budget overflow: scales at 1% of context window (`skillListingBudgetFraction`); 1,536-char cap
  per entry (`maxSkillDescriptionChars`).

## C. OpenAI Codex (developers.openai.com/codex/skills) — same open standard

Required frontmatter: `name` + `description` only. Layout: `SKILL.md` (req) + `scripts/`/`references/`/`assets/`
+ optional `agents/openai.yaml`. Locations: `.agents/skills` (repo) · `~/.agents/skills` (user) ·
`/etc/codex/skills` (admin) · bundled. Budget: skill listing ≤ **2% of context window or 8,000 chars**;
full SKILL.md loaded only on use. Explicitly "build[s] on the open agent skills standard (agentskills.io)."
AGENTS.md = always-on team rules; Skills = reusable task workflows (the two-place split).

## D. Anthropic official best-practices extra validation (platform.claude.com .../best-practices)

`name`: max 64 chars, lowercase/numbers/hyphens, **no XML tags, no reserved words "anthropic"/"claude"**.
`description`: non-empty, max 1024 chars, no XML tags, **third person** ("Processes Excel files", not
"I/You can…"). Naming = **gerund form** preferred (`processing-pdfs`); avoid `helper`/`utils`/`tools`.
"Build evaluations BEFORE writing extensive documentation" — ≥3 eval scenarios. Body < 500 lines.

## E. Harvested real SKILL.md frontmatter (verbatim)

### anthropics/skills — template/SKILL.md (the canonical starter)
```yaml
---
name: template-skill
description: Replace with description of the skill and when Claude should use it.
---
```

### anthropics/skills — skills/skill-creator/SKILL.md
```yaml
---
name: skill-creator
description: Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit, or optimize an existing skill, run evals to test a skill, benchmark skill performance with variance analysis, or optimize a skill's description for better triggering accuracy.
---
```

### anthropics/skills — skills/pdf/SKILL.md (uses `license`; references FORMS.md/REFERENCE.md)
```yaml
---
name: pdf
description: Use this skill whenever the user wants to do anything with PDF files. This includes reading or extracting text/tables from PDFs, combining or merging multiple PDFs into one, splitting PDFs apart, rotating pages, adding watermarks, creating new PDFs, filling PDF forms, encrypting/decrypting PDFs, extracting images, and OCR on scanned PDFs to make them searchable. If the user mentions a .pdf file or asks to produce one, use this skill.
license: Proprietary. LICENSE.txt has complete terms
---
```

### anthropics/skills — skills/mcp-builder/SKILL.md
```yaml
---
name: mcp-builder
description: Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. Use when building MCP servers to integrate external APIs or services, whether in Python (FastMCP) or Node/TypeScript (MCP SDK).
license: Complete terms in LICENSE.txt
---
```

### obra/superpowers — skills/writing-skills/SKILL.md (mature OSS; "Use when…" desc convention)
```yaml
---
name: writing-skills
description: Use when creating new skills, editing existing skills, or verifying skills work before deployment
---
```
obra/superpowers ships **16 skills** in a flat `skills/` namespace (test-driven-development,
systematic-debugging, brainstorming, writing-plans, using-git-worktrees, …). Its `writing-skills` skill adds
stricter house rules: getting-started skills `<150 words`, frequently-loaded `<200 words`; gerunds + active
verbs; "Description = When to Use, NOT What the Skill Does"; flat searchable namespace.

## F. anthropics/skills repo top-level layout
```
.claude-plugin/   README.md   THIRD_PARTY_NOTICES.md   skills/   spec/   template/
spec/agent-skills-spec.md            # the open standard
template/SKILL.md                    # 2-field starter
skills/<17 skills>                   # algorithmic-art, brand-guidelines, canvas-design, claude-api,
                                     # doc-coauthoring, docx, frontend-design, internal-comms, mcp-builder,
                                     # pdf, pptx, skill-creator, slack-gif-creator, theme-factory,
                                     # web-artifacts-builder, webapp-testing, xlsx
```
