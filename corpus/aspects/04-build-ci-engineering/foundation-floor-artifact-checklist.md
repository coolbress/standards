---
id: aspect-04-build-ci-engineering--foundation-floor-artifact-checklist
title: "Foundation-floor artifact checklist (② bootstrap) + repo-context conditioning"
parent: aspect-04-build-ci-engineering
kind: research-log
evidence_track: census+lit
status: review-needed
last_updated: "2026-06-27"
method: "Independent canonical-checklist survey (2026-06-26; citation-accuracy pass 2026-06-27) of what a senior produces when bootstrapping a production-grade project — OpenSSF Scorecard + Best-Practices Badge + OSPS Baseline (level map) + SLSA v1.2 + 12-Factor + GitHub community-health + SWEBOK/ISO-12207. Built to GAP-AUDIT gingoa's ② output; grounds the ② FEATURE floor + the repo-context-conditioning rule."
---

# Foundation-floor artifact checklist (② bootstrap)

Why this exists: the ② foundation is scored by its **weakest** floor item, so the audit needs the *full*
senior-expected artifact set — including the unglamorous things juniors skip. This is the independent
reference (built without looking at gingoa first, to avoid blind-spot inheritance). Tags: **MUST** /
**REC** / **ARCH** (archetype-specific).

> **This doc is the canonical ② *output contract*** — the floor file **SET** (below) × its standard **locations**
> + **push** (§Location & push) × repo-context conditioning. Per-artifact **format** lives in each aspect's own
> standard (03/04/05/06/09/10/22/24/25). It is to ② what
> [`../01-requirements-planning/planning-document-family.md`](../01-requirements-planning/planning-document-family.md)
> is to ① — one entry point, detail by reference (no duplication).

## The checklist (grouped)

**VCS & repo hygiene** — `.gitignore` (MUST) · `.gitattributes` (REC) · `CODEOWNERS` (MUST for teams; routes
mandatory review — inert without branch protection) · branch protection on `main` (MUST; require PR +
status checks, no force-push) · signed commits (REC; SLSA **Source L2** = signed/protected history — a **v1.2** Source-track
level, not in v1.0) · no binary artifacts in tree (MUST) ·
Conventional-Commits + commitlint (REC).

**Build & dependency** — committed lockfile (MUST) · all deps version-pinned (MUST) · **GitHub Actions pinned
to commit SHA** (MUST; tags are mutable = supply-chain vector) · dependency-update bot — Dependabot/Renovate
(MUST) · single reproducible build entrypoint (MUST) · warnings-as-errors in CI (MUST).

**CI/CD** — CI on every PR + push (MUST) · lint + typecheck + test + build as separate required checks (MUST) ·
`permissions:` minimal/`read-all` per workflow (MUST; default token is write-broad) · no `pull_request_target`
with untrusted checkout (MUST) · OIDC cloud auth, no long-lived secrets (REC) · OpenSSF Scorecard action (REC).

**Code quality** — linter config committed (MUST) · formatter enforced in CI (MUST) · `.editorconfig` (REC) ·
**SAST in CI — CodeQL/Semgrep/Bandit** (MUST — *a deliberate above-OSPS-L1 harness uplift*: OSPS leans SAST at
**L3** (OSPS-VM-06.02) and OpenSSF Best-Practices treats it as pre-release, but gingoa keeps it in the floor **by
choice** — broken/insecure code reaching `main` is the weak link a non-engineer can't catch — **not** because a
leveled standard mandates it there) · pre-commit hooks (REC, helper not gate) · secret detection —
gitleaks/push-protection (MUST).

**Testing** — automated suite green in CI (MUST) · tests required on every PR (MUST) · written test policy in
CONTRIBUTING (MUST) · **walking skeleton** — one real end-to-end path (MUST; Cockburn) · coverage threshold
gate (REC) · mutation/property/fuzz (ARCH: security-critical).

**Security & supply-chain floor** — `SECURITY.md` disclosure policy (MUST) · Dependabot/OSV alerts (MUST) ·
secret-scanning + push-protection (MUST) · **SBOM file** SPDX/CycloneDX (REC→MUST under EO 14028/CRA) — *the
SBOM **file** is producible at ②* (a static dep-tree artifact; OSPS places SBOM-on-release at L3); only **signed
provenance / release-signing** is genuinely a ④ release-tier control · MFA for write access (MUST; OSPS-AC-01 L1) ·
no home-rolled/broken crypto (MUST) · vuln-response SLA, medium+ ≤60d (MUST) · SLSA **Build** L1 provenance → L2
signed (REC; v1.2 Build-track levels, unchanged from v1.0).

