> ⚠️ **SUPERSEDED (2026-08-02)** — 이 문서의 사실 부분은 `../corpus/aspects/*/facts-2026-08-*.md`로, 판정 부분은 `../corpus/methods/` 및 `foundation/` 문서로 대체됐다. 역사 기록으로 보존하며, 활성 근거로 인용하지 않는다.

# 현대 소프트웨어 엔지니어링의 일상 실무: 버전 관리, 코드 리뷰, CI/CD, 테스트

> 조사일: 2026-08-02. 1차 출처(Google eng-practices, SWE at Google, trunkbaseddevelopment.com, Martin Fowler, DORA/dora.dev, Scrum Guide, 학술 논문) 중심으로 정리.

## 요약 (핵심 10줄)

1. 고성과 팀의 공통분모는 특정 브랜치 모델이 아니라 **"작게, 자주, 빨리 통합"**이다. DORA 연구상 trunk 기반(활성 브랜치 ≤3개, 하루 1회 이상 trunk 머지, 브랜치 수명 수 시간)이 배포 성과와 상관관계가 있다.
2. Git Flow는 그 창시자조차 2020년에 "지속 배포되는 웹앱이라면 GitHub Flow 같은 단순한 흐름을 쓰라"고 명시했다. 다중 버전 동시 지원 소프트웨어에만 여전히 유효하다.
3. 코드 리뷰의 제1 변수는 엄격함이 아니라 **속도**다. DORA 2023: 리뷰가 빠른 팀은 배포 성과가 50% 높다. Google 규범: 응답은 최대 1영업일, 실제 중앙값은 4시간 미만.
4. 리뷰가 작동하는 전제는 **작은 변경**이다. Google 변경 중앙값 ~24줄, "100줄이 적정, 1000줄은 과대"이며 리뷰어는 크기만을 이유로 반려할 수 있다. 400줄을 넘으면 결함 발견율이 급락한다(SmartBear/Cisco).
5. 최소한의 진짜 CI = 버전 관리된 메인라인 + 자동 빌드 + **자기검증 테스트** + 10분 이내 빌드 + 깨지면 즉시 수리. 이것이 없으면 나머지는 장식이다.
6. Delivery(언제든 배포 가능 상태 유지)와 Deployment(모든 변경 자동 배포)는 다르다. feature flag가 "배포 ≠ 릴리스" 분리를 가능케 하지만, flag는 부채이므로 수명을 짧게 관리해야 한다.
7. 테스트는 피라미드(다수의 빠른 소형 테스트 + 소수의 대형 테스트)가 기본형이다. Google 실측 비율 80/15/5. Testing Trophy는 "통합 테스트의 가성비"를 강조하는 보정이지 피라미드의 부정이 아니다.
8. TDD의 "테스트 먼저" 순서 자체는 실증 연구상 효과가 불분명하다. 효과의 원천은 **잘게 균일한 스텝 + 항상 테스트가 따라오는 것**이다. 현업 준수율도 낮다.
9. "Done"의 실무적 의미 = 머지 전: CI 녹색 + 리뷰 승인. 배포 전: 자동화 파이프라인 통과. 조직의 Definition of Done은 이 품질 기준의 명문화다.
10. 커밋/PR 위생 중 하중을 받는 것(load-bearing)은 "왜"를 담은 설명과 작은 단위이고, Conventional Commits 등 형식 규약은 **자동화가 소비할 때만** 가치가 있다 — 아니면 cargo cult다.

---

## 1. Git 워크플로우: 실제로 쓰이는 것

### 세 가지 모델 비교

| 모델 | 구조 | 현재 위상 |
|---|---|---|
| **Git Flow** | master + develop + feature/release/hotfix 브랜치 | 창시자가 웹앱에 비추천. 버전 지원 소프트웨어(설치형, 임베디드)용으로 축소 |
| **GitHub Flow** | main + 짧은 브랜치 + PR + 머지 후 삭제 | 사실상의 업계 표준 절차. 브랜치를 짧게 유지하면 trunk 기반과 수렴 |
| **Trunk-Based** | 단일 trunk, 직접 커밋 또는 수 시간짜리 단기 브랜치 | DORA가 고성과와 연관성을 확인한 모델 |

