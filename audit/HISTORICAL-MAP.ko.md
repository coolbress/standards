# 과거 하네스 리서치 계보와 현재 배치

이 문서는 claudeck v1 → claudeck → gingoa → goppi 자료를 “모두 최신 사실”로 합치는 대신,
각 자료를 **원본 증거, 현재 검토 대상, 설계 해석** 중 어디에 둘지 추적한다. 원본 사본은
`../imported/`, gingoa 계보의 활성 문서는 `../corpus/`, 프로젝트 적용 문서는
`../legacy/judgments/`에 있다.

## 판정 규칙

- **원본 보존**: 과거에 실제로 무엇을 조사·측정·결정했는지 증명한다. 내용의 현재성은 보증하지 않는다.
- **claim 후보**: 현행 1차 자료나 재현 실험으로 다시 검증한 뒤에만 active `verified` claim이 된다.
- **interpretation**: goppi/gingoa에 어떻게 적용할지에 관한 판단이다. 객관적 사실 corpus와 분리한다.
- **superseded**: 계보 이해에는 유용하지만 현재 설계 근거로 직접 사용하지 않는다.

## 세대별 crosswalk

| 세대 / 원본 | 현재 위치 | 연결되는 현재 영역 | 판정과 다음 단계 |
|---|---|---|---|
| claudeck-v1 `harness-notes.md` | `legacy/sources/claudeck-v1/` | aspect 27 control/state/security/lifecycle | historical 원본. 제품 동작은 R0-3/R1-5에서 현행 공식 문서로 재검증 |
| claudeck-v1 `researcher.md` | `legacy/sources/claudeck-v1/` | `methods/EVIDENCE-POLICY.md` | 방법론 prior art. 새 정책과 중복 비교 후 고유 규칙만 승계 |
| claudeck `harness-concept-notes.md` | `legacy/sources/claudeck/` | aspects 22, 27; census 계보 | 14-component taxonomy/census는 claim 후보, PART V 설계는 interpretation |
| gingoa research corpus | `corpus/` | 28 stable aspect paths | 구조는 승계, inherited 50문서는 `review-needed`; gingoa 적용 절은 legacy로 분리 |
| goppi `standards.md` | `legacy/sources/goppi/` | methods, aspects 01/04/05/08/09/17/22/24/27 | 1차 자료 연결은 재사용 후보, 제품·시장 사실은 만료 검토, goppi 규범은 interpretation |
| goppi `what-is-a-harness.md` | `legacy/sources/goppi/` | aspect 27 | `design.md`에 의해 superseded된 개념 에세이 |
| goppi `design.md` | `legacy/sources/goppi/` | R0-5 worth hypothesis, 전체 설계 | 현재 요구·판단의 기록. 객관 corpus에 직접 병합하지 않음 |
| goppi `references/` 10개 | `legacy/sources/goppi/references/` | security, review, verification, scaffold, sandbox, publishing | 적용 reference. 각 규칙은 해당 P0/P1 unit에서 source-to-claim 재심사 |
| goppi harness eval 원본 | `legacy/sources/goppi/harness-eval-results/` | R0-5, R1-4, R1-5 | 가장 직접적인 로컬 empirical evidence. n, isolation, scorer, 반복성 한계까지 함께 승계 |

## goppi eval 결과군 전수 배치

| 결과군 | 포함 원본 | 현재 연결 | 사용 제한 |
|---|---|---|---|
| harness-vs-vanilla pair | `delivery-hygiene*`, `clear-request-silence*`, `false-completion*`, `kickoff-second-scenario`, `kickoff-third-arm`, `review-precision`, `n1-ship-body-ablation` | R0-5 worth hypothesis | 대개 작은 n의 task-local 결과. 다른 host/task로 일반화 금지 |
| token/body cost measurement | `c1-review-slim-remeasure`, `g1-skill-body-sweep`, `g5-token-calibration`, `ship-body-measurement`, `h1-body-remeasure`, `i1-scaffold-body-measurement`, `i2-ship-body-measurement` | R0-5 cost/latency budget | 당시 host/tokenizer/skill revision에 종속; 현재 버전 재측정 필요 |
| contract/lifecycle gate | `c2-contract-gate`, `k1-secret-scan-fp-baseline`, `l1-pre-push-lifecycle`, `q5-secret-guard-pinned` | R0-4 security, R1-5 lifecycle | fixture coverage와 false-positive/negative 경계를 같이 보존 |
| mutation/coverage instrument | `o1-mutation-harness`, `t1-harness-coverage`, `t2-harness-coverage-closed` | R1-4 eval methodology | instrument 자체 결함·survivor·blind spot도 결과의 일부 |
| impossibility-claim audit | `u1-impossibility-claim-population` | methods, R1-4 | “검증 불가능” 판단을 모집단 전체로 확대하지 않음 |
| raw transcripts | `2026-07-22-delivery-hygiene-transcripts/{harness,vanilla}.txt` | pair 재현/감사 | 해석 전 원시 출력; active claim 문서로 직접 검색 노출하지 않음 |

## 현재성 결론

과거 자료는 사라지지 않았지만, **원본이 있다는 사실**과 **현재 설계 근거로 유효하다는 판정**을
분리했다. 현재 즉시 `verified`로 사용할 수 있는 보강 문서는
`harness-control-plane-standard.md`와 `github-workflow-current.md`뿐이다. 나머지 inherited 문서는
R0-1을 통과할 때까지 stable path를 가진 검토 대기 자료다.
