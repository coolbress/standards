# prompts + evals samples — verbatim quotes, ladders, grader tables (raw evidence)

Captured 2026-06-27. Immutable provenance for the prompts-and-evals build standard. All quotes are verbatim
from the cited official source.

---

# PART A — PROMPTS

## A1. Anthropic prompt-engineering technique ladder (platform.claude.com)

The overview page now redirects the full technique list to ONE living reference: **"Prompting best
practices"** — *"All prompting techniques — from clarity and examples to XML structuring, role prompting,
thinking, and prompt chaining — are covered in [Prompting best practices]. That's the living reference; start
there."* The page is organized: model-specific guidance → techniques for all current models → migration.

Technique sections (verbatim headers), in order:

| # | Technique (verbatim header) | Load-bearing rule (verbatim) |
|---|---|---|
| 1 | **Be clear and direct** | "Think of Claude as a brilliant but new employee who lacks context on your norms and workflows." **Golden rule:** "Show your prompt to a colleague with minimal context on the task and ask them to follow it. If they'd be confused, Claude will be too." If you want "above and beyond" behavior, "explicitly request it." |
| 2 | **Add context to improve performance** | "Providing context or motivation behind your instructions… can help Claude better understand your goals." (TTS-ellipses example.) "Claude is smart enough to generalize from the explanation." |
| 3 | **Use examples effectively** (few-shot/multishot) | "Examples are one of the most reliable ways to steer Claude's output." Make them **Relevant · Diverse · Structured** (wrap in `<example>`/`<examples>` tags). **"Include 3–5 examples for best results."** |
| 4 | **Structure prompts with XML tags** | "XML tags help Claude parse complex prompts unambiguously… Wrapping each type of content in its own tag (e.g. `<instructions>`, `<context>`, `<input>`) reduces misinterpretation." Use consistent descriptive tag names; nest for hierarchy. |
| 5 | **Give Claude a role** (system prompt) | "Setting a role in the system prompt focuses Claude's behavior and tone… Even a single sentence makes a difference." Role goes in the `system` parameter. |
| 6 | **Long context prompting** | "Put longform data at the top" (above query/instructions/examples). "Queries at the end can improve response quality by up to **30%** in tests." Wrap each doc in `<document>` + `<document_content>` + `<source>`. "Ground responses in quotes" — ask Claude to quote relevant parts first. (20k+ token inputs.) |
| 7 | **Chain complex prompts** | "Explicit prompt chaining (breaking a task into sequential API calls) is still useful when you need to inspect intermediate outputs or enforce a specific pipeline structure." "The most common chaining pattern is **self-correction:** generate a draft → have Claude review it against criteria → have Claude refine based on the review." |
| 8 | **Thinking / CoT** | "Prefer general instructions over prescriptive steps. A prompt like 'think thoroughly' often produces better reasoning than a hand-written step-by-step plan." "Multishot examples work with thinking" (use `<thinking>` tags in examples). "Manual chain-of-thought (CoT) prompting as a fallback" when thinking is off, with `<thinking>`/`<answer>` tags. "Ask Claude to self-check." |

## A2. Output/format control (verbatim)

- **"Tell Claude what to do instead of what not to do."** Instead of "Do not use markdown" → "Your response should be composed of smoothly flowing prose paragraphs."
- **"Use XML format indicators"** — "Write the prose sections… in `<smoothly_flowing_prose_paragraphs>` tags."
- **"Match your prompt style to the desired output"** — "removing markdown from your prompt can reduce the volume of markdown in the output."

## A3. PREFILL — deprecated (a Claude 4.6+ DIVERGENCE from the old ladder)

VERBATIM: "Starting with Claude 4.6 models and Claude Mythos Preview, **prefilled responses … on the last
assistant turn are no longer supported. Requests with prefilled assistant messages to these models return a
400 error.** Model intelligence and instruction following have advanced such that most use cases of prefill no
longer require it." Migration: use **Structured Outputs** for format; direct system-prompt instruction for
preamble-stripping ("Respond directly without preamble"); move continuations into the user message.

## A4. Claude 4.x / Opus-4.8 model-specific prompting (verbatim)

