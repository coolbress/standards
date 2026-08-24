---
id: aspect-07-construction-code-review--codereview--facts-2026-08
title: "Implementation & code review — facts (2026-08)"
parent: aspect-07-construction-code-review
kind: research-log
evidence_track: lit
status: draft
language: ko
last_updated: "2026-08-02"
method: "Haiku web-research agents, facts-only rules ([정의/규정]/[데이터]/[주장] labels), source-tier tagged [1차]/[2차]; session-lead verified"
---

# 코드리뷰 실무 구현 기준 및 연구

## 개요
코드리뷰 실무 기준은 구글, 마이크로소프트, 시스코 등의 대규모 조직에서 실증된 데이터와 오픈소스 표준에 의해 규정된다. 본 문서는 리뷰 규모, 속도, 발견율, git 워크플로우, 커밋 메시지 컨벤션의 원문 기준을 정리한다.

---

## 리뷰 규모 및 속도 [데이터]

**변경량 기준** — 구글 eng-practices는 "100줄은 보통 합리적, 1000줄은 보통 너무 큼"이라 규정한다 [https://google.github.io/eng-practices/review/developer/small-cls.html]. "파일 분산이 중요함: 파일 1개의 200줄 변경은 허용되나 50개 파일에 걸친 동일 변경은 보통 너무 크다."

**리뷰 효율** — ⚠️ **2026-08-24 재검증으로 정정됨.** 이전 판은 SmartBear **마케팅 페이지**를 인용해 *"200-400 LOC를 60-90분에 리뷰하면 70-90% 결함 발견율"* 이라 적었다. **1차 출처(케이스 스터디 원문 PDF)를 열어 보니 결론이 다르다** — 아래 claim table CR-001~004 참조.

### Claim table — SmartBear/Cisco 케이스 스터디 (1차 출처 직접 확인)

| Claim ID | Class | Claim and scope | Evidence | Confidence | 재검증 |
|---|---|---|---|---|---|
| **CR-001** | operational-lesson | 원문 결론 불릿: **"LOC under review should be under 200, not to exceed 400. Anything larger overwhelms reviewers and defects are not uncovered."** 즉 **권고는 200 미만이고 400은 상한**이다 — 400이 목표치가 아니다 | 1차 PDF `Conclusions` 절 | high (인용 정확도) / **low (일반화)** — 아래 CR-004 | 2026-08-24 |
| **CR-002** | operational-lesson | LOC 증가에 따른 효과 저하는 **200 부근에서 시작**한다: *"Anything below 200 lines produces a relatively high rate of defects… After that the results trail off considerably; no review larger than 250 lines produced more than 37 defects per 1000 lines."* **"급락(plummet)"이라는 표현은 LOC 에 쓰이지 않았다** | 1차 PDF | high | 2026-08-24 |
| **CR-003** | operational-lesson | 원문에서 *"Defect detection rates **plummet** after that time"* 는 **총 리뷰 시간(60분 초과·90분 상한)**에 대한 서술이지 **LOC 에 대한 것이 아니다** | 1차 PDF `Conclusions` 절 | high | 2026-08-24 |
| **CR-004** | limitation | 저자가 밝힌 한계 2건: ① 각주 5 — *"we're tacitly assuming that true defect density is constant over both large and small code changes"* ② *"we don't know how each of these reviews would have fared with a different process."* 표본은 **Cisco MeetingPlace 제품 그룹 1곳 · 개발자 50명 · 리뷰 2,500건 · 2005-07~2006-05** | 1차 PDF | high | 2026-08-24 |

> **분류가 왜 `operational-lesson` 인가**: [`EVIDENCE-POLICY`](../../methods/EVIDENCE-POLICY.md) §*Evidence hierarchy is claim-relative* 에서 **단일 조직의 1차 보고**는 operational-lesson 이고, 그 범주 오류는 ***"generalizing one organization to all teams"*** 다. 이것을 **효과·인과** 주장으로 쓰면(*"400줄 넘으면 결함 발견율이 급락한다"*) 재현 연구가 필요한데 **이 연구 하나로는 안 된다.**

### Claim table — 리뷰 속도·승인 절차 (R5-1 배치 A · 1차 출처 직접 확인)

| Claim ID | Class | Claim and scope | Evidence | Confidence | 재검증 |
|---|---|---|---|---|---|
| **CR-005** | industry-prevalence | Google 의 변경당 **수정 줄 수 중앙값은 24**: *"Over 10% of changes modify only a single line of code, and the median number of lines modified is 24."* ⚠️ 저자가 일반화 한계를 명시했다 — *"our results **may not generalize** to other contexts"* | [ICSE-SEIP 2018 원문 PDF](https://sback.it/publications/icse2018seip.pdf) | high (인용) / **low (일반화)** | 2026-08-24 **유지** |
| **CR-006** | industry-prevalence | ⚠️ **정정.** 이전 판은 *"리뷰 응답 실측 중앙값 4시간"* 이라 적었으나 원문은 **두 수치를 구분**한다: **첫 피드백까지의 대기**는 *"a median time of under an hour for small changes and about 5 hours for very large changes"*, **전체 리뷰 과정의 지연**이 *"under 4 hours"* 다. **4시간은 응답 시간이 아니라 전 과정 지연**이다 | 〃 | high | 2026-08-24 **수정** |
| **CR-007** | not-found | ⚠️ **1차 출처에서 찾을 수 없음.** *"빠른 리뷰 팀이 배포 성과 50% 높다"* 는 DORA 수치를 확인하지 못했다. `dora.dev` 능력 카탈로그에서 코드리뷰 관련 항목은 [`streamlining-change-approval`](https://dora.dev/capabilities/streamlining-change-approval/) **하나뿐**이고 거기에 그 수치가 없다 | 검색 실패 | — | 2026-08-24 **삭제 권고** |
| **CR-008** | misattribution | ⚠️ **오귀속.** *"다중 필수 승인자·형식적 체크리스트는 DORA 가 명시한 안티패턴"* 은 **DORA 가 한 말이 아니다.** DORA 가 비판한 것은 **CAB·고위 관리자 등 팀 외부의 중량급 변경 승인**이고, 오히려 **팀 내 동료 리뷰를 권장**한다: *"Use peer review to meet the goal of segregation of duties."* **동료 리뷰의 승인자 수와 체크리스트는 DORA 의 범위가 아니다** | [DORA streamlining-change-approval](https://dora.dev/capabilities/streamlining-change-approval/) | high | 2026-08-24 **삭제** |

> **CR-007·008 이 이 재검증의 요점이다.** 둘 다 *"DORA 가 그렇게 말한다"* 는 형태였는데, 하나는 **수치를 찾을 수 없었고** 하나는 **다른 대상에 대한 발견을 옮겨 붙인 것**이었다. 각주가 없어서가 아니라 **각주가 가리키는 곳에 그 말이 없어서** 틀렸다.

**재검증 기록 (배치 A)** — 검증일 `2026-08-24` · 검증자 `Claude Opus 5` + `codex-cli 0.145.0`(독립 질의, 결론 비공개) · **판정: 유지 1 · 수정 1 · 삭제 2** · **불일치 없음**(4개 항목 전부 일치. Codex 가 CR-008 을 자체 웹 검색으로 교차 확인) · 절차 [`reverification-protocol`](../../methods/reverification-protocol.md)

**재검증 기록** — 검증일 `2026-08-24` · 검증자 `Claude Opus 5` + `codex-cli 0.145.0` (독립 질의, 결론 비공개) · 1차출처 [`code-review-cisco-case-study.pdf`](https://static0.smartbear.co/support/media/resources/cc/book/code-review-cisco-case-study.pdf) · **판정 수정** · **불일치 없음**(4개 항목 전부 일치. Codex 가 한계 문장 1건을 추가로 발견) · 절차 [`reverification-protocol`](../../methods/reverification-protocol.md)

**검사 속도** — *"Inspection rates less than 300 LOC/hour result in best defect detection. Rates under 500 are still good; expect to miss significant percentage of defects if faster than that."* (1차 PDF `Conclusions`)

**반복 횟수** — "Modern Code Review: A Case Study at Google"(ICSE 2018)는 "80% 이상의 모든 변경이 최대 1회 반복만 거친다"고 기록했다 [https://doi.org/10.1145/3183519.3183525]. 리뷰어 수는 "보통 하나의 리뷰어만 필요하다"(소유권 및 가독성 요구사항 충족).

**리뷰 시간 절약** — "작은 CL에 대해 5분씩 여러 번 검토하는 것이 큰 CL의 30분 블록 검토보다 쉽다" [https://google.github.io/eng-practices/review/developer/small-cls.html].

---

## 리뷰 기준 [정의/규정]

**구글 기준** — "리뷰어는 CL이 시스템의 전체 코드 건전성을 명확히 개선하면 완벽하지 않아도 승인하는 것을 선호해야 한다" [https://google.github.io/eng-practices/review/reviewer/standard.html]. 평가 항목: 기능성(의도대로 동작하는가, 사용자에게 좋은가), 복잡성(단순화 가능한가), 테스트(올바르고 잘 설계되었는가), 명명(변수/클래스/메서드 이름이 명확한가).

**CL 설명 가이드** — 첫 줄은 "명령형으로 구체적으로 무엇을 하는지"를 요약해야 한다 [https://google.github.io/eng-practices/review/developer/cl-descriptions.html]. 예: "Delete the FizzBuzz RPC" vs "Deleting". 본문은 문제 맥락, 해결책 근거, 구현 결정, 한계, 버그 번호/벤치마크 결과를 포함한다. "Fix bug", "Add patch" 같은 설명은 부족하다.

---

## 마이크로소프트 코드리뷰 연구 [데이터]

**Bacchelli & Bird 2013** — 마이크로소프트 165명 관리자, 873명 개발자 조사 결과: "개발자들은 리뷰의 주목적을 결함 발견으로 여기나, 실제 성과는 다르다. 결함 발견보다 지식 이전, 팀 인식 제고, 대안 솔루션 창출이 더 흔하고 가치롭다" [https://codeclimate.com/blog/unexpected-outcomes-of-code-reviews]. "코드 및 변경 이해가 리뷰의 핵심 측면이며 개발자는 이해 필요를 충족하기 위해 광범위한 메커니즘을 활용한다(현 도구에서 대부분 미충족)."

---

## 페어프로그래밍 연구 [데이터]

**결함율** — 유타대학 실험: "페어는 15% 더 많은 개발자 시간을 소요했으나 솔루션 결함은 15% 적었다" [https://tuple.app/pair-programming-guide/scientific-research-into-pair-programming]. 한 연구는 "+18% 노력, -60% 결함"을 보고했다. "페어프로그래밍은 결함의 85-95%를 발견하고, 형식 코드리뷰는 60-70%를 발견한다." 이탈리아 제조업 회사의 14개월 산업 사례: "기존 코드 수정 시 페어프로그래밍으로 작성된 코드의 결함이 더 낮다."

---

## Git 워크플로우 규정 [정의/규정]

**Git Flow** — 여러 분기(master, develop, feature, release, hotfix) 사용 [https://medium.com/@patibandha/gitflow-vs-github-flow-vs-trunk-based-development-dded3c8c7af1]. "버전화되고 수동 조율이 필요한 대규모 엔터프라이즈에 적합."

**GitHub Flow** — 장기 분기 1개(main), 단기 feature 분기, 승인+CI 통과 후 병합 [https://medium.com/@patibandha/gitflow-vs-github-flow-vs-trunk-based-development-dded3c8c7af1]. "2-15명 팀의 웹 애플리케이션에 최적."

**Trunk-Based Development** — 단일 trunk(또는 main)를 소스 진실의 원천으로, 모든 팀원이 공유 분기에서 작업 [https://trunkbaseddevelopment.com/]. "Feature 분기는 시간 단위(일 단위 아님)로 유지. CI/CD 자동화 및 feature flag 필요." "개발자는 하루에 여러 번 trunk에 커밋. 모든 팀원은 24시간마다 최소 1회 trunk에 커밋(연속 통합)." "Google의 35,000명 개발자가 단일 저장소에서 협업."

---

## 커밋 메시지 컨벤션 [정의/규정]

**Conventional Commits** — 형식: `<type>[optional scope]: <description> [optional body] [optional footer(s)]` [https://www.conventionalcommits.org/en/v1.0.0/]. 필수 타입: `feat`(기능, MINOR), `fix`(버그, PATCH). 선택적: build, chore, ci, docs, style, refactor, perf, test. 파괴적 변경은 `!` prefix (예: `feat!:`) 또는 `BREAKING CHANGE:` footer로 표시. "타입 뒤 필수 콜론-공백, 본문은 공백 1줄 후, footer는 token-separator-value 형식."

---

## 출처

> ⚠️ 2026-08-24 재검증에서 **1차 출처가 추가됐다.** 이전 판은 벤더 마케팅 페이지만 인용했다.
> Code Review at Cisco Systems (SmartBear, 2006 · 케이스 스터디 원문 PDF):
> https://static0.smartbear.co/support/media/resources/cc/book/code-review-cisco-case-study.pdf
>
> Modern Code Review: A Case Study at Google (ICSE-SEIP 2018 · 원문 PDF):
> https://sback.it/publications/icse2018seip.pdf
>
> DORA — Streamlining change approval:
> https://dora.dev/capabilities/streamlining-change-approval/

> [1차] = 원저자·원기관 발행 / [2차] = 제3자의 정리·집계

- [1차] https://google.github.io/eng-practices/review/developer/small-cls.html
- [1차] https://google.github.io/eng-practices/review/reviewer/standard.html
- [1차] https://google.github.io/eng-practices/review/developer/cl-descriptions.html
- [1차] https://doi.org/10.1145/3183519.3183525 (ICSE 2018 Modern Code Review: A Case Study at Google)
- [1차] https://smartbear.com/learn/code-review/best-practices-for-peer-code-review/
- [2차] https://codeclimate.com/blog/unexpected-outcomes-of-code-reviews (Bacchelli & Bird 2013)
- [2차] https://tuple.app/pair-programming-guide/scientific-research-into-pair-programming
- [2차] https://medium.com/@patibandha/gitflow-vs-github-flow-vs-trunk-based-development-dded3c8c7af1
- [1차] https://trunkbaseddevelopment.com/
- [1차] https://www.conventionalcommits.org/en/v1.0.0/
