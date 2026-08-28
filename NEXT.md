# 다음 세션 인계 — 만들기 시작

> 작성 2026-08-24 · 갱신 **2026-08-28** · **이 문서는 낡는다.** 만들 것이 하나씩 끝나면 갱신하고,
> 전부 끝나면 지운다. 정본은 [`direction/`](direction/)이고 이 문서는 **작업 지시서**다.

## 이 세션에서 할 일

🎉 **완료의 정의가 충족됐다 (2026-08-28).**

```
new-project.sh → /kickoff → 이슈 → 브랜치 → PR → CI → 머지
```

**진짜 프로젝트(`coolbress/divcal`)에서 두 번 돌았고, 두 번째는 차가운 세션이 자율로** 돌았다.
`~~~~~~~~` 로 표시해두었던 `/kickoff` 구간이 실제로 채워졌다. 기록은 §첫 완주 완료.

**다음은 남은 만들 것**이다 — [`direction/04`](direction/04-the-plan.md) 의 ⑥~⑩·⑬.
🔶 그 전에 **소유자 결정 하나**가 걸려 있다(§남은 것).

## ⓪ 먼저 읽을 것 — 3개

| 순서 | 문서 | 왜 |
|---|---|---|
| 1 | [`direction/04-the-plan.md`](direction/04-the-plan.md) | **만들 것 13개 · 원칙 4 · 리서치에서 나온 수치 · 판정 기준** |
| 2 | [`direction/05-the-output-floor.md`](direction/05-the-output-floor.md) | **무엇이 저장소에 남아야 시니어급인가** (**12묶음**) · 아키타입 판정 |
| 3 | [`direction/02-why-past-attempts-failed.md`](direction/02-why-past-attempts-failed.md) §진단의 진단 | **같은 실수를 열 번 했다.** 열한 번째를 하지 않기 위해 |

나머지(`01`·`03`)는 **물어봤을 때만** 읽는다. `01`=요구 6가지의 근거, `03`=리서치 색인.

## 지금 상태

| | |
|---|---|
| 하네스 6세대 | **정리 끝** — 원격 3개 삭제(2026-08-24) · 로컬은 `~/Archive/` |
| 이 저장소 | 공개 · 룰셋 `main protection` 활성 · CI 초록 · **PR로만 머지 가능** |
| 벽 | **실물 확증 4/4** — 직접 푸시·빨간불 머지·`--admin` 강제 머지 전부 거부 |
| 만들 것 | **7/13** — ①②③④⑤⑪⑫. 🎉 **완료의 정의 충족 2026-08-28** — `divcal` 로 완주했다 |
| 완주 | ✅ **2회** — #1→#2(따뜻한 세션) · **#4→#5(차가운 세션 자율)**. 9·10 회고까지 받았다 |
| 감사 (2026-08-28) | `repo_audit` **4저장소 `RESULT CLEAN findings=0`**. 새 검사 `check_figure_citations` 기준선 16 |
| 정리 | ✅ **완료 2026-08-24 (2차)** — 원격 3개 삭제 · 로컬 5개 `~/Archive/`(1.1GB) · 홈 8표면 0건. ⚠️ 1차의 *"0건"* 은 **틀렸었다** — [2차 기록](legacy/judgments/harness-removal-record-2026-08-24.md) |

## 🎯 완료의 정의 — 이걸 먼저 읽어라

**이 저장소 안에서 도는 검증은 합성 시험이다.**
`standards`는 문서 저장소다 — `package.json`도 락파일도 테스트 스위트도 없다.
그래서 만들 것 대부분이 **여기서는 시험되지 않는다**:

| 여기서 시험되나 | 만들 것 |
|---|---|
| 🟢 된다 | ② 재사용 워크플로의 **기계장치**(호출이 도는가 · 검사 이름이 무엇이 되는가) · ⑫ gitleaks |
| 🔴 **안 된다** | ⑤ `new-project.sh`(새 저장소를 실제로 만들어야) · ③ 템플릿(인스턴스를 떠야) · ④ `/kickoff`(진짜 기획거리가 있어야) · ⑦ 세션 훅(이슈·마일스톤이 있어야) · ⑩ `floor-check`(락파일이 없어 FAIL만 난다) · **②의 내용**(`python-ci.yml` 은 uv 프로젝트가 있어야 돈다) |

