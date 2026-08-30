# census-data — immutable raw evidence

Raw repo-survey evidence behind the corpus's `[census]` claims. **Append-only: never edit a past census's
records** (add a new census instead). Synthesis lives in the aspect docs; this dir holds the provenance.

## Layout contract (normalized — follow this for every new census)
Each census is a subdirectory `census-<name>/` containing:

| File | Required? | What |
|---|---|---|
| `census.{py,sh}` | yes | the collector/generator (gh API + parsing). **Go-forward name = `census.py` or `census.sh`.** |
| `records.json` | mode A only | raw per-repo records (one object per repo) — the immutable evidence |
| `stats.json` | yes | the aggregated result (flat JSON: `n` + measured %/values; nested arrays for top-N) |

**Two census MODES:**
- **A — record census:** samples N repos, stores a per-repo `records.json` + derived `stats.json`. Used for
  file/feature presence %, archetype splits, commit/PR sampling. (governance · dev-environment · expanded ·
  release-ops · issue-pr · commit-body)
- **B — count census:** aggregate `gh api search/code` `total_count` per filename/path query — measures how
  COMMON a convention is across all of GitHub. No per-repo records (counts files, not repos) → `stats.json`
  only, `census.sh` holds the queries. (doc-conventions)

**Legacy script-name variants** (pre-normalization, left as-is — no external refs): `census-governance.py`,
`census-release-ops.py`, `census-unified.py` (expanded), `render-dev-env.py`+`render-weighted.py` (dev-env).
New censuses use `census.{py,sh}`.

**Methodology** (see `_schema.md §4`): manifest-filtered top-starred software (Munaiah 2017); recency-weighted
`w = 0.5^(age/2yr)` only for censuses whose preserved records contain `createdAt`; non-file foundation via
OpenSSF Scorecard API. Legacy records without `createdAt` are explicitly unweighted, rather than assigned an
invented timestamp.
Count-census numbers are GitHub estimates (default-branch only, auth-gated, `total_count` approximate).

### Uncertainty — measured, and deliberately not extended (2026-08-30)

**Robustness apparatus exists on 1 of 9 censuses** (`census-issue-pr`): Wilson 95% CI,
deterministic owner-cluster bootstrap (2,000 replicates, seeded), star-quartile stratification,
and an honest note that recency weighting is *not* applied because `createdAt` is absent.

🔴 **Extending it to the other eight was considered and rejected — it would not change one judgment.**
The floor asks for a stance only above **20% adoption**. Wilson 95% intervals for every
threshold-adjacent item were computed; **none straddles 20%**:

| item | point | n | 95% CI |
|---|---|---|---|
| `pre-commit` | 5.1% | 6,582 | 4.6 – 5.7 |
| devcontainer | 15.6% | 6,582 | 14.7 – 16.5 |
| `.gitattributes` | 28.9% | 6,582 | 27.8 – 30.0 |
| `FUNDING.yml` | 29.4% | 6,582 | 28.3 – 30.5 |
| Discussions | 39.5% | 6,582 | 38.3 – 40.7 |

At N=6,582 the half-width is **±0.5 – 1.2 pp**. Nothing near the line.

### ⚠️ But stratified numbers are a different story

Small strata carry **±3 – 5 pp**, and that *does* change how two of them may be compared:

| stratum | point | n | 95% CI |
|---|---|---|---|
| `.gitattributes` · cli | 42% | 312 | 36.6 – 47.5 |
| `.gitattributes` · library | 35% | 824 | 31.8 – 38.3 |

The intervals **nearly touch**. *"cli adopts it more than library"* is **weakly supported, not established.**

> 🔴 **Rule: never read two strata as different without checking whether their intervals overlap.**
> A stratified point estimate is a location, not a ranking.

## Integrity and statistical robustness

- `provenance/snapshot-manifest.json` binds normalized record/stat files and executable census code to SHA-256
  hashes. Legacy collection times and API versions that were not recorded remain explicitly `null`.
- Rebuild with `python3 census-data/provenance/provenance.py snapshot`; verify offline with the `validate`
  subcommand. The manifest is an integrity aid, not a substitute for Git history: this research tree is
  intentionally gitignored.
- `census-issue-pr/robustness.json` and `robustness-report.md` add Wilson intervals, owner-cluster bootstrap
  sensitivity, owner-equal estimates, and star-quartile strata for the headline writing-convention results.
  Rebuild with `python3 census-issue-pr/robustness.py build` and verify offline with its `validate` subcommand.
  These are descriptive adoption estimates, not normative requirements.

