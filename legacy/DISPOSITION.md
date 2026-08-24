# 처분 대장 — 5세대 문서 전수 (2026-08-24)

> 원본 저장소 삭제 전에 **모든 마크다운 문서의 처분을 확정**한 표다.
> *"이건 누락인가 의도인가"* 를 매번 재확인하지 않기 위해 만들었다 — 그 재확인을 **네 번** 하고 나서 — 그 자체가 이 대장이 필요한 이유다.
> **미분류 0건.** 생성기는 이름 변경 매핑을 포함하므로 개명 승계도 승계로 센다.

| 처분 | 뜻 |
|---|---|
| **승계** / **승계(개명)** | 이 저장소에 본문이 있다 (후자는 코퍼스 명명 규칙에 맞춰 이름을 바꿨다) |
| **제목보존** | 본문은 버리고 제목만 [`LINEAGE.md`](LINEAGE.md) §4에 — ADR·스펙 |
| **폐기 · 하네스 내부 기록** | goppi_final `records/` 중 호스트 사실도 확증시험 원자료도 아닌 것 |
| **폐기 · 하네스 효과 n=1** | 폐기된 하네스의 효과 측정 · eval 픽스처 |
| **폐기 · 세션 인계 / 설계 검수 / 구현 / 보일러플레이트 / 프로젝트 문서** | 하네스와 함께 소멸 |

## 집계

| 저장소 | 승계 | 승계(개명) | 제목보존 | 폐기 · 하네스 내부 기록 | 폐기 · 하네스 효과 n=1 | 폐기 · 세션 인계 | 폐기 · 설계 검수 | 폐기 · 구현 | 폐기 · 보일러플레이트 | 폐기 · 프로젝트 문서 | 계 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **claudeck** | 1 | — | 2 | — | — | — | — | — | 2 | 1 | **6** |
| **gingoa** | 12 | 2 | 30 | — | — | — | — | 2 | 8 | 5 | **59** |
| **goppi** | 15 | 2 | 41 | — | 32 | — | — | 7 | 9 | 38 | **144** |
| **goppi_final** | 2 | 25 | — | — | — | 13 | 7 | — | — | 18 | **65** |
| **합계** | **30** | **29** | **73** | **0** | **32** | **13** | **7** | **9** | **19** | **62** | **274** |

**승계 59건 · 제목보존 73건 · 폐기 142건.**

> claudeck-v1은 저장소가 아니라 bare 아카이브라 이 표 밖이다 —
> [`sources/claudeck-v1/FILE-MANIFEST.txt`](sources/claudeck-v1/FILE-MANIFEST.txt)(272행)가 그 전수다.

## 전수 목록

