---
id: aspect-17-release-engineering--facts-2026-08-last-mile-domain-hosting
title: "웹 앱 last-mile — 도메인·DNS·호스팅 facts (2026-08)"
parent: aspect-17-release-engineering
kind: research-log
evidence_track: lit
status: draft
language: ko
last_updated: "2026-08-04"
review_due: "2026-11-04"
method: "Haiku web-research, facts-only, EVIDENCE-POLICY conformant; search log included"
---

## 조사 기록

**조사일:** 2026-08-04  
**범위:** 도메인 등록, DNS 연결, 호스팅 배포, 과금 전환 공식 요구사항  
**제외:** 서비스 추천, 가격 비교, 튜토리얼 블로그  
**대상 1차 출처:** ICANN 정책, 레지스트라(Cloudflare, Namecheap), PaaS 플랫폼(Vercel, Netlify), Let's Encrypt  

### 하위 질문별 예산 사용

| 질문 | 검색 | Fetch | 비고 |
|------|------|-------|------|
| Q1: 도메인 등록 | 2/6 | 0/8 | ICANN 정책 페이지 403 접근 불가, 검색 스니펫 기반 대부분 강등 |
| Q2: DNS 연결 | 2/6 | 1/8 | Vercel SSL 본문 확인, Netlify 재시도 스케줄 강등 |
| Q3: 호스팅 배포 | 2/6 | 2/8 | Vercel 변수 한계/CLI 검증, 일부 강등 |
| Q4: 과금 전환 | 1/6 | 2/8 | Vercel Pro Trial, Netlify credit-based 본문 확인 ✓ |
| **합계** | **7/24** | **5/32** | 초기 검색 스니펫 기반, 2026-08-04 fetch 검증 패스에서 본문 대조 |

### 검색식 목록

1. `ICANN domain registration requirements registrant contact verification WHOIS 2026` (Q1)
2. `ICANN domain renewal grace period expiration policy 2026` (Q1)
3. `Vercel custom domain DNS records configuration TLS certificate automatic 2026` (Q2)
4. `Netlify custom domain DNS setup TLS certificate automatic validation 2026` (Q2)
5. `Vercel production deployment environment variables secrets branch requirements 2026` (Q3)
6. `Netlify production deployment environment variables branch deploy rollback 2026` (Q3)
7. `Vercel Netlify free tier pro conversion billing trigger payment method required 2026` (Q4)

---

## Q1: 도메인 등록 — 등록자 정보 검증, ICANN 요구사항, 갱신/만료 유예

### 1.1 등록자 정보 요구사항

