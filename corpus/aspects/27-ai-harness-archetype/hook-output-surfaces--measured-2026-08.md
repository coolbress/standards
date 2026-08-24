---
id: aspect-27-ai-harness-archetype--hook-output-surfaces--measured-2026-08
title: "훅 출력 표면 실측 — 하네스가 사용자에게 말할 수 있는가"
parent: aspect-27-ai-harness-archetype
kind: evidence
evidence_track: lit
status: draft
language: ko
last_updated: "2026-08-07"
method: "훅 이벤트별 출력 표면을 실행으로 측정. 공식 문서의 systemMessage 청중 기술 3곳을 뒤집었다. 원본: goppi_final/records/2026-08-07-output-surface-probe.md — 2026-08-24 이관, 본문 무수정."
---

> **이관 기록 (2026-08-24)**: 원본 저장소는 **삭제 예정**이다(2026-08-24 기준 로컬·원격 모두 존속). 이 문서는 **폐기된 하네스가 아니라 호스트(Claude Code)의
> 실제 동작**에 대한 1차 실측이므로 남긴다. 하네스의 계보는 `legacy/LINEAGE.md`.
> **재검증 결과는 문서 끝에 있다 — 먼저 읽을 것.**


> 📌 **후속 판정 있음 (2026-08-08)** — 본문은 2026-08-07 시점 그대로 보존한다(고쳐 쓰지 않는다).
> 이 기록이 유일하게 남긴 `UNVERIFIED`(§9 첫 항목 · §5 표의 "렌더링 UNVERIFIED")는
> **해소됐다**: `hook_system_message`는 사용자 터미널에 **렌더링된다**(사람 관측 n=1).
> → `user-channel-rendering--measured-2026-08.md`.
> 아래 §5·§9를 읽을 때 그 두 곳은 **현재 상태가 아니라 당시 상태**다.

> 성격: 실행한 명령과 읽은 출력만. 검증 못 한 것은 `UNVERIFIED`.
> 선행: `2026-08-07-slice1-closure.md` §8.6 — 상위 모델이 "조각 2보다 먼저"라고 지목한 항목.
> 도구: 헤드리스 자식 세션 **9회** (`claude -p --plugin-dir --output-format stream-json --include-hook-events`).

## 1. 왜 이것이 G4보다 먼저인가

조각 1은 **"하네스가 볼 수 있는가"**를 답했다. G4는 **"판정할 수 있는가"**를 답한다.
그런데 제품 주장은 **"사용자가 감지할 수 있는가"**다. 그 사이의 링크 —
**하네스가 사용자에게 말할 수 있는가** — 는 한 번도 시험되지 않았고 유일한 데이터가 음성이었다
(백그라운드 세션에서 `ask`가 프롬프트 없이 차단됨).

G4를 먼저 지으면 **전달 채널이 미확인인 판정 장치**를 짓는 것이다.

## 2. 방법 — 입력 탐침을 뒤집었다

조각 1은 훅 입력의 키 경로를 덤프해 스키마를 배웠다(`probeSchema`). 출력에는 같은 수법이 안 통한다 —
**훅은 자기 출력이 어디로 갔는지 볼 수 없다.** 그래서 방향을 뒤집었다:
채널마다 **고유 마커**를 내보내고, 그 마커가 어느 관측 표면에 나타나는지를 밖에서 셌다.

관측 표면 4개 (**누가 그 증거를 쓰는가** — spec §6의 필수 질문):

| # | 표면 | 누가 쓰는가 | 헤드리스에서 |
|---|---|---|---|
| 1 | 부모 프로세스의 `stream-json` | 호스트 | 볼 수 있다 |
| 2 | 자식 세션의 트랜스크립트 파일 | 호스트 | 볼 수 있다 |
| 3 | 자식 모델의 자기보고 | **모델** (약한 고리) | 볼 수 있다 |
| 4 | **사용자의 터미널** | — | **없다. 사람만 관측 가능** |

liveness 가드(조각 1 T-1의 교훈): 탐침은 발화할 때마다 자기 로그를 남긴다.
그래야 "마커가 안 보인다"가 **출력이 삼켜졌다**인지 **훅이 안 돌았다**인지 갈린다.

## 3. 실측 행렬

훅 이벤트 5종(SessionStart · UserPromptSubmit · PreToolUse · PostToolUse · Stop) × 채널.

