#!/usr/bin/env bash
set -uo pipefail
OUT=/private/tmp/claude-501/-Users-coolbress-gingoa/1b0ed757-610e-48a7-87bb-46119ecf31c4/scratchpad
REPOS="$OUT/repos.tsv"
PLAIN="$OUT/repos.plain"     # "full branch stars" space-separated
ROWS="$OUT/rows.tsv"

awk -F'\t' '{print $1, $2, $3}' "$REPOS" > "$PLAIN"
echo "repos: $(wc -l < "$PLAIN")"

classify() {
  local full="$1" branch="$2" stars="$3" tree paths trunc
  tree=$(gh api "repos/$full/git/trees/$branch?recursive=1" 2>/dev/null)
  if [ "$(jq -r '.tree // empty' <<<"$tree" 2>/dev/null)" = "" ]; then
    printf '%s\t%s\tERR\n' "$full" "$stars"; return
  fi
  trunc=$(jq -r '.truncated' <<<"$tree")
  paths=$(jq -r '.tree[].path' <<<"$tree")
  has() { grep -qiE "$1" <<<"$paths" && echo 1 || echo 0; }
  printf '%s\t%s\tOK\t%s\td_specs=%s\tr_specs=%s\tkiro=%s\topenspec=%s\trfcs=%s\tproposals=%s\tadr=%s\tspec_md=%s\thas_docs=%s\n' \
    "$full" "$stars" "$trunc" \
    "$(has '^docs/specs/')" "$(has '^specs/')" "$(has '^\.kiro/specs/')" "$(has '^openspec/')" \
    "$(has '(^|/)rfcs?/')" "$(has '(^|/)proposals?/')" "$(has '(^|/)(adr|adrs)/|^docs/decisions/')" \
    "$(has '(^|/)spec\.md$')" "$(has '^docs/')"
}
export -f classify

: > "$ROWS"
xargs -P 10 -n 3 bash -c 'classify "$@"' _ < "$PLAIN" >> "$ROWS"

echo ""; echo "=== status ==="; awk -F'\t' '{print $3}' "$ROWS" | sort | uniq -c
echo ""; echo "=== aggregate (OK repos) ==="
awk -F'\t' '
$3=="OK"{ ok++; if($4=="true")trunc++
  for(i=5;i<=NF;i++){split($i,a,"="); if(a[2]=="1")cnt[a[1]]++}
  if($0 ~ /d_specs=1|r_specs=1|kiro=1|openspec=1|rfcs=1|proposals=1|adr=1/)anyc++
  if($0 ~ /rfcs=1|proposals=1/)rfcprop++
}
END{ printf "OK=%d truncated=%d\n\n", ok, trunc
  n=split("d_specs r_specs kiro openspec rfcs proposals adr spec_md has_docs",o," ")
  for(i=1;i<=n;i++){k=o[i]; printf "%-11s %4d / %d  (%.1f%%)\n", k, cnt[k]+0, ok, 100*(cnt[k]+0)/ok}
  printf "\nANY structured dir   %d / %d  (%.1f%%)\n", anyc+0, ok, 100*(anyc+0)/ok
  printf "rfcs|proposals only  %d / %d  (%.1f%%)\n", rfcprop+0, ok, 100*(rfcprop+0)/ok
}' "$ROWS"