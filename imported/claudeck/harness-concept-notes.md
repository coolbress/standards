# 오픈소스 AI 하네스 — 개념·표준·책장·시공 + 우리 하네스 설계 (통합 정리)

> **단일 통합 문서** — 객관 토대(PART 0–IV: 목표·개념·책장·시공)와 그 위에 세운 **우리 하네스 설계(PART V)** 를 *순차적으로* 정리. 앞으로의 정리도 여기에 계속 이어붙인다.
> 구성: **0** 완벽에 가까운 소프트웨어란?(목표 정의) · **I** 하네스 개념 · **II** 패키지 구조 · **III** 실증 책장(채택률 통계) · **IV** 시공 표준 도면(복붙 골격) · **V** 우리 하네스 설계(기능 도출·책장 매핑·아키타입).
> 출처: 프로덕션급 표준 6렌즈 + 멀티에이전트/GUI/inception 3렌즈 전수조사 + 정의·계보 문헌 + GitHub 스타순 census(455 repo → 27개 직접 구조조사) + 14개 컴포넌트 시공 표준 추출. (2026-06, 각 PART 말미·맨 아래 출처)

---

# PART 0 — 완벽에 가까운 소프트웨어란 무엇인가? (하네스가 만들려는 *목표*)

> **왜 이게 시작점인가.** 하네스의 존재 이유 = 비엔지니어가 AI 에이전트(바이브코딩)로 *진짜 좋은* 소프트웨어를 내게 *이끄는* 것. 그러려면 먼저 그 **목표 — "완벽에 가까운(프로덕션급) 소프트웨어"란 무엇인가** — 가 객관적으로 못박혀 있어야 한다(목표가 흐리면 이끌 곳도 없음). 아래는 *특정 앱에 비특화된 범용 정의*다.
> **편향 제거 방법:** 6개 권위 표준 계열을, *서로의 결과를 모르고* 또 *어떤 제품 의도도 모르는* 6개 독립 리서치 에이전트가 각자 조사 → 교차 *수렴*으로 도출. (어느 한 표준의 주장이 아니라, 독립 전통들이 *겹쳐서 동의하는 것*만 핵심으로 인정.)

## 0.1 조사한 6개 권위 렌즈

| 렌즈 | 대표 표준 | 무엇을 정의하나 | 계열 |
|---|---|---|---|
| ① 형식 품질모델 | **ISO/IEC 25010:2023** (SQuaRE) | 9개 제품품질 특성 분류 | 내재(I) |
| ② 클라우드네이티브 | **12/15-Factor · WAF**(AWS/Azure/GCP) | 운영 5기둥 방법론 | 운영(II) |
| ③ 운영 신뢰성 | **Google SRE** (PRR·SLO·골든시그널) | 프로덕션 준비 게이트 | 운영(II) |
| ④ 전달 성능 | **DORA/Accelerate · CD** (4→5 keys·Joel) | 전달 throughput·stability | 운영(II) |
| ⑤ 보안·공급망 | **OWASP ASVS/Top10/SAMM · NIST SSDF · SLSA** | 보안·무결성 baseline | 교차 |
| ⑥ craft·출하 | **Google Code Review · Test Pyramid · Fowler · Gruntwork** | 시니어 검수·출하준비 | 내재+운영 |

## 0.2 한눈에 — 3가지 메타 결론 (가장 중요)

**① 프로덕션급 = 두 *계열*의 합집합.** 표준들이 서로 겹치지 않는 두 family로 갈린다:
- **계열 I — 내재 산출물 품질**(*무엇인가* / 정적 / 코드·문서 검사로 확인): 정합성 · craft·유지보수성 · 보안속성 · 성능속성 · 테스트가능성 · 사용성 · 안전 · 호환. → *ISO 25010 + 코드 craft 전통.*
- **계열 II — 운영·전달 품질**(*어떻게 도나·출하되나* / 동적 / 런타임·파이프라인으로 확인): 운영신뢰성 · 관측성 · CI/CD전달 · 운영준비 · 12-factor위생 · 비용. → *12F·SRE·DORA·WAF 전통.*
- **결정타:** 두 계열은 *서로의 영역을 명시적으로 배제*한다. ISO 25010은 "프로세스·배포가능성·관측성은 범위 밖"이라 못박고(가장 많이 지적되는 학계 갭), SRE/DORA/12F는 "코드 craft·로직 정합성은 우리 게 아님"이라 한다. → **어느 한 계열도 단독으로 '프로덕션급'을 정의 못 한다. 정의 = 둘의 합집합이며, 소프트웨어 *아키타입*으로 가중된다.**
- 👉 **바이브코딩이 닿는 "돌아간다"는 계열 II의 *런타임 일부*만 만족** — 계열 I 전체(craft·정합성·유지보수)와 계열 II의 게이트(관측·롤백·전달)는 통째로 빈 채로 남는다. 시니어의 "와"는 *양 계열이 아키타입 가중치대로 다 채워졌을 때.* **하네스가 메워야 할 빈틈이 바로 이 차집합.**

**② 단일 보편 체크리스트를 주장하는 표준은 0개.** 전부 *맥락/아키타입 의존*을 명시(25010="특성별 상대중요도는 맥락별" · 12F="stateless 웹서비스용" · SRE="돌고 있는 서비스 가정" · 라이브러리·CLI는 대부분 미커버). → **"보편 코어 + 아키타입별 추가" 구조는 발명이 아니라 수렴에서 *관측되는 사실*.**

**③ 채점은 평균 아니라 *축별 게이트(weakest-link)*.** SRE PRR의 blocker(하나 걸리면 다른 강점 무관히 탈락) · OWASP ASVS 누적레벨(L2는 L1 전부 통과) · Definition of Done(전 항목 AND) · DORA(4축 동시) — 다수 권위 표준이 *축별 pass/fail*을 쓴다. **"한 축만 빛나게"는 어느 표준에서도 프로덕션급으로 안 쳐진다**(평균-점수 채점이 오히려 비표준). → 향후 품질 측정의 원리.

## 0.3 두 계열 — 상보성 구조

```
프로덕션급(아키타입 A) = 계열 I (내재 산출물 품질)  ∪  계열 II (운영·전달 품질)   ↺ 아키타입 A 가중치

계열 I (ISO 25010 + 코드 craft) ──── 무엇인가 / 정적 / 코드·문서 검사
   정합성 · craft·유지보수성 · 보안(속성) · 성능(속성) · 테스트가능성 · 사용성 · 안전 · 호환
        ▲ 명시적 배제: "프로세스·배포·관측은 범위 밖" (ISO 25010 §scope, 다수 비판)

계열 II (12F + SRE + DORA + WAF) ─── 어떻게 도나·출하되나 / 동적 / 런타임·파이프라인
   운영신뢰성 · 관측성 · CI/CD전달 · 운영준비 · 12-factor위생 · 비용
        ▲ 명시적 배제: "코드 craft·로직 정합성은 우리 영역 아님" (DORA/SRE/12F)
```

두 계열의 교집합은 거의 비어 있다(보안·신뢰성·성능 정도만 양쪽에서 언급되나, ISO는 *속성*으로·운영계열은 *런타임 거동*으로 — 각도가 다름). 그래서 둘은 경쟁이 아니라 **직교 보완**. 완벽에 가까운 = 한쪽만이 아니라 *양쪽을, 아키타입이 요구하는 만큼* 다 채운 것.

## 0.4 수렴 매트릭스 (15차원 × 6렌즈 × 신뢰도)

신뢰도 = 몇 개 *독립* 전통이 강제하는가. ●=핵심 주장 · ◐=부분/암시 · ○=명시적 범위 밖.

| # | 차원 | 25010 | 클라우드 | SRE | DORA | 보안 | craft | 신뢰도 |
|---|---|:--:|:--:|:--:|:--:|:--:|:--:|---|
| 1 | **정합성/스펙충족** (correct·edge·재현실행) | ● | ◐ | ○ | ◐ | ◐ | ● | **보편** |
| 2 | **신뢰성** (fault-tol·availability·recovery) | ● | ● | ● | ◐ | ◐ | ● | **보편** |
| 3 | **보안 & 공급망 무결성** | ● | ● | ◐ | ◐ | ● | ◐ | **보편(6/6)** |
| 4 | **성능·확장성** | ● | ● | ● | ○ | ○ | ● | **보편** |
| 5 | **검증/테스트** | ◐ | ○ | ◐ | ● | ◐ | ● | **높음** |
| 6 | **유지보수성/craft** (낮은복잡도·모듈화·가독) | ● | ○ | ○ | ○ | ◐ | ● | **높음(내재)** |
| 7 | **관측성** (모니터·메트릭·트레이싱·로그) | ○⚠️ | ● | ● | ◐ | ◐ | ● | **높음(운영)** |
| 8 | **전달위생** (CI/CD·배포자동·롤백·불변릴리스) | ○ | ● | ● | ● | ◐ | ● | **보편(프로세스)** |
| 9 | **문서** (README·아키·기여·런북) | ◐ | ○ | ● | ○ | ○ | ● | **높음** |
| 10 | **운영준비** (온콜·런북·인시던트·용량·포스트모템) | ○ | ◐ | ● | ◐ | ○ | ● | 운영아키타입 |
| 11 | **설정/시크릿/12-factor 위생** (env·stateless·disposability) | ○ | ● | ◐ | ○ | ● | ◐ | 서비스아키타입 |
| 12 | **사용성·접근성·상호작용** | ● | ○ | ○ | ○ | ○ | ◐ | UI아키타입 |
| 13 | **호환·상호운용·이식성** | ● | ◐ | ○ | ○ | ○ | ○ | 라이브러리/중간 |
| 14 | **안전(Safety)** (fail-safe·hazard·위험식별) | ●신규 | ○ | ○ | ○ | ○ | ○ | 안전critical전용 |
| 15 | **비용·지속가능성** | ○ | ● | ◐ | ○ | ○ | ◐ | 클라우드규모전용 |

**읽는 법:** **1~9 = 보편 코어**(어느 SW든 — 두 계열/내재계열이 강제). **10~11 = 서비스 아키타입**일수록 강제. **12~15 = 아키타입 조건부**(UI→12, 라이브러리→13, 안전critical→14, 클라우드규모→15). 차원 7·8이 ISO 25010에서 `○⚠️ 갭`인 게 학계 최다 지적 "deployability·observability 누락" — 운영계열이 정확히 그 구멍을 메운다(상보성의 증거).

## 0.5 보편 코어 9 vs 아키타입 조건부 6

| 층 | 차원 | 적용 |
|---|---|---|
| 🟩 **보편 코어** | 정합성 · 신뢰성 · 보안 · 성능·확장 · 테스트 · 유지보수/craft · 관측성 · 전달위생 · 문서 | **모든** 소프트웨어 |
| 🟦 **아키타입 추가** | 운영준비 · 12-factor위생 | http-api/백엔드/서비스 |
| 🟦 | 사용성·접근성(a11y·반응형·XSS/CSRF) | web-app/프론트 |
| 🟦 | 공개API안정성·semver·deprecation·호환매트릭스 | library/package |
| 🟦 | 종료코드·stdout/stderr·--help·인자검증·설정우선순위 | cli |
| 🟦 | 안전(fail-safe·hazard) | 안전critical/임베디드 |
| 🟦 | 비용·지속가능성 | 클라우드 규모 운영 |

## 0.6 6개 표준 렌즈 — 핵심 요지 + 범위·비판

**① ISO/IEC 25010:2023** (형식 제품품질, 계열 I 정전) — **9 특성**: Functional Suitability · Performance Efficiency · Compatibility · Interaction Capability(구 Usability, +inclusivity로 접근성 통합) · Reliability · Security(+resistance 신규) · Maintainability · Flexibility(구 Portability, +scalability 신규) · **Safety(2023 신규 최상위)**. Quality-in-use는 25019로 분리. *범위 밖:* 프로세스·CI/CD·**deployability·observability 부재**(최다 지적 갭)·pass/fail 임계 없음. *비판:* 실용지침 부재·실무자 중시(배포가능성/관측성/TTM)가 1급 아님. 계보 McCall→Boehm→FURPS→9126→25010.

**② 클라우드네이티브** (계열 II 운영) — **12-Factor**(codebase·deps·**config in env**·backing services·build/release/run 불변·**stateless processes**·port binding·concurrency·**disposability** graceful SIGTERM·dev/prod parity·logs as streams·admin processes) **+15F**(API-first·**telemetry**·authN/Z) **+16F**(state-as-a-service, stateless 편향 보정). **WAF 보편 5기둥**: Reliability·Security·Cost·Operational Excellence·Performance. *범위 밖:* stateless 웹서비스 전용(CLI·라이브러리·배치 미커버)·코드품질·테스트 무관. *비판:* stateless 절대주의·2011 PaaS 산물·env-var 시크릿 회전불가.

**③ Google SRE** (계열 II 운영신뢰성) — **PRR** 4축(extant-bugs·reliability·automation·monitoring), 항목=**blocker/non-blocker**. **하드 blocker(무조건):** 관측성·롤백·인시던트소유·SLO정의. **SLI**(good/total)·**SLO**(목표 N일)·**SLA**(계약)·**Error Budget**(=100−SLO, 소진시 기능freeze). **4 Golden Signals**: Latency·Traffic·Errors·Saturation. 비협상: blameless 포스트모템·런북(stale=부재)·toil<50%·테스트된 롤백. *범위 밖:* 돌고 있는 서비스 전제(라이브러리·CLI·로컬도구 미커버)·로직 정합성 미검. *비판:* Google-scale shaped·체크박스 의례화·과게이팅.

**④ DORA/CD** (계열 II 전달, 실증) — **4(→5) keys**: Deployment Frequency(Elite=on-demand)·Change Lead Time(<1일)·Change Fail Rate(~5%)·Recovery(<1시간)·+Rework Rate(2024). 군집은 매년 cluster-analysis 재산출(고정 임계 아님). **CD 원칙**: build-quality-in·small-batches·automate·"아프면 더 자주"·모두의 책임. **파이프라인 필수**: 트렁크기반·불변 버전아티팩트·테스트게이트(unit/integration/SAST/SCA/SBOM/서명)·배포자동·테스트 롤백. **Joel Test 12**(소스컨트롤·1스텝빌드·데일리빌드…). *범위 밖:* 전달 throughput·stability만 — 내재 코드품질·로직정합성 측정 안 함, 개인평가 금지(명시). *비판:* 상관≠인과·자기보고·임계불안정·Goodhart 게이밍.

**⑤ 보안·공급망** (교차) — **ASVS 5.0**(L1기본/L2표준/L3고급, 누적 · 17장: validation·authN·authZ·crypto·config·logging…) · **Top10:2025**(A01 Access Control·A02 Misconfig·**A03 Supply Chain 신규**·…·**A10 Mishandling Exceptional Conditions 신규**) · **NIST SSDF** 4군(PO·PS·PW·RV) · **SLSA** L0~L3(provenance·서명·격리빌드) · SBOM(CycloneDX/SPDX). **수렴 요건:** 입력검증·MFA·최소권한·deny-by-default·시크릿볼트(평문0)·의존성핀+CVE스캔·TLS1.2+/AES-256·서명아티팩트·secure-by-default·보안로깅. *범위 밖:* ASVS=웹/API만·SLSA=빌드만·AI/LLM 미커버. *비판:* ASVS L3 비현실적·비번 12→8 논란·SLSA L3 채택마찰·SSDF 자기증명.

**⑥ craft·출하** (시니어 렌즈) — **Google Code Review**: Design·Functionality(엣지·동시성)·**Complexity**(과설계 경계)·Tests(1급, 깨지는지)·Naming·Comments(*왜*)·Consistency·Documentation. 기준="완벽"이 아니라 **"코드베이스 health 순개선"**. **테스트**: Test Pyramid(unit多/e2e極少)·직렬화·통합경계 필수·**커버리지는 지표지 목표 아님**(Beck/Fowler)·contract testing·flaky=부채. **유지보수성**: cyclomatic(≤10)·중복(<5%)·coupling低/cohesion高·**churn×complexity=hotspot**·tech-debt ratio(SQALE<5%=A)·SIG/TÜViT(25010기반). **DoD**(스토리→스프린트→릴리스 3계층, 전 항목 AND). **출하준비 수렴**(Fowler8+Gruntwork): 소유/문서·배포(롤백·피처플래그)·관측성(골든시그널)·신뢰성(redundancy·서킷·RTO/RPO·테스트백업·N+2)·보안·테스트·성능·인시던트·거버넌스. *비판:* Clean Code 논쟁(과도 micro-function·"주석=실패"는 과함 — Ousterhout가 균형후계)·커버리지 게이밍·체크리스트 cargo-cult(2024 Cortex: 66% "팀간 기준 불일치"가 최대 장애).

## 0.7 객관적 공백 — 어느 표준도 (충분히) 못 메우는 것

- **AI/LLM 소프트웨어** — 프롬프트인젝션·환각·비결정성·데이터드리프트: ASVS·Top10·25010 모두 미커버(OWASP LLM Top10/AISVS는 별개·미성숙).
- **비서비스 아키타입(CLI·라이브러리·배치·임베디드)** — 12F/SRE/DORA는 *돌고 있는 서비스* 전제. 라이브러리의 공개API안정성·semver·deprecation은 *어느 주류 표준에도* 1급으로 없고 관례로만 존재.
- **로직/도메인 정합성 — "올바른 답인지"** — SRE(에러율)·DORA(전달)·25010(스펙충족까지)이 모두 약함. **스펙↔구현 일치 감사**는 표준화 안 됨.
- **에너지효율/지속가능성** — WAF만 1급. 25010은 1급 특성 아님(EU Green Software 압력 중).

**표준 간 불일치(객관):** stateless(12F 절대 ↔ AI세션/게임서버는 본질 stateful) · 커버리지(Joel/DoD "있나?" ↔ Beck/Fowler "수치를 목표 삼지 말라") · DORA 임계 매년 이동 · ASVS L3·SLSA L3는 표준 자신이 "비현실적" 인정.

## 0.8 채점 의미론 — 표준들의 실제 방식 (관측)

| 표준 | 채점 단위 | 의미 |
|---|---|---|
| SRE PRR | **blocker(축별 pass/fail)** | blocker 하나면 다른 강점 무관히 탈락 |
| OWASP ASVS | **누적 레벨** | L2는 L1 전부 통과(약한 항목 불허) |
| Definition of Done | **전 항목 AND** | 하나라도 미충족=Done 아님 |
| ISO 25010 | **특성별 목표치** | 합산/평균 아니라 특성마다 별도 목표 |
| DORA | **4~5축 동시** | 한 축만 Elite여도 종합 Elite 아님 |

→ 권위 표준 다수가 *축별 게이트(weakest-link)* 의미론. 평균-점수가 비표준. (= 0.2 ③의 근거.)

