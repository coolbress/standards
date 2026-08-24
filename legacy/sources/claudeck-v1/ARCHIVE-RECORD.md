# claudeck-v1 — 아카이브 기록 (계보 인용의 근거)

`legacy/LINEAGE.md` §1·§3이 claudeck-v1에 대해 주장하는 수치는 **이 폴더의 기록으로 검증 가능하다.**
원본 bare 저장소(`~/Archive/claudeck-v1.git`, 11MB)는 **로컬에만 있고 이 저장소 밖이다** —
그래서 인용이 원본에 의존하지 않도록 검증 가능한 부분만 여기 옮겼다.

| 파일 | 무엇 | 무엇을 검증하나 |
|---|---|---|
| `GIT-HISTORY.tsv` | 전 커밋 해시·날짜·제목 (190행) | 커밋 수 · 기간 · **세대 중첩**(188/190이 claudeck 이전) |
| `FILE-MANIFEST.txt` | HEAD의 파일 경로 전수 (272행) | 규모 · 구성(`hooks/scripts` 52 · `eval/review-bench` 등) |
| `README-v1.md` | v1의 README 원문 | 자기 서술 — *"Your command deck for vibe-coding with Claude Code"* |
| `harness-notes.md` · `researcher.md` | 운영 노트 · 에이전트 정의 | 코퍼스가 `[census: claudeck v1]`로 인용하는 관찰 |

## 원본에 대해

- **위치**: `~/Archive/claudeck-v1.git` (bare) · **origin: `~/.claude`** — 전역 하네스를 그대로 버전 관리했다
- **원격 GitHub 저장소 `coolbress/claudeck-v1`은 이미 삭제됨**(404)
- **이 로컬 아카이브가 유일본이다.** 파일 본문(272개)이 필요하면 `git show HEAD:<path>`
- ⚠️ **백업이 없다.** 디스크가 죽으면 사라진다 — 위 3개 파일만이 이 저장소에 남는다

## 왜 272파일을 통째로 안 옮겼나

`legacy/` 규칙(계보이지 승인이 아니다)과 2026-08-24 처분 원칙(*소스코드는 버린다*)을 따른다.
**검증 가능성만 확보하고 산출물은 옮기지 않는다** — 계보의 주장을 되짚는 데 필요한 것은
커밋 목록과 파일 목록이지 코드 본문이 아니다.
