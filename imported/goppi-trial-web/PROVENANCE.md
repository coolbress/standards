# goppi-trial-web — 승계 기록

- **원본**: `~/goppi-trial-web` (로컬 전용 · 원격 없음 · 미푸시 커밋 5개)
- **이관일**: 2026-08-24 · 파일 사본 + `GIT-HISTORY.txt`(커밋 로그 원문)
- **이관 사유**: 원본이 로컬에만 존재해 소실 위험. 로컬 폴더는 이관 후 삭제됐다.

## 이것이 무엇인가

goppi G4의 **실물 확증시험이 실제로 수행된 저장소**다. 미니 웹 앱(`server.mjs`·`app.mjs`)에
인수기준 1개와 검사 1개(`ACCEPTANCE.json`·`check.mjs`)를 고정하고, 공격 4종을 심어
하네스가 차단하는지를 실제 호스트 훅 발화로 관측했다.

`goppi_final/records/`의 다음 문서들이 이 저장소를 **서술**한다 — 서술의 **물증**이 여기다:
`2026-08-18-external-trial.md` · `2026-08-18-g4-promotion-hardening.md` ·
`2026-08-19-trial-web-integration.md` · `2026-08-19-fp-instrumentation.md` ·
`2026-08-19-session13-prompt.md`

커밋 로그 자체가 시험 대본이다 — "C2 심기: app.mjs 한 줄 수정 — 검증 증거를 낡게 만드는
리비전 변경", "ask 규칙 재작성 — 1차 봉인은 무창 무인으로 무효" 등.

## 지위

`imported/` 층의 규칙을 따른다 — **계보 기록이지 승인이 아니다.** 여기 담긴 설계·주장은
현행 근거가 아니며, 인용하려면 현재 코퍼스에서 재확인해야 한다.
