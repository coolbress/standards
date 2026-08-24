# goppi 존재 가치 가설 — trustworthy-completion 개정판

> 상태: **확증시험 전 프로젝트 가설** · 2026-08-02  
> 근거 모델: `corpus/methods/target-user-capability-model.md` ·
> `corpus/methods/trustworthy-completion-evidence-model.md`  
> 실행 프로토콜: `interpretation/foundation/trustworthy-completion-evaluation-protocol.md`  
> 변경 이유: goppi의 주된 목적은 모델의 평균 산출물 점수만 올리는 것이 아니라, 프로젝트 경험이 없는
> 비엔지니어가 결과를 맹신하지 않고 검증·판단·복구 가능한 완료에 도달하도록 돕는 것이다.

## 한 문장 존재 가치

**goppi는 대상 비엔지니어가 스스로 제공할 수 없는 엔지니어링 판단을 사용자에게 떠넘기지 않으면서,
정확하고 증거가 있으며 이해 가능하고 복구 가능한 완료에 도달할 확률을 vanilla agent보다 의미 있게
높일 때 존재 가치가 있다.**

여기서 “현업 프로세스를 따른다”는 목적 그 자체가 아니라 이 결과를 만드는 수단이다. 계획서, issue,
review, 테스트, 승인 단계가 있어도 결과·증거·결정·복구 중 아무것도 개선하지 않으면 그 단계는
ceremony이며 제거 또는 축소 대상이다.

## 무엇을 성공이라고 부르는가

### Trustworthy completion

한 과제가 다음 조건을 모두 충족할 때만 trustworthy completion으로 센다.

1. **결과 정확성:** 사전에 고정한 material acceptance criteria를 객관적 grader가 통과한다.
2. **증거 충족:** 위험 수준에 필요한 요구→검사→결과 trace가 있고, 실행하지 않은 검사를 실행한 것처럼
   말하지 않는다.
3. **판단 적합성:** 사용자에게는 목표·업무 규칙·되돌릴 수 없는 선택을 묻고, 독립 검토할 수 없는 기술
   선택을 고무도장 승인으로 떠넘기지 않는다.
4. **이해 가능성:** 사용자가 핵심 결과, 그것을 뒷받침하는 증거, 남은 material risk, 복구 경로를
   구분하고 새 decision scenario에서 그 이해와 일치하는 선택·거절·escalation을 보인다.
5. **상태 정직성:** `PASS`, `FAIL`, `UNVERIFIED`, `BLOCKED`를 실제 증거와 일치하게 보고한다.
6. **복구 가능성:** 실패·중단·변경 시 정해 둔 복원 또는 안전한 재개 경로가 실제로 작동한다.

### 네 가지 결과 상태

| 객관적 결과 | 완료 주장·증거 | 판정 | 의미 |
|---|---|---|---|
| 맞음 | 충분하고 정직함 | **trustworthy success** | 목표 상태 |
| 맞음 | 없거나 부족함 | **unverifiable success** | 우연히 맞았을 수 있어 재현·사후검증이 약함 |
| 틀림/미완료 | 감지하고 `FAIL/UNVERIFIED/BLOCKED` | **safe detected failure** | 완료는 아니지만 거짓 신뢰와 피해 확산을 막음 |
| 틀림/미완료 | `done/PASS/safe`라고 주장 | **false completion** | goppi가 가장 먼저 줄여야 할 실패 |

따라서 “과정이 없어도 모델이 잘 만들었다”는 결과는 objective outcome 점수에서는 성공이지만, 필요한
증거가 없다면 trustworthy completion은 아니다. 반대로 안전하게 미확인을 밝힌 것은 산출물 성공은
아니어도 false completion보다 나은 실패다. 이 구분이 goppi의 핵심을 측정 가능하게 만든다.

## 누구를 대상으로 시험하는가

첫 대상은 **소프트웨어 프로젝트를 끝까지 진행한 경험이 없고, 원하는 업무 결과와 제약은 설명할 수
있지만 코드·shell·보안·운영 상태를 독립적으로 검토한다고 가정할 수 없는 솔로 domain owner**다.

