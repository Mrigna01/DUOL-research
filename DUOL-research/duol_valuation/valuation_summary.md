# DUOLINGO, INC. (NASDAQ: DUOL)
## PRO-FORMA VALUATION SUMMARY

**Valuation date: 2026-09-21, closing price. Research completed September 22, 2026.**

Base value is **$136.89 per diluted share**, compared with the **$149.42 market close**. This result depends on 2027–2030 growth and operating leverage, recurring stock-compensation expense and the discount rate. Posture: wait for evidence that revenue growth recovers and operating margins expand; rebuild the case if the filing-based triggers below are reached. Educational analysis, not an investment recommendation.

### Current market data

| Item | Value |
|---|---:|
| Latest completed DUOL close, Yahoo cross-checked to Nasdaq | $149.42 |
| Latest company estimated diluted shares | 50.700 million |
| Reported basic shares, June 30 (market-cap proxy) | 46.700 million |
| Market capitalization using reported basic shares | $6,977.914 million |
| Price times diluted shares (comparison basis) | $7,575.594 million |

### Model output and bridge ($ millions)

| Component | Value |
|---|---:|
| PV of remaining explicit cash flows | 878.249 |
| PV of terminal value | 4,732.633 |
| Enterprise value | 5,610.882 |
| Reported cash at June 30 | 1,180.887 |
| Reported short + long investments | 235.672 |
| Estimated economic cash accrued since June | 15.135 |
| Less known additional repurchases (approx.) | 2.297 |
| Less retained operating cash reserve | 100.000 |
| Traditional debt / extra lease adjustment | 0 / 0 |
| Equity value | 6,940.279 |
| Value per diluted share | **$136.89** |

### Discount rate

| Input | Value |
|---|---:|
| Raw DUOL / SPY beta | 0.851782 |
| Monthly closing prices / return observations | 61 / 60 |
| Period | August 2021–August 2026 |
| Beta standard error / R-squared | 0.5146 / 0.0451 |
| 95% beta confidence interval | -0.178 to 1.882 |
| Risk-free rate, September 1 Treasury convention | 4.75% |
| Equity risk premium, September 1 | 4.14% |
| Cost of equity | 8.2764% |
| Equity / traditional debt weights | 100% / 0% |
| Debt cost | Not applicable; zero weighted contribution |
| Normalized tax rate | 24% |
| WACC | **8.2764%** |

### Terminal assumptions

Terminal growth is 3.00%; 2031 UFCF is $350.933m; end-2030 terminal value is $6,651.020m. Terminal value contributes **84.35% of enterprise value**. Terminal EV/2031 revenue is 3.14x; EV/EBITDA including SBC expense is 13.16x. The base reinvestment arithmetic implies 100.8% incremental ROIC, which is a significant limitation, not a forecast of observed returns.

| convention                                    |   terminal_reinvestment |   terminal_fcf |   value_per_share |
|:----------------------------------------------|------------------------:|---------------:|------------------:|
| Base: operating balance drivers               |                 10.7699 |       350.9328 |          136.8891 |
| Steady-state 20% incremental ROIC             |                 54.2554 |       307.4473 |          125.3223 |
| Steady-state 30% incremental ROIC             |                 36.1703 |       325.5324 |          130.1328 |
| Mechanical final-year FCF growth (diagnostic) |                nan      |       384.3380 |          145.7747 |

### Forecast assumptions

|      Year |   Revenue $m |   EBIT margin |   SBC/revenue |   Capex $m |   Cash $m |
|----------:|-------------:|--------------:|--------------:|-----------:|----------:|
| 2026.0000 |    1207.0000 |        0.1010 |        0.1500 |    31.8725 | 1287.5735 |
| 2027.0000 |    1424.2600 |        0.1300 |        0.1400 |    37.6096 | 1658.6412 |
| 2028.0000 |    1652.1416 |        0.1650 |        0.1300 |    43.6271 | 2119.8231 |
| 2029.0000 |    1866.9200 |        0.2000 |        0.1200 |    49.2987 | 2674.2510 |
| 2030.0000 |    2053.6120 |        0.2250 |        0.1100 |    54.2285 | 3307.3851 |

All 120 year-specific inputs are labelled HISTORY / GUIDANCE / JUDGMENT in [assumptions.csv](assumptions.csv). FY2026 revenue, gross margin, SBC and tax inputs follow guidance; later growth/margin paths are judgment. The zero-debt treatment and balance conventions are explained in the notebook.

