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
| **B. Customer-discovery interviewing** | The Mom Test · JTBD Switch Interview (Moesta) · Continuous Discovery (Torres) | **Interview STYLE layer (most-missed):** talk about their life/**past specifics**, never your idea or **hypotheticals**; talk less and listen more. ⚠️ **2026-08-25 배치 5 (ELI-006)**: *"80%"* 라는 수치와 *"every word you speak is bias"* 라는 **따옴표 인용은 1차 출처로 확인되지 않았다** — 코퍼스가 출처로 단 것은 책이 아니라 **제3자 서평**이고, 그 서평에도 둘 다 없다. 규칙 자체는 널리 확인되므로 유지하되 **수치와 인용부호는 내린다.** Frame around the **job/progress** (4 forces: push/pull/anxiety/habit). Collect **stories, not opinions**; discover opportunities, not solutions. |
| **C. Classic RE** | Gause-Weinberg context-free questions · Volere (Robertson) · Zowghi-Coulin survey | **Context-free question set** (process/product/meta) that opens any project; the Volere **fit criterion** — every requirement carries a measurable "how we'll know it's met." |
| **D. Goal / opportunity decomposition** | KAOS · i* · Tropos (GORE) · Opportunity-Solution-Tree | Refine goals via **AND/OR**; **obstacle (anti-goal) analysis** = goal-driven fault-tree — derive requirements from *what can go wrong* (the unhappy-path completeness a category checklist misses). |
| **E. LLM clarifying-question mechanism** | Active Task Disambiguation (Bayesian Experimental Design) · Structured-Uncertainty Clarification (arXiv 2511.08798) · Ask-before-Plan · Modeling-Future-Turns (arXiv 2410.13788) | **Principled "which question next":** pick the question with **maximum expected information gain** (sample the solution space). **When** to ask = uncertainty estimate; **stop** when further questions yield ~no utility (the ambiguity threshold, made rigorous). |
| **F. Spec notation (the locked output)** | EARS (Mavin, RE'09) · Gherkin/BDD Given-When-Then · Example Mapping + Three Amigos (Spec by Example, Adzic) | Write acceptance criteria as **machine-parseable templates** (EARS; or Gherkin GWT). ⚠️ **2026-08-25 배치 5 (ELI-005) 정정 — 패턴은 5개가 아니라 6개**이고 키워드에 **`WHERE`** 가 빠져 있었다: Ubiquitous(키워드 없음) · State driven `While` · Event driven `When` · Optional feature `Where` · Unwanted behaviour `If…Then` · Complex(조합). Example Mapping's **"questions" pile = the clarification backlog**; concrete **examples** beat abstract prose. |
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
depth ≈ 8 / 12 / 18 turns, ~15–20 cap**; not a fixed list, not a 30-turn marathon). 🔴 **2026-08-25 배치 5 (ELI-004) 출처 철회 — `8 / 12 / 18` 은 iReDev 에도 AIRE 에도 없다.** 두 검증자가 독립으로 확인했다: iReDev 에는 턴 수 상한도 위험 비례 깊이 규칙도 없고, AIRE_03 은 **교육용 인터뷰 스크립트 생성** 연구다. `~15–20` 만 AIRE 원문에 있는데 그마저 *"we aim to include approximately **15 to 20 turns in the script**"* — **생성할 스크립트의 목표 길이**이지 실제 인터뷰의 측정된 상한이 아니다. **세 숫자는 프로젝트 판단이다.**; high-risk → hard-stop. Emit **EARS/GWT acceptance + fit-criterion + traceability ID** per requirement into
`prd.yml` (SSOT) → `PRD.md`. **Lock-gate** = checklist-as-unit-tests (markers 0 · 29148-clean · ISO-25010 complete ·
risks resolved) → `status: locked`. An **eval case set** grades competence. Each emitted requirement is traceable
(→ ADR/design → acceptance test), per [`requirements-engineering-craft.md`](requirements-engineering-craft.md).

## Empirical evidence + notation alternatives (2024–2026 augmentation)
The method is empirically supported (not just argued):
- **Elicitron** (Autodesk, ASME JCISE 2025) — generate *diverse simulated users* as LLM agents, run each through a
  simulated product experience, then interview them → surfaces **latent needs** the real-user interview misses. A
  concrete technique for the tacit-knowledge layer, beyond questioning the one real user. [lit] arXiv 2404.16045
- **LLMREI** (RE'25) — an LLM elicitation-interview chatbot makes ~human-level mistakes and elicits **up to 73.7%**
  of requirements across 33 simulated interviews — ⚠️ **2026-08-25 배치 5 (ELI-002): 73.7% 는 완전 도출 60.94% + 부분 도출 12.76% 의 합이다.** 완전 도출만 보면 **60.94%** 이고, 참가자는 대부분 학생이다 (zero-shot vs least-to-most prompting won; fine-tuning lost). A
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

## Claim table — 기획 인터뷰의 근거 (배치 5 · 1차 출처 직접 확인 2026-08-25)

이 행들은 [`direction/03`](../../../direction/03-what-research-says.md) *"기획은 어떻게 이끄나"* 절과
만들 것 ④ [`/kickoff`](https://github.com/coolbress/workflows/blob/main/commands/kickoff.md) 를 떠받친다.

| Claim ID | Class | Claim and scope | Evidence | Confidence | 재검증 |
|---|---|---|---|---|---|
| ELI-001 | empirical | ⭐ **흔한 실수 목록을 쥐여주면 LLM 후속질문이 사람을 이긴다 — 통제실험 2개.** 원문 그대로: *"the LLM-generated questions are **no worse than** the human-authored questions with respect to clarity, relevancy, and informativeness"*, 그리고 *"LLM-generated questions **outperform** human-authored questions **when guided by common mistakes types**."* 설계는 *"a controlled experiment"* + *"a second controlled experiment"* 다. → **이것이 `/kickoff` 에 실수 목록을 넣은 이유이고, 근거는 예상보다 강하다** | `FOLLOWUP-QGEN-RE25` | high | 2026-08-25 |
| ELI-002 | empirical | **LLM 인터뷰어의 도출률 기준선은 완전 60.94% · 부분 12.76%(합 73.7%)다.** 원문 그대로: *"LLMREI was able to **completely elicit up to 60.94%** of all requirements and **partially elicit up to 12.76%** (in total 73.7%)."* ⚠️ **`73.7%` 만 쓰면 3분의 1이 *부분* 도출이라는 사실이 가려진다.** 표본은 **33건의 모의 인터뷰**이고 참가자는 대부분 학생 — 저자 스스로 표본 크기를 한계로 든다 | `LLMREI-2025` | medium-high | 2026-08-25 **수치 분해** |
| ELI-003 | vendor-behavior | **턴당 ≤2문항 — 출처는 실재하고 인용도 맞다.** iReDev 의 Interviewer Agent 프로파일(Fig. 3): *"**Limit each question turn to no more than two questions** to maintain a natural conversational flow."* LLMREI 도 독립적으로 같은 조정을 했다(*"one question at a time or only ask two questions if it is about one specific topic"*). ⚠️ **다만 둘 다 프롬프트 설계 선택이지 비교 측정된 파라미터가 아니다** — 두 팀이 수렴했다는 것이 근거의 전부다 | `IREDEV-2025`; `LLMREI-2025` | medium | 2026-08-25 |
| ELI-004 | synthesis | 🔴 ***"위험별 깊이 8 / 12 / 18턴"* 은 출처가 없다.** 인용해 온 두 논문 어디에도 없다 — iReDev 에는 **턴 수 상한도 위험 비례 깊이 규칙도 없고**(*"multi-round dialogue"* 까지다), AIRE_03 은 **교육용 인터뷰 스크립트를 생성**하는 연구다. `~15–20` 만 AIRE 원문에 있으나 *"we aim to include approximately **15 to 20 turns in the script**"* — **생성물의 목표 길이**이지 인터뷰 깊이의 측정치가 아니다. → **세 숫자는 프로젝트 판단으로 재분류**한다. ⚠️ **2026-08-25 대체 근거 탐색도 실패** — 인터뷰 깊이의 **정지 기준·포화를 실증한 연구를 찾지 못했다** ([`evidence-holes-register`](../../methods/evidence-holes-register.md) EVH-004) | `IREDEV-2025`; `AIRE-SCRIPTGEN-2023` | high (반증) | 2026-08-25 **출처 철회** |
| ELI-005 | definition | **EARS 패턴은 5개가 아니라 6개다.** 표기법 저자 본인의 페이지 기준: Ubiquitous(키워드 없음) · State driven **`While`** · Event driven **`When`** · Optional feature **`Where`** · Unwanted behaviour **`If…Then`** · Complex(둘 이상 조합). 이 코퍼스와 `direction/03` 은 **5개**라 적고 키워드 목록에서 **`Where` 를 빠뜨렸다.** ⚠️ 또한 이 페이지는 *"reduces or even eliminates common problems"* 라 주장할 뿐 **모호성 감소의 실증을 제시하지 않는다** — 그 근거는 별도 Springer 벤치마크다 | `EARS-MAVIN` | high | 2026-08-25 **수정** |
| ELI-007 | empirical | ⭐ **2026-08-25 신규 — *"흔한 실수 목록"* 에는 독립된 분류가 둘 있다.** ⓐ **RE'25 후속질문 연구는 외부 프레임워크를 가져오지 않는다 — 자체 종합이다**: 14편의 선행연구에서 **28기준을 뽑아 14기준 · 2범주**(후속질문 · 질문 구성)로 좁혔다. ⓑ 별개로 **Bano et al. 2019** 가 **34개 실수 · 7개 테마**(질문 구성 · 질문 누락 · 인터뷰 순서 · 의사소통 · 분석가 행동 · 고객 응대 · 팀워크와 계획)를 관찰로 분류했다. → **④ `/kickoff` 의 실수 목록은 인용할 분류가 있다.** ⚠️ 한정: ⓐ 는 저자 종합이고, ⓑ 표본은 **학생 역할극**(110명/28조 → 138명/34조)이지 실무 인터뷰가 아니다 | `FOLLOWUP-QGEN-RE25`; `INTERVIEW-MISTAKES-BANO-2019` | medium-high | 2026-08-25 **신규** |
| ELI-006 | synthesis | ⚠️ **Mom Test 의 *"80% 듣기 · 'every word you speak is bias'"* 는 1차 출처로 확인되지 않았다.** 코퍼스가 단 출처는 **책이 아니라 제3자 서평**이고, 그 서평에 **수치도 그 문장도 없다.** 세 규칙(그들의 삶을 묻는다 · 미래 의견이 아니라 **과거의 구체**를 묻는다 · 말을 줄이고 듣는다)은 널리 확인되므로 **규칙은 유지**하되, **수치와 따옴표 인용은 내린다.** 원저 접근이 되면 `UNVERIFIABLE` 을 해제한다 — **1회 열람으로 해소된다** ([`evidence-holes-register`](../../methods/evidence-holes-register.md) EVH-006) | `MOMTEST-2013` | low (1차 미확인) | 2026-08-25 **`UNVERIFIABLE` 표시** |

> **배치 5 의 결론 — 기획 절은 *가장 강한 근거*와 *가장 약한 근거*를 나란히 들고 있었다.**
> **ELI-001 은 이 저장소에서 손에 꼽게 강하다** — 통제실험 두 개가 *"실수 목록을 주면 사람을 이긴다"* 를 직접 시험했다.
> `/kickoff` 가 실수 목록을 핵심으로 삼은 판단은 그대로 선다.
>
> 🔴 **반면 `8 / 12 / 18` 은 두 논문 이름을 달고 있었지만 그 논문들에 없다.** 배치 4 의 *"계획을 파일로"*(IPW-016)와
> **같은 형태**다 — 실재하는 논문을, 그 논문이 하지 않은 말의 근거로 달았다. 각주가 있어서 검증돼 보였을 뿐이다.
> 이 두 건이 연속으로 나왔다는 것은 **`direction` 의 인용 습관 자체에 계통 오차가 있다**는 신호다.

**재검증 기록 (배치 5 · 기획)** — 검증일 `2026-08-25` · 검증자 `Claude Opus 5` + `codex-cli 0.145.0`(독립 질의, 결론 비공개) · **판정: 유지 1 · 수치 분해 1 · 한정 1 · 출처 철회 1 · 수정 1 · `UNVERIFIABLE` 1** · **불일치 없음**(Codex 가 AIRE 원문의 *"approximately 15 to 20 turns in the script"* 를 **추가로 찾아내 `~15–20` 의 진짜 출처와 그 범위를 확정**했다 — 내 1차 조사에서는 못 찾은 문장이다) · 절차 [`reverification-protocol`](../../methods/reverification-protocol.md)