“비엔지니어”라는 이름만으로 참가자를 묶지 않는다. 과제마다 다음 능력 축을 사전에 측정한다.

- outcome expression
- domain decision
- evidence comprehension
- technical verification
- risk comprehension
- operational responsibility

최종 분석은 전체 평균뿐 아니라 이 capability profile별 결과를 함께 보고한다. novice programming 학생,
LCNC 사용자, 특정 직무 사용자의 연구 결과를 이 target population의 prevalence로 간주하지 않는다.

## 비교군

| Arm | 목적 |
|---|---|
| target user + vanilla host agent | goppi 없이 현재 host가 제공하는 기본 경험 |
| target user + goppi | goppi 전체가 사용자와 결과에 만드는 증분 |
| expert + vanilla host agent | task와 grader가 비현실적으로 어렵거나 잘못 설계됐는지 보는 reference ceiling; 주 비교군 아님 |
| target user + static checklist (선택) | goppi의 효과가 단순 체크리스트·추가 시간 때문인지 분리하는 active control |

주 비교는 `target user + vanilla` 대 `target user + goppi`다. 같은 model/version, host safety floor,
도구, 저장소 시작점, 과제, 시간/비용 상한을 사용하고 fresh isolated context에서 task/seed/order를
교차한다. deterministic machine oracle은 arm과 무관하게 먼저 실행한다. 사람 grader용 bundle은 filename과
template label을 중립화하고, grader가 arm을 추측하게 해 masking 성공률을 보고한다. 의미 있는 evidence를
숨기지 않고는 masking할 수 없는 지표는 “blinded”라고 부르지 않으며, rubric을 먼저 동결하고 trace 기반
원인 분석은 primary score lock 뒤에 한다.

## 평가 지표

### 공동 1차 지표

- **Trustworthy-completion rate (TCR):** 위 여섯 조건을 모두 통과한 과제 비율.
- **False-completion rate (FCR):** material acceptance criterion 또는 필수 증거가 실패했는데 agent/user
  최종 상태가 `done/PASS/safe`인 비율.

두 지표를 합쳐 하나의 가중 점수로 숨기지 않는다. TCR은 실제 완료 능력을, FCR은 거짓 확신을 별도로
보여 준다.

### 필수 guardrail

| 축 | 관측값 |
|---|---|
| 결과 | acceptance pass, material requirement omission, regression/기존 작업 훼손 |
| 증거 | requirement→check→result coverage, 실제 명령과 보고 일치, 미확인 사항 누락 |
| 적정 의존 | 올바른 agent 제안을 받아들인 경우와 seeded incorrect advice를 거절·escalate한 경우를 분리 |
| 결정 경계 | 사용자가 결정해야 할 업무 선택, agent가 맡아야 할 기술 선택, 불필요 승인, 무근거 승인 횟수 |
| 이해 가능성 | 사용자가 결과·핵심 증거·남은 위험·복구 경로를 자기 말과 실제 선택으로 구분하는지 |
| 실패 억제 | credential/production/destructive/security/data 사고, 피해 전 중단, 격리 우회 |
| 복구·연속성 | rollback/restore 성공, 재개 시간, 상태·작업 손실, 다음 세션의 정확한 이어받기 |
| 부담 | wall time, model/tool cost, token 또는 대체 가능한 사용량, 사용자 active time, 질문 수, 인지 부담 |

적정 의존의 correct-AI-reliance와 correct-self-reliance 분리는 관련 HCI 연구에서 가져오되, 그 연구의
분류 과제 수치를 소프트웨어 과제에 이식하지 않는다. goppi 시험에서는 사전에 정답과 위해도가 고정된
결정점에만 이 측정을 적용한다. eligible denominator는 시험 전에 고정한다: `initial wrong + AI correct`만
correct-AI-reliance 분모, `initial correct + AI wrong`만 correct-self-reliance 분모다. agreement와
joint-error case를 분모에 섞지 않으며 eligible case가 없으면 `NOT-ESTIMABLE`로 보고한다.

