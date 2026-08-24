---
id: aspect-27-ai-harness-archetype--facts-2026-08-compliance-verification
title: "Agent process-compliance verification — facts (2026-08)"
parent: aspect-27-ai-harness-archetype
kind: research-log
evidence_track: lit
status: draft
language: ko
last_updated: "2026-08-02"
review_due: "2026-11-02"
method: "Haiku web-research, facts-only, EVIDENCE-POLICY conformant; search log included"
---

# 에이전트 프로세스 준수 검증 — 팩트 문서 (2026-08)

## 조사 기록

**조사 범위**: 에이전트 동작 및 프로세스 준수 검증 방법; 궤적 평가(trajectory evaluation), 결정론적 게이트, 관찰가능성(observability) 표준.

**제외 항목**: 특정 공급업체의 미공개 구현; 학술지 미수록 블로그/뉘앙스; 주장되지만 문헌으로 검증되지 않은 방법.

**검색 실행일**: 2026-08-02  
**검색식**:  
1. "OpenAI Evals graders trajectory evaluation" (OpenAI 공식 문서)
2. "tau-bench agent trajectory evaluation policy compliance pass-k" (논문)
3. "OpenTelemetry GenAI semantic conventions agent tool" (표준)
4. "SWE-bench verified methodology deterministic" (검증 방법)
5. "LLM judge evaluation bias position verbosity" (연구 논문)
6. "Claude Code hooks PreToolUse exit code deterministic verification" (공식 문서)

**포함 기준**: OpenAI/Anthropic 공식 개발자 문서, 발표된 학술 논문 (arXiv/NeurIPS/OpenReview), 산업 표준 (OpenTelemetry), 벤더 공식 지침서만.

---

## 1. 궤적/에이전트 평가 방법

### 1.1 OpenAI Evals: 그레이더 유형

[규정] OpenAI Evals 플랫폼은 4가지 기본 그레이더 유형을 정의함 [developers.openai.com/api/docs/guides/graders]:

- **String Check Grader**: 정확 매칭 (동일성, 부분문자열, 대소문자 무시). 0 또는 1을 반환. [데이터]
- **Text Similarity Grader**: 퍼지 매칭, BLEU, ROUGE, 코사인 유사도. 졸업식 점수(graduated scores) 반환. [데이터]
- **Model Grader**: LLM을 심사자로 위임. 숫자 점수(지정 범위 내) 반환. [정의]
- **Python Grader**: 사용자정의 코드 실행. grade 함수는 정확히 2개 인수를 받고 float 값 출력. [규정]

[주장] 도구 호출(tool calls) 평가 시 함수 이름과 인수를 별도로 검사한 후 수식으로 점수 결합 가능. 텍스트 유사성/모델 그레이더는 매개변수 형식 차이로 인한 "과소 보상"에 대비 권장됨. [developers.openai.com/api/docs/guides/graders]

[데이터] OpenAI는 2026년 10월 31일 기존 사용자에 대해 Evals를 읽기 전용으로 전환하고, 11월 30일 종료 예정. [developers.openai.com API docs]

### 1.2 OpenAI Agent Evals: 궤적 수준 평가

[정의] "Trace grading"은 모델 호출, 도구 사용, 보안정책, 핸드오프의 종단간(end-to-end) 기록을 캡처하여 구조화된 기준으로 점수 매김. [데이터] 문제(workflow violate instruction/safety policy)는 trace-grading 프레임워크에 내장. [developers.openai.com/api/docs/guides/agent-evals]

[정의] 2단계 평가: (1) 정성적 trace 검사 (초기 워크플로우 문제 식별) → (2) 양적 eval run으로 확장 (벤치마킹). [developers.openai.com/api/docs/guides/agent-evals]

### 1.3 τ-bench: pass^k 메트릭과 정책 준수

[규정] τ-bench(도구-에이전트-사용자 상호작용 벤치마크)는 데이터베이스 상태 종료를 주석 처리된 목표 상태와 비교하는 결정론적 평가 사용. 대화 궤적 변동에 무관함. [arXiv:2406.12045]

[정의] **pass^k**: 에이전트가 k번의 독립적 시행 모두에서 성공할 확률. pass@k(최소 1회 성공)와 구별됨. 대화 확률성 하에서의 일관성 측정. [arXiv:2406.12045]

[데이터] 정책 준수 점수: 각 도메인(소매, 항공)에 서면 정책 문서 포함. 각 궤적을 프로그래밍 방식으로 평가—"resolution-pass"(사용자 의도 만족) + "policy-pass"(정책 위반 없음). [arXiv:2406.12045]

[데이터] GPT-4o 실험: pass^1 (소매) <50%, pass^8 (소매) <25%. 단일 불운한 시뮬레이터 경로가 경계 시나리오 뒤집을 수 있음. [arXiv:2406.12045]

