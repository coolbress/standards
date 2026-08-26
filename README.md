# standards

**소프트웨어를 현업 개발팀처럼 만들기 위한 근거·계보·방향 저장소.**

> **목적 한 줄**(정본은 [`direction/01`](direction/01-what-i-want.md)):
> *리서치로 찾은 현업 기준점을 따라 **비엔지니어가 에이전트로** 프로젝트를 굴리고,
> **최종 산출물이 시니어 엔지니어급**이 되며, 그 과정에서 **내가 맥락을 잃지 않는 것.***

하네스 **6세대**(claudeck-v1 → claudeck → gingoa → codex-native → goppi → goppi_final)에서 살아남은 것을 모았다.
목적은 네 가지다:

1. **모아둔 리서치를 한자리에** — 28측면 · SWEBOK/ISO 12207:2026/25010 앵커 · 6,582 저장소 census
2. **과거 하네스의 계보** — 무엇을 어떻게 지었나
3. **그때 알아낸 것과 왜 실패했나** — 실측과 진단
4. **그 위에서 앞으로의 방향** — 리서치 + 실패 사례에서 도출한 것

## 어디서 시작하나

### 지금 작업하러 왔으면 → **[`NEXT.md`](NEXT.md)**

작업 지시서. 무엇을 만들 차례이고 무엇을 하지 말아야 하는지.

### 처음이면 → `direction/`

| 순서 | 문서 | 답하는 질문 |
|---|---|---|
| 01 | [`direction/01-what-i-want.md`](direction/01-what-i-want.md) | 무엇을 원하는가 — **요구 6가지**, 문제 45개로 추적 |
| 02 | [`direction/02-why-past-attempts-failed.md`](direction/02-why-past-attempts-failed.md) | 왜 여섯 번 무너졌는가 |
| 03 | [`direction/03-what-research-says.md`](direction/03-what-research-says.md) | 리서치는 무엇을 말하는가 |
| 04 | [`direction/04-the-plan.md`](direction/04-the-plan.md) | 그래서 무엇을 만드는가 — 만들 것 12 |
| 05 | [`direction/05-the-output-floor.md`](direction/05-the-output-floor.md) | **무엇이 남아야 시니어급인가** — 산출물 바닥 |

### 계보가 궁금하면
[`legacy/LINEAGE.md`](legacy/LINEAGE.md) — 여섯 하네스 · 결정 64건 · 스펙 11종 제목 · 되살릴 수 없는 실측 12건

### 근거를 파려면

| 목적 | 문서 |
|---|---|
| 구조를 사람이 훑기 | [`MAP.md`](MAP.md) — 생성물. 등급별 문서 지도 |
| 에이전트 진입점 | [`corpus/INDEX.md`](corpus/INDEX.md) |
| 무엇을 근거로 인정하나 | [`corpus/methods/EVIDENCE-POLICY.md`](corpus/methods/EVIDENCE-POLICY.md) |
| **무엇이 안 바뀌고 무엇이 썩나** | [`corpus/methods/evidence-durability--grading-model.md`](corpus/methods/evidence-durability--grading-model.md) — 🟢🟡🔴 |
| **유일한 1차 사용자 자료** | [`corpus/census-data/owner-problem-map/`](corpus/census-data/owner-problem-map/) — 문제 45개 |
| 하네스가 자기 실패를 증명한 시험 | [`corpus/census-data/harness-confirmation-trial/`](corpus/census-data/harness-confirmation-trial/) |
| 아직 빈 곳 | [`audit/GAPS.ko.md`](audit/GAPS.ko.md) |

## 층위

```
direction/        ⭐ 결론 — 앞으로 어디로 가는가. 주장에 근거를 건다
corpus/              근거 — 판단이 들어가면 안 되는 층
  ├ aspects/         28측면 종합 + claim register
  ├ census-data/     원시 empirical 증거 (append-only)
  └ methods/         연구·큐레이션 규칙
legacy/           📜 과거 — 6세대가 남긴 전부. 진입점은 LINEAGE.md
  ├ LINEAGE.md       계보 서사 — 무엇을 지었고 왜 죽었나 (§5b 소유자 회고는 미완)
  ├ DISPOSITION.md   처분 대장 — 문서 274건 전수와 각각의 처분. 미분류 0
  ├ ARCHIVE-INDEX.md 저장소 밖 로컬 아카이브와 승계 여부
  ├ judgments/       그때의 판단 — 세대별로 묶음
  │   ├ goppi/ · gingoa/ · research-interpretation/
  └ sources/         원본 사본 — provenance이지 승인이 아니다
audit/               감사·공백·무결성 대장 (append-only)
tools/               구조 검증 · 지도 생성 · 검색 계약 평가
archive/             복구 가능한 스냅샷
```

