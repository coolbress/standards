---
id: framework-crosswalk-2026
title: "SWEBOK V4.0a × ISO/IEC/IEEE 12207:2026 × ISO/IEC 25010:2023 × goppi 28-Aspects"
kind: reference
status: review-needed
last_updated: "2026-08-02"
evidence_track: lit
freshness: versioned
review_due: "2027-02-02"
sources: [SWEBOK-4.0A, ISO-12207-2026, ISO-25010-2023]
---

# Framework Crosswalk 2026

## 판독 범위와 한계

- **SWEBOK V4.0a:** IEEE Computer Society가 2025-09 공개한 공식 guide의 18 Knowledge Areas를
  직접 사용했다.
- **ISO/IEC/IEEE 12207:2026:** 공식 catalog에서 edition 2, 2026-04 발행, software life-cycle
  process의 공통 framework라는 범위와 2017판 withdrawn만 확정했다. 전체 조항은 라이선스 본문이라
  아래 activity 대응은 **개념 수준 synthesis**이며 clause conformance 표가 아니다.
- **ISO/IEC 25010:2023:** 공식 catalog가 product quality model의 9 characteristics와 요구·시험·수용·
  측정 용도를 확인한다. 세부 subcharacteristic/clause 대응은 이 자료로 검증하지 않았다.
- 따라서 이 문서는 빠진 범위와 중복을 찾는 navigation crosswalk다. ISO 준수 선언에 사용하면 안 된다.

표기: `D` 직접 지식영역/품질 주제 · `P` 부분/간접 · `U` 공식 공개 범위만으로 확인 불가 ·
`G` goppi 고유 확장. 괄호 안 12207 activity 이름은 개념상 대응이며 조항 인용이 아니다.

## 28-aspect crosswalk

| # · goppi aspect | SWEBOK V4.0a | ISO 12207:2026 public-scope synthesis | ISO 25010:2023 quality synthesis | 판정 |
|---|---|---|---|---|
| 01 Requirements & Planning | D Requirements | D/P stakeholder & requirements definition | P quality requirements/acceptance use | 충분; 사용자 capability 별도 축 필요 |
| 02 Architecture & Design | D Architecture, Design | D/P system/software definition | P nine qualities drive tradeoffs | 충분 |
| 03 Dev Environment | D Construction; P CM/Operations | P enabling implementation environment | P maintainability/reliability indirect | goppi operational detail |
| 04 Build & CI | D Construction, Testing, Operations, Process | P implementation/verification support | P repeatable quality evaluation | 충분; CI는 수단이지 표준 목표 아님 |
| 05 SCM & Workflow | D Configuration Management | P change/configuration control | P maintainability/security indirect | 충분; merge 방식은 project choice |
| 06 Config & Secrets | D Security; P Operations/CM | P technical/support controls | D security; P reliability | 충분 |
| 07 Construction & Review | D Construction; P Quality/Professional Practice | D/P implementation/verification | P maintainability/functional suitability | 충분 |
| 08 Testing | D Testing, Quality | D/P verification/validation | D model used for test/acceptance | 충분 |
| 09 Application Security | D Security | P lifecycle security activities | D security, safety | 충분; 전용 security standards 필요 |
| 10 Supply-chain Security | D Security, CM; P Operations | P acquisition/supply/configuration | P security/reliability | 부분; SSDF/SLSA/OpenSSF 보강 유지 |
| 11 Maintainability/Tech Debt | D Maintenance, Quality | D/P maintenance/change | D maintainability, flexibility | 충분 |
| 12 Performance & Scalability | D Quality, Operations; P Design | P operation/technical management | D performance efficiency, reliability, flexibility | 충분 |
| 13 API & Interface | D Architecture, Design, Requirements | D/P interface/system definition | D compatibility, interaction capability, functional suitability | 충분 |
| 14 Data & Migrations | D Maintenance, Design; P Operations | P implementation/transition/maintenance | D reliability, maintainability, safety; data quality not established | 별도 data-quality 근거 필요 |
| 15 Accessibility & UX | D Requirements/Design/Quality; P Professional Practice | P stakeholder/validation | D interaction capability; accessibility detail not established | WCAG/EN 표준 보강 필요 |
| 16 Privacy & Data Protection | D/P Security, Professional Practice | P lifecycle risk/control | P security/safety; privacy standalone 여부 U | 독립 aspect 정당; privacy standards 필요 |
| 17 Release Engineering | D Operations, CM | P transition/release/operation | P reliability/maintainability | 충분 |
| 18 Packaging & Distribution | D Operations, CM; P Construction | P supply/transition | P compatibility/security | 충분; 생태계별 규칙 필요 |
| 19 Observability | D Engineering Operations, Quality | P operation/support | D reliability/performance efficiency | 충분 |
| 20 Operations/Incident/Reliability | D Operations, Maintenance, Management | D/P operation/support/retirement | D reliability, safety, performance | 조직 규모를 solo에 그대로 이식 금지 |
| 21 Economics/Cost/Sustainability | D Economics, Management | P technical/organizational management | U product quality model 직접 범위 아님 | sustainability/FinOps 별도 근거 필요 |
| 22 Documentation/Knowledge | D/P Professional Practice, Process, CM | P information-item support; detail U | P maintainability/interaction indirect | 15289·Diátaxis 별도 근거 유지 |
| 23 Developer Experience | D/P Professional Practice, Operations | P enabling/support process | P interaction capability/maintainability indirect | 실무 cross-cutting; 표준 직접 범위 약함 |
| 24 Governance/Collaboration/Compliance | D Management, Process, Professional Practice | P organizational/agreement processes | U/P quality governance indirect | 법·조직별 근거 필요 |
| 25 Licensing/FOSS | D/P Professional Practice, CM | P acquisition/supply | U product quality 직접 범위 아님 | 독립 aspect 정당; 법률 자문 대체 아님 |
| 26 MLOps/ML Lifecycle | P all lifecycle KAs; no dedicated KA | P lifecycle tailoring | P nine qualities; AI-specific quality U | 전문 확장; AI/data standards 별도 |
| 27 AI-Harness | P Security, Operations, Models/Methods; no dedicated KA | P tailoring/integration | P indirect qualities | G: agent authority/context/eval 고유 영역 |
| 28 Implementation Process & Agentic Workflow | D Process, Management, Models/Methods | D/P lifecycle selection/tailoring | U product quality 직접 범위 아님 | 충분; agent orchestration은 G |

