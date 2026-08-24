# goppi 개발 워크플로우 표준 — e2e 결론 문서

> 상태: **rev4 — cross-vendor 시니어 리뷰 반영판, 사용자 승인 확정(2026-08-06)** · 판단층(프로젝트 결정) — 객관 근거가 아님
> 승인 범위: 이 판이 **조각 1의 기준선**이다. 이후 변경은 판수를 올리고 사유를 남긴다.
> 리뷰 이력: (1) 2026-08-04 fresh-context 적대 리뷰(HIGH 4·MED 7·LOW 7) → rev2.
> (2) 2026-08-05 fresh-context 3인 리뷰(커버리지/적대적 메커니즘/사용자 여정) → **rev3**.
> findings: [`audit/WORKFLOW-REVIEW-2026-08-05.ko.md`](../../audit/WORKFLOW-REVIEW-2026-08-05.ko.md)
> (3) 2026-08-06 **시니어 인계 관점 2인 리뷰 — same-vendor + cross-vendor(OpenAI Codex/GPT-5.6 sol)** → **rev4**.
> findings: [`audit/SENIOR-REVIEW-2026-08-06.ko.md`](../../audit/SENIOR-REVIEW-2026-08-06.ko.md).
> **이 리뷰가 사용자 상수 ④(독립적 cross-vendor 적대 리뷰)를 처음으로 실제 충족한다** — 이전 리뷰는 전부 `DEGRADED`였다.
> 사용자 확정 결정(2026-08-03): 첫 아키타입 **웹 앱(풀스택)** · 호스트 **Claude Code 단일** · 결정적 게이트 **안전+정직 최소셋**
> 인용 범례: `NN facts` = 2026-08 facts 패스 원번호(경로는 `corpus/facts-2026-08-matrix.md` 머리에 매핑) ·
> `27/xxx` = `corpus/aspects/27-ai-harness-archetype/xxx.md` · HCP/ATM/TUC-nnn = 해당 표준의 claim ID

> 📍 **시각화**: 이 문서와 `steering-verification-design.md`를 한 장으로 옮긴 지도가 같은 폴더의
> [`goppi-workflow-map.html`](goppi-workflow-map.html)에 있다 — 세 층 요약 · 6 정거장 스윔레인(티어별 on/off) ·
> 조향 4층 · 하네스 컴포넌트 6면 · 아키타입 확장. **이 문서가 정본이고 지도는 파생물이다** — 설계를
> 고치면 지도도 같이 고친다(안 그러면 오래된 그림이 근거처럼 읽힌다).
> 더 짧은 요약판(사용자가 답할 질문 4가지 · 부탁 vs 자물쇠 · 조각 6개 빌드 순서):
> [`goppi-blueprint.html`](goppi-blueprint.html)

## 0. 지위와 계승 규칙

이 문서는 "기획→구현→검증→릴리스→운영을 goppi가 어떤 워크플로우로 이끄는가"의 **프로젝트 결정**이다.
과거 하네스의 아이디어는 **검토된 prior art로만** 등장하며, 채택에는 현행 근거가 필요하다. 근거가 판단인
곳은 "프로젝트 판단"으로 명시한다(근거를 가장하지 않는다). 더 우위의 최신 메커니즘이 있으면 과거 방식은
기각 사유와 함께 supersede한다(§6).

**rev3의 성격**: 이 판의 추가분은 대부분 "규칙을 문서에 적었다"이지 "게이트로 집행된다"가 아니다. 각
규칙의 집행 상태는 `steering-verification-design.md`의 Rule Registry가 carrier/gate/telemetry 3필드로
기록하며, 이 문서는 gate 없는 규칙을 **advisory로 명시**한다.

## 1. 워크플로우 원칙

| # | 원칙 | 근거 (정확 인용) |
|---|---|---|
| P1 | **루프가 단위다** — 얇은 수직 조각 하나당 전 단계를 돈다. 첫 조각은 항상 walking skeleton(Cockburn, [2차]) — 같은 계열의 tracer bullet(Hunt&Thomas, [1차])은 "불완전하지만 완결, 프로덕션으로 진화" | 08 facts(두 개념 별개 절) · 07 facts(INVEST V: 수직 분할) · 15 facts(크기별 성공률: 소규모>대규모 — CHAOS [2차], Eveleens&Verhoef 비판 병기) |
| P2 | **깊이는 위험에 비례, 단계는 고정하지 않는다** — 고정 파이프라인 기각은 **프로젝트 판단**이며, 지지 근거는 ① Anthropic 공식 "diff 한 문장이면 계획 생략"(28 facts [정의/규정]) ② Scott Logic의 10x 오버헤드 — 단, **단일 팀·기능 2개·블로그 1건의 [주장]**(28 facts)이지 일반 실측이 아님 ③ 06 facts: ISO 12207은 특정 모델을 요구하지 않음(공개 초록 수준 확인) | 28 facts · 06 facts · `05/github-workflow-current.md` risk-scaled 표 |
| P3 | **사용자는 PM 역할만** — outcome·업무 규칙·appetite·수용 판정. 기술 선택을 고무도장 승인으로 떠넘기지 않는다. 역할 구분의 지지 강도는 제한적(16 facts는 역할 정의마다 일반화 금지 경고, 소규모 역할 통합은 "공표 문서 부재") — 위임 불가 판단의 실질 근거는 능력 모델 | `methods/target-user-capability-model.md`(TUC-004: 축별 조건화, 승인≠이해) · 16 facts(참고 수준) |
| P4 | **완료 = trustworthy completion** — 정확성·증거·판단 배분·이해 가능성·상태 정직성·복구 가능성 6조건. 절차 수행 자체는 가치가 아니다 | `foundation/goppi-worth-hypothesis.md` · `methods/trustworthy-completion-evidence-model.md` |
| P5 | **상태는 파일로 외부화** — METR 분석은 장기 실패 원인을 상태 관리 붕괴로 **주장**(수치 미제공, 27 facts). 처방의 실근거는 HCP-007("compaction만으로 불충분 — durable handoff artifacts") + 구조화 노트테이킹(27/plugin-marketplace-memory) | 27 facts(instruction-adherence [주장]) · `27/harness-control-plane-standard.md` HCP-007 · `27/plugin-marketplace-memory-standard.md` |
| P6 | **주장은 그것을 반증할 수 있는 산출물과 함께만 완료로 센다** (rev3 신설, **프로젝트 판단**) — 인수기준은 실행 가능한 검사에 묶이지 않으면 인수기준이 아니고, 복구 경로는 실제 실행되지 않으면 경로가 아니다. 리뷰 WF-01·WF-04가 이 원칙의 부재를 지적했다 | 리뷰 findings WF-01·WF-04 · ATM(불변식 5는 "informed gate **and** tested recovery path"의 연언) |