**Config & secrets** — config separated from code, no hardcoded env (MUST; 12-Factor III) · `.env.example`
committed, real `.env` ignored (MUST) · secrets from a manager at runtime (REC).

**Dev-env & onboarding** — README clone→install→test in ≤5 commands (MUST) · `devcontainer.json` (REC) ·
unified task runner — Make/package scripts (MUST) · runtime/tool pins — `.nvmrc`/`.tool-versions`/`engines`
(REC) · setup verified by a CI bootstrap step (REC).

**Docs baseline** — README (MUST) · CONTRIBUTING (MUST) · CHANGELOG (MUST; Keep a Changelog) · `docs/adr/`
decision records (REC) · auto-gen API/interface ref (MUST if public surface) · lightweight design/threat doc
(REC; OSPS L2) · **docs/content linting in CI** (REC — markdownlint/Vale/link-check) + a **de-jargon /
forbidden-internal-terms gate** (REC; MUST for a public/internal doc split — Vale `reject.txt` or a custom
grep job) → see [`../22-documentation-knowledge/content-ci-linting-and-jargon-gate.md`](../22-documentation-knowledge/content-ci-linting-and-jargon-gate.md).

**Governance & community** — OSI `LICENSE` (MUST) · `CODE_OF_CONDUCT.md` (REC; MUST for public community) ·
`SECURITY.md` (MUST) · `SUPPORT.md` (REC) · `GOVERNANCE.md` (REC) · PR template (MUST) · issue-form templates
+ `config.yml` (REC) · `FUNDING.yml` (ARCH: OSS).

**Release/versioning hygiene** — SemVer/CalVer documented (MUST) · git tags per release (MUST) · GitHub Release
+ human changelog (MUST) · signed release artifacts (MUST for public release). *(Full ④ set →
[`aspects/17-release-engineering`](../17-release-engineering/).)*

## Location & push (the contract's location + remote dimension)
- **Location:** standard paths — repo **root** (`README` · `LICENSE` · `SECURITY.md` · `CONTRIBUTING` · `CHANGELOG` ·
  `.gitignore`/`.gitattributes`/`.editorconfig` · toolchain configs) · **`.github/`** (`workflows/` · `dependabot.yml` ·
  `CODEOWNERS` · issue/PR templates) · **`docs/`** (`adr/` · design) · **`src/`** + **`tests/`**. Each aspect's
  standard owns the exact format.
- **Push:** the **entire floor is committed + pushed** — it IS the repo's build / security / governance
  infrastructure (no team keeps CI config or `SECURITY.md` local). The **same 2-axis publish standard as ①** applies
  ([`../01-requirements-planning/planning-document-family.md`](../01-requirements-planning/planning-document-family.md)
  §Publish-location): in-repo + pushed; *public vs private = is the project open-source?*. **Local-only exceptions:**
  the **threat-model** (publishing aids attackers) + the **research corpus** (internal IP) — nothing else.
- **Enablement conditioning:** *which* controls are **active** at private-free vs public (Semgrep→CodeQL, Scorecard
  `publish_results`, branch-protection / 2-person-review flip on going public) is the
  [`visibility-provision-matrix.md`](visibility-provision-matrix.md). Push ≠ enablement: the *files* are always
  pushed; the *flip list* gates which checks turn on when the repo goes public.

## Most-commonly-missed (junior-skips, senior-flags)
SHA-pinned Actions (not tags) · per-workflow least-priv `permissions:` · lockfile present but CI uses
`install` not `ci`/`--frozen` · no `SECURITY.md` · secret-scanning/push-protection off · "protected" branch
whose required checks aren't wired to real jobs · **no walking skeleton** · missing `.env.example` ·
`CODEOWNERS` after enabling owner-review (→ unmergeable) · **no ADRs** · Dependabot configured but alerts
dismissed without PRs · no coverage gate (3% "passes").

