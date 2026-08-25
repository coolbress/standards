# 05 — 산출물이 시니어급이려면 무엇이 저장소에 있어야 하나

> 신설 2026-08-24 · rev1 · **소유자 지적으로 만들어졌다** — `01`~`04`가 *일하는 방식*만 다루고
> *산출물의 품질*은 거의 다루지 않았다. 목적은 *"현업 워크플로를 따라 기획·빌드하고
> **최종 산출물이 시니어 엔지니어급**이 되는 것"* 인데 뒤 절반이 비어 있었다.

## 왜 별도 문서인가

[`04`](04-the-plan.md)는 **"어떻게 일하는가"** 다 — 이슈·PR·CI·리뷰·머지.
이 문서는 **"무엇이 남는가"** 다 — 저장소를 열었을 때 시니어가 보고 *"제대로 지었다"* 고 말할 조건.

**둘은 다른 축이다.** 워크플로를 완벽히 따라도 `.gitignore`가 없고 락파일이 없고 시크릿이 커밋돼 있으면
산출물은 시니어급이 아니다.

## 근거

[`corpus/aspects/04-build-ci-engineering/foundation-floor-artifact-checklist.md`](../corpus/aspects/04-build-ci-engineering/foundation-floor-artifact-checklist.md)
`review-needed` — OpenSSF Scorecard · Best-Practices Badge · OSPS Baseline · SLSA v1.2 · 12-Factor ·
GitHub community-health · SWEBOK/ISO-12207을 대조해 만든 독립 체크리스트. **MUST 49 · REC 22.**

> **이 문서의 핵심 규칙**: *"② 기초는 **가장 약한 바닥 항목**으로 점수가 매겨진다."*
> 하나가 빠지면 나머지가 아무리 좋아도 그 수준이다.

## 바닥 — MUST 49개를 9묶음으로

| 묶음 | 무엇이 있어야 하나 |
|---|---|
| **VCS 위생** | `.gitignore` · **`main` 브랜치 보호**(PR 필수·검사 필수·force-push 금지) · 트리에 바이너리 산출물 없음 |
| **빌드·의존성** | **락파일 커밋** · 의존성 전부 버전 고정 · **GitHub Actions를 커밋 SHA로 핀**(태그는 가변 = 공급망 벡터) · **의존성 갱신 봇**(Dependabot/Renovate) · 재현 가능한 단일 빌드 진입점 · CI에서 warnings-as-errors |
| **CI/CD** | 매 PR·push에 CI · **lint·typecheck·test·build를 각각 별도 required check로** · 워크플로마다 `permissions:` 최소화(기본 토큰은 write-broad) · `pull_request_target` + 신뢰 불가 checkout 금지 |
| **코드 품질** | 린터 설정 커밋 · **포매터를 CI가 강제** · **SAST를 CI에**(CodeQL/Semgrep) · **시크릿 탐지**(gitleaks + push protection) |
| **테스트** | CI 초록 · **모든 PR에 테스트** · CONTRIBUTING에 테스트 정책 명문화 · **walking skeleton — 실제 end-to-end 한 줄기**(Cockburn) |
| **보안·공급망** | `SECURITY.md` · Dependabot/OSV 경보 · secret-scanning + push protection · **쓰기 권한에 MFA** · 자체 제작 암호 금지 · 취약점 대응 SLA(medium+ ≤60일) |
| **설정·시크릿** | **설정을 환경으로 외부화**(12-Factor III, 하드코딩 금지) · **`.env.example` 커밋 + 실제 `.env`는 ignore** |
| **개발환경·온보딩** | **README에 clone→install→test가 5명령 이내** · 통합 태스크 러너(Make/스크립트) |
| **문서** | README · CONTRIBUTING · **CHANGELOG**(Keep a Changelog) · 공개 표면이 있으면 API 레퍼런스 |
| **라이선스** 🆕 | **루트 `LICENSE`** — 의도적으로 고른 아웃바운드 라이선스 하나를 기계가 읽을 수 있게 선언한다(측면 25). ⚠️ **라이선스가 없으면 기본값은 *전부 저작권 보유*** 이므로 공개 저장소에서는 *"재사용 가능"* 이 성립하지 않는다. **2026-08-26 추가** — 커버리지 조사([`COVERAGE-JUDGMENT`](../audit/COVERAGE-JUDGMENT.ko.md))가 이 항목의 부재를 잡았고, **공개 저장소 3/3 이 실제로 위반 중이었다** |

