# 리서치 공백과 보강 순서

> ## ⚠️ 2026-08-24 전환 — 이 문서의 스코프가 바뀌었다 (먼저 읽을 것)
>
> 아래 P0/P1/R2 유닛은 **2026-08-02~05에 작성됐고, 전부 "goppi라는 하네스를 짓는다"를 전제한다**
> (P0 착수 조건이 *"build는 P0와 worth hypothesis가 닫힌 뒤"*, R1 유닛이 전부 하네스 빌드 입력).
> **그 전제는 폐기됐다** — [`direction/04`](../direction/04-the-plan.md)가 또 하나의 자체 하네스를
> 명시적으로 기각했다.
>
> **따라서 아래 유닛은 그대로 읽으면 안 된다.** 각 유닛의 존폐 재판정은 아래 §R3 표가 한다.
> 아래 본문은 **역사 기록으로 보존**한다(append-only 층 규칙).
>
> ⚠️ **ID 주의**: 아래 역사 절에도 `R3-*`가 있다(boundary & duty 패스, 2026-08-05). 신설 유닛은
> **`R5-*`** 로 번호를 바꿔 충돌을 피했다(2차 검수 지적).
>
> ⚠️ 아래 본문 :24가 인용하는 *"README 절대 규칙 6"* 은 **당시 README의 규칙**이고,
> 현행 README 규칙 6은 *"새로 짓기 전에 MAP.md를 훑는다"* 로 다른 규칙이다.

## R5 — 전환 후 공백 (2026-08-24 신설 · 현행)

