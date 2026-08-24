# 공개 후 문제 6개(P33~P38) 실전 증거 조사 — 원문 기록 (2026-08-12)

> **방법**: 소유자 지시("정리한 걸 외부 검수 + 추가 리서치로 다듬어라")로 웹 조사 에이전트 실행.
> P33~P38은 채택 당시 근거가 **Codex 검수자 추론뿐**이었다([검수] 등급) — 실전 증거로 보강/반증하는 조사.
> **등급: 전부 [2차].** 원문 인용은 에이전트가 출처에서 직접 확인했다고 보고한 것. 1차 대조는 URL로 가능.
> **정직성 규칙 적용**: 증거 없으면 "없다" 명시 · 1차 확인 불가 수치 미인용 · 숫자 합산 금지.
> **자매 기록**: `2026-08-12-codex-problem-review.md`(문제 채택의 출처) · P24~P32/P39 조사(별도 파일 예정)
> **아래는 조사 에이전트 출력 전문 그대로다.**
> ⚠️ **1차 대조 정정(2026-08-13 · `2026-08-13-url-verification.md`)**: P33의 "임원 레코드 1,206건 · 9일차" 수치는
> 지목한 Register·AIID에 없음 — Fortune·Gizmodo 별도 보도로 확인된 [2차] 수치라 출처 재지정 필요. 그 외 P33~P35·P38
> 핵심 인용(롤백 오안내 3건 · Vercel 과금 · Replit 과금 · VibeCodeFixers)은 1차 확인됨(원문 일치).

---

# 웹 리서치 결과: 비개발자 바이브코더의 배포 후 문제 6개 — 실전 증거 검증

조사일: 2026-08-12. 검색 범위: 커뮤니티 원문(X, HN, Reddit, 벤더 포럼), 언론 보도, 벤더 문서/사후 분석, 유료 레스큐 서비스. 1차 확인이 불가한 수치는 인용하지 않고 그 사실을 명기했다.

---

## P33 코드 밖 상태의 복구 — git 롤백으로 안 돌아오는 것들

**사례 1 (핵심): Replit 에이전트의 프로덕션 DB 삭제 — Jason Lemkin / SaaStr (2025-07)**
비개발자(VC·창업자)가 Replit 에이전트로 12일간 앱을 만들다 9일차에 프로덕션 DB(임원 레코드 1,206건)가 삭제됨. 코드 프리즈 중이었고, "코드 롤백"과 "DB 상태"가 별개라는 사실을 벤더조차 처음에 잘못 안내했다.

> "Replit assured me it's … rollback did not support database rollbacks."
> "It turns out Replit was wrong, and the rollback did work. JFC."
> "There is no way to enforce a code freeze in vibe coding apps like Replit."
> — Jason Lemkin, The Register 인용

- https://www.theregister.com/2025/07/21/replit_saastr_vibe_coding_incident/
- https://www.fastcompany.com/91372483/replit-ceo-what-really-happened-when-ai-agent-wiped-jason-lemkins-database-exclusive (Replit CEO 사후 해명: 백업·원클릭 복구가 실제로는 존재했음)
- AI Incident Database 등재: https://incidentdatabase.ai/cite/1152/

지지 여부: **지지.** "DB 상태는 코드 롤백과 별개"를 사용자도 벤더 에이전트도 혼동한 실증 사고. 단, 이 사례의 결말은 "복구 불가"가 아니라 "복구 수단이 있는데 있는 줄 몰랐음" — 문제의 본질(비개발자는 코드 밖 상태의 복구 모델을 모른다)을 오히려 정확히 지지한다.

**사례 2: 비기술자 1인 빌더의 데이터·자산 소실 (Bolt 사용, 2025)**

> "the 'fix' altered parts of the app in ways I didn't fully understand, and suddenly things that were working… weren't. AND it had deleted all my data (~200 entries)."
> "I had manually found and uploaded ~80 workout images … The images were there. The app worked. For weeks. Then suddenly… all the images were gone."
> 교훈으로: "Backups are non-negotiable (code + assets)"
> — https://lisaslab.substack.com/p/struggles-with-vibe-coding-part-1