- **Be explicit / request "above and beyond."** "Create an analytics dashboard. Include as many relevant features and interactions as possible. Go beyond the basics to create a fully-featured implementation."
- **Tool-triggering precision.** "If you say 'can you suggest some changes,' Claude will sometimes provide suggestions rather than implementing them… For Claude to take action, be more explicit" ("Change this function…").
- **Over-triggering fix.** "Claude Opus 4.5 and Claude Opus 4.6 are also more responsive to the system prompt… these models may now overtrigger. The fix is to dial back any aggressive language. Where you might have said 'CRITICAL: You MUST use this tool when...', you can use more normal prompting like 'Use this tool when...'."
- **Parallel tool calls.** "Claude's latest models run independent tool calls in parallel… you can boost this to ~100%" with a `<use_parallel_tool_calls>` block: "If you intend to call multiple tools and there are no dependencies between the tool calls, make all of the independent tool calls in parallel."
- **Thinking = adaptive.** "Claude Opus 4.6, 4.7, 4.8, and Sonnet 4.6 use adaptive thinking (`thinking: {type: 'adaptive'}`), where Claude dynamically decides when and how much to think… calibrated based on the `effort` parameter and query complexity." "In internal evaluations, adaptive thinking reliably drives better performance than extended thinking." `budget_tokens` is deprecated: "On Claude Opus 4.7 and later models, and on Claude Fable 5 and Claude Mythos 5, setting `budget_tokens` returns a 400 error." Use `effort` (the `output_config.effort` levels) or `max_tokens`.
- **Reduce file creation / overeagerness / hard-coding** — explicit anti-overengineering snippets ("Avoid over-engineering. Only make changes that are directly requested or clearly necessary."), anti-hardcode ("Implement a solution that works correctly for all valid inputs, not just the test cases.").
- **Minimize hallucinations (agentic coding):** `<investigate_before_answering>` "Never speculate about code you have not opened. If the user references a specific file, you MUST read the file before answering."
- **Long-horizon / multi-window state:** "Have the model write tests in a structured format" (e.g. `tests.json`); "It is unacceptable to remove or edit tests because this could lead to missing or buggy functionality"; "Use git for state tracking." Context-awareness compaction prompt provided.

## A5. Anthropic Console prompt tooling + versioning (verbatim, platform.claude.com)

- **Prompt generator** — "guides Claude to create high-quality prompt templates tailored to your specific tasks, following many of our prompt engineering best practices… particularly useful for solving the 'blank page problem'." (Meta-prompt; powered by Claude Sonnet 4.5.)
- **Prompt templates and variables** — placeholders are `{{double brackets}}`. Benefit list includes **Version control:** "Easily track changes to your prompt structure over time by keeping tabs only on the core part of your prompt, separate from dynamic inputs." Use "when you expect any part of your prompt to be repeated in another call."
- **Prompt improver** — 4 steps: "Example identification → Initial draft (structured template with XML tags) → Chain of thought refinement → Example enhancement." Output adds "Detailed chain-of-thought instructions… Clear organization using XML tags… Standardized example formatting… Strategic prefills." Best for "Complex tasks requiring detailed reasoning."
- **Evaluation tool** does prompt versioning: "**Prompt versioning**: Create new versions of your prompt and re-run the test suite to quickly iterate and improve results."

## A6. OpenAI prompt engineering (developers.openai.com)

- **Strategies:** few-shot ("a handful of input/output examples in the prompt"), RAG ("additional relevant context"), **message formatting** via Markdown headers + XML tags to "help the model understand logical boundaries of your prompt and context data."
- **Message-role authority hierarchy (3-tier):** **Developer messages** = "Instructions provided by the application developer, prioritized ahead of user messages." **User messages** = "prioritized behind developer messages." Mental model: "a function and its arguments in a programming language" — developer messages = the function definition (rules), user messages = the arguments (inputs). (`developer` role superseded the old `system` role for chain-of-command.)
- **Prompt caching structure:** "keep content that you expect to use over and over in your API requests at the beginning of your prompt" and among the first JSON parameters in your request.

## A7. OpenAI GPT-5 prompting guide (cookbook.openai.com) — verbatim

