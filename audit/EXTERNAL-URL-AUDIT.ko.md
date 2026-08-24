# 외부 URL 전수 감사 — 2026-08-02

## 판정

Active corpus의 **Markdown evidence/navigation surface + canonical `_meta/sources.jsonl`**에서 추출한
고유 HTTP(S) URL을 같은 실행에서 검사한다. 코드·raw census fixture·log·publication index에만 있는
URL-shaped data는 이 링크 무결성 gate의 대상이 아니다.

| 결과 | 수 | 의미 |
|---|---:|---|
| `reachable` | 495 | 요청 URL이 2xx/3xx 응답 |
| `redirected` | 68 | redirect를 따라 최종 URL이 2xx/3xx 응답 |
| `access-blocked` | 34 | 서버가 401/403/405/406/407/409/418/423/425/429/451로 자동 검사 접근을 제한 |
| `dead` | 0 | 404/410 없음 |
| `http-error` | 0 | 재시도 뒤 미분류 HTTP 오류 없음 |
| `network-error` | 0 | 재시도와 system-curl fallback 뒤 네트워크 오류 없음 |

이 검사는 **endpoint reachability 검사**다. `reachable`, `redirected`, `access-blocked` 어느 것도 해당
페이지가 corpus의 claim을 실제로 지지하거나 내용이 변하지 않았다는 뜻이 아니다. 모든 ledger record의
`content_verified`는 의도적으로 `false`다. `access-blocked`는 dead로 세지 않았고 content-verified로도
세지 않았다.

## 재현 표면

- 실행기: `tools/external_url_audit.py`
- URL별 원장: `external-url-status.jsonl`
- URL-set SHA-256·시각·집계: `external-url-status-meta.json`
- offline gate: `tools/validate_corpus.py`가 현재 corpus URL 집합과 ledger의 exact set, digest, count,
  result vocabulary, 집계, 30일 freshness를 대조한다.

실행 명령:

```sh
python3 .scratch/research/tools/external_url_audit.py --workers 20 --timeout 15 --retries 1
python3 .scratch/research/tools/validate_corpus.py
```

## 수정한 결함

- 불완전 scheme·ellipsis·가상 plugin 주소 5건을 비링크 표기 또는 명시적 example URL로 교정했다.
- 404/이전 경로·불안정 mirror 13종을 Vale, Fowler, Google Research, Scrum Guide, Scaled Agile,
  CISA, NTIA, Atlassian, DOI 등 현재 공식/원 발행 경로로 교체하거나 근거 범위를 낮췄다.
- 독립 review에서 발견한 source-registry-only URL 2개(NIST AI RMF, Anthropic Contextual Retrieval)를
  exact-set 추출에 추가하고 회귀 테스트를 고정했다.
- 후속 review에서 발견한 balanced-parenthesis DOI 절단, nonzero curl redirect false-green, 미래 timestamp·
  빈 detail 허용, file-wide ISO disposition false-green을 각각 재현하고 검사기와 회귀 테스트를 보강했다.
- ISO/IEC/IEEE 12207:2017 상세를 ISO/IEC/IEEE 12207:2026으로 자동 치환하지 않았다. 현행 공개 catalog가
  지지하는 범위만 남기고, 구판 상세는 역사적·review-needed 또는 INCONCLUSIVE로 표시했다.

### ISO 12207 경고 8개 파일의 정확한 처분