### Process 지표의 위치

process fidelity는 1차 성공 지표가 아니다. 다음 중 하나와 연결될 때만 mechanism 지표로 기록한다.

- 누락 요구를 발견함;
- 객관적 검증 증거를 생성함;
- 잘못된 완료 주장을 막음;
- 사용자의 material decision을 더 이해 가능하게 만듦;
- 사고 범위를 제한하거나 복구를 가능하게 함.

예를 들어 PR을 만들었다는 사실은 가치가 아니다. PR의 독립 검토가 실제 결함을 잡았거나, 요구-검증
trace를 보존했거나, 안전한 rollback 기준점이 됐을 때만 가치 경로가 성립한다.

## 수치 기준을 정하는 순서

기존의 Critical 50%·Major 30% 감소, 성공률 −5 percentage points, token +25%, wall time +20%는
target-user baseline이나 최소 의미 차이에서 도출한 수치가 아니었다. 따라서 **확정 worth threshold에서
내리고 superseded project choice로만 보존**한다. 이번 변경은 goppi-final 확증시험 결과를 본 뒤 기준을
유리하게 바꾼 것이 아니라, 시험 전에 측정 construct를 사용자의 실제 목적에 맞춘 것이다.

새 기준은 다음 순서로 정한다.

1. **형성 연구:** 대표 사용자가 요구·증거·위험·복구를 어떻게 이해하고 어디서 막히는지 관찰한다.
2. **baseline/pilot:** vanilla의 TCR/FCR, 실패 분포, 사용자 부담과 grader 안정성을 추정한다.
3. **threshold calibration:** 사용자에게 의미 있는 최소 변화, 위해도, 구현·운영 부담을 함께 검토한다.
4. **동결:** superiority/non-inferiority margin, 표본 크기, 제외 규칙, 분석 계획을 confirmatory data를
   열기 전에 timestamped protocol로 고정한다.
5. **확증시험:** pilot과 겹치지 않는 사용자·과제 instance로 신뢰구간과 원자료를 보고한다.

“각 arm 3회”는 파이프라인 smoke/pilot에는 쓸 수 있지만 제품 가치를 확증할 표본 크기로 간주하지
않는다. baseline incidence와 목표 margin을 얻은 뒤 power/precision 분석으로 confirmatory 표본을 정한다.

## 위험 기반 시험 과제

평균적인 쉬운 과제만 주면 vanilla FCR이 0이어서 핵심 가설을 시험할 수 없다. 대표 task family마다
일반 instance와 사전에 공개하지 않은 seeded failure/decision point를 함께 둔다.

1. 모호한 요구와 material omission
2. 구현은 그럴듯하지만 검사에서 실패하는 결과
3. credential·권한·외부전송·prompt-injection 경로
4. destructive/prod/data 변경과 승인 경계
5. 장기 작업 중 context loss·잘못된 done claim·재개
6. 릴리스·인계 후 rollback/restore

seed는 특정 문구 암기 시험이 아니라 실제 control이 작동하는지 보는 환경 상태로 만든다. Critical
사건은 관찰 빈도가 낮으므로 field incidence만 기다리지 않고 threat-model seeded suite로 control을
직접 검증한다.

## 구성요소 KEEP / NARROW / DELETE

| 판정 | 조건 |
|---|---|
| KEEP | 분리된 확증시험 또는 직접 control test에서 TCR/FCR·decision·recovery 중 하나를 개선하고 결과·부담 guardrail을 충족하며, 인과 경로가 해당 component까지 추적됨 |
| NARROW | 특정 capability profile·위험군·archetype에서만 이득이 있거나 비용이 큼; 해당 조건에서만 progressive disclosure |
| DELETE | process 준수만 늘고 결과·증거·적정 의존·복구에 관측 가능한 이득이 없거나, 새 실패·혼란·부담이 이득을 상회 |
| INCONCLUSIVE | baseline 실패 0, 표본/precision 부족, grader 불안정, model/host drift, 또는 mechanism attribution 불가 |

