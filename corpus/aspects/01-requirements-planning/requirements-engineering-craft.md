---
id: aspect-01-requirements-planning--requirements-engineering-craft
title: "Classic requirements-engineering craft — traceability · validation · elicitation · stakeholders · DoR · prioritization"
parent: aspect-01-requirements-planning
kind: research-log
evidence_track: lit
status: review-needed
last_updated: "2026-06-27"
method: "Standards dig (2026-06-27, web-verified): SWEBOK v4 KA1, ISO/IEC/IEEE 29148:2018 §5.2.5–5.2.6, IEEE-830/29148 SRS templates, Scrum DoR, Atlassian prioritization. Fills the classic-RE craft the aspect-01 body was thin/absent on; each item = the cited standard + how gingoa's LLM-harness instantiates it."
---

# Classic requirements-engineering craft

The aspect-01 body covers elicitation (Socratic), the INVEST/NFR/29148/MoSCoW/ADR baseline, and the AI-agentic
elicitation frontier. This sub-doc fills the *classic-RE craft* that grounds them — the SWEBOK v4 KA1 activities
and the agile entry-gate/prioritization toolkit — each as the named standard **+** how gingoa's non-engineer
+ LLM harness instantiates it. These items map onto the **elicit → analyze → validate** flow the aspect names
(elicitation-technique catalogue + stakeholders feed *elicit*; ACD + prioritization feed *analyze*; traceability,
V&V, and the Definition of Ready gate enforce *validate*).

## Traceability — the spine that lets a spec change cascade
SWEBOK v4 KA1 treats **traceability** as a first-class requirements activity, and a **Requirements Traceability
Matrix (RTM)** is its standard instrument: every requirement gets a **stable ID** and **bidirectional** links —
*backward* to its source (stakeholder need / higher-tier requirement) and *forward* to the artifacts that realize
and verify it (design, code, test case). 29148:2018 §5.2.5 even lists **traceable** as a property of a well-formed
*individual* requirement. The RTM is what makes impact analysis and validation-confirmation possible: change one
requirement, follow the links, and you know exactly what design and which tests must move. **gingoa:** the
contract's `prd.yml` SSOT assigns each requirement a stable ID; the harness threads **req → ADR/design →
acceptance-test** as explicit links so that when a non-engineer revises a requirement, the change *cascades
deterministically for the agent* (regenerate the affected design/tests) instead of silently desyncing — the
machine-readable RTM is what turns "edit the spec" into a safe, traceable operation. [SWEBOK v4 KA1; Perforce RTM] [lit, normative]

