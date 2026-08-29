# ECC 를 **카탈로그로** 읽었다 — 무엇을 가져오고 무엇을 버렸나

> 실측 2026-08-29 · 대상 [`affaan-m/everything-claude-code`](https://github.com/affaan-m/everything-claude-code)
> (⭐**244,044** · `pushed` 2026-08-29 · **48MB**)
>
> **[`ARSENAL`](ARSENAL.ko.md) §2 의 처분이 *"🟡 카탈로그로만 — 전체 설치 안 함"*이다.** 이 문서가 그 처분의 **실행 기록**이다.
> 읽은 방법: **클론하지 않고 GitHub API 로 트리와 매니페스트만** 읽었다(48MB · 클론 2분 초과).
> 읽기 전용이고, **이 저장소로 내용을 복사하지 않았다**(`ARSENAL` §2 의 금지).

## 0. 먼저 — **ECC 는 자신을 하네스라고 부른다**

| | |
|---|---|
| 저장소 설명 | *"The agent **harness** performance optimization system."* |
| 자기 플러그인 설명 | *"ECC is a **harness-native operator system** for Codex and adjacent agent harnesses."* |

| 실측 규모 | |
|---|---|
| 파일 | **3,505개** |
| `SKILL.md` | **898개** |
| `docs/` | **1,514파일** · `scripts/` 262 · `tests/` 273 · `rules/` 122 |

🔴 **통째로 들이면 그것이 일곱 번째 하네스다**([`02`](../direction/02-why-past-attempts-failed.md)).
`ARSENAL` 의 *"카탈로그로만"* 처분이 옳았고, 이 문서는 그 처분을 **뒤집지 않는다.**

## 1. 가져온 것 — 셋

### ⓐ 🔵 **ECC 도 훅 런타임을 기본에서 뺀다** — 독립 확증

설치 프로필 **7개** 중 둘이 `hooks-runtime` 을 **일부러** 제외한다:

| 프로필 | 모듈 수 | `hooks-runtime` |
|---|---|---|
| `minimal` | 5 | ❌ 설명 원문: *"…**no hook runtime**."* |
| `opencode` | 3 | ❌ 원문: ***"It intentionally excludes hooks-runtime; opt in with `--modules hooks-runtime`."*** |
| `core` · `developer` · `security` · `research` · `full` | 6 · 9 · 7 · 9 · 26 | ✅ |

**우리가 같은 날 [`04`](../direction/04-the-plan.md) §원칙 03 시행 기준에서 판별식 셋으로 도출한 결론과 방향이 같다** —
훅을 금지하지도, 기본으로 켜지도 않는다. **옵트인이다.**

⚠️ **이것을 근거로 쓰는 방식에 주의한다**(§3 인기 신호 ≠ 판정). 별 수가 근거가 아니라,
**독립된 설계자가 같은 자리에 같은 선을 그었다**는 사실이 근거다. 우리 판별식을 **대체하지 않고 옆에 선다.**

### ⓑ 🟢 **모듈 메타데이터** — 우리가 산문으로 묻던 것을 **필드로** 만든 것

ECC 의 모듈 **36개**는 각각 이 모양이다:

```json
{ "id": "framework-language", "kind": "skills",
  "dependencies": ["rules-core", "agents-core", "commands-core", "platform-configs"],
  "defaultInstall": false,
  "cost": "medium",          // light | medium | heavy
  "stability": "stable" }    // stable | beta | experimental
```

🔴 **이것이 우리에게 없던 것이다.** [`ARSENAL`](ARSENAL.ko.md) §4 는 열한 문항으로
*"시간·토큰·돈 비용은 얼마인가"*(9번) · *"어떤 조건이 되면 버릴 것인가"*(10번)를 **묻지만
답이 산문**이라 **기계가 못 읽는다.** 그리고 §1 의 *Loadout*(오늘 필요한 것만 담은 가방)은
**개념만 있고 구현이 없었다.**

**채택한다 — 단 축소해서.** ECC 는 프로필 7 · 모듈 36 이다. **우리가 그러면 그게 하네스다.**
우리 규모에서는 **필드 셋**(`cost`·`stability`·`defaultInstall`)과 **프로필 둘**이면 족하다.

### ⓒ 🔵 **`rules/` 축은 우리 바닥과 다른 축이다** — 대체가 아니라 보완

ECC `rules/common/` **10개**: `agents` · `code-review` · `coding-style` · `development-workflow` ·
`git-workflow` · `hooks` · `patterns` · `performance` · `security` · `testing`

| | 무엇을 규정하나 |
|---|---|
| ECC `rules/` | **코드를 어떻게 쓰나** |
| 우리 [`05`](../direction/05-the-output-floor.md) 바닥 12묶음 | **저장소에 무엇이 남나** |

- **우리에게 없는 것**: `performance` · `patterns` · `coding-style`
- **저기 없는 것**: 라이선스 · 릴리스 · 거버넌스(이슈 폼·PR 템플릿) · 설정·시크릿 · 빌드·의존성 · 개발환경·온보딩

👉 **겹치지 않는다.** 그리고 `performance`·`patterns`·`coding-style` 은 *"남는 것"* 축이 아니므로
**바닥의 범위 밖**이다(`coding-style` 은 우리가 **린터로** 대신한다 — `ruff.toml` 12규칙군).
🔵 **부재가 판정의 결과임을 여기 적어두는 것이 `05` §적힌 기각의 논리다.**

## 2. 안 가져오는 것 — 그리고 왜

| 안 가져옴 | 왜 |
|---|---|
| **MCP 서버 묶음** (ECC 는 플러그인에 `mcpServers` 를 담고 `platform-configs` 가 *MCP catalog* 를 배포한다) | 🔴 **근거가 갈린다.** ECC 는 **카탈로그를 파는 쪽**이라 목록이 상품이다. 우리는 **한 명이 쓰는 쪽**이고 성숙한 벤더 CLI(`gh`)가 있고 인증이 이미 걸려 있다. MCP 도구 정의는 **컨텍스트에 영구 상주**하고 매 호출마다 지불된다 — 실측 담론은 동일 작업에 **CLI 대비 4~32배**를 보고한다 |
| **프로필 7 · 모듈 36** | 우리 규모가 아니다. **프로필 둘**로 축소 |
| **`schemas/state-store` · `install-state` · `hooks/memory-persistence`** | 🔴 **전용 상태를 소유한다** — [`06`](../direction/06-how-we-work.md) 이 Router 에 **명시적으로 금지**한 것이고, 우리 판별식 ③ 이 걸러내는 자리다 |
| **`skills/` 898개** | 대전제 2. 필요한 것만 켠다 |

## 3. 🔴 이 읽기가 **우리 기록의 오류 하나를 잡았다**

[`ARSENAL`](ARSENAL.ko.md) §2 가 *"**Taste** · frontend-design · Impeccable | **프론트엔드 품질**"* 로 묶어놨는데,
**ECC 안의 `skills/taste` 는 프론트엔드가 아니다.** 실물 프론트매터:

> *"A creative-direction (taste) layer for **music videos and short-form edits** in the
> angelcore / cloud-trance / hyperpop visual family… **beat-synced editing grammar**"*

**영상 편집 스킬이다.** 이름이 같은 다른 물건이 최소 둘이라는 뜻이고, 대장이 **어느 쪽을 가리키는지 적지 않고 있었다.**
소유자가 가리킨 것은 [`tasteskill.dev`](https://www.tasteskill.dev/) 쪽이다 — §4 에 실측을 적었다.

🔵 **교훈은 이 저장소가 이미 아는 것이다** — **이름으로 부르면 어느 것인지 확정되지 않는다.**
`direction/` 이 코퍼스를 **경로로** 인용해야 하는 것과 같은 형태이고, `check_name_only_citations` 가 거는 규율이다.
**도구 대장에도 같은 규율이 필요하다: 후보는 이름이 아니라 저장소로 적는다.**

## 4. 소유자가 가리킨 **진짜 Taste** — 실측

| | |
|---|---|
| 출처 | [`Leonxlnx/taste-skill`](https://github.com/Leonxlnx/taste-skill) · [tasteskill.dev](https://www.tasteskill.dev/) |
| 규모 | ⭐**82,005** · **MIT** · `pushed` 2026-08-24 |
| 무엇 | *"The **Anti-Slop** Frontend Framework for AI Agents"* — 에이전트가 **밋밋하고 틀에 박힌 UI** 를 뱉는 것을 막는 설계 규칙 묶음 |
| 🔵 **형태** | **이미 Claude Code 플러그인이다** — `.claude-plugin/plugin.json`(v1.0.0) **과 자체 `marketplace.json` 을 갖는다** |
| 스킬 | **13개** — `taste-skill`(v2) · `taste-skill-v1` · `brutalist` · `minimalist` · `soft` · `redesign` · `stitch` · `output` · `brandkit` · `image-to-code` · `imagegen-frontend-web` · `imagegen-frontend-mobile` · `gpt-tasteskill` |
| 🔬 눈에 띈 것 | **`research/laziness/`** — *왜 LLM 이 게으른 출력을 내는가*를 root-cause(훈련 데이터 편향 · RLHF·연산 · 출력 길이 제한 · 인지적 지름길) / remediation / empirical-results / references 로 **문서화해 함께 배포**한다 |

🔵 **마지막 줄이 우리와 같은 모양이다** — 주장에 근거를 붙여 저장소에 남기는 것.
[`corpus/methods/EVIDENCE-POLICY.md`](../corpus/methods/EVIDENCE-POLICY.md) 가 우리 코퍼스에 거는 것과 같은 규율이다.

⚠️ **아직 판정하지 않는다.** `ARSENAL` §2 의 처분은 여전히 *"같은 화면 과제로 비교해 하나만"* 이고,
**우리에게 프론트엔드 과제가 아직 없다.** 비교 없이 채택하면 그것이 §4 8번(*실제 대표 작업에서 더 좋아졌는가*) 위반이다.

## 5. 그래서 설계 방향 — **얻은 것이 어디에 꽂히나**

| 얻은 것 | 어디에 |
|---|---|
| ⓐ 훅 옵트인 | [`04`](../direction/04-the-plan.md) §원칙 03 시행 기준의 **옆 증거**. 우리 배포에도 **프로필 둘**로 반영 |
| ⓑ 모듈 메타데이터 | [`ARSENAL`](ARSENAL.ko.md) §7 **Loadout 실물** — `cost`·`stability`·`defaultInstall` |
| ⓒ `rules` 축 구분 | [`05`](../direction/05-the-output-floor.md) §바닥에 **넣지 않기로 판정한 것**에 세 항목(`performance`·`patterns`·`coding-style`) |
| 🔴 Taste 오류 | `ARSENAL` §2 정정 + **후보는 저장소로 적는다**는 규율 |

## 6. 다시 읽을 조건

- ECC 가 **모듈/프로필 스키마를 바꿀 때**(우리가 베낀 자리다)
- 우리가 **프론트엔드 과제**를 처음 잡을 때 — §4 의 비교를 그때 한다
- 🔴 **`ARSENAL` §4 의 열한 문항에 답이 필요한 새 후보가 생길 때** — 이 문서가 그 답의 형식을 보여준다