## OSPS Baseline level map (grounds the conditioning below)
The repo-context conditioning that follows isn't re-derived — it maps onto the **OpenSSF OSPS Baseline**'s named
leveling (**~41 controls × 3 maturity levels × 6 lifecycle categories**). The levels are project-context tiers,
which is exactly the conditioning axis: `[lit]`
- **L1 — universal floor** (any project, any maintainer/user count): the basics every repo owes regardless of
  size. Load-bearing placements: **branch-protection** (OSPS-AC-03.01) · **MFA for write/admin access**
  (OSPS-AC-01.01).
- **L2 — 2+ maintainers + a small consistent user base:** **signed releases** (OSPS-BR-06.01) · **CI runs ≥1
  automated test suite before a commit is accepted** (OSPS-QA-06.01).
- **L3 — large, widely-adopted user base:** **non-author / two-person review on the primary branch**
  (OSPS-QA-07.01) · **SAST blocking on policy violation** (OSPS-VM-06.02) · **SBOM delivered with each release**
  (OSPS-QA-02.02).

This is what makes the deferrals below *principled*: a solo/private/free-plan repo legitimately sits at **L1**,
so deferring the L3 controls (mandatory non-author review, leveled SAST, release-SBOM) is the standard's *own*
leveling, not a gap — while gingoa still chooses to pull SAST and an SBOM **file** down into its floor as a
deliberate above-L1 uplift (see the SAST/SBOM notes above).

## Repo-context conditioning (the key audit lesson — 2026-06-26)
A *generic, public-repo/team* checklist **over-flags** for a real project's context. "MUST" is conditional on
three axes; condition before calling something a gap:
- **visibility (public vs private):** **CodeQL code-scanning** and some GitHub security features need **GitHub
  Advanced Security** on a *private* repo (paid) → on a private free-plan repo, do SAST with **Semgrep OSS**
  (plain CLI, no GHAS) instead; CodeQL becomes the choice when the repo goes public. **Branch protection**
  returns 403 on a private free plan → launch-deferral. **Dependabot npm** on a private repo auto-routes to
  GitHub Packages (no public-registry mirror, can't scope without a token) → defer to public, or use Renovate;
  `pnpm audit` is the compensating CVE gate.
- **plan (free vs paid/GHAS):** several "MUST"s are GHAS/paid-gated as above.
- **team size (solo vs team):** `CODEOWNERS`, mandatory multi-reviewer, GOVERNANCE are team-load-bearing; a
  solo repo legitimately defers them (still cheap to add as launch-ready).
**Rule:** a context-blocked floor item is a **documented, condition-bound deferral with a compensating
control**, not a silent gap — and not an oversight to "fix" by force-adding a thing that can't run. (This is
the inverse of *presence≠adequacy*: here *absence* can be adequacy, given context.) Product implication for
the ② FEATURE: emit **Semgrep for private** / **CodeQL for public** projects; gate branch-protection and
Dependabot-npm on visibility.

## gingoa application (dogfood)
gingoa's own repo (private, free plan, solo) had every context-*possible* floor item except **SAST** — a genuine
omission (never considered), closed 2026-06-26 with a Semgrep OSS job (`security.yml`, verified 0 findings) +
a launch-ready `CODEOWNERS`. The others my audit first flagged (Dependabot-npm, branch protection, coverage
gate, CODEOWNERS-as-enforced) are **conscious documented deferrals** (extracted to a launch-tracking issue when the foundation doc was retired), almost all
private-free-plan-gated — not misses.

## Sources
OpenSSF Scorecard checks (~20, incl. SBOM + Webhooks) https://github.com/ossf/scorecard/blob/main/docs/checks.md ·
OpenSSF Best Practices Badge https://www.bestpractices.dev/en/criteria/0 · OSPS Baseline (3 levels; 통제 수는 **FFA-005 충돌 등재** — `~41` 은 현행과 맞지 않는다;
level map above) — **현행 핀**(2026-08-26 갱신 · 이전 핀 `2025-02-25` 는 두 판 뒤였다 · FFA-004): https://baseline.openssf.org/versions/2026-02-19.html ·
SLSA v1.2 Build track https://slsa.dev/spec/v1.2/build-track-basics · SLSA v1.2 Source track (new in v1.2)
https://slsa.dev/spec/v1.2/source-requirements · 12-Factor https://12factor.net/ · GitHub community health files
https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file ·
GitHub protected branches https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches ·
CodeQL on private repos needs GHAS https://docs.github.com/en/code-security/code-scanning/introduction-to-code-scanning/about-code-scanning ·
Semgrep OSS https://semgrep.dev/docs/ · SWEBOK v4 https://ieeecs-media.computer.org/media/education/swebok/swebok-v4.pdf ·
ISO/IEC/IEEE 12207:2026 https://www.iso.org/standard/90219.html · Dev Containers https://containers.dev/

