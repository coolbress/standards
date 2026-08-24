# goppi_final 리서치 코퍼스 감사 — 2026-08-02

## 결론

기존 자료는 버릴 토대가 아니라 **좋은 원석과 과도한 확신이 섞인 토대**였다. 28-aspect 구조는 탐색
인덱스로 유지할 가치가 있지만, 다음 세 문장은 감사 전 상태로는 성립하지 않았다.

1. “객관 근거는 corpus에만 있다” — 프로젝트 결정과 `Implications for gingoa`가 섞여 있었다.
2. “28개 aspect 전부 verified” — claim 단위 출처·범위·시효 검증 없이 문서 단위로 과대 표기됐다.
3. “taxonomy locked” — 분류 자체의 재현 가능한 crosswalk가 없고 핵심 ISO 앵커가 이미 교체됐다.

따라서 기존 연구를 폐기하지 않고, **사실/출처 → 합성 → 프로젝트 결정**의 경계를 다시 세웠다.

## 변경 전 관측치

| 항목 | 관측 |
|---|---:|
| 활성 corpus 파일 | 203 |
| Markdown 파일 | 95 |
| aspect 디렉터리 | 28 |
| 크기 | 약 23MB |
| Markdown의 고유 외부 URL | 971 |
| `status: verified` 문서 | 51 |
| gingoa 적용 표기/섹션 포함 문서 | 39 |
| `[inferred]` 포함 문서 | 10 |
| 명시적 `[2차]`/`[2차?]` 포함 문서 | 12 |
| frontmatter 없는 Markdown | 31 (대부분 root navigation/raw census; 구 스키마가 예외를 정의하지 않음) |
| 동일 SHA-256 그룹 | 1개 — 0바이트 `.err` 14개뿐 |
| 실행 부산물 | `.pyc` 7개와 빈 `__pycache__` 4개 |

전체 변경 전 목록과 SHA-256은 [`before-manifest.tsv`](before-manifest.tsv)에 있다.

## 변경 후 검증 상태

| 항목 | 관측 |
|---|---:|
| 활성 corpus 파일 | 190 |
| Markdown 파일 | 102 |
| aspect 디렉터리 | 28 |
| 비어 있지 않은 exact duplicate 그룹 | 0 |
| 깨진 내부 링크 | 0 |
| source registry 레코드 | 38 |
| 새 정책으로 `verified`인 aspect 문서 | 3 |
| `review-needed` aspect 문서 | 50 |
| 현재 corpus Markdown + source registry의 고유 외부 URL | 597 |

`external_url_audit.py`로 active corpus Markdown + source registry의 597개 URL을 전수 실행한 결과는
reachable 495, redirected 68, access-blocked 34, dead/http-error/network-error 0이다. Access-blocked는 서버 응답은 있었지만 본문을 읽지
못한 상태이며 content 검증으로 세지 않는다. URL별 결과·URL-set digest·30일 freshness gate는
[`EXTERNAL-URL-AUDIT.ko.md`](EXTERNAL-URL-AUDIT.ko.md)에 기록했다. 변경 후 파일별 hash는
[`after-manifest.tsv`](after-manifest.tsv)에 있다.

### Trustworthy-completion 후속 보강

사용자 목적을 다시 확인한 뒤 기존 output/failure 중심 worth 가설을 target-user의 **정확성·claim-linked
evidence·이해 가능한 판단·정직한 상태·복구 가능성**을 함께 요구하는 trustworthy-completion 가설로
개정했다. NIST assurance/SSDF/GenAI profile과 appropriate-reliance 및 novice/non-programmer 원 연구 4개를
claim-level로 연결했고, 직접 근거가 약한 preprint는 낮은 confidence와 transfer 제한을 유지했다.

Critical 50%·Major 30%와 고정 비용 한도는 target baseline에서 나온 값이 아니므로 최종 threshold에서
내렸다. 형성 연구→grader dry-run→분리 pilot→threshold/분석 동결→confirmatory→필수 attribution→field
follow-up protocol로 교체했다. process step은 문서/절차 존재가 아니라 evidence·material issue·decision·
recovery에 기여할 때만 점수를 얻는다. 이 연구는 goppi의 효과를 입증하지 않았으며 제품 상태는 계속
`INCONCLUSIVE/NO-GO`다.

### AI retrieval 검증

[`retrieval-cases.jsonl`](retrieval-cases.jsonl)에 topic 28개와 lifecycle/evidence/status/freshness를 포함한
30개 질문을 사전등록했다. `evaluate_retrieval_contract.py` 결과는 30/30 PASS, 모든 목표가 INDEX에서 1-hop,
INDEX+선택 문서의 최대 read surface는 전체 Markdown의 3.13%였다. 별도 fresh-context 모델은 정답을 보지 않은
채 층화 표본 10문항을 10/10 올바른 경로로 찾고, `review-needed`/`verified`, freshness, claim/source ID를
구분했으며 전체 corpus를 로드하지 않았다. 이것은 현재 구조의 작은 행동 baseline이지, 모델·질문·언어가
바뀌어도 같은 성능을 보장하거나 변경 전 구조보다 우월함을 증명하는 결과는 아니다.

