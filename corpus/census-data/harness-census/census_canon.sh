#!/usr/bin/env bash
# Skeleton census of top OSS coding harnesses. Reads canonical_list.txt (one full_name/line),
# fetches repo meta + recursive git tree via gh api, emits file-presence booleans to results_canon.tsv.
set -uo pipefail
cd "$(dirname "$0")"
LIST=canonical_list.txt
OUT=results_canon.tsv
ERR=errors_canon.txt
TMP=$(mktemp)
: > "$ERR"

# ordered check keys (standard skeleton, then harness-distinctive)
KEYS="readme license gitignore ci tests lintcfg lockfile manifest contributing security coc issue_tmpl pr_tmpl dependabot docs_dir changelog editorconfig codeowners precommit skills agent_md plugins templates examples prompts schema mcp marketplace hooks commands"
printf 'repo\tstars\tlang\tfork\tarchived\t%s\n' "$(echo $KEYS | tr ' ' '\t')" > "$OUT"

# grep helper: $1 = pathfile, $2 = ERE pattern, $3 = case-flag(i/x)
has() { if [ "$3" = i ]; then grep -qiE "$2" "$1"; else grep -qE "$2" "$1"; fi && echo 1 || echo 0; }

n=0; ok=0
total=$(wc -l < "$LIST" | tr -d ' ')
while IFS= read -r repo; do
  [ -z "$repo" ] && continue
  n=$((n+1))
  meta=$(gh api "repos/$repo" --jq '[.default_branch,.stargazers_count,(.language//"?"),(.fork|tostring),(.archived|tostring)] | @tsv' 2>>"$ERR")
  if [ -z "$meta" ]; then echo "META_FAIL\t$repo" >> "$ERR"; echo "[$n/$total] FAIL $repo" >&2; continue; fi
  branch=$(echo "$meta" | cut -f1); stars=$(echo "$meta" | cut -f2); lang=$(echo "$meta" | cut -f3)
  fork=$(echo "$meta" | cut -f4); arch=$(echo "$meta" | cut -f5)
  gh api "repos/$repo/git/trees/$branch?recursive=1" --jq '.tree[].path' > "$TMP" 2>>"$ERR"
  if [ ! -s "$TMP" ]; then echo "TREE_FAIL\t$repo" >> "$ERR"; echo "[$n/$total] TREEFAIL $repo" >&2; continue; fi

  readme=$(has "$TMP" '^README' i)
  license=$(has "$TMP" '^(LICENSE|LICENCE|COPYING)' i)
  gitignore=$(has "$TMP" '^\.gitignore$' x)
  ci=$(has "$TMP" '^\.github/workflows/.+\.(yml|yaml)$|^\.gitlab-ci\.yml$|^\.circleci/|^azure-pipelines' x)
  tests=$(has "$TMP" '(^|/)tests?/|(^|/)__tests__/|(^|/)spec/|_test\.[a-z]+$|\.test\.[a-z]+$|\.spec\.[a-z]+$|(^|/)test_[^/]+\.py$' i)
  lintcfg=$(has "$TMP" '^biome\.jsonc?$|(^|/)\.eslintrc|(^|/)eslint\.config|^ruff\.toml$|(^|/)\.ruff\.toml$|^\.flake8$|^\.pylintrc$|(^|/)\.prettierrc|^prettier\.config|^rustfmt\.toml$|^\.rustfmt\.toml$|(^|/)\.golangci' i)
  lockfile=$(has "$TMP" '^(package-lock\.json|pnpm-lock\.yaml|yarn\.lock|poetry\.lock|uv\.lock|Cargo\.lock|go\.sum|Pipfile\.lock|composer\.lock|Gemfile\.lock|bun\.lock[b]?)$' i)
  manifest=$(has "$TMP" '^(package\.json|pyproject\.toml|setup\.py|Cargo\.toml|go\.mod|composer\.json|Gemfile|pom\.xml|build\.gradle)' i)
  contributing=$(has "$TMP" '^(\.github/)?CONTRIBUTING' i)
  security=$(has "$TMP" '^(\.github/)?SECURITY' i)
  coc=$(has "$TMP" '^(\.github/)?CODE_OF_CONDUCT' i)
  issue_tmpl=$(has "$TMP" '^\.github/ISSUE_TEMPLATE' x)
  pr_tmpl=$(has "$TMP" 'PULL_REQUEST_TEMPLATE' i)
  dependabot=$(has "$TMP" '^\.github/dependabot\.(yml|yaml)$' x)
  docs_dir=$(has "$TMP" '^docs?/' i)
  changelog=$(has "$TMP" '^CHANGELOG' i)
  editorconfig=$(has "$TMP" '^\.editorconfig$' x)
  codeowners=$(has "$TMP" '(^|/)CODEOWNERS$' i)
  precommit=$(has "$TMP" '^\.pre-commit-config\.yaml$' x)
  skills=$(has "$TMP" '(^|/)skills?/|(^|/)SKILL\.md$|/SKILL\.md$' i)
  agent_md=$(has "$TMP" '^(AGENTS?\.md|CLAUDE\.md|GEMINI\.md|\.cursorrules|\.windsurfrules)$|/CLAUDE\.md$|/AGENTS?\.md$' i)
  plugins=$(has "$TMP" '(^|/)plugins?/|plugin\.json$|\.claude-plugin' i)
  templates=$(has "$TMP" '(^|/)templates?/|(^|/)scaffold' i)
  examples=$(has "$TMP" '(^|/)examples?/' i)
  prompts=$(has "$TMP" '(^|/)prompts?/' i)
  schema=$(has "$TMP" 'schema[^/]*\.json$|\.schema\.|(^|/)schemas?/' i)
  mcp=$(has "$TMP" 'mcp[^/]*\.json$|(^|/)\.mcp|(^|/)mcp/' i)
  marketplace=$(has "$TMP" 'marketplace\.json$|(^|/)registry|catalog\.json$' i)
  hooks=$(has "$TMP" '(^|/)hooks?/|hooks\.json$' i)
  commands=$(has "$TMP" '(^|/)commands?/' i)

  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
    "$repo" "$stars" "$lang" "$fork" "$arch" \
    "$readme" "$license" "$gitignore" "$ci" "$tests" "$lintcfg" "$lockfile" "$manifest" \
    "$contributing" "$security" "$coc" "$issue_tmpl" "$pr_tmpl" "$dependabot" "$docs_dir" \
    "$changelog" "$editorconfig" "$codeowners" "$precommit" \
    "$skills" "$agent_md" "$plugins" "$templates" "$examples" "$prompts" "$schema" "$mcp" "$marketplace" "$hooks" "$commands" >> "$OUT"
  ok=$((ok+1))
  echo "[$n/$total] ok $repo (stars=$stars lang=$lang)" >&2
done < "$LIST"
rm -f "$TMP"
echo "=== DONE: $ok/$n rows written to $OUT; errors in $ERR ===" >&2