| 변이 | 채널 | 트랜스크립트 attachment | **모델 컨텍스트** | 비고 |
|---|---|---|---|---|
| A | stdout JSON `systemMessage`, exit 0 | `hook_system_message` **5/5** | **0/5 — 도달 안 함** | 전용 표면이 따로 만들어진다 |
| B | stdout 평문, exit 0 | `hook_success`만 | **2/5** (SessionStart·UserPromptSubmit) | `"<훅> hook success: <stdout>"` 형태 |
| C | `hookSpecificOutput.additionalContext`, exit 0 | `hook_additional_context` 5/5 | **5/5 전부** | L0가 쓰는 채널 |
| D | stderr JSON, exit 2 — **조각 1의 goppi** | **없음** | 도달(오류 문자열로) | JSON이 **파싱되지 않는다** |
| E | Stop `{decision:block, reason}` | `hook_blocking_error` | 도달 → **새 턴 유발** | B21 |
| G | stdout JSON + `hookEventName`, exit 0 | `hook_system_message` | reason만 도달 | **deny 집행됨** |
| H | 위와 같되 **exit 2** | `hook_system_message` | reason만 도달 | **집행 + fail-closed** |
| J | H + stderr 평문 동시 | `hook_system_message` | reason만 도달 | **stdout이 이긴다**(stderr 무시) |

## 4. 뒤집힌 것 셋

### 4.1 호스트 문서가 틀렸다 — `systemMessage`는 모델에게 가지 않는다

`hook-development/SKILL.md`는 두 곳에서 이렇게 쓴다:

> `systemMessage`: **Message shown to Claude** / "Explanation for Claude"

실측은 반대다. 변이 A에서 다섯 이벤트 **5/5** 전부 `hook_system_message` attachment가 생성됐는데
**모델 컨텍스트 도달은 0/5**였고, 자식 모델은 `NO-OUTPROBE-SEEN`이라고 답했다.
이름 그대로 **모델이 아닌 쪽**을 향한 전용 채널이다.

> 조각 1의 "문서를 믿지 말고 해봐라" 표에 **여섯 번째 줄**이 붙는다.

### 4.2 조각 1의 원인 귀속이 틀렸다 — 범인은 exit 0이 아니라 라우팅 키였다

조각 1 기록: *"PreToolUse의 deny는 stdout+exit 0이 아니라 **stderr + exit 2**여야 집행된다."*

**결론은 맞았고 원인은 틀렸다.** 첫 판이 낸 JSON에는 `hookSpecificOutput.hookEventName`이 **없었다.**
그 키를 넣자 변이 G(exit 0)에서도 변이 H(exit 2)에서도 **deny가 집행됐다**
(`is_error: true` · `toolDenialKind: permission-rule` · 대상 파일 미생성).

원인을 잘못 짚은 대가는 컸다 — 그 오귀속 때문에 goppi는 **stderr에 갇혔고**,
stderr JSON은 호스트가 파싱하지 않으므로 `systemMessage`가 **아무 데도 가지 않았다.**

### 4.3 goppi에게는 사용자 채널이 **없었다** — 기계 측정값

이 세션(`651290a8`)의 트랜스크립트 실측:

```
attachment 종류별: hook_success 4 · hook_additional_context 1 · hook_system_message 0
```

G1 deny를 의도적으로 발화시킨 뒤에도 **`hook_system_message` 0건**이다.
모델이 받은 것은 이 형태였다:

```
PreToolUse:Bash hook error: [node "${CLAUDE_PLUGIN_ROOT}/scripts/gate-pre-tool.mjs"]:
{"hookSpecificOutput":{"permissionDecision":"deny"},"systemMessage":"goppi G1: …"}
```

→ **"정직 고지가 도메인 오너에게 가는 것은 0개"(closure §8.6)가 주장에서 측정값이 됐다.**

## 5. 처분 — 고친 것

`respondPreTool(decision, modelReason, userMessage)` 로 재작성. 응답은 세 곳으로 갈린다:

| 나가는 곳 | 청중 | 확인 상태 |
|---|---|---|
| stdout `hookSpecificOutput.permissionDecisionReason` | **모델** | 확인됨 |
| stdout 최상위 `systemMessage` | **사람** (`hook_system_message` 생성) | 생성까지 확인 · **렌더링 UNVERIFIED** |
| exit code 2 | 집행 | 확인됨 |
| stderr 평문 | 대체 경로 | stdout이 읽히면 무시됨(변이 J) |