## Claim table — 외부 표준 인용 검증 (`05` 재검증 배치 1 · 1차 출처 직접 확인 2026-08-26)

이 문서는 [`direction/05`](../../../direction/05-the-output-floor.md) 의 **MUST 45 전부**를 떠받친다
(그 바닥이 인용하는 코퍼스 문서는 **이것 하나뿐**이다). 그런데 이 문서의 처분은
[`CLAIM-REVALIDATION`](../../../audit/CLAIM-REVALIDATION.ko.md) **C50-14 `RETAIN-RN/SYNTHESIS` · *"파일 presence≠adequacy"*** 다.
→ **여기가 인용한 외부 표준의 레벨 주장부터 1차 출처로 확인한다.** 반증 가능한 것이기 때문이다.

| Claim ID | Class | Claim and scope | Evidence | Confidence | 재검증 |
|---|---|---|---|---|---|
| FFA-001 | normative | ✅ **SAST 가 OSPS L3 라는 것은 맞다.** `OSPS-VM-06.02`: *"While active, all changes to the project's codebase MUST be automatically evaluated against a documented policy for security weaknesses and blocked…"* · **Maturity Level 3 only**. → 이 바닥이 SAST 를 MUST 로 두는 것은 **표준보다 위**이고, 이 문서가 그것을 *"by choice"* 라 밝힌 것은 **정확하다** | `OSPS-BASELINE-2026-02-19` | high | 2026-08-26 |
| FFA-002 | normative | ✅ **SBOM-on-release 가 L3 라는 것도 맞다.** `OSPS-QA-02.02`: *"When the project has made a release, all compiled released software assets MUST be delivered with a software bill of materials."* · **L3** | `OSPS-BASELINE-2026-02-19` | high | 2026-08-26 |
| FFA-003 | normative | ⚠️ **MFA 는 L1 이 맞으나 범위가 다르다.** `OSPS-AC-01.01` 은 L1·2·3 전부에 적용되지만, 원문은 *"read or **modify** a **sensitive resource** in the project's **authoritative repository**"* 다. 이 문서가 적은 *"MFA for **write access**"* 는 **읽기를 빼고 대상을 넓힌** 표현이다 — 방향은 맞고 **경계가 다르다** | `OSPS-BASELINE-2026-02-19` | high | 2026-08-26 **범위 정정** |
| FFA-004 | vendor-behavior | 🔴 **버전 핀이 낡았다 — 두 판 뒤처졌다.** 이 문서는 OSPS Baseline 을 **`2025-02-25`** 로 핀했는데 현행은 **`v2026.02.19`** 이고 그 사이 **`v2025.10.10`** 이 있었다. OSPS 사이트가 직접 *"Only the version labeled as **'current'** should be used for new compliance efforts"* 라 한다. ✅ **다만 위 세 레벨 배정은 현행에서도 그대로다** — **결론은 무너지지 않았고 핀만 낡았다** | `OSPS-BASELINE-2026-02-19` | high | 2026-08-26 **신규** |
| FFA-005 | synthesis | ⚠️ **통제 수 *"~41 controls"* 는 현행과 맞지 않고, 검증자가 갈렸다.** 현행 판을 센 결과가 **64**(L1 24 + L2 19 + L3 21, `Controls Overview` 항목 계수) vs **80**(카테고리 9개에 걸친 requirement 계수)로 **둘이 어긋난다.** 절차 §5 대로 **결론을 내지 않고 충돌로 등재**한다. ⚠️ **다만 *"~41 이 아니다"* 는 두 검증자가 일치**한다 (parent control 과 numbered requirement 를 다르게 셌을 가능성이 남는다) | `OSPS-BASELINE-2026-02-19` | low (충돌) | 2026-08-26 **충돌 등재** |
| FFA-006 | normative | 🔴 **SLSA Source L2 인용이 원문과 다르다.** 이 문서는 *"signed commits (REC; SLSA **Source L2 = signed**/protected history)"* 라 적어 **커밋 서명**을 정당화한다. 원문은 서명을 말하지 않는다 — *"Branch history is **continuous, immutable, and retained**, and the SCS issues **Source Provenance Attestations** for each new Source Revision."* **연속성·불변성·출처증명이지 서명이 아니다.** → 서명 권고의 근거로 Source L2 를 쓰지 않는다 | `SLSA-V12-SOURCE` | high | 2026-08-26 **인용 정정** |

