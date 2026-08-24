([.tree[].path]) as $p
| ($p | length) as $n
| (.truncated) as $tr
| def has(re): ($p | map(select(test(re;"i"))) | length) > 0;
[
  $n,
  $tr,
  (has("(^|/)(docs?/adr|adr|docs?/decisions)/")),
  (has("(^|/)(docs?/specs?|specs?)/")),
  (has("(^|/)(prd\\.md|.*product[-_ ]requirements.*\\.md)$")),
  (has("(^|/)requirements\\.md$")),
  (has("(^|/)roadmap\\.md$")),
  (has("(^|/)(rfcs?|docs?/rfcs?)/|(^|/)rfc[-_]?[0-9]")),
  (has("(^|/)changelog(\\.md|\\.rst|\\.txt)?$")),
  (has("(^|/)\\.specify/")),
  (has("(^|/)\\.kiro/")),
  (has("(^|/)openspec/")),
  (has("(^|/)agents\\.md$")),
  (has("(^|/)claude\\.md$")),
  (has("(^|/)docs?/")),
  (has("(^|/)(package\\.json|pyproject\\.toml|cargo\\.toml|go\\.mod|pom\\.xml|build\\.gradle|build\\.gradle\\.kts|gemfile|composer\\.json|package\\.swift|build\\.sbt|setup\\.py|mix\\.exs|pubspec\\.yaml)$"))
] | @tsv