> 🔴 **2026-08-25 커버리지 조사 — 이 바닥에 빠진 것이 있다.** *항상 켜짐* 20측면 중 **10개만** 위 9묶음에 반영돼 있다.
> 확증 공백 셋의 처분이 끝났다: **25 라이선스는 바닥에 넣었고**(아래 *라이선스* 줄 · 3저장소 반영), **02 ADR · 24 CODEOWNERS 는 넣지 않기로 판정했다**(아래 *판정* 절 — 근거는 코퍼스 자신의 census 와 1인 구조다).
> **그리고 25 의 누락은 실물로 나타났다 — 공개 저장소 3/3 에 `LICENSE` 가 없다**(2026-08-25 `gh api` 확인).
> 바닥에 없어서 → 템플릿에 안 들어갔고 → 인스턴스도 안 갖는다. `GAPS` **R5-17** · [`COVERAGE-JUDGMENT`](../audit/COVERAGE-JUDGMENT.ko.md)

### 판정 (2026-08-26) — **02 ADR · 24 CODEOWNERS 는 바닥에 넣지 않는다**

커버리지 조사가 확증 공백 셋을 냈다(`GAPS` R5-17). **25 라이선스는 넣었다.** 나머지 둘은 조사해 보니
**넣지 않는 것이 코퍼스 자신의 근거와 맞는다.** 판정을 남긴다 — 다음 사람이 *"빠졌네"* 하고 다시 넣지 않도록.

#### 02 아키텍처 — ADR: **활동은 유지, 산출물 형식은 강제하지 않는다**

`docs/adr/` 를 공개 저장소의 MUST 로 두는 것은 **코퍼스 자신의 census 와 어긋난다**:

| 근거 | 수치 |
|---|---|
| 429-저장소 governance census | 형식 **ADR 디렉터리 2~4%** · planning/design 문서 **공개 13~19%** |
| Buchgeher et al. (IEEE Access 2023, 900+ 저장소) | 채택은 낮으나 상승 중 · **ADR 보유 저장소의 약 50%가 레코드 1~5개** — *"tried, didn't stick"* |
| [`02 overview`](../corpus/aspects/02-architecture-design/02-architecture-design--overview.md) 자신의 문장 | *"seniors **do** design …, but they rarely **publish** the artifacts to a public remote"* |

그리고 [`24 overview`](../corpus/aspects/24-governance-collaboration-compliance/24-governance-collaboration-compliance--overview.md)가 **반대 방향으로 경고**한다 —
원격 아티팩트가 `ADR-NNNN` 같은 로컬 전용 문서를 인용하면 **dangling reference** 이고 **내부 구조가 샌다.**

> **활동 자체는 `[lit]` 로 받쳐진다** — *"real 결정을 기록한다"*. 그리고 **이 저장소는 이미 하고 있다**:
> [`04 §범위 결정`](04-the-plan.md)(R5-11 Python 전용) · [`01`](01-what-i-want.md)의 두 경계 · [`GAPS`](../audit/GAPS.ko.md) 처분란 · PR 본문.
> **형식이 없는 게 아니라 장소가 다를 뿐이다.** 빈 의식 스텁을 만드는 것은 `02` 자신이 금지한다(*"Never write empty ritual stubs"*).

→ **산출물 바닥에는 넣지 않는다.** 결정 기록은 **워크플로 축**([`04`](04-the-plan.md))이 담당한다.
C50-10 의 처분도 같다 — *"산출물과 시점은 risk/decision별 조건부"*.

#### 24 거버넌스 — CODEOWNERS: **1인에서 기계적으로 무효다**

CODEOWNERS 의 기능은 *"auto-requests the right reviewers"* 인데 —
**GitHub 은 PR 작성자에게 리뷰를 요청하지 않는다.** 1인 저장소에서 `* @coolbress` 는 **아무 일도 하지 않는다.**

**실측 2026-08-26** — 집행 경로 자체가 없다:

```
require_code_owner_review: false
required_approving_review_count: 0
```

[`01`](01-what-i-want.md) 경계 ②가 *"사람 동료 리뷰를 시뮬레이션하는 것이 아니다"* 인데,
**작동하지 않는 CODEOWNERS 를 두는 것이 정확히 그 시뮬레이션이다** — 파일은 있고 집행은 없다.
`04`의 *"presence≠adequacy"* 가 이름 붙인 것과 같은 형태다.

