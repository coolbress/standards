# archive — 복구 스냅샷 (2026-08-24 처분)

**여기 있던 tar.gz 스냅샷 3개(8.7MB)를 지웠다.**

## 왜 있었나

코퍼스가 `goppi_final/.scratch/`에 있던 시절, **버전 관리 밖이라 롤백 경로가 스냅샷뿐이었다.**
`corpus/_schema.md`가 그 사정을 적고 있다 — *"The tree is not under version control,
so the snapshot is the only rollback path."*

## 왜 지웠나

**2026-08-24에 git 저장소가 됐다.** 이제 롤백 경로는 git 이력이고,
스냅샷은 같은 일을 8.7MB 더 무겁게 하는 중복이다.

| 스냅샷 | 무엇을 되돌리려던 것 |
|---|---|
| `2026-08-02/pre-curation-snapshot.tar.gz` | 코퍼스 큐레이션 전 상태 |
| `2026-08-08/pre-rename-snapshot.tar.gz` | `_aspect.md` → `--overview.md` 개명 전 |
| `2026-08-08/pre-structure-snapshot.tar.gz` | 구조 개편 전 |

⚠️ **정직 고지**: git 이력은 **2026-08-24 추출 시점부터** 시작한다. 그 이전 상태
(2026-08-02·08-08의 개편 전 트리)는 **이 저장소로 되돌릴 수 없다.**
해시와 파일 수는 [`../audit/ARCHIVE-LEDGER.md`](../audit/ARCHIVE-LEDGER.md)에 남는다 —
**되돌릴 수는 없고 무엇이 있었는지는 안다.**