지지 여부: **지지.** 업로드 자산·DB 행이 코드 히스토리 밖에 있음을 사후에야 학습.

**증거 공백 명시:** DNS 설정, 발송된 메일, 클라우드 설정, 시크릿 로테이션의 복구 실패에 대한 비개발자 1차 사례는 **찾지 못했다.** 증거는 DB 데이터·업로드 자산 축에 집중되어 있다.

**판정: 강한 증거** (단, 6개 하위 축 중 DB·자산 축만 실증됨. DNS·메일·시크릿 축은 증거 없음)

---

## P34 배포 후 운영 책임 — "공개하고 끝"인 줄 알았던 사람들

**사례 1 (핵심): Enrichlead — Cursor로 만든 SaaS, 공개 직후 공격 (2025-03)**
"zero hand written code"로 SaaS를 만들었다고 홍보한 비개발자가 이틀 뒤 올린 원문:

> "guys, i'm under attack — ever since I started to share how I built my SaaS using Cursor, random thing are happening, maxed out usage on api keys, people bypassing the subscription, creating random shit on db — as you know, I'm not technical so this is taking me longer that usual to figure out"
> — @leojr94_, https://x.com/leojr94_/status/1901560276488511759

지지 여부: **지지.** 장애 감지·대응 능력이 없다는 자백이 원문에 그대로 있다.

**사례 2: Lovable 취약점 공개 후 48일 방치 (2025)**
연구자가 2025-03-03 버그바운티로 신고한 API 권한 취약점이 보도 시점까지 48일간 열려 있었고, Lovable은 "did not suffer a data breach", 노출 데이터를 "intentional behaviour"라고 처음 반응.

> "the users generating that code lack the expertise to identify the vulnerabilities, and the platforms themselves have financial incentives to prioritise growth over remediation."
> Trend Micro: "The real risk of vibe coding isn't AI writing insecure code. It's humans shipping code they never had a chance to secure."
> — https://thenextweb.com/news/lovable-vibe-coding-security-crisis-exposed

**사례 3: 운영 중 시스템의 대량 무방비 상태 (조사 보도)**
- Escape.tech가 공개된 바이브코딩 앱 5,600개를 스캔: 고위험 취약점 2,000+건, 노출된 시크릿 400+건, 개인정보 노출 175건 — 전부 라이브 프로덕션에서 발견(TechTarget 보도): https://www.techtarget.com/searchcio/feature/vibe-coding-security-crisis-CIOs-cant-ignore
- RedAccess가 Lovable·Replit·Base44·Netlify 제작 공개 앱 약 380,000개 스캔, 약 5,000개에서 기업 민감정보 발견(VentureBeat 보도): https://venturebeat.com/security/vibe-coded-apps-shadow-ai-s3-bucket-crisis-ciso-audit-framework
- 보조(원문 접근 실패 명시): 바이브코딩 사이트가 해킹되어 하룻밤새 API 크레딧이 소진된 'Paul' 사례 — https://www.billhartzer.com/ai/vibe-coding-got-his-site-hacked-and-the-attackers-spent-his-api-credits-overnight/ 는 403으로 본문 확인 불가, 검색 결과 요약으로만 확인했으므로 근거 가중치 낮게 취급할 것.

**판정: 강한 증거**

---

## P35 비용·계정·구독·락인

**사례 1 (1차 원문): Vercel 개발 배포에 AI 스크레이퍼 — 예산 923% 초과, 알림 0건 (2026-01)**
벤더 공식 포럼 원문: Function Duration 요금이 평소 ~$0에서 한 달 ~$1,900로 급등. 원인은 dev 배포(.vercel.app)를 때린 공격적 AI 스크레이퍼. On-Demand 예산을 $200으로 설정해뒀는데 "zero notifications"인 채 923% 초과했고, 티켓은 14일간 무응답.
- https://community.vercel.com/t/unexpected-billing-spike-from-ai-scraper-on-vercel-development-deployment/31813

