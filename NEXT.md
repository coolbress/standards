# 다음 세션 인계

> 갱신 **2026-09-02**. **이 문서는 낡는다** — 정본은 [`direction/`](direction/) 이고 이것은 **작업 지시서**다.
> 🔴 **100줄을 넘기지 않는다.** 일지는 여기 안 적는다 — `git log` 와 머지된 PR 본문이 일지다
> (2026-09-02 이전 일지는 `git log -p -- NEXT.md` 로 본다). 이 문서가 976줄까지 자란 적이 있고
> *"다음 할 일"* 표가 732번째 줄에 있었다 — 그래서 이 상한이 있다.

## 📍 정본은 어디인가 — 이 여섯만 보면 된다

| 묻는 것 | 정본 |
|---|---|
| 격차가 몇 건 남았나 | `python3 tools/check_gaps_ledger.py` — 🔴 수를 여기 안 적는다. **명령을 돌려라** |
| 소유자에게 물어둔 것 | `gh issue list --label decision` |
| 이 저장소에서 일하는 법 | [`AGENTS.md`](AGENTS.md) |
| 무엇으로 고르나 | [`direction/07`](direction/07-design-rules.md) — 원칙 넷과 시행 기준 |
| 사용자는 어느 단계에서 무엇을 치나 | `workflows/plugins/standards/skills/playbook/SKILL.md` — **플레이북** (0.10.0 · 2026-09-02) |
| 배포는 어떻게 생겼나 | [`audit/PLUGIN-DESIGN`](audit/PLUGIN-DESIGN.ko.md) · `claude plugin list` |

## 🎯 어디까지 왔나 — 시나리오로 센다 (구성요소 수로 세지 않는다)

| 시나리오 | 상태 |
|---|---|
| 공개 GitHub · Python · 신규 · 단독 소유자 · 에이전트 주행 | ✅ `divcal` 2회 완주 (2026-08-28) |
| 세션을 닫았다 열어 "계속하자" (cold restart) | ✅ 1회 (`divcal` #4→#5) |
| 벽이 실제로 막는가 (직접 푸시 · 빨간불 · `--admin`) | ✅ 4/4 실측 |
| **외부 설치자** — 깨끗한 기계에서 설치 → `/new-project` → 첫 PR | ⬜ |
| **기존 저장소** (brownfield) — `/floor-check` 부터 단계적으로 | ⬜ |
| **30일 유지** — 한 달 뒤 다시 열어 초록인가 · 첫 회귀 수리 | ⬜ (`divcal` 동결 중) |
| 워크플로 실패 · 리뷰 서비스 장애에서 복구 | 🟡 코덱스 한도 1회 겪음 (`R5-48`) |
| 시니어에게 실제 인수 | ⬜ |
| 비공개 저장소 | ⬜ 미지원 (`--private` 거부) |

⚠️ 목적 한 줄의 주어는 **비엔지니어**인데 완주는 **에이전트 주행**이었다 — 주어가 다르다. 위 ⬜ 는 전부 *남* 이 필요하다.

## ⏭️ 다음 세션이 할 일 — 순서대로

**2주 규칙 (2026-09-02 ~ 09-16)**: 🔴 **제품 PR 을 막는 게 아니면 `standards` PR 을 안 낸다.**
근거: `check_harness_cost` 하네스 320 · 제품 23 → **93%**. 열린 격차 7건 중 5건이 *"재료가 생기면"* 인데 재료는 제품에서만 나온다.

| # | 할 일 | 어디 |
|---|---|---|
| 1 | **`divcal` 을 플레이북대로** 티켓 2~3개 — `/grill-with-docs` 부터. `/kickoff` 은 없다 | `divcal` |
| 2 | 재기: ④ *"뭘 만들려던 거지"* 주당 횟수 · ③ⓑ 재설명 · `check_skill_firing`(Matt 스킬이 찍혀야 한다) · 머지된 PR 수 · `check_harness_cost` | 계기 |
| 3 | 외부 설치자 1명 — 깨끗한 기계에서 설치 → `/new-project` → 첫 PR | — |
| 4 | `kickoff` 잔재 넷 중 **실제로 아쉬웠던 것만** 되살린다 — 스킬로는 안 되살린다 | 템플릿 `AGENTS.md` |

열린 격차의 *왜 지금 못 하나* 는 [`audit/GAPS.ko.md`](audit/GAPS.ko.md) §R5 가 정본이다. 여기 복사하지 않는다.

### 🚫 지금 만들지 않는다

stack-manifest JSON · 유지비 계기판 확장 · `/floor-check` doctor · 플레이북에 "지금 어디" 표시 · Node 상자 ·
GitLab 추상화 · 스킬 추가 · 멀티에이전트 기본값 · 자체 런타임 · 필수 검사 추가. **실제 수요가 나올 때 만든다.**

### ⚠️ 굴리기 전에 알아둘 것

- **`third-party / review` 가 required 다.** 코덱스 한도를 넘기면 머지가 막힌다 — 기다리거나 룰셋에서 그 검사만 뺀다(관리자 · 1분)
- 문서를 고쳤으면 **`rebuild_after_manifest.py` → `build-routes.mjs`** 를 먼저 돌린다
- **`.github/workflows/*.yml` · `ruleset.json` 은 그것만 고치는 PR 로** — `check_referee_isolation` 이 막는다
- **`AGENTS.md` 의 `## Code Review Rules` 를 다른 변경과 같이 고치면 벽이 막는다** — 따로 낸다

## 🔒 자격증명 — 둘로 갈려 있다 (A-1)

| | 무엇 | 누가 |
|---|---|---|
| `GH_TOKEN` (기본 · `~/.zshenv` 가 `~/.config/gh-agent-token` 을 읽는다) | fine-grained — 쓰기: Contents · Issues · PRs · Workflows / 읽기: + Administration · Code scanning | 에이전트 |
| 관리자 토큰 | classic · 30일 만료 · **이 기계에 저장하지 않는다** | 사람만 |

관리자 작업(룰셋 · Actions 정책 · 시크릿 · CodeQL)은 **사람이 한다.** 에이전트는 명령을 만들어 넘긴다:

```bash
cd ~   # 🔴 저장소 밖에서
~/workflows/tools/with-admin-token.sh ~/workflows/new-project.sh <이름>
```

🔴 토큰을 명령줄에 쓰지 마라 — `~/.zsh_history` 에 남는다. 래퍼가 `/dev/tty` 에서 묻는다. **403 이 나면 그것이 정상이다.**

## 🎯 완료의 정의

**이 저장소 안의 검증은 합성 시험이다** — 문서 저장소라 락파일도 테스트 스위트도 없다.
만들 것은 **실제 프로젝트에서 end-to-end 로 돌아야** 끝난 것이다(`new-project.sh` → 기획 → 이슈 → 브랜치 → PR → CI → 머지).
goppi 는 합성 공격 0/4 를 막고 실사용 11건에 침묵했다 — **자기가 만든 시험만 통과한 것이다.** 그 형태를 피하려고 이 규칙이 있다.

## 2주 뒤 판정 기준

[`direction/04`](direction/04-the-plan.md) §판정 기준에 **사전 등록**돼 있다. **결과를 보고 기준을 옮기지 않는다.**
