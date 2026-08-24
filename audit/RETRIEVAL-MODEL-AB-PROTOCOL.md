# Fresh-context retrieval A/B protocol — preregistered before reading arm outputs

Date: 2026-08-02. Same host/model family, six isolated native contexts: three immutable pre-curation snapshot
arms and three current-corpus arms. No web, no audit/interpretation, no opposite arm. Each starts at its own
`INDEX.md`, answers the same ten questions, and must report every opened file plus byte count.

## Scoring

Each question has two independent binary points.

- **Answer correctness (0/1):** matches the scoped gold below; a corpus that falsely labels a compound claim
  verified does not earn correctness merely because the model repeated the label.
- **Citation support (0/1):** an actually opened path and nearby source/status directly support the answer.
  For `NOT FOUND`, the relevant routed document must be opened and the absence stated without invention.
- **Unsupported claims:** count affirmative factual/normative claims that exceed the opened evidence. This is a
  fault count, not a point.
- **Context cost proxy:** unique opened files and their exact total bytes. Collaboration telemetry does not expose
  per-subagent model tokens, so bytes are measured and token cost is `UNAVAILABLE`, not estimated as actual usage.

## Exact trial prompt

Each context received the following text with `{ARM}`, `{REP}`, and `{CORPUS_PATH}` substituted. The before path
was `/tmp/goppi-before.FM1Jsz/.scratch/research/corpus`; the after path was
`/Users/coolbress/goppi_final/.scratch/research/corpus`.

```text
Read-only blind retrieval trial, {ARM} arm, repetition {REP}. Use ONLY the corpus at {CORPUS_PATH}.
Do not read audit files, interpretation, imported/archive, the opposite arm, or the web. Start at that arm's
INDEX.md and follow links; do not bulk-read the corpus. For each question, read at most INDEX + two relevant
target/source-registry documents. Do not infer missing facts: answer NOT FOUND/UNSUPPORTED where needed.

Answer these exact 10 questions:
Q1. What evidence supports minimum GitHub Actions permissions and immutable action pinning, what is its
status/freshness, and which source supports it?
Q2. May the top-level Requirements & Planning claim be treated as verified current evidence? State status and
the reason visible in the corpus.
Q3. What are the major component planes of a current AI-agent harness, and what evidence status supports that map?
Q4. Find an integrated threat path connecting untrusted content, credentials, egress, filesystem/production
authority, and recovery. What controls are stated and what remains unsupported?
Q5. Does the 28-aspect taxonomy have a current SWEBOK V4.0a × ISO 12207:2026 × ISO 25010:2023 crosswalk?
State the licensed-standard limitation.
Q6. What evidence defines the capabilities/limitations of the intended non-engineer target user, and is transfer
to coding-agent users established?
Q7. What does the corpus say about scaling SRE/on-call practices to a solo non-engineer operator?
Q8. Can the inherited Software Testing synthesis be cited as verified? Give its status and the strongest bounded
conclusion you can support.
Q9. What rule distinguishes official product documentation from evidence that a product practice is effective?
Q10. Which navigation document connects planning, build, verification, release, operation, and retirement, and
how much of the corpus did you need to read?

For each Q return: Qn | answer | evidence path(s) | document status/freshness | source ID/URL if present |
unsupported/unknown. Never cite a path you did not open. Then list every file opened and run wc -c on those exact
files to report total files and total bytes as context-cost proxy. State ARM={ARM} and REP={REP}. Do not score
yourself and do not modify anything.
```

Observable runtime identity: host `Codex`; exact model ID/version, reasoning configuration, sampling parameters,
and per-run token telemetry are **not exposed by the collaboration runtime** and are recorded `UNAVAILABLE` in
each raw ledger. Reproduction can therefore match host/date/prompt/corpus, not an unavailable hidden model build.

## Scoped gold

| Q | Correct bounded answer |
|---|---|
| 1 | Current support is GitHub minimum `GITHUB_TOKEN` permissions + full commit SHA immutability. It needs a current scoped source, status, and expiry; a broad inherited aspect alone is insufficient. |
| 2 | No. The inherited Requirements top claim is a compound synthesis. Current arm says `review-needed`; old `verified` without atomic traceability is overconfidence. |
| 3 | Current map has control, capability, execution, state/context, assurance, distribution planes and a verified scoped claim register. If absent, say not found. |
| 4 | Current integrated path links untrusted influence → model/tool → credential/data/authority → egress or destructive effect, with prevention/detection/recovery. If only scattered advice exists, say no integrated model found. |
| 5 | Current arm has a 28-row conceptual crosswalk; detailed ISO 12207/25010 clause conformance is INCONCLUSIVE without licensed text. Old arm has no current crosswalk. |
| 6 | Current arm defines six task-specific capability axes and explicitly says transfer to coding-agent users is not established. Old arm has no empirical target-capability model. |
| 7 | No verified solo-operation scaling evidence is established in either arm. Current inherited operations synthesis is review-needed; org-scale SRE cannot be silently generalized. |
| 8 | No. The inherited Testing synthesis is not verified under the current policy; bounded testing concepts may be source candidates, not a universal bundle. |
| 9 | Official product docs are primary for product behavior/interface, not evidence of practice effectiveness. If the arm lacks this rule, say not found. |
| 10 | `lifecycle.md` is the navigation document. The current arm includes plan→build→verify→release/operate/maintain/retire without requiring full-corpus loading. |

## Aggregation

Report each repetition separately plus arm mean/range for correctness, citation support, unsupported claims,
files, and bytes. Do not merge deterministic 30-case metrics into model scores. A current-arm advantage is
descriptive for these ten questions and this model/date, not a universal retrieval benchmark.
