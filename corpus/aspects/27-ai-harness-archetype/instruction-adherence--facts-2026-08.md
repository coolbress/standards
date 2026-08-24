---
id: aspect-27-ai-harness-archetype--instruction-adherence--facts-2026-08
title: "LLM/agent instruction adherence — empirical facts (2026-08)"
parent: aspect-27-ai-harness-archetype
kind: research-log
evidence_track: lit
status: draft
language: ko
last_updated: "2026-08-02"
review_due: "2026-11-02"
method: "Haiku web-research, facts-only, EVIDENCE-POLICY conformant; search log included"
---

## 조사 목표
LLM과 에이전트가 지시사항을 따르는 신뢰성에 관한 측정 가능한 증거 수집. 성능 저하 조건, 벤치마크 데이터, 벤더 공식 입장.

## 조사 범위·제외
**포함**: 학술 논문(arxiv, ACL), 벤더 공식 엔지니어링 포스트, 측정된 수치 있는 연구.  
**제외**: 제품 마케팅, 재현 불가 주장, 추측.

## 조사 기록
- **일시**: 2026-08-02
- **검색식**: IFEval benchmark, "Lost in the Middle", context degradation, Anthropic instruction adherence, agent failure modes, long-horizon task adherence
- **포함 기준**: URL 인증 가능, 수치 근거, 재현 가능한 벤치마크

---

## 1. 명령 따르기 벤치마크: IFEval

**IFEval** [정의]: 자동으로 검증 가능한 지시사항 25가지 유형에 기반한 명령 준수 평가 벤치마크. 약 500개 프롬프트로 구성. "400단어 이상 작성", "AI 키워드 최소 3회 언급" 같은 객관적 지시사항을 측정. [1차: https://arxiv.org/abs/2311.07911]

**확장 연구**: M-IFEval는 영어 한정을 넘어 프랑스어, 일본어, 스페인어로 확대 [https://arxiv.org/abs/2502.04688]; IFEval-Audio는 음성 LLM의 명령 따르기 능력 평가 [https://arxiv.org/abs/2505.16774].

벤치마크 세부 성능 수치는 원문 참조 필요 [미측정].

---

## 2. 맥락 위치 효과: "Lost in the Middle"

**현상** [주장]: 정보가 맥락의 시작이나 끝에 있을 때 성능 최고, 중간에 위치할 때 급격히 저하. U자 곡선 성능 패턴 [1차: https://arxiv.org/pdf/2307.03172].

**범위**: 멀티 문서 QA, 키값 검색 작업에서 확인. 오픈소스/폐쇄 모델 모두 영향받음 [정의/규정].

**수치**: 원문 PDF는 기술적으로 추출 불가 상태. 일반적 결론만 인증: 중간 위치 정보 처리에서 성능 급격히 저하 현상 확인 [데이터: 정도 미측정].

---

## 3. 긴 맥락에서 성능 저하: 지시사항 수 효과

**"Prompt Design at Scale"** 연구 [1차: https://arxiv.org/html/2607.19257]는 지시사항 개수·형식·맥락 길이가 명령 준수와 환각에 미치는 영향 측정.

**지시사항 수에 따른 성능 붕괴** [데이터]:
- N=10 지시사항: 58.8–93.8% 완벽 응답률
- N=80: 모든 모델 ~0% 붕괴  
- N=120–160: "모든 모델 사실상 0% 완벽 응답" [정의/규정]

임계값 효과: 형식 선택 무관하게 나타남.

**맥락 길이와 회상률** [데이터]:
- 512k 토큰 실험에서 64–128k 토큰까지 회상 정확도 0.98–1.00 유지
- 이후 형식에 따라 저하, 최대 48 퍼센트포인트 차이 발생
- **주요 실패 모드**: 환각이 아니라 **거부율이 79–90%까지 상승** (맥락 한계 근처)
- "0/5,760 absent-fact 탐침에서 거짓 정보 생성 없음" [데이터: 환각 부재]

---

## 4. Anthropic 공식 입장: 맥락 및 지시사항 준수

**"Effective Context Engineering for AI Agents"** [1차: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents]:
- 토큰 수 증가에 따라 맥락 회상 능력 저하. "모든 모델에서 나타남, 다만 저하 기울기는 모델마다 다름" [주장]
- **"성능 경사" 패턴**: 급격한 절벽 아닌 점진적 저하 [정의/규정]
- 시스템 프롬프트 크기 효과에 대한 구체적 수치 **없음** [미측정]

**결론**: Anthropic은 맥락을 유한 자원으로 대우하되, 정확한 저하 임계값이나 시스템 프롬프트 블로트 영향 수치 미공개.

---

## 5. 에이전트별 준수 실패: 장기 작업

**METR 분석** [1차: https://arxiv.org/html/2604.11978v1]:
- 장기 작업 실패는 **토큰당 추론 품질 저하가 아니라 상태 관리 붕괴**에서 비롯 [주장]
- 주요 실패 경로: 정보 추적, 지시사항 제약(파일 형식, 명명 규칙) 유실, 상태 일관성 상실 [정의/규정]
- "에이전트가 새 기능에 집중하다 광범위 맥락 상실 → 기존 기능 의도하지 않은 파괴" [주장]

**워크플로 붕괴** [주장]: 장기 수평 작업 실패는 개별 추론이 아니라 계획·검증·일관성 유지 불가에서 발생 [정의/규정].

수치 데이터: METR 벤치마크별 실패율·성공률 구체 수치는 미제공 [미측정].

---

## 6. 미해결 항목

**증거 부족 영역**:
- 시스템 프롬프트 크기 임계값("80% 제거 → 측정 불가" 클레임 미확인) [미측정]
- 스킬 트리거 신뢰도 비율 공개 데이터 부재 [미측정]
- 명령 우선순위 계층 준수 측정 (Anthropic/OpenAI 공식 평가) [미측정]
- 에이전트 단계 스킵 정량 분석(SWE-bench 궤적 공개 집계) [미측정]

---

## 출처

### [1차] 학술 논문/벤더 공식
- https://arxiv.org/abs/2311.07911 — IFEval: Instruction-Following Evaluation for LLMs (2023)
- https://arxiv.org/pdf/2307.03172 — Lost in the Middle: How Language Models Use Long Contexts (Liu et al., 2024)
- https://arxiv.org/html/2607.19257 — Prompt Design at Scale: Format, Instruction Count, Context Length Effects (2026)
- https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents — Anthropic Engineering: Effective Context Engineering
- https://arxiv.org/html/2604.11978v1 — METR: Long-Horizon Task Failure Diagnosis

### [2차] 관련 확장 연구
- https://arxiv.org/abs/2502.04688 — M-IFEval: Multilingual variant
- https://arxiv.org/abs/2505.16774 — IFEval-Audio: Audio LLM variant
- https://arxiv.org/html/2512.04307 — Long-Context Reasoning in WebAgents
