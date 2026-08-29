# 이 저장소에서 일하는 법

**리서치 코퍼스와 방향 문서다.** 코드 저장소가 아니다 — 산출물은 `direction/`(현행 판단) ·
`corpus/`(근거) · `audit/`(격차·감사)다. `CLAUDE.md` 는 심볼릭 링크 — **정본은 `AGENTS.md`.**

## 검사 — 문서를 고쳤으면 **먼저 재생성하고** 돌린다

```bash
python3 tools/rebuild_after_manifest.py   # 🔴 문서를 고쳤으면 항상. 안 하면 해시가 어긋난다
node    tools/build-routes.mjs            # ROUTES.jsonl 재생성
python3 tools/validate_corpus.py          # 스키마 · claim · 인용 사슬 · URL 원장
python3 -m unittest discover -s tools -p 'test_*.py'
ruff check tools/                         # 규칙은 ruff.toml 이 정본 (12군)
mypy                                      # 설정은 mypy.ini 가 정본 (strict)
```

나머지 검사는 **`tools/check_*.py` 를 그냥 다 돌린다** — 목록을 여기 적으면 바로 낡는다.
🔴 **`README.md` 의 목적 한 줄은 손으로 고치지 않는다** — `direction/01` §한 줄이 정본이고
`check_purpose_sync` 가 둘이 갈리는 것을 막는다.
`repo_audit.py`·`check_template_drift.py`·`check_decision_referrals.py` 는 **네트워크를 탄다**(CI 밖).

## 🔴 ALWAYS

- **`direction/` 이 코퍼스를 인용할 땐 경로로.** 이름만 쓰면 claim 불변식이 **우회된다**
- **덜 익은 문서(`draft`·`review-needed`)를 인용하면 그 줄에 status 를 병기한다**
- **`GAPS` 의 상태는 취소선이 정한다.** 제목에 *"종료"* 를 쓰면 닫힌 것으로 읽힌다 —
  부분 진행은 **본문**에 적는다
- **수치를 쓰기 전에 1차 출처를 읽는다.** `last30days` 는 후보 발견이지 판정이 아니다
- 🔴 **격차를 착수하면 첫 일은 그 격차의 *서술* 을 원자료로 확인하는 것이다.**
  2026-08-29 까지 **셋이 틀려 있었다** — `R5-7`(원자료가 삭제됐는데 인용 중) ·
  `R5-9①`(*"본문은 보존돼 있다"* 는데 없었다) · `R5-6`(*"부재"* 라는데 진술 6건이 있었다).
  **요약이 원자료보다 오래 산다.** 이건 검사로 못 잡는다 — 읽는 수밖에 없다

## ⚠️ ASK FIRST — `decision` 라벨 이슈로 회부한다

되돌리기 어렵거나 · 소유자 취향이 갈리거나 · **내가 권한이 없을 때**만.
읽기 전용 · 되돌리기 쉬운 것 · **이미 정착된 패턴 안의 행동** · 진행 확인은 **묻지 않는다**
(`direction/06` §회부 규율 — 과다 회부는 승인을 고무도장으로 만든다).

## 🚫 NEVER

- `legacy/` 를 고치기 — **append-only** 다. `LINEAGE` §5b 는 **소유자만** 쓴다
- 코퍼스 본문의 옛 이름(`gingoa`·`goppi`)을 현재 이름으로 바꾸기 —
  **그때 그 프로젝트의 참인 기록**이다 (`GUIDE.ko.md` 상단이 읽는 규칙)
- 출처 없는 수치를 `direction/` 이 인용하기 (절대규칙 3)

## 규율

- **PR 제목은 `type(scope): 요약`** — 표준 11종뿐. 지역 의미는 **scope** 로 (`docs(research):`)
- **닫힌 회부는 `direction/`·`audit/` 에 인용돼야 한다** — RFC 는 이슈에 살아도 되지만 **결정은 커밋된다**
- 다음 할 일: `gh issue list` 와 `audit/GAPS.ko.md` (`check_gaps_ledger` 가 내는 수가 정본)