추가 before/after 비교는 동일 30문항을 snapshot과 현재 구조에 적용했다. 양쪽 routing은 30/30으로
같았지만 status calibration은 1/29→29/29, 근거표 없는 verified target은 29→0, answer anchor는
28/33→33/33으로 개선됐다. 5회 order 반복 편차는 0이었다. 이것은 구조/metadata 검사이며 반복 모델
성능은 아니다. 별도로 같은 10문항을 native fresh context 3회/arm에 실행해 correctness
5·5·9→10·10·10, unsupported claim 5·5·1→0·0·0, 평균 read bytes 56.1% 감소를 관측했다. 이 model
pilot은 내용+상태+구조의 합산 효용이며 다른 모델/언어 일반화와 actual tokens는 입증하지 않는다. 상세는
[`RETRIEVAL-BEFORE-AFTER.ko.md`](RETRIEVAL-BEFORE-AFTER.ko.md)에 있다.

## 판정과 처리

| 발견 | 객관적 판정 | 처리 |
|---|---|---|
| 0바이트 `.err` 14개 | 정보가 없고 모두 같은 empty-file hash | active corpus에서 제거; 별도 archive 사본도 사용자 승인 후 삭제, snapshot에서만 복구 가능 |
| `.pyc` 7개 / 빈 cache dir 4개 | 원본 Python에서 재생성되는 실행 부산물, 근거 아님 | 파일·빈 dir 제거; 별도 archive 사본도 사용자 승인 후 삭제, snapshot에서만 복구 가능 |
| 비어 있지 않은 exact duplicate | 발견되지 않음 | 없음 |
| 동일한 300자 이상 H2 본문 | 변경 후 normalized-section 검사에서 0그룹 | 기계 검사를 validator에 고정 |
| `three-tier-ledger.md` | goppi/gingoa 제품 결정 ledger이지 일반 근거가 아님 | `interpretation/legacy/`로 이동 |
| 구 `GUIDE.ko.md` | gingoa 운영모델·완료 주장이 섞인 사용자 안내 | 원본을 legacy로 이동하고 중립 안내로 교체 |
| 구 `lifecycle.md` | 일반 life cycle과 gingoa activation 결정이 혼합 | legacy로 이동하고 navigation crosswalk로 교체 |
| 구 `_schema.md` | evidence/application 혼합을 허용하고 verified 의미가 약함 | legacy로 이동하고 claim 중심 schema로 교체 |
| 구 `TAXONOMY.md` | 유용하지만 “LOCKED/definitive” 주장과 2017 ISO 앵커가 부정확 | legacy로 이동하고 provisional taxonomy로 교체 |
| `Implications for gingoa` 등 33개 H2 | 일반 근거가 아니라 과거 제품 적용 판단 | verbatim으로 `interpretation/legacy/gingoa-specific-sections.md`에 추출 |
| `gingoa_applied` frontmatter | corpus와 과거 제품 적용을 결합 | active corpus에서 제거, extraction 기록에 보존 |
| inherited `verified` 50개 | 현재 claim-level 정책을 통과한 기록이 없음 | `review-needed`로 하향 |

구조적·의미적 중복은 hash 하나로 완전히 판정할 수 없다. 사람 검토에서는 `GUIDE`·`INDEX`·`TAXONOMY`·
`lifecycle`·`three-tier-ledger`가 navigation, evidence rule, gingoa decision을 반복·혼합하는 지점을 비교했고,
각 역할을 navigation/schema/interpretation으로 분리했다. 기계 검사는 동일 파일 hash와 동일한 substantial H2
본문을 막으며, paraphrase 수준의 중복은 claim-level revalidation에서 다시 판단한다.

격리 파일의 원래 경로·새 경로·hash는 [`ARCHIVE-LEDGER.md`](ARCHIVE-LEDGER.md)에 있다. Git이 없는
환경이라 본문 변경 전 전체 복구 스냅샷도 만들었다:

- `.scratch/research/archive/2026-08-02/pre-curation-snapshot.tar.gz`
- SHA-256 `85e64e38b1977a8d9e47bd7eaf25fb9e9b2d14c072a3e9d0a1cf462bac0a090f`

## 노후·오류 위험

### 확인된 노후 앵커

ISO 공식 catalog는 ISO/IEC/IEEE 12207:2017을 withdrawn, ISO/IEC/IEEE 12207:2026을 current edition으로
표시한다. 경고 대상 8개 파일을 재검토해 현행 공개 catalog가 지지하는 범위, 역사적 2017판 상세,
clause-level INCONCLUSIVE를 분리했다. 구판 상세를 2026판에 재귀속하지 않았고 validator가 모든 12207
참조의 명시적 current-edition disposition을 검사한다.

### 제품 문서의 높은 변동성

기존 Markdown에는 `developers.openai.com` 44개, `code.claude.com` 27개 등 제품 문서 링크가 많다.
이 출처들은 제품 동작에는 적합하지만 빠르게 변한다. 문서에 `valid_as_of`, `review_due`, version/revision을
강제하지 않았으므로 “verified”가 시간 경과를 표현하지 못했다.

