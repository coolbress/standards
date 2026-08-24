---
id: aspect-27-ai-harness-archetype--approval-attribution-channels--measured-2026-08
title: "승인 귀속 채널 실측 — 사람 클릭을 증명할 수 있는가"
parent: aspect-27-ai-harness-archetype
kind: evidence
evidence_track: lit
status: draft
language: ko
last_updated: "2026-08-18"
method: "훅의 ask가 승인 창을 보장하는지, 클릭을 증명할 채널이 있는지 실측 탐색. 원본: goppi_final/records/2026-08-18-blocker1-channel-probe.md — 2026-08-24 이관, 본문 무수정."
---

> **이관 기록 (2026-08-24)**: 원본 저장소는 삭제됐다. 이 문서는 **폐기된 하네스가 아니라 호스트(Claude Code)의
> 실제 동작**에 대한 1차 실측이므로 남긴다. 하네스의 계보는 `imported/LINEAGE.md`.
> **재검증 결과는 문서 끝에 있다 — 먼저 읽을 것.**


> 소유자 결정(세션 #11): "다른 증명 채널 실측 탐색" 후 방향 결정. 이 기록은 ① 지금까지의
> 실측 결론 ② 합성 한계 ③ 다음 실물 세션이 돌릴 탐침·재검증 대본.

## 문제 재확인 (Codex BLOCKER 1)

2단계 프로토콜의 승격 산물(`transition_approved`)은 "훅이 ask를 반환한 뒤 호스트가 실행을
허용했고 그 명령이 성공 종료했다"까지만 증명한다. **"사람이 승인 창을 눌렀다"는 증명하지
못한다** — 허용목록·호스트 안전분류가 창 없이 ask를 자동 충족하면 같은 산물이 생긴다.
질문: 호스트가 노출하는 다른 훅 채널로 "창이 실제로 떴다/사람이 결정했다"를 가를 수 있나?

## 실측 결론 (이 세션 · 기존 이벤트 재분석)

### ① permission_request 채널 — **기각 (재확인)**

trial-web의 봉인 승격 3건과 `permission_request` 이벤트를 시각으로 대조:

| 봉인 승격 | 직전 G4 ask 회부 | 동반 permission_request | 소유자 창 관측 |
|---|---|---|---|
| 16:04:28 | 16:04:22 (contract) | 16:04:22.901 ✓ | **창 안 뜸(무창 확정)** |
| 16:22:06 | 16:22:01 (contract) | 16:22:01.719 ✓ | 불확실 |
| 16:27:31 | 16:27:12 (contract) | 16:27:12.414 ✓ | **창 뜸(스크린샷)** |

⇒ **무창 봉인(1차)에도 permission_request가 발화했다.** 따라서 이 이벤트의 발화는 창 표시를
가르지 못한다 — "권한 판정이 일어났다"까지만 의미한다. external-trial.md line 51~56이 이미
"결정 전 이벤트 · 과잉 추론"으로 적었고, 이번 대조가 **무창 사례로 직접 확증**했다.
계측 실측: `permission_request`의 `user_response=null · schema_recognized=false` — 호스트는
결정 결과(허용/거부)를 이 이벤트에 싣지 않는다(입력 키에 응답 필드 없음).

### ② 창을 띄우는 주체 = goppi 훅의 ask가 아니라 `permissions.ask` 규칙 (신호)

3차 유효 봉인의 창 스크린샷이 인용한 것은 **"Permission rule Bash(node …goppi*)"**
(external-trial.md line 93) — goppi PreToolUse 훅의 ask 반환이 아니라 프로젝트
settings.json의 `permissions.ask` 규칙이다. 함의:
- 2단계 프로토콜은 "훅 ask → 창"을 암묵 전제하는데, 실측은 "창을 띄우는 건 permissions.ask
  규칙"이라고 말한다. 훅의 ask 반환만으로 창이 보장되는지는 **여전히 UNVERIFIED**.
- 그리고 `permissions.ask` 규칙은 프로젝트 settings.json에 있어 **G1 보호 밖**이다
  (Codex 특별요청 ② · 평범한 편집으로 제거 가능). 즉 창의 트리거를 에이전트가 지울 수 있다.
- ⚠️ 1차 무창의 근본 원인은 **여전히 미해명**(external-trial.md line 97). 좁혀진 사실:
  같은 문자열이 3차엔 창을 강제했다 → "매칭 불가 확정"은 근거보다 강한 문장이었다(정정됨).

### ③ 합성으로는 더 못 간다

창은 실물 대화상자다. 합성 훅 호출(대조 스위트·재현 스크립트)로는 창을 띄울 수 없어,
"창 발화 채널"을 합성으로 탐색하는 것은 원리적으로 불가능하다. 남은 후보(아래)는 **실물
세션 + 소유자 관측**으로만 검증된다.

## 공식 문서·타 하네스 탐색 (2026-08-18 · 소유자 제안)

출처: SDK permissions 문서(code.claude.com/docs/en/agent-sdk/permissions) · hooks reference
(code.claude.com/docs/en/hooks) · hooks-guide · disler/claude-code-hooks-mastery ·
sd0x-dev-flow · GitHub issue #19298.

### ★ 무창 봉인의 근본 규명 — goppi 2단계 전제가 호스트와 어긋난다

공식 권한 평가 순서(6단계): **① Hooks → ② Deny 규칙 → ③ Ask 규칙 → ④ 권한 모드 →
⑤ Allow 규칙 → ⑥ canUseTool(사람 창)**. 문서 인용:
- **"A hook can deny the call outright or pass it on."** — PreToolUse 훅은 deny(차단) 또는
  pass(넘김)만 확실히 한다. 훅이 반환하는 **ask는 창을 보장하지 않는다** — 아래 규칙 평가로
  넘어갈 뿐이다.
- **"Auto-approved tools never reach canUseTool."** — allow 규칙·acceptEdits·
  bypassPermissions·안전분류가 승인하면 사람 결정 지점(canUseTool=창)에 **도달하지 않는다**.
- 창이 뜨는 경로는 둘뿐: ③ ask 규칙 매칭 → canUseTool, 또는 어느 것도 안 풀려 ⑥ 도달.

⇒ **goppi의 2단계 프로토콜은 "훅이 ask 반환 → 창 → 사람 클릭"을 전제하는데, 호스트에선
훅의 ask가 창을 만들지 않는다.** 창을 만드는 건 ③ ask **규칙**(프로젝트 settings.json ·
G1 밖)이다. 봉인 요청이 allow 규칙/안전분류로 자동 승인되면 창을 건너뛰고 PostToolUse만
발화 → **무창 봉인**. external-trial 실측(3차=ask 규칙이 창 강제 · 1차=규칙 미로드 무창)과
정확히 정합. **이것이 Codex BLOCKER 1의 기계적 원인이다.**

### 타 하네스의 접근 — "사람 클릭 증명"은 아무도 안 풀었다

- **disler/claude-code-hooks-mastery**(대표 훅 예제 모음): PermissionRequest를 "Fires: When
  user is shown a permission dialog"로 **오해**하고 있다. 우리 무창 실측이 이 통념이 틀렸음을
  보였다 — 유명 예제도 이 지점을 정확히 몰랐다.
- **sd0x-dev-flow · autonomous-coding-harness**(하네스 엔지니어링 레퍼런스): 사람 게이트를
  "hook-enforced dual review · state-machine gate · PreToolUse deny · 승인은 워크플로
  체크포인트"로 구현한다. 즉 **auto-approve(안전) + hard-block(위험)** 이분법이거나, Agent
  SDK의 **canUseTool 콜백**으로 결정을 프로그램이 가로챈다. 어느 쪽도 "창을 눌렀다는 사후
  증명"을 시도하지 않는다 — 결정 자체를 코드가 소유한다.
- **Agent SDK canUseTool**: "fires whenever Claude would show a permission prompt … when
  hooks and permission rules don't cover it." 자동승인은 canUseTool에 도달하지 않으므로,
  canUseTool 호출 = 사람 결정 지점 도달이 **보장**된다. 이것이 정확한 게이팅의 정공법이다.
  ⚠️ **단 canUseTool은 Agent SDK 전용이다 — goppi는 CLI 플러그인(훅)이라 못 쓴다.** 이건
  아키텍처 재검토 사안(아래 소유자 결정 (다)).

### 새 후보 채널의 정확한 스펙

- **Notification(matcher=notification_type)** — 전체 값: `permission_prompt` · `idle_prompt` ·
  `auth_success` · `elicitation_dialog/url_dialog/complete/response` · `agent_needs_input` ·
  `agent_completed`. hooks-guide 테스트 절차가 실증: *"Shift+Tab으로 manual 모드 → 권한 필요
  작업 요청 → 데스크톱 알림 수신."* ⇒ **permission_prompt는 창이 뜰 때 발화**한다. 자동승인
  시엔 알림 이유가 없으니 미발화 가설 → permission_request보다 강한 창-표시 신호 후보.
  ⚠️ **결정적 제약: Notification payload에 tool_use_id가 없다**(common fields +
  notification_type뿐). 특정 봉인 요청에 **결속 불가** — "이 세션에서 최근 창이 떴다"는
  시간 신호만 되고, external-trial이 "시간은 판별력 없다"고 이미 적었다.
- **PermissionRequest** — "When a tool call needs a permission decision"(**결정 전**). 무창
  포함 → 기각(재확인). decision object(allow/deny/escalate) 반환은 가능하나 issue #19298에서
  무시 버그 이력.
- **PermissionDenied** — "When **auto mode** denies a tool call"(거부 후 · 거부 결과 실림 ·
  retry:true 반환). auto 모드 자동 거부라 **사람 허용 증명엔 부적합**. 사람이 manual 창에서
  거부한 것도 여기로 오는지는 미확인(실물 검증 항목).

### 종합 판단

호스트가 노출하는 **결속 가능한**(tool_use_id 있는) 채널 중 "창 표시"를 가르는 것은 아직
없다. Notification permission_prompt가 가장 유망하나 결속이 시간 근접뿐이라 약하다. 정공법은
Agent SDK canUseTool인데 CLI 훅에선 불가. ⇒ 실물 탐침으로 Notification permission_prompt의
판별력(자동승인 시 미발화)을 확인하되, 서더라도 결속 약함은 남는다.

## 남은 후보 채널 (claude-code-guide 조사 · 전부 문서 미명시 → 실물 검증 필요)

호스트가 지원하는 훅 이벤트 중 미탐색분: `Notification` · `PermissionDenied` ·
`PostToolUseFailure` · `Elicitation`/`ElicitationResult`. 각 발화 조건은 **공식 문서에
없다**(claude-code-guide n=1 조사). 가설:

- **Notification** — 데스크톱 알림 계열. *만약* 창 표시 시에만 발화하고 자동 허용 시엔
  발화하지 않는다면 창 표시의 양성 신호가 된다. 미검증.
- **PermissionDenied** — *만약* 사람이 거부를 누를 때만 발화한다면, "거부"는 확실한 사람
  행동이다(비대칭 증명 — 허용은 못 증명해도 거부는 증명). 미검증.
- ⚠️ 두 후보 다 "자동 허용 경로에선 발화 안 함"이 성립해야 쓸모가 있다 — 그게 정확히
  permission_request가 실패한 지점이다. 실물 비교시험 없이 채택 금지.

## 다음 실물 세션이 돌릴 대본

### A. 채널 탐침 — "Notification permission_prompt가 창 표시를 가르는가" (소유자 관측 필수)

핵심 가설(공식 문서 기반): **Notification(permission_prompt)은 canUseTool(사람 창)에 도달할
때만 발화하고, allow 규칙/안전분류 자동승인에는 발화하지 않는다.** 참이면 permission_request가
못 한 창-표시 판별을 얻는다(단 결속은 시간 근접뿐).

1. **임시 계측 훅 추가**(프로덕션 gate 훅과 분리 — 별도 스크립트 `probe-hook.mjs`):
   `hooks.json`에 `Notification`(matcher `permission_prompt` 및 전체)·`PermissionDenied`·
   `PostToolUseFailure` 계측 훅을 추가하고 각 발화를 L3에 `probe_hook{event, notification_type,
   input_keys, ts}`로 남긴다(record-permission.mjs의 input_keys 패턴 — tool_use_id 유무를
   특히 확인). ⚠️ 계측 훅은 프로덕션 gate와 **분리** — 이 세션의 게이트 동작을 안 바꾼다.
2. **세 경로를 실행하고 소유자가 창 유무를 관측**(누르기 전 스크린샷):
   - (a) **창 뜨는 경로**: `permissions.ask`에 정확 매칭되는 봉인 요청. → 허용.
   - (b) **자동 허용 경로**: `permissions.allow`에 넣은 무해 명령, 또는 안전분류가 자동 통과할
     명령(예: `ls`). 창 안 뜸.
   - (c) **거부 경로**: (a)를 소유자가 창에서 **거부**. PermissionDenied가 사람 거부를 잡나?
3. **비교표**: 각 경로에서 발화한 훅·notification_type을 대조. `permission_prompt`가 (a)에만
   뜨고 (b)엔 안 뜨면 → 창-표시 판별력 있음.
4. **판별 기준**: `permission_prompt`가 무창 자동승인(b)에서 **발화하지 않음**을 실측해야 채택.
   하나라도 (b)에서 발화하면 permission_request와 같은 운명(기각). 채택하더라도 **tool_use_id
   결속 부재**는 남는 약점 — 승격 조건에 넣으려면 "직전 Bash 요청 후 N초 내 permission_prompt"
   같은 시간 근사가 최선이고, external-trial이 시간의 판별력 없음을 이미 지적했다.
5. **자동승인 경로의 정체 규명**(무창 원인 확정): 봉인 요청이 (b)를 타는 이유가 안전분류인지
   allow 규칙인지 확인 — 무창 세션에서 `permission_mode`·매칭 규칙을 L3로 관측하고, ask 규칙을
   정확 매칭으로 고정했을 때 무창이 사라지는지(3차 재현). 사라지면 원인=규칙 미매칭, 아니면
   안전분류가 훅 ask를 삼키는 것.

### B. 실물 호스트 재검증 — 수리본(rev5)이 실제 설치 산물에서 서는가

⚠️ **현재 캐시는 구버전이다.** 캐시 사본(`~/.claude/plugins/cache/goppi-local/goppi/0.1.0`)에
`classifyRequestCommand`가 없다(개수 0) — 이 세션의 봉인도 구버전 훅이 처리했다. `marketplace
update`는 메타데이터만 검증하고 파일 캐시를 갱신하지 않았다(디렉토리 mtime 불변).

**이 세션에서 완료한 부분 (실측):**
1. ✅ plugin.json 버전 0.1.0 → **0.1.1**. `claude plugin install goppi@goppi-local`로
   재설치 → 캐시에 `0.1.1/` 생성. `grep -c classifyRequestCommand`: 0.1.1=1, 0.1.0=0 —
   **수리본이 실제 설치 산물로 캐시에 들어감** 확인.
2. ✅ **실제 설치 산물(0.1.1 캐시)에 대한 공격 4종 재현 = 0/4** (전부 차단). 저장소 소스가
   아니라 캐시 경로를 겨냥한 사본으로 실행 — 실물 설치 코드가 취약하지 않음을 실측.
   (단 이것도 훅을 execFileSync로 직접 호출하는 **합성**이다 — 호스트가 훅을 발화시키는
   완전 통합은 아니다.)

**현재 세션 훅 버전 — 우연히 확정 (실물 신호):**
3. ✅ **현재 세션 훅이 이미 수리본(0.1.1)으로 갱신됨.** 재봉인 요청 중 실측: `cd … ; node …`
   형태의 봉인 요청이 `decision=deny reason=grammar`(허용되지 않는 문자 ';')로 거부됐다
   (09:18:23Z L3 이벤트). 이는 `classifyRequestCommand`의 문법 검사가 **실제 세션 훅으로
   발화**했다는 실증 — 구버전(0.1.0)의 `requestKindOf`엔 문법 검사가 없다. 즉 이 세션의
   `claude plugin install` 재설치가 현재 세션 훅에도 반영됐다(재시작 없이). 세미콜론을 뺀
   단일 명령은 문법을 통과했고, 그다음 모드 가드(`mode=acceptEdits ≠ default`)에서 deny —
   fail-closed 정상. ⇒ **rev5 grammar·모드가드가 실물 세션 훅으로 작동함**(합성 대조 + 실물
   단발 관측 일치).

**다음 실물 세션이 완료할 부분:**
4. trial-web에서 **공격 4종을 실물 호스트로 재현**: 문자열 언급(ATK1)·복합 명령·실패 실행·
   TOCTOU·세션 불일치가 실제 설치본에서 봉인을 못 만드는지. + 정상 경로는 여전히 통과하는지.
   (봉인 요청은 소유자 창 관측 — B 대본과 합쳐 실행.)
5. **프로젝트 ask 규칙 삭제 공격**(Codex 특별요청 ② · BLOCKER급): settings.json의
   permissions.ask를 지운 뒤 봉인 요청 시 창이 뜨는지/승격되는지 — 창의 트리거가 규칙에만
   있다면 삭제 후 무창 자동충족이 재현될 것이다(호스트 통합시험 · A 대본 ②-(b)와 연결).

## 부수 발견 — negative-control M1 격리 결함 (이 세션 수리)

실물 재검증으로 `claude plugin install goppi@goppi-local`(기본 scope=user)를 실행하자,
**사용자 홈 `~/.claude/settings.json`의 enabledPlugins에 goppi가 추가**됐다(원래 없던 것 —
프로젝트 레벨에만 있었다). 그 직후 negative-control의 M1(미설치)이 깨졌다: 기대 INSTALL
FAIL인데 실제 LOG-PERM WARN.

원인: `check-install.mjs:61`의 `checkInstalled`는 설치 확인 후보로 **실제 사용자 홈**
(`join(homedir(), ".claude", "settings.json")`)을 포함한다(프로덕션에선 옳다). 그런데
`negative-control.mjs`의 `runVerifier`가 HOME을 격리하지 않고 `...process.env`를 그대로
넘겨, M1이 fixture 프로젝트 settings를 비워도 실제 사용자 홈에서 goppi가 발견돼 INSTALL
PASS가 났다. **검사가 저장소 밖 상태에 오염되는 격리 결함** — "미설치를 잡는다"는 주장이
사용자 홈에 goppi가 있으면 거짓이 된다.

수리: `runVerifier`의 env에 `HOME: root`를 고정 — 후보 3이 fixture 안(후보 1과 동일 파일)을
가리켜 픽스처가 심은 상태만 본다. 검증: 사용자 홈에 goppi를 다시 넣은 오염 상태에서도
negative-control 17/17 유지(격리 전이면 M1이 깨졌을 상황). install이 남긴 사용자 홈 항목은
원복함(codex는 유지).

⚠️ 교훈: 실물 install은 **사용자 홈 설정을 바꾼다**(scope=user 기본). 다음 실물 재검증 때도
같은 부작용이 생기니, 검사 격리(HOME 고정)가 방어선이다.

## 소유자에게 (방향 결정 재료)

지금까지의 실측 + 공식 문서 탐색이 가리키는 정직한 그림: **호스트 위에서 "사람이 눌렀다"를
CLI 훅으로 결속해 증명할 확실한 채널은 없다.** 근거가 두 겹으로 굳었다 — ① permission_request는
무창에도 발화(실측) ② 훅의 ask는 창을 만들지 않고, 자동승인은 canUseTool(사람 창)에 도달하지
않는다(공식 문서). 결속 가능한 창-표시 신호가 호스트 훅 표면에 없다. 세 갈림길:
- **(가) 실물 탐침으로 Notification permission_prompt 검증** — 소유자가 화면 앞에서 A 대본
  실행. 자동승인 시 미발화면 창-표시 판별을 얻는다. **단 tool_use_id 결속이 없어**(payload에
  부재) 시간 근사에 그친다 — 강한 증명은 아니다. 서면 보조 신호로 추가, 안 서면 (나).
- **(나) "이 경계는 원리적으로 협조 위에 선다"를 정직 고지로 확정** — 차단 회로만 GO로
  분리하고, 사람 증명은 승인 창 관측(소유자 확인)으로만 성립함을 L0/등록부에 못박는다.
  rev5가 이미 승격 산물의 의미를 강등했다 — (나)는 그것을 최종 상태로 받는 것. **문서 탐색이
  (나)를 지지한다**: 유명 하네스도 사람 클릭을 사후 증명하지 않고 결정을 코드가 소유한다.
- **(다) 아키텍처 재검토 — Agent SDK canUseTool** — "자동승인은 canUseTool에 도달하지 않는다"가
  보장하는 유일한 정확 게이팅. 하지만 goppi는 CLI 플러그인(훅)이라 못 쓴다 — 하네스 실행 형태를
  SDK 앱으로 바꾸는 큰 방향 전환이고, "솔로 오너가 CLI에서 쓴다"는 전제와 충돌. 별도 트랙.

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