> ⚠️ **위 🟢 칸의 첫 판은 *"이 저장소 `ci.yml`을 `uses:` 호출로 바꿔보기"* 였다. 그렇게 하면 안 된다.**
> 재사용 호출은 검사 이름을 `{호출잡}/{피호출잡}` 으로 바꾼다(실측 · 코퍼스 CPR-007).
> 이 저장소 룰셋은 `integrity` 를 요구하므로, 바꾸는 순간 그 이름이 영원히 보고되지 않아
> **자기 벽을 자기가 부순다.** 기계장치는 **별도 프로브 워크플로를 얹어서** 재는 것이 안전하다
> (기존 `integrity` 잡을 건드리지 않으므로 벽이 유지된다). 실제로 그렇게 쟀다 — PR #33.

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
리서치의 처방도 같다 — **walking skeleton: 첫 조각은 end-to-end 한 줄기**(Cockburn)
([`direction/05`](direction/05-the-output-floor.md) 바닥의 *테스트* 묶음 · ⚠️ 2026-08-26 정정 — 이전 판은 `03` 을 가리켰으나 거기에 없다).

## 순서 — ⑤를 먼저 하면 막힌다

첫 판의 권장 순서(⑤ → ② → ③)는 **의존이 정반대**라 쓸 수 없다:

| | 무엇이 먼저 있어야 하나 |
|---|---|
| ⑤ `new-project.sh` | `gh repo create --template coolbress/project-template` → **③** |
| ③ 템플릿의 5줄 `ci.yml` | `uses: coolbress/workflows/...` → **②** |
| ⑤ `ruleset.json` | 요구하는 context 를 **②가 실제로 내보내야** 한다 |

마지막 줄이 특히 위험하다 — ②가 없는 채로 룰셋만 걸면 필수 검사가 영원히 보고되지 않아
**머지가 불가능한 저장소**가 나온다.

**순서: ② ✅ → ③ ✅ → ⑤ ✅ → 실전 프로젝트 end-to-end.** ①은 ⑤가 돌면 자동으로 채워졌다.

## ✅ ③⑤ 완료 (2026-08-24) + 루프 1회 통과

