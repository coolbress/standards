# standards — 근거 코퍼스

소프트웨어를 **현업 팀처럼 만들기 위한 근거**를 모아 둔 저장소다. 28개 측면(aspect)에 걸쳐
"현업 시니어는 실제로 무엇을 하는가"를 표준 문서·1차 출처·저장소 census로 정리했고,
각 주장에는 **출처·범위·근거 등급·불확실성**이 붙어 있다.

원래 `goppi_final/.scratch/research/`에 있었다. 2026-08-24에 이곳으로 추출했다 —
그 폴더는 `.gitignore` 대상이라 **509k 단어가 버전 관리 밖에 있었고**, 백업 경로가 로컬
tar 스냅샷뿐이었기 때문이다.

## 어디서 시작하나

| 목적 | 파일 |
|---|---|
| 구조를 사람이 훑기 | [`MAP.md`](MAP.md) — 생성물. 등급별 문서 지도 |
| 에이전트 진입점 | [`corpus/INDEX.md`](corpus/INDEX.md) |
| 무엇을 믿을 수 있나 | [`corpus/methods/EVIDENCE-POLICY.md`](corpus/methods/EVIDENCE-POLICY.md) |
| **무엇이 안 바뀌고 무엇이 썩나** | [`RESEARCH-LIFETIME.md`](RESEARCH-LIFETIME.md) — 🟢🟡🔴 수명 등급 |
| 아직 빈 곳 | [`audit/GAPS.ko.md`](audit/GAPS.ko.md) |

## 층위

```
corpus/          근거 — aspect 종합 · claim register · census 원시 데이터
  ├ aspects/     28개 측면 (SWEBOK v4 · ISO/IEC/IEEE 12207:2026 · ISO 25010 앵커)
  ├ census-data/ 저장소 조사 원시 데이터 (append-only)
  └ methods/     근거 정책 · 프레임워크 crosswalk
interpretation/  판단 — 근거와 **분리**된 결정 기록
imported/        과거 하네스(claudeck·gingoa·goppi) 원본 사본 — 계보용, 승인 아님
audit/           감사 기록 · 공백 추적 · 무결성 대장 (append-only)
archive/         활성 검색에서 뺐지만 복구 가능한 자료
tools/           구조 검증 · 지도 생성 · 검색 계약 평가
```

## 절대 규칙

1. census의 **보급률**과 좋은 practice를 동일시하지 않는다.
2. 공식 제품 문서를 **제품 효과성**의 증거로 쓰지 않는다.
3. `review-needed`나 `draft`를 검증된 결론으로 인용하지 않는다.
4. 합성 판단은 `synthesis`, 프로젝트 선택은 `interpretation/`으로 표시한다.
5. 새 연구는 **질문·검색일·포함/제외·claim-source 관계·시효·종료 기준**을 갖는다.

## 검사

```bash
python3 tools/validate_corpus.py        # 구조·프론트매터·매니페스트·URL 대장
node    tools/build-routes.mjs --check  # 라우팅 지도 최신 여부 (낡으면 exit 1)
python3 tools/external_url_audit.py     # 외부 URL 생사 (네트워크 · ~7분)
```

CI가 앞의 둘을 매 push/PR에 돌린다. URL 감사는 월 1회.
문서를 고쳤다면 `tools/rebuild_after_manifest.py`와 `build-routes.mjs`를 다시 돌려야 검증이 통과한다.

## 알려진 상태

- 상속된 `verified` 50건은 2026-08-02 감사에서 `review-needed`로 내렸다. 원자 claim 승격 전이다.
- 외부 URL 2건이 죽어 있다(ISO 25010 · tessl). 대체 URL 확정은 별도 유닛 — `audit/2026-08-24-host-and-github-delta.ko.md`.
- 28-aspect taxonomy는 provisional이다.