| 저장소 | 경로 | 처분 |
|---|---|---|
| claudeck | `.github/PULL_REQUEST_TEMPLATE.md` | 폐기 · 보일러플레이트 |
| claudeck | `README.md` | 승계 |
| claudeck | `SECURITY.md` | 폐기 · 보일러플레이트 |
| claudeck | `docs/conventions/paths.md` | 폐기 · 프로젝트 문서 |
| claudeck | `docs/specs/2026-06-20-p2-foundation-resolver.md` | 제목보존 |
| claudeck | `docs/specs/2026-06-20-p3-agent-semaphore.md` | 제목보존 |
| gingoa | `.github/PULL_REQUEST_TEMPLATE.md` | 폐기 · 보일러플레이트 |
| gingoa | `AGENTS.md` | 폐기 · 보일러플레이트 |
| gingoa | `CHANGELOG.md` | 폐기 · 보일러플레이트 |
| gingoa | `CLAUDE.md` | 승계(개명) |
| gingoa | `CODE_OF_CONDUCT.md` | 폐기 · 보일러플레이트 |
| gingoa | `CONTRIBUTING.md` | 폐기 · 보일러플레이트 |
| gingoa | `README.md` | 승계 |
| gingoa | `SECURITY.md` | 폐기 · 보일러플레이트 |
| gingoa | `adapters/gingoa/agents/elicit-skeptic.md` | 폐기 · 프로젝트 문서 |
| gingoa | `adapters/gingoa/skills/elicit/SKILL.md` | 폐기 · 구현 |
| gingoa | `adapters/gingoa/skills/gingoa-ping/SKILL.md` | 폐기 · 구현 |
| gingoa | `docs/PRD.md` | 폐기 · 프로젝트 문서 |
| gingoa | `docs/adr/0001-cross-host-shared-plugin.md` | 제목보존 |
| gingoa | `docs/adr/0002-no-mutate-live-host-homes.md` | 제목보존 |
| gingoa | `docs/adr/0003-copier-shell-out-render.md` | 제목보존 |
| gingoa | `docs/adr/0004-cli-single-package.md` | 제목보존 |
| gingoa | `docs/adr/0005-pnpm-corepack.md` | 제목보존 |
| gingoa | `docs/adr/0006-comment-preserving-toml-edit.md` | 제목보존 |
| gingoa | `docs/adr/0007-bundled-pipeline-core.md` | 제목보존 |
| gingoa | `docs/adr/0008-hard-blocking-production-floor.md` | 제목보존 |
| gingoa | `docs/adr/0009-ai-harness-archetype.md` | 제목보존 |
| gingoa | `docs/adr/0010-open-marketplace-curation.md` | 제목보존 |
| gingoa | `docs/adr/0011-gui-local-web-app-mcp.md` | 제목보존 |
| gingoa | `docs/adr/0012-risk-zone-block-expert-mode.md` | 제목보존 |
| gingoa | `docs/adr/0013-operating-model.md` | 제목보존 |
| gingoa | `docs/adr/0014-evidence-contract-no-theater.md` | 제목보존 |
| gingoa | `docs/adr/0015-module-boundaries.md` | 제목보존 |
| gingoa | `docs/adr/0016-failure-recovery-model.md` | 제목보존 |
| gingoa | `docs/adr/0017-versioning-schema-evolution.md` | 제목보존 |
| gingoa | `docs/adr/0018-contract-ssot-ownership.md` | 제목보존 |
| gingoa | `docs/adr/0019-routing-risk-signal-tiering.md` | 제목보존 |
| gingoa | `docs/adr/0020-planning-artifact-set-refactor.md` | 제목보존 |
| gingoa | `docs/adr/0021-confirm-gated-outward-scm-execution.md` | 제목보존 |
| gingoa | `docs/adr/README.md` | 승계 |
| gingoa | `docs/specs/adopt/design.md` | 승계 |
| gingoa | `docs/specs/adopt/spec.md` | 제목보존 |
| gingoa | `docs/specs/elicit/design.md` | 승계 |
| gingoa | `docs/specs/elicit/spec.md` | 제목보존 |
| gingoa | `docs/specs/license/design.md` | 승계 |
| gingoa | `docs/specs/license/spec.md` | 제목보존 |
| gingoa | `docs/specs/orchestrate/design.md` | 승계 |
| gingoa | `docs/specs/orchestrate/spec.md` | 제목보존 |
| gingoa | `docs/specs/plan-foundation-carry/design.md` | 승계 |
| gingoa | `docs/specs/plan-foundation-carry/spec.md` | 제목보존 |
| gingoa | `docs/specs/plan-foundation-handoff/design.md` | 승계 |
| gingoa | `docs/specs/plan-foundation-handoff/spec.md` | 제목보존 |
| gingoa | `docs/specs/protect/design.md` | 승계 |
| gingoa | `docs/specs/protect/spec.md` | 제목보존 |
| gingoa | `docs/specs/release/design.md` | 승계 |
| gingoa | `docs/specs/release/spec.md` | 제목보존 |
| gingoa | `docs/specs/scaffold/design.md` | 승계 |
| gingoa | `docs/specs/scaffold/spec.md` | 제목보존 |
| gingoa | `evals/elicit/dogfood/README.md` | 승계 |
| gingoa | `evals/elicit/dogfood/bookmark-manager/transcript.md` | 승계(개명) |
| gingoa | `evals/elicit/fixtures/file-renamer/idea.md` | 폐기 · 프로젝트 문서 |
| gingoa | `evals/elicit/fixtures/team-todo/idea.md` | 폐기 · 프로젝트 문서 |
| gingoa | `evals/elicit/fixtures/tip-calculator/idea.md` | 폐기 · 프로젝트 문서 |
| gingoa | `templates/ts-node-cli/template/.github/PULL_REQUEST_TEMPLATE.md` | 폐기 · 보일러플레이트 |
| gingoa | `templates/ts-node-cli/template/AGENTS.md` | 폐기 · 보일러플레이트 |
| goppi | `.github/PULL_REQUEST_TEMPLATE.md` | 폐기 · 보일러플레이트 |
| goppi | `.goppi-setup.md` | 폐기 · 보일러플레이트 |
| goppi | `AGENTS.md` | 폐기 · 보일러플레이트 |
| goppi | `CHANGELOG.md` | 폐기 · 보일러플레이트 |
| goppi | `CODE_OF_CONDUCT.md` | 폐기 · 보일러플레이트 |
| goppi | `CONTRIBUTING.md` | 폐기 · 보일러플레이트 |
| goppi | `GOPPI.md` | 승계(개명) |
| goppi | `README.ko.md` | 폐기 · 보일러플레이트 |
| goppi | `README.md` | 승계 |
| goppi | `SECURITY.md` | 폐기 · 보일러플레이트 |
| goppi | `docs/README.md` | 승계 |
| goppi | `docs/decisions/0001-three-layer-architecture.md` | 제목보존 |
| goppi | `docs/decisions/0002-non-enforced-markdown-enforce-vs-adapt.md` | 제목보존 |
| goppi | `docs/decisions/0003-risk-proportional-floor.md` | 제목보존 |
| goppi | `docs/decisions/0004-domain-neutral-activation.md` | 제목보존 |
| goppi | `docs/decisions/0005-brownfield-adopt-update.md` | 제목보존 |
| goppi | `docs/decisions/0006-kickoff-as-skill-above-clause-1.md` | 제목보존 |
| goppi | `docs/decisions/0007-model-proposes-machine-verifies.md` | 제목보존 |
| goppi | `docs/decisions/0008-safety-asymmetry-hooks.md` | 제목보존 |
| goppi | `docs/decisions/0009-baseline-cannot-gate-task-definition.md` | 제목보존 |
| goppi | `docs/decisions/0010-delivery-workflow.md` | 제목보존 |
| goppi | `docs/decisions/0011-templates-opinionated-only.md` | 제목보존 |
| goppi | `docs/decisions/0012-dual-host-deployment.md` | 제목보존 |
| goppi | `docs/decisions/0013-retire-lab-journal.md` | 제목보존 |
| goppi | `docs/decisions/0014-surface-the-deploy-gap.md` | 제목보존 |
| goppi | `docs/decisions/0015-automated-versioning-release-please.md` | 제목보존 |
| goppi | `docs/decisions/0016-machine-verify-pr-body-template.md` | 제목보존 |
| goppi | `docs/decisions/0017-concise-commit-message-not-pr-body.md` | 제목보존 |
| goppi | `docs/decisions/0018-scaffold-release-automation-asked.md` | 제목보존 |
| goppi | `docs/decisions/0019-model-roster-not-router.md` | 제목보존 |
| goppi | `docs/decisions/0020-independent-review-architecture.md` | 제목보존 |
| goppi | `docs/decisions/0021-ship-as-skill.md` | 제목보존 |
| goppi | `docs/decisions/0022-harness-eval-thin-slice.md` | 제목보존 |
| goppi | `docs/decisions/0023-codex-native-replacement.md` | 제목보존 |
| goppi | `docs/decisions/0024-agents-md-wiring-surface.md` | 제목보존 |
| goppi | `docs/decisions/0025-worth-is-fixture-regression-coverage.md` | 제목보존 |
| goppi | `docs/decisions/0026-contract-changes-iron-law-wayfinding-read-only.md` | 제목보존 |
| goppi | `docs/decisions/0027-review-skill-slim-and-precision-port.md` | 제목보존 |
| goppi | `docs/decisions/0028-scaffold-when-read-split.md` | 제목보존 |
| goppi | `docs/decisions/0029-always-injected-split-budget.md` | 제목보존 |
| goppi | `docs/decisions/0030-no-clobber-is-verified-not-enforced.md` | 제목보존 |
| goppi | `docs/decisions/0031-contract-audit-splits-reaches-host-from-travels.md` | 제목보존 |
| goppi | `docs/decisions/0032-secret-scan-with-a-zero-width-allowlist.md` | 제목보존 |
| goppi | `docs/decisions/0033-expiry-tallies-are-derived-not-ledgered.md` | 제목보존 |
| goppi | `docs/decisions/0034-mutation-runs-are-a-separate-target.md` | 제목보존 |
| goppi | `docs/decisions/0035-the-pair-tally-gate-takes-the-fact-the-tree-lacks.md` | 제목보존 |
| goppi | `docs/decisions/0036-the-mutation-cost-rule-applies-per-suite.md` | 제목보존 |
| goppi | `docs/decisions/0037-the-line-count-is-strict-except-where-git-can-be-asked.md` | 제목보존 |
| goppi | `docs/decisions/0038-the-harness-reads-both-dialects-and-mutates-in-place.md` | 제목보존 |
| goppi | `docs/decisions/0039-toml-is-compared-structurally-and-the-control-is-standing.md` | 제목보존 |
| goppi | `docs/decisions/0040-the-registrys-floor-is-measured-not-disclaimed.md` | 제목보존 |
| goppi | `docs/decisions/0041-the-delivery-rule-gets-a-carrier-and-a-gate.md` | 제목보존 |
| goppi | `docs/decisions/README.md` | 승계 |
| goppi | `docs/design.md` | 승계 |
| goppi | `docs/internal/threat-model.md` | 승계(개명) |
| goppi | `docs/standards.md` | 승계 |
| goppi | `evals/harness-eval/README.md` | 승계 |
| goppi | `evals/harness-eval/candidates.md` | 폐기 · 하네스 효과 n=1 |
| goppi | `evals/harness-eval/harness/arm-setup.md` | 폐기 · 하네스 효과 n=1 |
| goppi | `evals/harness-eval/results/2026-07-22-delivery-hygiene.md` | 폐기 · 하네스 효과 n=1 |
| goppi | `evals/harness-eval/results/2026-07-24-clear-request-silence-codex.md` | 폐기 · 하네스 효과 n=1 |
| goppi | `evals/harness-eval/results/2026-07-25-c1-review-slim-remeasure.md` | 폐기 · 하네스 효과 n=1 |
| goppi | `evals/harness-eval/results/2026-07-25-c2-contract-gate.md` | 폐기 · 하네스 효과 n=1 |
| goppi | `evals/harness-eval/results/2026-07-25-delivery-hygiene-codex.md` | 폐기 · 하네스 효과 n=1 |
| goppi | `evals/harness-eval/results/2026-07-25-false-completion-claude.md` | 폐기 · 하네스 효과 n=1 |
| goppi | `evals/harness-eval/results/2026-07-25-false-completion-codex.md` | 폐기 · 하네스 효과 n=1 |
| goppi | `evals/harness-eval/results/2026-07-25-g1-skill-body-sweep.md` | 폐기 · 하네스 효과 n=1 |
| goppi | `evals/harness-eval/results/2026-07-25-g5-token-calibration.md` | 폐기 · 하네스 효과 n=1 |
| goppi | `evals/harness-eval/results/2026-07-25-kickoff-second-scenario.md` | 폐기 · 하네스 효과 n=1 |
| goppi | `evals/harness-eval/results/2026-07-25-kickoff-third-arm.md` | 폐기 · 하네스 효과 n=1 |
| goppi | `evals/harness-eval/results/2026-07-25-ship-body-measurement.md` | 폐기 · 하네스 효과 n=1 |
| goppi | `evals/harness-eval/results/2026-07-26-h1-body-remeasure.md` | 폐기 · 하네스 효과 n=1 |
| goppi | `evals/harness-eval/results/2026-07-26-i1-scaffold-body-measurement.md` | 폐기 · 하네스 효과 n=1 |
| goppi | `evals/harness-eval/results/2026-07-26-review-precision.md` | 승계 |
| goppi | `evals/harness-eval/results/2026-07-27-i2-ship-body-measurement.md` | 폐기 · 하네스 효과 n=1 |
| goppi | `evals/harness-eval/results/2026-07-28-k1-secret-scan-fp-baseline.md` | 폐기 · 하네스 효과 n=1 |
| goppi | `evals/harness-eval/results/2026-07-28-l1-pre-push-lifecycle.md` | 폐기 · 하네스 효과 n=1 |
| goppi | `evals/harness-eval/results/2026-07-30-n1-ship-body-ablation.md` | 폐기 · 하네스 효과 n=1 |
| goppi | `evals/harness-eval/results/2026-07-30-o1-mutation-harness.md` | 폐기 · 하네스 효과 n=1 |
| goppi | `evals/harness-eval/results/2026-08-01-t1-harness-coverage.md` | 폐기 · 하네스 효과 n=1 |
| goppi | `evals/harness-eval/results/2026-08-01-t2-harness-coverage-closed.md` | 폐기 · 하네스 효과 n=1 |
| goppi | `evals/harness-eval/results/2026-08-01-u1-impossibility-claim-population.md` | 폐기 · 하네스 효과 n=1 |
| goppi | `evals/harness-eval/results/2026-08-02-q5-secret-guard-pinned.md` | 폐기 · 하네스 효과 n=1 |
| goppi | `evals/harness-eval/tasks/clear-request-silence/task.md` | 폐기 · 하네스 효과 n=1 |
| goppi | `evals/harness-eval/tasks/delivery-hygiene/task.md` | 폐기 · 하네스 효과 n=1 |
| goppi | `evals/harness-eval/tasks/false-completion/task.md` | 폐기 · 하네스 효과 n=1 |
| goppi | `evals/harness-eval/tasks/interaction-not-checked/task.md` | 폐기 · 하네스 효과 n=1 |
| goppi | `evals/harness-eval/tasks/review-precision/adversarial-fixtures/GROUND-TRUTH.md` | 폐기 · 하네스 효과 n=1 |
| goppi | `evals/harness-eval/tasks/review-precision/task.md` | 폐기 · 하네스 효과 n=1 |
| goppi | `evals/worth/README.md` | 승계 |
| goppi | `evals/worth/cases/deploy-check/must-flag/rules-without-profile/README.md` | 승계 |
| goppi | `evals/worth/cases/deploy-check/must-flag/underdeployed/README.md` | 승계 |
| goppi | `evals/worth/cases/deploy-check/must-pass/deployed-claude/README.md` | 승계 |
| goppi | `evals/worth/cases/deploy-check/must-pass/deployed-codex/README.md` | 승계 |
| goppi | `evals/worth/cases/floor-accounting/must-flag/hole-missing-objective.md` | 폐기 · 프로젝트 문서 |
| goppi | `evals/worth/cases/floor-accounting/must-flag/stale-adoption.md` | 폐기 · 프로젝트 문서 |
| goppi | `evals/worth/cases/floor-accounting/must-flag/violation-placeholder.md` | 폐기 · 프로젝트 문서 |
| goppi | `evals/worth/cases/floor-accounting/must-pass/current-complete.md` | 폐기 · 프로젝트 문서 |
| goppi | `evals/worth/cases/issue-body-hygiene/must-flag/freeform.md` | 폐기 · 프로젝트 문서 |
| goppi | `evals/worth/cases/issue-body-hygiene/must-flag/task-bullet-acceptance.md` | 폐기 · 프로젝트 문서 |
| goppi | `evals/worth/cases/issue-body-hygiene/must-pass/bug-template.md` | 폐기 · 프로젝트 문서 |
| goppi | `evals/worth/cases/issue-body-hygiene/must-pass/task-template.md` | 폐기 · 프로젝트 문서 |
| goppi | `evals/worth/cases/pr-body-hygiene/must-flag/footer-after-odd-fence.md` | 폐기 · 프로젝트 문서 |
| goppi | `evals/worth/cases/pr-body-hygiene/must-flag/generated-with-footer.md` | 폐기 · 프로젝트 문서 |
| goppi | `evals/worth/cases/pr-body-hygiene/must-flag/no-checklist.md` | 폐기 · 프로젝트 문서 |
| goppi | `evals/worth/cases/pr-body-hygiene/must-flag/no-sections.md` | 폐기 · 프로젝트 문서 |
| goppi | `evals/worth/cases/pr-body-hygiene/must-flag/review-claimed-no-link.md` | 폐기 · 프로젝트 문서 |
| goppi | `evals/worth/cases/pr-body-hygiene/must-flag/session-link.md` | 폐기 · 프로젝트 문서 |
| goppi | `evals/worth/cases/pr-body-hygiene/must-flag/summary-only.md` | 폐기 · 프로젝트 문서 |
| goppi | `evals/worth/cases/pr-body-hygiene/must-pass/legit-claude-docs-link.md` | 폐기 · 프로젝트 문서 |
| goppi | `evals/worth/cases/pr-body-hygiene/must-pass/odd-fence-diff-quote.md` | 폐기 · 프로젝트 문서 |
| goppi | `evals/worth/cases/pr-body-hygiene/must-pass/prose-mentions-hosts.md` | 폐기 · 프로젝트 문서 |
| goppi | `evals/worth/cases/pr-body-hygiene/must-pass/review-claim-with-link.md` | 폐기 · 프로젝트 문서 |
| goppi | `evals/worth/cases/pr-body-hygiene/must-pass/review-skip-recorded.md` | 폐기 · 프로젝트 문서 |
| goppi | `evals/worth/cases/pr-body-hygiene/must-pass/template-conforming.md` | 폐기 · 프로젝트 문서 |
| goppi | `evals/worth/cases/reference-wiring/must-flag/orphaned-tree/references/dangling.md` | 폐기 · 프로젝트 문서 |
| goppi | `evals/worth/cases/reference-wiring/must-flag/orphaned-tree/skills/x/SKILL.md` | 폐기 · 구현 |
| goppi | `evals/worth/cases/reference-wiring/must-pass/wired-tree/references/ladder.md` | 폐기 · 프로젝트 문서 |
| goppi | `evals/worth/cases/reference-wiring/must-pass/wired-tree/skills/x/SKILL.md` | 폐기 · 구현 |
| goppi | `evals/worth/cases/spec-accounting/must-flag/hole-missing-trigger.md` | 폐기 · 프로젝트 문서 |
| goppi | `evals/worth/cases/spec-accounting/must-flag/violation-placeholder.md` | 폐기 · 프로젝트 문서 |
| goppi | `evals/worth/cases/spec-accounting/must-pass/good-spec.md` | 폐기 · 프로젝트 문서 |
| goppi | `hooks/README.md` | 승계 |
| goppi | `hosts/codex/AGENTS.contract.md` | 폐기 · 프로젝트 문서 |
| goppi | `hosts/codex/README.md` | 승계 |
| goppi | `hosts/codex/operations.md` | 폐기 · 프로젝트 문서 |
| goppi | `references/debugging.md` | 폐기 · 프로젝트 문서 |
| goppi | `references/governed-contract.md` | 폐기 · 프로젝트 문서 |
| goppi | `references/model-roster.md` | 승계 |
| goppi | `references/outbound-gate.md` | 폐기 · 프로젝트 문서 |
| goppi | `references/production-floor.md` | 폐기 · 프로젝트 문서 |
| goppi | `references/repo-bootstrap.md` | 폐기 · 프로젝트 문서 |
| goppi | `references/review-report.md` | 폐기 · 프로젝트 문서 |
| goppi | `references/sandbox-presets.md` | 폐기 · 프로젝트 문서 |
| goppi | `references/skill-authoring.md` | 폐기 · 프로젝트 문서 |
| goppi | `references/verification-ladder.md` | 폐기 · 프로젝트 문서 |
| goppi | `skills/governed/SKILL.md` | 폐기 · 구현 |
| goppi | `skills/harness-eval/SKILL.md` | 폐기 · 하네스 효과 n=1 |
| goppi | `skills/kickoff/SKILL.md` | 폐기 · 구현 |
| goppi | `skills/review/SKILL.md` | 폐기 · 구현 |
| goppi | `skills/scaffold/SKILL.md` | 폐기 · 구현 |
| goppi | `skills/ship/SKILL.md` | 폐기 · 구현 |
| goppi | `templates/PULL_REQUEST_TEMPLATE.md` | 폐기 · 보일러플레이트 |
| goppi | `templates/README.template.md` | 폐기 · 프로젝트 문서 |
| goppi_final | `DECISIONS.md` | 승계(개명) |
| goppi_final | `DESIGN.md` | 폐기 · 프로젝트 문서 |
| goppi_final | `ENFORCEMENT-MAP.md` | 폐기 · 프로젝트 문서 |
| goppi_final | `FOUNDING-IDEA.md` | 승계(개명) |
| goppi_final | `NEXT-SESSION.md` | 폐기 · 프로젝트 문서 |
| goppi_final | `PRD.md` | 폐기 · 프로젝트 문서 |
| goppi_final | `RESEARCH-LIFETIME.md` | 승계(개명) |
| goppi_final | `harness/goppi/L0.md` | 폐기 · 프로젝트 문서 |
| goppi_final | `harness/probe/README.md` | 승계 |
| goppi_final | `progress.md` | 폐기 · 프로젝트 문서 |
| goppi_final | `records/2026-08-02-worth-hypothesis.md` | 폐기 · 프로젝트 문서 |
| goppi_final | `records/2026-08-02-trustworthy-completion-evaluation-protocol.md` | 폐기 · 프로젝트 문서 |
| goppi_final | `records/2026-08-06-empty-state-runtime-verification.md` | 폐기 · 프로젝트 문서 |
| goppi_final | `records/2026-08-06-session1-prompt.md` | 폐기 · 세션 인계 |
| goppi_final | `records/2026-08-06-slice1-runtime.md` | 폐기 · 프로젝트 문서 |
| goppi_final | `records/2026-08-06-vanilla-smoke-baseline.md` | 승계(개명) |
| goppi_final | `records/2026-08-07-output-surface-probe.md` | 승계(개명) |
| goppi_final | `records/2026-08-07-session2-prompt.md` | 폐기 · 세션 인계 |
| goppi_final | `records/2026-08-07-session3-prompt.md` | 폐기 · 세션 인계 |
| goppi_final | `records/2026-08-07-slice1-closure.md` | 폐기 · 프로젝트 문서 |
| goppi_final | `records/2026-08-08-headless-runner.md` | 폐기 · 프로젝트 문서 |
| goppi_final | `records/2026-08-08-research-refresh.md` | 승계(개명) |
| goppi_final | `records/2026-08-08-session4-prompt.md` | 폐기 · 세션 인계 |
| goppi_final | `records/2026-08-08-session5-prompt.md` | 폐기 · 세션 인계 |
| goppi_final | `records/2026-08-08-user-channel-render-verdict.md` | 승계(개명) |
| goppi_final | `records/2026-08-11-edge-and-carrier-verdict.md` | 폐기 · 프로젝트 문서 |
| goppi_final | `records/2026-08-11-session6-prompt.md` | 폐기 · 세션 인계 |
| goppi_final | `records/2026-08-12-agent-failure-research.md` | 승계(개명) |
| goppi_final | `records/2026-08-12-codex-problem-review.md` | 승계(개명) |
| goppi_final | `records/2026-08-12-codex-remap-review.md` | 승계(개명) |
| goppi_final | `records/2026-08-12-newproblem-evidence-research.md` | 승계(개명) |
| goppi_final | `records/2026-08-12-postlaunch-evidence-research.md` | 승계(개명) |
| goppi_final | `records/2026-08-12-problem-map-draft.md` | 승계(개명) |
| goppi_final | `records/2026-08-12-session7-prompt.md` | 폐기 · 세션 인계 |
| goppi_final | `records/2026-08-12-user-wishes-research.md` | 승계(개명) |
| goppi_final | `records/2026-08-13-codex-v3-review.md` | 폐기 · 설계 검수 |
| goppi_final | `records/2026-08-13-codex-v4-review.md` | 폐기 · 설계 검수 |
| goppi_final | `records/2026-08-13-codex-v5-verdict.md` | 승계(개명) |
| goppi_final | `records/2026-08-13-p40-45-evidence-research.md` | 승계(개명) |
| goppi_final | `records/2026-08-13-problem-map-v3-draft.md` | 승계(개명) |
| goppi_final | `records/2026-08-13-session8-prompt.md` | 폐기 · 세션 인계 |
| goppi_final | `records/2026-08-13-url-verification.md` | 폐기 · 프로젝트 문서 |
| goppi_final | `records/2026-08-17-codex-design-rev0-review.md` | 폐기 · 설계 검수 |
| goppi_final | `records/2026-08-17-codex-design-rev1-review.md` | 폐기 · 설계 검수 |
| goppi_final | `records/2026-08-17-codex-design-rev2-review.md` | 폐기 · 설계 검수 |
| goppi_final | `records/2026-08-17-codex-design-rev3-review.md` | 폐기 · 설계 검수 |
| goppi_final | `records/2026-08-17-e1-e2-transition-probe.md` | 폐기 · 프로젝트 문서 |
| goppi_final | `records/2026-08-17-pretool-ask-exit-code-fix.md` | 승계(개명) |
| goppi_final | `records/2026-08-17-reverse-audit.md` | 폐기 · 프로젝트 문서 |
| goppi_final | `records/2026-08-17-session9-prompt.md` | 폐기 · 세션 인계 |
| goppi_final | `records/2026-08-17-stop-render-observation.md` | 승계(개명) |
| goppi_final | `records/2026-08-18-blocker1-channel-probe.md` | 승계(개명) |
| goppi_final | `records/2026-08-18-codex-g4-external-review.md` | 폐기 · 설계 검수 |
| goppi_final | `records/2026-08-18-external-trial.md` | 승계(개명) |
| goppi_final | `records/2026-08-18-g4-promotion-hardening.md` | 폐기 · 프로젝트 문서 |
| goppi_final | `records/2026-08-18-session10-prompt.md` | 폐기 · 세션 인계 |
| goppi_final | `records/2026-08-18-session11-prompt.md` | 폐기 · 세션 인계 |
| goppi_final | `records/2026-08-19-confirmation-trial-preregistration.md` | 승계(개명) |
| goppi_final | `records/2026-08-19-fp-instrumentation.md` | 승계(개명) |
| goppi_final | `records/2026-08-19-session12-prompt.md` | 폐기 · 세션 인계 |
| goppi_final | `records/2026-08-19-session13-prompt.md` | 폐기 · 세션 인계 |
| goppi_final | `records/2026-08-19-trial-web-integration.md` | 승계(개명) |
| goppi_final | `records/2026-08-20-trial-goppi_test-log.md` | 승계(개명) |
| goppi_final | `records/INDEX.md` | 승계 |
| goppi_final | `reviews/slice1-handover-review-protocol.md` | 폐기 · 프로젝트 문서 |