| | |
|---|---|
| [`coolbress/project-template`](https://github.com/coolbress/project-template) | 공개 · `is_template` · **도는 uv 프로젝트**(빈 껍데기가 아니다) |
| [`coolbress/workflows`](https://github.com/coolbress/workflows) `new-project.sh` | 저장소 생성 + **서버 바닥 설치** — 벽 · 시크릿 탐지 · Dependabot · SHA 강제 · 머지 설정. **전 단계 fail-closed** ⚠️ *줄 수로 적지 않는다* (감사 E-5) |

### 템플릿이 빈 껍데기면 안 되는 이유 — 설계 제약 하나

`uv sync --locked` 는 **락파일이 없으면 실패한다.** 그런데 벽 때문에 빨간 상태에서는
아무것도 머지할 수 없다. 즉 **템플릿이 도는 프로젝트가 아니면 인스턴스의 첫 PR 부터 막힌다.**
그래서 템플릿에 `pyproject.toml` · `uv.lock` · 패키지 · 테스트가 실제로 들어 있고,
푸시 전에 로컬에서 5개(lint·format·typecheck·test·build)를 통과시켰다.

### 🔬 end-to-end 1회 통과 — 실측

`new-project.sh loop-probe` 로 만든 임시 저장소에서:

```
new-project.sh → 이슈(AC-1·AC-2) → 브랜치 → PR → CI 4/4 초록 → 머지 → 이슈 자동 종료
```

⑤가 실제로 건 것: `public` · `secret_scanning: enabled` · `push_protection: enabled` ·
룰셋 `active` · `우회: never` · 요구 검사 `ci / lint`·`ci / typecheck`·`ci / test`·`ci / build`.

**벽 4/4** (새 저장소에서 다시): 직접 푸시 `GH013` 거부 · 브랜치 허용 ·
빨간불 머지 거부 · **소유자 `--admin` 강제 머지 거부**(`Required status check "ci / typecheck" is failing`).

### 4개로 쪼갠 설계가 값을 한 지점

일부러 타입 힌트를 뺀 PR 에서:

```
ci / lint        pass   ← ruff 는 통과시켰다
ci / typecheck   fail   ← mypy strict 만 잡았다
ci / test        pass
ci / build       pass
```

한 잡 4스텝이었으면 *"CI 실패"* 하나만 보이고 **무엇이 왜 실패했는지 알 수 없었다.**

`loop-probe` 는 확인 후 **삭제했다** — 임시 프로브였다.

## ✅ 첫 완주 완료 — `divcal` (2026-08-27 착수 · **2026-08-28 완료**)

### 저장소를 만드는 데까지 나온 결함 넷 (2026-08-27)

**저장소를 하나 만드는 데까지 실제 결함 넷이 나왔다.** 전부 *"돌려보니 달랐다"* 에서 나왔다.

| | 무엇이 틀렸나 | 어떻게 드러났나 |
|---|---|---|
| **1** | `new-project.sh` 가 **재사용 워크플로를 allowlist 에 안 걸었다** | 감사 범위를 넓히자 즉시 — 그대로 뒀으면 **첫 CI 가 `startup_failure`** 로 죽고 저장소가 잠겼다 |
| **2** | 🔴 **붙여넣은 토큰의 공백 한 칸** | `gh api` 는 되는데 `git push` 만 거부. **헤더는 서버가 공백을 잘라내고 HTTP Basic 은 base64 안에 남긴다** |
| **3** | **실패를 너무 늦게 안다** | `uv lock`·`sync` 까지 다 하고 푸시에서 넘어졌다 → **클론 직후 푸시 선확인**으로 |
| **4** | 새 프로젝트를 **토큰 목록에 추가해야 하는데 아무도 안 알려준다** | 저장소는 완벽한데 **에이전트가 라벨 하나 못 만들었다**(403). 이제 스크립트가 말한다 |

🟢 **fail-closed 가 실사용에서 두 번 발화했고 두 번 다 정확했다** — 저장소를 만들고, 실패하고, **지웠다.**
**벽 없는 저장소를 안 남겼고 재시도 비용이 0 이었다.**

### 완료 조건 진행

| # | | 결과 |
|---|---|---|
| 1 | 저장소 생성 | ✅ (3번째 시도 — 위 결함 2·3 때문) |
| 2 | **서버 설정 확인** | ✅ squash 전용·자동삭제 · 시크릿탐지·푸시보호·Dependabot 전부 `enabled` · Actions `selected`+SHA강제+**패턴 2개** · CodeQL `configured` · 룰셋 1개·우회자 0·strict |
| 3 | `/kickoff` 인터뷰 | ✅ 4문항 · `[확인 필요]` 0개 |
| 4 | 여덟 답을 이슈 본문에 | ✅ [#1](https://github.com/coolbress/divcal/issues/1) — Issue Form 3칸 + 추가 5절 |
| 5 | 작은 실제 기능 + 테스트 | ✅ src 205줄 · 테스트 15개 |
| 6 | 브랜치 → PR | ✅ [#2](https://github.com/coolbress/divcal/pull/2) |
| 7 | required check 전부 보고·통과 | ✅ 6/6 |
| 8 | squash 머지 · `main` | ✅ 이슈 자동 종료 · 브랜치 자동 삭제 |
| 9 | 🔴 세션을 닫았다 다시 연다 | ✅ 2026-08-28 |
| 10 | 🔴 무엇을 못 찾는지 기록 | ✅ **아래 회고** |

⚠️ **`divcal` 을 `REPOS` 에 넣었다.** 기본 기대값(`PROJECT_CHECKS`·`PROJECT_ACTION_PATTERNS`)만으로
**그대로 통과**했다 — 오늘 *"새 프로젝트는 한 줄이면 끝나게"* 만든 설계가 실물에서 맞았다.

## 🎯 첫 완주 — 완료 조건 열 가지 (2026-08-27)

**저장소가 만들어지는 것은 완주가 아니다.** 여기까지 이어져야 한다:

| # | 무엇 |
|---|---|
| 1 | `divcal` 저장소 생성 (**저장소 밖에서** · 래퍼로 토큰 입력) |
| 2 | 생성 직후 **서버 설정 확인** — 아래 별도 표 |
| 3 | `/kickoff` 인터뷰 완료 |
| 4 | **여덟 답을 이슈 본문에 전부** 기록 (Issue Form 은 셋만 받는다) |
| 5 | **아주 작은 실제 기능 하나**를 테스트와 함께 |
| 6 | 브랜치 → PR |
| 7 | **required check 가 전부 실제로 보고되고 통과** |
| 8 | squash 머지 · `main` 확인 |
| 9 | 🔴 **세션을 닫았다 다시 연다** |
| 10 | 🔴 *"이 프로젝트 계속 진행해줘"* 만 말하고 **무엇을 못 찾는지 기록** |

### 🔬 9·10 결과 — **상태를 못 찾은 게 아니었다**

차가운 세션은 *"이 프로젝트 계속 진행해줘"* 한 줄만 받고 **7단계 만에 정확히 파악했다**:

```
README → git log → find → gh issue list → 소스 4파일 → gh issue view 1 → 로컬 검사
```

그 세션이 **혼자 이슈 [#4](https://github.com/coolbress/divcal/issues/4) 를 내고 PR [#5](https://github.com/coolbress/divcal/pull/5) 로 머지했다.** 회고가 남긴 것:

| | 못 찾은 것 | 회고 원문 |
|---|---|---|
| **①** | **다음 할 일의 순서** | *"백로그가 **부정형 목록**으로만 존재했다. 순위도 이유도 없어서 결국 임의로 추려 물어야 했다. **그 한 번의 질문이 저장소가 답해주지 못한 유일한 것**"* |
| **②** | `pyproject.toml` | 권한 거부 후 재시도 안 함 → *"줄길이 100 을 E501 에러에서 역산했다 — **설정을 읽어서가 아니라 깨져서**"* |
| **③** | `CONTRIBUTING.md` | README 와 PR 템플릿이 **두 번** 가리켰는데 **두 번 다 안 읽힘** |

🔴 **가장 중요한 관측 — 산문 속 포인터는 안 따라간다.** `CLAUDE.md` 가 `coolbress/workflows` 를
**명시**했고 *바닥·정본·생성기* 라는 단어를 다 봤는데 **하나도 안 열었다.** `~/standards` 는
존재조차 몰랐다. → **`NEXT.md` 를 아무리 잘 써도 `divcal` 세션에 안 닿는다**(훅 없음 · 링크 없음).
[`06`](direction/06-how-we-work.md) 의 **상태 probe 를 상상으로 설계하지 않아도 되게 됐다.**

🔴 **③ 이 제일 아프다.** `CONTRIBUTING.md`(57줄, 스텁 아님)가 이미 *"200줄 목표·400줄 상한"* 과
*"세는 건 사람이 읽을 diff 다 — 락파일·생성물은 따로 센다"* 를 적고 있었다. **그날 만든
`ci / diff-size` 의 설계가 거기 이미 있었는데 아무도 안 읽었다.**

### 그래서 고친 것 (2026-08-28)

| | 무엇 | 어디 |
|---|---|---|
| ① | 백로그 **9개를 열린 이슈로** + [#15 추적](https://github.com/coolbress/divcal/issues/15) 이 순서와 근거를 갖는다 | `divcal` |
| ②③ | `CLAUDE.md` → **`AGENTS.md`**(36줄) + 심볼릭 링크. 못 찾은 셋만 적었다 | `divcal` [#16](https://github.com/coolbress/divcal/pull/16) |

**AGENTS.md 에 상태 절은 안 넣었다.** 가변 상태는 `gh issue list` 가 갖는다 — 회고 세션이
시작 30초에 이미 그걸 돌렸다. ETH Zurich(138 repos·5,694 PR): **150줄 초과는 효용 체감**이고
*"비관련 내용은 선택적 무시가 아니라 **지시 전체의 무시**를 부른다."*

### 2번 — `divcal` 은 아직 자동 감사 밖이다

`repo_audit` 의 `REPOS` 에 **한 줄 더해야** 감사된다(템플릿 프로젝트는 기대값이 같아서 그거면 끝난다).
더하기 전까지는 손으로 확인한다:

Actions allowlist **두 패턴** · required check **전부** · CodeQL · secret scanning + push protection ·
Dependabot · 룰셋 **1개** · bypass **없음** · strict · squash 전용 · **실제 PR 의 모든 검사 보고**

## ✅ 그래서 완료의 정의는 **충족됐다** (2026-08-28)

```
new-project.sh → /kickoff → 이슈 → 브랜치 → PR → CI → 머지
                 ~~~~~~~~  ← 이 구간이 채워졌다
```

*아이디어 → 과제 번역* 구간이 **진짜 프로젝트에서 두 번** 돌았다. 두 번째는 차가운 세션이
**자율로** 했고, 그 세션이 낸 이슈 #4 에는 `/kickoff` 0절이 요구한 **시중 확인 절**이 들어 있다 —
Snowball Analytics · Sharesight(서비스)와 [`jhauberg/dledger`](https://github.com/jhauberg/dledger)(CLI)를 찾아 job 이 다른 이유 셋을 적었다.

### 오늘 들어간 것 (2026-08-28) — PR 9개 · 릴리스 2개 · 4저장소

| 저장소 | 무엇 |
|---|---|
| `workflows` | [#24](https://github.com/coolbress/workflows/pull/24) `ci / diff-size` 잡 · [#25](https://github.com/coolbress/workflows/pull/25) `/kickoff` 0절을 **시중 확인**으로 · [#26](https://github.com/coolbress/workflows/pull/26) 룰셋에 등재 · [#27](https://github.com/coolbress/workflows/pull/27) 멈춤 게이트 → **3갈래 판정** · **v3.2.0 · v3.3.0** |
| `project-template` | [#13](https://github.com/coolbress/project-template/pull/13) 핀 v3.2.0 |
| `divcal` | [#2](https://github.com/coolbress/divcal/pull/2) 첫 기능 · [#3](https://github.com/coolbress/divcal/pull/3) 핀 v3.2.0 · **[#5](https://github.com/coolbress/divcal/pull/5) 차가운 세션이 자율로** · [#16](https://github.com/coolbress/divcal/pull/16) `AGENTS.md` |
| `standards` | [#105](https://github.com/coolbress/standards/pull/105) 감사 기대값 · [#106](https://github.com/coolbress/standards/pull/106) 파이썬 버전 고정 · [#107](https://github.com/coolbress/standards/pull/107) 수치 축·표본 + 새 검사 |

🔴 **그날 배운 것 하나가 세 저장소를 관통한다 — *문서에만 있는 규칙은 발화하지 않는다*.**
`divcal` #1 이 이슈 본문에 *"400줄 이하"* 를 써놓고 436줄을 냈는데 **아무것도 막지 않았다.**
그래서 문장을 검사로 바꿨고(`ci / diff-size`), 같은 형태를 `standards` 에서도 찾아
(`X/Y` 표기를 축 없이 씀) **검사로 바꿨다**(`check_figure_citations`).

⚠️ **다만 계량기가 규칙만큼 중요했다.** 그 PR 을 새 계량기로 다시 재면 **385줄로 통과**한다 —
**규칙이 틀린 게 아니라 계량기가 틀렸었다**(README 산문이 코드와 같은 무게로 세어졌다).

### 🔶 남은 것 — 소유자 결정 하나

**바닥의 `CONTRIBUTING` 요구를 `present` → `adequate` 로 올릴 것인가.**
`census-gov-adequacy`(n=2,000·내용 파싱): present **61.5%** · adequate **41.2%** — **있는 것 중 1/3 이 스텁**이다.

🔴 **문서 한 줄이 아니다.** 진짜로 하려면 **검사가 따라오고**, 그게 **만들 것 ⑩ `floor-check`** 의
첫 조각이다. 안 붙이면 오늘 고친 그 병을 새로 만드는 것이다.

⚠️ **`CONTRIBUTING` 자체는 바닥에서 빼지 않기로 확정했다** — 근거는 두 갈래다.
`census-governance-floor`(**n=6,582**)에서 별 구간을 고정해도 **`AGENTS.md` 채택 저장소가
CONTRIBUTING 을 더 갖는다**(`<1k` 63.3% 대 18.0% · `10k+` 83.9% 대 63.3%). 대체 신호가 없다.
시중 조사(30일)도 같은 방향이었다 — 대체 담론 자체가 없고, 오히려 **AGENTS.md 쪽이 역풍**을 맞는다.

## ✅ ④ 완료 (2026-08-24) — `/kickoff`

`coolbress/workflows` 의 `commands/kickoff.md`. `~/.claude/commands/` 에는 **사본이 아니라
심볼릭 링크**로 건다 — 본문이 벽 안에서 버전 관리되고 `git pull` 로 갱신이 전파된다.

코퍼스의 [`elicitation-interview-build-standard`](corpus/aspects/01-requirements-planning/elicitation-interview-build-standard.md)에서
도출했다: Mom Test 스타일 · 턴당 2문항 · 정보이득 질문 선택 · 위험 비례 깊이 8/12/18 ·
8개 커버리지 · `[확인 필요]` 마커 · AC 안정 ID + 검사 매핑 + `UNVERIFIABLE` · 잠금 게이트.

**핵심은 흔한 실수 목록이다.** 실증(RE'25 · arXiv 2507.02858)은 LLM 인터뷰어가
**그 목록을 쥐고 있을 때만** 사람보다 나은 후속 질문을 한다는 것을 보였다 —
있으면 좋은 게 아니라 이 커맨드가 값을 하는 이유다.

0번 절은 **"이미 있는 것인지 먼저 확인"** 이다. 이 확인을 건너뛴 실수가 **열 번** 있었고, **그 절이 이 세션에서 두 번 발화해 두 번 다 막았다**(`zipline Ledger` · `LedgerLens`).

## ✅ ② 완료 (2026-08-24) — `coolbress/workflows`

공개 저장소. main 보호됨. **직접 푸시 `GH013` 거부 실측.**

| 파일 | 무엇 |
|---|---|
| `.github/workflows/python-ci.yml` | 재사용 CI — **`lint`·`typecheck`·`test`·`build` 4개 별도 잡**. uv·ruff·mypy·pytest. Actions 전부 SHA 핀 · `permissions: contents: read` |
| `.github/workflows/ci.yml` | 자기 검사 — actionlint(다이제스트 핀). 잡 이름 `integrity` |
| `ruleset.json` | ⑤가 `--input` 으로 쓸 벽의 실물 |

**4개로 쪼갠 이유**: 바닥이 *"lint·typecheck·test·build를 **각각 별도 required check**로"* 를
MUST 로 요구한다([`05`](direction/05-the-output-floor.md) §CI/CD). 한 잡 4스텝이면 첫 실패에서
멈춰 나머지 상태를 알 수 없고 룰셋이 개별 검사를 요구할 수도 없다.

### 🔴 ③·⑤가 반드시 지켜야 할 결합

검사 이름은 **`{호출잡}/{피호출잡}`** 이다(실측 · CPR-007). 호출잡을 `ci` 로 두면:

```
ci / lint     ci / typecheck     ci / test     ci / build
```

`ruleset.json` 이 요구하는 것도 이 네 이름이다. **템플릿의 호출잡 이름을 바꾸면 룰셋이
요구하는 이름이 영원히 보고되지 않아 저장소가 조용히 머지 불가로 잠긴다.**

### ② 에 그 뒤 들어간 것 · 아직 없는 것

*"루프가 한 번 초록으로 돈 뒤에 붙인다"* 는 규칙(walking skeleton · *벽보다 도구를 먼저 늘리기 ✕*)을
지켰고, 루프가 돌자 순서대로 붙였다:

| | 무엇 | 언제 |
|---|---|---|
| ✅ | **`ci / secrets`**(gitleaks) — 푸시 보호가 통과시키는 **개인키 PEM** 을 잡는다 | v3.1.0 |
| ✅ | ⑫ **SAST** — 공개는 CodeQL default setup ([근거](audit/SAST-CODEQL-VS-SEMGREP.ko.md)) | 2026-08-27 |
| ✅ | **`ci / diff-size`** — 리뷰 가능성 게이트. 룰셋 등재까지 | v3.2.0 · v3.3.0 |
| ⬜ | pipeline-guard (테스트 동반 검사) | — |
| ⬜ | ⑩ `floor-check` | 위 §남은 것의 결정에 걸려 있다 |
| 🔴 | **비공개 → Semgrep OSS** — *결정됐고 미구현*. `--private` 는 시작 전에 거부한다 | 측정 장비는 `workflows` 의 `research/c2-sast` 브랜치에 **주차돼 있다** |

✅ **`python-ci.yml` 의 내용은 이제 실제 프로젝트에서 돈다** — `divcal` 이 PR 4개를 그걸로 태웠다.

### ⑤의 실물 (참고 — 이 저장소에 걸린 것)

```bash
gh api repos/coolbress/<repo>/rulesets -X POST --input ruleset.json
```

`ruleset.json`의 핵심: `bypass_actors: []` (비우면 소유자도 못 넘는다 — 실측 확인),
`required_status_checks: [{context: "integrity"}]`, `pull_request.required_approving_review_count: 0`
(솔로는 자기 PR을 승인할 수 없다 — 승인 도장을 흉내내지 않고 CI를 진짜 게이트로 쓴다).

⚠️ **룰셋은 GitHub Free에서 공개 저장소에만 걸린다.** 비공개면 Pro가 필요하다
(실측: `403 Upgrade to GitHub Pro or make this repository public`).

## 🔴 하지 말 것 — 이 프로젝트가 여섯 번 무너진 이유

1. **하네스를 짓지 않는다.** 런타임에 도는 것을 만들면 그게 6세대다.
   판별식: **런타임에 도는가?** 돌면 하네스, 안 돌면 템플릿.
2. **로직을 설정 층에 넣지 않는다.** `new-project.sh`가 20줄을 넘어가면 그게 신호다.
3. **에이전트에게 규율을 프롬프트로 심지 않는다.** 벽은 GitHub에 있다.
4. **새로 짓기 전에 [`MAP.md`](MAP.md)를 주제어로 훑는다** (README 절대규칙 6).
   *"없다"* 고 단정하기 전에 확인한다 — 이 실수를 **열 번** 했다.
5. **지적을 받으면 그 좌표가 아니라 그 종류를 전 저장소에 grep한다** (절대규칙 7).

## 이 저장소에서 작업할 때

```bash
python3 tools/validate_corpus.py        # 구조·프론트매터·매니페스트·URL 대장
node    tools/build-routes.mjs --check  # 라우팅 지도 최신 여부
python3 tools/repo_audit.py             # 서버 설정 drift — 읽기만 한다 (4저장소)
python3 tools/check_pr_title_conformance.py   # PR 제목 규약 준수율 — 전환 조건 ⓑ (네트워크)
python3 tools/check_template_drift.py          # 인스턴스가 템플릿을 따라오나 (네트워크)
```

문서를 고쳤으면 `tools/rebuild_after_manifest.py`와 `build-routes.mjs`를 **다시 돌려야** CI가 통과한다.
`main`은 보호돼 있으므로 **브랜치 → PR → CI 초록 → 머지**로만 들어간다.

### 🔒 자격증명은 둘로 갈려 있다 (A-1 · 2026-08-27)

| | 무엇 | 누가 |
|---|---|---|
| **`GH_TOKEN`**(기본) | fine-grained — **쓰기**: Contents · Issues · PRs · Workflows / 🔑 **읽기**: + Administration · Code scanning | **에이전트** |
| 관리자 토큰 | classic(`repo`·`workflow`·`delete_repo`·`security_events`) · **30일 만료** | **사람만** — 이 컴퓨터에 **저장하지 않는다** |

🔴 **관리자 열쇠는 방에 없다** (2026-08-27). `gh auth logout` 으로 열쇠고리에서 뺐다.
관리자 작업은 **그때그때 붙여넣는다**:

```bash
cd ~   # 🔴 저장소 밖에서 — 스크립트가 저장소 안이면 멈춘다
~/workflows/tools/with-admin-token.sh ~/workflows/new-project.sh <이름>
```

🔴 **토큰을 명령줄에 쓰지 마라.** `GH_TOKEN=... 명령` 은 **`~/.zsh_history` 에 그대로 남는다**
(`histignorespace` 는 앞에 공백이 있을 때만 듣는다). 래퍼가 **물어본다.**

**그 프로세스가 사는 몇 초 동안만 존재한다** — 열쇠고리에도 파일에도 안 남는다.

🔑 **읽기를 준 이유**: 안 주면 `repo_audit` 이 **아무것도 확인하지 못한다**(`unknown=12`).
**감사기가 눈을 뜨는 것과 벽이 무너지는 것은 다른 문장이다.** 쓰기는 그대로 전부 403 이다 —
룰셋 수정·삭제 · Actions 정책 · 저장소 설정 · 환경 생성 · CodeQL 켜기 · 시크릿.

`~/.zshenv` 가 `~/.config/gh-agent-token`(0600)을 읽어 `GH_TOKEN` 에 건다.
**`.zshrc` 가 아니라 `.zshenv` 인 이유**: `.zshrc` 는 **대화형 셸만** 읽어 도구 셸에 안 닿는다.

🔴 **`env -u GH_TOKEN` 은 이제 아무것도 안 준다** — 실측: `You are not logged into any GitHub hosts`.
규율이 아니라 **없는 것**이다. 이전 판의 *"막히면 토큰을 빼고 실행하라"* 안내는 삭제했다.

**403 이 나면 그것이 정상이다.** 관리자 작업(룰셋 · Actions 정책 · 시크릿 · Environments ·
CodeQL default setup)은 **사람이 한다.** 에이전트는 명령을 만들어 넘긴다.

## 열린 공백 — [`audit/GAPS.ko.md`](audit/GAPS.ko.md) §R5

| | 무엇 | 영향 |
|---|---|---|
| ~~**R5-1**~~ | ✅ **종료** — 9건 전부 재검증(배치 A·B·C). 유지 3 · 수정/한정 4 · 삭제 2 · **목록 자체 오류 3건** | — |
| **R5-2** | 요구 ⑥(막다른 길 신호)에 **만들 것이 없다** | circuit-breaker가 출발점 |
| **R5-3** | 요구 ③이 **협조 기반 수단**으로 채워진다 | 지표 ⓐⓑⓒ로 2주 관찰 |
| **R5-6** | 계보의 **"느낀점"이 비어 있다** — [`legacy/LINEAGE.md`](legacy/LINEAGE.md) §5b | **소유자만 쓸 수 있다** |
| **R5-8** | 아키타입 층은 **설계 닫힘**, 구현은 만들 것 ④⑩⑬ | 첫 공개 웹앱 때 |
| ~~**R5-10**~~ | ✅ **종료** — ④ `/kickoff` 4종(ⓐ공개·ⓑ개인정보·ⓒ연구·ⓓ이미있음 n=3) 전부 통과 | — |
| ~~**R5-13**~~ | ✅ **종료 2026-08-25** — `direction/03` 하중 18건 재검증 5배치 완료(프로그램 #49 1단계). 유지 6 · 한정/수정 7 · 철회/삭제 3 · 판단으로 재분류 2 | — |
| ~~**R5-12**~~ | ✅ **종료 2026-08-25** — 위반 20건(CPR 8·GEB 6·CAS 6) 수정 후 **검사 범위를 전 문서로 확대**. `claim_rows_total=112` · 오류 0 | — |
| ~~**R5-15**~~ | ✅ **종료 2026-08-25** — 7건은 폐기가 아니라 **이동**이었다(`interpretation/` → `legacy/judgments/goppi/`). 경로 재지정 후 CI 에 `unittest discover` 추가. **28/28** | — |
| ~~**R5-14**~~ | ✅ **종료 2026-08-25** — 굵게 42행 전부 해제 + Evidence 위반 10행 수정. **재검증 프로그램이 자기 산출물만 검사 밖에 두고 있었다** | — |
| ~~**R5-11**~~ | ✅ **종료 2026-08-25** — **의도적 Python 전용으로 확정**(소유자 결정). 실측: `~/divtadel` 은 **원격 없음 · 테스트 0 · lint 0** 이라 4검사 워크플로를 만들면 그 프로젝트가 첫 PR 부터 자기잠금된다 | 다시 여는 조건은 `direction/04` §범위 결정 |

## 2주 뒤 판정 기준

[`direction/04`](direction/04-the-plan.md) *"판정 기준 — 사전 등록"* 에 지표가 박혀 있다.
**결과를 보고 기준을 옮기지 않는다.**
