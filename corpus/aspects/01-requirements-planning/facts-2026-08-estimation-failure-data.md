---
id: aspect-01-requirements-planning--facts-2026-08-estimation-failure-data
title: "Project failure/success & estimation data — facts (2026-08)"
parent: aspect-01-requirements-planning
kind: research-log
evidence_track: lit
status: draft
language: ko
last_updated: "2026-08-02"
method: "Haiku web-research agents, facts-only rules ([정의/규정]/[데이터]/[주장] labels), source-tier tagged [1차]/[2차]; session-lead verified"
---

# 소프트웨어 프로젝트 성공·실패율 및 추정 관련 측정 데이터

## 개요
Standish CHAOS 리포트, McKinsey-Oxford 연구, Boehm 곡선, Cone of Uncertainty 등 IT 프로젝트 성패 및 추정 비용에 관한 주요 실측 데이터 및 학계 비판을 수집한 문서. 연도별/규모별 성공률, 비용초과 통계, 결함 수정 비용 곡선 주장과 그에 대한 반박, AI가 개발 생산성에 미치는 영향에 대한 수치를 기록한다.

---

## 1. Standish CHAOS 리포트: 프로젝트 성패율

### [데이터] 연도별 성공/도전/실패율

CHAOS 리포트는 프로젝트를 세 가지로 분류한다 [정의/규정]: 성공(온 스케줄, 온 예산, 합의된 기능 전달), 도전(일정/비용/범위 중 하나 이상 미달성), 실패(완료 전 취소 또는 미사용) [https://budgetoverrun.com/studies/standish-chaos-report].

연도별 수치 [데이터]:
- 1994: 성공 16%, 실패 31%, 도전 53%
- 1996: 성공 27%, 실패 40%, 도전 33%
- 2000: 성공 28%, 실패 23%, 도전 49%
- 2002: 성공 34%, 실패 15%, 도전 51%
- 2009: 성공 32%, 실패 24%, 도전 44%
- 2010: 성공 37%, 실패 21%, 도전 42%
- 2015: 성공 29%, 실패 19%, 도전 52%
- 2020: 성공 31%, 실패 19%, 도전 50% [https://budgetoverrun.com/studies/standish-chaos-report]

프로젝트 규모별로 성공률이 상이함: 소규모 프로젝트는 대규모 프로젝트보다 성공률이 현저히 높다 [https://budgetoverrun.com/studies/standish-chaos-report].

### [데이터] 프로젝트 규모에 따른 성공률 패턴

소규모 프로젝트(초기 가격 $15M 미만)는 대규모 프로젝트(초기 가격 $15M 이상)보다 높은 성공률을 기록한다. CHAOS 2020 기준 전체 프로젝트의 69%가 도전 또는 실패로 분류되었다 [https://budgetoverrun.com/studies/standish-chaos-report].

---

## 2. Eveleens & Verhoef의 CHAOS 방법론 비판 [주장]

### 핵심 주장

Eveleens와 Verhoef는 2010년 IEEE Software에 "The Rise and Fall of the Chaos Report Figures"를 발표하여 Standish 정의의 네 가지 주요 결함을 지적했다 [https://www.cs.vu.nl/~x/the_rise_and_fall_of_the_chaos_report_figures.pdf]:

1. 정의가 오도적임: 비용·기간·기능에 대한 추정 정확도만 기반으로 함
2. 일방향 측정: 추정값 초과달성도 성공으로 포함되지 않음, 비현실적 성공률 초래
3. 정책 왜곡: 정의에 따라 조직이 보수적 추정으로 변경, 좋은 추정 실무 저해
4. 편향된 평균: 서로 다른 추정 프로세스의 편향이 알려지지 않은 상태로 평균화됨

### [데이터] 실증 연구

Eveleens와 Verhoef는 1,211개 실제 프로젝트의 5,457개 예측 데이터(총액 수백 백만 유로 규모)를 분석했다. 이들의 데이터는 Standish 정의를 적용했을 때 보고된 성공률과 실제 조직의 추정 프로세스 간의 괴리를 보여준다 [https://www.cs.vu.nl/~x/the_rise_and_fall_of_the_chaos_report_figures.pdf].

---

## 3. McKinsey-Oxford 대규모 IT 프로젝트 연구 [데이터]

### 비용초과 및 성능 지표

McKinsey와 옥스포드 대학은 5,400개 이상의 IT 프로젝트($15M 이상 초기 예산)를 조사했다 [https://budgetoverrun.com/studies/mckinsey-large-it-projects]:

- **평균 비용초과**: 45%
- **평균 일정초과**: 7%
- **가치 전달 미달성**: 56% (예상 대비 미달)
- **심각한 위협 프로젝트**: 대규모 IT 프로젝트의 17%가 회사 존속을 위협할 정도의 비용초과 발생
- **총 비용초과액**: $66 billion (룩셈부르크 GDP 이상)

부문별 통계 [데이터] [https://budgetoverrun.com/statistics]:
- 건설 초대형 프로젝트(>$1B): 98% 초과, 평균 80% 초과
- IT/소프트웨어 프로젝트: 평균 45% 초과
- 정부 공공부문 IT: 개인 부문 대비 3배 높은 초과율
- 교통 기반시설: 86-90% 초과, 평균 28%

---

## 4. Boehm의 결함 수정 비용 곡선 [주장] [데이터]

### 원래 주장

Barry Boehm은 1970년대 후반 TRW, IBM, GTE의 63개 프로젝트 데이터를 기반으로 "Software Engineering Economics"(1981)에서 결함 수정 비용 곡선을 제시했다 [https://www.techwell.com/techwell-insights/2013/10/what-does-it-really-cost-fix-software-defect].

비용 단계별 비율 예시 [데이터]: 요구사항 단계 $1 → 설계 $10 → 코딩 $100 → 테스팅 $1,000 → 본 환경 $50-200배 [https://www.techwell.com/techwell-insights/2013/10/what-does-it-really-cost-fix-software-defect].

### [주장] 최근 수정 및 비판

2001년 Boehm과 Basili의 개정판은 소규모 agile 및 CI/CD 환경에서는 곡선이 완만하다고 보고했다. 소규모 비판적 시스템의 경우 비율이 100:1이 아닌 5:1 수준이라고 밝혔다 [https://reworkcost.com/boehm-cost-of-change-curve].


---

## 5. Cone of Uncertainty (McConnell) 및 비판 [정의/규정] [주장]

### [정의/규정] Cone of Uncertainty

Steve McConnell은 1996년 "Software Project Survival Guide"에서 프로젝트 초기에는 요구사항, 솔루션, 계획, 인원 등이 불명확하며, 이러한 변수들이 추정값의 변동성을 야기한다는 개념을 제시했다. 불확실성은 조사가 진행됨에 따라 감소하고, 초기 추정값의 변동 폭(cone)도 좁혀진다 [https://medium.com/pm101/cone-of-uncertainty-framework-78927c1840f].

### [주장] Little의 실측 연구 및 재보정의 부재

추정 정확도는 소프트웨어 정의의 세밀도에 따라 달라진다. 그러나 초기 추정 이후 불확실성을 재보정하려는 노력은 거의 이루어지지 않는다는 연구 결과가 있다 [https://medium.com/pm101/cone-of-uncertainty-framework-78927c1840f]. 초기에 설정된 추정값이 프로젝트 종료까지 유지되는 경향이 있으며, 실제 cone 축소가 의사결정에 반영되지 않는다.

---

## 6. Brooks의 법칙 (No Silver Bullet) [주장]

### 원문

Fred Brooks는 1986년(IEEE Computer Vol. 20, No. 4, 1987년 4월)에 "No Silver Bullet—Essence and Accident in Software Engineering"을 발표하여 다음과 같이 주장했다 [https://www.cs.unc.edu/techreports/86-020.pdf]:

"기술이든 관리 기법이든, 어떤 하나의 개발 방식도 생산성, 신뢰성, 단순성에서 한 자릿수 개선을 약속할 수 없다 (even one order of magnitude improvement)."

하드웨어(무어의 법칙)처럼 2년마다 2배 향상을 기대할 수 없으며, 본질적 복잡성(essential complexity)과 우발적 복잡성(accidental complexity) 간의 구분이 필요하다 [https://www.cs.unc.edu/techreports/86-020.pdf].

---

## 7. Scope Creep 측정 데이터 [데이터]

### PMI 통계

PMI의 2018년 "Pulse of the Profession"에 따르면, 지난 12개월 완료 프로젝트 중 52%가 scope creep 또는 통제되지 않은 범위 변경을 경험했다(5년 전 43%에서 상향). 이는 프로젝트 복잡도의 증가 추세(2013년 35% → 2018년 41%)와 함께 나타난다 [https://budgetoverrun.com/statistics].

### 재정 영향

프로젝트의 36%가 원래 예산을 초과하며, scope creep으로 인한 평균 비용초과가 약 27%에 이른다. 2026년 IPM 조사에서 45%는 불명확한 목표를 scope creep의 가장 빈번한 원인으로 꼽았다 [https://budgetoverrun.com/statistics].

성능 높은 프로젝트는 scope creep 비율이 낮고 실패 시에도 예산 손실이 적다 [https://budgetoverrun.com/statistics].

---

## 8. AI 도입 영향 수치 — Faros AI 블로그의 DORA 2025 리포트 정리 [데이터]

> 주의: 이 절의 수치는 DORA 리포트 원문이 아니라, Faros AI 블로그가 DORA 2025 리포트를 정리·소개하며 제시한 것이다. 원문 수치와의 대조는 별도 확인이 필요하다.

### [데이터] AI 도입률 및 개인 생산성

Faros AI 블로그가 DORA 2025 리포트(약 5,000명 응답)를 정리하며 제시한 수치 [https://www.faros.ai/blog/key-takeaways-from-the-dora-report-2025]:

- AI 도구 사용률: 95% (오버 80% 생산성 향상 보고)
- 완료 작업: +21% ~ +33.7%
- Merge된 Pull Request: 초기 +98%, 이후 +16.2%
- Epic 완료 (개발자당): +66.2%

### [주장] Amplifier Effect: 조직 수준에서의 결과

같은 블로그는 개인 생산성 증가에도 불구하고 조직 수준의 배포 지표는 정체 또는 악화되었다고 보고한다 [https://www.faros.ai/blog/key-takeaways-from-the-dora-report-2025]:

- 배포 빈도, Lead Time, Change Failure Rate: 정체 또는 압력 증가
- 버그 (개발자당): +54%
- PR당 사고(Incidents): +242.7%
- PR 리뷰 시간: +441%

같은 글은 "AI는 증폭기로 작동하며 기존 팀 상태를 증폭시킨다"는 해석을 제시한다 [주장]. 또한 2026년 데이터는 개선 신호를 보였으나 "비용"이 수반되었다고 기술한다 [https://www.faros.ai/blog/key-takeaways-from-the-dora-report-2025].

---

## 9. Jørgensen 소프트웨어 추정 연구 [데이터] [주장]

### Moløkken & Jørgensen 2003 메타분석

Moløkken과 Jørgensen은 2003년 국제 실증 소프트웨어 공학 심포지엄에서 발표한 조사 메타분석에서 다음 수치를 보고했다: 소프트웨어 프로젝트의 [데이터] 60~80%가 노력 또는 일정 초과를 경험하며, 평균 초과량은 [데이터] 30~40% [https://www.researchgate.net/publication/4038461_A_review_of_surveys_on_software_effort_estimation].

### 전문가 판단 vs 형식 모델

Jørgensen은 2004년 "A Review of Studies on Expert Estimation of Software Development Effort"에서 100개 발행물을 검토한 결과, [데이터] 83~84%의 추정이 순수 전문가 판단으로 수행되었다고 보고했다. Jørgensen은 "형식 모델이 더 정확한 추정을 초래한다는 실질적 증거가 없다"고 결론지었으며, 16개 검토 연구 중 10개에서 전문가 판단의 평균 정확도가 모델보다 높았다 [https://dl.acm.org/doi/10.1016/S0164-1212(02)00156-5].

### 인지 편향과 닻 효과

Jørgensen의 연구는 소프트웨어 개발자의 추정에서 수치 닻(numerical anchor)의 강력한 효과를 입증했다. 닻은 경험 많은 추정자의 추정을 약 [데이터] 2배 인자로 왜곡할 수 있으며, 인지 편향 인식 제고가 닻 효과를 감소시키지만 완전히 제거하지는 못한다고 보고했다 [https://dl.acm.org/doi/10.1016/j.jss.2015.03.015].

### 장기 개선 부재

Moløkken-Østvold과 Jørgensen의 분석은 "소프트웨어 추정 정확도에 수십 년간 실질적 개선이 없었다"고 지적했다 [https://www.researchgate.net/publication/259885547_A_Systematic_Mapping_of_Factors_Affecting_Accuracy_of_Software_Development_Effort_Estimation].

---

## 출처 목록

> [1차] = 원저자·원기관 발행 / [2차] = 제3자의 정리·집계

- [2차] https://budgetoverrun.com/studies/standish-chaos-report
- [2차] https://budgetoverrun.com/statistics
- [1차] https://www.cs.vu.nl/~x/the_rise_and_fall_of_the_chaos_report_figures.pdf
- [2차] https://www.techwell.com/techwell-insights/2013/10/what-does-it-really-cost-fix-software-defect
- [2차] https://reworkcost.com/boehm-cost-of-change-curve
- [2차] https://medium.com/pm101/cone-of-uncertainty-framework-78927c1840f
- [1차] https://www.cs.unc.edu/techreports/86-020.pdf
- [2차] https://www.faros.ai/blog/key-takeaways-from-the-dora-report-2025
- [2차] https://budgetoverrun.com/studies/mckinsey-large-it-projects
- [원문 사본·제3자 archive] https://opencommons.org/File%3AChaos_report_1994.pdf (1994 CHAOS 리포트의 archive file page; Standish 원 발행본 URL은 현재 공개 확인 불가)
- [1차] https://www.researchgate.net/publication/4038461_A_review_of_surveys_on_software_effort_estimation
- [1차] https://dl.acm.org/doi/10.1016/S0164-1212(02)00156-5
- [1차] https://dl.acm.org/doi/10.1016/j.jss.2015.03.015
- [1차] https://www.researchgate.net/publication/259885547_A_Systematic_Mapping_of_Factors_Affecting_Accuracy_of_Software_Development_Effort_Estimation
