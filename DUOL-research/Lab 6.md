# Duolingo (DUOL) Reverse DCF Inputs

Prepared September 10, 2026. Company financial amounts are in USD millions unless otherwise indicated. Historical company data are sourced primarily from Duolingo's Form 10-K for the year ended December 31, 2025. Forecast inputs are analyst assumptions, not company-reported facts.

## Final model inputs

| Input | Value | Unit | As-of date | Source / Locator | Notes |
|---|---:|---|---|---|---|
| Starting FCFF | 360.424 | $m | Year ended Dec. 31, 2025 | [2025 Form 10-K](./DUOL-10-K.pdf), Item 7, FCF reconciliation, filing p. 67 / PDF p. 96; Statement of Cash Flows, filing p. 86 / PDF p. 122 | OCF + after-tax interest - capitalized software/intangibles - PP&E purchases. Calculation below. |
| Growth Year 1 | 15.0% | annual FCFF growth | Forecast year 2026 | 10-K Item 7, filing pp. 60-71 / PDF pp. 85-101; [Q2 2026 10-Q](https://www.sec.gov/Archives/edgar/data/1562088/000162828026053603/duol-20260630.htm), Item 2 | Forecast assumption. Anchored to 15%-18% FY2026 revenue guidance and tempered by lower planned profitability and mixed quarterly FCF. |
| Growth Year 2 | 18.0% | annual FCFF growth | Forecast year 2027 | Same operating sources as Year 1 | Forecast assumption. Allows operating leverage after 2026 investment spending while remaining far below 2023-2025 historical FCFF growth. |
| Growth Year 3 | 16.0% | annual FCFF growth | Forecast year 2028 | Same operating sources as Year 1 | Forecast assumption. Continued subscriber/product scaling, with maturation beginning to reduce growth. |
| Growth Year 4 | 13.0% | annual FCFF growth | Forecast year 2029 | Same operating sources as Year 1 | Forecast assumption. Explicit fade toward a mature-company rate. |
| Growth Year 5 | 10.0% | annual FCFF growth | Forecast year 2030 | Same operating sources as Year 1 | Forecast assumption. Final explicit year continues the fade before the terminal period. |
| WACC | 8.5286% | annual discount rate | Sept. 10, 2026 | Calculated below using current market inputs | 100% equity weight because reported financial debt is zero. Code value: `0.085286`. |
| Terminal growth | 3.0% | perpetual annual growth | Long-run period after 2030 | [Federal Reserve longer-run inflation goal](https://www.federalreserve.gov/monetarypolicy/2026-07-mpr-statement.htm); [CBO 2026-2036 outlook](https://www.cbo.gov/publication/62105) | Conservative nominal rate below the roughly 3.8% combination of 2% inflation and 1.8% projected real GDP growth. Not a continuation of Duolingo's short-term growth. |
| Cash only (reference) | 1,036.389 | $m | Dec. 31, 2025 | 10-K, Consolidated Balance Sheets, filing p. 82 / PDF p. 118 | Literal cash and cash equivalents; not the value selected for `NON_OPERATING_CASH`. |
| Cash plus investments | 1,275.565 | $m | Dec. 31, 2025 | 10-K, Consolidated Balance Sheets, filing p. 82 / PDF p. 118 | Confirmed model value: $1,036.389 cash + $104.078 short-term investments + $135.098 long-term investments. |
| Debt | 0.000 | $m | Dec. 31, 2025 | 10-K, Consolidated Balance Sheets, filing p. 82 / PDF p. 118; Note 8, Leases, filing p. 104 / PDF p. 146 | No financial borrowing debt is reported. The model excludes $100.983m operating-lease liabilities because FCFF also leaves operating lease payments in operating cash flow. |
| Diluted shares | 48.308 | million shares | Year ended Dec. 31, 2025 | 10-K, Note 13, Earnings Per Share, filing p. 110 / PDF p. 156 | Diluted weighted-average shares, as specifically required. This is not the current basic share count. |
| Current stock price | 145.16 | $/Class A share | Sept. 10, 2026, 4:56:23 p.m. EDT | Live U.S. equity market-data quote for NASDAQ: DUOL; [Nasdaq quote page](https://www.nasdaq.com/market-activity/stocks/duol) | Latest recorded trade, equivalent to 20:56:23 UTC. Stored as `COMPANY_TARGET_SHARE_PRICE` for the reverse DCF. |

## FCFF calculation

The assignment formula is:

`FCFF = Operating Cash Flow + Interest Expense x (1 - Tax Rate) - CapEx`

Duolingo's 2025 statement of operations reports interest income but no interest expense, and its cash-flow statement reports no interest paid. Therefore, the interest add-back is zero. The filing's own FCF definition treats both capitalized software/intangible purchases and PP&E purchases as capital expenditures.

| Component | Value | Unit | As-of date | Source / Locator |
|---|---:|---|---|---|
| Net cash provided by operating activities | 387.823 | $m | FY2025 | 10-K, Statement of Cash Flows, filing p. 86 / PDF p. 122 |
| Interest expense | 0.000 | $m | FY2025 | 10-K, Statement of Operations, filing p. 84 / PDF p. 120; no interest expense reported |
| Tax rate used on interest | 21.0% | rate | FY2025 | 10-K, Note 9, Income Taxes, federal statutory rate reconciliation, filing p. 106 / PDF p. 148 |
| After-tax interest add-back | 0.000 | $m | FY2025 | $0.000 x (1 - 21.0%) |
| Capitalized software and intangible-asset purchases | 9.303 | $m | FY2025 | 10-K, Statement of Cash Flows, filing p. 86 / PDF p. 122 |
| Property and equipment purchases | 18.096 | $m | FY2025 | Same locator |
| Total CapEx | 27.399 | $m | FY2025 | $9.303 + $18.096 |

Arithmetic:

`FCFF = $387.823m + $0.000m x (1 - 21.0%) - $27.399m = $360.424m`

This equals Duolingo's reported 2025 free cash flow of $360.424m in Item 7.

## Growth forecast rationale

### Recent history

| Period | Revenue / FCFF evidence | Source |
|---|---|---|
| FY2023 | Revenue $531.109m; reconstructed FCFF $139.930m | 10-K, Statements of Operations and Cash Flows, filing pp. 84 and 86 / PDF pp. 120 and 122 |
| FY2024 | Revenue $748.024m (+40.8%); FCFF $264.373m (+88.9%) | Same statements and Item 7 |
| FY2025 | Revenue $1,037.589m (+38.7%); FCFF $360.424m (+36.3%) | 10-K, Item 7 and financial statements |
| First half 2026 | Revenue $590.421m (+22.2%); FCFF $226.416m (+19.6%) | Q2 2026 10-Q, Statements of Operations and Item 2 FCF reconciliation |
| Q2 2026 | Revenue $298.454m (+18.3%); FCFF $78.630m (-8.9%) | Q2 2026 10-Q, Item 2 |

Item 7 explains that 2025 revenue growth was driven mainly by a larger average paid-subscriber base, while advertising benefited from increased DAUs. It also shows operating leverage: revenue grew 39%, operating expenses grew 27%, and operating margin increased from 8% to 13%. However, gross margin declined from 73% to 72%, partly because of AI-related costs and revenue mix.

Recent results point to deceleration. In the [Q2 2026 shareholder letter filed with the SEC](https://www.sec.gov/Archives/edgar/data/1562088/000162828026053299/q2fy26duolingo6-30x26share.htm), management maintained FY2026 targets of 15%-18% revenue growth and 10%-12% bookings growth. Management is prioritizing product and user investment, which may suppress near-term margins. First-half FCFF still rose 19.6%, but Q2 FCFF declined 8.9% because capital spending increased and quarterly operating cash flow softened.

The proposed sequence is therefore 15%, 18%, 16%, 13%, and 10%. Year 1 is conservative relative to first-half FCFF growth and aligned with management's revenue range. Year 2 assumes some payoff from 2026 investment. Years 3-5 fade progressively as the business becomes larger. These are reasoned analyst assumptions, not directly sourced company forecasts, and should be sensitivity-tested.

## WACC calculation

### Inputs

| WACC component | Value | Unit | As-of date | Source / derivation |
|---|---:|---|---|---|
| Risk-free rate | 4.844% | annual yield | Sept. 10, 2026 | U.S. 10-year Treasury market yield at 22:10:55; [market history](https://www.investing.com/rates-bonds/u.s.-10-year-bond-yield-historical-data). Latest official Federal Reserve H.15 observation available during preparation was 4.80% for Sept. 8. |
| Equity beta | 0.89 | beta coefficient | Sept. 10, 2026 | [StockAnalysis statistics](https://stockanalysis.com/stocks/duol/statistics/), data attributed to S&P Global Market Intelligence and updated Sept. 10, 2026 |
| Equity risk premium | 4.14% | annual premium | Sept. 1, 2026 | [Aswath Damodaran, NYU Stern implied ERP](https://pages.stern.nyu.edu/adamodar/New_Home_Page/home.htm), trailing-12-month adjusted-payout estimate |
| Cost of equity | 8.5286% | annual rate | Sept. 10, 2026 | 4.844% + 0.89 x 4.14% |
| Pre-tax cost of debt | N/A - unresolved | annual rate | Sept. 10, 2026 | Duolingo has no financial debt or observable company borrowing rate. No fabricated rate is inserted. |
| Tax rate | 21.0% | rate | FY2025 | 10-K, Note 9, federal statutory rate, filing p. 106 / PDF p. 148. The reported -127.0% effective rate is unsuitable because of the valuation-allowance release and equity-compensation effects. |
| After-tax cost of debt | N/A - unresolved | annual rate | Sept. 10, 2026 | Pre-tax debt cost is unavailable; this has no valuation effect at a 0% debt weight. |
| Market value of equity | 6,791.495 | $m | Sept. 10, 2026, 4:56:23 p.m. EDT | Live market-data quote: reported market capitalization $6,791,494,808 |
| Financial debt | 0.000 | $m | Dec. 31, 2025 | 10-K balance sheet; no borrowing debt reported |
| Equity weight | 100.0% | capital weight | Sept. 10, 2026 | $6,791.495m / ($6,791.495m + $0.000m) |
| Debt weight | 0.0% | capital weight | Sept. 10, 2026 | $0.000m / ($6,791.495m + $0.000m) |

Calculations:

`Cost of Equity = 4.844% + 0.89 x 4.14% = 8.5286%`

`After-tax Cost of Debt = N/A x (1 - 21.0%) = N/A`

`WACC = 100.0% x 8.5286% + 0.0% x N/A = 8.5286%`

The undefined debt cost does not contaminate the calculation because its weight is exactly zero. A target-capital-structure WACC would require a separately justified debt weight and synthetic borrowing spread; neither is supplied by the filing.

## Terminal growth rationale

The proposed 3.0% terminal rate is a conservative nominal long-run rate. The Federal Reserve reaffirmed a 2% longer-run PCE inflation goal in 2026, while CBO projects average real GDP growth of 1.8% from 2027 through 2036. Combining those mechanically would suggest nominal economic growth near 3.8%, but 3.0% provides a margin of safety and avoids assuming that Duolingo can outgrow the economy forever. It is materially below every explicit-period FCFF growth assumption.

## Cash, debt, and share-count interpretation

`dcf.py` adds `NON_OPERATING_CASH` to enterprise value and subtracts `DEBT`. The strict assignment wording supports cash and cash equivalents of $1,036.389m. However, Duolingo also holds $239.176m of short- and long-term marketable investments that appear financial rather than operating. The confirmed model treatment includes them, producing $1,275.565m. Relative to cash only, this adds about $4.95 per diluted share.

Debt should mean interest-bearing financial debt in this simplified FCFF model. Including operating-lease liabilities as debt without also adjusting operating cash flow for lease financing would mix accounting treatments. Accordingly, proposed debt is zero.

The assignment explicitly asks for diluted weighted-average shares from the EPS note, and `dcf.py` divides equity value by that input. The proposed 48.308m therefore follows the assignment. For a live market valuation, current fully diluted shares would be conceptually preferable, but that is a different requirement and would need a separate reconciliation.

## Unresolved assumptions

- **Cash definition:** resolved by confirmation. The model includes cash plus short- and long-term investments, totaling $1,275.565m.
- **Growth rates:** 15%, 18%, 16%, 13%, and 10% are analyst forecasts supported by historical and management evidence, not company guidance for FCFF.
- **Beta methodology:** the 0.89 provider beta is sourced but its precise lookback/frequency is not disclosed on the cited page. An industry beta or independently calculated regression would give a different WACC.
- **Debt cost:** unresolved and intentionally left N/A because Duolingo has no financial debt. It has no effect on WACC at a zero debt weight.
- **Share count:** 48.308m is the required historical diluted weighted-average count, not a current fully diluted count.
- **Market price:** $145.16 is timestamped market data and must be refreshed if the valuation date changes.

## Final `dcf.py` input block

The confirmed cash-plus-investments version is:

```python
STARTING_FCFF = 360.424
GROWTH_RATES = [0.15, 0.18, 0.16, 0.13, 0.10]
WACC = 0.085286
TERMINAL_GROWTH = 0.03
NON_OPERATING_CASH = 1275.565
DEBT = 0.0
DILUTED_SHARES = 48.308
```

No placeholder comment is included inside `dcf.py` because each model value above has either direct filing support or an explicit, sourced estimation method. The unresolved debt cost is not a `dcf.py` input and has zero weight in WACC.

## Valuation floor and conditional call

- **Company DCF value:** $251.99 per diluted share using the sourced historical inputs and documented forecast assumptions above.
- **Sensitivity grid:** $166.53 to $268.11 per share across WACC values of 9%-11% and terminal-growth values of 2%-4%. The $166.53 lower-right valuation case uses the highest WACC (11%) and lowest terminal growth (2%) in the grid.
- **Growth implied by the recorded $145.16 market price:** a uniform shift of -15.077219 percentage points from the forecast path. This produces annual FCFF growth of approximately -0.077%, 2.923%, 0.923%, -2.077%, and -5.077%. Starting FCFF, WACC, terminal growth, cash and investments, debt, and diluted shares are held fixed. This is an implied assumption under the model, not proof that the shares are mispriced.
- **Conditional call:** Initiate if DUOL trades below approximately $166.53 per share and the next quarterly report does not materially weaken the operating assumptions; otherwise, watch-defer. At the recorded $145.16 price, the price condition is met, but execution should still be checked against the next operating result.
- **One item to monitor:** next-quarter operating margin. A material deterioration would challenge the forecast assumption that investment spending eventually converts into operating leverage and FCFF growth.

## Sensitivity grid

Value per diluted share, holding starting FCFF, the five explicit growth rates, cash and investments, debt, and diluted shares fixed:

| WACC / Terminal growth | 2.0% | 3.0% | 4.0% |
|---:|---:|---:|---:|
| 9.0% | $209.01 | $233.63 | $268.11 |
| 10.0% | $185.10 | $202.90 | $226.64 |
| 11.0% | $166.53 | $179.89 | $197.06 |

Any combination for which terminal growth is greater than or equal to WACC is invalid. None of the configured combinations violates that condition.

## Reverse DCF results

### Training case

- Target price: $30.00 per share.
- Training inputs held fixed: starting FCFF $100.000m; growth rates 8%, 6%, 5%, 4%, and 3%; WACC 10%; terminal growth 3%; non-operating cash $50.000m; debt $300.000m; diluted shares 50.000m.
- Solved uniform growth shift: **+1.777948 percentage points**.
- Shifted growth path: approximately 9.777948%, 7.777948%, 6.777948%, 5.777948%, and 4.777948%.
- Resulting DCF value: $30.000000 per share.

### Duolingo case

- Target price: $145.16 per share, recorded Sept. 10, 2026 at 4:56:23 p.m. EDT.
- Company inputs held fixed: starting FCFF $360.424m; growth rates 15%, 18%, 16%, 13%, and 10%; WACC 8.5286%; terminal growth 3%; non-operating cash and investments $1,275.565m; debt $0.000m; diluted shares 48.308m.
- Solved uniform growth shift: **-15.077219 percentage points**.
- Shifted growth path: approximately -0.077219%, 2.922781%, 0.922781%, -2.077219%, and -5.077219%.
- Resulting DCF value: $145.160000 per share.

Both reverse-DCF results are implied growth assumptions conditional on the inputs held fixed. They are not proof of mispricing.

## Complete `python dcf.py` output

```text
FCFF Year 1: 414.4876
FCFF Year 2: 489.0954
FCFF Year 3: 567.3506
FCFF Year 4: 641.1062
FCFF Year 5: 705.2168
Present value of five explicit FCFF: 2171.4955
Terminal value at Year 5: 13138.4679
Present value of terminal value: 8726.1710
Enterprise value: 10897.6665
Equity value: 12173.2315
Value per diluted share: 251.9920
Present value of terminal value as share of enterprise value: 0.8007

Sensitivity grid: value per diluted share ($)
WACC / Terminal growth | 2.0%    | 3.0%    | 4.0%
-----------------------+---------+---------+--------
9.0%                   | $209.01 | $233.63 | $268.11
10.0%                  | $185.10 | $202.90 | $226.64
11.0%                  | $166.53 | $179.89 | $197.06

Reverse DCF - training inputs: uniform shift to all five explicit growth rates
Target share price: $30.00
Search bracket: -20.00% to +10.00%
Inputs held fixed: starting FCFF=$100.000m; base growth rates=['8.00%', '6.00%', '5.00%', '4.00%', '3.00%']; WACC=10.0000%; terminal growth=3.00%; non-operating cash=$50.000m; debt=$300.000m; diluted shares=50.000m
Solved uniform growth shift: +1.777948%
Shifted growth rates: ['9.777948%', '7.777948%', '6.777948%', '5.777948%', '4.777948%']
DCF value per diluted share at solution: $30.000000
Interpretation: implied growth shift for the stated fixed inputs; not proof of mispricing.

Reverse DCF - Duolingo company inputs: uniform shift to all five explicit growth rates
Target share price: $145.16
Search bracket: -20.00% to +10.00%
Inputs held fixed: starting FCFF=$360.424m; base growth rates=['15.00%', '18.00%', '16.00%', '13.00%', '10.00%']; WACC=8.5286%; terminal growth=3.00%; non-operating cash=$1275.565m; debt=$0.000m; diluted shares=48.308m
Solved uniform growth shift: -15.077219%
Shifted growth rates: ['-0.077219%', '2.922781%', '0.922781%', '-2.077219%', '-5.077219%']
DCF value per diluted share at solution: $145.160000
Interpretation: implied growth shift for the stated fixed inputs; not proof of mispricing.
```
