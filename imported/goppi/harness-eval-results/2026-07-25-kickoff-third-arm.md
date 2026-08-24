# pair — kickoff 3rd arm: can a strengthened clause 1 explain the skill away? 2026-07-25 (Session G, G-3)
<!-- genre: pair -->

The discriminating run the 2nd scenario pre-designed
(`2026-07-25-kickoff-second-scenario.md`, closing section): run 2's margin traced
to **one question about purpose** in the first reply, which is arguably contract
clause 1's own job. So the arm that decides keep-vs-thin is **contract-only with
clause 1 strengthened on purpose-asking**, against the kickoff arm.

**Pre-registered before any spend** (arms, the added sentence, the decision rule,
the cost cap, and the arm-order draw — all fixed in writing first). This design
could have ended the skill; that is why it was worth running.

## Arms — the delta is one sentence

- **S — strengthened contract, no skill.** Base contract **byte-identical** to run
  2's arm material (today's `GOPPI.md` minus the HTML Evidence block; verified by
  diff, 3,836 bytes). One sentence added to clause 1, `+177` chars, verified by
  diff as the only difference between the two arms' contracts:
  > **When a request names an output but not what it is for, ask what the output
  > will be used to decide before proposing one — a request's stated form often
  > hides the actual job.**
- **K — unmodified contract + kickoff skill.**