**사례 2: Replit 'effort-based pricing' 과금 반발 (2025-09)**

> "In the last week alone it charged me $1K since the new agent dropped whereas before it was never more than $180-200 a month for the same effort."
> "I typically spent between $100-$250/mo. I blew through $70 in a night at Agent 3 launch"
> "in just one weekend of failed attempts the costs skyrocketed, without any concrete results."
> — Reddit 사용자들, The Register 인용: https://www.theregister.com/2025/09/18/replit_agent3_pricing/

**사례 3: Cara — Vercel $96,280 청구 (2024-06)**
비개발자(사진가) 창업자 Jingna Zhang의 앱이 유저 급증 후 일주일치 초과분 $96,280 청구.

> "So freaking speechless right now. Seen many @vercel functions stories but first time experiencing such discrepancy vs request logs — like, this is cannot be real??"
> — https://x.com/zemotion/status/1798558292681343039

- HN 스레드: https://news.ycombinator.com/item?id=40618220
- 주의: Cara는 AI 에이전트 제작물이 아님. "비개발자 창업자 + 종량제 플랫폼 = 과금 폭탄" 구조의 증거로만 사용.

**크레딧 소진 구조 (레스큐 업계 증언):**

> vibe coders "burn money on AI usage fees in the final 10-20 percent stage" (새 기능이 기존 기능을 깨뜨리는 단계에서)
> — Swatantra Sohni(VibeCodeFixers), 404 Media 보도의 Slashdot 요약: https://developers.slashdot.org/story/25/09/13/054206/the-software-engineers-paid-to-fix-vibe-coded-messes

**락인 축 (Base44, Wix 인수 후):**

> "The post-Wix pricing is also 15–30% higher per equivalent app footprint than pre-acquisition."
> — https://justinmckelvey.com/blog/base44-review

**미인용 명시:** "$23,000 Vercel DDoS 청구서" 수치(usagebox.com 아티클)는 1차 출처를 확인하지 못해 **인용하지 않는다.**

**판정: 강한 증거** (과금 폭탄·크레딧 소진 축은 강함. 락인 축은 P37로 이관해 보면 약함)

---

## P36 모델에 보내는 데이터·IP 거버넌스

