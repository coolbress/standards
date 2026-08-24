---
id: aspect-04-build-ci-engineering--cross-project-reuse--facts-2026-08
title: "프로젝트 간 재사용 층 — 템플릿 저장소·재사용 워크플로·.github 상속 (facts 2026-08)"
parent: aspect-04-build-ci-engineering
kind: research-log
evidence_track: lit
status: draft
language: ko
last_updated: "2026-08-24"
method: "질문 1개로 한정한 표적 조사(2026-08-24): 저장소 하나의 바닥(foundation-floor)을 여러 프로젝트에 반복 설치하지 않으려면 GitHub이 제공하는 기계장치는 무엇이고 각각의 경계는 어디인가. 1차 출처는 GitHub 공식 문서 3편, 여기에 소유자 계정(coolbress)의 Actions 접근 정책 실측을 병기. 포함: 템플릿 저장소 복사 범위·재사용 워크플로 문법과 한계·.github 기본 파일 상속 조건. 제외: 조직(organization) 전용 기능(워크플로 템플릿 피커·조직 룰셋)은 개인 계정 범위 밖이라 경계만 기록. 종료 기준: 세 기계장치 각각에 '무엇이 옮겨지고 무엇이 안 옮겨지는가'가 1차 근거로 확정될 것."
sources:
  - "https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template"
  - "https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows"
  - "https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file"
  - "https://docs.github.com/rest/actions/permissions"
---

# 프로젝트 간 재사용 층

`foundation-floor-artifact-checklist.md`는 **저장소 하나**의 산출물 집합을 규정한다. 이 문서는 그 집합을
**여러 저장소에 반복 설치하는 문제**를 다룬다 — 체크리스트가 커질수록 프로젝트마다 손으로 옮기는 비용이
커지고, 옮기다 빠뜨린 항목이 곧 그 저장소의 가장 약한 바닥이 되기 때문이다(부모 문서 §"weakest floor").

## Claim table

| Claim ID | Class | Claim and scope | Evidence | Confidence | Valid as of / expiry |
|---|---|---|---|---|---|
| CPR-001 | vendor-behavior | 템플릿 저장소로 새 저장소를 만들면 **디렉터리 구조와 파일**(옵션으로 전체 브랜치)이 복사되고 **단일 커밋**으로 시작한다. 문서는 설정·브랜치 보호·룰셋·라벨·시크릿·이슈·협업자의 복사를 규정하지 않는다. 포크와 달리 커밋 이력이 따라오지 않으며, 기여 그래프에는 집계된다. | GitHub 템플릿 문서 | high (복사 대상) / medium (미복사 항목은 문서의 침묵에 근거) | 2026-08-24; 연 1회 |
| CPR-002 | vendor-behavior | 재사용 워크플로는 `{owner}/{repo}/.github/workflows/{file}@{ref}` 로 호출한다. **`.github/workflows/` 바로 아래에 있어야 하며 하위 디렉터리는 지원되지 않는다.** `ref`는 SHA·태그·브랜치. 입력은 `with:`, 시크릿은 `secrets:` 또는 `secrets: inherit`. **최대 10단계**까지 연결된다. 공개·비공개 저장소 모두 대상이 된다. | GitHub Actions 재사용 문서 | high | 2026-08-24; 연 1회 |
| CPR-003 | local-census | 소유자 계정 coolbress의 비공개 저장소 `fyan`·`goppi`에서 `GET /repos/{o}/{r}/actions/permissions/access`는 **`{"access_level":"none"}`** 을 반환한다(기본값). 공개 저장소 `VertexLab`의 같은 호출은 **422**와 `"Access policy only applies to internal and private repositories."` 를 반환한다. | 2026-08-24 `gh api` 실행 | high (n=3, 단일 계정) | 2026-08-24 |
| CPR-004 | synthesis | 따라서 **공개 저장소의 워크플로는 접근 정책 없이 참조 가능**하고, **비공개 저장소의 워크플로를 다른 저장소가 참조하려면 `access_level`을 명시적으로 올려야 한다**(개인 계정은 `user`). 기본값이 `none`이므로 비공개 재사용 저장소는 **설정을 켜기 전까지 조용히 실패한다.** | CPR-002 + CPR-003 | medium-high | 실제 실행 검증 전까지 (아래 미해결 1) |
| CPR-005 | vendor-behavior | 계정 소유 **공개** `.github` 저장소의 커뮤니티 헬스 파일은 해당 파일이 없는 저장소에 기본값으로 쓰인다. **비공개 `.github` 저장소는 지원되지 않는다.** 이슈/PR 템플릿은 특히 공개 `.github`를 요구한다. 저장소가 자체 `.github/ISSUE_TEMPLATE/` 폴더에 파일을 하나라도 두면 **기본 폴더의 내용은 전부 무시된다**(부분 병합 없음). | GitHub 기본 커뮤니티 헬스 파일 문서 | high | 2026-08-24; 연 1회 |
| CPR-006 | local-census | 2026-08-24 기준 `coolbress/.github` 저장소는 존재하지 않는다(404). | `gh api repos/coolbress/.github` | high | 2026-08-24 |
| CPR-007 | local-census | 재사용 워크플로를 호출하면 상태 검사의 **context 이름이 `{호출잡}/{피호출잡}` 이 된다.** `coolbress/standards` 에서 잡 이름 `ci` 로 `python-ci.yml`(잡 4개)을 호출한 PR 의 검사는 `ci / lint`·`ci / typecheck`·`ci / test`·`ci / build` 로 보고됐다. 같은 PR 의 비-재사용 잡 `integrity` 는 이름이 그대로였다. | 2026-08-24 프로브 PR `coolbress/standards#33` | high (n=1, 단일 호출 형태) | 2026-08-24 |
| CPR-008 | synthesis | 따라서 **호출부의 잡 이름이 required status check 의 context 에 포함된다.** 룰셋이 `lint` 를 요구하는데 호출잡이 `ci` 면 `ci / lint` 가 보고되어 요구된 이름은 **영원히 보고되지 않고**, 저장소는 *검사는 초록인데 머지만 막히는* 상태로 잠긴다. 기존 저장소의 잡을 재사용 호출로 **바꾸는** 경우 특히 위험하다 — 이름이 바뀌면서 이미 걸린 룰셋의 요구가 조용히 미충족이 된다. | CPR-007 | high | CPR-007 과 동일 |

