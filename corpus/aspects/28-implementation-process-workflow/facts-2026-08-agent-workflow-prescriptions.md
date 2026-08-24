---
id: aspect-28-implementation-process-workflow--facts-2026-08-agent-workflow-prescriptions
title: "AI-agent development workflow prescriptions — facts (2026-08)"
parent: aspect-28-implementation-process-workflow
kind: research-log
evidence_track: lit
status: draft
language: ko
last_updated: "2026-08-02"
review_due: "2026-11-02"
method: "Haiku web-research, facts-only, EVIDENCE-POLICY conformant; search log included"
---

## 조사 기록

**질문**: AI-agent 개발 환경(GitHub Spec Kit, Amazon Kiro, Anthropic Claude Code, OpenAI Codex, Cursor/Windsurf/Devin)이 개발 workflow를 어떻게 규정하는가?

**범위**: 공식 문서, 판매자 블로그, 명시된 저자의 비판 기사 수집. BMAD/OpenSpec는 검색 결과 부족으로 제외.

**검색일**: 2026-08-02

**검색식 목록**:
- GitHub Spec Kit workflow prescriptions (2024–2025)
- Amazon Kiro requirements.md/design.md/tasks.md specification
- Anthropic Claude AI agent workflow best practices (2026)
- OpenAI Codex agents workflow prescriptions
- Scott Logic Spec Kit critique overhead measurement (2024–2025)
- Cursor Windsurf Devin workflow prescriptions

**포함 기준**: 워크플로우 단계, 각 단계의 산출물, 규정된 프로세스 모델을 명시하는 출처만 수록.

---

## GitHub Spec Kit [1차]