## 2. 표준 루프 — 6 스테이션

각 스테이션: 목적 → 산출물 → 리스크 비례 규칙 → 사용자 체크포인트.
**체크포인트 공통 규칙(리뷰 H2·WF-12 반영)**: S0에서 사용자의 능력 축(C0–C2 × 6축,
`target-user-capability-model.md`)을 기록하되 **초기값은 전 축 C0으로 고정**한다(보수적 위험 평가 —
자기보고 승격 금지, TUC-008 illusion of competence). 승격은 **새 결정 시나리오에서의 실제 선택 관측**으로만
한다.

**장황도는 능력 축이 아니라 행위의 비가역성에 조건화한다(rev4 개정, SR-16)**: rev3은 체크포인트 깊이를
능력 축에 걸었는데, 승격 절차가 미설계(B22)여서 **실질적으로 전 축 영구 C0 = 항상 최대 장황 모드**가
된다. 그런데 이 설계는 §3 G2에서 스스로 **TUC-005(반복 승인 피로)** 를 인용한다 — 매 결정마다 최대
설명을 읽히면 사용자는 읽지 않고 승인하게 되고, 그것은 승인 이벤트 계측(설계 §4.2)은 통과하면서 실질은
고무도장인 최악의 조합이다. 따라서 **깊이의 1차 축은 "이 행위가 되돌릴 수 있는가"**이고, 능력 축은
**설명의 언어와 이해 확인 여부**에만 쓴다(무엇을 말할지가 아니라 어떻게 말할지). 5문장 보고는 형식이지
이해의 증거가 아니다(rubric 자체 경고).

### S0 INTAKE — 문제 심문
- 목적: 해결책이 아니라 문제·성공기준·appetite를 고정. Mom Test식(과거의 구체 행동, 아이디어 승인 금지 — 07 facts).
- **모드 분기(WF-08 신설)**: 첫 질문은 "새로 만드는가, 이미 있는 것을 인수하는가"다. 인수 모드이면
  `01/brownfield-planning-adoption.md`(IMPORT/CONVERT/REVERSE-ENGINEER 3분기, 역공학 결과는 사용자
  확인 전까지 `INFERRED`)와 `04/brownfield-adoption-floor.md`(read-only AUDIT 모드, 3-way disposition,
  additive-first·never clobber, relaxed green-gate + ratchet)를 적용한다. `lifecycle.md`: greenfield/
  brownfield는 별개 생명주기가 아니라 **적용 모드**다.
- **의무 미리보기(WF-19 신설)**: Mom Test는 사용자가 겪어 본 것만 끌어낸다 — 겪은 적 없는 **법적·계약적
  의무는 끌어내지 못한다.** 따라서 아키타입 팩의 last-mile(③)·운영(④) 칸에서 "사람만 할 수 있는 단계"와
  "과금·외부 노출·법적 책임이 발생하는 지점"을 **S0에서 미리 읽어** 티어·appetite·non-goals에 반영한다.
  전제가 성립하지 않으면(예: 결제 온보딩에 필요한 사업자 요건 미충족) 그 사실을 S1 진입 전에 알린다.
  집행: **advisory**(게이트 없음) — 누락은 L3 계측 대상.
- 산출물: **얇은 스펙**(문제 1문단/성공 기준/non-goals/**ID가 붙은 인수기준 체크리스트**/appetite/
  rabbit holes — Shape Up pitch 동형, 07 facts) + **능력 축 기록** + **조각 목록(위험 우선)**.
- **인수기준 ID(WF-01 신설)**: 각 인수기준은 안정 ID(`AC-1`, `AC-2`…)를 갖는다. ID가 없으면 S3에서
  검사에 묶을 수 없고, 요구가 바뀔 때 재검증 범위를 계산할 수 없다. 근거: SWEBOK v4 KA1(traceability는
  1급 활동), ISO 29148:2018 §5.2.5(traceable은 개별 요구의 well-formedness 속성),
  `01/requirements-engineering-craft.md`("stable ID … req → ADR/design → acceptance-test as explicit links").
- **목표 L등급과 8면 disposition(rev4 신설, SR-03·SR-12)**: `production-output-rubric.md`의 검증 표면은
  "모든 기획 spec은 **목표 L등급과 8개 판정면의 disposition**을 기록한다"고 규정하는데, rev3의 S0 산출물
  목록에 그 칸이 없었다. **공개 웹 앱은 정의상 L2**인데 L2를 선언할 자리가 없으면, AC가 해피패스만 담을
  때 실패 경로·회귀·health check가 어디서도 켜지지 않는다(두 벤더 리뷰어 독립 지적). → 얇은 스펙에
  `목표 L등급` 한 줄과 8면 disposition 표(칸 8개)를 넣는다. 비용은 거의 0이고, L2를 선언한 순간
  회귀·실패 경로 검사와 health check가 S3 판정 대상이 되어 G4의 AC 커버리지와 **두 층**을 이룬다.
- **조각 목록(WF-22 신설)**: 사용자 프로젝트의 수직 조각 목록은 S0 산출물이며 `progress.md`에 산다.
  매 루프 종료 시 갱신이 조각 DoD에 포함된다. (spec.md §7의 조각 순서표는 **하네스 빌드용**이지 사용자
  프로젝트용이 아니다 — 둘을 혼동하지 않는다.)
- 비례 규칙: 인터뷰는 (의도 모호 AND 결과 중대)일 때만; 명확·소형은 한 문단 번역. — prior art: goppi kickoff 실험(14 vs 3)은 **인터뷰의 가치**를 측정한 것이고, 트리거 조건 자체는 미검증 → 트리거 적중은 L3 계측 대상.
- 체크포인트: 미러백 승인(능력 조건화 적용).

### S1 SHAPE — 계획·설계
- 목적: 이번 조각의 실행 계획. 설계 문서는 **조건부** — 조건(비가역성·큰 트레이드오프)은 **프로젝트 판단**(08 facts가 기록하는 것은 작성 시기 "요구 확립 후·구현 전" [주장]까지). 결정은 ADR-lite(08 facts: Nygard 5절)로 저장소에.
- **인수기준 → 검사 번역(WF-01 신설, 이 스테이션의 필수 산출물)**: 각 `AC-n`을 실행 가능한 검사에
  매핑한 표(`AC-n → 검사 ID → 검사 파일 위치`)를 만든다. 매핑할 수 없는 인수기준은 **`UNVERIFIABLE`로
  표시하고 사용자에게 그 사실을 알린다** — 조용히 통과시키지 않는다. 이 번역의 타당성은 사용자가
  검토할 수 없는 영역이므로(technical_verification C0–C1), **독립 리뷰의 첫 항목**이 된다(S3).