### 1.4 SWE-bench Verified: 결정론적 검증과 인간 검증의 혼합

[규정] SWE-bench Verified는 OpenAI와 협력하여 GitHub 문제 500개를 인간 주석자가 필터링—문제 설명 명확성, 테스트 패치 정확성, 주어진 정보로 해결 가능성 검증. [www.swebench.com/verified.html]

[데이터] 평가 절차: 후보 패치 적용 → 단위 테스트 스위트 호출 → 모두 통과 시 성공 선언. 결정론적(deterministic) pass/fail 오라클. [www.swebench.com/verified.html]

[주장] Pass@1 및 PatchDiff(테스트 부실과 행동 불일치 발굴)를 통해 품질 게이트 다층화. 코드 리뷰 서브에이전트를 추가 게이트로 사용 가능. [arXiv search results on SWE-bench]

---

## 2. LLM-as-Judge: 편향과 보정

### 2.1 확인된 편향

[규정] LLM 심사자에서 3가지 주요 편향 확인: 

- **Position Bias**: 응답 순서에 따른 체계적 선호도. 특정 위치에 제시된 응답 선호.
- **Verbosity Bias**: 길이와 품질 혼동. 더 긴 응답에 대한 보상 경향.
- **Self-Preference Bias**: 동일 모델 패밀리 출력에 대한 선호도. 원형(circular) 평가 문제.

[문헌] "MM-JudgeBias" (2026): MLLM 심사자는 position bias보다 verbosity bias에 더 취약. [arXiv:2604.18164]

[문헌] "The Coin Flip Judge?" (2026): 위치 효과 완화 위해 swap-augmented evaluation(재정렬로 여러 라운드) 제안. 분산 분해(variance decomposition)로 편향 기여도 격리 정량화. [arXiv:2606.13685]

[문헌] 다중 평가 라운드(ordering 변경), 프롬프트 엔지니어링, 다수결 투표로 신뢰성 개선. 일부 결과는 무작위 확률과 거의 차이 없음. [arXiv:2606.13685]

### 2.2 인간-일치 보고 실무

[규정] 논문 평가 방법론에 인간 동의율(inter-annotator agreement, Kappa, 정확도) 보고 기대—벤더 가이드라인 부재. 개별 학술 출판 관행. [meta-research across cited papers]

---

## 3. 결정론적 검증: 훅과 종료 코드

### 3.1 Claude Code: Stop 훅

[규정] Stop 훅은 Claude가 응답 후 턴(turn)을 종료 직전에 실행. [code.claude.com/docs/en/hooks]

[데이터] 사용 사례: (1) 종료 후 상태 검증, (2) 조직 정책 준수 확인, (3) 감사 로깅, (4) 환경 상태 예상 확인.

[정의] Stop 훅 결정: `decision: "block"` (이유 제시) → Claude가 턴 종료 방지, 대화 계속. Exit code 2도 동일 효과.

[정의] 또는 `additionalContext`로 피드백 삽입하여 Claude가 계속 진행하도록 유도 가능.

### 3.2 Claude Code: PreToolUse 훅

[규정] PreToolUse는 도구 매개변수 생성 후, 도구 호출 처리 전 실행. Bash, Edit, Write, Read, Glob, Grep, Agent, WebFetch, WebSearch, MCP 도구 모두 적용 가능. [code.claude.com/docs/en/hooks]

[데이터] 결정: `allow`(허용), `deny`(차단), `ask`(사용자 승인 요청), `defer`(이 훅 결정 생략).

[데이터] Exit code 2 = 차단 오류, stderr → Claude에 오류 메시지 전달. Exit code 0 = 이의 없음, 정상 진행.

[규정] 입력 수정 가능: `updatedInput` 필드로 도구 인수 재작성 (예: 대시 명령 주입 방지). [code.claude.com/docs/en/hooks]

[정의] 여러 PreToolUse 훅이 updatedInput 반환 시 마지막 완료 훅이 적용. 훅 병렬 실행 → 순서 비결정론적.

### 3.3 결정론적 규정 준수 검사 예시

[규정] Stop 훅을 테스트 스위트, 빌드 종료 코드, 린터, 출력 대 픽스처 diff, 브라우저 스크린샷 대 디자인 비교로 사용 가능—턴 종료 전 검사 통과 필수. [code.claude.com/docs/en/hooks]

[데이터] 예: `rm -rf` 차단 Bash 훅—PreToolUse matcher "Bash(rm *)"로 구성하면 명령 정규식 매칭 시 hook 스크립트 실행, permissionDecision "deny" 반환.

---

## 4. 관찰가능성 표준: OpenTelemetry GenAI

### 4.1 의미론적 컨벤션(Semantic Conventions)

