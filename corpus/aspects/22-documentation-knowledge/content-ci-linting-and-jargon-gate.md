---
id: aspect-22-documentation-knowledge--content-ci-linting-and-jargon-gate
title: "Content/prose linting in CI + the de-jargon (forbidden-internal-terms) gate"
parent: aspect-22-documentation-knowledge
kind: research-log
evidence_track: census+lit
status: review-needed
last_updated: "2026-06-27"
method: "Lit survey (Vale/markdownlint/cspell/lychee docs + GitHub/GitLab/Datadog/Grafana/Stoplight/PostHog practice) + gh search/code adoption census (2026-06-27). Grounds whether a 'no internal jargon before publishing' CI gate is standard at the ② foundation, and which tool/approach is de-facto."
---

# Content/prose linting in CI + the de-jargon gate

Why this exists: gingoa keeps **internal working-notes local + a clean public face** (a public/internal doc
split). The question this answers: is enforcing "no internal jargon leaks to public docs" **as a CI gate** an
industry-standard ② foundation practice, and what is the de-facto tool? (Verdict: yes, grounded — and it is
the *executable* form of the "de-jargon gate".)

## Is content linting in CI standard? — YES (lit)
Docs-as-code normalized running doc linters in CI at the same seriousness as code linters:
- **markdownlint** — structural Markdown linting; near-universal in doc repos (GitHub Docs runs it pre-commit
  + CI with error-severity blocking merge).
- **Vale** — prose/style + terminology linter; run as a PR CI Action (errata-ai/vale-action) by GitLab,
  Datadog, Grafana, PostHog, Stoplight — error-level rules fail CI.
- **cspell / codespell** — spell-check in CI. **lychee / markdown-link-check** — link-checkers (already in
  aspect-22's "freshness in CI" bullet).
Framed by practitioners as "configure once at project start, runs forever" — i.e. a **foundation-stage** add.

## The de-jargon / forbidden-terms gate specifically — a NAMED first-party feature (lit)
This is not a workaround:
- **Vale `reject.txt` + `Vale.Avoid`** — built-in: every term/phrase/regex in `reject.txt` is flagged as an
  error; `level: error` fails CI. `Vale.Terms` enforces accepted terms; `substitution` rules do "ban X → use
  Y". **This is the de-facto tool for banning terms.**
- Real public/internal-leak uses: Stoplight added an internal product-misspelling to `reject.txt`; Grafana
  substitutes internal architecture terms ("on-prem"→"self-managed") so they never reach public docs;
  GitHub's content linter flags outdated internal release terminology; PostHog scopes rules per content type
  (internal vs public). Vale's glob rule-scoping applies different rules to public vs internal dirs.
- **textlint** (`textlint-rule-terminology`/`stop-words`) and **alex** (inclusivity) are adjacent. A **custom
  grep CI job** is the documented minimal-viable when a prose toolchain isn't in the stack.
- **Where it sits:** dominant pattern = **PR CI, error-severity blocks merge** (± a pre-commit local
  accelerator). A separate pre-publish gate is less common; the PR gate is primary.

## gh adoption census (2026-06-27, `search/code total_count`; estimates, code-search caveats)
- workflow mentions: **markdownlint 8,752** · **vale 6,904** — both heavily used in CI.
- configs: `.markdownlint.json` 4,540 + `.yaml` 1,864 + `rc` 824 = **~7,228 markdownlint** · **`.vale.ini`
  1,244** · **`cspell.json` 2,692**.
- Reading: **markdownlint = most-adopted (structural)**, **Vale = the de-facto for prose + forbidden-terms**
  (strong CI presence), cspell moderate. Raw: `census-data/census-doc-conventions/`.

## Verdict + de-facto approach (statistics-grounded)
- **A de-jargon / forbidden-internal-terms CI gate is grounded + standard at ② foundation** (near-zero cost,
  high retrofit cost; table-stakes for a public/internal doc split).
- **De-facto tool for the broad case:** markdownlint (structural) + **Vale** (prose/terms) pairing; **Vale
  `reject.txt`** is the named de-facto for forbidden-terms.
- **For a single-purpose jargon-block** (gingoa's immediate need — just "no internal shorthand in public
  files"): a **custom grep CI job is the legitimate minimal-viable** (documented), with **Vale as the upgrade
  path** when full prose/style linting is wanted.

## Sources
Vale styles (Avoid/Terms) https://vale.sh/docs/styles · Vale vocab (reject.txt) https://vale.sh/docs/keys/vocab ·
errata-ai/vale-action https://github.com/errata-ai/vale-action · GitHub content linter https://docs.github.com/en/contributing/collaborating-on-github-docs/using-the-content-linter ·
GitLab Vale tests https://docs.gitlab.com/development/documentation/testing/vale/ · Datadog Vale https://www.datadoghq.com/blog/engineering/how-we-use-vale-to-improve-our-documentation-editing-process/ ·
Grafana lint-prose https://grafana.com/docs/writers-toolkit/review/lint-prose/rules/ · Stoplight Vale https://blog.stoplight.io/linting-the-stoplight-docs-with-vale ·
textlint-rule-terminology https://github.com/sapegin/textlint-rule-terminology · Dan Clarke grep banned-words https://www.danclarke.com/git-hooks-and-banned-words/ ·
lychee-action https://github.com/lycheeverse/lychee-action · Earthly markdown-lint https://earthly.dev/blog/markdown-lint/ · gh census 2026-06-27 (this doc).