### Check status

**ALL 120 REQUIRED CHECKS PASSED — VALUATION ENABLED.**

| check_name                               | status   |   observations |
|:-----------------------------------------|:---------|---------------:|
| Historical balance                       | PASS     |              3 |
| Historical gross profit                  | PASS     |              3 |
| Historical EBIT                          | PASS     |              3 |
| Historical net income                    | PASS     |              3 |
| Historical assets sum                    | PASS     |              3 |
| Historical liabilities sum               | PASS     |              3 |
| Historical cash bridge                   | PASS     |              2 |
| Balance sheet                            | PASS     |              5 |
| Assets total                             | PASS     |              5 |
| Liabilities total                        | PASS     |              5 |
| Cash reconciliation                      | PASS     |              5 |
| PPE roll-forward                         | PASS     |              5 |
| Intangibles roll-forward                 | PASS     |              5 |
| Equity roll-forward                      | PASS     |              5 |
| Income statement                         | PASS     |              5 |
| CFO construction                         | PASS     |              5 |
| UFCF construction                        | PASS     |              5 |
| NWC roll-forward                         | PASS     |              5 |
| Debt roll-forward                        | PASS     |              5 |
| Minimum cash                             | PASS     |              5 |
| No invalid values                        | PASS     |              5 |
| Economically valid balances              | PASS     |              5 |
| Valid assumption: accrued_ratio          | PASS     |              1 |
| Valid assumption: ap_ratio               | PASS     |              1 |
| Valid assumption: ar_ratio               | PASS     |              1 |
| Valid assumption: buybacks               | PASS     |              1 |
| Valid assumption: capex_ratio            | PASS     |              1 |
| Valid assumption: da_ratio               | PASS     |              1 |
| Valid assumption: deferred_cost_ratio    | PASS     |              1 |
| Valid assumption: deferred_revenue_ratio | PASS     |              1 |
| Valid assumption: diluted_shares         | PASS     |              1 |
| Valid assumption: ga_ex_sbc              | PASS     |              1 |
| Valid assumption: gross_margin           | PASS     |              1 |
| Valid assumption: growth                 | PASS     |              1 |
| Valid assumption: investment_yield       | PASS     |              1 |
| Valid assumption: minimum_cash           | PASS     |              1 |
| Valid assumption: option_proceeds        | PASS     |              1 |
| Valid assumption: ppe_capex_share        | PASS     |              1 |
| Valid assumption: prepaid_ratio          | PASS     |              1 |
| Valid assumption: rd_ex_sbc              | PASS     |              1 |
| Valid assumption: sbc_ratio              | PASS     |              1 |
| Valid assumption: sm_ex_sbc              | PASS     |              1 |
| Valid assumption: tax_rate               | PASS     |              1 |
| Valid assumption: terminal_growth        | PASS     |              1 |
| Valid assumption: wacc                   | PASS     |              1 |
| Valid assumption: withholding_ratio      | PASS     |              1 |
| WACC > terminal growth                   | PASS     |              1 |

All 11 deliberately broken-model tests blocked valuation. 171 independent audit checks passed. The 11 ABG reference checks passed their disclosed rounding tolerances.

### Sensitivity results

| assumption      |   downside |     base |   upside |   absolute_sensitivity |   percentage_sensitivity |
|:----------------|-----------:|---------:|---------:|-----------------------:|-------------------------:|
| wacc            |   118.5241 | 136.8891 | 163.8670 |                45.3429 |                   0.3312 |
| growth          |   122.9031 | 136.8891 | 152.3727 |                29.4696 |                   0.2153 |
| sbc_ratio       |   126.3112 | 136.8891 | 147.4670 |                21.1558 |                   0.1545 |
| terminal_growth |   127.7761 | 136.8891 | 147.9101 |                20.1340 |                   0.1471 |
| rd_ex_sbc       |   131.6002 | 136.8891 | 142.1781 |                10.5779 |                   0.0773 |
| sm_ex_sbc       |   131.6002 | 136.8891 | 142.1781 |                10.5779 |                   0.0773 |
| ga_ex_sbc       |   131.6002 | 136.8891 | 142.1781 |                10.5779 |                   0.0773 |
| gross_margin    |   131.6002 | 136.8891 | 142.1781 |                10.5779 |                   0.0773 |
| capex_ratio     |   133.4096 | 136.8891 | 140.3687 |                 6.9591 |                   0.0508 |
| tax_rate        |   133.9356 | 136.8891 | 139.8427 |                 5.9071 |                   0.0432 |

