# Routing

Use this reference only when the appropriate mode is unclear.

## Signals

Consider four dimensions:

| Dimension | Low | High |
|---|---|---|
| Scope | one localized outcome | multiple dependent components |
| Ambiguity | target and proof are obvious | choices materially change the result |
| Risk | reversible local change | security, money, data loss, production, or external effects |
| Duration | one short execution loop | investigation or iteration with an uncertain path |

## Decision

- Choose **Direct** when all dimensions are low.
- Choose **Structured** when scope, ambiguity, or regression risk is material but the work remains bounded.
- Choose **Governed** when consequential risk is high, the path requires durable iteration, or evidence gates must prevent an invalid result.

## Calibration examples

| Request | Mode | Reason |
|---|---|---|
| Rename a label and run its focused test | Direct | localized and cheaply verified |
| Add onboarding across UI, API, and tests | Structured | dependent multi-file outcome |
| Diagnose a payment incident without changing production | Governed | high impact and strict evidence boundary |
| Summarize a supplied document | Direct | no engineering workflow needed; the Skill may be skipped entirely |
| Research a strategy with point-in-time data gates | Governed | invalid evidence must stop promotion |

Mode changes are allowed when inspection reveals new evidence. Briefly tell the user when the change materially affects time, authority, or deliverables.
