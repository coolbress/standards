# Retrieval 변경 전·후 비교 — 2026-08-02

## 아주 쉽게 말하면

도서관을 다시 정리했다고 생각하면 된다. 질문 30개를 들고 옛 도서관과 새 도서관에 각각 들어가서
다음을 확인했다.

1. 맞는 책까지 길이 연결되어 있는가?
2. 그 책 안에 필요한 근거 표지가 있는가?
3. 아직 검토 중인 책을 “검증 완료”라고 잘못 표시하지 않았는가?
4. 검증 완료라고 했다면 주장-출처 표가 실제로 있는가?
5. 답 하나를 찾으려고 도서관 전체를 읽어야 하는가?

변경 전은 **책 위치는 잘 찾았지만 거의 모든 책에 잘못된 verified 도장**이 찍혀 있었다. 변경 후는
찾는 속도는 유지하면서 그 도장을 바로잡고, 현재 근거에는 claim/source/expiry를 붙였다.

## 비교 설계

- 입력: immutable `pre-curation-snapshot.tar.gz`와 현재 active corpus.
- 문항: 기존 `retrieval-cases.jsonl` 30개. 29개는 양쪽에 같은 정보가 있던 구조 비교, 1개(현행
  GitHub Actions permission/action pinning)는 새 foundation 보강 효과로 별도 표기.
- 동일 조건: 각 arm의 INDEX에서 최대 2-hop, INDEX+target 두 문서만 읽는 계약.
- 반복: case order를 다르게 한 deterministic 5회. 결과 편차가 생기면 실패.
- 검사기: `tools/evaluate_retrieval_before_after.py`; snapshot을 풀어 쓰지 않고 tar 내용을 read-only로 읽음.

## 실행 결과

| 지표 | 변경 전 | 변경 후 | 해석 |
|---|---:|---:|---|
| 2-hop 내 target route | 30/30 | 30/30 | 탐색 길은 원래도 좋았고 유지됨 |
| 필요한 answer anchor | 28/33 | 33/33 | 새 lifecycle anchor 2개와 현재 GitHub claim/source/expiry 3개가 보강됨 |
| 상태 보정 | 1/29 | 29/29 | 옛 28 aspect의 과대 `verified`가 `review-needed`로 교정됨 |
| 근거표 없는 verified target | 29 | 0 | 가장 큰 개선; “도장만 verified” 제거 |
| traceable verified target | 0 | 1 | 현행 GitHub target이 claim/source register를 가짐 |
| median 두 문서/전체 Markdown | 2.03% | 2.06% | INDEX 보강으로 +0.03%p, 실질 차이 작음 |
| 최대 두 문서/전체 Markdown | 3.11% | 3.11% | 전체 corpus 로딩 불필요 |
| deterministic 5회 편차 | 0 | 0 | 검사 자체가 순서에 흔들리지 않음 |

실행 판정: **PASS**. “새 구조가 길을 더 잘 찾는다”가 핵심 결과는 아니다. 같은 routing을 유지하면서
**근거 상태를 훨씬 정직하게 읽게 만든 것**이 측정된 개선이다.

## 별도 fresh-context 모델 A/B

이 5회 반복 자체는 코드로 검사한 구조 반복이지 AI 모델 반복이 아니다. 그 누락은 별도 동일 10문항,
fresh context 3회/arm으로 보완했다. 결과는 before 정답 5·5·9/10, after 10·10·10/10; unsupported
claim 5·5·1→0·0·0; 평균 read bytes 227,812→100,120이었다. 상세 채점과 한계는
[`RETRIEVAL-MODEL-AB-RESULTS.ko.md`](RETRIEVAL-MODEL-AB-RESULTS.ko.md)에 있다.

따라서 판정은 둘로 나뉜다.

- **구조·근거 상태 A/B:** CLOSED/PASS.
- **반복 fresh-model A/B pilot:** CLOSED/PASS for this task/model/date; arm별 3회, answer correctness,
  citation support, unsupported claim, file/byte context proxy 기록. 실제 model token은 telemetry 부재로
  `UNAVAILABLE`이며 일반화는 INCONCLUSIVE다.

이 구분은 결과를 축소하려는 것이 아니라 “deterministic 30/30”을 “AI가 언제나 30/30”으로 바꾸는
과장을 막는다.
