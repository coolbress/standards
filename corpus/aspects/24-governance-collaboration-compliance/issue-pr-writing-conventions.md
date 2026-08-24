---
id: aspect-24-governance-collaboration-compliance--issue-pr-writing-conventions
title: "Issue/PR template WRITING conventions — field types, required, help text, checklist & type-of-change style"
parent: aspect-24-governance-collaboration-compliance
kind: research-log
evidence_track: census+lit
status: review-needed
last_updated: "2026-07-07"
method: "conventions.py re-harvest of the 1104 template-bearing repos in census-issue-pr/records-2k.json (1610 issue forms · 10,181 fields · 503 PR templates; PyYAML field-level parse, 99.8% parse-ok) + GitHub's official issue-forms schema as the authoritative syntax reference. Answers HOW each section is written, the depth the header/label censuses (census2k.py, taskform.py) discarded. CONFIRMED at wider N: a 2nd pass (`conventions.py harvest_wide`, `conventions-6k-*`) re-ran over the template-bearing subset of the N=6,582 governance-floor pool (2425 repos · 3248 forms · 20,837 fields · 1077 PR templates; star floor 29 vs 8.2k) — every convention held within a few points (see below). A 3rd pass (`conventions.py harvest_roster`/`roster`, `conventions-roster-*`) captured the field LABELS the earlier passes discarded and clustered them into per-form-category section ROSTERS (which sections a bug/feature/task form ships + required-when-present); a 28.6% free-text tail is left honest and the taxonomy is re-runnable without re-harvest (labels are stored)."
sources:
  - "https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-githubs-form-schema"
  - "https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms"
  - "https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository"
---

# Issue/PR template WRITING conventions

Why this exists: the prior censuses answered **which** issue-template types ship (`taskform.py`: bug 94% /
feature 72% baseline) and **which** sections each body has (`census2k.py`: field-label + PR-header frequency).
They did **not** answer **how** each section is written — the field TYPE, whether it is REQUIRED, whether it
carries help text, the checklist/comment style. That "작성법 (writing method)" layer is the evidence a
*tiered* template standard needs, so it was re-harvested (`conventions.py`) from the template BODIES.

## Authoritative reference (lit)

GitHub's **form schema** is the canonical grammar every issue FORM obeys — five field `type`s
(`markdown` · `textarea` · `input` · `dropdown` · `checkboxes`), each with `attributes` (`label`,
`description`, `placeholder`, `options`, `render`) and `validations` (`required`). The census below measures
which of these the field is _actually_ used in the wild → docs.github.com/…/syntax-for-githubs-form-schema.

## Issue-form conventions (census — N=1104 repos · 1610 forms · 10,181 fields · 99.8% parse-ok)

- **Field type — textarea dominates.** `textarea 54%` · `markdown 14%` (the leading intro/guidance block) ·
  `input 14%` (short scalars: version, URL) · `checkboxes 9%` (acknowledgements) · `dropdown 8.5%` (enums:
  OS, severity, version-range). → The canonical form body is **free-prose textareas** framed by a markdown
  intro, with dropdowns for closed enums and inputs for short scalars.
- **Required is applied to the load-bearing fields, NOT to acknowledgements.** Input-field required-rate
  **54%** overall, but split sharply by type: `dropdown 73%` · `input 65%` · `textarea 57%` ↔
  **`checkboxes 3.8%`**. → The convention: make the enum/scalar/main-prose fields required; leave the
  checkbox acknowledgements optional. By category the strictness rises for terse forms: `task 68%` >
  `bug 57%` > `docs 52%` > `feature 49%` ≈ `question 49%`.
- **Help text is near-universal.** **87%** of input-like fields carry a `description` or `placeholder`. →
  Every field guides the filer; a bare unlabelled field is non-standard.
- **Preflight ("is there an existing issue / have you searched") — a senior minority.** **22%** of forms
  embed a preflight/dedup checkbox. Present enough to be a recognised senior default, absent enough to be
  archetype/maturity-gated, not universal.
- **In-form Code-of-Conduct checkbox — rare (6.4%).** CoC acknowledgement is usually a repo-level file, not
  an in-form checkbox → CoC-in-form is *context-gated*, not a floor.
- **Form size scales with purpose.** Median fields/form: `bug 8` (rich: repro/expected/actual/env/logs) ·
  `feature 4` · `docs 4` · `question 4` · **`task 3` (lean)**. → bug forms are the heavy ones; feature/task
  forms are deliberately lean.
- **`render:` (fenced code/log block) — a real convention** (546 fields), the "relevant log output" textarea
  pattern that formats pasted logs as code.

## Section roster — which sections each form-category ships (census — `conventions.py roster`, N=1104 repos · 669 bug · 516 feature forms)

A follow-on pass (`harvest_roster`) re-harvested the field LABELS — the writing-method pass stored only
`has_label` booleans — and clustered them into canonical section buckets (`SECTION_BUCKETS`), giving the
per-category *roster*: which sections a bug/feature/task form actually ships, at form-level presence, and
whether each is required when present. Label clustering is free text → it carries judgment; a residual
**28.6%** of labels don't cluster (dominated by contribution-willingness checkboxes — "Are you willing to
submit a PR?", "Participation" — plus bare non-clustering tokens "Question / Type / OS / Impact / Component"
and enterprise-niche "Company name") and are honestly left in an `other` tail. Raw labels are stored, so the
taxonomy can be refined and `roster` re-run WITHOUT a re-harvest.

