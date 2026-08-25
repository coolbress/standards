# 커버리지 판정 — 28측면 중 무엇이 하중을 받아야 하나

> 조사일 2026-08-25 · 프로그램 [#49](https://github.com/coolbress/standards/issues/49) 커버리지 단계 ·
> **질문**: 재검증은 *있는 인용이 맞는지* 만 봤다. **빠진 주제는 무엇인가?**

## 왜 이 조사가 필요했나

1·2단계는 `direction/03`이 **이미 인용한** 18건을 검증했다. 그 선택 자체는 검증하지 않았다 —
**과거 세션이 우연히 인용한 것**이 대상이 됐을 뿐이다. 소유자 목적이
*"객관적·**광범위한** 리서치를 근거로 워크플로와 **산출물 기준**을 정한다"* 이므로,
*광범위*와 *산출물 기준* 두 축을 각각 재야 한다.

## 조사 1 — 분류는 실재하고 완전하다

28측면 전수의 `gated_archetypes` frontmatter를 셌다:

| 값 | 개수 | 측면 |
|---|---:|---|
| `[]` | **20** | 01·02·03·04·05·06·07·08·09·10·11·17·18·19·20·22·23·24·25·28 |
| 게이트 있음 | **8** | 12·13·14·15·16·21·26 (+27 `ai-harness`) |

[`direction/05`](../direction/05-the-output-floor.md)의 R5-8 판정(*"gated 7 + internal 1"*)과 **일치한다.**

## 🔴 조사 2 — 그런데 그 필드는 **스키마에 없고 검사도 없다**

| 확인 | 결과 |
|---|---|
| [`corpus/_schema.md`](../corpus/_schema.md)에 `gated_archetypes` 정의 | **없음** |
| [`validate_corpus.py`](../tools/validate_corpus.py)가 이 필드를 검사 | **안 한다** (등장 0회) |
| `direction/05`가 이 필드를 근거로 쓰는가 | **쓴다** — *"코퍼스 28측면의 `gated_archetypes` frontmatter가 이미 이걸 규정한다"* |

**즉 방향의 아키타입 층 전체가 *정의된 적 없고 검사된 적 없는 필드* 위에 서 있다.**

### 그리고 `[]` 를 *"항상 켠다"* 로 읽은 것은 근거가 없다

빈 배열은 *"게이트가 없다(=항상)"* 로도, *"게이트 미지정"* 으로도 읽힌다. **원문이 후자를 가리킨다** —
`[]` 인 세 측면의 claim 자체가 **조건을 전제한다**:

| 측면 | `gated_archetypes` | 그런데 claim 원문은 |
|---|---|---|
| **19** 관측성 | `[]` | *"instrument **services** for the three pillars…"* |
| **20** 운영·사고 | `[]` | *"operate a **running service** against explicit SLOs…"* |
| **18** 패키징·배포 | `[]` | *"ship from a tagged, SemVer'd CI release that **publishes to the archetype's canonical channel**…"* |

`[]` 가 *"항상"* 이라면 **로컬 CLI 스크립트에도 SLO와 on-call이 요구된다.** 성립하지 않는다.
→ **분류와 claim 본문이 어긋나 있고, 어긋남을 잡을 검사가 없다.**

## 조사 3 — 바닥은 *"항상 켜짐 20개"* 중 **10개**만 반영한다

[`direction/05`](../direction/05-the-output-floor.md)의 바닥 9묶음을 측면에 역매핑했다.
그리고 **바닥 전체가 코퍼스 문서 *하나*에서 나온다** — [`foundation-floor-artifact-checklist`](../corpus/aspects/04-build-ci-engineering/foundation-floor-artifact-checklist.md)
(`status: review-needed` · `kind: research-log`). 그 문서의 처분은 [`CLAIM-REVALIDATION`](CLAIM-REVALIDATION.ko.md) **C50-14**:
***RETAIN-RN/SYNTHESIS · "파일 presence≠adequacy"***.

| 측면 | 바닥에 항목이 있나 | 판정 |
|---|---|---|
| 03·04·05·06·07·08·09·10·22·23 | ✅ 있다 | 반영됨 (10개) |
| **25** 라이선스 | ❌ **`LICENSE` 0회** | 🔴 **확증 공백** — 아래 실물 위반 |
| **02** 아키텍처 | ❌ **`ADR` 0회** | 🔴 **공백** — claim이 *"capture each significant decision as an ADR"*, ADR은 저장소에 남는 파일이다 |
| **24** 거버넌스 | ❌ **`CODEOWNERS` 0회** | 🔴 **부분 공백** — 브랜치 보호는 있으나 소유권·ADR이 없다 |
| **17** 릴리스 | 🟡 `CHANGELOG`만 (`SemVer` 0회) | 🟡 **부분** — 자동 릴리스·태깅이 바닥에 없다 |
| **11** 유지보수 | ❌ 없음 | 🟡 **정당할 수 있다** — C50-22가 *"universal bundle 근거 없음"* 으로 처분 |
| **18·19·20** | ❌ 없음 | 🟡 **분류 오류 의심** (위 조사 2) — 부재가 오히려 맞고, `[]` 가 틀렸을 수 있다 |
| **01·28** | ❌ 없음 | ✅ **정당한 부재** — 워크플로 축이라 [`04`](../direction/04-the-plan.md)가 담당한다 |

## 🔴 조사 4 — 실물 확인: LICENSE가 **공개 저장소 3/3에 없다**

문서 분석이 아니라 실측이다 (`gh api repos/{r}/license`, 2026-08-25):

| 저장소 | 공개 | LICENSE | CODEOWNERS |
|---|---|---|---|
| `coolbress/standards` | ✅ | 🔴 **없음(404)** | 🔴 없음 |
| `coolbress/project-template` | ✅ | 🔴 **없음(404)** | 🔴 없음 |
| `coolbress/workflows` | ✅ | 🔴 **없음(404)** | 🔴 없음 |

측면 25의 claim은 *"pick a single deliberate outbound license, declare it machine-readably
(**a root LICENSE** plus per-file SPDX)"* 다. **라이선스 없는 공개 저장소는 기본적으로 전부 저작권 보유**이므로,
*"재사용하라고 만든 템플릿"* 이라는 목적과 정면으로 어긋난다.

> **이것이 커버리지 조사의 값이다.** 바닥이 25측면을 반영하지 않았고 → 템플릿에 안 들어갔고 →
> 그 템플릿으로 뜬 저장소도 안 갖는다. **한 측면의 누락이 세 저장소로 전파됐다.**
> 재검증 5배치는 이걸 못 잡는다 — **있는 인용을 검사할 뿐 빠진 주제를 찾지 않기 때문이다.**

## 종합 — 답은 *"아직 아니다"* 이고, 이유는 셋이다

1. **분류의 근거가 없다** — `gated_archetypes`는 스키마 미정의·미검사이고, `[]` 를 *"항상"* 으로 읽은 것은 세 측면의 claim과 모순된다.
2. **바닥의 근거가 얇다** — MUST 49 전체가 `review-needed` 문서 **하나**에서 나오고, 그 문서의 처분은 *"synthesis · presence≠adequacy"* 다.
3. **누락이 실물로 나타났다** — 25측면 누락 → LICENSE 없는 공개 저장소 3개.

**다음**: 위 🔴 3건(25·02·24)을 바닥에 넣을지 판정하고, `gated_archetypes`의 의미를 스키마에 정의한 뒤 검사를 붙인다.
`GAPS` **R5-16**(분류 미정의) · **R5-17**(바닥 공백 3건)으로 등재했다.