- Git Flow 원문(2010)에 저자 Vincent Driessen이 2020년 추가한 "note of reflection": 웹앱은 "지속 배포되고, 롤백하지 않으며, 다중 버전을 지원할 필요가 없으므로" Git Flow를 억지로 끼워 맞추지 말고 **GitHub Flow 같은 더 단순한 워크플로우**를 쓰라. Git Flow는 명시적 버저닝·다중 버전 동시 운영이 필요한 소프트웨어에만 여전히 적합하다. — https://nvie.com/posts/a-successful-git-branching-model/
- GitHub Flow의 6단계: 브랜치 생성 → 변경 커밋 → PR 생성 → 리뷰 반영 → 머지 → 브랜치 삭제. — https://docs.github.com/en/get-started/using-github/github-flow
- Trunk-Based Development: 모두가 단일 trunk에서 협업. 소규모 팀은 trunk 직접 커밋, 규모가 커지면 리뷰/CI용 **단기(수 시간~수 일) 브랜치**를 쓰되 머지 후 즉시 삭제. 장기 develop 브랜치를 두지 않는 것이 핵심이며, CI(하루 1회 이상 통합)의 전제 조건이다. — https://trunkbaseddevelopment.com/

### DORA가 확인한 것 (증거)

- 2016–2017 연구: trunk 기반 개발을 실천하는 팀이 **배포 속도·안정성·가용성 모두에서 더 높은 성과**. 구체 지표: **활성 브랜치 3개 이하, 최소 하루 1회 trunk 머지, 코드 프리즈/안정화 기간 없음**. 개별 브랜치 수명은 "며칠~몇 주"가 아니라 "**몇 시간 이내**"가 목표. — https://dora.dev/capabilities/trunk-based-development/
- DORA가 지목한 trunk 기반의 실패 요인: 다중 승인을 요구하는 무거운 리뷰(→ 개발자가 변경을 몰아서 크게 만듦), 비동기 리뷰 지연(→ 브랜치 수명 연장, 충돌), 자동 테스트 부재(→ trunk 불안정). 즉 **작은 배치 + 빠른 리뷰 + 자동 테스트가 3종 세트**로 있어야 작동한다. — 같은 문서
- 작은 배치 기준: "완료·검증까지 **1주일 넘게 걸리는 코드 배치는 너무 크다**." 시간~2일 단위로 슬라이스(INVEST 원칙), 하루 1회 이상 릴리스 가능한 작은 변경을 trunk에 체크인. — https://dora.dev/capabilities/working-in-small-batches/

**Load-bearing vs ceremony 판정**: 하중을 받는 것은 "브랜치 수명 단축 + 매일 통합"이라는 행동이지 모델의 이름이 아니다. GitHub Flow를 쓰면서 브랜치를 2주 끌면 Git Flow의 단점만 재현하는 것이고, PR 절차 없이도 페어링+직접 커밋으로 고성과를 내는 팀이 있다. **브랜치 다이어그램을 정교하게 그리는 것 자체는 ceremony다.**

---

## 2. 코드 리뷰: Google 방식과 실증 데이터

### 리뷰어가 실제로 보는 것 (Google eng-practices)

Google의 리뷰 항목: **설계**(이 변경이 이 위치에, 지금, 이런 상호작용으로 맞는가) > **기능성**(의도대로 동작하는가, 엣지 케이스·동시성) > **복잡성**("읽는 사람이 빨리 이해할 수 없는 코드"는 반려 — 미래를 위한 과잉 설계 금지) > **테스트**(변경과 함께 오는 유효한 테스트 — 코드가 깨지면 실제로 실패하는 테스트) > **네이밍·주석**(주석은 what이 아니라 **why**) > **스타일 가이드 준수** > **문서 갱신**. — https://google.github.io/eng-practices/review/reviewer/looking-for.html