- **조각 형태 규칙 — 파괴적 스키마 변경(WF-11 신설)**: 데이터 스키마의 파괴적 변경은 한 조각이 아니라
  **expand → migrate → contract 3배포**로 쪼갠다. 마이그레이션은 버전드·**forward-only**. 근거:
  `aspects/14-data-management-migrations`("Ruled out: single-deploy breaking schema changes under load",
  "Ruled out: a backup that has never been restored"). 아키타입 게이팅상 풀스택 웹 앱에서 발화한다.
  **선행 조건(rev4 신설, SR-02)**: forward-only를 택하면 데이터 되돌림의 유일한 수단은 **그 시점의
  백업**이다(근거 문서 자신이 "down migration은 스키마만 되돌리고 데이터 변경은 되돌리지 않는다"를
  기록). 따라서 마이그레이션 실행 **전에 복원 기준점(스냅샷)을 확보**하고 그 시각을 기록한다. 이것은
  S5의 복원 리허설(과거에 한 번 성공)과 **다른 것**이다 — 리허설은 절차가 작동함을, 스냅샷은 지금 이
  데이터가 되돌아갈 수 있음을 뜻한다. 플랫폼 기본값에 기대지 않는다(근거: Supabase Free는 자동 백업
  없음, AWS RDS 기본 보존 1일 — `20/facts-2026-08-solo-operations-minimum`).
- **요구 변경 전파(WF-20 신설)**: 사용자가 도중에 인수기준을 바꾸면 그 `AC-n`에 매핑된 검사와 그것을
  참조하는 조각을 재검증 범위로 산출해 보고한다. circuit breaker는 appetite 초과만 다루고 의도 변경은
  다루지 않았다 — 이 규칙이 그 공백을 메운다. 집행: **advisory**.
- 비례 규칙: 단순 변경은 계획 생략(Anthropic, 28 facts). appetite 초과 예상 시 circuit breaker — 자동 연장 없이 범위 재협상 회부(07·13 facts: Shape Up 규정).
- **appetite 기본값(WF-23)**: 제품 사용자용 기본값은 **조각당 작업 세션 3회**를 잠정 고정값으로 쓴다
  (**프로젝트 판단** — Shape Up의 2주/6주는 팀 스케일이고 번안 근거가 없다). 이 숫자는 형성 연구 전까지
  근거가 없으며, circuit breaker가 임계 없이 비어 있는 것보다 보수적 고정값이 낫다는 판단이다. 실측 후 동결.
- 체크포인트: 되돌리기 어려운 선택만, 소비자 언어로(능력 조건화 적용). **플랫폼 선택은 되돌리기 어려운
  선택으로 분류한다** — 비용 상한이 하드 캡인지 알림뿐인지가 플랫폼에 따라 갈리기 때문이다(WF-30, S5 참조).

### S2 BUILD — 구현
- 규칙: 짧은 브랜치·잦은 통합(09 facts: trunkbaseddevelopment.com [정의/규정] — 24h 내 trunk 커밋), 작은 배치, 미완성은 flag 뒤로(11 facts: toggle 4분류 — 단 Fowler는 release flag를 "최후 수단"으로 기록). **테스트 동반 커밋은 프로젝트 규칙**(지지 근거: 09 facts — Google 리뷰 평가 항목에 테스트 포함).
- 첫 조각 = walking skeleton(배포 파이프라인 관통).
- **저장소 바닥 — 팩 ① 최소 정의(rev4 신설, SR-01·04·08)**: 근거는 코퍼스에 이미 있었다 —
  [`04/foundation-floor-artifact-checklist.md`](../../corpus/aspects/04-build-ci-engineering/foundation-floor-artifact-checklist.md)
  (MUST/REC 태그가 붙은 산출물 계약 + **"Most-commonly-missed (junior-skips, senior-flags)"** 절).
  rev3까지 이 문서를 한 번도 인용하지 않아 **인계자가 clone하고 처음 여는 파일들이 어느 스테이션에도
  없었다**(두 벤더 리뷰어가 독립 지적). 첫 조각에서 아래를 만든다:
  1. **README** — `clone → install → test`가 **5개 명령 이하**로 끝난다(체크리스트 MUST)
  2. **`.env.example`** 커밋 + 실제 `.env`는 ignore. 필요한 환경변수의 **이름·형식·필수 여부**가 여기 있다
  3. **시작 시점 설정 스키마 검증** — 없으면 부팅은 되고 특정 라우트에서 늦게 터진다.
     *aspect 06의 근거는 "국제 표준 부재, 프레임워크 기능으로만 존재"이지만 **표준 부재는 채택 금지
     사유가 아니다** — §6 row 12에서 성능에 대해 쓴 논리("표준 없음 ⇒ 미채택이 위반은 아님")의 대칭이다*
  4. **린터 설정 커밋 + 포매터 CI 강제**(체크리스트 MUST)
  5. **단일 task runner**(Make 또는 package scripts) + **런타임/도구 핀**
  6. **앱 관측성 4종(SR-08)** — 구조화 로그 + **correlation ID** · **release marker(배포 버전)** ·
     health check · 알림이 실제로 발화하는지 1회 시험. ⚠️ **L3 하네스 로그는 사용자의 요청 실패를
     설명하지 못한다** — 하네스 계측과 앱 관측성은 다른 층이다
  7. **로컬 실행 검증** — 깨끗한 환경에서 `clone → setup → migrate → start → smoke`가 실제로 통과
  - **리스크 비례**: 위 체크리스트는 공개·팀 저장소 기준이라 그대로 쓰면 **over-flag한다** — 그 문서
    자신의 **"Repo-context conditioning"** 절(솔로/프라이빗/무료 플랜에서 무엇이 정당한 유예인지)을
    티어 규칙으로 채택한다. 팩 ①의 완전한 명세는 B12/B24.
- 상태: progress.md Current State 갱신(P5) + 조각 목록 갱신.
- 체크포인트: 없음. 게이트 트리거 시 개입.

