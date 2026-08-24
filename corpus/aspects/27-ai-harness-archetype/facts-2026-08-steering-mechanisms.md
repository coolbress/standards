---
id: aspect-27-ai-harness-archetype--facts-2026-08-steering-mechanisms
title: "Frontier harness steering mechanisms — facts (2026-08)"
parent: aspect-27-ai-harness-archetype
kind: research-log
evidence_track: lit
status: draft
language: ko
last_updated: "2026-08-02"
review_due: "2026-11-02"
method: "Haiku web-research, facts-only, EVIDENCE-POLICY conformant; search log included"
---

## 조사 기록

**질문:** Frontier AI agent harness들이 모델에 지시를 전달하는 공식적인 메커니즘 (steering surfaces)은 무엇인가?

**범위:** Claude Code, Codex, OpenAI 플랫폼, Cursor, Gemini CLI 공식 문서 조사. MCP 스펙 수준 사실만.

**제외:** 설계 권장사항, 구현 세부사항, 테스트 커버리지.

**검색일:** 2026-08-02
**검색 횟수:** 6회 (예산 내)
**Fetch 횟수:** 8회 (예산 내)

**검색식:**
1. `Claude Code CLAUDE.md system prompt steering` → code.claude.com/docs
2. `Anthropic context engineering instruction placement` → docs.anthropic.com
3. `OpenAI Model Spec instruction hierarchy` → developers.openai.com
4. `MCP Model Context Protocol tools resources steering` → modelcontextprotocol.io
5. `Cursor .cursorrules project steering` → cursor.com/docs
6. `Claude Code hooks PreToolUse permissions` → code.claude.com/docs

---

## 1. Claude Code 스티어링 표면

### 1.1 CLAUDE.md (메모리/지시)

**[정의]** Claude Code가 매 세션마다 로드하는 프로젝트/사용자별 지시 파일. `~/.claude/CLAUDE.md` (전역) 또는 `.claude/CLAUDE.md` (프로젝트 수준).

### 1.2 Hooks (PreToolUse, Stop, PostToolUse 등)