리뷰의 기준 원칙: 완벽이 아니라 **"코드베이스의 전반적 건강을 확실히 개선하는 상태면 승인"**. 사소한 개선 요구로 머지를 막지 말되, 코드 건강을 악화시키는 변경은 작아도 막는다. — https://google.github.io/eng-practices/review/reviewer/standard.html

### 작은 CL 철학

- 원칙: CL(변경) 하나 = **자기완결적 변경 하나**. "100줄이 대체로 적정, 1000줄은 대체로 과대." 리뷰어는 **크기가 크다는 이유만으로 반려할 재량**이 있다. 작은 CL은 더 빨리·더 꼼꼼히 리뷰되고, 버그가 적고, 반려돼도 낭비가 적고, 롤백이 쉽다. 예외는 자동 리팩토링 도구 출력과 파일 삭제 정도뿐. — https://google.github.io/eng-practices/review/developer/small-cls.html
- 실측(9백만 건 리뷰 분석, "Modern Code Review: A Case Study at Google", ICSE-SEIP 2018): **변경 크기 중앙값 ~24줄**(Microsoft 등 타사 연구보다 훨씬 작음), 소형 변경의 첫 피드백 대기 중앙값 **1시간 미만**, 전체 리뷰 완료 중앙값 **4시간 미만**. — https://sback.it/publications/icse2018seip.pdf (해설: https://www.michaelagreiler.com/code-reviews-at-google/)
- 리뷰 용량의 인지적 한계(SmartBear의 Cisco 10개월/2,500건 리뷰 연구): 한 번에 **200–400 LOC**를 60–90분 리뷰할 때 결함의 70–90%를 발견. 400 LOC 초과 또는 시간당 500 LOC 초과 속도에서는 결함 발견 밀도가 급락. — https://smartbear.com/learn/code-review/best-practices-for-peer-code-review/

### 속도 규범 — 리뷰의 최우선 변수

- Google 규범: 리뷰 요청에 대한 응답은 **최대 1영업일**(다음날 아침까지). 단, 집중 작업 중이면 중단하지 말고 자연스러운 휴지기(작업 완료, 점심, 회의 후)에 응답 — 맥락 전환 비용이 더 크기 때문. 전체 리뷰 소요보다 **개별 응답 속도**가 개발자 경험을 좌우한다. 사소한 지적만 남았으면 "코멘트 달린 LGTM"으로 승인해 시간대 차이로 하루를 날리지 않게 한다. — https://google.github.io/eng-practices/review/reviewer/speed.html
- DORA 2023: **코드 리뷰 속도 개선이 배포 성과를 50% 끌어올리는 가장 큰 단일 요인**(trunk 기반, CI, 느슨한 결합 아키텍처 등 여러 역량 중에서). 단, 이미 빠르거나 리뷰가 없는 팀이라면 더 쥐어짤 것 없음. — https://dora.dev/research/2023/dora-report/ (해설: https://codeclimate.com/blog/2023-dora-state-of-devops)

### 가치 있는 리뷰 vs 고무도장(rubber-stamping)

리뷰가 가치를 내는 조건: (1) 변경이 리뷰어의 인지 한계 안에 있고(≤400줄), (2) 리뷰어가 설계·기능·테스트를 실제로 판단하며, (3) 피드백이 시간 단위로 돌아온다. 반대로 1000줄 PR에 10분 만에 "LGTM"이 찍히는 것은 리뷰가 아니라 절차 통과다 — 큰 PR일수록 리뷰가 허술해지는 역설("10줄 PR엔 10개 코멘트, 1000줄 PR엔 LGTM")은 위 SmartBear 데이터가 뒷받침한다. **다중 필수 승인자, 형식적 체크리스트 채우기는 DORA가 명시적으로 지목한 안티패턴**(변경 배치를 키우는 부작용)이다. — https://dora.dev/capabilities/trunk-based-development/

---

## 3. CI/CD의 실제

### 최소한의 "진짜" CI (Martin Fowler)

Fowler의 CI 실천 목록 중 뼈대: — https://martinfowler.com/articles/continuousIntegration.html

