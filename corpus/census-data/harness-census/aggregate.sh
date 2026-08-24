#!/usr/bin/env bash
# Aggregate results.tsv -> presence %, overall + split by harness type.
# Type heuristic: APPLICATION harness = has pkg manifest AND (ci or tests or lockfile).
#                 CONTENT harness     = otherwise (skill/plugin/prompt packs, doc collections).
set -uo pipefail
cd "$(dirname "$0")"
IN="${1:-results.tsv}"
awk -F'\t' '
NR==1 { for(i=1;i<=NF;i++) col[i]=$i; ncol=NF; next }
$4=="true" { next }                       # drop forks
{
  total++
  manifest=$13; ci=$9; tests=$10; lock=$12
  isapp = (manifest==1 && (ci==1 || tests==1 || lock==1)) ? 1 : 0
  if(isapp){app++} else {content++}
  for(i=6;i<=ncol;i++){ if($i==1){ sum[i]++; if(isapp) asum[i]++; else csum[i]++ } }
}
END{
  printf "POPULATION: %d non-fork repos  (application=%d, content=%d)\n\n", total, app, content
  printf "%-14s %8s %8s %8s\n","check","ALL%","APP%","CONTENT%"
  printf "%-14s %8s %8s %8s\n","-----","----","----","-------"
  for(i=6;i<=ncol;i++){
    a = total? 100*sum[i]/total:0
    pa= app? 100*asum[i]/app:0
    pc= content? 100*csum[i]/content:0
    printf "%-14s %7.0f%% %7.0f%% %7.0f%%\n", col[i], a, pa, pc
  }
}' "$IN"
