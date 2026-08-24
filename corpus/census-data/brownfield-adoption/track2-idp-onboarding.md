# Track 2 (raw) — Platform engineering / IDP: new-vs-existing & audit mode

Research thread for gingoa's brownfield **②-audit mode**: run the production-floor audit on a non-gingoa tree and
report gaps WITHOUT clobbering. How IDPs distinguish "scaffold a new service" from "onboard/audit an EXISTING one."

## Per-platform summary
| Tool | New vs existing | Onboard mechanism | Audit approach | Impose or measure |
|---|---|---|---|---|
| **Backstage** | Two SEPARATE flows: Scaffolder (new) vs "Register Existing Component" (existing) | `catalog-info.yaml` PR to existing repo — additive, no code change; if absent Backstage PROPOSES a PR (never pushes/overwrites) | Tech Insights: Facts→Checks→Scorecards, continuous, non-blocking, Slack/PR nudges | measures + nudges |
| **Roadie** | Managed Backstage; bulk `catalog:register` PRs via Scaffolder | same + bulk PR | Tech Insights dashboards, continuous | measures + nudges |
| **Cortex** | Scorecard-over-catalog primary; scaffold secondary | `cortex.yaml` auto-discovered via GitHub org scan; additive | Scorecards: Bronze/Silver/Gold LADDER, ALL rules at a level to advance; CQL rules (`git.fileExists(...)`, `sonarqube.metric>80`); aspirational | measures + notifies |
| **OpsLevel** | Maturity-FIRST; creation out of scope | Git integration auto-discovery; no codegen | Org Rubric (ladder) + team Scorecards; **Maturity Report**: pass/fail per level, "Fix This" buttons, notes for complex gaps. **"does not block anything"** | measures + guides |
| **Port** | Catalog-first; GitHub org auto-sync | connect org → auto-discovery; no code mod | Scorecards Basic→Bronze→Silver→Gold; "audit and visibility tools, not enforcement" | measures only |
| **Humanitec + Score** | `score.yaml` added to any repo (new or existing) | add `score.yaml` (additive); orchestrator transforms to target config | no rubric; baseline = binary "has score.yaml" | operationally imposes deploy; onboard additive |
| **CNOE / idpbuilder** | Ref arch (Backstage+ArgoCD+Gitea); new=Templates, existing=catalog-info.yaml+ArgoCD | inherits Backstage PR model | inherits Tech Insights; no own rubric | measures |
| **Kratix** | Promise creation-first; existing via Promise Request → reconcile (adopt-into-management) | Promise Request triggers Configure workflow (more invasive — may modify cluster) | none built-in; compliance embedded in Promise pipeline | **imposes** (governance-through-provisioning) — the outlier |

## Cross-cutting findings
1. **Universal new-vs-existing split:** template/scaffold = greenfield ONLY; existing services are CATALOGED via
   additive metadata, never regenerated. Backstage makes it two explicit UI flows; Cortex/OpsLevel don't even lead with
   scaffolding — they're "existing-service maturity" tools.
2. **Production-floor baseline pattern (strongest signal) = OpsLevel Rubric + Maturity Report:** ordered tiers
   (Bronze/Silver/Gold) = the floor at completeness stages; pass ALL checks at a level to hold it; report surfaces gaps
   (what/why/how-to-fix) but never blocks; team Scorecards allow Day-0 onboarding without org-wide Rubric = exactly the
   "relaxed green gate."
3. **Metadata-addition as the onboarding primitive:** drop ONE yaml (`catalog-info.yaml`/`cortex.yaml`/`score.yaml`),
   commit it — additive, no code change. This IS the ownership-baseline act.
4. **"Propose a PR" not "write directly":** Backstage Register opens a PR proposing the file when absent. Brownfield-safe
   pattern = detect → propose → human approves.
5. **Scorecard-as-audit is universal and explicitly NON-BLOCKING:** Port "audit and visibility, not enforcement"; Cortex
   "aspirational"; OpsLevel "does not block anything"; Backstage Tech Insights nudges, doesn't gate. Industry consensus:
   the floor audit is a REPORTING surface, not a deploy gate; enforcement (if any) is a separate human-decided step.
6. **Kratix = outlier** (imposes via provisioning) — ill-suited as the brownfield-audit analogy.
7. **Gap:** CNOE/Kratix lack first-class "register an existing workload without changing it" docs — a known ecosystem gap.

## Transferable to gingoa ②-audit-mode
| gingoa need | IDP analogue | mechanism |
|---|---|---|
| detect have-vs-required | OpsLevel Rubric pass/fail per level | `reconcileFloor` in READ-ONLY mode: actual tree vs floor items |
| 3-way disposition (present/missing/conflict) | Backstage detect-then-PR; OpsLevel pass/fail + "Fix This" | present=skip, missing=propose-add, conflict=surface delta + human decides |
| additive-first (never clobber) | Backstage Register PR; Cortex cortex.yaml add-only | `adopt` writes only MISSING; CONFLICT surfaced as report, not auto-resolved |
| relaxed green-gate (start RED) | OpsLevel Day-0 team Scorecards; Port "Basic" entry tier | audit passes even at low score; only ADDED items proved green |
| report levels/tiers | OpsLevel Bronze/Silver/Gold; Cortex levels | floor tiers (required/recommended/aspirational) per item category |
| audit-only, non-blocking | universal IDP consensus | `adopt --audit` = no writes, structured gap report (JSON/MD) |
| ownership baseline | catalog-info.yaml commitment = "I own this in the IDP" | `.copier-answers.yml` + ADR-0017 ownership record |
| propose-PR not push | Backstage PR-first | adopt: write MISSING to a branch + open PR (not direct push to main) |

**Strongest transferable model: OpsLevel Rubric + Maturity Report** → gingoa `adopt`: (1) read-only floor scan; (2) maturity
report per-item PASS/FAIL/CONFLICT + level; (3) actionable gaps ("MISSING: CONTRIBUTING.md — governance.contributing,
required"); (4) additive-first resolution (write MISSING to branch, surface CONFLICT); (5) never block, always complete the
report even on a fully non-compliant tree. Port's "Basic" entry tier = a project with zero floor items is still adoptable.

## Sources
Backstage register-a-component / software-templates / catalog / Spotify onboarding / #22162 · Roadie tech-insights + scaffolder-fill-catalog ·
Cortex scorecard product/examples/create · OpsLevel maturity/scorecards/maturity-report/rubric · Port scorecards-and-initiatives / docs ·
Score CNCF acceptance + score-spec · CNOE idpbuilder · Kratix promise workflows · Backstage Soundcheck+TechInsights.
