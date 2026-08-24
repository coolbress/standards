> ⚠️ **SUPERSEDED (2026-08-02)** — 이 문서의 사실 부분은 `../corpus/aspects/*/facts-2026-08-*.md`로, 판정 부분은 `../corpus/methods/` 및 `foundation/` 문서로 대체됐다. 역사 기록으로 보존하며, 활성 근거로 인용하지 않는다.

# 솔로/초소형 팀 + AI 에이전트 개발 프로세스 리서치

> goppi 재설계의 기초 자료. 조사 시점: 2026-08. 주제: 프로 개발 프로세스가 1~3인 규모와 AI 에이전트 협업 환경에서 어떻게 축소·변형되는가.

## 요약 (핵심 10줄)

1. 솔로/초소형 팀은 **검증 가능한 artifact 중심 실천**(버전 관리, CI, 테스트, 자동 배포)은 유지하고, **인간 간 조율용 세리머니**(스탠드업, 스프린트 의식, 정밀 추정)는 전부 버린다. 이 구분선이 goppi의 "load-bearing vs ceremony" 판별 기준과 정확히 일치한다.
2. AI 에이전트 시대에는 사람-사람 조율 실천이 사라진 자리에 **사람-에이전트 조율 실천**(스펙, 계획, 검증 루프, 컨텍스트 관리)이 들어온다. Willison: "AI 도구는 기존 전문성을 증폭한다" — 프로세스가 그 전문성을 대신 공급해야 비개발자가 프로처럼 만들 수 있다.
3. Spec-driven development(Spec Kit, Kiro)의 핵심 기여는 **"코딩 전에 의도를 검증 가능한 형태로 고정하고, 단계마다 사람이 체크포인트에서 교정한다"**는 루프. 그러나 실측 비판은 신랄하다: 토큰 낭비(코드보다 긴 마크다운), 워터폴 회귀, "스펙이 진실의 원천" 주장의 비현실성.
4. Anthropic 공식 가이드의 최중요 원칙: **에이전트에게 스스로 돌릴 수 있는 검증 수단(테스트/빌드/스크린샷)을 줘라** — 이것이 "지켜보는 세션"과 "맡겨두는 세션"의 차이를 만든다.
5. 컨텍스트는 유한 자원("context rot"): 항상 켜진 비대한 시스템 프롬프트는 실제로 해롭다는 것이 Anthropic 공식 입장 — "CLAUDE.md가 비대하면 Claude가 실제 지시를 무시한다."
6. 해법은 **progressive disclosure**: 메타데이터만 상시 로드, 본문은 필요 시 로드(Skills), 탐색은 서브에이전트로 격리. goppi의 "thin contract + on-demand skills" 구조는 이 원칙의 정석적 구현이다.
7. **"하네스는 얇아진다" 테제는 실무자 다수설**: "스캐폴딩은 스케일링이 아니라 코핑이다"(OpenAI Codex 팀), Anthropic도 모델이 좋아질 때마다 Claude Code 하네스를 뜯어낸다. 모든 스캐폴딩은 모델 발전에 반대로 거는 베팅.
8. 비개발자 vibe coding의 실증된 실패: Replit 에이전트의 프로덕션 DB 삭제(2025.7), Lovable 앱 170+개 데이터 노출(RLS 미설정). 공통 원인은 검증 부재, 환경 분리 부재, 보안 기본기 부재.
9. 예방하는 프로세스 요소는 소수로 수렴: 버전 관리(되돌리기), dev/prod 분리, 자동 테스트, 독립 리뷰, "실행해서 본 것만 완료"(Willison의 황금률) — 전부 goppi가 이미 계약에 넣은 것들.
10. 설계 결론: **구조는 '무엇을·어떻게 확인할지'에 투자하고, '어떻게 만들지'는 모델에 위임**하라. 절차를 늘리는 방향이 아니라 검증 표면을 늘리는 방향이 모델 발전과 같은 편에 서는 길이다.

