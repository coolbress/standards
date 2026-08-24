# judgments — 과거 하네스의 판단 (⚠️ 대부분 **폐기된 하네스의** 판단이다)

이 층은 근거(`corpus/`)와 분리된 **판단**을 담는다. 다만 현재 내용은 **거의 전부
2026-06~08의 goppi/gingoa가 내린 판단**이며, 그 프로젝트들은 폐기됐다.

## 현행 방향은 여기가 아니다

> **`direction/`이 현행이다.** 둘이 충돌하면 `direction/`이 이긴다.
> 이 층은 *"그때 무엇을 어떻게 판단했나"* 의 기록으로 읽는다.

## 구성

| 경로 | 무엇 | 지위 |
|---|---|---|
| `00-overview.md` ~ `05-goppi-analysis.md` | SDLC · 엔지니어링 실무 · 기획 · 솔로/AI개발 해석 | 대부분 `SUPERSEDED` 표기됨 — 사실 부분은 `corpus/aspects/*/facts-2026-08-*.md`로 이관 |
| `goppi-final-decisions.md` | **결정 로그** — 맥락·결정·**기각한 대안**·사유. §C(Rabbit holes)가 이 계보의 사인을 예언했다: *"메타 잠식 — 구 goppi의 사망 모드이자 이 프로젝트 최대 리스크"* | **여기부터 읽어라.** 기각의 이유는 재사용된다 |
| `foundation/` | **goppi의 설계 결정** — 워크플로 표준 rev4 · 가치가설 · 산출물 루브릭 · 조향 설계 | **역사 기록.** 단, 방법론(6스테이션·AC 추적성·위험비례)은 `direction/03`이 선별 인용한다 |
| `legacy/` | gingoa 전용 스키마·분류·생명주기 | 역사 기록 |

## 왜 지우지 않았나

`foundation/goppi-workflow-standard.md`는 **cross-vendor 적대 리뷰(Codex/GPT-5.6)를 거쳐 rev4까지 간
설계 문서**다. 하네스는 죽었지만 **그 안의 방법론 일부는 살아 있다** — 특히 인수기준 안정 ID와
`AC-n → 검사` 매핑, `UNVERIFIABLE` 표기 규칙(WF-01). `direction/03-what-research-says.md`가
그 조각들을 근거로 인용한다.

**인용할 때 규칙**: 이 층의 문서는 *판단*이지 근거가 아니다. 사실이 필요하면 `corpus/`로 간다.
