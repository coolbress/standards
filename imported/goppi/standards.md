# standards — where goppi's scaffold sits, and the professional bar it targets

<!-- snapshot-date: 2026-07-17 — Part B (the competitive landscape) is a dated
     snapshot and rots fast; re-verify before relying on it. Part A (the
     standards-derived bar) is slow-moving. See "Expiry conditions". -->

On-demand context for *why* goppi's `scaffold` skill is shaped the way it is:
what the professional bar actually is (from standards), and what the rest of the
field does and doesn't do (from a dated survey). This is **positioning +
justification knowledge**, not part of the floor itself — the floor is
`production-floor.md`. Every load-bearing claim here was verified against a
primary source on the snapshot date; claims that could not be pinned were
dropped or explicitly softened (see Evidence).

Two parts with **different shelf lives**, kept separate on purpose:
- **Part A — the professional inception bar**: standards-grounded, slow-moving,
  durable. This is the external justification for the floor.
- **Part B — the competitive landscape**: a survey snapshot, dated, expires fast.
  Read it as "true as of 2026-07-17," never as timeless.

---

## Part A — The professional inception bar (durable; standards-grounded)

What senior engineers and industry standards define as the minimum professional
setup for a serious project — and, crucially, what is genuinely universal vs.
what scales to risk (so goppi does not over-scaffold).

### The near-universal core (primary-sourced) — and where goppi's floor gates it

Two caveats up front, so this does not contradict goppi's own risk-gated floor:
(a) several of these are **OpenSSF Badge** MUSTs, which is an **OSS/public** bar —
not literally "every local script"; (b) goppi's floor keeps the same items but
**gates two by risk** — LICENSE by *exposure* and CI by *correctness/frequency*
(see the risk-tiering rule below and `references/production-floor.md`). The floor is
a risk-gated *refinement* of this list, not a flat copy.

