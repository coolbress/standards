---
id: aspect-27-ai-harness-archetype--prompts-and-evals-standard
title: "Prompts · Evals build standard (prompt authoring/versioning + eval-harness design — the frontier-AI standard)"
parent: aspect-27-ai-harness-archetype
kind: reference
evidence_track: lit
status: review-needed
last_updated: "2026-06-27"
sources:
  - "https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview"
  - "https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices"
  - "https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-tools"
  - "https://platform.claude.com/docs/en/test-and-evaluate/develop-tests"
  - "https://platform.claude.com/docs/en/test-and-evaluate/eval-tool"
  - "https://www.anthropic.com/research/statistical-approach-to-model-evals"
  - "https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents"
  - "https://developers.openai.com/api/docs/guides/prompt-engineering"
  - "https://developers.openai.com/api/docs/guides/prompt-guidance"
  - "https://developers.openai.com/api/docs/guides/prompting/migrate-from-prompt-object"
  - "https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide"
  - "https://developers.openai.com/cookbook/examples/gpt-5/gpt-5-1_prompting_guide"
  - "https://developers.openai.com/cookbook/examples/gpt4-1_prompting_guide"
  - "https://developers.openai.com/api/docs/guides/reasoning-best-practices"
  - "https://developers.openai.com/api/docs/guides/evals"
  - "https://developers.openai.com/api/docs/guides/graders"
  - "https://developers.openai.com/api/docs/guides/agent-evals"
method: "lit — read IN FULL the Anthropic 'Prompting best practices' living reference (the full technique ladder + Claude 4.x/Opus-4.8 model guidance), the Console prompting-tools (generator/templates/improver) + Evaluation-tool docs, the 'Define success criteria and build evaluations' test-and-evaluate doc, the 'A statistical approach to model evals' research page, and the 'Demystifying evals for AI agents' engineering post; plus the OpenAI prompt-engineering / prompt-guidance / migrate-from-prompt-object guides, the GPT-5 prompting guide (cookbook), the reasoning-best-practices guide, and the Evals / graders / agent-evals guides (cross-vendor convergence/divergence check). Verbatim quotes + technique/grader tables deposited at census-data/frontier-ai-components/prompts-and-evals/."
---

> **Standard (claim):** Prompts and evals are **one closed loop**, and both are **source code**. A frontier-grade
> **prompt** is a **versioned, reviewed artifact stored in the repo** (not pasted into chat) — built on the
> shared technique ladder (be clear & direct · add context/motivation · 3–5 structured examples · XML-tagged
> structure · a system/role · let the model think · long-context-at-the-top · chain for self-correction),
> tuned to the model in use (Claude 4.x: explicit-but-not-CRITICAL, parallel tool calls, **adaptive thinking
> via `effort`**, **prefill deprecated**; GPT-5: `reasoning_effort` + tool-preambles + **contradiction-free**
> instructions), authored/improved with the vendor meta-tools and **iterated against evals**. A frontier-grade
> **eval harness** is a **golden dataset of task-specific cases + a grader** (code-graded fastest → LLM-as-judge
> for nuance, calibrated to humans → human as gold standard), built **eval-first** to encode the spec, run in
> **CI as a regression gate** and in production as drift monitoring, with **outcomes graded over trajectory**,
> **partial credit**, **transcripts read**, and **error bars** (SEM / paired-differences / power analysis). The
> two vendors have **converged**: both now say *put prompts in the repo, version by git/PR, eval-gate every
> change* — OpenAI is actively **deprecating its managed prompt objects** in favor of a code `prompts/` module.
> **Evidence:** lit (Anthropic prompt-engineering + eval docs + research + engineering posts; OpenAI prompt +
> GPT-5 + reasoning + evals/graders/agent-evals guides) · **Confidence:** high

This sub-doc is the concrete build spec behind aspect-27's "prompt engineering + versioning" and "evals /
eval-harness" bullets — the deep, AI-specific layer beneath aspect-08 (software testing) and the partner to
[`skill-authoring-standard.md`](skill-authoring-standard.md)'s "eval-driven authoring". gingoa scaffolds prompts
and eval harnesses for user projects (and dogfoods both: its agents run on authored prompts; its PRD/EARS is its
first eval set), so this is the standard the scaffold must emit to. Facts are pinned to the Anthropic + OpenAI
docs current at capture (2026-06-27).