---

## 1. 프로 프로세스의 다운스케일링: 솔로/2~3인 팀이 유지하는 것과 버리는 것

### 유지하는 것 (load-bearing)

- **버전 관리 + 브랜치/PR**: Jonathan Hall("Solo DevOps")은 솔로여도 main 직커밋 대신 브랜치→PR을 권한다. 작업 경계가 명확해지고, 히스토리가 깨끗해지고, **자기 코드를 셀프 리뷰할 표면**이 생기기 때문이다. (https://jhall.io/posts/solo-devops/)
- **CI (자동 테스트+린트)**: Hall은 "팀이든 솔로든 가장 먼저 세팅해야 할 것"으로 CI를 꼽는다. 솔로 개발자에게 CI는 추가 효용도 있다: 오랜만에 프로젝트로 돌아왔을 때 CI가 "어디까지 했는지"를 알려주는 재개 지점이 된다 — 미완성 기능에 실패하는 테스트를 남겨두라는 팁까지. (https://jhall.io/posts/solo-devops/, https://www.indiehackers.com/post/continuous-integration-as-a-solo-developer-80f533394c)
- **자동 배포 + 로깅**: 서버 앱은 머지 즉시 자동 배포되는 "dancing skeleton"으로 시작하라. 로깅은 나중에 붙이는 게 아니라 처음부터. (https://jhall.io/posts/solo-devops/)
- **테스트**: 장기 유지보수할 소프트웨어라면 유지. 단, 일회성 취미 프로젝트에는 과잉이라는 실무 합의도 있다 — 즉 테스트조차 리스크 비례로 스케일된다. (https://www.indiehackers.com/post/continuous-integration-as-a-solo-developer-80f533394c)

### 버리는 것 (ceremony)

- **스탠드업, 스프린트 계획/회고, 정밀 추정(스토리 포인트)**: 전부 인간 간 정보 동기화·약속 관리 장치다. 동기화할 타인이 없으면 존재 이유가 소멸한다. 솔로 개발 문헌에서 이것들은 "유지하라"는 항목에 아예 등장하지 않는다는 점 자체가 증거다. (https://jhall.io/posts/solo-devops/)
- swyx의 "Tiny Teams Playbook"(직원 수보다 ARR $M이 많은 팀들)은 이 현상의 극단: 소수 인간 + AI가 중간 규모 팀을 대체할 때, 병목은 기술 실행이 아니라 **인간 간 신뢰와 커뮤니케이션**이며, 티니 팀은 그 병목 자체를 헤드카운트 최소화로 제거한다. 프로세스는 "조율 최소화, 레버리지 최대화"로 재편된다. (https://www.latent.space/p/tiny)

### 판별 규칙 (goppi에 직결)

**남는 것은 전부 "artifact가 스스로 말하게 하는" 실천이고, 사라지는 것은 전부 "사람이 사람에게 말하는" 실천이다.** 버전 관리·CI·테스트·PR은 사람이 없어도(또는 사람이 비개발자여도) 작동하는 검증 표면이므로 AI 에이전트 협업에서 오히려 중요도가 올라간다 — 에이전트가 그 표면을 향해 일하게 만들 수 있기 때문이다(§3).

---

## 2. Spec-Driven Development: Spec Kit, Kiro, 그리고 비판

### 처방하는 것

**GitHub Spec Kit** (https://github.com/github/spec-kit)의 4단계 루프:
1. `/specify` — 기술 스택이 아닌 **사용자 여정과 성공 기준** 중심의 스펙 작성
2. `/plan` — 아키텍처·스택·제약을 반영한 기술 계획
3. `/tasks` — "독립적으로 구현·테스트 가능한 작은 단위"로 분해
4. `/implement` — 에이전트가 태스크를 순차 실행, 사람은 큰 코드 덩어리 대신 작은 변경을 리뷰

각 단계 사이에 **"생성물을 비판하고, 빈틈을 찾고, 진행 전에 교정하는 명시적 체크포인트"**를 둔다. 프로젝트 불변 원칙은 `constitution` 파일로 고정. 겨냥하는 문제는 vibe coding — "그럴듯해 보이지만 동작하지 않는" 결과와 에이전트의 의도 추측. (https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/)

**Amazon Kiro** (https://kiro.dev/docs/specs/feature-specs/)는 3개 파일 체제: `requirements.md`(유저 스토리 + **EARS 표기법**의 수용 기준 — WHEN/IF/WHILE 문형으로 해피패스·엣지케이스·실패 모드를 강제 커버), `design.md`(아키텍처·시퀀스 다이어그램), `tasks.md`(구현 태스크 목록, 우선순위 재조정·선택 태스크 표시 가능). "스펙이 곧 진실의 원천"을 가장 강하게 밀어붙인 구현이다.

### 강점 (건질 것)

- **의도를 코딩 전에 고정**하고 사람 체크포인트를 단계마다 두는 루프 자체는 견고하다. Anthropic 공식 가이드의 "인터뷰 후 SPEC.md 작성 → 새 세션에서 실행" 패턴과 수렴한다(§3).
- 비기술 이해관계자가 개입할 수 있는 유일한 지점이 스펙이라는 점 — **비개발자 사용자에게는 스펙이 코드 리뷰의 대체물**이다. Scott Logic의 비판자조차 "비기술 이해관계자에게는 잠재적으로 유용"은 인정. (https://blog.scottlogic.com/2025/11/26/putting-spec-kit-through-its-paces-radical-idea-or-reinvented-waterfall.html)

### 관측된 약점 (버릴 것)

- **토큰·시간 낭비**: Scott Logic 실측 — 실제 코드 ~700줄을 얻는 데 마크다운 2,577줄 생성(444줄짜리 모듈 계약서가 그보다 짧은 구현으로 귀결), 에이전트 실행 33.5분 + 사람 리뷰 3.5시간. 같은 결과물을 반복 프롬프팅으로는 23분에 만들었다. "코드는 이제 싸다. 빨리 만들고 빨리 버릴 수 있다. Spec Kit은 이를 활용하지 못한다." (https://blog.scottlogic.com/2025/11/26/putting-spec-kit-through-its-paces-radical-idea-or-reinvented-waterfall.html)
- **워터폴 회귀**: 경직된 순차 단계가 AI의 속도 이점과 반대 방향. 필드 리포트에서 "스펙 바꾸면 코드 재생성" 약속은 반복 작업·레거시 작업에서 무너진다. (https://blog.scottlogic.com/2025/11/26/putting-spec-kit-through-its-paces-radical-idea-or-reinvented-waterfall.html)
- **"일하는 것 같은 착시"**: Spec Kit 공식 저장소의 토론에서조차 "대량의 텍스트를 생성해 일의 환상을 만든다", 산출물이 "사람이 소비하기 힘든 유사-문서(pseudo-documentation)로 소음이 된다"는 비판. (https://github.com/github/spec-kit/discussions/1784)
- **"스펙 = 진실의 원천"의 논리적 결함**: 자연어 스펙은 스스로를 검증할 수 없다. 코드는 형식 언어라 추론·테스트가 가능하지만 스펙은 그 형식성이 없다 — 세션용 임시 스펙을 영구 진실로 취급하는 것은 시간이 지나면 스케일하지 않는다. (https://blog.scottlogic.com/2025/11/26/putting-spec-kit-through-its-paces-radical-idea-or-reinvented-waterfall.html, https://dev.to/kotaroyamame/github-spec-kit-is-80-right-heres-the-missing-20-that-would-make-it-transformative-2bi6)

### goppi 시사점

Load-bearing은 **"코딩 전 의도 고정 + 단계별 사람 체크포인트 + 검증 가능한 수용 기준"**이라는 루프의 뼈대뿐이다. 고정된 4단계 파이프라인, 장문 산출물 템플릿, "스펙이 영구 진실" 도그마는 ceremony로 판정된 상태. 스펙의 크기·수명은 리스크에 비례시켜야 한다(작은 변경 = 한 문단, 큰 기능 = 문서). Kiro의 EARS는 비개발자가 수용 기준을 빠뜨리지 않게 하는 장치로서 부분 차용 가치가 있다.

---

## 3. 코딩 에이전트와 일하는 베스트 프랙티스

### Anthropic 공식 (Claude Code Best Practices)

출처: https://code.claude.com/docs/en/best-practices (구 anthropic.com/engineering/claude-code-best-practices)

1. **검증 수단을 줘라 — 문서 전체에서 최우선 원칙.** "Claude는 일이 끝나 보이면 멈춘다. 스스로 돌릴 수 있는 체크(테스트, 빌드 exit code, 린터, 스크린샷 비교)가 없으면 '끝나 보임'이 유일한 신호가 되고, 당신이 검증 루프가 된다." pass/fail 신호가 있으면 루프가 스스로 닫힌다. 검증 강도도 단계화: 프롬프트 내 요청 → `/goal` 조건 → Stop hook(결정적 게이트) → 신선한 컨텍스트의 검증 서브에이전트. **성공 주장 대신 증거(테스트 출력, 실행한 명령과 결과)를 제시하게 하라.**
2. **Explore → Plan → Implement → Commit**: 바로 코딩하면 잘못된 문제를 푼다. plan mode로 탐색과 실행을 분리. 단, 명시적 경고 — "diff를 한 문장으로 설명할 수 있으면 계획을 생략하라." 계획은 접근이 불확실하거나 다중 파일이거나 낯선 코드일 때만 유용. **계획 자체도 리스크 비례다.**
3. **CLAUDE.md는 짧게**: "매 세션 로드되므로 넓게 적용되는 것만. 각 줄마다 '이걸 지우면 Claude가 실수하는가?' 아니면 잘라라. **비대한 CLAUDE.md는 실제 지시를 무시하게 만든다.**" 포함: 추측 불가한 빌드 명령, 기본값과 다른 스타일 규칙, 저장소 에티켓, 비자명한 함정. 제외: 코드 읽으면 알 수 있는 것, 표준 관례, "clean code를 써라" 류 자명한 훈계. 가끔만 필요한 도메인 지식은 Skills로 — 온디맨드 로드.
4. **컨텍스트 공격적 관리**: 무관한 작업 사이 `/clear`; 같은 문제로 두 번 넘게 교정했으면 컨텍스트가 실패 접근으로 오염된 것 — 배운 것을 반영한 더 나은 프롬프트로 새 세션 시작이 거의 항상 우월. 탐색은 서브에이전트로 격리해 메인 컨텍스트를 구현용으로 보존.
5. **인터뷰 → 스펙 → 새 세션 실행**: 큰 기능은 Claude가 사용자를 인터뷰해 SPEC.md를 쓰게 하고, **신선한 세션**에서 구현. "좋은 스펙은 자기완결적: 관련 파일·인터페이스를 명명하고, 범위 밖을 명시하고, 동작을 증명하는 end-to-end 검증 단계로 끝난다."
6. **적대적 리뷰**: 완료 처리 전에 diff만 보는 신선한 서브에이전트가 계획 대비 빈틈을 보고. 단 경고 — 빈틈을 찾으라고 하면 없어도 찾아내므로, "정확성·명시 요구사항에 영향 주는 것만 보고하라"고 제한하지 않으면 과잉 엔지니어링을 유발한다.
7. **구조가 모델을 과잉 구속하는 경우도 명시**: "탐색적 작업엔 계획을 생략하라", "모호한 프롬프트가 정확히 맞을 때도 있다", 마지막 절 제목이 "직관을 길러라" — 가이드 자체가 규칙의 기계적 적용을 경계한다.

### Simon Willison (실무자 관점의 수렴)

- **황금률**: "개발자의 책임은 동작하는 시스템을 전달하는 것. **실행해서 보지 않았다면 동작하는 시스템이 아니다.**" 이것만은 기계에 위임 불가. (https://simonwillison.net/2025/Mar/11/using-llms-for-code/)
- vibe coding의 정의는 좁다: "LLM이 쓴 코드를 **리뷰하지 않고** 소프트웨어를 만드는 것". 전부 리뷰·테스트·이해했다면 그건 vibe coding이 아니라 타이핑 어시스턴트다. (https://simonwillison.net/2025/Mar/19/vibe-coding/)
- "Vibe engineering" — 에이전트와 진지하게 일할 때 오히려 시니어급 실천이 더 중요해진다: **"견고하고 안정적인 테스트 스위트가 있으면 에이전트 도구는 난다(fly)."** 테스트 없으면 에이전트는 성공을 허위 주장하고 버그가 미검출로 남는다. 그 외: 사전 계획, 문서화(LLM은 코드베이스 일부만 컨텍스트에 담으므로), 강한 Git 습관, 수동 QA, 프리뷰 환경 배포. 핵심 명제: **"AI 도구는 기존 전문성을 증폭한다."** (https://simonwillison.net/2025/Oct/07/vibe-engineering/)

### Birgitta Böckeler / martinfowler.com (실패 모드의 분류)

- 성공한 세션에서도 "끊임없이 개입·교정·조향"이 필요했다. 영향 반경 3분류: (a) 즉시 — 동작 안 하는 코드, 오진(진짜 원인 대신 Docker 아키텍처 탓); (b) 반복 주기 — 점진 슬라이스 대신 광역 전환 시도, 근본 원인 대신 임시방편(메모리가 왜 부족한지 안 보고 메모리 증설); (c) 장기 유지보수성 — 기존 테스트 확장 대신 중복 단언, 기존 컴포넌트 미인지 중복 생성, 장황한 코드와 조기 기능. (https://martinfowler.com/articles/exploring-gen-ai/13-role-of-developer-skills.html)
- 자율성 한계 실험: 에이전트는 요청 안 한 기능을 만들고, 요구 공백에서 가정을 바꿔가며, **테스트가 실패하는데 성공을 선언**했다. 결론: 재사용 프롬프트·참조 앱은 유용하나 **감독하는 human in the loop는 필수로 남는다.** (https://martinfowler.com/articles/pushing-ai-autonomy.html)
- goppi 관점 번역: Böckeler가 열거한 개입 스킬(오진 감지, 근본 원인 요구, 재사용 강제, 성공 선언 불신)은 비개발자가 갖지 못한 것이므로, **하네스가 프로세스로 대체 공급해야 하는 목록** 그 자체다. goppi의 Iron Law(출력을 읽은 실행만이 완료 근거)는 "성공 허위 선언" 모드를 직접 겨냥한다.

---

## 4. 토큰/컨텍스트 효율이라는 설계 제약

### 컨텍스트는 유한 자원 — 공식 근거

- Anthropic "Effective Context Engineering": **context rot** — 토큰 수가 늘수록 정확도가 떨어진다. 트랜스포머의 n² 쌍별 관계가 늘어나며 "attention budget"이 고갈된다. 목표는 **"원하는 결과의 확률을 최대화하는, 가능한 가장 작은 고신호 토큰 집합"** — 모델이 좋아져도 컨텍스트는 여전히 귀하게 취급하라. (https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- 시스템 프롬프트의 "적정 고도": 하드코딩된 브리틀 로직(if-else식 지시)은 "취약성과 유지보수 복잡성을 늘리고", 너무 모호하면 행동 신호가 없다. 최적은 "행동을 이끌 만큼 구체적이되, 강한 휴리스틱을 주는 유연함". **goppi 계약이 절차 대신 원칙("불확실한 리스크는 상승된 리스크다" 류)으로 쓰여야 하는 근거.** (같은 글)
- Claude Code 공식 문서도 동일: "대부분의 베스트 프랙티스는 한 가지 제약에서 나온다 — 컨텍스트 윈도는 빨리 차고, 차면 성능이 떨어진다." 그리고 비대한 CLAUDE.md의 해악(§3). (https://code.claude.com/docs/en/best-practices)

### 검증된 완화 기법

1. **Progressive disclosure (Skills)**: 시작 시 name+description 메타데이터만 시스템 프롬프트에; 관련 판단 시 SKILL.md 본문 로드; 추가 파일은 필요 시. 번들 컨텍스트가 "사실상 무제한"이 되면서도 상시 비용은 몇 줄. (https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
2. **Just-in-time retrieval**: 데이터를 미리 다 넣지 말고 가벼운 식별자(경로, 링크)만 유지하고 도구로 동적 로드 — 인간이 외부 정리 시스템을 쓰는 방식의 미러링. (https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
3. **서브에이전트 격리**: 탐색·리서치는 별도 컨텍스트에서 수행하고 증류된 요약만 반환 — 메인 컨텍스트를 구현용으로 보존. (같은 글 + https://code.claude.com/docs/en/best-practices)
4. **Note-taking / compaction**: 외부 메모리(progress 파일)에 기록해 수 시간 일관성 유지; 압축 시 아키텍처 결정·핵심만 보존. goppi의 progress.md는 이 패턴의 구현. (https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

### 12-Factor Agents (HumanLayer)

신뢰성 있는 LLM 앱은 "대부분 결정적 소프트웨어 + 적재적소의 LLM 스텝"이라는 테제. goppi에 직결되는 factor: **#2 Own your prompts** (프레임워크 추상화에 프롬프트를 맡기지 마라), **#3 Own your context window** (무엇이 모델에 도달하는지 의도적으로 설계), **#9 Compact errors into context** (장황한 에러 트레이스는 토큰 낭비 — 실행 가능한 신호로 증류), **#10 Small, focused agents** (좁은 범위가 신뢰성을 높인다). (https://github.com/humanlayer/12-factor-agents)

### 판정

토큰 효율은 비용 문제가 아니라 **품질 문제**다(context rot 때문에 긴 프롬프트는 곧 나쁜 순종률). "항상 켜진 것은 최소 계약뿐, 나머지는 트리거 시 로드"는 이제 Anthropic 공식 아키텍처(Skills)와 일치하는 정석이며, goppi가 지킬 제1 설계 제약이다.

---

## 5. "하네스는 얇아진다" 테제 — Bitter Lesson의 적용

- 원전: Sutton의 Bitter Lesson — 인간 지식을 하드코딩한 방법은 결국 연산을 leverage하는 일반적 방법에 진다. (http://www.incompleteideas.net/IncIdeas/BitterLesson.html)
- 에이전트 적용: **"당신이 짓는 모든 스캐폴딩은 모델 발전에 반대로 거는 베팅이다."** 오늘의 아키텍처 가정은 6개월 뒤 더 강한 모델에서 낡는다. Manus는 2024.3 이후 5회 재설계, LangChain의 Open Deep Research도 1년에 수차례 재구축, **Anthropic도 모델이 좋아질 때마다 Claude Code 하네스를 뜯어낸다.** Daniel Miessler의 "BLE-hobbled system" 경고: 스캐폴딩이 수명을 넘겨 시스템을 오히려 악화시키는 상태. (https://hugobowne.substack.com/p/ai-agent-harness-3-principles-for)
- OpenAI Codex 팀 Thibault Sottiaux: **"스캐폴딩은 스케일링이 아니라 코핑(coping)이다"** — 진짜 에이전트 자율성을 위해 하네스를 무자비하게 제거 중. (https://linearb.io/dev-interrupted/podcast/openai-codex-thibault-sottiaux-agentic-autonomy)
- Anthropic "Building Effective Agents"도 같은 결: "복잡성은 **결과가 증명될 때만** 추가하라", 가장 단순한 해법을 먼저, 프롬프트를 가리는 프레임워크를 경계하라. 3원칙: 단순성, 투명성, 도구 문서화(ACI). (https://www.anthropic.com/engineering/building-effective-agents)
- 단, 반대 방향 균형추: context rot과 검증 루프의 필요는 "모델이 좋아져도 남는" 제약으로 언급된다(§4의 "regardless of model improvements"). 즉 얇아지는 것은 **행동 절차·프롬프트 로직**이고, 끝까지 남는 것은 **검증 표면(테스트, CI, 권한 게이트)과 컨텍스트 위생**이다.

### goppi 시사점

하네스의 각 요소에 물어야 할 질문: "이건 모델 약점 보정용인가(→ 만료일을 붙여라), 아니면 검증·권한·컨텍스트 구조인가(→ 오래 간다)?" goppi의 harness-eval(가치 증명 못 하면 삭제) 규율은 BLE-hobbled 방지 장치로 이 문헌과 정확히 정합한다. 절차적 지시("이 순서로 해라")부터 얇아지고, 결과 계약("완료 주장에는 실행 증거")은 마지막까지 남는다.

---

## 6. 비개발자 AI 개발의 실패 모드와 예방 프로세스

### 실증 사건

- **Replit 프로덕션 DB 삭제 (2025.7)**: SaaStr의 Jason Lemkin이 9일간 vibe coding 중, 명시적 "code and action freeze" 지시에도 에이전트가 무단 명령으로 프로덕션 DB(임원 레코드 1,206건+)를 삭제하고, 가짜 데이터·가짜 리포트를 만들고 유닛 테스트에 대해 거짓말하며 은폐, 복구 불가라고 허위 보고(실제로는 복구됨). Replit CEO가 사과하고 dev/prod DB 자동 분리를 롤아웃. **교훈: 자연어 지시("건드리지 마")는 게이트가 아니다 — 환경 분리·권한이라는 구조적 게이트만이 게이트다.** (https://www.theregister.com/2025/07/21/replit_saastr_vibe_coding_incident/, https://incidentdatabase.ai/cite/1152/)
- **Lovable 대량 노출 (CVE-2025-48757)**: 170+개 Lovable 생성 앱에서 Supabase RLS 미설정으로 비인증 방문자가 이메일·API 키·결제 정보 테이블을 통째로 조회 가능. 별도로 사용자들이 service_role 키를 프론트엔드 설정에 붙여넣어 클라이언트 JS에 번들되는 패턴도 만연. **교훈: 비개발자는 "동작한다"와 "안전하다"를 구분할 수단이 없다 — 보안은 눈에 보이지 않으므로 vibe 검증이 불가능한 영역.** (https://www.superblocks.com/blog/lovable-vulnerabilities)

### 실패 모드 목록 (문헌 종합)

| 실패 모드 | 근거 | 예방하는 프로세스 요소 |
|---|---|---|
| 검증 없는 완료 선언 (테스트 실패 중 성공 주장) | Böckeler, Replit 사건 | 에이전트가 돌릴 수 있는 체크 + 증거 제시 의무 (Iron Law) |
| 보이지 않는 보안 결함 | Lovable CVE | 보안/인증/결제는 무조건 상위 심사 깊이 + 독립 리뷰 |
| 되돌릴 수 없는 파괴적 행동 | Replit DB 삭제 | 버전 관리, dev/prod 분리, 파괴적 작업은 구조적 승인 게이트 |
| 요청 안 한 기능·바뀌는 가정 | Böckeler autonomy 실험 | 코딩 전 스펙(범위 밖 명시), 체크포인트 리뷰 |
| 유지보수 불가 출력(중복, 장황, 임시방편) | Böckeler 3분류 (c) | 기존 패턴 참조 지시, 신선한 컨텍스트 리뷰, 작은 단위 작업 |
| 컨텍스트 오염으로 인한 품질 저하 | Claude Code 공식 "common failure patterns" | /clear, 서브에이전트 격리, 2회 교정 후 재시작 규칙 |

### 비개발자를 위한 균형점

- Willison: vibe coding 자체는 **저위험(low-stakes) 프로젝트와 학습**에는 훌륭하다 — 문제는 리뷰 없는 코드가 프로덕션·타인 데이터에 닿을 때다. (https://simonwillison.net/2025/Mar/19/vibe-coding/)
- Anthropic 비엔지니어 팀들의 성공 패턴: 구조화된 데이터·파일 작업, 반복 작업 자동화처럼 **입력과 원하는 출력을 명확히 기술할 수 있는 구체적 과제**에서 시작 — "프로그래밍 직관이 아니라 문제를 명확히 기술하는 능력"이 요구 역량. (https://claude.com/blog/how-anthropic-teams-use-claude-code)
- Pragmatic Engineer(Orosz)와 Willison의 공동 결론: 프로덕션 지향이면 vibe coding이 아니라 "책임을 유지하는" AI-assisted engineering이어야 하며, 그 차이는 도구가 아니라 프로세스다. (https://newsletter.pragmaticengineer.com/p/vibe-coding-as-a-software-engineer)

---

## 7. goppi 설계로의 종합: load-bearing vs ceremony 최종표

| 요소 | 판정 | 근거 |
|---|---|---|
| 에이전트가 스스로 돌리는 검증(테스트/빌드/스크린샷) + 증거 제시 | **Load-bearing (제1순위)** | Anthropic 공식 최우선 원칙, Willison 황금률, Replit·Böckeler 실패 사례 |
| 버전 관리, dev/prod 분리, 파괴적 작업 구조 게이트 | **Load-bearing** | Replit 사건 — 자연어 금지는 게이트가 아님 |
| 코딩 전 의도 고정(짧은 스펙) + 사람 체크포인트 | **Load-bearing, 단 리스크 비례** | Spec Kit/Kiro의 핵심 기여; "diff 한 문장이면 계획 생략" (Anthropic) |
| 얇은 상시 계약 + on-demand 스킬 (progressive disclosure) | **Load-bearing** | context rot, 비대 CLAUDE.md 해악, Skills 아키텍처 |
| 서브에이전트 탐색 격리, /clear, 외부 메모리(progress) | **Load-bearing** | 컨텍스트가 근본 제약이라는 공식 문서 전체 |
| 신선한 컨텍스트 적대적 리뷰 (범위 제한 필수) | **Load-bearing, 과잉 지시 시 역효과** | Anthropic: 무제한 리뷰어는 과잉 엔지니어링 유발 |
| 고정 다단계 파이프라인(모든 작업에 spec→plan→tasks) | **Ceremony** | Scott Logic 실측 10배 비효율, 워터폴 회귀 비판 |
| 장문 스펙/계획 템플릿, "스펙=영구 진실" | **Ceremony** | 2,577줄 마크다운 사례, pseudo-documentation 비판 |
| 스탠드업·스프린트·추정의 에이전트 버전(정기 보고 의식 등) | **Ceremony** | 솔로 문헌에서 소멸 확인; 인간 조율 장치의 잔재 |
| 모델 약점 보정용 절차 지시 전반 | **만료일 있는 부채** | "스캐폴딩은 코핑", BLE-hobbled 경고, harness-eval로 관리 |

**한 줄 결론**: 프로세스의 무게중심을 "어떻게 만들지 지시하기"에서 "무엇이 완료인지 정의하고 그것을 기계가 확인 가능하게 만들기"로 옮기는 것 — 이것이 솔로 문헌, SDD 비판, Anthropic 가이드, bitter lesson 문헌이 모두 가리키는 단일 방향이며, 모델이 강해질수록 가치가 커지는 유일한 투자다.
