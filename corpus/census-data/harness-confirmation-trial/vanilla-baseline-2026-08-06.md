# vanilla 스모크 — 기준선 관측 기록 (2026-08-06)

> 성격: **관측 기록만**이다. 이 문서는 판정하지 않고, 무엇을 관측했는지와 무엇을 관측하지
> 않았는지만 적는다. 목적은 goppi 설치 **전**의 호스트 상태를 고정해, 이후 차이를 귀속할 수
> 있게 하는 것이다.
> 선행: `2026-08-06-empty-state-runtime-verification.md`(goppi 부재 확인).

## 0. 이 기준선이 "vanilla"인 조건

이 호스트는 **순정 Claude Code가 아니다.** 제3자 훅 13종과 사용자 개인 권한 세트(G7)가 있다.
따라서 이 문서에서 vanilla는 "아무것도 없는 상태"가 아니라 **"goppi만 없는 상태"**를 뜻한다.
확증시험의 vanilla arm이 이 정의를 쓰려면 두 arm이 아래 구성을 **똑같이** 가져야 한다
(spec §2 성공기준 3). 그 결정은 아직 하지 않았다.

## 1. 호스트 구성 스냅샷 (2026-08-06)

| 항목 | 값 |
|---|---|
| 모델 | `opus[1m]` · effortLevel `xhigh` |
| MCP 서버 | **0개** (`claude mcp list` → "No MCP servers configured") |
| 플러그인 | **1개** — `codex@openai-codex` v1.0.3 (enabled) |
| 마켓플레이스 | `claude-plugins-official` · `openai-codex` |
| 사용자 스킬 | `computer-use` · `orca-cli` · `orchestration` — **3개 전부 `skillOverrides`에서 `off`** |
| 훅 | 13종 등록 (orca 10 = 무발화 · codex 플러그인 3 = `SessionStart` 발화 확인) |
| 프로젝트 설정 | `.claude/settings.local.json` — `allow: ["Skill(codex:rescue)"]` 한 줄 |
| VCS | **Git working tree 아님** (`progress.md` 기록과 일치) |

### G7 안전 세트 — 전문

```
deny  (6): Bash(rm -rf *) · Bash(git reset --hard:*) · Read(./.env) · Read(./.env.*)
           Read(~/.ssh/**) · Read(./secrets/**)
ask  (12): Bash(git push*) · Bash(gh pr merge*) · Bash(gh release*) · Bash(npm publish*)
           Bash(*deploy*) · Bash(gh issue create*) · Bash(gh pr create*) · Bash(gh pr comment*)
           Bash(curl*) · Bash(wget*) · Bash(scp*) · Bash(rsync*)
allow (4): Bash(node:*) · Bash(timeout:*) · WebSearch · WebFetch
```

## 2. 권한 층이 살아 있는가 — 실증 2방향

게이트가 **발화한다**는 것과 게이트가 **효과가 있다**는 것은 다르다. 메시지만 보고 통과시키지
않기 위해 관측 가능한 부작용으로 확인했다.

**양성 — deny가 실제로 막는가:**

```
$ rm -rf <scratchpad>/g7-probe-empty
→ Permission to use Bash with command rm -rf ... has been denied.
$ [ -d <scratchpad>/g7-probe-empty ] → PASS: 대상 생존
```

차단 **메시지**뿐 아니라 대상 디렉토리가 살아 있다 = 실행이 실제로 일어나지 않았다.

**음성 — 매처 밖은 통과하는가:**

```
$ mkdir <probe>/inner && rmdir <probe>/inner → 통과
```

→ **G7 deny는 "삭제"를 막는 것이 아니라 문자열 `rm -rf`를 막는다.** 같은 결과를 내는
`rmdir` · `rm -r` · `find -delete` · 언어 런타임의 삭제 호출은 이 규칙에 걸리지 않는다.

## 3. G7 ↔ goppi 게이트 갭 표 (조각 1의 직접 입력)

goppi의 G1–G4를 이 기준선 위에 얹을 때, **이미 덮인 것과 새로 만들 것**은 다음과 같다.

