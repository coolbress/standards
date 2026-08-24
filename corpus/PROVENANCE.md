# corpus/ — 승계 기록 (PROVENANCE)

> **2026-08-02 audit notice:** 아래는 승계 당시 기록이다. 현재 governing schema는 `_schema.md`, 감사
> 결과는 `../audit/AUDIT.ko.md`, gap 상태는 `../audit/GAPS.ko.md`가 우선한다. 승계 당시의 “locked”와
> “verified” 표시는 현재 검증 상태가 아니다.

- **원본**: `~/gingoa/docs/research/` (gingoa 하네스의 엔지니어링 표준 코퍼스)
- **이관일**: 2026-08-02 · 이관 방식: 파일 사본 (원본 저장소는 무수정 보존)
- **이관 범위**: INDEX.md · _schema.md · TAXONOMY.md · lifecycle.md · GUIDE.ko.md · three-tier-ledger.md · aspects/ (28개 aspect + sub-docs, 82 md) · census-data/ (불변 원시 증거)
- **상태**: 이관 직후 — 내용은 gingoa 시점(2026-06) 그대로. `gingoa_applied:` frontmatter, "Implications for gingoa" 섹션 등 gingoa 종속 표기가 남아 있음.

## goppi_final에서의 지위

이 코퍼스가 goppi_final 리서치의 **본체(표준 층)**다. 승계 당시 28-aspect 분류는 SWEBOK·당시
ISO/IEC/IEEE 12207:2017(현재 폐기된 역사적 판본)·25010·29148·OWASP·SLSA·DORA·SRE 등에 앵커되어 4각 심층 리서치로
잠금(locked)됐고(TAXONOMY.md), 스키마·증거 태그(`[lit]/[census]/[inferred]`)·상태 라이프사이클은
`_schema.md`가 규정했다. 2017판은 현재 폐기(withdrawn)됐으며 현행판은 ISO/IEC/IEEE 12207:2026이다.
새 리서치는 루트에 흩어두지 않고 이 코퍼스의 해당 aspect에 접목한다(§3b).

## 승계 후 적응 (완료 기록)

- [x] **2026-08-02 facts 층 접목 완료** — 11개 파일이 `facts-2026-08-*.md`로 각 aspect에 편입(§3a frontmatter, `kind: research-log`, `language: ko`), `<topic>--overview.md` Sub-documents + INDEX deep-dive에 링크. 매트릭스는 corpus 루트 `facts-2026-08-matrix.md`(경로 매핑 헤더 포함).

> **열린 작업은 이 파일에서 추적하지 않는다.** 남은 적응·유지보수 항목(gingoa 표기 정리, imported 접목,
> census 시효, 태그 통일, 교차 링크 등)은 [`../audit/GAPS.ko.md`](../audit/GAPS.ko.md)의 유지보수 backlog가
> 단일 추적처다 (2026-08-02 이관 — TODO 이원화 제거). 이 파일은 계보(lineage) 기록만 보존한다.

## 2026-08-02 evidence-boundary audit

- [x] 변경 전 203-file manifest + SHA-256 생성
- [x] 빈 `.err` 14개와 `.pyc` 7개를 recoverable archive로 이동
- [x] gingoa-specific H2 33개와 `gingoa_applied` metadata를 `legacy/judgments/`로 분리
- [x] inherited `status: verified` 50개를 `review-needed`로 하향
- [x] gingoa-specific guide/lifecycle/tier-ledger/schema/taxonomy를 active evidence surface에서 분리
- [x] claim/evidence/freshness 중심 schema와 source registry 도입
- [x] ISO/IEC/IEEE 12207:2017이 폐기되고 ISO/IEC/IEEE 12207:2026으로 대체됐음을
  [ISO 공식 catalog](https://www.iso.org/standard/90219.html)에서 확인

(P0 연구 단위의 현재 상태는 [`../audit/GAPS.ko.md`](../audit/GAPS.ko.md)만이 권위 있다.)

Full recovery snapshot:
`.scratch/research/archive/2026-08-02/pre-curation-snapshot.tar.gz`
(`sha256:85e64e38b1977a8d9e47bd7eaf25fb9e9b2d14c072a3e9d0a1cf462bac0a090f`).

## facts(06–16) → 실제 편입 위치

| 원 파일 | 현재 경로 |
|---|---|
| 06 | `aspects/28-implementation-process-workflow/facts-2026-08-sdlc-models.md` |
| 07 | `aspects/01-requirements-planning/facts-2026-08-requirements.md` |
| 08 | `aspects/02-architecture-design/facts-2026-08-design-practice.md` |
| 09 | `aspects/07-construction-code-review/facts-2026-08-codereview.md` |
| 10 | `aspects/08-software-testing/facts-2026-08-testing.md` |
| 11 | `aspects/04-build-ci-engineering/facts-2026-08-cicd-release.md` |
| 12 | `aspects/20-operations-incident-reliability/facts-2026-08-operations-sre.md` |
| 13 | `aspects/28-implementation-process-workflow/facts-2026-08-agile-adoption.md` |
| 14 | `aspects/09-application-security/facts-2026-08-security-sdlc.md` |
| 15 | `aspects/01-requirements-planning/facts-2026-08-estimation-failure-data.md` |
| 16 | `aspects/24-governance-collaboration-compliance/facts-2026-08-roles-teams.md` |
| 17 | `facts-2026-08-matrix.md` (corpus 루트) |
