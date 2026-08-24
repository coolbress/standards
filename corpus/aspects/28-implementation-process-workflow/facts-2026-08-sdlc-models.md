---
id: aspect-28-implementation-process-workflow--facts-2026-08-sdlc-models
title: "SDLC models & standards — facts (2026-08)"
parent: aspect-28-implementation-process-workflow
kind: research-log
evidence_track: lit
status: draft
language: ko
last_updated: "2026-08-02"
method: "Haiku web-research agents, facts-only rules ([정의/규정]/[데이터]/[주장] labels), source-tier tagged [1차]/[2차]; session-lead verified"
---

# SDLC 모델과 표준: 실제 규정 사항

## 개요

이 문서는 Waterfall(1970), V-model, Spiral(Boehm), RUP, ISO/IEC/IEEE 12207, CMMI, 현대적 지속적 전달 등 주요 SDLC 모델과 표준을 정리한다. ISO 부분은 2017판 기반의 역사적 상세와 ISO/IEC/IEEE 12207:2026 공개 catalog에서 확인 가능한 현행 범위를 분리한다.

---

## Waterfall 모델 (Winston Royce, 1970)

[정의/규정]
Royce의 원문은 대규모 소프트웨어 프로젝트를 위한 일곱 가지 순차적 단계를 규정한다: 시스템 요구사항 → 소프트웨어 요구사항 → 분석 → 프로그램 설계 → 코딩 → 테스트 → 운영 [https://medium.com/@milo.todorovich/a-summary-of-the-waterfall-paper-ae9153788d1]. 예비 프로그램 설계 단계를 분석 전에 추가하고, 각 단계의 완료를 기록으로 남기며, 새로운 시스템은 프로토타입에 "전체 일정의 1/4에서 1/3"을 투자할 것을 처방한다 [https://medium.com/@milo.todorovich/a-summary-of-the-waterfall-paper-ae9153788d1]. 코드 리뷰와 검사, 그리고 설계에 참여하지 않은 독립적 테스트 전문가 배치를 요구한다 [https://medium.com/@milo.todorovich/a-summary-of-the-waterfall-paper-ae9153788d1].

[주장]
Royce는 이 모델이 단순히 분석과 코딩 두 단계만으로는 "실패할 수밖에 없다"고 주장했으며, 개발 단계 간의 반복적 피드백 루프가 전체 시스템 재설계를 초래하여 "시간과 예산의 100% 이상 초과"를 야기할 수 있다고 우려했다 [https://medium.com/@milo.todorovich/a-summary-of-the-waterfall-paper-ae9153788d1].

[주의사항]
역사적 오류: Royce는 waterfall 용어를 사용하지 않았으며, 이 선형 모델을 실무에서 작동하는 방법론으로 옹호하지 않았다 [https://pragtob.wordpress.com/2012/03/02/why-waterfall-was-a-big-misunderstanding-from-the-beginning-reading-the-original-paper/].

---

## V-Model

[정의/규정]
V-Model은 waterfall의 확장으로, 개발 단계 좌측 (검증)과 테스트 단계 우측 (타당성 검증)을 대칭으로 배치한다 [https://www.tutorialspoint.com/sdlc/sdlc_v_model.htm]. 다섯 가지 발전 단계: 요구사항 분석 → 시스템 설계 → 아키텍처 설계 → 모듈 설계 → 코딩. 각 좌측 단계에는 대응하는 우측 테스트 단계가 있다: 단위 테스트, 통합 테스트, 시스템 테스트, 인수 테스트 [https://www.tutorialspoint.com/sdlc/sdlc_v_model.htm]. "개발 주기의 모든 단계마다 직접 대응하는 테스트 단계가 있다"는 원칙을 처방한다 [https://www.tutorialspoint.com/sdlc/sdlc_v_model.htm]. 테스트 계획을 설계 단계 중에 작성하고, 코딩 이후가 아닌 선행 작성을 요구한다 [https://www.tutorialspoint.com/sdlc/sdlc_v_model.htm].

---

## Spiral 모델 (Barry Boehm, 1986)

[정의/규정]
Spiral 모델은 위험 중심의 소프트웨어 프로세스이며, 각 나선 루프는 단계를 나타낸다: 계획 → 위험 분석 → 개발 → 평가 [https://en.wikipedia.org/wiki/Spiral_model]. 각 루프마다 위험 분석을 수행하고, 기본적 결함은 초기 단계에서 발견될 가능성이 높아 수정 비용이 낮다고 처방한다 [https://en.wikipedia.org/wiki/Spiral_model]. 프로토타이핑과 점진적 재검토를 규정한다. 프로젝트의 고유한 위험 패턴에 따라 waterfall, 증분, 진화적 프로토타이핑 등의 요소를 통합하도록 처방한다 [https://en.wikipedia.org/wiki/Spiral_model]. 대규모 복잡 프로젝트(6개월 ~ 2년)를 대상으로 한다 [https://en.wikipedia.org/wiki/Spiral_model].

[데이터]
NASA는 Space Shuttle 소프트웨어 및 Earth Observing System에 Spiral 모델을 적용했다 [https://en.wikipedia.org/wiki/Spiral_model].

---

## RUP (Rational Unified Process)

[정의/규정]
RUP는 네 가지 단계(Inception, Elaboration, Construction, Transition)와 아홉 가지 훈련(Discipline)으로 구성된다 [https://www.geeksforgeeks.org/software-engineering/rup-and-its-phases/]. 

엔지니어링 훈련 6개: 요구사항, 분석과 설계 (원본 코드의 청사진 역할), 구현, 테스트, 배포, 비즈니스 모델링 [https://en.wikibooks.org/wiki/RUP_-_IBM_Rational_Unified_Process/Disciplines_or_Workflows].

지원 훈련 3개: 구성과 변경 관리, 프로젝트 관리, 환경 [https://en.wikibooks.org/wiki/RUP_-_IBM_Rational_Unified_Process/Disciplines_or_Workflows].

각 단계 내에서 반복이 수행되고, 각 반복마다 요구사항이나 테스트 같은 특정 훈련의 활동을 변동 강도로 수행한다 [https://www.geeksforgeeks.org/software-engineering/rup-and-its-phases/].

---

## ISO/IEC/IEEE 12207

[현행 공개 근거]
ISO 공식 catalog에서 ISO/IEC/IEEE 12207:2017은 폐기(withdrawn)됐고 ISO/IEC/IEEE 12207:2026이
2026년 4월 발행된 현행판이다 [https://www.iso.org/standard/90219.html]. 공개 초록은 이 표준이 특정
생명주기 모델이나 개발 방법론을 요구하지 않는 공통 software life-cycle-process framework이며, 그
process들을 동시·반복·재귀·점진적으로 적용할 수 있다는 범위까지 확인한다.

[역사적 2017판 분류 — 현행 2026 조항으로 재귀속 금지]
아래 네 범주는 2017판을 설명한 2차 자료에서 승계한 내용이다. 유료 2026 본문으로 대조하지 못했으므로
현행판의 세부 process taxonomy를 증명하는 근거로 사용하지 않는다:
1. 계약 과정: 조직 간 계약, 취득, 공급, 고객-공급자 관계
2. 조직 프로젝트 활성화 과정: 생명주기 모델 관리, 인프라 관리, 인적 자원 관리
3. 기술 관리 과정: 프로젝트 계획, 평가, 제어, 의사결정, 위험 관리, 구성 관리
4. 기술 과정: 이해관계자 요구사항 정의, 요구사항 분석, 아키텍처 설계, 구현, 통합, 검증, 타당성 검증, 운영, 유지보수, 폐기 [https://quality.arc42.org/standards/iso12207].

“Agile/DevOps 지원”과 품질 속성에 대한 기존 문장도 2차 자료의 해석으로 격하한다. 공개 ISO 초록은
agile 접근에도 적용 가능하다고만 밝히며, 특정 품질 속성 처방이나 방법 선택법을 입증하지 않는다.

---

## CMMI (Capability Maturity Model Integration)

[정의/규정]
CMMI는 다섯 가지 성숙도 단계를 규정한다 [https://www.tutorialspoint.com/cmmi/cmmi-maturity-levels.htm]:

**Level 1 (초기)**: 과정이 "일반적으로 임시적이고 혼란스럽다". 성공은 개인 역량에 의존하며, 예산과 일정 초과가 빈번하다 [https://www.tutorialspoint.com/cmmi/cmmi-maturity-levels.htm].

**Level 2 (관리됨)**: 프로젝트는 "요구사항이 관리되고 과정이 계획, 수행, 측정, 제어된다". 산출물을 추적하고 이해관계자 약속을 문서화한다 [https://www.tutorialspoint.com/cmmi/cmmi-maturity-levels.htm].

**Level 3 (정의됨)**: "과정이 특성화되고 이해되며, 표준, 절차, 도구, 방법론으로 기술된다". 조직이 표준화된 과정을 수립하고 프로젝트에 일관되게 적용한다 [https://www.tutorialspoint.com/cmmi/cmmi-maturity-levels.htm].

**Level 4 (정량적 관리)**: "전체 과정 성과에 상당히 기여하는 부분 과정들을 선택하여 통계 및 정량적 기법으로 관리한다" [https://www.tutorialspoint.com/cmmi/cmmi-maturity-levels.htm].

**Level 5 (최적화)**: "과정이 변동의 공통 원인에 대한 정량적 이해를 바탕으로 지속적으로 개선된다". 혁신과 성능 향상에 집중한다 [https://www.tutorialspoint.com/cmmi/cmmi-maturity-levels.htm].

Staged 표현은 22개 프로세스 영역을 5 단계로 그룹화하여 조직의 단일 성숙도 레벨을 산출한다 [https://www.tutorialspoint.com/cmmi/cmmi-maturity-levels.htm].

---

## 지속적 전달 (Continuous Delivery) 생명주기

[정의/규정]
지속적 전달은 코드 변경을 배포 파이프라인을 통해 프로덕션 준비 상태로 유지하는 프레임워크이며, 다섯 단계를 규정한다: 개발 → 커밋 (버전 관리) → 테스트 (자동 테스트) → Stage (실제 환경 모의) → 배포 (프로덕션) [https://codefresh.io/learn/continuous-delivery/]. 

파이프라인 전반에 걸쳐 자동화를 강조하고, "통합과 회귀 테스트를 개발자의 일상 업무에 포함"시키도록 처방하며, "테스트를 별도 단계로 분리하지 않는다" [https://continuousdelivery.com/]. 코드를 "항상 배포 가능한 상태"로 유지하고, 수천 명의 개발자가 매일 변경해도 안전하게 관리하도록 요구한다 [https://continuousdelivery.com/]. 배포 위험을 최소화하기 위해 blue-green 배포 같은 기법을 처방한다 [https://continuousdelivery.com/]. 

지속적 전달은 자동 프로덕션 배포 직전에서 멈추고, 지속적 배포(Continuous Deployment)는 자동으로 프로덕션에 릴리스한다는 점에서 구별된다 [https://www.redhat.com/en/topics/devops/what-is-ci-cd].

[주장]
"배포가 빈번할 필요가 없는 팀(예: 의료 분야)에는 지속적 전달이 일반적으로 더 선호되며, 더 느리지만 기말 사용자 기능성을 보장하는 추가 감시층을 제공한다" [https://www.redhat.com/en/topics/devops/what-is-ci-cd].

---

## Agile Manifesto (2001)

[정의/규정]
Agile Manifesto는 2001년 2월 11-13일 유타 주 Snowbird ski resort에서 17명의 개발자가 작성했다 [https://agilemanifesto.org/]. 

네 가지 핵심 가치를 규정한다:
1. 프로세스와 도구보다 개인과 상호작용
2. 포괄적 문서보다 작동하는 소프트웨어
3. 계약 협상보다 고객 협력
4. 계획 준수보다 변화에 대한 응답 [https://agilemanifesto.org/].

12개 원칙을 규정한다: (1) 고객 만족을 통한 지속적 가치 전달 [https://agilemanifesto.org/principles.html], (2) 변화 요구를 환영함 [https://agilemanifesto.org/principles.html], (3) 2주~2개월 간격의 빈번한 작동 소프트웨어 전달(더 짧은 주기 선호) [https://agilemanifesto.org/principles.html], (4) 비즈니스 담당자와 개발자의 일일 협력 [https://agilemanifesto.org/principles.html], (5) 동기 부여된 개인과 환경 제공 [https://agilemanifesto.org/principles.html], (6) 면대면 대화 최우선 [https://agilemanifesto.org/principles.html], (7) 진행 상황의 주요 지표로 작동 소프트웨어 [https://agilemanifesto.org/principles.html], (8) 지속 가능한 개발 속도 유지 [https://agilemanifesto.org/principles.html], (9) 기술적 우수성과 설계 품질 지속 [https://agilemanifesto.org/principles.html], (10) 단순함(하지 않는 일 최대화) [https://agilemanifesto.org/principles.html], (11) 자기조직화 팀에서 최고의 아키텍처와 설계 도출 [https://agilemanifesto.org/principles.html], (12) 정기적 효과성 반성 및 조정 [https://agilemanifesto.org/principles.html].

[데이터]
전 세계 조직의 95% 이상이 Agile 개발 방법론을 실천한다 [https://www.wrike.com/agile-guide/agile-manifesto/].

---

## 출처 목록

> [1차] = 원저자·원기관 발행 / [2차] = 제3자의 정리·집계

- [2차] https://medium.com/@milo.todorovich/a-summary-of-the-waterfall-paper-ae9153788d1
- [2차] https://pragtob.wordpress.com/2012/03/02/why-waterfall-was-a-big-misunderstanding-from-the-beginning-reading-the-original-paper/
- [2차] https://www.tutorialspoint.com/sdlc/sdlc_v_model.htm
- [2차] https://en.wikipedia.org/wiki/Spiral_model
- [2차] https://www.geeksforgeeks.org/software-engineering/rup-and-its-phases/
- [2차] https://en.wikibooks.org/wiki/RUP_-_IBM_Rational_Unified_Process/Disciplines_or_Workflows
- [2차] https://quality.arc42.org/standards/iso12207
- [2차] https://en.wikipedia.org/wiki/ISO/IEC_12207
- [1차·현행 catalog] https://www.iso.org/standard/90219.html
- [2차] https://www.tutorialspoint.com/cmmi/cmmi-maturity-levels.htm
- [2차] https://codefresh.io/learn/continuous-delivery/
- [1차] https://continuousdelivery.com/ (Continuous Delivery 공저자 Jez Humble의 사이트)
- [2차] https://www.redhat.com/en/topics/devops/what-is-ci-cd
- [1차] https://agilemanifesto.org/
- [1차] https://agilemanifesto.org/principles.html
- [2차] https://www.wrike.com/agile-guide/agile-manifesto/
