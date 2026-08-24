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

## 이 중 무엇이 **자동으로** 채워지나

**대부분은 `project-template`(만들 것 3)에 한 번 넣으면 끝난다** — 파일이기 때문이다.

| 어디서 | 무엇 |
|---|---|
| `project-template` | `.gitignore` · `.env.example` · 린터·포매터 설정 · `SECURITY.md` · `CONTRIBUTING.md`(테스트 정책 포함) · `CHANGELOG.md` · README 골격 · `.editorconfig` |
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

## ⬜ 아직 방향에 없는 것 — 아키타입별 층

바닥 위에 **무엇을 만드느냐에 따라 추가되는 것**이 있고, 이건 아직 `direction`에 없다:

| 아키타입 | 추가로 필요한 것 | 코퍼스 |
|---|---|---|
| **공개 웹앱** | **WCAG 2.2 AA**(법적 의무 축 포함) · **개인정보**(GDPR Art.25 · PIPA 제30조) · 관측성(구조화 로그·RED 메트릭) · **SLO와 에러 예산** · 백업/복원 · **spend cap** | 15 · 16 · 19 · 20 · 21 |
| **API가 있는 것** | **OpenAPI 계약 먼저** · 버저닝 | 13 |
| **DB가 있는 것** | **전진 전용 버전 마이그레이션** | 14 |
| **배포되는 것** | SemVer 태그 · **release-please** · CHANGELOG 자동화 | 17 · 18 |
| **라이브러리** | 라이선스 선언(root LICENSE + SPDX) | 25 |

**이건 `/kickoff`가 물어야 한다** — *"무엇을 만드나"* 에 따라 켤 층이 달라지기 때문이다.
→ [`audit/GAPS.ko.md`](../audit/GAPS.ko.md) **R5-8**.

## 한 줄

> **`01`~`04`는 "일을 어떻게 하는가", 이 문서는 "무엇이 남는가"다.**
> 워크플로를 완벽히 따라도 바닥이 비면 산출물은 시니어급이 아니다 —
> **바닥은 가장 약한 항목으로 점수가 매겨지기 때문이다.**
