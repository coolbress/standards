# 다음 세션 인계 — 만들기 시작

> 작성 2026-08-24 · **이 문서는 낡는다.** 만들 것이 하나씩 끝나면 갱신하고,
> 전부 끝나면 지운다. 정본은 [`direction/`](direction/)이고 이 문서는 **작업 지시서**다.

## 이 세션에서 할 일

**[`direction/04-the-plan.md`](direction/04-the-plan.md)의 만들 것 13개를 순서대로 만든다.**
지금은 **①번(브랜치 보호)** 차례다.

## ⓪ 먼저 읽을 것 — 3개

| 순서 | 문서 | 왜 |
|---|---|---|
| 1 | [`direction/04-the-plan.md`](direction/04-the-plan.md) | **만들 것 13개 · 원칙 4 · 리서치에서 나온 수치 · 판정 기준** |
| 2 | [`direction/05-the-output-floor.md`](direction/05-the-output-floor.md) | **무엇이 저장소에 남아야 시니어급인가** (MUST 49) · 아키타입 판정 |
| 3 | [`direction/02-why-past-attempts-failed.md`](direction/02-why-past-attempts-failed.md) §진단의 진단 | **같은 실수를 일곱 번 했다.** 여덟 번째를 하지 않기 위해 |

나머지(`01`·`03`)는 **물어봤을 때만** 읽는다. `01`=요구 6가지의 근거, `03`=리서치 색인.

## 지금 상태

| | |
|---|---|
| 하네스 5세대 | **정리 끝** — 원격 3개 삭제(2026-08-24) · 로컬은 `~/Archive/` |
| 이 저장소 | 공개 · 룰셋 `main protection` 활성 · CI 초록 · **PR로만 머지 가능** |
| 벽 | **실물 확증 4/4** — 직접 푸시·빨간불 머지·`--admin` 강제 머지 전부 거부 |
| 만들 것 | **1/13** (①이 이 저장소에서 검증됨 — 다만 **합성 시험**이다. 위 *완료의 정의* 참조) |
| 정리 | ✅ **완료 2026-08-24** — 홈에 하네스 0건 · 원격 3개 삭제 · 로컬 5개 `~/Archive/`(1.1GB) |

## 🎯 완료의 정의 — 이걸 먼저 읽어라

**이 저장소 안에서 도는 검증은 합성 시험이다.**
`standards`는 문서 저장소다 — `package.json`도 락파일도 테스트 스위트도 없다.
그래서 만들 것 대부분이 **여기서는 시험되지 않는다**:

| 여기서 시험되나 | 만들 것 |
|---|---|
| 🟢 된다 | ② 재사용 워크플로(이 저장소 `ci.yml`을 `uses:` 호출로 바꿔보기) · ⑫ gitleaks |
| 🔴 **안 된다** | ⑤ `new-project.sh`(새 저장소를 실제로 만들어야) · ③ 템플릿(인스턴스를 떠야) · ④ `/kickoff`(진짜 기획거리가 있어야) · ⑦ 세션 훅(이슈·마일스톤이 있어야) · ⑩ `floor-check`(락파일이 없어 FAIL만 난다) |

### 그래서 완료의 정의는 이렇다

> **②③⑤가 끝나면 새 프로젝트를 하나 만들어 end-to-end로 돌린다.**
> `new-project.sh` → `/kickoff` → 이슈 → 브랜치 → PR → CI → 머지가
> **한 번 통과할 때까지 ①~⑤는 미완이다.**

**시험 프로젝트는 작고 진짜인 것**이어야 한다. 가짜 프로젝트로는 *아이디어→과제 번역* 구간이
시험되지 않는다 — 확증시험 세션 2가 소유자 결정으로 *"실제 만들고 싶은 아이디어"*를 쓴 이유다.

### 왜 이 규칙이 필요한가

goppi가 정확히 이 함정에서 죽었다:

> **합성 공격 4종은 0/4로 전부 막았는데, 실사용에서 프로덕션을 바꾼 명령 11건에는 발화 0건이었다.**
> **자기가 만든 시험만 통과한 것이다.**