## Why prompts and evals are one closed loop (and why both are source code)

The two vendors describe the **same cycle**. Anthropic's prompt-engineering overview opens by *requiring* an
eval before you tune a prompt: "This guide assumes that you have: 1. A clear definition of the success criteria…
2. Some ways to empirically test against those criteria… 3. A first draft prompt." OpenAI frames evals as
"behavior-driven development… describe desired system behavior, implement it, then test." A prompt change you
can't measure is a vibe; an eval with no prompt to improve is inert. **The loop is: define success criteria →
write a golden eval set → draft a prompt → run the eval → read the failures → refine the prompt (or the tools,
or the spec) → re-run.** Every sibling component standard (skills §7, MCP §1b, hooks/subagents §5) routes its
"don't ship on vibes" rule here; this doc is that rule's deep layer.

The second thesis — **prompts are source code** — is now stated by *both* vendors, the single strongest
cross-vendor convergence in this doc. OpenAI is **deprecating** its managed reusable-prompt objects: "Prompt
creation will be de-emphasized beginning **June 3, 2026**, and `v1/prompts` is scheduled to shut down on
**November 30, 2026**" [lit, migrate-from-prompt-object]. Its replacement guidance is verbatim what aspect-27
already demands: "Store production prompts in your application code… Move versioning to your repo using git
commits, PR review, and tests or evals… Replace prompt variables with function arguments so dynamic values are
explicit and typed… **Create a small `prompts/` module, keep each prompt as a named builder function, and add
lightweight eval fixtures so prompt changes are reviewed like product logic.**" Anthropic reaches the same place
from templates+variables: separating fixed from `{{variable}}` content gives "**Version control:** Easily track
changes to your prompt structure over time" [lit, prompting-tools]. So a prompt belongs in `prompts/`, in PRs,
diffed, pinned to a model id, eval-gated — never in chat state (aspect-27's "ruled out: prompts-as-chat-state").

## 1. The prompt technique ladder (the shared craft floor)

Anthropic now collapses the whole technique family into one living reference — "All prompting techniques — from
clarity and examples to XML structuring, role prompting, thinking, and prompt chaining — are covered in
[Prompting best practices]. That's the living reference; start there" [lit]. The ladder, each rule load-bearing
and verbatim-sourced:

1. **Be clear and direct.** "Think of Claude as a brilliant but new employee who lacks context on your norms."
   The **golden rule:** "Show your prompt to a colleague with minimal context… If they'd be confused, Claude
   will be too." Want above-and-beyond? "explicitly request it." OpenAI's GPT-5 guide is the mirror image with a
   sharper warning: "**poorly-constructed prompts containing contradictory or vague instructions can be more
   damaging to GPT-5 than to other models**" — the model burns reasoning tokens reconciling the contradiction.
2. **Add context / motivation.** "Providing context or motivation behind your instructions… can help Claude
   better understand your goals" ("…read aloud by a TTS engine, so never use ellipses"); "Claude is smart enough
   to generalize from the explanation" [lit].
3. **Use examples (few-shot / multishot).** "Examples are one of the most reliable ways to steer Claude's
   output." Make them **Relevant · Diverse · Structured** in `<example>`/`<examples>` tags; "**Include 3–5
   examples for best results**" [lit]. (OpenAI: "a handful of input/output examples.")
4. **Structure with XML tags.** "XML tags help Claude parse complex prompts unambiguously… Wrapping each type of
   content in its own tag (`<instructions>`, `<context>`, `<input>`) reduces misinterpretation." OpenAI converges
   on "Markdown headers and XML tags" to mark "logical boundaries"; GPT-5 uses `<instruction_spec>`-style tags.
5. **Give a role (system prompt).** "Setting a role in the system prompt focuses Claude's behavior… Even a single
   sentence makes a difference." The role goes in the `system` parameter (OpenAI: the **`developer` message**,
   §2).