1. 모든 것(코드·테스트·스키마·설정)을 버전 관리된 **메인라인**에
2. 스크립트에 의한 **자동 빌드** (사람 손 없이)
3. **자기검증 빌드(self-testing build)**: 빌드에 자동 테스트가 포함되어 "짓궂은 임프가 코드를 망가뜨리면 반드시 테스트가 빨간불이 되는" 수준
4. 각자 **매일 메인라인에 푸시**, 푸시마다 CI가 자동 검증
5. **깨진 빌드 수리가 신규 기능보다 우선** — 메인라인은 항상 녹색
6. **10분 이내 커밋 빌드** — "빌드에서 깎아낸 1분은 커밋할 때마다 모든 개발자가 아끼는 1분"
7. 미완성 기능은 feature flag나 branch-by-abstraction으로 숨김
8. 프로덕션 유사 환경 테스트, 빌드 상태 가시화, 배포 자동화

**판정**: 1–6이 load-bearing이다. 특히 "자기검증 테스트 없이 컴파일만 하는 파이프라인"은 CI라는 이름의 ceremony다. 반대로 커버리지 배지, 과도한 파이프라인 단계 수는 하중을 받지 않는다.

### Integration vs Delivery vs Deployment

- **CI**: 매일 메인라인에 통합하고 자동 검증. 브랜치에 CI 서버만 붙인 것은 CI가 아니다 — "메인라인으로 되돌려 푸시하지 않으면 팀원이 그 작업을 볼 수 없다."
- **Continuous Delivery**: "소프트웨어를 **언제든 프로덕션에 릴리스할 수 있는 상태**로 만드는 규율." 판별 테스트: 사업 책임자가 "지금 버전 당장 배포해달라"고 해도 아무도 당황하지 않는가. 배포 시점은 비즈니스가 결정.
- **Continuous Deployment**: 검증을 통과한 **모든 변경이 자동으로** 프로덕션에 나감. — https://martinfowler.com/bliki/ContinuousDelivery.html

### Feature Flags: "배포 ≠ 릴리스"

- 4분류: **Release toggle**(미완성 기능을 꺼둔 채 trunk에 머지 — trunk 기반 개발의 핵심 도구), **Experiment toggle**(A/B 테스트), **Ops toggle**(장애 시 비싼 기능 차단·성능 저하 완화), **Permission toggle**(베타/내부/프리미엄 사용자 한정). — https://martinfowler.com/articles/feature-toggles.html
- 핵심 가치: 코드 **배포**(deploy)와 기능 **릴리스**(release)의 분리. 하루 여러 번 배포하면서 사용자에게 보이는 시점은 따로 제어.
- 경고: 토글은 "**운반 비용이 붙는 재고(inventory)**"다. 만료일 설정, 만료된 토글이 남으면 실패하는 테스트, 동시 토글 개수 상한, 목적 달성 즉시 제거 — 이 관리가 없으면 토글은 복잡도 부채가 된다.

### 배포 전략 (고수준)

- **Blue-Green**: 동일한 두 프로덕션 환경을 두고 라우터 스위치로 전환. 문제 시 "라우터를 blue로 되돌리면" 즉시 롤백. 유의점: DB 스키마 변경은 앱 배포와 분리해 "양쪽 버전을 모두 지원하는 마이그레이션 먼저" 원칙으로. — https://martinfowler.com/bliki/BlueGreenDeployment.html
- **Canary**: 신버전을 일부 사용자(내부 직원 → 무작위 표본 → 점진 확대)에게만 라우팅하며 지표를 모니터링, 이상 시 트래픽 회수. 실프로덕션에서 안전한 탈출구를 갖고 검증하는 방식. 다중 버전 동시 운영 복잡도가 비용. — https://martinfowler.com/bliki/CanaryRelease.html

---

## 4. 테스트 전략

### 테스트 피라미드 — 기본형