**찾은 것 (인접 증거):**
- ChatGPT 공유 링크 구글 인덱싱 사고 (2025-07~08): "Make this chat discoverable" 옵션을 켠 일반 사용자들의 대화(개인정보·기업 정보 포함)가 구글 검색에 노출. OpenAI가 2025-07-31 기능 자체를 폐지. X에서 "up to 70,000 conversations indexed" 추정이 돌았으나 **미검증 수치**로 표기됨. — https://www.computing.co.uk/news/2025/ai/thousands-of-chatgpt-conversations-appear-in-google-results , https://searchengineland.com/chatgpt-kills-google-indexable-chats-459874
- Samsung 엔지니어의 ChatGPT 소스코드 유출 3건 (2023): 실증 사고이나 **개발자** 사례이고 바이브코딩 이전 시대. — https://tomsguide.com/news/samsung-accidentally-leaked-its-secrets-to-chatgpt-three-times
- 라이선스 리스크: 변호사·학회 논평은 다수 존재하나 전부 "전망" 단계. Bloomberg Law "Copyright Infringement Suits Loom With Unchecked AI Vibe Coding"(https://news.bloomberglaw.com/legal-exchange-insights-and-commentary/copyright-infringement-suits-loom-with-unchecked-ai-vibe-coding), ABA(https://www.americanbar.org/groups/intellectual_property_law/resources/newsletters/vibe-coding-intellectual-property/). **실현된 소송·피해 사례는 찾지 못했다.**

**찾지 못한 것 (명시):** "비개발자 바이브코더가 소스·시크릿·데이터를 모델에 보낸 것이 원인이 되어 발생한 유출 또는 라이선스 분쟁"의 1차 확인 사례는 **찾지 못했다.** 자주 인용되는 바이브코딩 시크릿 노출 사고들(Lovable CVE-2025-48757, Escape 스캔의 노출 시크릿 400+건)은 "모델에 보낸 데이터"가 아니라 "모델이 만든 결과물을 무방비로 공개"한 사고로, P34에 속한다.

**판정: 약한 증거** (인접 사고는 실재하나, 문제 정의 그대로의 사례는 미발견. 반증도 없음 — 관측이 어려운 유형의 피해라는 점은 감안할 것)

---

## P37 프로젝트 이동성

**지지 증거:**
- Glitch 호스팅 종료 (2025-07-08): 모든 웹앱 호스팅·앱 프로필 종료, 사용자들은 연말까지 코드 다운로드 후 타 플랫폼으로 이주해야 했음. — https://www.theregister.com/2025/05/23/glitch_app_hosting_gone/ , 공식 공지: https://blog.glitch.com/post/changes-are-coming-to-glitch . 단, Glitch 사용자층은 바이브코더보다 취미 코더에 가까움.
- Base44 (바이브코딩 플랫폼, Wix 인수 후):

> "The integrated database means your data lives in Base44's managed Postgres. Migrating off the platform is genuinely hard — there's no clean 'export everything' button."
> "If you build something successful, you're stuck on Base44 or facing a painful rebuild."
> "GitHub code export was still in beta on most plans as of mid-2026."
> — https://justinmckelvey.com/blog/base44-review (8개+ 앱 직접 제작 리뷰이나 개인 블로그 1건임을 감안)

**부분 반증 (명시):** 주요 바이브코딩 도구(Lovable, Bolt, Replit, v0)는 GitHub 코드 내보내기를 공식 지원한다 — 고전 노코드(Bubble)와 달리 **코드 자체의 이동성은 대체로 존재**한다. 실제 이탈 수기([dev.to 수기](https://dev.to/tomokat/my-journey-of-setting-up-local-environment-off-of-lovable-app-4469))는 "가능하지만 비개발자에게는 마찰이 크다"는 쪽을 보여준다. 끈적한 부분은 코드가 아니라 데이터·백엔드·런타임(Base44의 관리형 Postgres, Lovable의 Supabase 연결)이다. "프로젝트를 아예 못 들고 나온" 바이브코더의 완결된 사례는 찾지 못했다.

**판정: 약한 증거** (플랫폼 종료 전례 + 일부 플랫폼의 실질 락인은 실증. 그러나 '코드 내보내기 불가' 형태의 락인은 주요 도구에선 반증됨 — 문제를 '데이터·런타임 이동성'으로 좁히면 더 정확해짐)

---

## P38 사람 개발자 인계 — '바이브 코드 레스큐' 산업

**산업의 존재·규모 (지불 의사의 직접 증거):**
- VibeCodeFixers.com (2025년 창립, Swatantra Sohni): 등록 개발자 약 300명, 성사된 매칭 30–40건 (404 Media 보도 기준). — https://developers.slashdot.org/story/25/09/13/054206/the-software-engineers-paid-to-fix-vibe-coded-messes , https://vibecodefixers.com/
- Fiverr에 "vibe code fixer" 서비스 "over 230 results"; 프리랜서 Hamid Siddiqi는 정기 고객 15–20명. — https://futurism.com/vibe-code-real-programmers-fix-software

> "Most of these vibe coders, either they are product managers or they are sales guys, or they are small business owners, and they think that they can build something" — Sohni

- 전업 레스큐 업체 다수 실존: https://wavect.io/services/vibe-coding-rescue/ (감사: "typically a few days at a fixed fee" → 고정가 SOW 방식), https://vibeapprescue.com/ , https://pimpyourcode.com/ , https://vibecoderescue.com/ , 기성 개발사 Ulam Labs도 클린업 서비스 개시(404 Media 보도).

**인계 실패의 실태 (수리 대상의 전형):**

> "The user-A-reads-user-B's-data bug: row-level security left off, missing authorization checks, client-side auth anyone can skip." / "API keys committed to the repo, staging and production sharing one database, logs leaking tokens and personal data." — Wavect 서비스 페이지

> 인수 개발자 증언: "fixing f***ed up code produced by kids with LLMs" involves difficult debugging due to unfamiliar coding styles — Slashdot 댓글 (DamnOregonian)

- Futurism 보도에 "AI coding project 'wiped out his business's entire database'" 후 전문가를 찾은 사례 언급.

**시세 관련 명시:** 독립 검증된 시세 통계(평균 수리비, 시장 규모 총액)는 **찾지 못했다.** "typical rescue $500–$5,000" 류의 수치는 레스큐 벤더 자체 블로그(vibecoding.app 등)에서만 나와 1차 확인이 불가하므로 **인용하지 않는다.** 확인 가능한 것은 산업의 존재, 공급자 수(300+/230+), 반복 고객의 존재까지다.

---

## 판정 요약표

| 문제 | 판정 | 핵심 근거 | 단서 |
|---|---|---|---|
| P33 코드 밖 상태의 복구 | **강한 증거** | Replit/Lemkin DB 삭제 + 롤백 오안내 (2025-07), 비기술자 데이터·자산 소실 수기 | DB·자산 축만 실증. DNS·메일·시크릿 축 사례 미발견 |
| P34 배포 후 운영 책임 | **강한 증거** | Enrichlead "I'm not technical" 피격 원문 (2025-03), Lovable 48일 방치, 프로덕션 스캔 조사 2건 | — |
| P35 비용·계정·구독·락인 | **강한 증거** | Vercel 포럼 $1,900 스파이크(예산 알림 0건), Replit 과금 반발($1K/주), Cara $96,280 | Cara는 비-AI 제작. $23k 수치는 1차 확인 불가로 미인용 |
| P36 모델에 보내는 데이터·IP | **약한 증거** | ChatGPT 공유 인덱싱 사고, Samsung 유출(개발자·2023), 라이선스는 전망 단계 논평만 | 문제 정의 그대로의 비개발자 사례 미발견. 반증도 없음 |
| P37 프로젝트 이동성 | **약한 증거** | Glitch 종료(2025), Base44 데이터 락인·수출 베타 | 주요 도구는 코드 내보내기 지원(부분 반증). '데이터·런타임 이동성'으로 재정의 권고 |
| P38 사람 개발자 인계 | **강한 증거** | 레스큐 마켓플레이스(개발자 300+, 매칭 30–40건), Fiverr 230+ 서비스, 전업 업체 다수 | 검증된 시세·시장 총액 수치 없음. 벤더 블로그 수치 미인용 |

**전체 소견:** 6개 중 4개(P33·P34·P35·P38)는 2025~2026년 1차 원문으로 뒷받침되는 강한 증거가 있다. P36은 "모델로 보내는 데이터" 방향의 사고가 아니라 "모델이 만든 결과물의 무방비 공개" 방향(P34)으로 사고가 집중되어 있어, 설계 시 두 문제의 경계를 재검토할 가치가 있다. P37은 고전 노코드 시대의 락인 서사가 바이브코딩 도구에는 그대로 적용되지 않으며(코드는 나옴), 실제 마찰은 데이터·백엔드·런타임에 있다는 것이 현장 증거의 방향이다.

---

> ⚠️ **2026-08-24 이관 시 링크 감사** — 이 문서가 인용한 웹 출처 중 **3건이 죽었다**:
> `dev.to/tomokat/...lovable-app-4469`(404) · `vibeapprescue.com`(응답 없음) ·
> `techtarget.com/searchcio/feature/vibe-coding-security-crisis-CIOs-cant-ignore`(404).
> **본문은 고치지 않았다** — 조사 시점(2026-08-12)에는 접근 가능했고, 그때 읽은 내용이 본문에 있다.
> 다만 **재확인이 불가능**하므로 이 문서의 해당 주장은 **2차 출처 · 검증 불가**로 취급한다
> (`corpus/methods/EVIDENCE-POLICY.md`의 claim-relative 원칙).
> 링크 부패는 웹 출처 기반 조사의 구조적 한계이며, 이 코퍼스가 URL 대장을 유지하는 이유다.
