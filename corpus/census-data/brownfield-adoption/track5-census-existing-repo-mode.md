# Track 5 (raw) — Census: existing-repo mode across 51 tools

Quantitative 전수조사 (51 tools: scaffolders · generators · spec-driven · IDP · harness · language-native init) of
how each handles being run against an EXISTING (non-empty) project vs a new one. Method: `gh api` stars (point-in-time)
+ official docs/READMEs + web verification. Primary strategy recorded where a tool spans several; 3 genuinely unknown
(sao, boilr, tessl) marked so, not guessed.

## Stats (n = 51)
- **Existing-repo mode:** yes **38 (74.5%)** · no 10 · unknown 3 → of 48 determinate, **79% support existing-repo**.
- **Collision (primary):** refuse-unless-forced **15 (29%)** · prompt-per-file **14 (28%)** · skip/additive-into-namespace 7 ·
  n/a (LLM harness / zip) 5 · unknown 4 · **3-way-merge 3 (6%)** (copier, cruft, mrm) · silent-overwrite 3 (6%) · backup 0.
- **Ownership baseline:** has one **6 (12%)** — answers-file ×4 (copier `.copier-answers.yml`, cruft `.cruft.json`,
  yeoman+jhipster `.yo-rc.json`), template-ref ×2 (projen `.projenrc`, backstage `catalog-info.yaml`) · none 44 · unknown 1.
  (config files like `nx.json`/`package.json` do NOT count — no template lineage.)
- **Brownfield docs mode (spec-driven, n=6):** reverse-engineer 3 (kiro, BMAD, agent-os) · fresh/manual 3 (spec-kit core,
  OpenSpec delta-specs, tessl) · import 0 in-set (+1 outside: backstage register).
- **Verb families:** refuses-non-empty ~8 · in-place `init`/cwd ~12 · dedicated `update`/reconcile 2–3 (copier, cruft; projen
  regen) · `add`/`init`-to-existing ~4 (astro add, ng add, nx init/import, specify init --here) · generator-into-existing ~8 ·
  `--force`/`--overwrite` clobber flag ~8 · spec reverse-engineer verb 3.

## Findings (de-facto standard)
1. **Existing-repo is the norm (~75%), but almost none do true RECONCILIATION** — most brownfield support is either a blunt
   `--force` clobber or an add-one-thing generator (`ng add`/`astro add`/plop). Whole-project template-lineage UPDATE is rare.
2. **Gold standard for brownfield template updates = copier/cruft: committed answers-file + 3-way merge vs template git
   history.** Only 3 tools do a real merge (copier, cruft, ~mrm codemods). **Validates ADR-0003/0017's copier choice.**
3. **Ownership/lineage baseline is uncommon (~12%) but the convention when present is unambiguous: a committed answers file
   at repo root** (`.copier-answers.yml` = reference). gingoa's baseline choice is mainstream.
4. **Collision handling is safe-by-default:** refuse-unless-forced (29%) or interactive prompt (28%) dominate; silent
   overwrite (6%) and 3-way-merge (6%) both rare. **Never clobber by default** — supports gingoa's additive-first / conflict-
   surface-don't-clobber.
5. **A distinct verb for brownfield is an emerging convention, not an edge case:** `cargo new` vs `init`, copier `copy` vs
   `update`, `nx init`/`nx import`, backstage scaffold vs register. **Strong prior art for a separate `adopt` verb** (not
   `scaffold --overwrite`).
6. **Spec-driven/AI tools converge on: additive install into a reserved namespace dir** (`.specify`/`.kiro`/`.bmad`/
   `.openspec`/`.agent-os`) so adoption COEXISTS. Docs story splits 3 ways: reverse-engineer from code (kiro, BMAD
   document-project Phase 0, agent-os discover-standards) · incremental hand-authored delta specs (OpenSpec) · drop generic
   templates (spec-kit core). Leading pattern for the docs question = **reverse-engineer/document existing state as a
   mandatory first phase**.

Caveats: 51 is broad not exhaustive; primary-strategy tallies flatten multi-mode tools (directional); spec-driven cluster <1yr
old + fast-moving; language-native subcommand stars = parent toolchain repo.