**왜 stdout인데 exit 2인가**: exit 0은 **fail-open**이다. 호스트가 JSON을 못 읽으면 도구가 그냥 실행된다.
설계 §2 L2의 "fail-closed(보안)/fail-open(작업 보호) 비대칭"상 G1은 fail-closed여야 한다.
호스트는 **exit 2에서도 stdout을 파싱한다**(변이 H). 그래서 둘 다 가진다.

**stderr 평문을 함께 내는 이유**: 헤드리스 `ask` 경로에서 stdout의 reason이 유실되고
`"No stderr output"`이 되는 것을 관측했다(변이 I). 그 경로를 메우는 대체선이다.

G2의 **복구 두 필드(SR-02)를 사용자 문장으로 옮겼다** — 사람이 판단하라고 만든 필드가
그전에는 모델에게만 갔다.

## 6. 실물 end-to-end 검증 (단위 검사가 아니라)

`output-surface-control.mjs`는 게이트를 직접 호출해 **형태**만 본다.
호스트가 그 형태를 받아들이는지는 실세션에서만 알 수 있고, **훅은 세션 경계에서 로드**되므로
현재 세션에서는 확인할 수 없다. → **자식 세션이 유일한 경로다.**

```
$ claude -p --plugin-dir <실물 goppi> --output-format stream-json --include-hook-events
  프롬프트: 증거 경로에 append 하라
```

결과:

```
① hook_system_message / PreToolUse
   "goppi가 명령을 막았습니다 — 검사 결과를 담는 기록 경로에 쓰려는 것으로 판정했습니다.
    검사를 받는 쪽이 그 결과를 고칠 수 없어야 하기 때문입니다. 읽기는 막지 않습니다."
② 모델이 받은 것: is_error=true · denialKind=permission-rule
   "goppi G1: 하네스 증거 경로에 대한 쓰기로 판정했습니다 (write_redirect). …"   ← 원문 JSON 덤프가 사라졌다
③ 자식 모델의 보고: **BLOCKED**
④ 대상 파일: No such file or directory   ← 차단이 파일시스템 수준에서 성립
```

## 7. B21 해소 — Stop 훅은 **사후 표기하지 못한다. 사후 추가는 한다**

B21: *"Stop 훅이 이미 출력된 완료 메시지를 사후 표기할 수 있는가."*

- **수정: 불가.** `{decision:"block", reason}` 은 `hook_blocking_error` attachment가 되어
  **모델에게** 가고 모델이 **새 턴**을 만든다. 이미 출력된 메시지는 그대로 남는다.
  즉 하네스가 보고서에 `UNVERIFIED`를 **찍는** 것이 아니라, **모델에게 다시 말하라고 시키는** 것이고
  그 새 턴의 내용은 **모델이 쓴다.**
- **추가: 가능(형식적으로).** 변이 A에서 Stop 이벤트도 `hook_system_message`를 만들었다.
  완료 메시지 **뒤에 하네스가 쓴 문장**을 붙일 수 있다 — G4 fallback의 운반체 후보다.

→ spec §11의 *"하네스가 보고서에 UNVERIFIED를 찍는다고 약속하지 않는다"* 는 **유지되어야 하고,**
이제 그 이유가 **미확인이 아니라 확인된 구조**다.

## 8. 부수로 확정된 것 — 항목 ②(헤드리스 러너)의 전제

`--include-hook-events` 가 실재하고, `stream-json`은 훅 생명주기를 **원출력째로** 싣는다:

```
system:hook_started / system:hook_response  { output, stdout, stderr, exitCode, durationMs, command }
```

→ closure §8.6의 *"`stream-json`이 무엇을 담는지는 UNVERIFIED"* 가 **해소됐다.**
부모 프로세스는 자식 세션의 훅 발화를 전부 볼 수 있다.

## 9. 이 기록이 보장하지 않는 것

- **`hook_system_message`가 사용자 터미널에 렌더링되는지는 `UNVERIFIED`다.**
  헤드리스에는 터미널이 없고, 이것은 **사람만 관측할 수 있다.**
  확인 전까지 **"goppi가 사용자에게 말한다"고 말하지 않는다.** 확인된 것은
  *"호스트가 사용자용 전용 레코드를 만들고, 그 내용은 모델에게 가지 않는다"*까지다.
- **문장이 이해되는지는 판정하지 않았다.** 제품 GO 7조건의 "이해 가능성"은 확증시험 소관이다.
- **빈도·피로 미측정.** G1은 조각 1에서 정당한 작업을 9회 막았다. 매 발화마다 사용자에게
  문장을 보내는 것이 옳은지는 데이터가 없다 — 조각 4(오탐 측정)의 입력으로 남긴다.