| goppi 게이트 항목 (설계 §3) | G7의 현 상태 | 조각 1에서 |
|---|---|---|
| G1 비가역 삭제 | **부분** — `rm -rf` 문자열만 | 범위 확장은 조각 4. 조각 1은 아래 로그 경로 한정 |
| G1 force push | **없음** — `git push*`가 `deny`가 아니라 `ask` | 조각 4 |
| G1 프로덕션 파괴 | **없음** | 조각 4 |
| **G1 L3 로그 경로 쓰기 차단** | **없음 — 전부 신규** | **조각 1의 핵심 (§4.2-3)** |
| G2 배포·공개 | **대부분 덮임** — `*deploy*` · `npm publish` · `gh release` · `gh pr merge` · `git push` | 중복 회피 필요 (§4 참조) |
| G2 외부 전송 | **덮임(도구 경로 한정)** — `curl`/`wget`/`scp`/`rsync` | 언어 런타임 HTTP는 미커버 |
| G2 과금·자격증명 변경 | **없음** | 조각 1의 ask 최소셋 후보 |
| G3 시크릿 리터럴 유입 | **없음** — G7은 시크릿 **읽기**를 deny할 뿐, 도구 입력으로의 유입은 다른 축 | 조각 4 |
| G4 완료 주장 | **없음** | 조각 2 |

## 4. 이 관측이 드러낸 조각 1의 제약 3건

세 건 모두 **설계를 부정하지 않고 구현 방법을 좁힌다.** 판단이며, 근거는 위 §2·§3이다.

### C-1. G2 ask 최소셋은 G7과 겹치지 않아야 귀속이 된다

spec §4.2-5는 G2 발화 시 **승인 이벤트 3필드**를 L3에 기록하라고 요구한다. 그런데 G7의 ask 12개와
goppi G2가 같은 명령 표면에서 겹치면, 발화한 승인 요청이 **G7 것인지 G2 것인지 구분되지 않는다.**
구분이 안 되면 그 이벤트는 조건 3·4의 신호가 아니라 잡음이다.

→ 두 갈래 중 하나를 골라야 한다: **(i)** G2 최소셋을 G7과 **서로소**인 행위로 잡는다(과금·자격증명
변경 등 — §3 표에서 "없음"인 칸), 또는 **(ii)** `PermissionRequest` 훅으로 어느 규칙이 발화했는지를
페이로드에서 읽어 귀속한다. (ii)가 가능한지는 **미확인** — 훅 페이로드에 규칙 식별자가 있는지
확인하지 않았다. 조각 1에서 (ii)를 먼저 시험하고, 안 되면 (i)로 간다.

### C-2. 열거형 deny로는 "훅만 쓴다"를 강제할 수 없다

설계 §2.1-3은 L3 로그 경로에 대해 `Write`/`Edit`와 Bash 리다이렉션(`>`, `>>`, `tee`, `dd`,
`cp`, `mv`)을 G1 deny에 넣으라고 한다. §2의 음성 대조가 보인 것은 **권한 매처가 문자열 열거이고,
같은 효과를 내는 미열거 경로가 남는다**는 것이다 — 예: `python3 -c "open(p,'a').write(...)"`는
저 6개 어디에도 걸리지 않는다.

→ 조각 1의 eval 시나리오(≥3)에 **미열거 채널로의 쓰기 시도**를 반드시 넣고, 막히지 않으면
막히지 않는다고 기록한다. 설계 §2.1-5의 정직성 조건("1~4 구현 전까지 '증거 원천은 하네스 측'이라
말하지 않는다")을 **구현 후에도** 조건부로 유지해야 할 가능성이 있다: 정확한 문구는
"열거된 채널은 막힌다"이지 "모델이 쓸 수 없다"가 아니다.
⚠️ 이것은 설계 변경 제안이 아니라 **조각 1이 확인할 항목**이다. 결과를 보고 spec에 반영한다.

### C-3. `Stop` 훅에서 차단 가능한 것이 이미 1개 있다

codex 플러그인의 stop-review-gate가 `Stop`에 등록돼 있다(timeout 900). goppi G4는 두 번째가 된다.
설계 §3의 8회 한도가 훅별인지 세션 합산인지 미확인 — **조각 2의 선행 확인 항목**이며 조각 1을
막지는 않는다.

## 5. 이 기준선이 보장하지 않는 것

- **성능·비용 기준선이 아니다.** 토큰·지연·세션 수를 측정하지 않았다.
- **모델 행동 기준선이 아니다.** vanilla arm의 산출물 품질을 관측하지 않았다. 그것은 확증시험
  프로토콜의 일이고 이 문서의 범위가 아니다.
- **ask 규칙의 발화를 실증하지 않았다.** deny만 실증했다. ask 실증은 사용자에게 승인 프롬프트를
  띄우는 일이라 이번에 하지 않았다 — 조각 1에서 G2를 배선할 때 자연히 실증된다.
- **`PermissionRequest` 훅 페이로드의 내용을 확인하지 않았다** (C-1의 (ii)).
- **재현 가능한 스냅샷이 아니다.** 이 폴더는 Git working tree가 아니라 위 구성이 바뀌어도
  diff가 남지 않는다. 이 문서 자체가 그 시점의 유일한 기록이다.