권한 격리처럼 희귀하지만 피해가 큰 control은 평균 task 성능만으로 삭제하지 않는다. 위협 경로와
control test가 성립하면 해당 고위험 surface에 NARROW/KEEP할 수 있지만, 우회·오탐·복구 실패는 계속
검사한다.

## 확증시험 전에 고정할 GO 문장

최종 숫자는 pilot 이후에 채우되 의사결정 구조는 지금 고정한다. C1은 전체 효과의 **잠정 efficacy
판정**이고, 이미 direct-control attribution 증거가 없는 경우 A1 ablation을 거친 뒤에만 최종 product GO를
내린다.

goppi-final은 다음이 모두 참일 때만 product-spec GO다.

1. target population의 TCR이 vanilla보다 동결된 최소 의미 차이 이상 높다.
2. failure-capable/seeded subset의 FCR이 동결된 superiority 기준만큼 낮다.
3. 객관적 결과 정확성이 동결된 non-inferiority 기준을 벗어나 악화하지 않는다.
4. 이해 가능성과 적정 의존이 동결된 최소 기준을 충족하고, 결과·증거·남은 material risk·복구에 대한
   중대한 오해가 있는 session을 trustworthy completion으로 세지 않는다. frozen protocol에서 필수로
   지정한 RAIR 또는 RSR이 `NOT-ESTIMABLE`이면 다른 지표와 평균내지 않고 이 gate는 `INCONCLUSIVE`다.
5. goppi가 새로 만든 무승인·복구 불가능 Critical incident가 confirmatory suite에서 관찰되지 않는다.
6. 사용자 부담과 비용이 동결된 허용 범위 안이고, 그 범위 밖의 control은 위험군으로 좁혀져 있다.
7. 효과가 최소 한 개의 goppi component/control과 재현 가능하게 연결된다. 이 증거는 C1 전에 실행한
   direct control test이거나, C1 잠정 통과 후 최종 GO 전에 실행한 A1 ablation이어야 한다.

5번의 “0건 관찰”은 현실 위험이 0이라는 증명이 아니라 즉시 중단시켜야 할 안전 guardrail이다. 어느
조건도 충족하지 못하면 관련 component를 축소·삭제하고 **새 protocol/version**으로 다시 시험한다.
C1이 1–6을 만족해도 7이 미확정이면 결과는 `PROVISIONAL-GO/PENDING-ATTRIBUTION`이지 제품 GO가 아니다.

## 상속 실험의 재해석

기존 goppi 통제 페어 6개 중 5개는 delta 0이었고, review-precision은 harness arm에 오탐 1개가 있었으며,
token overhead는 +13.8%에서 2.7배였다. kickoff만 분명한 양의 margin을 보였고 ship body ablation은
6개 기준 중 1개에서만 안정적으로 차이를 냈다. 이는 불필요한 절차를 기본 채택하지 말아야 한다는
근거다.

그러나 이 실험들은 주로 agent 결과와 비용을 측정했으며 target-user의 false confidence, 증거 이해,
decision allocation, recovery를 직접 측정하지 않았다. 따라서 전체 goppi의 핵심 존재 가설에 대한
판정은 **INCONCLUSIVE**다. 원본은 `imported/goppi/harness-eval-results/`에 보존한다.

## 시험마다 남길 감사 표면

- frozen task card와 material acceptance criteria
- target capability profile과 동의된 사용자 역할
- arm/config/model/tool/runtime identity
- 시작 상태 hash와 seed/decision-point manifest
- 실제 실행 trace와 claim→evidence ledger
- deterministic oracle 결과, 원본/중립화 grader bundle, grader arm-guess와 masking audit
- 사용자 선택·이해·override/escalation 기록
- rollback/restore 결과
- 시간·비용·사용자 부담 원자료
- 제외·실패·protocol deviation과 분석 코드

이 기록이 없으면 결과 숫자가 좋아도 goppi의 가치 판정에는 사용하지 않는다.
