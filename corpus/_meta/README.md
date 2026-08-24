# Machine-readable metadata

- `sources.jsonl` is the canonical identity/version registry for sources used by newly curated material.
- One JSON object per line; UTF-8; stable `id`; no comments or trailing commas.
- A registry entry establishes source identity and scope, not the truth of every statement in that source.
- Claim-level records remain close to the claim in Markdown until a generated `claims.jsonl` export is justified
  by retrieval evaluation.

