---
id: aspect-27-ai-harness-archetype--claude-code-agent-surface--facts-2026-08
title: "Claude Code 에이전트 표면 갱신 — 서브에이전트·MCP·모델 지형 (facts 2026-08)"
parent: aspect-27-ai-harness-archetype
kind: research-log
evidence_track: lit
status: draft
language: ko
last_updated: "2026-08-24"
method: "질문 2개로 한정한 표적 조사(2026-08-24): ① 2026-07-02 조사 이후 Claude Code의 서브에이전트/MCP 표면이 어떻게 바뀌었고 기존 코퍼스 기술 중 무엇이 틀렸는가 ② 외부 모델을 브레인 아래에 붙이는 경로는 무엇인가. 1차 출처는 Claude Code 공식 문서 2편(sub-agents, mcp). 모델 지형 부록은 2차 출처(벤치마크 블로그)만 있어 별도 절로 격리하고 수명을 🔴로 표기. 포함: frontmatter 필드 전수·중첩/동시 한계·컨텍스트 격리 실제 내용·MCP 등록 명령과 승인 제약. 제외: Codex CLI 현행 표면(미갱신 — 아래 미해결). 종료 기준: 기존 코퍼스와 어긋나는 항목이 1차 출처로 특정될 것."
sources:
  - "https://code.claude.com/docs/en/sub-agents"
  - "https://code.claude.com/docs/en/mcp"
---

# Claude Code 에이전트 표면 갱신 (2026-08)

`multi-agent-orchestration-standard.md`(2026-07-02)와 `hooks-commands-subagents-standard.md`의
호스트 기술 중 **세 항목이 현행과 어긋난다.** 이 문서가 그 항목을 대체한다. 두 문서의 *전략* 층
(오케스트레이터-워커 토폴로지, 단일 작성자 원칙, 토큰 경제, 생성자-검증자)은 영향받지 않는다 —
어긋난 것은 호스트 제품 세부이고, 그것은 `RESEARCH-LIFETIME.md`에서 🔴로 분류된 층이다.

## Claim table

| Claim ID | Class | Claim and scope | Evidence | Confidence | Valid as of / expiry |
|---|---|---|---|---|---|
| CAS-001 | vendor-behavior | 서브에이전트 `model` 필드는 `sonnet`·`opus`·`haiku`·**`fable`**·전체 모델 ID·`inherit`(기본)를 받는다. 해석 순서는 `CLAUDE_CODE_SUBAGENT_MODEL` 환경변수 → 호출별 파라미터 → frontmatter → 메인 대화. **비-Anthropic 모델은 값으로 받지 않는다.** | Claude Code sub-agents 문서 | high | 2026-08-24; 호스트 minor마다 |
| CAS-002 | vendor-behavior | 서브에이전트 중첩은 **기본 3단**(`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`로 조정), 동시 실행은 **최대 20**(`CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`). 최상위 서브에이전트의 요약만 메인 대화로 돌아온다. | 같은 문서 | high | 2026-08-24; 호스트 minor마다 |
| CAS-003 | vendor-behavior | frontmatter 전수: `name`·`description`·`tools`·`disallowedTools`·`model`·`permissionMode`·`skills`·`mcpServers`·`hooks`·`memory`·`maxTurns`·`background`·`isolation`·`color`·**`initialPrompt`**. `isolation: worktree`는 격리된 git worktree에서 실행한다. | Claude Code sub-agents 문서 | high | 2026-08-24; 호스트 minor마다 |
| CAS-004 | vendor-behavior | 비-fork 서브에이전트가 **받는 것**: 자기 시스템 프롬프트·위임 메시지·**CLAUDE.md 계층**·git status 스냅샷·프리로드 스킬·형제 로스터. **못 받는 것**: 대화 이력·출력 스타일·메인의 자동 메모리·메인의 컨텍스트 크기. **Explore·Plan 에이전트는 CLAUDE.md와 git status도 받지 않는다.** fork 서브에이전트는 이력·프롬프트·도구·모델을 전부 상속한다. | 같은 문서 | high | 2026-08-24; 호스트 minor마다 |
| CAS-005 | vendor-behavior | MCP 서버 등록은 `claude mcp add --transport http\|sse\|stdio <name> …` 또는 `claude mcp add-json`. 스코프는 `local`(기본)·`project`(`.mcp.json`, 커밋 가능)·`user`. **v2.1.196부터 `.mcp.json` 서버는 워크스페이스를 신뢰하기 전까지 `⏸ Pending approval` 상태이며, 저장소에 커밋된 `enableAllProjectMcpServers`/`enabledMcpjsonServers`는 신뢰 전 폴더에서 무시된다** — 클론한 저장소는 자신의 MCP 서버를 스스로 승인할 수 없다. | Claude Code MCP 문서 | high | 2026-08-24; 호스트 minor마다 |
| CAS-006 | synthesis | CAS-001에 따라 **외부(비-Anthropic) 모델을 브레인 아래에 붙이는 경로는 두 가지뿐이다** — (a) MCP 서버를 통한 도구 호출, (b) Bash로 다른 CLI를 셸아웃. 서브에이전트 `model` 필드로는 불가능하다. (b)만 별도 프로세스이므로 터미널 멀티플렉서의 판(pane) 단위 관측 대상이 된다. | CAS-001 + CAS-005 | medium-high | CAS-001 변경 시 |