## 세 기계장치의 경계 요약

| 장치 | 옮기는 것 | 안 옮기는 것 | 갱신 전파 |
|---|---|---|---|
| 템플릿 저장소 | 파일 트리 | 설정·보호·룰셋·라벨·시크릿 | ❌ 복사 시점 고정 |
| 재사용 워크플로 | 워크플로 **로직** | — (호출부 5줄은 각 저장소에 남음). ⚠️ **검사 이름은 호출부가 정한다**(CPR-007) | ✅ `@ref` 갱신으로 전파 |
| `.github` 상속 | 헬스 파일 기본값 | 저장소가 자체 파일을 두면 전체 무효 | ✅ 원본 수정이 즉시 반영 |

**템플릿 드리프트는 이미 조사된 문제다.** CPR-001의 "복사 시점 고정"은 스캐폴더 생태계가 오래 다뤄 온
문제이고, 선행 census([`brownfield-adoption/track5-census-existing-repo-mode.md`](../../census-data/brownfield-adoption/track5-census-existing-repo-mode.md))의
판정은 **copier/cruft 방식 — 커밋된 answers-file + 템플릿 git 대비 3-way merge**가 gold standard라는 것이다
(재적용 지원 도구는 census 51개 중 3개, 6%). GitHub 템플릿 저장소에는 그 기능이 없으므로, 갱신 전파가
필요한 것을 템플릿에 두는 선택은 이 한계를 받아들이는 것이다 — 또는 copier 계열을 얹거나, 아래처럼
갱신이 필요한 부분만 재사용 워크플로로 밀어내야 한다.

**세 장치는 배타적이지 않다.** 갱신 전파가 필요한 것(CI 로직)은 재사용 워크플로에, 프로젝트마다 달라지는
것(설정 파일)은 템플릿에, 계정 전체 기본값은 `.github`에 두는 분업이 각 장치의 경계와 맞는다.

## 미해결

1. **비공개 재사용 워크플로가 Free 플랜에서 실제로 실행되는지 여전히 미검증.** CPR-002는 문서가
   공개·비공개를 구분하지 않는다는 사실이고, CPR-003은 접근 정책 필드가 존재한다는 사실이다.
   `access_level=user`로 올린 뒤 실제 워크플로 실행이 성공하는지는 **실측되지 않았다.**
   → **2026-08-24 대응: 검증하지 않고 회피했다.** `coolbress/workflows` 를 **공개**로 만들어
   CPR-004의 확정된 절반(공개는 접근 정책 없이 참조 가능)만 쓴다. 실제 호출이 성공하는 것은
   CPR-007의 프로브가 함께 보였다. **비공개 재사용이 필요해지면 그때 이 항목을 닫아야 한다.**
2. **공개 `.github` 저장소의 기본값이 같은 계정의 비공개 저장소에도 상속되는지** 문서가 대상 저장소의
   가시성을 규정하지 않는다. 미확인.
3. 조직 전용 기능(워크플로 템플릿 피커, 조직 수준 룰셋)은 개인 계정에서 쓸 수 없다 — 경계만 기록하고
   조사하지 않았다.

## Sources
- GitHub — Creating a repository from a template: https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template
- GitHub Actions — Reuse workflows: https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows
- GitHub — Creating a default community health file: https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file
- GitHub REST — Actions permissions: https://docs.github.com/rest/actions/permissions
