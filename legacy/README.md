# legacy — 과거 하네스가 남긴 전부

**5세대**(claudeck-v1 → claudeck → gingoa → goppi → goppi_final)가 남긴 것을 한자리에 모았다.
**이 층은 전부 지나간 것이다.** 현행 방향은 [`direction/`](../direction/)이고,
둘이 충돌하면 `direction/`이 이긴다.

## 먼저 읽을 것

**[`LINEAGE.md`](LINEAGE.md)** — 다섯 하네스가 무엇을 하려 했고, 어떻게 지었고, 왜 죽었나.
결정 64건 · 스펙 11종의 제목과 되살릴 수 없는 실측 12건이 여기 있다. **나머지는 이 문서의 각주다.**

## 구성

| 경로 | 무엇 | 어떻게 읽나 |
|---|---|---|
| `LINEAGE.md` | 계보 서사 | **진입점** |
| `judgments/` | 그때 내린 **판단** — goppi 워크플로 표준 rev4 · 가치가설 · 산출물 루브릭 · gingoa 스키마 | 역사 기록. 단 방법론 일부는 `direction/03`이 선별 인용한다 |
| [`DISPOSITION.md`](DISPOSITION.md) | **처분 대장** — 4세대 저장소의 마크다운 274건 전수와 각각의 처분. 미분류 0. (claudeck-v1은 bare 아카이브라 표 밖 — 전수는 `sources/claudeck-v1/FILE-MANIFEST.txt`) | *"누락인가 의도인가"* 를 여기서 확인 |
| [`ARCHIVE-INDEX.md`](ARCHIVE-INDEX.md) | **이 저장소 밖의 로컬 아카이브 목록** — `~/Archive/`에만 있고 백업이 없는 것들 | 무엇이 승계됐고 무엇이 안 됐나 |
| `sources/` | **원본 사본** — claudeck·goppi 관찰 노트, goppi-trial-web 물증 | provenance이지 승인이 아니다 |

## 인용 규칙

1. 이 층의 문서는 **판단이거나 역사**다. 사실이 필요하면 [`corpus/`](../corpus/)로 간다.
2. 여기 담긴 설계·주장은 **현행 근거가 아니다.** 인용하려면 현재 코퍼스에서 재확인해야 한다.
3. `sources/`의 파일은 **고쳐 쓰지 않는다.**

## 왜 지우지 않았나

- **`LINEAGE.md`** — 이 저장소 목적의 절반(계보·실패 분석)이 여기 있다.
- **`judgments/foundation/workflow-standard.md`** — cross-vendor 적대 리뷰를 거쳐 rev4까지 간
  설계 문서다. 하네스는 죽었지만 **인수기준 안정 ID · `AC-n → 검사` 매핑 · `UNVERIFIABLE` 표기**(WF-01)는
  살아 있고 `direction/03`이 근거로 인용한다.
- **`sources/`** — 코퍼스가 실제로 인용하는 것만 남겼다(2026-08-24 가지치기에서 32건 삭제).
  `goppi-trial-web/`은 실물 확증의 **물증**이라 세트로 유지한다.
