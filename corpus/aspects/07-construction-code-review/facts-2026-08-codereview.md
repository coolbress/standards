---
id: aspect-07-construction-code-review--facts-2026-08-codereview
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

**리뷰 효율** — SmartBear가 시스코 팀을 대상으로 수행한 연구는 "200-400 LOC를 60-90분에 리뷰하면 70-90% 결함 발견율을 얻는다"고 보고했다 [https://smartbear.com/learn/code-review/best-practices-for-peer-code-review/]. "300 LOC/시간 이하의 검사 속도가 최고 결함 발견을 산출하며, 500 이하도 양호하다. 그 이상 속도에서는 상당한 결함 누락을 예상하라."

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