| 파일 | 이전 문제 | 처분 |
|---|---|---|
| `corpus/PROVENANCE.md` | 승계 당시 generic/2017 anchor와 “2026 edition”만 병기 | 2017 withdrawn·2026 current를 공식 catalog URL과 함께 명시; 역사 기록으로 보존 |
| `corpus/facts-2026-08-matrix.md` | generic ISO 12207이 방법론 중립·프로세스 분류를 함께 뒷받침하는 것처럼 보임 | 2026 공개 초록이 지지하는 방법론 중립 범위만 남기고 상세 분류 재귀속 금지 |
| `corpus/aspects/24-governance-collaboration-compliance/24-governance-collaboration-compliance--overview.md` | 2017 catalog와 상세 process 명칭을 current governance anchor로 사용 | current 2026 catalog로 교체; 상세 process/clause 대응은 `INCONCLUSIVE` |
| `corpus/aspects/02-architecture-design/02-architecture-design--overview.md` | 판본 없는 metadata anchor | `ISO-12207-2026-catalog-scope`로 범위 고정 |
| `corpus/aspects/14-data-management-migrations/14-data-management-migrations--overview.md` | Wikipedia/구판 process detail이 DB migration claim을 보조 | ISO/Wikipedia source와 anchor 제거; 구판 attribution 제거 이유를 명시하고 DB 공식 문서만 유지 |
| `corpus/aspects/28-implementation-process-workflow/28-implementation-process-workflow--overview.md` | ISO가 risk-tier classifier를 직접 지지하는 것처럼 표현 | risk-tier 근거에서 ISO 제거; 2026 공개 범위와 clause-level `INCONCLUSIVE`를 별도 기록 |
| `corpus/aspects/28-implementation-process-workflow/facts-2026-08-sdlc-models.md` | 2017 상세·2차 자료와 2026 현행판을 혼합 | 2026 공개 범위와 역사적 2017 상세를 분리; PacificCert 제거·ISO 공식 catalog 추가 |
| `corpus/aspects/28-implementation-process-workflow/research-log.md` | 2017 tailoring 상세를 현행 근거처럼 사용 | 2017을 withdrawn/historical로 표시; 2026 clause mapping을 `INCONCLUSIVE`로 제한 |

### 첫 실행에서 미해결된 18개 URL-shaped target의 정확한 처분

| 이전 target | 처분 / 현재 target |
|---|---|
| 불완전 `https://` scheme 2종 | 링크가 아닌 `HTTPS` scheme 설명으로 교정 |
| `https://docs.example.com/plugin` | 명시적 예약 예시 `https://example.com/` |
| `https://github.com/author/plugin` | 실제 공개 예시 repo `https://github.com/git/git` |
| ellipsis git URL | 실제 공개 git URL `https://github.com/git/git.git` |
| `https://blog.brq.com/en/what-is-a-release-train/` | SAFe 공식 ART glossary URL로 교체 |
| `https://djaa.com/the-principles-and-general-practices-of-the-kanban-method/` | DJAA의 현재 `revisiting-...` URL로 교체 |
| `https://docs.vale.sh/keys/vocab` | Vale 현재 `https://vale.sh/docs/keys/vocab` |
| `https://martinfowler.com/articles/contract-test.html` | Fowler 현재 `https://martinfowler.com/bliki/ContractTest.html` |
| UTD의 CHAOS report PDF mirror | 원 발행 URL 부재를 밝히고 OpenCommons archive file page로 교체 |
| Google mutation-testing 이전 slug | Google Research의 현재 `practical-mutation-testing-at-scale-a-view-from-google` URL |
| `understandlegacycode.com/blog/characterization-tests/` | 동일 저자의 현재 `characterization-tests-or-approval-tests` URL |
| Michigan의 TLS-failing requirements PDF mirror | 원 출판물 DOI `10.1007/3-540-28244-0_2`로 교체 |
| Aha의 삭제된 3-role 비교 글 | 현재 Aha product-manager guide + Scrum Guide의 Product Owner 정의로 범위 분리 |
| Atlassian의 삭제된 ITIL incident URL | 현재 incident-vs-problem-management URL |
| CISA SBOM PDF의 잘못된 `...Transparency 24.pdf` | 공식 `...Transparency 2024.pdf` |
| Leapwork의 삭제된 test-pyramid slug | 현재 `what-is-test-automation` URL |
| NTIA의 이전 report route | 공식 `sbom_minimum_elements_report.pdf` |

## 남는 한계

- 34개 access-blocked URL의 본문은 이 자동 검사에서 읽지 못했다. 중요한 verified claim은 별도의
  claim-level source 검증을 따라야 한다.
- 링크는 시간이 지나면 다시 깨질 수 있으므로 meta의 `completed_at`이 30일을 넘으면 validator가 다시
  warning을 낸다.
- 변경 전 snapshot의 971개 URL은 불변 역사 자료이며 이 active-corpus 전수 검사의 대상이 아니다.