### 출처 계층 오류 가능성

Medium 12개, Wikipedia 5개, ResearchGate 4개 등 2차/미러 출처가 남아 있다. 존재 자체가 오류는 아니지만,
원 표준·원 논문이 있는 핵심 주장이 이 경로에만 의존하면 갱신해야 한다. 이번 감사는 971개 URL 모두의
사실 내용을 재검증했다고 주장하지 않는다. 그 대신 과대 상태를 내리고 claim-level 재검증 backlog를 만들었다.

### census의 해석 한계

GitHub census는 파일/설정의 채택률을 관측한다. 표본·탐지식·GitHub 편향을 가지며 효과성이나 규범을 증명하지
않는다. 기존 문서 일부는 “흔함 → floor/standard”로 넘어가는 합성을 충분히 분리하지 않았다. 앞으로 census
결과는 `local-census` claim으로 기록하고 권장안은 별도 `synthesis`로 남겨야 한다.

## AI가 읽기 쉬운 구조에 대한 조사 결과

“AI 연구 코퍼스 표준” 하나는 없다. 채택한 방식은 다음 표준과 검증된 관행의 최소 결합이다.

- FAIR: 식별자, 풍부한 metadata, provenance, machine-actionability.
- W3C PROV-O: provenance 관계 표현.
- RO-Crate 1.2: 공유/보존할 때 쓸 JSON-LD research-object package.
- NIST RDaF 2.0: research data lifecycle.
- PRISMA 2020 + Kitchenham/Charters: 검색·선정·평가·합성을 재현 가능하게 보고.
- Agent Skills와 현 Codex docs: metadata → 본문 → 필요한 reference 순서의 progressive disclosure.

따라서 일상 authoring은 Markdown + YAML, source identity는 JSONL, 배포/보존 export는 선택적 RO-Crate로
정했다. `llms.txt`는 웹사이트용 emerging convention이고 로컬 corpus의 검증 표준이 아니므로 추가하지 않았다.
상세 정책은 [`../corpus/methods/EVIDENCE-POLICY.md`](../corpus/methods/EVIDENCE-POLICY.md)에 있다.

## 아직 “모든 claim이 완전히 검증됨”이라고 부를 수 없는 이유

- 상속 문서 50개의 load-bearing disposition은 끝났지만, 48개를 원자 verified claim으로 승격하는 작업은
  필요할 때만 진행한다. review-needed 문서 전체를 verified로 부르지 않는다.
- active corpus Markdown + source registry 597개 URL의 endpoint reachability는 전수 검사했지만 claim-support/content drift는
  verified claim의 claim-level 검증 범위에서만 확인한다. 변경 전 snapshot 971개 URL은 역사 보존 대상이다.
- ISO 12207:2026 본문은 유료 표준이라 공식 catalog metadata 이상 coverage를 단정할 수 없다.
- 기존 census raw data는 무결성 검사를 할 수 있지만 표본을 새로 수집해 최신성을 재검증하지 않았다.
- framework 구조 crosswalk는 완료됐지만 ISO 상세 clause mapping은 licensed text 없이 INCONCLUSIVE다.
- retrieval fresh-context A/B pilot은 완료됐지만 다른 model/언어/task와 actual token 비용은 미측정이다.
- 완전 초심자 domain owner의 full-lifecycle baseline, 최소 의미 차이, comprehension/RAIR/RSR threshold,
  confirmatory 결과와 component attribution은 아직 미측정이다.

이 항목을 숨기지 않고 [`GAPS.ko.md`](GAPS.ko.md)의 P0 backlog로 고정했다. 이번 감사의 성과는 기존 자료를
또 엎은 것이 아니라, 무엇을 믿어도 되는지와 무엇을 아직 믿으면 안 되는지를 처음으로 분리한 것이다.
과거 자료가 어느 현재 영역과 backlog로 연결되는지는 [`HISTORICAL-MAP.ko.md`](HISTORICAL-MAP.ko.md)에
전수 배치했다.

## 조사에 사용한 현재 1차 자료

- IEEE Computer Society SWEBOK V4.0a — https://www.computer.org/education/bodies-of-knowledge/software-engineering
- ISO/IEC/IEEE 12207:2026 catalog — https://www.iso.org/standard/90219.html
- NIST RDaF 2.0 — https://doi.org/10.6028/NIST.SP.1500-18r2
- FAIR Principles — https://www.go-fair.org/fair-principles/
- W3C PROV-O — https://www.w3.org/TR/prov-o/
- RO-Crate 1.2 — https://www.researchobject.org/ro-crate/specification/1.2/
- PRISMA 2020 — https://www.prisma-statement.org/prisma-2020
- Agent Skills specification — https://agentskills.io/specification
- Codex customization — https://learn.chatgpt.com/docs/customization/overview
- OpenAI Sandbox Agents — https://developers.openai.com/api/docs/guides/agents/sandboxes
- MCP specification 2025-11-25 — https://modelcontextprotocol.io/specification/2025-11-25
- GitHub Flow — https://docs.github.com/en/get-started/using-github/github-flow
- GitHub secure use reference — https://docs.github.com/en/actions/reference/security/secure-use
