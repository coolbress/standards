# 배포 설계 — 소유자의 목적 다섯을 틀 안 어디에 넣나

> 실측 2026-08-29 · 후보 **다섯을 전부 저장소로 열어** 쟀다([`ARSENAL`](ARSENAL.ko.md) §4 *"후보는 이름이 아니라 저장소로"*).
> 앞선 읽기: [`ECC-CATALOG-READING`](ECC-CATALOG-READING.ko.md) · [`SKILL-OVERLAP`](SKILL-OVERLAP.ko.md) · [`CODE-QUALITY-JUDGMENT`](CODE-QUALITY-JUDGMENT.ko.md)

## 1. 실측표 — **다섯 다 이미 Claude Code 플러그인이다**

| 후보 | ⭐ | 라이선스 | 훅 | MCP | 핀 |
|---|---|---|---|---|---|
| [`mattpocock/skills`](https://github.com/mattpocock/skills) | 240,562 | MIT | ❌ | ❌ | 🟢 **공식 마켓에 SHA 로** |
| [`Leonxlnx/taste-skill`](https://github.com/Leonxlnx/taste-skill) | 82,018 | MIT | ❌ | ❌ | 🟡 자체 마켓 (우리가 항목을 쓴다) |
| [`mvanhorn/last30days-skill`](https://github.com/mvanhorn/last30days-skill) | 60,062 | MIT | ❌ | ❌ | 🟡 자체 마켓 · ✅ **이미 설치돼 있다** |
| [`DietrichGebert/ponytail`](https://github.com/DietrichGebert/ponytail) | 115,858 | MIT | 🔶 **3종** | ❌ | 🟡 자체 마켓 |
| [`JuliusBrussee/caveman`](https://github.com/JuliusBrussee/caveman) | 101,692 | 🔴 **MIT + BSL-1.1 혼합** | 🔶 2종 | 🔴 `mcp/` | — |

🔵 **다섯 다 플러그인이라는 것이 설계를 단순하게 만든다** — 우리가 스킬 내용을 복사할 이유가 없다(§2 금지).

## 2. 🔴 구조적 정정 — **Claude Code 에는 "프로필" 이 없다**

ECC 는 프로필 7개를 **자체 설치 스크립트**(`manifests/install-profiles.json` + `scripts/`)로 만든다.
**우리가 그걸 흉내내면 그게 설치기이고, 설치기는 하네스의 시작이다.**

👉 **프로필 둘 = 플러그인 둘.** 네이티브 `dependencies` 로 푼다:

```
coolbress-standards            (기본 · 훅 없음)
coolbress-standards-hooks      dependencies: ["coolbress-standards"]  (+훅)
```

**우리가 설치기를 안 만든다.** `claude plugin install` 이 이미 의존성을 **전이적으로** 켠다.

## 3. 목적 다섯 → 자리

### ⓐ 프론트엔드를 이쁘게 → **`taste-skill`** · 기본 프로필

- 실물 스킬 이름은 `design-taste-frontend`. **자기 범위를 스스로 못박는다**:
  > *"랜딩 페이지 · 포트폴리오 · 리디자인. **대시보드도, 데이터 테이블도, 다단계 제품 UI 도 아니다.**"*
  > *"**어떤 규칙도 자동으로 발화하지 않는다.** 먼저 브리프를 읽고 맞는 것만 꺼내라."*
- 🟢 훅 없음 · MIT · 조건부 발화 → **기본 프로필에 넣어도 상시 비용이 프론트매터뿐**
- ⚠️ **v2 는 실험판**(v1 은 legacy) → `stability: experimental`
- 🔴 **`ARSENAL` §2 의 비교 조건은 그대로다** — `frontend-design`(공식·핀 없음)·`Impeccable` 과
  **같은 화면 과제로 한 번 비교하고 하나만 켠다.** 우리에게 아직 프론트엔드 과제가 없다

### ⓑ 에이전트가 합리적으로 코드를 짜게 → **`ponytail`** · **+훅** 프로필

- 실물 `SKILL.md`: *"실제로 되는 **가장 게으른** 해법을 강제한다… **YAGNI** · 커스텀 코드보다 **표준 라이브러리** ·
  의존성보다 **네이티브 기능** · 오십 줄보다 **한 줄**"* · 강도 `lite|full|ultra`
- 🔵 **이건 우리 규칙 1·2 의 *코드 층* 판이다** — *만들기 전에 먼저 찾는다* · *작고 가볍게*.
  그리고 강도 세 단계는 우리 *"가드 깊이는 위험 비례"* 와 같은 형태다
- 🔶 **훅 3종**(`SessionStart` · `SubagentStart` · `UserPromptSubmit`)이라 **프로필이 갈리는 이유가 바로 이것**이다.
  판별식으로 재면 ①**보여준다**(모드 주입) ②**빼도 돈다** ③**경계선** — 매 프롬프트 훅은 *제어 루프* 에 가깝다.
  **그래서 기본이 아니라 옵트인이다**(🔵 ECC 도 `hooks-runtime` 을 같은 이유로 옵트인에 둔다)

### ⓒ 쉽게 설명 · 출력 토큰 절약 → 🔴 **`caveman` 기각.** 목적은 **우리 틀에 이미 자리가 있다**

**기각 근거 셋 — 하나만으로도 충분하다:**

| | |
|---|---|
| 🔴 **라이선스** | `engine/`·`proxy/`·`cacheengine/`·`rewriter/`·`browse/`·`mcp/`·`shrink/`·`cavemem` 이 **BSL-1.1**(오픈소스 아님). 원문: *"새 Engine-linked 런타임 모듈은 **기본이 BSL-1.1**"*. [`05`](../direction/05-the-output-floor.md) §라이선스가 요구하는 *"의도적으로 고른 아웃바운드 라이선스 **하나**"* 가 성립하지 않는다 |
| 🔴 **상태 소유** | `cacheengine` · `cavemem`(메모리) → **판별식 ③ 위반** |
| 🔴 **규모·성격** | **1,393파일 · 9.5MB** · `release-binaries` · `engine-ci` · `provider-catalog` — **스킬이 아니라 엔진**이다 |

⚠️ 플러그인 설명의 *"측정된 65% 절감"* 은 **자기 측정이고 unprompted baseline 대비**다 — 채택 근거가 아니라 **검증 대상**이다.

🔵 **그런데 목적은 살아 있고, 자리도 이미 있다:**

| | |
|---|---|
| 만들 것 **⑧ⓐ** | *"쉬운 말이 **기본값**"* — R5-24 가 `wait-what` 을 강한 후보로 지목했다(mattpocock 안에 있다) |
| `needs-simpler` 라벨 | 요구 ③ⓑ 계측 — **네 저장소에 이미 달려 있다** |

**즉 도구를 안 들여도 목적은 재고 있고, 채우는 것은 이미 들일 묶음 안에 있다.**

### ⓓ 현업 시니어의 개발 흐름을 알고 따르게 → **`mattpocock-skills`** · 기본 프로필

- 🟢 **공식 마켓에 SHA 로 핀돼 있다** — 우리가 항목을 쓸 필요조차 없다
- 훅 없음 · MCP 없음 · **상시 비용 실측 ≈1,841토큰**(스킬 35개 프론트매터)
- 덮는 것: `tdd` · `code-review`(2축) · `codebase-design`(deep modules) · `improve-codebase-architecture` ·
  `domain-modeling` · `diagnosing-bugs` · `to-spec` · `to-tickets` · `wait-what` · `grilling`
- 🔵 [`SKILL-OVERLAP`](SKILL-OVERLAP.ko.md) 이 **🤝 안내 4/4 겹침**을 실측했다 — **우리가 쓸 것이 거의 없다**

### ⓔ 리서치에서 최신 트렌드 → **`last30days`** · 기본 프로필 · **규율은 이미 서 있다**

- ✅ **이미 이 기계에 설치돼 있다**(`~/.claude/skills/last30days/`)
- 🔴 **규율이 두 곳에 이미 박혀 있다** — [`ARSENAL`](ARSENAL.ko.md) §3 *"후보를 **발견**한다. **판정**은 공식 자료가 한다"* ·
  `AGENTS.md` *"`last30days` 는 후보 발견이지 판정이 아니다"*
- 👉 **새로 정할 것이 없다.** 하나만 바뀐다 — **플러그인 의존성으로 명시**하면 다른 기계에서도 따라온다

## 4. 그래서 **우리가 만드는 것은 넷뿐이다**

```
coolbress-standards                        (기본)
├── commands/kickoff.md          ← workflows 에 이미 있다. 심볼릭 링크 수작업을 없앤다
├── commands/new-project.md      ← 벽을 "세우는" 도구 (벽 자체는 GitHub 에 남는다)
├── skills/where-is-the-truth/   ← 우리 저장소 지도. 🔵 남에게 없다 — 우리 것이니까
└── plugin.json
      dependencies: mattpocock-skills · taste-skill · last30days-skill

coolbress-standards-hooks                  (+훅 · 옵트인)
├── hooks/ SessionStart          ← 만들 것 ⑦ (이슈 낭독) · fail-open · 빠르게
└── plugin.json
      dependencies: coolbress-standards · ponytail
```

**나머지는 전부 의존성이다.** 🚫 `mcpServers` 없음(‑ `gh` 가 있다 · 토큰 4~32배) · 🚫 `monitors` 없음 · 🚫 전용 상태 없음.

## 5. ⚠️ 이 설계가 지는 위험 셋 — **미리 적는다**

| | 위험 | 어떻게 잰다 |
|---|---|---|
| **①** | 🔴 **`ponytail`(최소주의) × `taste-skill`(디자인 풍부)이 프론트엔드 과제에서 충돌한다.** 시중 관찰: *"의견이 강한 스킬은 동의하지 않으면 **자기 스킬과 싸우게 된다**"* | **둘이 같이 발화하는 과제 하나**로 실측. `ponytail` 이 `+훅` 에 있어 **기본에서는 안 만난다** — 그게 1차 완화다 |
| **②** | ⚠️ **스킬 수.** 시중 휴리스틱은 *"잘 고른 **8~12개**가 시니어 하루의 대부분을 덮는다"* 인데 우리 기본은 mattpocock 35 + taste 13 + last30days = **50+** | 비용은 작다(≈1,841토큰). **문제는 비용이 아니라 발화 신뢰도** — *"메가 스킬은 늦게 뜨고 덜 발화한다"*. 실사용에서 **엉뚱한 스킬이 뜨는지**를 본다 |
| **③** | **핀 갱신이 사람 일이다** | `ARSENAL` §2b — **갱신은 PR 로.** `claude plugin update` 만 쓰면 무엇이 언제 바뀌었는지가 저장소에 안 남는다 |

## 6. 착수 순서 — **값이 확실한 것부터**

1. 🟢 **`project-template` 의 `.claude/settings.json` + `SessionStart`** — `divcal` 실패의 직접 처방이고 **커밋되고 리뷰된다.** 플러그인 없이도 값을 낸다
2. 🟢 **`coolbress-standards`(기본) 뼈대** — 커맨드 둘 + 지도 스킬 + 의존성 셋
3. 🟡 **`coolbress-standards-hooks`** — ⑦ 과 `ponytail`. **①의 충돌을 재고 나서**
4. ⬜ **`taste-skill` 비교** — 프론트엔드 과제가 처음 생길 때(`ARSENAL` §4 8번)