도구를 만든 곳에서 그 도구를 시험하는 것은 같은 형태다.
리서치의 처방도 같다 — **walking skeleton: 첫 조각은 end-to-end 한 줄기**
([`direction/03`](direction/03-what-research-says.md)).

## ① 지금 할 일 — 브랜치 보호를 새 프로젝트에

이 저장소에는 이미 걸려 있다. **다음 프로젝트에 같은 것을 거는 게 ①의 완성**이다.
그런데 ①은 ⑤(`new-project.sh`)와 같이 만드는 게 낫다 — 매번 손으로 걸 이유가 없다.

**권장 순서**: ⑤ `ruleset.json` + `new-project.sh` → ② `coolbress/workflows` → ③ `project-template`

### ⑤의 실물 (참고 — 이 저장소에 걸린 것)

```bash
gh api repos/coolbress/<repo>/rulesets -X POST --input ruleset.json
```

`ruleset.json`의 핵심: `bypass_actors: []` (비우면 소유자도 못 넘는다 — 실측 확인),
`required_status_checks: [{context: "integrity"}]`, `pull_request.required_approving_review_count: 0`
(솔로는 자기 PR을 승인할 수 없다 — 승인 도장을 흉내내지 않고 CI를 진짜 게이트로 쓴다).

⚠️ **룰셋은 GitHub Free에서 공개 저장소에만 걸린다.** 비공개면 Pro가 필요하다
(실측: `403 Upgrade to GitHub Pro or make this repository public`).

## 🔴 하지 말 것 — 이 프로젝트가 다섯 번 무너진 이유

1. **하네스를 짓지 않는다.** 런타임에 도는 것을 만들면 그게 6세대다.
   판별식: **런타임에 도는가?** 돌면 하네스, 안 돌면 템플릿.
2. **로직을 설정 층에 넣지 않는다.** `new-project.sh`가 20줄을 넘어가면 그게 신호다.
3. **에이전트에게 규율을 프롬프트로 심지 않는다.** 벽은 GitHub에 있다.
4. **새로 짓기 전에 [`MAP.md`](MAP.md)를 주제어로 훑는다** (README 절대규칙 6).
   *"없다"* 고 단정하기 전에 확인한다 — 이 실수를 **일곱 번** 했다.
5. **지적을 받으면 그 좌표가 아니라 그 종류를 전 저장소에 grep한다** (절대규칙 7).

## 이 저장소에서 작업할 때

```bash
python3 tools/validate_corpus.py        # 구조·프론트매터·매니페스트·URL 대장
node    tools/build-routes.mjs --check  # 라우팅 지도 최신 여부
```

문서를 고쳤으면 `tools/rebuild_after_manifest.py`와 `build-routes.mjs`를 **다시 돌려야** CI가 통과한다.
`main`은 보호돼 있으므로 **브랜치 → PR → CI 초록 → 머지**로만 들어간다.

⚠️ **`GITHUB_TOKEN` 환경변수가 keyring 자격증명을 덮는다.** `gh auth` 계열이 막히면:
`env -u GITHUB_TOKEN -u GH_TOKEN gh <명령>`

## 열린 공백 — [`audit/GAPS.ko.md`](audit/GAPS.ko.md) §R5

| | 무엇 | 영향 |
|---|---|---|
| **R5-1** | `direction`이 인용하는 **미승계 claim 9건**(수치 7 + 문장 2) | 1차 출처 재확인 또는 삭제 |
| **R5-2** | 요구 ⑥(막다른 길 신호)에 **만들 것이 없다** | circuit-breaker가 출발점 |
| **R5-3** | 요구 ③이 **협조 기반 수단**으로 채워진다 | 지표 ⓐⓑⓒ로 2주 관찰 |
| **R5-6** | 계보의 **"느낀점"이 비어 있다** — [`legacy/LINEAGE.md`](legacy/LINEAGE.md) §5b | **소유자만 쓸 수 있다** |
| **R5-8** | 아키타입 층은 **설계 닫힘**, 구현은 만들 것 ④⑩⑬ | 첫 공개 웹앱 때 |

## 2주 뒤 판정 기준

[`direction/04`](direction/04-the-plan.md) *"판정 기준 — 사전 등록"* 에 지표가 박혀 있다.
**결과를 보고 기준을 옮기지 않는다.**