- 두 가지 본질 규칙: "**서로 다른 입도의 테스트를 써라**" + "**상위 계층으로 갈수록 테스트 수를 줄여라**." 이유는 속도(단위=초, E2E=분+), 유지비, 그리고 E2E의 고질적 flakiness. 역피라미드(E2E 다수·단위 소수)는 "아이스크림 콘" 안티패턴 — 느리고 유지 불가능한 스위트가 된다. 상위 테스트가 잡는 실패는 가능한 한 **하위 계층으로 밀어 내려서** 중복을 없앤다. — https://martinfowler.com/articles/practical-test-pyramid.html
- Google의 실무 버전 (SWE at Google, ch.11): unit/integration/e2e라는 이름 대신 **크기(size)**로 분류 — **small**(단일 프로세스, I/O·네트워크·sleep 금지 → 빠르고 결정적), **medium**(단일 머신, localhost 허용), **large**(다중 머신). 권장 비율 **small 80% / medium 15% / large 5%**. flaky 테스트가 1%를 넘으면 "엔지니어가 테스트를 신뢰하지 않게 되어 가치를 잃기 시작"하며 Google은 ~0.15%를 유지하는 데 지속 투자한다. "Beyoncé Rule": **"If you liked it, then you shoulda put a test on it"** — 지키고 싶은 동작(성능·보안·접근성 포함)에는 전부 자동 검증을 붙인다. — https://abseil.io/resources/swe-book/html/ch11.html

### Testing Trophy — 피라미드에 대한 보정

- Kent C. Dodds("Write tests. Not too many. Mostly integration."): 현대 도구에서는 **통합 테스트가 확신 대비 비용(confidence/cost) 최고의 지점**. 단위 테스트만으로는 "조각들이 함께 동작한다"는 확신을 못 준다(과도한 mocking이 통합 지점의 확신을 지움). 커버리지 100% 추구는 ~70% 이후 수확 체감 — 로직 없는 코드까지 테스트해 리팩토링만 느려진다. 타입/린트(정적 분석)가 아래층을 담당하되 비즈니스 로직 검증은 대체 못 한다. — https://kentcdodds.com/blog/write-tests
- **종합 판정**: 피라미드와 트로피는 실무적으로 같은 결론으로 수렴한다 — "빠르고 결정적인 테스트를 다수, 넓은 범위 테스트를 소수, flaky한 E2E는 최소한". 논쟁은 '단위 테스트의 mocking 정도'에 대한 것이지, "E2E를 많이 쓰라"는 진영은 없다.

### TDD의 실제 채택률과 효과

- 실증 연구(Fucci et al., "A Dissection of the TDD Process", 전문가 39명·82개 데이터 포인트): 품질·생산성 향상은 **스텝의 잘게 나눔(granularity)과 균일함(uniformity)**과 관련이 있었고, **테스트를 먼저 쓰는지 나중에 쓰는지(sequencing)는 유의미한 영향이 없었다**. "TDD의 효능은 test-first 자체가 아니라, TDD류 프로세스가 강제하는 잘고 꾸준한 스텝에서 온다." — https://arxiv.org/abs/1611.05994
- 준수율: 통제된 실험에서조차 참가자의 40%만 프로토콜을 준수, 27%는 전혀 따르지 않음. TDD 연구 전반이 비결정적(inconclusive)이라는 메타 분석도 있다. — https://arxiv.org/pdf/2007.09863
- **판정**: "항상 red-green-refactor"는 실무 표준이 아니다. load-bearing인 것은 **"변경과 같은 커밋/PR에 테스트가 함께 오고, 잘게 진행한다"**는 것. test-first 의식 자체를 강제하는 것은 ceremony에 가깝다.

### 머지/배포 전 "검증됨"의 실무 정의

- **머지 전**: CI 녹색(자기검증 빌드 통과) + 리뷰어 승인 + 변경에 상응하는 테스트 동반(Google 리뷰 항목의 필수 요소). Fowler: 테스트 없는 빌드 통과는 검증이 아니다.
- **배포 전**: 배포 파이프라인의 상위 단계(통합·수용 테스트, 프로덕션 유사 환경) 통과. Continuous Delivery의 정의 자체가 "언제든 배포 가능함을 파이프라인이 상시 증명하는 상태"다. — https://martinfowler.com/bliki/ContinuousDelivery.html
- **배포 후**: canary/모니터링이 최종 검증 계층. "테스트가 전부 통과했다"가 아니라 "프로덕션 지표가 정상"까지가 검증의 끝이다. — https://martinfowler.com/bliki/CanaryRelease.html