### 출처 (PART 0 — 프로덕션급 표준 6렌즈)
**ISO 25010:** [25010:2023](https://www.iso.org/standard/78176.html) · [iso25000.com 전체분류](https://iso25000.com/index.php/en/iso-25000-standards/iso-25010) · [arc42 2023 delta](https://quality.arc42.org/articles/iso-25010-update-2023) · [INNOQ 비판](https://www.innoq.com/en/articles/2023/02/iso-25010-shortcomings/) · [EASE 2025 DevOps 갭](https://dl.acm.org/doi/10.1145/3727967.3756847)
**클라우드:** [12factor.net](https://12factor.net/) · [15-Factor](https://domenicoluciani.com/2021/10/30/15-factor-app.html) · [AWS WAF](https://docs.aws.amazon.com/wellarchitected/latest/framework/the-pillars-of-the-framework.html) · [Azure WAF](https://learn.microsoft.com/en-us/azure/well-architected/pillars) · [GCP WAF](https://docs.cloud.google.com/architecture/framework) · [Google 16-Factor](https://cloud.google.com/transform/from-the-twelve-to-sixteen-factor-app) · [CNCF 성숙도](https://maturitymodel.cncf.io/tldr/)
**SRE:** [PRR(SRE Book ch32)](https://sre.google/sre-book/evolving-sre-engagement-model/) · [Implementing SLOs](https://sre.google/workbook/implementing-slos/) · [4 Golden Signals](https://developer.cisco.com/articles/what-are-the-golden-signals/what-are-the-golden-signals-that-sre-teams-use-to-detect-issues/) · [Cortex PRR](https://www.cortex.io/post/how-to-create-a-great-production-readiness-checklist)
**DORA/CD:** [DORA 2024](https://dora.dev/research/2024/dora-report/) · [Four Keys](https://dora.dev/guides/dora-metrics-four-keys/) · [4→5 metrics](https://cd.foundation/blog/2025/10/16/dora-5-metrics/) · [CD 원칙](https://continuousdelivery.com/principles/) · [Joel Test](https://www.joelonsoftware.com/2000/08/09/the-joel-test-12-steps-to-better-code/)
**보안/공급망:** [ASVS](https://owasp.org/www-project-application-security-verification-standard/) · [ASVS 5.0 개요](https://codific.com/owasp-asvs-a-comprehensive-overview/) · [Top10:2025](https://owasp.org/Top10/2025/) · [SAMM](https://owaspsamm.org/model/) · [NIST SSDF](https://csrc.nist.gov/projects/ssdf) · [SLSA](https://slsa.dev/) · [SLSA Levels](https://slsa.dev/spec/v1.0/levels) · [CycloneDX](https://cyclonedx.org/)
**craft/출하:** [Google Code Review](https://google.github.io/eng-practices/review/reviewer/looking-for.html) · [Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html) · [Gruntwork 체크리스트](https://gruntwork.io/blog/the-production-readiness-checklist-for-aws) · [Cortex 2024 준비도](https://www.cortex.io/report/the-2024-state-of-software-production-readiness) · [Clean Code 비판](https://bugzmanov.github.io/cleancode-critique/clean_code_second_edition_review.html) · [SIG/SQALE](https://www.researchgate.net/publication/340267633_Comparing_maintainability_index_SIG_Method_and_SQALE_for_technical_debt_identification) · [Scrum.org DoD](https://www.scrum.org/resources/blog/done-understanding-definition-done) · [Production-Ready Microservices](https://www.oreilly.com/library/view/production-ready-microservices/9781491965962/)

---

# PART I — 하네스의 개념

## 1. 한 문장 정의
**하네스 = 날것의 AI 모델을 "믿고 일 시킬 수 있는 일꾼"으로 바꿔주는, 모델 주위의 모든 장치.**

| 부품 | 뜻 | 비유 |
|---|---|---|
| **모델(Model)** | 추론하는 AI 두뇌 (Opus, Hermes 등) | 🧠 뇌 |
| **스캐폴드(Scaffold)** | 뇌가 *무엇을 보고 판단하는지* (지시문·스킬·자료) | 📋 뇌가 읽는 매뉴얼 |
| **하네스(Harness)** | *실제로 돌리는 몸* — 행동 반복·도구 실행·정지 판단·사고 방지 | 🦾 몸·신경계 |

➡ **에이전트(Agent) = 모델 + 하네스.** "챗봇에 그냥 말 거는 것" vs "Claude Code가 알아서 코드 짜고 테스트하고 커밋" = 하네스 유무의 차이.
어원: 소프트웨어 "test harness"(코드를 통제하며 자동 실행하는 발판). 마구(馬具)가 말을 통제·방향잡듯, 모델을 통제·방향잡는다.

## 2. 왜 중요한가 — "하네스는 모델만큼 중요하다"
같은 모델이라도 **하네스만 바꿔도 성능이 크게 갈린다**(실측):
- 같은 모델, 하네스 차이로 **점수 46% ↔ 80%** (34점 차)
- 하네스만 바꿔 **52% ↔ 76%** (모델·문제 고정 실험)
- 멀티에이전트 구성이 단일보다 **+90%**
- 연구 결론: *"신뢰성의 가장 큰 향상은 모델을 안 바꾸고 나온다."*

➡ 진짜 가치는 하네스에 있고, **모델은 갈아끼우는 부품** — "모델 비종속 / 사용자가 모델 자유 선택" 설계의 근거.

## 3. 하네스의 구성요소 12가지 (전체 해부도)
하네스 전체를 뜯으면 12개 층 — *호스트가 이미 가진 것 + 패키지가 더하는 것*을 모두 포함한 해부도:

1. **에이전트 루프** — 생각→행동→결과관찰→다시 (무한 반복)
2. **컨텍스트 관리** — 한정된 "기억 창" 채우기 + 넘치면 요약/압축
3. **도구 / MCP** — 바깥(파일·검색·DB)에 손 뻗는 통로 (MCP=표준 연결규약)
4. **메모리** — 작업중 기억 / 과거 실행 / 일반 지식 / 사용자 취향
5. **스킬(Skills)** — 재사용 가능한 "할 줄 아는 절차" (필요할 때만 펼침)
6. **오케스트레이션 / 멀티에이전트** — 일을 쪼개 위임하고 합침
7. **가드레일 / 권한** — "할 수 있는 것"을 제한해 사고 방지
8. **헌법 / 지시문** — 정체성·규칙 (CLAUDE.md / AGENTS.md)
9. **라우팅 / 제어흐름** — 다음 행동 결정 (규칙 vs 모델 판단)
10. **검증 / 품질 게이트** — 커밋 전 검사 (테스트·린트·리뷰)
11. **관측 / 평가(evals)** — 기록 + *품질을 숫자로 측정*
12. **세션 수명주기** — 체크포인트·이어하기·압축

> 이 중 **에이전트 루프·샌드박스·기본 컨텍스트창**은 보통 *호스트가 소유*. 패키지가 ship하는 건 그 위층(스킬·헌법·라우팅·게이트·메모리·오케스트레이션·evals 등) — PART II~IV가 그 부분을 다룬다.

---

# PART II — 오픈소스 하네스 "패키지"

## 4. 패키지란? (호스트 위에 얹히는 층)
Claude Code·Codex·Hermes 등은 *그 자체로 이미 하네스*다. "오픈소스 하네스 패키지" = 그 위에 얹혀 능력을 더하는 **플러그인(plugin)**, 배포처는 **마켓플레이스(marketplace)**.

```
[ 패키지 ]        헌법·스킬·라우팅·메모리·품질게이트·템플릿   ← 더하는 층 (PART II~IV)
──────────────────────────────────────────────────────────────
[ 호스트 하네스 ]  에이전트 루프·도구실행·기억창·샌드박스       ← Claude Code / Codex / Hermes (이미 있음)
──────────────────────────────────────────────────────────────
[ 모델 ]          Opus / Hermes-4 …                            ← 갈아끼움
```

즉 밑바닥(루프·샌드박스)은 호스트가 가지고, 패키지는 **"머리쓰는 층 + 프로세스 층"**을 만들어 각 호스트에 꽂는다.

## 5. 패키지의 3겹 구조
패키지를 분해하면 3겹 — 무엇을 담고(A), 어떻게 호스트에 붙고(B), 어떻게 배포·유지되나(C):

- **겹 A — 호스트 공식 컴포넌트 5종 (몸통):** Skills · Agents · Commands · Hooks · MCP servers.
  ⭐ Skills는 **오픈 표준(agentskills.io, 2025-12)** → 한 곳에서 만든 스킬이 CC·Codex·Cursor·Gemini에서 *그대로* 돎(크로스호스트 이식성의 핵심). *각 컴포넌트의 채택률은 PART III, 시공법은 PART IV.*
- **겹 B — 호스트 결합 어댑터 (붙는 방식, 호스트별로 다름):** 매니페스트(`.claude-plugin/plugin.json`+`marketplace.json`) · 훅 등록(settings.json array-merge) · MCP 설정(`.mcp.json`). 스킬·MCP는 대체로 공통, **훅·매니페스트가 호스트별로 갈리는 부분**.
- **겹 C — 지원 기계장치 (배포·유지):** CLI/설치기(npm bootstrap) · 설정 시스템(모델↔역할 2블록) · 헌법·템플릿 · doctor(설치 무결성·드리프트) · eval 하네스(*패키지 자체 품질 측정*) · 문서·버전(README·semver·마켓 등록).

→ 요약: **A=무엇을 담나(이식 표준 핵심) · B=어떻게 붙나(호스트별 변주) · C=어떻게 배포·증명하나.**

---

# PART III — 실증: 표준 책장 (OSS 27개 전수조사)

> PART II가 *이론*이라면 이건 *실측*. GitHub 스타순 census(455 repo)에서 "하네스 증강 패키지"와 같은 종 27개를 골라, 각 repo의 **실제 파일트리+README를 직접 조사**(설명문 금지, 실증거 only)해 무엇을 ship하는지 센 결과. (27 에이전트 병렬, 617k 토큰.)

## 6.1 분모 — "스타 상위 ≠ 하네스 패키지"
스타 상위 120개 중 "증강 패키지" 종은 **27개(22.5%)**. 나머지 93개는 다른 종:
- **A.** 호스트 에이전트(기반 자체) ~19 — openclaw·codex·claude-code·gemini-cli·goose·aider·cline·warp
- **B.** 프레임워크/플랫폼 ~14 — langchain·dify·crewAI·MetaGPT·Flowise·AutoGPT
- **C. ★ 증강 패키지 27** — 분석 대상
- **D.** 큐레이션 리스트 ~12 / **E.** 프롬프트유출·가이드 ~10 / **F.** 프록시·라우터 ~9 / **G.** 제품·앱·도메인 ~28

→ 실제 비교군은 **27개**.

## 6.2 책장 3선반 (컴포넌트 채택률, n=27)
- **🟩 FLOOR (척추, ≥70%):** `Skills 89%` · `CI 81%` · `Constitution(CLAUDE/AGENTS.md) 74%` · `marketplace.json 74%` · `plugin.json 70%`
- **🟨 COMMON (성숙하면, 40–60%):** `commands 59%` · `hooks 56%` · `evals-dir 52%` · `agents 52%` · `templates 48%` · `MCP 44%`
- **🟥 SPARSE (희소, <35%):** `model-binding 33%` · `elicitation 33%` · `enforced-gates 30%`

한 줄: 표준 척추 = **`SKILL.md + plugin.json + marketplace.json + CLAUDE.md/AGENTS.md + CI`**. 성숙하면 `commands·hooks·agents·MCP·templates`. 희귀한 건 `모델바인딩·인터뷰·차단게이트`.

## 6.3 두께 분포 (12개 만점)
- **12/12 완전체:** affaan-m/ECC · Yeachan-Heo/oh-my-claudecode · Yeachan-Heo/oh-my-codex (단 3개)
- **subtype:** skill-pack 15(56%, 단일 도메인·스킬+매니페스트만) · multi-component 7(26%) · mcp-tool·methodology·memory·marketplace 각 소수
→ **과반(56%)이 얇은 skill-pack.** 풀 하네스 패키지는 1/4뿐.

## 6.4 사용자 경험(UX) — 양봉 분포
- **설치:** npm/npx **41%** ↔ `/plugin marketplace add` **41%** (대부분 *둘 다* 제공) · 나머지 curl·git·pip 소수
- **사용:** NL 자동발동(SKILL.md 프론트매터 자동발견) **41%** ↔ slash-command **37%** · mcp·auto-hook 소수

## 6.5 Moat 3종(인터뷰→차단게이트→eval) 점유 + 빈 칸
**5/27이 3종을 모두 닫음:** garrytan/gstack · gsd-build/get-shit-done · Yeachan-Heo/oh-my-claudecode · Imbad0202/academic-research-skills · Yeachan-Heo/oh-my-codex. 특히 oh-my-claudecode·oh-my-codex는 **12/12 완전체 + 3종 전부**.

그러나 다음 교집합은 **0/27** (landscape의 빈 칸):

| 축 | 27개 중 점유 | 정밀 판정 |
|---|---|---|
| 비엔지니어가 사용자 | **0/27** | 27개 전부 *엔지니어 운영* 도구 |
| 아이디어→프로젝트 기초 scaffold | **0/27** | elicit 9개는 전부 *개발태스크 명료화*(deep-interview류), 프로젝트 기초 골격 생성 0 |
| spec-준수 / production-readiness eval | **0/27** | evals 15개는 전부 *SWE-bench·도메인품질*. "빌드된 SW가 스펙대로+시니어급인가" audit은 0 |

→ 컴포넌트 *집합*은 점유됐지만 **{비엔지니어 + 아이디어→골격 + spec-준수 eval} 3중 교집합**은 미점유.

## 6.6 부록 — 27개 전수 매트릭스
표기: S=skills A=agents C=commands H=hooks M=mcp P=plugin.json K=marketplace T=templates E=evals(dir) N=constitution B=model-binding I=ci · 뒤 `el/g/ev` = elicit/gates/evals(capability)

| repo | subtype | #/12 | 컴포넌트 | el/g/ev | 설치 | 사용 |
|---|---|---|---|---|---|---|
| obra/superpowers | skill-pack | 6 | S·H·P·K·E·N | ✓/✗/✓ | mkt | nl |
| affaan-m/ECC | multi | **12** | ALL | ✗/✓/✓ | npm | nl |
| multica/andrej-karpathy-skills | skill-pack | 4 | S·P·K·N | ✗/✗/✗ | mkt | read |
| anthropics/skills | skill-pack | 3 | S·K·T | ✗/✗/✗ | mkt | nl |
| mattpocock/skills | skill-pack | 4 | S·P·N·I | ✓/✗/✗ | npm | slash |
| msitarzewski/agency-agents | skill-pack | 4 | A·M·T·I | ✗/✗/✗ | curl | nl |
| garrytan/gstack | skill-pack | 9 | S·A·C·H·T·E·N·B·I | ✓/✓/✓ | git | slash |
| nextlevelbuilder/ui-ux-pro-max | skill-pack | 6 | S·P·K·T·N·I | ✗/✗/✗ | npm | nl |
| thedotmack/claude-mem | memory | 10 | S·A·C·H·M·P·K·E·N·I | ✗/✗/✓ | npm | auto-hook |
| JuliusBrussee/caveman | skill-pack | 10 | S·A·C·H·M·P·K·E·N·I | ✗/✗/✓ | curl | nl |
| safishamsi/graphify | skill-pack | 5 | S·C·H·N·I | ✗/✗/✗ | pip | slash |
| nexu-io/open-design | mcp-tool | 10 | S·A·C·M·K·T·E·N·B·I | ✗/✓/✓ | mkt | mcp |
| gsd-build/get-shit-done | methodology | 7 | A·C·H·T·N·B·I | ✓/✓/✓ | npm | slash |
| addyosmani/agent-skills | multi | 8 | S·A·C·H·P·K·N·I | ✓/✗/✗ | mkt | slash |
| ruvnet/ruflo | multi | 10 | S·A·C·H·M·P·K·T·B·I | ✗/✗/✗ | npm | nl |
| santifer/career-ops | multi | 7 | S·C·P·K·T·N·I | ✓/✗/✗ | npm | slash |
| colbymchenry/codegraph | mcp-tool | 3 | M·E·I | ✗/✗/✓ | curl | mcp |
| Leonxlnx/taste-skill | skill-pack | 3 | S·P·K | ✗/✗/✗ | npm | nl |
| mvanhorn/last30days-skill | skill-pack | 11 | S·A·C·H·M·P·K·E·N·B·I | ✗/✗/✓ | mkt | slash |
| DietrichGebert/ponytail | skill-pack | 9 | S·C·H·M·P·K·E·N·I | ✗/✗/✓ | mkt | auto-hook |
| wshobson/agents | marketplace | 11 | S·A·C·H·M·P·K·E·N·B·I | ✗/✓/✓ | mkt | slash |
| Yeachan-Heo/oh-my-claudecode | multi | **12** | ALL | ✓/✓/✓ | mkt | slash |
| kepano/obsidian-skills | skill-pack | 3 | S·P·K | ✗/✗/✗ | mkt | nl |
| coreyhaines31/marketingskills | skill-pack | 6 | S·P·K·E·N·I | ✗/✗/✓ | npm | nl |
| Imbad0202/academic-research-skills | multi | 10 | S·A·C·H·P·K·T·E·N·I | ✓/✓/✓ | mkt | slash |
| Yeachan-Heo/oh-my-codex | multi | **12** | ALL | ✓/✓/✓ | npm | cli |
| K-Dense-AI/scientific-agent-skills | skill-pack | 3 | S·T·I | ✗/✗/✗ | npm | nl |

---

# PART IV — 시공 표준 도면 (각 칸을 *어떻게 짓는가*)

> PART III가 "무엇을/얼마나 ship하나"라면 이건 "각 칸을 *표준대로 짓는 법*". 공식 스펙(agentskills.io·Claude Code docs·MCP·agents.md) + 캐논 구현 3~4개의 **실제 파일을 직접 fetch**해 추출(14 에이전트, 458k 토큰).
> 각 카드 = ①공식표준 ②포맷 ③위치 ④스키마 ⑤관례 ⑥**최소 골격(복붙)** ⑦변종 + 실증 출처. 골격은 무손실 보존.


## 시공 도면 — 한눈 요약 (표준점)

| # | 컴포넌트 | 선반 | 공식? | 위치 |
|---|---|---|---|---|
| 1 | Skills | 🟩 FLOOR | ✅ 공식 | One skill = one directory containing `SKILL.md`. |
| 2 | Plugin manifest | 🟩 FLOOR | ✅ 공식 | Path is plugin-root/.claude-plugin/plugin.json. |
| 3 | Marketplace manifest | 🟩 FLOOR | ✅ 공식 | `.claude-plugin/marketplace.json` at the repository root (the `.claude-plugin/` directory,… |
| 4 | Constitution | 🟩 FLOOR | ✅ 공식 | Repository ROOT is canonical for all of: `CLAUDE.md`, `AGENTS.md`, `GEMINI.md` (all four r… |
| 5 | CI | 🟩 FLOOR | ✅ 공식 | `.github/workflows/*.yml` at the REPO ROOT (must be exactly this path — GitHub only discov… |
| 6 | Slash commands | 🟨 COMMON | ✅ 공식 | Project scope: `.claude/commands/<name>.md` → `/<name>` (or `/<plugin>:<name>` when shippe… |
| 7 | Hooks | 🟨 COMMON | ✅ 공식 | Plugin convergent path: <plugin-root>/hooks/hooks.json (ponytail, agent-skills, claude-mem… |
| 8 | Agents | 🟨 COMMON | ✅ 공식 | Spec-defined, priority order (higher wins on name collision): managed (`<managed-settings>… |
| 9 | Evals harness | 🟨 COMMON | 🟡 de-facto | Two dominant placements. |
| 10 | Templates | 🟨 COMMON | 🟡 de-facto | A directory literally named `templates/` is the universal convention. |
| 11 | MCP server | 🟨 COMMON | ✅ 공식 | CONFIG `.mcp.json`:   - Project scope → repo root `/.mcp.json` (checked into VCS, shared w… |
| 12 | Model-binding config | 🟥 SPARSE | 🟡 de-facto | Codex-native: project `./.codex/config.toml` OR user `${CODEX_HOME:-~/.codex}/config.toml`… |
| 13 | Elicitation | 🟥 SPARSE | 🟡 de-facto | Skill: `skills/<category>/<skill-name>/SKILL.md` (mattpocock uses category dirs: `skills/p… |
| 14 | Enforced gates | 🟥 SPARSE | 🟡 de-facto | Claude Code plugin: `hooks/hooks.json` at plugin root, with scripts under `hooks/` or `scr… |

---

## 1. Skills (SKILL.md)  ·  🟩 FLOOR

**① 공식 표준** — YES — official, two-layer. (1) The **Agent Skills open standard** at agentskills.io is the cross-tool spec Claude Code conforms to. (2) **Claude Code skills docs** (code.claude.com/docs/en/skills, redirected from docs.claude.com) define the canonical implementation + CC-specific extensions. Spec mandates: a skill is a directory containing a required `SKILL.md` = YAML frontmatter (between `---` markers) + markdown body. The frontmatter tells Claude WHEN to use the skill; the body is the instructions loaded only when triggered (progressive disclosure — body costs ~0 context until used). Per the spec table, ALL frontmatter fields are technically optional; only `description` is *recommended* so the model knows when to auto-load. CC extends the open standard with `disable-model-invocation`, `user-invocable`, `allowed-tools`/`disallowed-tools`, `effort`, `paths`, subagent execution, and dynamic context injection. Note: custom commands (`.claude/commands/*.md`) have been MERGED into skills — both produce `/name` and share the same frontmatter.

**② 포맷** — Markdown file named exactly `SKILL.md`, with a leading YAML frontmatter block delimited by `---` lines, followed by a Markdown body (`# Title`, `## Overview`, `## When to Use`, steps, etc.). The file lives inside a per-skill *directory* whose name (lowercase-hyphenated by de-facto convention) becomes the `/command`. Supporting files (REFERENCE.md, scripts/, templates/, examples/) sit alongside SKILL.md in the same directory and are referenced from the body by relative path so the model loads them on demand.

**③ 위치** — One skill = one directory containing `SKILL.md`. Three discovery levels (spec-mandated precedence: enterprise > personal > project; a same-named skill overrides a bundled one): Personal `~/.claude/skills/<skill-name>/SKILL.md` (all projects); Project `.claude/skills/<skill-name>/SKILL.md` (this repo; also discovered in parent dirs up to repo root and on-demand in nested `.claude/skills/` for monorepos); Plugin `<plugin>/skills/<skill-name>/SKILL.md` (namespaced `plugin-name:skill-name`). The directory name → command name (e.g. `.claude/skills/deploy-staging/` → `/deploy-staging`). Canonical public repos place them at `skills/<skill-name>/SKILL.md` from repo root.

**④ 스키마(키·필수/선택)** —

Frontmatter keys (all optional per spec; only `description` recommended):
- `name` (string, optional) — display label in listings; defaults to directory name. Does NOT change the `/command` you type (except for a plugin-root SKILL.md). De-facto: lowercase-hyphenated, matches dir name.
- `description` (string, RECOMMENDED) — what it does + WHEN to use; drives auto-trigger. If omitted, first body paragraph is used. Put the key use case FIRST: combined `description`+`when_to_use` is truncated at **1,536 characters** in the listing.
- `when_to_use` (string, optional, CC) — extra trigger phrases/examples; appended to description, counts toward the 1,536-char cap.
- `disable-model-invocation` (bool, optional, CC; default false) — true = manual `/name` only, never auto-loaded (also blocks subagent preload).
- `user-invocable` (bool, optional, CC; default true) — false = hide from `/` menu (background knowledge).
- `allowed-tools` (string|YAML list, optional, CC) — tools usable without permission prompt while active (space/comma-sep, e.g. `Read Grep`).
- `disallowed-tools` (string|YAML list, optional, CC) — tools removed from the pool while active.
- `effort` (enum, optional, CC) — low|medium|high|xhigh|max; overrides session effort.
- `paths` (string|YAML list, optional, CC) — glob(s); auto-load only when working on matching files.
- `license` (string, optional) — seen in anthropics/skills (e.g. pdf).
- `arguments` (YAML list, optional, CC) — named args mapping to `$name` positional placeholders in the body.
Body: free Markdown. De-facto sections observed: `# Title`, `## Overview`, `## When to Use`, numbered workflow steps, links to supporting files.

**⑤ 관례·주의** —

- Directory name = command; keep it lowercase-hyphenated and descriptive (gerund phrases common in obra: `writing-skills`, `test-driven-development`).
- `name` in frontmatter should equal the directory name (all 4 repos do this).
- `description` is the highest-leverage field: third person, lead with what it does, then explicit "Use when…" triggers (every repo front-loads triggers). Stay well under 1,536 chars.
- Progressive disclosure: keep SKILL.md focused/short; push long reference material (REFERENCE.md, FORMS.md), scripts, and examples into sibling files referenced by relative path — they load only when the body points to them (anthropics/pdf, skill-creator).
- Body voice = imperative instructions to the agent ("Write the test first. Watch it fail."), often with a hard rule / "Iron Law" callout.
- License field only where redistribution matters (anthropics proprietary skills).
- Cross-host portability: the agentskills.io standard means SKILL.md works across tools; Codex/Copilot/Gemini also read `~/.agents/skills/`. CC-only fields (effort, paths, allowed-tools) are ignored elsewhere — keep core behavior in the body, not in CC-only frontmatter, for portable skills.
- Live reload: edits to SKILL.md text are picked up mid-session; a brand-new top-level skills dir needs a restart.

**⑥ 최소 골격 (복붙 시작점)** —

````text
Directory layout (personal skill):

  ~/.claude/skills/summarize-changes/
  └── SKILL.md            # required; the only mandatory file

Minimal copy-paste SKILL.md:

  ---
  name: summarize-changes
  description: Summarizes uncommitted changes and flags anything risky. Use when the user asks what changed, wants a commit message, or asks to review their diff.
  ---

  # Summarize Changes

  ## Overview
  Review the working tree and report what changed, grouped by intent, flagging anything risky.

  ## Steps
  1. Run `git status` and `git diff` to read the uncommitted changes.
  2. Group the changes by logical intent (feature, fix, refactor, config).
  3. For each group, write one line: what changed and why it matters.
  4. Flag risks explicitly: secrets, deleted tests, broad blast radius, schema/migration edits.
  5. End with a one-line summary suitable as a commit message subject.

Manual-only command variant (add to frontmatter):

  disable-model-invocation: true   # only triggers via /summarize-changes

Larger skill with supporting files (anthropics pattern):

  skills/pdf/
  ├── SKILL.md          # overview + quick start + pointers
  ├── REFERENCE.md      # loaded only when SKILL.md links to it
  ├── FORMS.md
  └── scripts/fill_form.py
````

**⑦ 변종·분기** —

- **Frontmatter minimalism**: obra/superpowers uses the absolute minimum — `name` + `description` ONLY (description is a single "Use when…" clause, no separate when_to_use). anthropics/skills also stays at name+description (+`license` on proprietary ones). Neither uses allowed-tools/effort/paths in the public skills — those CC extensions are rare in canon.
- **Description style**: anthropics writes long, exhaustive trigger lists ("This includes… If the user mentions a .pdf file…"); obra writes one terse trigger clause; addyosmani writes a sentence of what-it-does + 2-3 "Use when" sentences; kepano leads with the action then "Use when working with .base files…".
- **Body shape**: obra = principle-driven process docs with hard rules/"Iron Law" and cross-skill prerequisites (`You MUST understand superpowers:test-driven-development`); anthropics = tool/operation guides with code blocks + offloaded REFERENCE files (progressive disclosure heavily used); addyosmani = multi-axis checklists; kepano = numbered create→validate workflows for a file format.
- **Supporting files**: anthropics splits into REFERENCE.md/FORMS.md/scripts/ + ships a `template/SKILL.md` and a `skill-creator` meta-skill with evals; obra cross-links reference docs per runtime; kepano/addyosmani tend to be single-file SKILL.md.
- **Naming**: obra = gerund phrases (`writing-skills`); others = noun/topic (`pdf`, `obsidian-bases`, `code-review-and-quality`).
- **Command merge**: a flat `.claude/commands/foo.md` (no directory, no supporting files) is the legacy equivalent — same frontmatter, but skills are recommended for supporting-file capability.

**증거(실증 fetch)** — `anthropics/skills:template/SKILL.md` · `anthropics/skills:skills/skill-creator/SKILL.md` · `anthropics/skills:skills/pdf/SKILL.md` · `obra/superpowers:skills/writing-skills/SKILL.md` · `obra/superpowers:skills/test-driven-development/SKILL.md` · `addyosmani/agent-skills:skills/code-review-and-quality/SKILL.md` · `kepano/obsidian-skills:skills/obsidian-bases/SKILL.md` · `docs:code.claude.com/docs/en/skills` · `spec:agentskills.io`

---

## 2. Plugin manifest (.claude-plugin/plugin.json)  ·  🟩 FLOOR

**① 공식 표준** — OFFICIAL SPEC EXISTS. Claude Code "Plugins reference" (code.claude.com/docs/en/plugins-reference, 301-redirected from docs.claude.com/en/docs/claude-code/plugins) defines the full plugin.json schema authoritatively; the "Create plugins" guide gives the minimal example. Spec-MANDATED: (a) the manifest lives at .claude-plugin/plugin.json; (b) the manifest is OPTIONAL entirely — if omitted, Claude Code auto-discovers components in default locations and derives the plugin name from the directory name; (c) if a manifest IS present, name is the ONLY required field (kebab-case, no spaces); (d) unrecognized top-level fields are silently ignored, so a plugin.json can double as a package.json / VS Code / Cursor / MCPB manifest; (e) ONLY plugin.json goes inside .claude-plugin/ — all component dirs (skills/, agents/, hooks/, commands/, .mcp.json) live at the plugin ROOT, never inside .claude-plugin/. Everything beyond name is optional metadata or an explicit component-path override.

**② 포맷** — Single strict-JSON file named plugin.json (UTF-8, no comments, no frontmatter). Path-valued fields (skills, commands, agents, hooks, mcpServers, lspServers, outputStyles) may be EITHER a single string OR an array of strings; paths are relative to plugin root, conventionally dot-slash-prefixed. The runtime variable CLAUDE_PLUGIN_ROOT (referenced as ${CLAUDE_PLUGIN_ROOT}) expands to the plugin's install dir and is used inside string values (notably hook/MCP command strings) for portable absolute paths — observed in caveman's hooks.

**③ 위치** — Path is plugin-root/.claude-plugin/plugin.json. The .claude-plugin/ dir sits at the plugin root and contains ONLY this file (plus, at a marketplace repo root, marketplace.json). Two real layouts: (1) single-plugin repo gives .claude-plugin/plugin.json at repo root (addyosmani/agent-skills, JuliusBrussee/caveman, ruvnet/ruflo root). (2) monorepo of many plugins gives one manifest per subdir, e.g. plugins/NAME/.claude-plugin/plugin.json (wshobson/agents ~80; ruvnet/ruflo ~38 under plugins/). Component dirs (skills/, agents/, hooks/) sit as siblings of .claude-plugin/, NOT inside it.

**④ 스키마(키·필수/선택)** —

REQUIRED: name (string, kebab-case, no spaces) — sole required field; namespaces all components (/plugin-name:skill). OPTIONAL metadata: version (string, semver; if omitted and git-distributed the commit SHA is used so every commit = a new version); description (string, shown in plugin manager); author (object {name required-within, email?, url?}); displayName (string); homepage (string URL); repository (string URL OR object {type,url} — both seen: addyosmani string, ruflo object); license (string SPDX e.g. MIT); keywords (string[]); bugs (object {url}); category (string); tags (string[]); engines (object e.g. {claudeCode: >=2.0.0, node: >=20.0.0}). OPTIONAL component-path overrides (string | string[], default-discovered if omitted): skills, commands, agents, hooks (path to hooks.json), mcpServers (path to a json file OR an inline object map of server defs — ruflo uses inline {command,args,description,optional}), lspServers, outputStyles. OPTIONAL: experimental (object {themes?, monitors?}), dependencies (array of string | {name,version}). Unknown top-level keys are ignored.

**⑤ 관례·주의** —

- name MUST be kebab-case, unique, equals the namespace prefix users see; match it to the directory name. - Component-path fields are usually OMITTED — rely on default discovery (skills/, agents/, hooks/hooks.json, .mcp.json at root). Only set them to point at non-default locations (addyosmani points commands at [./.claude/commands, ./commands] and lists agents file-by-file). - In any command string (hooks, mcpServers) use ${CLAUDE_PLUGIN_ROOT}, not relative paths, so it works regardless of install dir. - version: set explicitly for controlled updates; omit to let the git SHA drive per-commit versioning. - Strict JSON only — no trailing commas/comments. - Real manifests are small: 4–8 keys typical (wshobson = name/version/description/author/license only); kitchen-sink (ruflo root, ~14 keys incl. keywords/tags/engines/mcpServers) is the outlier. - Run `claude plugin validate` before publishing. - GOTCHA: never place skills/agents/hooks INSIDE .claude-plugin/ — the docs call this the most common mistake.

**⑥ 최소 골격 (복붙 시작점)** —

````text
Minimal valid (spec quickstart):
{
  "name": "my-first-plugin",
  "description": "A greeting plugin to learn the basics",
  "version": "1.0.0",
  "author": { "name": "Your Name" }
}

Typical real (distilled from wshobson/agents backend-development):
{
  "name": "backend-development",
  "version": "1.3.2",
  "description": "Backend API design and test-driven backend development",
  "author": { "name": "Seth Hobson", "email": "seth@example.com" },
  "license": "MIT"
}

On-disk layout (component dirs are SIBLINGS of .claude-plugin/, at plugin root):
my-plugin/
  .claude-plugin/
    plugin.json      <-- ONLY this file goes here
  skills/
    hello/SKILL.md
  agents/
    reviewer.md
  hooks/
    hooks.json

Manifest WITH an inline MCP server + a hook (real pattern, caveman/ruflo), using ${CLAUDE_PLUGIN_ROOT}:
{
  "name": "my-plugin",
  "version": "0.1.0",
  "description": "Does a thing",
  "author": { "name": "Me", "url": "https://github.com/me" },
  "license": "MIT",
  "hooks": {
    "SessionStart": [
      { "hooks": [ { "type": "command", "command": "node \"${CLAUDE_PLUGIN_ROOT}/src/hooks/activate.js\"", "timeout": 5 } ] }
    ]
  },
  "mcpServers": {
    "my-server": { "command": "npx", "args": ["my-server@latest", "mcp", "start"], "optional": true }
  }
}
````

**⑦ 변종·분기** —

1) MINIMAL-METADATA vs KITCHEN-SINK: wshobson plugins carry just name/version/description/author/license; ruflo root carries ~14 keys (keywords, tags, category, engines, bugs, inline mcpServers). Both valid. 2) NO-VERSION vs PINNED-VERSION: caveman + addyosmani OMIT version (rely on git SHA per-commit updates); wshobson/ruflo pin semver. 3) repository STRING vs OBJECT: addyosmani uses a plain URL string; ruflo uses {type:git,url:...}. 4) COMPONENT PATHS implicit vs explicit: most rely on default discovery and never declare skills/agents/commands; addyosmani explicitly enumerates commands (array of dirs) and agents (array of individual .md files) and points skills at a custom dir. 5) mcpServers AS-FILE-PATH vs INLINE-OBJECT: spec shows a path string (./mcp-config.json); ruflo embeds the full server map (command/args/description/optional) directly in plugin.json. 6) REPO TOPOLOGY: single root plugin (addyosmani, caveman) vs monorepo with one manifest per plugin subdir (wshobson ~80, ruflo ~38) — the monorepo root then also carries .claude-plugin/marketplace.json. 7) CROSS-HOST manifests: wshobson ships a parallel .codex-plugin/plugin.json per plugin (and a root .cursor-plugin/plugin.json) — same manifest shape reused for other agent hosts, leveraging the ignore-unknown-fields rule.

**증거(실증 fetch)** — `claude-code-docs:code.claude.com/docs/en/plugins` · `claude-code-docs:code.claude.com/docs/en/plugins-reference` · `wshobson/agents:plugins/backend-development/.claude-plugin/plugin.json` · `wshobson/agents:plugins/*/.codex-plugin/plugin.json` · `wshobson/agents:.cursor-plugin/plugin.json` · `addyosmani/agent-skills:.claude-plugin/plugin.json` · `JuliusBrussee/caveman:.claude-plugin/plugin.json` · `ruvnet/ruflo:.claude-plugin/plugin.json` · `ruvnet/ruflo:plugins/ruflo-core/.claude-plugin/plugin.json`

---

## 3. Marketplace manifest (.claude-plugin/marketplace.json)  ·  🟩 FLOOR

**① 공식 표준** — SPEC-MANDATED. Official Claude Code spec exists: "Create and distribute a plugin marketplace" at code.claude.com/docs/en/plugin-marketplaces (redirected from docs.claude.com/en/docs/claude-code/plugin-marketplaces). It mandates: a JSON file at `.claude-plugin/marketplace.json`; required top-level keys `name`, `owner`, `plugins`; each plugin requires `name` and `source`. Plugin entries may carry ANY field from the plugin-manifest schema (description, version, author, commands, hooks, etc.) PLUS marketplace-specific fields `source`, `category`, `tags`, `strict`. Source can be a relative string path or a typed object (`github`, `url`, `git-subdir`, `npm`). Users add via `/plugin marketplace add` and refresh via `/plugin marketplace update`. All 4 canonical repos conform.

**② 포맷** — JSON (single object), UTF-8. Lives at fixed path `.claude-plugin/marketplace.json` in the repo root. No frontmatter. Top-level object with `name` (string), `owner` (object), optional `metadata` (object), and `plugins` (array of objects). Note: the file's own `source` (object form) reuses the key name `source` for the type discriminator, e.g. `"source": {"source": "github", "repo": "..."}`.

**③ 위치** — `.claude-plugin/marketplace.json` at the repository root (the `.claude-plugin/` directory, NOT `.claude/`). Confirmed in anthropics/skills, ruvnet/ruflo, multica-ai/andrej-karpathy-skills, and wshobson/agents — the latter additionally mirrors it to `.agents/plugins/marketplace.json` and `.cursor-plugin/marketplace.json` for other hosts, but `.claude-plugin/marketplace.json` is the canonical Claude path.

**④ 스키마(키·필수/선택)** —

TOP-LEVEL:
- `name` (string, REQUIRED) — marketplace identifier, kebab-case (e.g. "anthropic-agent-skills", "claude-code-workflows", "ruflo", "karpathy-skills").
- `owner` (object, REQUIRED) — `{ name (REQUIRED), email?, url? }`.
- `plugins` (array, REQUIRED) — list of plugin entries.
- `metadata` (object, OPTIONAL) — `{ description?, version?, pluginRoot? }`. `pluginRoot` is a base dir prepended to relative plugin sources. `description`/`version` here are accepted for backward-compat.
- `description` (string, OPTIONAL) — top-level description (ruflo uses this instead of metadata.description).
- `id` (string, OPTIONAL/de-facto) — used by multica-ai mirroring `name`; not in the spec's required/optional tables.

PLUGIN ENTRY:
- `name` (string, REQUIRED) — plugin id.
- `source` (string | object, REQUIRED) — relative path string (e.g. "./" or "./plugins/foo"), or typed object: `{source:"github", repo:"owner/repo", ref?, sha?}` | `{source:"url", url, ref?, sha?}` | `{source:"git-subdir", url, path, ref?, sha?}` | `{source:"npm", package, version?}`. For url/git sources, when both `ref` and `sha` set, `sha` is the effective pin.
- `description` (string, OPTIONAL but universal in practice).
- `version` (string, OPTIONAL) — semver.
- `author` (object, OPTIONAL) — `{name REQUIRED, email?, url?}`.
- `homepage` (string, OPTIONAL), `license` (string, OPTIONAL).
- `category` (string, OPTIONAL) — marketplace-specific.
- `keywords` / `tags` (string array, OPTIONAL) — multica uses `keywords`; spec marketplace field is `tags`.
- `strict` (boolean, OPTIONAL, default true) — when false, the marketplace entry (not plugin.json) is authoritative for component lists; lets you declare `skills`/`commands`/`agents`/`hooks` inline.
- Inline component arrays (OPTIONAL): `skills`, `commands`, `agents`, `hooks`, `mcpServers` — paths relative to source; used with `strict:false` (see anthropics/skills `skills` arrays).

**⑤ 관례·주의** —

- Path is fixed and load-bearing: must be `.claude-plugin/marketplace.json`.
- `name` and plugin `name`s are kebab-case.
- `source: "./"` means "the marketplace repo itself is the plugin root" (anthropics/skills, karpathy) — used for single-repo skill collections; `source: "./plugins/<name>"` for a monorepo of plugins (wshobson, ruflo).
- Relative-path sources ONLY resolve when the marketplace is added via Git (GitHub/GitLab/git URL). If users add via a direct URL to the JSON file, relative paths break — use github/url/npm object sources for URL distribution.
- `strict:false` + explicit `skills` arrays is the pattern for shipping multiple skills out of one repo subtree without a per-plugin plugin.json.
- Per-plugin `version`/`author` (wshobson) lets a monorepo vendor third-party plugins with distinct provenance; minimal marketplaces (ruflo) omit them and let each plugin's own plugin.json supply metadata.
- Pin reproducibly with `sha` (40-char) on github/url/git-subdir sources; `ref` is a movable branch/tag.
- Keep it valid JSON (no comments/trailing commas) — ruflo gates it with a CI `validate-marketplace.yml` workflow.

**⑥ 최소 골격 (복붙 시작점)** —

````text
// .claude-plugin/marketplace.json — minimal, monorepo-of-plugins (most common)
{
  "name": "my-marketplace",
  "owner": {
    "name": "Your Name",
    "email": "you@example.com",
    "url": "https://github.com/you"
  },
  "metadata": {
    "description": "Short catalog description",
    "version": "1.0.0"
  },
  "plugins": [
    {
      "name": "my-plugin",
      "source": "./plugins/my-plugin",
      "description": "What this plugin does",
      "version": "1.0.0",
      "author": { "name": "Your Name" },
      "category": "workflows",
      "keywords": ["example"]
    }
  ]
}

// VARIANT A — single-repo skill collection (repo root IS the plugin), strict:false
// {
//   "name": "my-skills",
//   "owner": { "name": "Your Name" },
//   "plugins": [{
//     "name": "my-skills",
//     "source": "./",
//     "description": "...",
//     "strict": false,
//     "skills": ["./skills/foo", "./skills/bar"]
//   }]
// }

// VARIANT B — external plugin pinned by git source:
//   "source": { "source": "github", "repo": "owner/repo", "ref": "main", "sha": "<40-char-sha>" }

Required repo layout:
  .claude-plugin/marketplace.json
  plugins/my-plugin/.claude-plugin/plugin.json   (per-plugin manifest, when source is "./plugins/...")
  # OR (Variant A): skills/<name>/SKILL.md directly under repo root
````

**⑦ 변종·분기** —

1. Source granularity: SINGLE-REPO-as-plugin (`source:"./"`, anthropics/skills, multica-ai) vs MONOREPO-of-plugins (`source:"./plugins/<name>"`, wshobson 84 plugins, ruflo ~15). 
2. Metadata richness: MINIMAL — only name/source/description per plugin, no per-plugin version/author (ruflo) vs RICH — every plugin carries version/author/homepage/license/category (wshobson, for vendoring 3rd-party plugins with provenance).
3. Description placement: top-level `description` (ruflo) vs `metadata.description` (anthropics, wshobson, multica).
4. Strict mode: `strict:false` + inline `skills[]` arrays to enumerate components without per-plugin plugin.json (anthropics/skills) vs default strict (rely on each plugin's plugin.json — wshobson/ruflo).
5. Tag key: `keywords` (multica-ai) vs spec-named `tags`; `id` field present (multica-ai) but absent elsewhere/spec.
6. Multi-host mirroring: wshobson also publishes `.agents/plugins/marketplace.json` and `.cursor-plugin/marketplace.json` (cross-host) — others ship only the Claude path.
7. CI validation: ruflo gates the manifest with `.github/workflows/validate-marketplace.yml`; others don't.

**증거(실증 fetch)** — `anthropics/skills:.claude-plugin/marketplace.json` · `wshobson/agents:.claude-plugin/marketplace.json` · `ruvnet/ruflo:.claude-plugin/marketplace.json` · `multica-ai/andrej-karpathy-skills:.claude-plugin/marketplace.json` · `ruvnet/ruflo:.github/workflows/validate-marketplace.yml` · `code.claude.com/docs/en/plugin-marketplaces (official spec)`

---

## 4. Constitution (CLAUDE.md / AGENTS.md)  ·  🟩 FLOOR

**① 공식 표준** — TWO overlapping official specs exist, both consulted (fetched live).

(1) AGENTS.md standard (agents.md) — SPEC-MANDATED facts: it is "just standard Markdown," no required sections, no schema, freeform headings. Location = repo ROOT (nested copies allowed in subprojects; "closest AGENTS.md to the edited file wins"). It is a deliberately open, schema-less format. So the ONLY hard rules are: filename `AGENTS.md`, plain markdown, root placement.

(2) Claude Code memory spec (code.claude.com/docs/en/memory) — SPEC-MANDATED for CLAUDE.md: filename is `CLAUDE.md` (Claude Code does NOT read AGENTS.md). Locations + load order (broad→specific): managed policy (/Library/Application Support/ClaudeCode/, /etc/claude-code/, C:\Program Files\ClaudeCode\) → user `~/.claude/CLAUDE.md` → project `./CLAUDE.md` or `./.claude/CLAUDE.md` → `./CLAUDE.local.md` (gitignored, personal). Ancestor files load in FULL at launch; subdir files load on-demand. `@path/to/import` syntax expands files into context at launch (relative paths resolve to the importing file; max recursion depth = 4 hops; imports inside backticks/code-fences are NOT parsed). To bridge both tools: a `CLAUDE.md` whose body is `@AGENTS.md` (or a symlink). DE-FACTO (strongly recommended, not enforced): target < 200 lines; specific+concrete > vague; markdown headers/bullets; `<!-- HTML comments -->` are stripped before injection (free maintainer notes). CLAUDE.md is context, NOT enforced config — use hooks for hard enforcement.

**② 포맷** — Plain Markdown. No YAML frontmatter on the constitution file itself (frontmatter+`paths:` only appears on the SEPARATE `.claude/rules/*.md` files, not on CLAUDE.md/AGENTS.md). Body is freeform `#`/`##` headers + bullet lists. Two special inline constructs: `@relative/or/absolute/path` = import directive (expanded at launch); `` `@literal` `` in backticks = escaped, not imported. Block-level `<!-- ... -->` HTML comments are stripped from context (human-only notes). Filenames are fixed literals: `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `CLAUDE.local.md`, optional `CONTEXT.md` (de-facto, repo-specific glossary — mattpocock).

**③ 위치** — Repository ROOT is canonical for all of: `CLAUDE.md`, `AGENTS.md`, `GEMINI.md` (all four repos keep these at root — caveman notes they "must stay at root" for plugin autodiscovery). Alternatives Claude Code also reads: `./.claude/CLAUDE.md` (project), `~/.claude/CLAUDE.md` (user/personal), managed-policy OS paths (org). `./CLAUDE.local.md` = gitignored personal overlay. Subdirectory `CLAUDE.md` = path-scoped, lazy-loaded. Topic spillover goes to `.claude/rules/*.md` (loaded at launch, or path-scoped via `paths:` frontmatter) or to `docs/` referenced by `@import`.

**④ 스키마(키·필수/선택)** —

There is NO mandated key schema — it is freeform markdown. The "fields" are de-facto SECTIONS observed across the canon (all OPTIONAL per spec; pick what the project needs):
- Title `# CLAUDE.md` / `# <Project> — Contributor Guidelines` — OPTIONAL but universal.
- Project overview / what-it-is — common (karpathy, caveman).
- "What lives where" / repo layout (fenced dir tree) — common (caveman, mattpocock).
- Behavioral rules / coding standards (numbered or `##` sections, bold imperative lead) — the substance (karpathy's 4 numbered laws; caveman's README rules).
- Build/test/commit commands — spec-recommended.
- Contribution / PR gates (read PR template, search prior PRs, identify the agent) — superpowers.
- "If You Are an AI Agent" preamble — superpowers (agent-targeted hard stop).
- Glossary / ubiquitous language — de-facto, in CONTEXT.md not CLAUDE.md (mattpocock).
- `@imports` to SKILL.md / docs — caveman & superpowers AGENTS.md are PURE import manifests.
REQUIRED-by-spec: only the filename + markdown-ness. Everything above is convention.

**⑤ 관례·주의** —

- Size: target < 200 lines (spec de-facto); longer = weaker adherence. Spill to `.claude/rules/` or `@import`d docs.
- Specificity: concrete + verifiable ("Run `npm test` before committing", "API handlers live in `src/api/handlers/`") beats vague ("test your changes"). All canon rules are imperative + bolded lead-in.
- Structure: markdown headers + bullets, not prose paragraphs. karpathy uses numbered laws; caveman uses `## section` + bullet rules + a fenced dir tree.
- Cross-host portability: to serve Claude + Codex + Gemini + Cursor/etc from ONE source, make AGENTS.md/GEMINI.md thin `@import` manifests pointing at the real SKILL.md/docs (caveman, superpowers do exactly this), and make CLAUDE.md either its own content OR `@AGENTS.md` + Claude-only addendum. Symlink works on macOS/Linux; on Windows use `@AGENTS.md` import (symlinks need admin).
- `@import` gotchas: relative paths resolve to the IMPORTING file (not cwd); max 4 hops; backtick a path to keep it literal; first external import triggers a one-time approval dialog.
- `<!-- comments -->` are free (stripped from context) — use for maintainer notes.
- Keep instructions non-contradictory across nested files (Claude picks arbitrarily on conflict).
- CLAUDE.md is guidance, not enforcement — anything that MUST happen (pre-commit lint) belongs in a hook, not here.
- Self-consistency rule (caveman, mattpocock): the layout/feature tables in the constitution must be kept in sync with actual code/README.

**⑥ 최소 골격 (복붙 시작점)** —

````text
PATTERN A — single self-contained CLAUDE.md (karpathy/caveman style), repo root:

```markdown
# CLAUDE.md — myproject

<!-- maintainer note: keep this under 200 lines; spill detail to .claude/rules/ -->

## Project overview
One paragraph: what this is, who uses it, how it ships.

## What lives where
\`\`\`
myproject/
├── README.md        # product front door
├── CLAUDE.md        # this file (maintainer/agent instructions)
├── AGENTS.md        # cross-tool autodiscovery (imports the skills)
├── src/             # source of truth
└── tests/
\`\`\`

## Build & test
- Build:  `npm run build`
- Test:   `npm test`   (run before every commit)
- Lint:   `npm run lint`

## Coding standards
1. **Simplicity first.** Minimum code that solves the problem; nothing speculative.
2. **Surgical changes.** Touch only what the request requires; match existing style.
3. **Verify, don't assume.** State assumptions; if unclear, stop and ask.

## Commits / PRs
- Conventional Commits. Reference the issue. Never `--no-verify`.
```

PATTERN B — cross-host: thin import manifests + a bridge (caveman/superpowers style):

```
repo-root/
├── CLAUDE.md      # body = "@AGENTS.md" + optional "## Claude Code" addendum
├── AGENTS.md      # pure import manifest (below)
└── GEMINI.md      # same imports, Gemini-flavored references
```

AGENTS.md (literal — caveman):
```markdown
@./skills/myskill/SKILL.md
@./skills/myskill-commit/SKILL.md
```

CLAUDE.md bridge (literal — Claude Code docs):
```markdown
@AGENTS.md

## Claude Code
Use plan mode for changes under `src/billing/`.
```
(or, no Claude-specific content needed:  `ln -s AGENTS.md CLAUDE.md`)
````

**⑦ 변종·분기** —

Real divergences observed (the builder's fork-in-the-road):
1. SELF-CONTAINED vs IMPORT-MANIFEST. karpathy & caveman CLAUDE.md = full prose rules. caveman & superpowers AGENTS.md/GEMINI.md = pure `@import` lists pointing at SKILL.md. mattpocock CLAUDE.md = layout/invariant rules only (no behavioral laws).
2. AUDIENCE. karpathy = generic anti-slop coding laws (portable across any repo). superpowers = aggressive agent-targeted CONTRIBUTION gate ("Stop. Read this... 94% PR rejection rate", identify-your-model). caveman = maintainer guide for THIS product (README-as-product rules). So constitutions split into: behavioral-law / contribution-policy / repo-maintainer-guide.
3. CROSS-HOST STRATEGY. caveman & superpowers ship CLAUDE.md + AGENTS.md + GEMINI.md as parallel files (some identical: superpowers' CLAUDE.md and AGENTS.md are byte-identical contributor guides; its GEMINI.md is a 2-line import). Bridge alternatives: `@AGENTS.md` import vs symlink.
4. GLOSSARY SPLIT. mattpocock factors ubiquitous-language/domain terms into a SEPARATE `CONTEXT.md` (with Avoid-lists and flagged ambiguities) rather than bloating CLAUDE.md — a de-facto pattern, no spec basis.
5. LAYOUT-AS-CONTRACT. caveman & mattpocock embed the canonical dir tree / file-placement rules and make them self-enforcing invariants; karpathy & superpowers omit layout entirely.

**증거(실증 fetch)** — `multica-ai/andrej-karpathy-skills:CLAUDE.md` · `JuliusBrussee/caveman:CLAUDE.md` · `JuliusBrussee/caveman:AGENTS.md` · `JuliusBrussee/caveman:GEMINI.md` · `obra/superpowers:CLAUDE.md` · `obra/superpowers:AGENTS.md` · `obra/superpowers:GEMINI.md` · `mattpocock/skills:CLAUDE.md` · `mattpocock/skills:CONTEXT.md` · `spec:agents.md` · `spec:code.claude.com/docs/en/memory`

---

## 5. CI (.github/workflows) — harness-package GitHub Actions (skill validation / plugin-install test / release)  ·  🟩 FLOOR

**① 공식 표준** — SPEC-MANDATED (GitHub Actions workflow syntax, official): each file is a "workflow" YAML under `.github/workflows/`. GitHub mandates the top-level keys `on:` (trigger) and `jobs:` (one or more jobs); `name:` is optional-but-conventional. Each job mandates `runs-on:` and either `steps:` or `uses:` (reusable workflow). Steps use either `uses:` (a published action `owner/repo@ref`) or `run:` (shell). Expression syntax `${{ ... }}`, contexts (`github`, `secrets`, `vars`, `needs`, `steps`, `matrix`, `env`, `inputs`), `permissions:`, `concurrency:`, `strategy.matrix`, `needs:`, and step `outputs` via `$GITHUB_OUTPUT` are all part of the official spec. WebFetch was not invoked here; the spec is well-established (docs.github.com/actions/reference/workflow-syntax-for-github-actions). Everything HARNESS-SPECIFIC below (what the workflows actually DO — validate SKILL.md, run `claude plugin validate/install`, cut releases, eval) is DE-FACTO convention converged across the 4 canonical repos, not mandated by GitHub.

**② 포맷** — YAML (`.yml`), one workflow per file. UTF-8, 2-space indent. No frontmatter — the whole file IS the structured doc. Top-level keys observed: `name`, `on`, `concurrency`, `permissions`, `env`, `jobs`. Filename is free-form but semantic (`validate-skill.yml`, `test-plugin-install.yml`, `pr-skill-scan.yml`, `release.yml`, `eval-report.yml`).

**③ 위치** — `.github/workflows/*.yml` at the REPO ROOT (must be exactly this path — GitHub only discovers workflows here). Companion scripts the workflows call live OUTSIDE workflows: `scripts/*.js` (addyosmani), `.github/scripts/*.js` (marketingskills), or root `*.py` (K-Dense, wshobson `plugins/plugin-eval/scripts/`). The plugin/marketplace manifests they validate live at `.claude-plugin/marketplace.json`, `plugins/*/.claude-plugin/plugin.json`.

**④ 스키마(키·필수/선택)** —

Top-level keys:
- `name:` (optional, string) — display name.
- `on:` (REQUIRED) — triggers. Observed: `push:`/`pull_request:` each with optional `branches:` and `paths:` filters (path-scoping to `**/SKILL.md` or `skills/**` is the dominant harness pattern); `workflow_dispatch:` with optional `inputs:` (typed: `choice`/`string`, with `description`/`required`/`default`); `schedule:` with `- cron:`.
- `permissions:` (optional but recommended) — least-privilege; `contents: read` default, `contents: write` for release/sync, `pull-requests: write` for PR-comment jobs.
- `concurrency:` (optional) — `group:` (often keyed on `${{ github.ref }}` or PR number) + `cancel-in-progress: true`.
- `env:` (optional) — workflow-level env.
- `jobs:` (REQUIRED) — map of job-id → job. Each job:
  - `name:` (optional), `runs-on:` (REQUIRED; `ubuntu-latest` or `ubuntu-slim`), `if:` (optional gate, e.g. skip drafts/dependabot or guard on a prior step's output), `needs:` (optional, job deps), `outputs:` (optional, surface step outputs), `timeout-minutes:` (optional), `strategy:` (optional; `fail-fast: false` + `matrix:` from `fromJson(needs.*.outputs.*)`), `permissions:` (optional, per-job override), `env:`, `steps:` (REQUIRED list).
  - Each step: `name:` (optional), `id:` (optional, needed if step has outputs), `uses:` XOR `run:`, `with:` (action inputs), `env:` (step secrets), `if:` (optional; `always()` common for report/comment steps), `working-directory:` (optional).
Step outputs: `echo "key=val" >> "$GITHUB_OUTPUT"`; job summary: `>> "$GITHUB_STEP_SUMMARY"`.

**⑤ 관례·주의** —

- Pin actions to a major tag (`actions/checkout@v6`, `setup-node@v4`, `astral-sh/setup-uv@v5`, `upload-artifact@v4`); wshobson hardens further by pinning to a full commit SHA with a `# v4` comment.
- `actions/checkout` with `fetch-depth: 0` whenever you `git diff` (changed-skill detection) or read tags (release notes).
- Path-filter triggers (`paths: ["**/SKILL.md"]`) so CI only fires on relevant changes — universal.
- Changed-skill detection is a two-job DAG: a `detect-changes` job emits a JSON array via `$GITHUB_OUTPUT`, downstream job consumes it with `strategy.matrix.skill: ${{ fromJson(...) }}` and `if: needs.detect-changes.outputs.skills != '[]'`. `fail-fast: false` so one bad skill doesn't mask others.
- `if:` guards skip noise: `github.event.pull_request.draft != true && github.actor != 'dependabot[bot]'`.
- Report/comment steps run `if: always()`; PR comments are upserted (idempotent) via `marocchino/sticky-pull-request-comment@v2` with a stable `header:`.
- Secrets via `${{ secrets.* }}`, never inline; non-secret config via `${{ vars.* }}` with a `|| 'default'` fallback.
- Least-privilege `permissions:` at workflow level; widen only the job that needs it.
- Plugin-install smoke test = install the real CLI (`npm install -g @anthropic-ai/claude-code`) then `claude plugin validate .` → `marketplace add ./` → `plugin install <name>@<marketplace> --scope user`, chained with `needs:`.
- Release = trigger on `push` to main filtered to `pyproject.toml` (version bump), extract version, guard against an existing tag, generate notes from `git log <prev>..HEAD`.

**⑥ 최소 골격 (복붙 시작점)** —

````text
# .github/workflows/validate-skill.yml
# Harness CI: validate changed SKILL.md skills + smoke-test plugin install.
name: Validate Skills

on:
  push:
    branches: [main]
    paths: ["**/SKILL.md", ".claude-plugin/**"]
  pull_request:
    branches: [main]
    paths: ["**/SKILL.md", ".claude-plugin/**"]
  workflow_dispatch:

concurrency:
  group: validate-${{ github.ref }}
  cancel-in-progress: true

permissions:
  contents: read

jobs:
  # 1) Discover only the skills that changed -> JSON array output
  detect-changes:
    runs-on: ubuntu-latest
    if: github.event.pull_request.draft != true && github.actor != 'dependabot[bot]'
    outputs:
      skills: ${{ steps.changed.outputs.skills }}
    steps:
      - uses: actions/checkout@v6
        with:
          fetch-depth: 0
      - id: changed
        run: |
          set -euo pipefail
          if [ "${{ github.event_name }}" = "pull_request" ]; then
            BASE=${{ github.event.pull_request.base.sha }}
            HEAD=${{ github.event.pull_request.head.sha }}
          else
            BASE=${{ github.event.before }}; HEAD=${{ github.event.after }}
          fi
          SKILLS=$(git diff --name-only --diff-filter=ACMR "$BASE" "$HEAD" \
            | grep 'SKILL.md$' | xargs -r -I{} dirname {} | sort -u \
            | jq -R -s -c 'split("\n") | map(select(length > 0))')
          echo "skills=$SKILLS" >> "$GITHUB_OUTPUT"

  # 2) Validate each changed skill in parallel
  validate-skill:
    needs: detect-changes
    if: needs.detect-changes.outputs.skills != '[]'
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        skill: ${{ fromJson(needs.detect-changes.outputs.skills) }}
    steps:
      - uses: actions/checkout@v6
      - run: test -f "${{ matrix.skill }}/SKILL.md"   # swap for your validator script

  # 3) Plugin-install smoke test (real CLI)
  test-install:
    runs-on: ubuntu-latest
    needs: validate-skill
    steps:
      - uses: actions/checkout@v6
      - run: npm install -g @anthropic-ai/claude-code
      - run: claude plugin validate .
      - run: claude plugin marketplace add ./
      - run: claude plugin install my-plugin@my-marketplace --scope user
````

**⑦ 변종·분기** —

Real divergences a builder must choose between:
1. CHANGED-DETECTION vs WHOLE-REPO. marketingskills + K-Dense diff to find only changed skills (matrix fan-out, scales to many skills); addyosmani just runs `node scripts/validate-skills.js` over everything (simpler, fine for small repos).
2. VALIDATOR. External published action (`Flash-Brew-Digital/validate-skill@v1`, marketingskills) vs in-repo script — Node (`scripts/validate-skills.js`, addyosmani) vs Python/uv (`scan_pr_skills.py`, K-Dense) vs pure stdlib JSON checks inline (`python3 -m json.tool`, wshobson). vs the real CLI (`claude plugin validate .`, addyosmani).
3. RUNNER. `ubuntu-latest` (most) vs `ubuntu-slim` (marketingskills, faster cold start).
4. TOOLCHAIN. `setup-node@v4` + `npm` (JS validators) vs `astral-sh/setup-uv` + `uv sync` (Python validators, with `enable-cache`).
5. ACTION PINNING. major tag `@v6` (most) vs full commit SHA `@34e1148… # v4` (wshobson, supply-chain hardened).
6. PR FEEDBACK. K-Dense posts an upserted sticky PR comment + uploads artifact; others just fail the check.
7. RELEASE TRIGGER. K-Dense auto-releases on `pyproject.toml` change (version-file-driven, tag-guard + git-log notes); marketingskills instead auto-COMMITS synced manifests back via `git-auto-commit-action` (no tags).
8. EVAL. wshobson adds a separate `workflow_dispatch`+weekly-`cron` eval job (typed `depth` input quick/standard/deep, `ANTHROPIC_API_KEY`, 180-min timeout, artifact + job-summary) — an advanced tier most repos omit.

**증거(실증 fetch)** — `coreyhaines31/marketingskills:.github/workflows/validate-skill.yml` · `coreyhaines31/marketingskills:.github/workflows/sync-skills.yml` · `addyosmani/agent-skills:.github/workflows/test-plugin-install.yml` · `wshobson/agents:.github/workflows/eval-report.yml` · `wshobson/agents:.github/workflows/validate.yml` · `K-Dense-AI/scientific-agent-skills:.github/workflows/pr-skill-scan.yml` · `K-Dense-AI/scientific-agent-skills:.github/workflows/release.yml`

---

## 6. Slash commands (Claude Code custom commands)  ·  🟨 COMMON

**① 공식 표준** — YES — official Claude Code spec at code.claude.com/docs/en/slash-commands (redirected from docs.claude.com). KEY current fact: "Custom commands have been merged into skills." A file at `.claude/commands/deploy.md` and a skill at `.claude/skills/deploy/SKILL.md` both create `/deploy` and work the same way; existing `.claude/commands/*.md` files keep working. The spec mandates: a Markdown file whose filename (minus `.md`) becomes the command name; optional YAML frontmatter; the file body is the prompt injected when invoked. Spec-mandated frontmatter keys (all OPTIONAL): `description`, `argument-hint`, `allowed-tools`, `model`, `disable-model-invocation`. Spec-mandated body interpolations: `$ARGUMENTS` (all args), `$1`/`$2`/... (positional), `!`cmd`` (run bash, inline its stdout — requires Bash in allowed-tools), `@path` (inline a file's contents). Namespacing is spec-mandated via subdirectories: `.claude/commands/gsd/help.md` → invoked as `/gsd:help`. The plugin/skill layer follows the agentskills.io open standard; the bare `.claude/commands/*.md` form is the Claude-Code-native command format. NOTE: the `.toml` form (`description`+`prompt`) is NOT Claude Code — it is the Gemini-CLI command format; in agent-skills it is the source-of-truth that gets compiled into `.claude/commands/*.md`.

**② 포맷** — Markdown (`.md`), UTF-8. Structure: optional YAML frontmatter delimited by `---` ... `---`, then a free-form Markdown body that is the literal prompt sent to the model on invocation. No frontmatter at all is valid (body-only command). De-facto: bodies use lightweight section structure — either Markdown `##` headings (addyosmani, omc) or pseudo-XML tags `<objective>`/`<process>`/`<context>` (gsd). Cross-host alt format observed: TOML with `description` + multiline `prompt = """..."""` (Gemini-CLI `.gemini/commands/*.toml` and a vendor-neutral `commands/*.toml`), compiled to the `.md` form.

**③ 위치** — Project scope: `.claude/commands/<name>.md` → `/<name>` (or `/<plugin>:<name>` when shipped by a plugin/namespaced repo). User scope: `~/.claude/commands/<name>.md`. Subdirectories namespace the command: `.claude/commands/gsd/help.md` → `/gsd:help`. Equivalent skill form: `.claude/skills/<name>/SKILL.md`. Repos that ship as plugins keep masters at top-level `commands/<...>.md` (gsd: `commands/gsd/*.md`; omc: `commands/*.md`) which install into `.claude/commands/` or are exposed via the plugin manifest.

**④ 스키마(키·필수/선택)** —

Frontmatter (YAML, all OPTIONAL):
- `description` (string) — one-line summary shown in the `/` menu and help. Most common key; sometimes empty string `""` to deliberately suppress the long skill description from every session (omc compat shims).
- `argument-hint` (string) — usage hint shown after the command name, e.g. `"<phase-number> [--wave N] [--tdd]"` (gsd).
- `allowed-tools` (YAML list or comma string) — restricts tools the command may use, e.g. `[Read, Write, Edit, Bash, Agent, TodoWrite, AskUserQuestion]`. Required only if the body uses `!`bash`` (needs Bash) or tool calls.
- `model` (string) — pin a model for this command (spec).
- `disable-model-invocation` (bool) — spec: prevent Claude from auto-invoking; user-only via `/`.
- `name` (string) — explicit command name incl. namespace, e.g. `gsd:help` (gsd sets it on every file even though filename already implies it; de-facto, belt-and-suspenders).
- `requires` (YAML list, e.g. `[phase, verify-work]`) — NON-STANDARD, gsd-internal dependency declaration; ignored by Claude Code.
Body interpolation tokens (spec, used in body text): `$ARGUMENTS`, `$1`/`$2`, `!`shell-cmd``, `@relative/or/~/path`.
TOML variant fields (Gemini/source form): `description` (string, required), `prompt` (string, required, the body).

**⑤ 관례·주의** —

- Filename = command name (kebab-case): `code-simplify.md` → `/code-simplify`. Keep names short, verb-first.
- Thin-dispatcher pattern is dominant: the command body is SHORT and delegates to a heavier skill/workflow rather than inlining logic — "Invoke the <skill> skill" (addyosmani), "Read ... skills/verify/SKILL.md and follow it exactly" (omc), "Follow ~/.claude/get-shit-done/workflows/help.md with $ARGUMENTS" (gsd via `@`-include). This keeps the per-session prompt budget tiny (the explicit rationale in omc: "without loading the full skill description in every session").
- Pass args through verbatim with `$ARGUMENTS`; document modes/flags in the body and `argument-hint`.
- `description` should be plain and action-oriented; it is what the model/user sees in the menu.
- Namespace plugin-owned commands under a subdir (`gsd/`) to avoid collisions; the dir becomes the `/<ns>:` prefix.
- gsd convention: pseudo-XML body sections (`<objective>`,`<execution_context>`,`<context>`,`<process>`) + `@`-include of an external workflow file = command is pure routing.
- Cross-host portability (addyosmani): author once in `commands/*.toml`, generate per-host (`.claude/commands/*.md` + `.gemini/commands/*.toml`) via a build/validate script (`scripts/validate-commands.js`).
- Gotcha: empty `description: ""` is intentional, not a bug, on compatibility shim commands.

**⑥ 최소 골격 (복붙 시작점)** —

````text
Minimal body-only command — `.claude/commands/spec.md`:

```markdown
---
description: Write a structured spec before any code
---
Invoke the spec-driven-development skill.

Ask the user clarifying questions about: objective and target users; core
features and acceptance criteria; tech-stack constraints; boundaries.

Then write a SPEC.md in the project root and confirm before proceeding.
Arguments (optional focus area): $ARGUMENTS
```

Invoke with `/spec` or `/spec auth-flow`.

Fuller, namespaced command with args + tools + bash/file interpolation — `.claude/commands/gsd/execute.md` → `/gsd:execute`:

```markdown
---
name: gsd:execute
description: Execute the next phase plan with test-driven verification
argument-hint: "<phase-number> [--tdd]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - TodoWrite
---
<objective>
Execute phase $1 of the active plan. Stop after one task unless told otherwise.
</objective>

<context>
Arguments: $ARGUMENTS
Current branch: !`git branch --show-current`
Plan file:
@docs/plan.md
</context>

<process>
1. Read the next pending task's acceptance criteria.
2. Write a failing test (RED), implement minimally (GREEN), run the suite.
3. Commit, mark the task done, then stop.
</process>
```

TOML / Gemini source variant — `commands/spec.toml` (compiles to the .md above):

```toml
description = "Write a structured spec before any code"
prompt = """
Invoke the spec-driven-development skill.
Ask clarifying questions, then write SPEC.md. Arguments: {{args}}
"""
```
Directory layout:
```
.claude/commands/
  spec.md            -> /spec
  build.md           -> /build
  gsd/
    execute.md       -> /gsd:execute
    help.md          -> /gsd:help
```
````

**⑦ 변종·분기** —

1. Frontmatter richness: addyosmani & omc use a single `description` (often empty) and lean on the body; gsd uses a full frontmatter contract (`name`,`description`,`argument-hint`,`allowed-tools`, plus its non-standard `requires`).
2. Body style: Markdown `##` headings (addyosmani, omc) vs pseudo-XML tags `<objective>/<process>/<context>` (gsd).
3. Dispatch mechanism: "Invoke the X skill" by name (addyosmani) vs "Read skills/.../SKILL.md and follow it" by path (omc) vs `@`-include an external workflow file (gsd `@~/.claude/get-shit-done/workflows/help.md`).
4. Source-of-truth & portability: hand-written `.md` per host (gsd, omc) vs single `.toml` source compiled to both `.claude/commands/*.md` and `.gemini/commands/*.toml` with a validate script (addyosmani) — the real fork-in-the-road for multi-host support.
5. Skill-vs-command: gstack does NOT ship `.md` slash commands at all — its "commands" are TypeScript MCP/CLI handlers (`*/src/commands.ts`); it exposes capability as skills/MCP tools, the modern "merged into skills" path, rather than `.claude/commands/*.md`.
6. Namespacing: flat `commands/*.md` (omc, addyosmani) vs subdir-namespaced `commands/gsd/*.md` → `/gsd:*` (gsd).
7. Thin-dispatcher (all md repos) vs fat self-contained command (addyosmani `build.toml` inlines the full TDD procedure).

**증거(실증 fetch)** — `addyosmani/agent-skills:.claude/commands/spec.md` · `addyosmani/agent-skills:commands/build.toml` · `addyosmani/agent-skills:.gemini/commands/build.toml` · `addyosmani/agent-skills:scripts/validate-commands.js` · `gsd-build/get-shit-done:commands/gsd/help.md` · `gsd-build/get-shit-done:commands/gsd/execute-phase.md` · `Yeachan-Heo/oh-my-claudecode:commands/verify.md` · `Yeachan-Heo/oh-my-claudecode:commands/release.md` · `garrytan/gstack:design/src/commands.ts` · `docs:code.claude.com/docs/en/slash-commands`

---

## 7. Hooks (hooks.json + settings.json hooks)  ·  🟨 COMMON

**① 공식 표준** — YES. Official spec: Claude Code Hooks (https://docs.claude.com/en/docs/claude-code/hooks -> 301 -> https://code.claude.com/docs/en/hooks); fetched OK. Mandates: top-level hooks object keyed by EVENT NAME; each event -> ARRAY of matcher-groups; each group has optional matcher (string) + REQUIRED hooks array of handlers; each handler has type ("command" = universal portable form; http/mcp_tool/prompt/agent also exist) + command + optional timeout (sec). Exit codes spec-mandated: 0=success (stdout parsed as JSON decision only if present), 2=blocking (stderr->Claude, stdout ignored), other=non-blocking. SAME hooks object in plugin hooks/hooks.json and settings.json hooks key. All 4 repos converge; richer fields (decision/permissionDecision/http/mcp_tool, extra events) are spec-documented but rarely used by the canon (SessionStart/UserPromptSubmit + type:command).

**② 포맷** — JSON (strict, no comments/frontmatter). Single object; only required member is hooks (object). Plugin file is named hooks.json with optional sibling description string. The same hooks object is also embedded under the hooks key of settings.json / settings.local.json.

**③ 위치** — Plugin convergent path: <plugin-root>/hooks/hooks.json (ponytail, agent-skills, claude-mem plugin/hooks/hooks.json, superpowers hooks/hooks.json). Sibling executable scripts in hooks/ (session-start.sh, run-hook.cmd, *.js). Per-user: ~/.claude/settings.json. Per-project shared: .claude/settings.json (commit). Private: .claude/settings.local.json (gitignore). Cross-host siblings: codex-hooks.json/hooks-codex.json, copilot-hooks.json/hooks-cursor.json.

**④ 스키마(키·필수/선택)** —

TOP LEVEL: hooks (object, REQUIRED); description (string, OPTIONAL, plugin only).
hooks[EventName] = ARRAY of matcher-group objects. Events used by canon: SessionStart, UserPromptSubmit, Setup; spec adds PreToolUse, PostToolUse, Stop, SubagentStop, Notification, PreCompact, SessionEnd, etc.
MATCHER-GROUP: matcher (string, OPTIONAL -- omit/"*"=all; SessionStart="startup|resume|clear|compact"; tool events use "Bash"/"Edit|Write" or regex/mcp__server__tool); hooks (array, REQUIRED).
HANDLER: type (string, REQUIRED -- "command" portable); command (string, REQUIRED -- shell string, or executable when args present); timeout (number, OPTIONAL sec; default ~600s, 30s UserPromptSubmit). OPTIONAL extras: args (array->exec form), shell ("bash", claude-mem), async/asyncRewake (bool; superpowers async:false), statusMessage (string, ponytail), commandWindows (string, ponytail PowerShell variant -- de-facto), if (string e.g. "Bash(rm *)"), once (bool).
PLACEHOLDERS: ${CLAUDE_PLUGIN_ROOT}, ${CLAUDE_PROJECT_DIR}, ${CLAUDE_CONFIG_DIR}, ${CLAUDE_PLUGIN_DATA}, ${CLAUDE_ENV_FILE}, ${tool_input.field}.
STDIN to hook: session_id, transcript_path, cwd, permission_mode, hook_event_name (+tool_name/tool_input on tool events).
STDOUT JSON (OPTIONAL, exit 0 only): continue (bool), stopReason/systemMessage, suppressOutput (bool), decision ("block"/"approve"), reason, hookSpecificOutput { hookEventName (REQ if used), additionalContext (string injects context), permissionDecision ("allow"/"deny"/"ask"), permissionDecisionReason }. EXIT: 0=ok, 2=block, other=non-blocking error.

**⑤ 관례·주의** —

- type:"command" everywhere (only portable handler). - Quote every ${...} path in shell-form commands. - Fail-OPEN: commands end with || true or || exit 0 and guard script existence so a broken hook never blocks the session (agent-skills: [ -f "$SCRIPT" ] && bash ... || true; ponytail: command -v node ... || exit 0). - SessionStart matcher conventionally "startup|resume|clear|compact"; UserPromptSubmit takes NO matcher. - Resolve root via ${CLAUDE_PLUGIN_ROOT} with fallback ${CLAUDE_PROJECT_DIR}/.claude/hooks/... - Emit context as {"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"..."}}; escape via jq (agent-skills) or careful bash (superpowers), never naive interpolation. - Small timeouts interactive (5s ponytail), large only for heavy bg (claude-mem 60-300s). - Cross-host: ship parallel sibling files (codex/cursor/copilot) rather than overloading one; superpowers uses one run-hook.cmd dispatcher for Windows. - Keep JSON tiny; logic in sibling script (except claude-mem inlines a big PATH-bootstrap one-liner).

**⑥ 최소 골격 (복붙 시작점)** —

````text
Plugin layout:
  my-plugin/
  +- hooks/
     +- hooks.json
     +- session-start.sh   (chmod +x)

hooks/hooks.json:
{
  "description": "my-plugin hooks",
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume|clear|compact",
        "hooks": [
          {
            "type": "command",
            "command": "SCRIPT=\"${CLAUDE_PLUGIN_ROOT}/hooks/session-start.sh\"; [ -f \"$SCRIPT\" ] || SCRIPT=\"${CLAUDE_PROJECT_DIR}/.claude/hooks/session-start.sh\"; [ -f \"$SCRIPT\" ] && bash \"$SCRIPT\" || true",
            "timeout": 5
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "command -v node >/dev/null 2>&1 && node \"${CLAUDE_PLUGIN_ROOT}/hooks/track.js\" || exit 0",
            "timeout": 5
          }
        ]
      }
    ]
  }
}

hooks/session-start.sh (fail-open context injection):
#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONTENT=$(cat "${SCRIPT_DIR}/../skills/using-my-plugin/SKILL.md" 2>/dev/null || echo "")
if command -v jq >/dev/null 2>&1 && [ -n "$CONTENT" ]; then
  jq -cn --arg ctx "$CONTENT" \
    '{hookSpecificOutput:{hookEventName:"SessionStart",additionalContext:$ctx}}'
fi
exit 0

settings.json equivalent (same hooks object, no description):
{
  "hooks": {
    "SessionStart": [
      { "matcher": "startup",
        "hooks": [ { "type": "command", "command": "/abs/path/load-context.sh", "timeout": 5 } ] }
    ]
  }
}
````

**⑦ 변종·분기** —

1) Event coverage: agent-skills + superpowers = SessionStart only; ponytail = SessionStart + UserPromptSubmit; claude-mem = Setup (300s warm-up) + SessionStart (2 chained handlers) + UserPromptSubmit. 2) Inline vs script: most keep the JSON command tiny and delegate to a sibling script; claude-mem inlines a large PATH-bootstrap + plugin-root-discovery one-liner. 3) Cross-platform: ponytail adds parallel commandWindows (PowerShell) per handler; superpowers routes through one hooks/run-hook.cmd dispatcher (+async:false); claude-mem/superpowers ship separate codex/cursor sibling files; agent-skills bash-only. 4) Output protocol: superpowers hand-rolls JSON via bash escaping, notes Claude Code wants hookSpecificOutput.additionalContext vs Cursor's additional_context (snake_case) -- emit only the host's field; agent-skills uses jq + non-standard {priority,message}; claude-mem emits {"continue":true,"suppressOutput":true}. 5) Fail-open idiom: || true (agent-skills) vs || exit 0 (ponytail) vs explicit exit 1+stderr when a required script is genuinely missing (claude-mem). 6) description key present in claude-mem, absent elsewhere. 7) timeout: 5s interactive (ponytail) vs 60-300s bg bootstrap (claude-mem); superpowers omits timeout, sets async:false.

**증거(실증 fetch)** — `DietrichGebert/ponytail:hooks/claude-codex-hooks.json` · `addyosmani/agent-skills:hooks/hooks.json` · `addyosmani/agent-skills:hooks/session-start.sh` · `thedotmack/claude-mem:plugin/hooks/hooks.json` · `thedotmack/claude-mem:plugin/hooks/codex-hooks.json` · `obra/superpowers:hooks/hooks.json` · `obra/superpowers:hooks/session-start` · `docs.claude.com:en/docs/claude-code/hooks (redirects to code.claude.com/docs/en/hooks)`

---

## 8. Agents (subagent role .md)  ·  🟨 COMMON

**① 공식 표준** — YES — official Anthropic spec: "Create custom subagents" (https://code.claude.com/docs/en/sub-agents, redirected from docs.claude.com/en/docs/claude-code/sub-agents). It MANDATES: a subagent is a Markdown file = YAML frontmatter + Markdown body; the body becomes the subagent's system prompt (it receives ONLY this, not the full CC system prompt, plus basic env like cwd). Only `name` and `description` are REQUIRED. All other frontmatter is optional with documented defaults. Spec-defined supported fields: description, name, tools, disallowedTools, model, permissionMode, mcpServers, hooks, maxTurns, skills, initialPrompt, memory, effort, background, isolation, color (the JSON `--agents` flag mirrors these but uses `prompt` instead of the markdown body). Identity comes ONLY from the `name` field — subfolders don't affect invocation; duplicate names within one scope are silently discarded.

**② 포맷** — Markdown file (`.md`) = YAML frontmatter delimited by `---` ... `---`, followed immediately by a Markdown body that IS the system prompt. UTF-8; one agent per file. Body convention varies (plain Markdown headings, or XML-tagged sections like `<role>`/`<Agent_Prompt>` — see variants).

**③ 위치** — Spec-defined, priority order (higher wins on name collision): managed (`<managed-settings>/.claude/agents/`, prio 1) > plugin (prio 2) > project `.claude/agents/` (prio 3, check into VCS) > user `~/.claude/agents/` (prio 4, personal/cross-project). Scanned RECURSIVELY, so subfolders (e.g. `agents/review/`, `agents/engineering/`) are allowed for organization only. Project dirs are also discovered by walking up from cwd to repo root. Observed in-repo: wshobson = `plugins/<plugin>/agents/<name>.md`; Yeachan & gsd = flat `agents/<name>.md`; msitarzewski = `engineering/<name>.md` grouped by domain.

**④ 스키마(키·필수/선택)** —

REQUIRED: `name` (string; canonical = kebab-case unique identifier, sole basis of identity/invocation) and `description` (string; natural-language trigger Claude reads to decide delegation — write it for routing, often ends "Use PROACTIVELY when…"). OPTIONAL (spec): `tools` (comma-separated allowlist; inherits ALL if omitted — do NOT list `Skill`, use `skills`), `disallowedTools` (comma-separated denylist, removed from inherited/specified set), `model` (`sonnet`|`opus`|`haiku`|`fable`|full id e.g. `claude-opus-4-8`|`inherit`; default `inherit`), `effort` (`low`|`medium`|`high`|`xhigh`|`max`), `permissionMode`, `mcpServers`, `hooks`, `maxTurns`, `skills`, `initialPrompt`, `memory`, `background`, `isolation` (e.g. `worktree`), `color`. NON-SPEC keys seen in the wild (free-form, ignored by loader but used by repo tooling/UX): `color` (named or hex), `emoji`, `vibe`, `level`, `category`. Note: plugin agents ignore `hooks`/`mcpServers`/`permissionMode`.

**⑤ 관례·주의** —

- `name`: kebab-case, globally unique across the whole agent tree (collisions silently discarded). Often namespaced by plugin/domain prefix (`api-scaffolding-backend-architect`, `gsd-code-reviewer`, `team-lead`).
- `description`: the most load-bearing field — it is Claude's routing signal. Make it specific and trigger-rich; the convention "Use PROACTIVELY when…" / "Spawned by /cmd" steers auto-delegation.
- Body = system prompt: open in 2nd person ("You are X…"), declare the role, then responsibilities. Strong convention to state NON-responsibilities / handoffs to other agents (Yeachan: "You are not responsible for… (executor/architect)"). Single-responsibility per agent.
- Restrict tools deliberately: read-only reviewers use `tools: Read, Grep, Glob` (allowlist) or `disallowedTools: Write, Edit` (denylist) — never both styles for the same intent.
- Model: pick by cost/capability (Haiku=cheap/fast classifier, Sonnet=balanced, Opus=hard reasoning) or `inherit` to follow the session.
- Output-artifact agents name their deliverable explicitly in body (gsd: "produce REVIEW.md").
- Cross-host portability: the YAML+body format is also the de-facto AGENTS.md/agent convention; keep non-spec keys minimal for portability since unknown keys are ignored.

**⑥ 최소 골격 (복붙 시작점)** —

````text
Minimal valid (spec example):
```markdown
---
name: code-reviewer
description: Reviews code for quality and best practices. Use PROACTIVELY after writing or changing code.
tools: Read, Glob, Grep
model: sonnet
---

You are a senior code reviewer ensuring high standards of quality and security.

## Focus
1. Correctness — does it do what it should?
2. Security — input validation, auth, injection risks.
3. Maintainability — will someone understand this in 6 months?
4. Tests — are the important paths covered?

## Rules
- Be specific: cite file:line, not "security issue".
- Explain WHY, then suggest the fix.
- Prioritize findings: 🔴 blocker / 🟡 suggestion / 💭 nit.
- You are NOT responsible for implementing fixes — report only.
```
Directory placement:
```
.claude/agents/            # project scope (check into VCS)
  code-reviewer.md
  review/                  # subfolders allowed (organization only)
    security-auditor.md
~/.claude/agents/          # user scope (all projects)
```
Bare minimum that loads (only the 2 required fields + a body):
```markdown
---
name: safe-researcher
description: Read-only research agent; gathers context without modifying files.
---

You are a research assistant. Investigate and summarize; never edit files.
```
````

**⑦ 변종·분기** —

1. BODY STRUCTURE: plain-Markdown-headings (msitarzewski, wshobson, gsd partly) vs XML-tagged system prompt — Yeachan uses `<Agent_Prompt><Role><Why_This_Matters>…`, gsd uses `<role><adversarial_stance><required_reading>`. XML tagging is a deliberate prompt-engineering choice for section addressability.
2. NAMESPACING: flat unique `name` (Yeachan: `code-reviewer`) vs prefixed (`gsd-code-reviewer`, `api-scaffolding-backend-architect`, `team-lead`) to avoid cross-plugin collisions.
3. TOOL POLICY: omit `tools` = inherit all (msitarzewski) vs explicit allowlist `tools: Read, Write, Bash, Grep, Glob` (gsd) vs denylist `disallowedTools: Write, Edit` (Yeachan). Read-only-reviewer enforcement is a fork in the road.
4. MODEL BINDING: hardcoded alias `model: opus`/`sonnet` (Yeachan, wshobson uses `inherit`) vs `model: inherit` (wshobson backend-architect) vs omitted entirely (msitarzewski) — couples or decouples agent from session model.
5. NON-SPEC METADATA: heavy persona/UX keys `color/emoji/vibe` + first-person "Identity & Memory" persona (msitarzewski) vs lean spec-only frontmatter (wshobson). msitarzewski/Yeachan add ranking keys (`level`, `color` hex).
6. ARTIFACT CONTRACT: pure-advisory agents (return summary to caller) vs file-producing agents that write a named artifact like `REVIEW.md` in a phase dir and are "Spawned by /cmd" (gsd) — the latter encodes a workflow-orchestration contract in the description.

**증거(실증 fetch)** — `claude-code-docs:code.claude.com/docs/en/sub-agents` · `msitarzewski/agency-agents:engineering/engineering-code-reviewer.md` · `msitarzewski/agency-agents:engineering/engineering-backend-architect.md (path)` · `wshobson/agents:plugins/api-scaffolding/agents/backend-architect.md` · `Yeachan-Heo/oh-my-claudecode:agents/code-reviewer.md` · `gsd-build/get-shit-done:agents/gsd-code-reviewer.md`

---

## 9. Evals harness (evals/) — gold-set fixtures + judge/Elo + per-skill evals.json + SWE-bench (shelf: COMMON)  ·  🟨 COMMON

**① 공식 표준** — NO single official spec. All patterns below are DE-FACTO, converging across 4 real repos. Two genuine EXTERNAL standards are referenced by implementations: (1) SWE-bench harness (princeton-nlp/swebench, swebench.harness.run_evaluation) — a real versioned dataset+grader that oh-my-claudecode wraps verbatim; (2) Elo rating math (universal: K-factor=32, base rating 1500.0, expected = 1/(1+10**((Rb-Ra)/400))) which wshobson implements exactly. Everything else — the per-skill evals.json shape, the gold/<task>/manifest.yaml + tuples/ + expected_outcomes.json layout, the LLM-judge anchored-rubric pattern, the ground-truth fixture/finding shape — is community convention with NO governing body. Anthropic skill guidance recommends evals but mandates no format. Treat every field name below as conventional, not normative.

**② 포맷** — Mixed, by approach. (A) Per-skill assertion evals: skills/<name>/evals/evals.json — one JSON object. (B) Gold-set corpora: evals/gold/<task>/ = manifest.yaml (YAML config) + tuples/NNN-*.json (one JSON input per case) + expected_outcomes.json (single JSON keyed by tuple-id) + README.md. (C) Judge/Elo engine: a Python package (pyproject.toml, src/<pkg>/) emitting JSON reports + a corpus/index.json. (D) SWE-bench: predictions.jsonl (JSONL, one prediction/line) + results/*.json + stats.json. (E) Ground-truth review fixtures: benchmarks/<agent>/fixtures/<domain>/*.md (the input) paired with benchmarks/<agent>/ground-truth/*.json (expected findings). Reports are JSON validated against a *.schema.json.

**③ 위치** — Two dominant placements. CO-LOCATED (per-skill, marketingskills): skills/<skill-name>/evals/evals.json — the eval sits beside the skill it tests; every skill gets its own. CENTRALIZED (whole-repo): a top-level evals/ (academic-research-skills: evals/gold/<task>/...), benchmarks/ (oh-my-claudecode ground-truth corpora), or benchmark/ (oh-my-claudecode SWE-bench runner). The Elo/judge engine ships as its own plugin dir: plugins/plugin-eval/ with src/, scripts/, agents/, commands/. Reports/baselines land in benchmarks/baselines/<date>-*.json or predictions/<variant>/. Runner scripts: scripts/run_evals.py (centralized) discovers every gold/<task>/manifest.yaml; CI wires it via .github/workflows/eval-harness.yml with a path filter on evals/gold/**.

**④ 스키마(키·필수/선택)** —

PER-SKILL evals.json (marketingskills): skill_name (str, req); evals (array, req) of {id (int, req), prompt (str, req — the user message to feed the skill), expected_output (str, req — prose description of correct behavior, used as judge rubric), assertions (array<str>, req — atomic checkable claims, the gradable unit), files (array, req but usually [] — attached input files)}.
GOLD-SET manifest.yaml (academic): task_name, manifest_version, task_type ('outcome-gradable'), outcome_gradable (bool), description, target {entrypoint (dotted module.fn), predicted_field, expected_outcomes_path, tuple_dir}, sample_n (int), labels (array<str> — the class enum), thresholds {aggregate {metric:'accuracy', direction:'higher_is_better', comparison:'>=', threshold_value:0.90}, per_class {... threshold_value:0.85, classes:[...]}}, tuple_distribution (array of {kind, n, expected_<field>}). All req for a gradable task.
TUPLE NNN-*.json: tuple_id (req, must match filename stem + key in expected_outcomes), kind (req, one of tuple_distribution kinds), corpus_entry (req — the actual input payload, domain-shaped).
expected_outcomes.json: object keyed by tuple_id -> {<predicted_field>: <expected label>, ...per-resolver/per-check detail}.
GROUND-TRUTH json (omc): fixtureId, fixturePath, domain, expectedVerdict ('REJECT'|'ACCEPT'), isCleanBaseline (bool), findings (array of {id, severity (CRITICAL|MAJOR|MINOR), category, summary, keywords (array<str> — substring matchers used for scoring), location (opt), explanation}).
SWE-bench predictions.jsonl line: {instance_id, model_name_or_path, model_patch (the diff)}.
ENGINE corpus/index.json entry: {name, path, category, line_count, elo_rating (default 1500.0)}.

**⑤ 관례·주의** —

- Assertions are the atomic gradable unit: write each as one independently true/false claim; pass-rate = fraction satisfied (de-facto judge target). Keep prompts realistic, including deliberately casual/underspecified phrasings (marketingskills eval id 2,3) to test triggering.
- Tuple naming: NNN-{kind-slug}-{discriminator}.json, zero-padded sequential; the stem MUST equal tuple_id MUST equal the expected_outcomes key (3-way invariant; a validator enforces it: scripts/check_evals_gold_set).
- Gold sets balance classes deliberately and document distribution in the manifest (tuple_distribution); include at least one by-design hard/negative canary (academic's title-only fabrication exercising the unresolvable path).
- Thresholds are gates, not vibes: aggregate (e.g. accuracy>=0.90) AND per-class floors (>=0.85) so a rare class can't be masked by an easy majority.
- Judge rubrics are ANCHORED 0.0/0.25/0.5/0.75/1.0 with a one-line behavior description at each anchor (wshobson ORCHESTRATION_RUBRIC); never an unanchored 1-10.
- Model tiers are aliased (haiku/sonnet/opus -> full id) not hardcoded inline; judge runs async.
- Composite scoring: weighted dimensions summing to 1.0, each blended across layers (static/judge/monte_carlo) per a LAYER_BLENDS table.
- Elo: K=32, init 1500, bootstrap CI via resampling matchups (n_resamples=500, 2.5/97.5 pctile), seedable for determinism.
- Ground-truth scoring is keyword-substring based (findings[].keywords) so it is graderless/cheap; pair every dirty fixture with a clean baseline (isCleanBaseline) to measure false-positive rate.
- Baselines are snapshotted dated (benchmarks/baselines/YYYY-MM-DD-*.json); runner supports --baseline before.json --compare after.json to emit lift_pre/lift_post and a CI lift-gate blocks un-acknowledged regressions.
- Missing entrypoint/gold set => report 'pending'/'skipped', never a hard fail (graceful partial harness).
- SWE-bench: always wrap the OFFICIAL harness, never reimplement grading; accept JSON or JSONL predictions.
GOTCHA: the co-located vs centralized choice is load-bearing — co-located scales per-skill but has no cross-skill ranking; centralized gives Elo/lift but couples to a runner.

**⑥ 최소 골격 (복붙 시작점)** —

````text
PATTERN A — per-skill assertion eval (simplest, start here):
skills/my-skill/evals/evals.json
------------------------------------------------
{
  "skill_name": "my-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "Realistic user request that should trigger and exercise the skill.",
      "expected_output": "Prose describing correct behavior; doubles as the judge rubric. Mention the must-haves.",
      "assertions": [
        "Checks for the prerequisite file first",
        "Uses the required framework/structure",
        "Produces the structured output format"
      ],
      "files": []
    },
    {
      "id": 2,
      "prompt": "A deliberately casual / underspecified phrasing to test triggering.",
      "expected_output": "Should still trigger and handle the edge case.",
      "assertions": ["Triggers on casual phrasing", "Asks for the missing parameter"],
      "files": []
    }
  ]
}

PATTERN B — centralized gold set with threshold gate (graded, CI-able):
evals/
  README.md
  gold/
    my_task/
      README.md
      manifest.yaml
      expected_outcomes.json
      tuples/
        001-positive-basic.json
        002-negative-edge.json

evals/gold/my_task/manifest.yaml
------------------------------------------------
task_name: my_task
manifest_version: "1.0.0"
task_type: outcome-gradable
outcome_gradable: true
description: |
  One-line statement of what this measures and which canary cases matter.
target:
  entrypoint: my_module.classify
  predicted_field: label
  expected_outcomes_path: expected_outcomes.json
  tuple_dir: tuples
sample_n: 2
labels: ["pass", "fail"]
thresholds:
  aggregate:    {metric: accuracy, direction: higher_is_better, comparison: ">=", threshold_value: 0.90}
  per_class:    {metric: accuracy, direction: higher_is_better, comparison: ">=", threshold_value: 0.85, classes: ["pass", "fail"]}
tuple_distribution:
  - {kind: positive, n: 1, expected_label: "pass"}
  - {kind: negative, n: 1, expected_label: "fail"}

evals/gold/my_task/tuples/001-positive-basic.json
------------------------------------------------
{
  "tuple_id": "001-positive-basic",
  "kind": "positive",
  "corpus_entry": { "input": "the actual payload your entrypoint consumes" }
}

evals/gold/my_task/expected_outcomes.json
------------------------------------------------
{
  "001-positive-basic": { "label": "pass" },
  "002-negative-edge":  { "label": "fail" }
}

Run:  PYTHONPATH=. python -m scripts.run_evals --task my_task --output report.json
Gate: scripts/check_ranking_lift.py report.json   (blocks on un-acknowledged regression)

PATTERN E — ground-truth review fixture (graderless, keyword-scored):
benchmarks/my-agent/fixtures/code/code-sqli.md   <- the buggy input
benchmarks/my-agent/ground-truth/code-sqli.json
------------------------------------------------
{
  "fixtureId": "code-sqli",
  "fixturePath": "fixtures/code/code-sqli.md",
  "domain": "code",
  "expectedVerdict": "REJECT",
  "isCleanBaseline": false,
  "findings": [
    {
      "id": "SQL-CRIT-1",
      "severity": "CRITICAL",
      "category": "finding",
      "summary": "SQL injection via string interpolation in search query",
      "keywords": ["SQL", "injection", "interpolation", "parameteriz", "prepared"],
      "location": "GET /search:33",
      "explanation": "User input concatenated into SQL; must use parameterized queries."
    }
  ]
}
(Always add a paired clean fixture with isCleanBaseline:true and findings:[] to measure false positives.)
````

**⑦ 변종·분기** —

1. PLACEMENT: co-located per-skill (marketingskills: skills/*/evals/evals.json) vs centralized (academic: evals/gold/, omc: benchmarks/). Co-located = trivially per-skill, no global ranking; centralized = Elo + lift + CI gates but needs a runner.
2. GRADING MECHANISM, 4 observed flavors: (a) LLM-judge against an anchored rubric / expected_output prose (wshobson, marketingskills' expected_output); (b) deterministic outcome-classification accuracy vs a fixed label enum with thresholds (academic manifest); (c) keyword-substring matching over expected findings (omc ground-truth — cheap, no model); (d) external official harness pass/fail (omc SWE-bench wrapping swebench).
3. SCORING UNIT: pairwise Elo ranking of skills against each other (wshobson, K=32, bootstrap CI) vs absolute per-task accuracy/threshold (academic) vs binary verdict+finding-recall (omc reviewer) vs %resolved (SWE-bench).
4. CONFIG SURFACE: rich YAML manifest with per-class thresholds + distribution (academic) vs zero-config flat JSON list of cases (marketingskills) vs Python DIMENSION_WEIGHTS/LAYER_BLENDS constants in code (wshobson).
5. EXPECTED-OUTPUT REPRESENTATION: free-text prose rubric (marketingskills, wshobson) vs structured machine-checkable labels/resolver-outcomes (academic) vs structured findings list with keywords (omc).
6. REGRESSION HANDLING: dated baseline snapshots + lift_pre/lift_post compare + CI block (academic, omc benchmark/compare_results.py) vs none (marketingskills is point-in-time).
7. MODEL DEPENDENCE: judge requires claude-agent-sdk and a live model (wshobson, marketingskills) vs fully offline deterministic (academic outcome-grading, omc keyword scoring) — the offline ones are reproducible in CI without API keys, a real design fork.

**증거(실증 fetch)** — `coreyhaines31/marketingskills:skills/ab-testing/evals/evals.json` · `coreyhaines31/marketingskills:skills/copywriting/evals/evals.json` · `Imbad0202/academic-research-skills:evals/README.md` · `Imbad0202/academic-research-skills:evals/gold/citation_extraction/manifest.yaml` · `Imbad0202/academic-research-skills:evals/gold/citation_extraction/expected_outcomes.json` · `Imbad0202/academic-research-skills:evals/gold/citation_extraction/tuples/001-valid-doi-numpy-2020.json` · `wshobson/agents:plugins/plugin-eval/.claude-plugin/plugin.json` · `wshobson/agents:plugins/plugin-eval/src/plugin_eval/elo.py` · `wshobson/agents:plugins/plugin-eval/src/plugin_eval/corpus.py` · `wshobson/agents:plugins/plugin-eval/src/plugin_eval/layers/judge.py` · `wshobson/agents:plugins/plugin-eval/src/plugin_eval/engine.py` · `Yeachan-Heo/oh-my-claudecode:benchmarks/code-reviewer/ground-truth/code-sql-injection.json` · `Yeachan-Heo/oh-my-claudecode:benchmark/README.md` · `Yeachan-Heo/oh-my-claudecode:benchmark/evaluate.py`

---

## 10. Templates (scaffolding) — COMMON shelf  ·  🟨 COMMON

**① 공식 표준** — No single official spec governs harness-package templates. The named reference is **cookiecutter** (de-facto standard for project scaffolding): it mandates a `cookiecutter.json` config at repo root declaring variables, a single `{{ cookiecutter.<var> }}` Jinja2 token syntax, and a templated project directory literally named `{{ cookiecutter.project_slug }}/` whose path components and file contents are rendered. NONE of the four canonical repos use cookiecutter or Jinja2 — they are skill/agent "scaffolding" templates, not project generators. So cookiecutter is the conceptual ancestor only. The REAL de-facto standard observed is two divergent, simpler conventions: (a) **machine-substituted ALL-CAPS tokens** `{{TOKEN}}` / positional `{N}` filled by a renderer (career-ops HTML/TeX, gsd `template.cjs`); (b) **human/agent-filled `[bracketed text]`** placeholders with inline instructional `<!-- comments -->` deleted after use (academic-research, gsd markdown specs). All are flat files copied into the work area and filled, not a parameterized directory tree.

**② 포맷** — Plain template files in the artifact's native format — no wrapper, no required frontmatter. Observed file types: `.html`, `.tex`, `.md`, `.js`, `.xml`, `.json`, `.yml`. Tokens are embedded inline in that native syntax: `{{NAME}}` / `{{LANG}}` / `{{PAGE_WIDTH}}` (career-ops), `{N}` / `{phase_name}` (gsd headings), `[bracketed text]` plus `<!-- instructional comments -->` (academic, gsd). One config-style template is structured data: gsd `templates/config.json` is a literal default JSON object (no tokens — copied verbatim as a starting config). `.example`/`.template` infix marks copy-me-first files (career-ops `portals.example.yml`, `modes/_profile.template.md`).

**③ 위치** — A directory literally named `templates/` is the universal convention. Two placement patterns: (1) **repo-root `templates/`** for a single-purpose tool (career-ops `templates/`, gsd `get-shit-done/templates/`); (2) **per-skill `<skill-name>/templates/`** co-located beside `SKILL.md` for multi-skill packages (anthropics `skills/algorithmic-art/templates/`, academic `academic-paper/templates/`, `academic-paper-reviewer/templates/`). Shared/cross-skill templates go in `shared/templates/`. Sub-grouping by category is allowed (gsd `templates/codebase/*.md`). Script-internal asset templates may sit under `scripts/templates/` (anthropics `skills/docx/scripts/templates/*.xml`). Note: `.github/ISSUE_TEMPLATE/` and `PULL_REQUEST_TEMPLATE` are a SEPARATE GitHub-native convention, not this component.

**④ 스키마(키·필수/선택)** —

There is no enforced key schema for the template files themselves (they are free-form artifacts). The fields are the *tokens* a template exposes:
- career-ops cv-template.html — `{{LANG}}`, `{{NAME}}`, `{{PAGE_WIDTH}}` (all required; ALL-CAPS double-brace).
- career-ops cv-template.tex — no inline tokens; structural LaTeX macros (`\resumeItem{}`, `\resumeSubheading{}{}{}{}`) are the fill points.
- gsd templates/config.json (the one structured template) keys: `mode` (req, "interactive"), `granularity` (req), `workflow.{research,plan_check,verifier,auto_advance,nyquist_validation,security_enforcement,security_asvs_level,security_block_on,discuss_mode,...}`, `ship.pr_body_sections[]`, `planning.{commit_docs,search_gitignored,sub_repos[]}`, `git.create_tag`, `parallelization.{enabled,max_concurrent_agents,...}`, `gates.{confirm_*}`, `safety.*`, `hooks.context_warnings`, `project_code` (nullable), `agent_skills` (obj), `claude_md_path` (req). All have committed defaults; consumer overrides.
- gsd markdown templates (AI-SPEC.md) — heading tokens `{N}`, `{phase_name}` (machine-filled by template.cjs), body `<!-- HTML comment instructions -->` (human-filled, deleted after).
- academic *_template.md — `[bracketed text]` placeholders (required-to-replace), `*`-marked required fields, `## Usage` instruction block at top.
Convention: a token is REQUIRED unless an instruction marks it optional/`(if applicable)`.

**⑤ 관례·주의** —

- Directory always `templates/` (plural). Filenames suffixed `-template`/`_template` or infixed `.template`/`.example` (career-ops, academic) — though anthropics/gsd often omit the suffix when the dir already says `templates/`.
- Two non-mixable token styles: pick ONE per file. `{{ALL_CAPS}}` or `{N}` = a renderer substitutes it (career-ops `template.cjs`); `[sentence-case bracket]` = a human/agent fills it by hand. Never mix machine + manual tokens in the same file ambiguously.
- Self-documenting: lead the file with a `## Usage`/`Usage Instructions` block (academic) or a top `<!-- THIS IS A TEMPLATE ... WHAT TO KEEP / WHAT TO EDIT -->` banner (anthropics viewer.html). Instructional comments are meant to be DELETED after fill.
- "Structure, not content": anthropics templates explicitly say they prescribe shape/best-practices only, not the creative output — keep skeleton, replace algorithm/params.
- `.example` config templates are copied to a real (often gitignored) name before edit (career-ops: copy `portals.example.yml`→`portals.yml`).
- Templates are committed, version-controlled, license-attributed where derived (career-ops .tex credits sb2nov, MIT).
- Keep templates small/single-responsibility; one template per output artifact type (gsd has minimal/standard/complex summary variants selected by heuristic).
- Cross-host portability: pure text + native-format tokens, no build step required to read them.

**⑥ 최소 골격 (복붙 시작점)** —

````text
Per-skill layout (most common, anthropics/academic style):

  my-skill/
  ├── SKILL.md
  └── templates/
      ├── report_template.md        # human-filled [brackets]
      └── viewer.html               # machine/agent-filled {{TOKENS}}

templates/report_template.md  (human-fill convention):

  # Report Template

  ## Usage
  Replace all `[bracketed text]` with your content.
  Delete instructional comments (`<!-- ... -->`) after use.
  Fields marked `*` are required.

  ---

  # [Report Title]

  **Author:** [Name] *
  **Date:** [YYYY-MM-DD] *

  ## Summary *
  [2-3 sentences: what was done and the key result.]

  ## Findings
  1. [Finding one]
  2. [Finding two]   <!-- add rows as needed; delete if none -->

templates/viewer.html  (machine-substituted convention):

  <!DOCTYPE html>
  <!-- TEMPLATE: keep structure, edit only the marked regions. -->
  <html lang="{{LANG}}">
  <head><meta charset="UTF-8"><title>{{TITLE}}</title></head>
  <body>
    <main style="max-width:{{PAGE_WIDTH}}">
      <h1>{{NAME}}</h1>
    </main>
  </body>
  </html>

Config-default template (gsd style) — templates/config.json copied verbatim as the starting config:

  {
    "mode": "interactive",
    "granularity": "standard",
    "workflow": { "research": true, "verifier": true },
    "gates": { "confirm_plan": true },
    "claude_md_path": "./CLAUDE.md"
  }

Renderer contract (if machine-substituted): a small lib reads the file, `str.replace(/\{\{(\w+)\}\}/g, k => vars[k])`, writes to the work area (cf. gsd bin/lib/template.cjs: select-by-heuristic then fill).
````

**⑦ 변종·분기** —

1. **Fill mechanism** — the core fork: machine-substituted `{{TOKEN}}`/`{N}` requiring a renderer (career-ops HTML+TeX, gsd headings via template.cjs) VS. human/agent-filled `[brackets]` + deletable `<!-- comments -->`, zero tooling (academic-research, gsd markdown specs). Some files combine: machine heading tokens + manual body.
2. **Placement** — repo-root single `templates/` (career-ops, gsd) vs. per-skill `skill/templates/` co-located with SKILL.md (anthropics, academic) vs. `shared/templates/` for reuse.
3. **Token syntax** — double-brace ALL_CAPS `{{NAME}}` (career-ops) vs. single-brace `{N}` (gsd headings) vs. square `[text]` (academic) vs. native macros `\resumeItem{}` (TeX) vs. NO tokens, verbatim copy (gsd config.json, anthropics structural templates).
4. **Granularity / selection** — one template per artifact (career-ops) vs. multiple tiers chosen by a heuristic selector (gsd minimal/standard/complex summaries) vs. category sub-dirs (gsd templates/codebase/*).
5. **Self-doc placement** — top `## Usage` block (academic) vs. leading HTML/comment banner with KEEP/EDIT checklist (anthropics).
6. **Config vs. document templates** — most are document skeletons; gsd `config.json` is a structured-data default (full key set, no tokens, override-after-copy). `.example`/`.template` filename infix signals copy-before-edit (career-ops).

**증거(실증 fetch)** — `santifer/career-ops:templates/cv-template.html` · `santifer/career-ops:templates/cv-template.tex` · `santifer/career-ops:templates/portals.example.yml` · `gsd-build/get-shit-done:get-shit-done/templates/config.json` · `gsd-build/get-shit-done:get-shit-done/templates/AI-SPEC.md` · `gsd-build/get-shit-done:get-shit-done/bin/lib/template.cjs` · `anthropics/skills:skills/algorithmic-art/templates/generator_template.js` · `anthropics/skills:skills/algorithmic-art/templates/viewer.html` · `Imbad0202/academic-research-skills:academic-paper/templates/imrad_template.md` · `Imbad0202/academic-research-skills:academic-paper-reviewer/templates/peer_review_report_template.md`

---

## 11. MCP server (.mcp.json + server) — COMMON shelf  ·  🟨 COMMON

**① 공식 표준** — TWO official specs, both consulted and both real:

1. Model Context Protocol (modelcontextprotocol.io) — the open JSON-RPC 2.0 wire protocol. Mandates: newline-delimited JSON-RPC 2.0 over a transport (stdio | Streamable HTTP | SSE | WebSocket); the `initialize` handshake (client sends protocolVersion + capabilities, server replies with its capabilities + serverInfo {name, version}); and the capability methods `tools/list`+`tools/call`, `prompts/list`+`prompts/get`, `resources/list`+`resources/read`, plus server-initiated `roots/list`. Tool result = `{ content: [{type:"text",text}], structuredContent?, isError? }`. (codegraph/transport.ts encodes the JSON-RPC envelope + standard error codes -32700/-32600/-32601 verbatim.)

2. Claude Code MCP docs (code.claude.com/docs/en/mcp, fetched OK after 301 from docs.claude.com) — the HOST-side `.mcp.json` config schema + scopes. SPEC-MANDATED here: the `mcpServers` object keyed by server name; per-server `type`/transport selector; for stdio → `command`+`args`+`env`; for http/sse/ws → `url`+`headers`. `type:"streamable-http"` is an accepted alias for `"http"`. Three scopes: local (default, `~/.claude.json`), project (`.mcp.json` checked into VCS), user (`~/.claude.json`, all projects). Claude Code sets `CLAUDE_PROJECT_DIR` in the spawned stdio server's env; `${CLAUDE_PLUGIN_ROOT}`/`${CLAUDE_PLUGIN_DATA}` expand in plugin-bundled configs.

The `.mcpb`/Desktop `manifest.json` (manifest_version 0.3) seen in last30days is a SEPARATE, de-facto packaging spec (Anthropic's bundle format), not the MCP wire spec and not `.mcp.json`.

**② 포맷** — Two artifacts, distinct formats:

(A) The CONFIG — `.mcp.json`: a JSON object, no frontmatter. Top-level `{ "mcpServers": { "<name>": {…} } }`. Same shape inlined under `plugin.json`'s `mcpServers`, or under `projects.<path>.mcpServers` in `~/.claude.json` for local/user scope.

(B) The SERVER — an executable program in any language linking an MCP SDK:
  - JS/TS: `@modelcontextprotocol/sdk` (`McpServer` + `StdioServerTransport`), ESM (`"type":"module"`), tool/prompt schemas via `zod`. (ponytail/index.js, package.json)
  - Go: `github.com/mark3labs/mcp-go` (`server.NewMCPServer` + `server.ServeStdio`). (last30days/main.go)
  - or a hand-rolled JSON-RPC loop over stdin/stdout (codegraph/transport.ts).
The server's only hard contract is: speak MCP on its stdin/stdout (stdio) or bind a URL (http). It is wired to a host purely by a `.mcp.json` entry.

**③ 위치** — CONFIG `.mcp.json`:
  - Project scope → repo root `/.mcp.json` (checked into VCS, shared with team).
  - Plugin scope → plugin root `/.mcp.json` or inlined in `plugin.json`.
  - Local/user scope → NOT a file you author; Claude Code writes it into `~/.claude.json` (under `projects.<path>.mcpServers` for local, top-level for user) via `claude mcp add`.

SERVER code: conventionally its own subdir/package, e.g. `ponytail-mcp/` (DietrichGebert/ponytail), `mcp/` Go module (mvanhorn/last30days-skill), `src/mcp/` (colbymchenry/codegraph), `apps/daemon/src/mcp*.ts` (nexu-io/open-design). Entry point is `index.js` / `cmd/<name>/main.go` / `index.ts`.

**④ 스키마(키·필수/선택)** —

`.mcp.json` keys:
  mcpServers              object, REQUIRED — map of serverName → serverEntry.

serverEntry (stdio):
  command                 string, REQUIRED — executable (e.g. "node","python","/abs/path/bin").
  args                    string[], optional — argv after command.
  env                     object<string,string>, optional — env vars; supports `${VAR}` / `${VAR:-default}` expansion.
  type                    string, optional — "stdio" (default if command present).
  timeout                 number(ms), optional — per-server tool-exec timeout (overrides MCP_TOOL_TIMEOUT).

serverEntry (http / sse / ws):
  type                    string, REQUIRED — "http" | "streamable-http"(alias) | "sse" | "ws".
  url                     string, REQUIRED — server endpoint (https:// or wss://).
  headers                 object<string,string>, optional — e.g. {"Authorization":"Bearer …"}.
  timeout                 number(ms), optional.

Server-side capability registration (the actual surface a builder writes):
  tool: name(REQUIRED) + description + inputSchema(zod/JSON-Schema) + optional outputSchema + annotations{readOnlyHint, destructiveHint, openWorldHint, idempotentHint}. Handler returns {content:[{type:"text",text}], structuredContent?, isError?}. (ponytail registerTool; last30days NewTool + WithString/WithReadOnlyHintAnnotation.)
  prompt: name + title + description + argsSchema; returns {messages:[{role,content}]}. (ponytail registerPrompt.)
  serverInfo: {name REQUIRED, version REQUIRED} passed at construction (McpServer({name,version}) / NewMCPServer(name,version)).

`.mcpb` manifest.json (de-facto, Desktop bundles only): manifest_version, name, version, description, author, server{type:"binary"|"node"|…, entry_point, mcp_config{command,args,env}}, user_config{<key>{type,title,description,sensitive,required}}.

**⑤ 관례·주의** —

- One server = one clear purpose; tools added one-per-file with one `AddTool`/`registerTool` call each (last30days research.go comment makes this explicit).
- Stdio is the default/portable choice for local tools needing system access; pick http/sse for remote/shared. Stdio servers are NOT auto-reconnected; http/sse reconnect with exponential backoff (5 attempts).
- NEVER write to stdout for logging on a stdio server — stdout is the JSON-RPC channel. Log to stderr (last30days: `fmt.Fprintf(os.Stderr,…)`; exit non-zero on transport failure).
- Resolve project paths from `CLAUDE_PROJECT_DIR` env (Claude Code injects it) or via the MCP `roots/list` request — do NOT rely on cwd. In project/user-scoped `.mcp.json`, `${CLAUDE_PROJECT_DIR}` needs a default `${CLAUDE_PROJECT_DIR:-.}`; in plugin configs it substitutes directly.
- Use `${VAR}` expansion + `sensitive:true` user_config for secrets; never hardcode API keys in `.mcp.json` (which is committed).
- Annotate tools honestly: `readOnlyHint`/`destructiveHint`/`openWorldHint` (both ponytail and last30days set all three) so the host can gate dangerous calls.
- Mark tools that return structured data with both a text `content` block AND `structuredContent`/`outputSchema` (ponytail does both) for hosts that consume either.
- Version the serverInfo; last30days stamps build version via ldflags to namespace its per-user cache so multiple installed versions coexist.
- Project-scoped `.mcp.json` servers are pending-approval until the user accepts (security gate); keep the entry minimal and reviewable.
- Cross-host portability: the `.mcp.json` shape is the de-facto interchange format (open-design deliberately mirrors it + Cursor's so users copy-paste between tools).

**⑥ 최소 골격 (복붙 시작점)** —

````text
DIR LAYOUT (stdio Node server + project-scoped config):

  myproj/
  ├── .mcp.json                ← committed, project scope
  └── mytool-mcp/
      ├── package.json
      └── index.js             ← the server

--- .mcp.json (project root) ---
{
  "mcpServers": {
    "mytool": {
      "command": "node",
      "args": ["${CLAUDE_PROJECT_DIR:-.}/mytool-mcp/index.js"],
      "env": { "MYTOOL_API_KEY": "${MYTOOL_API_KEY}" }
    }
  }
}

--- mytool-mcp/package.json ---
{
  "name": "mytool-mcp",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.26.0",
    "zod": "^3.23.0"
  }
}

--- mytool-mcp/index.js ---
#!/usr/bin/env node
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({ name: "mytool", version: "0.1.0" });

server.registerTool(
  "echo",
  {
    title: "Echo",
    description: "Return the given text. Read-only, no side effects.",
    inputSchema: { text: z.string().describe("Text to echo back.") },
    outputSchema: { text: z.string() },
    annotations: { readOnlyHint: true, openWorldHint: false },
  },
  ({ text }) => ({
    content: [{ type: "text", text }],
    structuredContent: { text },
  }),
);

// NEVER console.log here — stdout is the JSON-RPC channel. Use console.error.
await server.connect(new StdioServerTransport());

Run/verify:  cd mytool-mcp && npm install && node index.js   (then point a host at it, or `claude mcp add --transport stdio mytool -- node mytool-mcp/index.js`)

--- HTTP variant of the .mcp.json entry (no local process) ---
{
  "mcpServers": {
    "stripe": { "type": "http", "url": "https://mcp.stripe.com" }
  }
}
````

**⑦ 변종·분기** —

Real divergences a builder must decide between:

1. LANGUAGE / SDK: high-level SDK (ponytail = `@modelcontextprotocol/sdk` McpServer; last30days = Go `mark3labs/mcp-go`) vs hand-rolled JSON-RPC loop over stdin/stdout (codegraph/transport.ts — chosen because it also multiplexes a Unix-socket daemon transport sharing one engine across N clients). Default to an SDK; hand-roll only if you need an exotic transport.

2. TRANSPORT: stdio (all four local servers) vs Streamable-HTTP/SSE (open-design supports `'stdio'|'sse'|'http'`; Claude docs add `ws`). stdio = simplest, local, no reconnect; http = remote/shared, auto-reconnect, needs `url`/`headers`/auth.

3. SURFACE PRIMITIVE: tools only (last30days, codegraph) vs tools + prompts (ponytail exposes BOTH a `ponytail` prompt and a `ponytail_instructions` tool — because no portable MCP "inject every turn" primitive exists, so it serves the prompt menu AND tool-pullers). Decide which host injection points you must cover.

4. CLIENT vs SERVER role: most repos BUILD a server; open-design is an MCP CLIENT that stores external servers in its own `<dataDir>/mcp-config.json` (`{servers:[{id,transport,enabled,authMode,command,args,env,url,headers}]}`) and re-emits a `.mcp.json` at spawn time — note the richer per-entry fields (id, enabled, authMode:'none'|'oauth') beyond the bare `.mcp.json` schema.

5. PACKAGING/DISTRIBUTION: raw repo subdir + `claude mcp add` (ponytail, codegraph) vs `.mcpb` Desktop bundle with a `manifest.json` (manifest_version 0.3) declaring `server.type:"binary"`, `mcp_config`, and a typed `user_config` block for secrets (last30days). The manifest's `${user_config.X}` / `${__dirname}` expansion is a Desktop-specific superset of `.mcp.json` env expansion.

6. CONFIG STORAGE / SCOPE: hand-authored project `.mcp.json` (committed) vs plugin-bundled `.mcp.json`/`plugin.json` (`${CLAUDE_PLUGIN_ROOT}` expansion) vs `claude mcp add` writing local/user entries into `~/.claude.json`.

**증거(실증 fetch)** — `DietrichGebert/ponytail:ponytail-mcp/index.js` · `DietrichGebert/ponytail:ponytail-mcp/package.json` · `DietrichGebert/ponytail:ponytail-mcp/README.md` · `mvanhorn/last30days-skill:mcp/cmd/last30days-pp-mcp/main.go` · `mvanhorn/last30days-skill:mcp/internal/tools/research.go` · `mvanhorn/last30days-skill:mcp/manifest.json` · `colbymchenry/codegraph:src/mcp/index.ts` · `colbymchenry/codegraph:src/mcp/transport.ts` · `nexu-io/open-design:apps/daemon/src/mcp-config.ts` · `code.claude.com/docs/en/mcp` · `modelcontextprotocol.io`

---

## 12. Model-binding config (role &lt;-&gt; model/provider)  ·  🟥 SPARSE

**① 공식 표준** — No single official spec. Two de-facto standards converge across the repos:

1. SPEC-MANDATED (Codex CLI): the `model_providers` block is a real, schema-backed Codex construct (`#:schema https://developers.openai.com/codex/config-schema.json`, https://developers.openai.com/codex/config-reference). It defines `model`, `model_provider`, and `[model_providers.<id>]` tables (base_url/env_key/wire_api). Per-role overrides live in separate native-agent files referenced from `[agents.<role>]`.

2. DE-FACTO (the harness 2-block pattern, no official spec): a PROVIDERS block (provider id -> base_url + credential env/secret name) + a MODELS/ROLES block (each model entry carries `provider`; roles/modes/agents map to a model name). Resolution is a priority chain: role/agent-specific > mode default > `default` key > env-var fallback > hardcoded default. ruflo's `config.json` (`models[]` + `secrets{}`) and oh-my-codex's `.omx-config.json` (`models`/`agentModels`/`env`) are the two cleanest real instances. last30days implements provider indirection in code (a static provider catalog + a priority resolver) rather than in config.

I confirmed: there is NO universal cross-repo file format — TOML (Codex/ruflo `.agents`), JSON (ruflo app config, oh-my-codex), and Python catalog (last30days) all coexist. The CONVERGENT invariant is the two-level indirection: role/mode -> model-name -> provider -> credentials.

**② 포맷** — Three real encodings observed (builder picks one):
- TOML (Codex-native): `.codex/config.toml` / `.agents/config.toml` — top-level `model`/`model_provider`, `[model_providers.<id>]` tables, `[profiles.<name>]` overrides, `[agents.<role>]` pointing at per-role `*.toml` files (each its own `model = ...`).
- JSON: ruflo `config.json` (`models[]` array of objects + `secrets{}` map); oh-my-codex `.omx-config.json` (`models`, `agentModels`, `agentReasoning`, `env` objects).
- Python catalog + resolver (last30days `providers.py`): module-level model-name constants + per-provider client classes + URL/env constants; resolution by priority in code.
No frontmatter. TOML files carry a `#:schema` comment line for editor validation.

**③ 위치** — Codex-native: project `./.codex/config.toml` OR user `${CODEX_HOME:-~/.codex}/config.toml`; per-role files at `.codex/agents/<role>.toml` (referenced by `[agents.<role>].config_file`). ruflo Codex variant: `.agents/config.toml`. 
Harness app/JSON: ruflo `src/config/config.json` (template `config.example.json`); oh-my-codex `${CODEX_HOME:-~/.codex}/.omx-config.json` (project scope `./.codex/.omx-config.json`, selected via `./.omx/setup-scope.json`). 
Code resolver: `skills/<name>/scripts/lib/providers.py`. 
Operator-facing doc: `CONFIGURATION.md` / `docs/MODELS.md` / `docs/reference/omx-config-schema-routing.md` at repo root or under `docs/`.

**④ 스키마(키·필수/선택)** —

PROVIDERS block:
- Codex `[model_providers.<id>]`: `base_url` (req for non-OpenAI), `env_key` (req — name of the API-key env var), `wire_api` (opt: "responses"|"chat"), `name` (opt display). Top-level `model_provider` (opt) selects the active id; defaults to built-in.
- ruflo `secrets{}`: `<provider>ApiKey` -> secret-manager name (req per used provider). Providers themselves are implicit, auto-detected from model name (gemini-* -> gemini; contains "/" -> openrouter; else openai).

MODELS / ROLES block:
- ruflo `models[]` entry: `name` (req, the model id), `provider` (req: gemini|openai|openrouter), `displayName` (opt), `description` (opt), `supportsTools` (opt bool), `multimodal` (opt bool), `parameters{}` (opt, e.g. temperature). First/flagged entry = default.
- oh-my-codex `.omx-config.json`: `models{}` (req-ish: mode-key -> model-name; `default` key is the catch-all), `agentModels{}` (opt: role/agent-name -> model-name), `agentReasoning{}` (opt: role -> low|medium|high|xhigh), `env{}` (opt: `OMX_DEFAULT_FRONTIER_MODEL`/`OMX_DEFAULT_STANDARD_MODEL`/`OMX_DEFAULT_SPARK_MODEL` fallbacks).
- Codex per-role `agents/<role>.toml`: `model` (req), `model_reasoning_effort` (opt), `sandbox_mode` (opt), `developer_instructions` (opt). Registered via top-level `[agents.<role>]` with `description` + `config_file`.

PROFILES (opt, Codex): `[profiles.<name>]` re-declaring `model`/`approval_policy`/`sandbox_mode`/`web_search`; selected with `codex -p <name>`.

**⑤ 관례·주의** —

- Two-level indirection is the load-bearing convention: role/mode -> model-name -> provider -> credentials. Never bind a role straight to a URL/key.
- Credentials are NEVER inlined: store the env-var NAME (`env_key`/`OPENAI_API_KEY`) or secret-manager name (`openai-api-key`), not the value.
- Resolution is an explicit priority chain, most-specific wins: role/agent-specific > mode-specific > `default` key > env-var fallback > hardcoded constant (oh-my-codex documents exactly this; flags/CLI beat env in last30days).
- Fail-soft on bad config: oh-my-codex returns null/falls back on malformed JSON or wrong-shaped sections; "unknown keys are not a stable extension point."
- Provider can be explicit (`provider: "openai"`) or inferred from model-name pattern (ruflo MCP bridge). Explicit is safer; inference is terser.
- Keep a `default` model entry/key so an unmapped role still resolves.
- Naming: model `name` = exact upstream id; OpenRouter ids are `vendor/model` (the "/" doubles as the provider hint).
- Cross-host: config files don't travel between machines/harnesses — set host-local fallbacks via env, and keep a committed `*.example` template separate from the live file.
- Doc the schema alongside the code (`CONFIGURATION.md`/`MODELS.md`) and update it in the same PR as the knob.

**⑥ 최소 골격 (복붙 시작점)** —

````text
Pick ONE encoding.

A) DE-FACTO 2-BLOCK JSON (ruflo-style — clearest providers+models+roles):
```json
{
  "providers": {
    "openai":     { "apiKeyEnv": "OPENAI_API_KEY",     "secret": "openai-api-key" },
    "gemini":     { "apiKeyEnv": "GOOGLE_API_KEY",     "secret": "google-api-key" },
    "openrouter": { "apiKeyEnv": "OPENROUTER_API_KEY", "secret": "openrouter-api-key" }
  },
  "models": [
    { "name": "gpt-5.5",                      "provider": "openai",     "displayName": "GPT-5.5",      "supportsTools": true, "default": true },
    { "name": "gemini-2.5-flash",             "provider": "gemini",     "displayName": "Gemini Flash", "supportsTools": true },
    { "name": "anthropic/claude-sonnet-4.6",  "provider": "openrouter", "displayName": "Claude Sonnet","supportsTools": true }
  ],
  "roles": {
    "default":  "gpt-5.5",
    "reviewer": "gpt-5.5",
    "explorer": "gemini-2.5-flash",
    "spark":    "anthropic/claude-sonnet-4.6"
  }
}
```
Resolution (most-specific wins): roles[<role>] -> roles.default -> first model with "default": true.
Credentials: read providers[model.provider].apiKeyEnv from the environment; never inline the key.

B) CODEX-NATIVE TOML (spec-backed) — config.toml + per-role files:
```toml
#:schema https://developers.openai.com/codex/config-schema.json
model = "gpt-5.5"
model_provider = "openai"

[model_providers.openai]
base_url = "https://api.openai.com/v1"
env_key  = "OPENAI_API_KEY"
wire_api = "responses"

[model_providers.openrouter]
base_url = "https://openrouter.ai/api/v1"
env_key  = "OPENROUTER_API_KEY"
wire_api = "chat"

[profiles.strict]
model = "gpt-5.5"
sandbox_mode = "read-only"

[agents.reviewer]
description = "PR reviewer: correctness, security, missing tests."
config_file = "agents/reviewer.toml"
```
`.codex/agents/reviewer.toml`:
```toml
model = "gpt-5.5"
model_reasoning_effort = "high"
sandbox_mode = "read-only"
developer_instructions = """Review like an owner. Prioritize correctness, security, regressions, missing tests."""
```
````

**⑦ 변종·분기** —

Real divergences a builder must decide:
1. ENCODING: TOML (Codex-native, schema-validated, profile+per-role-file model — ECC, ruflo `.agents`) vs JSON (declarative catalog — ruflo app, oh-my-codex) vs Python module (catalog+resolver in code — last30days). TOML if you live inside Codex; JSON if config-driven; code if the catalog is small/static.
2. PROVIDER BINDING: explicit per-model `provider` field (ruflo config, last30days) vs name-pattern INFERENCE (ruflo MCP bridge: gemini-*/"/"/else). Explicit = safe & multi-key; inference = terser, fragile on new vendors.
3. ROLE GRANULARITY: single global `model` + profiles (ECC base) vs per-role files each with own `model`+`reasoning_effort` (ECC agents/) vs `agentModels{}`+`agentReasoning{}` maps (oh-my-codex) vs mode tiers `frontier|standard|spark` (oh-my-codex `models`/env). 
4. CONFIG vs CODE catalog: ruflo/oh-my-codex put the model list in data; last30days hardcodes constants (GEMINI_PRO, OPENAI_DEFAULT) + client classes in `providers.py` and only exposes selection via env/flags.
5. CREDENTIAL REF: env-var name (`env_key`, last30days `*_API_KEY`) vs secret-manager name (ruflo `secrets{}`).
6. SCOPE/PRECEDENCE: user `~/.codex` vs project `./.codex` vs `CODEX_HOME` override, arbitrated by a `setup-scope.json` (oh-my-codex); ECC documents "copy to ~/.codex for global, keep in repo for local."
7. WIRE API: Codex `wire_api = responses|chat`; last30days hardcodes distinct per-provider URLs (OpenAI Responses, XAI Responses, OpenRouter chat/completions, Gemini generateContent).

**증거(실증 fetch)** — `affaan-m/ECC:.codex/config.toml` · `affaan-m/ECC:.codex/agents/reviewer.toml` · `Yeachan-Heo/oh-my-codex:src/config/models.ts` · `Yeachan-Heo/oh-my-codex:docs/reference/omx-config-schema-routing.md` · `ruvnet/ruflo:.agents/config.toml` · `ruvnet/ruflo:ruflo/src/config/config.example.json` · `ruvnet/ruflo:ruflo/docs/MODELS.md` · `mvanhorn/last30days-skill:skills/last30days/scripts/lib/providers.py` · `mvanhorn/last30days-skill:CONFIGURATION.md`

---

## 13. Elicitation (capability via skills + commands)  ·  🟥 SPARSE

**① 공식 표준** — No official spec exists. Elicitation is a DE-FACTO capability: a Claude Code / Codex skill (SKILL.md) — sometimes thinly wrapped by a slash command — that runs a Socratic interview to drive a vague request to an execution-ready artifact. The only "mandated" layer is the host's skill contract (YAML frontmatter with `name` + `description`; optional `disable-model-invocation`, `argument-hint`). Everything ELSE — question flow, gating, output artifact — is convention that converges across the canonical repos. Four de-facto invariants observed in 4/4 repos: (1) ONE question at a time, never batch; (2) attach the model's own best-guess/recommended answer to each question; (3) a STOP/confidence gate that decides when interviewing ends; (4) emit a durable artifact (spec / one-pager / transcript) for downstream handoff and DO NOT implement in the same skill.

**② 포맷** — Markdown file named `SKILL.md` with YAML frontmatter, in a named skill directory. Two documented body styles: (a) plain Markdown prose with `##`/`###` sections (mattpocock, addyosmani); (b) pseudo-XML semantic tags — `<Purpose>`, `<Use_When>`, `<Do_Not_Use_When>`, `<Execution_Policy>`, `<Final_Checklist>` (Yeachan-Heo oh-my-codex/claudecode). A slash command (`.md` or `.toml` under `commands/`) is an OPTIONAL thin wrapper that just re-invokes the skill (grill-me = "Run a `/grilling` session"). Supporting files (frameworks.md, refinement-criteria.md, examples.md, scripts/*.sh) are optional progressive-disclosure siblings the body tells the model to read on demand.

**③ 위치** — Skill: `skills/<category>/<skill-name>/SKILL.md` (mattpocock uses category dirs: `skills/productivity/grill-me/`, `skills/engineering/grill-with-docs/`; addyosmani flat: `skills/idea-refine/`; Yeachan-Heo: `skills/deep-interview/SKILL.md` and plugin-scoped `plugins/oh-my-codex/skills/deep-interview/SKILL.md`). Optional slash-command wrapper: `commands/<name>.md` (Claude) or `commands/<name>.toml` / `.gemini/commands/<name>.toml` (Gemini, addyosmani ships both). Output artifacts written under repo-relative dirs: `docs/ideas/<slug>.md` (addyosmani), `.omx/specs/` + `.omx/interviews/` + `.omx/context/` (oh-my-codex), `.omc/specs/` (oh-my-claudecode).

**④ 스키마(키·필수/선택)** —

FRONTMATTER keys: `name` (required, string, kebab-case, == dir name); `description` (required — carries trigger phrases that make the skill model-invocable; rich descriptions enumerate WHEN/WHEN-NOT plus quoted triggers like "interview me","grill me","don't assume"); `disable-model-invocation` (optional bool — true on thin wrappers so only the user/command triggers them, mattpocock); `argument-hint` (optional, e.g. `"[--quick|--standard|--deep] <idea>"`, Yeachan-Heo); Yeachan-Heo-only orchestration keys: `pipeline: [..]`, `handoff-policy: approval-required`, `handoff: <path>`, `level: <int>`. BODY conventions (de-facto, recurring): Overview/Purpose; When-to-Use + When-NOT-to-Use (gating IN); Loading Constraints ("do not invoke in non-interactive contexts / CI / loop"); The Process (numbered phases); per-question Format block (`Q:` + `GUESS:`/`HYPOTHESIS:`+`CONFIDENCE:`); Stop Condition (confidence ~95% OR ambiguity-score <= threshold); Output artifact schema; Handoff/next-skill. The emitted SPEC artifact fields (addyosmani one-pager / SDD spec, convergent): Objective/Problem, Key Assumptions, Recommended Direction, MVP/Scope, Non-goals ("Not Doing"), Success Criteria, Open Questions; SDD adds Tech Stack, Commands, Project Structure, Code Style, Testing Strategy, Boundaries(Always/Ask-first/Never).

**⑤ 관례·주의** —

Naming: kebab-case dir == frontmatter `name`. The `description` is load-bearing — it is the ONLY thing the host model sees to auto-trigger, so it must pack trigger phrases + when-not. One-question-at-a-time is universal ("Asking multiple questions at once is bewildering" — grilling; "never batch multiple interview rounds" — deep-interview). Every question ships the model's recommended/guess answer ("For each question, provide your recommended answer" — grilling; `GUESS:` — interview-me). Prefer codebase exploration over asking when answerable ("If a question can be answered by exploring the codebase, explore the codebase instead"). Surface assumptions explicitly before proceeding (SDD `ASSUMPTIONS I'M MAKING:` block). Two STOP-gate styles: qualitative confidence (~95%, interview-me) vs quantitative ambiguity score with per-dimension weights + profile thresholds (deep-interview: Quick<=0.30/5 rounds, Standard<=0.20/12, Deep<=0.15/20; dimensions = Intent/Outcome/Scope/Constraint/Context Clarity; target the weakest dimension each round; max-rounds is a hard cap not a target; never hand off while Non-goals/Decision-Boundaries unresolved). Escalation rails: user "stop/just do it" -> persist state + write a pending-approval spec, DO NOT mutate. Progressive disclosure: keep SKILL.md lean, push rubrics/frameworks/examples to sibling .md read on demand. Hard rule across all repos: the elicitation skill NEVER implements — it ends by writing an artifact and offering handoff.

**⑥ 최소 골격 (복붙 시작점)** —

````text
Directory:
  skills/elicit-interview/SKILL.md
  commands/interview-me.md        # optional thin wrapper

--- skills/elicit-interview/SKILL.md ---
---
name: elicit-interview
description: One-question-at-a-time Socratic interview that drives a vague ask to an execution-ready spec. Use when a request is underspecified (missing who / why / success / constraint), or when the user says "interview me", "grill me", "don't assume", "stress-test this". Do NOT use for unambiguous fixes or in non-interactive contexts (CI, loops).
argument-hint: "<vague idea or plan>"
---

# Elicit Interview

## When to Use / NOT Use
USE: ask missing one of who / why / success / binding-constraint; user invokes a trigger phrase.
NOT: rename/typo/mechanical edit; user asked for speed over rigor; pure info question; non-interactive runtime (flag as blocker instead of guessing).

## Process
1. **Hypothesize.** Write your current read in ONE sentence + a confidence number.
   HYPOTHESIS: <one sentence>
   CONFIDENCE: ~30%  (below ~70%, append what's still missing)
2. **Explore first.** If a question is answerable from the codebase, read it — don't ask.
3. **Ask ONE question at a time, each with your guess. Wait for the reply before the next.**
   Q: <one focused question>
   GUESS: <your best answer + the reasoning behind it>
   - Target the weakest unresolved dimension: Intent / Outcome / Scope / Constraint / Context.
   - Pressure-test each answer (demand an example, expose an assumption, force a tradeoff) before moving on.
   - Re-state confidence after each answer.
4. **Stop** when confidence ~95% (or ambiguity <= threshold) AND Non-goals + Boundaries are resolved.
   If the user says "just do it", stop and write a pending-approval spec — do NOT implement.

## Output (write after user confirms)
Save to `docs/specs/<slug>.md`:
```markdown
# Spec: <name>
## Problem        <what & why; who the user is>
## Assumptions    <surfaced — correct now or I proceed>
## Direction      <recommended approach>
## Scope (MVP)    <in>
## Not Doing      <explicit non-goals>
## Success Criteria  <specific, testable>
## Open Questions <unresolved>
```

## Handoff
Offer the next step (plan / spec-driven build). This skill never writes code.

--- commands/interview-me.md ---
---
name: interview-me
description: Run an elicitation interview.
disable-model-invocation: true
---
Run the `elicit-interview` skill on $ARGUMENTS.
````

**⑦ 변종·분기** —

(1) GATING STYLE — qualitative confidence (interview-me ~95%; grilling "until shared understanding") vs QUANTITATIVE ambiguity scoring with weighted dimensions + numeric profile thresholds and max-round caps (Yeachan-Heo deep-interview: --quick/--standard/--deep). The math gate is the heavyweight fork. (2) WRAPPER PATTERN — mattpocock splits a thin trigger skill (grill-me, `disable-model-invocation:true`) from the reusable engine skill (grilling); others put everything in one SKILL.md. (3) BODY SYNTAX — plain Markdown (mattpocock/addyosmani) vs pseudo-XML tags + Final_Checklist (Yeachan-Heo). (4) OUTPUT SCOPE — lightweight one-pager `docs/ideas/<slug>.md` (idea-refine) vs full 6-section SDD spec (Tech Stack/Commands/Structure/Style/Testing/Boundaries) vs triple artifact context-snapshot + interview-transcript + spec under `.omx/` (deep-interview). (5) PHASING — divergent-then-convergent ideation (idea-refine: expand 5-8 variations, then cluster/stress-test) vs pure convergent clarification (interview-me / grilling / deep-interview). (6) COMPANION DOCS — grill-with-docs additionally emits ADRs + glossary via a domain-modeling skill; idea-refine ships frameworks.md/refinement-criteria.md siblings + an optional init shell script. (7) HOST PORTABILITY — addyosmani ships parallel `.claude` + `.gemini` + root command files (.md and .toml); Yeachan-Heo has parallel codex/claudecode editions with host-specific tool calls (`omx question` vs `AskUserQuestion`). (8) HANDOFF DECLARATION — implicit prose ("offer next step") vs explicit frontmatter `pipeline`/`handoff`/`handoff-policy: approval-required`.

**증거(실증 fetch)** — `mattpocock/skills:skills/productivity/grill-me/SKILL.md` · `mattpocock/skills:skills/productivity/grilling/SKILL.md` · `mattpocock/skills:skills/engineering/grill-with-docs/SKILL.md` · `addyosmani/agent-skills:skills/idea-refine/SKILL.md` · `addyosmani/agent-skills:skills/idea-refine/refinement-criteria.md` · `addyosmani/agent-skills:skills/interview-me/SKILL.md` · `addyosmani/agent-skills:skills/spec-driven-development/SKILL.md` · `Yeachan-Heo/oh-my-codex:skills/deep-interview/SKILL.md` · `Yeachan-Heo/oh-my-claudecode:skills/deep-interview/SKILL.md`

---

## 14. Enforced gates (capability via hooks + CI)  ·  🟥 SPARSE

**① 공식 표준** — No official spec for "enforced gates" as a named artifact — it is a CAPABILITY built on two officially-specced substrates. (1) Claude Code hooks: a PreToolUse hook that BLOCKS is mandated by the hooks contract — either exit code 2 (stderr is fed back to the agent as the block reason) or stdout JSON `{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"..."}}`. Exit 0 = allow/passthrough; any other non-zero = non-blocking error (logged, ignored). Cursor has a parallel `beforeShellExecution`/`beforeMCPExecution` event model. (2) GitHub Actions CI gates: de-facto — a job step that `exit 1` fails the check, and branch protection / required-checks makes it blocking. Cedar (protect-mcp variant) is an official AWS policy language; its `forbid` is authoritative over `permit`. De-facto vs spec: the exit-2 and deny-JSON semantics are spec-mandated by Claude Code; the WHAT-to-block policy (no-verify, write-scope, command allowlist) is entirely convention.

**② 포맷** — Two parts. (a) A hook MANIFEST — JSON (`hooks/hooks.json` or `.claude/settings.json` for Claude Code; `.cursor/hooks.json` for Cursor) mapping an event (PreToolUse/Stop/beforeShellExecution) + a `matcher` regex (tool name) to a `command`. (b) The GATE LOGIC — either an inline shell one-liner inside the manifest, OR an external executable script (`.sh`/`.js`/`.py`) the command shells out to, that reads the tool payload on stdin / env and emits a block via exit code or JSON. CI variant: a YAML workflow under `.github/workflows/` whose step `exit 1`s on violation.

**③ 위치** — Claude Code plugin: `hooks/hooks.json` at plugin root, with scripts under `hooks/` or `scripts/` (referenced via `${CLAUDE_PLUGIN_ROOT}`). Project-local: `.claude/settings.json` `hooks` key. Cursor: `.cursor/hooks.json` + `.cursor/hooks/*.js`. CI gates: `.github/workflows/*.yml`. Optional Cedar policy: `./protect.cedar` (path via `$PROTECT_MCP_POLICY`).

**④ 스키마(키·필수/선택)** —

hooks.json (Claude Code): `hooks` (required, obj) → event key e.g. `PreToolUse`/`PostToolUse`/`Stop`/`SessionStart` (array) → each entry: `matcher` (optional regex on tool name, e.g. `"Bash"`, `"Write|Edit|MultiEdit|Bash"`, `".*"`; omit = all) + `hooks` (required array) → `{type:"command" (required), command:(required string)}`. Cursor hooks.json: `version`(int) + `hooks`→eventName(array)→`{command,event,description}`. Block contract (the heart): exit `2` + stderr text = BLOCK (stderr = reason shown to agent); OR stdout JSON `hookSpecificOutput.{hookEventName(req), permissionDecision:"deny"(req for block), permissionDecisionReason(str)}`; exit `0` + passthrough JSON (NO permissionDecision key) = ALLOW/fall-through to normal permission flow — NEVER emit `"allow"` (that skips all other rules). Guard script internal decision dict: `{decision:"allow"|"deny", reason:str}`. Cedar policy: `permit(principal,action,resource) when {...}` / `forbid(...)` — forbid wins.

**⑤ 관례·주의** —

FAIL-SAFE DIRECTION is the central design axiom and it diverges by gate purpose: a SECURITY/scope guard fails CLOSED (deny on unexpected schema — "the guard cannot fail open"), while an OPTIONAL hardening layer fails OPEN (passthrough+exit 0 on any env/parse error, and stays SILENT on stderr because PreToolUse is a hot path and per-call stderr IS log-spam). Block reason strings must be ACTIONABLE (tell the agent what to do instead, e.g. "Run the commit without bypass flags"). Use `printf '%s'` not `echo` to read `$TOOL_INPUT` (echo mangles special chars). Matcher-scope narrowly (`Bash` only) so other tools aren't intercepted. For no-verify guards, do FLAG-POSITION-AWARE tokenization (skip `-m`/`-F` values) or you false-block commit messages containing the literal "--no-verify". Derive script paths from `$0`/`${CLAUDE_PLUGIN_ROOT}`, not cwd. Portability: prefer POSIX `sh`/Bash 3.2; a launcher that finds a "real" python (skipping Windows Store stub aliases) is the cross-host pattern. CI gates: provide an escape hatch (`[skip-defer-check]` in commit msg) and `set -euo pipefail`.

**⑥ 최소 골격 (복붙 시작점)** —

````text
DIR (Claude Code plugin):
  myplugin/
    hooks/
      hooks.json
      block.sh

# hooks/hooks.json — wire a blocking PreToolUse gate
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command",
            "command": "bash \"${CLAUDE_PLUGIN_ROOT}/hooks/block.sh\"" }
        ]
      }
    ]
  }
}

# --- VARIANT A: inline one-liner (no script needed) ---
# replace command above with:
#   "if printf '%s' \"$TOOL_INPUT\" | grep -qE '(^|&&|;|\\|)\\s*git\\s+.*--(no-verify|no-gpg-sign)'; then echo 'BLOCKED: --no-verify is not allowed; run without bypass flags so pre-commit hooks execute.' >&2; exit 2; fi"

# --- VARIANT B: external script, exit-2 block ---
# hooks/block.sh
#!/bin/sh
PAYLOAD=$(cat)                          # tool payload JSON on stdin
CMD=$(printf '%s' "$PAYLOAD" | python3 -c 'import sys,json;print(json.load(sys.stdin).get("tool_input",{}).get("command",""))' 2>/dev/null)
case "$CMD" in
  *"--no-verify"*|*"--no-gpg-sign"*)
    echo "BLOCKED: bypass flag not allowed. Re-run without it." >&2
    exit 2 ;;                            # exit 2 + stderr = BLOCK
esac
printf '%s\n' '{"hookSpecificOutput":{"hookEventName":"PreToolUse"}}'   # passthrough
exit 0

# --- VARIANT C: JSON deny (write-scope guard, fail CLOSED) ---
# emit on stdout instead of exit 2:
#   {"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"target escapes allowed write scope"}}
#   (allow = same object MINUS the permissionDecision key)

# --- VARIANT D: CI gate (.github/workflows/gate.yml) ---
name: Quality Gate
on: { pull_request: {}, push: { branches: [main] } }
permissions: { contents: read }
jobs:
  gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Enforce
        run: |
          set -euo pipefail
          if grep -rE '\-\-no-verify' .githooks 2>/dev/null; then
            echo "::error::bypass flag committed"; exit 1   # exit 1 = fail check
          fi
````

**⑦ 변종·분기** —

(1) BLOCK MECHANISM: exit-2+stderr (wshobson block-no-verify, ECC) vs stdout JSON `permissionDecision:deny` (academic write-scope guard). Both are spec-valid; JSON gives a cleaner reason channel + passthrough form. (2) POLICY LOCATION: inline shell one-liner in hooks.json (wshobson block-no-verify — zero deps) vs external script (ECC .js, academic .py) vs external DSL — Cedar policy file evaluated by `npx protect-mcp` (wshobson protect-mcp, with a paired PostToolUse `sign` for cryptographic receipts). (3) FAIL DIRECTION: fail-CLOSED for security/scope (academic guard denies on unknown schema) vs fail-OPEN for optional hardening (academic run_guard launcher passthrough+exit0+silent on any error). (4) WHAT IS BLOCKED: git bypass-flags (wshobson, ECC) / write-target outside scope + wholesale Bash-deny for fenced agents (academic) / arbitrary tool+command via Cedar permit-forbid (wshobson protect-mcp) / a release TAG when open `defer:<tag>` issues remain (academic CI). (5) HOST: Claude Code PreToolUse (academic, wshobson) vs Cursor beforeShellExecution wrapping the same core logic via an adapter (ECC — one engine, two surfaces) vs pure GitHub Actions CI. (6) LAUNCHER: direct `python3 script.py` vs a POSIX-sh launcher that probes for real Python first (academic #454 Windows-portability pattern).

**증거(실증 fetch)** — `wshobson/agents:plugins/protect-mcp/hooks/hooks.json` · `wshobson/agents:plugins/protect-mcp/test/fixtures/test-policy.cedar` · `wshobson/agents:plugins/block-no-verify/skills/block-no-verify-hook/SKILL.md` · `wshobson/agents:plugins/block-no-verify/.claude-plugin/plugin.json` · `affaan-m/ECC:.cursor/hooks/before-shell-execution-block-no-verify.js` · `affaan-m/ECC:.cursor/hooks.json` · `Imbad0202/academic-research-skills:hooks/hooks.json` · `Imbad0202/academic-research-skills:hooks/run_guard.sh` · `Imbad0202/academic-research-skills:scripts/ars_write_scope_guard.py` · `Imbad0202/academic-research-skills:.github/workflows/defer-label-gate.yml`

---

**시공 표준 한 줄:** **FLOOR 5칸은 공식 스펙이 존재**(그대로 따르면 됨) — `SKILL.md + .claude-plugin/{plugin,marketplace}.json + CLAUDE.md/AGENTS.md + .github/workflows`. **COMMON·SPARSE로 갈수록 공식 없는 de-facto 수렴 패턴** — 특히 `evals · model-binding · elicitation`은 공식 표준이 아직 안 굳은 영역(표준을 *세울* 수 있는 자리).

---

# PART V — 우리 하네스 설계 (주관: 무엇을·어떻게 빌드하나)

> 여기부터는 **"우리가 빌드하는 것"의 설계.** 위 PART 0–IV(객관: 기준·개념·책장·시공)를 *토대*로, 맨땅 greenfield 원칙(brick-by-brick; 기존 하네스/OSS는 *이 단계에서* 참고·차용으로만)으로 도출. (2026-06-21 통합.)

## V.0 대전제 (북극성)

**비엔지니어도 AI Agent를 이용해 프로덕션급(시니어 개발자가 와도 "와 잘 만들었네요") 소프트웨어를 개발할 수 있게, 모델을 *이끌어주는* 하네스.**

핵심 통찰: **"와 잘 만들었네"는 "돌아간다"가 아니다.** 바이브코딩한 비엔지니어도 *돌아가는* 건 만든다. 시니어의 "와"는 그 위의 **craft + 운영가능성 + 제대로 된 과정의 흔적**이 *약한 고리 없이* 갖춰질 때 나온다. 비엔지니어는 이걸 *요청할 줄 모른다(뭘 모르는지 모름)* → **그 빈틈을 모델이 알아서 채우도록 이끄는 게 하네스의 일.**

## V.1 프로덕션급 기준점 (LOCKED v2 ✅ — PART 0 표준 대조 반영)

**🔑 No-weak-link:** 프로덕션급 = 모든 차원이 *균일하게* 높음. **채점은 평균이 아니라 최저 차원(min, not avg)** — 한 군데라도 구멍이면 프로덕션급 아님. (PART 0 0.8에서 이게 *표준에서 관측되는* 의미론임을 확인.)

#### 🧱 레이어 1 — 보편 코어 (10차원, 모든 SW FLOOR)
| 차원 | 충족 조건 |
|---|---|
| **정합성** | 스펙 충족 · 엣지까지 올바른 출력 · clone→한 번에 실행(재현성) |
| **견고성** 🆕 | 결함/예외/잘못된 입력/동시성에도 안 무너짐 · 우아한 실패·복구 *(서비스 등급 availability·redundancy·graceful-shutdown은 L2)* |
| **Craft** | 가독성·그 언어다움 · 건전한 추상화/모듈화 · 낮은 복잡도·죽은코드 0 |
| **테스트** | 의미 있는 테스트(행동 검증, 커버리지≠목표) · green CI |
| **설계 근거** | 왜 이렇게 지었나 = ADR · 명확한 데이터모델/계약 |
| **보안** | 입력 검증 · 시크릿 0 · 의존성 위생(+공급망) · 안전한 기본값 |
| **성능 위생** 🆕 | 명백한 낭비 0 · 합리적 자원 · 핫패스 O(n²) 회피 *(부하/스케일/CWV 목표치는 L2)* |
| **진단성** 🆕 | 좋은 에러메시지 · 구조화 로그 · 디버그 가능 *(full 관측성=telemetry/tracing/health는 L2)* |
| **문서** | README · 아키텍처 · 기여/온보딩 (개발자문서 vs 사용자문서 구분) |
| **출하 위생** | 깔끔한 커밋/PR · CI/CD 게이트 · dep 핀+lockfile · semver · changelog · LICENSE/SECURITY/.gitignore |

> 🆕 3개(견고성·성능위생·진단성) = PART 0 표준 대조로 추가/승격된 *보편 커널*. 각 커널의 **서비스/아키타입 등급 확장**은 아래 L2가 받는다. v1(7) → **v2(10)**.

#### 🏗️ 레이어 2 — 아키타입별 추가 (해당 종류에만) → 기능·매핑은 V.6
| 아키타입 | 추가로 충족해야 할 것 |
|---|---|
| **http-api / 백엔드** | 관측성(헬스·메트릭·구조화로그·트레이싱) · 신뢰성(timeout·retry·rate-limit·graceful shutdown) · 12-Factor · API 계약(OpenAPI·버저닝) · authn/authz · DB 마이그레이션 · 부하/성능 |
| **web-app / 프론트** | 접근성(a11y) · 성능(번들·CWV·lazy) · 반응형·브라우저 호환 · XSS/CSRF·CSP · 에러 바운더리 · (해당시 SEO) |
| **cli** | 종료코드 규약 · stdout/stderr 분리·파이프/비대화형 · `--help`/man · 인자 검증 · 설정 우선순위(flag>env>file) · 크로스플랫폼 |
| **library / package** | 공개 API 안정성·semver 엄수 · 의존성 최소 · 타입 정의 · API 문서(docstring) · 호환 매트릭스 · 예제 · deprecation 정책 · *(관측성·헬스 불필요)* |
| **AI/LLM** 🆕(0/표준 갭) | 프롬프트 인젝션 방어 · 환각/사실성 · 비결정성(회귀 허용오차·seed) · 출력 스키마 준수 · 프롬프트 버저닝 · 토큰/비용 예산 · jailbreak/세이프티 |

> 표준 앵커: ISO/IEC 25010 · 12-Factor · Google SRE · DORA · OWASP (상세 = PART 0).

### V.1.5 표준 대조 감사기록 (PART 0 ↔ 루브릭)
구조는 검증됨(2레이어 = 표준 수렴 / weakest-link = 표준 관측 의미론). 보편 코어 보강 3개 = **R1 견고성**(정합성에서 복원력 분리; ISO가 Functional Suitability↔Reliability 별개 최상위) · **R2 성능위생**(ISO Performance Efficiency 보편 floor; 부하/스케일은 L2) · **R3 진단성**(CLI·library도 진단 필요; full 관측성은 L2 — library "관측성 불필요"는 표준이 *확증*). **의도적 델타:** 설계근거(ADR)를 L1 승격(표준엔 보편 floor 아님; "시니어 와" 청중 위해) · CLI·library 행이 표준보다 촘촘(PART 0 0.7 빈영역 선점). **별도 결정 대기:** AI/LLM 아키타입(아래 V.6에서 신설) · Safety/Cost 아키타입(의도적 v1 OOS).

## V.2 기준점 → 하네스 *기능* 도출 → 5개 family

§V.1 각 차원을 모델이 *실제로 충족하게* 하려면 하네스가 *해야* 하는 것을 뽑으면 **5개 메커니즘 family**로 수렴:

| v2 차원 | 하네스가 해야 하는 것 | 메커니즘 |
|---|---|---|
| **정합성** | 빌드 전 모호함 제거(Socratic) · 스펙→수용기준 테스트 · **스펙↔구현 eval**(moat) · clone→1커맨드 스캐폴드 | Elicit·Scaffold·**Eval** |
| **견고성** | 엣지/실패 케이스 테스트 강제 · 에러경로 누락 리뷰 차단 | Gate·Orchestrate |
| **Craft** | lint/복잡도 게이트(cyclomatic≤10·중복<5%) · 리뷰어 Design/Complexity/Naming | Gate·Orchestrate |
| **테스트** | TDD/테스트-존재 게이트 · green-CI 머지 게이트 | Gate |
| **설계근거** | docs/adr/ 스캐폴드 · 결정 시 ADR 유도 · 스펙이 결정+기각대안 포착 | Scaffold·Elicit |
| **보안** | secret-leak 차단 · CVE스캔+SBOM · 입력검증 리뷰 · secure-by-default | Gate·Scaffold |
| **성능위생** | 핫패스 이슈 리뷰 플래그 · (서비스) 부하테스트 레일 | Gate·Orchestrate |
| **진단성** | 에러메시지·구조화 로그 리뷰 요구 · 로깅 스캐폴드 | Gate·Scaffold |
| **문서** | README/아키/기여 스캐폴드 · 헌법 유지 · 문서갱신 게이트 | Scaffold·Gate |
| **출하위생** | CI/CD+conventional-commits+PR/issue 템플릿+semver/changelog · 커밋/PR 게이트 | Scaffold·Gate |
| **no-weak-link**(메타) | 차원별 축 게이트 + 최저차원 채점 eval | **Eval** |

**5 family:** ①**Elicit**(모호→명확 스펙) ②**Scaffold**(표준 템플릿으로 context+env+rails 대신 셋업) ③**Orchestrate**(lead가 task를 적절 에이전트 병렬 위임, planner-worker-judge) ④**Gate**(hook/CI로 통과 못 하면 못 나가게) ⑤**Eval**(스펙↔구현+프로덕션준비도 최저차원 채점) ← **업계 0/표준 빈칸 = moat.**
> 1·2 = 시작점(빌드 전), 3 = 실행, 4·5 = 출구 강제·측정. 사용자 제시 기능은 1·2·3에 몰려 있고 — **4(Gate)·5(Eval)는 사용자 미제시·루브릭 필수 보강.**

## V.3 기능 — 명료화 · 적합성 · 보강 (리서치 근거)

> 범례 — 적합성: ✅/🟡범위조정/🔴재고. 빌드: 🟦의존성(최우위 존재)/🟩brick(없음, 내 소스)/🟨아이디어추출+경량화(아쉬움)/🟪호스트-네이티브 재사용(CC/Codex 이미 제공).

**F1 · 설정+마일스톤 GUI** ✅ 🟩+🟦 — CLI 설정을 GUI로도(one-and-only 아님) + repo별 "어디까지/뭐 남았나" 시각화. *근거:* 터미널 도구는 GUI 안 싣고 커뮤니티가 만듦; 지배 패턴 = **로컬 웹 대시보드 = on-disk 상태 thin-viewer**(CloudCLI 12k★); 마일스톤 = 칸반+진척바(vibe-kanban 27k★, 일몰 → 빈자리); 설정 SSOT = CLI의 같은 config를 GUI가 읽기/쓰기(JSON Schema→폼); 별도-상태 앱 = divergence 1순위 실패. ⚠️ **표준 책장 14칸 밖 = 신규 15번째 선반(컨트롤플레인).**

**F2 · 비엔지니어 프로젝트 셋업 시작점** ✅ 🟨+🟦 — 표준 템플릿 내장 → 시작/이어붙일 때마다 context·env·workflow를 모델이 대신 셋업(공통 뼈대+프로젝트별 세부). = blueprint 영역. *근거:* **THE 빈칸** — Kiro/Spec Kit(114k★)/BMAD(49k★)/Tessl 전부 *엔지니어 전제*; "비엔지니어 모델-run 인터뷰 + context문서 AND workflow레일 둘 다 프로젝트별로 채움"을 아무도 안 함(Fowler/Böckeler 갭). 내용 = GitHub Community Standards·Conventional Commits·OpenSSF; 메커니즘 = **copier**(`copier update`로 드리프트 해결).

**F2a · Socratic 스펙 명료화** ✅ 🟨 — 입맛대로 바로 실행 X, 명확해질 때까지 토의 후 빌드. *근거:* "spec = prompt-eng + context-eng" **정확**(Karpathy; arXiv "super-prompt"; 정제 스펙 에러 ~50%↓, 근거 thin). **Ouroboros = 가장 엄밀**(모호도=1−Σ(명확도×가중치), 게이트≤0.20, 유사도≥0.95 루프) → 객관 게이트 차용.

**F2b · 멀티에이전트 오케스트레이션** ✅ 🟪 호스트 재사용 — 세션 연 곳=lead, task는 적절 에이전트 병렬. *근거:* dispatch = **CC 네이티브 `Agent` primitive (MCP/skill 아님)**; Anthropic orchestrator-worker(lead+3~5, 별도 컨텍스트, ~15×토큰 naive/2~5× typed-artifact); `/workflows`는 10+/반복 스케일용 = 안 겹침; 세마포어 = 표준(claudeck 보유); 분할 = DAG·read병렬/write직렬·planner-worker-judge(+7.2pt). → **claudeck executing-plans·semaphore·worktree가 이미 최우위 = 재빌드 X.**

**F2b-viz · 토폴로지 GUI** 🟡(F1 패널) 🟦+🟨 — **React Flow DAG**가 승자(LangGraph Studio·MS Conductor); agent-office는 Phaser.js 데모 = 아이디어만(공간 메타포·이벤트 피드).

**보강(미제시·필수):** **A1 Gate** 🔴 🟪+🟩 — hook/CI 차단(규칙 준수율 ~70% → 하드 제약은 hook 필요); 호스트 hook + claudeck 기존 게이트 재사용. **A2 Spec-compliance EVAL** 🔴 🟩 — 최저차원 채점; 업계 0/표준 빈칸 = moat 직접 빌드. **A3 모델-바인딩** 🟡 🟩 ([[claudeck-agent-model-decoupling]]).
**nice-to-have:** N1 번다운(GUI) · N2 context 자동 갱신 · N3 크로스-세션 메모리(🟪 호스트).

## V.4 동작 모델 — unit/block (당신 직관의 정식화)

**3겹 중첩 unit + 횡단 block 파이프라인:**

```
┌─ PROJECT unit (영속 · 다세션 횡단) ── repo에 삶 · 천천히 진화 ──────┐
│  context(헌법·docs·spec) · 마일스톤 · env · rails                    │
│  = "뭘 만들지 + 표준" — 모든 세션이 읽음. blueprint로 1회 셋업.        │
│  ┌─ SESSION unit (1 작업세션 · 휘발) ── lead orchestrator ────────┐ │
│  │  project-context 읽음 → goal을 파이프라인 통과 → 산출물 write    │ │
│  │  ┌─ TASK unit (세션 내 · 일회용) ── 병렬 subagent ───────────┐ │ │
│  │  │  파일격리 worktree · typed-artifact 반환 · 끝나면 폐기      │ │ │
│  │  └─────────────────────────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
횡단 BLOCK(tier별 조립/생략): [Elicit]→[Scaffold]→[Plan]→[Orchestrate]→[Gate]→[Eval]  (= V.2의 5 family)
```

- **유기적 동작:** Project 상태는 세션 가로질러 *축적*(마일스톤·ADR·spec — "길 잃음" 해소 / GUI가 봄) · Session 상태는 휘발이나 project로 *write-back*(커밋·마일스톤·ADR) · Task 상태는 폐기(worktree, typed-artifact만 올림).
- *리서치 정합:* 별도 컨텍스트창=unit별(Anthropic) · 영속 context문서=project층(Spec Kit constitution/CLAUDE.md) · lead=session · 파일격리 subagent=task.
- **block = tier별 조립**(claudeck Tier 0/1/2/3가 이미 이 형태): 사소한 수정=[Gate]만 / 새 기능=[Elicit→…→Eval] 전체. **GUI는 3 unit 각각 시각화**(Project→마일스톤 · Session→토폴로지 · Task→agent 노드).

## V.5 기능 family → 책장 매핑 (빌드/차용 결정)

> 책장 14칸(PART IV) + **신규 15번째(GUI/컨트롤플레인)**. 범례 = V.3.

| family | 책장 칸 | 결정 | 무엇을·왜 |
|---|---|---|---|
| **Elicit** | #13 Elicitation + spec/blueprint | 🟨+🟩 | 우리 spec/blueprint brick + Ouroboros 객관-모호도-게이트 차용 |
| **Scaffold** | #10 Templates · #4 Constitution · #5 CI | 🟨+🟦 | 내용=업계표준 · 메커니즘=copier 의존성 · blueprint가 조립 |
| **Orchestrate** | #8 Agents (+호스트 /workflows) | 🟪 | CC subagents+/workflows+claudeck semaphore·executing-plans·worktree 재사용. 재빌드 X |
| **Gate** | #7 Hooks · #14 Enforced-gates · #5 CI | 🟪+🟩 | 호스트 hook + claudeck 기존 게이트 재사용 |
| **Eval** ⭐ | #9 Evals harness | 🟩 | brick = 최우선. 스펙↔구현+준비도 최저차원 채점 = 0/표준 빈칸 = moat |
| **모델-바인딩** | #12 Model-binding | 🟩 | agent=역할·모델=사용자소유 |
| **GUI/컨트롤플레인** ⭐ | **#15 신규 선반** | 🟩+🟦 | brick(웹 대시보드 thin-viewer) + 의존성(React Flow·JSON-Schema폼); vibe-kanban/CloudCLI 차용, agent-office 아이디어만 |

**빌드 우선순위:** 🟪 거의 공짜(재사용) = Orchestrate·Gate절반 · 🟨 아이디어+경량화 = Scaffold·Elicit · 🟩 **진짜 차별화 빌드 = ① Eval(moat) ② GUI(15선반) ③ blueprint 완성** · 🟦 의존성 = copier·React Flow·JSON-Schema폼.

## V.6 Layer-2 아키타입별 기능 + 책장 매핑 〔신규〕

**핵심 발견 — Layer-2는 새 선반을 만들지 않는다.** 아키타입 요구는 *새 family가 아니라* 같은 5 family/기존 책장에 **아키타입별 *내용*을 주입**한다: **#13 Elicitation이 아키타입을 *감지* → #10 Templates가 아키타입 레일 스캐폴드 → #8 Agents가 아키타입 리뷰어 → #5 CI/#7 Hooks가 아키타입 게이트 → #9 Evals가 아키타입 준비도 채점.** (예외: GUI만 #15 신규 선반이었음.)

```
[Elicit #13: 아키타입 감지] → [Scaffold #10: 레일] → [Orchestrate #8: 리뷰어] → [Gate #5/#7: 검사] → [Eval #9: 준비도]
                                          └────── 전부 *아키타입별 내용*으로 파라미터화 ──────┘
```

아키타입별 요구 → 하네스 기능(명명된 업계표준 도구) → family/책장:

**🌐 http-api / 백엔드**
| 요구 | 하네스 기능(표준 도구) | family·책장 |
|---|---|---|
| 관측성 | health endpoint + OpenTelemetry + 구조화 로거 스캐폴드 | Scaffold #10 / Eval #9 |
| 신뢰성 | timeout·retry·rate-limit·graceful-shutdown 미들웨어 + fault test | Scaffold #10 / Gate #5 |
| 12-Factor | env-config + Dockerfile 스캐폴드 + config-in-env 린트 | Scaffold #10 / Gate #7 |
| API 계약 | OpenAPI 스펙+codegen + contract test(schemathesis/Pact) + breaking-change 탐지 | Scaffold #10 / Gate #5 / Eval #9 |
| authn/authz | auth 미들웨어 스캐폴드 + authz 리뷰어 | Scaffold #10 / Agents #8 |
| DB 마이그레이션 | 마이그레이션 도구(Prisma/Alembic/Flyway) + applies-test | Scaffold #10 / Gate #5 |
| 부하/성능 | k6/Locust 부하테스트 CI + perf 예산 | Gate #5 / Eval #9 |

**🖥️ web-app / 프론트**
| 요구 | 하네스 기능 | family·책장 |
|---|---|---|
| a11y | eslint-plugin-jsx-a11y 스캐폴드 + axe-core/Pa11y CI + a11y 점수 | Scaffold #10 / Gate #5 / Eval #9 |
| 성능(CWV) | Lighthouse CI 예산 + CWV eval | Gate #5 / Eval #9 |
| 반응형·호환 | Playwright 크로스브라우저 CI | Gate #5 |
| XSS/CSRF·CSP | CSP 헤더+sanitizer 스캐폴드 + 보안 리뷰어 | Scaffold #10 / Agents #8 |
| error boundary | 에러바운더리 컴포넌트 스캐폴드 | Scaffold #10 |
| SEO | meta/sitemap 스캐폴드 + Lighthouse SEO | Scaffold #10 / Gate #5 |

**⌨️ cli**
| 요구 | 하네스 기능 | family·책장 |
|---|---|---|
| 종료코드 규약 | exit-code 맵 스캐폴드 + exit-code 테스트 | Scaffold #10 / Gate #5 |
| stdout/stderr·파이프 | 출력 관례 스캐폴드 + 비대화형 테스트 | Scaffold #10 / Gate #5 |
| --help/인자검증 | arg-parser(clap/argparse/commander) + --help 스냅샷 테스트 | Scaffold #10 / Gate #5 |
| 설정 우선순위 | flag>env>file 로더 스캐폴드 | Scaffold #10 |
| 크로스플랫폼 | CI 매트릭스(Linux/macOS/Windows) | Gate #5 |

**📦 library / package**
| 요구 | 하네스 기능 | family·책장 |
|---|---|---|
| 공개 API 안정성·semver | API breaking-change 탐지(api-extractor/cargo-semver-checks) + semantic-release | Gate #5 / Eval #9 |
| 의존성 최소 | dep-count/번들사이즈 예산 | Gate #5 |
| 타입 정의 | 선언파일/타입스텁 스캐폴드 + type-coverage | Scaffold #10 / Gate #5 |
| API 문서 | typedoc/sphinx 스캐폴드 + doc-coverage | Scaffold #10 / Gate #5 |
| 호환 매트릭스 | CI 매트릭스(다버전/다런타임) | Gate #5 |
| 예제·deprecation | examples/ 스캐폴드 + examples-run 테스트 · deprecation 관례 | Scaffold #10 / Gate #5 |

**🤖 AI/LLM 🆕 (0/표준 갭 — 우리가 *표준을 세울* 자리)**
| 요구 | 하네스 기능 | family·책장 |
|---|---|---|
| 프롬프트 인젝션 | injection-test 스위트 + 입력 가드 스캐폴드 | Gate #7 / Scaffold #10 |
| 환각/사실성 | groundedness/factuality eval | **Eval #9** |
| 비결정성 | 허용오차 회귀 eval + seed 핀 + eval-gate | **Eval #9** / Gate #5 |
| 출력 스키마 준수 | structured-output 검증 hook | Gate #7 |
| 프롬프트 버저닝 | 프롬프트 버전관리 스캐폴드 | Scaffold #10 |
| 토큰/비용 예산 | 토큰-예산 캡(세마포어 인접) | Gate #7 / Eval #9 |
| jailbreak/세이프티 | red-team eval | **Eval #9** |

> **AI/LLM은 #9 Evals에 가장 무겁게 쏠림 = 정확히 우리 moat 빌드와 일치.** 이 아키타입은 *어느 표준도 안 다룸*(PART 0 0.7) → claudeck이 선점·표준화 가능. **단, Safety-critical·Cost/지속가능성 아키타입은 의도적 v1 OOS**(비엔지니어 앱 범위 밖).

### V.6.1 Layer-2가 어느 책장에 쌓이나 (집계)
- **#10 Templates** ← 아키타입 레일 스캐폴드의 *주된 적재처*(전 아키타입). **copier 아키타입 팩**으로 구현(공통 뼈대 + 아키타입별 분기).
- **#5 CI** ← 아키타입 게이트의 주된 적재처(contract/load/a11y/Lighthouse/cross-platform/semver/compat-matrix).
- **#9 Evals** ← http-api 준비도 + library semver + **AI/LLM 전반**(moat 집중).
- **#7 Hooks** ← 인라인 게이트(config-in-env·structured-output·token-budget·injection).
- **#8 Agents** ← 아키타입 리뷰어(authz·보안·a11y).
- **#13 Elicitation** ← *아키타입 감지*(blueprint 인터뷰가 아키타입을 정해 위 전부를 파라미터화).
→ **결론: Layer-2 빌드 = 새 선반 0개. 기존 #5/#7/#8/#9/#10에 *아키타입 콘텐츠 팩*을 추가 + #13이 감지.** (GUI #15만 유일한 신규 선반.)

---

# PART VI — 책장 v2 (OSS 하네스 전수조사 검증) 〔2026-06-21 신규〕

> 뼈대를 실제로 *짓기 전에*, "어떤 컴포넌트가 *있어야 하는가*"를 OSS 하네스 50+개로 다시 딥 검증.
> 누적 80+ repo(PART III 27 census + PART IV 14 시공표준 + 본 3-렌즈 sweep). **결론: 콘텐츠 14칸은 견고,
> 그러나 *운영(ops) 절반*을 우리가 안 지었고 Codex 어댑터가 구버전이었다 → 둘 다 보강.** 컴포넌트 타입이
> 수렴 → **조사 종료, 빌드 시작.** 책장은 확장 가능 = 향후 발견은 증분 추가지 재설계 아님.

## VI.1 컴포넌트 taxonomy 검증 (채택률 실측)

3-렌즈 sweep(taxonomy 50+repo · cross-host · lifecycle). 캐논: oh-my-claudecode 36.7k★ · oh-my-codex 31k★ · BMAD 49k★ · ECC · ruflo · Anthropic plugin spec.

- **FLOOR(≥70%):** Constitution · Skills(SKILL.md) · commands/prompts · hooks · agents · plugin.json · MCP · CI · **CHANGELOG** · templates.
- **COMMON(40–70%):** marketplace.json · **output-styles/personas** · **benchmark(≠eval)** · evals · **statusline/HUD** · **persistent memory** · examples · **doctor** · i18n docs · **release protocol** · security policy · **install/uninstall** · LSP config · monitor.
- **RARE(<40%):** elicitation · enforced-gates · skills-lock · **GUI** · telemetry · sandbox/permissions · dep-pinning · **model-binding** · themes · channels · SBOM/signing · coverage-tracking · RAG.

**우리 15칸에 *없던* 빈칸(강한 증거):** statusline/HUD(claude-hud 18k★) · persistent-memory(agentmemory·Hermes) · doctor(6+repo 수렴) · benchmark · output-styles(plugin.json 1급 필드) · install/update/uninstall lifecycle · release protocol.
**Anthropic plugin.json 1급 필드 9개:** skills·commands·agents·hooks·mcpServers·**outputStyles·lspServers·monitors·themes** — 뒤 4개를 놓치고 있었음. **elicitation·enforced-gates는 *1급 필드 아님* → 독립 셸프가 아니라 능력(skills+hooks)** = 우리 분류가 옳았음을 확인.

## VI.2 크로스호스트 아키텍처 (핵심 발견 — 우리 구조가 더 원칙적)

- **업계 지배 패턴 = sibling repos**(omc/omx 별도 repo, skill 중복·발산). BMAD만 단일repo 멀티호스트지만 어댑터가 1~2파일 ad-hoc. → **우리의 공유 core + per-host adapter 분리가 더 원칙적**(양 호스트 도그푸드를 한 소스에서 → 정당화).
- **SKILL.md = 진짜 크로스호스트 네이티브**(agentskills.io, 32+ 채택). discovery 경로만 호스트별; 호스트 전용 프리미티브 쓰는 skill은 `compatibility` frontmatter로 신고.
- **Codex 어댑터 3대 정정:** ① `prompts/`는 *레거시* → plugin-mode skill discovery(`.codex-plugin/`). ② `config.toml`은 *외과적 머지*(`config-fragments/*.toml`), 템플릿 통째 덮어쓰기 금지. ③ Codex hooks = **7-event**(SubagentStart/Stop·SessionEnd·PostToolUseFailure **없음**) → **차단게이트 CC=강제·Codex=best-effort** = parity 갭. `host-probe`로 명시적 degrade.

## VI.3 lifecycle/ops (성숙 하네스가 다 갖춘 운영 절반)

- **install → update → migrate → doctor → uninstall** 전 단계 표준화(omx가 레퍼런스: setup/update/uninstall/doctor.ts).
- **다운스트림 프로젝트 드리프트 = copier** `copier update`: `.copier-answers.yml`의 `_commit`(템플릿 git-tag) 기준 3-way 머지(old출력 vs 현재 = 사용자델타 → new출력+델타). **템플릿 git-tag 없으면 update 깨짐.**
- **하네스 자기 릴리스 = Changesets**(AI 커밋엔 semantic-release보다 적합 — 의도를 PR별 md로 명시).
- **자유 OTEL**(`CLAUDE_CODE_ENABLE_TELEMETRY=1`) — 빌드 불필요, doctor가 체크만.

## VI.4 책장 v2 (최종)

| 구분 | 항목 |
|---|---|
| **콘텐츠 14칸 + #15** | 유지 (견고) |
| **운영 셸프 추가** | doctor · update · uninstall · migrate · **host-probe** · **memory** · output-styles · benchmark · release-automation(.changeset) · copier-drift 규율 |
| **능력(셸프 아님)** | elicitation(#13) · enforced-gates(#14) = skills+hooks로 실현 |
| **전략적 유지(RARE지만 차별화)** | model-binding(#12) · evals(#9) · GUI(#15) |
| **Tier-3 로드맵(미빌드, 경량)** | skills-lock · sandbox/permissions · OTEL 배선 · LSP/monitor/themes · statusline 통합 · SBOM/provenance · i18n |

## VI.5 → Gingoa로 실체화

이 검증을 반영해 하네스를 **이름 확정(`Gingoa` = 손오공 긴고아 = 궤도에 묶는 머리테)** + **제로베이스 크로스호스트 뼈대**로 `/Users/coolbress/gingoa`에 생성(영어 전용). 공유 core(`skills·templates·evals·config·memory`) + `adapters/{claude-code,codex}` + 설치 CLI(`bin·src`, lifecycle). 전 컴포넌트 결정표(증거 포함)는 repo의 **`docs/COMPONENTS.md`**. 상세는 메모리 [[gingoa-harness-build]].

---

### 출처
- 하네스/스캐폴드 정의·계보: HuggingFace Agent Glossary, METR, Anthropic engineering
- "하네스가 모델만큼 중요": Harness-Bench(arxiv 2605.27922), Cursor 연구, METR
- 12요소·context engineering: arxiv 2604.08224, Anthropic "Effective Context Engineering"
- 플러그인 5대 컴포넌트: Claude Code Plugin Marketplaces 공식 문서
- Skills 오픈 표준: agentskills.io (Anthropic 2025-12), GuildSkills 크로스-에이전트 레지스트리
- Hermes Agent(학습루프·메모리): Nous Research 문서
- **PART III 책장(채택률·UX·moat):** GitHub 스타순 census(455 repo → top-120 → Category C 27개), 각 repo 실제 git tree+README 직접 조사
- **PART IV 시공 표준(14칸 도면):** 공식 스펙 + Category C 중 캐논 3~4개 실제 파일 직접 fetch (14 에이전트, 458k 토큰)
- **PART V 설계(주관) 근거 — 3렌즈 전수조사:** ① 멀티에이전트 오케스트레이션(Claude Code subagents/`/workflows`/Agent SDK·Anthropic orchestrator-worker·LangGraph/CrewAI/AutoGen/Symphony·세마포어 표준·DAG/planner-worker-judge) ② CLI-하네스 GUI(opencodex·agent-office·CloudCLI 12k★·vibe-kanban 27k★·Tauri v2·React Flow·JSON-Schema 폼) ③ inception/templates(Ouroboros·Kiro/Spec Kit 114k★/BMAD 49k★/Tessl·GitHub Community Standards·Conventional Commits·OpenSSF Scorecard·cookiecutter 24k★/copier)
- **PART VI 책장 v2 검증 — 3-렌즈 OSS sweep(50+ repo):** ① 컴포넌트 taxonomy(oh-my-claudecode 36.7k★·oh-my-codex 31k★·BMAD 49k★·ECC·ruflo·jarrodwatts/claude-hud 18k★ 등 실제 git tree fetch + Anthropic plugin spec) ② 크로스호스트 아키텍처(sibling-repo vs core+adapter·SKILL.md 개방표준·Codex plugin-mode/config.toml 머지/hook parity) ③ lifecycle/ops(omx setup/update/uninstall/doctor.ts·copier `copier update` 드리프트·Changesets vs semantic-release·OTEL)
- ※ 원본 census(.md/.json)·standalone bookshelf·construction-standard·standalone 표준조사·**harness-vision.md**는 이 파일로 통합 후 삭제 (2026-06-21)