Ranking depends on the stated shock sizes: revenue growth ±3 points; SBC ±2 points; WACC ±1 point; gross margin and expense ratios ±1 point. It is not a unit-free ranking of business importance. Four financing/allocation assumptions have zero direct FCFF valuation effect but still rerun cash, equity and liquidity checks.

### Seven discount rates

|   wacc |   enterprise_value |   equity_value |   value_per_share |   terminal_share_ev |
|-------:|-------------------:|---------------:|------------------:|--------------------:|
| 0.0528 |         13326.3588 |     14655.7558 |          289.0682 |              0.9283 |
| 0.0628 |          9182.9743 |     10512.3713 |          207.3446 |              0.8989 |
| 0.0728 |          6978.6578 |      8308.0548 |          163.8670 |              0.8706 |
| 0.0828 |          5610.8825 |      6940.2794 |          136.8891 |              0.8435 |
| 0.0928 |          4679.7738 |      6009.1708 |          118.5241 |              0.8174 |
| 0.1028 |          4005.2785 |      5334.6754 |          105.2204 |              0.7923 |
| 0.1128 |          3494.3639 |      4823.7608 |           95.1432 |              0.7681 |

### Named operating cases

| case                                  |   value_per_share |   terminal_share_ev |   minimum_forecast_cash | check_status      |
|:--------------------------------------|------------------:|--------------------:|------------------------:|:------------------|
| Bear                                  |          113.5447 |              0.8480 |               1256.4891 | PASS              |
| Base                                  |          136.8891 |              0.8435 |               1287.5735 | PASS              |
| Bull                                  |          164.2989 |              0.8413 |               1319.6042 | PASS              |
| Incorrect sum of isolated bear shocks |          112.3252 |            nan      |                nan      | NOT A MODEL RERUN |

Bear jointly reduces growth by 3 points and gross margin by 1 point, and raises R&D excluding SBC by 1 point; bull reverses these. The sum of isolated impacts is shown only to demonstrate why a joint rerun is necessary.

### Market-implied expectations

| variable                    |   base_case |   market_implied |   residual | status                             |   search_low |   search_high |
|:----------------------------|------------:|-----------------:|-----------:|:-----------------------------------|-------------:|--------------:|
| WACC                        |      0.0828 |           0.0776 |    -0.0000 | SOLVED; FULL MODEL CHECKS PASS     |       0.0410 |        0.3000 |
| Terminal growth             |      0.0300 |           0.0356 |     0.0000 | SOLVED; FULL MODEL CHECKS PASS     |      -0.0300 |        0.0600 |
| Revenue growth path shift   |      0.0000 |           0.0245 |     0.0000 | SOLVED; FULL MODEL CHECKS PASS     |      -0.1000 |        0.1500 |
| Operating margin path shift |      0.0000 |           0.0237 |     0.0000 | SOLVED; FULL MODEL CHECKS PASS     |      -0.0600 |        0.1000 |
| Gross margin path shift     |      0.0000 |           0.0237 |     0.0000 | SOLVED; FULL MODEL CHECKS PASS     |      -0.0800 |        0.1500 |
| Capex / revenue             |      0.0264 |         nan      |   nan      | NO FEASIBLE ROOT IN STATED BRACKET |       0.0050 |        0.1200 |

Within this model, holding all other assumptions constant, the current share price requires the solved value in each row. Path shifts are percentage-point additions to every forecast year; a margin shift reduces G&A excluding SBC by the same amount. These are alternative explanations, not claims about investors' actual beliefs. The capex-only solve has no feasible root in the stated interval after preserving already-incurred H1 capex and the model checks.

### Review triggers

- Reported gross margin below 70.6%: rerun the 1-point margin downside, $131.60/share.
- Revenue trajectory at least 3 percentage points below the forecast growth path: rerun the growth downside, $122.90/share.
- SBC above 17% of revenue: rerun the 2-point SBC downside, $126.31/share.

These triggers require reassessment using the next two quarterly filings, including seasonality and full-year guidance; they are not automatic trading rules.

### Data and methodology limitations