- **대화형 세션의 `ask`는 여전히 미검증이다.** 헤드리스에서는 프롬프트가 뜰 수 없다.
- 헤드리스 arm의 결과가 대화형 arm으로 일반화된다고 주장하지 않는다 —
  `ask`의 맥락 의존성(spec §11.1)이 그 반례다.

## 10. 부수 관측 — FP-2가 이 세션에서 재현됐다

### 10.1 탐침을 저장소로 옮긴 뒤 **실행해 보고 나서야** 깨진 것을 찾았다

`harness/probe/`로 보존하며 경로를 다시 썼는데, **새 위치에서 한 번도 돌려보지 않은 채**
README에 실행법을 적었다. 실제로 돌리자 판독기가 자식 트랜스크립트를 **찾지 못했다**.

원인: 호스트의 프로젝트 슬러그 규칙을 `cwd.split("/").join("-")`로 흉내냈는데
실제로는 `_` 와 `.` 도 `-` 로 바뀐다
(`/Users/x/goppi_final/harness/probe/.work/childcwd` → `-Users-x-goppi-final-harness-probe--work-childcwd`).

→ 규칙을 고쳐 흉내내지 **않았다.** 그것도 문서화되지 않은 동작이고, 이 탐침이 배운 것이 정확히
*"문서화되지 않은 동작을 추측하지 마라"*다. **세션 ID(uuid)로 파일을 찾도록** 바꿨다 — 규칙이 바뀌어도 안 깨진다.

> 문서화되지 않은 호스트 동작을 추측한 **세 번째** 사례다
> (① deny의 집행 조건 ② `systemMessage`의 청중 ③ 프로젝트 슬러그).
> 셋 다 **실행해 보기 전까지는 틀린 줄 몰랐다.**

부수로 판독기의 표시도 고쳤다: 마커를 쓰지 않는 실행(`verify-real-goppi`)에서
"모델 컨텍스트 도달: (없음)"이 **기대된 결과를 음성 발견처럼** 읽히게 했다 —
T-2(다른 세션이 기대된 FAIL을 프로토콜 위반으로 오진)와 같은 계열이라 문구를 갈랐다.

### 10.2 FP-2가 이 세션에서 재현됐다

이 기록을 만드는 도중 **내 명령이 G1에 막혔다.** 인라인 node 코드 안의 `.split(` 이
쓰기 동사로 매칭됐고 같은 명령줄에 하네스 경로가 있었다.
spec §11.1의 *"하네스 자신이 G1의 최악 오탐 환경"* 과 §8.6의 *"§11.1의 '사용자 프로젝트에서는 드물다'가
미실측 안심 문장"* 을 동시에 뒷받침하는 실물이다. 등록부 `known_limits`에 실측으로 기록했다.

---

> ## 🔍 2026-08-24 재검증 (이관 시)
>
> **측정 시점**: Claude Code **v2.1.233** (2026-08-07~18) · **재검증 시점**: **v2.1.241** — 8패치 차이.
>
> **재측정은 하지 못했다.** 훅은 세션 경계에서 로드되므로 진행 중인 세션에서 다시 돌릴 수 없다
> (원 기록도 같은 벽에 부딪혀 사람 관측에 의존했다).
>
> **대신 현행 공식 문서와 대조했다** — 그리고 **본문의 측정 결과와 일치한다**:
> `systemMessage`는 *"the **user** (in the transcript), **not the model**"*,
> `additionalContext`는 *"the **model**"*, *"**stderr is NOT parsed as JSON**"*,
> stdout이 stderr에 우선. **네 항목 모두 본문과 같다.**
>
> ⚠️ **다만 "당시 공식 문서가 틀리게 적고 있었다"는 주장은 재확인할 수 없다.** 현행 문서는 맞게 적고
> 있으므로, ① 당시 틀렸다가 수정됐거나 ② 그 주장 자체가 과했거나 둘 중 하나인데 구분할 근거가 없다.
> **이 문서를 "공식 문서를 뒤집은 기록"으로 인용하지 말 것.** 인용 가능한 것은 *측정된 동작*이고,
> 그것은 현행 문서와 일치한다.
>
> **등급**: 호스트 표면은 🔴(수개월 단위 변동)이다 — `corpus/methods/evidence-durability--grading-model.md` §4.
> 결정이 이 문서에 걸리면 **해당 minor 버전에서 다시 측정**하라.