| Unit | 질문 | 왜 열려 있나 | 종료 기준 |
|---|---|---|---|
| **R5-1** ✅ **종료 2026-08-24 (배치 A·B·C 완료)** 리서치 미승계 claim | `direction`이 인용하지만 코퍼스에 없는 것을 어떻게 처분하나 — **수치 7건**(중앙값 24줄 · 응답 4시간 · DORA 50% · Git Flow 2020 note · 피라미드 80/15/5 · TDD 순서 · feature flag 부채) **+ 문장 2건**(*"브랜치 다이어그램은 ceremony"* · *"다중 승인자·형식 체크리스트는 DORA 안티패턴"* — 2차 검수에서 추가 발견) | SUPERSEDED 문서(`legacy/judgments/research-interpretation/02-engineering-practices.md`)에만 있고, 그 문서는 *"활성 근거로 인용하지 않는다"* 배너가 붙어 있다 | 각 수치를 1차 출처로 재확인해 해당 aspect의 facts 문서로 승계하거나, `direction`에서 **삭제**. 절차는 [`reverification-protocol`](../corpus/methods/reverification-protocol.md). <br>⚠️ **이 목록 자체가 부분적으로 틀렸다**: **80/15/5 는 미승계가 아니다** — [`matrix--facts-2026-08.md`](../corpus/matrix--facts-2026-08.md) 에 *"Google 80/15/5 vs Fowler 계열 ~70/20/10"* 로 **충돌 항목으로 이미 등재**돼 있다. 처분은 *"승계 또는 삭제"* 가 아니라 *"인용 쪽에 충돌임을 반영"* 이다. <br>✅ **배치 A 완료 (2026-08-24)** — `codereview--facts` **CR-005~008**: 중앙값 24줄 **유지** · 4시간 **수정**(응답→전 과정 지연) · DORA 50% **삭제**(1차 출처에 없음) · *"다중 승인자·체크리스트 DORA 안티패턴"* **삭제**(오귀속 — DORA 는 외부 CAB 을 비판했다). **4건 중 3건이 틀렸다.** <br>✅ **배치 B 완료 (2026-08-24)** — `github-workflow-current` **GHW-008·009**: Git Flow 2020 note **출처 부착**(⚠️ **미승계가 아니었다** — 결론은 `05 overview` 에 이미 있었고 출처만 없었다. **목록 오류 2건째**) · *"브랜치 다이어그램은 ceremony"* **프로젝트 판단으로 재분류**(*"다이어그램을 그리는 행위"* 를 측정한 연구를 찾지 못했다). 부수 발견: **DORA 의 ≤3 브랜치·일 1회 병합은 설문 자기보고**이지 저장소 계측이 아니다(GHW-009). <br>✅ **배치 C 완료 (2026-08-24)** — `testing--facts` **TDD-001·002** · `17 overview` **REL-001·002**: TDD 순서 **유지**(1차 출처 부착 — 기존 인용이 **2차 출처 블로그**를 경유하고 있었다 · 표본 n=39 한정 병기) · *"feature flag 는 부채"* **한정 추가**(원문 표현은 *"inventory which comes with a carrying cost"* 이고 Permissioning 토글은 수년 존속이 설계 의도다 — 과일반화였다). <br>🎯 **R5-1 3개 배치 전부 완료.** 총 **9건 중** 유지 3 · 수정/한정 4 · 삭제 2. **목록 자체의 오류 3건**(80/15/5 · Git Flow · TDD 순서 — 셋 다 *"미승계"* 가 아니었다) |
| **R5-2** 요구 ⑥ 막다른 길 신호 | CI 연속 실패·같은 파일 반복 수정 같은 **전략 전환 시점**을 무엇으로 감지하나 | `direction/01` 요구 6(P22)에 **만들 것이 없다**. 출발점은 `28-implementation-process`의 *circuit-breaker · 진동 감지* | 감지 신호 2개 이상을 정의하고, 그중 **CI로 관측 가능한 것**을 최소 1개 배선 |
| **R5-3** 요구 ③ 판정 기준 | *결정이 나에게 오고 판독 가능한 형태로 온다*를 **어떻게 측정하나** | 이 요구를 채우는 수단(전역 규칙·`/kickoff`)이 전부 **협조 기반**인데, 확증시험은 협조 기반 회부가 실사용에서 무너짐을 보였다(승인 피로·판독 실패) | 사전등록된 관측 지표 확보 — 아래 `direction/04` 판정 기준 참조 |
| **R5-4** 인용 status 규율 | README 절대규칙 3(*review-needed·draft 인용 금지*)이 사문화됐다 — `direction`이 인용하는 문서 대부분이 그 상태다 | 상속 verified 50건이 2026-08-02에 전부 강등됐다. 규칙을 지키면 direction은 거의 아무것도 인용할 수 없다 | 규칙을 **status 병기 의무**로 개정하거나(→ 2026-08-24 시행), direction이 하중을 싣는 claim만 verified로 승격 |
| **R5-6** 소유자 회고 부재 | 계보가 *"느낀점"* 을 담지 못한다 — 1인칭 경험 서술이 기록에 우연히 남은 6조각뿐 | 저장소 목적 2가 *"알아낸 것 **및 느낀점**"* 인데 후자가 비어 있다. **소유자만 쓸 수 있다** | `LINEAGE.md` §5b를 소유자가 채우고 `[1차]` 규율(소유자만 수정) 적용 |
| **R5-7** G4 강제 해제 관측의 원자료 부재 | *"연속 9회 차단 후 호스트가 조용히 해제"* 가 `LINEAGE` §5에 있으나 확증시험 원자료에 없다 | 원본 `records/` 삭제 시 출처 없는 요약만 남는다 | 재측정하거나 `LINEAGE` §5에서 내린다 |
| **R5-8** ✅ **설계 닫힘 2026-08-24** 아키타입별 추가 층 | 바닥 위에 **무엇을 만드느냐에 따라 켜지는 층**이 방향에 없다 — 공개 웹앱(WCAG 2.2 AA · GDPR/PIPA · 관측성 · SLO · spend cap) · API(OpenAPI 계약) · DB(전진 전용 마이그레이션) · 배포(SemVer·release-please) · 라이브러리(라이선스) | 목적은 *"최종 산출물이 시니어급"* 인데 아키타입 축이 통째로 빠졌다. 코퍼스 aspect 13·14·15·16·17·18·19·20·21·25가 각각 규정한다 | **설계 완료** ([`direction/05`](../direction/05-the-output-floor.md) *"아키타입별 층 — 누가 판정하나"*): 28측면 중 **gated는 7개뿐**이고, 그중 **3개는 저장소 존재로 판정**(13·14·26) · **1개는 사실상 universal**(12) · **`/kickoff`가 묻는 것은 2개뿐**(공개 여부 · 개인정보). 문진표를 만들지 않는 이유는 P40(거짓 양성)이다. **구현은 만들 것 4·10·13** — 13은 첫 공개 웹앱 때만 |
| **R5-9** codex-native의 미승계 운영 규칙 | 여섯 번째 하네스(2026-08-24 발견)의 판단 대부분은 코퍼스에 **더 강한 근거로 이미 있다**(단일 작성자·오케스트레이터-워커·테스트 피라미드·GitHub Flow·호스트 표면·green≠증거·presence≠adequacy·vanilla 대조군·ablation). 그러나 **운영 규칙 4건은 사본에만 있다** — ① **증거 사다리 5단**(정적→집중→통합→E2E→광역회귀, *"수용 기준이 위 단을 요구하면 아래 단으로 대체하지 않는다"*) ② **머지 직전 head OID 고정**(`--match-head-commit`) ③ **머지 = 작업 경계**(다음 이슈를 같은 스레드에서 자동 착수하지 않는다) ④ **`.worktreeinclude`**(관리 워크트리에서 ignored 파일이 넘어가는 유일한 경로) | ①은 테스트 **피라미드**(스위트 구성비)와 다른 것 — *변경 하나를 무엇으로 증명하는가*의 선택 규칙이다. ②③은 `direction/04`의 이슈→PR→CI→머지 파이프라인이 실제로 안전하려면 필요한 지점이고, ④는 Codex 위임 시 파일이 조용히 누락되는 원인이다 | 각각을 현재 1차 출처로 재검증해 `08`(①)·`05-scm-workflow`(②③)·`27`(④)에 접목하거나, **의도적 미승계로 확정**한다. 본문은 [`legacy/sources/codex-native/`](../legacy/sources/codex-native/)에 보존돼 있다 |
| **R5-10** ✅ **종료 2026-08-24** ④ `/kickoff` 채점 | 이 인터뷰 커맨드가 **아이디어 종류를 가리지 않고** 작동하나 → **ⓐⓑⓒⓓ 4종 전부 통과** | 커맨드 본문에 특정 아이디어 용어는 **0건**(포트폴리오·거래·투자·zipline·pyfolio 전수 확인)이고 내용은 코퍼스 [`elicitation-interview-build-standard`](../corpus/aspects/01-requirements-planning/elicitation-interview-build-standard.md)에서 나왔다. **그런데 실제로 돌려본 아이디어는 1개뿐이다.** 그 표준 자신이 처방을 갖고 있는데(*"`(idea → gold requirements)` case set grades the interviewer + prevents regression"*) **만들지 않았다.** ~~특히 **아키타입 hard-stop(공개 노출·개인정보)은 한 번도 발화한 적이 없다**~~ → **2026-08-24 발화 확인** (아래 ⓐⓑ). 이것은 goppi가 죽은 형태(합성 시험만 통과)와 같은 계열이다 | 구조가 **다른** 아이디어 3종으로 돌려 실패 지점을 각각 기록한다: ✅ **ⓐ 공개 웹앱 · ⓑ 개인정보 — 2026-08-24 둘 다 발화, 거짓 양성 아님.** *"LedgerLens 를 공개 서비스로 낸다"* 로 인터뷰를 시작하자 0번 절이 **이미 운영 중**임을 찾아냈고(`app.divtadel.com` 실도메인 라우트 · D1 `users`·`email_verifications`·`password_resets`·`vaults`), 아키타입 2문항의 답이 **가정이 아니라 관측**으로 확정되며 hard-stop 이 걸렸다. **가상의 기획이 아니라 이미 돌고 있는 서비스에서 걸린 진짜 양성이다.** ✅ **ⓒ 연구·조사 과제 — 2026-08-24 통과, 다만 예상이 틀렸다.** GAPS R5-1(미승계 claim 9건) 을 소재로 돌려 이슈 3건(#40·#41·#42)을 산출했다. **예상**: *"AC 대부분이 `UNVERIFIABLE` 이 될 것"*. **실제**: 존재·배선·전파는 전부 `grep`/`validate_corpus.py` 로 검사 가능했고, `UNVERIFIABLE` 은 이슈당 **1개**로 수렴했다 — 그것도 매번 같은 것, 즉 ***"검증이 실질적으로 제대로 이뤄졌는가"*** 다. **연구 과제가 검사 불가한 게 아니라, 검사 불가한 부분이 좁고 일정하다**: 기계는 *"필드가 채워졌다"* 까지 보고 *"판단이 타당한가"* 는 못 본다. ⚠️ **마찰 1건**: 인터뷰 방식이 Mom Test(고객 발견) 기반이라 **소유자가 자기 문서를 정리하는 과제**에서는 물어볼 *"과거 사용 행동"* 이 얇다. 무너지진 않았으나 결이 안 맞는다. <br>✅ ⓓ **"이미 있는 것"은 2026-08-24 세 번 통과 (n=3)** — 0번 절이 `zipline` `Ledger.process_transaction()` 을 찾아내 범위를 *"포트폴리오 엔진 신규"* → *"거래내역 → pyfolio 입력 다리"* 로 **좁혔다.** 커맨드가 직전 턴의 내 추천을 거슬렀으므로 형식적 통과는 아니다. **2차: 같은 날 웹앱 아이디어에서 `divtadel/app` 의 `LedgerLens`(운영 중, 전날 커밋)를 찾아 인터뷰를 중단시켰다** — `direction/02` 재발 **10번**이 그 건이다. **3차: 같은 날 *"공개 서비스로 낸다"* 가 이미 배포돼 있음을 `wrangler.toml` 로 확인** — 세 번 다 직전 턴의 내 추천을 거슬렀다 |
| **R5-11** ②③ 이 **Python 전용**이다 | 소유자가 실제로 만드는 웹 스택에 재사용 워크플로도 템플릿도 없다 | 실측 2026-08-24: `coolbress/workflows` 에는 `python-ci.yml` **하나뿐**, `coolbress/project-template` 은 `pyproject.toml`·`uv.lock`·`src/`·`tests/` 로 **uv 프로젝트 전용**. 그런데 `divtadel/app` 은 **React · Vite · TypeScript · Cloudflare Workers** 로 돌고 있고, `direction/05` 의 아키타입 층이 켜지는 대상도 그쪽이다. **즉 정작 벽이 가장 필요한 아키타입이 벽 밖에 있다** | `web-ci.yml`(lint·typecheck·test·build) + TS 템플릿을 추가하거나, **의도적으로 Python 만 지원한다고 확정**한다. ⚠️ 순서 주의 — 완주를 한 번도 못 한 상태에서 스택을 늘리는 것은 `direction/04` 의 *"벽보다 도구를 먼저 늘리기"* 에 걸린다 |
| **R5-12** claim table 이 **`verified` 문서에서만 검사된다** | `draft`·`review-needed` 문서의 claim 행은 형식 검증을 받지 않는다 | 실측 2026-08-24: `validate_corpus.py:573` 이 `for path in verified_documents:` 로 돌아 `claim_table_errors` 를 **`status: verified` 문서에만** 적용한다. 그 결과 `codereview--facts-2026-08.md`(`draft`)에 **허용되지 않는 class 5종**(`operational-lesson`·`limitation`·`industry-prevalence`·`not-found`·`misattribution`)을 단 claim 8행이 들어갔는데 **CI 가 초록이었다.** ⚠️ **R5-1 이 다루는 주장 대부분이 바로 그 `draft`·`review-needed` 문서들에 산다** — 검사가 가장 필요한 곳이 검사 밖이다. 같은 문서의 Evidence 필드도 등록 source ID 가 아니라 **원시 URL** 이라 verified 승격 시 함께 실패한다 | 검사 범위를 `draft` 까지 넓히거나, **claim table 이 있는 문서는 status 와 무관하게 검사**한다. 넓히기 전에 기존 위반 건수를 먼저 센다 — 한 번에 켜면 전부 빨간불이 된다 |
| **R5-13** 🔄 `direction/03` **하중 18건 재검증** (프로그램 #49) | `direction/03` 은 코퍼스와 방향을 잇는 다리다. 그 주장이 검증되지 않으면 방향 전체가 검증되지 않은 것이다 | 2026-08-24 측정: `direction/03` 의 주장성 항목 **20개** 중 재검증 **2** · 미검증 **18**. `active` 53개 전수보다 여기가 먼저다 — 53개 중 **49개가 산문**이라 검증 단위가 없다 | 5배치로 나눠 전수 재검증. <br>✅ **배치 1 완료 (2026-08-24) — 벽의 근거 4건.** `28 overview` **IPW-001~005**: **결론은 무너지지 않았고 오히려 강해졌다.** 다만 인용 구조가 틀려 있었다 — ⓐ *"출력 악화"* 의 출처가 서베이로 적혀 있었으나 실제로는 Huang et al. 이고 **추론 과제 한정** ⓑ **Reflexion 인용이 방향 반대**(자기교정 실패가 아니라 피드백 기반 성공을 보인 논문) ⓒ **가장 직접적인 근거가 통째로 빠져 있었다** — *"신뢰할 만한 외부 피드백이 있으면 자기교정은 잘 작동한다"*(IPW-002). 부수: census 10~13% 를 **원자료에서 재계산해 12.7% 확인**(n=118). <br>⬜ **배치 2~5**: 만들 것 ⑥ 근거 · 게이트/이슈 규칙 · 라우팅 · 잔여 |
| **R5-5** 코퍼스 정체성 잔여 | `corpus/INDEX.md`가 *"goppi_final Engineering Evidence Corpus"* 이고, 수명 등급 모델 §5.5의 라우트 집계가 낡았다 | goppi 시대 문서가 현행 진입점 자리에 있다 | 재브랜딩 + 낡은 절 격리 (2026-08-24 부분 시행) |

### 아래는 2026-08-02~05 시점 기록 (역사)

> 우선순위 원칙: goppi-final 설계를 바꿀 수 있는 공백, 안전/권한 공백, 현재 근거의 신뢰도를 막는 공백을
> 먼저 닫는다. “자료를 더 많이 모으기”가 아니라 의사결정 질문과 종료 기준이 있는 research unit만 연다.

## P0 — 기획 전에 반드시 닫기

| Unit | 상태 | 현재 공백 | 산출물과 종료 기준 |
|---|---|---|---|
| R0-0 Target user capability & responsibility | EVIDENCE MODEL CLOSED / USER STUDY OPEN 2026-08-02 | EUSE/LCNC에 더해 초보 Code LLM·비전공 실무자 verification·적정 의존 연구를 claim-level로 연결; 실제 target population 분포와 full-project 행동은 미측정 | [`target-user-capability-model.md`](../corpus/methods/target-user-capability-model.md); 형성 연구→분리 pilot→confirmatory 전에는 population claim 금지 |
| R0-1 Claim-level revalidation | TRIAGE CLOSED / PROMOTION OPEN 2026-08-02 | 50/50 load-bearing claim의 disposition 완료; 48개는 아직 원자 claim register로 재작성 전 | [`CLAIM-REVALIDATION.ko.md`](CLAIM-REVALIDATION.ko.md); verified 문서가 필요할 때 해당 claim만 1차 자료로 승격 |
| R0-2 Current framework crosswalk | STRUCTURE CLOSED / ISO CLAUSES INCONCLUSIVE 2026-08-02 | 28개 coverage/gap/overlap은 표로 만듦; 유료 ISO 상세 조항은 미확정 | [`framework-crosswalk-2026.md`](../corpus/methods/framework-crosswalk-2026.md); 라이선스 본문+review 전 ISO conformance 표현 금지 |
| R0-3 Harness control plane | CLOSED 2026-08-02 | 기존 aspect-27이 콘텐츠 컴포넌트 중심이고 approvals/recovery/state/isolation/observability/update가 약했음 | [`harness-control-plane-standard.md`](../corpus/aspects/27-ai-harness-archetype/harness-control-plane-standard.md)에 6-plane 표준·claim register·검증 표면 기록 |
| R0-4 Agent security model | MODEL CLOSED / BUILD EVAL OPEN 2026-08-02 | 통합 dataflow·12 threat path·8 invariant·red-team suite 고정; 구현은 아직 없음 | [`agent-threat-model.md`](../corpus/aspects/27-ai-harness-archetype/agent-threat-model.md); 구현이 모든 seeded test를 통과해야 build GO |
| R0-4A Comprehensible report & approval | FORMAT CLOSED / RELIANCE EVAL OPEN 2026-08-02 | what/harm/control/evidence/recovery 형식은 고정; 되풀이만으로 이해를 인정하지 않도록 새 decision scenario와 seeded incorrect advice를 추가 | [`production-output-rubric.md`](../legacy/judgments/goppi/foundation/production-output-rubric.md); target-user 선택·거절·escalation·recovery 시험 필요 |
| R0-5A Production-output rubric | CLOSED AS PROJECT DECISION 2026-08-02 | L0–L3, 8면, 6 archetype 추가 gate 고정 | [`production-output-rubric.md`](../legacy/judgments/goppi/foundation/production-output-rubric.md); 보편 표준이 아니라 spec 수용 기준으로 사용 |
| R0-5B Trustworthy completion / assurance basis | EVIDENCE MODEL CLOSED / GOPPI TRANSFER OPEN 2026-08-02 | NIST assurance·GenAI profile, appropriate reliance, 비전공 실무자/초보 coder 연구로 결과·증거·적정 의존 분리 근거를 연결; full-lifecycle harness 직접 연구는 없음 | [`trustworthy-completion-evidence-model.md`](../corpus/methods/trustworthy-completion-evidence-model.md); goppi target-user confirmatory study 전 효과 일반화 금지 |
| R0-5 goppi worth hypothesis | CONSTRUCT + PROTOCOL CLOSED / THRESHOLD + PRODUCT PROOF OPEN 2026-08-02 | 1차 가치를 target 비엔지니어의 trustworthy completion과 false completion 감소로 개정; 임의 50%/30%·비용 수치는 superseded, 형성→pilot→분리 confirmatory protocol과 raw audit surface를 정의 | [`worth-hypothesis.md`](../legacy/judgments/goppi/foundation/worth-hypothesis.md) · [`trustworthy-completion-evaluation-protocol.md`](../legacy/judgments/goppi/foundation/trustworthy-completion-evaluation-protocol.md); baseline/pilot 뒤 margin 동결·확증 실행 전 제품 가치 INCONCLUSIVE |
| R0-6 GitHub delivery workflow refresh | CLOSED 2026-08-02 | current rulesets, merge queue, deployment environments, Actions pinning/permissions 근거가 흩어져 있었음 | [`github-workflow-current.md`](../corpus/aspects/05-scm-workflow/github-workflow-current.md)에 공식 source map·risk-scaled controls·rollback 경계 기록 |
| R0-7 Research retrieval eval | STRUCTURAL + MODEL PILOT CLOSED 2026-08-02 | 30문항 deterministic 5회와 동일 10문항 fresh model 3회/arm 완료; 다른 모델/언어 일반화와 actual token은 미측정 | [`RETRIEVAL-BEFORE-AFTER.ko.md`](RETRIEVAL-BEFORE-AFTER.ko.md) · [`RETRIEVAL-MODEL-AB-RESULTS.ko.md`](RETRIEVAL-MODEL-AB-RESULTS.ko.md): model correctness 5·5·9→10·10·10, unsupported 5·5·1→0·0·0, bytes −56.1% |

| R0-8 Workflow→agent application & adherence | FACTS CLOSED 2026-08-02 / DESIGN OPEN | 조향 표면·지시 준수 실증·준수 검증 방법이 전용 facts로 없었음 — goppi ADR-0041 "운반체 없는 규칙" 교훈의 일반화 근거 | 4개 facts sub-doc 작성 완료(28: agent-workflow-prescriptions · 27: steering-mechanisms/instruction-adherence/compliance-verification — 검색 로그·예산·claim 라벨·미확보 영역 명시). **잔여**: ① steering의 Codex/Gemini 표면 INCONCLUSIVE(host-config-schemas가 부분 커버) ② 스킬 발화 신뢰율·단계 이탈률은 공개 데이터 부재 — goppi 자체 계측 대상 ③ 이를 근거로 한 조향·검수 **설계**는 별도 (spec 단계) |

**빌드 순서 합의 (2026-08-02):** README 절대 규칙 6("build는 P0와 worth hypothesis가 닫힌 뒤")은 다음 순서로
읽는다 — R0-5의 **형성 연구와 vanilla-arm 기준선(TCR/FCR)은 goppi 없이 빌드 전에 실행 가능하며 선행**하고,
goppi-arm **확증시험은 빌드 이후 product GO를 gate**한다 (protocol의 C1/A1 구분과 일치). 확증시험 미완을
빌드 착수의 blocker로 읽으면 순환이 되므로, 빌드 전 gate는 "construct/protocol/threshold-절차 고정 + 형성·기준선
착수"까지다.

## P1 — 첫 설계와 함께 닫기

| Unit | 질문 | 필요한 근거 |
|---|---|---|
| R1-1 Long-horizon state/recovery | 세션·run state·workspace snapshot·memory·wayfinding을 어떻게 구분하고 복구하는가? | OpenAI/Anthropic official behavior + failure-injection prototype |
| R1-2 Context and memory | 무엇을 항상 주입하고 무엇을 JIT 검색하며 무엇을 기억하지 말아야 하는가? | host docs + retrieval eval; stale/poisoned memory cases |
| R1-3 Model and work routing | 언제 single-agent, subagent, multi-agent, cheaper model이 실제 이득인가? | task-decomposition experiments with token/time/quality, not vendor benchmark alone |
| R1-4 Eval methodology | deterministic/semantic/stateful graders를 어떻게 조합하고 judge를 어떻게 보정하는가? | representative failures, human agreement, variance and repeated trials |
| R1-5 Harness lifecycle | install/update/migrate/rollback/deprecate를 Claude/Codex 양쪽에서 어떻게 검증하는가? | host compatibility matrix + clean install and upgrade fixtures |
| R1-6 Observability and economics | 어떤 trace/metrics가 디버깅과 worth 판단에 필요하며 개인정보/비용을 어떻게 제한하는가? | telemetry schema, redaction, cost budget, retention policy |
| R1-7 Human decision rights | 모델이 제안/자동실행/중단할 경계를 어떤 위험 신호로 정하는가? | NIST AI RMF, agent security guidance, user tests, false-positive/negative eval |
| R1-8 Brownfield adoption | 기존 규칙과 충돌할 때 import/merge/ratchet/decline을 어떻게 결정하는가? | representative repositories, no-clobber/rollback tests, ownership lineage |
| R1-9 Solo-operated / low-operations software | **FACTS CLOSED 2026-08-04 / DESIGN OPEN** · managed service를 써도 1인 소유자에게 어떤 비용·장애·복구·보안 책임이 남는가? | 산출: [`20/facts-2026-08-solo-operations-minimum`](../corpus/aspects/20-operations-incident-reliability/solo-operations-minimum--facts-2026-08.md) — AWS·Vercel·Render·Fly.io·Supabase 공식 문서로 책임분담/알림/백업·복원/spend cap(hard vs alert-only)/런타임 EOL·인시던트 오너십 수집. **미조사: Netlify·Railway·Cloudflare 책임 모델, 알림 보존기간, SLA** (문서 `미해결` 절). 설계 반영은 spec B17 |
| R1-10 Archetype last-mile | **FACTS CLOSED 2026-08-04 / DESIGN OPEN** · 코드 이후 실제 공개까지 도메인·호스팅·고지·결제 장벽을 어떻게 안전하게 넘는가? | 산출 2건: [`17/…domain-hosting`](../corpus/aspects/17-release-engineering/last-mile-domain-hosting--facts-2026-08.md)(ICANN·PaaS — 과금/노출/자격증명 발생 지점 5개; fetch 검증 후 미확인 claim 9개 강등) · [`17/…payments-privacy`](../corpus/aspects/17-release-engineering/last-mile-payments-privacy--facts-2026-08.md)(Stripe 온보딩·PCI SSC·GDPR Art.13/14 — 사람만 할 수 있는 단계). **미확보: PIPA 제30조 각 호 원문(law.go.kr 접근 실패)·PCI SAQ 공식 PDF·GDPR 원문 대조** |
| R1-11 Web-app scaffold baseline | **FACTS CLOSED 2026-08-04 / DESIGN OPEN** · 2026 현행 웹 앱의 표준 구성(스택 중립 베이스라인)은 무엇이 공식 문서로 규정되는가? | 산출: [`04/facts-2026-08-web-scaffold-baseline`](../corpus/aspects/04-build-ci-engineering/web-scaffold-baseline--facts-2026-08.md) — OWASP·PostgreSQL·Supabase·GitHub·Next.js/Vercel·Sentry 공식 문서. **침묵의 위험 지점 5개**(RLS 미적용 전체 노출·service_role 우회·Actions 마스킹 실패·`NEXT_PUBLIC_` 인라인·Sentry 미스크럽)와 **표준 vs 플랫폼 상충**(시크릿의 환경변수 저장) 병기. **CI 최소 게이트는 공식 규정 부재로 부분 미해결.** scaffold 기본값 표는 spec B12 |

## R2 — craft-layer 패스 (2026-08-05, FACTS CLOSED)

**동기**: 표준 rev3 §6이 28 aspect를 전부 처분했지만 그중 16행이 **상속 미검증 문서 + 판단**에 기대고
있었다. "현업 시니어가 알아보는가"를 근거로 답하려면 S2/S3/S5가 실제로 기대는 축부터 근거가 필요했다.

| Unit | 산출 | 핵심 결과 |
|---|---|---|
| R2-1 | [`03/…reproducible-environment`](../corpus/aspects/03-dev-environment/reproducible-environment--facts-2026-08.md) · [`06/…config-validation-secrets`](../corpus/aspects/06-config-secrets/config-validation-secrets--facts-2026-08.md) | **시작 시점 설정 검증에 국제 표준이 없다**(프레임워크 기능으로만 존재) · 시크릿 회전 주기의 구체값은 어느 벤더 문서에도 없음 · GitHub secret scanning이 스스로 밝힌 탐지 한계 |
| R2-2 | [`19/…structured-logging-metrics`](../corpus/aspects/19-observability-telemetry/structured-logging-metrics--facts-2026-08.md) · [`22/…repo-docs-adr-runbook`](../corpus/aspects/22-documentation-knowledge/repo-docs-adr-runbook--facts-2026-08.md) | **표준 vs 처방 구분**: 12-Factor · RED/USE · Diátaxis · Keep a Changelog · ADR(Nygard) · SRE runbook은 **표준 기관 산출물이 아니다**(7건) |
| R2-3 | [`11/…refactoring-debt-discipline`](../corpus/aspects/11-maintainability-techdebt-refactoring/refactoring-debt-discipline--facts-2026-08.md) · [`10/…dependency-updates-scope`](../corpus/aspects/10-supply-chain-security/dependency-updates-scope--facts-2026-08.md) | **SLSA·Scorecard·SBOM 어느 것도 자체 호스팅 웹 앱 적용을 명시하지 않음**(SBOM 의무는 정부/규제 산업 판매 기준) → 표준 §6 aspect 10의 기각이 판단에서 **확인**으로 승격 |
| R2-4 | [`14/…migration-discipline`](../corpus/aspects/14-data-management-migrations/migration-discipline--facts-2026-08.md) · [`25/…license-obligations`](../corpus/aspects/25-licensing-foss-compliance/license-obligations--facts-2026-08.md) | **AGPL-3.0 §13·GPL-3.0·MIT·Apache-2.0 §4 원문 직접 확인** + 조문 인용표 · expand-contract의 원저자 귀속(Nygard 2007) 확인 |

**품질 관리**: 4패스 모두 오케스트레이터가 전수 검사했고 **3건에 수리 패스**를 돌렸다 — 서술형/스킴 없는
인용을 완전 URL로 교체, 벤더 해설(SonarSource)의 1차 오분류 재분류, 스니펫 기반 claim 강등, 예산 미사용분
추가 조사. 이후 외부 URL 753개 전수 검사에서 **dead 0**으로 인용 실재성이 기계적으로 확인됐다.

## R3 — boundary & duty 패스 (2026-08-05, FACTS CLOSED)

**동기**: R2 이후 남은 8개 중 6개(12·13·15·16·21·24)는 판단으로만 처분돼 있었고, 그중 둘(15·16)은
**법적 의무**가 걸려 있었다. 18 패키징·26 MLOps는 **아키타입 게이팅**으로 닫힌 것이라 리서치하지 않았다.

| Unit | 산출 | 핵심 결과 |
|---|---|---|
| R3-1 | [`15/…accessibility-obligations`](../corpus/aspects/15-accessibility-ux/accessibility-obligations--facts-2026-08.md) | WCAG 2.2 적합성 정의 · 의무 발생 조건 표 · 자동 검사 한계. **EAA 조문·한국 법령 조항은 fetch 실패로 미확보** |
| R3-2 | [`16/…privacy-statutory-duties`](../corpus/aspects/16-privacy-data-protection/privacy-statutory-duties--facts-2026-08.md) | **개인정보 보호법 제30조 제1항 각 호 원문 확보**(처리방침 필수 기재 11항목, 시행일 2025-10-02, 법률 제20897호) — **R1-10b의 최대 미해결 종결**. GDPR Art.13/14는 요약본 기반 |
| R3-3 | [`12/…web-performance-thresholds`](../corpus/aspects/12-performance-scalability/web-performance-thresholds--facts-2026-08.md) · [`21/…serverless-cost-model`](../corpus/aspects/21-economics-cost-sustainability/serverless-cost-model--facts-2026-08.md) | Core Web Vitals=Google 정책 · 성능 예산·FinOps=처방 · **어느 플랫폼도 "성능=비용"을 규정하지 않음**(Lambda GB-s 예 / Cloudflare CPU-ms 아니오) |
| R3-4 | [`13/…api-scope-boundary`](../corpus/aspects/13-api-interface-design/api-scope-boundary--facts-2026-08.md) · [`24/…solo-governance-handover`](../corpus/aspects/24-governance-collaboration-compliance/solo-governance-handover--facts-2026-08.md) | **RFC 9110·OpenAPI는 공개/내부 API를 구분하지 않음** · **개발자 인계에 공식 표준이 팀 규모와 무관하게 없음** · GitHub 커뮤니티 항목은 전부 "권장" |

**이 패스의 성과는 "기각을 확인한 것"이 아니라 "기각 사유가 틀렸음을 잡은 것"이다.** 표준 §6의 네 행
(12·13·23·24)에서 결론은 대체로 유지됐지만 **이유를 교정**했다 — "해당 없음/스케일 때문"이 아니라
"표준이 요구하지 않으므로 비용 대비로 고른다" 또는 "규범이 없으므로 우리가 정한다"가 정확한 진술이다.

**남은 미검증 aspect (2개)**: 18 패키징 · 26 MLOps — 둘 다 **아키타입 게이팅**으로 닫힘(웹 앱은
레지스트리 배포가 없고 `gated: data-ml`은 범위 밖). 아키타입 추가 시 열린다.

## R4 — 법령 원문 재시도 (2026-08-05, **부분 실패 — 도구 환경 제약 확정**)

R3-1/R3-2가 fetch 실패로 남긴 3건을 **접근 경로를 바꿔** 재시도했다. 산출:
[`15/facts-2026-08-accessibility-legal-sources`](../corpus/aspects/15-accessibility-ux/accessibility-legal-sources--facts-2026-08.md).

| 대상 | 결과 |
|---|---|
| 한국 장애인차별금지법 | **부분** — 제20·21조 조문은 확보했으나 **위키문헌 경유**(사용자 편집 사이트, 국가법령정보센터 원문 미대조 → 2차). **시행령 별표3의 단계적 적용 대상은 404로 미확보** = 누가 의무 대상인지 여전히 모름 |
| EAA (Directive 2019/882) | **2차만** — 전자상거래 포함·미소기업 예외를 접근성 벤더 4곳이 일치해 서술. **Directive 원문 미확인** |
| GDPR Art.13/14 | **실패** — EUR-Lex 원문 대조 불가 |

**이 패스의 1차 확보는 0건이다.** 그리고 이것이 이 패스의 실질적 결론이다:

> **EUR-Lex는 이 도구 환경에서 본문 추출이 되지 않는다** — 기본 페이지 · CELEX TXT · PDF 세 형식을
> 각각 시도해 모두 동적 로딩(JavaScript 렌더링)으로 실패했다. "더 시도하면 된다"가 아니라 **환경 제약**
> 으로 기록한다. 다음 시도자는 다른 접근 수단(오프라인 사본, 회원국 관보, 별도 API)이 필요하다.

**설계 반영**: 표준 §6의 aspect 15를 **"품질 축은 근거로 서고, 법적 의무 축은 판정 불가"**로 재작성했다.
goppi는 접근성 의무를 단정하지 않고 S0에서 **"확인이 필요합니다"까지만** 말한 뒤 판정을 사용자에게
넘긴다(P3의 결정 배분). 근거 없이 법적 판단을 대행하는 것보다 정직하고, 능력 모델과도 일관된다.

**전 패스 공통 남은 한계**: EAA 조문 원문 · 한국 장차법 시행령 별표3 · GDPR Art.13/14와 ePrivacy의
EUR-Lex 원문 · ISO 12207:2026과 SWEBOK v4 전문(유료) · CISQ 기술부채 표준(사이트 장애).
**이들은 조각 1~2 착수를 막지 않는다** — 전부 조건부 의무(EU 사용자·특정 사업자 규모)이거나 유료 표준이며,
해당 조건이 실제로 발생할 때 사용자 확인 항목으로 처리한다.

## Trustworthy-completion 보강 후 남은 직접 연구 공백

다음은 자료를 더 읽는 것만으로 닫히지 않는다. goppi가 실제로 만들고 실행해야 하는 실증 단위다.

1. **완전 초심자의 full-lifecycle 기준선:** 검색된 직접 연구는 짧은 프로그래밍·데이터 분석·접근성
   과제 중심이다. 프로젝트 경험이 전혀 없는 domain owner가 요구→구현→검증→출시/인계→복구까지
   수행한 baseline 분포는 `INCONCLUSIVE`다.
2. **최소 의미 차이:** TCR/FCR이 몇 percentage point 변해야 사용자가 체감하고 추가 복잡성을 정당화하는지
   근거가 없다. 형성 연구와 vanilla pilot으로 보정한 뒤 confirmatory data 전에 동결해야 한다.
3. **이해 측정의 타당성:** 단순 teach-back, 만족도, 신뢰도는 적정 의존을 대신하지 못한다. correct/incorrect
   advice가 섞인 새 사례에서 선택·거절·escalation·recovery 행동과 objective oracle의 일치도를 검증해야 한다.
4. **프로세스의 인과 기여:** goppi 전체 효과가 보이더라도 어느 component가 증거·결정·복구를 개선했는지
   모르면 유지할 수 없다. static-checklist active control과 component ablation이 필요하다.
5. **장기·현장 효과:** lab 성공이 유지보수, 운영 변경, 모델/host drift, 비용, 사용자 피로에서도 유지되는지
   알 수 없다. confirmatory lab 뒤 prospective field follow-up이 필요하다.
6. **아키타입별 assurance surface:** 한 evidence bundle이 CLI, web app, API, data/ML, mobile에 모두 충분하지
   않다. primary archetype 결정 시 claim→evidence→recovery profile을 별도로 확증해야 한다.

## P2 — archetype 또는 규모 신호가 있을 때

- Safety-critical/medical/automotive/embedded engineering.
- Internationalization/localization and regional compliance.
- Mobile-store release and device testing.
- Enterprise platform engineering, internal developer portals, multi-team ownership.
- Regulated data retention, formal privacy impact assessment, sector-specific security.
- MLOps/model governance when goppi scaffolds data/ML systems.
- FinOps/sustainability beyond observable cost budgets.

## 가져온 과거 리서치의 상태

| 원본 | 현재 가치 | 다음 처리 |
|---|---|---|
| claudeck-v1 `harness-notes.md` | 운영 실패·gotcha의 historical signal | R0-3/R1-5 claim 후보만 추출; 제품 사실은 현재 docs로 재검증 |
| claudeck-v1 `researcher.md` | query reframing과 출처 규율 | **완료 2026-08-02**: 차이표 결과 전면 중복 아님 — EVIDENCE-POLICY에 없던 ① 제품범주명→도메인 스코핑 검색 규칙 ② 검색·fetch 예산 상한(초과 시 중단·보고) ③ 웹 불가 시 "미검증" 라벨 fallback을 `EVIDENCE-POLICY.md` "Search craft" 절로 흡수. 원본은 imported 보존(provenance); 도구 특정 내용(context7/Jina)은 하네스 설계 시점 재평가 |
| claudeck `harness-concept-notes.md` | 14-component taxonomy와 OSS census의 가장 큰 prior art | component claims를 6-plane map에 crosswalk; 당시 설계 PART V는 interpretation 유지 |
| gingoa corpus | 폭넓은 engineering topic map + raw census | 50개 문서 claim-level revalidation; taxonomy는 stable path로만 유지 |
| goppi `standards.md` | risk proportionality와 expiry 규칙 | general evidence와 goppi position을 분리해 R0-5로 흡수 |
| goppi `what-is-a-harness.md` | 성숙한 설계 synthesis | 객관 근거가 아니라 interpretation; superseded 상태 유지 |
| goppi harness eval results | agent 산출물·비용 component 차이에 대한 직접 empirical evidence; target-user trustworthy completion에는 불충분 | 원자료는 보존하고 새 protocol의 smoke/ablation 설계 입력으로만 사용; 기존 수치로 product GO 금지 |

## 유지보수 backlog (research unit 아님 — 단일 추적처)

> 2026-08-02에 `corpus/PROVENANCE.md`의 열린 체크리스트를 여기로 이관 (TODO 이원화 제거). 필요 시점에 처리.

- [ ] 활성 corpus의 `gingoa_applied:` frontmatter 잔존 6건 제거
- [ ] 태그 체계 통일: facts sub-doc `[정의/규정]/[데이터]/[주장]`+`[1차]/[2차]` ↔ corpus `[lit]/[census]/[inferred]` (급하지 않음 — 각 문서 frontmatter `method`가 체계를 명시)
- [ ] 부차 aspect 교차 링크: 09→05, 11→17, 12→19, 14→10, 16→23 (현재 "also serves" 문구로만 표시)
- [ ] census 원시 데이터 최신성 재수집 — 필요해진 claim에 한해
- [ ] `legacy/sources/` 잔여 접목 — imported/README "다음 처리" 기준, GAPS unit이 요구하는 claim만
- [x] `legacy/judgments/` 깨진 링크 21개 — 각 파일 상단 아카이브 배너로 처리 (2026-08-02)
- [x] `interpretation/00–04` SUPERSEDED 배너 (2026-08-02)
- [x] `matrix--facts-2026-08.md` 슬림화 — 수치 상이 목록 + 1차 재확인 대상만 유지 (2026-08-02)
- [x] `tools/` bytecode ignore 규칙 (2026-08-02; 기존 `__pycache__` 폴더는 rm 권한 정책상 잔존 — 무해)
- [x] claudeck-v1 `researcher.md` 차이표 (2026-08-02 — 위 표 참조)

## 각 research unit의 공통 Definition of Done

1. 질문·범위·제외·검색일·검색식이 있다.
2. 중요한 claim마다 source와 scope가 있다.
3. primary/official source가 없으면 그 사실을 명시한다.
4. 서로 다른 수치·주장을 보존하고 adjudication을 synthesis로 표시한다.
5. freshness/expiry trigger가 있다.
6. corpus validator와 해당 retrieval/eval check가 실행된다.
7. 다른 context의 reviewer가 source-to-claim trace와 과도한 일반화를 검사한다.
