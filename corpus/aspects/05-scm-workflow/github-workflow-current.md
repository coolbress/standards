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
| GHW-010 | vendor-behavior | **DORA 의 세 수치는 원문 그대로 확인된다.** dora.dev 역량 페이지: *"Have **three or fewer active branches** in the application's code repository."* · *"**Merge branches to trunk at least once a day.**"* · *"**Don't have code freezes and don't have integration phases.**"* 그리고 브랜치 수명: *"branches in trunk-based development typically **last no more than a few hours**."* ⚠️ **근거의 성격이 페이지 자신에 적혀 있다** — *"**Analysis of DORA data from 2016 and 2017** shows that teams achieve higher levels of software delivery and operational performance … **if they follow these practices**."* 즉 **설문 데이터 분석에 기반한 조건부·상관 진술**이고, 무작위 배정이나 저장소 계측이 아니다 (GHW-009 를 1차 확인으로 승격) | `DORA-TBD`; `DORA-SODR-2017` | high (수치) / medium-high (인과) | 2026-08-25 |
| GHW-011 | vendor-behavior | ⚠️ **CR-008 의 삭제는 절반만 옳았다.** 배치 A 는 *"다중 필수 승인자·형식적 체크리스트는 DORA 안티패턴"* 을 **오귀속으로 통째 삭제**했으나, **앞 절반에는 실제 DORA 출처가 있다** — 같은 역량 페이지의 *Common pitfalls* 가 *"**An overly heavy code-review process**. Many organizations have a heavyweight code review process that **requires multiple approvals** before changes can be merged into trunk"* 을 **trunk-based development 채택의 흔한 장애물**로 명시한다. 🔴 **단 범위가 다르다**: *"코드리뷰 일반의 안티패턴"* 이 아니라 ***trunk-based development 채택의 장애물***이고, **체크리스트는 이 페이지에 0회 등장**한다(뒤 절반은 여전히 무출처). 부수: 같은 절이 *"Performing code reviews **asynchronously**"* 도 장애물로 들며 **동기 리뷰를 권한다** | `DORA-TBD` | high | 2026-08-25 **선행 배치 정정** |
| GHW-012 | local-census | **이슈 우선은 크기 조건부다 — 폐기 문서에서 승계.** *"Issue-before-PR is **size-conditional, NOT universal**"* · 판정 기준은 줄 수가 아니라 ***"non-trivial"*** 이다 — 사소·소규모·후속 변경은 **바로 PR**, 이슈 우선은 **방향이 뒤집힐 수 있는 작업**(새 기능·API·아키텍처·breaking)에 한한다. 소수파(**모든 non-trivial PR 에 이슈 요구**)는 **~20–25%** 이고 **언어 코어·유지보수자 희소 프로젝트에 몰린다**(Django·Go·TypeScript) — Homebrew 는 정반대(*"do not open both"*). ⚠️ **표본은 CONTRIBUTING 가이드 11개 + GitHub Flow 문서**다. 저장소 계측이 아니라 **문서에 적힌 규범의 표본**이고 n 이 작다. 🔴 **승계 사유**: 이 주장의 유일한 거처가 [`05 overview`](05-scm-workflow--overview.md) 였는데 그 문서의 처분이 **`C50-16 SUPERSEDED`**(*"현재 설계 근거로 사용하지 않는다"*)다. **`direction/01·03·04` 가 그 문서를 근거로 인용하고 있었다** — 규칙 위반이었다. 주장 자체에는 근거가 있으므로 **폐기하지 않고 여기로 옮긴다** | `ISSUE-VS-PR-CENSUS-2026` | medium (n=11 · 문서 규범 표본) | 2026-08-26 **승계** |
| GHW-007 | synthesis | A defensible default path is isolate change → automated verification → risk/ownership-proportional review → protected merge → observable deployment → recoverable rollback. This is a recommended control chain, not a GitHub-mandated standard. | `GITHUB-FLOW`; `GITHUB-PR`; `GITHUB-DEPLOY`; `GITHUB-ACTIONS-SECURE` | medium | review 2026-11-02 |
| GHW-013 | vendor-behavior | **머지 직전에 head OID 를 고정할 수 있다 — 안 하면 검토한 것과 다른 커밋이 들어간다.** `gh pr merge --match-head-commit <SHA>` 는 *"Commit SHA that the pull request head must match to allow merge"* 다(**설치본 gh 2.79.0 실측**). 🔴 **`strict_required_status_checks_policy` 로는 못 막는다** — 그건 **base 가 밀렸는지**를 보지 `head` 가 바뀌었는지를 안 본다. 검토와 머지 사이에 브랜치로 push 가 한 번 들어가면 **본 적 없는 커밋이 머지된다.** ⚠️ 플래그는 판마다 다르므로 쓰기 전에 `gh pr merge --help` 를 본다 | `GH-CLI-PR-MERGE` | high | 2027-02-28 |
| GHW-014 | normative | **머지는 작업의 기본 경계다.** 검증된 머지 + 연결 이슈 종료를 한 과제의 끝으로 본다 — *"do not start a materially separate next issue in the same thread"*. ⚠️ **예외가 규칙에 붙어 있다**: *"Unless the user explicitly requested continuous roadmap execution."* 즉 소유자가 **연속 실행을 명시적으로 요청하면** 그때는 이어서 간다. 이 저장소는 두 방식을 다 쓴다 — 기본은 경계, 요청이 있으면 연속 | `CODEX-NATIVE-ARCHIVE` | medium | 2027-02-28 |

**승계 기록 (2026-08-26)** — `05 overview` 가 `SUPERSEDED` 인데 `direction` 이 그 문서의 *이슈 크기 조건부* 주장을 근거로 쓰고 있었다. 주장에는 근거가 있으므로(11개 CONTRIBUTING + GitHub Flow 문서 census) **폐기하지 않고 승계본인 이 문서로 옮겼다.** ⚠️ **강도는 🟢 이 아니라 🟡 다** — `direction/03` 이 이것을 🟢 로 표시하고 있었는데, **인용 사슬이 코퍼스에서 멈췄고 그 아래 표본이 n=11 문서 규범**이다 · 절차 [`reverification-protocol`](../../methods/reverification-protocol.md)

**재검증 기록 (배치 5 · DORA)** — 검증일 `2026-08-25` · 검증자 `Claude Opus 5`(1차 출처 직접 열람 + 원문 텍스트 추출로 기계 대조) · **판정: GHW-010 신규(GHW-009 를 1차 확인으로 승격) · GHW-011 신규(선행 배치 CR-008 부분 정정)** · ⚠️ **불일치 없음이나 검증자 1종** — Codex 실행분이 브라우저 미연결로 원문 열람에 실패했고, **추측 대신 *"확인할 수 없다"* 를 반환했다**(정상 동작). 세 수치는 페이지 원문을 로컬로 내려 `grep` 으로 문자열 일치까지 확인했으므로 수치 자체는 기계 확인이지만, **해석(GHW-011 의 범위 판정)은 단일 검증자다** — 절차 §4 의 교차검증 요건을 이 행은 충족하지 않는다. 그대로 적는다 · 절차 [`reverification-protocol`](../../methods/reverification-protocol.md)

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