### S3 VERIFY — 검증
- 목적: "존재 ≠ 검증"의 기계화. CI 녹색 + **인수기준 커버리지** + 완료주장 게이트(G4 — 한계 포함 상세는 조향 설계 §3).
- **인수기준 커버리지(WF-01 — 이 스테이션의 핵심 변경)**: 판정 대상은 "검사가 실행됐는가"가 아니라
  **"각 `AC-n`을 참조하는 검사가 존재하고 그 결과가 무엇인가"**다. S1의 매핑 표를 기준으로
  `AC-n` 각각에 `PASS / FAIL / UNVERIFIED(매핑 없음 또는 미실행)`를 붙인다. 하나라도 `UNVERIFIED`면
  전체 완료 주장은 `UNVERIFIED`다. 근거: 리뷰 WF-01의 실패 시나리오 — 인수기준을 덮지 않는 테스트가
  exit 0을 내면 "결과는 틀렸고 증거 트레이스는 정직한" false completion이 성립한다.
- **검사 약화 금지(WF-01 2차 경로)**: G4가 블록한 상태에서 **검사 정의 파일**(테스트·CI 설정·임계값)을
  바꾸는 것은 코드 수정보다 싼 통과 경로다(`--passWithNoTests`, `skip`, 임계 하향). 이 변경은 L3에
  별도 이벤트로 기록하고 검증 보고에 명시한다. 집행: **advisory + 계측**(게이트화는 오탐 측정 후 판단).
- 독립 리뷰: **CRITICAL 한정**(rev4 개정, SR-09 — rev3은 STANDARD에도 걸었으나 §4 표의 자체 통제시험이
  recall 동일·FP +1을 기록하므로 **자기 증거와 배치를 일치**시킨다). 단 **집행은 초기 advisory+계측**이 정직한 표기(리뷰 M3): 티어 감지 휴리스틱(경로/diff 기반 PreToolUse)을 spec에서 게이트 후보로 검토, 이탈 데이터로 승격. 리뷰어는 fresh context + 저자 결론 미제공 — 근거: `27/hooks-commands-subagents-standard.md` §5(Writer/Reviewer 분리, Anthropic).
  - **리뷰어의 첫 항목은 구현 품질이 아니라 "검사가 요구를 실제로 커버하는가"다**(WF-01).
  - **동등성 부인 고지(WF-06)**: 사용자 보고에 고정 문구를 넣는다 — *"이 검토는 같은 모델 계열의
    fresh-context 검토이며, 책임을 지는 전문가의 검토와 동등하지 않습니다."* 근거: 능력 모델이
    "unavailable human technical review를 대체할 때 동등하지 않음을 명시하라"를 규범으로 둔다.
  - **채택 근거의 정직한 표기(WF-06)**: 이 컴포넌트는 과거 통제시험에서 사전 등록된 harmful 조건을
    발화시킨 이력이 있다(§4 표 참조). 그래서 CRITICAL 한정 + 오탐 계측 조건부로만 계승한다.
- 산출물 판정: `production-output-rubric.md` 8판정면. **웹 앱 게이트는 rubric의 web/mobile UI 행과
  일치시킨다(WF-24)**: 인증/세션 · 행 수준 접근 제어(RLS) · **개인정보 취급** · **정책 고지(처리방침)** ·
  접근성 · 브라우저/기기 호환 · 비밀 관리. (rev2는 3종만 적어 rubric보다 좁았고, 그 결과 처리방침 없는
  앱이 S3를 통과해 S4에서야 문제를 만났다.)
- 체크포인트: 검증 보고 — 통과/실패/**미확인**/복구 경로 구분(능력 조건화 적용; 이해 미확인 시 완료로 세지 않음 — P4 조건 4).

### S4 SHIP — 릴리스
- 규칙: 코드 반영과 사용자 노출의 분리는 11 facts가 기록한 수단(Delivery/Deployment 구분·toggle·canary)으로 달성 — 웹 앱: 스테이징 확인 → 프로덕션. 외부·과금·공개 행위는 승인 게이트(구조적) — 자연어 지시는 게이트가 아님: **ATM-005**(Replit 사건, 위협모델)·TUC-003.
- **공개 전 체크리스트(WF-05 — R1-10 facts의 번역, 신규 리서치 아님)**: 아키타입 팩 ③이 확보한
  "사람만 할 수 있는 단계"를 **순서·선행조건·실패 시 되돌림**과 함께 산출물로 만든다. 웹 앱 팩의 현재
  내용(근거: `17/facts-2026-08-last-mile-domain-hosting.md` · `…-payments-privacy.md`):
  도메인 등록자 정보 제출·검증 · DNS/TLS 확인 · 환경변수 민감도 표시(비가역) · 프로덕션 브랜치 병합
  승인 · 결제수단 등록 · 유료 플랜 선택 · PSP 신원 확인(정부 발급 신분증·UBO·은행계좌 소유 일치) ·
  PCI 책임 주체 지정 · 개인정보처리방침 승인·공개 · GDPR 정보 제공 책임 확인.
- **라이선스(WF-25 신설)**: 아웃바운드 LICENSE 파일 존재와 인바운드 의존성 라이선스 스캔을 공개 전
  확인 항목에 포함한다. 근거: `aspects/25-licensing-foss-compliance` Web-app/SaaS 행 — **"AGPL awareness
  is critical — AGPL deps trigger network-use copyleft, forcing source disclosure for the hosted service."**
  대상 사용자가 독립 판단할 수 없고 사후 교정이 불가능한 노출이므로 공개 전에 건다.
- **out-of-band 단계의 검증 규칙(WF-18 신설)**: 사용자가 대시보드에서 직접 하는 단계는 하네스의 게이트·
  계측이 닿지 않는다(L2는 에이전트의 도구 호출 경로 위에만 존재). 따라서 **사람의 진술을 PASS 근거로
  쓰지 않는다.** 관측 가능한 부작용으로만 PASS 처리한다(배포된 URL의 처리방침 경로 fetch, DNS/TLS 실측,
  결제 테스트 트랜잭션). 관측 수단이 없으면 정직하게 `UNVERIFIED`로 남긴다.
- 체크포인트: 배포 승인 — 영향·되돌리기 방법 포함(능력 조건화 적용). **승인 요청에는 "직전 복원 실행
  결과"가 첨부된다**(WF-04, 조향 설계 §3 G2 참조).

### S5 OPERATE — 운영자 없는 운영

rev2에서 이 절은 두 줄이었다. §2 머리가 약속한 네 항목(목적/산출물/비례 규칙/체크포인트)을 채운다(WF-05).

- **목적**: 24시간 대기 인력 없이, 1인 소유자가 **알림을 읽고 정해진 절차대로 행동할 수 있는 상태**를
  유지한다. SRE 전체 체계(12 facts)는 스케일 부적합으로 미채택 — 근거는 `framework-crosswalk-2026` 20행
  판정("조직 규모를 solo에 그대로 이식 금지").
