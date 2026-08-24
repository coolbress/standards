# Outbound-data gate — what may leave to another vendor (G6 · G7)

**Size ≠ sensitivity.** "Only send the diff" is a size rule, not a sensitivity
rule — a 30-line auth diff can carry a customer identifier, a proprietary
algorithm, or an infrastructure hostname. Before **any** artifact leaves the
session for a different vendor's model (cross-vendor review, second opinion,
anything), it passes this gate. Kept as its own reference (not folded into the
roster) because the roster expires when hosts ship auto-routing — this gate does
not (see the roster's Expiry).

External transmission is an **external action** under contract clause 2:
approval in one context does not carry to the next send.

## Procedure

1. **Assemble the exact payload first** — the literal text that will be sent
   (diff + spec excerpt + question). Gate what actually leaves, not a
   description of it.
2. **Deterministic scan** — run the payload through the existing secret guard;
   do not re-implement or re-list its patterns, the script is the single source:

   ```bash
   printf '%s' "$PAYLOAD" | "${CLAUDE_PLUGIN_ROOT}"/hooks/scripts/secret-guard.sh
   ```

   (`${CLAUDE_PLUGIN_ROOT}` is how the installed plugin addresses itself — the
   gate usually runs from a *user project*, not the goppi repo; use the
   installed goppi plugin dir, or `hooks/scripts/secret-guard.sh` relative to
   the goppi checkout when working in the repo itself.)

   Exit 0 = no credential-format hit. Exit 2 = a hit **or** scanner failure —
   both block (the guard is fail-closed). If the script is unreachable in this
   environment, say so and treat the scan as failed — never claim a scan that
   did not run.
3. **Advisory scan (model judgment)** — read the payload once with only this
   lens: personal data, customer identifiers, proprietary logic or internal
   names, infrastructure details. These have no reliable literal patterns; a
   regex cannot own this layer.
4. **On any hit (either layer): block and ask.** Show the user a plain-language
   preview — **what** was flagged (the lines), **where** it would go (vendor +
   tool), **why** it looks sensitive — and proceed only on explicit approval.
   Do not summarize away the flagged content; show it.
5. **Record the transmission** in the session record (progress.md; when
   review-related, in the review's PR comment — the PR body's `## Verification`
   stays a one-line summary): what was sent, to which vendor, and the gate
   result — including approved-after-flag sends.
6. **First cross-vendor send of a project**: tell the user once that consumer
   subscription CLIs are subject to that vendor's data-retention policy
   (design §6).

## What is enforced vs advisory — honestly

- **Scan-enforced (deterministic)**: credential-literal formats only — the
  secret-guard pattern set. It is a literal-pattern lint, not an exfiltration
  boundary (encoded/indirected secrets pass it; the sandbox owns that layer).
- **Advisory (judgment)**: PII / customer data / proprietary content
  recognition, and the decision that a payload is "review-worthy" at all.
  Cannot be made deterministic (§4.3 — same reason MCP writes and domain
  grants can't be fully gated by permissions).
- **Not covered here**: transmissions that bypass the session model entirely
  (a user pasting into a web UI), and MCP write tools — those need per-tool
  ask rules as they are adopted (design §4.3).
- False-block and leak rates are **unmeasured** [inferred] — both directions
  are S4 eval targets (a gate that over-blocks dies by the self-deletion rule;
  a gate that leaks is worse than none).

## Evidence

- [lit-internal] design §6 outbound-data gate (v0.5, review #2 finding #10 —
  "size ≠ sensitivity"); §4.3 external-action approval truth (ask-rules +
  sandbox + plain-language preview approximate the gate, none alone suffices);
  §2 clause 2 (external actions need explicit approval, per event).
- [lit-internal] `hooks/scripts/secret-guard.sh` — fail-closed stdin scanner,
  high-precision credential formats; reused here so the pattern set has one
  home (review #2 lesson: duplicated pattern lists drift).
- [census] Vendor data-retention: consumer subscription CLI traffic is subject
  to vendor policy; noted to the user rather than assumed away.

## Expiry conditions

- A host ships a native outbound-content scanner/DLP hook covering third-party
  model calls → migrate the deterministic layer to it; keep the advisory layer
  and the approval step (clause 2 is the user's, not the host's).
- S4 eval measures false-block rate high with zero true blocks over a real
  usage window → re-scope the pattern set or demote the deterministic layer
  (self-deletion discipline, §2 value 6).