1. **Version control from commit one** — one codebase in a VCS. [lit] 12-Factor
   Factor I ("a twelve-factor app is *always* tracked in a version control
   system"); DORA *version control*; NIST SSDF **PS.1** (protect all forms of code).
2. **Explicit dependencies + a committed lockfile** — deps declared in a manifest,
   lockfile committed for identical/reproducible trees. [lit] 12-Factor Factor II;
   npm docs (package-lock.json "is intended to be committed"). *(goppi's floor was
   tightened to match this (v2, 2026-07-17): "commit the lockfile whenever a package
   manager produces one" — skipped only when there is genuinely no package manager
   to pin, e.g. goppi itself.)*
3. **Config & secrets out of code, in the environment** — pass the litmus test:
   "could be made open source at any moment without compromising credentials."
   [lit] 12-Factor Factor III; OpenSSF Badge `no_leaked_credentials` (MUST NOT).
4. **A README / basic docs** (universal) **+ a LICENSE** (*exposure-gated* — a public
   repo needs one; a private local project can defer it). [lit] OpenSSF Badge
   `documentation_basics` (MUST), `floss_license` + `license_location` (MUST *for the
   OSS badge*, standard location in-repo).
5. **A runnable verification of the main claim** (universal) — an *automated test in
   CI* is its *correctness/shared/frequency-gated* form; the floor's `verify` allows a
   documented procedure for exploratory/non-executable work and escalates to CI when
   correctness matters or the code is shared. [lit] OpenSSF Badge `test` (MUST *for the
   badge*); DORA *test automation* + *continuous integration*; NIST SSDF **PW.8** (test
   executable code); Scorecard **CI-Tests**.

### The risk-tiering rule (everything else scales — it is not uniform)

The standards themselves are tiered, not flat checklists. **Process rigor tracks
reversibility × blast-radius × exposure, not project size.**

- **SLSA** (v1.2, approved 2025-11-24) is an explicit ladder: Build **L0** = no
  guarantees (dev/test); **L1** = provenance exists but forgeable; **L2** = signed
  provenance on a hosted platform (forging "requires an explicit attack"); **L3** =
  hardened/isolated, non-falsifiable. Levels are chosen by adversary capability. [lit]
- **OpenSSF Scorecard** is an advisory risk-weighted average (Critical 10 / High
  7.5 / Medium 5 / Low 2.5; each check 0–10) — "an inherently opinionated process…
  consumers may value some heuristics more than others based on their own risk
  tolerance." [lit]
- **OpenSSF Best Practices Badge** is cumulative Passing → Silver → Gold; even
  within Passing it tiers (static analysis MUST, dynamic analysis only SUGGESTED). [lit]
- **NIST SSDF** (SP 800-218 v1.1, Feb 2022) is outcome-based and explicitly
  risk-based: "Not all practices are applicable to all use cases; organizations
  should adopt a risk-based approach to determine what practices are relevant,
  appropriate, and effective." [lit]
- **The decision-theoretic anchor**: Bezos Type-1 (irreversible "one-way door" →
  slow, careful) vs Type-2 (reversible "two-way door" → fast, low-ceremony); the
  named failure mode is applying the heavyweight process to reversible decisions. [lit]

**What scales, and its trigger** (matches goppi's deferral model):
- **Public exposure** → SECURITY, CONTRIBUTING, CODE_OF_CONDUCT (GitHub's
  "community profile" is *explicitly scoped to public repos*; a CoC presupposes a
  community). [lit]
- **>1 committer** → branch protection / required review, CODEOWNERS (these
  enforce a *coordination* process — waste until coordination can break). [lit]
- **Shipping artifacts others depend on** → signed/reproducible builds, provenance
  (SLSA L2→L3), SBOM, pinned-by-hash deps; release integrity + archival (SSDF
  PS.2/PS.3). [lit]

### The trust/observability bar (for consequential outputs)

When a project produces numbers a decision rests on, the bar shifts from "does it
run" to **"can a third party independently reproduce it"**: pinned dependencies +
versioned inputs + a test suite trustworthy enough to gate release (DORA: "when
tests pass we should be confident the software is releasable") + a provenance/audit
record of exactly what produced the result (SLSA provenance; SSDF PS.2/PS.3). A
test suite nobody trusts to gate a release is cargo-cult, not evidence. [lit]

**How the floor maps to this** — goppi's floor is not ad-hoc: its 6 objectives
cover the universal core; its gating axes are the risk-tiering rule; its
domain-activation note is the trust/observability bar. Part A is the external
justification that the floor is standards-aligned, not invented.

### The documentation bar (audience-scaled)

Docs are part of the professional bar, and they scale to **audience, not project
size** (Write the Docs: "give users the information they need, but not too much").
The de-facto structure standard is **Diátaxis** (orig. Divio "documentation
system", D. Procida, 2017; renamed ~2020) — four audience-need types, each with a
distinct writing orientation: **Tutorials** (learning), **How-to guides** (task),
**Reference** (facts), **Explanation** (understanding). Adopted by Django,
Cloudflare, Canonical. The audience ladder:

- **Any shared repo** → README (root; makeareadme / standard-readme) + LICENSE.
- **Versioned / released** → CHANGELOG (keepachangelog 1.1.0) + SemVer 2.0.0.
- **Accepts contributions** → CONTRIBUTING.
- **Has external users / learners** → the Diátaxis `docs/` set — *omitting any
  quadrant whose audience doesn't exist yet* (a tool with users but no beginners
  needs How-to + Reference, not Tutorials). Templates: The Good Docs Project.

*Honest counter (Hillel Wayne):* the 4-doc model is **not universal** — designed
for *tools*, weaker for frameworks/languages, misses concept-overviews/snippets,
and is over-applied. So the floor gates docs on audience and does not force the
quadrants onto a shape they were not built for. (goppi's own docs sit at the
low rungs — README + design doc + ADRs — because it is a pre-public harness with
no external users; full Diátaxis is deferred until it has them.)

### The anti-over-scaffolding view (why goppi's ceiling on ceremony is correct)

Experienced engineers treat premature ceremony as a *net cost*, not a safety
margin: Fowler's YAGNI ("cost of carry" — presumptive features tax every later
change); Knuth's actual quote is a risk-tiering statement ("forget small
efficiencies… about 97% of the time; yet… the critical 3%"); McKinley's
"innovation tokens" / choose-boring-technology; over-engineering as a named
anti-pattern; cargo-cult process (adopting the form without the substance). This
is the literature behind goppi refusing to gold-plate a throwaway. [lit]

---

## Part B — The competitive landscape (SNAPSHOT as of 2026-07-17; expires fast)

Who else does "an agent sets up your project," and what they do and don't do.
**Dated. Fast-rotting** (CRA sunset 2025-02; Windsurf acquired by Cognition
2025-07; Tessl pivoted 2026-01). Re-verify before relying on any specific.

### The field splits into three camps — none occupies goppi's quadrant

- **SDD pipelines** (GitHub Spec-Kit, AWS Kiro, BMAD-METHOD, Tessl): elicit
  **functional/product** intent via fixed templates/slash-commands; most apply the
  same ceremony regardless of stakes; scaffold **spec/story/test artifacts, ~zero
  repo hygiene** (no CI/LICENSE/SECURITY/governance by default). Category's #1
  criticism is "**waterfall in markdown**" (Scott Logic: 2,577 lines of markdown
  for 689 of code; Fowler: a bug fix blown into 16 acceptance criteria). [survey]
- **IDE / agent-memory tools** (Cursor, Windsurf/Devin, Claude Code `/init`, Aider,
  Codex/AGENTS.md): **brownfield-first, non-destructive** (real strength =
  codebase indexing); produce **unenforced markdown instruction files, no
  professional baseline, no risk-scaling**. #1 criticism: "rules silently ignored"
  (Anthropic concedes "no guarantee of strict compliance"). [survey]
- **App builders** (Replit, Lovable, Bolt): generate runnable **greenfield** code
  but **skip tests/CI/security/governance** so consistently they are the canonical
  vibe-coding cautionary tales (Replit deleted a production DB; scans of
  vibe-coded apps found thousands of vulns / exposed secrets). [survey]

### The empty quadrant (falsifiable, precisely worded)

> **As of 2026-07-17, no publicly-available, documented tool does all three by
> default: (a) an opening interview framed as *engineering risk* — exposure
> (public/private), collaboration (solo/contributors), consequence (throwaway/
> decision-grade); (b) risk-scales the amount of process to those stakes; and
> (c) provisions the boring professional baseline (VCS, tests, CI, .gitignore,
> context-appropriate LICENSE/SECURITY/governance) by default.**

**Precision — one tool contests a loose reading.** **BMAD-METHOD** genuinely does
(a-ish)+(b): it interviews *and* scale-adapts ceremony (Levels 0–4, bug-fix →
enterprise). But its interview is **product-intent + complexity, not
exposure/collaboration/consequence**, and it lays **zero repo baseline** (planning
docs only). So do **not** claim "no tool interviews or scales ceremony" — that is
false. The true, tight claim is the two things nobody does: **frame the interview
as engineering risk AND risk-scale the professional baseline itself.**

Partial-overlap map: (a)+(b) missing (c) = BMAD. (c) alone = Backstage/Port/Cortex
golden paths, Kiro's init-prompt (opt-in, template not interview). (a) alone =
Tessl, Spec-Kit `/clarify`. **No tool pairs (a)+(c) meaningfully.** [survey]

### The brownfield-update / no-drift maturity axis

The property that separates **platform-grade** scaffolding from **one-shot**
starters is **a first-class, supported path to propagate later template/standard
evolution into already-generated projects** — via one of three mechanisms:
- **merge-based re-apply** — `copier update` (git 3-way merge vs `.copier-answers.yml`
  `_commit`; user edits survive; inline-conflict default since **v8.0.0**,
  2023-06-04) and **cruft** for Cookiecutter (`.cruft.json` + template commit hash).
- **regenerate-from-code** — **Projen** (`.projenrc` is truth; re-synthesize;
  managed files owned/read-only, anti-tamper CI check). Reaches no-drift by
  *owning* the generated surface, not by merging.
- **versioned migration runners** — **Nx** `nx migrate` → `migrations.json` →
  `--run-migrations` (rewrites existing config/code; Angular `ng update` lineage).

**One-shot** (emit once, keep no memory of the template): **Backstage Scaffolder**
(update feature request #14416 closed NOT_PLANNED 2023-01-10), **Cookiecutter core**
(update requested since 2013 #55, never implemented in core; still-open successors
through #2119, 2024), **Yeoman** (re-run does file-level overwrite prompts, no
versioned template merge), **cargo-generate** (#291 open RFC),
**create-next-app/CRA/Vite** (framework codemods transform *your code* for API
changes ≠ re-applying the starter template). [survey]

Note the nuance: "**without clobbering user work**" is precisely true only for
copier/cruft (3-way merge). Projen forbids hand-edits to owned files; Nx edits in
place and asks you to review. The uniform property is "a supported update path
exists at all," not a single mechanism.

### Where goppi sits

- **Occupies the empty quadrant** — risk-framed interview + risk-scaled baseline
  by default + non-destructive brownfield adopt. Independent surveys describe this
  quadrant as unoccupied; goppi's design targets it directly. Concept validated,
  not maturity.
- **Weakest exactly on the decisive maturity axis** — brownfield *update*. goppi
  has the *design* (.goppi-setup.md = the answers file, `floor-version` = the template
  ref, propose-the-delta = the re-apply) — structurally the copier/cruft model —
  and it is now **built and machine-enforced** (floor-version stale-detection in
  `floor-accounting`) and **validated once** (a fresh agent ran the update path
  end-to-end) — though not fleet-hardened like copier; goppi explicitly disclaims a
  persisted ratchet. On the axis pros rank as decisive, goppi is "right design,
  built + n=1-validated."
- **Shares the memory-tool limitation** — advisory markdown, not enforced;
  correctness depends on model compliance (mitigated by Layer-2 hooks + accounting,
  but real — the A/B eval caught goppi's own output citing a checker it hadn't run).

**Senior verdict**: the philosophy, position, and risk model are correct and ahead
of the field — goppi does set up projects the professional way, scaled to need.
Calling it a *mature* system is premature until (1) the brownfield-update path is
built and validated and (2) evidence goes past n=1.

### Keeping this snapshot current — discovery feeds (census, not standards)

Part B rots fast, so it needs a *discovery* channel that surfaces newly-trending
harnesses / agent tools before this snapshot goes stale. One such feed is the
**AI Repo Radar** ([ai-repo-radar-1u7.pages.dev](https://ai-repo-radar-1u7.pages.dev/)) —
a Korean daily trend-tracker of AI OSS by category (MCP / Agent / RAG / Eval /
Framework / …) ranked by a custom "practical score." Treat it strictly as
**`[census]` discovery**: it answers *"what is prevalent / worth investigating,"*
NOT *"what is correct."* Its methodology, data source, and authorship are
undisclosed and it is individually curated — so it is a **signal to look, never
evidence of a standard**. Anything found through it earns a place in goppi's floor
only after passing the Part A / primary-source bar. This is the same discipline the
`[census]` tag enforces everywhere: **prevalence ≠ necessity**.

## Evidence
- [lit] Professional-bar standards, all verified against primary sources on
  2026-07-17: OpenSSF Scorecard (weights Critical 10/High 7.5/Med 5/Low 2.5, check
  names) and Best Practices Badge (cumulative Passing→Silver→Gold; criterion names
  `floss_license`/`license_location`/`documentation_basics`/`test`/`no_leaked_credentials`;
  static MUST / dynamic SUGGESTED); NIST SSDF SP 800-218 **v1.1** (Feb 2022; the
  authoritative final — v1.2 is draft only) risk-based/outcome-based wording +
  PS.1/PW.8/PS.2/PS.3/RV.3; SLSA **v1.2** (approved 2025-11-24; Build L0–L3
  unchanged from v1.0/1.1, adds a Source Track); 12-Factor I/II/III; DORA
  capabilities; npm package-lock ("intended to be committed"). *Interpretation not
  in the source, flagged as ours*: the "internal→L2 / external→L3" mapping (SLSA
  frames by adversary capability and targets L3 for "most releases"); the
  "solo dev doesn't need branch protection" line (practitioner blog, directional).
- [survey] Competitive landscape — a **dated web survey** (2026-07-17), three
  research passes + one adversarial verification pass that tried to *refute* the
  empty-quadrant claim. Load-bearing brownfield-update facts pinned to primary
  docs/issues with dates (copier v8.0.0 changelog; Nx migrate docs; projen source
  on `main`; cruft; Backstage #14416; cookiecutter #55/#2119; cargo-generate #291;
  CRA sunset 2025-02-14). **Corrections applied during hardening** (would otherwise
  have been errors): copier inline-default is v8.0.0 not "6.0"; Projen Dependabot is
  OFF by default (depsUpgrade is the on-by-default upgrader); Backstage FTE/$ figures
  are vendor-reported (Roadie/Port) → dropped as fact; cookiecutter #55 is
  closed/completed not "open"; SLSA version corrected v1.0→v1.2.
- [inferred] goppi's own positioning (occupies quadrant / weakest on update /
  advisory-markdown limit) — synthesis over the above + the 2026-07-17 A/B eval;
  not independently externally reviewed.
- [census] Discovery feed — **AI Repo Radar** (ai-repo-radar-1u7.pages.dev, checked
  2026-07-20): a daily AI-OSS trend tracker by category with a custom "practical
  score"; methodology / data source / authorship undisclosed, individually curated.
  Used only to keep Part B current (surface trending harnesses to investigate) — NOT
  a standard. **Reliability caveat (measured):** its star counts are not credible —
  repos created in early 2026 show 80k–230k stars weeks later — so treat it as a
  *directional map of tool categories*, not a ranking. **First scan (2026-07-20,
  N=4,538 repos): no actionable gap for goppi** — the field's loudest themes (memory,
  skill-registries, orchestration, runtime eval/observability, token proxies) are
  goppi's declared non-goals or already on its roadmap (`harness-eval` / `review`),
  and several trending "laziest-senior / best-practice-floor" repos independently
  converge on goppi's own thin thesis. One item was logged and **closed via primary
  source** (2026-07-20): spec-kit's `/analyze` runs six cross-artifact passes
  (duplication / ambiguity / underspecification / constitution-alignment /
  coverage-gaps / inconsistency) over a **three-file split** (`spec.md` + `plan.md` +
  `tasks.md`) with structured requirement/task IDs. goppi's `spec-accounting.sh`
  already machine-checks the *mechanizable floor* of these (unresolved
  `{{placeholder}}`, filled deliverable/verification/scope rows, ≥1 acceptance box,
  ceremony cap); the deeper coverage/consistency passes presuppose spec-kit's
  structured 3-artifact model, which goppi deliberately does not adopt — that
  fixed-gate model is precisely the "waterfall in markdown" §3.1 rejects. **No build
  change; confirmed not a gap.** Prevalence ≠ necessity; nothing here changed goppi's build.

## Expiry conditions
- **Part B (the survey) is time-boxed** — treat as stale after ~6 months (by
  ~2027-Q1, from the 2026-07 snapshot) or immediately when a named tool ships the
  missing leg. Re-run the
  adversarial "find a tool that does all three" pass before citing the empty-quadrant
  claim again. The claim dies the day any tool risk-frames its interview AND
  risk-scales the baseline by default (BMAD adding a repo baseline + exposure axis
  would be the most likely refuter).
- **The brownfield-update section expires when goppi builds its own update path** —
  then goppi moves from "one-shot-only" to the mature set, and this section must be
  rewritten to reflect that (and to stop citing goppi as weakest there).
- **Part A (standards) is durable but versioned** — re-check SLSA (past v1.2),
  NIST SSDF (if the v1.2/Rev.1 draft is finalized), and Scorecard/Badge criteria on
  a slow cadence; the universal-core list itself is unlikely to change.
- If production-floor.md's objectives/axes stop matching Part A's bar, one of them
  is wrong — reconcile rather than let them drift.
