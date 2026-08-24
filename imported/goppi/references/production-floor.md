# production-floor — the universal project floor (what goppi scaffolds)

<!-- floor-version: 5 -- bump when the objectives/axes/deferral model change; a
     scaffolded project records this in .goppi-setup.md so `scaffold` can detect a stale
     adoption and propose the delta (see the skill's update path). `evals/
     floor-accounting.sh` compares this stamp to the .goppi-setup.md record and fails on
     drift, so staleness is machine-caught, not left to memory.
     v1→v2 (2026-07-17): orient now includes an AGENTS.md output; capture-env
     lockfile guidance tightened to the standard; stale-adoption detection added.
     v2→v3 (2026-07-18): orient's docs story — a docs/ + ADR structure gated by
     decision-significance, plus audience-scaled docs-content (Diátaxis) gated by
     whether the project has external consumers.
     v3→v4 (2026-07-19, external review): intent ledger records EVERY control-driving
     axis (no control derived from an unrecorded axis); added a distribution/supply-chain
     axis; `verify` escalates from a documented procedure to an executable check for
     Evidence/Operate/shared code; AGENTS.md gated on materially-exceeding the README;
     lockfile follows the ecosystem's app-vs-library convention; the Codex permission
     rules (`.codex/rules`) are a laid control on Codex; brownfield UPDATE re-checks the
     security invariants (workflow-hygiene) so a same-version regression is caught.
     v4→v5 (2026-07-21): the distribution axis gains release *operational* automation
     (auto version/changelog/tag from Conventional Commits) as an ASKED control for
     versioned/released projects — GitHub default: release-please templates; never
     forced onto a project that does not release (ADR-0018). -->

On-demand knowledge the `scaffold` skill reads when starting or adopting a
project. It defines **only what is universal** — true for any project regardless
of domain, language, or archetype. It is *knowledge* (objectives + selection
rules), not a file catalog and not an engine.

**The boundary (load-bearing):**
- **goppi owns the universal** — the project objectives + workflow invariants below.
- **The model owns domain rigor** — a capable model already knows its field's
  standards. goppi does not name those standards (that would make it a
  domain-biased catalog); instead it **forces the model to make its domain
  reasoning observable** at the Evidence/Operate stages (see "domain activation").
- **The project owns its specifics** — a project's own conventions and rules (its
  constitution, methodology, exact thresholds) live in that project (constitution §7).

## The one principle

> **Every material risk has a proportionate control and observable evidence —
> not every catalog item gets a CI check.**

Presence ≠ adequacy: a file existing is not the control working. Absence is
allowed, but never *silent* (see "accounting").

## Project objectives (these get accounted for)

Each is a *goal* for the project; how it materializes scales to the stage. These
are what the accounting records.

1. **orient** — a minimal README/note for the human (purpose, current status,
   entry point, exploratory vs claim-worthy) **and, for a persisting agent-worked
   project where agent-specific guidance (build/test/run commands, structure,
   conventions) *materially exceeds* what the human README already carries, an
   `AGENTS.md`** (the cross-tool de-facto standard "README for agents") — skip it
   for a throwaway, and also when a one-command README already tells an agent
   everything (a second near-duplicate doc only drifts). goppi's own contract still rides via CLAUDE.md/AGENTS.md
   deployment (§5) — this objective is about the *project's* agent-orientation.
   For a project that carries **architecturally-significant decisions** — ones that
   affect structure, key quality attributes, or are hard to reverse (MS Azure WAF;
   AWS) — a `docs/` home with **ADRs** (short record per such decision + the options
   ruled out; supersede, don't delete). The gate is **decision-significance, not
   project size**: a throwaway or simple single-purpose tool has no such decision
   and skips it; a small-but-decision-heavy project still warrants them.
   Documentation as a whole scales to **audience, not size**: a `CHANGELOG`
   (keepachangelog + SemVer) once the project is versioned/released; and for a
   project with **external users or learners**, a **Diátaxis** `docs/` set —
   Tutorials (learning) / How-to (task) / Reference (facts) / Explanation
   (understanding) — omitting any quadrant whose audience does not exist yet, and
   not forcing the four modes onto a shape they were not built for. Docs are
   **public by default** (OSS publishes design rationale — Rust RFCs, PEPs, ADRs);
   organize `docs/` by audience tier and signpost it, rather than hiding rationale.
   The only private tier is narrow (security embargoes, secrets, unreleased drafts).
2. **version-control** — the work is under version control with a recoverable
   history (git init + first commit) for any project meant to persist.
3. **separate-state** — credentials, private/raw data, caches, and generated
   artifacts stay out of version control *unless explicitly intended*; intended
   fixtures/examples/deliverables are explicitly kept in.
4. **capture-env** — when execution matters, declare dependencies and runtime
   version via the project's native mechanism, and pin for reproducible installs
   **following the ecosystem's application-vs-library convention**: an *application*
   commits its lockfile; a *library* usually does not (it resolves against a
   consumer's tree) — in that case record how CI obtains a reproducible resolution
   instead. Skip only when there is genuinely no package manager to pin. [lit]
   12-Factor II is *explicit dependency declaration/isolation*, not one lockfile
   policy for every distribution model.
5. **verify** — a command or procedure that validates the project's *real* claim —
   not a mandatory generic lint/typecheck/test/build. A **documented procedure**
   suffices for Explore / non-executable work; for **Evidence, Operate, or code
   others depend on**, `verify` must be an **executable** check (and escalates to CI
   when the correctness/frequency/hermetic-input axes call for it — see the gating
   table).
6. **mark-state** — distinguish exploratory work, reproducible evidence, and
   operational output so unfinished work is not mistaken for validated work.

## Workflow invariants (how the scaffold behaves — NOT project-ledger items)

These govern the scaffold's own conduct; they are not "controls laid into the
project" and are not accounted per-project:

- **do-no-harm** — detect and preserve existing conventions; never clobber;
  additive only; confirm before behavioral additions.
- **scale-to-risk** — select controls by the gating axes below, not by prevalence.
- **transparency** — every applied control is disclosed with a one-line undo.

## Domain activation (fix for "rigor assumed, not activated")

Relying on the model to "know its domain" is not enough — knowing is not doing.
So at **Evidence** and **Operate** stages, the model must record, in the
project's own files, an observable **claim & controls note**:

- the **material claim** the work makes (e.g. "this result is correct / this
  number is trustworthy" — whatever the work asserts),
- the **top domain-specific failure modes** *for this work* — named by the model
  from its own competence (goppi does not list them),
- the **controls it applied** against each, and the **evidence** they ran.

goppi supplies the *requirement to make this observable*; the model supplies the
*domain content*. This closes the "generic run marked compliant while a
domain check was silently skipped" hole without embedding any domain catalog.

## Gating axes — each control follows its OWN axis (no bundled "shared/serious")

Detect what you can; ask at most the few genuinely-user decisions (≤2 per round,
follow-up allowed when risk stays ambiguous). Then map each control to its axis:

| Axis | Signal | Drives |
|---|---|---|
| **Exposure** | private-local → privately-shared → externally-consumed → public | LICENSE, SECURITY (**prefer the host's private vulnerability reporting over a personal email**), docs visibility — ask it with the plain-language script below, never in licence jargon |
| **Collaboration / community** | solo → trusted collaborators → external contributors → active community | CONTRIBUTING, PR/issue templates, required review, CODEOWNERS, **CODE_OF_CONDUCT** (**prepare-now when the user *explicitly* states they expect/want contributors** — community intent is stated, not speculative; otherwise activate at first outside contribution, not at hour-zero of a merely-public repo) |
| **Correctness dependence** | exploration → produces claims → consequential decision | verification depth, **CI** (also driven by repeat-frequency + hermetic inputs) |
| **Data-integrity dependence** | none → ordinary data → temporal/as-of correctness | reproducibility & provenance rigor (content owned by model/project) |
| **Recovery cost / reversibility** | cheap redo → expensive/irreversible loss | branch protection, required green CI, backups (even solo) |
| **Information sensitivity** | public-ok → private → regulated/PII | secret handling, access controls, redaction |
| **Execution frequency** | one-off → repeated → automated | CI, dependency maintenance, monitoring |
| **Blast radius** | local result → personal automation → externally consequential | operational/runtime controls — for a runtime *service*, the concrete list to account for is health/readiness checks, migration **rollback** (not just apply), the auth gate, PII redaction in logs, rate limiting, API versioning, and cost guards; name the ones that apply and say why the rest do not |
| **Distribution / supply-chain** | not distributed → internal artifact → externally-consumed package/image | release integrity: provenance/SBOM, signed & reproducible builds, dependency review, pinned-by-hash deps, release/tag protection (SLSA L1→L2→L3) — *which level & format is the model's domain call; goppi requires only that it be accounted* · **release operational automation** (version/CHANGELOG/tag derived from Conventional Commits) once the project is *versioned/released* — an **asked** control, never forced (ADR-0018) |

**Release operational automation (asked; distribution axis, v5).** Distinct from
release *security* above: this is the operational side — deriving the version bump,
CHANGELOG, and tag from Conventional Commits automatically. When the distribution
axis says *versioned/released* **and** the host is GitHub, the scaffold **asks**
("set up automated releases?"); on opt-in it lays goppi's release-please templates
(`templates/release-please.yml` + config + manifest — SHA-pinned action, least-priv
permissions, release-PR pattern so nothing pushes to a protected default branch).
Honest limits: (1) a project that does not release must not get it — asked, never
laid by default; (2) release-please is **GitHub-generic, not universal** — ecosystems
with their own idiom (npm → semantic-release or changesets, etc.) may substitute the
idiomatic tool; (3) **one manual step remains**: the target repo's setting "Allow
GitHub Actions to create and approve pull requests" (`actions/permissions/workflow`
`can_approve_pull_request_reviews=true`) cannot be flipped by scaffold — the user is
instructed, and the accounting records it as a **manual follow-up**, so auto vs
manual stays honest; and (4) **release-please presumes Conventional Commits** —
it derives the version bump from commit subjects, so a project without that
convention gets a release workflow that never bumps past its manifest floor.
**Pair it with a commit/PR-title convention (and its gate) whenever one is not
already in place**, or the control is recorded `active` while being inert — the
"presence ≠ adequacy" failure this floor exists to prevent.

Notes: CI is **not** a "shared" consequence — it follows correctness, frequency,
and whether inputs are hermetic (a private-but-consequential project can warrant
CI with no sharing). Conventional Commits / squash are optional workflow choices,
not a "seriousness" consequence. Irreversible/commitment items (a LICENSE
*choice*, creating a remote, going public) always **confirm**, never auto.

**The two context choices, in plain language** (ported from gingoa's elicit
skill — both are the user's to make, so neither is ever picked silently):

- **Visibility** — "Is this project public — anyone can see the code — or
  private, just for you or your team?" A public project also gets a Code of
  Conduct (per the collaboration axis's stated-intent rule above).
- **Licence** — a non-engineer cannot be expected to know licences, so offer a
  short guided pick rather than jargon: most projects use a **permissive**
  licence like **MIT** (anyone can use it, few strings) or **Apache-2.0**
  (permissive plus a patent grant); some use a **copyleft** licence like
  **GPL-3.0** (changes must stay open); a few dedicate to the **public domain**
  (Unlicense). Close with the default, not a quiz: "if you're not sure, **MIT**
  is the common default — is that fine, or would you like one of the others?"

Declining is allowed and safe: record the skip, leave visibility undeclared
(deferring the Code of Conduct), and **announce** the licence default rather
than applying it silently — the rule immediately below.

**The tie-breaker when detect-vs-ask is genuinely close: cost-of-wrong-default
vetoes auto.** Cheapness of detection is not the deciding factor — the question
is what a wrong default costs and who pays. A default that is awkward to undo
(a published repo, a chosen licence, a remote that now exists) is asked even
when the signal looks obvious; a default that is one edit away is taken silently
even when the signal is weak. Detection confidence breaks ties *within* a cost
tier, never across one.

**A skipped question is recorded, and its default is announced.** The user may
decline to decide — that is legitimate and must stay cheap. What is not
legitimate is the decision vanishing: record the skip in the ledger, apply the
safe default, and **say in the summary which default was applied**, in the
user's language. A silently-applied default is indistinguishable from a
question that was never asked, which is the state the ledger exists to prevent.

## The stage profile (lifecycle × how heavy)

| Stage | Materializes as |
|---|---|
| **Explore** | version-control (if it'll persist) · source/secret/data separation · explicit "not validated" status. Little else; a Run/Reproduce section may say "not executable yet." |
| **Evidence** | frozen inputs · clean run · a lightweight run record · **the domain-activation note** (model names & checks its domain failure modes). |
| **Operate** | automated checks · monitoring · recovery · dependency/security maintenance · deployment controls · **release integrity for externally-consumed artifacts** (provenance/SBOM/signing per the distribution axis) · domain-activation note. |

## The deferral model — two kinds of `deferred`

A control that isn't active now is `deferred` **with a trigger** — but there are
two kinds, and the scaffold must say which:

- **prepare-now** — set it up now because a *known, planned* future needs it and
  doing so **does not interfere with current work** (e.g. SECURITY.md when public
  is planned). Eligibility: (1) the future is *stated by the user*, not
  speculative; (2) setting it up now is inert while waiting. **Commitment-bearing
  artifacts are excluded** — a LICENSE *choice*, publishing, creating a remote
  still require explicit confirmation now, never auto-prepared.
- **activate-on-trigger** — keep it *unset* until the trigger, because enabling
  it now would **interfere** (e.g. required-review / multi-approval would deadlock
  a solo maintainer; enable at team-join). The structure may exist; the
  enforcement waits.

Distinct controls get distinct triggers — **required-review** (collaboration) and
**branch-protection** (recovery-cost) are separate, not one bundle.

**Templates get their gates — the collaboration axis lays both.** A PR or issue
template is a *suggestion*; the machine gate is what makes it a control (model
proposes, machine verifies — ADR-0007/0016), and it is what catches a body opened
by a scripted `gh … --body …`, which bypasses the web-UI auto-fill entirely. So
whenever the delivery PR/issue templates are laid, **`templates/pr-body.yml` and
`templates/issue-body.yml` are copied into the project's `.github/workflows/`**
alongside them. The two are not symmetric and the difference is inherent, not an
oversight: the **PR gate hard-blocks the merge**, while the **issue gate can only
apply a `needs-template` label** — an issue has no merge to block. goppi's own
repo dogfoods both (`evals/pr-body-hygiene.sh`, `evals/issue-body-hygiene.sh`).
If the templates are unreachable, generate equivalents rather than skipping the
gate — a template without its gate is the state this control exists to prevent.

## Intent ledger (recorded before deriving controls)

The scaffold records the intent-axis answers as an explicit ledger — at minimum the
**three interview axes** (exposure, collaboration, consequence/lifecycle), **plus
every other gating axis that materially drives a laid control** (recovery-cost,
information-sensitivity, execution-frequency, data-integrity, blast-radius,
distribution/supply-chain) — each marked *detected* or *asked*. Controls are derived
from the ledger, never from assumption: **no control may be laid whose driving axis
is absent from the ledger.** That closes the silent-under-provisioning hole — a
project scored "complete" while recovery-cost or sensitivity was never recorded, so
backups or redaction were silently skipped. Keep the interview cheap (detect what
you can; ask ≤2 genuine user-decisions per round); an axis that drives a control but
stays ambiguous blocks completion until recorded. `floor-accounting.sh` machine-enforces
**one** axis-basis today — a project with CI (a `.github/workflows/` dir) must record
its correctness/frequency axis (keyed off the actual workflows dir, so it can't
false-positive on prose). The other axis-bases (branch-protection ⇐ recovery-cost,
redaction ⇐ information-sensitivity) are **recorded by the model and verified by
inspection, not machine-checked**: branch-protection is a remote setting with no local
file to key off, and sensitivity is prose the checker cannot parse without false
positives — and a false-positive control would erode trust in the whole check
(self-deletion, §2 value 6). The requirement — *no control from an unrecorded axis* —
is the floor's rule; the checker mechanizes only the one case it can do precisely.

## Accounting (a light omission checker, honestly labelled)

When the scaffold applies the floor, it writes a short record — **one row per
project objective** — each as `active` (control + evidence), `n/a` (reason), or
`deferred` (kind — prepare-now / activate-on-trigger — + trigger), plus the
`floor-version` it was adopted against. The scaffold **runs
`evals/floor-accounting.sh` on that record** before declaring completion.

This is an **omission smoke-test, not a proof of adequacy** — it verifies nothing
was silently dropped; it does not verify each control actually works. Adequacy is
the model's judgment + (for shared/CI'd projects) the real checks themselves.

**A narrower permission posture is accounted the same way — write the reason
down.** `hosts/goppi-doctor.sh` compares a project's deny/ask set against goppi's
own, and the severity of a shortfall follows *who made the promise*: on a project
goppi never touched it is **advice**, but a `.goppi-setup.md` means goppi laid that
set here, so a posture below it is a **regression against what this project was
promised** and the audit **fails**. The escape is this accounting model, not a
silencing flag — record the control in `.goppi-setup.md` as

```
posture-exception: <control> — <why this project is narrower>
```

and it is excused: still printed, never blocking. Paying in a written reason is
exactly what `n/a (reason)` costs for an objective, and it keeps a deliberate
narrowing distinguishable from a silent one.

The same checker also **detects a stale adoption**: if the record's `floor-version`
is behind the current floor, it exits non-zero (STALE) so the **update path**
(skill Path B) runs and proposes the delta. This is the machine-checkable core of
brownfield-update — drift is *caught*, not left to the model remembering to
compare. (Downstream projects may treat STALE as visibility rather than a hard
gate, per the brownfield "audit-only" doctrine; goppi holds *itself* to current.)

It also runs a few **conditional controls** — the "model proposes, machine
verifies" pattern that *narrows* (never eliminates) reliance on model compliance:
if the intent ledger says exposure is **public**, a `LICENSE` must exist (universal
core for public projects); and no unresolved `{{placeholder}}` may remain in the
record (completion contract; GitHub Actions `${{ … }}` is not a placeholder).
These turn specific judgments into verified facts. They are deliberately few and
high-precision — a false positive erodes trust in the whole check, so only
controls that are near-universal and cheaply verifiable belong here.

## Completion contract (fix for placeholder/invalid output)

Before declaring a scaffold done: all `{{placeholders}}` in copied templates are
resolved, any emitted YAML/JSON parses, and the `verify` command actually runs
(or is honestly marked "not executable yet" at Explore). **Cited verification must
be real**: any checker or result named in the accounting shows its actual output
or is marked "verified by inspection" — never "result below" for a run you did not
paste, and never a reference to a script/path absent from the project (the
`floor-accounting.sh` checker lives in the plugin, not the scaffolded repo — cite
it as "run from the plugin: <output>" or say "verified by inspection").

## Brownfield = adopt (never scaffold-over)

Existing project → `adopt`, not `scaffold --overwrite`:
detect → **coexist** (additive, never clobber) → **dry-run/diff first**; a
behavioral addition (a workflow file, an ignore rule, anything that changes what
runs) requires explicit confirmation → propose gaps through **the project's own
delivery flow** (a local repo may have no remote/PR — then it's local commits;
never push/merge without authorization, never force PR-first) → **audit-only** (a
red floor is still adoptable; scores are visibility, not gates).

**The contract is a laid control, and on Codex it is non-negotiable (ADR-0031).**
`scaffold` step 4's host-enforcement bullet lays the rules file and the profile;
**the contract belongs beside them**, and this is its home because the skill body
had no budget left to carry it (measured: adding it inline put that body at
**5,019 / 5,000**, and the compressed form still left a 4-token margin — so the
rule lives here, where it costs nothing, rather than being asserted in a body
that is over its cap).
Claude can receive the contract from outside the repo — a user-scope
`@…/GOPPI.md` import in `~/.claude/CLAUDE.md` reaches every project on that
machine. **Codex has no `@import` at all**, which is why `hosts/sync-agents.sh`
inlines the contract into `AGENTS.contract.md` in the first place. So for a target
that runs on Codex, the contract must live in **its own** tree: generate it with
`hosts/sync-agents.sh` and append the result to the target's `AGENTS.md`, beside
the rules file and the profile.

For a Claude-only target the operator **must do one of two things, and record
which** — lay the contract in the tree, or confirm the user-scope import actually
resolves and note that the project depends on it. Leaving it unstated is what let
`scaffold` reach step 6 with nothing to show. The two are not equivalent: in the tree, it
travels to whoever clones the repo; left to a user-scope import, it works
perfectly for the person who set it up and gives a teammate nothing.
`hosts/goppi-doctor.sh` reports those two states differently rather than grading
them the same — a tree contract passes as "travels", a user-scope one passes with
the limitation named, and neither present is still a failure.

**Prove additive; do not merely promise it (ADR-0030).** "Never clobber" used to be
prose with nothing behind it, and the harm it admits — a control the owner chose,
silently removed — is not detectable afterwards. So: **before** writing anything
into a project goppi does not own, make sure a before-state exists (a clean commit,
or a copy of its protected files taken **outside** the tree). **After** the writes,
run `evals/additive-only.sh --git <target>` — or `--baseline <copy> <target>` where
git cannot help — and read the exit code:

- **0** — everything the before-state held survived.
- **1** — CLOBBER: a control the owner chose was dropped. It names the exact entry.
- **2** — there was no before-state to compare against. **This is not a pass**;
  "I could not check" must never be recorded as "additive ✓".

Any non-zero **blocks the adoption's completion claim**: restore what it names, re-apply
goppi's additions on top, re-run. It **blocks** on the control surface
(`.claude/settings.json`, `.claude/settings.local.json`, `.codex/config.toml`,
`.codex/rules/*.rules`, `.gitignore`) and only **reports** on contract wiring,
governance/CI and floor documents, where a loss can be a diff the owner legitimately
confirmed and the script cannot see the confirmation. Honest ceiling: it proves the
before-state survived — not that what was added is adequate, and under `--git` it can
say nothing about files that were never **committed**, `.claude/settings.local.json`
included (it is gitignored by design). It ends each run by naming any control file
that exists **now with no before-state**, so that gap is visible rather than silent;
**if the target's tree is dirty, take a copy first and use `--baseline`.** Plugin
unreachable ⇒ diff the protected files against the before-state by hand and record
that the gate was unavailable.

**First adoption vs UPDATE — the test and the order.** A `.goppi-setup.md` in the
project means it was adopted before, so the run is an **update**, not a fresh
adopt, and its steps are ordered:
1. **Re-check the security floor of what goppi laid, before any stop decision** —
   `evals/workflow-hygiene.sh` against the project's own `.github/workflows/`.
   This runs first precisely so a **same-`floor-version` regression** is caught on
   a run that would otherwise conclude "nothing to do"; it is a delta to fix
   regardless of version.
2. **Detect staleness mechanically, never by eye** — run `floor-accounting.sh
   <record> [current-floor-version]` and read its exit code (STALE = the record's
   version is behind the floor). Plugin unreachable ⇒ compare the record's
   `floor-version` by hand against this file's stamp. If it is current **and**
   intent is unchanged **and** step 1 is clean, there is nothing to do — say so
   and stop, rather than manufacturing a delta.
3. **Propose only the delta** — the `floor-version` changelog line at the top of
   this file states exactly what changed between the recorded version and now —
   as a diff, confirming each behavioral change; re-lay only what is new or
   changed, never what is already there. Then rewrite the record's
   `floor-version` and re-run the checker until it passes: **the passing re-run is
   the evidence the update landed**, and nothing else is.

**Adoption interviews for intent too.** Detection gives facts (git, language,
files); it never gives intent, and an existing project's *contents* are not its
owner's plan. Adopt asks the same axes a greenfield run asks and records them
before deriving any control — the recorded failure this rule exists to prevent is
a demo that assumed "private → LICENSE n/a" for a project already planned to go
public. On "public later" the deferral model applies, but a commitment item (the
LICENSE *choice*) still confirms now. Keep separate controls separate while
classifying gaps: **approval-required and branch-protection are distinct gates.**

*No ratchet promise, and no idempotent template state.* A thin no-engine harness
has no persisted state, so goppi does not claim a monotonic "Clean as You Code" gap
count, and its **update path is best-effort, not idempotent**: it tracks the
`floor-version` + intent, not per-file base hashes, so it cannot promise that re-running
yields a byte-identical tree. What it **can** prove since ADR-0030 is narrower and is
the part that matters: `evals/additive-only.sh` shows mechanically that the **control
surface** the owner already had survived the run, and refuses to certify a run with no
before-state. Outside that surface the update path stays best-effort. If you need
guaranteed template-state management (provable non-clobber *everywhere*, 3-way merge on
template upgrades), that is still a determinism engine's job — use **Copier / cruft** for
it; goppi composes with them, it does not replace them (design §3.1). What goppi *does* enforce
on an update is the **security floor of what it laid**: it re-runs the invariant
checks (`workflow-hygiene`) against the project's own workflow files, so a
same-`floor-version` regression — e.g. a `permissions` block deleted from a CI file
goppi contributed — is still caught without a version bump. It applies the ratchet
*spirit* — hold new work you add to the bar, leave pre-existing alone — as guidance,
not an enforced invariant.

## What is NOT here (by design)

- **Domain content** (any field's specific failure modes / controls): the model
  supplies these via domain activation; a project codifies them in its own
  constitution/methodology. goppi names none.
- **Generic language boilerplate** (a Python `.gitignore`, a pytest config): the
  model generates these; `templates/` carries only goppi's *opinionated* pieces.

The opinionated pieces `templates/` does carry are **re-reviewed at every model
upgrade / harness-eval** (self-deletion, design §2 value 6): if a capable model now
reliably generates an equivalent, delete the template. What earns their keep today
is that hand-generation *drifts* — goppi's own `.github/ci.yml` lost its security
baseline while `templates/ci.delivery.yml` kept it. `evals/workflow-hygiene.sh` now
catches that drift, so a template's opinion cannot silently rot out of the dogfood
instance ("model proposes / machine verifies").

The regression leg of the prove-or-delete discipline is **machine-measured for
the deterministic components** (2026-07-21; reframed 2026-07-25, ADR-0025):
`evals/worth/run.sh` runs reproducible fixtures WITH vs WITHOUT (a null
verifier) each deterministic component (9 today: secret-guard, deploy-check,
the six checkers, and the delivery-hygiene pair scorer) and reports the delta
as **fixture-regression coverage**; **zero
coverage is a machine regression trigger** — the component no longer catches
its own fixture set. Honest scope: this narrows — it does not close — the
"enforcement is mostly prose" gap. Coverage is measured *on that fixture set
only*; it cannot detect host-native subsumption (that stays with the prose
`## Expiry conditions` + harness-eval pairs, ADR-0025), and the judgment layer
(depth classification, kickoff) remains outside verifier reach by design
(ADR-0009); see `evals/worth/README.md` for the full ceiling.

## Evidence
- [lit] External adversarial reviews (gpt-5.6-sol, 2026-07-16): review #1 established the objectives/axes/stage-profile and "every material risk → proportionate control + evidence"; review #2 (of this scaffold) drove: domain-activation (rigor must be observable, not assumed), separating project-objectives from workflow-invariants, adding version-control + recovery-cost/sensitivity/frequency axes, ungating CI/PR/docs from a "shared/serious" bundle, the honest accounting label + completion contract, and dropping the unsupported brownfield ratchet.
- [census] gingoa repo survey (N=6,582 top-starred, `/Users/coolbress/gingoa/docs/research/census-data/`): prevalence ≠ necessity; public-OSS reference class over-represents publication/collaboration norms (LICENSE 94%, CONTRIBUTING 48%/41%-adequate, PR-template 29%, branch-protection 13% strong, squash 97% = *allowed* not selected). Used to gate the publication/collaboration bundle by exposure/collaboration, and to note where goppi must NOT undershoot (CI by correctness, protection by recovery-cost, docs by criticality — not by sharing alone).
- [lit] SWEBOK v4 / ISO-IEC-IEEE 12207·25010 / NIST SSDF / SLSA / OpenSSF / DORA (via gingoa TAXONOMY.md) — the frameworks behind the aspect standards; goppi carries the universal subset only.
- [lit-internal] constitution §7 (repo owns domain truth) + design §2.6 ("well-designed" ≠ build threshold).
- [lit/survey] `docs/standards.md` — the external justification for this floor (the standards-derived professional bar) and the dated competitive-landscape snapshot showing where goppi sits. Primary-sourced, verified 2026-07-17.
- [lit] **ADRs (Architecture Decision Records)** — established senior practice, **primary-source verified 2026-07-18** (basis for the v3 orient addition). Origin: M. Nygard, "Documenting Architecture Decisions" (2011-11-15). ThoughtWorks Technology Radar Vol.17 (2017-11) placed "Lightweight ADRs" in the top **Adopt** ring. Tooling/templates: adr.github.io, Nat Pryce `adr-tools` (default `doc/adr`), **MADR** (default `docs/decisions/` — goppi's path). First-party large-org adoption: **AWS Prescriptive Guidance**, **Microsoft Azure Well-Architected Framework**. Nygard's canonical fields = Title/Status/Context/Decision/Consequences, and **"supersede, don't delete"** is his (verbatim). **Corrections from hardening:** (1) the **rejected-alternatives** field is *not* Nygard's — it comes from **MADR ("Considered Options")** / **MS WAF ("alternatives you ruled out")**; goppi keeps it, attributed there. (2) **The gate is decision-significance, not project size**: write an ADR only for an "architecturally significant" decision — MS WAF: "affects the system's structure, key quality attributes, or is difficult to reverse"; AWS (via Richards & Ford, *Fundamentals of Software Architecture*, 2020). A throwaway has no such decision → skips it; ThoughtWorks otherwise leans "for most projects… no reason not to." *Honest counter-evidence:* ADRs are criticized for going **stale** (decisions drift into PRs/chat while the file rots) — goppi's drift-guarding (workflow-hygiene, re-review triggers) is the mitigation posture; the criticism is secondary-sourced. *Not found:* no first-party Google/GitHub-corporate mandate (the `adr` GitHub org is community, not GitHub Inc.).
- [lit] **Documentation content/structure** — primary-source verified 2026-07-18. The de-facto framework is **Diátaxis** (orig. Divio "documentation system", D. Procida; **2017 origin**, renamed Diátaxis ~2020): four audience-need types — **Tutorials** (learning) / **How-to** (task) / **Reference** (facts) / **Explanation** (understanding); adopted by Django (labels Explanation "Topic guides"), Cloudflare, Canonical (diataxis.fr). Doc-type templates: **The Good Docs Project**. README: makeareadme.com / standard-readme. **CHANGELOG**: keepachangelog 1.1.0 (Added/Changed/Deprecated/Removed/Fixed/Security, ISO-8601, newest-first) + **SemVer 2.0.0**. **Gate = audience, not size** (Write the Docs: "give users the information they need, but not too much"): README always; CHANGELOG once versioned/released; the full Diátaxis set only with external users/learners, omitting quadrants with no audience. Locations: `docs/` for the set; README/CHANGELOG at root; CONTRIBUTING at root/`docs/`/`.github/`. *Honest counter (Hillel Wayne, "My Problem With the Four-Document Model"):* the 4-doc model is **not universal** — built for *tools*, weaker for frameworks/languages, misses concept-overviews/snippets, and is over-applied ("this is the only way"); don't force the quadrants onto the wrong shape. *Dropped (unverifiable):* the Google "Minimum Viable Documentation" post (404) — the audience gate rests on Write the Docs + Diátaxis instead.
- [lit] **Documentation organization & visibility** — primary-source verified 2026-07-18. In OSS, **design rationale is public by default** (transparency), not hidden: Rust RFCs (github.com/rust-lang/rfcs), Python PEPs (peps.python.org — "the revision history is the historical record"), Kubernetes KEPs, and ADRs are all public version-controlled files. **"Keep design docs internal" is a *company* norm (Google), not OSS** — do not port it to a public release. The only genuinely-private tier is narrow: **security embargoes** (SECURITY.md + coordinated disclosure), secrets, pre-announcement drafts. **Published ≠ public**: a docs-site build may *exclude* files (MkDocs `exclude_docs`, Sphinx `exclude_patterns`) for curation, but they stay readable in the public repo — unpublished-to-site is not confidentiality. Organize `docs/` by **audience tier** (user guide / contributor-design / decision-records), signposted; a GitHub Wiki on a public repo is public and de-synced from the code's versions, so it is not an "internal" home. *Over-engineering caveat:* for a small repo "a folder of markdown is enough" — the fix is signposting/tiering, not new tooling.
- [lit] **Bilingual / multilingual docs** — primary-source verified 2026-07-18. The standard is **one canonical source language + translations in separate labeled files/trees** (Docusaurus `i18n/<locale>/`; Kubernetes localization — "must be based on the English files", fix upstream English first; Sphinx gettext `.po`; Weblate monolingual-base). Use **BCP-47 / RFC 5646** codes (`ko`, `zh-CN`) — sibling `README.ko.md` for plain repos, `docs/<lang>/` for a tree. **English source is a *convention* (reach), not a codified rule** — but de-facto: ~87% of repos are English (2025), and mixed-language repos score *worse* than clean-English on stars/contributors ([survey] arXiv 2602.19446, 2026 preprint — directional); Apache mandates English for public/governance comms (transparency/auditability). So: **when the maintainer's language ≠ the audience's, canonical docs go in the audience's lingua franca (English); native-language versions are labeled translations.** *Honest counter:* translation drift can be net-negative — MDN froze/archived unmaintained locales ("a stale translation is worse than none"); so **don't translate what you can't keep current**, and archive (don't translate) superseded docs. *Not codified:* the language of a genuinely-private design/thinking doc — but once contributor-facing, English is the well-supported choice.

## Expiry conditions
- Model competence covers an objective so reliably that stating it changes nothing → ablate it (§2 value 6).
- Host/`gh` ships an equivalent guided scaffold/adopt for non-engineers → keep only goppi's deltas (domain-activation, accounting, the model/project boundary).
- S4 eval shows an objective/axis never changes an outcome, or the domain-activation note is never used → demote or delete it.
