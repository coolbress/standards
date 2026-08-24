# legacy/sources/ — 과거 하네스 리서치 원본 이관

과거 하네스 4대(claudeck v1 → claudeck → gingoa → goppi)에서 가져온 리서치 원본.
**파일 내용은 바이트 수정 없이 사본 그대로** — 출처·시점·성격은 이 표가 기록한다.
(gingoa의 리서치는 여기가 아니라 `../corpus/`로 통째로 승계 — 그쪽 PROVENANCE.md 참조)

| 파일 | 원 위치 | 작성 시점 | 성격 |
|---|---|---|---|
| `claudeck-v1/harness-notes.md` | `~/Archive/claudeck-v1.git` HEAD `docs/harness-notes.md` | ~2026-06 | 하네스 개념·운영 노트 (v1 시절) |
| `claudeck-v1/researcher.md` | 같은 아카이브 `agents/researcher.md` | ~2026-06 | 리서치 방법론 에이전트 — 쿼리 스코핑(제품명→학술 도메인 재스코핑) 규율은 A/B 검증됨(goppi design §8이 인용). **처리 완료 2026-08-02**: EVIDENCE-POLICY와 차이표 → 고유 규칙 3개(도메인 스코핑·검색 예산·미검증 라벨 fallback)를 `corpus/methods/EVIDENCE-POLICY.md` "Search craft" 절로 흡수, 원본은 여기 보존 |
| `claudeck/harness-concept-notes.md` | `~/claudeck/.scratch/` | 2026-06 | **통합 하네스 연구서** (2,061줄): PART 0 "프로덕션급 소프트웨어" 정의(6개 권위 표준 렌즈를 상호 맹검 6개 에이전트로 조사→교차 수렴) · I 하네스 개념 · II 패키지 구조 · III 채택률 census(455 repo→27 구조조사) · IV 14개 컴포넌트 시공 표준 · V (당시의) 설계 |
| `goppi/standards.md` | `~/goppi/docs/standards.md` | 2026-07-17 (Part B는 스냅샷, 만료 조건 자체 명시) | Part A 전문가 inception 기준선(1차 출처 기반) + Part B 경쟁 지형(SDD 도구 시장) — Evidence/Expiry 블록 포함 |
| `goppi/what-is-a-harness.md` | `~/goppi/.scratch/` | 2026-07 | 하네스 개념 에세이 (goppi design.md로 **superseded** — 배경 자료) |
| `goppi/design.md` | `~/goppi/docs/design.md` | 2026-07 | goppi의 설계와 그 안의 리서치 결론. **적용/판단 문서이며 객관 corpus가 아님** |
| `goppi/references/` (10) | `~/goppi/references/` | 2026-07 | Evidence 블록을 가진 goppi 운영 reference. **적용 산출물** |
| `goppi/harness-eval-results/` (26) | `~/goppi/evals/harness-eval/results/` | 2026-07-22–08-02 | harness-vs-vanilla 비교, ablation, mutation, coverage, false-completion 등 실증 결과 원본 |

## 이관하지 않은 것 (위치만 기록)

- `~/goppi/.scratch/goppi-notes.md` — 실험노트(적용 로그, 리서치 아님).
- `~/goppi/.scratch/design.ko.md` — 설계 원본(한국어), 리서치 아님.
- `~/Archive/claudeck-v1.git`의 나머지 (272파일) — 제품 문서·에이전트·평가 벤치. 필요 시 `git show HEAD:<path>`로 추출.

## 무결성 검증

2026-08-02에 기존 5개 imported 문서와 새 goppi design/references/eval 결과를 원본과 SHA-256 또는
directory diff로 대조했다. 결과는 `../audit/imported-integrity.tsv`에 기록한다. imported는 source copy일
뿐 endorsement가 아니며, active claim으로 쓰려면 corpus policy에 따라 현재 1차 자료로 다시 검증한다.

## 다음 처리

각 원본을 통째로 corpus에 복제하지 않는다. `../audit/GAPS.ko.md`의 research unit이 필요한 claim만
현재 출처로 재검증해 claim register에 접목한다. 특히 goppi eval 결과는 R0-5 worth hypothesis의 가장
직접적인 로컬 empirical evidence지만, task 설계와 grader 자체도 독립 검토해야 한다.

## 계보

**[`LINEAGE.md`](LINEAGE.md)** — claudeck → gingoa → goppi → goppi_final 네 하네스가 무엇을 하려 했고 왜 죽었는지. 원본 저장소(로컬·원격)는 2026-08-24에 삭제됐고, 이 문서가 그 자리를 대신한다. 결정 64건의 제목 목록과 되살릴 수 없는 실측 수치를 포함한다.


## 2026-08-24 가지치기 — 무엇이 남았고 왜인가

원본 저장소 삭제와 함께 **인용되지 않는 32개 파일을 지웠다.** 남긴 기준은 하나다 —
**살아있는 문서가 실제로 인용하는가.**

| 남은 것 | 왜 |
|---|---|
| `LINEAGE.md` | 네 하네스의 계보. 삭제된 것들을 대신한다 |
| `claudeck/·claudeck-v1/` 3건 | 코퍼스가 `[census: claudeck v1]`로 인용하는 초기 관찰 (서브에이전트 권한 릴레이 부재 등) |
| `goppi/` 5건 | `design.md`·`standards.md`·`what-is-a-harness.md`·`model-roster.md`·`review-precision.md` — 인용됨 |
| `goppi-trial-web/` 전체 | G4 실물 확증의 **물증** — 세트로 의미가 있어 통째로 유지 |

**지운 것**: 하네스 eval 결과 23건(하네스 효과 측정 · n=1 · 하네스와 함께 소멸) ·
하네스 참조 문서 9건(폐기된 구현의 설계) · 트랜스크립트.
핵심 수치는 `LINEAGE.md` §5에, 방법론은 `corpus/census-data/harness-confirmation-trial/`에 남아 있다.
