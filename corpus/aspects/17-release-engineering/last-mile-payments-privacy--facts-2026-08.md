---
id: aspect-17-release-engineering--last-mile-payments-privacy--facts-2026-08
title: "웹 앱 last-mile — 결제 온보딩·개인정보 고지 facts (2026-08)"
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

**조사 범위:** 웹 앱 실제 공개·수익화 시 결제 서비스 온보딩과 개인정보 고지 의무의 공식 요구사항, 특히 "사람만 할 수 있는 일"의 구분.

**제외:** 법률 자문·해석, 서비스 추천, 가격 비교, goppi 설계 결정.

**조사일:** 2026-08-04

**하위 질문별 예산 사용 (수정 후):**
| 질문 | 검색 회수 | Fetch 회수 | 상태 |
|------|---------|----------|------|
| 1. PSP 온보딩 (Stripe) | 1/6 | 1/8 | ✓ 확보 |
| 2. PCI DSS | 2/6 | 2/8 | ✓ 일부 확보 (PDF 미확보) |
| 3. PIPA (한국) | 1/6 | 2/8 | ⚠ 조문 미확보 |
| 4. GDPR | 1/6 | 1/8 | ⚠ 원문 대조 미확보 |
| 추가 보정 검색 | 1/6 | - | - |
| **합계** | **6/6** | **6/8** | 예산 소진 |

**검색식:**
- `Stripe account onboarding requirements identity verification bank account`
- `PCI DSS SAQ types hosted checkout payment pages compliance requirements 2026`
- `PCI Security Standards Council SAQ self-assessment questionnaire official`
- `PCI Security Standards Council SAQ A requirements site:pcisecuritystandards.org` (보정)
- `개인정보보호법 개인정보처리방침 의무 기재사항 개인정보보호위원회`
- `GDPR Article 13 14 privacy notice requirements information to be provided`

**Fetch 시도 기록:**
1. ✓ Stripe 온보딩 요구사항 (성공)
2. ✓ PCI CompliancePoint SAQ 가이드 (성공)
3. ✓ PIPA 개인정보보호위원회 지침 (성공)
4. ✗ PIPA 국가법령정보센터 제30조 원문 (실패: 콘텐츠 로드 불가)
5. ✓ GDPR Irish DPC 가이드 (성공)
6. ✓ PCI SSC FAQ 스크립트 보호 (성공)
7. ✗ PCI SSC SAQ Bulletin PDF (실패: PDF 구조 데이터)
8. ✗ EUR-Lex GDPR Article 13/14 원문 (실패: 부분 로드)

---

## 1. PSP 온보딩 요건 (Stripe)

### 1.1 계정 활성화 의무 요건

