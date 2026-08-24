# 오탐(FP) 측정 배선 — 조각 4 착수 · 2026-08-19 세션 #13

> 소유자 결정(AskUserQuestion): 다음 조각 = **(a) 오탐 측정**. ADR-0032("오탐율 없이 deny/block을
> 늘리지 않는다")의 분모를 만드는 조각. NEXT-SESSION #13 ② 메뉴에서 선택됨.

## 문제 — 왜 지금까지 오탐율이 없었나

- 오탐 **관측 개수**는 있었다(FP-2 계열 4건 + 조각 1에서 정당 작업 9회 차단). **비율은 없었다** —
  분모(발화 수)는 L3 `gate_fired`로 있는데, **분자(오탐 수)를 만들 재료가 없었다**:
  G1 deny 이벤트에는 `matched`(판정 부류)만 있고 **명령 자체가 없어** 사후에 "정당한 읽기였나,
  실제 쓰기 시도였나"를 판별할 수 없다. G2 `approval_requested`는 `cmd_sha256`(해시)뿐이라 마찬가지.
- #12(trial-web)에서 FP-2 계열 재발: G1이 정당한 읽기(`python3`·`sed`가 하네스 경로 언급)를
  4회 이상 차단. 이 발화들도 판별 재료가 없어 **영구 판별 불가**로 남는다.

## 무엇을 지었나 (측정이지 수리가 아니다 — deny/ask는 하나도 늘지 않았다)

| 층 | 내용 |
|---|---|
| 계측 (`gate-pre-tool.mjs` 4개 emit 지점) | G1 bash deny + `harness_path_read`: `cmd_sha256`·`cmd_head`(200자) · G1 파일도구 deny: `target` · G2 `approval_requested`: `cmd_head` 추가. L3-EXEC이 이미 명령 전문을 기록하므로 **새 노출 계열이 아니다** |
| 라벨 (`harness/verify/fp-label.mjs`) | 발화(ts#pid)를 `fp`/`tp`/`unknown`으로 라벨. `--why` 필수(근거 없는 라벨은 주장) · 재라벨 거부(정정은 git 이력으로) · `--by owner\|agent` — **agent 라벨은 이해충돌**(게이트 대상이 자기 차단을 판정)이라 잠정 |
| 대장 (`harness/verify/fp-labels.jsonl`) | **저장소 추적 파일** — 증거 경로(훅 전용·WF-02)가 아니라 git이 감사 표면. 첫 라벨 때 생성된다 |
| 리포트 (`harness/verify/fp-report.mjs`) | 규칙별: 발화(분모) · 계측 이전(영구 판별 불가) · 라벨 가능 · 라벨됨 · fp/tp/unknown · **라벨 대비 오탐율**(owner 확정/agent 잠정 분리) · 미라벨 잠정 표기. 무결성(유령 라벨·중복 키·파싱 불가) 깨지면 통계 대신 FAIL. 참고 분모로 `harness_path_read`(정당 트래픽 규모) 병기 |
| 대조 (`harness/verify/fp-control.mjs`) | 12케이스: 계측 4(A) · 라벨 도구 거부 동작 4(B) · 리포트 수학·dangling FAIL 4(C). **빨강 먼저 확인**(구현 전 8/12 FAIL) → 구현 후 12/12 초록. 합성(execFileSync) + 임시 GOPPI_HOME — 실제 증거·대장 안 건드림 |

## 실측

- `fp-control.mjs` **12/12 초록** (빨강 8건을 먼저 봤다 — 검사가 실패할 수 있음을 확인).
- 기존 대조 10종 **전부 PASS** — 게이트 응답(stdout·exit)은 안 바뀌었고 이벤트 필드만 늘었다.
- **실물 호스트 훅 발화 1회 확인**(합성 아님): 하네스 경로 읽기 명령에 현재 세션 훅이
  `harness_path_read` + `cmd_sha256`+`cmd_head`를 기록(2026-08-19T06:25:10Z · 훅은 이벤트마다
  새로 spawn되므로 재시작 없이 반영 — #11 실측과 일치).
- 첫 리포트(이 저장소): G1 발화 23 · G2 발화 5 — **전부 계측 이전 = 영구 판별 불가**.
  오탐율은 지금부터 쌓인다. 과거 발화에 소급 라벨은 불가능하고, 하지 않는다.

## 범위 밖 (정직 표기)

- **G4 발화는 이 측정 범위 밖** — 오탐·피로 측정은 등록부 G4 expiry의 실사용 측정 항목이고,
  의미론(전환 차단)이 달라 같은 정의에 편입하면 귀속이 흐려진다.
- **`run-all-controls.sh` 편입은 안 했다** — 계약(ACCEPTANCE.json)에 해시 고정된 파일이라
  고치면 봉인이 어긋난다. 편입 + 재봉인은 소유자 manual 모드 사안(세션 후반 몰아서 1회).
- 이 대조는 **기계 정합**만 본다. 라벨의 내용(정말 오탐인가)은 사람 판단이고, 확정치는
  owner 라벨만이다.
- 오탐 자체는 **그대로다** — 이 조각은 측정이다. 게이트 수리는 비율이 나온 뒤의 결정이다(ADR-0032).

## 운영 절차 (다음 세션·소유자)

```sh
node harness/verify/fp-label.mjs                 # 미라벨 발화 목록
node harness/verify/fp-label.mjs --label <ts#pid> --as fp --by owner --why "근거"
node harness/verify/fp-report.mjs                # 분모 있는 오탐율
node harness/verify/fp-control.mjs               # 정합 대조 12케이스
```

다른 프로젝트(예: trial-web)는 `--cwd <경로>`로 같은 대장에 라벨한다(라벨에 project 슬러그 기록).
