---
id: aspect-27-ai-harness-archetype--pretool-ask-exit-codes--measured-2026-08
title: "PreToolUse ask의 exit code 동작 실측"
parent: aspect-27-ai-harness-archetype
kind: evidence
evidence_track: lit
status: draft
language: ko
last_updated: "2026-08-17"
method: "exit 2가 승인 대화상자를 죽이는 현상을 3회 재현·계측으로 특정하고 수리. 원본: goppi_final/records/2026-08-17-pretool-ask-exit-code-fix.md — 2026-08-24 이관, 본문 무수정."
---

> **이관 기록 (2026-08-24)**: 원본 저장소는 삭제됐다. 이 문서는 **폐기된 하네스가 아니라 호스트(Claude Code)의
> 실제 동작**에 대한 1차 실측이므로 남긴다. 하네스의 계보는 `legacy/LINEAGE.md`.
> **재검증 결과는 문서 끝에 있다 — 먼저 읽을 것.**


> **증상**: default 모드에서 봉인 요청(`approve-contract-request.mjs`)을 3회 실행 —
> 게이트는 3회 전부 `decision=ask`를 정확히 발화했는데(L3 `gate_fired` 13:46:54 ·
> 13:47:45 · 13:50:43, 각각 tool_use_id·nonce 기록), **승인 대화상자는 한 번도 뜨지
> 않았다**(소유자 관측 n=1 — AskUserQuestion으로 확인). 에이전트에게는
> `PreToolUse:Bash hook error: … 사람 승인이 필요합니다`가 즉시 돌아왔다.
> 호스트: Claude Code 2.1.233.

## 원인 — exit 2에서 PreToolUse의 stdout JSON은 버려진다

`respondPreTool`(`harness/goppi/scripts/lib/harness.mjs`)이 ask 판정 JSON을 stdout에
쓰고 **`process.exit(2)`로 종료**했다. 현 호스트의 PreToolUse 처리:

- **exit 2** → stdout JSON **무시** · stderr를 차단 오류로 모델에게 반환 · **대화상자 없음**
- **exit 0 + stdout JSON(`permissionDecision:"ask"`)** → 정상 회부(대화형이면 대화상자)

주석의 기대("stderr는 대체 경로. stdout이 읽히면 무시된다" — 2026-08-08 관측)는
현 호스트의 ask에 성립하지 않는다.

## 교차 증거 — 우리 실측 안에 답이 이미 있었다

| 증거 | 내용 |
|---|---|
| E2 탐침 `tprobe.mjs:49` | ask를 **exit 0**으로 냈고 — 헤드리스 전 모드에서 정상 "회부 처리"됨(E2 실측표) |
| E1 실측 "exit 2 + stdout JSON 집행" | **Stop 훅 한정**의 실측이었다. PreToolUse로 과일반화된 채 §1.3.3에 반영 |
| git 이력 (`735d6ea`→`e27704c`→`433f5c2`) | baseline은 stdout+exit 0 → 조각 1에서 stderr+exit 2 → 8/08 수리 때 stdout 복귀·**exit 2 잔존** |
| 오늘 실전 n=3 | ask 발화 3회 전부 대화상자 없이 hook error로 사망 |

**P20 계열**: 탐침(측정)과 제품(집행)이 다른 exit 코드를 쓰고 있었고, Stop의 실측을
PreToolUse에 옮겨 적으면서 아무도 갈라 보지 않았다. 문서와 실측이 갈리면 실측이 이긴다 —
그리고 실측끼리 갈리면 **해당 이벤트의 실측**이 이긴다.

## 수리 (커밋 참조)

1. **`harness/goppi/scripts/lib/harness.mjs`** — `respondPreTool`: **ask는 exit 0**,
   deny는 exit 2 유지(차단은 exit 2로도 성립 · 전 대조가 catch 경로에서 판정을 읽음).
   ⚠️ 대가: ask는 stdout 파싱 실패 시 무판정 통과(fail-open) — 형태 단언(아래 3)이 그 빈틈을 지킨다.
2. **`harness/verify/gate-control.mjs`** — `call()` 성공 경로(exit 0)에서도 stdout 판정 파싱.
   **변이 확인**: harness.mjs 수리 직후·control 수리 전 실행 → **G2 ask 4케이스가 정확히 빨강**
   (25건 중 4건 FAIL) → control 수리 후 25/25 초록. 검사의 적발력 증명.
3. **`harness/verify/output-surface-control.mjs`** — 형태 계약을 판정별로 분리
   (deny=EXIT2+STDERR-FALLBACK · ask=EXIT0·대체경로 없음) + 음성 변이 **X8-ask가exit2** 신설.
4. 전체 스위트: `run-all-controls.sh` 10종 전부 PASS (수리 중간에 output-surface가
   정확히 FAIL을 냈다 — 이 대조 역시 살아 있음을 실증).

## 계약 영향