- **Agentic eagerness — lower:** "Switch to a lower `reasoning_effort`. This reduces exploration depth but improves efficiency and latency." **higher / persistence:** "You are an agent - please keep going until the user's query is completely resolved, before ending your turn and yielding back to the user."
- **`reasoning_effort`:** three tiers, `"medium"` default; "**Minimal reasoning effort**" introduced as the fastest. "minimal reasoning performance can vary more drastically depending on prompt than higher reasoning levels."
- **Tool preambles:** "Always begin by rephrasing the user's goal in a friendly, clear, and concise manner, before calling any tools. Then, immediately outline a structured plan."
- **Instruction precision + the contradiction trap:** GPT-5 follows instructions with "surgical precision," BUT "**poorly-constructed prompts containing contradictory or vague instructions can be more damaging to GPT-5 than to other models**" — the model "expend[s] reasoning tokens… trying to reconcile the contradiction."
- **Responses API reasoning persistence:** "we observed Tau-Bench Retail score increases from **73.9% to 78.2%** just by switching to the Responses API and including `previous_response_id`."
- **Metaprompting:** success "using GPT-5 as a meta-prompter for itself" — ask it what phrases to add/remove from an underperforming prompt. (Plus the **GPT-5 Prompt Optimizer** in the Playground.)
- **Structure:** XML-like `<instruction_spec>` tags; markdown only where semantically correct.

## A8. OpenAI reasoning best practices (developers.openai.com) — verbatim

- "Keep it simple: The models excel at understanding and responding to brief, clear instructions."
- "**Avoid chain-of-thought framing:** Reasoning models perform internal reasoning, so prompting them to 'think step by step' is unnecessary and can reduce performance." (DIVERGES from Anthropic non-thinking-mode CoT advice.)
- "**Use developer messages, not system messages**" (since `o1-2024-12-17`).
- "**Start with zero-shot:** Reasoning models often don't need few-shot examples to produce good results."
- Cost: use the Responses API with `store=true` + pass previous reasoning items "to avoid redundant computation."

## A9. PROMPT-AS-ARTIFACT + VERSIONING — the strongest cross-vendor convergence (verbatim)

OpenAI is **deprecating reusable prompt objects** and telling developers to put prompts in code:
- "**Prompt creation will be de-emphasized beginning June 3, 2026, and `v1/prompts` is scheduled to shut down on November 30, 2026.**"
- "Store production prompts in your application code instead of creating reusable prompt objects" — this enables "typed inputs, code review, tests, and your normal deployment process."
- "**Move versioning to your repo using git commits, PR review, and tests or evals.**"
- "**Replace prompt variables with function arguments so dynamic values are explicit and typed.**"
- Recommended pattern: "**Create a small `prompts/` module, keep each prompt as a named builder function, and add lightweight eval fixtures so prompt changes are reviewed like product logic.**" / "prompt changes go through the same review and release process as product logic."

(The legacy reusable prompt object: `prompt: { id: "pmpt_123", version, variables }` referenced in the
Responses API — being phased out.)

This is the literal statement of aspect-27's "prompts are source code" bullet, now from BOTH vendors.

---

# PART B — EVALS

## B1. Anthropic "Define success criteria and build evaluations" (platform.claude.com) — verbatim

**Eval design principles:**
1. "**Be task-specific:** Design evals that mirror your real-world task distribution. Don't forget to factor in edge cases!"
2. "**Automate when possible:** Structure questions to allow for automated grading (e.g., multiple-choice, string match, code-graded, LLM-graded)."
3. "**Prioritize volume over quality:** More questions with slightly lower signal automated grading is better than fewer questions with high-quality human hand-graded evals."

**Success criteria** = Specific · Measurable · Achievable · Relevant. Example (verbatim): "Our sentiment
analysis model should achieve an F1 score of at least 0.85 on a held-out test set of 10,000 diverse Twitter
posts, which is a 5% improvement over our current baseline." "Most use cases will need multidimensional
evaluation."

**Three grading methods — "choose the fastest, most reliable, most scalable method":**
1. "**Code-based grading:** Fastest and most reliable, extremely scalable, but also lacks nuance" (exact match `output == golden_answer`; string match `key_phrase in output`).
2. "**Human grading:** Most flexible and high quality, but slow and expensive. Avoid if possible."
3. "**LLM-based grading:** Fast and flexible, scalable and suitable for complex judgement. Test to ensure reliability first then scale."

