---
id: corpus-guide-ko
title: "리서치 코퍼스 안내"
kind: navigation
status: verified
last_updated: "2026-08-29"
evidence_track: none
freshness: durable
sources: []
---

# 리서치 코퍼스 안내

이 폴더는 “객관적 진리 모음”이 아니라 **주장마다 출처·범위·불확실성을 추적할 수 있는 근거 저장소**입니다.
가장 먼저 [`INDEX.md`](INDEX.md)를 읽고, 필요한 aspect만 점진적으로 여세요.

> ## 🔴 문서 안의 `gingoa`·`goppi`·`claudeck` 은 **이 저장소가 아닙니다**
>
> 이 코퍼스는 **폐기된 하네스들**(`claudeck-v1` → `claudeck` → `gingoa` → `codex-native` →
> `goppi` → `goppi_final`)을 위해 수집되기 시작했고, 그 시절 문서는 그때의 이름으로 주어를 씁니다 —
> 예: *“gingoa's ① output set”*. **그 문장들은 고치지 않습니다.**
> 그때 그 프로젝트가 무엇을 정했는지에 대한 **참인 기록**이고, 이름을 바꾸면 기록이 거짓이 됩니다.
>
> **읽는 규칙은 하나입니다** — 코퍼스 본문의 옛 이름은 **폐기된 하네스**를 가리키지
> **이 저장소(`coolbress/standards`)를 가리키지 않습니다.** 계보는
> [`../legacy/LINEAGE.md`](../legacy/LINEAGE.md), 현행 판단은 [`../direction/`](../direction/) 입니다.
>
> ⚠️ **새 문서는 옛 이름을 주어로 쓰지 않습니다.** `tools/check_corpus_identity.py` 가 기준선을 잡고 있습니다
> (`GAPS` R5-5).

## 신뢰 규칙

- `verified`: 현재 정책으로 주장과 근거가 검토된 문서입니다.
- `review-needed`: 과거 gingoa에서 승계했거나 현재 표준으로 재검토가 필요한 문서입니다.
- `draft`: 수집이나 검증이 끝나지 않았습니다.
- GitHub census는 “얼마나 흔한가”를 보여줄 뿐 “무엇이 좋은가”를 결정하지 않습니다.
- 공식 제품 문서는 해당 제품 동작에는 1차 자료지만 효과성의 증거는 아닙니다.
- 프로젝트 판단은 `../direction/`(현행) 또는 `../legacy/judgments/`(과거)에 기록하며 corpus의 사실처럼 취급하지 않습니다.

## 구조

| 위치 | 역할 |
|---|---|
| `_schema.md` | 문서·주장·상태 규칙 |
| `methods/EVIDENCE-POLICY.md` | 리서치 및 AI 탐색 방식의 근거 |
| `_meta/sources.jsonl` | 새로 검증한 출처의 기계 판독 레지스트리 |
| `TAXONOMY.md` | 안정된 28개 경로와 현재 한계 |
| `lifecycle.md` | 단계별 탐색용 로컬 오버레이 |
| `aspects/` | 주제별 합성 문서와 세부 근거 |
| `census-data/` | 재현 가능한 로컬 조사 자료 |
| `../audit/` | 이번 감사 결과·manifest·격리 기록 |
| `../legacy/sources/` | 과거 프로젝트 원본 사본 |
| `../legacy/judgments/` | 과거 하네스의 판단 · `../direction/` | 현행 방향 |
| `../archive/` | 활성 탐색에서 제외했지만 복구 가능한 자료 |

2026-08-02 감사에서 과거 `verified` 문서 50개는 `review-needed`로 낮췄고, 이후 50/50 load-bearing
claim disposition을 기록했습니다. `review-needed` 원문은 계속 설계 사실로 직접 인용하지 않습니다.
현재 부족 영역과 해제 조건은 `../audit/GAPS.ko.md`, 기획 판단 기준은
`../legacy/judgments/goppi/foundation/`, 통합 agent 보안 지도는
`aspects/27-ai-harness-archetype/agent-threat-model.md`에 있습니다.
