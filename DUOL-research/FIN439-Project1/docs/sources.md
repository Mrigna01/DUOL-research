# Source map and conventions

Valuation date: September 21, 2026. USD millions and millions of shares unless stated. Inputs are retained snapshots, not live feeds. Derived working CSVs are transparent extractions; they are not additional primary sources.

| Working input | Retained evidence / locator | Definition |
| --- | --- | --- |
| data/historical_financials.csv | docs/DUOL-10-K.pdf; data/sources/annual_inline_xbrl.json and companyfacts.json; data/source_ledger.csv | FY2023-2025; FY2025 filing accession 0001628280-26-012494; financial statements printed pp83-86, PDF pp119-122 |
| Tax release and EPS | Same filing, PDF pp85/120 and EPS Note13 | $256.7m tax valuation-allowance release; reported diluted EPS $8.57; distinguish total tax line from release |
| data/h1_2026.csv | Q2 10-Q accession 0001628280-26-053603 via companyfacts snapshot; retained q2-2026-letter.html | Filed June balances and H1 flows; not September balances |
| 2026 guidance and diluted shares | data/sources/q2-2026-letter.html, pp10-11 | Revenue $1,207m; gross margin 71.6%; SBC 15%; tax 23-25%; latest diluted estimate 50.7m, not weighted-average EPS shares |
| data/monthly_prices.csv | data/sources/DUOL-prices.json and SPY-prices.json | 61 monthly closes August2021-August2026 produce 60 returns; unadjusted-close convention disclosed |
| Price $149.42 | data/sources/DUOL-daily.json and nasdaq-price.json | September21 close; ignore incomplete September22 intraday observation |
| Treasury 4.75%, ERP 4.14% | data/sources/damodaran-retrieved-2026-10-16.html | September1 input vintage, corroborated by previous-month section of later retrieval, not a September snapshot |
| COUR/UDMY exclusions | data/sources/cour-fy2025-results.html and cour-merger-2026-05-11.html | Annual GAAP loss; May11 combination and 0.800 exchange ratio; no unmatched post-merger numerator |
| Known-answer fixture | evidence/abg_known_answer.py; data/sources/pro-forma-abg-tutorial.md | Original Lab09 fixture compared with published rounded $291.75 |

Primary links: [FY2025 filing](https://www.sec.gov/Archives/edgar/data/1562088/000162828026012494/0001628280-26-012494-index.htm); [Q2 letter](https://www.sec.gov/Archives/edgar/data/1562088/000162828026053299/q2fy26duolingo6-30x26share.htm); [Q2 10-Q](https://www.sec.gov/Archives/edgar/data/1562088/000162828026053603/duol-20260630.htm); [Damodaran](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/home.htm); peer links in comparable-policy.md.

Dated liquidity is estimated from the accounting cash-flow forecast: prorate H2 CFO, CFI and recurring CFF by 83/184, date estimated repurchase cash separately, add June cash and investments, and deduct the $100m reserve. Noncash SBC is added back in accounting cash; withholding is financing cash. Future FCFF retains SBC as an economic cost. No terminal cash balance is added to enterprise value.

The source inputs are in data/liquidity_bridge.csv. H1 recognized repurchases of $70.278m less $69.603m cash payments leave a $0.675m payable (Q2 10-Q pp9-11; recognized and paid amounts also appear in retained companyfacts.json). Approximately $71.9m purchased through August 1 less $70.278m recognized in H1 implies $1.622m new trades. Assume these new trades and the June payable settle by September 21, making estimated payments $2.297m; the cumulative figure is rounded, not an exact dated cash observation. No additional unreported repurchases are assumed. The June payable is removed from operating NWC; its settlement is financing cash and does not reduce equity again. The forecasting statements retain filed H1 totals unchanged; only the operating NWC classification is adjusted. outputs/liquidity_bridge.csv makes the components visible.

Holding all else fixed, treating the $0.675m payable as still unsettled at the valuation date would increase cash and leave an equal financing liability: equity value is unchanged if both sides are included. The chosen settled convention avoids omitting that obligation. Portfolio investments are held constant in forecasts; interest is excluded from operating FCFF. Operating leases remain operating, and financial debt is zero. Terminal investment is recomputed at perpetual growth; implied terminal ROIC is high and explicitly stressed at 20%.

Original labs and their file hashes establish research lineage. Later source retrievals are labeled later verification. No cutoff-sensitive October operating information is substituted into the September model. Source hashes are retained in evidence/source-hashes.json.

The 50.7m diluted share count is the June 30 estimate disclosed in August, carried forward to the valuation date. It is not a measured September share count. Unknown subsequent awards, treasury-stock-method changes and unreported repurchases are not invented; a fresh share inventory would require a valuation refresh.
