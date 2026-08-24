---
id: aspect-20-operations-incident-reliability--operations-sre--facts-2026-08
title: "Operations & SRE — facts (2026-08)"
parent: aspect-20-operations-incident-reliability
kind: research-log
evidence_track: lit
status: draft
language: ko
last_updated: "2026-08-02"
method: "Haiku web-research agents, facts-only rules ([정의/규정]/[데이터]/[주장] labels), source-tier tagged [1차]/[2차]; session-lead verified"
---

# Operations, SRE, DevOps 운영 관행 조사

## 개요

Google SRE Book의 핵심 개념과 업계 표준 정의를 정리한 자료. SLI/SLO/Error Budget, Toil, Incident Management, Blameless Postmortem, 모니터링, On-Call 규정, Observability, DevOps 정의, DORA 메트릭 등을 포함. 모든 내용은 공개된 1차 출처 기준.

---

## SLI, SLO, Error Budget

### [정의/규정] Service Level Indicator (SLI)
Google SRE Book는 SLI를 "서비스 수준을 측정하는 신중하게 정의된 정량적 측도(carefully defined quantitative measure of some aspect of the level of service)"로 정의 [https://sre.google/sre-book/service-level-objectives/]. 일반적 예시: 요청 지연시간(latency), 에러율(error rate), 시스템 처리량(throughput), 가용성.

### [정의/규정] Service Level Objective (SLO)
SLO는 "SLI에 대한 목표값 또는 값의 범위(target value or range of values for a service level)"로 정의 [https://sre.google/sre-book/service-level-objectives/]. 예: 평균 검색 지연시간 100ms 이하 유지.

### [정의/규정] Error Budget
Google SRE Book는 Error Budget을 "SLO를 놓칠 수 있는 허용 비율(rate at which the SLOs can be missed)"로 규정 [https://sre.google/sre-book/service-level-objectives/]. 조직은 100% SLO 준수를 요구하기보다 일일 또는 주간 기반으로 error budget을 추적 및 관리. 이를 통해 배포 속도와 신뢰성 간 균형 조율.

---

## Toil 정의

### [정의/규정] Toil의 6가지 특성
Google SRE Book는 toil을 "manual, repetitive, automatable, tactical, devoid of enduring value, and that scales linearly as a service grows"로 정의 [https://sre.google/sre-book/eliminating-toil/]. 구체적으로:
- **Manual**: 인간의 직접 개입 필요
- **Repetitive**: 반복적, 새로운 문제 해결이 아님
- **Automatable**: 기계가 인간만큼 효과적으로 수행 가능
- **Tactical**: 반응적, 인터럽트 기반
- **No enduring value**: 작업 후 서비스 상태가 변하지 않으면 toil
- **Scales linearly**: 서비스 성장에 선형적으로 증가

SRE Book은 "업무가 이 특성들과 일치할수록 toil일 가능성이 높다"고 명시 [https://sre.google/sre-book/eliminating-toil/].

---

## Incident Management 체계

### [정의/규정] IMAG (Incident Management At Google)
Google은 4개 역할 중심의 사건 대응 프레임워크 운영 [https://sre.google/sre-book/managing-incidents/]:

**Incident Commander (IC)**: "사건의 고수준 상태를 파악(holds the high-level state about the incident)" 하는 역할. 대응팀 구조화, 책임 할당, 장애물 제거 담당.

**Operational Lead (OL)**: "IC와 협력하여 운영 도구를 적용(works with the incident commander to respond to the incident by applying operational tools)" 하는 역할. OL만이 사건 중 시스템 수정 권한 보유.

**Communications Lead (CL)**: "사건 대응팀의 공개적 면모(public face of the incident response task force)" 역할. 이메일 등으로 정기적 업데이트 발송.

**Planning Lead (PL)**: "OL 지원(supports Ops by dealing with longer-term issues)" 역할. 버그 등록, 물품 주문, 인수인계, 시스템 복구 추적.

SRE Book은 "명확한 역할 분리가 개별 자율성을 높이고 상충 행동을 방지"한다고 기술 [https://sre.google/sre-book/managing-incidents/].

---

## Blameless Postmortem

### [정의/규정] Postmortem 정의
Google SRE Book는 postmortem을 "사건 기록, 영향, 완화/해결 조치, 근본 원인, 재발 방지 후속 조치를 담은 문서"로 정의 [https://sre.google/sre-book/postmortem-culture/].

### [규정] Blamelessness 원칙
Blameless postmortem의 핵심: "모든 관여자가 좋은 의도를 가졌고 보유한 정보로 올바른 행동을 했다고 가정(assumes that everyone involved in an incident had good intentions and did the right thing with the information they had)" [https://sre.google/sre-book/postmortem-culture/]. SRE Book은 "사람은 '고칠 수' 없지만 시스템과 프로세스는 고칠 수 있다"고 명시.

### [규정] Postmortem 구성
SRE Book 예시 postmortem은 포함: 사건 메타데이터, 타임라인, 영향 평가, 근본 원인 분석, 우선순위 조정 행동 항목 [https://sre.google/sre-book/postmortem-culture/]. Google은 Google Docs 기반 내부 템플릿 사용.

---

## On-Call 규정

### [규정] 시간 배분 규칙
Google SRE Book은 "SRE 시간의 최소 50%는 엔지니어링에, 최대 25%는 on-call 업무에 할당" 규정 [https://sre.google/sre-book/being-on-call/]. 남은 25%는 기타 운영 업무.

### [규정] 팀 규모 요구사항
SRE Book은 "24/7 커버리지 유지 시 25% 규칙 준수에 필요한 단일 사이트 팀 최소 8명" 규정. 이중 사이트 팀은 "야간 근무를 피할 수 있는 follow-the-sun 로테이션을 위해 위치당 최소 6명" 요구 [https://sre.google/sre-book/being-on-call/].

### [규정] 사건 처리 기준
SRE Book은 "한 번의 on-call 사건에 root cause analysis, remediation, follow-up에 약 6시간 소요되므로 12시간 교대당 최대 2건 사건 한계" 규정 [https://sre.google/sre-book/being-on-call/].

### [규정] 응답 시간 목표
SRE Book은 "사용자 대면 또는 높은 시간 민감도 서비스 5분, 낮은 민감도 서비스 30분" 페이징 응답 시간 수립 규정 [https://sre.google/sre-book/being-on-call/].

---

## 모니터링: Golden Signals

### [정의/규정] 4가지 Golden Signals
Google SRE Book의 "Monitoring Distributed Systems" 장은 모든 사용자 대면 시스템이 측정해야 할 4가지 메트릭 규정 [https://sre.google/sre-book/monitoring-distributed-systems/]:

**1. Latency**: 요청 충족에 필요한 시간. SRE Book은 "성공한 요청의 지연시간과 실패한 요청의 지연시간을 구분할 것" 강조. 빠른 에러는 심각한 문제를 숨길 수 있음.

**2. Traffic**: 시스템에 가해지는 수요 측도. 웹 서비스는 초당 HTTP 요청, 스트리밍은 네트워크 I/O, 데이터베이스는 초당 트랜잭션으로 측정.

**3. Errors**: 실패 요청의 비율. 명시적(HTTP 500), 암시적(성공 코드지만 부정확 콘텐츠), 정책 기반(약속된 응답시간 초과) 포함.

**4. Saturation**: 서비스가 "얼마나 꽉 찼는지" 측정. 가장 제약된 리소스 기준. 용량 여유 예측과 100% 전 성능 저하 포함.

SRE Book은 "4가지 signal이 문제일 때 담당자를 호출하면 서비스는 최소한 적절히 모니터링 된다" 명시 [https://sre.google/sre-book/monitoring-distributed-systems/].

---

## Observability: 3요소

### [정의/규정] Observability의 3 요소
업계는 observability를 3가지 신호 유형으로 정의 [https://www.elastic.co/blog/3-pillars-of-observability]:

**Metrics**: "시스템에서 무엇이 일어나는지" 측정하는 숫자 데이터. CPU 사용률, 메모리, 응답시간, 에러율, 가용성 포함. Elastic는 "metrics는 알려진 것들(known knowns)을 측정하는 원본 숫자 데이터"라고 정의.

**Logs**: "왜 일어나는지" 답변하는 타임스탬프 기록. 네트워크, OS, 애플리케이션, IoT 기기에서 발생. Elastic는 "logs는 특정 이벤트 관련 타임스탬프 항목으로 구성된 구조화/비구조화 데이터"로 정의.

**Traces**: "어디에서 일어나는지" 추적. 분산 시스템 전역 사용자 행동 기록. Elastic는 "traces는 사용자 관점에서 애플리케이션을 보여주는 첫 신호로 사용자가 수행하는 행동 기록"이라고 정의 [https://www.elastic.co/blog/3-pillars-of-observability].

---

## DevOps: 정의 및 역사

### [정의/규정] DevOps 개념
DevOps는 "여정 또는 열망이지 도착점이 아님(a journey, or perhaps an aspiration, rather than defined destination)"으로 묘사. 애플리케이션 개발과 운영팀의 통합, 자동화 도구를 통한 지속적 개선 및 배포 추구 [https://devops.com/the-origins-of-devops-whats-in-a-name/].

### [데이터] DevOps 역사 및 원조
**사전 단계**: 린 제조, 애자일 개발, IaaS/PaaS 클라우드, 지속적 통합 도구들의 수렴.

**Patrick Debois의 역할**: 벨기에 컨설턴트 Debois는 데이터센터 마이그레이션 업무 중 "애플리케이션 방법론과 인프라 방법론 간 분리의 벽과 응집력 부족" 목격 [https://devops.com/the-origins-of-devops-whats-in-a-name/]. 2008년 Andrew Schafer와 "Agile Infrastructure" 토론, Agile Systems Administrator 그룹 공동 설립.

**결정적 순간**: 2009년 Flickr 엔지니어 John Allspaw와 Paul Hammond가 O'Reilly Velocity Conference에서 "10+ Deploys per Day: Dev and Ops Cooperation at Flickr" 발표. 업계는 이를 "DevOps 채택을 촉발한 획기적 순간(seminal moment in time)"으로 평가 [https://devops.com/the-origins-of-devops-whats-in-a-name/]. Debois는 이에 영감받아 2009년 벨기에 헨트에서 첫 Devopsdays 컨퍼런스 개최, 공식 용어 수립.

---

## DORA 메트릭: 운영 Capability

### [정의/규정] DORA 개요
DORA (DevOps Research and Assessment)는 Google Cloud에서 10년 이상 업계 연구 기반 개발한 표준 DevOps 메트릭. "소프트웨어 배포 속도와 안정성의 4가지 측정 (four measurements of software delivery velocity and stability)" [https://www.atlassian.com/devops/frameworks/dora-metrics].

### [정의/규정] 4가지 DORA 메트릭
DORA는 조직 성과를 평가하는 4개 메트릭 규정 [https://www.pivotpointsecurity.com/what-are-the-5-key-devops-research-assessment-dora-metrics-and-why-should-i-care/]:

**Deployment Frequency**: 조직이 얼마나 자주 성공적으로 프로덕션에 코드 배포하는지. 작은 배치를 빠르고 효율적으로 전달하는 능력 측정.

**Lead Time for Changes**: DevOps 팀이 코드 커밋에서 배포까지 평균 속도. 배포 속도 메트릭.

**Change Failure Rate**: 배포된 변경 중 실패(프로덕션 인시던트, 롤백 등)하는 비율. 안정성 메트릭.

**Mean Time to Restore (MTTR)**: 프로덕션 사건에서 정상 서비스로 복구되는 평균 시간. 회복력 메트릭.

각 메트릭은 Low, Medium, High, Elite 성숙도 레벨로 평가 [https://www.atlassian.com/devops/frameworks/dora-metrics].

---

## Runbook / Playbook

### [주장] 용어 정의
SRE 업계에서 runbook은 특정 운영 절차의 단계별 지침서, playbook은 여러 runbook을 조합한 더 광범위한 사건 대응 가이드로 사용 [https://sre.google/resources/practices-and-processes/incident-management-guide/]. Google의 incident management 가이드는 명확한 절차 문서화를 강조하나 formal terminology 정의는 제한적.

---

## 출처 목록

> [1차] = 원저자·원기관 발행 / [2차] = 제3자의 정리·집계

- [1차] [Google SRE Book - Service Level Objectives](https://sre.google/sre-book/service-level-objectives/)
- [1차] [Google SRE Book - Eliminating Toil](https://sre.google/sre-book/eliminating-toil/)
- [1차] [Google SRE Book - Managing Incidents](https://sre.google/sre-book/managing-incidents/)
- [1차] [Google SRE Book - Postmortem Culture](https://sre.google/sre-book/postmortem-culture/)
- [1차] [Google SRE Book - Being On-Call](https://sre.google/sre-book/being-on-call/)
- [1차] [Google SRE Book - Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/)
- [2차] [Elastic - 3 Pillars of Observability](https://www.elastic.co/blog/3-pillars-of-observability)
- [2차] [DevOps.com - The Origins of DevOps](https://devops.com/the-origins-of-devops-whats-in-a-name/)
- [2차] [Atlassian - DORA Metrics](https://www.atlassian.com/devops/frameworks/dora-metrics)
- [2차] [Pivot Point Security - DORA Metrics](https://www.pivotpointsecurity.com/what-are-the-5-key-devops-research-assessment-dora-metrics-and-why-should-i-care/)
- [1차] [Google SRE - Incident Management Guide](https://sre.google/resources/practices-and-processes/incident-management-guide/)