## 기존 코퍼스 정정 (무엇이 어떻게 틀렸는가)

| 문서 | 기존 기술 | 현행 | 처분 |
|---|---|---|---|
| `multi-agent-orchestration-standard.md` (교차호스트 표) | 중첩 "**up to 5 levels** (v2.1.172)" | **기본 3단**, 환경변수로 조정 | CAS-002가 대체 |
| 같은 문서 | 동시 실행 한계 미기재 | **최대 20** | CAS-002가 보충 |
| `hooks-commands-subagents-standard.md` | frontmatter 목록 — **어긋나지 않음**(`fable`·`disallowedTools`·`permissionMode`·`mcpServers`·`memory`·`maxTurns`·`isolation: worktree`·`background`·`color` 이미 수록) | `initialPrompt` 1건만 추가 | CAS-003이 보충 (정정 아님) |

`RESEARCH-LIFETIME.md` §4(🔴 층)의 "호스트 표면은 minor 올라갈 때마다 재확인" 규칙이 발화한 사례다 —
다만 **어긋난 것은 중첩/동시 한계 2건뿐**이고 컴포넌트 문서의 frontmatter 기술은 현행과 맞았다.
**조사 과정의 교훈**: 전략 문서(`multi-agent-orchestration-standard.md`)의 요약표만 보고 컴포넌트 문서
(`hooks-commands-subagents-standard.md`)를 읽지 않으면 없는 결함을 보고하게 된다. 두 층은 의도적으로
분리돼 있으므로(부모 문서 §"Why this sub-doc"), 호스트 세부의 현행성 판정은 **컴포넌트 문서 쪽**이 정본이다.

## 오케스트레이션 전략 층에 대한 함의

- `isolation: worktree`가 **네이티브 한 줄 설정**이 됐다. 부모 문서가 인용한 CAID의 worktree 격리
  (+26.7pp)는 이제 구현 대상이 아니라 설정 대상이다.
- CAS-004는 Cognition의 **생성자-검증자** 패턴이 이 호스트에서 성립함을 구체화한다. 리뷰어 서브에이전트는
  프로젝트 규칙(CLAUDE.md)은 받되 **작성자의 대화 이력은 받지 않는다** — 부모 문서가 인용한
  *"리뷰어의 제한된 컨텍스트가 오히려 버그 검출을 높인다"* 의 조건이 기본값으로 충족된다.
- CAS-005는 프로젝트 템플릿에 `.mcp.json`을 넣어도 **새 저장소마다 1회 사람 승인이 필요**함을 뜻한다.
  MCP 배선은 완전 자동화되지 않는다.

## 부록 — 2026-08 모델 지형 [2차 출처 · 수명 🔴]

> ⚠️ **이 절만 2차 출처(벤치마크 집계 블로그)다.** 코퍼스 절대규칙 2와 EVIDENCE-POLICY의
> "효과성/인과에는 복제된 1차 연구" 원칙에 따라, 아래 순위는 **요구사항의 근거로 쓰지 않는다.**
> `references/model-roster.md`의 원칙 — *"A roster, not a router"* · 티어를 **세션 모델 기준 상대값**으로
> — 은 🟢이고, 아래 고유명사는 🔴다. **역할 배치만 골조로 쓰고 이름은 분기마다 갈아끼운다.**

| 모델 | 2026-08 시점의 강점 주장 | 가격대 | 로스터 역할 |
|---|---|---|---|
| Claude Opus 5 | 코딩·에이전트 최상위권 | 구독 | 드라이버 |
| Claude Fable 5 | 최상위 추론·장기 호흡. thinking 상시, effort low~max | Opus 대비 2배 | 드라이버(상향) |
| GPT-5.6 Sol | 터미널 계열 벤치 최상위권. 계열이 달라 반증에 적합 | 중 | 교차벤더 반증 |
| Gemini 3.7 Flash | 멀티모달·대량 컨텍스트, 전세대 대비 대폭 저렴 | 매우 낮음 | 대량 읽기·요약 |
| Grok 4.6 | 가격 대비 지능 선두 주장, 터미널 작업 강세 | 중 | 셸·CI 스크립트 |
| Kimi K3 | 오픈웨이트 최상위, 장기 호흡 에이전트 상위 | 중저 | 추론 2차 의견 |
| DeepSeek V4 (Flash) | 코딩 최저가 프론티어 | 최저 | 대량 반복·테스트 생성 |
| GLM-5.3 | 쉬움~중간 난이도에서 최상위와 체감차 없음 주장 | 매우 낮음 | 보일러플레이트 |

## 미해결

1. **Codex CLI 현행 표면 미갱신.** 부모 문서의 교차호스트 표는 2026-07-02 1회 웹조사이며 문서 스스로
   "결정이 이 수치에 걸리면 재검증하라"고 경고한다. 이번 조사에서 갱신하지 않았다.
2. 외부 모델 브리지 구현체(PAL MCP·OpenRouter MCP 계열)는 **2차 출처로만 확인**했고 실행 검증하지 않았다.
   두 문서 모두 "툴 수가 컨텍스트를 소비하니 필요한 것만 켜라"고 경고한다.
3. 모델 지형 부록의 벤치마크 수치는 재현하지 않았다.

## Sources
- Claude Code — Subagents: https://code.claude.com/docs/en/sub-agents
- Claude Code — MCP: https://code.claude.com/docs/en/mcp
