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
