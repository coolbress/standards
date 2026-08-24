---
id: aspect-27-ai-harness-archetype--stop-event-rendering--measured-2026-08
title: "Stop 이벤트 렌더 관측"
parent: aspect-27-ai-harness-archetype
kind: evidence
evidence_track: lit
status: draft
language: ko
last_updated: "2026-08-17"
method: "Stop 훅 출력의 사용자 렌더 여부 관측. 원본: goppi_final/records/2026-08-17-stop-render-observation.md — 2026-08-24 이관, 본문 무수정."
---

> **이관 기록 (2026-08-24)**: 원본 저장소는 삭제됐다. 이 문서는 **폐기된 하네스가 아니라 호스트(Claude Code)의
> 실제 동작**에 대한 1차 실측이므로 남긴다. 하네스의 계보는 `imported/LINEAGE.md`.


> **판정: 렌더링 확인.** G4의 마지막 미확인 운반체가 닫혔다.
> 방법: 세션 #9(터미널 CLI · Claude Code 2.1.233)의 첫 턴 종료에서 G4가 실전 발화했고,
> 소유자가 화면에 보인 내용을 세션 #8에 그대로 전달했다 — 2026-08-08 G1 렌더링 확인과
> 같은 절차(고의/자연 발화 → 사람이 화면 확인).

## 관측된 것 (소유자 전달 원문 요지)

1. **`systemMessage` → 터미널 렌더링 ✅** — 별도 블록으로:
   `Stop says: 에이전트는 "완료"라고 선언했지만, goppi 판정은 다릅니다: …`
   중립 3선택지 화면 **전문이 그대로** 표시됐다. E1 헤드리스 실측(`system:informational`
   표면 생성)의 마지막 조각 — **사용자 도달** — 이 사람 관측으로 성립했다.
2. **에이전트 행동 계약 준수 ✅** — 세션 #9의 에이전트는 reason의 지시대로 판정 요약을
   그대로 전하고 멈췄다(임의 재시도 없음). 단계 B의 "행동 금지 + 사용자 대기"가 실전에서
   작동했다.
3. **부수 발견 — `reason`도 사용자에게 노출된다**: `⏺ Ran 5 stop hooks` 아래
   `Stop hook error: goppi G4: 완료 판정이 갈렸다…` 형태로 **모델용 reason이 화면에 그대로
   보였다.** 두 청중 분리(모델 reason / 사용자 systemMessage)가 Stop의 표시 층에서는
   완전하지 않다 — reason을 쓸 때 사용자가 읽어도 되는 문장으로 써야 한다는 제약이 생겼다
   (현행 reason은 문제없음 — 제약으로 기록).

## 함께 적발·수리된 결함 — 라벨 치환

- 예상(NEXT-SESSION: "봉인이 없다")과 화면 라벨(`CONTRACT-TAMPERED` · "승인된 상태와
  다릅니다")이 갈렸다. **실제 원인은 예상대로 봉인 없음이었다** — 봉인 파일 부재 확인 +
  L3 이벤트 `cause: "CONTRACT-UNSEALED"` 정확 기록. 게이트가 화면 verdict 라벨만 TAMPERED로
  뭉뚱그려 **승인 대기를 변조처럼 읽히게 했다** — 이 저장소가 금지하는 치환(상태 정직 위반)의
  화면판이고, 세션 #9 에이전트가 "예상과 실측이 갈렸다"고 정직하게 보고해 드러났다.
- **수리**: `CONTRACT-UNSEALED`를 별도 verdict·별도 화면 문구("승인 대기 — 변조가 아니라
  절차 미완")로 분리. 대조 C24 신설(봉인 없음 → '승인 대기' 표기 · '승인된 상태와 다릅니다'
  부재 확인). 스위트 24케이스 전량 통과.

## 범위와 한계

- n=1 · Stop 이벤트 · 터미널 CLI 한 표면. 데스크톱/웹/IDE 표면과 salience·피로는 미측정
  (기존 한계 유지 — 등록부 expiry 조건).
- "Ran 5 stop hooks" — Stop 훅 5개가 공존(다른 플러그인 포함). 공존 훅과의 상호작용은 미측정.