## Records (JSON)
```json
[
  {"name":"yeoman","stars":3959,"category":"generator","existing_repo_mode":"yes","verb":"runs-in-cwd","collision":"prompt","ownership":"answers-file(.yo-rc.json)"},
  {"name":"plop","stars":7669,"category":"generator","existing_repo_mode":"yes","verb":"add/modify/append","collision":"skip","ownership":"none"},
  {"name":"hygen","stars":5935,"category":"generator","existing_repo_mode":"yes","verb":"inject","collision":"skip","ownership":"none"},
  {"name":"degit","stars":7889,"category":"scaffolder","existing_repo_mode":"no","verb":"--force","collision":"refuse","ownership":"none"},
  {"name":"nx","stars":28969,"category":"generator","existing_repo_mode":"yes","verb":"nx init / nx import","collision":"prompt","ownership":"none","docs_mode":"import"},
  {"name":"projen","stars":2937,"category":"generator","existing_repo_mode":"yes","verb":"regenerate-from-.projenrc","collision":"overwrite","ownership":"template-ref(.projenrc)"},
  {"name":"sao","stars":1047,"category":"scaffolder","existing_repo_mode":"unknown","collision":"unknown","ownership":"none"},
  {"name":"mrm","stars":1645,"category":"generator","existing_repo_mode":"yes","verb":"mrm <task>","collision":"3way-merge","ownership":"none"},
  {"name":"create-next-app","stars":140212,"category":"scaffolder","existing_repo_mode":"no","verb":"new","collision":"refuse","ownership":"none"},
  {"name":"create-t3-app","stars":29024,"category":"scaffolder","existing_repo_mode":"no","verb":"new","collision":"refuse","ownership":"none"},
  {"name":"cookiecutter","stars":24978,"category":"scaffolder","existing_repo_mode":"yes","verb":"--overwrite-if-exists/--skip-if-file-exists","collision":"overwrite","ownership":"none"},
  {"name":"copier","stars":3444,"category":"scaffolder","existing_repo_mode":"yes","verb":"copier update","collision":"3way-merge","ownership":"answers-file(.copier-answers.yml)"},
  {"name":"cruft","stars":1576,"category":"scaffolder","existing_repo_mode":"yes","verb":"cruft update / link","collision":"3way-merge","ownership":"answers-file(.cruft.json)"},
  {"name":"cargo-generate","stars":2434,"category":"scaffolder","existing_repo_mode":"yes","verb":"generate --init","collision":"unknown","ownership":"none"},
  {"name":"giter8","stars":1752,"category":"scaffolder","existing_repo_mode":"no","verb":"g8","collision":"refuse","ownership":"none"},
  {"name":"mason","stars":1127,"category":"generator","existing_repo_mode":"yes","verb":"mason make --on-conflict","collision":"prompt","ownership":"none"},
  {"name":"boilr","stars":1763,"category":"scaffolder","existing_repo_mode":"unknown","collision":"unknown","ownership":"none"},
  {"name":"gonew","stars":7977,"category":"language-native-init","existing_repo_mode":"no","verb":"gonew","collision":"refuse","ownership":"none"},
  {"name":"scaffdog","stars":769,"category":"generator","existing_repo_mode":"yes","verb":"generate","collision":"prompt","ownership":"none"},
  {"name":"tiged","stars":466,"category":"scaffolder","existing_repo_mode":"no","verb":"--force","collision":"refuse","ownership":"none"},
  {"name":"cargo","stars":15180,"category":"language-native-init","existing_repo_mode":"yes","verb":"init(cwd) vs new(dir)","collision":"refuse","ownership":"none"},
  {"name":"dotnet new","stars":3160,"category":"language-native-init","existing_repo_mode":"yes","verb":"new --force","collision":"refuse","ownership":"none"},
  {"name":"npm init","stars":9900,"category":"language-native-init","existing_repo_mode":"yes","verb":"init(cwd)","collision":"prompt","ownership":"none"},
  {"name":"go mod init","stars":134899,"category":"language-native-init","existing_repo_mode":"yes","verb":"mod init(cwd)","collision":"refuse","ownership":"none"},
  {"name":"rails new","stars":58589,"category":"language-native-init","existing_repo_mode":"yes","verb":"new; --force/--skip","collision":"prompt","ownership":"none"},
  {"name":"django startproject","stars":87921,"category":"language-native-init","existing_repo_mode":"yes","verb":"startproject name .","collision":"refuse","ownership":"none"},
  {"name":"flutter create","stars":177513,"category":"language-native-init","existing_repo_mode":"yes","verb":"create .","collision":"overwrite","ownership":"none"},
  {"name":"dart create","stars":11194,"category":"language-native-init","existing_repo_mode":"yes","verb":"create --force","collision":"refuse","ownership":"none"},
  {"name":"mvn archetype:generate","stars":5120,"category":"language-native-init","existing_repo_mode":"no","verb":"archetype:generate","collision":"refuse","ownership":"none"},
  {"name":"Spring Initializr","stars":3692,"category":"language-native-init","existing_repo_mode":"no","verb":"zip","collision":"n/a","ownership":"none"},
  {"name":"composer create-project","stars":29478,"category":"language-native-init","existing_repo_mode":"no","verb":"create-project","collision":"refuse","ownership":"none"},
  {"name":"spec-kit","stars":117117,"category":"spec-driven","existing_repo_mode":"yes","verb":"specify init --here/--force","collision":"prompt","ownership":"none","docs_mode":"fresh(brownfield via community ext)"},
  {"name":"kiro","stars":3954,"category":"spec-driven","existing_repo_mode":"yes","verb":"design-first analyze","collision":"skip","ownership":"none","docs_mode":"reverse-engineer"},
  {"name":"BMAD-METHOD","stars":49954,"category":"spec-driven","existing_repo_mode":"yes","verb":"document-project/brownfield","collision":"skip","ownership":"none","docs_mode":"reverse-engineer"},
  {"name":"OpenSpec","stars":58190,"category":"spec-driven","existing_repo_mode":"yes","verb":"openspec init (delta specs)","collision":"skip","ownership":"none","docs_mode":"fresh(delta)"},
  {"name":"agent-os","stars":4993,"category":"spec-driven","existing_repo_mode":"yes","verb":"/discover-standards","collision":"skip","ownership":"none","docs_mode":"reverse-engineer"},
  {"name":"tessl","stars":69,"category":"spec-driven","existing_repo_mode":"unknown","collision":"unknown","ownership":"unknown","docs_mode":"fresh"},
  {"name":"claude-flow","stars":62430,"category":"harness","existing_repo_mode":"yes","verb":"runs-in-cwd","collision":"n/a","ownership":"none"},
  {"name":"aider","stars":46926,"category":"harness","existing_repo_mode":"yes","verb":"runs-in-cwd","collision":"n/a","ownership":"none"},
  {"name":"continue","stars":34629,"category":"harness","existing_repo_mode":"yes","verb":"IDE assistant","collision":"n/a","ownership":"none"},
  {"name":"opencode","stars":181308,"category":"harness","existing_repo_mode":"yes","verb":"runs-in-cwd","collision":"n/a","ownership":"none"},
  {"name":"backstage","stars":33756,"category":"IDP","existing_repo_mode":"yes","verb":"register-existing (catalog-info.yaml) vs scaffolder(new)","collision":"skip","ownership":"template-ref(catalog-info.yaml)","docs_mode":"import"},
  {"name":"jhipster","stars":22423,"category":"generator","existing_repo_mode":"yes","verb":"regenerate; --force","collision":"prompt","ownership":"answers-file(.yo-rc.json)"},
  {"name":"angular-cli","stars":27018,"category":"generator","existing_repo_mode":"yes","verb":"ng add/generate/update","collision":"prompt","ownership":"none"},
  {"name":"redwoodjs","stars":17615,"category":"scaffolder","existing_repo_mode":"yes","verb":"create(new)/rw generate(existing)","collision":"prompt","ownership":"none"},
  {"name":"blitzjs","stars":14129,"category":"scaffolder","existing_repo_mode":"yes","verb":"new / generate","collision":"prompt","ownership":"none"},
  {"name":"create-expo-app","stars":50376,"category":"scaffolder","existing_repo_mode":"no","verb":"create; prebuild=add-native","collision":"refuse","ownership":"none"},
  {"name":"create-vue","stars":4372,"category":"scaffolder","existing_repo_mode":"yes","verb":"prompt; vue-cli --merge/--force","collision":"prompt","ownership":"none"},
  {"name":"nuxi init","stars":60476,"category":"scaffolder","existing_repo_mode":"yes","verb":"init; -f","collision":"prompt","ownership":"none"},
  {"name":"create-remix","stars":33148,"category":"scaffolder","existing_repo_mode":"no","verb":"create; --overwrite","collision":"refuse","ownership":"none"},
  {"name":"create-astro / astro add","stars":60638,"category":"scaffolder","existing_repo_mode":"yes","verb":"astro add(existing)/create(new)","collision":"prompt","ownership":"none"}
]
```