---

## 5. Definition of Done과 DORA 지표

### Definition of Done (DoD)

- Scrum Guide 2020 정의: "**증분(Increment)이 제품에 요구되는 품질 기준을 충족한 상태에 대한 공식 기술**." DoD를 못 채운 작업은 릴리스도, 스프린트 리뷰 제시도 불가 — 백로그로 되돌아간다. 조직 표준이 있으면 그것이 **최소선**이고 팀은 더 엄격할 수만 있다. — https://scrumguides.org/scrum-guide.html
- 실무에서 잘 작동하는 DoD의 전형: "코드 작성 + 테스트 통과(CI 녹색) + 리뷰 승인 + 문서/플래그 정리 + (팀에 따라) 스테이징 배포 확인". 핵심 기능은 **"done"이라는 단어의 의미를 팀 전체가 공유해 '80% 완성'을 done이라 부르는 것을 막는 것**이다. 체크리스트가 20항목으로 부풀어 아무도 안 읽으면 ceremony로 전락한다.

### DORA 4 (현재 5) 핵심 지표

- 처리량: **배포 빈도**(Deployment Frequency), **변경 리드 타임**(커밋→프로덕션), **실패 배포 복구 시간**. 불안정성: **변경 실패율**(즉시 개입이 필요한 배포 비율), **배포 재작업률**(2024부터 추가). — https://dora.dev/guides/dora-metrics-four-keys/
- 핵심 발견: **속도와 안정성은 트레이드오프가 아니다**. 최상위 팀은 다섯 지표 모두에서 우수하고 하위 팀은 모두에서 나쁘다. "장기적으로 실제 트레이드오프는 '더 좋은 소프트웨어를 더 빨리' vs '더 나쁜 소프트웨어를 더 느리게' 사이에 있다."
- 왜 이 지표인가: 네 지표는 "작게 자주 통합·배포하고, 깨지면 빨리 복구한다"는 건강한 프로세스의 **결과 지표**라서, 개별 실천(트렁크 기반, CI, 작은 배치…)의 효과가 모두 여기로 수렴한다.
- 사용 주의(원문 명시): 목표로 삼으면 게이밍된다(Goodhart) — 진단 도구로 쓸 것. 팀 간 비교·경쟁 금지, 애플리케이션 단위로 측정, 측정 정밀도보다 개선 대화가 먼저.

---

## 6. 커밋/PR 위생: 무엇이 하중을 받는가

### 커밋 메시지 / CL 설명

- Google 규범: 첫 줄은 **명령형의 독립적인 한 줄 요약**("Deleting…"이 아니라 "Delete the RPC") — 히스토리를 스캔하는 미래 독자가 첫 줄만으로 변경을 파악할 수 있어야 한다. 본문에는 **무슨 문제를, 왜 이 접근으로** 풀었는지 + 버그 번호·벤치마크·설계 문서 링크. "Fix bug", "Add patch", "Phase 1" 같은 설명은 실격. 설명이 중요한 이유: 코드가 말해줄 수 없는 **why**가 미래의 Chesterton's fence 상황을 풀어준다. — https://google.github.io/eng-practices/review/developer/cl-descriptions.html

### Conventional Commits

- 형식 `type(scope): description` (feat/fix/docs/refactor/test/chore…), `BREAKING CHANGE`/`!`로 주요 변경 표시. SemVer와 직결: fix→PATCH, feat→MINOR, breaking→MAJOR. 가치는 **자동 changelog 생성, 자동 버전 결정, 자동 릴리스 트리거**. 스펙 스스로 "모든 기여자가 따를 필요는 없다"고 명시 — squash 머지 워크플로우에서는 메인테이너가 머지 시점에 정리하면 된다. — https://www.conventionalcommits.org/en/v1.0.0/
- **판정**: 릴리스 자동화(semantic-release 등)가 커밋을 **기계적으로 소비**하는 프로젝트에서는 load-bearing. 그런 자동화가 없는 프로젝트에서 접두사만 붙이는 것은 cargo cult — 그 노력은 첫 줄 요약의 품질과 본문의 "why"에 쓰는 편이 낫다.

