# Fresh-context retrieval A/B 결과 — 3회/arm

> 실행일 2026-08-02 · 같은 host/model family의 native fresh context 6개 · read-only · web 없음 · 각 arm은
> 상대 arm/audit/interpretation을 보지 않음. 채점 기준은 결과를 읽기 전에
> [`RETRIEVAL-MODEL-AB-PROTOCOL.md`](RETRIEVAL-MODEL-AB-PROTOCOL.md)에 고정했다.

## 결과

| Arm · repetition | 정답 /10 | 인용 지지 /10 | unsupported claim | unique files | bytes read |
|---|---:|---:|---:|---:|---:|
| before · 1 | 5 | 8 | 5 | 16 | 207,765 |
| before · 2 | 5 | 8 | 5 | 17 | 221,758 |
| before · 3 | 9 | 10 | 1 | 18 | 253,912 |
| **before 평균 (범위)** | **6.33 (5–9)** | **8.67 (8–10)** | **3.67 (1–5)** | **17.00 (16–18)** | **227,812 (207,765–253,912)** |
| after · 1 | 10 | 10 | 0 | 11 | 96,623 |
| after · 2 | 10 | 10 | 0 | 11 | 96,623 |
| after · 3 | 10 | 10 | 0 | 12 | 107,113 |
| **after 평균 (범위)** | **10.00 (10–10)** | **10.00 (10–10)** | **0.00 (0–0)** | **11.33 (11–12)** | **100,120 (96,623–107,113)** |

현재 arm은 이 표본에서 파일 수 33.3%, 읽은 bytes 56.1%를 줄였다. subagent별 실제 input/output token은
collaboration telemetry가 제공하지 않아 `UNAVAILABLE`이며 bytes를 context-cost proxy로 사용했다.

## 질문별 adjudication 원장

표기 `C/S/U` = correctness point / citation-support point / unsupported-claim count.

| Q | before-1 | before-2 | before-3 | after-1 | after-2 | after-3 | 핵심 판정 |
|---|---|---|---|---|---|---|---|
| 1 GitHub permission/pinning | 0/0/1 | 0/0/1 | 1/1/0 | 1/1/0 | 1/1/0 | 1/1/0 | old는 direct current GitHub 근거가 없고 한 반복은 default 권한 모순까지 발견; current는 GHW-005/expiry 직결 |
| 2 Requirements status | 0/1/1 | 0/1/1 | 1/1/0 | 1/1/0 | 1/1/0 | 1/1/0 | old metadata를 그대로 믿은 두 반복은 compound claim을 verified current로 과신 |
| 3 Harness planes | 0/1/1 | 0/1/1 | 0/1/1 | 1/1/0 | 1/1/0 | 1/1/0 | old는 additive component list만 있고 6-plane current map 없음 |
| 4 Integrated threat path | 1/1/0 | 1/1/0 | 1/1/0 | 1/1/0 | 1/1/0 | 1/1/0 | old 반복도 통합 model 부재를 정직하게 표시; current는 prevention/detection/recovery 연결 |
| 5 Standards crosswalk | 1/1/0 | 1/1/0 | 1/1/0 | 1/1/0 | 1/1/0 | 1/1/0 | old는 부재·licensed limitation을 식별, current는 28행과 INCONCLUSIVE 경계 탐색 |
| 6 Target-user evidence | 1/1/0 | 1/1/0 | 1/1/0 | 1/1/0 | 1/1/0 | 1/1/0 | old는 직접 능력 연구 부재, current는 6축+transfer 미확립을 회수 |
| 7 Solo operation | 1/1/0 | 1/1/0 | 1/1/0 | 1/1/0 | 1/1/0 | 1/1/0 | 양쪽 모두 validated solo scaling 부재를 과장하지 않음; current는 review status 명시 |
| 8 Testing status | 0/1/1 | 0/1/1 | 1/1/0 | 1/1/0 | 1/1/0 | 1/1/0 | old verified 도장을 따른 두 반복은 전체 synthesis를 승격; current는 review-needed 회수 |
| 9 Product docs ≠ effectiveness | 0/0/1 | 0/0/1 | 1/1/0 | 1/1/0 | 1/1/0 | 1/1/0 | old는 explicit rule 없이 inference, current evidence policy는 직접 규칙 제공 |
| 10 Lifecycle navigation | 1/1/0 | 1/1/0 | 1/1/0 | 1/1/0 | 1/1/0 | 1/1/0 | 둘 다 lifecycle을 찾았지만 current만 retirement와 status를 한 경로에서 제공 |

독립 context 식별자: `retrieval_before_1`, `retrieval_before_2`, `retrieval_before_3`,
`retrieval_after_1`, `retrieval_after_2`, `retrieval_after_3`. 각 context는 10개 답, 실제 연 파일 목록,
`wc -c` 결과를 반환했고 파일을 수정하지 않았다. 여섯 원문 답변, file list, byte calculation,
runtime-identity limitation은 [`model-ab-raw/MANIFEST.tsv`](model-ab-raw/MANIFEST.tsv)와 같은 폴더의
`before-1..3.md`/`after-1..3.md`에 SHA-256과 함께 보존한다.

## 결론과 한계

- 이 task set에서 current corpus는 **더 정확하고 안정적이며 더 적은 문서**로 답했다.
- 가장 큰 변화는 topic routing 자체보다 status/claim/source/expiry를 같이 회수해 **과대 verified를
  답으로 내보내지 않은 것**이다.
- before 3회차가 9/10까지 올라간 것은 모델이 모순을 스스로 발견할 수 있음을 보여주지만, 5–9의 범위는
  구조가 그 판단을 모델 재량에 맡겼다는 뜻이다. after는 세 번 모두 10/10이었다.
- 열 문항 중 일부는 새 target-user/threat/crosswalk 내용을 직접 묻는다. 따라서 이 결과는 순수한 layout
  효과가 아니라 **curation content + evidence status + retrieval architecture의 합산 효용**이다. 순수 구조
  비교는 별도 deterministic 29개 shared-information set 결과를 사용한다.
- 세 반복·한 host/model family·한 날짜·영어 질문의 소규모 pilot이다. 다른 모델/언어/질문에 대한 일반화,
  source truth 자체, 실제 token 비용은 입증하지 않는다.
