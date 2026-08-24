---
id: aspect-05-scm-workflow--github-workflow-current
title: Current GitHub workflow — evidence and bounded defaults
parent: aspect-05-scm-workflow
kind: reference
status: verified
last_updated: 2026-08-02
evidence_track: lit
freshness: volatile
review_due: 2026-11-02
sources:
  - GITHUB-FLOW
  - GITHUB-PR
  - GITHUB-DEPLOY
  - GITHUB-ACTIONS-SECURE
  - GITFLOW-NOTE
  - DORA-SODR-2017
  - DORA-TBD
---

# Current GitHub workflow — evidence and bounded defaults

This note separates GitHub's current product facts from a recommended workflow. GitHub
documents mechanisms; it does not prescribe one universal issue, branch, review, merge,
or deployment policy for every project.

## Claim table

| Claim ID | Class | Claim and scope | Evidence | Confidence | Valid as of / expiry |
|---|---|---|---|---|---|
| GHW-001 | vendor-behavior | GitHub Flow is a branch-based workflow: create a branch, make and commit changes, open a pull request, address review, merge, then delete the branch. | `GITHUB-FLOW` | high | 2026-08-02; review 2026-11-02 |
| GHW-002 | vendor-behavior | A pull request brings conversation, commits, checks, and file changes together and exposes merge readiness; repository settings determine mandatory gates. | `GITHUB-PR` | high | 2026-08-02; review 2026-11-02 |
| GHW-003 | vendor-behavior | Branch protections or rulesets can require reviews and checks; environments can add reviewers, waits, and branch restrictions; merge queues retest queued changes against the current base. Availability varies by configuration and plan. **구체 경계(Free+비공개=불가)는 [`github-enforcement-boundaries--facts-2026-08`](github-enforcement-boundaries--facts-2026-08.md) GEB-001·002 · 2026-08-24 실측.** | `GITHUB-DEPLOY` | high | 2026-08-02; review 2026-11-02 |
| GHW-004 | vendor-behavior | Reverting a merged pull request creates a new pull request that reverses the merge; complex or conflicting changes can require a manual revert. | `GITHUB-DEPLOY` | high | 2026-08-02; review 2026-11-02 |
| GHW-005 | vendor-behavior | GitHub recommends minimum necessary `GITHUB_TOKEN` permissions and says only a full-length commit SHA is immutable when pinning an action. | `GITHUB-ACTIONS-SECURE` | high | 2026-08-02; review 2026-11-02 |
| GHW-006 | synthesis | GitHub Flow does not itself require an issue, a commit-message convention, squash merging, a particular reviewer count, or a deployment strategy. These are project policy choices. | `GITHUB-FLOW`; `GITHUB-PR` | medium-high | review when GitHub Flow changes |
| GHW-008 | vendor-behavior | **Git Flow 창시자의 2020 철회 단서.** Vincent Driessen 이 원 글에 **"Note of reflection" (2020-03-05)** 를 덧붙였다: 지속적 배포 팀에는 *"a much simpler workflow"* (GitHub Flow)를 권하고, *"Web apps are typically continuously delivered, not rolled back… **This is not the class of software that I had in mind** when I wrote the blog post 10 years ago."* 다만 **명시적으로 버전이 붙는 소프트웨어·다중 버전 지원**에는 *"git-flow may still be as good of a fit"* 이라고 남겼다 — **전면 철회가 아니라 적용 범위의 한정**이다 | `GITFLOW-NOTE` | high | 2026-08-24 재검증 |
| GHW-009 | synthesis | ⚠️ **DORA 의 브랜치 수치는 설문 자기보고다.** *"≤3 active branches · 하루 1회 이상 trunk 병합"* 은 **저장소 계측이나 통제실험이 아니라 State of DevOps 설문 응답**에 기반한다. [`05 overview`](05-scm-workflow--overview.md) 가 *"DORA's **measured** rule"* 이라 쓴 표현은 계측을 함의하므로 **한정을 병기해야 한다** | `DORA-SODR-2017`; `DORA-TBD` | medium-high | 2026-08-24 |
| GHW-007 | synthesis | A defensible default path is isolate change → automated verification → risk/ownership-proportional review → protected merge → observable deployment → recoverable rollback. This is a recommended control chain, not a GitHub-mandated standard. | `GITHUB-FLOW`; `GITHUB-PR`; `GITHUB-DEPLOY`; `GITHUB-ACTIONS-SECURE` | medium | review 2026-11-02 |

**재검증 기록 (R5-1 배치 B)** — 검증일 `2026-08-24` · 검증자 `Claude Opus 5` + `codex-cli 0.145.0`(독립 질의) · **판정: GHW-008 신규 승계 · GHW-009 한정 추가** · **불일치 없음**(Codex 가 GHW-009 의 설문-자기보고 성격을 추가로 짚었다) · 절차 [`reverification-protocol`](../../methods/reverification-protocol.md)

> **R5-1 목록 오류 2건째**: *"Git Flow 2020 note"* 는 **미승계가 아니었다.** 결론은 [`05 overview`](05-scm-workflow--overview.md) *"GitFlow — ruled out for continuously-delivered software"* 로 **이미 승계돼 있었고, 창시자 note 라는 출처만 안 붙어 있었다.** 처분은 *"승계 또는 삭제"* 가 아니라 **출처 부착**이다.

## Risk-scaled application

| Context | Minimum defensible controls |
|---|---|
| Solo, local-only experiment | Small branch or isolated worktree; local checks; reversible commits. |
| Solo, remotely published repository | Required automated checks; protected default branch where practical; explicit self-review evidence. |
| Team repository | Checks plus ownership-aware review; branch protection/rulesets; clear merge policy. |
| Production deployment | Environment protection, least-privilege workflow permissions, pinned dependencies/actions, observable rollout, and tested rollback. |

Independent human approval may be impossible in a one-person project. That limitation
must be stated rather than simulated; automated checks, protected merges, and an
independent model review can reduce risk but are not equivalent to accountable peer review.

## Do not infer

- Repository prevalence is not proof that a practice is effective.
- A green check is not proof that requirements are satisfied; it proves only the configured checks passed.
- A pull request is not automatically an independent review.
- A squash-first or Conventional Commits policy can be useful, but neither is imposed by GitHub Flow.

## Sources

- [GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow)
- [About pull requests](https://docs.github.com/en/pull-requests/get-started/about-pull-requests)
- [Deploying code](https://docs.github.com/en/pull-requests/concepts/deploying-code)
- [Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use)
