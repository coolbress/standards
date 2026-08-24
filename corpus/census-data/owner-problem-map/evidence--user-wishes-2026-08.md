# 사용자 "소원(wishes)" 광범위 조사 — 원문 기록 (2026-08-12)

> **방법**: 소유자 지시로 조사 에이전트 2개 병렬 실행 — ① 개발자/실무자의 위시(GitHub 이슈 반응수 직접 집계 + 포럼 + 서베이) ② 비개발자 빌더의 위시(커뮤니티·리뷰·가이드 역설계·유료 서비스).
> **등급: 전부 [2차].** 스타/추천수는 2026-08-12 기준. FOUNDING-IDEA §3 [1차] 절에는 넣지 않는다.
> **용도**: 문제(무조건 해결) vs 개선 희망(하네스 확장)의 2층 재구성 — 세션 #6 소유자 제안.
> **자매 기록**: `2026-08-12-agent-failure-research.md` (실패 요인 = 문제 쪽 근거)

---

## ① 개발자/실무자의 위시 — 행동으로 드러난 것 (이슈 추천수·자작 도구 스타수)

### A. 계획 먼저 (Planning & Spec-first)
- **Codex "Plan Mode" 요청 406👍** ([openai/codex#2101](https://github.com/openai/codex/issues/2101), 구현됨) — 코드 전에 계획+승인. 비개발자에겐 실행 전 계획이 **유일하게 이해하고 개입할 수 있는 지점**.
- **GitHub Spec Kit 126,311★** — "code is no longer the first step, the spec is." 행동으로 드러난 위시 중 최대. 단 스펙을 "쓰는" 행위가 비개발자에겐 장벽 — 하네스가 대신/보조해야.
- Aider "변경 전 확인 강제" 요청 ([#649](https://github.com/Aider-AI/aider/issues/649) 41👍) — 도구 불문 반복 패턴.

### B. 세션을 넘는 기억
- **"매 세션 0에서 시작 — 10~15분 재설명"** 이 결핍을 메우는 자작 도구 최소 5~6종(Memento·OMEGA·claude-mem 등) 병렬 존재. Anthropic auto-memory 공식화가 방증.
- "Claude Code ↔ Projects 연결" 383👍 ([anthropics/claude-code#2511](https://github.com/anthropics/claude-code/issues/2511)).
- **AGENTS.md 표준 지원 4,542👍 — claude-code 저장소 전체 이슈 반응수 1위** ([#6235](https://github.com/anthropics/claude-code/issues/6235)) — "프로젝트 지식은 도구가 아니라 프로젝트에 귀속돼야."
- 비개발자 증폭: 재설명할 **언어 자체가 없음** — 기억은 하네스가 대신 들어야.

### C. 되돌리기 / 체크포인트 / 보호 구역
- **Codex "/undo 돌려달라" 382👍 + 체크포인트 복원 199👍** ([#9203](https://github.com/openai/codex/issues/9203), [#11626](https://github.com/openai/codex/issues/11626)) — 코드+대화 컨텍스트를 함께 되돌리기. Claude Code /rewind·Cursor checkpoint가 같은 위시의 응답.
- **강제 보호 구역**: "There is no way to enforce a code freeze in vibe coding apps... There just isn't." (Replit 사건) + Codex "민감 파일 제외" 461👍 + 시크릿 주입 144👍 + 복합 명령 권한 분해 175👍.
- 비개발자 증폭: **극대** — git 없는 사용자의 유일한 안전망. 프롬프트 지시("건드리지 마")는 강제가 아님을 사후에야 배움.

### D. 검증 — "끝났다"를 믿을 수 있게
- **"거짓말 못 하게 하는 Stop Hook"** 워크어라운드 생태계 — 테스트/린트/빌드 통과 전 "완료" 선언 차단을 사람들이 직접 구현 ([claude-code-hooks-mastery 3,883★](https://github.com/disler/claude-code-hooks-mastery)).
- **에이전트에게 "눈"** — 브라우저/스크린샷 자가 검증 루프. Playwright MCP가 최다 설치권. "once code hit a real browser, the feedback loop belonged to the developer."
- **"추측하지 말고 물어봐라"** — "AI coding assistants are too eager to please and impress, rarely asking clarifying questions before diving in." AskUserQuestion 출시가 방증.
- 비개발자 증폭: **극대** — "almost right" 66%를 식별할 눈이 없음. 질문 유도는 비개발자 하네스의 핵심 요건.

### E. 비용·사용량 가시성
- **ccusage 17,870★ + Usage Monitor 8,619★** — "your only feedback mechanism is hitting the wall mid-conversation." 사용량 한도 이슈 693👍 등.
- 비개발자 증폭: 큼 — 단 CLI 형태는 못 쓰므로 **내장형**이어야.

### F. 진행 상황과 투명성
- "사고 과정 항상 표시" 329👍 · 읽는 파일 표시 186👍 · 컨텍스트 잔량 140👍 · 완료 알림음 186👍 — 합계 990+👍.
- 원격 모니터링(Omnara Launch HN 147p · Copilot "Mission Control" 공식화) — "assign, steer, and track... in one centralized, real-time view."
- 비개발자 증폭: 큼 — 단 raw thinking이 아니라 **"3단계 중 2단계, 로그인 화면 고치는 중" 같은 평문 번역** 필요.

### G. 리뷰 워크플로
- 변경 승인 UI 요청 4건 800+👍 (Codex diff/approval 226👍 등, 세 도구 공통).
- 비개발자 증폭: **형태를 바꿔야** — diff는 무의미. "동작 변화 요약 + 화면 미리보기"로 번역.

### H. 멀티 에이전트 오케스트레이션
- 자작 오케스트레이터 합계 15만+★ (vibe-kanban 27,745★ · ruflo 67,694★ · SuperClaude 23,823★ 등) — 워크어라운드 생태계 중 최대.
- 비개발자 관련성: **낮음** (내부 구현 기법으로만 유효).

### I. 서베이 총괄
- **SO 2025** (49k명): "almost right, but not quite" 66% 최대 불만 · 정확도 highly trust 3.1% · **75.3%가 AI를 못 믿을 때 사람 도움을 원함**.
- **JetBrains 2025** (24,534명): "delegate mundane tasks... but stay in control" — 위시의 본질은 능력이 아니라 **통제 가능한 위임**.
- **DORA 2025**: **60%+가 배포 후에야 AI 관련 오류 발견**. "Speed without stability is just accelerated chaos."

### 종합 — 비개발자 증폭 순위 (조사 에이전트 판정)
되돌리기/체크포인트(극대) ≈ 강제 가드레일(극대) ≈ 완료 전 기계 검증(극대) ≈ 추측 대신 질문(극대) > 세션 간 기억 > 계획 승인 게이트 > 진행 평문 보고 > 비용 가시성 > 리뷰 UX ≫ 멀티에이전트(낮음).
**패턴**: 벤더가 수용해 출시한 기능 목록(Plan Mode·/rewind·AskUserQuestion·auto-memory·Mission Control)이 곧 "검증된 위시 목록". 서베이 3종의 수렴점 = "I want to delegate, but stay in control."

---

## ② 비개발자 빌더의 위시 — 커뮤니티·리뷰·유료 서비스 역설계

**핵심 발견**: 비개발자의 소원은 "더 좋은 코드 생성"이 아니라 압도적으로 **생성 이후** — 비용 예측 · 보안 확인 · 완료 판단 · 출시 후 안정성 · 개발자 인계.

### A. 비용 확신 — "결과가 나오기 전에 얼마인지"
- Replit effort-based 과금 집단 반발: "a pricing casino — you place the bet, then see the bill." 주 $1,000 도달 사례. **어떤 주요 플랫폼도 "실행 전 비용 미리보기"를 제공하지 않음.**
- Lovable: "AI가 스스로 만든 버그를 고치는 루프에 크레딧 과금"이 Trustpilot·Reddit·G2 통틀어 **가장 빈번한 불만**.
- Bolt: "you watch tokens disappear without producing working results, and you lack the skills to fix it."

### B. 보안 확신 — "출시 전에 누가 봐줬으면"
- 보안 체크리스트 가이드 9종+ 대량 발생 = 내장 보안 검증 부재의 증거. 최다 누락 = Supabase RLS.
- **유료 보안 스캐너**(VibeAppScanner 등) 등장 — 지불 의사 증명.
- Replit 사건의 교훈 언어화: "Guardrails must be architectural, not conversational." → 사건 후 dev/prod 자동 분리·롤백 강화·planning 모드 도입(소원이 제품을 바꾼 사례).

### C. 시작 전 계획
- SaaStr 14교훈(비개발자 VC, 150시간): "Write a Detailed Specification Document — Over-spec now" / "Define Your Production Requirements Before You Start" / "Understand What Looks Easy But Isn't"(이메일·OAuth).
- "개발자 언어부터 배워라" 가이드(용어 1,450개 암기)의 존재 = **"사용자 말 → 개발 개념" 번역 계층의 부재**.

### D. 오류의 평이한 설명 + 둠 루프 탈출
- 초심자 가이드 단골: "ask it to explain the error in plain language before suggesting a fix" — 수동 절차로 보상 중.
- **루프 감지 위시**: "loops through failed fix attempts that consume additional credits without resolution." — "루프에 빠졌음"을 감지·알림하는 기능은 어느 플랫폼에도 없음.

### E. 진행 가시성과 "끝났는지"
- "Each step felt productive, but nothing felt stable enough to trust... It felt like progress. It wasn't."
- **출시 준비 체크리스트 7종+ · 유료 PDF까지** — "Am I done?"의 시장화. 핵심 검증 3종: happy path / **permission failure** / **interrupted flow**. "the UI is not security."
- **어떤 플랫폼도 "실제로 검증된 것 vs AI가 됐다고 주장하는 것"을 구분해 보여주지 않음.**
- "당신의 새 직업은 QA 엔지니어" — 시간 60%를 수동 테스트에. 플랫폼 내장 E2E 부재 공통.

### F. 출시 후 생존
- Product Hunt 육성 위시: 출시 후 "auth breaking, database timeouts, a webhook that silently fails" — "error monitoring, store readiness, and **knowing what is safe to change without breaking production**."
- **"바이브 코드 레스큐" 유료 산업 최소 7개 업체** — 최강 지불 의사 증거. "AI tools get founders 80% of the way there, but the last 20%... requires a human developer who understands what the AI got wrong." (148,000건 불만·2,400개 스타트업 분석 인용)
- 월간 유지보수 체크리스트: "apps fail from forgotten dependencies, expired credentials, and quiet billing changes rather than from code bugs."

### G. 개발자 인계 (출구 전략)
- "tools that let you own/export the code and keep a clear full-stack structure, so a developer can actually debug it later." Lovable GitHub 동기화가 정확히 이 이유로 칭찬받음.
- "Plan Your Exit Strategy from Day One."

### H. 백엔드 가시성
- Lovable 사용자 소원: 스프레드시트형 DB · 시각적 로직 추적 · 내장 RBAC. Supabase 설정 = "a wall for non-technical users."
- v0: "beautiful components but no clear path to making them functional applications" (v0 사용자 63%가 비개발자).

### 종합 — 소원의 구조 (조사 에이전트 판정)
1. **소원의 무게중심은 "생성"이 아니라 "확신"**: 비용 확신 · 보안 확신 · 완료 확신 · 생존 확신.
2. **지불 의사 증명 3종**: 레스큐 산업(7개+) · 유료 보안 스캐너 · 유료 출시 체크리스트 — 셋 다 **출시 직전·직후 구간**.
3. **아직 아무도 응답하지 않은 소원**: 실행 전 비용 미리보기 · 루프 감지 · **"검증된 진행" 표시** · 요청 밖 변경 알림 · 평이한 언어의 출시 게이트.
4. **가이드 역설계 → 자동화 후보 5**: ① 스펙부터 쓰기 ② 오류 평이 설명 ③ 권한 실패·중단 흐름 테스트 ④ 시크릿 노출 검색 ⑤ 월간 크레덴셜 점검.

### 신뢰도 주의
Reddit 원문은 대부분 2차 출처(리뷰 집계·기술 매체) 경유. Trustpilot/G2/Product Hunt 인용문은 원문 그대로. 보안 스캐너·레스큐 업체 자료는 이해관계 있음(개별 사건은 교차 확인됨).