**LLM-judge tips (verbatim):** "Have detailed, clear rubrics." "Empirical or specific" (output only
'correct'/'incorrect' or 1–5). "**Encourage reasoning:** Ask the LLM to think first before deciding an
evaluation score, and then discard the reasoning. This increases evaluation performance." Grader-prompt
pattern: "Think through your reasoning in `<thinking>` tags, then output 'correct' or 'incorrect' in
`<result>` tags." Note: "Generally best practice to use a different model to evaluate than the model used to
generate the evaluated output."

Eval-type catalog shown: exact match · cosine similarity (SBERT) · ROUGE-L · LLM Likert (1–5) · LLM binary
classification · LLM ordinal scale.

## B2. Anthropic Console Evaluation tool (platform.claude.com) — verbatim

- Requires "at least 1-2 dynamic variables using the double brace syntax: `{{variable}}`" to create eval sets.
- Test-case creation: "+ Add Row" manual · "**Generate Test Case**" (Claude auto-generates, one row per click; editable "generation logic") · "Import test cases from a CSV file."
- "**Side-by-side comparison**: Compare the outputs of two or more prompts to quickly see the impact of your changes."
- "**Quality grading**: Grade response quality on a **5-point scale** to track improvements in response quality per prompt."
- "**Prompt versioning**: Create new versions of your prompt and re-run the test suite to quickly iterate."
- "If you update your original prompt text, you can re-run the entire eval suite against the new prompt."

## B3. Anthropic "A statistical approach to model evals" (anthropic.com/research, Evan Miller, Nov 2024) — 5 recs

1. **SEM / Central Limit Theorem:** "report the SEM, derived from the Central Limit Theorem, alongside each calculated eval score" to measure underlying skill independent of question-selection variance.
2. **Clustered standard errors:** for non-independent questions, cluster "on the unit of randomization (for example, passage of text)"; "**clustered standard errors on popular evals can be over three times as large as naive standard errors.**"
3. **Reduce within-question variance:** CoT evals — "resampling answers from the same model several times, and using the question-level averages as the question scores"; deterministic — use "next-token probabilities."
4. **Paired-differences analysis** (not two-sample): question-score correlation between frontier models "ranges from 0.3 and 0.7," making paired tests a powerful variance reducer.
5. **Power analysis:** "calculate the number of questions that an eval should have" to test a hypothesis (e.g. Model A beats Model B by X%) reliably. (Paper: "Adding Error Bars to Evals", arXiv:2411.00640.)

## B4. Anthropic "Demystifying evals for AI agents" (anthropic.com/engineering, 2026) — verbatim

- **Evals encode the spec:** "two engineers reading the same initial spec could come away with different interpretations on how the AI should handle edge cases" → "An eval suite resolves this ambiguity." Useful "at the start of agent development to explicitly encode expected behavior."
- **Good task:** "A good task is one where two domain experts would independently reach the same pass/fail verdict." Tasks must be solvable — "a 0% pass rate across many trials typically signals a broken task, not incapable agents."
- **Start small:** begin with "**20-50 simple tasks drawn from real failures**" rather than waiting for hundreds; early development has "large effect size" so small samples suffice.
- **Balanced problem sets:** test "both where behaviors *should* and *shouldn't* occur."
- **Three grader types:** Code-based (fast/cheap/objective, brittle) · Model-based (flexible/scalable, non-deterministic, needs calibration) · Human (gold standard, expensive/slow). "**LLM-as-judge graders should be closely calibrated with human experts.**"
- **Metrics:** **pass@k** = "the likelihood that an agent gets at least one correct solution in k attempts"; **pass^k** = "the probability that all k trials succeed" — "critical for customer-facing agents."
- **Grade outcomes, not trajectory:** "it's often better to grade what the agent produced, not the path it took" (avoid punishing valid alternative approaches). Build **partial credit**: "A support agent that correctly identifies the problem and verifies the customer but fails to process a refund is meaningfully better than one that fails immediately."
- **READ TRANSCRIPTS:** "You won't know if your graders are working well unless you read the transcripts and grades from many trials." Teams should "sample transcripts to read weekly."
- **Eval saturation:** at ~100% pass rates, "eval saturation" "provides no signal for improvement."
- **Lifecycle:** Pre-launch automated evals in CI/CD → production monitoring/drift → A/B testing with traffic → user feedback / transcript review (ongoing).

## B5. OpenAI Evals (developers.openai.com) — verbatim

