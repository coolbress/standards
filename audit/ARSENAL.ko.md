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
| [Ponytail](https://github.com/DietrichGebert/ponytail) | 먼저 찾고 최소한으로 구현 | 스킬 | 🟡 **구현 과제에서 시험** |
| [last30days](https://github.com/mvanhorn/last30days-skill) | 최근 반응과 새 후보 찾기 | 스킬 | 🟡 **후보 발견 전용** — 🔴 **판정에는 쓰지 않는다**(아래 §3) |
| [Everything Claude Code](https://github.com/affaan-m/everything-claude-code) | 도구 카탈로그 | 목록 | 🟡 **카탈로그로만** — 전체 설치 안 함 |
| [Ouroboros](https://github.com/Q00/ouroboros) | 인터뷰부터 실행까지 Agent OS | 하네스 | 🔴 **전체 도입 보류** — 인터뷰 방식만 비교. **일곱 번째 하네스를 들이지 않는다** |
| [Caveman](https://github.com/JuliusBrussee/caveman) | 짧게 설명 · 컨텍스트 축소 | 스킬+proxy | 🔴 **무거운 proxy 보류** — 간결성만 시험 |
| Taste · [frontend-design](https://github.com/anthropics/claude-code/tree/main/plugins/frontend-design) · [Impeccable](https://github.com/pbakaus/impeccable) | 프론트엔드 품질 | 스킬/플러그인 | 🟡 **같은 화면 과제로 비교해 하나만** — 셋을 동시에 켜지 않는다 |
| Herdr | 여러 터미널·에이전트 보기 | 화면 관리 | 🟡 관찰이 필요할 때 |
| Ghostty | 터미널 | 화면 | 🟢 사용 중 |
| **직접 만든 도구** | 외부 도구 사이의 빈틈 | — | 🔴 **빈틈이 실제로 확인됐을 때만.** 원칙: 규칙 1(*만들기 전에 먼저 찾는다*) |

> 🔴 **외부 스킬의 내용을 이 저장소로 복사하지 않는다.** 그렇게 하면 참조가 아니라
> **또 하나의 거대한 하네스**가 된다 — 여섯 번 무너진 그 모양이다([`02`](../direction/02-why-past-attempts-failed.md)).

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

## 5. 🗑 덜어낼 것 — 그리고 지금 어디에 있나

*"가볍게 만들기 위해 뺄 것"* 일곱 가지. **덜어내기도 결정이므로 추적한다.**

| 뺄 것 | 지금 |
|---|---|
| 코드가 아닌 변경에도 테스트를 강요하는 규칙 | 🔶 [`AUDIT`](TEMPLATE-WORKFLOWS-AUDIT.ko.md) **D-5** — 문서 세 곳이 서로 다르게 말한다 |
| 릴리스하지 않는 프로젝트의 **빈 CHANGELOG** | 🔶 **D-7** · 프로필 결정(**D-2**)에 걸린다 |
| 실제 환경 변수가 없는 **빈 `.env.example`** | 🔶 **D-7** |
| 사람 승인이 0인데 켜 둔 review 옵션 | 🔶 **A-2** — 솔로가 자기 PR 을 승인할 수 없다는 트레이드오프 |
| CodeQL 과 Semgrep 을 **이유 없이 함께** | 🔬 **C-2** — 탐지율·오탐 비교가 미조사 |
| push protection 이 있는데 **gitleaks 를 무조건 더하기** | 🔬 **C-3** — 겹침이 값을 하는지 미측정 |
| 모든 프로젝트에 coverage 숫자 · Docker · SBOM · 서명 강제 | ✅ **이미 반영** — [`05`](../direction/05-the-output-floor.md) 가 `RETAIN-RN/SPLIT` 로 *"묶음째 보편"* 지위를 낮췄다 |

## 6. 자격증명은 도구가 아니라 **문**이다

> **에이전트가 못 끄는 벽**은 권한이 갈려야 성립한다 — [`AUDIT`](TEMPLATE-WORKFLOWS-AUDIT.ko.md) **A-1**.

평소 에이전트가 쥐는 것: **Contents · Pull requests · Issues** 읽기/쓰기.
쥐지 않는 것: **Administration · Actions 설정 · Secrets · Environments · Workflows 쓰기**.

**검증은 실패로 한다** — 에이전트 자격증명으로 `gh api repos/…/rulesets --method PUT` 을 시도해
**403 이 나야 갈린 것**이다. 성공하면 벽이 아니다.