- Valuation date is September 21, 2026, the latest completed close available when researched September 22. The intraday September 22 quote was not mixed with closing prices.
- Treasury 4.75% and ERP 4.14% are the paired September 1, 2026 Damodaran inputs. Treasury/FRED direct downloads timed out; the model does not claim a September 21 Treasury observation.
- Financial anchor is June 30, 2026. FY2026 combines filed H1 and projected H2. Only 101/184 of H2 economic cash flow remains after September 21. H2 cash generation is spread uniformly for the date bridge (JUDGMENT), despite subscription seasonality. ACT/365 year-end timing uses actual future dates.
- Interim-to-date liquidity is an economic cash estimate: H2 UFCF plus after-tax interest, prorated to the valuation date, less approximately $2.297m known additional repurchases. It charges SBC as a cash-equivalent reserve. It is not an observed September balance sheet; future forecast cash is not added to enterprise value.
- Operating leases remain operating: rent is embedded in expense ratios, accrued current lease obligations in operating liabilities, ROU assets and long-term lease balances held constant. No lease debt is added to WACC or subtracted again in the equity bridge. This is a simplified renewal assumption, not a contractual lease schedule.
- Deferred tax assets, goodwill, tax balances, other long-term assets and investments are held at the interim values (JUDGMENT); no acquisitions, new debt, dividends, FX or investment mark-to-market gains are modeled. Deferred tax assets are not separately added to equity value. Normalized taxes omit possible future tax-asset cash savings.
- Subscription bookings minus revenue approximates deferred-revenue change. Historical balances calibrate the forecast. User counts, subscriber conversion and a revenue-per-year-end-payer proxy explain economics but are not independently compounded into revenue: adding those drivers would introduce unsupported ARPU/churn assumptions.
- SBC is included once in operating expenses and is not added back to UFCF. Accounting CFO adds SBC and credits equity; withholding and repurchases reduce cash/equity. Future share growth is not also imposed on the valuation denominator. The 50.7m company estimate includes outstanding unvested awards; this is a conservative simplified dilution convention, not an option-pricing valuation. Reported basic shares of 46.7m are a June-date market-cap proxy.
- Forecast SBC allocation of 70% R&D, 10% marketing and 20% G&A is JUDGMENT for presentation; total expense drives value. D&A is already inside expense ratios and is allocated between PPE and intangibles by opening carrying value (JUDGMENT). Frozen balances and allocation conventions are disclosed in model_conventions.csv.
- Terminal working capital grows at terminal growth, not the final explicit 10% revenue growth rate. The base implies unusually high incremental returns on measured reinvestment because subscription deferred revenue funds operations and R&D is expensed. Explicit 20% and 30% incremental-ROIC alternatives show this risk.
- Raw beta has low R-squared and a wide confidence interval. SPY adjusted-return beta and Blume beta are reported as alternatives; no dealer peer beta is transplanted to DUOL.
- Full video audiovisual playback was unavailable in the web reader; both full slide decks, spoken notes and caption files were reviewed. The ABG reference uses the exact 17.951349m share count supplied in Lab09 and matches the displayed $291.75 base and rounded scenario answers.
- The course also requires student/partner oral predictions and sceptic discussion. Agent-authored predictions and simulated questions are provided transparently; no human peer review or oral participation is claimed. No GitHub upload or course submission has been performed.


### Primary sources

- [FY2025 10-K](https://www.sec.gov/Archives/edgar/data/1562088/000162828026012494/duol-20251231.htm), statements pp83–87; Notes 5, 7, 10, 12–13. Existing local filing preserved.
- [FY2024 10-K](https://www.sec.gov/Archives/edgar/data/1562088/000156208825000042/duol-20241231.htm), FY2023 comparatives and KPIs.
- [Q2 2026 shareholder letter](https://www.sec.gov/Archives/edgar/data/1562088/000162828026053299/q2fy26duolingo6-30x26share.htm), outlook p10, dilution p11 and financial appendices.
- [Q2 2026 10-Q](https://www.sec.gov/Archives/edgar/data/1562088/000162828026053603/duol-20260630.htm), H1 statements.
- [Damodaran September risk inputs](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/home.htm), frozen snapshot in data/raw.
- [Course tutorial](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-05/pro-forma-abg-tutorial.md), full local slides and captions.

Reproduce: `python duol_valuation/run.py` from the parent DUOL-research directory.
