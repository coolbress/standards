---
id: aspect-05-scm-workflow--github-enforcement-boundaries--facts-2026-08
title: "GitHub 집행 경계 — 플랜별 룰셋 가용성과 이슈 폼의 API 우회 (facts 2026-08)"
parent: aspect-05-scm-workflow
kind: research-log
evidence_track: lit
status: draft
language: ko
last_updated: "2026-08-24"
method: "질문 2개로 한정한 표적 조사(2026-08-24). ① Free 플랜 + 비공개 저장소에서 룰셋/브랜치 보호가 실제로 집행되는가 ② 이슈 폼의 required 검증이 REST/CLI 경로에도 적용되는가. 1차 출처는 GitHub 공식 문서, 여기에 소유자 계정(coolbress)에 대한 로컬 API 실측을 병기. 포함: 룰셋 API 응답·이슈 생성 API 파라미터 목록. 제외: Team/Enterprise 플랜 동작(범위 밖), Issue Types(미조사). 종료 기준: 두 질문 각각에 1차 근거 또는 재현 가능한 실측이 붙을 것."
sources:
  - "https://docs.github.com/rest/repos/rules"
  - "https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms"
  - "https://docs.github.com/en/rest/issues/issues"
---

# GitHub 집행 경계 — 플랜과 API 경로

**선행 문서가 이미 다룬 것**: 저장소 가시성×플랜에 따른 기능 게이트는
[`../04-build-ci-engineering/visibility-provision-matrix.md`](../04-build-ci-engineering/visibility-provision-matrix.md)
(2026-06-26)가 규정한다 — 브랜치 보호/룰셋과 Environments는 `PUB ✅ / PRIV-free ⛔ / PRIV-paid ✅`,
그리고 **Actions 분은 공개 무제한 / 비공개 Free 2,000분·월 과금**이다. 그 문서가 정본이다.

**이 문서가 더하는 것은 두 가지다.**
1. 위 게이트가 **실제 API 응답으로 어떻게 나타나는지**의 재현 가능한 실측(GEB-002) — 문서의 처방이
   현장에서 어떤 실패 모양을 갖는지 고정한다.
2. **이슈 폼의 required 검증이 REST/CLI 경로에 걸리지 않는다**는 사실(GEB-003·004) — 선행 census
   ([`../24-.../issue-pr-writing-conventions.md`](../24-governance-collaboration-compliance/issue-pr-writing-conventions.md))는
   템플릿의 *작성법*을 다뤘고 *집행 경로*는 다루지 않았다. 이 빈칸이 채워지는 자리다.

이 두 항목은 부모 aspect의 tension T3(*로컬/클라이언트 측 검사는 게이트가 아니다*)와 같은 계열의
결론으로 수렴한다.

## Claim table

| Claim ID | Class | Claim and scope | Evidence | Confidence | Valid as of / expiry |
|---|---|---|---|---|---|
| GEB-001 | vendor-behavior | 룰셋(및 클래식 브랜치 보호)은 GitHub Free에서 **공개 저장소에만** 적용된다. 비공개는 Pro 이상. **신규 사실이 아니다** — `visibility-provision-matrix.md`(2026-06-26)가 이미 `PRIV-free ⛔`로 규정했고, 이 줄은 2026-08-24 실측으로 그것이 여전히 참임을 확인한 것이다. | 선행 matrix + 로컬 실측(GEB-002)이 반환한 GitHub 문구 | high | 2026-08-24; 플랜 정책 변경 시 재확인 |
| GEB-002 | local-census | 소유자 계정 coolbress에서 비공개 저장소 `fyan`·`goppi`의 `GET /repos/{o}/{r}/rulesets`는 **403**과 `"Upgrade to GitHub Pro or make this repository public to enable this feature."`를 반환한다. 공개 저장소 `VertexLab`의 같은 호출은 **200**과 `enforcement: active`인 룰셋 1건을 반환한다. | 2026-08-24 `gh api` 실행 | high (n=3, 단일 계정) | 2026-08-24; 플랜 변경 시 무효 |
| GEB-003 | vendor-behavior | `POST /repos/{owner}/{repo}/issues`의 파라미터는 `title`(필수)·`body`·`milestone`·`labels`·`assignees`·`issue_field_values`·`type`이다. **이슈 템플릿·이슈 폼을 참조하거나 검증하는 파라미터가 없다.** | GitHub REST 문서 | high | 2026-08-24; API 버전 변경 시 재확인 |
| GEB-004 | synthesis | 따라서 이슈 폼의 `validations.required`는 **웹 UI 제출 경로에만** 걸린다. 에이전트나 스크립트가 쓰는 REST/CLI 경로는 폼을 거치지 않으므로 필수 필드가 집행되지 않는다. 이는 우회(bypass)가 아니라 **설계상 별개 경로**다. | GEB-003 + 폼 문서가 "기여자가 폼을 채우면 응답이 마크다운으로 변환되어 본문에 추가된다"고만 규정 | medium-high | 재검토: GitHub이 API에 템플릿 파라미터를 추가하면 |

## 함의 (근거 층에 남기는 범위)

- 폼은 **사람이 웹에서 작성할 때의 안내 장치**다. 기계가 만드는 이슈의 품질을 폼으로 보장할 수 없다.
- 이슈 본문의 필수 항목을 **기계 경로에서도** 요구하려면 집행 지점이 폼이 아니라 **CI 검사**여야 한다.
  이는 부모 aspect의 tension T3(*pre-commit 훅은 게이트가 아니다 — 진짜 게이트는 CI + 브랜치 보호*)와
  같은 형태의 결론이며, 같은 이유(로컬/클라이언트 측 검사는 우회 가능)에서 나온다.
- GEB-001·002가 참인 환경에서는 **CI 검사도 최종 집행이 되지 못한다.** 검사는 돌지만 병합을 막지 못하기
  때문이다. 즉 비공개 + Free 조합에서는 제어 사슬(GHW-007)의 "protected merge" 고리가 빠진다.
- 같은 선택(비공개 유지 vs 공개 전환 vs 유료 전환)에는 **Actions 분 과금**도 함께 걸린다 — 선행 matrix에
  따르면 공개는 무제한, 비공개 Free는 2,000분/월이다. CI를 집행 지점으로 삼는 설계는 이 예산에 민감하다.

## 미해결

- **조사 과정 교훈(2026-08-24)**: 이 문서의 초안은 GEB-001을 신규 발견으로 기술했다. 실제로는
  선행 `visibility-provision-matrix.md`가 이미 규정한 사실이었다. 04(build-ci)와 05(scm)에 같은 주제가
  나뉘어 있어 05만 검색하면 놓친다. **가시성×플랜 게이트는 04에 산다.**

- **Issue Types 및 `issue_field_values`** — GEB-003에서 파라미터의 존재만 확인했다. 저장소 수준의 구조화
  필드가 폼보다 강한 집행 수단인지, API 경로에서도 필수성이 검증되는지는 **미조사**다. 조사 가치가 있다.
- Team/Enterprise 플랜에서의 조직 수준 룰셋 동작은 이 문서의 범위 밖이다.
- 공개 저장소로 전환하는 선택지의 부수 효과(코드 노출·시크릿 스캐닝 동작 차이)는 다루지 않았다.

## Sources
- GitHub REST — Repository rules: https://docs.github.com/rest/repos/rules
- GitHub — Syntax for issue forms: https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms
- GitHub REST — Issues: https://docs.github.com/en/rest/issues/issues
