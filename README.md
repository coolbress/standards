# standards

**소프트웨어를 현업 개발팀처럼 만들기 위한 근거·계보·방향 저장소.**

> **목적 한 줄**의 정본은 [`direction/01` §한 줄](direction/01-what-i-want.md) 이다 — 여기 복사하지 않는다.
> 사본은 갈린다(2026-08-30 에 두 판 뒤처진 채 잡혔다). 링크만 둔다.

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
| 06 | [`direction/06-how-we-work.md`](direction/06-how-we-work.md) | 에이전트와 어떻게 일하는가 — 진입로·프로젝트 흐름·모델 라우팅 |

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

## 무엇을 지었나 — **네 층, 사는 곳이 다르다**

**이 저장소는 그중 한 층이다.** 나머지 셋은 다른 저장소에 산다.

```
🔒 벽     GitHub 서버              에이전트가 못 끈다        coolbress/workflows + ruleset
📦 상자   copier 템플릿            한 번 렌더, 인스턴스 소유  coolbress/project-template
🤝 안내   플러그인 둘              모델이 읽고 고른다        coolbress/workflows 안
📚 근거   ⭐ 여기                  왜 이 규칙이 있나         coolbress/standards
```

🔴 **벽은 플러그인에 안 들어간다.** 들어가는 순간 에이전트가 끌 수 있고, **끌 수 있으면 벽이 아니다.**

🔵 **이것도 하네스다.** 업계는 저장소·테스트·CI·피드백 루프 전체를 *harness* 라 부른다. 우리가 짓지 않는 것은
**상주형 자체 런타임**(매 턴 도는 제어 루프 · 전용 상태 · 자체 queue)이다 — 여섯 번 그걸 짓고 여섯 번 죽었다.

**보장이 셋으로 갈린다** — 인식은 **훅**(결정적) · 선택은 **스킬**(모델 자유) · 판정은 **벽**(우회 불가).
> *"안 쓰면 걸린다" 가 아니라 — **"안 써도 결과로 걸린다."***

## 이 저장소의 층위

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
