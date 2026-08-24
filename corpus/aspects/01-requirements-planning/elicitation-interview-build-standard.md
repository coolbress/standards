---
id: aspect-01-requirements-planning--elicitation-interview-build-standard
title: "Requirements-elicitation interview engine — the build standard (US-2 'Elicit')"
parent: aspect-01-requirements-planning
kind: reference
evidence_track: census+lit
status: review-needed
last_updated: "2026-06-27"
method: "Broad-spectrum survey (2026-06-27) across SEVEN families, not just AI-spec tools: AI-native spec tools (Spec-Kit/Kiro/BMAD) · customer-discovery interviewing (The Mom Test/JTBD/Continuous Discovery) · classic RE (Gause-Weinberg/Volere/elicitation surveys) · goal-oriented RE (KAOS/i*/Opportunity-Solution-Tree) · the LLM clarifying-question mechanism (information-gain/uncertainty/ask-before-plan) · spec notation (EARS/Gherkin-BDD/Example-Mapping) · forcing functions (Amazon Working-Backwards PR/FAQ). Defines HOW to build gingoa's US-2 elicitation feature to the minimum bar AND to optimize it. Complements the AI-agentic prior-art in elicitation-prior-art.md."
---

# Requirements-elicitation interview engine — the build standard

gingoa's **US-2 (Elicit)** turns a non-engineer's idea into a rigorous, locked requirements document by
INTERVIEWING. It automates the ① planning stage for a user's project. This is the build standard, drawn from
seven prior-art families — the key insight being that a naive "ask some questions → write a PRD" machine misses
three whole layers (interview *style*, principled question *selection*, structural *completeness*).

## The seven prior-art families (what each contributes)