## Requirements validation & verification — distinct from elicit/analyze
SWEBOK v4 KA1 makes **Requirements Validation** its own activity, separate from elicitation and analysis: confirm
the *right* requirements were captured, well-formed, before anyone builds. Named techniques: **requirements
reviews/inspection** (a reviewer group hunts errors, bad assumptions, ambiguity, standards-deviation),
**prototyping** (validate the engineer's interpretation), **model validation** (check analysis-model quality),
and **acceptance tests** — SWEBOK's rule that *each requirement be written so the finished product can be shown
to satisfy it* (i.e. **every requirement has an acceptance test**). The 29148 quality set (§5.2.5–5.2.6) is the
machine **pass-criterion** for this gate, and **cross-artifact consistency** (do the spec, design, and tasks
agree?) is part of it — GitHub Spec-Kit's `/analyze` command is the modern automation of exactly this check.
**gingoa:** validation is a real stage gate, not a vibe — the harness runs the 29148 well-formedness check as an
automated stop, demands an acceptance test per requirement (EARS / Given-When-Then), and runs a Spec-Kit-style
cross-artifact consistency pass + a post-draft adversarial review (see `elicitation-prior-art.md`) before the
contract is allowed to drive the build. [SWEBOK v4 KA1 §Requirements Validation; GitHub Spec-Kit] [lit, normative]

## Classic elicitation-technique catalogue
Before the LLM-era techniques, RE has a canonical elicitation toolkit (SWEBOK v4 KA1): **interviews** (structured/
unstructured stakeholder conversation — the traditional default), **scenarios & use cases** (give context to user
tasks; "what-if" / "how-is-this-done" framing), **facilitated workshops/meetings** (JAD-style group consensus),
**observation / ethnography** (watch real work where stakeholders can't articulate tacit needs), and **prototyping**
(clarify ambiguous requirements by giving users something concrete to react to). Each trades off cost, coverage, and
the kind of requirement it surfaces (interviews miss tacit work; observation surfaces it). **gingoa:** the harness
does not run the whole catalogue — it picks **one** instantiation suited to a non-engineer who cannot sit in a
workshop or be observed: a **Socratic, interview-first LLM dialogue** (adaptive, ≤2 questions/turn, serial context,
hidden 5W1H × {functional/NFR/constraint/risk} coverage — full design in `elicitation-prior-art.md`). The classic
catalogue is the *menu*; gingoa's chosen technique is the *dish*, deliberately scoped to the solo non-engineer. [SWEBOK v4 KA1; sdh.global elicitation-techniques] [lit, normative]

## Stakeholder identification & classification
SWEBOK v4 KA1 names **stakeholders** as a primary *source of requirements* and requires they be **identified and
classified** — because different stakeholder classes own different requirements and different acceptance authority:
**users** (who operate it) vs **buyers/customers** (who pay, set business goals) vs **operations/maintainers** (who
run it — uptime, observability) vs **regulators** (who impose compliance constraints) vs, in gingoa's world, **the
AI agent itself** (which needs unambiguous machine-readable instruction). 29148's **Stakeholder Requirements
Specification (StRS)** is the artifact that captures this source layer distinct from the system spec. **gingoa:**
this is precisely the **non-engineer's blind spot** — a solo founder naturally speaks only as the *user* and forgets
the *ops*, *buyer*, *regulator*, and *agent* viewpoints. The Socratic interview's coverage tracker explicitly probes
each stakeholder class (Who operates it? Who pays? Who must it comply with? What does the agent need stated?) so the
contract captures requirements and acceptance criteria the non-engineer didn't know were askable. [SWEBOK v4 KA1; ISO 29148 StRS via ReqView] [lit, normative]

## Definition of Ready (DoR) — the entry gate
The **Definition of Ready** is the agile **entry gate**, the mirror of the already-covered Definition of Done: a
checklist a backlog item must satisfy *before* it enters a build iteration, so work never starts on an
under-specified story. Standard DoR criteria: **INVEST satisfied**, **acceptance criteria present**,
**dependencies and assumptions resolved**, and the item **right-sized/estimable**. gingoa adds **29148-clean** to
that list (the well-formedness pass above). **gingoa:** the harness will not hand the agent a story that fails DoR —
DoR-clean is the precondition for ③ build, exactly as DoD is the precondition for "done." This closes the loop:
DoR gates entry, validation gates the contract, DoD gates exit. [Scrum.org DoR; Agile Alliance DoR] [lit]

## Prioritization beyond MoSCoW — RICE + Kano
MoSCoW (in the aspect body) **filters** the MVP cut (Must/Should/Could/Won't) but does not *rank within* a class or
explain *why* a feature matters. Two complementary frameworks fill that: **RICE** = Reach × Impact × Confidence ÷
Effort — a numeric **rank** for comparing many unlike candidates on one scoreboard (which Shoulds first?); **Kano** =
**classifies** features by satisfaction-type — **basic/must-have** (absence angers, presence unnoticed),
**performance** (more is linearly better), **delighter/excitement** (unexpected, disproportionate delight). The
sequence is: **Kano** to classify, **RICE** to rank, **MoSCoW** to cut to the timebox. **gingoa:** MoSCoW remains the
MVP-cut instrument (it slices the walking-skeleton scope); RICE/Kano are the *analyze-stage* lenses the harness uses
to order a long candidate list and to make sure the MVP includes every Kano **basic** (a missing basic sinks the
product) before spending effort on delighters. [Atlassian prioritization frameworks] [lit]

## Assumptions · Constraints · Dependencies (ACD) — a taught first-class output
29148 / IEEE-830 SRS templates carry **Assumptions and Dependencies** (and **Constraints**) as named sections
precisely because they are not requirements but they **bound and can invalidate** requirements: an **assumption**
that proves false retroactively breaks the requirements that rested on it; a **dependency** on another team/vendor/
service gates delivery; a **constraint** (regulatory, platform, budget, tech-stack mandate) **bounds the solution
space** and is **distinct from an NFR** (a constraint is imposed *on* the solution; an NFR is a *quality* the
solution must exhibit). **gingoa:** ACD is an explicit contract section the Socratic interview elicits, not an
afterthought — surfacing "what are we assuming?", "what do we depend on?", and "what bounds the solution?" early is a
core part of the gap the harness fills for a non-engineer who would otherwise leave them implicit (and have the agent
discover them mid-build). [ISO 29148 / IEEE-830 SRS via ReqView] [lit, normative]

## Lightweight estimation
Estimation stays deliberately **light** — its only job at ① is to *confirm* INVEST's **Estimable** and **Small**
and to **right-size the MVP cut**, not to produce a heavyweight upfront plan (which would be waterfall over-planning,
ruled out by the aspect). The named method is **relative / t-shirt sizing** (S/M/L, or relative story points) — coarse,
fast, comparative — used purely as a "is this small and estimable enough to be DoR-ready?" check. **gingoa:** the
harness applies relative sizing only to validate INVEST E/S and to keep the walking-skeleton slice small; it does not
build a velocity model or a Gantt chart. [Scrum.org DoR (sizing as a DoR criterion)] [lit]

## Sources
- SWEBOK Guide v4.0, KA1 Software Requirements (elicit/analyze/validate; sources & stakeholders; elicitation techniques; requirements validation) — https://ieeecs-media.computer.org/media/education/swebok/swebok-v4.pdf · http://swebokwiki.org/Chapter_1:_Software_Requirements
- ISO/IEC/IEEE 29148:2018 §5.2.5–5.2.6 (traceable as an individual characteristic; quality set) — https://cdn.standards.iteh.ai/samples/72089/62bb2ea1ef8b4f33a80d984f826267c1/ISO-IEC-IEEE-29148-2018.pdf · https://www.cwnp.com/req-eng/
- Requirements Traceability Matrix (forward/backward, req-IDs, req→design→test) — https://www.perforce.com/resources/alm/requirements-traceability-matrix
- GitHub Spec-Kit (`/analyze` cross-artifact consistency) — https://github.com/github/spec-kit
- Classic elicitation-technique catalogue — https://sdh.global/blog/business/requirements-elicitation-techniques/
- ISO 29148 StRS / IEEE-830 SRS templates (stakeholder spec; Assumptions/Constraints/Dependencies sections) — https://www.reqview.com/doc/iso-iec-ieee-29148-templates/
- Definition of Ready (entry gate; INVEST + acceptance criteria + dependencies + sizing) — https://www.scrum.org/resources/blog/walking-through-definition-ready · https://agilealliance.org/glossary/definition-of-ready/
- Prioritization beyond MoSCoW (RICE rank · Kano satisfaction-type) — https://www.atlassian.com/agile/product-management/prioritization-framework

Items above map onto the aspect's **elicit → analyze → validate** flow: elicitation catalogue + stakeholders feed
*elicit*; ACD + RICE/Kano prioritization feed *analyze*; traceability (RTM), V&V, and the Definition of Ready gate
enforce *validate*.