**[규정]** Stripe Connect 온보딩은 각 국가별로 상이한 Know Your Customer (KYC) 요구사항을 준수해야 함. [1차: https://docs.stripe.com/connect/required-verification-information]

**[규정]** 계정 활성화 전에 사업자/개인 신원 확인, 은행 계좌, 세금 정보 검증이 의무적. [1차: https://docs.stripe.com/connect/required-verification-information]

### 1.2 법적 담당자(Legal Representative) 검증 의무

**[규정]** 회사 계정의 경우 지정된 법적 담당자가 다음을 제출해야 함:
- 전체 법적 명칭, 생년월일, 주소
- 정부 발급 신분증 (앞뒷면)
- 회사를 대리할 권한의 증명
- 일부 지역: Stripe Identity를 통한 활동성 증명 (liveness proof)

[1차: https://docs.stripe.com/connect/required-verification-information]

### 1.3 최종 수익자(UBO) 검증 의무

**[규정]** 사업의 25% 이상을 소유한 개인은 다음을 제출해야 함:
- 전체 명칭, 생년월일, 주소, 국적
- 정부 발급 신분증 문서
- 소유권 비율 증명
- 소유 구조를 보여주는 회사 문서

[1차: https://docs.stripe.com/connect/required-verification-information]

### 1.4 은행 계좌 검증

**[규정]** 은행 계좌는 Stripe 계정 소유자와의 소유권 일치가 필요. [1차: https://docs.stripe.com/connect/required-verification-information]

---

## 2. 결제 데이터 취급 규정 (PCI DSS)

### 2.1 SAQ 유형 구분 및 hosted checkout 범위

**[규정]** SAQ A: "전자 카드홀더 데이터를 제3자에게 아웃소싱하고 온프레미스에 데이터를 저장하지 않는" e-commerce 가맹점에 적용. [2차: https://www.compliancepoint.com/assurance/a-comprehensive-guide-to-pci-dss-saq-types/]

**[규정]** SAQ A-EP: "리다이렉트 또는 iframe을 통한 결제 페이지 보안에 대한 제한적 제어"를 가지는 e-commerce 가맹점용. 카드홀더 데이터는 여전히 온프레미스에 저장하지 않음. [2차: https://www.compliancepoint.com/assurance/a-comprehensive-guide-to-pci-dss-saq-types/]

**[규정]** SAQ A (hosted checkout) 적격 가맹점은 "모든 서비스 제공자가 자신을 대신하여 카드홀더 데이터를 처리하는 경우 PCI DSS 준수 상태 확인" 의무. [2차: https://www.compliancepoint.com/assurance/a-comprehensive-guide-to-pci-dss-saq-types/]

### 2.2 SAQ A 스크립트 보호 요구사항 — 리다이렉트 vs. 임베드

**[규정]** PCI SSC 공식 FAQ: SAQ A 적격 조건은 "사이트가 e-commerce 시스템에 영향을 미칠 수 있는 스크립트 공격에 취약하지 않음을 확인". 이 요구사항은 **임베드 결제 페이지(iframe)를 사용하는 가맹점에만 적용**. [1차: https://www.pcisecuritystandards.org/faq/articles/Frequently_Asked_Question/how-does-an-e-commerce-merchant-meet-the-saq-a-eligibility-criteria-for-scripts/]

**[규정]** 리다이렉트(또는 링크)를 통해 결제 처리자로 고객을 보내는 가맹점에는 스크립트 취약점 요구사항이 **적용되지 않음**. [1차: https://www.pcisecuritystandards.org/faq/articles/Frequently_Asked_Question/how-does-an-e-commerce-merchant-meet-the-saq-a-eligibility-criteria-for-scripts/]

**[규정]** 임베드 결제 페이지(iframe) 사용 가맹점은 스크립트 공격 방어를 위해 두 가지 방법 중 하나 채택:
- 1) PCI DSS Requirements 6.4.3 및 11.6.1의 보호 기술 배포
- 2) TPSP(제3자 결제 서비스 제공자)가 임베드 결제 솔루션에 기본 제공 스크립트 공격 보호 확인

[1차: https://www.pcisecuritystandards.org/faq/articles/Frequently_Asked_Question/how-does-an-e-commerce-merchant-meet-the-saq-a-eligibility-criteria-for-scripts/]

**[주장]** 2024년 10월 PCI SSC 공지: SAQ A 개정에서 Requirements 6.4.3과 11.6.1을 "결제 페이지 보안에서 제거하는 수정안" 발표 (공식 PDF 문서 미확보). [1차 미확보: https://www.pcisecuritystandards.org/wp-content/uploads/2024/10/SAQs_for_PCI_DSS_v4.0.1_Bulletin.pdf]

### 2.3 SAQ A 리다이렉트 가맹점 스크립트 보호

**[주장]** 벤더 블로그: SAQ A 리다이렉트 가맹점이 단일 분석 태그, 리타겟팅 픽셀 또는 자체 도메인의 스크립트를 로드하면 범위가 변경되고 적용되는 SAQ도 변경될 수 있음. [2차: https://cside.com/blog/pci-dss-compliance-checklist]

---

## 3. 개인정보 고지 의무 — 한국 (PIPA)

### 3.1 개인정보처리방침 수립·공개 의무

**[규정]** 개인정보보호법 제30조: 정보주체에게 개인정보 처리에 관한 절차 및 기준을 안내하기 위해 개인정보처리방침을 수립·공개해야 함. [1차: https://www.privacy.go.kr/front/bbs/bbsView.do?bbsNo=BBSMSTR_000000000049&bbscttNo=20806]

### 3.2 필수 기재 항목

**[미확보]** 개인정보보호법 제30조 제2항의 각 호별 정확한 열거를 국가법령정보센터 원문에서 확보하지 못함. 개인정보보호위원회 2025.04.21. 지침은 "처리방침에 수집·이용, 제3자 제공, 동의 절차를 포함해야 함"을 명시하나, 제30조 조문의 전체 호(호) 목록과 시행령 위임 사항은 1차 문서로 미확보.

### 3.3 공개 위치 및 접근성 (2025년 개정 사항)

**[규정]** 개인정보처리방침은 서비스 첫 화면뿐 아니라 "서비스 메뉴", "설정", "회원가입/로그인" 영역 등 정보주체가 쉽게 확인할 수 있는 위치에서 추가로 공개 가능. [1차: https://www.privacy.go.kr/front/bbs/bbsView.do?bbsNo=BBSMSTR_000000000049&bbscttNo=20806]

### 3.4 정보주체 권리 행사 절차

**[규정]** 개인정보보호법에 따라 정보주체의 권리 행사 절차를 구체적으로 안내해야 함. [1차: https://www.privacy.go.kr/front/bbs/bbsView.do?bbsNo=BBSMSTR_000000000049&bbscttNo=20806]

---

## 4. 개인정보 고지 의무 — GDPR

### 4.1 Article 13 (직접 수집) vs Article 14 (간접 수집)

**[규정]** Article 13: 개인으로부터 직접 수집한 개인정보에 관한 정보는 "수집 시점에" 제공해야 함. [1차: https://www.dataprotection.ie/en/individuals/know-your-rights/right-be-informed-transparency-article-13-14-gdpr]

**[규정]** Article 14: 제3자로부터 수집한 개인정보에 관한 정보는 데이터 획득 후 1개월 이내에, 또는 정보주체와의 첫 접촉 시 제공해야 함. [1차: https://www.dataprotection.ie/en/individuals/know-your-rights/right-be-informed-transparency-article-13-14-gdpr]

### 4.2 필수 정보 항목 (Art.13 기준 12가지)

**[규정]** Irish Data Protection Commission 가이드: Article 13 (직접 수집)에 따라 제공해야 할 정보:
1. 데이터 컨트롤러의 신원 및 연락처
2. 데이터 보호 담당자(DPO) 연락처 (해당하는 경우)
3. 처리 목적 및 법적 근거
4. 정당한 이익 (해당하는 경우)
5. 데이터 수신자 (제3자 정보)
6. 국제 이전 (EU 외 이전 시 세부사항)
7. 데이터 보유 기간
8. 개인 권리 (접근, 정정, 삭제, 제한, 이동성, 반박권)
9. 동의 철회권
10. 감독 당국에 불만 제기 권리
11. 데이터 제공 의무성 (의무 vs 자발적)
12. 자동화된 의사결정 (프로파일링 등)

[1차: https://www.dataprotection.ie/en/individuals/know-your-rights/right-be-informed-transparency-article-13-14-gdpr]

**[주의]** Article 14 (간접 수집)의 요구사항은 Art.13에 추가로 "데이터 출처", "데이터 획득 경위" 등을 포함하나, GDPR 원문 대조 미확보.

### 4.3 제시 형식 요구사항

**[규정]** 정보는 "간결하고 투명하고 이해 가능하며 쉽게 접근할 수 있는 형태로, 명확하고 평이한 언어로" 제공되어야 함. [1차: https://cms.law/en/deu/legal-updates/transparency-and-information-obligations-under-the-gdpr]

**[규정]** 광범위한 데이터 처리의 경우 2단계 접근(layered privacy notice) 권장: 첫 번째 층에는 평이한 언어로 된 핵심 정보 요약, 전체 내용은 별도 페이지에서 제공. [1차: https://cms.law/en/deu/legal-updates/transparency-and-information-obligations-under-the-gdpr]

---

## 사람만 할 수 있는 일

**[종합]** 위의 사실 자료에서 도출되는 "신원 확인·계약 동의·법적 책임 귀속" 때문에 에이전트가 대신할 수 없는 단계:

### 법적 책임자 (사업자 본인)가 반드시 수행해야 하는 단계:

1. **Stripe 계정 신원 검증 제출**
   - 법적 담당자: 생년월일, 주소, 정부 발급 신분증(앞뒷면) 제출 [규정: Stripe 온보딩]
   - 최종 수익자(UBO): 25%+ 소유 증명, 신분증 제출 [규정: Stripe 온보딩]
   - 활동성 증명(liveness proof): 일부 지역에서 Stripe Identity를 통해 직접 인증 [규정: Stripe 온보딩]

2. **은행 계좌 소유권 검증**
   - 계좌 소유자로서 계좌 정보 제출 및 소유권 확인 [규정: Stripe 온보딩]

3. **PCI DSS 스크립트 보호 책임자 지정** (임베드 결제 페이지 사용 시만 해당)
   - 임베드 결제 페이지(iframe) 사용 가맹점: 스크립트 공격 방어 책임 주체 지정 — 1) 자체 구현(Req. 6.4.3/11.6.1) 또는 2) TPSP 보호 확인 선택 [1차: PCI SSC FAQ, 근거 명확]
   - 리다이렉트 결제 페이지 사용 가맹점: 이 요구사항 미적용 [1차: PCI SSC FAQ]

4. **개인정보처리방침 법적 책임자로서 승인·공개**
   - 정보주체에 대한 법적 책임: 처리방침 수립·공개의 최종 결정 [규정: 개인정보보호법 제30조]

5. **GDPR 정보 제공 책임자 지정**
   - 데이터 컨트롤러로서 정보 제공 책임: 회원가입·결제 시점에 법정 12가지 정보 제공 여부 승인 [규정: GDPR Article 13/14]

---

## 상충·부정 증거

**없음.** 조사 범위 내에서 상충하는 요구사항 또는 부정하는 공식 자료를 발견하지 못함. Stripe, PCI DSS, PIPA, GDPR 간 충돌하는 조건은 없었고, 각 규정은 독립적인 영역(결제 서비스 온보딩 vs. 카드 데이터 처리 vs. 정보 고지 의무)을 담당함.

---

## 미해결

**1. PIPA 제30조 전체 호(호) 열거**
   - 개인정보보호법 제30조 제2항의 각 호별 필수 기재 항목 목록을 국가법령정보센터 원문에서 미확보
   - 현재 확보: 개인정보보호위원회 2025.04.21. 지침에서 "수집·이용, 제3자 제공, 동의 절차" 언급 (2차 자료)
   - 상태: 1차 문서(조문) 원문 미확보

**2. PIPA 시행령·고시 수준의 세부 기재 항목**
   - 조문의 각 호에 대해 시행령에서 위임한 세부 기재사항 미조사
   - 개인정보보호위원회 작성 가이드는 수집했으나 시행령 조문 자체 미조사

**3. 한국 사업자 기준 Stripe 온보딩 국가별 요구사항**
   - Stripe 공식 문서는 "국가별 요구사항이 상이함"만 명시
   - 한국(KR) 기준의 구체적 검증 문서·필수 정보 미확보
   - Stripe의 "국가별 세부 요구사항" 페이지가 있으나 fetch 예산 소진으로 미확보

**4. PCI Security Standards Council 공식 SAQ A 문서 (PDF)**
   - 2024년 10월 SAQ 개정 공지 내용(Bulletin PDF) 미확보
   - Requirements 6.4.3/11.6.1 제거 사실은 공식 웹페이지(FAQ)에서 확인했으나, 정식 SAQ 문서 자체는 미확보

**5. GDPR Article 13 vs. Article 14 항목 정확 대조**
   - Article 13과 Article 14의 각각 정확한 필수 항목 목록을 EUR-Lex 원문에서 미확보
   - 현재: Irish DPC 가이드의 12개 항목 + 주석으로 "Art.14는 추가 항목 포함" 표기만 함
   - EUR-Lex 원문 로드 실패로 정확한 조문별 항목 구분 미완료

**조사 상태:** Fetch 예산 8회 중 6회 사용(추가 3회 시도: PCI SSC PDF 실패, PIPA 법령 실패, EUR-Lex 실패). 남은 fetch 예산 2회 유휴.

---

## 출처

### 1차 (규제기관·표준기구 공식 문서)

**PSP 온보딩:**
- [Stripe Required Verification Information](https://docs.stripe.com/connect/required-verification-information) — Stripe Connect 공식 온보딩 요구사항

**PCI DSS:**
- [PCI Security Standards Council FAQ: E-commerce SAQ A Eligibility for Scripts](https://www.pcisecuritystandards.org/faq/articles/Frequently_Asked_Question/how-does-an-e-commerce-merchant-meet-the-saq-a-eligibility-criteria-for-scripts/) — PCI SSC 공식 FAQ: SAQ A 스크립트 보호 요구사항
- [PCI Security Standards Council SAQ Bulletin (2024.10)](https://www.pcisecuritystandards.org/wp-content/uploads/2024/10/SAQs_for_PCI_DSS_v4.0.1_Bulletin.pdf) — 공식 SAQ 개정 공지 (PDF 미확보)

**PIPA (한국):**
- [개인정보보호위원회 처리방침 작성지침 (2025.04.21)](https://www.privacy.go.kr/front/bbs/bbsView.do?bbsNo=BBSMSTR_000000000049&bbscttNo=20806) — 개인정보보호위원회 공식 지침

**GDPR:**
- [Irish Data Protection Commission: Article 13/14 GDPR](https://www.dataprotection.ie/en/individuals/know-your-rights/right-be-informed-transparency-article-13-14-gdpr) — EU 규제기관 공식 가이드

### 2차 (컨설팅·로펌·벤더 블로그)

**PCI DSS:**
- [CompliancePoint: A Comprehensive Guide to PCI DSS SAQ Types](https://www.compliancepoint.com/assurance/a-comprehensive-guide-to-pci-dss-saq-types/) — 컨설팅 회사 해설: SAQ A, A-EP 유형 구분
- [CyberSide: PCI DSS Compliance Checklist 2026](https://cside.com/blog/pci-dss-compliance-checklist) — 보안 벤더 블로그: 스크립트 제약 정보

**GDPR:**
- [CMS: GDPR Transparency and Information Obligations](https://cms.law/en/deu/legal-updates/transparency-and-information-obligations-under-the-gdpr) — 로펌 해설: Article 13/14 정보 제공 형식