**The skill copy is run 2's, not today's — disclosed because it matters.** Today's
`skills/kickoff/SKILL.md` differs from run 2's *only* by Evidence/Expiry
paragraphs added afterwards, which record run 2's result and pre-announce this
run ("the margin came from one question about purpose"; "the discriminating third
arm is contract-only with clause 1 strengthened"). Injecting that would have
handed arm K the answer key. Operating instructions are identical between the two
copies (verified by diff).

## Held identical to run 2

`opening.txt` · `closing.txt` · `persona.md` · the 8-item hidden intent card ·
`run.sh` (3 exchanges, persona played by a **separate** session) · the judge
prompt header, byte-identical at 3,199 bytes · scoring
(HIT×2 + PARTIAL − CONTRADICTED×2, max 16; **the user's agreement is worth zero**).
Model `claude-fable-5`, Claude Code 2.1.220, prompts bypassed equally in both arms.

**Arm order randomized** — run 2's recorded confounder. `shuf -n1 -e S-first
K-first` drew **K-first**, recorded in the pre-registration *before* the judge
prompt was built, so the judge saw the kickoff arm as "A". Leak check on the
finished prompt: zero occurrences of "kickoff", "clause 1", or "skill".

## Result — blind judge

| card item | **A** = kickoff arm | **B** = strengthened-contract arm |
|---|---|---|
| 1 decision at the door | HIT | HIT |
| 2 volunteer decides in <1 min | HIT | PARTIAL |
| 3 only $2/$5/$10 — lookup is waste | HIT | **CONTRADICTED** |
| 4 asking prices ≠ realized sales | PARTIAL | **CONTRADICTED** |
| 5 4th copy → discard | HIT | MISS |
| 6 must work offline | PARTIAL | MISS |
| 7 no app, no code to maintain | HIT | HIT |
| 8 non-goals: donor tracking, receipts | HIT | HIT |
| **totals** | 6 H · 2 P · 0 M · 0 C | 3 H · 1 P · 2 M · 2 C |
| **score** | **14** | **3** |
| cost | $1.5364 | $0.8857 |
| turns | 4 assistant | 4 assistant |
| tokens | **not captured by this run's harness** | **not captured by this run's harness** |
| wall time | not captured | not captured |

Judge $0.7115. **Pair total $3.1336**, inside the pre-registered $4.50 cap.

**A required field is missing, and it is a harness defect, not a host one.**
`harness/arm-setup.md` requires per-arm **tokens** (with the host's input/output/
cache split) and **wall time** in every result file from 2026-07-25 on. The host
reports both — the same session's body measurements record them — but `run.sh`,
reused verbatim from run 2 for comparability, extracts only `session_id`,
`result` and `total_cost_usd` from each turn's JSON and discards the rest. So
the fields are **not recoverable without re-running**, and they are recorded as
not-captured rather than estimated. Run 2 has the identical gap; this file
inherits it rather than introducing it, but this session's spec named the
requirement, so it is a miss either way. **Fix owed before the next pair**:
`run.sh` must persist each turn's raw JSON.

Six load-bearing judge quotes were **verified against the transcripts** before
this file was written (judge output is untrusted data, contract clause 2) — all
six matched, plus two negative controls: arm B never mentions the duplicate rule
(0 hits), and **neither** arm ever mentions offline/wifi (0 hits each), matching
the MISS/PARTIAL on card 6.

## The call — pre-registered rule, applied as written

| rule (fixed before the run) | outcome |
|---|---|
| S ≥ K − 2 → THIN | 3 ≥ 12? **no** |
| **S ≤ K − 5 → KEEP** | 3 ≤ 9? **yes** |
| gap 3–4 → inconclusive | gap is 11 |
| K < 5 → inconclusive | K = 14 |

**KEEP.** kickoff's marginal value survived a deliberate, fairly-built attempt to
explain it away.

## What actually happened — and it corrects run 2's stated mechanism

**The strengthened clause fired.** Arm B's first reply asked the purpose question
almost verbatim — *"**「값어치」를 어디에 쓰실 건가요?**"* — offering four candidate
uses, and the user answered with the door decision immediately
(*"책 상자가 들어오면 그 자리에서 팔지 버릴지 소장할지 정해야 해서"*). Arm B
therefore reached the run-2 winning move **in turn one, and scored HIT on card 1**.

Then it stopped. Across four assistant turns arm B asked **2 questions**; arm A
asked **10**. Arm B took the first agreeable answer and went to design, committing
to market-value machinery (*"중고 시세가 실제로 형성되어 있는 책… 경계 금액은 실제
데이터를 보고 정해서"*) — card item 3's named waste, calibrated on card item 4's
bad data. Arm A kept interviewing and extracted the manager's actual procedure
(*"① 낙서·물얼룩 있으면 처분 → ② 서가에 이미 3권 있으면(4권째) 처분 → ③ 팔 때는
$2/$5/$10 중 하나"*), which is the whole job.

So run 2's causal story — "the margin came from one question about purpose" — is
**incomplete, and this run is what shows it**. The purpose question is necessary
and reproducible from a contract line; it is nowhere near sufficient. What kickoff
supplies is the **sustained interview**: continuing to probe after the first
plausible answer, which is precisely what an agreeable user makes it easy to skip.
A one-line contract addition does not buy that, and this is the first evidence in
the repo that separates the two.

The cost split says the same thing from another direction: arm B spent **58% of
arm A's cost** ($0.8857 vs $1.5364) and produced a plan that would have built both
named wastes. That is a **cost** ratio — the token ratio is unavailable for the
reason above, and the two are not interchangeable.

## Honest scope

- **n=1 scenario, single judge, one host, one day.** Same model family for both
  arms, the persona, and the judge — a shared-bias risk this design does not
  remove.
- **Cross-run scores are not comparable.** Arm K scored 9 in run 2 and 14 here on
  the same scenario and card; the two runs used different judge sessions and the
  persona is stochastic (in this run the user volunteered the door decision
  earlier than in run 2, which if anything made arm B's task *easier*). Only the
  within-run comparison — 14 vs 3, same judge, same day, blind, randomized order —
  is load-bearing. Run 2's 9 vs −2 stands on its own terms.
- **The strengthened sentence was written by the same driver that wanted an
  answer.** It was built as the strongest fair version (it encodes the exact
  winning move, in contract voice, in one line) and fixed in writing before the
  run, but a differently-worded strengthening could perform differently. What this
  run rules out is *that sentence*, not every possible clause-1 rewrite.
- **This is not a §4.1 gate result.** The strengthened clause was arm material,
  not a proposal to land; nothing in `GOPPI.md` changed, and the contract's
  always-injected number is untouched.
- **The persona's blinding is asserted by construction, not verified.** The judge
  was leak-checked; the persona session was not. It is seeded per arm with the
  card and the persona rules and sees only the assistant's replies, so it carries
  no arm label — but it is a fresh stochastic session per arm, and its
  forthcomingness is therefore free to differ between arms. It did: in this run
  the user volunteered the door decision in reply 1 (earlier than in run 2). That
  direction *disadvantages* the arm that lost, so it does not explain the gap —
  but a persona effect of unknown size sits inside the 11 points, and no check in
  this design bounds it. `run.sh` is held byte-identical to run 2 but its contents
  are not reproduced here, so the claim below that every result-shaping input is
  reproduced holds for the fixtures, not for the harness script.
- Three exchanges is a short conversation, capped for cost and applied equally.
- Both arms ran with permission prompts bypassed, equally, per `arm-setup.md` — so
  this pair says nothing about the G7 layer.
- Pre-registration, both transcripts, the judge prompt and its raw JSON are in the
  session scratch dir; every input that shapes the result is reproduced above.