### PR 설명과 이슈 연결

- PR 설명은 CL 설명과 동일한 원칙(문제→접근→한계)이 적용되며, 리뷰 속도의 입력값이다 — 리뷰어가 맥락 파악에 쓰는 시간을 직접 줄인다.
- 이슈 연결(`Fixes #123` 등 closing keyword)은 추적성 + 머지 시 자동 close라는 실용 기능이 있다. — https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue 다만 "모든 PR에 이슈 필수" 규칙은 이슈 트래커를 실제로 계획/추적에 쓰는 팀에서만 의미가 있다. 한 줄짜리 수정에 형식적 이슈를 만들어 붙이는 것은 ceremony다.

### 종합: load-bearing vs cargo cult 판정표

| 실천 | 판정 | 근거 |
|---|---|---|
| 작은 PR/CL (~수백 줄 이하, 자기완결) | **Load-bearing** | 리뷰 품질·속도·버그율에 직접 효과 (Google, SmartBear, DORA) |
| 브랜치 수명 단축·매일 통합 | **Load-bearing** | DORA 성과 상관, CI의 전제 |
| 자기검증 CI (테스트 포함, ~10분, 깨지면 즉시 수리) | **Load-bearing** | 이것이 없으면 "언제든 배포 가능"이 성립 불가 |
| 리뷰 1영업일 내 응답 | **Load-bearing** | DORA 2023 최대 단일 요인(+50%) |
| 테스트가 변경과 함께 오는 것 | **Load-bearing** | Google 리뷰 필수 항목, self-testing build의 재료 |
| 커밋 첫 줄 요약 + 본문의 why | **Load-bearing** | 미래 독자·리뷰 속도에 직접 기여 |
| feature flag (만료 관리 동반 시) | **Load-bearing** | 배포/릴리스 분리, trunk 기반의 동반 도구 |
| 특정 브랜치 모델 명칭·다이어그램 준수 | Ceremony | 행동(수명·통합 빈도)이 본질 |
| Conventional Commits (자동화 없는 곳에서) | Cargo cult 위험 | 소비자 없는 형식 |
| 커버리지 100% / 커버리지 배지 | Cargo cult 위험 | ~70% 이후 수확 체감 (Dodds) |
| test-first 순서의 의식적 강제 | Cargo cult 위험 | 실증상 순서 무관, 잘게+테스트 동반이 본질 |
| 다중 필수 승인·형식적 리뷰 체크리스트 | Cargo cult 위험 | DORA 명시 안티패턴 (배치 크기 증가) |
| 모든 PR에 형식적 이슈 강제 | Cargo cult 위험 | 트래커를 실제로 쓰는 팀에서만 유효 |

---

## 7. 하네스 설계 시사점 (비개발자용 AI 에이전트 관점)

1. **기본 플로우는 GitHub Flow 형태 + trunk 기반의 규율**: 짧은 브랜치, 작은 단위, 즉시 머지·삭제. Git Flow류의 develop/release 구조를 기본값으로 깔지 말 것.
2. **에이전트에게 "작게"를 강제하는 것이 최대 레버리지**: 변경을 ~수백 줄 이하 자기완결 단위로 슬라이스하는 능력이 리뷰 가능성·롤백 가능성·검증 가능성을 전부 결정한다.
3. **"done" 선언의 최소 조건을 기계화**: 테스트 동반 + CI 녹색 + (사람 또는 독립 에이전트의) 리뷰 통과. "코드가 존재함 ≠ 검증됨"이 업계 전체의 합의다.
4. **리뷰는 빠르고 가볍게, 단 코드 건강 기준은 유지**: "완벽이 아니라 개선이면 승인"(Google) + 시간 단위 턴어라운드가 목표 상태다.
5. **형식 규약은 자동화가 소비할 때만 도입**: changelog/버전 자동화를 하네스가 제공한다면 Conventional Commits가 유효해지고, 아니면 "명령형 한 줄 + why 본문"이면 충분하다.