- **산출물**:
  1. **알림별 평문 runbook** — 능력 모델의 `operational_responsibility` C1은 "can act on plain alerts
     **and runbooks**"이다. 평문 알림만으로는 C1도 부족하고 runbook이 짝이어야 한다. rubric의 "사용자가
     실행 가능한 평문 runbook"이 여기서 생산된다(rev2까지는 rubric에만 있고 어느 정거장의 산출물도 아니었다).
  2. **복원 리허설 실행 기록** — 백업 존재가 아니라 **복원 1회 실행 결과**를 남긴다(WF-04).
  3. **만료 대장** — 만료일이 있는 항목(런타임 EOL·TLS 인증서·유료 플랜·도메인 갱신)을 날짜 필드와 함께
     기록한다(WF-03).
  4. **비용 상한 설정과 그 동작의 기록** — 아래 참조.
  5. **인계 패키지**(WF-26, rev4 개정 SR-13) — **첫 절은 rubric「인계 가능」면**(목적·실행·검증·알려진
     한계)이다. 인계받는 사람이 먼저 필요한 것은 하네스 경계가 아니라 **"이게 뭐고 어떻게 돌리나"**이며,
     그 실물은 S2 팩 ①의 README다(**첫 릴리스 전에 인계해도 README는 이미 존재한다** — S5는 S4 이후라
     인계 패키지만으로는 그 시점을 못 덮는다). 둘째 절이 경계 목록이다: 저장소에 남는 것(spec·progress·
     ADR·테스트·CI·서버측 통제)과 **하네스와 함께 사라지는 것**(G1–G4·Rule Registry·L3 계측 ·
     **만료 대장을 세션 시작에 표면화하는 장치** — 대장 자체는 남지만 읽어주는 장치가 사라진다. 런타임
     EOL은 "기존 배포는 돌고 새 배포만 막히는" 실패라 인계 후 시한폭탄이 된다). 사용자는 "파괴 방지와 완료 주장
     검증이 있다"고 들었으므로, 그것이 언제 없어지는지도 들어야 한다. rubric의 "인계 가능" 판정면을 이
     산출물의 판정면으로 쓴다.
- **비례 규칙** — ⚠️ **여기의 티어는 변경 표면이 아니라 프로젝트의 운영 수준이다(rev4 명시, SR-15)**:
  §3의 티어 트리거는 "이번 변경이 무엇을 건드리나"인데, 운영 최소셋은 "이 프로젝트가 무엇을 감당해야
  하나"로 정해진다. **오타 수정 하나(LIGHT)가 운영 수준을 낮추지 않는다.** 아래 등급은 프로젝트가
  공개돼 있고 사용자 데이터를 다루는지로 판정한다. 프로젝트 운영 수준이 LIGHT면 알림 1종(장애)과 비용
  상한만. STANDARD 이상은 위 산출물 전체. CRITICAL은
  복원 리허설을 **조각 완료 조건**에 포함한다.
