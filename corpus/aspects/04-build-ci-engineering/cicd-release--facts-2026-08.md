---
id: aspect-04-build-ci-engineering--cicd-release--facts-2026-08
title: "CI/CD & release engineering — facts (2026-08)"
parent: aspect-04-build-ci-engineering
kind: research-log
evidence_track: lit
status: draft
language: ko
last_updated: "2026-08-02"
method: "Haiku web-research agents, facts-only rules ([정의/규정]/[데이터]/[주장] labels), source-tier tagged [1차]/[2차]; session-lead verified"
---

# CI/CD 및 Release Engineering 연구 자료

## 개요

Continuous Integration(CI)은 팀원 모두가 최소 일일 단위로 mainline에 코드를 통합하는 소프트웨어 개발 실천이다 [https://martinfowler.com/articles/continuousIntegration.html]. Continuous Delivery(CD)는 모든 변경이 프로덕션 배포 가능 상태를 유지하되 수동 승인이 필요하고, Continuous Deployment는 모든 변경을 자동으로 프로덕션에 배포한다 [https://martinfowler.com/delivery.html]. DORA 메트릭과 배포 전략(blue-green, canary) 등이 배포 신뢰성을 측정하는 핵심 도구이다.

---

## Continuous Integration 정의 및 실천

[정의/규정] Martin Fowler는 CI를 다음과 같이 정의한다: "여러 개발자의 작업 사본을 하루에 여러 번 통합하는 소프트웨어 개발 실천" [https://martinfowler.com/articles/continuousIntegration.html].

[정의/규정] 핵심 실천 항목:
- 일일 최소 통합 빈도: 팀의 모든 사람이 최소 매일 통합해야 함 [https://martinfowler.com/articles/continuousIntegration.html]
- 10분 빌드: 구축 속도 목표는 약 10분으로, 빠른 피드백 루프 달성 [https://martinfowler.com/articles/continuousIntegration.html]
- 자동화된 자체 검증 빌드: 데이터베이스 스키마 포함, 포괄적 테스트 통합 [https://martinfowler.com/articles/continuousIntegration.html]
- 단일 mainline 분기: "단일, 공유 분기가 제품의 현재 상태로 작용" [https://martinfowler.com/articles/continuousIntegration.html]

[주장] Fowler는 빌드 속도의 중요성을 강조한다: "매분 절감한 시간이 팀 전체의 일일 여러 커밋에 걸쳐 누적" [https://martinfowler.com/articles/continuousIntegration.html].

---

## Continuous Delivery vs Continuous Deployment

[정의/규정] Fowler의 정의 [https://martinfowler.com/delivery.html]:
- **Continuous Delivery**: 모든 변경이 프로덕션 배포 가능 상태를 유지하되, 버튼 클릭으로 배포하는 단계에서 멈춤
- **Continuous Deployment**: 모든 변경을 자동으로 프로덕션에 배포함

[정의/규정] Continuous Delivery 특성 [https://martinfowler.com/delivery.html]:
- 소프트웨어를 생명 주기 전체에서 배포 가능 상태로 유지
- 새 기능 개발보다 배포 가능성을 우선시
- 변경 시 프로덕션 준비 상태에 대한 자동화된 피드백
- 버튼 클릭으로 임의 버전을 임의 환경에 배포 가능

[주장] "Continuous deployment은 continuous delivery보다 더 완전한 자동화 형태로 볼 수 있다" [https://www.atlassian.com/continuous-delivery/principles/continuous-integration-vs-delivery-vs-deployment].

---

## Feature Toggles/Flags 분류

[정의/규정] Fowler는 Feature Flag를 두 가지 주요 차원으로 분류한다 [https://martinfowler.com/bliki/FeatureFlag.html]:
- **Release Toggles**: 개발 및 운영 중 미완성/위험 기능을 일부 또는 전체 사용자로부터 숨김. Mainline 개발 실천 가능
- **Experiment Toggles**: A/B 테스트 목적
- **Ops Toggles**: 프로덕션 운영 스태프의 시스템 제어
- **Permissioning Toggles**: 다양한 사용자 세그먼트/그룹의 기능 접근 관리

[주장] Fowler는 경고한다: "release flags는 프로덕션 배포 시 마지막 수단이어야 함. 대신 Keystone Interface 접근법을 우선하라" [https://martinfowler.com/bliki/FeatureFlag.html].

---

## 배포 전략

[정의/규정] **Blue-Green Deployment** [https://martinfowler.com/bliki/BlueGreenDeployment.html]:
- 동일한 두 프로덕션 환경에서 하나는 사용자 트래픽 처리, 다른 하나는 업데이트 준비
- 준비 완료 시 전체 트래픽을 새 환경으로 전환
- 장점: 즉시 롤백 가능, 이전 환경을 다음 배포의 롤백 대상으로 유지

[정의/규정] **Canary Deployment** [https://martinfowler.com/bliki/CanaryRelease.html]:
- 새 버전을 소수 사용자에게만 먼저 노출하여 위험 감소
- 성능 모니터링, 피드백 수집 후 전체 사용자에게 확대
- blue-green보다 점진적이고 세밀한 제어 가능

---

## DORA 메트릭

[정의/규정] DORA(DevOps Research and Assessment)의 4+1 메트릭 [https://www.libertify.com/interactive-library/state-of-devops-2024-dora/]:
- **Deployment Frequency(배포 빈도)**: 프로덕션 배포 빈도
- **Lead Time for Changes(변경 리드타임)**: 코드 커밋 → 프로덕션 배포 소요 시간
- **Change Failure Rate(변경 실패율)**: 프로덕션 장애 야기 배포 비율
- **Mean Time to Recovery(복구 시간)**: 배포 실패 복구까지 소요 시간
- **Deployment Rework Rate(배포 재작업율)**: 사용자 대면 버그 해결용 계획되지 않은 배포 비율 (2024년 추가) [https://octopus.com/devops/metrics/dora-metrics/]

[데이터] 2024 성과 수준별 벤치마크 [https://www.libertify.com/interactive-library/state-of-devops-2024-dora/]:
- **Elite**: 다중 일일 배포, 1일 미만 리드타임, 5% 미만 실패율, 1시간 미만 복구
- **High**: 주 1~일 1회 배포, 주 1회 미만 리드타임
- **Medium**: 월 1회~주 1회 배포, 월 1회 미만 리드타임
- **Low**: 월 1회 미만 배포

[데이터] Elite vs Low 성과 격차 [https://www.taskade.com/blog/dora-metrics-explained]: "Elite는 Low 대비 127배 빠른 리드타임, 182배 많은 배포, 8배 낮은 실패율, 2,293배 빠른 복구" [https://octopus.com/devops/metrics/dora-metrics/].

---

## Semantic Versioning (SemVer)

[정의/규정] 공식 SemVer 2.0.0 명세 [https://semver.org/]:
- 버전 형식: **MAJOR.MINOR.PATCH** (예: 1.9.0)
- **MAJOR**: 호환되지 않는 API 변경
- **MINOR**: 역호환 기능 추가
- **PATCH**: 역호환 버그 수정

[정의/규정] 핵심 규칙 [https://semver.org/]:
- 각 구성요소는 음이 아닌 정수, 숫자 증가 (1.9.0 → 1.10.0)
- 릴리스 후 내용 불변: 변경 시 새 버전 필요
- 0.y.z: 초기 개발 (모든 사항 변경 가능)
- 1.0.0: 첫 안정 공개 API, 이후 번호 매김 규칙 정의
- Pre-release/메타데이터: 하이픈/플러스 부가 (1.0.0-alpha, 1.0.0+20130313144700)
- 버전 우선순위: 숫자로 비교 (1.0.0-alpha < 1.0.0)

---

## Release Train

[정의/규정] Release Train은 고정 일정 배포 조율 기법이다 [https://www.thoughtworks.com/radar/techniques/release-train]:
- 고정, 신뢰할 수 있는 일정에 모든 배포 진행
- 기능 준비 여부와 무관하게 일정대로 배포 ("기차는 기다리지 않음")
- 팀이 기능 준비를 놓치면 다음 주기까지 대기

[정의/규정] **Agile Release Train (ART)** - SAFe(Scaled Agile Framework) 개념 [https://framework.scaledagile.com/blog/glossary_term/agile-release-train-art-2/]:
- 공통 미션 팀(팀들의 팀): 일반적으로 50~125명 규모
- 공통 계획, 공통 리듬으로 배포
- 여러 팀의 런타임 종속성 조율 기법

---

## CI/CD 도구 채택 현황

[데이터] 2025 JetBrains State of Developer Ecosystem 조사 [https://blog.jetbrains.com/teamcity/2025/10/the-state-of-cicd/]:

**조직 채택율**:
- GitHub Actions: 33%
- Jenkins: 28%
- GitLab CI: 19%

**개인 프로젝트 채택율**:
- GitHub Actions: 39%
- Jenkins: 13%
- GitLab CI: 10%

**GitHub 생태계**:
- GitHub Actions 이용률: 68%

[데이터] 다중 도구 사용 [https://blog.jetbrains.com/teamcity/2025/10/the-state-of-cicd/]:
- 2개 도구: 32%
- 3개 이상: 9%

[데이터] 18% 응답자가 CI/CD 도구 미사용 [https://blog.jetbrains.com/teamcity/2025/10/the-state-of-cicd/].

---

## 모노레포 vs 멀티레포

[주장] Google은 수만 명의 개발자가 사용하는 모놀리식 저장소를 운영한다 [https://www.uncommonengineer.com/docs/books/papers/Google3/]:
- 워크스페이스 디렉토리 구조 (팀/담당자별 책임)
- Trunk 기반 개발, 분산 저장소 Piper, 클라이언트 CitC, 워크플로우 도구(Critique, CodeSearch, Tricorder, Rosie) 활용

[주장] 업계 입장 차이 [https://www.sonarsource.com/resources/library/monorepo/]:
- **모노레포 옹호**: 코드 공유 간편, 종속성 관리 단순화, 문서 동기화 일원화
- **멀티레포 옹호**: 독립 워크플로우, 세밀한 제어
- Android, Chrome 등 Google 대규모 프로젝트는 멀티레포 모델 사용

---

## 출처

> [1차] = 원저자·원기관 발행 / [2차] = 제3자의 정리·집계

- [1차] https://martinfowler.com/articles/continuousIntegration.html
- [1차] https://martinfowler.com/articles/originalContinuousIntegration.html
- [1차] https://martinfowler.com/delivery.html
- [1차] https://martinfowler.com/bliki/FeatureFlag.html
- [1차] https://martinfowler.com/bliki/BlueGreenDeployment.html
- [1차] https://martinfowler.com/bliki/CanaryRelease.html
- [1차] https://semver.org/
- [2차] https://www.libertify.com/interactive-library/state-of-devops-2024-dora/ (DORA 원문 아님 — 제3자 요약)
- [2차] https://octopus.com/devops/metrics/dora-metrics/
- [2차] https://www.taskade.com/blog/dora-metrics-explained
- [2차] https://www.thoughtworks.com/radar/techniques/release-train
- [1차] https://framework.scaledagile.com/blog/glossary_term/agile-release-train-art-2/
- [1차] https://blog.jetbrains.com/teamcity/2025/10/the-state-of-cicd/
- [1차] https://blog.jetbrains.com/teamcity/2026/03/best-ci-tools/
- [1차] https://www.uncommonengineer.com/docs/books/papers/Google3/
- [2차] https://www.sonarsource.com/resources/library/monorepo/
- [2차] https://www.atlassian.com/continuous-delivery/principles/continuous-integration-vs-delivery-vs-deployment


## Claim table — 10분 빌드 (`03` 미검증 해소 · 1차 출처 직접 확인 2026-08-26)

| Claim ID | Class | Claim and scope | Evidence | Confidence | 재검증 |
|---|---|---|---|---|---|
| CIB-001 | normative | ✅ **10분 빌드는 원문에 있다 — 단 실증이 아니라 가이드라인이다.** Fowler: *"the **XP guideline** of a **ten minute build** is perfectly within reason."* 출처가 XP(Beck)이고 Fowler 가 **합리적이라 승인**한 형태다 — **측정된 임계가 아니다.** 같은 글이 *"nobody has a higher priority task than **fixing the build**"*(Beck)로 *"깨지면 즉시 수리"* 도 받친다 | `FOWLER-CI` | high (인용) / **medium (규범 강도)** | 2026-08-26 **신규** |

**재검증 기록 (`03` ⚪ 해소 · 10분 빌드)** — 검증일 `2026-08-26` · 검증자 `Claude Opus 5` · **판정: 신규 1(지위 = 실무 가이드라인)** · 절차 [`reverification-protocol`](../../methods/reverification-protocol.md)