[규정] OpenTelemetry GenAI 시맨틱 컨벤션은 에이전트 동작을 3가지 신호로 캡처: Traces, Metrics, Events. [opentelemetry.io/blog/2025/ai-agent-observability/]

[정의] Span 트리: 최상위 `invoke_agent` 스팬, 각 LLM 호출마다 `chat` 자식 스팬, 각 도구 호출마다 `execute_tool` 스팬. 채팅봇 → 에이전트 → MCP → 마이크로서비스 → 사용자까지 분산 추적. [opentelemetry.io/blog/2026/genai-observability/]

### 4.2 표준화된 속성(Attributes)

[데이터] 캡처 속성:
- `gen_ai.request.model` (예: gpt-4o)
- `gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens`
- `gen_ai.response.finish_reasons` (예: stop, tool_calls)
- 콘텐츠 기록 시: `gen_ai.system_instructions`, `gen_ai.input.messages`, `gen_ai.output.messages`

[정의] 프레임워크별로 공통 표준 준수하며 프레임워크 벤더별 컨벤션 정의 가능—표준화된 메트릭/추적/로그로 관찰성 솔루션 통합 용이. [opentelemetry.io/docs/specs/semconv/]

---

## 5. 프로세스 준수: 공식 방법

### 5.1 τ-bench 정책 준수 점수

[규정] τ-bench는 "policy-pass" 평가를 프로그래밍 방식 구현: 각 궤적을 도메인 정책 문서와 비교하여 정책 위반 감지. [arXiv:2406.12045]

[정의] 이는 τ-bench를 다른 벤치마크와 구별하는 방법론적 핵심. "resolution-pass"(목표 달성)와 독립적. [arXiv:2406.12045]

### 5.2 Claude Code 훅을 통한 준수 감시

[규정] PreToolUse/Stop 훅으로 모든 도구 호출 로깅, 감시, 규정 준수 감시 가능. 민감한 작업에 인간 승인 요구 가능. [code.claude.com/docs/en/hooks]

[정의] 훅은 입출력 데이터 삭제(sanitization)를 통해 규정 준수 자동화 가능—구체적 실행 방법은 조직별 구현.

---

## 6. 미해결 영역: 공식 표준 부재

### 6.1 표준화되지 않은 영역

[주장] 다음 영역에서는 발표된 표준 방법 부재:

- **Skill-invocation compliance metrics**: 에이전트가 "규정된 워크플로우를 따랐는가"를 정량화하는 표준화된 메트릭 부재. τ-bench의 "policy-pass"는 정책 문서 준수이지 프로세스 워크플로우 준수 아님.
- **Constitution-based compliance in agents**: AI Constitution(헌법) 기반 에이전트 준수 검증의 표준화된 공개 방법 부재.
- **Cross-framework compliance auditing**: 서로 다른 에이전트 프레임워크 간 준수 메트릭 표준화 부재.

[정의] OpenAI/Anthropic 공식 문서에서도 "에이전트 X가 요구된 의사결정 트리를 따랐는가"를 정량화하는 공식 방법 미제시.

### 6.2 진행 중인 표준화

[주장] OpenTelemetry GenAI 컨벤션은 2025~2026년 확장 진행 중 (agent/tool span 표준화 동안). 프로세스 준수 스팬 속성은 아직 미정의 (추측 불가).

---

## 출처

### [1차] 공식 개발자 문서

- [OpenAI Evals Graders Guide](https://developers.openai.com/api/docs/guides/graders)
- [OpenAI Agent Evals Guide](https://developers.openai.com/api/docs/guides/agent-evals)
- [Claude Code Hooks Reference](https://code.claude.com/docs/en/hooks)
- [OpenTelemetry GenAI Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/)

### [2차] 학술 논문

- [τ-bench: A Benchmark for Tool-Agent-User Interaction](https://arxiv.org/abs/2406.12045) — pass^k, 정책 준수 점수
- [SWE-bench Verified](https://www.swebench.com/verified.html) — 인간 검증, 결정론적 테스트
- [MM-JudgeBias: Multimodal MLLM Judge Biases](https://arxiv.org/pdf/2604.18164)
- [The Coin Flip Judge? Reliability and Bias in LLM-as-a-Judge](https://arxiv.org/pdf/2606.13685) — position, verbosity, self-preference bias; swap-augmented evaluation
- [Self-Preference Bias in LLM-as-a-Judge](https://arxiv.org/abs/2410.21819)

### [2차] 산업 블로그/표준

- [OpenTelemetry: GenAI Observability 2025-2026](https://opentelemetry.io/blog/2025/ai-agent-observability/)
- [OpenTelemetry: Inside the LLM Call 2026](https://opentelemetry.io/blog/2026/genai-observability/)