- "**Evaluations (often called evals) test model outputs to ensure they meet style and content criteria that you specify.**" Behavior-driven: describe behavior → implement → test.
- **3-step:** describe task as an eval config → run with test inputs → analyze + iterate.
- **Data source config:** JSON Schema; templating `{{ item.property }}` (test data) + `{{ sample.output_text }}` (model output); upload as JSONL.
- Works "via API or the OpenAI dashboard."

## B6. OpenAI grader types (developers.openai.com/graders) — verbatim list

| Grader | What it does (verbatim) | Ops / metrics |
|---|---|---|
| **String Check** | "return a 0 or 1" exact/substring | `eq`, `neq`, `like`, `ilike` |
| **Text Similarity** | closeness to reference | `fuzzy_match`, `bleu`, `gleu`, `meteor`, `cosine`, `rouge_1`…`rouge_5`, `rouge_l` |
| **Score Model** | "take the input and return a numeric score based on the prompt within the given range" (LLM judge) | range-scored |
| **Label Model** | classifies outputs into categories (LLM classifier) | label set |
| **Python** | "arbitrary python code to grade the model output" | returns float |
| **Multigrader** | "Combines the output of multiple graders to produce a single score" | weighted formula |

## B7. OpenAI agent evals / trace grading (developers.openai.com) — verbatim

- "**Trace grading is the fastest way to identify workflow-level issues.**" A trace = "the end-to-end record of model calls, tool calls, guardrails, and handoffs for one run"; graders "score those traces with structured criteria so you can find regressions and failure modes at scale."
- Trace grading answers: did the agent select the right tools? did handoffs occur as intended? did a workflow violate instructions/safety? did a prompt/routing change improve end-to-end behavior?
- Progression: trace inspection (establish expectations) → datasets + eval runs (repeatability, benchmarking, systematic prompt-variation comparison).
- Cookbook: "Build an Agent Improvement Loop with Traces, Evals, and Codex" — "keeps traces, reviewer judgment, generated evals, optimization, and implementation handoff inside one runnable improvement loop." Online (production, real-time) + offline (batch) eval.

---

# PART C — CROSS-VENDOR CONVERGENCE / DIVERGENCE

**CONVERGE:**
- **Prompts = source code.** Both vendors now say store prompts in the repo, versioned by git/PR, eval-gated. OpenAI is actively *deprecating* its managed prompt objects (`v1/prompts` shutdown Nov 30 2026) → "Create a small `prompts/` module… named builder function… lightweight eval fixtures." Anthropic frames templates+variables as enabling "Version control… separate from dynamic inputs."
- **Eval-first / spec-as-eval.** Anthropic: evals "encode expected behavior" at the start; OpenAI: evals are "behavior-driven development." Both: start small (Anthropic 20-50 real-failure tasks), automate grading, iterate.
- **Grader taxonomy is the same three classes** (code / LLM-judge / human), same trade-offs, same LLM-judge calibration warning, same "encourage reasoning then discard" + "different model to grade" tips.
- **CI/CD regression evals + production monitoring + A/B + transcript review** lifecycle is shared.
- **Outcome > trajectory grading** for agentic/multi-turn (Anthropic explicit; OpenAI trace-grading scores outcomes/tool-selection).
- **Structure with tags/markdown; be explicit; give context.**

**DIVERGE:**
- **Prefill:** Anthropic deprecated last-turn prefill (400 error) on Claude 4.6+; was a core technique. OpenAI never had it (uses developer-message + structured output).
- **CoT prompting:** Anthropic still recommends manual `<thinking>`/`<answer>` CoT *when thinking is off*; OpenAI says **do not** "think step by step" a reasoning model ("can reduce performance"). Both agree: with native thinking/reasoning on, prefer general instructions over prescriptive steps.
- **Role nomenclature:** Anthropic = `system` + `user` (+`assistant`); OpenAI = `developer` (superseded `system`) + `user`, with an explicit instruction-authority hierarchy.
- **Thinking control:** Anthropic `effort` (+ adaptive thinking, `budget_tokens` deprecated/400); OpenAI `reasoning_effort` (minimal/low/medium/high) + Responses-API `previous_response_id` reasoning persistence.
- **Managed eval UI:** Anthropic Console Evaluation tool (generate test cases, 5-point grade, prompt versions) vs OpenAI Evals API/dashboard + trace grading + Prompt Optimizer.