→ **바닥에 넣지 않는다.** 측면 24 의 나머지 절반(**브랜치 보호**)은 **이미 바닥에 있다**(VCS 위생).
**다시 여는 조건**: 기여자가 **2인 이상**이 되거나 룰셋에서 `require_code_owner_review` 를 켤 때.

## 이 중 무엇이 **자동으로** 채워지나

**대부분은 `project-template`(만들 것 3)에 한 번 넣으면 끝난다** — 파일이기 때문이다.

| 어디서 | 무엇 |
|---|---|
| `project-template` | `.gitignore` · `.env.example` · 린터·포매터 설정 · `SECURITY.md` · `CONTRIBUTING.md`(테스트 정책 포함) · `CHANGELOG.md` · README 골격 · `.editorconfig` · **`LICENSE`(MIT · 2026-08-26)** — 템플릿의 라이선스는 **뜨는 모든 프로젝트에 복사된다** |
| `coolbress/workflows` (만들 것 2) | lint·typecheck·test·build 4검사 · **SAST** · **gitleaks** · `permissions:` 최소화 · **Actions SHA 핀** |
| `new-project.sh` (만들 것 5) | 브랜치 보호 룰셋 · **Dependabot 설정** · secret-scanning·push-protection 켜기 |
| GitHub 계정 설정 | **MFA**(1회) |
| 프로젝트마다 사람이 | **walking skeleton** — 첫 조각을 end-to-end 한 줄기로 (`/kickoff`가 유도) |

**즉 바닥 49개 중 대부분이 만들 것 2·3·5에 이미 들어가야 했다.** 이 문서가 그 목록을 확정한다.

## 🔴 새로 생기는 만들 것

| # | 무엇 | 왜 |
|---|---|---|
| **10** | **바닥 검사 CI 잡** (`floor-check`) — 락파일 있나 · `.env`가 커밋됐나 · Actions가 SHA 핀인가 · `.env.example` 있나 | 바닥은 **가장 약한 항목으로 점수가 매겨진다**. 사람이 매번 확인할 수 없다 |
| **11** | **Dependabot/Renovate 설정을 템플릿에** | MUST인데 만들 것에 없었다 |
| **12** | **SAST + gitleaks를 `coolbress/workflows`에** | MUST인데 `ci.yml` 4검사에만 있었다 |

## 위험 비례 — 전부를 항상 켜지 않는다

[`03`](03-what-research-says.md)의 *"깊이는 위험에 비례"* 와
[`corpus/aspects/04/visibility-provision-matrix.md`](../corpus/aspects/04-build-ci-engineering/visibility-provision-matrix.md)를 따른다:

- **비공개 + Free 플랜**: CodeQL·secret-scanning이 **막힌다** → Semgrep·gitleaks로 대체(matrix가 대체재를 규정)
- **로컬 실험**: 바닥 전체가 과하다. `github-workflow-current.md`의 risk-scaled 표를 쓴다
- **공개 웹앱**: 바닥 전부 + 접근성(WCAG 2.2 AA)·개인정보(GDPR/PIPA) — 아래

## 아키타입별 층 — 누가 판정하나

### 먼저: 대부분은 **항상 켜진다**

코퍼스 28측면의 `gated_archetypes` frontmatter가 이미 이걸 규정한다:

> 🔴 **2026-08-25 커버리지 조사 정정 — 이 문단은 필드를 과대해석했다.**
> `gated_archetypes` 는 **`_schema.md` 에 정의가 없고 `validate_corpus.py` 가 검사하지도 않는다.**
> 그리고 **`[]` 를 *"항상 켠다"* 로 읽을 근거가 없다** — `[]` 인 **19**(*"instrument **services**"*) ·
> **20**(*"operate a **running service** against SLOs"*) · **18**(*"publishes to the canonical channel"*)
> 의 claim 자체가 조건을 전제한다. `[]` 가 *"항상"* 이면 로컬 CLI 에도 SLO·on-call 이 요구된다.
> **아래 20/7/1 집계는 맞지만, 그 20개가 *무조건 켜진다*는 해석은 아직 근거가 없다.**
> [`COVERAGE-JUDGMENT`](../audit/COVERAGE-JUDGMENT.ko.md) · `GAPS` **R5-16**


| 종류 | 개수 | 뜻 |
|---|---|---|
| `universal` + `cross-cutting` | **20** | **무엇을 만들든 켠다** — 위 바닥 49개가 대부분 여기서 나온다 |
| `gated` | **7** | 조건부 |
| `internal` | 1 | 하네스 자신용(폐기) |

