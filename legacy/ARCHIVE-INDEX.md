# ~/Archive — 로컬 아카이브 목록 (이 저장소 밖)

`legacy/`가 인용하는 원본 중 **이 저장소에 없는 것**의 목록이다. 전부 `/Users/coolbress/Archive/`에
**로컬로만** 존재하며 **백업이 없다** — 디스크가 죽으면 사라진다.

| 항목 | 크기 | 무엇 | 이 저장소에 승계된 것 |
|---|---|---|---|
| `claudeck-v1.git` | 11MB | v1 bare 저장소 (190커밋·272파일 · origin=`~/.claude`) | [`sources/claudeck-v1/`](sources/claudeck-v1/) — 커밋 목록 · 파일 목록 · README · 노트 2건 |
| `goppi-removal-2026-08-04/` | 44MB | 구 goppi 제거 백업 — 설정 4종 · plugin-remnants · doctor BEFORE/AFTER · SHA256SUMS | [`judgments/harness-removal-record-2026-08-04.md`](judgments/harness-removal-record-2026-08-04.md) — 기록 본문 |
| `goppi-final-2026-08/GOPPI_state/` | 32KB | precompact 훅이 남긴 세션 스냅샷 4건 (2026-08-02) | ❌ 승계 안 함 — 참조 0건이고 같은 기간을 `progress.md`가 덮었다(원 아카이브 사유 그대로) |
| `2026-08-24-harness-cleanup/goppi-trial-web/` | 224KB | 트라이얼 저장소 원본 | ✅ [`sources/goppi-trial-web/`](sources/goppi-trial-web/) — 해시 6/6 대조 완료 |

## 원칙

**검증 가능성은 이 저장소에, 산출물은 아카이브에.** `legacy/`의 주장은 여기 없이도 되짚을 수 있어야 한다 —
그래서 커밋 목록·파일 목록·기록 본문은 승계했고, 코드 본문과 바이너리 백업은 안 했다.

⚠️ **아카이브가 사라져도 이 저장소의 인용은 깨지지 않는다.** 다만 *원본 대조*는 불가능해진다 —
그 한계는 각 승계 문서가 명시한다.

## 아카이브를 지우려면

`~/Archive/`는 **이 저장소의 삭제 계획 대상이 아니다.** 지우려면 위 표의 "승계된 것" 열이
전부 채워져 있는지 먼저 확인하라. `GOPPI_state`만 승계 없이 비어 있고, 그것은 의도적이다.
