# Track 1 (raw) — Scaffolder / code-generator brownfield modes

Research thread for the greenfield-vs-brownfield **adoption model** (②foundation focus). How generators handle
running against an EXISTING project vs a new one: verb, collision strategy, ownership baseline, carry-forward.

## Per-tool table

| Tool | Brownfield | Verb / entry | Collision strategy | Ownership baseline | Evidence |
|---|---|---|---|---|---|
| **copier** | Partial — `update` needs prior baseline; `copy` on existing = binary; no shipped `adopt` | `copy` (init), `update` (lifecycle), proposed `adopt` (open #2486) | `update`: **3-way merge** (old-render base + user project + new-render); `--conflict inline` (git markers, default) or `rej`. `copy`: skip/overwrite binary | `.copier-answers.yml`: `_src_path`, `_commit` (exact tag/SHA of last render — the merge-base key), all answers | copier docs: Updating / Configuring; #2486 |
| **cruft** (cookiecutter ext) | YES — `cruft link` = the explicit brownfield entry verb | `create`/`update`/`link` (adopt)/`check` (CI audit) | `update`: git diff/patch old→new; 3-way merge, `.rej` fallback; interactive accept/reject | `.cruft.json`: `template`, `commit` (SHA at adoption), `context` (answers), `skip` (glob array) | cruft.github.io; cruft #181 |
| **Yeoman** | YES — runs against any dir; no separate adopt verb | `yo <gen>` | Per-file interactive prompt: overwrite/skip/overwrite-all/quit/diff; `--force` non-interactive. No merge | **None** — no memory of what it generated | yeoman.io/authoring/file-system |
| **Nx** | YES — `nx init` designed for incremental adoption of existing repos | `nx init`, `nx g <gen>` | No standard protocol; per-generator in-memory tree, skip/overwrite by code; no enforced prompts | `nx.json`+`project.json` track config intent, not template lineage | nx.dev start-with-existing-project / import-project |
| **Plop** | Limited — targets existing dirs but file-exists = FAIL by default | `plop` | FAIL on existing (default); `force:true`/`--force` overwrite. No merge/diff/prompt | **None** | plopjs.com; plop #32 |
| **Hygen** | Partial — `inject` appends non-destructively; `add` varies | `hygen <gen> <action>` | `add`: `HYGEN_OVERWRITE` env (presence-only) — unset aborts, set overwrites; `inject` appends safely. No merge | **None** | hygen #113/#115 |
| **degit** | NO — aborts on non-empty dest | `degit <repo> <dest>` | ABORT if non-empty (default); `--force` blind overwrite. No merge | **None** | degit #231 |
| **create-next-app / CRA** | NO — assumes empty target; whitelist of acceptable pre-existing files (`.git` etc.), refuses otherwise | `create-next-app [dir]` | REFUSE if non-whitelisted files present. CRA `eject` = one-way sever from template mgmt | **None** (`package.json` ≠ lineage) | nextjs create-next-app; CRA #7802 |

## Copier 3-way merge (the reference algorithm)
Three states: **base** = re-render from OLD template (`_commit` checkout) · **ours** = project on disk · **theirs**
= re-render from NEW template. Diff(base→ours) = user customizations, re-applied over (base→theirs); overlaps →
conflict markers (`--conflict inline`) or `.rej` (`--conflict rej`). Dest must be a clean git tree. `.copier-answers.yml`
`_src_path`+`_commit` make it work; multiple templates via multiple answers files. Migrations run pre/post keyed to
version thresholds (gated behind `--trust`/`--UNSAFE` — they execute code). **Brownfield gap:** `copier copy` on a
non-empty dir is binary (no `_commit` base); #2486 proposes `copier adopt` via **empty-base 3-way merge** (existing=ours,
template=theirs, empty=synthetic base) → open/unassigned as of 2026-07.

## Cruft `link` (the only shipped brownfield-entry verb)
`cruft link TEMPLATE_REPO` prompts/accepts `--commit` (the SHA the project claims consistency with), writes `.cruft.json`
with that baseline; thereafter `cruft update` patches (baseline→latest) via git 3-way merge, `.rej` on failure. `"skip"`
array = user-owned files exempt from updates. `cruft check` exits non-zero when the project lags template HEAD (CI drift).

## Eject (informational)
Inverse of adoption — CRA `eject` copies internal configs in, removes the dep, permanently severs template management.
No update path after. "Stop being managed" exit, not an entry.

## Principles transferable to gingoa ②
1. **3-state model is the correct algorithm — don't invent alternatives.** copier's base/ours/theirs is the de-facto
   standard; gingoa's post-adoption `update` gets it for free via ADR-0003's copier shell-out.
2. **Ownership file must encode 3 things:** template source · exact commit/version at last render (merge-base key) ·
   answers/context. Without the commit, 3-way merge is impossible. Scaffold must write it on first generation.
3. **3-way disposition (missing→add / equal→skip / different→CONFLICT)** is exactly how the ecosystem resolves
   brownfield. Only "different" is contested: copier/cruft → merge markers; Yeoman → per-file prompt.
4. **"Additive-first" is gingoa's innovation** — no shipped tool formalizes "prefer adding new files over surfacing
   conflicts on existing ones." Formalize as: conflicts surface ONLY on files that are (a) present AND (b) diverged;
   purely-new template files are added silently.
5. **Synthetic empty-base trick** (copier #2486) is the ecosystem consensus for first-time entry — empty tree as merge
   base makes dispositions resolve to add / skip / conflict.
6. **The `skip` list / user-owned zone** is the other half of the baseline — files the manager must never touch.
7. **CI drift detection is first-class** (cruft `check`) — gingoa should expose `gingoa check`/`diff` to fail CI on
   scaffold-version drift.

## Reference standard
**copier** = strongest lifecycle model (3-way merge, answers-file, migrations; already ADR-0003's engine) but leaves the
brownfield ENTRY gap. **cruft** = reference for brownfield ENTRY (`link` + `.cruft.json` commit-pinned baseline).
Practical gingoa path: `adopt` writes `.copier-answers.yml` with a synthetic `_commit` (the template version the project
claims), then delegates lifecycle to `copier update` (which now has a real 3-way base).

## Sources
copier: updating / configuring / DeepWiki answer-file / #2486 adopt · cruft.github.io / cruft #181 / cruft repo ·
yeoman authoring+conflicter+#966 · nx start-with-existing / import-project · plopjs + #32 · hygen #113/#115 ·
degit #231 · create-next-app CLI · CRA #7802 · cookiecutter #784.
