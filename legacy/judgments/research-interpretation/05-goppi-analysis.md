---
title: "기존 goppi (~/goppi) 분석"
kind: prior-art
status: historical
last_updated: 2026-08-02
language: ko
---

> 📇 **검색 등급: `reference`** — 물어봤을 때만 열린다(첫 홉 아님).
> 프론트매터는 2026-08-08에 **추가**됐다(본문 무수정). 이유: 라우터가 이 파일을 `active`로 잡고 있었는데,
> **분석 대상인 구 goppi는 2026-08-04에 제거됐다**(`~/Archive/goppi-removal-2026-08-04/`).
> 첫 홉에 구 세대 분석이 필요한 작업은 없다 — `kind: prior-art` 가 등급을 `reference` 로 내린다.
> ⚠️ 형제 파일 `00~04` 는 프론트매터가 없고 본문 SUPERSEDED 배너로만 표시된다.
> 이 층은 프론트매터를 쓰지 않는 관례였고, 이 파일만 예외로 둔 것은 **라우터가 오분류했기 때문**이다.

# 기존 goppi (~/goppi) 분석 — 2026-08-02

> goppi_final 재설계의 기초 자료. 분석 대상: `/Users/coolbress/goppi` @ commit `7f57f9a` (96 커밋, 이슈/PR ~150개, 첫 커밋 2026-07-21).

## 현재 구조

- **3층**: L0 = 5조항 계약(GOPPI.md, 52줄, ~1.4k 토큰 상시) · L1 = 스킬 6개(kickoff·scaffold·review·ship·harness-eval·governed) + reference 10개 + 템플릿 · L2 = 훅 3개(secret-guard·precompact-snapshot·deploy-check) + 권한 deny/ask + 샌드박스.
- **자기 검증 장치**: ADR 41개, `check.sh` 산하 accounting 체커 ~15종, worth 평가(WITH/WITHOUT), mutation harness(103 뮤테이션 · 683 케이스), harness-vs-vanilla 통제 페어 6개, 스킬 본문 토큰 실측(스위트 24,857/25,000 예산).
- 듀얼 호스트(Claude Code + Codex), 영어 canonical.

## 지킬 가치가 있는 자산

1. **정직한 측정 문화** — Iron Law, n=1을 n=1로 기록, 실패·철회·discard까지 기록. 재설계의 핵심 계승 대상.
2. **위험 비례 원칙** (Direct/Structured/Governed) + "불확실한 리스크는 상승된 리스크".
3. **집행의 분리에 대한 정확한 인식** — 계약 문구는 advisory, 진짜 게이트는 권한/훅/샌드박스 (§4.3). 리서치 04의 "자연어는 게이트가 아니다"(Replit 사건)와 정합.
4. **kickoff** — 통제 비교에서 유일하게 가치가 측정된 스킬 (14 vs 3, KEEP). 승부처는 첫 질문이 아니라 "지속된 인터뷰".
5. thin-contract + progressive disclosure 아키텍처 방향 자체 — 리서치 04의 공식 권고와 일치.

## 문제 (사용자 직감이 goppi 자체 데이터로 확인됨)

### 1. 라이프사이클 커버리지 skew
현업 루프(문제 심문→스펙→설계→구현→검증→릴리스→운영) 중 goppi가 커버하는 것은 스펙 일부(kickoff, 기본 침묵) · 셋업(scaffold) · 리뷰(review) · **전달 세리머니(ship)** 뿐. 빠진 것: 설계 결정(ADR-lite 루프), 수직 슬라이스/walking skeleton 계획, 사용자 제품의 테스트 전략, 디버깅 루프, appetite/circuit-breaker, 배포·운영. orient(G2)는 미구현. → "github workflow에만 집중" 직감은 구조적 사실.

### 2. 근본 리서치의 방향 오류
design.md §3의 리서치는 전부 "하네스를 어떻게 만들 것인가"(Anthropic/OpenAI 하네스 설계, 스캐폴딩 논문, SDD 도구 시장)였고, "소프트웨어는 현업에서 어떻게 만들어지는가"(SDLC, 요구사항 공학, 테스트 전략, 릴리스 관행)는 리서치된 적 없음. 하네스가 인코딩해야 할 대상 지식이 빠짐. → 이번 research/01~04가 그 공백을 채움.

### 3. advisory 레이어의 가치 미입증 (goppi 자신의 측정)
harness-vs-vanilla 페어 6개: 5개 델타 0, 1개(review-precision)는 하네스 쪽이 오탐 1개로 미세하게 해로움. 토큰 오버헤드는 +13.8% ~ 2.7배. kickoff만 예외적으로 명확한 양의 마진. ship 본문 ablation은 6개 기준 중 1개(포지 참조 날조 방지)만 신뢰성 있게 차별화 — 4,964 토큰 중 대부분은 계약만으로 충족.

### 4. 규칙에 운반체(carrier)가 없었음 (ADR-0041)
"모델이 goppi 의도대로 작동 안 함"의 대부분은 모델 문제가 아니라 전달 경로 문제: GOPPI.md에 issue/PR/ship 언급 0회, 스킬이 `.claude/skills/`에 없어 호출 불가, 모든 게이트는 존재하는 산출물의 모양만 검사해 **누락은 어디에도 안 보임**. 세션 Q⑤에서 3중 위반이 CI 녹색으로 통과.

### 5. 하네스가 자신을 소비
최근 세션들(M·N·Q·R·T·T2)의 작업은 거의 전부 goppi가 goppi를 검증하는 메타 작업(자기 테스트 스위트의 뮤테이션 커버리지, 커버리지 리포터의 크레딧 버그, 토큰 마진 21토큰 단위 관리). ~3천 줄 마크다운 하네스에 683 케이스·103 뮤테이션의 검증 장치. 유지비가 원래 목적(비개발자의 소프트웨어 빌드)의 개발 용량을 잠식 — "결과 우선"이 하네스 자신에게 미적용된 역설.

## 종합 판정

goppi는 "시니어의 전달 규율 + 정직성 문화" 인코딩에는 성공했으나 "소프트웨어 프로젝트가 어떻게 진행되는가"라는 본체가 빠져 있다. 뼈대(계약·비례 원칙·L2 집행·측정 문화·kickoff)는 계승 가치가 높다. 재설계의 방향은 research/00-overview.md의 결론과 동일: **절차 지시가 아니라 (a) 현업 루프의 인코딩 — 문제 심문→얇은 스펙→walking skeleton→수직 슬라이스→검증, (b) 기계가 확인 가능한 완료 정의(검증 표면), (c) 규칙이 실제로 모델 컨텍스트에 도달하는 운반체 설계.**

2026-08-02 이후의 고정된 제품 판정 기준은
[`foundation/worth-hypothesis.md`](foundation/worth-hypothesis.md), 산출물 수용 기준은
[`foundation/production-output-rubric.md`](foundation/production-output-rubric.md)가 우선한다. 이 문서의
과거 평가는 그 가설을 만들게 한 local evidence이지, 새 하네스의 가치 증명이 아니다.