[정의/규정] GitHub Spec Kit은 "Spec → Plan → Tasks → Implement" 4단계 workflow를 기본 제시. 각 단계는 Markdown artifact를 생성하여 다음 단계에 전달 [https://github.github.com/spec-kit/]

[정의/규정] 핵심 구성요소는 "Constitution" — project의 불가변 원칙을 담은 항구적 규칙 파일로, 모든 후속 명령이 참조 [https://github.github.com/spec-kit/]

[정의/규정] 산출물: rich templates, quality checklists, cross-artifact analysis를 포함. 25개 이상의 presets, 138개 이상의 community extensions 제공 [https://github.github.com/spec-kit/]

[정의/규정] 확장된 예시 프로세스: AIDE (7 step), Canon (baseline-driven), Product Forge (product-management-focused), FX→.NET (7-phase .NET migration), MAQA (multi-agent + QA checkpoints) [https://github.github.com/spec-kit/]

---

## Amazon Kiro [1차]

[정의/규정] Kiro는 3단계 spec model 처방: Requirements/Bug Analysis → Design → Tasks [https://kiro.dev/docs/specs/]

[정의/규정] Requirements 단계: user stories + acceptance criteria 형식, EARS (Easy Approach to Requirements Syntax) 표기법 사용. "WHEN [condition/event] THE SYSTEM SHALL [expected behavior]" 형식 [https://kiro.dev/docs/specs/]

[정의/규정] Design 단계: 기술 아키텍처, sequence diagrams, data flow, error handling, testing strategy 문서화 [https://kiro.dev/docs/specs/]

[정의/규정] Tasks 단계: discrete, trackable implementation tasks. Kiro는 tasks.md의 dependency graph를 구축하여 waves로 그룹화. Waves는 순차 실행, wave 내 tasks는 동시 실행 [https://kiro.dev/docs/specs/]

[정의/규정] 각 단계의 산출물: requirements.md (또는 bugfix.md), design.md, tasks.md [https://aws.amazon.com/blogs/industries/from-spec-to-production-a-three-week-drug-discovery-agent-using-kiro/]

---

## Anthropic Claude Code [1차]

[정의/규정] Claude Code는 4단계 권장 workflow 처방: Explore → Plan → Implement → Commit [https://code.claude.com/docs/en/best-practices]

[정의/규정] Explore: plan mode에서 파일 읽기 및 질문 답변 (변경 없음) [https://code.claude.com/docs/en/best-practices]

[정의/규정] Plan: 상세 implementation plan 작성. 어떤 파일을 수정하는가, session flow는 무엇인가를 명시. Ctrl+G로 텍스트 에디터에서 plan을 직접 편집 가능 [https://code.claude.com/docs/en/best-practices]

[정의/규정] Implement: plan을 벗어나지 않으면서 코드 작성, 테스트 실행, 실패 수정 [https://code.claude.com/docs/en/best-practices]

[정의/규정] Commit: 설명적 메시지로 commit, PR 생성 [https://code.claude.com/docs/en/best-practices]

[정의/규정] 계획 회피 규정: "scope이 명확하고 수정이 작으면(typo, log line, variable rename 등) 직접 실행 권고. diff를 한 문장으로 설명할 수 있으면 plan mode 스킵" [https://code.claude.com/docs/en/best-practices]

[정의/규정] 검증-우선 처방: "verification check를 제공하라 (tests, build, screenshot). check가 없으면 Claude는 '완료처럼 보인다'는 신호만 사용하고, verification loop가 폐쇄되지 않음. check이 있으면 Claude는 work → check 실행 → result 읽음 → iterate를 반복하여 check가 통과할 때까지 진행" [https://code.claude.com/docs/en/best-practices]

[정의/규정] Interview-first workflow: 큰 feature의 경우, minimal prompt로 시작하여 Claude에게 AskUserQuestion tool을 사용하여 detailed interview 진행하도록 함. Interview 완료 후 fresh session에서 spec.md 실행. New session이 clean context를 가짐 [https://code.claude.com/docs/en/best-practices]

---

## OpenAI Codex [1차]

[정의/규정] Codex agents workflow: 각 phase는 task-specific subagents에게 위임하고, explicit repository artifacts를 통해 handoff [https://github.com/shinpr/codex-workflows]

[정의/규정] Planning phase 강조: "hard tasks에서 planning step을 스킵하는 것이 degraded sessions의 가장 흔한 원인. corrections이 수렴하지 않고 복합하기 시작함. Planning phase를 과소평가하지 말 것" [검색 결과 요약]

[정의/규정] Interactive planning: "implement하고 싶다고 Codex에 명시하고 필요한 정보를 물어달라고 지시하면, Codex가 질문함. 이를 통해 requirements를 organize하고 misunderstanding을 implementation 이전에 방지" [검색 결과 요약]

[정의/규정] Process steps: inspect existing codebase → select smallest sufficient process → pause at decision boundaries → implement one task at a time → check finished work still matches requirements [https://github.com/shinpr/codex-workflows]

---

## Scott Logic Spec Kit 비판 [2차]

[데이터] Scott Logic은 두 feature (Circuit Management, Geolocation)에서 Spec Kit 측정:
- Circuit Management: 33.5분 agent 실행시간, 2,577줄 markdown, 3.5시간 review time, 689줄 코드
- Geolocation: 23.5분 agent 실행시간, 2,262줄 markdown, ~2시간 review time, ~300줄 코드
[https://blog.scottlogic.com/2025/11/26/putting-spec-kit-through-its-paces-radical-idea-or-reinvented-waterfall.html]

[주장] Scott Logic: "Spec Kit로 약 10배 느림" 비교 (iterative 방식 8분 agent time, minimal markdown, 15분 code review vs Spec Kit의 누적 시간) [https://blog.scottlogic.com/2025/11/26/putting-spec-kit-through-its-paces-radical-idea-or-reinvented-waterfall.html]

[주장] Colin Eberhardt (Scott Logic): "I didn't see any qualitative benefit to justify the overhead" — specification-driven code가 iteratively-developed code보다 낫지 않음에도 훨씬 많은 시간 소비 [https://blog.scottlogic.com/2025/11/26/putting-spec-kit-through-its-paces-radical-idea-or-reinvented-waterfall.html]

[주장] Colin Eberhardt: Spec Kit implementation에서 "small, and very obvious bug" 발견. Extensive specification 후에도 버그 존재 [https://blog.scottlogic.com/2025/11/26/putting-spec-kit-through-its-paces-radical-idea-or-reinvented-waterfall.html]

[주장] Colin Eberhardt: SDD는 "return to waterfall" methodology. AI의 "빠르고 저렴한 코드 생성 능력"을 capitalize하지 못함 [https://blog.scottlogic.com/2025/11/26/putting-spec-kit-through-its-paces-radical-idea-or-reinvented-waterfall.html]

---

## Cursor, Windsurf, Devin [1차]

[정의/규정] Cursor Composer: iterative, human-controlled development. 각 step 승인 필요 [검색 결과 요약]

[정의/규정] Windsurf (Cascade agent, 2026에 Devin Desktop으로 rebranding): autonomous multi-step workflows with minimal intervention. Structured Flow approach로 discrete phases 구조화 [검색 결과 요약]

[정의/규정] Devin (standalone agent): task execution model. 전체 workflow 처리 시도 — planning, coding, running, debugging, iterating until completion. Cognition이 2025-07에 Windsurf 인수 후 2026에 rebranding [검색 결과 요약]

---

## 미해결

BMAD 및 OpenSpec 공식 문서를 찾지 못함. Google Codex 혹은 다른 OpenAI official workflow guidance (AGENTS.md 이상의 명확한 process model)에 대한 1차 source 제한적.

---

## 출처

### Primary Sources [1차]

- [GitHub Spec Kit Official Docs](https://github.github.com/spec-kit/)
- [GitHub Spec Kit Repository](https://github.com/github/spec-kit)
- [Amazon Kiro Specs Documentation](https://kiro.dev/docs/specs/)
- [AWS Blog: From spec to production — Kiro drug discovery agent](https://aws.amazon.com/blogs/industries/from-spec-to-production-a-three-week-drug-discovery-agent-using-kiro/)
- [Anthropic Claude Code Best Practices](https://code.claude.com/docs/en/best-practices)
- [Scott Logic: Putting Spec Kit Through Its Paces](https://blog.scottlogic.com/2025/11/26/putting-spec-kit-through-its-paces-radical-idea-or-reinvented-waterfall.html)
- [Codex Workflows GitHub Repository](https://github.com/shinpr/codex-workflows)

### Secondary Sources [2차]

- [Putting Spec Kit Through Its Paces — Scott Logic Blog Post](https://blog.scottlogic.com/2025/11/26/putting-spec-kit-through-its-paces-radical-idea-or-reinvented-waterfall.html)
- [GitHub's Spec Kit Puts the Spec Back in Software Development — DevOps.com](https://devops.com/githubs-spec-kit-puts-the-spec-back-in-software-development/)
- [Windsurf vs Cursor (2026) Comparison](https://www.vibecodingacademy.ai/blog/windsurf-vs-cursor)
- [Devin vs Cursor: Where Each One Really Fits — Emergent.sh](https://emergent.sh/learn/devin-vs-cursor)
- [Devin vs Cursor in 2026 — Apidog Blog](https://apidog.com/blog/whats-new-in-devin-2026/)
