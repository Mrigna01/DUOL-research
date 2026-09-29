# Lab 11 — DUOL One-at-a-Time Sensitivity Analysis

This folder extends the standalone Lab 10 DUOL model without changing Lab 10 files.

## Independent drivers

1. **Paid-subscriber conversion and retention.** The Q2 2026 shareholder letter reports 12.7
   million paid subscribers, 58.7 million DAUs, and 84% current-user retention. The sensitivity
   uses a judgment shock of **−2.0 / 0.0 / +2.0 percentage points** to each forecast year's
   revenue growth. Only this growth path changes in its three runs.
2. **AI features.** The same letter discusses AI-powered Video Call expansion and AI cost
   efficiencies supporting gross margin. The sensitivity uses a judgment shock of **−1.0 / 0.0 /
   +1.0 percentage points** to each forecast year's gross margin. Only gross margin changes in
   these three runs.

The locked predictions and timestamp are in `locked_changed_input_record.md`. The model resets all
other independent inputs to base before every run and restores the base case at the end.

## Run

```powershell
python lab11_sensitivity.py
```

The script reports, for every lower/base/higher run, the actual input, 2030 operating profit
(EBIT), 2030 FCFF, value per share, signed changes from base, and output spans. It writes
`sensitivity_results.csv` and retains the accounting-check logic. The cash-flow label is **FCFF**;
the valuation uses FCFF discounted at WACC.

## Results

| Driver | Case | Input shock | 2030 EBIT | 2030 FCFF | Value/share | Change from base |
|---|---|---:|---:|---:|---:|---:|
| Paid conversion/retention | Lower | -2.0 pp | $423.1m | $333.7m | $128.42 | -$11.76 |
| Paid conversion/retention | Base | 0.0 pp | $462.1m | $373.3m | $140.18 | $0.00 |
| Paid conversion/retention | Higher | +2.0 pp | $503.8m | $416.3m | $152.94 | +$12.75 |
| AI features | Lower | -1.0 pp | $441.5m | $357.7m | $135.19 | -$4.99 |
| AI features | Base | 0.0 pp | $462.1m | $373.3m | $140.18 | $0.00 |
| AI features | Higher | +1.0 pp | $482.6m | $388.9m | $145.18 | +$4.99 |

Output spans across valid lower/base/higher cases are:

- Paid conversion/retention: **$80.7m EBIT**, **$82.6m FCFF**, **$24.52 per share**.
- AI features: **$41.1m EBIT**, **$31.2m FCFF**, **$9.99 per share**.

All six runs passed the accounting and liquidity checks. The final base rerun matched the original
base result, confirming that the sensitivity process restored the independent inputs correctly.

## V — reconciled result and partner evidence

The restored base case produced the same result as the original Lab 10 case: 2030 EBIT of
$462.1 million, 2030 FCFF of $373.3 million, and value per share of $140.18. The lower and higher
cases changed only the selected driver; all linked statements, cash and valuation quantities were
recalculated from that change.

For the paid conversion/retention driver, the higher case was $152.94 per share versus the base
of $140.18. The independently recomputed change is $152.94 − $140.18 = **+$12.75**. The lower
case was $128.42, or **−$11.76** from base. For AI features, the higher case was $145.18 versus
$140.18, a recomputed **+$4.99**; the lower case was $135.19, or **−$4.99**.

My prediction was correct on direction for both drivers. The realized result shows that the paid
conversion/retention shock had the larger effect over these stated ranges. The AI result was
smaller than the subscriber result because the AI scenario changed gross margin by one percentage
point, while the subscriber scenario changed revenue growth by two percentage points in every
forecast year and therefore also changed the scale of the working-capital and terminal cash flows.

**Partner exchange 2.** I showed my partner the AI higher case ($145.18) and base case ($140.18).
My partner recomputed the difference as +$4.99 and checked that the other driver remained at its
base value. The trace was: AI efficiency improves gross margin, which raises EBIT; higher EBIT
raises FCFF after tax; higher FCFF raises the explicit-period and terminal values. The accounting
checks passed in both cases.

**Partner exchange 3.** My partner asked: “How do you see AI affecting the company financially,
and how do you separate AI-driven revenue benefits from AI-driven cost effects?” I answered that
AI can improve learning features, engagement and eventually paid conversion, but it can also add
inference and product-development costs. This Lab 11 isolates the cost-efficiency channel through
gross margin; it does not claim that all AI revenue effects are captured in that one shock.

My partner also asked whether the ranking could be caused by the chosen ranges. Yes. The conclusion
is only that paid conversion/retention has the larger span **over these ranges**; a wider AI range
could change the ranking. We should not rank Duolingo and IBM by raw dollar changes because their
business scales and operating structures are different. IBM's comparable causal question is its
software and hybrid-cloud mix, while Duolingo's is engaged learners converting to and retaining
paid subscriptions.

## Sensitivity lesson and reflection

One-at-a-time sensitivity changes one independent input while resetting every other input to base,
then lets the statements and valuation recalculate. The selected range affects the ranking: a
larger or smaller shock can make a driver appear more or less influential. A sensitivity table is
not a probability forecast; it shows conditional outcomes under specified assumptions, not the
likelihood that any case will occur.

The driver that mattered most over these ranges was paid conversion and retention. The result that
surprised me was that a one-point AI margin improvement moved value by about $5 per share, which is
meaningful but less than the subscriber-growth shock. That reinforces the research priority of
tracking paid subscribers, retention and conversion while still monitoring AI costs and monetization.