`gate-control.mjs`는 AC-2의 check_files 고정 대상 → 해시 갱신 + check_id
**T-G2-ASK-v3 → v4** (changePolicy에 따라 소유자 승인 필요 — 본 세션에서 회부).
`harness.mjs`·`output-surface-control.mjs`는 고정 대상 아님(judgeNote의 기지 공백).

## 남는 것 (정직 표기)

- ~~exit 0 + JSON ask의 실물 대화상자는 `UNVERIFIED`~~ →
  **❌ 반증됨 (2026-08-17 14:47 · 소유자 스크린샷 n=1) — 대화상자는 뜨지 않았다.**
  14:29 봉인 후 이 파일의 이전 판은 "대화상자가 떴고 소유자가 승인 클릭"이라고
  적었다 — **그것은 명령이 실행됐다는 사실에서의 과잉 추론이었다**(근거보다 강한
  문장 금지 위반 · 같은 세션 안에서 자체 적발). 소유자가 "누른 기억이 없다"고
  이의 제기 → 지켜보는 재관측(14:47) → 스크린샷: 창 없이 즉시 실행,
  `∟ PreToolUse:Bash says:` 한 줄만 렌더링.
  **원인 — 판별 실험으로 확정 (2026-08-17 15:01)**: 전역 허용 목록
  `Bash(node:*)`(~/.claude/settings.json)가 훅 ask를 **창 없이 자동 충족**한다.
  판별 실험: 비허용목록 명령 `stripe products create`(G2-BILLING ask) →
  **창이 실제로 떴고**(소유자 스크린샷 — goppi G2 승인 화면 전문: 회부 사유 ·
  복원 상태 SR-02 필드 · "판단하실 것" 렌더링, **G2 승인 화면의 첫 실전 관측**) →
  소유자 결정까지 24초. 반면 허용목록 매칭 봉인 명령은 요청→실행 1.6초 · 창 없음.
  `permission_request` 이벤트는 **양쪽 다** 발화(자동 승인되는 AskUserQuestion에도
  발화 확인) — 창 표시의 증거가 못 된다(결정 전 이벤트라는 기존 실측과 정합).
  **귀결: 14:29·14:47 두 봉인 모두 사람 증명이 없다 — 2단계 프로토콜의 사람
  증명은 "허용 목록에 안 맞는 명령"일 때만 성립할 수 있고, 이는 아직 미관측이다.**
  모드 가드의 정확한 거부(auto 3회 + acceptEdits 2회)는 유효한 관측으로 유지.
  systemMessage의 `says:` 렌더링은 ask 경로에서도 확인(스크린샷 n=1 — 단 이것은
  통보이지 승인이 아니다).

## 수리 2 — 프로젝트 ask 규칙이 허용 목록을 이긴다 (2026-08-17 15:05 실측)

프로젝트 `.claude/settings.json`에 `permissions.ask` 3규칙 추가
(approve-contract-request · skip-request · hold-transition — goppi 요청 명령 전부).
직후 봉인 재요청 실측:

- **창이 떴다** — 전역 `Bash(node:*)` allow에도 불구하고 (프로젝트 ask > 사용자 allow)
- 설정 변경은 **재시작 없이 즉시 적용**됐다
- 소유자가 내용을 읽고 승인 — 요청→실행 **7.4초**(사람 결정 간격) →
  `transition_approved` 15:05:00 · nonce `1a8e953d…` · digest `964fd574…`
- **⇒ 이 봉인이 사람 증명이 성립한 첫 봉인이다** (14:29·14:47은 자동 승인 산물)

### 한계 (정직 표기)

- ask 규칙은 **협조 위에 선다** — 에이전트가 settings.json을 편집해 지울 수 있다
  (G1 보호 대상 아님). `/plugin` off와 같은 경계 등급.
- **플러그인은 권한 규칙을 실어 나르지 못한다** — 외부 프로젝트(확증시험 ③)에서는
  ask 3규칙을 **손으로 추가**해야 사람 증명이 성립한다. 설치 절차·known_limits에 반영 필요.
- 사용자의 전역 `Bash(node:*)`는 매우 넓은 규칙이다(모든 node 스크립트 무프롬프트).
  goppi와 무관하게 정리를 권고했다 — 결정은 소유자 몫.
- 승인 피로는 실전 재관측됐다(14:29 무의식 클릭 스트림 · "이 세션 동안 허용" 선택이
  모드를 acceptEdits로 옮기는 부수 경로 2회) — DESIGN §1.6 **Q5의 첫 현장 증거**.
- G2의 ask(자격증명·프로덕션·도메인·과금)도 같은 경로로 죽어 있었을 가능성이 크다 —
  8/08 이후 대화형 G2 승인 프롬프트의 실물 관측 기록이 없다면, 이번 수리가 G2 실효의
  복구이기도 하다. 사용자 대면 관측은 다음 G2 발화 때 자연 확인.
- 2026-08-08 `user-channel-render-verdict`(PreToolUse says: 렌더링 n=1)는 당시 호스트
  기준의 관측이다. 현 호스트에서 exit 2 경로의 systemMessage 렌더링은 재관측 전까지
  그 범위를 신뢰하지 않는다.

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
