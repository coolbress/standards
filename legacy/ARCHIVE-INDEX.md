# ~/Archive — 로컬 아카이브 목록 (이 저장소 밖)

`legacy/`가 인용하는 원본 중 **이 저장소에 없는 것**의 목록이다. 전부 `/Users/coolbress/Archive/`에
**로컬로만** 존재하며 **백업이 없다** — 디스크가 죽으면 사라진다.

| 항목 | 크기 | 무엇 | 이 저장소에 승계된 것 |
|---|---|---|---|
| `claudeck-v1.git` | 11MB | v1 bare 저장소 (190커밋·272파일 · origin=`~/.claude`) | [`sources/claudeck-v1/`](sources/claudeck-v1/) — 커밋 목록 · 파일 목록 · README · 노트 2건 |
| `goppi-removal-2026-08-04/` | 44MB | 구 goppi 제거 백업 — 설정 4종 · plugin-remnants · doctor BEFORE/AFTER · SHA256SUMS | [`judgments/harness-removal-record-2026-08-04.md`](judgments/harness-removal-record-2026-08-04.md) — 기록 본문 |
| `goppi-final-2026-08/GOPPI_state/` | 32KB | precompact 훅이 남긴 세션 스냅샷 4건 (2026-08-02) | ❌ 승계 안 함 — 참조 0건이고 같은 기간을 `progress.md`가 덮었다(원 아카이브 사유 그대로) |
| `2026-08-24-harness-cleanup/goppi-trial-web/` | 224KB | 트라이얼 저장소 원본 | ✅ [`sources/goppi-trial-web/`](sources/goppi-trial-web/) — 해시 6/6 대조 완료 |
| `2026-08-24-harness-cleanup/claudeck/` | 1.8MB | **원격 삭제됨(2026-08-24)** · 로컬 사본 | 계보 §3 · [`sources/claudeck/`](sources/claudeck/) · 처분 전수는 [`DISPOSITION.md`](DISPOSITION.md) |
| `2026-08-24-harness-cleanup/gingoa/` | 698MB | **원격 삭제됨** · 로컬 사본 | **28측면 코퍼스 전체**가 `corpus/`로 승계 · ADR 21 제목 §4 · 헌법 `judgments/gingoa/` |
| `2026-08-24-harness-cleanup/goppi/` | 22MB | **원격 삭제됨** · 로컬 사본 | 결정 41 제목 §4 · references `sources/goppi/` · 5조 계약 `judgments/goppi/` |
| `2026-08-24-harness-cleanup/goppi_test/` | 319MB | LedgerLens 레거시 (하네스 아님) | ❌ 승계 안 함 — 후속 저장소 `~/divtadel`이 운영판이다 |
| `2026-08-24-harness-cleanup/goppi_final/` | 42MB | **마지막 세대** · 원격은 처음부터 없었다 | **이 저장소의 모체** — `corpus/`·`legacy/`·`direction/`이 전부 여기서 나왔다. 처분 전수는 [`DISPOSITION.md`](DISPOSITION.md) |
| `harness-removal-2026-08-24/` | 560KB | **설정 제거 백업** — Claude·Codex 설정 7종 + SHA256 + 플러그인 캐시 | 절차는 [`judgments/harness-removal-record-2026-08-04.md`](judgments/harness-removal-record-2026-08-04.md)(선례) |

## 2026-08-24 제거 실행 기록

| 단계 | 결과 |
|---|---|
| 실제 상태 조회 | 선례의 교훈대로 문서가 아니라 시스템에 물었다 — **Codex `config.toml`의 `trust_level` 4블록과 `writable_roots`의 `gingoa`** 를 그렇게 찾았다(문서만 봤으면 놓쳤다) |
| 백업 + 해시 | `harness-removal-2026-08-24/` · 설정 7종 · SHA256 |
| goppi 플러그인 제거 | 흔적 **0건** — 플러그인·pluginUsage·projects 4건·캐시·Codex 설정 |
| 로컬 4개 → Archive | claudeck · gingoa · goppi · goppi_test |
| **원격 3개 삭제** | ✅ **API 404로 확인** (claudeck · gingoa · goppi) |
| `goppi_final` | ✅ **이동 완료 2026-08-24** — 홈에 하네스 0건 |

## 원칙

**검증 가능성은 이 저장소에, 산출물은 아카이브에.** `legacy/`의 주장은 여기 없이도 되짚을 수 있어야 한다 —
그래서 커밋 목록·파일 목록·기록 본문은 승계했고, 코드 본문과 바이너리 백업은 안 했다.

⚠️ **아카이브가 사라져도 이 저장소의 인용은 깨지지 않는다.** 다만 *원본 대조*는 불가능해진다 —
그 한계는 각 승계 문서가 명시한다.

## 아카이브를 지우려면

`~/Archive/`는 **이 저장소의 삭제 계획 대상이 아니다.** 지우려면 위 표의 "승계된 것" 열이
전부 채워져 있는지 먼저 확인하라. `GOPPI_state`만 승계 없이 비어 있고, 그것은 의도적이다.
