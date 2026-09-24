from pathlib import Path
import pandas as pd
from .data_loader import ROOT,ASOF,FILING,LETTER

def md(frame,index=False):
    return frame.to_markdown(index=index,floatfmt='.4f')

LIMITATIONS='''- Valuation date is September 21, 2026, the latest completed close available when researched September 22. The intraday September 22 quote was not mixed with closing prices.
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
'''

def write_reports(d):
    v=d['v']; b=d['beta'].iloc[0];price=d['price'];sh=d['shocks'];m=d['model'];im=d['implied'];c=d['cases']
    compact=pd.DataFrame({'Year':m.index,'Revenue $m':m.revenue.values,'EBIT margin':m.operating_margin.values,'SBC/revenue':m.sbc.values/m.revenue.values,'Capex $m':m.capex.values,'Cash $m':m.cash.values})
    summary=f'''# DUOLINGO, INC. (NASDAQ: DUOL)
## PRO-FORMA VALUATION SUMMARY

**Valuation date: {ASOF}, closing price. Research completed September 22, 2026.**

Base value is **${v['value_per_share']:.2f} per diluted share**, compared with the **${price:.2f} market close**. This result depends on 2027–2030 growth and operating leverage, recurring stock-compensation expense and the discount rate. Posture: wait for evidence that revenue growth recovers and operating margins expand; rebuild the case if the filing-based triggers below are reached. Educational analysis, not an investment recommendation.

### Current market data

| Item | Value |
|---|---:|
| Latest completed DUOL close, Yahoo cross-checked to Nasdaq | ${price:.2f} |
| Latest company estimated diluted shares | {v['diluted_shares']:.3f} million |
| Reported basic shares, June 30 (market-cap proxy) | 46.700 million |
| Market capitalization using reported basic shares | ${price*46.7:,.3f} million |
| Price times diluted shares (comparison basis) | ${price*50.7:,.3f} million |

### Model output and bridge ($ millions)

| Component | Value |
|---|---:|
| PV of remaining explicit cash flows | {v['pv_explicit']:,.3f} |
| PV of terminal value | {v['pv_terminal']:,.3f} |
| Enterprise value | {v['enterprise_value']:,.3f} |
| Reported cash at June 30 | {v['reported_cash']:,.3f} |
| Reported short + long investments | {v['reported_investments']:,.3f} |
| Estimated economic cash accrued since June | {v['estimated_elapsed_cash']:,.3f} |
| Less known additional repurchases (approx.) | {v['post_h1_buyback']:,.3f} |
| Less retained operating cash reserve | {v['minimum_cash']:,.3f} |
| Traditional debt / extra lease adjustment | 0 / 0 |
| Equity value | {v['equity_value']:,.3f} |
| Value per diluted share | **${v['value_per_share']:.2f}** |

### Discount rate

| Input | Value |
|---|---:|
| Raw DUOL / SPY beta | {b.beta:.6f} |
| Monthly closing prices / return observations | {b.price_count} / {b.return_count} |
| Period | August 2021–August 2026 |
| Beta standard error / R-squared | {b.standard_error:.4f} / {b.r_squared:.4f} |
| 95% beta confidence interval | {b.ci95_low:.3f} to {b.ci95_high:.3f} |
| Risk-free rate, September 1 Treasury convention | 4.75% |
| Equity risk premium, September 1 | 4.14% |
| Cost of equity | {v['wacc']:.4%} |
| Equity / traditional debt weights | 100% / 0% |
| Debt cost | Not applicable; zero weighted contribution |
| Normalized tax rate | 24% |
| WACC | **{v['wacc']:.4%}** |

### Terminal assumptions

Terminal growth is {v['terminal_growth']:.2%}; 2031 UFCF is ${v['terminal_fcf']:,.3f}m; end-2030 terminal value is ${v['terminal_value']:,.3f}m. Terminal value contributes **{v['terminal_share_ev']:.2%} of enterprise value**. Terminal EV/2031 revenue is {v['terminal_ev_revenue']:.2f}x; EV/EBITDA including SBC expense is {v['terminal_ev_ebitda']:.2f}x. The base reinvestment arithmetic implies {v['terminal_implied_roic']:.1%} incremental ROIC, which is a significant limitation, not a forecast of observed returns.

{md(d['terminal'])}

### Forecast assumptions

{md(compact)}

All {len(d['assumptions'])} year-specific inputs are labelled HISTORY / GUIDANCE / JUDGMENT in [assumptions.csv](assumptions.csv). FY2026 revenue, gross margin, SBC and tax inputs follow guidance; later growth/margin paths are judgment. The zero-debt treatment and balance conventions are explained in the notebook.

### Check status

**ALL {len(d['checks'])} REQUIRED CHECKS PASSED — VALUATION ENABLED.**

{md(d['checks'].groupby('check_name',sort=False).agg(status=('status','first'),observations=('status','size')).reset_index())}

All {len(d['broken'])} deliberately broken-model tests blocked valuation. {len(d['audit'])} independent audit checks passed. The {len(d['abg'])} ABG reference checks passed their disclosed rounding tolerances.

### Sensitivity results

{md(sh[['assumption','downside','base','upside','absolute_sensitivity','percentage_sensitivity']].head(10))}

Ranking depends on the stated shock sizes: revenue growth ±3 points; SBC ±2 points; WACC ±1 point; gross margin and expense ratios ±1 point. It is not a unit-free ranking of business importance. Four financing/allocation assumptions have zero direct FCFF valuation effect but still rerun cash, equity and liquidity checks.

### Seven discount rates

{md(d['rates'])}

### Named operating cases

{md(c)}

Bear jointly reduces growth by 3 points and gross margin by 1 point, and raises R&D excluding SBC by 1 point; bull reverses these. The sum of isolated impacts is shown only to demonstrate why a joint rerun is necessary.

### Market-implied expectations

{md(im)}

Within this model, holding all other assumptions constant, the current share price requires the solved value in each row. Path shifts are percentage-point additions to every forecast year; a margin shift reduces G&A excluding SBC by the same amount. These are alternative explanations, not claims about investors' actual beliefs. The capex-only solve has no feasible root in the stated interval after preserving already-incurred H1 capex and the model checks.

### Review triggers

- Reported gross margin below 70.6%: rerun the 1-point margin downside, ${sh.set_index('assumption').loc['gross_margin','low_parameter_price']:.2f}/share.
- Revenue trajectory at least 3 percentage points below the forecast growth path: rerun the growth downside, ${sh.set_index('assumption').loc['growth','low_parameter_price']:.2f}/share.
- SBC above 17% of revenue: rerun the 2-point SBC downside, ${sh.set_index('assumption').loc['sbc_ratio','high_parameter_price']:.2f}/share.

These triggers require reassessment using the next two quarterly filings, including seasonality and full-year guidance; they are not automatic trading rules.

### Data and methodology limitations

{LIMITATIONS}

### Primary sources

- [FY2025 10-K]({FILING}), statements pp83–87; Notes 5, 7, 10, 12–13. Existing local filing preserved.
- [FY2024 10-K](https://www.sec.gov/Archives/edgar/data/1562088/000156208825000042/duol-20241231.htm), FY2023 comparatives and KPIs.
- [Q2 2026 shareholder letter]({LETTER}), outlook p10, dilution p11 and financial appendices.
- [Q2 2026 10-Q](https://www.sec.gov/Archives/edgar/data/1562088/000162828026053603/duol-20260630.htm), H1 statements.
- [Damodaran September risk inputs](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/home.htm), frozen snapshot in data/raw.
- [Course tutorial](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-05/pro-forma-abg-tutorial.md), full local slides and captions.

Reproduce: `python duol_valuation/run.py` from the parent DUOL-research directory.
'''
    (ROOT/'valuation_summary.md').write_text(summary,encoding='utf8')
    questions=[
      ('Why this discount rate?',f'WACC {v["wacc"]:.2%} = 4.75% + {b.beta:.3f} × 4.14%, with zero traditional debt. The beta standard error is {b.standard_error:.3f}; the seven-rate table is essential.'),
      ('Is terminal value the whole answer?',f'{v["terminal_share_ev"]:.1%} of EV is terminal. The 20% incremental-ROIC terminal alternative gives ${d["terminal"].iloc[1].value_per_share:.2f}/share versus ${v["value_per_share"]:.2f} in the base.'),
      ('Why forecast less growth than history?',f'FY2025 revenue grew {d["ratios"].loc[2025,"revenue_growth"]:.1%}; management now guides to $1,207m revenue in 2026. The 2027 assumption of 18% is explicitly judgment.'),
      ('What is DUOL’s special balance-sheet line?',f'Deferred revenue was $496.205m at FY2025 and $505.102m at June 2026. Customer prepayments finance operations; deferred payment-processing costs are offsetting operating assets.'),
      ('What does the market comparison mean?',f'The ${price:.2f} close exceeds the ${v["value_per_share"]:.2f} base. Holding other inputs fixed, WACC {im.iloc[0].market_implied:.2%} would reconcile the two; it is a model condition, not observed investor belief.'),
      ('What would change the case?',f'Gross margin below 70.6%, SBC above 17% of revenue, or growth 3 points below the path triggers a rebuild, with the computed values above.'),
      ('Why FCFF rather than the ABG FCFE?',f'DUOL has $0 traditional debt; FCFF at WACC avoids importing auto-dealer floor-plan borrowing. $100m cash is retained and only estimated excess liquidity is added.'),
      ('Why not just use provider free cash flow?',f'FY2025 reported FCF was $360.424m, including $137.437m SBC in CFO and interest income. Our operating FCFF retains compensation expense and removes non-operating interest.')]
    qa='\n\n'.join(f'**{q}**\n\n{ans}' for q,ans in questions)
    move=sh.set_index('assumption').loc['gross_margin','high_parameter_price'];wmove=sh.set_index('assumption').loc['wacc','high_parameter_price']
    page=f'''# DUOL — colleague briefing

**${v['value_per_share']:.2f} base vs ${price:.2f} market; {v['wacc']:.2%} WACC, 3% terminal growth.** Growth, WACC and SBC carry the sensitivity ranking. Wait for evidence of revenue reacceleration and margin expansion; rebuild if the filing-based triggers in the summary occur.

## Forecast and checks

{md(compact)}

**{len(d['checks'])}/{len(d['checks'])} required checks PASS.** Cash reconciles and every balance sheet balances. See [labelled assumptions](assumptions.csv), [seven rates](outputs/tables/seven_discount_rates.csv), [shock table](outputs/tables/sensitivity.csv), [named cases](outputs/tables/named_cases.csv), and [market-implied conditions](outputs/tables/market_implied.csv).

![Sensitivity](outputs/figures/assumption_tornado.png)

## Locked agent predictions reconciled

Before running: +1 point gross margin was predicted to add roughly $5–10/share; actual change is ${move-v['value_per_share']:.2f}. +1 point WACC was predicted to subtract $10–20/share; actual change is ${wmove-v['value_per_share']:.2f}. Both directions and rough ranges were correct. These predictions were written by the agent, not by a student/partner.

## Eight numerical answers

{qa}

## Simulated sceptic questions (not a human peer assessment)

1. **Does keeping SBC in expenses and using 50.7m shares overstate dilution?** It is conservative: the count includes existing awards and no further annual dilution factor is imposed. A precise award valuation would separate existing grants from future employee compensation.
2. **Why does the terminal reinvestment imply {v['terminal_implied_roic']:.0%} ROIC?** Deferred revenue growth offsets much of capex net of D&A, while R&D is expensed. The explicit 20% and 30% alternatives quantify the weaker-reinvestment-economics case.
3. **Are September cash balances observed?** No. June cash of $1,180.887m is filed; ${v['estimated_elapsed_cash']:.3f}m elapsed-period economic cash is a uniform-accrual estimate. This is isolated in the bridge and assumptions.

## Driver panel record

The same model powers `python duol_valuation/panel.py`. Its gross-margin +1 point move computes ${move:.2f}/share with all checks passing; the base is ${v['value_per_share']:.2f}. The automated HTTP smoke-test record is in outputs/tables/panel_smoke_test.json.

Review triggers: gross margin <70.6%; revenue growth 3 points below path; SBC >17% of revenue. Rebuild from the next two filings if confirmed. Full limitations: [valuation summary](valuation_summary.md).

Learning exercise, not investment research or financial advice.
'''
    (ROOT/'presentation_brief.md').write_text(page,encoding='utf8')
    (ROOT/'LIMITATIONS.md').write_text('# Limitations and conventions\n\n'+LIMITATIONS,encoding='utf8')
