# Issue-before-PR vs PR-only — contribution-workflow norm (research deposit)

Origin: owner asked (2026-06-28) whether handling a small/follow-up change as **PR-only** (no preceding
issue) is industry standard, after deciding to land a small constitution-docs change without an issue.
Method: researcher agent sampled 11 major OSS CONTRIBUTING guides + GitHub's own flow docs.

## Verdict (one line)
**Size-conditional is the dominant norm: trivial / small / follow-up changes may go straight to a PR;
non-trivial (feature / API / architecture / breaking) changes should have an issue first.** GitHub flow
does not require an issue at all. Only ~20–25% of sampled projects require an issue for every non-trivial PR.

## Project sample
| Project | Stance | Threshold language | Source |
|---|---|---|---|
| React | recommend for non-trivial; bug fixes skip | "non-trivial changes to the implementation" | https://legacy.reactjs.org/docs/how-to-contribute.html |
| Angular | required for Major Features; Small Features → PR | "Major Feature" vs "Small Features"; "When in doubt, open an issue first" | https://raw.githubusercontent.com/angular/angular/main/CONTRIBUTING.md |
| Vue (core) | recommend for non-trivial API surface; bug fixes skip | "non-trivial API surface addition" | https://raw.githubusercontent.com/vuejs/core/main/.github/contributing.md |
| Go | strong issue-first | "Excluding very trivial changes, all contributions should be connected to an existing issue." | https://go.dev/doc/contribute |
| Rust | permissive; "just open a PR" for most | "large, complex, cross-cutting" → discuss first | https://rustc-dev-guide.rust-lang.org/contributing.html |
| Node.js | no blanket rule; large changes → issue first | "substantial change" | https://raw.githubusercontent.com/nodejs/node/main/doc/contributing/large-pull-requests.md |
| VS Code | discuss significant changes w/ issue assignee first | "significant changes" | https://github.com/microsoft/vscode/wiki/How-to-Contribute |
| TypeScript | work only on already-approved issues | feature vs bug | https://raw.githubusercontent.com/microsoft/TypeScript/main/CONTRIBUTING.md |
| Django | strict issue-first | "Non-trivial pull requests (anything more than fixing a typo) without Trac tickets will be closed!" | https://raw.githubusercontent.com/django/django/main/CONTRIBUTING.rst |
| Kubernetes | no issue-first requirement | (none) | https://raw.githubusercontent.com/kubernetes/community/master/contributors/guide/contributing.md |
| Homebrew | PR-preferred ("do not open both") | (none; PR over issue) | https://docs.brew.sh/How-To-Open-a-Homebrew-Pull-Request |
| GitHub flow | issue optional ("if your PR addresses an issue, link it") | (none) | https://docs.github.com/en/get-started/using-github/github-flow |

## Threshold
Not a line-count — the keyword is **"non-trivial."** Practical test: *could a maintainer reasonably reject
the whole direction, wasting the implementation?* If yes → issue first. Below the line (PR-direct OK): typo
fixes, cosmetic/docs tweaks, small clear bug fixes, trivial refactors.

## Minority strict pattern (~20–25%)
Django (closes non-typo PRs w/o ticket), Go (trivial-only exception), TypeScript (approved-issues-only) —
correlates with high-governance / language-core / scarce-maintainer-bandwidth projects.

## gingoa application
Small docs / spec-clarification / follow-up changes → **PR-only is industry-aligned**; the issue-first gate
matters for direction-uncertain or API/architecture changes — which gingoa already gates via its ADR + spec
process. Matches the repo's own precedent (#15–#25 = issueless follow-up PRs).