- **비용 상한은 사용자 결정이다(WF-30 신설)**: "비용 상한"은 서로 다른 두 동작을 덮는 한 단어다 —
  하드 캡(도달 시 서비스 일시중지, 방문자에게 오류 노출, 자동 재개 없음)과 알림 전용(과금은 계속됨).
  근거: `20/facts-2026-08-solo-operations-minimum.md` 하위질문 4. 이것은 **사업 결정**("예약이 안 되는
  대신 돈이 안 나간다" vs "돈이 나가는 대신 예약이 된다")이므로 소비자 언어로 사용자에게 제시한다.
  P3의 "사용자는 PM 역할"이 이 방향으로도 적용된다 — 사용자가 결정할 수 있는 것을 결정으로 올린다.
- **루프 폐쇄는 두 갈래다(WF-03)**:
  - ① **사건 신호** — 에러·사용 신호 → S0 입력 (rev2까지의 유일한 경로)
  - ② **정비 신호** — 런타임 EOL·의존성 CVE·기술부채·만료 대장의 경과 항목 → S0 입력.
    사용자가 요청하지 않았는데 도착하는 작업이며, **소유자가 goppi다**(사용자가 아니다).
    근거: `aspects/10`("pinning **without** Renovate/Dependabot is worse than tag-pinning"),
    `aspects/11`(SWEBOK KA Maintenance는 유지보수를 "majority of total lifecycle cost"로 규정),
    R1-9 facts("패치는 자동, **메이저 업그레이드는 고객 결정**").
    **실패 모양의 특수성**: deprecated 런타임은 기존 배포는 계속 돌고 **새 배포만 막힌다** — 아무 일도
    없다가 급한 수정을 올리려는 순간 사고와 차단이 동시에 온다. 그래서 상시 감시가 아니라 **세션 시작
    부트스트랩이 만료 대장의 경과 항목을 표면화**하는 방식으로 잡는다(하네스 밖 상주 프로세스 불필요).
- **은퇴(WF-27)**: `lifecycle.md` stage 4는 "Release, operate, maintain, **retire**"다. 종료 절차
  (데이터 내보내기 경로 + 과금 중단 지점 + 도메인 처리)를 아키타입 팩 ④에 둔다. 1인 소유자에게 "앱을
  닫는다"는 실제 비용 이벤트다.
- **체크포인트**: 평문 알림 수신 시 — 무슨 일이 났고 무엇을 해야 하는지. 비용 상한 동작 선택. 인계 시점.

## 3. 리스크 티어

| 티어 | 트리거 (surface 기반) | 적용 |
|---|---|---|
| LIGHT | 소형·가역이며 **사용자 노출 표면을 바꾸지 않음** | S0 한 문단 → S2 → S3 자기검증 → **S4 축약 레인** |
| STANDARD | 다파일·회귀 위험·공개 인터페이스 | 전 스테이션, 리뷰 1회, 스펙·progress 필수 |
| CRITICAL | 보안·인증·돈·데이터 파괴/이전·프로덕션·외부 공개 | STANDARD + 독립 리뷰 + 승인 게이트 + **복구 계획 선행 및 복원 1회 실증** |

- **LIGHT의 최소 매핑 프로토콜(rev4 신설, SR-07 — cross-vendor 리뷰어가 잡은 rev3 신규 모순)**:
  §3은 LIGHT에서 **S1을 생략**하는데, S3와 설계 §3.1은 **"S1의 매핑 표를 기준으로"** G4가 판정한다.
  즉 문구 수정 하나가 정직하게는 `UNVERIFIED`가 되거나, 문서에 없는 방식으로 매핑을 만들어야 했다.
  → **LIGHT는 S1 전체를 생략하되 `AC-n → 검사` 매핑 한 줄만 S0에서 직접 만든다.** 설계 문서·ADR·
  요구 변경 전파는 생략한다. G4의 입력이 비지 않게 하는 최소 장치다.
- **LIGHT의 배포 경로(WF-13)**: rev2의 "소형·가역·**로컬**"은 모호했다 — '배포 안 됨'으로 읽으면 살아
  있는 앱의 모든 변경이 최소 STANDARD가 되어 P2가 기각한 오버헤드가 티어 트리거로 되돌아오고, '영향
  범위가 좁음'으로 읽으면 프로덕션 도달 경로가 정의되지 않는다. rev3의 정의: LIGHT는 **배포된다**. 단
  **S1 생략 + S3 자기검증 + S4는 축약 레인**(승인 화면 1문장, 롤백 지점만 확인)을 탄다. G1–G4는 티어와
  무관하게 항상 발화한다.
- 모호 시 위험 축 상향 — prior art(goppi 계약) 유지. **이것은 프로젝트 판단이다**(WF-28 수정): rev2는
  근거로 TUC-012를 인용했으나, TUC-012의 실제 내용은 "대표 표본·인간 숙련도와 GAI 능력 시험의 분리·
  일화적 평가로부터의 외삽 금지"로 **위험 축 상향을 지지하지 않는다.** 인용을 철회하고 판단으로 표기한다.
- **집행 정직성(리뷰 M3)**: 티어 판정은 의미론적 판정이라 현재 게이트가 없다 — Rule Registry상 carrier=L1 스킬,
  gate=**없음(advisory)**, telemetry=단계 이탈률로 등록하고, 기계 감지 휴리스틱을 spec에서 설계한다.

## 4. prior art 계승/기각 표

| 과거 방식 | 판정 | 사유 |
|---|---|---|
| goppi 5조항 계약(advisory 중심) | 변형 계승 | 원칙 유지, 집행은 게이트+계측으로 이동(27 facts) |
| goppi kickoff 트리거 | 계승(계측 조건부) | 인터뷰 가치는 측정됨(14 vs 3); 트리거 조건은 미검증 → 계측으로 검증 |
| **goppi review(독립 리뷰 레이어)** | **조건부 계승 — 부정 증거 병기(WF-06 신설 행)** | 통제시험 `legacy/sources/goppi/harness-eval-results/2026-07-26-review-precision.md`는 사전 등록된 harmful 조건이 **발화**했다고 기록한다: recall 8/8 대 8/8(동일), false positive vanilla 0 대 harness 1 → **"1 > 0. That condition is met."** 그 문서 자신이 n=1·채점기 결함·recall 동일을 함께 기록한다. rev2는 이 항목을 표에 올리지 않은 채 CRITICAL 필수로 재도입했다(§0 계승 규칙 우회). rev3의 판정: **CRITICAL 한정 + 오탐 계측 필수 + 동등성 부인 고지**를 조건으로 계승하고, 오탐율이 개선되지 않으면 축소·삭제 후보로 둔다 |
| goppi ship 고정 세리머니 | 기각→재설계 | ADR-0041 운반체 실패 + P2. 행동 기준(짧은 브랜치·통합)만 유지 |
| goppi 듀얼 호스트 | 기각(연기) | 사용자 결정. 스킬 개방 표준(agentskills.io)이 이식성 확보 |
| gingoa 28-aspect 오버레이 | 변형 계승 | **스테이션→aspect 매핑은 신규 작업** — rev3의 §6에서 실행 |
| SDD 고정 파이프라인 | 기각(프로젝트 판단) | 근거는 P2에 정확 표기(10x는 단일 [주장]). "의도 고정+체크포인트" 뼈대는 S0·S1에 흡수 |

## 5. 미결정 → spec.md로

- 각 스테이션의 스킬/게이트/계측 배치 → `steering-verification-design.md`
- CRITICAL 감지 휴리스틱(경로/diff 기반)의 게이트화 검토(M3)
- appetite 제품 기본값의 실측·동결(rev3는 잠정 3세션 — S1 참조)
- 능력 축 C0→C1 승격의 관측 절차 정의
- 이 워크플로우의 가치 판정은 확증시험(TCR/FCR)만이 한다

## 6. 28 aspect 배치·기각 표 (rev3 신설 — WF-07)

리뷰 지적: facts 패스가 닿지 않은 aspect(10·11·12·14·25)가 **기각도 수용도 아닌 침묵** 상태였고,
누락 집합이 "리서치가 닿은 범위"와 정확히 일치했다. §4가 "기각은 사유와 함께"를 자기 규율로 삼으므로,
28행 전부에 **배치 또는 기각 사유**를 붙인다. 이 표를 채우기 전에는 이 문서를 "기준점"이라 부르지 않는다.

범례: 팩 ①=scaffold 기본값 · ②=산출물 게이트 · ③=last-mile · ④=운영 최소셋 · ⑤=eval 시나리오
(아키타입 팩 정의는 `spec.md` §8.2)

| aspect | 배치 | 비고 |
|---|---|---|
| 01 요구·계획 | **S0**(얇은 스펙·AC ID·Mom Test) · **S1**(ADR) | brownfield 분기의 근거 문서도 여기 |
| 02 아키텍처·설계 | **S1**(ADR-lite, 조건부 설계 문서) | 전체 아키텍처 문서는 조건부 — P2 |
| 03 개발 환경 | **팩 ①** + S2 | **근거 확보(R2-1)**: [`03/facts-2026-08-reproducible-environment`](../../corpus/aspects/03-dev-environment/facts-2026-08-reproducible-environment.md) — devcontainer 스펙·버전 고정·lockfile·dev/prod 패리티. ⚠️ 12-Factor는 **표준 기관 산출물이 아닌 저자 방법론** |
| 04 빌드·CI | **팩 ①**(저장소 바닥 전체 — S2 참조) · **S3**(녹색 조건) | **근거 재배치(rev4, SR-01)**: rev3은 이 행의 비고칸이 비어 있었고, 팩 ①의 유일한 근거였던 web-scaffold-baseline은 스스로 "CI 최소 게이트는 규정 없음"으로 끝난다. → 같은 aspect의 [`04/foundation-floor-artifact-checklist`](../../corpus/aspects/04-build-ci-engineering/foundation-floor-artifact-checklist.md)(MUST/REC 산출물 계약 + "junior-skips, senior-flags" 절 + **repo-context conditioning**)를 팩 ①의 정본 근거로 올린다. rev3까지 이 문서를 인용하지 않은 것이 두 벤더 리뷰어가 공통 지적한 최대 결함이다 — **같은 폴더의 brownfield 짝은 S0에서 인용했다** |
| 05 SCM·워크플로우 | **S2**(짧은 브랜치·잦은 통합) · **M7 서버측 통제**(브랜치 보호·required checks) | 서버측은 게이트가 아니라 scaffold 기본값 |
| 06 설정·시크릿 | **G3** + **팩 ①** | **근거 확보(R2-1)**: [`06/facts-2026-08-config-validation-secrets`](../../corpus/aspects/06-config-secrets/facts-2026-08-config-validation-secrets.md) — **시작 시점 설정 검증은 국제 표준 부재, 프레임워크 기능으로만 존재**(확인된 부정 결과) · 회전 주기의 구체값은 어느 벤더 문서에도 없음 · GitHub secret scanning이 밝힌 탐지 한계 |
| 07 구현·코드리뷰 | **S2**(테스트 동반 커밋) · **S3**(독립 리뷰) | |
| 08 테스트 | **S1**(AC→검사 번역) · **S3**(커버리지 판정) | WF-01의 주 무대 |
| 09 애플리케이션 보안 | **S3 웹 게이트** · **G1–G3** · 위협모델 | |
| 10 공급망 보안 | **부분 배치 + 부분 기각** — 의존성 업데이트 봇은 **팩 ①**, EOL/CVE는 **S5 정비 신호**. SBOM·서명·provenance attestation은 **기각** | **기각 근거가 판단에서 확인으로 바뀜(R2-3)**: [`10/facts-2026-08-dependency-updates-scope`](../../corpus/aspects/10-supply-chain-security/facts-2026-08-dependency-updates-scope.md)의 적용 범위 표 — **SLSA·OpenSSF Scorecard·SBOM 어느 공식 문서도 자체 호스팅 웹 앱 적용을 명시하지 않는다**(SBOM 현행 의무는 정부/규제 산업 판매 기준). 단 "적용되지 않는다"는 명시적 선언도 없으므로 **명시 없음**이 정확한 상태다. 라이브러리/패키지 아키타입 추가 시 재검토 |
| 11 유지보수·기술부채 | **S5 정비 신호** · **S0 조각 목록**(부채 항목) | **근거 확보(R2-3)**: [`11/facts-2026-08-refactoring-debt-discipline`](../../corpus/aspects/11-maintainability-techdebt-refactoring/facts-2026-08-refactoring-debt-discipline.md) — 리팩터링/행동변경 분리(Fowler·Google) · ISO 25010은 **전문 유료라 카탈로그 수준까지만 1차** · CISQ 표준은 사이트 장애로 미확보 |
| 12 성능·확장성 | **미채택 + 팩 ② 최소 1개** | **기각 사유 교정(R3-3)**: [`12/facts-2026-08-web-performance-thresholds`](../../corpus/aspects/12-performance-scalability/facts-2026-08-web-performance-thresholds.md) · [`21/…serverless-cost-model`](../../corpus/aspects/21-economics-cost-sustainability/facts-2026-08-serverless-cost-model.md). ① 성능 예산을 요구하는 **표준이 없다** — Core Web Vitals는 **Google의 정책**, 성능 예산은 처방이다. 그래서 미채택은 표준 위반이 아니다. ② 그러나 rev3의 **"비용 상한으로 대체한다"는 논리는 성립하지 않는다** — 과금 단위가 플랫폼마다 달라(Lambda GB-s는 실행시간=비용, Cloudflare CPU-ms는 아님) **어느 플랫폼도 성능=비용을 공식 원칙으로 규정하지 않는다**. 사용자 체감 성능은 비용과 **별개 축**이므로 팩 ②에 체감 지표 1개를 남긴다 |
| 13 API·인터페이스 설계 | **최소 채택(팩 ②)** — rev3의 전면 기각에서 변경 | **기각 사유 교정(R3-4)**: [`13/facts-2026-08-api-scope-boundary`](../../corpus/aspects/13-api-interface-design/facts-2026-08-api-scope-boundary.md) — **RFC 9110과 OpenAPI는 공개/내부 API를 구분하지 않는다**(구분 명시 없음, 모든 HTTP에 균등 적용). 따라서 rev3의 "내부 API만 갖는 앱이라 해당 없음"은 **성립하지 않는다**. 정확한 진술: 규격은 적용되지만 전면 채택의 이득이 이 규모에서 비용을 넘지 않는다는 **프로젝트 판단**이며, 코퍼스의 `gated:` 표기는 활성화 규칙이지 규격의 적용 범위가 아니다. 최소분(오류 응답 형태·상태 코드 일관성)은 팩 ②로 |
| 14 데이터·마이그레이션 | **S1 조각 형태 규칙**(expand-contract) · **팩 ②** · **S5 복원 리허설** | **근거 확보(R2-4)**: [`14/facts-2026-08-migration-discipline`](../../corpus/aspects/14-data-management-migrations/facts-2026-08-migration-discipline.md) — 도구별 rollback/downgrade 규정과 제약 · **expand-contract의 원저자 귀속(Nygard 2007) 확인** |
| 15 접근성·UX | **S3 웹 게이트**(품질) + **S0 의무 미리보기**(확인 필요 신호까지만) | **근거 확보(R3-1)**: [`15/…accessibility-obligations`](../../corpus/aspects/15-accessibility-ux/facts-2026-08-accessibility-obligations.md) — WCAG 2.2 적합성 정의·레벨·자동 검사가 못 잡는 항목. **품질 축은 근거로 선다.** ⚠️ **법적 의무 축은 판정 불가(R4)**: [`15/…accessibility-legal-sources`](../../corpus/aspects/15-accessibility-ux/facts-2026-08-accessibility-legal-sources.md) — 재시도에도 **1차 확보 0건**이다. 장차법 조문은 위키문헌 경유(원문 미대조), **시행령 별표3(단계적 적용 대상)은 404로 미확보**, EAA의 전자상거래 포함·미소기업 예외는 **복수 2차 일치이나 Directive 원문 미확인**, EUR-Lex는 3가지 URL 형식 모두 실패(**도구 환경 제약**). → 따라서 goppi는 **접근성 의무를 단정하지 않는다.** S0에서 "공개 대상에 EU 사용자가 포함되는가 / 어떤 사업자인가"를 물어 **"확인이 필요합니다"까지만** 말하고, 판정은 사용자에게 넘긴다(P3의 결정 배분) |
| 16 개인정보 | **S0 의무 미리보기** · **S3 웹 게이트** · **S4 last-mile** | **근거 확보(R3-2)**: [`16/facts-2026-08-privacy-statutory-duties`](../../corpus/aspects/16-privacy-data-protection/facts-2026-08-privacy-statutory-duties.md) — **개인정보 보호법 제30조 제1항 각 호 원문**(처리방침 필수 기재 11항목, 시행일 2025-10-02) + 제15·16·22조(만 14세 미만 포함). R1-10b가 실패했던 조문을 확보해 S0 의무 미리보기의 **실제 내용**이 생겼다. GDPR Art.13/14는 **요약본 기반 — EUR-Lex 원문 미대조** |
| 17 릴리스 엔지니어링 | **S4** 전체 | |
| 18 패키징·배포 | **기각(아키타입 게이팅)** — 웹 앱은 레지스트리 배포가 없다. 아키타입 확장 시 재검토 | |
| 19 관측·텔레메트리 | **L3**(하네스 계측) · **팩 ①**(앱 관측성 4종 — S2) · **팩 ④**(알림 운영) | **근거 확보(R2-2) + 층 구분 경고(rev4, SR-08)**: [`19/facts-2026-08-structured-logging-metrics`](../../corpus/aspects/19-observability-telemetry/facts-2026-08-structured-logging-metrics.md) — OTel 로그 규약·HTTP 메트릭. ⚠️ **RED/USE는 표준이 아니라 처방**. ⚠️⚠️ **하네스 관측성과 앱 관측성은 다른 층이다** — cross-vendor 리뷰어의 표현대로 "**L3 하네스 로그는 사용자의 요청 실패를 설명하지 못한다**". rev3은 이 행을 L3와 팩 ④에만 배치해 correlation ID·release marker·health check가 어디에도 없었다 |
| 20 운영·인시던트 | **S5** 전체 · **팩 ④** | |
| 21 경제성·비용 | **S5 비용 상한** · **팩 ④** | **근거 확보(R3-3)**: [`21/facts-2026-08-serverless-cost-model`](../../corpus/aspects/21-economics-cost-sustainability/facts-2026-08-serverless-cost-model.md)의 과금 단위 표 — 플랫폼마다 과금 단위가 다르므로 **비용 상한의 의미도 다르다**. FinOps는 재단의 처방이지 표준이 아니다. 사용자 결정 항목(WF-30)의 근거 |
| 22 문서화 | **S0**(spec) · **S1**(ADR) · **S5**(runbook·인계 패키지) | **근거 확보(R2-2)**: [`22/facts-2026-08-repo-docs-adr-runbook`](../../corpus/aspects/22-documentation-knowledge/facts-2026-08-repo-docs-adr-runbook.md) — ⚠️ **Keep a Changelog·Diátaxis·ADR(Nygard)·SRE runbook은 모두 표준 기관 산출물이 아닌 처방**이다. 인용 시 강도를 그렇게 표기한다 |
| 23 개발자 경험·온보딩 | **기각 유지 + 인계는 S5로** | **기각 사유 교정(R3-4)**: [`24/facts-2026-08-solo-governance-handover`](../../corpus/aspects/24-governance-collaboration-compliance/facts-2026-08-solo-governance-handover.md) — **개발자 인계·온보딩에 공식 표준이 팀 규모와 무관하게 존재하지 않는다**(확인된 부정 결과). 따라서 rev3의 "1인이라 온보딩 대상이 없다"는 **틀린 이유**다. 정확한 진술: **규범이 없으므로 우리가 정한다** — 그 산출물이 S5 인계 패키지(WF-26)이며, 근거가 아니라 프로젝트 설계임을 표기한다 |
| 24 거버넌스·협업·컴플라이언스 | **부분 기각(스케일)** — 팀 거버넌스는 미채택 | **부분 교정(R3-4)**: 결정권 배분은 P3로 흡수, 규제 준수는 16·25로 분산 — 유지. 단 **GitHub 커뮤니티 항목(SECURITY.md 등)은 전부 "권장"이며 1인이라고 특별히 면제되는 것이 아니다** — "스케일 때문에 해당 없음"이 아니라 "권장이므로 비용 대비로 고른다"가 정확하다. 취약점 신고 경로는 저장소 공개 시 재검토 |
| 25 라이선스·FOSS | **팩 ①**(LICENSE) · **팩 ②**(의존성 스캔) · **S4**(공개 전 확인) | **근거 확보(R2-4)**: [`25/facts-2026-08-license-obligations`](../../corpus/aspects/25-licensing-foss-compliance/facts-2026-08-license-obligations.md) — **AGPL-3.0 §13·GPL-3.0·MIT·Apache-2.0 §4 원문 직접 확인** + 조문 인용표 · SPDX/REUSE 규격 |
| 26 MLOps | **기각(아키타입 밖)** — `gated: data-ml` | |
| 27 AI 하네스 아키타입 | **goppi 자신의 빌드에만 적용**(메타) — 사용자 프로젝트에는 미적용 | 이 구분을 잃으면 메타 잠식이다 |
| 28 구현 프로세스·에이전틱 워크플로우 | **이 표준 문서 자체** | |

**표의 한계**: 이 배치는 aspect의 `<topic>--overview.md` 요약과 crosswalk 판정열에 근거한 **프로젝트 판단**이며,
각 aspect 본문의 모든 처방을 대조한 결과가 아니다.

⚠️ **2026-08-08 갱신** — 이 문장의 이전 판은 *"기각 사유가 부실한 행(특히 12·24)은 재검토 대상"*이라
적었으나 **R3-3·R3-4가 12·24의 사유를 이미 교정했고 그 교정이 위 표에 반영돼 있다.**
표의 자기서술이 표의 내용보다 낡아 있었다(적대 감사 F-12).

**남은 진짜 재검토 대상은 row 10이다.** 비고에 *"기각 근거가 판단에서 **확인**으로 바뀜(R2-3)"*이라
적었는데, 인용 증거는 *"어느 공식 문서도 자체 호스팅 웹 앱 적용을 **명시하지 않는다**"*는 **침묵**이고,
같은 행이 스스로 *"'적용되지 않는다'는 명시적 선언도 없으므로 **명시 없음이 정확한 상태**"*라고 시인한다.
**침묵이 확인해 주는 것은 침묵뿐이다.** 그리고 이 저장소 자신의 원칙과 충돌한다 —
S2 항목 3의 *"표준 부재는 채택 금지 사유가 아니다"*, 그리고 R3가 row 13·23에 강제한 형식
*"표준이 요구하지 않으므로 **비용 대비로 고른다**"*.
**비대칭 적용**이었다: 침묵→채택은 허용(row 06 설정 검증)하면서 침묵→기각만 "확인"으로 격상했다.
→ **결론(솔로 웹 앱에서 SBOM·서명·provenance 기각)은 유지한다. 등급만 "프로젝트 판단"으로 내린다** —
"확인"이라 적힌 기각은 재소송되지 않기 때문이다(적대 감사 F-5).