6. **Let the model think.** "Prefer general instructions over prescriptive steps. A prompt like 'think
   thoroughly' often produces better reasoning than a hand-written step-by-step plan." Use `<thinking>` tags in
   few-shot examples; manual `<thinking>`/`<answer>` CoT as a fallback when thinking is off; "Ask Claude to
   self-check" [lit]. (Vendor **divergence** — see §3.)
7. **Long-context.** "Put longform data at the top" (above the query); "Queries at the end can improve response
   quality by up to **30%**." Wrap each document in `<document>`+`<document_content>`+`<source>`; "ground
   responses in quotes" first [lit].
8. **Chain complex prompts.** Still worth it "when you need to inspect intermediate outputs or enforce a specific
   pipeline structure." "**The most common chaining pattern is self-correction:** generate a draft → review it
   against criteria → refine based on the review" — each step a separate API call you can log/eval/branch [lit].
   This is the prompt-level form of the planner→impl→review loop (hooks-commands-subagents §3d).

**Output/format control** (a recurring footgun): "**Tell Claude what to do instead of what not to do**" ("smoothly
flowing prose paragraphs" not "Do not use markdown"); use XML format indicators; "match your prompt style to the
desired output" [lit].

## 2. Roles & message structure (the artifact's shape)

A prompt is a structured message list, not a string. The roles are the load-bearing skeleton:

- **Anthropic:** the `system` parameter (role/rules/durable context) + `messages[]` of `user`/`assistant` turns.
  Fixed content vs `{{variable}}` content is the version-control seam [lit, prompting-tools].
- **OpenAI:** a **three-tier authority hierarchy** — **developer** ("Instructions provided by the application
  developer, **prioritized ahead of user messages**") > **user** ("prioritized behind developer messages") >
  assistant. Mental model: "a function and its arguments… developer messages [=] a function definition" (rules),
  user messages = the arguments (inputs) [lit, prompt-engineering]. The `developer` role **superseded `system`**
  for chain-of-command on the reasoning models. **Divergence to flag in a portable prompt:** Anthropic authors to
  `system`, OpenAI to `developer`.
- **Prompt caching shapes the order:** put the stable, reused content "at the beginning of your prompt" and among
  the first JSON params so it caches [lit, OpenAI]. This rhymes with Anthropic's long-context "longform data at
  the top".

## 3. Model-specific tuning (where the vendors and versions diverge)

The shared ladder is the floor; the *current model* changes the dialect. A prompt artifact **MUST pin a model
id** because the guidance is version-specific:

**Claude 4.x / Opus-4.8** [lit, claude-prompting-best-practices]:
- **Explicit, but not over-prompted.** "Be more explicit" to make Claude *act* vs *suggest* ("Change this
  function", not "can you suggest changes"). BUT 4.5/4.6 "are also more responsive to the system prompt… these
  models may now overtrigger. The fix is to dial back any aggressive language. Where you might have said
  'CRITICAL: You MUST use this tool when...', you can use more normal prompting like 'Use this tool when...'."
- **Parallel tool calls.** Independent calls run in parallel; a `<use_parallel_tool_calls>` block boosts this to
  "~100%": "make all of the independent tool calls in parallel… if some tool calls depend on previous calls… call
  them sequentially."
- **Adaptive thinking via `effort`.** "Claude Opus 4.6, 4.7, 4.8, and Sonnet 4.6 use adaptive thinking
  (`thinking: {type: 'adaptive'}`)… calibrated based on the `effort` parameter and query complexity." "In
  internal evaluations, adaptive thinking reliably drives better performance than extended thinking." **`budget_tokens`
  is deprecated** — "On Claude Opus 4.7 and later models… setting `budget_tokens` returns a 400 error"; use
  `effort` or `max_tokens`.
- **Prefill is gone.** "Starting with Claude 4.6 models… **prefilled responses … on the last assistant turn are no
  longer supported… return a 400 error.**" The old "prefill `{`" / "prefill `Here is`" tricks → **Structured
  Outputs**, system-prompt "respond directly without preamble", or tool calling. *(A prior-era technique the
  ladder dropped — exactly the "time-sensitive content" footgun the skills standard warns about; an authored
  prompt that still prefills is now a bug.)*
- **Agentic coding guardrails** (each a verbatim system-prompt snippet): anti-overengineering ("Avoid
  over-engineering. Only make changes that are directly requested or clearly necessary"), anti-hardcode
  ("Implement a solution that works correctly for all valid inputs, not just the test cases"),
  `<investigate_before_answering>` ("Never speculate about code you have not opened… you MUST read the file
  before answering"), and multi-window state ("write tests in a structured format" / "It is unacceptable to
  remove or edit tests" / "Use git for state tracking").

**OpenAI GPT-5** [lit, gpt-5 prompting guide]:
- **`reasoning_effort`** — `"medium"` default, plus a "**minimal reasoning**" fastest tier; "minimal reasoning
  performance can vary more drastically depending on prompt than higher reasoning levels."
- **Agentic eagerness is dialable** — lower via lower `reasoning_effort`; higher via a persistence prompt: "You
  are an agent - please keep going until the user's query is completely resolved, before ending your turn."
- **Tool preambles** — "Always begin by rephrasing the user's goal… before calling any tools. Then, immediately
  outline a structured plan."
- **Responses-API reasoning persistence** — "Tau-Bench Retail score increases from **73.9% to 78.2%** just by
  switching to the Responses API and including `previous_response_id`" (pass prior reasoning items, `store=true`).
- **Metaprompting** — "using GPT-5 as a meta-prompter for itself" + the **Prompt Optimizer** in the Playground.

**OpenAI GPT-5.1** (the current sibling that updates the GPT-5 guide) [lit, gpt-5-1 prompting guide]:
- **A new `"none"` reasoning tier** that "forces the model to never use reasoning tokens" — a faster floor below
  GPT-5's `"minimal"`, for low-latency turns that don't need thinking.
- **Sharper agentic persistence** — "Persist until the task is fully handled **end-to-end within the current turn**
  whenever feasible: do not stop at analysis or partial fixes" (a tighter form of the GPT-5 keep-going prompt).
- **User-update preambles on a cadence** — post "short updates (1–2 sentences) every few tool calls", "at least
  every 6 execution steps or 8 tool calls (whichever comes first)" — so a long tool run stays legible.
- **First-class `apply_patch` + `shell` tools** — a structured-diff edit tool (create/update/delete; reported
  ~35% lower failure rate) and a sandboxed command tool, the GPT-side analogue of Claude's Edit/Bash.

**OpenAI GPT-4.1** is where these agentic prompts were first codified, as **three reminders** to put in a system
prompt [lit, gpt-4-1 prompting guide]: **persistence** ("You are an agent - please keep going until the user's
query is completely resolved, before ending your turn"), **tool-calling** ("use your tools to read files and gather
the relevant information: do NOT guess or make up an answer"), and **planning** ("You MUST plan extensively before
each function call, and reflect extensively on the outcomes"). It also states a concrete authoring rule the §4
tooling guidance assumes: **pass tools via the API `tools` field, never inject tool descriptions/parsers into the
prompt** — the guide measures a ~2% benchmark gain from API-parsed schemas over prompt-injected ones, and keeps
the model aligned with its training. (GPT-5/5.1's persistence + preambles above are the direct descendants of
these reminders.)

**Reasoning-model prompting (the sharpest divergence)** [lit, OpenAI reasoning-best-practices]: "Keep it simple…
brief, clear instructions"; "**Avoid chain-of-thought framing:** Reasoning models perform internal reasoning, so
prompting them to 'think step by step' is unnecessary and can reduce performance"; "Use developer messages, not
system messages"; "**Start with zero-shot.** Reasoning models often don't need few-shot examples." Anthropic's
manual-CoT advice (ladder #6) applies **only when thinking is off** — with native thinking/reasoning on, *both*
vendors agree: prefer general instructions over prescriptive steps, don't hand-write the chain.

## 4. Authoring & versioning tooling (how the artifact is built and tracked)

- **Anthropic Console prompt tools** [lit, prompting-tools]: the **prompt generator** ("guides Claude to create
  high-quality prompt templates… particularly useful for solving the 'blank page problem'"); **templates +
  `{{variables}}`** (the fixed/variable seam that enables version control + testability + the eval tool); the
  **prompt improver** (4 steps — example identification → structured XML draft → CoT refinement → example
  enhancement; "best for complex tasks requiring detailed reasoning").
- **OpenAI** has officially routed prompt versioning **into the repo** (§intro): a code `prompts/` module of
  named builder functions, variables → typed function args, versioned by git/PR, "reviewed like product logic",
  with "lightweight eval fixtures." The managed prompt object (`prompt: {id:"pmpt_…", version, variables}`) is
  being sunset.
- **The synthesis** (the rule gingoa adopts): use the vendor meta-tools to *draft/improve*, then **commit the
  result into `prompts/` as the source of truth**, pinned to a model id, with the eval set beside it. The Console/
  Playground is the workbench; the repo is the warehouse.

## 5. Eval-harness design (the dataset + grader contract)

### 5a. Build eval-first; encode the spec
Anthropic's agent-eval post makes evals the *first* artifact: "two engineers reading the same initial spec could
come away with different interpretations on how the AI should handle edge cases" → "**An eval suite resolves this
ambiguity.**" OpenAI's "behavior-driven development" is the same move. So the eval set is written **before** the
extensive prompt — identical to the skills standard's "Create evaluations BEFORE writing extensive documentation".

### 5b. The dataset — task-specific, edge-case-rich, start small, stay balanced
Eval design principles [lit, Anthropic develop-tests, verbatim]: "**Be task-specific:** Design evals that mirror
your real-world task distribution. Don't forget to factor in edge cases!"; "**Automate when possible**"; "**Prioritize
volume over quality:** More questions with slightly lower signal automated grading is better than fewer questions
with high-quality human hand-graded evals." Sizing [lit, demystifying-evals]: start with "**20-50 simple tasks
drawn from real failures**" (early development has "large effect size," so small samples suffice) — don't wait for
hundreds. A **good task** is "one where two domain experts would independently reach the same pass/fail verdict";
"a 0% pass rate across many trials typically signals a broken task, not incapable agents." Keep the set
**balanced** — "Test both where behaviors *should* and *shouldn't* occur."

### 5c. The grader — pick the fastest reliable one
The **three grader classes** are identical across vendors, with identical trade-offs [lit, Anthropic + OpenAI]:

| Grader | When | Trade-off (verbatim) |
|---|---|---|
| **Code-based** (exact/string match, schema, asserts) | clear-cut categorical answers | "Fastest and most reliable, extremely scalable, but… lacks nuance" / "brittle to valid variations" |
| **LLM-as-judge** (model-graded) | nuanced/subjective judgement | "Fast and flexible, scalable and suitable for complex judgement. **Test to ensure reliability first then scale.**" non-deterministic; **must be calibrated to humans** |
| **Human** | gold standard / calibration | "Most flexible and high quality, but slow and expensive. Avoid if possible." |

**LLM-judge craft** [lit]: "Have detailed, clear rubrics"; be "Empirical or specific" (output only
'correct'/'incorrect' or a 1–5 score); "**Encourage reasoning:** Ask the LLM to think first… and then discard the
reasoning. This increases evaluation performance" (the `<thinking>`→`<result>` pattern); "Generally best practice
to use a **different model to evaluate** than the model used to generate." Crucially, "**LLM-as-judge graders
should be closely calibrated with human experts**" — you confirm low human↔model divergence before trusting the
judge.

**OpenAI's grader menu** is the concrete API form of those classes [lit, graders]: `string_check`
(`eq`/`neq`/`like`/`ilike` → 0/1) · `text_similarity` (`fuzzy_match`/`bleu`/`gleu`/`meteor`/`cosine`/`rouge_*`) ·
`score_model` (LLM numeric score) · `label_model` (LLM classifier) · `python` (arbitrary code → float) ·
`multigrader` (weighted combination). Anthropic's catalog is the same shapes by hand: exact-match · cosine/SBERT ·
ROUGE-L · LLM Likert(1–5) · LLM binary · LLM ordinal.

### 5d. Agentic/multi-turn — grade outcomes, give partial credit, use pass^k
For agents the metric design changes [lit, demystifying-evals]: "**it's often better to grade what the agent
produced, not the path it took**" — grading "a sequence of tool calls in the right order" punishes valid
alternative routes. Build **partial credit**: "A support agent that correctly identifies the problem and verifies
the customer but fails to process a refund is meaningfully better than one that fails immediately." Reliability
metrics: **pass@k** = "the likelihood that an agent gets at least one correct solution in k attempts"; **pass^k** =
"the probability that all k trials succeed" — "critical for customer-facing agents." OpenAI's **trace grading** is
the same idea operationalized: "the fastest way to identify workflow-level issues" — score the "end-to-end record
of model calls, tool calls, guardrails, and handoffs for one run" (right tool? handoff as intended? instruction/
safety violation?) "with structured criteria so you can find regressions and failure modes at scale."

### 5e. Read transcripts; watch for saturation
Non-negotiable [lit, demystifying-evals, verbatim]: "**You won't know if your graders are working well unless you
read the transcripts and grades from many trials**"; teams should "sample transcripts to read weekly." And watch
the ceiling: at ~100% pass rates "**eval saturation**" "provides no signal for improvement" — a saturated eval
needs harder cases, not celebration.

## 6. Statistics — put error bars on the number

A single eval percentage is a point estimate with hidden variance. Anthropic's "A statistical approach to model
evals" (the field reference, arXiv:2411.00640) gives five recommendations [lit, verbatim]:

1. **Report the SEM** (standard error of the mean, from the Central Limit Theorem) "alongside each calculated eval
   score" — it measures underlying skill independent of which questions you happened to pick.
2. **Cluster standard errors** on the unit of randomization (e.g. a passage shared by several questions) — "clustered
   standard errors on popular evals can be **over three times as large** as naive standard errors" (so naive SEMs
   over-state significance).
3. **Reduce within-question variance** — for CoT evals, "resampling answers from the same model several times, and
   using the question-level averages"; for deterministic answers, use "next-token probabilities."
4. **Use paired-differences** (not a two-sample test) to compare two models/prompts — question-score correlation
   between frontier models "ranges from 0.3 and 0.7," so pairing cancels question-difficulty variance.
5. **Power analysis** — "calculate the number of questions that an eval should have" to reliably detect a stated
   effect (Model A beats Model B by X%) before you run it.

The practical upshot for a harness: when an eval gate says "prompt v2 scored 87% vs v1's 85%," that delta is only
real if it clears the paired-difference error bar — otherwise it's noise, and the gate must not pass v2 on it.

## 7. The eval lifecycle (where evals run)

Both vendors describe the same staged lifecycle [lit, demystifying-evals + OpenAI agent-evals]:
1. **Pre-launch / CI-CD** — automated evals run on every change as a **regression gate** (the golden set must not
   regress). This is the AI-specific extension of aspect-08's test gate.
2. **Production monitoring** — track real-world metrics + **distribution drift** post-launch (OpenAI: online
   evaluation in real time).
3. **A/B testing** — validate significant changes against live traffic with enough volume for significance.
4. **User feedback / transcript review** — ongoing calibration; sample transcripts weekly.

OpenAI ships this as a runnable loop ("Build an Agent Improvement Loop with Traces, Evals, and Codex" —
"keeps traces, reviewer judgment, generated evals, optimization, and implementation handoff inside one runnable
improvement loop").

## Anti-patterns (each cited)

- **Prompts as chat state** — unversioned, unreviewed, un-pinned-to-a-model prompts pasted into a session;
  non-reproducible and un-eval-able. Both vendors now say put them in `prompts/`, git-versioned [lit].
- **Tuning a prompt with no eval** — "vibes" iteration; Anthropic's overview *requires* success criteria + a test
  before prompt engineering [lit].
- **Writing the eval after the prompt** — inverts eval-first; the eval should *encode the spec* up front
  [lit, demystifying-evals + skills §7].
- **Contradictory / vague instructions** — "more damaging to GPT-5 than to other models"; the model wastes
  reasoning reconciling the conflict [lit].
- **Still prefilling on Claude 4.6+** — a 400 error now; migrate to structured outputs / direct instruction [lit].
- **"CRITICAL: you MUST…" over-prompting on 4.5/4.6** — causes over-triggering; use normal "Use this tool when…"
  [lit]. (And telling a reasoning model to "think step by step" — "can reduce performance" [lit].)
- **Hand-writing the chain for a thinking/reasoning model** — "general instructions… often produce better
  reasoning than a hand-written step-by-step plan" [lit].
- **Grading trajectory not outcome** (agentic) — punishes valid alternate paths; grade what was produced + give
  partial credit [lit].
- **Trusting an uncalibrated LLM judge** — non-deterministic and possibly mis-aligned with humans; calibrate
  against human experts first, and read transcripts [lit].
- **A bare eval percentage with no error bar** — naive SEMs over-state significance (clustered SEs can be >3×);
  use paired-differences + power analysis before claiming a regression/win [lit].
- **An ambiguous or unsolvable eval task** — "0% pass rate… typically signals a broken task"; a good task has two
  experts agreeing on the verdict [lit].
- **A saturated eval kept as a gate** — ~100% pass gives "no signal"; raise the difficulty [lit].

## How gingoa should author + version prompts and build its eval-harness

gingoa runs on authored prompts (its planner/implementer/reviewer agents) and scaffolds prompts + eval harnesses
for user projects. **gingoa's own PRD/EARS is the canonical worked example:** `docs/prd.yml` carries one user
story per lifecycle stage, "each acceptance criterion is in **EARS notation**" (`docs/PRD.md`) — the project
instruction is that **"the EARS acceptance criteria are the tests to satisfy"** (CLAUDE.md "Build to the spec").
That makes the **EARS acceptance set gingoa's first golden eval set**: each EARS criterion is a task whose
pass/fail two engineers would agree on (the §5b "good task" bar), graded code-first where the criterion is
checkable and LLM-judge where it is behavioral. The scaffold MUST emit, to match this standard:

1. **Prompts as committed source.** A `prompts/` module of **named builder functions** (OpenAI's verbatim
   pattern), each prompt: variables → typed function args, **pinned to a model id**, on the shared ladder (clear &
   direct · context · 3–5 structured examples · XML tags · a `system`/`developer` role · think-or-not per model ·
   long-data-at-top · self-correction chain where staged). Version by **git/PR**, diffed, reviewed "like product
   logic" — never chat state. Offer the vendor generator/improver as a *drafting* aid whose output lands in
   `prompts/`. Flag the **portability seam** (Anthropic `system` vs OpenAI `developer`; prefill deprecated;
   `effort` vs `reasoning_effort`) so a cross-host prompt targets the right dialect.
2. **An eval set beside every prompt** — start at **20–50 tasks drawn from real failures + edge cases**, balanced
   (should/shouldn't), each a two-experts-agree task. For gingoa itself, **seed it from the PRD/EARS acceptance
   criteria** so the spec is the eval. Store as data (JSONL/JSON) the way the skill/MCP/subagent scaffolds already
   emit `evals/evals.json`.
3. **A grader picked fastest-reliable-first** — **code-graded** (exact/string/schema/assert) wherever the
   criterion is checkable; **LLM-as-judge** with a detailed rubric + "reason-then-discard" + a **different grader
   model** for nuance, and a **human-calibration step** before the judge is trusted; human only as gold standard.
   For agentic flows, **grade outcomes with partial credit**, report **pass@k / pass^k**, and offer trace-grading.
4. **The eval as a CI regression gate** — wire the golden set into the same CI that runs lint/typecheck/test/build
   (aspect-04 / aspect-08), so a prompt or tool change that regresses the set **fails the gate** (presence ≠
   adequacy: a prompt with no passing eval is not a deliverable). Compute an **error bar** (SEM; paired-difference
   vs the previous prompt version; power-checked sizing) so a "win/regression" is real, not noise — and surface an
   **eval-saturation** warning when the set hits ~100%.
5. **Transcript review + drift hooks** — emit a "read N transcripts" note (weekly cadence) and, for deployed
   agents, the production-monitoring/A-B/drift stubs so the lifecycle (§7) is wired, not just the pre-launch gate.

This makes the gingoa prompt + eval scaffold emit **versioned, model-pinned prompts in `prompts/`** and a
**golden eval set gated in CI** at the Anthropic/OpenAI quality bar — closing the prompt↔eval loop, grounding
gingoa's own dev loop in its PRD/EARS, and gating both like every other shipped guardrail.

## Sources

- Anthropic — Prompt engineering overview (the eval-first preconditions; pointer to the living reference) — https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview
- Anthropic — Prompting best practices (the full technique ladder + Claude 4.x/Opus-4.8 model guidance; adaptive thinking; prefill deprecation; parallel tools) — https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- Anthropic — Console prompting tools (prompt generator · templates+variables · prompt improver; the version-control seam) — https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-tools
- Anthropic — Define success criteria and build evaluations (eval design principles · 3 grader methods · LLM-judge tips) — https://platform.claude.com/docs/en/test-and-evaluate/develop-tests
- Anthropic — Using the Evaluation tool (Console: generate test cases · side-by-side · 5-point grade · prompt versioning) — https://platform.claude.com/docs/en/test-and-evaluate/eval-tool
- Anthropic — A statistical approach to model evals (SEM · clustered SEs · variance reduction · paired-differences · power analysis; arXiv:2411.00640) — https://www.anthropic.com/research/statistical-approach-to-model-evals
- Anthropic — Demystifying evals for AI agents (evals encode the spec · 20-50 tasks · pass@k/pass^k · outcome>trajectory · partial credit · read transcripts · saturation · lifecycle) — https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- OpenAI — Prompt engineering (strategies · developer/user/assistant authority hierarchy · prompt caching order) — https://developers.openai.com/api/docs/guides/prompt-engineering
- OpenAI — Prompt guidance (outcome-first; store prompts in code; reusable-objects deprecation) — https://developers.openai.com/api/docs/guides/prompt-guidance
- OpenAI — Migrate from prompt objects (the verbatim "prompts in code / `prompts/` module / git-versioned" rule + the June-3-2026 / Nov-30-2026 sunset dates) — https://developers.openai.com/api/docs/guides/prompting/migrate-from-prompt-object
- OpenAI — GPT-5 prompting guide (reasoning_effort · eagerness · tool preambles · contradiction trap · Responses-API persistence 73.9%→78.2% · metaprompting) — https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide
- OpenAI — GPT-5.1 prompting guide (new `none` reasoning tier · end-to-end-within-the-turn persistence · update-preamble cadence every 6–8 tool calls · apply_patch/shell tools) — https://developers.openai.com/cookbook/examples/gpt-5/gpt-5-1_prompting_guide
- OpenAI — GPT-4.1 prompting guide (the three agentic reminders: persistence · tool-calling · planning; "use the API `tools` field, don't inject tool descriptions into the prompt") — https://developers.openai.com/cookbook/examples/gpt4-1_prompting_guide
- OpenAI — Reasoning best practices (keep-it-simple · avoid CoT framing · developer messages · zero-shot first) — https://developers.openai.com/api/docs/guides/reasoning-best-practices
- OpenAI — Evals (behavior-driven · datasets/JSONL · templating · run via API/dashboard) — https://developers.openai.com/api/docs/guides/evals
- OpenAI — Graders (string_check · text_similarity · score_model · label_model · python · multigrader) — https://developers.openai.com/api/docs/guides/graders
- OpenAI — Evaluate agent workflows / trace grading (trace = model+tool+guardrail+handoff record; outcome/regression at scale) — https://developers.openai.com/api/docs/guides/agent-evals
- Raw verbatim quotes + technique/grader tables + convergence/divergence — `census-data/frontier-ai-components/prompts-and-evals/samples.md`
