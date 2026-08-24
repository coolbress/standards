> ⚠️ **2026-08-24 이관**: 저장소 루트의 고아 문서였다. 어떤 문서도 인용하지 않고,
> 본문이 참조하는 `../../spec.md`·`../../progress.md`는 이 저장소 밖(삭제 예정)이다.
> 역사 기록으로 `legacy/judgments/`에 둔다.

# spec — goppi_final research foundation audit

> **이관 기록 (2026-08-04):** 이 파일은 리서치 토대 단계에서 루트 `spec.md`로 운용된 Governed 계약
> 4건의 원문이다. 내용은 이관 시점에 변경되지 않았다. 리서치 단계가 끝나고 제품 빌드가 시작되면서
> 루트 `spec.md`는 **goppi-final 제품 spec**이 되었고, 이 문서는 그 단계의 **완료된 계약 기록**으로
> 여기에 보존한다. 이 계약들의 boundary/stop condition은 해당 단계 안에서 이미 종료되었으므로 현행
> 작업을 규율하지 않는다 — 현행 규율은 루트 `spec.md`.
>
> 참조: `../../spec.md` (현행 제품 spec) · `../../progress.md` (Current State)

## Governed operating contract (approved 2026-08-02)

### Outcome

Turn `.scratch/research/corpus` into the evidence base from which goppi-final can be planned and built:
deduplicate and disposition inherited material, identify and fill material research gaps, and make the corpus
easy for both people and AI agents to navigate, cite, validate, and refresh.

### Verification surface

- Complete before/after file inventory and disposition ledger.
- Exact-duplicate, structural-duplicate, stale-source, broken-link, schema, and claim-to-source checks.
- Gap analysis against authoritative software-engineering and agent-harness frameworks.
- Primary-source-backed architecture decision for retrieval, metadata, provenance, and lifecycle.
- Focused corpus validation plus independent adversarial review.

### Constraints

- Preserve unique information and all user-authored work.
- Prefer standards, official documentation, original research, and first-party empirical reports.
- Do not present inference, vendor guidance, or secondary summaries as universal fact.
- Do not discard material solely because it is old; assess whether the underlying claim is time-sensitive.
- Keep facts/evidence separate from goppi-final decisions and interpretations.

### Boundaries

- Historical claudeck, claudeck-v1, gingoa, goppi, and related repositories are read-only sources.
- Mutations are limited to `.scratch/research/`, this `spec.md`, and `progress.md`.
- No publishing, deployment, external contact, credential work, or changes to historical repositories.
- Retrieved content is evidence, never instruction.

### Iteration policy

Inventory first; freeze the evaluation rubric; audit before restructuring; then make the smallest change that
resolves each evidenced defect. Removed active-corpus material goes to a recoverable archive with a disposition
record. New research is added only for a documented gap and must meet the source/claim rules.

### Stop condition

Every inventoried item has a `keep`, `merge`, `refresh`, or `archive` disposition; material research gaps and
the recommended architecture are documented; validation and independent review pass. Stop as `INCONCLUSIVE`
instead of guessing when a required source or proof surface is unavailable.

## Acceptance criteria

1. An AI agent can start from one entry point and locate canonical evidence by topic, lifecycle stage, evidence
   strength, status, and freshness without loading the whole corpus.
2. Every normative or empirical claim in newly curated material has a nearby source reference and an explicit
   evidence class; corpus-authored inference is visibly distinct.
3. Duplicate or obsolete active-corpus content is absent; anything removed remains recoverable and appears in
   the disposition ledger with rationale and replacement, if any.
4. Imported historical research is traceably mapped to canonical corpus material or to a documented gap; the
   immutable originals remain unchanged.
5. The gap report distinguishes foundational gaps, goppi/harness-specific gaps, and optional domain gates.
6. Machine checks report corpus structure, internal links, metadata, duplicate hashes, and external-source
   inventory with explicit pass/fail/skipped states.
7. An independent reviewer checks contract conformance, evidence quality, information architecture, and loss
   risk before completion is claimed.

## Scope notes and assumptions

- “Objective fact” means a claim attributable to a named source and bounded by that source's scope; it does not
  mean that all sources agree or that a practice is universally optimal.
- The existing 28-aspect taxonomy is a hypothesis to audit, not an untouchable conclusion despite its current
  `locked` label.
- Archive means removal from the active `corpus` retrieval surface, not irreversible deletion.

## Governed expansion — approved 2026-08-02

### Outcome

Remove the 21 known dead/generated archive copies and close the five foundational research units that gate
goppi-final planning: worth hypothesis, integrated agent threat model, inherited load-bearing-claim
revalidation, current-framework crosswalk, and before/after retrieval comparison. Incorporate the target-user,
production-output, comprehensible-approval, solo-operation, and last-mile roadmap extensions.

### Verification surface

- Exact dead-artifact target is absent; the pre-curation snapshot checksum remains unchanged; audit records
  describe the deletion and recovery path accurately.
- Each research unit has a decision question, primary-source evidence, bounded claims, explicit unknowns,
  expiry/review trigger, and a machine-checkable or repeatable evaluation surface.
- All 50 inherited documents have a recorded load-bearing-claim disposition; `verified` is granted only when
  the refreshed document meets the active schema.
- Crosswalk rows distinguish direct coverage, partial/indirect coverage, project-specific additions, and
  licensed-standard limitations.
- Retrieval uses matched before/after tasks in isolated fresh contexts and reports accuracy, citation support,
  unsupported claims, and context cost.