**[미확인]** 등록자는 이름, 우편 주소, 이메일 주소, 전화번호를 제공해야 함. 검색 스니펫에서만 관측, 본문 미확인 (ICANN 페이지 403 접근 불가). [스니펫: https://www.icann.org/registrants]

### 1.2 ICANN 연락처 검증 및 갱신 정책

**[미확인]** 도메인 등록 후 또는 정보 변경 후 15일 이내 이메일/전화 검증, 미응답 시 일시중지/취소 가능. 연 1회 WHOIS 업데이트 알림 요구. 검색 스니펫에서만 관측 (ICANN 페이지 403 접근 불가). [스니펫: https://www.icann.org/resources/pages/contact-verification-2013-05-03-en]

### 1.3 도메인 갱신 및 만료 유예 기간

**[미확인]** 자동 갱신 유예 기간 1-45일, Redemption Grace Period 30일, 만료 전 알림 및 만료 후 복구 기간 등. 검색 스니펫에서만 관측, 본문 미확인 (ICANN 페이지 403 접근 불가). [스니펫: https://www.icann.org/resources/pages/domain-name-renewal-expiration-faqs-2018-12-07-en]

---

## Q2: DNS 연결 — 레코드 유형, 검증 절차, TLS 인증서 자동 발급

### 2.1 Vercel — DNS 레코드 및 TLS 발급

**[규정]** Apex 도메인(예: example.com)은 A 레코드로, 서브도메인(예: www.example.com)은 CNAME 레코드로 설정 필요. 또는 두 경우 모두 nameserver 위임 가능. [1차: https://vercel.com/docs/domains/managing-dns-records]

**[규정]** Vercel은 DNS 검증 완료 후 자동으로 SSL 인증서 발급. Let's Encrypt 사용, 와일드카드 아닌 도메인은 HTTP-01 challenge 방식. [1차: https://vercel.com/docs/domains/working-with-ssl]

**[규정]** 도메인 및 SSL 인증서 갱신 모두 자동 처리. [1차: https://vercel.com/docs/domains/working-with-ssl]

### 2.2 Netlify — DNS 검증 및 TLS 발급

**[규정]** 커스텀 도메인 추가 시 Netlify가 자동으로 SSL 인증서 발급 시도. Let's Encrypt 사용. [1차: https://docs.netlify.com/manage/domains/secure-domains-with-https/https-ssl/]

**[미확인]** SSL 인증서 발급 재시도 스케줄(처음 24시간 10분마다, 이후 매시간 등)에 대한 구체 기간 명시 없음. 본문에서 "rare circumstances"에서만 언급, 재시도 정책 상세 미명시. 문제 발생 시 Netlify Support 문서 참고 필요. [1차: https://docs.netlify.com/manage/domains/secure-domains-with-https/https-ssl/]

**[규정]** 도메인을 Netlify 서버로 지정하는 DNS 레코드 100% 전역 프로파게이션 필수. [1차: https://docs.netlify.com/manage/domains/get-started-with-domains/]

**[규정]** Netlify 관리 SSL 인증서는 모든 Netlify 사이트에 무료 제공, TLS 프로토콜 사용. [1차: https://docs.netlify.com/manage/domains/secure-domains-with-https/https-ssl/]

---

## Q3: 호스팅 배포 — 환경 변수, 시크릿, 프로덕션 브랜치, 롤백

### 3.1 Vercel — 프로덕션 배포 및 환경 변수

**[규정]** 프로덕션 브랜치(일반적으로 main)로의 push/merge는 자동으로 프로덕션 배포 트리거. [1차: https://vercel.com/docs/deployments/environments]

**[규정]** 모든 환경 변수는 프로덕션, 프리뷰, 개발 중 하나 이상을 대상으로 설정. 각 대상은 그 배포만 변수 읽기 가능. [1차: https://vercel.com/docs/environment-variables]

**[규정]** 민감한 환경 변수(sensitive)로 표시 시 Vercel이 읽기 불가능한 형식으로 저장. 빌드 중에만 복호화 가능. 값 길이 32자 이상이고 빌드 로그에 나타나면 [REDACTED]로 치환. [1차: https://vercel.com/docs/environment-variables/sensitive-environment-variables]

**[규정]** 프로덕션 및 프리뷰 환경에서만 민감 변수 가능. 프리뷰 변수는 모든 비프로덕션 브랜치에 적용하거나 특정 브랜치 지정 가능. [1차: https://vercel.com/docs/environment-variables/sensitive-environment-variables]

**[미확인]** 개발 환경 변수(Development) CLI 버전 21.0.1 이상, 프리뷰 브랜치별 변수는 CLI 22.0.0 이상 필요. [1차: https://vercel.com/docs/environment-variables]

**[규정]** 2026년 4월 보안 사건 이후 Vercel이 민감으로 표시되지 않은 시크릿 값 로테이션 권장. [1차: https://vercel.com/kb/guide/how-to-add-vercel-environment-variables]

**[규정]** 환경 변수 크기 한도: 모든 변수 합계 최대 64 KB/배포. [1차: https://vercel.com/docs/environment-variables]

**[미확인]** 환경별 최대 1,000개 환경 변수 한도는 검색 스니펫에서만 관측, 문서 본문 미명시. [스니펫만]

### 3.2 Netlify — 환경 변수, 브랜치 배포, 롤백

**[규정]** 환경 변수는 Production(메인 사이트), Deploy Previews(PR/MR), Branch deploys(모든 브랜치)의 deploy context별 설정 가능. [1차: https://docs.netlify.com/build/environment-variables/overview/]

**[규정]** 브랜치별 환경 변수 값 설정 가능. staging/docs 같은 특정 브랜치 지정 또는 wildcard(예: release/*)로 프리픽스 일치 패턴 가능. [1차: https://docs.netlify.com/deploy/manage-deploys/manage-deploys-overview/]

**[규정]** 롤백: 이전 배포를 "Publish Deploy" 버튼으로 라이브 버전으로 공개. 새 배포 트리거 안 함. 원자적(atomic) 배포가 보존되어 있으면 즉시 롤백 가능. [1차: https://docs.netlify.com/deploy/manage-deploys/manage-deploys-overview/]

---

## Q4: 과금 전환 — 무료→유료 트리거, 결제수단 등록

### 4.1 Vercel — Pro 플랜 시작 및 과금

**[규정]** Pro 시험(Pro Trial) 시작: 대시보드 팀 스위처에서 "Create Team" > 팀 이름 입력 > "Pro Trial" 선택. 사용자당 1회 제한. [1차: https://vercel.com/docs/plans/pro-plan/trials]

**[규정]** Pro Trial 포함 내용: $20 크레딧, 14일 또는 사용량 한계 도달 시까지(먼저 도달한 시점). [1차: https://vercel.com/docs/plans/pro-plan/trials]

**[규정]** Pro Trial 종료 조건: 14일 경과 또는 Active CPU, Provisioned Memory, Function Invocations 한계의 100% 도달. [1차: https://vercel.com/docs/plans/pro-plan/trials]

**[규정]** 유료 Pro 전환: 결제수단 추가 필수. 결제수단 없으면 trial 종료 시 자동으로 Hobby(무료) 플랜으로 다운그레이드. [1차: https://vercel.com/docs/plans/pro-plan/trials]

**[규정]** 과금 시작: trial 종료 후 결제수단이 있으면 즉시 과금. 결제수단 없으면 과금 없음. [1차: https://vercel.com/docs/plans/pro-plan/trials]

**[규정]** Hobby 플랜: 무료, 빌링 사이클 없음. 사용량 한계 초과 시 30일 대기 필수. [1차: https://vercel.com/docs/plans/hobby]

### 4.2 Netlify — Credit-based 플랜 과금

**[규정]** Personal 또는 Pro Credit-based 플랜 유지 시 유효한 신용카드 필수. [1차: https://docs.netlify.com/manage/accounts-and-billing/billing/billing-for-credit-based-plans/billing-faq-for-credit-based-plans/]

**[규정]** Netlify는 신용카드만 수락(Enterprise 제외, ACH/wire transfer 가능). [1차: https://docs.netlify.com/manage/accounts-and-billing/billing/billing-for-credit-based-plans/billing-faq-for-credit-based-plans/]

**[규정]** 무료 tier 사용량 한계 도달 시(100%): 새 빌드 비활성화, 모든 사이트 일시중지. 복구를 위해 결제수단 추가 및 유료 플랜 업그레이드 필요. [1차: https://docs.netlify.com/manage/accounts-and-billing/billing/billing-for-credit-based-plans/billing-faq-for-credit-based-plans/]

**[규정]** Pro 플랜 업그레이드 시 과금 즉시 시작. 업그레이드는 빌링 사이클 중간이면 proration 적용. [1차: https://docs.netlify.com/manage/accounts-and-billing/billing/billing-for-credit-based-plans/billing-faq-for-credit-based-plans/]

**[규정]** Netlify는 무료 시험 기간 미제공. 무료 플랜으로 테스트 후 업그레이드. [1차: https://docs.netlify.com/manage/accounts-and-billing/billing/billing-for-credit-based-plans/billing-faq-for-credit-based-plans/]

---

## 인간 승인이 필요한 지점

**공식 요구사항에서 인간의 명시적 승인/결정이 요구되는 정확한 단계 (과금 발생 · 외부 공개 · 자격증명 취급):**

### A. 도메인 등록 단계

1. **등록자 정보 제출 및 검증** (본문 미확인 — 강등됨)
   - 인간 행동: 도메인 레지스트라에서 이름, 주소, 이메일, 전화번호 입력
   - 인간 승인: 검증 응답 (기간/절차 본문 미확인) [미확인: Q1.2]
   - 과금 발생: 도메인 등록 비용 (1회 또는 매년)

### B. 호스팅 배포 단계 (자격증명 취급)

2. **환경 변수/시크릿 설정** (Vercel/Netlify 대시보드)
   - 인간 행동: 프로덕션 환경 변수(API 키, DB 연결 문자열 등) 설정 [규정 3.1, 3.2]
   - 인간 승인: 민감한 변수(sensitive)로 표시 여부 결정 필수. 표시 시 값 재입력 불가, 빌드 중에만 복호화됨 [규정 3.1]
   - 자격증명 보안: 32자 이상이면 빌드 로그에서 [REDACTED]로 치환 [규정 3.1]

3. **프로덕션 브랜치 merge 승인** (Git/GitHub/GitLab)
   - 인간 행동: main 브랜치로 PR/MR merge [규정 3.1 함의]
   - 인간 승인: merge 승인 (code review)
   - 결과: 병합 직후 자동 프로덕션 배포 트리거 [규정 3.1]

### C. 과금 전환 단계

4. **결제수단 등록** (Vercel/Netlify 대시보드)
   - 인간 행동: 신용카드 정보 입력 및 등록 [규정 4.1, 4.2]
   - 인간 승인: 과금 시작 동의 (결제수단 등록 행위가 암묵적 동의) [규정 4.1, 4.2]
   - 과금 발생:
     - Vercel: Pro Trial 종료 후 즉시 (결제수단이 있을 때만) [규정 4.1]
     - Netlify: 무료 tier 사용량 한계(100%) 도달 시 site 일시중지 → 결제수단 추가 후 복구 [규정 4.2]

5. **유료 플랜 업그레이드 선택** (선택적)
   - Vercel Pro Trial: 종료 14일 또는 사용량 한계 도달 시 선택 필요
     - 결제수단 있음 → Pro 계속 (과금)
     - 결제수단 없음 → 자동 Hobby로 다운그레이드 (무료) [규정 4.1]
   - Netlify: 사용량 100% 도달 후 결제수단 추가 필수 (과금 즉시) [규정 4.2]

### 참고: 인간 승인 불요 항목

- **DNS 레코드 설정**: 인간 행동만 필요, 승인 불요. DNS 설정 후 자동 프로파게이션 검증 및 TLS 인증서 자동 발급 [규정 2.1, 2.2]
- **TLS 인증서 발급**: 전자동, 인간 행동/승인 불요. DNS 검증 후 자동 발급, Let's Encrypt/HTTP-01 challenge [규정 2.1]

---

## 상충·부정 증거

### 특별한 상충 사항

**[주장]** Vercel Pro Trial에서 결제수단 추가는 선택이지만, 추가하지 않으면 trial 종료 시 자동 다운그레이드. 명시적 "유료 전환 승인"이 아닌 "소극적 선택" 구조. [1차: https://vercel.com/docs/plans/pro-plan/trials]

**[주장]** Netlify는 사용량 한계(100%) 도달 시 site 일시중지 → 복구를 위해 결제수단 필수. Vercel처럼 trial 기간이 없어 무료 상태에서 과금으로의 전환 시점이 명확하지 않음. [1차: https://docs.netlify.com/manage/accounts-and-billing/billing/billing-for-credit-based-plans/billing-faq-for-credit-based-plans/]

### 명시되지 않은 부분

**[주장]** ICANN 또는 호스팅 문서에서 "도메인 등록자 신원 검증(KYC/AML)"의 구체적 절차나 정부 ID 요구 기준은 명시되지 않음. 레지스트라별로 다를 수 있음. [규정 1.1 한계]

**[주장]** Let's Encrypt HTTP-01 challenge 성공 조건(웹 서버가 /.well-known/acme-challenge/ 응답 필수)은 Vercel/Netlify 문서에 명시되지만, 호스팅 provider가 자동 처리하는 범위는 문서화 부족. [규정 2.1 한계]

---

## 미해결

### 본문 확인 실패로 삭제/강등한 claim (2026-08-04 fetch 검증 패스)

**Q1 — ICANN 정책 페이지 403 접근 불가**
- ❌ 등록 후 15일 이내 이메일/전화 검증 및 미응답 시 일시중지/취소 [스니펫만, 본문 미확보]
- ❌ 자동 갱신 유예 기간 1-45일 [스니펫만, 본문 미확보]
- ❌ Redemption Grace Period 30일 [스니펫만, 본문 미확보]
- ❌ 만료 전 1개월·1주일 알림, 만료 후 5일 내 복구 알림 [스니펫만, 본문 미확보]
- ❌ 2026년 5월 12일 등록 데이터 정책 개정 (긴급 공개 요청 응답 기한) [스니펫만, 본문 미확보]

**Q2 — Netlify SSL 재시도 스케줄**
- ⚠️ Netlify SSL 발급 재시도 "처음 24시간 10분마다, 이후 매시간" [스니펫만, 본문에 구체 기간 미명시]

**Q3 — Vercel 환경 변수 한계 및 CLI 버전**
- ⚠️ Vercel 환경별 최대 1,000개 환경 변수 한도 [스니펫만, 본문 미명시]
- ⚠️ Vercel 프리뷰 브랜치별 변수는 CLI 21.0.1 이상 필요 [본문에는 22.0.0 명시]

**확인된 claim (본문 확보)**
- ✓ Vercel SSL Let's Encrypt 사용, HTTP-01 challenge [확인]
- ✓ Vercel 민감 변수 32자 이상 [REDACTED] [확인]
- ✓ Vercel 2026년 4월 보안 사건 이후 시크릿 로테이션 권장 [확인]
- ✓ Vercel Pro Trial $20 크레딧, 14일 또는 사용량 한계 [확인]
- ✓ Netlify 결제수단 필수, 즉시 과금 [확인]

### 예산 내 미조사 항목

1. **다른 호스팅 플랫폼**(Render, Fly.io, Cloudflare Pages) — Q3/Q4의 환경 변수·과금 비교
   - 이유: Vercel/Netlify로 공통 패턴 파악 가능, 추가 fetch 여유 있지만 핵심 질문 충분히 해결
   
2. **도메인 레지스트라별 가격 및 부가 서비스**(Cloudflare Registrar vs Namecheap)
   - 제외 대상: 가격 비교는 임무 범위 외
   
3. **Cloudflare Pages의 도메인 설정 (Cloudflare Registrar와 통합 시)**
   - 이유: Vercel/Netlify 사용자 기준으로 충분, 검색 예산 남음

### 예산 내 해결되지 않은 명시적 질문

- **레지스트라 선택 시 강제 요구사항**: ICANN 정책은 모든 공인 레지스트라에 동일하지만, 각 레지스트라의 추가 검증(세금 ID, 회사 등록증 등)은 미조사. [예산 부족 아님, 범위 판단: 1차 공식 문서에 개인/소상공인 기준 미명시]

---

## 출처

### 1차 출처 (공식 문서)

**ICANN & 도메인 정책**
- https://www.icann.org/registrants — ICANN 등록자 정보 홈
- https://www.icann.org/resources/pages/contact-verification-2013-05-03-en — 연락처 검증 정책
- https://www.icann.org/en/contracted-parties/consensus-policies/registration-data-policy — 등록 데이터 정책 (2026-05-12 개정)
- https://www.icann.org/resources/pages/whois-data-accuracy-2017-06-20-en — WHOIS 데이터 정확성
- https://www.icann.org/resources/pages/domain-name-renewal-expiration-faqs-2018-12-07-en — 갱신/만료 FAQ
- https://www.icann.org/en/contracted-parties/consensus-policies/expired-registration-recovery-policy/expired-registration-recovery-policy-21-02-2024-en — 만료 등록 복구 정책 (ERRP, 2024-02-21)

**Vercel — 도메인·배포·과금**
- https://vercel.com/docs/domains/managing-dns-records — DNS 레코드 관리
- https://vercel.com/docs/domains/working-with-ssl — SSL 인증서
- https://vercel.com/docs/deployments/environments — 배포 환경
- https://vercel.com/docs/environment-variables — 환경 변수
- https://vercel.com/docs/environment-variables/sensitive-environment-variables — 민감 환경 변수
- https://vercel.com/docs/plans/hobby — Hobby 플랜
- https://vercel.com/docs/plans/pro-plan/trials — Pro Trial (2026-06-16 업데이트)
- https://vercel.com/kb/guide/how-to-add-vercel-environment-variables — 환경 변수 설정 (보안 사건 언급)

**Netlify — 도메인·배포·과금**
- https://docs.netlify.com/manage/domains/secure-domains-with-https/https-ssl/ — HTTPS/SSL
- https://docs.netlify.com/manage/domains/get-started-with-domains/ — 커스텀 도메인 시작
- https://docs.netlify.com/build/environment-variables/overview/ — 환경 변수 개요
- https://docs.netlify.com/deploy/manage-deploys/manage-deploys-overview/ — 배포 관리·롤백
- https://docs.netlify.com/manage/accounts-and-billing/billing/billing-for-credit-based-plans/billing-faq-for-credit-based-plans/ — Credit-based 과금 FAQ

### 2차 출처

없음 (모두 1차 공식 문서)

---

## 메타데이터

- **생성자:** Haiku 4.5 web-research agent
- **정책 준수:** EVIDENCE-POLICY (facts-only, 검색/fetch 예산 준수, 라벨링, 신선도 표시)
- **예산 사용 상황:** 검색 7/24 (29%), Fetch 5/32 (16%)
- **최종 사실 수:**
  - 규정/정의 (본문 확인): 15개
  - 미확인 (스니펫만): 8개
  - 합계: 23개 (초기 30개에서 수정)
- **1차/2차 비율:** 100% 1차 / 0% 2차
- **수정 현황:**
  - 삭제된 claim: 5개 (Q1 ICANN 접근 불가)
  - 강등된 claim: 4개 (Q2 Netlify, Q3 Vercel 환경 변수)
  - 본문 확인됨: 14개 (Vercel SSL, 민감 변수, 보안 사건, Pro Trial, Netlify 과금)
- **인간 승인 지점:** 5개 (도메인 등록자 정보, 환경 변수 민감도 표시, 프로덕션 merge 승인, 결제수단 등록, 유료 플랜 선택)
- **미해결 항목:** 2개 + 본문 미확인 9개 (ICANN 접근 불가로 인한 강등)
