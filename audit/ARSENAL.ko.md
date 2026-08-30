# Arsenal — 도구 대장

> 신설 2026-08-26 · **`.scratch/agent-project-operating-system` 에만 있던 분류·처분을 승격**했다.
> 승격한 이유는 하나다 — **`.scratch/` 는 `.gitignore` 대상이라 추적되지 않는다.**
> 다른 컴퓨터에서 clone 하거나 로컬을 정리하면 **정본이 가리키던 근거가 통째로 사라진다.**
>
> **Arsenal 은 큰 도구 창고다** — 지금 쓰는 것만이 아니라 **발견한 것 · 시험 중인 것 · 보류한 것 · 버린 것**을 남긴다.
> [`01`](../direction/01-what-i-want.md) §도구 창고가 개념을, 여기가 **실물 대장**을,
> [`SKILL-OVERLAP`](SKILL-OVERLAP.ko.md) 이 **만들 것 13개와의 대조**를 갖는다.

## 1. 종류를 먼저 가른다

**같은 칸에 있는 것끼리만 경쟁한다.** 이 표가 없으면 *"Fable 과 Ponytail 중 뭘 쓰지"* 같은 질문을 하게 된다 —
하나는 **모델**이고 하나는 **스킬**이라 애초에 경쟁 관계가 아니다.

| 종류 | 하는 일 | 예 | 지금 |
|---|---|---|---|
| **터미널 화면** | 명령을 보여준다 | Ghostty | 사용 중 · 언제든 교체 가능 |
| **여러 화면 관리** | pane 과 세션을 나눈다 | Herdr | 관찰이 필요할 때 |
| **에이전트 실행 환경** | 모델이 파일과 명령을 쓰게 한다 | Claude Code · Codex | 둘 다 사용 |
| **모델** | 생각하고 계획하고 코드를 만든다 | Fable · Claude · GPT/Codex · Gemini | 라우팅은 [`06`](../direction/06-how-we-work.md) §모델 |
| **스킬** | 특정 작업 절차를 알려준다 | Ponytail · grilling · Taste | 항목별 처분 아래 |
| **플러그인** | 실행 환경에 기능을 더한다 | Herdr File Viewer · frontend-design | 필요할 때만 |
| **연결 도구** | 바깥 도구와 잇는다 | GitHub CLI · Browser · MCP | `gh` 는 상시 |
| **여러 에이전트 방식** | 일을 나눠 처리한다 | subagent · Agent Team | **기본은 한 명** ([`06`](../direction/06-how-we-work.md)) |

> **Loadout 은 오늘 필요한 것만 담은 가방이다.** 모든 도구를 항상 켜지 않는 것이
> 대전제 2(*작고 가볍게*)를 실행 가능하게 만드는 장치다. 오늘의 가방 예시는 [`01`](../direction/01-what-i-want.md) 에 있다.

## 2. 후보와 처분