| FFA-007 | vendor-behavior | ✅ **Scorecard 인용은 맞다.** 체크 목록에 **`SBOM`** 과 **`Webhooks`** 가 실제로 있고(각각 SBOM 문서 보유 · 웹훅 토큰 인증 확인), 총 개수도 *"~20"* 수준이다(열거 20종: Binary-Artifacts · Branch-Protection · CI-Tests · CII-Best-Practices · Code-Review · Contributors · Dangerous-Workflow · Dependency-Update-Tool · Fuzzing · License · Maintained · Packaging · Pinned-Dependencies · SAST · SBOM · Security-Policy · Signed-Releases · Token-Permissions · Vulnerabilities · Webhooks) | `SCORECARD-CHECKS` | medium-high | 2026-08-26 |
| FFA-008 | vendor-behavior | 🔴 ***"CodeQL on private repos needs GHAS"* — 사실은 맞고 제품명이 낡았다.** GitHub 현행 문서: *"If you want to use code scanning on private repositories, you need a **GitHub Code Security license**."* **GHAS 가 아니라 `GitHub Code Security`** 다(제품이 갈렸다). ⚠️ **함의**: 비공개 저장소에서는 **Pro 만으로 SAST MUST 를 CodeQL 로 채울 수 없다** — 별도 유료 제품이 필요하다. 대안은 이 문서가 이미 든 **Semgrep OSS** 다. 🟢 **다만 지금 깨진 것은 없다** — `ruleset.json` 이 요구하는 것은 `ci / lint`·`typecheck`·`test`·`build` **4개뿐**이고 **SAST 는 아직 벽에 없다**(만들 것 ⑫ 미착수). **⑫ 를 지을 때 지켜야 할 제약**으로 등재한다 | `GITHUB-CODE-SCANNING` | high | 2026-08-26 **신규** |

> **배치 1 의 결론 — 레벨 주장은 살아남았고, 낡은 것은 핀과 인용이다.**
> SAST L3 · SBOM L3 · MFA L1 **세 건 다 현행 표준에서 확인**됐고 두 검증자가 일치했다.
> 무너진 것은 ⓐ **버전 핀**(두 판 뒤처짐) ⓑ **통제 수**(~41 은 아니다 · 정확한 값은 충돌)
> ⓒ **SLSA Source L2 를 서명으로 읽은 것**(원문은 연속성·불변성·출처증명이다).
>
> **배치 1~5 와 같은 형태가 또 나왔다** — *결론은 맞고 인용이 틀렸다.* 다만 여기서는 **하나가 더 있다**:
> **외부 표준은 갱신된다.** 리서치 인용은 논문이 안 변해서 한 번 맞으면 유지되지만,
> **레벨 표준은 판이 바뀌므로 핀에 만료가 붙어야 한다.**

**재검증 기록 (`05` 배치 2 · 나머지 인용)** — 검증일 `2026-08-26` · 검증자 `Claude Opus 5` · **판정: 유지 1(Scorecard) · 신규 1(CodeQL 제품명 변경 + ⑫ 제약)** · **OSPS 핀을 `2026-02-19` 로 올렸다**(FFA-004 처분) · 절차 [`reverification-protocol`](../../methods/reverification-protocol.md)

**재검증 기록 (`05` 배치 1)** — 검증일 `2026-08-26` · 검증자 `Claude Opus 5` + `codex-cli 0.145.0`(독립 질의, 결론 비공개) · **판정: 유지 2 · 범위 정정 1 · 인용 정정 1 · 신규(핀 노후) 1 · 충돌 등재 1** · ⚠️ **불일치 1건**(통제 수 64 vs 80 — 결론 내지 않고 등재) · 절차 [`reverification-protocol`](../../methods/reverification-protocol.md)
