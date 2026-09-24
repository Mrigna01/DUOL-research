# Final quality-control record

The final valid model was retained after all destructive tests ran on deep copies. Build results are machine-readable in `outputs/tables/run_status.json`.

| Audit area | Evidence / conclusion |
|---|---|
| Historical financials and fiscal periods | Three annual years extracted by exact date and filing type; 171 independent audit records include separately parsed original filing XBRL versus SEC API agreement and H1 statement cross-checks. |
| Units and denominators | USD millions, shares millions, rates decimals; price is USD/share. Shares must be positive; no incomplete or padded beta observations. |
| Revenue growth and margins | Ratios calculated from filings; annual 2026 targets are reconciled to actual H1, with forecast H2 as the residual. |
| Source labels | 120 year-specific driver rows; 24 named numeric drivers; guidance limited to actually disclosed 2026 items. Further boundaries are labelled in model_conventions.csv. |
| Balance sheets and cash | Every forecast year's component totals, cash bridge, equity, PPE, intangibles and NWC roll forward. Historical totals and cash bridges also pass. |
| UFCF and SBC | Independent formula check; D&A added back once; software and PPE capex included; SBC retained as economic cost; no duplicate future dilution factor. |
| Deferred revenue | Subtracted within operating NWC; deferred platform costs offset it. Terminal NWC uses terminal growth, not final explicit growth. |
| Cash and investments | June cash, short investments and long investments distinct; restricted cash excluded from excess liquidity; $100m operating cash reserve retained; future accumulated forecast cash not added to EV. |
| Beta | 61 monthly prices /60 returns, Aug2021–Aug2026; SPY, simple returns, intercept regression; covariance/variance independently agrees with regression. Adjusted-price/Blume alternatives reported. |
| Discount rate | 4.75% Treasury and4.14% ERP explicitly dated Sept1; source checked. Zero traditional debt means equity weight100%; no unsupported borrowing quote. |
| Terminal value | Spread positive; terminal cash flow positive; arithmetic independently agrees; contribution84.35% of EV disclosed; 20%/30% incremental-ROIC alternatives quantify reinvestment risk. |
| Periods | Only101/184 of forecast H2 remains afterSept21; actual future year-end dates/365; terminal discounted using same final date. |
| Equity bridge and price | Independent EV→equity→per-share calculation; Nasdaq independently confirms149.42 close; latest disclosed diluted estimate50.7m used with qualifications. |
| Sensitivity | All24 numeric drivers rerun full statements/checks; seven WACCs; joint bear/bull cases; rate/growth grid. Zero-effect financing/allocation cases disclosed. |
| Root solving | Five feasible independently solved one-variable roots, residual<0.000001/share; no feasible capex-only root within stated constraints is shown explicitly. |
| Check-breaking | Eleven tests block actual DCF calls, including a cash-floor-only failure where accounting still balances; original valid model restored. |
| Course reproduction | Exact Lab09 share count17.951349m resolves slide rounding: ABG291.751666→291.75; all11 known-answer checks pass displayed precision. |
| Notebook | All25 requested sections;24 code cells executed; zero error outputs. |
| Figures | Seven charts created in PNG/SVG from calculated results; reviewed for legibility, labels, dates and units. |
| Panel | Local-only HTTP page and valuation endpoint tested; gross-margin +1pp changes value from136.889140 to142.178087 with checks PASS. |
| Submission boundaries | Local artifacts complete. Human oral/partner review is not fabricated; external GitHub or course upload not performed. |

## Material judgment risks

The terminal model implies roughly101% returns on incremental measured reinvestment. Negative operating working capital and expensed R&D explain the arithmetic but do not prove sustainability. At20% incremental ROIC, value falls to125.32/share. The raw beta is0.8518 with standard error0.5146 and R-squared0.0451. Neither precision of the arithmetic nor passing accounting tests removes forecast uncertainty.

The September liquidity bridge is estimated, not observed. Taxes use a normalized rate and do not separately monetize the206.039m deferred-tax asset. Operating leases, long-lived nonoperating balances and investment holdings use simplified steady balances. These conventions are explicitly described in the notebook and LIMITATIONS.md.
