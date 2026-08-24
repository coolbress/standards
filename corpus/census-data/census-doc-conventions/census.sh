#!/usr/bin/env bash
# census-doc-conventions — Mode B (count census).
# Measures how common planning/spec/ADR document CONVENTIONS are across GitHub, via
# `gh api search/code` total_count per filename/path query. Counts FILES (default branch,
# auth-gated, indexed subset) — estimates, not per-repo records. Results → stats.json.
# Run 2026-06-26 (account: coolbress). Pace queries: search/code has a strict secondary
# rate limit (~30/min primary + abuse detection) — sleep between calls or it 403s.
set -u
count() { local q="$1"; local n; n=$(gh api -X GET search/code -f q="$q" --jq '.total_count' 2>/dev/null); printf '%-44s %s\n' "$q" "${n:-ERR}"; sleep 8; }

echo '## naming (filename total_count)'
for q in \
  'filename:AGENTS.md' 'filename:CLAUDE.md' 'filename:constitution.md' \
  'filename:PRD.md' 'filename:product-requirements.md' 'filename:requirements.md' \
  'filename:spec.md' 'filename:design.md' 'filename:plan.md' 'filename:tasks.md' \
  'filename:vision.md' 'filename:ROADMAP.md' 'filename:GLOSSARY.md'; do count "$q"; done

echo '## ADR + decision-record location'
for q in 'path:docs/adr' 'path:docs/adr filename:0001' 'path:doc/adr' 'path:docs/decisions'; do count "$q"; done

echo '## planning-dir conventions'
for q in 'path:docs/design extension:md' 'path:docs/specs' 'path:docs/spec extension:md' 'path:docs/rfcs'; do count "$q"; done

echo '## spec-tool adoption: committed vs gitignored (proxy)'
for q in \
  'path:.specify/memory filename:constitution.md' 'path:.specify/memory' \
  'path:.kiro/specs filename:requirements.md' 'path:.kiro/steering' \
  'path:openspec/changes' 'path:openspec/specs' 'path:.bmad-core' \
  '.specify filename:.gitignore' '.kiro filename:.gitignore' 'openspec filename:.gitignore'; do count "$q"; done

echo '## content-linting tool adoption (added 2026-06-27 — grounds the de-jargon CI gate)'
for q in \
  'filename:.markdownlint.json' 'filename:.markdownlint.yaml' 'filename:.markdownlintrc' \
  'filename:.vale.ini' 'filename:cspell.json' \
  'path:.github/workflows vale' 'path:.github/workflows markdownlint'; do count "$q"; done