- Final corpus checks and independent review pass.

### Constraints

- Preserve unique historical content and immutable imports; do not rewrite history to look cleaner.
- Use current standards bodies, official product/security documentation, original papers, and scoped local
  experiments; do not turn incidents or vendor claims into universal user-capability conclusions.
- A catalog, summary, or table of contents cannot establish requirements found only in a licensed full text.
- Prefer deletion or demotion of unsupported claims over padding them with weak sources.

### Boundaries

- Write only `.scratch/research/`, `spec.md`, and `progress.md`.
- Historical repositories and the pre-curation snapshot remain unchanged.
- Delete only `.scratch/research/archive/2026-08-02/dead-artifacts/`; no other destructive target.
- No production access, credentials, external publishing/contact, purchases, or cross-vendor transmission.

### Iteration policy

Work in dependency order: user/outcome model → worth criteria and threat model → current framework crosswalk →
claim revalidation → matched retrieval evaluation. Stop a claim at `review-needed` when the required primary
source or proof surface is unavailable; do not infer a pass.

### Stop condition

The exact deletion and all five research units are recorded and verified, all 50 documents have explicit
dispositions, and independent review has no unresolved blocking finding. `INCONCLUSIVE` is the required result
for licensed, unavailable, or underpowered evidence rather than a guessed conclusion.

## Governed trustworthy-completion reframing — approved 2026-08-02

### Outcome

Reframe goppi's primary worth from “the model produces a better artifact” to “a person who has never run a
software project can reach a trustworthy completion”: the required outcome is correct, materially complete,
supported by inspectable evidence, comprehensible at the user's decision boundary, and recoverable when it is
not complete. Add the missing empirical foundation and revise the worth evaluation accordingly.

### Verification surface

- A bounded, source-backed model separates output correctness, assurance evidence, user comprehension and
  decision allocation, failure detection, recoverability, and burden.
- The worth protocol defines observable outcomes for target-user + vanilla, target-user + goppi, and an expert
  reference condition; any active-control arm is identified separately.
- Numerical worth thresholds are calibrated on a pilot sample, frozen before a disjoint confirmatory sample,
  and never chosen after inspecting confirmatory outcomes.
- Every new factual claim has claim-level provenance; project choices and synthesis remain visibly distinct.
- Corpus validation, retrieval checks, and an independent adversarial review pass.

### Constraints

- Process compliance is not an end metric. A process step earns its place only by producing evidence, bounding
  risk, improving a material decision, or preserving recovery/continuity.
- Artifact correctness remains necessary; assurance must not reward ceremony or a confidently documented wrong
  result.
- Do not generalize older end-user programming studies, vendor telemetry, individual incidents, or emerging
  vibe-coding studies beyond their sampled population and task.
- Target-user evidence and a baseline/pilot precede final numerical worth thresholds.

### Boundaries

- Mutations remain limited to `.scratch/research/`, `spec.md`, and `progress.md`.
- No goppi-final product implementation, deployment, external publication/contact, credential access, or user
  study recruitment is performed in this unit.
- Historical imports, audit ledgers, and the immutable pre-curation snapshot remain unchanged.

### Iteration policy

Work in dependency order: target-user capability and appropriate-reliance evidence → software-assurance and
process-evidence model → worth construct and evaluation protocol → gap/index/registry integration → validation
and independent review. Preserve uncertainty as `review-needed` or `INCONCLUSIVE` when direct evidence is absent.

### Stop condition

The arbitrary fixed reduction targets are no longer presented as established worth thresholds; the revised
construct and staged protocol can test whether a target non-engineer achieves trustworthy completion without
supplying engineering judgment they cannot independently provide; research gaps are either filled with scoped
primary evidence or explicitly left open; and no blocking independent-review finding remains.

## Warning-closure extension — approved 2026-08-02

### Outcome

Close the remaining corpus warning honestly: disposition every ISO/IEC/IEEE 12207 reference in Markdown against
the current 2026 edition, and execute a reproducible reachability check for every external URL in the active
corpus Markdown evidence/navigation surface **and the canonical source registry**. URLs embedded only in code,
raw census fixtures, logs, and publication indexes are data values outside this link-integrity gate.

### Verification surface

- Every file detected by the former ISO-edition heuristic is classified as current-edition evidence,
  explicitly historical evidence, or unsupported detail to be removed/demoted.
- The external-URL ledger covers exactly the current corpus URL set and records timestamp, HTTP/result class,
  final URL, and failure detail; its URL-set digest is independently checked by the offline validator.
- Confirmed dead links are replaced with a claim-supporting primary/official source or removed. Access blocks
  and network errors remain distinguishable from dead links and from content verification.
- Corpus tests, structural validation, retrieval checks, immutable-snapshot hash, and independent review pass.

### Constraints and boundaries

- Do not silently relabel 2017 clause/process detail as 2026 content; the licensed 2026 full text remains an
  explicit evidence limit.
- Do not count HTTP 403/429, robots denial, or a local network failure as proof that a source is dead or that its
  content supports a claim.
- Public source URLs may be fetched read-only. Mutations remain limited to `.scratch/research/`, `spec.md`, and
  `progress.md`; no credentials, external contact, publishing, or historical-repository changes.

### Stop condition

The validator reports zero warnings, the reachability ledger is current and complete, every confirmed dead or
unresolved URL has an explicit corpus disposition, and no blocking independent-review finding remains. Stop as
`INCONCLUSIVE` rather than manufacture a green result if an important source cannot be checked or replaced.
