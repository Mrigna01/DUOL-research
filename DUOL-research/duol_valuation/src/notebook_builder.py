import nbformat as nbf
from .data_loader import ROOT

def build_notebook():
    cells=[]
    def md(s):cells.append(nbf.v4.new_markdown_cell(s))
    def code(s):cells.append(nbf.v4.new_code_cell(s))
    md('# 1. Project Objective\n\n# Duolingo, Inc. — NASDAQ: DUOL\n**FIN 43900 Weeks 5–6 | Valuation date: September 21, 2026 close**\n\nBuild and audit a linked pro-forma valuation, then test what drives its result. Financial amounts and share counts are in **millions**, except per-share prices. This is an educational analysis, not investment advice.\n\nThe visible check blocks in Sections 9, 12 and 24 gate valuation. The original workspace files were preserved. All calculations use frozen public-source snapshots so the notebook runs offline.')
    code('''from pathlib import Path
import sys, json, copy
import numpy as np
import pandas as pd
from IPython.display import display, Markdown, Image
project_root = Path.cwd() if (Path.cwd() / "src").exists() else Path.cwd() / "duol_valuation"
sys.path.insert(0, str(project_root))
from src.data_loader import ROOT, load_data, price_data
from src.historical_analysis import analyze
from src.beta import estimate
from src.assumptions import build_assumptions, unpack
from src.forecast import project
from src.checks import run_model_checks, require_pass, display_checks
from src.valuation import dcf
from src.sensitivity import sensitivities, rerun
from src.implied_expectations import solve_implied
from src.validation import broken_tests, independent_audit
from src.abg_validation import validate_abg
from src.pipeline import IS, BS, CF, terminal_variants
from src.charts import make_charts
pd.options.display.float_format = '{:,.4f}'.format
pd.options.display.max_rows = 160
''')
    md('## 2. Course Methodology\n\nThe [ABG tutorial](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-05/pro-forma-abg-tutorial.md) was reviewed before model construction: both slide decks, full spoken notes and VTT captions. YouTube links opened but audiovisual playback was unavailable.\n\nProcess: source three years → label inputs → build one year in statement order → calculate cash last → enforce checks → deliberately break the model → expand to five years → value → measure beta → seven rates → shocks and joint cases → price-implied assumptions → present.\n\nABG uses FCFE because floor-plan borrowing is integral to a dealer. DUOL uses FCFF/WACC, with no traditional debt and leases treated as operating throughout. Its funding advantage is prepaid subscription revenue, not inventory loans. The reference calculations below use Lab09?s exact 17.951349m share count and match the $291.75 base to cents, with scenario tolerances matching the displayed decimal precision.')
    code('abg = validate_abg()\ndisplay(abg)')
    md('## 3. Duolingo Overview\n\nDuolingo monetizes a large free learning audience through paid subscriptions, advertising, English tests and in-app purchases. Subscription revenue represented 84.2% of FY2025 revenue. Engagement and conversion matter, but paid subscribers are a period-end count while revenue is earned throughout the year.\n\nThe model therefore anchors total revenue to management guidance, uses subscriber/MAU/DAU history as a diagnostic, and avoids fabricating churn, ARPU or a causal user-to-revenue forecast. Deferred revenue provides funding; deferred platform fees partially offset it. R&D, marketing, SBC and AI delivery costs shape margins.')
    md('## 4. Data Sources\n\nHistorical statements: FY2025 10-K and FY2024 comparative balances, cross-checked against SEC companyfacts. H1 actuals: Q2 2026 10-Q. Guidance: Q2 shareholder letter pp10–11. Prices: Yahoo, with Nasdaq confirming the selected close. Treasury/ERP: Damodaran September 1 snapshot. The latest completed closing price is used instead of the partial September 22 trading session.\n\nExact accession and tag provenance is in `data/processed/source_ledger.csv`; original file inventory and course snapshots are in `data/raw`. Failed Treasury/FRED requests are disclosed; no September 21 yield was invented.')
    code('''history, interim = load_data()
prices, market_price = price_data()
beta_statistics, returns = estimate(prices)
assumptions = build_assumptions(history, beta_statistics.iloc[0].beta)
inputs = unpack(assumptions)
display(pd.DataFrame([{'valuation_date':'2026-09-21','DUOL_close':market_price,'financial_anchor':'2026-06-30','rate_input_vintage':'2026-09-01'}]))
display(pd.read_csv(ROOT / 'data/processed/source_ledger.csv').head(12))''')
    md('## 5. Historical Financial Statements\n\nFiscal years ended December 31, 2023–2025. The cash-flow capex definition includes **both PPE and capitalized software/intangibles**; it excludes acquisitions. The 2025 tax benefit is exceptional and is not a sustainable operating margin.')
    code('''display(history[IS].T)
display(history[BS].T)
display(history[['cfo','cfi','cff','capex_ppe','capex_software','sbc','da','investment_purchases','investment_maturities','options_proceeds','withholding','share_repurchases','cf_deferred_revenue_increase','cf_ar_increase','cf_deferred_cost_increase','cf_ap_increase','cf_accrued_increase','basic_shares','diluted_shares']].T)''')
    md('## 6. Historical Analysis\n\nAll ratios are computed from the tables above. Growth for the first historical year is intentionally unavailable because this presentation uses three annual years. MAU/DAU are Q4 averages and paid subscribers are year-end counts. Revenue divided by year-end subscribers is a **monetization proxy, not ARPU**. Negative working capital reflects customer prepayments, not a missing asset.\n\nQ2 2026 provides a recent diagnostic: 58.7m DAU (+23%), 140.6m MAU (+10%), 12.7m paid subscribers (+17%), $289.1m bookings (+8%) and $258.035m subscription revenue (+22%). These differing growth rates caution against extrapolating user growth directly into revenue.')
    code('historical_ratios, operating_kpis = analyze(history)\ndisplay(historical_ratios.T)\ndisplay(operating_kpis.T)')
    md('## 7. Forecast Assumptions\n\n**HISTORY** is a filed figure or calculated historical ratio; **GUIDANCE** is a company outlook; **JUDGMENT** is an analyst choice. The 2026 revenue outlook is $1,207m, gross margin 71.6%, SBC about 15% of revenue and tax rate 23–25% (24% selected). Later years are not company guidance.\n\nR&D/marketing/G&A drivers exclude SBC but include embedded D&A. SBC is added once to these expenses, split 70/10/20 as a presentation convention. Cash is not forecast as a revenue ratio. Guidance range bounds are stored when disclosed; the current point revenue outlook supersedes mechanically choosing a midpoint of the earlier 15–18% range. The low/high shock columns refer to parameter direction, not necessarily valuation direction.')
    code('display(assumptions)\ndisplay(pd.read_csv(ROOT / "model_conventions.csv"))')
    md('## 8. Year 1 Pro-Forma\n\nThe first annual column combines reported H1 2026 and forecast H2. Forecast H2 revenue/expenses are annual targets less reported H1. The **June 30 balance sheet** opens the H2 roll-forward. Working capital is built from operating ratios, assets roll by capex less D&A, equity rolls by income plus SBC plus financing flows, and **cash is computed last**. Investment balances are held constant; cash movements are not hidden in investments.')
    code('year1 = project(history, interim, inputs, n=1)\ndisplay(year1[IS].T)\ndisplay(year1[BS].T)\ndisplay(year1[CF].T)')
    md('## 9. Model Check Block\n\nThese checks recompute totals from components and tie cash, fixed assets and equity to prior balances. A $100m floor is an analyst liquidity policy. No DUOL revolver is invented; an unfunded cash shortfall blocks valuation.')
    code('year1_checks = run_model_checks(year1, interim, inputs, history)\ndisplay_checks(year1_checks)\ndisplay(year1_checks)')
    md('## 10. Broken-Model Test\n\nDeep copies are corrupted: cash linkage, assets, cash floor, NaNs, cash flow, depreciation and UFCF. Invalid terminal growth and zero shares are also tested. Each test calls the **actual valuation function** and must receive an identifying exception. The original Year 1 remains intact.')
    code('broken = broken_tests(year1, interim, inputs, history)\ndisplay(broken[["test","status","valuation_blocked"]])\nfor row in broken.itertuples(): print(row.test + " -> " + row.error[:250])\nrequire_pass(run_model_checks(year1, interim, inputs, history))\nprint("Original Year 1 restored and valid; expansion now permitted.")')
    md('## 11. Five-Year Pro-Forma Statements\n\nOnly after Year 1 passes, the same function creates 2026–2030. Later years start from the previous forecast balance sheet. Annual income and cash-flow statement columns are full-year amounts; `period_` lines in 2026 identify the forecast H2 component. No prior historical cash-flow line is silently carried as a future forecast.')
    code('model = project(history, interim, inputs, n=5)\ndisplay(model[IS].T)\ndisplay(model[BS].T)\ndisplay(model[CF].T)')
    md('## 12. Final Forecast Checks')
    code('checks = run_model_checks(model, interim, inputs, history)\ndisplay_checks(checks)\ndisplay(checks[checks.check_name.isin(["Balance sheet","Cash reconciliation","Minimum cash"])])')
    md('## 13. Free Cash Flow\n\n**UFCF = EBIT − max(EBIT,0) × normalized tax + D&A − capex − Δ operating NWC.** NWC is receivables + deferred fees + prepaid expenses − payables − accrued expenses − deferred revenue. Cash/investments, deferred taxes and long-term lease balances are excluded.\n\nD&A is embedded in operating expenses and added back once. SBC remains an economic expense; only accounting CFO adds it back and credits equity. This avoids treating recurring equity compensation as free financing. No extra annual dilution multiplier is imposed. Operating lease costs remain in EBIT, so lease liabilities are not deducted a second time.\n\nFor 2026, `ufcf` is H2 only; `annual_ufcf` adds analytical normalized-tax H1 UFCF for a full-year operating comparison. H1 already-earned cash flow is excluded from the forward DCF.')
    code('display(model[["period_ebit","nopat","period_da","period_capex","delta_nwc","ufcf","annual_ufcf"]].T)')
    md('## 14. Beta Estimation\n\nExact course convention: **SPY, monthly unadjusted closing prices, simple returns, covariance/variance slope with an intercept**. August 2021–August 2026 supplies 61 prices and 60 returns. DUOL began trading in July 2021, so this full window is available. September is incomplete and excluded.\n\nAn adjusted-price regression is a robustness check because SPY pays dividends. Reported beta is raw; Blume = 0.67 × raw + 0.33 is shown separately. Standard error, confidence interval and low R² disclose sampling uncertainty.')
    code('display(beta_statistics.T)\ndisplay(prices.head())\ndisplay(prices.tail())')
    md('## 15. Cost of Equity\n\nCAPM uses the September 1, 2026 published Treasury convention of 4.75% and implied ERP of 4.14% from the frozen Damodaran snapshot. These are dated relevant inputs, not an assertion that a current-day Treasury quote was retrieved. The adjusted-default-spread variant is not mixed into these inputs.')
    code('cost_of_equity = 0.0475 + beta_statistics.iloc[0].beta * 0.0414\nprint(f"Cost of equity = 4.75% + {beta_statistics.iloc[0].beta:.6f} × 4.14% = {cost_of_equity:.4%}")')
    md('## 16. WACC\n\n**WACC = E/(D+E) × Ke + D/(D+E) × Kd × (1−tax).** Traditional interest-bearing debt is zero; equity weight is 100%. Lease obligations are operating throughout this model. Kd is not applicable and contributes zero. Market equity uses the reported June basic share count as a dated proxy; DCF per-share division uses the company’s 50.7m estimated diluted count.')
    code('display(pd.DataFrame([{"Market price":market_price,"Basic share proxy m":46.7,"Market equity $m":market_price*46.7,"Debt $m":0,"Equity weight":1.,"Debt weight":0.,"Ke":cost_of_equity,"Kd contribution":0.,"Tax":.24,"WACC":inputs["wacc"][0]}]))')
    md('## 17. Base-Case DCF\n\nOnly cash flows after September 21 are discounted: 101/184 of H2 2026 and all of 2027–2030, using actual year-end dates/365. The equity bridge adds June cash and investments plus estimated elapsed-period economic cash, subtracts the $100m operating reserve and known additional buybacks. Estimated elapsed cash charges SBC as a reserve; it is not an observed balance. The future forecast cash balance is **not** added again.')
    code('valuation, discounting = dcf(model, interim, inputs, history)\ndisplay(discounting)\ndisplay(pd.Series(valuation, name="Base valuation").to_frame())')
    md('## 18. Terminal Value Analysis\n\nThe terminal year is rebuilt at 3% growth, with last explicit margins, tax rate and capex/D&A ratios held constant. Deferred revenue and other NWC grow at **3%**, avoiding perpetuating a 10% explicit-year working-capital inflow. Terminal FCF is divided by WACC minus g. Nonpositive FCF or an invalid spread blocks valuation.\n\nThe very high implied incremental ROIC warrants scrutiny. The alternatives below replace net reinvestment with `NOPAT × g / ROIC`, at 20% and 30%, without adding it on top of base capex. A mechanical last-FCF extrapolation is shown as a diagnostic, not the selected answer.')
    code('terminal_cases = terminal_variants(valuation, model, inputs)\ndisplay(terminal_cases)')
    md('## 19. Seven Discount-Rate Scenarios\n\nThe same statements are valued at base WACC ±1, ±2 and ±3 percentage points. Every rate exceeds terminal growth. Scenario functions still rerun the checks. Each operating shock rebuilds all statements, not just the final value.')
    code('shocks, rates, named_cases, rate_growth_grid = sensitivities(history, interim, inputs, assumptions)\ndisplay(rates)')
    md('## 20. Assumption Shock Analysis\n\nAll 24 numeric driver paths are shocked. Rankings reflect the explicit shock sizes and measured swing, not a subjective ordering. Financing distributions and accounting allocations can have zero direct FCFF value impact while changing cash/equity. The combined bear case is compared with the incorrect sum of isolated impacts.\n\nAgent predictions were recorded before the first rerun: gross margin +1 point should add $5–10/share; WACC +1 point should subtract $10–20/share. These are not claimed student/partner predictions.')
    code('display(shocks[["assumption","parameter_low","parameter_high","downside","base","upside","absolute_sensitivity","percentage_sensitivity"]])\ndisplay(named_cases)\nprint("Actual +1pp margin impact:", shocks.set_index("assumption").loc["gross_margin","high_parameter_price"] - valuation["value_per_share"])\nprint("Actual +1pp WACC impact:", shocks.set_index("assumption").loc["wacc","high_parameter_price"] - valuation["value_per_share"])')
    md('## 21. Market-Implied Expectations\n\nBrent root finding searches feasible checked models and changes one variable at a time. Path shifts apply to all five forecast years. Operating margin is changed through G&A, not an independent contradictory EBIT plug. A failed or economically impossible root remains visible.\n\n**Within this model, holding other assumptions constant, the market price would require approximately the value in each solved row.** These are alternative conditional explanations; they do not identify investors’ literal beliefs.')
    code('implied = solve_implied(history, interim, inputs, market_price)\ndisplay(implied)')
    md('## 22. Visualizations\n\nThe professor’s exact three analytical purposes are reproduced: tornado, one-axis market/case comparison, and rate/growth heat map. Operating performance, seven-rate curve, beta scatter and cash-flow chart supplement them. Every image is generated from the model outputs above.')
    code('figures = make_charts(history,model,valuation,shocks,rates,named_cases,rate_growth_grid,returns,beta_statistics.iloc[0],market_price,ROOT/"outputs/figures")\nfor name in figures:\n    display(Image(filename=str(ROOT/"outputs/figures"/(name+".png"))))')
    md('## 23. Interpretation\n\nThe base requires revenue reacceleration after the 2026 reset and operating leverage toward a 22.5% EBIT margin in 2030. It remains below the selected market close. This is a conditional model result, not evidence of mispricing.\n\nReview triggers: gross margin below 70.6%, revenue growth 3 points below the path, or SBC above 17% of revenue. Review the next two filings and update the combined operating case if these persist.\n\nThe companion `presentation_brief.md` contains the numerical eight-question defence and clearly labelled simulated sceptic questions. The local driver panel uses this same model. Human oral peer review cannot be performed by the agent.')
    code('display(Markdown((ROOT/"LIMITATIONS.md").read_text(encoding="utf8")))')
    md('## 24. Final Model Checks\n\nIndependent arithmetic/source checks, actual broken-model valuation refusals and final valid-state checks are displayed together. No warning is suppressed to make the model appear valid.')
    code('''audit = independent_audit(history,interim,model,inputs,valuation,discounting,shocks,implied,prices)
full_broken_tests = broken_tests(model,interim,inputs,history)
display(audit)
display(full_broken_tests[['test','status','valuation_blocked']])
display_checks(run_model_checks(model,interim,inputs,history))
assert all(cell.status == 'PASS' for cell in audit.itertuples())
assert all(full_broken_tests.valuation_blocked)
print('Final valid model retained; all source/arithmetic audit and corruption tests passed.')''')
    md('## 25. Conclusion\n\nUse the model as a transparent set of testable conditions: guidance anchors the first year, judgment carries the later margin/growth recovery, and the largest sensitivities identify where further research matters. The terminal reinvestment alternative and wide beta uncertainty are material limitations.\n\nAll computational work is reproducible with `python duol_valuation/run.py` from DUOL-research. Course submission is via GitHub links to the notebook, markdown and Python/supporting files. The entire local folder is the submission bundle; human partner/oral participation is not represented as completed.')
    code('print(f"DUOL base value: ${valuation[\"value_per_share\"]:.2f}; market close: ${market_price:.2f}; WACC: {valuation[\"wacc\"]:.4%}; all required model checks PASS.")')
    nb=nbf.v4.new_notebook(cells=cells,metadata={'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python','version':'3.13'}})
    nbf.write(nb,ROOT/'duol_valuation.ipynb')
    return nb
