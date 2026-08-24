# pair — kickoff marginal value, 2nd controlled scenario, 2026-07-25 (Session C)
<!-- genre: pair -->

The second measurement the repeated-eval criterion requires before any
keep/thin/delete call on `kickoff`. First measurement: 2026-07-18, café
inventory, blind judge **22 vs 18 for the contract-only arm** ("clear not
decisive"; design §12). This run was deferred once by user decision during
Session B and executed here under approval given 2026-07-25.

Arms: **contract-only** vs **contract + kickoff skill** — both carry GOPPI.md,
so this measures the *skill's* marginal value, not goppi's presence.

## What run 1 exposed, and how the design answers it

Run 1's recorded failure mode: **the candidate mirror-back acts as a leading
question for an agreeable user** — the arm proposes criteria, the user says
"yes", and the "confirmation" is scored as intent alignment when it is nothing
of the kind. That is a scoring defect, not a skill defect, so the fix belongs
in the scoring design:

- The role-played user is **explicitly a yes-man** (persona rules: agree with
  every proposal, never correct a wrong summary, answer only what is asked).
- **The user's agreement is worth zero points.** Scoring compares each arm's
  final plan against a **hidden intent card** neither arm ever sees — exactly
  the executable-O definition design §11 G1 records ("a translation task whose
  planted intent card is driver-known, scored on whether each arm's derived
  criteria cover the card").
- The persona is played by a **separate session**, not by the builder — run 1's
  recorded confounder.

Per card item, per arm: HIT / PARTIAL / MISS / **CONTRADICTED** (the plan does
the opposite — builds a named non-goal or the named waste).
Score = HIT×2 + PARTIAL − CONTRADICTED×2, max 16.

## Scenario and card

Neighborhood library book-donation intake. Opening message, identical and
verbatim in both arms: *"동네 도서관에서 책 기증을 받고 있는데요, 뭐가
들어왔는지랑 얼마나 값어치가 있는지 알고 싶어요. 좀 정리해줄 수 있을까요?"*
Closing message, also fixed and identical: *"좋아요, 그럼 뭘 만들지 정리해서
알려주세요."* Three exchanges between them.

The card plants traps in **both** directions — over-building and under-hearing:

| # | Card item | Trap |
|---|---|---|
| 1 | The pain is a keep/sell/discard decision **at the door**, not a report | request sounds like a report |
| 2 | A volunteer decides one book in **under a minute**, without the manager | — |
| 3 | Sale prices are only **$2 / $5 / $10** — market lookup is wasted work | over-build |
| 4 | Volunteers copy **asking prices** off a used-book site — not realized sales | bad data at the source |
| 5 | **4th copy of a title → discard**; copies vs titles must be distinguishable | — |
| 6 | Must work **offline** at the intake table (no wifi) | — |
| 7 | **No app, no code to maintain** — the shared spreadsheet is fine | over-build |
| 8 | Explicit non-goals: **donor tracking, tax receipts** (the library refuses receipts) | build-the-non-goal |

## Result — blind judge

| | contract-only (judge's "A") | contract + kickoff (judge's "B") |
|---|---|---|
| HIT | 0 | **5** |
| PARTIAL | 2 | 1 |
| MISS | 4 | 1 |
| **CONTRADICTED** | **2** | 1 |
| **Score** | **−2** | **9** |
| cost · turns | $1.4861 · 4 assistant turns | $1.4506 · 4 assistant turns |

Judge cost $0.6767. **Total for this pair: $3.6134** (approved band $2–5).

**The contract-only arm built both named wastes.** It committed to per-book
market valuation (verified in transcript: *"중고 시세까지 제가 알아서 찾아 채울
수 있습니다"*, plus an age-based percentage schema) — card item 3's explicit
waste — and to donor aggregation for *"기증 확인서나 감사 인사"* — card item 8,
which the library has decided it will not do at all.

**The mechanism, per the judge and verified in the transcript**: the kickoff arm
asked what the valuation was *for* in its first reply — *"'얼마나 값어치가
있는지'는 어디에 쓰실 정보인가요?"* — and that one question surfaced the door
decision, the three price tiers, the 4th-copy rule, and the no-receipts policy.
The contract-only arm never asked, and so never learned the sheet existed.

## What the kickoff arm still got wrong

Recorded because a win that hides its own defects is not a measurement:

- **CONTRADICTED on card 7**: it proposed building a *도구* (a tool you feed a
  list into) when the rules it had itself extracted — bad condition → discard;
  4th copy → discard; otherwise pick one of three prices — fit on a laminated
  card. It heard "no software to maintain" and specified software.
- **MISS on card 6**: offline never came up. Dropping the price lookup makes
  offline possible **by accident, not by design**.
- **PARTIAL on card 4 — and this is the sharpest finding of the run**: the
  kickoff arm *heard* the asking-price practice (*"중고책 파는 사이트에서
  가격을 찾아서 거기에 베껴 적는 식이에요"*) and cut the lookup, but its stated
  grounds were convenience and the three tiers — it never named the defect that
  the copied numbers are prices nobody actually paid. **It fixed the symptom
  without diagnosing it.** Neither arm caught this. In run 1, the *contract-only*
  arm caught its analogous data-source trap and that catch decided the run;
  here the trap went uncaught by both, which is a caution against reading either
  run as a verdict on "which arm reasons better".

## The keep/thin/delete call

**KEEP** — with the ledger stated plainly rather than averaged:

- Run 1 (café inventory, 2026-07-18): contract-only won, "clear not decisive",
  and its decisive margin came from design judgment outside kickoff's scope (a
  recorded partial confounder).
- Run 2 (this run): kickoff won **decisively** on card coverage, and the causal
  path is visible in the transcript — one purpose question early, which the
  contract-only arm never asked.

Two measurements, one each way, is **not** "even". Run 2's scoring is the one
that matches §11 G1's executable-O definition; run 1 predates that definition
and scored a different thing. The honest reading is: kickoff's marginal value is
**real but scenario-dependent**, and it shows up exactly where the request's
stated form hides the actual job (a "report" request that is really a decision
aid). That is a keep, not a proof.

Thin/delete stays live for a future run: the mechanism that earned the win here
was **one question about purpose**, which is arguably contract clause 1's job
("translate plain-language requests into a deliverable"). A third scenario worth
running is contract-only *with* clause 1 strengthened on purpose-asking versus
kickoff — if that closes the gap, kickoff thins to a line.

## Honest scope

- **n=1 scenario, single judge, one host, one day.** Same model family
  (`claude-fable-5`) for both arms, the persona, and the judge — a shared-bias
  risk this design does not remove.
- **Arm order was NOT randomized**: contract-only was always presented to the
  judge as "A" and kickoff as "B". Position bias is therefore uncontrolled and
  the margin should be read with that discount.
- The judge's four load-bearing quotes were **verified against the transcripts**
  before this file was written (judge output is untrusted data, contract clause
  2) — all four matched.
- Three exchanges is a short conversation; a longer one might let the
  contract-only arm recover. The cap was chosen for cost and applied equally.
- Both arms ran with permission prompts bypassed, equally, per `arm-setup.md` —
  so this pair says nothing about the G7 layer.
- Transcripts, intent card, persona rules, and the judge prompt are preserved in
  the session scratch dir; the card and persona rules are reproduced above in
  full so the run can be rebuilt.