**`direction/`과 `legacy/`가 충돌하면 `direction/`이 현행이다** — `legacy/`는 폐기된 하네스의 기록이고, `direction/`은 그 실패 이후의 방향이다.

## 절대 규칙

1. census의 **보급률**과 좋은 practice를 동일시하지 않는다.
2. 공식 제품 문서를 **제품 효과성**의 증거로 쓰지 않는다.
3. `review-needed`·`draft` 문서를 인용할 때는 **인용 지점에 status를 병기한다.** *(2026-08-24 개정 — 원문은 "인용하지 않는다"였으나, 2026-08-02 감사에서 상속 `verified` 50건이 전부 강등돼 지키면 아무것도 인용할 수 없는 사문이 됐다. `audit/GAPS` R5-4.)* 하중이 큰 claim은 `verified` 승격을 먼저 한다.
4. 합성 판단은 `synthesis`, 프로젝트 선택은 `direction/`으로 표시한다.
5. 새 연구는 **질문·검색일·포함/제외·claim-source 관계·시효·종료 기준**을 갖는다.
6. **새로 짓기 전에 [`MAP.md`](MAP.md)를 주제어로 훑는다** — 없는 것을 새로 만들었다고 착각한 사례가 **8회** 있다([`direction/02`](direction/02-why-past-attempts-failed.md) *진단의 진단* 전수표).
7. **지적을 받으면 그 좌표가 아니라 그 종류를 전 저장소에 grep한다** — 좌표만 고치면 다음 검수가 같은 결함을 다른 좌표에서 찾는다(2026-08-24 2차 적대 검수 총평).
8. **"없다"고 쓰기 전에 디스크를 본다** — 계보·이력·산출물에 대한 부정 주장은 저장소 grep으로 끝내지 않고 `~/`를 실제로 훑은 뒤에 쓴다. `~/plugins/codex-native`가 **여섯 번째 하네스**로 2026-08-24에야 발견됐다([`direction/02`](direction/02-why-past-attempts-failed.md) *진단의 진단* 8번). **정리 스크립트의 `0건` 출력도 디스크를 본 것이 아니다** — 스크립트가 훑은 표면 목록을 먼저 읽는다(같은 표 9번). **그리고 이미 읽은 자료도 조회하지 않으면 없는 것과 같다** — 공백을 주장하기 전에 주제어로 grep 한다(같은 표 10번).

## 검사

```bash
python3 tools/validate_corpus.py        # 구조·프론트매터·매니페스트·URL 대장
node    tools/build-routes.mjs --check  # 라우팅 지도 최신 여부 (낡으면 exit 1)
python3 tools/external_url_audit.py     # 외부 URL 생사 (네트워크 · ~7분)
```

CI가 앞의 둘을 매 push/PR에 돌리고, `main`은 **룰셋으로 보호**된다 —
직접 푸시·빨간불 머지·관리자 강제 머지 모두 거부됨을 실측으로 확인했다
([GEB-005·006](corpus/aspects/05-scm-workflow/github-enforcement-boundaries--facts-2026-08.md)).
문서를 고쳤다면 `tools/rebuild_after_manifest.py`와 `build-routes.mjs`를 다시 돌려야 검증이 통과한다.

## 알려진 상태

- 상속된 `verified` 50건은 2026-08-02 감사에서 `review-needed`로 내렸다.
- 외부 URL 4건이 죽어 있고 1건은 응답이 없다 — 인용 문서가 각각 고지한다.
- 28-aspect taxonomy는 provisional이다.
- **호스트(Claude Code) 표면 문서는 🔴 등급이다** — 측정 시점 버전을 확인하고, 결정이 걸리면 다시 측정하라.