| Family | Sources | Build ingredient it contributes |
|---|---|---|
| **A. AI-native spec tools** | Spec-Kit · Kiro · BMAD-METHOD | `[NEEDS CLARIFICATION]` don't-guess marker + checklist-as-"unit-tests-for-English" lock-gate (Spec-Kit); EARS-structured requirements + analyze-for-gaps (Kiro); **multi-AGENT pipeline** Analyst→PM→Architect (BMAD) |
| **B. Customer-discovery interviewing** | The Mom Test · JTBD Switch Interview (Moesta) · Continuous Discovery (Torres) | **Interview STYLE layer (most-missed):** talk about their life/**past specifics**, never your idea or **hypotheticals**; listen 80% — "every word you speak is bias." Frame around the **job/progress** (4 forces: push/pull/anxiety/habit). Collect **stories, not opinions**; discover opportunities, not solutions. |
| **C. Classic RE** | Gause-Weinberg context-free questions · Volere (Robertson) · Zowghi-Coulin survey | **Context-free question set** (process/product/meta) that opens any project; the Volere **fit criterion** — every requirement carries a measurable "how we'll know it's met." |
| **D. Goal / opportunity decomposition** | KAOS · i* · Tropos (GORE) · Opportunity-Solution-Tree | Refine goals via **AND/OR**; **obstacle (anti-goal) analysis** = goal-driven fault-tree — derive requirements from *what can go wrong* (the unhappy-path completeness a category checklist misses). |
| **E. LLM clarifying-question mechanism** | Active Task Disambiguation (Bayesian Experimental Design) · Structured-Uncertainty Clarification (arXiv 2511.08798) · Ask-before-Plan · Modeling-Future-Turns (arXiv 2410.13788) | **Principled "which question next":** pick the question with **maximum expected information gain** (sample the solution space). **When** to ask = uncertainty estimate; **stop** when further questions yield ~no utility (the ambiguity threshold, made rigorous). |
| **F. Spec notation (the locked output)** | EARS (Mavin, RE'09) · Gherkin/BDD Given-When-Then · Example Mapping + Three Amigos (Spec by Example, Adzic) | Write acceptance criteria as **machine-parseable templates** (EARS `WHEN/IF/WHILE…SHALL`, 5 patterns; or Gherkin GWT). Example Mapping's **"questions" pile = the clarification backlog**; concrete **examples** beat abstract prose. |
| **G. Forcing functions** | Amazon Working-Backwards **PR/FAQ** | Write the future press-release + FAQ FIRST as a customer-clarity forcing function. **Internal FAQ = every-department question sweep** → a stakeholder-completeness checklist. |

## The distilled US-2 build recipe (what to take from the full spectrum)

| Layer | From | gingoa US-2 mechanism |
|---|---|---|
| Question **style** | Mom Test | No leading / no hypothetical questions; ground in **past, specific** behaviour (a non-engineer polite-lies otherwise) |
| Question **selection** | info-gain research (E) | Next question = **max expected information gain** — the rigorous form of gingoa's "measured-not-felt adaptive depth" |
| **Framing** | JTBD / OST | Job/opportunity first ("what are you trying to make progress on, and what blocks it?") before features |
| **Coverage / completeness** | GORE obstacles + ISO-25010 + Working-Backwards Internal-FAQ | nine quality axes **+ anti-goals (what can go wrong) + per-stakeholder sweep** |
| **Architecture** | BMAD | multi-agent **Interviewer / Analyst / Skeptic** — aligns with the operating model (model-proposes · gates-demand-evidence · review-breaks-claims) |
| **Output notation** | EARS + Volere fit-criterion + Gherkin examples | acceptance criteria in EARS (or GWT) + a fit criterion per requirement (replaces prose) |
| Don't-guess + **lock-gate** | Spec-Kit | `[NEEDS CLARIFICATION]` markers during; lock only when markers = 0, every req 29148-clean + EARS-testable, every ISO-25010 axis addressed, risk zones resolved |
| **Risk gate** | gingoa ADR-0012 (the differentiator) | depth adapts to risk; payments/PII/public-exposure **hard-stop** → expert-mode opt-in (Spec-Kit/Kiro have no risk gate) |
| **Eval** | ReqElicitGym (interview competence) + eval-first | a `(idea → gold requirements)` case set grades the interviewer + prevents regression |

## Three insights the narrow view (Spec-Kit/Kiro/EARS only) misses
1. **Interview STYLE is its own layer.** Without the Mom-Test anti-bias discipline a non-engineer polite-lies and the PRD is garbage-in. Spec-Kit/Kiro have no such layer.
2. **"Which question next" is a solved research problem** — expected-information-gain question selection is the mathematical basis for adaptive depth (don't hand-wave it).
3. **Completeness comes from structure, not a flat checklist** — obstacle/anti-goal analysis + a per-stakeholder (Internal-FAQ) sweep surface far more than "did we cover the categories."

## How gingoa builds US-2 (concrete)
A multi-agent loop: **Interviewer** asks (Mom-Test style, info-gain-selected, JTBD-framed; **≤2 questions/turn with
full serial context** — each question sees all prior answers, iReDev) ↔ **Analyst** attaches `[NEEDS CLARIFICATION]`,
measures ambiguity/coverage over {functional · 9 NFR · scope · constraints · assumptions · risks · anti-goals ·
stakeholders}, runs the **risk classifier** (ADR-0012). Loop until ambiguity-threshold + 0 markers (**risk-adjusted
depth ≈ 8 / 12 / 18 turns, ~15–20 cap** — iReDev/AIRE; not a fixed list, not a 30-turn marathon); high-risk → hard-stop. Emit **EARS/GWT acceptance + fit-criterion + traceability ID** per requirement into
`prd.yml` (SSOT) → `PRD.md`. **Lock-gate** = checklist-as-unit-tests (markers 0 · 29148-clean · ISO-25010 complete ·
risks resolved) → `status: locked`. An **eval case set** grades competence. Each emitted requirement is traceable
(→ ADR/design → acceptance test), per [`requirements-engineering-craft.md`](requirements-engineering-craft.md).

## Empirical evidence + notation alternatives (2024–2026 augmentation)
The method is empirically supported (not just argued):
- **Elicitron** (Autodesk, ASME JCISE 2025) — generate *diverse simulated users* as LLM agents, run each through a
  simulated product experience, then interview them → surfaces **latent needs** the real-user interview misses. A
  concrete technique for the tacit-knowledge layer, beyond questioning the one real user. [lit] arXiv 2404.16045
- **LLMREI** (RE'25) — an LLM elicitation-interview chatbot makes ~human-level mistakes and elicits **up to 73.7%**
  of requirements across 33 simulated interviews (zero-shot vs least-to-most prompting won; fine-tuning lost). A
  realistic competence baseline + a prompting-strategy signal. [lit] arXiv 2507.02564
- **Follow-Up Question Generation** (RE'25) — GPT-4o follow-ups match human quality, and **beat human when GUIDED by
  a framework of common interviewer mistakes** — direct empirical validation of feeding the interviewer a
  Mom-Test-style mistake rubric (do this, don't just hope). [lit] arXiv 2507.02858
- **ReqElicitGym** — the interview-competence benchmark to grade/regress the interviewer. [lit] arXiv 2602.18306

**Acceptance-notation is a researched choice, not the only option.** EARS is the simplest + most-adopted controlled-NL
template; **MASTeR / Rupp** (the IREB de-facto standard) is more expressive (FR/NFR/conditional patterns) for
requirements EARS can't cleanly state; **Adv-EARS · Boilerplates · SPIDER** also exist; a controlled benchmark
(Springer RE journal) compares them — all cut ambiguity vs free text. gingoa picks **EARS** (simplicity +
AI-parseability) and **escalates to MASTeR/Rupp for requirements that resist EARS**. The PRD's section structure
aligns with the **ISO-29148 SRS** triad (Introduction · Overall-Description · Specific-Requirements). [lit]

## Sources
Elicitron (Autodesk/ASME, arXiv 2404.16045) https://arxiv.org/abs/2404.16045 · LLMREI (RE'25, arXiv 2507.02564) https://arxiv.org/abs/2507.02564 ·
Follow-Up Question Generation (RE'25, arXiv 2507.02858) https://arxiv.org/abs/2507.02858 · Rupp/MASTeR + requirement-template benchmark (Springer RE) https://link.springer.com/article/10.1007/s00766-024-00427-0 ·
ISO/IEC/IEEE 29148 SRS template https://www.reqview.com/doc/iso-iec-ieee-29148-templates/ · EARS empirical (template comparison) https://link.springer.com/article/10.1007/s42979-025-03843-3 ·
The Mom Test (Fitzpatrick) https://mtlynch.io/book-reports/the-mom-test/ · JTBD Switch Interview / 4 forces (Moesta)
https://jobstobedone.org/ · Continuous Discovery + Opportunity-Solution-Tree (Torres) https://www.producttalk.org/opportunity-solution-tree/ ·
Gause-Weinberg context-free questions + Volere — RE survey (Zowghi-Coulin) https://doi.org/10.1007/3-540-28244-0_2 ·
Volere https://www.volere.org/ · GORE / KAOS (van Lamsweerde) https://webperso.info.ucl.ac.be/~avl/gore.php ·
Active Task Disambiguation / info-gain clarification — Structured-Uncertainty (arXiv 2511.08798) https://arxiv.org/html/2511.08798v1 ·
Modeling-Future-Turns to teach clarifying questions (arXiv 2410.13788) https://arxiv.org/html/2410.13788v1 ·
EARS (Mavin, RE'09) https://alistairmavin.com/ears/ · Specification by Example / Example Mapping / Three Amigos
https://johnfergusonsmart.com/three-amigos-requirements-discovery/ · Amazon Working-Backwards PR/FAQ https://workingbackwards.com/concepts/working-backwards-pr-faq-process/ ·
BMAD-METHOD https://github.com/bmad-code-org/BMAD-METHOD · GitHub Spec-Kit https://github.com/github/spec-kit/blob/main/spec-driven.md ·
AWS Kiro Specs https://kiro.dev/docs/specs/ · ReqElicitGym (interview competence, arXiv 2602.18306) https://arxiv.org/abs/2602.18306 ·
GenAI for RE — systematic review (arXiv 2409.06741) https://arxiv.org/abs/2409.06741