**[정의]** 세션/턴/도구 호출 시점에 자동 실행되는 사용자 정의 명령어, HTTP 엔드포인트, 또는 LLM 검증. [1차: https://code.claude.com/docs/en/hooks]

**[규정] 종류:**
- `PreToolUse`: 도구 호출 전 (모든 도구, EndConversation 제외) [1차: https://code.claude.com/docs/en/hooks]
- `PostToolUse`: 도구 호출 후 [1차: https://code.claude.com/docs/en/hooks]
- `Stop`: 사용자 프롬프트 제출 시 [1차: https://code.claude.com/docs/en/hooks]
- `SessionStart`, `SessionEnd` [1차: https://code.claude.com/docs/en/hooks]
- `FileChanged`, `ConfigChange`, `CwdChanged` (비동기) [1차: https://code.claude.com/docs/en/hooks]

**[규정]** 강제성: 혼합. Exit code 2 또는 JSON `decision: "block"`으로 행동 차단 가능 (PreToolUse, Stop, UserPromptSubmit, PermissionRequest). PostToolUse/PostToolBatch는 이미 발생한 행동 로깅만 가능 (advisory). [1차: https://code.claude.com/docs/en/hooks]

**[정의]** 검증 타입: command (bash/powershell), http (HTTP POST), mcp_tool (MCP 서버), prompt (Claude 모델), agent (서브에이전트). [1차: https://code.claude.com/docs/en/hooks]

### 1.3 권한 시스템 (Permissions)

**[정의]** 파일 읽기(무조건), Bash 명령어(확인 필요), 파일 수정(세션별) 승인을 세분화 제어. [1차: https://code.claude.com/docs/en/permissions]

**[규정]** 계층: deny > ask > allow. 매칭하는 deny 규칙이 호출을 차단. ask 규칙은 hook이 "allow" 반환해도 프롬프트 실시. [1차: https://code.claude.com/docs/en/permissions]

**[주장]** 강제성: 하드 게이트. "Permission rules are enforced by Claude Code, not by the model." 프롬프트나 CLAUDE.md의 지시는 Claude가 *시도*할 일을 형성하지만 Claude Code가 허용할 일을 바꾸지 못함. [1차: https://code.claude.com/docs/en/permissions]


---

## 2. OpenAI 플랫폼 지시 계층

### 2.1 역할 계층 (Role-based Hierarchy)

**[주장]** 개발자/시스템 역할의 지시가 사용자 역할의 지시를 우선할 수 있음: "User instructions may overwrite the _CODING GUIDELINES_ section in this developer message." [1차: https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide]

**[주장]** 그러나 OpenAI는 *충돌 해결 계층*보다는 **명확한 프롬프트 설계**를 강조. "poorly-constructed prompts containing contradictory... instructions can be more damaging to GPT-5 than to other models." [1차: https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide]

**[주장]** 충돌 예방을 프롬프트 설계 단계에서 수행. "Establishing clear instruction precedence within the prompt itself." [1차: https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide]

---

## 3. Cursor 스티어링 표면

### 3.1 .cursorrules / .cursor/rules (프로젝트 규칙)

**[정의]** 프로젝트 수준 지시. `.cursor/rules/*.mdc` 파일로 버전 관리. Frontmatter로 `alwaysApply`, `description`, `globs` 지정. [1차: https://cursor.com/docs/rules]

**[규정]** 에이전트 시작 시 모델 컨텍스트에 포함 ("at the start of the model context"). [1차: https://cursor.com/docs/rules]

**[규정]** 계층: 팀 규칙 > 사용자 규칙 > 프로젝트 규칙. 팀 규칙은 대시보드 관리, "organizational standards ensure를 위해 precedence." [1차: https://cursor.com/docs/rules]

### 3.2 Agent Hooks (Cursor 클라우드)

**[정의]** Tool execution, file/shell work 주변 팀 hooks. beforeSubmitPrompt, afterAgentResponse, afterAgentThought, stop, subagentStart. [1차: https://cursor.com/docs/rules]

**[규정]** 에이전트 행동 관찰 및 제어 (prompts, responses, thinking, subagents, compaction, turn completion). [1차: https://cursor.com/docs/rules]

---

## 4. MCP (Model Context Protocol) 스티어링

### 4.1 Tools

**[정의]** MCP 서버가 노출하는 도구. 모델 제어 가능 (model-controlled): "language model can discover and invoke tools automatically based on its contextual understanding." [1차: https://modelcontextprotocol.io/specification/2025-06-18/server/tools]

**[규정]** 스키마: inputSchema, outputSchema (선택), name, description, title. 서버가 선언하지 않으면 클라이언트가 검증할 수 없음. [1차: https://modelcontextprotocol.io/specification/2025-06-18/server/tools]

**[주장]** 신뢰 & 안전: "applications SHOULD: Provide UI that makes clear which tools are being exposed, insert clear visual indicators when tools are invoked, present confirmation prompts to the user." [1차: https://modelcontextprotocol.io/specification/2025-06-18/server/tools]

---

## 5. Anthropic 공식 지침

### 5.1 프롬프트 엔지니어링 개요

**[주장]** "When to prompt engineer" — 모든 문제가 프롬프트 엔지니어링으로 해결 불가. "sometimes improve latency and cost more easily by selecting a different model." [1차: https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/overview]

**[정의]** 기법: Clarity, examples, XML structuring, role prompting, thinking, prompt chaining. [1차: https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/overview]

### 5.2 지시 배치 (CLAUDE.md vs 시스템 프롬프트)

**[정의]** 컨텍스트 윈도우: 시스템 프롬프트, 메시지 (도구 결과 포함), 이미지, 문서 모두 컨텍스트 윈도우 소비. Extended thinking도 포함. [1차: https://platform.claude.com/docs/en/docs/build-with-claude/context-windows]

---

## 6. Vendor 주장: Advisory vs 강제

### 6.1 Claude Code

**[규정]** 강제 게이트:
- Permissions (deny/ask/allow): 하드 게이트, 하네스 자체가 강제 [1차: https://code.claude.com/docs/en/permissions]
- Hooks (exit code 2): PreToolUse에서 호출 차단 가능 [1차: https://code.claude.com/docs/en/hooks]

### 6.2 OpenAI 플랫폼

**[주장]** 계층: Developer/system > user (역할 기반), 그러나 충돌 해결은 프롬프트 설계 ("establishing clear precedence within prompt itself"). [1차: https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide]

### 6.3 Cursor

**[규정]** 강제: Team rules > 사용자 규칙. 조직 표준 유지. [1차: https://cursor.com/docs/rules]

**[규정]** Project rules는 `alwaysApply` 플래그로 제어 가능 또는 @-mention으로 수동 적용. [1차: https://cursor.com/docs/rules]

---

## 7. Codex 지시 표면 (미조사)

**미해결:** Codex 공식 문서를 찾지 못함. Search에서 Codex 관련 PRIMARY 소스 없음. 검색 예산 소진으로 재검색 미실시.

---

## 8. Gemini CLI (미조사)

**미해결:** Google Gemini CLI 공식 문서를 검색하지 못함. 검색 도메인이 제한되지 않았는데도 결과 없음. 검색 예산으로 인해 추가 검색 미실시.

---

## 미해결

### 미매핑된 주장 (1차 소스 부재)

- **Skills 메커니즘:** 메타데이터 항상-온, 본문 온디맨드 진행적 공개 - 공식 문서 미확인
- **Slash commands:** `/` 명령어 트리거 메커니즘 - 공식 문서 미확인
- **Subagents:** 제한된 권한의 별도 인스턴스 - 공식 문서 미확인
- **CLAUDE.md 텍스트의 Advisory 성격:** "프롬프트 텍스트로 전달됨, 모델이 무시 가능" - GOPPI.md (2차) 참고만
- **MCP Resources:** 도구가 반환하는 추가 컨텍스트, URI 링크, embedded - 일반 지식, 특정 fetch 없음
- **MCP Prompts:** 서버가 노출하는 프롬프트 템플릿 - 특정 fetch 없음
- **Anthropic "CLAUDE.md 짧게 유지" 지침:** "each line 'if removed would Claude err?'" - GOPPI.md (2차 참고)

### 미조사 범위 (검색 및 fetch 예산 소진)

- Codex AGENTS.md, config.toml, execpolicy 공식 문서
- Gemini CLI GEMINI.md 공식 문서
- Anthropic long-context-tips 상세 내용 (redirect 후 fetch 미실시, 예산 소진)

---

## 출처

### 1차 (공식 문서)

- [Claude Code: Hooks Reference](https://code.claude.com/docs/en/hooks)
- [Claude Code: Configure Permissions](https://code.claude.com/docs/en/permissions)
- [Anthropic: Prompt Engineering Overview](https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/overview)
- [OpenAI: GPT-5 Prompting Guide](https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide)
- [MCP Specification 2025-06-18: Tools](https://modelcontextprotocol.io/specification/2025-06-18/server/tools)
- [Cursor Docs: Rules](https://cursor.com/docs/rules)
- [Anthropic: Context Windows](https://platform.claude.com/docs/en/docs/build-with-claude/context-windows)

### 2차 (프로젝트 CLAUDE.md)

- GOPPI.md (user's private instructions)
- Observed: "CLAUDE.md short, each line 'if removed would Claude err?'" — normative but source TBD