## Catalog
| Census | Mode | n | Measures | Feeds aspects |
|---|---|---|---|---|
| `census-dev-environment` | A | 429→938 | manifest/readme/gitignore/CI/lint/test/lockfile/pins — the L0/L1 floor | 03 · 04 |
| `census-expanded` | A | 938 | deterministic widened re-census (the honest baseline) | 03 · 04 · 05 |
| `census-governance` | A | 429 | ADR/RFC/design-doc presence, license, security policy, Scorecard | 01 · 05 · 09 · 10 · 24 · 25 |
| `census-release-ops` | A | 429 | SemVer/releases/notes/CC/changelog/cadence/container/CD/IaC/obs | 17 · 20 |
| `census-issue-pr` | A | 500→2000 | issue templates/forms/config + PR template + CC PR-title adoption (`census2k.py` widened to top-2000-by-stars software, 2026-07-05 — rankings held, presence-% fell w/ wider N). **`taskform.py` enrichment** (2026-07-05): re-harvested ISSUE_TEMPLATE form file-names/`name:` for the 629 form-repos → form-TYPE taxonomy (bug 94% · feature 72% baseline; task-class only 4.1% → `task` NOT a census-standard form). **`conventions.py` enrichment** (2026-07-07): re-harvested the form/PR BODIES for the 1104 template-bearing repos (1610 forms · 10,181 fields · 503 PR templates) → per-field WRITING conventions the header/label censuses discarded: field-TYPE dist (textarea 54% dominant), required-rate by type (dropdown 73/input 65/textarea 57 ↔ checkboxes 3.8), help-text near-universal (87%), preflight-checkbox 22% / in-form CoC 6%, PR checklist **empty `- [ ]` 62%** + HTML-comment guidance 70% + **"type of change" only 12%, and when present 85% checkbox (free-text "feat" 1.7%)**. Rich raw kept in `conventions-records.json` (re-analysable w/o re-harvest). **Wide-N confirmation** (`conventions.py harvest_wide` → `conventions-6k-*`, same day): re-ran over the template-bearing subset of the N=6,582 governance-floor pool (2425 repos · 3248 forms · 20,837 fields · 1077 PR templates, star floor 29) — every convention held within a few pp (help-text 87.1→87.2 identical, textarea 54.1→53.2, type-of-change 12% + freetext 1.6% held; only PR HTML-comment guidance moved −6pp, still 64%) → conventions are population-wide floors, not top-repo artifacts; `compare` sub-command diffs the two. **`conventions.py roster` enrichment** (2026-07-07): a 3rd pass (`harvest_roster`/`roster`) captured the field LABELS the earlier passes discarded and clustered them into per-form-category section ROSTERS — bug (669 forms) = environment 83% / repro 74% / description 68% / expected 52% (all required-when-present) + logs 47% / context 41% (optional) + preflight 25%; feature (516) = proposed 51% / problem 47% (required) + alternatives 27% / context 47% + preflight 26%; task (N=26) has no strong wild roster (a principled gingoa structure). 28.6% free-text label tail left honest (willingness-checkbox / bare tokens / enterprise-niche); raw labels stored in `conventions-roster-records.json` → taxonomy re-runnable without re-harvest | 05 · 24 |
| `census-gov-adequacy` | A | 2000 | governance-floor files **PRESENCE vs ADEQUACY** (content-parsed, not presence-only — Tier-1 method pilot): CONTRIBUTING/SECURITY/CoC/CODEOWNERS/LICENSE substance + adequacy-gap | 24 · 25 |
| `census-governance-floor` | A | 6582 | governance/quality FILE floor across the **full item set** (LICENSE/CONTRIBUTING/SECURITY/CoC/CODEOWNERS/CHANGELOG/.editorconfig/.gitattributes/.env.example/pre-commit/dependabot/renovate/AGENTS.md/CLAUDE.md/FUNDING/Discussions/ADR-dir/issue+PR templates/merge-policy) **stratified by archetype** (ecosystem + monorepo/library/cli via manifest text) — grounds the 3-tier auto/senior-default/context classification (2026-07-05; star floor 29, 3.3× the issue-pr set). Method: GraphQL native fields + **directory-tree entry detection** (root/.github/docs/ISSUE_TEMPLATE/workflows), NOT per-file probes (13× faster). ⚠️ eco-tag skew: Java over-rep/low-gov drags aggregate, Python under-counted (requirements.txt-only fails manifest filter) → use node/go/rust as gingoa's reference class | 24 · 04 · 05 · 25 · 27 |
| `census-commit-body` | A | 250 | squash-merge body: CC subject, body, Closes, Co-Authored-By | 05 |
| `census-doc-conventions` | B | GitHub-wide | planning/spec/ADR doc naming·location·publish (filename/path counts) + spec-tool commit-vs-gitignore | 01 · 04 |
| `harness-census` | A | 200 (+36 canonical) | AI-harness capability layer (skills/hooks/mcp/marketplace/schema) + software floor | 27 |

`harness-census` uses an exploratory RAW layer (`census.sh` collector + `results*.tsv` + `pool.json` + `raw/`
+ `SUMMARY.md`) but **now carries a normalized `stats.json`** (added 2026-06-26 — the floor + capability-layer
percentages from `SUMMARY.md` in the catalog shape), so it conforms. The raw tsv/pool layer is kept as-is.
