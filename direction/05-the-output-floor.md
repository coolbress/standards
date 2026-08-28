# 05 — 산출물이 시니어급이려면 무엇이 저장소에 있어야 하나

> 재도출 2026-08-26 · **rev3** — 같은 문서 안의 모순 하나를 없앴다.
> **§근거는 SAST 를 🔵 *"프로젝트 선택"* 으로 정확히 적는데 §남은 만들 것은 *"Semgrep + gitleaks"* 를
> 확정처럼 적고 있었다.** 근거가 서는 층과 아직 안 서는 층을 한 문서가 다르게 말하면 안 된다.
> rev2 · 프로그램 [#49](https://github.com/coolbress/standards/issues/49) **3단계 배치 2**.
> 신설 2026-08-24 — 소유자 지적으로 만들어졌다: `01`~`04`가 *일하는 방식*만 다루고 *산출물의 품질*은 비어 있었다.
> ✅ **2026-08-26 — 그 지적이 마침내 `01` 의 목적 한 줄에도 반영됐다**(rev4). 이 문서는 그 한 줄의 **③ 조각**을 담당한다.
> **이 판은 각 항목의 근거 강도를 본문에 넣는다.** 교정의 내력은 여기 없다 —
> [`COVERAGE-JUDGMENT`](../audit/COVERAGE-JUDGMENT.ko.md) 와 코퍼스 claim table 에 있다.

**강도 표시는 [`03`](03-what-research-says.md) 과 같다**: 🟢 1차 확인 · 🟡 한정 · 🔵 판단(근거로 인용하지 않는다) · ⚪ 미검증.

## 📝 PR 제목 규약 · `Dockerfile` — 두 번째 센서스가 잡은 둘 (2026-08-28)

`check_floor_coverage` 를 **`census-expanded`(n=938)까지** 넓히자 둘이 더 나왔다.
🔴 **둘 다 실물이 하고 있는데 바닥이 침묵이었다** — `AGENTS.md`·이슈 폼·머지 방법과 같은 종류다.

### PR 제목 = Conventional Commits — **squash 와 묶여 있다**

**우리가 실제로 하고 있다**(PR 템플릿이 *"제목은 `type(scope): 요약`"* 을 요구한다). 근거는 결합이다:
**squash 모델에서 PR 제목이 곧 랜딩 커밋**이 되므로, 거기에 규약을 걸면 changelog·SemVer 가
기계적으로 도출된다. 머지 방법과 따로 정할 수 없다.

🔵 **다만 above-census 다.** 측면 05 의 실측(N=2,000): CC PR 제목 strict **21%** · partial 41% ·
mean 0.33. **census 다수가 아니다** — *"자동화 **enabler** 이지 업계 기준선이 아니다"*(tension T1).
`cc_adopted` 는 n=938 에서 **39.4%**.

🔴 **이슈 제목에는 걸지 않는다.** 야생에서 이슈 제목 CC 는 **1~2%** 다 — 대비가 핵심이고,
강제하면 야생 규범과 정면으로 어긋난다(`IPC-001`).

### 🔵 결정 (2026-08-28) — **지금은 강제하지 않는다.** 조건은 아래

**`GAPS` R5-30 종료.** 실측과 근거 넷으로 정했다.

**① 강제 없이 이미 지켜진다.** 4저장소 머지 PR **152건 전수**(확장 어휘 기준):

| | | |
|---|---|---|
| `workflows` (**릴리스하는 유일한 저장소**) | 27/27 | **100%** |
| `project-template` · `divcal` | 20/20 | **100%** |
| `standards` | 103/105 | 98.1% |
| **합계** | **150/152** | **98.7%** |

안 지킨 2건은 **규약이 정착하기 전**(#30·#31)이다. 🔴 **이건 *문서에만 있는 규칙* 이 아니다** —
`divcal` #1 의 400줄은 준수 **0%** 였고 이건 **98.7%** 다. 같은 처방을 쓰면 안 된다.

**② 정당화는 자동화인데 우리는 그 자동화를 안 돌린다.** CC 가 값을 하는 자리는
**CHANGELOG 생성**과 **SemVer 자동 범프**인데, 실측: 릴리스 노트도 태그도 **손으로 만든다**
(`workflows` 에 `release-please`·`semantic-release`·`changesets`·`generate_release_notes` 가 없다).
**소비자가 없는 규칙을 강제하는 것이 cargo-cult 다.** 나쁜 제목이 **실제로 뭔가를 깨뜨려야**
강제가 값을 한다 — **자동화가 먼저고 강제가 나중이다.**

**③ 검사가 오탐을 낼 위험이 실증됐다.** 표준 어휘로 재니 `standards` 가 70.5% 로 나왔는데,
"위반" 32건이 전부 `research:` · `audit:` · `decision:` · `move:` — **문서·리서치 저장소용 확장 어휘**였다.
**표준 commitlint 설정을 그대로 넣었으면 정당한 PR 30건을 막았을 것이다.**

**④ 시중도 갈렸다.** *"Stop Using Conventional Commits"* 가 **r/git 244점 · 79댓글**(2026-08-23)로
돌았고 HN 에서도 논쟁 중이다. 최상위 반응이 이 결정과 같은 말을 한다 —
*"표준 형식은 좋아한다. 다만 **프로젝트마다 자기 방식이 있다**."*

> 🔴 **강제로 전환하는 조건 (하나라도 참이면)**
> ⓐ 릴리스 노트나 SemVer 를 **CC 에서 도출하기 시작**한다 ·
> ⓑ 준수율이 **95% 아래**로 떨어진다 — **`tools/check_pr_title_conformance.py` 가 잰다**
>   (2026-08-28 실측 **98.7%** · n=153) ·
> ⓒ 기여자가 **2인 이상**이 된다.
> 그때 만들 것은 **`ci / pr-title`** 이고, **반드시 아래 확장 어휘를 넣는다.**

### 우리 타입 어휘 — **표준이 아니다. 그래서 적는다**

`feat` · `fix` · `docs` · `style` · `refactor` · `perf` · `test` · `build` · `ci` · `chore` · `revert`
**＋ 우리 것:** `research` · `audit` · `decide`/`decision` · `move` · `deps` · `security`

**안 적으면 다음 사람이 표준 설정을 넣고 30건을 막는다.** 실제로 이 문단을 쓰는 과정에서
한 번 그랬다(위 ③).

### ⚠️ 자동화를 원하면 **CC 강제보다 이쪽이 먼저다**

GitHub 의 **`generate_release_notes`**(Releases API 의 불린 하나)는 **CC 없이** 머지된 PR 을
**라벨로 묶어** 노트를 만든다. 우리는 이미 라벨을 쓰고 squash 로 머지하므로 **전제가 갖춰져 있다.**

| | CC 강제 + `semantic-release` | `generate_release_notes` |
|---|---|---|
| 새로 만들 것 | `ci / pr-title` 검사 + 릴리스 파이프라인 | **없다** — API 인자 하나 |
| 규약 요구 | PR 제목 CC **100%** | 없음(라벨만) |
| SemVer 범프 | 자동 | 사람이 정한다 |

🔵 **SemVer 범프를 사람이 정하는 것이 우리에겐 손해가 아니다** — MAJOR 판정(잡 이름 변경)이
*"소비자 룰셋이 조용히 잠긴다"* 는 판단을 요구하고 **그건 커밋 타입으로 도출되지 않는다.**

⬜ **미착수** — `GAPS` R5-31.

### 🔴 copier 가 `project-template` 의 릴리스 결정을 뒤집는다 (2026-08-28)

**소유자 결정 2026-08-26 은 *"`coolbress/workflows` 만 릴리스한다"*** 였고 이유가
*"`project-template` 은 **`gh repo create --template` 이 태그를 참조하지 않아** 릴리스가
기능적으로 무의미하다"* 였다.

🔴 **그 전제가 깨졌다.** copier 로 전환하면서 실측했다:

```
$ uvx copier update
No git tags found in template; using HEAD as ref
```

**`copier update` 는 기본으로 최신 *태그* 를 목표로 삼는다.** 태그가 없으면 `HEAD` 로 떨어지는데,
그건 **아직 안 익은 커밋으로 인스턴스를 끌고 갈 수 있다는 뜻**이다.

✅ **결정·실행 2026-08-28 — 태그를 단다** ([v1.0.0](https://github.com/coolbress/project-template/releases/tag/v1.0.0)).

시중 관행이 명확하다 — *"Copier templates **should be versioned with Git tags**."*
copier 는 모든 태그를 읽어 **PEP 440** 으로 비교하고 최신 것을 체크아웃한 뒤 갱신한다.
⚠️ **SemVer 가 아니라 PEP 440 이다** — `v1.2.3` 표기는 양쪽 다 유효하지만 **정렬은 PEP 440 이 한다.**

**MAJOR 의 정의는 인스턴스 기준이다** — *"`copier update` 를 돌린 인스턴스가 **손으로 뭔가
해야 하는가**"*. copier 문서의 예시(`setup.cfg` → `pyproject.toml` 전환)와 같은 기준이고,
`workflows` 의 *"잡 이름 변경은 언제나 MAJOR"* 와 같은 형태다(소비자가 고쳐야 하는가).

🔬 **실측**: 태그 전 `_commit: a21d142` + *"No git tags found"* → 태그 후 **`_commit: v1.0.0`**,
경고 없음, 내용 변경 없음.

### 🔑 아키타입은 `/kickoff` 4번째 문항이 준다 (2026-08-28)

**바닥이 아키타입으로 조건을 걸어놓고 그 입력이 없었다.** `/kickoff` 은 공개·개인정보·라이선스
셋만 물었다. 2026-08-28 부터 **넷째를 묻는다** — *"이건 어떤 종류인가요? **CLI · 라이브러리 ·
서비스/웹앱 · 데이터·ML**"*.

| 조건부 항목 | 어느 답에서 켜지나 |
|---|---|
| `Dockerfile` | 서비스/웹앱 · 데이터·ML |
| `.env.example` · 설정 외부화 | 서비스 (*12-Factor 는 service 맥락 — 모든 아키타입 적용은 기각*) |
| 관측성 · 비용 상한 (만들 것 ⑬) | **공개** + 웹앱 |
| 릴리스 | 남이 `uses:`/의존으로 참조하는 저장소만 |

**실물 증거**: `divcal` 은 CLI 인데 `.env.example` 을 받았다 — 조건이 입력 없이 굴러갔다.

🔴 **모르면 가장 좁은 것을 고른다.** 넓히는 것은 **파일을 더하는 일**이고, 좁히는 것은
**안 쓰는 파일을 지우는 일**이라 스텁으로 남는다.

⚠️ **`new-project.sh` 는 아직 이 답을 안 받는다.** `/kickoff` 이 물어 이슈 본문에 남기고
사람이 적용한다. **자동 적용은 미착수**(`GAPS` R5-32).

### `Dockerfile` — 아키타입 조건부

n=938 에서 **48.0%**. 요구가 아니라 **조건**이다: 측면 03 이 *"backend-service / data-ml /
web-app 은 `Dockerfile` + `docker-compose`"* 로 아키타입을 명시한다.

**지금 우리 아키타입(CLI · 라이브러리)에는 해당 없다** — `divcal` 은 런타임 의존성 0 이고
`uv run` 하나로 돈다. **서비스 아키타입이 생기면 요구가 된다.**
`devcontainer` 는 **15.6%** 로 임계 아래라 묻지 않는다.

## 🚫 적힌 기각 — 안 쓰는 것도 입장이다 (2026-08-28)

**침묵과 기각은 다르다.** 침묵은 다음 사람이 *"빠뜨린 건가"* 를 매번 다시 묻게 만든다.
`CODEOWNERS` 는 왜 안 쓰는지 적어뒀는데 아래는 안 적혀 있었다 — `tools/check_floor_coverage.py`
가 이제 그 침묵을 잡는다(채택률 **20% 이상**만 묻는다. 드문 것을 전부 해명하게 하면
바닥이 문진표가 되고 그 자체가 **P40**(불필요한 방해) 위반이다).

| 산출물 | 채택률(N=6,582) | 왜 안 쓰나 | 다시 여는 조건 |
|---|---|---|---|
| **Discussions** | 39.5% | **1인 프로젝트에 포럼은 빈 방이다.** 질문·제안은 이슈가 받는다 | 외부 사용자 문의가 실제로 생기면 |
| **`FUNDING.yml`** | 29.4% | 후원을 받을 계획이 없다. **링크가 죽은 FUNDING 은 `presence≠adequacy` 그 자체** | 후원을 받기로 하면 |
| **`.gitattributes`** | 28.9% | 🟡 **조건부 기각.** 쓰임은 둘이다 — 개행 정규화(`* text=auto`)와 LFS. 지금은 **텍스트만 · 단일 OS** 라 개행 충돌이 난 적이 없고, 바이너리는 트리에 두지 않는다(VCS 위생) | **Windows 기여자**가 생기거나 바이너리를 커밋해야 하면 |
| **`SUPPORT.md`** | 2.4% | 임계 아래. `CONTRIBUTING` 이 그 자리를 채운다 | — |
| **Renovate** | 6.1% | **Dependabot 과 같은 일**을 한다. 둘을 같이 두면 갱신 PR 이 겹친다 | Dependabot 이 못 하는 생태계가 생기면 |
| **pre-commit** | 5.1% | 🔴 **원칙적 기각이다.** 로컬 훅은 `--no-verify` 로 **에이전트가 우회할 수 있다.** 원칙 01 이 *"집행은 에이전트 밖에서"* 이므로 같은 검사를 **CI 에 둔다**(`ci / lint`·`typecheck`) | 훅이 CI 를 **대체**하지 않고 **선행**하기만 한다면 |

> 🔴 **`pre-commit` 기각이 이 표에서 가장 중요하다.** 채택률이 낮아서가 아니라
> **집행 위치가 틀렸기 때문**이다. 채택률이 높았어도 같은 결론이었을 것이다 —
> *"드물면 안 쓰는 것"* 이라는 census 판독을 여기에 쓰면 **이유를 잘못 적는 것**이 된다.

## 🧾 이슈 폼 · 머지 방법 — 실물이 하는데 바닥이 안 적던 둘 (2026-08-28)

[`PURPOSE-DIRECTION-AUDIT`](../audit/PURPOSE-DIRECTION-AUDIT.ko.md) 가 `AGENTS.md` 와 **같은 종류**로 찾은 둘이다.
소유 측면이 이미 답을 갖고 있었다.

### 이슈 폼 — 근거가 이 바닥에서 가장 센 축에 든다

측면 24 가 소유하고(`IPC-003`·`IPC-005`), **결과 근거**까지 있다 —
Sülün et al. (**ACM TOSEM 2024** · 100 프로젝트 · 템플릿 350개 · 이슈 **190만 건 이상**):

| | 템플릿 없음 | 있음 |
|---|---|---|
| 해결 시간 | **381.02일** | **103.18일** |
| 댓글 수 | 4.95 | 4.32 |

**YAML 폼은 해결 시간·재오픈·논의 길이를 더 줄인다.** 채택은 **100개 중 99개.**
🟢 **대부분의 바닥 항목이 *채택률* 근거인데 이건 *결과* 근거다.**

우리 census 도 같은 방향이다 — 이슈 템플릿 **78%**(n=500) → **68%**(N=2,000) → **47.9%**(N=6,582).
⚠️ **YAML 폼은 최상위에서만 앞선다**(N=2,000 에서 폼 31% vs legacy `.md` 34%) — 그래도 GitHub 이
권고하는 방향이고 위 결과 근거가 폼 쪽을 가리킨다.

🔴 **폼의 *종류*는 별건이다.** 측면 24 가 census 표준을 **bug + feature 두 폼**으로 못박고
*"`task` 는 census 표준이 아닌 의도적 add-on"* 이라고 명시하는데, **템플릿은 `task.yml` 하나만 준다.**
바닥은 *"이슈 폼이 있을 것"* 까지만 요구하고 **폼 구성은 미결로 남긴다**(`GAPS` R5-28).

### 머지 방법 — 고르는 것이 아니라 **하나로 강제하는 것**이 요구다

측면 05 의 결론은 *"**no single winner; pick one and enforce consistency. 불일치가 진짜 결함이다**"* 다.
그래서 바닥이 요구하는 것은 **squash 가 아니라 일관성**이고, squash 는 **우리의 선택**이다(🔵).

census(N=6,582): squash **97% 허용** · merge-commit 74% · rebase 81%.
실제 머지 행동(n=250 · squash 커밋 4,041건): **76% 가 squash-merge.**

🔴 **census 는 *허용*을 재고 우리는 *전용*이다.** 우리 룰셋은 `allowed_merge_methods: ["squash"]` 로
나머지를 **막는다** — 이건 **above-census 선택**이고 그렇게 적어야 한다. 근거는 측면 05 의 결합이다:
squash 모델에서 **PR 제목이 곧 랜딩 커밋**이 되어 changelog·SemVer 자동화가 성립한다.

## 🤖 `AGENTS.md` — 바닥이 놓치고 있던 것 (2026-08-28)

**코퍼스가 이미 답을 갖고 있었는데 바닥이 인용하지 않았다.** 측면 01 의 `planning-output-census`
(**n=267** · software 221)가 이렇게 적는다:

> *"**CONFIRMS the constitution choice, strongly.** `AGENTS.md` (**35% all / 41% sw**) +
> `CLAUDE.md` (29% / 34%) are the **most-adopted of any planning artifact measured** …
> shipping `AGENTS.md`+`CLAUDE.md` as a ① artifact is **squarely the de-facto standard**."*

`ADR` 디렉터리는 **1.1%** 인데 `AGENTS.md` 는 **41%** 다. 그런데 바닥의 문서 묶음에는
`CONTRIBUTING`·`CHANGELOG`·`SECURITY` 가 있고 **`AGENTS.md` 는 없었다.**

그리고 측면 01 에는 작성 표준(`constitution-authoring-standard`)까지 **이미 있다** —
절 골격 · **<200줄** · 이중 파일 규칙 · 안티패턴. **바닥이 그 문서군 전체를 안 쓰고 있었다.**

### 🔴 미해결 — 어느 쪽이 SSOT 인가

| | |
|---|---|
| 코퍼스 (2026-06-27 · `review-needed`) | **`CLAUDE.md` 가 SSOT**, `AGENTS.md` 는 유지되는 축약 미러. 이유: *"두 호스트의 읽기 한도가 달라서"* |
| `divcal` 실물 (2026-08-28) | **`AGENTS.md` 가 파일**, `CLAUDE.md` 는 심볼릭 링크 |

**심볼릭 링크면 두 경로가 같은 바이트라 드리프트가 0 이다** — 코퍼스 자신이 *"symlink for zero drift"*
를 더 나은 선택지로 적어놓고 한도 차이 때문에 미러를 골랐다. 그런데 44줄짜리 파일은 **양쪽 한도
(32 KiB · 150줄) 아래**라 그 이유가 물리지 않는다. 그리고 그 사이 `AGENTS.md` 가 **AAIF/Linux
Foundation 표준**이 됐다(20개 이상 에이전트).

🔶 **바닥은 방향을 고정하지 않는다.** 요구하는 것은 **둘 다 있을 것 · 드리프트가 없을 것**이다.
코퍼스 문서는 `review-needed` 이고 재검증 대상으로 남긴다.

### ⚠️ 길이가 내용만큼 중요하다

ETH Zurich(**138 repos · 5,694 PR**): LLM 이 생성한 컨텍스트 파일은 성공률 **−3%**,
사람이 쓴 것도 **+4% 에 비용 +20~159%**. **150줄을 넘기지 않는다**(코퍼스의 <200줄과 같은 방향).
*"비관련 내용은 선택적 무시가 아니라 **지시 전체의 무시**를 부른다."*

🔴 **상태(*"지금 어디까지"*)를 넣지 않는다.** 가변 상태는 파일이 아니라 **열린 이슈**가 갖는다 —
`divcal` 완주 회고에서 차가운 세션이 시작 30초에 `gh issue list` 를 돌렸다.

## 🔴 `CONTRIBUTING` 은 파일이 아니라 **내용**을 요구한다 (2026-08-28)

소유 측면의 처분이 **C50-14 `presence≠adequacy`** 인데 바닥은 파일만 요구하고 있었다.
`census-gov-adequacy`(n=2,000 · 내용 파싱): present **61.5%** · adequate **41.2%** —
**있는 것 중 1/3 이 빌드·테스트 설명 없는 스텁**이다.

`adequate = has_devflow AND has_prflow`. 템플릿이 **그 두 표지를 담은 파일**을 주고,
**인스턴스의 `ci / test` 가 그걸 지킨다**(`tests/test_contributing.py`).

> 🔬 **왜 중앙 검사(⑩)가 아니라 템플릿 시험인가.** 템플릿에 그 패턴이 **이미 있었다** —
> `tests/test_env_example.py` 가 *"`presence ≠ adequacy` … CONTRIBUTING 은 present 62% 인데
> adequate 는 41%"* 를 **근거로 인용해놓고 정작 CONTRIBUTING 검사는 안 썼다.**
> 새 만들 것을 짓는 대신 **있는 패턴을 한 번 더 쓴다.**

⚠️ **`CONTRIBUTING` 을 바닥에서 빼는 안은 기각됐다.** `census-governance-floor`(**n=6,582**)에서
별 구간을 고정해도 **`AGENTS.md` 채택 저장소가 CONTRIBUTING 을 더 갖는다**
(`<1k` 63.3% 대 18.0% · `10k+` 83.9% 대 63.3%). **대체 신호가 없다.**

## 왜 별도 문서인가

[`04`](04-the-plan.md)는 **"어떻게 일하는가"** 다 — 이슈·PR·CI·리뷰·머지.
이 문서는 **"무엇이 남는가"** 다 — 저장소를 열었을 때 시니어가 보고 *"제대로 지었다"* 고 말할 조건.

**둘은 다른 축이다.** 워크플로를 완벽히 따라도 `.gitignore`가 없고 락파일이 없고 시크릿이 커밋돼 있으면
산출물은 시니어급이 아니다.

## 근거 — 그리고 그 근거의 한계

바닥의 출처는 [`foundation-floor-artifact-checklist`](../corpus/aspects/04-build-ci-engineering/foundation-floor-artifact-checklist.md)
**하나**다(`review-needed` · **MUST 45 · 10묶음**). OpenSSF Scorecard · Best-Practices Badge · OSPS Baseline ·
SLSA v1.2 · 12-Factor · GitHub community-health · SWEBOK/ISO-12207 을 대조해 만든 독립 체크리스트다.

🔴 **그 문서의 처분을 먼저 읽어야 한다** — **C50-14 `RETAIN-RN/SYNTHESIS` · *"파일 presence≠adequacy"***.
**파일이 있다는 것이 적절하다는 뜻이 아니다.** 야생 실측이 그것을 잰다:
**CONTRIBUTING 이 present 61.5% 인데 adequate 는 41.2%** — **있는 것 중 1/3(67%)이 빌드·테스트 설명
없는 스텁**이다 (`census-gov-adequacy` **n=2,000** · 내용 파싱 · `adequate = has_devflow AND has_prflow`).

> 🔴 **표기 규약 — `X/Y` 를 축 없이 쓰지 않는다.**
> 이 문서는 한때 `X/Y` 를 **두 가지 다른 뜻**으로 썼다: 위 줄은 `present/adequate`(n=2,000)인데
> 아래 §바닥 표의 `75/70%` 는 `uni/wgt`(비가중 / 최근성가중 `w = 0.5^(age/2yr)` · n=938)였고
> **어느 쪽도 그걸 밝히지 않았다.** 아래만 읽으면 *"adequate 70%"* 로 읽히는데 실제는 **41.2%** 다.
> **수치는 소유 문서를 떠날 때 축과 n 을 데리고 가야 한다.**

> **템플릿이 파일을 넣어주는 것은 presence 만 해결한다.** 스텁을 모든 인스턴스에 복사하면
> 이 프로젝트가 그 1/3 통계에 기여하는 쪽이 된다.

✅ **외부 표준 인용은 1차 출처로 확인했다**(`FFA-001~008`): SAST **L3** · SBOM-on-release **L3** · MFA **L1** —
**세 레벨 다 현행 표준에서 유지**된다. 🔴 다만 **OSPS 핀이 두 판 뒤처져 있었고**(2026-08-26 갱신),
***"SLSA Source L2 = signed history"* 는 원문과 다르다** — 원문은 *"continuous, immutable, and retained"* +
**Source Provenance Attestations** 이고 **서명이 아니다**(`FFA-006`).

## 바닥 — 12묶음

| 묶음 | 무엇이 있어야 하나 | 소유 측면 · 강도 |
|---|---|---|
| **VCS 위생** | `.gitignore` · **`main` 브랜치 보호**(PR 필수·검사 필수·force-push 금지) · 트리에 바이너리 산출물 없음 · **머지 방법 하나를 골라 강제**(우리는 squash 전용) · **PR 제목은 Conventional Commits**(둘은 묶여 있다 — 아래) | 🟢 **가장 강하다** — `github-workflow-current`(GitHub 1차 문서 `GHW-001~003`) + **이 저장소 벽 4/4 실물 확증** / 🔵 **머지 방법의 *선택*은 판단** — 측면 05 가 *"no single winner; pick one and enforce consistency"* 로 못박는다 |
| **빌드·의존성** | **락파일 커밋** · 의존성 버전 고정 · **Actions 를 커밋 SHA 로 핀** · **의존성 갱신 봇** · 재현 가능한 단일 빌드 진입점 · CI 에서 warnings-as-errors | 🟢 SHA 핀(`GHW-005`: *"only a full-length commit SHA is immutable"*) / 🟡 나머지는 `03`·`10` 이 소유하고 **처분이 `SPLIT`**(보편 번들 기각) |
| **CI/CD** | 매 PR·push 에 CI · **lint·typecheck·test·build 를 각각 별도 required check 로** · 워크플로마다 `permissions:` 최소화 · `pull_request_target` + 신뢰 불가 checkout 금지 | 🟢 **우회 불가**는 git 1차 문서가 받친다(`IPW-005`) / 🔵 **4종 분리는 이 프로젝트의 선택** — `04` 의 처분(`C50-12`)이 *"4종이 보편"* 을 기각했다 |
| **코드 품질** | 린터 설정 커밋 · **포매터를 CI 가 강제** · **SAST** · **시크릿 탐지**(gitleaks + push protection) | 🟡 린터·포매터는 원칙이 선다 / 🔵 **SAST 는 표준이 요구해서가 아니라 선택이다** — 출처가 *"a deliberate above-OSPS-L1 harness uplift … **not** because a leveled standard mandates it"* 라 명시하고, **OSPS 는 L3 에 둔다**(`FFA-001`) |
| **테스트** | CI 초록 · **모든 PR 에 테스트** · CONTRIBUTING 에 테스트 정책 · **walking skeleton — 실제 end-to-end 한 줄기**(Cockburn) | 🟢 **동반은 강하다**(`04 foundation-floor` MUST · `08` 이 4대 검사 중 하나로) / 🟡 피라미드 비율은 **권고이지 실측이 아니다**(`PYR-001`) |
| **보안·공급망** | `SECURITY.md` · Dependabot/OSV 경보 · secret-scanning + push protection · **쓰기 권한에 MFA** · 자체 제작 암호 금지 · 취약점 SLA(medium+ ≤60일) | 🟢 MFA 는 **OSPS L1**(`FFA-003` — 단 원문 범위는 *"read or modify a **sensitive resource**"*) / 🟡 나머지는 `09`·`10` 소유, 처분 `SPLIT` |
| **설정·시크릿** | **설정을 환경으로 외부화**(12-Factor III) · **`.env.example` 커밋 + 실제 `.env` 는 ignore** | 🟡 `06` 소유 · 처분이 *"12-Factor 는 **service 맥락**"* 이라 **모든 아키타입 적용은 기각** |
| **개발환경·온보딩** | **README 에 clone→install→test 가 5명령 이내** · 통합 태스크 러너 · 🟡 **`Dockerfile` 은 아키타입 조건부**(아래) | 🟡 5명령은 **재는 것**이라 검사 가능 / IDP·platform 문턱은 조직별(`C50-36`) |
| **문서** | README(**≈100% uni / 100% wgt** · n=938 — **유일한 보편**) · **`AGENTS.md`**(에이전트 컨텍스트 · **35% all / 41% sw** · n=267 — **측정된 계획 산출물 중 채택률 1위**) · 🔴 **CONTRIBUTING 은 *내용*을 요구한다**(빌드·테스트 설명 **+** PR 흐름 — present 75% uni / 70% wgt · n=938 · 더 깊은 표본 48.2% · n=6,582 · **adequate 는 41.2%** · n=2,000) · 🟡 **CHANGELOG 는 릴리스와 함께 조건부**(*Keep a Changelog* 는 **릴리스 단위로 쌓는 형식** — 릴리스가 없으면 채울 단위가 없다 · **present 52% uni / 51% wgt** · n=938) · 공개 표면이 있으면 API 레퍼런스 | 📊 census 로 강도가 갈린다 · `22` 소유 · ⚠️ **de-jargon 게이트는 해당 없음** — 조건이 *"public/internal doc split"* 인데 이 저장소는 `legacy/`·`audit/`·`direction/` 이 **전부 공개**라 샐 것이 없다 |
| **거버넌스** | **이슈 폼**(YAML) · **PR 템플릿** — 형태는 census 규격: 중앙값 **3절** · **빈** 체크리스트(62% · 중앙값 5항목) · 인라인 HTML 주석(70%) · *"type of change"* 는 **CC 를 쓰면 뺀다**(11.5%) | 🟡 자체 census(`IPC-002`) · 🔴 **모집단 한정을 지우지 않는다** — 제3자(Zhang et al., **1.8M 저장소**)가 재니 **PR 템플릿 채택은 전체의 1.2%** 이고 채택자는 *"mostly **prevalent** projects"* 다(`IPC-004`). **우리 44~53% 는 상위 저장소 기준**이다. ⚠️ `CODE_OF_CONDUCT.md` 는 *"MUST for public community"* 라 **기여를 받기 시작하면** 켠다 |
| **릴리스** 🔒 | **참조되는 저장소만 해당한다.** SemVer 문서화 · 릴리스마다 git 태그 · GitHub Release + 변경 요약 | 🔵 **갱신 2026-08-28 — 이제 둘이다**(`workflows` · `project-template`). **규칙은 안 바뀌었고 사실이 바뀌었다**: copier 전환으로 모든 인스턴스의 `.copier-answers.yml` 이 `_src_path: gh:coolbress/project-template` 로 **템플릿을 참조한다.** (이전 판: *"`workflows` 만 — 남이 `uses:` 로 참조하는 쪽이 거기뿐"*). 🟢 **핀은 커밋 SHA, 태그는 그 SHA 를 읽기 위한 것**: `@<SHA> # v1.0.0` |
| **라이선스** | **루트 `LICENSE`** — 의도적으로 고른 아웃바운드 라이선스 하나를 기계가 읽게 선언한다 | 🟢 **채택률과 무관하게 선다** — 법적 효과가 있고 **없으면 공개 저장소에서 *"재사용 가능"* 이 성립하지 않는다**. 🔴 다만 **per-file SPDX·scan·CLA 는 바닥이 아니다**(`C50-39` 가 *"모든 파일 SPDX"* 를 기각) |

> 🔴 **이 표 전체에 걸리는 한정 하나** — 소유 측면 대부분의 재검증 처분이 **`RETAIN-RN/SPLIT`**, 즉
> ***"복합 보편 주장을 원자 claim 으로 나누고 범위를 좁혀야 한다"*** 다. **개별 항목이 틀렸다는 게 아니라
> *"묶음째로 모든 프로젝트에 보편"* 이라는 지위가 근거보다 세다.**
>
> 🔴 **그리고 두 종류가 한 MUST 로 묶여 있다.** 코퍼스가 직접 논증한다 — *"브랜치 보호 13% … **바로 그것이
> 비엔지니어가 요구할 생각을 못 하는 시니어 관행이다**"*. **보호 장치는 드문 것이 켜야 할 이유**이고,
> **협업 문서는 드물면 그냥 안 쓰는 것**이다. 같은 기준으로 읽으면 안 된다.

### 바닥에 **넣지 않기로** 판정한 것

부재가 판정의 결과라는 것을 적어두지 않으면 **누락과 구별되지 않는다.**

- **ADR(`docs/adr/`)** — 🔵 **활동은 유지, 형식은 강제하지 않는다.** census 가 반대 방향이다: 형식 ADR 디렉터리 **2~4%** ·
  planning/design 문서 공개 **13~19%** · Buchgeher(900+ 저장소)에서 **채택 저장소의 약 50%가 레코드 1~5개**(*"tried, didn't stick"*).
  `02` 자신이 *"seniors **do** design … but they rarely **publish**"* 라 쓰고, `24` 는 원격에서 `ADR-NNNN` 인용을
  **dangling reference** 로 경고한다. **결정 기록은 이미 하고 있다** — `04 §범위 결정` · `01` 의 두 경계 · `GAPS` 처분란.
  **형식이 없는 게 아니라 장소가 다르다.**
- **CODEOWNERS** — 🔵 **1인에서 기계적으로 무효다.** 기능이 *"auto-requests the right reviewers"* 인데
  **GitHub 은 PR 작성자에게 리뷰를 요청하지 않는다.** 실측으로 집행 경로도 없다(`require_code_owner_review: false` ·
  `required_approving_review_count: 0`). [`01`](01-what-i-want.md) 경계 ②(*"동료 리뷰를 시뮬레이션하지 않는다"*)에 걸린다 —
  **파일은 있고 집행은 없는 것이 `presence≠adequacy` 그 자체다.** 다시 여는 조건: **기여자 2인 이상** 또는 `require_code_owner_review` 활성화.
- **SBOM** — ✅ **부재가 맞다.** 이 프로젝트는 **EO 14028·CRA 적용 대상이 아니고**, OSPS 도 **L3** 에 둔다(`FFA-002`).

## 이 중 무엇이 **자동으로** 채워지나

**대부분은 `project-template`(만들 것 3)에 한 번 넣으면 끝난다** — 파일이기 때문이다.

| 어디서 | 무엇 |
|---|---|
| `project-template` | `.gitignore` · `.env.example` · 린터·포매터 설정 · **`AGENTS.md`**(+ `CLAUDE.md` 심볼릭 링크) · `SECURITY.md` · **내용이 있는 `CONTRIBUTING.md`**(검사로 지킨다) · `CHANGELOG.md`(릴리스 안 하면 지우라고 명시) · README 골격 · `.editorconfig` · **PR 템플릿** · **`LICENSE`** |
| `coolbress/workflows` (만들 것 2) | lint·typecheck·test·build 4검사 · **SAST**(⑫ 미착수) · **gitleaks**(⑫) · `permissions:` 최소화 · Actions SHA 핀 |
| `new-project.sh` (만들 것 5) | 브랜치 보호 룰셋 · secret-scanning·push-protection · **공개여부·라이선스를 인자로 받는다** · **벽을 못 걸면 저장소를 남기지 않는다** |
| GitHub 계정 설정 | **MFA**(1회) |
| 프로젝트마다 사람이 | **walking skeleton** — 첫 조각을 end-to-end 한 줄기로 (`/kickoff` 가 유도) |

🔴 **템플릿이 넣는 것은 `presence` 뿐이다** — 위 §근거의 *1/3 스텁* 을 만들지 않으려면 **내용이 실제로 있어야 한다.**

## 남은 만들 것

| # | 무엇 | 왜 |
|---|---|---|
| **10** | **`floor-check` CI 잡** — 락파일 있나 · `.env` 가 커밋됐나 · Actions 가 SHA 핀인가 · `.env.example` 있나 | 바닥은 **가장 약한 항목으로 점수가 매겨진다.** 사람이 매번 확인할 수 없다 |
| ~~**12**~~ ✅ | **완료 2026-08-27** — SAST **CodeQL default setup 3/3** · 시크릿 **푸시 보호 + `ci / secrets`(gitleaks)** · **둘 다 required check** | ✅ 제약(`FFA-008`)**과** 성능을 둘 다 쟀다([`SAST-CODEQL-VS-SEMGREP`](../audit/SAST-CODEQL-VS-SEMGREP.ko.md)): 진입점이 있을 때 **CodeQL 8/8 · Semgrep 7/8**, 오탐 둘 다 0. 🔴 **진입점이 없으면 둘 다 급락**(1/9 · 3/9) — *"SAST 를 켜 뒀으니 안전"* 은 **진입점이 모델링될 때만** 참이다. 🔴 **둘 다 하드코딩 자격증명을 놓쳤다.** 그래서 시크릿은 **따로 두 층**이다([`SECRET-DETECTION-OVERLAP`](../audit/SECRET-DETECTION-OVERLAP.ko.md)): **푸시 보호=벽**(커밋 전 차단, 에이전트가 못 끈다) · **gitleaks=그물**(이미 올라간 뒤 머지를 막는다). 🔴 **푸시 보호가 개인키 PEM 을 통과시킨다** — 그 자리가 gitleaks 가 값을 하는 곳이다 |
| **13** | **공개 웹앱 층** — 접근성(axe) · 개인정보 체크리스트 · spend cap · 헬스체크 | **`/kickoff` 답이 "공개"일 때만.** 첫 아키타입 하나만 만든다 |

## 위험 비례 — 전부를 항상 켜지 않는다

- **비공개 + Free**: 룰셋 자체가 안 걸린다(`GEB-001·002`) → `new-project.sh` 가 **저장소를 남기지 않고 멈춘다.** CodeQL 도 별도 라이선스가 필요하다 → **Semgrep·gitleaks 로 대체**
- **로컬 실험**: 바닥 전체가 과하다. `github-workflow-current` 의 risk-scaled 표를 쓴다
- **공개 웹앱**: 바닥 전부 + 접근성 · 개인정보 — 아래

## 아키타입별 층 — 누가 판정하나

코퍼스 28측면의 `gated_archetypes` frontmatter가 **`[]` 20 · 게이트 8** 로 갈린다.

> 🔴 **다만 이 필드에는 근거가 없다**(`GAPS` R5-16) — [`_schema.md`](../corpus/_schema.md) 에 **정의가 없고**
> [`validate_corpus.py`](../tools/validate_corpus.py) 가 **검사하지 않는다.** 그리고 **`[]` 를 *"항상 켠다"* 로 읽을 근거가 없다** —
> `[]` 인 **19**(*"instrument **services**"*) · **20**(*"operate a **running service**"*) · **18**(*"publishes to the canonical channel"*)
> 의 claim 자체가 조건을 전제한다. `[]` 가 *"항상"* 이면 **로컬 CLI 에도 SLO·on-call 이 요구된다.**

**원칙: 선언을 만들지 말고, 가능하면 저장소가 스스로 드러내게 한다.**

| 측면 | 판정 방식 |
|---|---|
| **13** API · **14** 마이그레이션 · **26** MLOps | 🟢 **존재로 판정** — `openapi.*`·`migrations/`·모델 파이프라인이 있으면 켠다 |
| **12** 성능 | 🟡 거의 전부 해당 → 사실상 universal, **예산 수치만 `/kickoff` 가 받는다** |
| **15** 접근성 · **16** 개인정보 · **21** 비용 | 🔴 **파일로 판정 불가 — 의도다** → `/kickoff` |

### `/kickoff` 가 묻는 것은 **세 가지**다

**기준은 하나다: 파일로 알 수 없고(의도) · 틀리면 되돌리기 어려운 것만 묻는다.**

1. **"공개할 건가요, 혼자 쓸 건가요?"** → 접근성(15)·비용(21)·관측성이 켜진다.
   🔴 **비공개면 벽 이야기가 먼저다** — Free 에서 룰셋이 안 걸린다.
2. **"남의 개인정보를 다루나요?"** → 개인정보(16)가 켜진다 — GDPR Art.25 · PIPA 제30조.
3. **"라이선스는 무엇으로?"** (2026-08-26 추가) → 기본 MIT · 특허 조항이 필요하면 Apache-2.0.

**묻지 않는 것**: 릴리스 여부(**가역** — 나중에 태그 하나면 된다) · CODEOWNERS(**저장소가 기여자 수로 드러낸다**).
**문진표를 만들지 않는다** — 문제 지도 **P40**(*재량으로 될 일을 물어 방해받는다*)이 거짓 양성을 실패로 센다.

## 한 줄

> **`01`~`04`는 "일을 어떻게 하는가", 이 문서는 "무엇이 남는가"다.**
> 워크플로를 완벽히 따라도 바닥이 비면 산출물은 시니어급이 아니다 —
> **바닥은 가장 약한 항목으로 점수가 매겨지기 때문이다.**
> 그리고 **파일이 있다는 것이 적절하다는 뜻은 아니다**(`presence≠adequacy`).
