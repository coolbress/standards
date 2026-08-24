---
id: aspect-27-ai-harness-archetype--harness-self-threat-model--2026-07
title: "하네스 자기 공격면 STRIDE 전수 (goppi, 2026-07)"
parent: aspect-27-ai-harness-archetype
kind: evidence
evidence_track: lit
status: draft
language: en
last_updated: "2026-07-29"
method: "goppi 자신의 공격면에 대한 STRIDE 전수 패스. 원본 goppi/docs/internal/threat-model.md — 2026-08-24 이관, 본문 무수정. 코퍼스의 agent-threat-model.md(118줄, 일반 에이전트 위협 지도)와 별개 문서이며 이쪽이 3배 길고 하네스 자신을 대상으로 한다."
---

> **이관 기록 (2026-08-24)**: 하네스는 폐기됐으나 이 문서는 남긴다 — **"하네스가 자기 자신을 공격면으로
> 놓고 STRIDE를 돌리면 무엇이 나오는가"** 의 전수 기록이고, 발견을 지우지 않고 **취소선으로 남긴** 형식
> 자체가 방법론이다. 일반 에이전트 위협 지도는
> [`agent-threat-model.md`](agent-threat-model.md)이고 **이 문서와 별개다.**


Last updated: **2026-07-29** — first pass in Session H (issue #72); **G2 and G4
closed in Session I (issue #75)**, **G5 closed in Session K (issue #85)**, their
rows updated in place and the findings struck through rather than deleted.
**Open findings: 0** — and the count is worth reading precisely, because this
document's own rule is that prose must not be laundered into a control. **Three
of the five (G2, G4, G5) are closed by code with tests behind it. Two (G1, G3)
are closed as *documented limitations* — a recorded honest boundary, not a
mitigation**; G3 in particular still has no detection and says so. "Zero open"
is a statement about *this* enumeration and how each item was answered, not a
claim that the surface is exhausted; the re-review triggers at the bottom are
what keep it honest. · Form: gingoa
`docs/internal/threat-model.md` · Anchors: design §4.3 (enforcement truth),
§11 G7, `hooks/README.md` "Known limitations", ADR-0012, ADR-0023.

**Why this exists.** goppi is not a library a project imports. It **installs hooks
into two hosts, rewrites a contract file, and plants permission rules into
repositories it does not own**. Every prior security pass here was reactive —
Session A (2026-07-24) answered an external critique's seven findings, which is
triage, not coverage: a critique finds what the critic happened to look at. This
is the first systematic pass over the surface goppi presents *as a tool*.

**Scope** = goppi's own installation, sync, distribution and planting surface.
Explicitly **not** in scope: whether the *contract text* makes a model behave
well (that is §11's measurement problem, not a security property), and the
runtime prompt-injection surface of a session using goppi (that belongs to the
sandbox and `references/sandbox-presets.md`, and is summarised under Residual).

## Assets (what must not be harmed)

1. **The user's host configuration** — `~/.claude/settings.json`,
   `~/.codex/config.toml`, and every key the user already put there. Corruption
   or silent loss is the #1 harm, because the user did not write the thing that
   broke it.
2. **The target project's tree** — a repo goppi did not create and does not own.
   `scaffold` writes into it. Clobbering an existing control is worse than never
   having laid one, because it removes a protection the owner chose.
3. **Session content** — `progress.md`, git state, branch names, captured into
   `GOPPI_state/precompact/` by the PreCompact hook. This is conversation-derived
   material and must not become public repository history.
4. **goppi's own repo integrity** — no secret committed, and the distribution
   path (git-backed marketplace) not a vector into two hosts at once.

## Trust boundaries & data flow

- goppi runs with **the user's own privileges** on the user's machine. It is not
  a service, holds no server-side trust, and has **no network egress and no
  telemetry** — verified 2026-07-26 by grepping every shipped runtime script
  (`hooks/scripts/*.sh`, `hosts/*.sh`, `hosts/codex/*.sh`): the only `http(s)`
  and `curl` occurrences are *string data inside test fixtures*.
- goppi **handles no credentials of its own.** It has no token, no auth, no
  account. Its entire relationship with secrets is *preventing other things from
  reading them* (`secret-guard.sh`, sandbox `denyRead`, the Codex profile).
- **Inputs it trusts only after validation**: hook stdin payloads (host-supplied
  JSON, best-effort parsed, never `eval`ed); `GOPPI.md` as sync input; a target
  project's existing config when adopting; the `.codex/rules` file as read by
  Codex's own engine.
- **Three enforcement layers, and only two are real** (design §4.3, restated
  because a threat model that forgets this over-claims): contract text is
  **advisory**; permission rules are **friction** (bypassable by flag
  permutation, absolute path, indirection, chaining); the **sandbox / committed
  Codex profile is the boundary**. Nothing below assumes otherwise.

## Threats → mitigations (STRIDE-flavored)

| # | Threat | Vector | Mitigation (as-built, file opened 2026-07-26) |
|---|---|---|---|
| T0 | **Tampering — the contract silently reaches no one** | the contract is deployed by a *user-scope* `~/.claude/CLAUDE.md` import (what `README.md` recommends), so it is personal to one machine and travels with no repository; a teammate who clones gets none, and on Codex there is no `@import` at all | `hosts/goppi-doctor.sh` now answers **two** questions instead of conflating them (ADR-0031, #81): in the tree → PASS "travels" · reachable only via the user-scope import → PASS **with the limitation named** · neither → FAIL. Reachability is *verified* — the import path is resolved and the target must carry all five clauses, so a dangling import or stub is not a pass. Codex keeps the strict rule. **Found because the old check FAILed 8 of 9 real projects on the author's machine while asserting "the host runs with no operating contract at all", which was false.** |
| T1 | **Tampering — contract sync emits a truncated contract** | an HTML comment lands mid-file, `awk` strip cuts early, Codex silently gets a 2-clause contract | `hosts/sync-agents.sh` asserts **all five clause headers survive the strip and aborts (exit 2) otherwise** — refuses to inline a truncated contract rather than shipping one. `--check` drift gate wired into `check.sh`. **Adequate.** |
| T2 | **Tampering — scaffold clobbers a target's existing controls** | adoption writes settings/rules over what the owner already chose | `skills/scaffold/SKILL.md` Path B still states the rule (never scaffold-over, additive only, diff-and-confirm), and since **2026-07-26 (#75, ADR-0030) a machine judges the result**: `evals/additive-only.sh` compares a before-state (git ref, or a baseline captured outside the target) against the tree and **fails** when the control surface — `.claude/settings.json`, `.claude/settings.local.json`, `.codex/config.toml`, `.codex/rules/*.rules`, `.gitignore` — lost an entry. Read-only by construction; loss is counted as a **multiset** (a flipped `decision`/`:root` masked by a sibling line is caught) and an added `.gitignore` **negation** counts as removal; **no before-state ⇒ exit 2, never a pass**, and any control file existing *now* with no before-state is named at the end of the run rather than passing silently. Contract wiring / CI / floor docs are reported, not blocked, because a loss there can be a confirmed diff. **Adequate for the control surface; see G2 for the ceiling.** |
| T3 | **Information disclosure — session content reaches public history** | PreCompact writes `progress.md` head + git status + branches into `GOPPI_state/` *inside the project tree*; if that path is not ignored it can be committed and pushed | `templates/gitignore.base` ships `/GOPPI_*/`, `/spec.md`, `/progress.md` (Session A, P1-2); goppi's own `.gitignore` carries `GOPPI_*/` — verified with `git check-ignore -v`. **Covers scaffolded projects only — see G1.** |
| T4 | **Information disclosure — a secret rides a command out** | model puts a literal credential on a Bash/WebFetch argument | `hooks/scripts/secret-guard.sh`, PreToolUse, **fail-closed**, zero deps, grep self-test, 10s timeout. Limits are documented rather than hidden (`hooks/README.md` 1, 2, 2b): literal-pattern only; variable/file/encoded indirection passes; the boundary is the sandbox. ~~**Adequate for its stated scope.**~~ → **QUALIFIED BY SURFACE 2026-07-29 (#106).** That sentence named a *pattern* scope and no *surface* scope, which made it false where it mattered most. Measured with one command across three surfaces: Claude Code **blocked** · Codex **CLI blocked** before execution · Codex **desktop ran it, exit 0, no diagnostic**. **Measured: the hook did not run.** Whether that is dispatch, discovery, or hook *trust* not carrying to that surface is **not narrowed** — the app logs are unreachable and #21639 is upstream's to answer, so this document does not claim a mechanism it did not separate. What *is* established: the matcher and script are right (they fire on Claude Code and the Codex CLI, same script, same payload), and `openai/codex#21639` (OPEN, externally reproduced) names the Desktop app-server path. **Trust on the desktop surface specifically is unverified** — it was granted on the CLI, and desktop runs a different bundled build. **Adequate on Claude Code and Codex CLI. On Codex desktop this control does not run at all** — and note the shape of the miss: the repo could say "verified on Codex" only because its evidence was payloads piped into the script, which reaches no dispatcher. Per-event confidence, deliberately not flattened: `PreToolUse` **CONFIRMED failing**; `SessionStart`/`deploy-check` failing per #21639's external repro but **not confirmed locally**; `PreCompact` **INCONCLUSIVE**. |
| T5 | **Denial of service — a fail-closed hook bricks the session** | `secret-guard` breaks and blocks every Bash call | zero dependencies + up-front grep self-test + 10s host timeout; the other two hooks are deliberately **fail-open** (`precompact-snapshot.sh` exits 0 on every path; `deploy-check` warns only). Posture is per-hook and justified in `hooks/README.md` §"Posture rationale". **Adequate.** |
| T6 | **Elevation — a stale cached skill keeps executing old rules** | the plugin cache holds a version the repo has since fixed; the session runs the cached copy | **None.** Observed live this session: `goppi:governed` loaded from `~/.claude/plugins/cache/goppi/goppi/0.13.0/` while this tree was at 0.14.0. **See G3.** |
| T7 | **Spoofing — a present-but-hostile control passes the audit** | a repo ships a `.claude/settings.json` or `.codex/rules` that is present and parseable but weaker than goppi's, or actively permissive | `hosts/goppi-doctor.sh` proves presence + basic validity (Session A, P0-2: unparseable rules or a missing `:root="deny"` profile are a **FAIL**), and since **2026-07-26 (#75)** it also **compares content against goppi's own committed set** — by control class, not literal string, so an equivalent phrasing is not a gap. A weaker Claude posture is **named control-by-control** and the summary line stops reporting a bare "PRESENT ✓"; an **unparseable** `.claude/settings.json` is a **FAIL** (parity with the rules rule), and on Codex a rules file carrying **no `forbidden`/`prompt` decision at all** is a **FAIL**, since the absent case already was. **Adequate; the residual is severity, see G4.** |
| T8 | **Repudiation — a bypass leaves no trace** | prefix/glob rules are evaded; nothing logs the evasion | Accepted and recorded, not mitigated: design §11 G7 already states "a silent bypass leaves no log, so '0' does not prove no-incident". The compensating control is the sandbox, which fails closed. **Accepted risk, honestly labelled.** |
| T9 | **Supply chain — a compromised GitHub Action** | third-party action in goppi's own CI | `evals/workflow-hygiene.sh` machine-enforces: every third-party `uses:` pinned to a **full 40-hex SHA**, a least-privilege `permissions:` block, no `permissions: write-all`, no `pull_request_target` — run against both `.github/workflows/` **and** `templates/`, so the boilerplate goppi plants cannot rot below its own floor. goppi ships **no runtime dependencies** (bash + python3 stdlib). **Adequate.** |
| T10 | **Supply chain — a secret committed to goppi's own repo** | ordinary human error | `evals/secret-scan.sh`, blocking in `check.sh` and therefore in CI, since **2026-07-28 (#85, ADR-0032)**. Scan **paths** come from `git ls-files --cached --others --exclude-standard`, **content** from the worktree — *not* the filesystem: `gitleaks dir .` was measured flagging a canary under gitignored `GOPPI_state/`, a **local-only false block** CI's clean checkout could never reproduce, which is the CI/local drift `ci.yml` exists to prevent. Symlinks are scanned as **the target path git actually stores**, not the pointee. **Repository-controlled exemptions are zero, and the gate checks that before printing it** — a discovered `.gitleaks.toml` (in either mode) or a set `GITLEAKS_CONFIG` **fails the run** rather than being silently honoured, because a printed-but-unchecked security claim is worse than an absent one. The wording is deliberately narrow: goppi can prove *it* exempts nothing; gitleaks' own stopwords and entropy filters remain, and are in fact why zero was reachable. Zero is reachable at all because the measurement found the whole false-positive surface to be **one fixture line**, corrected at the source instead of exempted (fidelity cost zero: `secret-guard` is a regex matcher, and the corrected value is still blocked under the same rule). Falsifiable rather than asserted: a **canary of runtime-generated real-shaped credentials must be caught**, a gitignored secret must not block, an untracked-but-committable one must, findings are **redacted** so the gate cannot publish what it detects, and a **scanner that fails to complete FAILs the gate** instead of reading as "found nothing". Under `--ci` an **absent scanner FAILs**, and locally it exits **3 = BLOCKED** so `check.sh` says "not fully proven" rather than ok — never a green tick over an unrun check. Scanner delivered as a **checksum-pinned MIT binary, no sudo, no third-party action** (`gitleaks-action` rejected: minified bundle under a commercial EULA with repo access). **Extended 2026-07-28 (#89, ADR-0032 ⓛ) with a second point in the lifecycle**, because the tree scan was measured missing a case entirely: a secret added in one commit and removed in the next reads clean to `check.sh` *and* to CI while sitting in the pushed history. `hooks/git/pre-push.sh` — **opt-in, installed by hand, never planted by `scaffold`** — runs `secret-scan.sh --range` over exactly the commits a push would publish, catching that case before the credential leaves the machine, which is the moment rotation becomes unavoidable. It holds **no rules of its own**: it computes a commit range and calls the same script CI calls, so a local hook and CI cannot disagree about what a secret is. **Rule currency has a mechanism since 2026-07-28 (#94)**, rather than the bare "maintenance item" it was: dependabot **structurally cannot** watch a version inside a `run:` step (its ecosystems are a fixed list with no regex manager — checked, not assumed), so `.github/workflows/pin-currency.yml` compares the pin against gitleaks' latest release on a monthly schedule and **fails when it falls behind**. The comparison itself (`evals/pin-currency.sh`) is a **pure, network-free** script fixture-tested by `check.sh`, so the unified gate stays runnable offline; only the scheduled job touches the network, and being scheduled it cannot block a merge. **Adequate for the committable tree and for what a push publishes; the remaining ceilings are `--no-verify` (tested), stale-tracking-ref narrowing (measured) and the alarm's own lag of at most one month, all under Residual.** |
| T11 | **Tampering — hook scripts altered on disk** | anything with write access to the plugin dir runs code as the user at every tool call | **Partial, and unequal between hosts.** Codex requires the user to **review and trust the hook hash** via `/hooks` before hooks fire (`hosts/codex/README.md`, `operations.md`). **Claude Code has no equivalent hash-trust step** — hooks from an installed plugin run once loaded, so on Claude this threat is **unmitigated**. Asymmetry is inherent to the hosts, not a goppi defect; triaged under Residual below rather than left in the table as a half-answer. |

## Secret flow

goppi handles **no secrets of its own** — no token, no credential store, no
remote sink. Its only relationship with secrets is defensive, in three layers
whose strength is unequal and stated as such (design §4.3): permission `Read()`
denies bind the host's *file tools only* and **do not reach Bash subprocesses**;
`secret-guard` is *input friction* on literal patterns; the **sandbox `denyRead`
set (Claude, while on) and the committed `:root="deny"` profile (Codex, always
on once the folder is trusted) are the actual boundary**.

If goppi ever gains a credential of its own — a publish token, marketplace auth —
this section must be rewritten *before* that code ships, not after.

## Findings

**Fixed in this pass** (bounded, by the session contract, to documentation and
the permission surface already being edited):

- **G1 — snapshot exposure outside scaffolded projects.** T3's mitigation reaches
  projects that ran `scaffold`. A **brownfield** project, or any repo where a user
  simply installed the plugin, gets PreCompact snapshots written into its tree
  with no ignore rule — and the hook cannot add one itself without violating the
  no-clobber rule (T2). Recorded as a documented limitation in
  `hooks/README.md` this session rather than silently carried.
- **G3 — plugin-cache version skew.** Recorded here and in `hooks/README.md`: the
  skill a session executes may not be the one in the tree being edited, so a
  fixed rule can keep failing until the cache turns over. No detection exists.
  **And the obvious check is not one (observed 2026-07-28, third first-hand
  occurrence).** `~/.claude/plugins/installed_plugins.json` read
  `0.17.0 @ 3906d25` — matching `HEAD` exactly — while the skill body that actually
  loaded came from the `0.16.2` cache directory. A session that checks the registry
  and finds it current will conclude there is no skew **and be wrong**. So the
  registry is not a detection method for G3; the only reliable signal seen so far is
  the path a skill reports when it loads. Recorded because the sharper form is the
  useful part: not merely "skew happens" but "the check you would reach for does not
  see it".
  **A working check, and a corrected number (2026-07-29 Session M, re-confirmed
  2026-07-30 Session N).** `diff -rq` between the cached version's `skills/` and the
  tree answers the question the registry cannot: on both dates it exited **0**
  (byte-identical), so the bodies being measured were the tree's — and on 2026-07-30
  the registry SHA was two commits *behind* `HEAD` while the bodies were still
  identical, because those commits touched only documentation. So the pair to run is
  `diff -rq` **plus** `git diff --name-only <registry-sha>..HEAD` filtered to loaded
  paths; the registry SHA alone is neither necessary nor sufficient.
  **Cache size — a trend, not a snapshot** (`~/.claude/plugins/cache/goppi/goppi/`,
  counted each time; nothing prunes the cache, so every released version stays on disk):
  **up to 15 versions on 2026-07-27** (0.1.1 … 0.15.0, tree at 0.16.1) → **20 on
  2026-07-29** (0.1.0 … 0.20.2) → **20 on 2026-07-30** → **21 on 2026-07-31**
  (0.1.0 … 0.21.0, Session O; it went from 20 to 21 *during* that session as 0.21.0
  was cached). The number moves in the worse direction on its own, which is the
  argument for this row. Written into the tree because it had been recorded only in
  session-local files, which is how PR #115's review report was lost.
  **The skew runs in BOTH directions, and the second one was observed 2026-07-31
  (Session O).** The `review` skill reported its own base directory as
  `~/.claude/plugins/cache/goppi/goppi/0.20.2/skills/review` — the **0.20.2** cache —
  **while the registry read `0.21.0 @ 71c0a33`**: the registry *ahead* of what
  actually loaded, the mirror
  image of Session N's case above. A session that had checked only the registry would
  have concluded it was running 0.21.0's bodies and been wrong about which directory
  executed. No behavioural skew that time: `diff -rq` of `0.20.2/skills` against the
  tree also exited **0**. Recorded because it is this row's own thesis in a new
  direction — **the check you would reach for does not see it, whichever way the drift
  runs**, and only the path a skill reports when it *loads* did. Same day, the
  registry also sat at **0.21.0 while the tree was at v0.23.0**, so it lags releases
  as well as leading loads.
  ⚠️ **Correction, and the method error is the useful part.** An earlier version of
  this paragraph (landed 2026-07-30, #124) claimed the 15 figure existed *"nowhere in
  this repo"*. **It does exist** — as a dated measurement, in the session backlog. Two
  things went wrong and only one was the handoff's fault: the handoff mis-attributed
  the figure to *this row* (this row said only "No detection exists", so that part of
  the correction stands), but the number itself was real. The claim that it existed
  nowhere came from reading a **`grep … | head -5`** as exhaustive — the search
  returned **six** matches and the one that mattered was in the truncated tail. A
  universal negative was asserted from a deliberately bounded search. Rule that
  follows: **never claim absence from a search that was capped, filtered to one file
  type, or piped through `head`** — re-run it uncapped and over the whole tree first.

**Backlog, with grounds for not fixing here** — each was real; each needed code and
its own verification, which was outside Session H's stated blast radius. **All three
are now closed** — G2 and G4 by Session I (#75), G5 by Session K (#85) — and each is
struck through below with what actually shipped and what it did *not* buy. The
grounds for deferring are kept, not deleted: in every case the deferral bought a
measurement that changed the answer.

- ~~**G2 — `scaffold`'s no-clobber guarantee is prose, not code.**~~ → **FIXED
  2026-07-26 (#75, ADR-0030).** The finding stands as written: gingoa enforced the
  same intent mechanically (`requireObjectOrAbsent` / `backUpOnce` /
  `filterOwned`), goppi's equivalent was a model instruction, and the failure was
  not detectable afterwards. **The port was rejected on architecture** — those are
  engine internals and `scaffold` has no write path — so the promise was made
  *falsifiable* instead of enforced: `evals/additive-only.sh`, read-only, wired as
  a Path B completion gate, blocking on the control surface. A `PreToolUse` hook
  was rejected as **intent-blind** (the same write is correct or catastrophic
  depending on an intent no hook can see) and a pre-write backup helper as still
  advisory; ADR-0030 records both with grounds. **Remaining ceiling, deliberately
  not claimed away**: under `--git` it cannot see content that was never
  *committed* (`.claude/settings.local.json` is gitignored by design — such paths
  are named at the end of a run, and `--baseline` is the answer), it does not
  judge whether an *addition* was wise, and it judges a result rather than
  preventing the write — which is defensible here, unlike the secret case
  (ADR-0008), only because the harm is recoverable and the gate refuses to certify
  a run with no before-state.
- ~~**G4 — `goppi-doctor` cannot tell a weaker posture from goppi's.**~~ →
  **FIXED 2026-07-26 (#75).** Equivalence is now compared against goppi's own
  committed set — one home, no third copy — by control class rather than literal
  string, and the summary line no longer reports a bare "PRESENT ✓" over a posture
  that is not proven equivalent. **Severity is the residual, and it is a choice,
  not an oversight**: on Claude a weaker posture **warns** (naming each uncovered
  control) because an *absent* Claude posture is only a warn here — the real
  Claude boundary is the session sandbox (§4.3) — so failing "weak" while warning
  "absent" would be incoherent. Only unparseable settings FAIL. On Codex, where an
  absent rules file is already a FAIL, a rules file with no restrictive decision
  FAILs too. Verified against **nine real project trees** with the pre-change
  script run side by side: **identical FAIL sets, zero new blocks** (design §11's
  zero-false-block goal binds goppi's own gates).
- ~~**G5 — no secret scanning in goppi's own CI.**~~ → **FIXED 2026-07-28 (#85,
  ADR-0032).** The finding stands as written, and so does the reason it was
  deferred twice: a scanner is a new blocking gate whose false-positive behavior
  must be measured before it blocks merges. **That measurement is what decided the
  design, and it contradicted the premise it was run to confirm.** The expectation
  — recorded going in as confirmed, with a file count attached — was that this
  repo's deliberate credential-shaped fixtures would light up any scanner, making
  the *allowlist* the real design surface. Measured (`gitleaks 8.30.1`, default
  rules, `results/2026-07-28-k1-secret-scan-fp-baseline.md`): **tree = 1 finding,
  full history = 4, all four the same line.** The other fixtures do not fire for
  reasons that were **probed rather than assumed** — the AWS example key is
  stopword-allowlisted inside gitleaks (one changed character makes it fire) and
  the all-`A` token fails an entropy filter (an entropic token of identical shape
  fires). So the exemption surface was one line, it was **corrected at the source**,
  and the landed **allowlist is zero entries wide** — the gate prints that fact
  rather than leaving it to memory. Detection was measured in the opposite
  direction too (**5 of 6** runtime-generated real credentials caught) and is held
  there by a committed canary, because a gate with no false positives is trivially
  achievable by detecting nothing. **Remaining ceiling, deliberately not claimed
  away**: this scans the **committable tree, not history**, so a secret introduced
  and then removed within one branch is still in the pushed commits and this gate
  will not see it — `--history` runs that scan as an **audit**, kept out of
  `check.sh` for two reasons, the second found by this PR's own review: an immutable
  commit's finding could only ever be *exempted*, and **a history scan's result is a
  property of the clone rather than the repository** (`gitleaks git` follows refs, and
  a long-lived clone carries stale remote-tracking refs for branches deleted on origin
  — measured at 4 findings across 137 commits in the author's clone against 1 across 55
  on a fresh one; pruning stale refs closes most of the gap but not all of it, since
  local branches for squash-merged PRs survive it), so it would hand
  different verdicts to the maintainer, CI and a new contributor on identical code. Content also comes from the **worktree, not the
  index**, so a staged-then-unstaged secret is invisible locally (CI closes that by
  scanning the checked-out commit). Detection is only as current as a **version pin
  that does not auto-update**, and the earlier-firing option (GitHub push protection)
  is unavailable to a private personal-account repo — **re-open if goppi goes
  public.**

## Where this overlaps Session A, and what is new

Session A (2026-07-24, issue #48) answered an external critique on the
**credential-read** surface: workspace-secret `denyRead` parity, the secret-PATH
friction extension, `goppi-doctor` failing on unparseable rules and a missing
profile, and the runtime-state gitignore. Those are T4, T7 and part of T3 above,
and they are **not re-litigated** — they are cited as mitigations that already
hold.

What this pass adds is the surface nobody had enumerated: **T1** (sync
truncation), **T2/G2** (planting into a tree goppi does not own), **T6/G3**
(distribution and version skew), **T10/G5** (goppi's own supply chain), **T11**
(hook-trust asymmetry between hosts), and the explicit statement that goppi holds
no credentials and emits no traffic — a claim worth having verified and dated
rather than assumed.

## Residual / out-of-scope (tracked, not silently dropped)

- ~~**T10's gate detects, it does not prevent — tracked in issue #89.** `secret-scan.sh`
  blocks in CI, by which point the credential is already in a pushed commit and
  rotation is required regardless. A `pre-commit` hook would fire before the object
  exists; ADR-0032 compared scanner, exemptions and tree-vs-history but **never
  compared where in the lifecycle the gate sits**, so that axis is undecided rather
  than rejected.~~ → **RESOLVED 2026-07-28 (#89, Session L)** — and the entry above was
  *understating* it. Measured: a secret added in one commit and removed in the next was
  caught by **nothing** — tree scan clean, CI clean, credential in the pushed history
  (verified against a real bare remote and a fresh clone). So the axis was not merely
  undecided; leaving it undecided was hiding a gap. Decided in **ADR-0032 ⓛ** after
  comparing `pre-commit` · `pre-push` · CI-only: an **opt-in `pre-push` hook**
  (`hooks/git/pre-push.sh`) scans the commits a push is about to publish, via
  `secret-scan.sh --range` — the same script, same rules, so the two cannot fork.
  **`scaffold` plants nothing** into repositories goppi does not own (ⓛ-4).
  **New ceilings, replacing the old one and equally named:** `git push --no-verify`
  defeats the hook (tested, not merely stated) so it is an *earlier catch*, never
  prevention — CI stays the enforcing layer; and for a branch the remote does not have
  yet, a **stale remote-tracking ref narrows the scanned range**, bounded by the fact
  that anything it hides was published by an earlier push. This still does not re-open
  G5, and the "zero open findings" line above still must not be read as "nothing left
  to improve".
- **T10's rule currency now has an alarm, and the alarm has its own two ceilings —
  tracked here rather than implied (#94, 2026-07-28).** `.github/workflows/pin-currency.yml`
  compares the pinned gitleaks version against the latest release **weekly**, and fails
  when it falls behind; dependabot structurally cannot do this (fixed ecosystem list, no
  regex manager — checked, not assumed). Ceiling one: **lag of up to about a week**, the
  schedule's period. ~~Ceiling two, and the weaker link: **the alarm reaches a human only
  through GitHub's failed-workflow notification, which is a per-account setting this
  repository cannot see or verify.**~~ → **CLOSED 2026-07-29 (#99).** The job now opens
  (or force-updates) a **pull request** carrying the bump, so the signal is
  repository-visible state rather than an email nobody can verify was sent. De-duplication
  is a fixed branch name; the digest comes from the release's own `checksums.txt`; the
  edit is applied by a pure, fixture-tested script that reads the file back rather than
  trusting `sed`. **It does not merge** — a rule-set change alters what the gate detects,
  so a human stays the merge gate by design. **Remaining ceiling, measured**: a PR opened
  by `github-actions[bot]` does not start its own checks automatically; they queue as
  `action_required` until a maintainer approves, so verification is *one click away*
  rather than automatic. **That click is kept on purpose** (2026-07-29): removing it
  needs either a stored write-capable token — which would contradict this document's
  own "goppi handles no credentials of its own" and place that token inside the secret
  scanner's supply chain — or a merged-on-evidence-without-checks path, which this
  document already treats as a weakness elsewhere. Grounds and both rejected
  alternatives are in ADR-0032's currency consequence. Verified end to end 2026-07-29 against a deliberately stale pin
  on a throwaway branch: the PR appeared, `pr-body` skipped by its bot exemption,
  `pr-title` passed, and `ci` **caught a real defect** in the change that produced it.
  De-duplication was demonstrated the way the criterion asked — by running it **twice**:
  two runs, exactly **one** open PR, and the second run left the branch alone
  (`already carries 8.30.1 — leaving it untouched`) rather than force-pushing over
  what a reviewer might have committed there.
  Re-open this if the PR is ever seen to not appear, or if it appears and is ignored for
  more than one cycle.
- **The unit of every claim in this document is the SURFACE, not the host (#106,
  2026-07-29).** `secret-guard` is live on Claude Code and on the Codex **CLI**, and
  **does not fire at all on Codex desktop** — measured with one command across all
  three. goppi's registration, trust, matcher and script are correct; the desktop path
  does not dispatch `PreToolUse`, and `openai/codex#21639` (OPEN) names it externally.
  **Two consequences worth keeping in view.** First, the repo could carry "verified on
  Codex" for months because its evidence was Codex-shaped payloads piped into the
  scripts — that proves parsing, reaches no dispatcher, and is why `check.sh`'s
  `ok: hooks … Codex-shaped payloads` stayed green while one supported surface ran
  unguarded (that line is corrected in this same change to say **PARSE**, and to say what
  it is not proof of). Second, **the detection inherits the control's hole**: `deploy-check`, the
  advisory that exists to warn when the posture is incomplete, is dispatched by the same
  machinery, so on the surface where the warning is needed it cannot fire. Per-event
  confidence, not flattened: `PreToolUse` **CONFIRMED failing** · `SessionStart` failing
  per external repro, **not confirmed locally** · `PreCompact` **INCONCLUSIVE**.
  Re-open scope when #21639 closes: re-drive the three surfaces rather than assuming the
  fix. Deliberately **not** in this entry: a self-probe detection layer — bundling an
  unargued detection layer into a change whose thesis is *stop claiming what you have not
  verified* would repeat that mistake one altitude up.
  **Reporting upstream: DECIDED 2026-07-29 (#109) — no, with a ground rather than a
  shrug.** Measured before deciding: `openai/codex#21639` is OPEN, last updated
  2026-07-28, **24 comments**, and every data point this repository holds is already in
  that thread — externally reproduced, CLI works, the Desktop app-server path fails,
  relocating hooks does not help. A confirmation comment would add a count, not
  information, and external contact costs an approval each time. **Re-open if that stops
  being true**: a narrower localization, a surface the thread has not covered, or a
  reproduction on a build it has not seen would be new information and worth sending.
  **Also deferred, and named here rather than left in a commit message — this section's
  rule is "tracked, not silently dropped":** a **sweep of every remaining "verified on
  host X" claim** in the repo. #106 bounded itself to T4, this entry, the Codex parity
  table, `design.md` §8 and `hosts/codex/operations.md`. Still carrying the flattened
  per-host unit, at minimum: `README.md` ("live-verified on both hosts") and its Korean
  counterpart `README.ko.md`, plus every `## Expiry conditions` block phrased per host.
  Those are claims about *the repo's landing page*, so the sweep is worth its own issue
  rather than an opportunistic edit.
- **Runtime prompt injection** against a session using goppi — the sandbox's job
  (`references/sandbox-presets.md` Preset U, the untrusted-input trigger), not
  this document's. The 24/25 credential-theft evidence is why model-layer defense
  is not counted here at all.
- **Whether the contract text changes model behavior** is a measurement question
  (§11), not a security property. A threat model must not launder advisory prose
  into a control.
- **Org-level enforcement.** Everything goppi ships is user-trustable and
  user-revocable by design. Un-bypassable enforcement needs a managed
  `requirements.toml` (Codex) or managed settings (Claude) — the user's
  administrator, not goppi.
- **T11 on Claude Code — accepted, and it is not goppi's to close.** An attacker
  who can write to the plugin cache can already run code as the user by many
  other routes, so goppi's hooks are not the marginal exposure; and the host
  offers no hash-trust primitive to bind them to even if it were. Codex's
  `/hooks` trust step is the mitigation where one exists. **Re-open if Claude
  Code ships a hook-integrity mechanism** — at that point declining to use it
  would become a goppi defect rather than a host gap.

## Re-review trigger

Re-run this pass when any of these fire: goppi gains a credential or any network
egress · a new hook or host is added · the distribution path changes (a
non-local marketplace source) · `scaffold` gains write behavior beyond additive
file creation · a G-item above is fixed (update the row, don't delete the
history).