- **Bug form (median 4 sections):** environment **83%** (req-when-present 84%) · repro-steps **74%** (79%) ·
  description **68%** (90%) · expected **52%** (74%) · logs **47%** (22%) · additional-context **41%** (3%) ·
  actual **27%** (84%) · preflight **25%** (4%). → Canonical bug roster = **environment + repro-steps +
  description + expected** (all required-when-present) + **logs + context** (optional) + a **preflight** dedup
  checkbox in a senior ~25% minority. "Actual behavior" is a minority *separate* section — most forms fold it
  into expected.
- **Feature form (median 3 sections):** proposed-solution **51%** (req 78%) · problem/motivation **47%** (79%) ·
  additional-context **47%** (3%) · description **35%** (83%) · alternatives **27%** (26%) · preflight **26%**
  (3%) · environment **10%**. → Canonical feature roster = **problem + proposed-solution** (both required) +
  **alternatives + context** (optional), preflight ~26%. Deliberately lean.
- **Task form (N=26 — rare, noisy):** the wild's task forms are sparse and inconsistent (description 62% ·
  context 23% · acceptance 15% · scope 12% · goal 12%) — **no strong canonical roster**. A goal/scope/acceptance
  task form is a *principled structure*, not a wild-derived one (consistent with task being a ② deliberate add,
  not a census floor).
- **Cross-check — required is applied to load-bearing content sections, not to checkbox/context sections:**
  description 90% · environment 84% · actual 84% · repro 79% · expected 74% required-when-present ↔ logs 22% ·
  preflight 4% · context 3%. Confirms the writing-method census's required-by-type split at the *section* level.

## PR-template conventions (census — N=503 PR templates)

- **Checklist ships EMPTY.** `empty '- [ ]' 62%` · `pre-checked 0.2%` · `no-checklist 38%`. → The standard
  is an **empty** contributor-ticked checklist (median **5** items); a pre-checked checklist is essentially
  never done.
- **Inline HTML-comment guidance is standard (70%).** Most PR templates embed `<!-- … -->` guidance so the
  rendered PR body stays clean while the author sees instructions.
- **Lean — median 3 sections.** (Summary/Description + Testing + Checklist is the modal shape.)
- **"Type of change" is a MINORITY convention, and free-text is NOT how it's written.** Present in only
  **11.5%** of PR templates; when present, **84.5% render it as a checkbox list**, 13.8% as a plain bullet
  list, and **free-text 1.7%**. → Two load-bearing facts for the tier ledger: (i) type-of-change is a
  minority section, and (ii) writing it as free text (`Type of change: feat`) is against the grain — the
  wild uses a checkbox list. Combined with the fact that **it duplicates a Conventional-Commits PR title**
  (which gingoa already gate-enforces via `pr-title.yml`), a CC-enforcing repo has positive grounds to
  **drop** it — matching why CC-adopting repos skip it.

## Robustness — confirmed at N=6,582 (wide pass)

Re-running over the governance-floor pool's template-bearing subset (2425 repos, star floor **29** — the
less-governed long tail the top-2000 excludes) moved **nothing** material. The quality rates most at risk of
being top-repo artifacts held dead-on: **help-text 87.1 → 87.2** (identical — a genuine population-wide floor,
not elite polish), preflight 22.4 → 22.3, required-rate 54.3 → 55.9 (slightly higher), field-type
distribution all within ±1pp (textarea 54.1 → 53.2). The **DROP-type-of-change** call strengthened —
type-of-change stays a ~12% minority and, when present, is *more* checkbox-dominant at wide N (84.5 → 89.8%),
free-text still ~1.6%. The only >3pp move: PR HTML-comment guidance 69.8 → 63.8 (still a 64% majority → keep).
**Net: no tier change; the standard is now grounded at the same N=6,582 rigor as the governance-floor census,
and the conventions are shown to be population-wide floors rather than top-tier-only.**

## What this grounds (descriptive → the tier ledger)

The conventions above are the *how-written* inputs to gingoa's tiered template standard (the tier
CLASSIFICATION — which of these are ①auto / ②senior-default / ③context-confirm — is decided in the ledger
this feeds, not asserted here). The census-standard *writing method* gingoa's shipped forms/PR template
should conform to: textarea-for-prose + dropdown-for-enums + required-on-load-bearing-fields +
help-text-on-every-field + empty-checklist + HTML-comment-guidance + no-redundant-type-of-change.

The **section roster** adds the *which-sections* input: gingoa's shipped forms match the wild roster with no
missing floor section (bug = environment/repro/description/expected/logs/context; feature =
problem/proposed/alternatives/context), the **preflight** add is roster-confirmed at 24–26%, and the
required-when-present pattern grounds the required-on-load-bearing conform — i.e. the roster *validated* the
shipped section design rather than surfacing a gap.

→ feeds the 3-tier ledger and [[template-standard-dogfood-gap]]; grounded in `census-data/census-issue-pr/`
(`conventions.py`, `conventions-records.json`, `conventions-stats.json`, `conventions-roster-records.json`,
`conventions-roster.json`).