## 구조 판정

### 빠진 범위

28 aspects는 전통적 software-engineering lifecycle과 product quality의 큰 영역을 넓게 덮는다. 하지만
다음은 별도 근거나 적용 축이 필요하다.

1. **Target-user capability/responsibility:** SWEBOK 지식영역과 lifecycle/process model이 “사용자가
   무엇을 이해하고 검증할 수 있는가”를 goppi가 필요한 해상도로 제공하지 않는다. aspect 29가 아니라
   모든 결정을 조건화하는 cross-cutting axis로 유지한다.
2. **Data quality, privacy, accessibility, sustainability, legal/regulatory compliance:** core 세 표준의
   개념 대응만으로 구체 통제나 준수를 만들 수 없다. 기존 전문 출처를 유지한다.
3. **AI-agent authority, prompt injection, memory/state, tool/egress boundary:** 세 표준의 tailoring과 기존
   security 원칙으로 일부 덮이지만 직접 구조는 없다. aspect 27의 goppi 고유 영역이다.
4. **Service quality와 solo operation:** ISO 25010 product quality와 운영 팀 관행만으로 1인 운영 모델을
   자동 도출할 수 없다.
5. **Last-mile release obligations:** 도메인·결제·개인정보 고지·스토어 정책은 선택한 아키타입과 관할에
   따라 활성화해야 한다.

### 중복처럼 보이지만 유지할 경계

- 04 Build/CI와 08 Testing: 04는 자동화·feedback infrastructure, 08은 verification strategy와 oracle.
- 06 Config/Secrets와 09 Security: 06은 runtime configuration/credential lifecycle, 09는 전체 threat/control.
- 17 Release와 18 Distribution: 17은 change-to-release process, 18은 artifact/channel/consumer contract.
- 19 Observability와 20 Operations: 19는 신호 생성, 20은 의사결정·incident·recovery.
- 23 DX와 22 Docs: 23은 작업 성과/마찰, 22는 정보 산출물과 지식 수명주기.
- 27 Harness와 28 Workflow: 27은 agent system/component boundary, 28은 프로젝트 수행 process.

이 경계는 검색 routing에는 유용하지만 한 구현 통제가 여러 aspect에 걸칠 수 있다. 중복 파일을 만들기
보다 canonical owner 한 곳과 cross-link를 사용한다.

## 결론과 해제 조건

- R0-2의 **구조 누락 탐색은 완료**: 28 aspects를 폐기하거나 전면 재구성할 근거는 없다.
- R0-2의 **ISO clause-level 검증은 INCONCLUSIVE**: ISO 12207:2026과 25010:2023 라이선스 본문을
  정당하게 확보한 뒤 process/characteristic 세부 대응을 독립 검토해야 한다.
- 그때까지 taxonomy는 `provisional-stable`이며 “ISO compliant”라는 표현을 금지한다.

## Sources

- `SWEBOK-4.0A` — https://www.computer.org/education/bodies-of-knowledge/software-engineering
- `ISO-12207-2026` — https://www.iso.org/standard/90219.html
- `ISO-25010-2023` — https://www.iso.org/standard/78176.html

