# 하네스 제거 실행 기록 — 2026-08-24 (2차)

> **이 문서는 정정이다.** 같은 날 앞서 커밋된 *"홈에 하네스 0건"* (#28)은 **틀렸다.**
> 그 주장 이후 홈을 **종류로** 다시 훑어 잔재 **5종류**를 더 찾았고, 그것들을 처분한 기록이다.
> 선례는 [`harness-removal-record-2026-08-04.md`](harness-removal-record-2026-08-04.md)이며,
> **그 선례가 남긴 교훈이 그대로 재발했다** — 아래 §문서 가정과 실제의 차이.

## 왜 2차가 필요했나

1차 정리는 `~/Archive/harness-removal-2026-08-24/POST-SESSION-CLEANUP.sh` 로 끝났다.
그 스크립트는 `~/.claude.json` 의 **세 곳**(`pluginUsage` · `githubRepoPaths` · `projects` 고아)만 훑고
*"하네스 잔재: 0건 ✓"* 을 출력한다. 그 출력은 **스크립트가 본 범위 안에서만** 참이었다.

실제로 훑어야 할 표면은 여덟 곳이었다.

## 무엇이 남아 있었나

| # | 잔재 | 정체 | 처분 |
|---|---|---|---|
| 1 | `~/.goppi-harness/` (2.5MB) | 하네스 **런타임 집행 이벤트 대장** — `events/` 21개 `.jsonl`(L3-EXEC 로그) · `quarantine/` · `state/` | **아카이브 이동** |
| 2 | `~/Agent Harness/하네스란 무엇인가.md` (33KB) | 2026-07-14 작성. 저장소 [`sources/goppi/what-is-a-harness.md`](../sources/goppi/what-is-a-harness.md)에 **이미 승계된 중복본** | **아카이브 이동** |
| 3 | `plugins/known_marketplaces.json` → `goppi-local` | 사라진 `goppi_final/harness` 를 가리키는 **죽은 마켓플레이스 정의**. 1차 스크립트는 이것을 소비하는 `pluginUsage` 만 지우고 **정의는 남겼다** | **제거** |
| 4 | `plugins/data/` 5개 | `goppi-goppi` · `goppi-goppi-local` · `goppi-inline` · `outprobe-inline` · `transition-probe-inline` (전부 0B) | **삭제** |
| 5 | `~/.claude/settings.json.bak-goppi11` (6.1KB) | goppi 시대 `settings.json` 백업 — 당시 훅 구성이 담긴 유일한 사본 | **아카이브 이동** |
| 6 | `.claude.json` → `githubRepoPaths` 고아 1건 | `coolbress/harness-phase2-sandbox-20260525-105700` → `/private/tmp/…` (부재) | **제거** |
| 7 | `~/.claude.json` `pluginUsage`·`projects` 3건 | 1차 스크립트가 잡은 것 (`goppi@goppi-local` · `goppi_final` · `goppi_test`) | **제거** |
| 8 | `~/.claude/projects/` 89개 (244.9MB) | **세션 대화 로그** — 아래 별도 절 | **문서화 후 삭제** |

### 검증

- **1·5는 삭제가 아니라 이동이다.** `~/Archive/harness-removal-2026-08-24/` 아래
  `goppi-harness-runtime-state/` · `Agent-Harness-home-copy/` · `settings.json.bak-goppi11`.
- `.goppi-harness` 는 **죽은 데이터임을 확인하고** 옮겼다: 살아있는 설정
  (`settings.json` · `.zshrc` · `.codex/config.toml`)에서 참조 **0건**, 이후 쓰기 **0건**.
  마지막 쓰기(17:35)는 종료된 goppi_final 세션의 exec 기록이었다.
- **손대지 않은 것**: `settings.json` 의 permissions · model · herdr 훅 · skillOverrides.
  herdr는 하네스가 아니다 (2026-08-04 선례가 orca 훅을 남긴 것과 같은 판단).

## 문서 가정과 실제의 차이 — **선례의 교훈이 그대로 재발했다**

[2026-08-04 기록](harness-removal-record-2026-08-04.md)이 남긴 문장은 이것이었다:

> **제거 절차를 문서만 보고 짜면 안 되고 실제 상태를 먼저 조회해야 한다.**

2026-08-24 1차 정리는 그 교훈을 **스크립트에 넣지 못했다.** `POST-SESSION-CLEANUP.sh` 는
*"하네스는 `.claude.json` 세 곳에 산다"* 는 **가정을 코드로 굳혔고**, 그 가정이 참인지는
검사하지 않았다. 그리고 스스로 *"잔재 0건 ✓"* 을 출력해 **가정을 확증으로 보이게 했다.**

이것은 코퍼스가 이미 가진 명제의 실례다 — *"green ≠ 증거"*, 그리고
*"초록 체크는 요구가 충족됐다는 증명이 아니라 **설정된 검사가 통과했다**는 증명일 뿐이다"*
([`05 github-workflow-current`](../../corpus/aspects/05-scm-workflow/github-workflow-current.md) §Do not infer).

**하네스가 자기 시험만 통과한 것과 같은 형태다** — goppi가 합성 공격 0/4를 막고
실사용 11건에 침묵한 것, 그리고 [`direction/04`](../../direction/04-the-plan.md) *완료의 정의*가
경계하는 바로 그것.

### 재발 9번

*"없다"* 고 단정한 것이 틀린 사례가 하나 더 늘었다.
[`direction/02`](../../direction/02-why-past-attempts-failed.md) §진단의 진단 전수표에 **9번**으로 오른다.
8번(codex-native 누락)과 **같은 주에, 같은 종류로** 났다.

정정 계기도 같다 — 소유자가 *"이거 안 되는데"* 를 지적했고,
[README 절대규칙 7](../../README.md)대로 **좌표가 아니라 종류를 훑어서** 나왔다.
좌표만 고쳤으면(=`bash` 로 스크립트를 돌려주고 끝냈으면) 5종류는 그대로 남았다.

## 세션 대화 로그 처분 (#8)

`~/.claude/projects/` 의 하네스 계보 디렉터리 **89개 · 세션 316개 · 244.9MB**
(2026-07-23 ~ 2026-08-24). 88개가 goppi 계보이고, 나머지 하나 `-Users-coolbress-gingoa` 는
**세션 0개의 빈 디렉터리**다 — gingoa 세대는 이 디렉터리 형식보다 앞서 실제 대화가 남지 않았다.
claudeck·claudeck-v1은 아예 없다.

> 이 문장의 첫 판은 *"전부 goppi 계보이고 gingoa·claudeck은 없다"* 였다. **틀렸다** —
> 전수표 마지막 행이 gingoa였다. 요약을 먼저 쓰고 전수를 나중에 붙이면 이렇게 된다.
> 이 문서가 다루는 실패의 축소판이라 지우지 않고 남긴다.

| 묶음 | 디렉터리 | 세션 | 크기 |
|---|---:|---:|---:|
| goppi_final 본체 | 1 | 140 | 96.7MB |
| goppi 본체 | 1 | 57 | 85.3MB |
| goppi_test (LedgerLens 레거시) | 1 | 11 | 58.7MB |
| 하네스 eval 실행 팔(arm)·프로브 작업본 | 84 | 103 | 2.9MB |
| goppi-trial-web (확증시험) | 1 | 5 | 1.3MB |
| 기타 하위 작업본 | 1 | 0 | 0.0MB |

### 처분: **삭제**

**근거 세 가지.**

1. **근거 사슬을 끊지 않는다.** 코퍼스의 실측 문서 6건
   ([`hook-output-surfaces`](../../corpus/aspects/27-ai-harness-archetype/hook-output-surfaces--measured-2026-08.md) ·
   [`pretool-ask-exit-codes`](../../corpus/aspects/27-ai-harness-archetype/pretool-ask-exit-codes--measured-2026-08.md) ·
   [`stop-event-rendering`](../../corpus/aspects/27-ai-harness-archetype/stop-event-rendering--measured-2026-08.md) ·
   [`user-channel-rendering`](../../corpus/aspects/27-ai-harness-archetype/user-channel-rendering--measured-2026-08.md) ·
   [`approval-attribution-channels`](../../corpus/aspects/27-ai-harness-archetype/approval-attribution-channels--measured-2026-08.md) ·
   [`harness-self-threat-model`](../../corpus/aspects/27-ai-harness-archetype/harness-self-threat-model--2026-07.md))이
   원자료로 가리키는 것은 **명령 출력과 `.goppi-harness/events/`** 이지 이 대화 로그가 아니다.
   **삭제 전에 전수 확인했다.** 그리고 `.goppi-harness` 는 삭제가 아니라 보존이다(#1).
2. **처분 종류가 이미 확정돼 있다.** 84개 디렉터리는 하네스 eval 실행 팔·프로브의 작업본이고,
   [`DISPOSITION.md`](../DISPOSITION.md)가 그 계열을 **폐기 · 하네스 효과 n=1** 로 이미 판정했다.
   본체 3개(goppi · goppi_final · goppi_test)의 **산출물**은 `~/Archive/`(1.1GB)에 보존돼 있다 —
   사라지는 것은 그것을 만든 **대화**지 산출물이 아니다.
3. **소유자 결정.** 2026-08-24, *"standards 폴더의 적절한 곳에 문서화를 하고 제거"*.

### 되돌릴 수 없다

이 절이 남는 유일한 기록이다. 아래가 **삭제된 것의 전수**다.

<details>
<summary>전수 89개</summary>

| 디렉터리 | 세션 | 크기 | 기간 |
|---|---:|---:|---|
| `-Users-coolbress-goppi-final` | 140 | 96.67MB | 2026-08-02~2026-08-24 |
| `-Users-coolbress-goppi` | 57 | 85.33MB | 2026-07-23~2026-08-12 |
| `-Users-coolbress-goppi-test` | 11 | 58.70MB | 2026-08-19~2026-08-24 |
| `-Users-coolbress-goppi-trial-web` | 5 | 1.32MB | 2026-08-18~2026-08-19 |
| `-private-tmp-claude-501--Users-coolbress-goppi-final-651290a8-838c-4f05-9419-60bdf079fe8a-scratchpad-childcwd` | 10 | 0.32MB | 2026-08-07~2026-08-07 |
| `-Users-coolbress-goppi-final-harness-probe-transition-probe--work-childcwd` | 7 | 0.23MB | 2026-08-17~2026-08-17 |
| `-private-tmp-claude-501--Users-coolbress-goppi-06422959-dbf9-42e3-80f5-abd62e6e396c-scratchpad-revbench-vanilla` | 1 | 0.11MB | 2026-07-26~2026-07-26 |
| `-private-tmp-claude-501--Users-coolbress-goppi-dfd1ee83-4d39-4995-8052-2474a14955e4-scratchpad-pair2-S` | 1 | 0.10MB | 2026-07-30~2026-07-30 |
| `-private-tmp-claude-501--Users-coolbress-goppi-06422959-dbf9-42e3-80f5-abd62e6e396c-scratchpad-run3-arm-kickoff` | 1 | 0.10MB | 2026-07-25~2026-07-25 |
| `-private-tmp-claude-501--Users-coolbress-goppi-1f3e1bec-0645-40d3-b395-d5e65cb313de-scratchpad-kickoff-arm-kickoff` | 1 | 0.09MB | 2026-07-25~2026-07-25 |
| `-private-tmp-claude-501--Users-coolbress-goppi-1f3e1bec-0645-40d3-b395-d5e65cb313de-scratchpad-kickoff-arm-contract` | 1 | 0.09MB | 2026-07-25~2026-07-25 |
| `-private-tmp-claude-501--Users-coolbress-goppi-06422959-dbf9-42e3-80f5-abd62e6e396c-scratchpad-run3` | 2 | 0.08MB | 2026-07-25~2026-07-25 |
| `-private-tmp-claude-501--Users-coolbress-goppi-1f3e1bec-0645-40d3-b395-d5e65cb313de-scratchpad-kickoff` | 2 | 0.08MB | 2026-07-25~2026-07-25 |
| `-private-tmp-claude-501--Users-coolbress-goppi-06422959-dbf9-42e3-80f5-abd62e6e396c-scratchpad-run3-judge` | 1 | 0.08MB | 2026-07-25~2026-07-25 |
| `-private-tmp-claude-501--Users-coolbress-goppi-1f3e1bec-0645-40d3-b395-d5e65cb313de-scratchpad-kickoff-judge` | 1 | 0.07MB | 2026-07-25~2026-07-25 |
| `-private-tmp-claude-501--Users-coolbress-goppi-06422959-dbf9-42e3-80f5-abd62e6e396c-scratchpad-revbench-harness` | 1 | 0.07MB | 2026-07-26~2026-07-26 |
| `-Users-coolbress-goppi-final-harness-probe--work-childcwd` | 2 | 0.06MB | 2026-08-08~2026-08-08 |
| `-private-tmp-claude-501--Users-coolbress-goppi-dfd1ee83-4d39-4995-8052-2474a14955e4-scratchpad-pair-S` | 1 | 0.06MB | 2026-07-30~2026-07-30 |
| `-private-tmp-claude-501--Users-coolbress-goppi-06422959-dbf9-42e3-80f5-abd62e6e396c-scratchpad-run3-arm-strengthened` | 1 | 0.06MB | 2026-07-25~2026-07-25 |
| `-private-tmp-claude-501--Users-coolbress-goppi-dfd1ee83-4d39-4995-8052-2474a14955e4-scratchpad-pair-C` | 1 | 0.06MB | 2026-07-30~2026-07-30 |
| `-private-tmp-claude-501--Users-coolbress-goppi-dfd1ee83-4d39-4995-8052-2474a14955e4-scratchpad-pair2-C` | 1 | 0.05MB | 2026-07-30~2026-07-30 |
| `-private-tmp-claude-501--Users-coolbress-goppi-1f3e1bec-0645-40d3-b395-d5e65cb313de-scratchpad-gate-A-old` | 1 | 0.04MB | 2026-07-25~2026-07-25 |
| `-private-tmp-claude-501--Users-coolbress-goppi-1f3e1bec-0645-40d3-b395-d5e65cb313de-scratchpad-gate-C-diag-new` | 1 | 0.03MB | 2026-07-25~2026-07-25 |
| `-private-tmp-claude-501--Users-coolbress-goppi-1f3e1bec-0645-40d3-b395-d5e65cb313de-scratchpad-gate-C-fix-new` | 1 | 0.03MB | 2026-07-25~2026-07-25 |
| `-private-tmp-claude-501--Users-coolbress-goppi-1f3e1bec-0645-40d3-b395-d5e65cb313de-scratchpad-gate-C-fix-old` | 1 | 0.03MB | 2026-07-25~2026-07-25 |
| `-private-tmp-claude-501--Users-coolbress-goppi-d6e5f837-01d4-4841-a75d-fd6f8b7d4802-scratchpad-pair-false-completion-harness` | 1 | 0.03MB | 2026-07-25~2026-07-25 |
| `-private-tmp-claude-501--Users-coolbress-goppi-1f3e1bec-0645-40d3-b395-d5e65cb313de-scratchpad-gate-A-new` | 1 | 0.03MB | 2026-07-25~2026-07-25 |
| `-private-tmp-claude-501--Users-coolbress-goppi-1f3e1bec-0645-40d3-b395-d5e65cb313de-scratchpad-gate-C-diag-old` | 1 | 0.03MB | 2026-07-25~2026-07-25 |
| `-private-tmp-claude-501--Users-coolbress-goppi-d6e5f837-01d4-4841-a75d-fd6f8b7d4802-scratchpad-pair-false-completion-vanilla` | 1 | 0.03MB | 2026-07-25~2026-07-25 |
| `-private-tmp-claude-501--Users-coolbress-goppi-c503403c-bd2b-4275-9c1a-c70fa8dbf61c-scratchpad-m4-scaffold` | 2 | 0.03MB | 2026-07-26~2026-07-26 |
| `-private-var-folders-rv-7p9kr9gj6952vjs-1sb308fc0000gn-T-goppi-arm-5Ao9FY` | 1 | 0.03MB | 2026-08-08~2026-08-08 |
| `-private-var-folders-rv-7p9kr9gj6952vjs-1sb308fc0000gn-T-goppi-arm-fiiXwy` | 1 | 0.03MB | 2026-08-08~2026-08-08 |
| `-private-var-folders-rv-7p9kr9gj6952vjs-1sb308fc0000gn-T-goppi-arm-EadXG8` | 1 | 0.03MB | 2026-08-08~2026-08-08 |
| `-private-var-folders-rv-7p9kr9gj6952vjs-1sb308fc0000gn-T-goppi-arm-XoXXEx` | 1 | 0.03MB | 2026-08-08~2026-08-08 |
| `-private-var-folders-rv-7p9kr9gj6952vjs-1sb308fc0000gn-T-goppi-arm-xXde5k` | 1 | 0.03MB | 2026-08-08~2026-08-08 |
| `-private-tmp-claude-501--Users-coolbress-goppi-dfd1ee83-4d39-4995-8052-2474a14955e4-scratchpad-probe` | 1 | 0.02MB | 2026-07-30~2026-07-30 |
| `-private-var-folders-rv-7p9kr9gj6952vjs-1sb308fc0000gn-T-goppi-arm-SPlrR8` | 1 | 0.02MB | 2026-08-08~2026-08-08 |
| `-private-var-folders-rv-7p9kr9gj6952vjs-1sb308fc0000gn-T-goppi-arm-PjWmTj` | 1 | 0.02MB | 2026-08-08~2026-08-08 |
| `-private-var-folders-rv-7p9kr9gj6952vjs-1sb308fc0000gn-T-goppi-arm-j0cjcE` | 1 | 0.02MB | 2026-08-08~2026-08-08 |
| `-private-var-folders-rv-7p9kr9gj6952vjs-1sb308fc0000gn-T-goppi-arm-2dTJ7w` | 1 | 0.02MB | 2026-08-08~2026-08-08 |
| `-private-tmp-claude-501--Users-coolbress-goppi-1f3e1bec-0645-40d3-b395-d5e65cb313de-scratchpad-m1-ctrskills` | 1 | 0.02MB | 2026-07-25~2026-07-25 |
| `-private-tmp-claude-501--Users-coolbress-goppi-d6e5f837-01d4-4841-a75d-fd6f8b7d4802-scratchpad-g5-m3` | 1 | 0.02MB | 2026-07-25~2026-07-25 |
| `-private-tmp-claude-501--Users-coolbress-goppi-d6e5f837-01d4-4841-a75d-fd6f8b7d4802-scratchpad-probe-claude` | 1 | 0.02MB | 2026-07-25~2026-07-25 |
| `-private-tmp-claude-501--Users-coolbress-goppi-06422959-dbf9-42e3-80f5-abd62e6e396c-scratchpad-m4-scaffold-rev2` | 1 | 0.01MB | 2026-07-25~2026-07-25 |
| `-private-tmp-claude-501--Users-coolbress-goppi-8d3445a7-8f2a-4036-a349-71a5fe0ed7af-scratchpad-m4run3-kickoff` | 1 | 0.01MB | 2026-07-26~2026-07-26 |
| `-private-tmp-claude-501--Users-coolbress-goppi-1f3e1bec-0645-40d3-b395-d5e65cb313de-scratchpad-m1-ship5` | 1 | 0.01MB | 2026-07-25~2026-07-25 |
| `-private-tmp-claude-501--Users-coolbress-goppi-8d3445a7-8f2a-4036-a349-71a5fe0ed7af-scratchpad-m4run3-baseline` | 1 | 0.01MB | 2026-07-26~2026-07-26 |
| `-private-tmp-claude-501--Users-coolbress-goppi-c503403c-bd2b-4275-9c1a-c70fa8dbf61c-scratchpad-m4b-ship4-1785120957` | 1 | 0.01MB | 2026-07-27~2026-07-27 |
| `-private-tmp-claude-501--Users-coolbress-goppi-c503403c-bd2b-4275-9c1a-c70fa8dbf61c-scratchpad-m4b-ship-retry-1785112170` | 1 | 0.01MB | 2026-07-27~2026-07-27 |
| `-private-tmp-claude-501--Users-coolbress-goppi-c503403c-bd2b-4275-9c1a-c70fa8dbf61c-scratchpad-m4c-base-1785162697` | 1 | 0.01MB | 2026-07-27~2026-07-27 |
| `-private-tmp-claude-501--Users-coolbress-goppi-06422959-dbf9-42e3-80f5-abd62e6e396c-scratchpad-m4-harness-eval` | 1 | 0.01MB | 2026-07-25~2026-07-25 |
| `-private-tmp-claude-501--Users-coolbress-goppi-1f3e1bec-0645-40d3-b395-d5e65cb313de-scratchpad-m1-base` | 1 | 0.01MB | 2026-07-25~2026-07-25 |
| `-private-tmp-claude-501--Users-coolbress-goppi-c503403c-bd2b-4275-9c1a-c70fa8dbf61c-scratchpad-m4b-ship3-1785118941` | 1 | 0.01MB | 2026-07-27~2026-07-27 |
| `-private-tmp-claude-501--Users-coolbress-goppi-c503403c-bd2b-4275-9c1a-c70fa8dbf61c-scratchpad-m4b-ship2-1785112404` | 1 | 0.01MB | 2026-07-27~2026-07-27 |
| `-private-tmp-claude-501--Users-coolbress-goppi-1f3e1bec-0645-40d3-b395-d5e65cb313de-scratchpad-m1-ship2` | 1 | 0.01MB | 2026-07-25~2026-07-25 |
| `-private-tmp-claude-501--Users-coolbress-goppi-c503403c-bd2b-4275-9c1a-c70fa8dbf61c-scratchpad-m4c-final-cbaa1f1` | 1 | 0.01MB | 2026-07-27~2026-07-27 |
| `-private-tmp-claude-501--Users-coolbress-goppi-06422959-dbf9-42e3-80f5-abd62e6e396c-scratchpad-m4-baseline` | 1 | 0.01MB | 2026-07-25~2026-07-25 |
| `-private-tmp-claude-501--Users-coolbress-goppi-c503403c-bd2b-4275-9c1a-c70fa8dbf61c-scratchpad-m4b-base-36b3185` | 1 | 0.01MB | 2026-07-27~2026-07-27 |
| `-private-tmp-claude-501--Users-coolbress-goppi-1f3e1bec-0645-40d3-b395-d5e65cb313de-scratchpad-m1-ship0` | 1 | 0.01MB | 2026-07-25~2026-07-25 |
| `-private-tmp-claude-501--Users-coolbress-goppi-c503403c-bd2b-4275-9c1a-c70fa8dbf61c-scratchpad-m4b-ship-36b3185` | 1 | 0.01MB | 2026-07-27~2026-07-27 |
| `-private-tmp-claude-501--Users-coolbress-goppi-8d3445a7-8f2a-4036-a349-71a5fe0ed7af-scratchpad-m4run1-scaffold` | 1 | 0.01MB | 2026-07-26~2026-07-26 |
| `-private-tmp-claude-501--Users-coolbress-goppi-8d3445a7-8f2a-4036-a349-71a5fe0ed7af-scratchpad-m4run1-kickoff` | 1 | 0.01MB | 2026-07-26~2026-07-26 |
| `-private-tmp-claude-501--Users-coolbress-goppi-06422959-dbf9-42e3-80f5-abd62e6e396c-scratchpad-m4-scaffold` | 1 | 0.01MB | 2026-07-25~2026-07-25 |
| `-private-tmp-claude-501--Users-coolbress-goppi-8d3445a7-8f2a-4036-a349-71a5fe0ed7af-scratchpad-m4run1-ship` | 1 | 0.01MB | 2026-07-26~2026-07-26 |
| `-private-tmp-claude-501--Users-coolbress-goppi-8d3445a7-8f2a-4036-a349-71a5fe0ed7af-scratchpad-m4run2-kickoff` | 1 | 0.01MB | 2026-07-26~2026-07-26 |
| `-private-tmp-claude-501--Users-coolbress-goppi-8d3445a7-8f2a-4036-a349-71a5fe0ed7af-scratchpad-m4run3-scaffold` | 1 | 0.01MB | 2026-07-26~2026-07-26 |
| `-private-tmp-claude-501--Users-coolbress-goppi-8d3445a7-8f2a-4036-a349-71a5fe0ed7af-scratchpad-m4run1-baseline` | 1 | 0.01MB | 2026-07-26~2026-07-26 |
| `-private-tmp-claude-501--Users-coolbress-goppi-06422959-dbf9-42e3-80f5-abd62e6e396c-scratchpad-m4-governed` | 1 | 0.01MB | 2026-07-25~2026-07-25 |
| `-private-tmp-claude-501--Users-coolbress-goppi-1f3e1bec-0645-40d3-b395-d5e65cb313de-scratchpad-m1-ctrstrip` | 1 | 0.01MB | 2026-07-25~2026-07-25 |
| `-private-tmp-claude-501--Users-coolbress-goppi-1f3e1bec-0645-40d3-b395-d5e65cb313de-scratchpad-m1-ship4` | 1 | 0.01MB | 2026-07-25~2026-07-25 |
| `-private-tmp-claude-501--Users-coolbress-goppi-1f3e1bec-0645-40d3-b395-d5e65cb313de-scratchpad-m1-ship7` | 1 | 0.01MB | 2026-07-25~2026-07-25 |
| `-private-tmp-claude-501--Users-coolbress-goppi-1f3e1bec-0645-40d3-b395-d5e65cb313de-scratchpad-m1-rev2` | 1 | 0.01MB | 2026-07-25~2026-07-25 |
| `-private-tmp-claude-501--Users-coolbress-goppi-1f3e1bec-0645-40d3-b395-d5e65cb313de-scratchpad-m1-rev` | 1 | 0.01MB | 2026-07-25~2026-07-25 |
| `-private-tmp-claude-501--Users-coolbress-goppi-d6e5f837-01d4-4841-a75d-fd6f8b7d4802-scratchpad-g5-m4` | 1 | 0.01MB | 2026-07-25~2026-07-25 |
| `-private-tmp-claude-501--Users-coolbress-goppi-d6e5f837-01d4-4841-a75d-fd6f8b7d4802-scratchpad-g5-m2` | 1 | 0.01MB | 2026-07-25~2026-07-25 |
| `-private-tmp-claude-501--Users-coolbress-goppi-c503403c-bd2b-4275-9c1a-c70fa8dbf61c-scratchpad-m4-scaffold-fresh-e77540b-2` | 1 | 0.01MB | 2026-07-26~2026-07-26 |
| `-private-tmp-claude-501--Users-coolbress-goppi-c503403c-bd2b-4275-9c1a-c70fa8dbf61c-scratchpad-m4b-ship5-1785121346` | 1 | 0.01MB | 2026-07-27~2026-07-27 |
| `-private-tmp-claude-501--Users-coolbress-goppi-c503403c-bd2b-4275-9c1a-c70fa8dbf61c-scratchpad-m4c-scaffold-85af491` | 1 | 0.01MB | 2026-07-27~2026-07-27 |
| `-private-tmp-claude-501--Users-coolbress-goppi-8d3445a7-8f2a-4036-a349-71a5fe0ed7af-scratchpad-m4run4-scaffold` | 1 | 0.01MB | 2026-07-26~2026-07-26 |
| `-private-tmp-claude-501--Users-coolbress-goppi-06422959-dbf9-42e3-80f5-abd62e6e396c-scratchpad-m4-scaffold-rev` | 1 | 0.01MB | 2026-07-25~2026-07-25 |
| `-private-tmp-claude-501--Users-coolbress-goppi-06422959-dbf9-42e3-80f5-abd62e6e396c-scratchpad-m4-kickoff-rev` | 1 | 0.01MB | 2026-07-25~2026-07-25 |
| `-private-tmp-claude-501--Users-coolbress-goppi-c503403c-bd2b-4275-9c1a-c70fa8dbf61c-scratchpad-m4-baseline` | 1 | 0.01MB | 2026-07-26~2026-07-26 |
| `-private-tmp-claude-501--Users-coolbress-goppi-06422959-dbf9-42e3-80f5-abd62e6e396c-scratchpad-m4-kickoff` | 1 | 0.01MB | 2026-07-25~2026-07-25 |
| `-private-tmp-claude-501--Users-coolbress-goppi-1f3e1bec-0645-40d3-b395-d5e65cb313de-scratchpad-m1-ship3` | 1 | 0.01MB | 2026-07-25~2026-07-25 |
| `-private-tmp-claude-501--Users-coolbress-goppi-1f3e1bec-0645-40d3-b395-d5e65cb313de-scratchpad-m1-ship6` | 1 | 0.01MB | 2026-07-25~2026-07-25 |
| `-private-tmp-claude-501--Users-coolbress-goppi-1f3e1bec-0645-40d3-b395-d5e65cb313de-scratchpad-m1-ship` | 1 | 0.01MB | 2026-07-25~2026-07-25 |
| `-private-tmp-claude-501--Users-coolbress-goppi-1f3e1bec-0645-40d3-b395-d5e65cb313de-scratchpad-m1-ctr` | 1 | 0.01MB | 2026-07-25~2026-07-25 |
| `-private-tmp-claude-501--Users-coolbress-goppi-d6e5f837-01d4-4841-a75d-fd6f8b7d4802-scratchpad-g5-m1` | 1 | 0.01MB | 2026-07-25~2026-07-25 |
| `-Users-coolbress-gingoa` | 0 | 0.00MB | -~- |

</details>

## 상태

| | |
|---|---|
| 홈 최상위 | 0건 |
| `~/.claude.json` | 0건 |
| `~/.claude` 설정·백업 파일 | 0건 |
| `~/.claude/plugins` | 0건 |
| `~/.claude/projects` | 0건 |
| 셸 · Codex 설정 | 0건 |

> 이 표의 *"0건"* 은 **여덟 표면을 전부 훑은 뒤**의 것이다.
> #28의 *"0건"* 과 글자는 같고 **근거가 다르다** — 그 차이가 이 문서다.