**즉 아키타입 판정이 필요한 것은 7개뿐이다.** 나머지 20개는 판정 없이 항상이다 —
그래서 이 문제는 처음 보였던 것보다 훨씬 작다.

### gated 7개 — 판정 방식을 셋으로 가른다

**원칙: 선언을 만들지 말고, 가능하면 저장소가 스스로 드러내게 한다.**
선언 파일을 두면 **선언과 실제가 어긋나는 드리프트**가 새 문제로 생긴다.

| 측면 | 게이트 조건 | 판정 방식 |
|---|---|---|
| **13** API 설계 | library·cli·backend | 🟢 **존재로 판정** — `openapi.*`·`*.proto`·공개 export가 있으면 켠다 |
| **14** 마이그레이션 | backend·data-ml | 🟢 **존재로 판정** — `migrations/`·ORM 스키마가 있으면 켠다 |
| **26** MLOps | data-ml | 🟢 **존재로 판정** — 모델/데이터 파이프라인이 있으면 |
| **12** 성능 | web·backend·data-ml·mobile·library | 🟡 **거의 전부 해당** → 사실상 universal로 취급하되 **예산 수치는 `/kickoff`가 받는다** |
| **15** 접근성 | web·mobile | 🟡 프레임워크로 추정은 되나 **법적 의무 여부는 추정 불가** → `/kickoff` |
| **16** 개인정보 | handles-user-data | 🔴 **파일로 판정 불가 — 의도다** → `/kickoff` |
| **21** 비용·spend cap | cloud·published | 🔴 **배포 의도 — 파일로 판정 불가** → `/kickoff` |

### 그래서 `/kickoff`가 물을 것은 **두 가지뿐**이다

`/kickoff`에 아키타입 문진표를 만들지 않는다. **질문 2개면 된다:**

1. **"사람들에게 공개할 건가요, 나 혼자 쓸 건가요?"**
   → 공개면 **접근성(15) · 비용/spend cap(21) · 관측성 · SLO**가 켜진다.
   `github-workflow-current.md`의 risk-scaled 표(*local-only / published / team / production*)와 같은 축이다.
2. **"남의 개인정보를 다루나요?"** (이름·이메일·결제·위치 등)
   → 그렇다면 **개인정보(16)** 가 켜진다 — GDPR Art.25 · PIPA 제30조.

**나머지 5개는 묻지 않는다.** 저장소가 드러내거나(13·14·26), 항상 켠다(12).

### 왜 이 분업인가

- **묻는 것이 적을수록 좋다** — 문제 지도 **P40**(*"재량으로 될 일을 계속 물어 불필요하게 방해받는다"*)이
  거짓 양성을 실패로 센다. 아키타입 문진 10문항은 그 자체가 P40 위반이다.
- **존재로 판정하면 드리프트가 없다** — 선언 파일은 갱신을 잊으면 거짓말이 된다.
  `migrations/`가 생겼는데 선언이 안 바뀌면 검사가 안 켜진다. **저장소가 진실이다.**
- **의도는 물어야 한다** — 공개 여부와 개인정보는 파일에 안 적혀 있고, **둘 다 법적 의무를 부른다.**
  틀리면 되돌릴 수 없는 종류다(문제 지도 P21a·P33·P35).

### 만들 것에 미치는 영향

| # | 조정 |
|---|---|
| **4** `/kickoff` | 질문 **2개 추가**(공개 여부 · 개인정보). 문진표가 아니다 |
| **10** `floor-check` | **존재 기반 조건부 검사** — `migrations/` 있으면 마이그레이션 검사, `openapi.*` 있으면 계약 검사. 없으면 **skip**(FAIL 아님) |
| **13** 🆕 **공개 웹앱 층** | 접근성(axe) · 개인정보 체크리스트 · spend cap · 헬스체크 — **`/kickoff` 답이 "공개"일 때만.** 첫 아키타입 하나만 만든다 |

> ⚠️ **한 번에 다 만들지 않는다.** `03`의 *"깊이는 위험에 비례"* 와 이 저장소의 제외 항목
> (*"세팅 자체에 시간 쓰기"*)을 따른다. **첫 프로젝트가 공개 웹앱일 때 13번을 만들고, 그 전에는 안 만든다.**

## 한 줄

> **`01`~`04`는 "일을 어떻게 하는가", 이 문서는 "무엇이 남는가"다.**
> 워크플로를 완벽히 따라도 바닥이 비면 산출물은 시니어급이 아니다 —
> **바닥은 가장 약한 항목으로 점수가 매겨지기 때문이다.**