| 후보 | 하는 일 | 종류 | 처분 |
|---|---|---|---|
| [Matt Pocock Skills](https://github.com/mattpocock/skills) | 인터뷰 · 스펙 · 티켓 · TDD · 리뷰 | 스킬 | 🟢 **항목별 채택** — 대조는 [`SKILL-OVERLAP`](SKILL-OVERLAP.ko.md) |
| [Ponytail](https://github.com/DietrichGebert/ponytail) | 먼저 찾고 최소한으로 구현 | 스킬(플러그인) | 🟢 **채택 방향 확정 2026-08-29 — `+훅` 프로필.** 실물: MIT · ⭐115,858 · `SKILL.md` 가 *"YAGNI · 커스텀보다 표준 라이브러리 · 의존성보다 네이티브 · 오십 줄보다 한 줄"* 이라 **우리 규칙 1·2 의 코드 층 판**이고, 강도 `lite|full|ultra` 는 *가드 깊이는 위험 비례* 와 같은 형태다. 🔶 **훅 3종**(`SessionStart`·`SubagentStart`·`UserPromptSubmit`)이라 **기본이 아니라 옵트인**이다. 설계는 [`PLUGIN-DESIGN`](PLUGIN-DESIGN.ko.md) §3ⓑ |
| [last30days](https://github.com/mvanhorn/last30days-skill) | 최근 반응과 새 후보 찾기 | 스킬 | 🟡 **후보 발견 전용** — 🔴 **판정에는 쓰지 않는다**(아래 §3) |
| [Everything Claude Code](https://github.com/affaan-m/everything-claude-code) | 도구 카탈로그 | 목록 | 🟢 **카탈로그로 읽었다 (2026-08-29)** — 기록은 [`ECC-CATALOG-READING`](ECC-CATALOG-READING.ko.md). 셋을 가져오고 넷을 버렸다. **전체 설치는 여전히 안 함** — 파일 3,505개이고 **자기를 하네스라 부른다** |
| [Ouroboros](https://github.com/Q00/ouroboros) | 인터뷰부터 실행까지 Agent OS | 하네스 | 🔴 **전체 도입 보류** — 인터뷰 방식만 비교. **일곱 번째 하네스를 들이지 않는다** |
| [Caveman](https://github.com/JuliusBrussee/caveman) | 짧게 설명 · 컨텍스트 축소 | **엔진**(스킬 아님) | 🔴 **기각 2026-08-29 — 근거 셋, 하나만으로도 충분하다.** ① **라이선스**: `engine/`·`proxy/`·`cacheengine/`·`mcp/`·`cavemem` 이 **BSL-1.1**(오픈소스 아님)이고 원문이 *"새 Engine-linked 모듈은 **기본이 BSL-1.1**"* 이라 적는다 — [`05`](../direction/05-the-output-floor.md) §라이선스의 *아웃바운드 하나* 가 성립 안 한다 ② **상태 소유**(`cacheengine`·`cavemem`) — 판별식 ③ 위반 ③ **1,393파일·9.5MB·release-binaries** — 스킬이 아니라 엔진이다. ⚠️ *"측정된 65% 절감"* 은 **자기 측정**이라 검증 대상이지 채택 근거가 아니다. 🔵 **목적은 살린다** — 만들 것 ⑧ⓐ(*쉬운 말이 기본값*) + `needs-simpler` 라벨이 **이미 그 자리**다 |
| 🔄 **[Taste Skill](https://github.com/Leonxlnx/taste-skill)**([tasteskill.dev](https://www.tasteskill.dev/)) · [frontend-design](https://github.com/anthropics/claude-code/tree/main/plugins/frontend-design) · [Impeccable](https://github.com/pbakaus/impeccable) | 프론트엔드 품질 — *anti-slop* | 스킬/플러그인 | 🟡 **같은 화면 과제로 비교해 하나만.** 🔴 **정정 2026-08-29 — 이 행이 *이름만* 적혀 있어서 엉뚱한 것을 가리켰다**: ECC 안의 `skills/taste` 는 **뮤직비디오 편집** 스킬이다. 소유자가 가리킨 것은 `Leonxlnx/taste-skill`(⭐82,005 · MIT · **이미 Claude Code 플러그인** · 스킬 13개)이고, **비교는 프론트엔드 과제가 생길 때 한다**(§4 8번). 실측은 [`ECC-CATALOG-READING`](ECC-CATALOG-READING.ko.md) §4 |
| Herdr | 여러 터미널·에이전트 보기 | 화면 관리 | 🟡 관찰이 필요할 때 |
| Ghostty | 터미널 | 화면 | 🟢 사용 중 |
| **직접 만든 도구** | 외부 도구 사이의 빈틈 | — | 🔴 **빈틈이 실제로 확인됐을 때만.** 원칙: 규칙 1(*만들기 전에 먼저 찾는다*) |

> 🔴 **외부 스킬의 내용을 이 저장소로 복사하지 않는다.** 그렇게 하면 참조가 아니라
> **또 하나의 거대한 하네스**가 된다 — 여섯 번 무너진 그 모양이다([`02`](../direction/02-why-past-attempts-failed.md)).
>
> ⚠️ **그러므로 *항목별 채택* 은 *스킬 하나만 복사* 가 아니다.** 핀된 묶음을 **참조로 들이고
> 우리가 고른 항목만 쓰는 것**이다 — 복사가 금지돼 있으므로 이것이 유일하게 규칙에 맞는 모양이다.

### 2b. 외부 스킬을 **어떻게 핀하나** (실측 2026-08-29 · R5-24)

🔴 **핀은 설치 명령이 아니라 *마켓플레이스 항목* 에 산다.** `claude plugin install` 에는
`--version`·`--ref` 옵션이 **없다**. 항목이 SHA 를 담는다:

```json
{ "source": { "source": "url", "url": "https://github.com/…", "sha": "<40자 커밋 SHA>" } }
```

공식 마켓(`anthropics/claude-plugins-official`) 실측: **291개 중 238개(81.8%)가 `sha` 를 갖는다.**
**우리 규칙과 같은 모양이다** — 핀은 SHA, 태그(`ref`)는 그 SHA 를 읽기 위한 것.

| 대상이 | 우리가 할 일 |
|---|---|
| **공식 마켓에 있고 SHA 가 붙어 있다** | 그대로 설치한다. 핀은 이미 걸려 있다 (`mattpocock-skills`) |
| **공식 마켓에 있는데 SHA 가 없다** | 핀이 없다는 **사실을 근거로 기록**하고 판단한다 (`frontend-design` — 소스가 로컬 경로다) |
| **공식 마켓에 없다** | **우리 마켓플레이스 항목을 직접 쓴다** (Ponytail · Caveman · Taste · ECC · Impeccable) |

🔴 **갱신 정책**: 핀을 올리는 것은 **PR** 이다. `claude plugin update` 는 최신으로 끌어오므로
그것만 쓰면 *무엇이 언제 바뀌었는지*가 저장소에 안 남는다 — Actions 핀을 올릴 때와 같은 규율이다.

### 2c. 🔬 2026 후보 훑기 — **셋을 재고 셋 다 안 넣는다** (2026-08-30)

소유자 질문: *"좋은 무기를 트렌드 검색으로 다 넣는 게 낫지 않나?"*
훑었고 **답은 아니다**. 이유가 항목마다 다르다.

| 후보 | 설치 수 | 처분 | 왜 |
|---|---|---|---|
| **Superpowers** (`obra`) | ~752k | 🔴 **기각 — 경쟁 프레임워크지 빈칸이 아니다** | 아래 |
| **Frontend Design** (Anthropic 공식) | ~277k | 🔴 **기각 — `taste-skill` 과 같은 자리** | 겹치면 안 넣는다(§4). 소유자가 이미 고른 것이 있다 |
| **Context7** | ~349k | 🔴 **이미 적힌 기각에 걸린다** | MCP 서버다. [`PLUGIN-DESIGN`](PLUGIN-DESIGN.ko.md) §*"🚫 `mcpServers` 없음 — `gh` 가 있다 · 토큰 4~32배"* |

#### Superpowers 를 왜 안 넣나 — **우리 결정과 정면으로 부딪힌다**

12~14개 스킬이 **방법론 하나를 통째로** 깐다. 그 항목들이 우리 층과 하나씩 겹치는데,
**겹침보다 나쁜 것은 그중 둘이 우리가 근거를 대고 내린 결정과 반대**라는 점이다:

| Superpowers | 우리 |
|---|---|
| brainstorming · writing/executing plans | `/kickoff` · **`mattpocock-skills` 가 이미 그 자리다**(실측: 발화 기록에 `writing-plans`·`executing-plans` 가 찍힌다) |
| requesting/receiving code review | `/review`(외부 모델 우선) |
| verification before completion | **원칙 02** — 완료는 주장이 아니라 머지된 커밋 |
| **test-driven-development 강제** | 🔴 **반대 결정**: `CONTRIBUTING` 이 *"실패하는 테스트를 먼저 쓰는 것을 **권한다 — 강제하지는 않는다.** 순서 자체의 효과는 **증거가 갈린다**"* |
| **subagent-driven / dispatching parallel agents** | 🔴 **반대 결정**: **원칙 04 — 판단은 위임하지 않는다** |

**프레임워크를 들이면 그 방법론도 같이 들어온다.** 대전제 1(*있는 걸 다시 만들지 않는다*)은
**빈칸을 메울 때** 적용되는 것이지, **이미 결정한 자리를 덮으라는 말이 아니다.**

#### 🔴 그리고 지금 더 넣는 것 자체가 틀린 순서다

실측 — `check_skill_firing`: 사건 **15** · 서로 다른 **12** · **우리 것 1**.
1차 보고가 그 형태를 정확히 부른다: *"the agent had all the tools and **none of the instructions
to use them**"* · *"the **silent fallback to training data** is the actual problem"*.

**무기가 모자란 게 아니라 무기고가 있다는 걸 안 알려준 것**이었다.
`coolbress-standards-hooks` v0.5.0 이 그 안내를 넣었다(≈300토큰 · 강제 아님).

> **순서: 안내를 켠다 → 발화를 다시 잰다 → 그래도 안 움직이면 그때 무기를 본다.**
> 안 움직이는데 무기를 더 넣으면 **상시 토큰만 늘고 발화는 그대로**다.

⚠️ **핀은 셋 다 HEAD 다**(2026-08-30 확인 · `taste-skill`·`last30days`·`ponytail`) — 뒤처져서 생긴 문제가 아니다.

## 3. 인기 신호와 사실 판정을 가른다

**`last30days` 같은 도구는 *후보를 발견*한다. *판정*은 공식 자료가 한다.**
별 수·화제성은 *"이게 존재한다"* 는 신호지 *"이게 맞다"* 는 근거가 아니다 —
이 저장소가 [`EVIDENCE-POLICY`](../corpus/methods/EVIDENCE-POLICY.md) 로 코퍼스에 거는 것과 같은 기준을 도구에도 건다.

## 4. 새 도구를 들이기 전에 묻는 열한 가지

1. 실제로 **반복되는** 어떤 문제를 푸는가?
2. **기본 기능이나 기존 도구에 이미 있는가?**
3. 큰 도구 창고 · 프로젝트 시작 상자 · 서버 통과문 중 **어디에 속하는가**?
4. 어떤 **능력 칸**을 채우는가?
5. **같은 능력을 이미 맡은 도구가 있는가?**
6. 언제 켜고 **언제 끄는가**?
7. 어떤 **권한과 자격증명**을 쓰는가?
8. **실제 대표 작업**에서 더 좋아졌는가?
9. 시간 · 토큰 · 돈 · 관리 비용은 얼마인가?
10. **어떤 조건이 되면 버릴 것인가?**
11. **인기 신호와 사실 판정을 헷갈리고 있지 않은가?**

> **답이 흐리면 일단 넣지 않는다.**

**대장에 적을 것**: 해결하는 문제 · 종류와 능력 칸 · 공식 저장소 · 상태(시험·채택·보류·제거) ·
고정한 버전이나 commit · 대표 시험 결과 · 켜는 조건 · 같은 일을 하는 다른 후보 · 필요한 권한 ·
시간/토큰/돈 · 다시 확인할 때 · **버릴 조건**.

> 🔴 **후보는 *이름* 이 아니라 *저장소* 로 적는다** (2026-08-29 신설).
> 이 대장의 *Taste* 행이 이름만 들고 있어서 **엉뚱한 물건을 가리켰다** — 같은 이름의 다른 스킬이 최소 둘이다
> ([`ECC-CATALOG-READING`](ECC-CATALOG-READING.ko.md) §3). `direction/` 이 코퍼스를 **경로로** 인용해야 하는 것과
> **같은 형태의 결함**이고, 그쪽은 `check_name_only_citations` 가 막는다. **여기는 아직 사람이 지킨다.**

## 5. 🗑 덜어낼 것 — 그리고 지금 어디에 있나

*"가볍게 만들기 위해 뺄 것"* 일곱 가지. **덜어내기도 결정이므로 추적한다.**

| 뺄 것 | 지금 |
|---|---|
| ~~코드가 아닌 변경에도 테스트를 강요하는 규칙~~ | ✅ **덜어냈다 2026-08-27**(D-5) — 세 문서가 한 문장만 말한다. 기준이 **파일**에서 **동작**으로 바뀌었다 |
| 릴리스하지 않는 프로젝트의 **빈 CHANGELOG** | 🔶 **D-7** · 프로필 결정(**D-2**)에 걸린다 |
| 실제 환경 변수가 없는 **빈 `.env.example`** | 🔶 **D-7** |
| 사람 승인이 0인데 켜 둔 review 옵션 | ✅ **결정 2026-08-27**(A-2) — **승인 0 을 유지한다.** 도장을 흉내내는 대신 **CI 를 진짜 게이트로** 쓴다 |
| ~~CodeQL 과 Semgrep 을 **이유 없이 함께**~~ | ✅ **덜어냈다** — [`C-2 실측`](SAST-CODEQL-VS-SEMGREP.ko.md): 잡는 것이 거의 겹친다. **공개는 CodeQL 하나, 비공개는 Semgrep 하나** |
| ~~push protection 이 있는데 **gitleaks 를 무조건 더하기**~~ | ✅ **덜어내지 않는다** — [`C-3 실측`](SECRET-DETECTION-OVERLAP.ko.md): 겹치는 게 아니라 **다른 것을 잡는다**. 🔴 **푸시 보호가 개인키 PEM 을 통과시킨다** |
| 모든 프로젝트에 coverage 숫자 · Docker · SBOM · 서명 강제 | ✅ **이미 반영** — [`05`](../direction/05-the-output-floor.md) 가 `RETAIN-RN/SPLIT` 로 *"묶음째 보편"* 지위를 낮췄다 |

## 6. 자격증명은 도구가 아니라 **문**이다

> **에이전트가 못 끄는 벽**은 권한이 갈려야 성립한다 — [`AUDIT`](TEMPLATE-WORKFLOWS-AUDIT.ko.md) **A-1**.

✅ **2026-08-27 시행됨.**

| 권한 | 값 |
|---|---|
| Contents · Issues · Pull requests · Workflows | Read **and write** |
| **Administration** · **Code scanning alerts** | 🔑 **Read-only** — 벽을 *읽되* 옮기지는 못한다 |
| Secrets · Environments · Variables · Webhooks · Pages | **No access** |

🔴 **읽기를 막았더니 감사기가 눈이 멀었다.** 첫 판은 Administration 도 `No access` 였고,
그 결과 `repo_audit` 이 **아무것도 확인하지 못했다**(`unknown=12`).
**감사기가 눈을 뜨는 것과 벽이 무너지는 것은 다른 문장이다.**

**검증은 실패로 했다** — 성공이 아니라 **403 을 확인**했다:

| 시도 | 결과 |
|---|---|
| 룰셋 수정 · 삭제 | 🔒 **403** |
| Actions 정책 변경 · 시크릿 읽기 | 🔒 **403** |
| 저장소 설정 변경 · 환경 생성 | 🔒 **403** |
| **CodeQL default setup 켜기** | 🔒 **403** |
| 시크릿 읽기 | 🔒 **403** |
| 서버 설정 **읽기**(Actions 정책 · 보안 · CodeQL · 룰셋) | 🔑 **200** — 읽기 권한을 준 뒤 |
| 읽기 · 이슈 · PR · `git push` | ✅ 정상 |

🔴 **분리 직전에 이전 자격증명도 쟀다** — 저장소 설정 PATCH **성공**, 시크릿 목록 읽기 **성공**.
***벽이 서 있던 게 아니라 내가 안 지우기로 하고 있었을 뿐이다.*** 그건 벽이 아니라 규율이다.

**운용**: `~/.zshenv` 가 `~/.config/gh-agent-token`(0600)을 읽어 `GH_TOKEN` 에 건다.
⚠️ **`.zshrc` 가 아니라 `.zshenv` 인 이유**: `.zshrc` 는 **대화형 셸만** 읽어 도구 셸에 안 닿는다.

🔴 **관리자 열쇠는 이 컴퓨터에 없다** (2026-08-27) — `gh auth logout` 으로 열쇠고리에서 뺐다.
처음엔 *"에이전트는 `env -u GH_TOKEN` 을 안 쓴다"* 는 **규율**로 막으려 했는데,
`security find-generic-password -w` 로 **`gh` 를 안 거치고도 프롬프트 없이 뚫렸다.**
**규율로 막을 수 있는 것과 없는 것을 가르는 자리가 여기였다.**

## 7. Loadout 의 실물 — **필드 셋** (2026-08-29 신설)

§1 의 *Loadout*(오늘 필요한 것만 담은 가방)은 **개념만 있고 구현이 없었다.**
[`ECC-CATALOG-READING`](ECC-CATALOG-READING.ko.md) §1ⓑ 에서 가져온다 — ECC 는 §4 의 열한 문항 중
**두 개를 기계가 읽는 필드로** 만들었다.

**후보마다 이 셋을 적는다:**

| 필드 | 값 | 무엇을 답하나 |
|---|---|---|
| `cost` | `light` · `medium` · `heavy` | §4 **9번**(시간·토큰·돈). 🔴 **재는 것은 상시 부담이다** — 스킬은 프론트매터, MCP 는 도구 정의. 실측 단위를 같이 적는다 |
| `stability` | `stable` · `beta` · `experimental` | 얼마나 믿고 켜나 |
| `defaultInstall` | 예 · 아니오 | **가방에 기본으로 넣나** — 이게 Loadout 그 자체다 |

**지금 값** (실측한 것만 적는다 — 나머지는 재고 나서 채운다):

| 후보 | `cost` | `stability` | `defaultInstall` | 훅 |
|---|---|---|---|---|
| [Matt Pocock Skills](https://github.com/mattpocock/skills) | **light** — 프론트매터 35개 **≈1,841토큰**(본문 149KB 는 필요할 때만) | stable | 🟢 **예 — 기본 프로필** | ❌ |
| [last30days](https://github.com/mvanhorn/last30days-skill) | **light** | stable | 🟢 **예** — ✅ **이미 설치됨**. 규율은 §3(발견 전용) | ❌ |
| [Taste Skill](https://github.com/Leonxlnx/taste-skill) | **light** — 스킬 13개 · *"어떤 규칙도 자동 발화하지 않는다"* | ⚠️ **experimental** (v2 실험판 · v1 legacy) | 🟡 **기본에 두되 비교 전까지 판단 보류** — 범위가 **랜딩·포트폴리오·리디자인**으로 한정된다 | ❌ |
| [Ponytail](https://github.com/DietrichGebert/ponytail) | **light** — 파일 159 | stable (v4.9.0) | 🔶 **아니오 — `+훅` 옵트인** | 🔶 **3종** |
| [Caveman](https://github.com/JuliusBrussee/caveman) | 🔴 **heavy** — 1,393파일 · 엔진 | — | 🔴 **기각**(라이선스 BSL-1.1 · 상태 소유) | 🔶 2종 |
| MCP 서버 일반 | 🔴 **heavy** — 도구 정의가 **컨텍스트에 영구 상주**, 개당 150~600토큰 · 매 호출 지불 | — | ❌ **아니오** | — |
| [ECC](https://github.com/affaan-m/everything-claude-code) | 🔴 **heavy** — 파일 3,505 · `SKILL.md` 898 | stable | ❌ **아니오 — 카탈로그로만** | 🔶 |

🔴 **프로필은 둘까지만 만든다.** ECC 는 **7개 · 모듈 36개**다. 우리가 그 수를 따라가면 그게 하네스다
(대전제 2). 우리 둘은 **기본**(안내 + 커맨드)과 **`+훅`**(만들 것 ⑦ 옵트인)이다 —
🔵 **ECC 도 `minimal`·`opencode` 프로필에서 훅 런타임을 *일부러* 뺀다**(§ⓐ 실측).

> 🔴 **그리고 프로필을 *설치기* 로 만들지 않는다** (2026-08-29). Claude Code 에는 프로필 개념이 없고,
> ECC 는 그걸 **자체 설치 스크립트**로 만든다 — **설치기는 하네스의 시작이다.**
> 우리는 **플러그인 둘 + 네이티브 `dependencies`** 로 같은 것을 얻는다. 설계는 [`PLUGIN-DESIGN`](PLUGIN-DESIGN.ko.md).
