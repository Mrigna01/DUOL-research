# Validation and AI Use | DUOL

Prepared October 18, 2026. Valuation date: September 21, 2026. This record documents my final DUOL valuation model. Execution logs from my earlier expanded package are not presented as tests of this implementation.

## System and reproduction

model.py is my sole DUOL accounting/valuation engine. analysis.py runs the required cases, sensitivities, named stresses, reverse DCF and multiples and writes visible-output.html. panel.py exposes selected bounded assumptions; validate.py independently reconstructs identities and tests failures. Lab 09's ABG model is retained only as a known-answer fixture. Model execution uses the Python standard library; reportlab and pypdf are needed only to rebuild the three PDFs.

The fresh-run evidence is evidence/cold-run.log and evidence/cold-environment.txt. They identify the interpreter, clean-copy conditions, commands, exit codes and any first failure. The authoritative computational run summary is outputs/run-status.json. Data inputs are retained locally; no online lookup is required to reproduce the valuation.

## Executed tests and limits

| Test | Evidence | Outcome and scope |
| --- | --- | --- |
| 148 accounting/input checks | outputs/model_checks.csv | Historical balances and cash flows; projected cash/equity/assets; FCFF and CFO identities; finite values, liquidity and rate boundaries |
| 70 independent validation tests | outputs/validation_checks.csv | Source comparisons, normalization, grid monotonicity, bridge, deliberate corruptions, directional changes and reverse solves |
| Known-answer fixture | evidence/abg_known_answer.py; validation_checks.csv | Lab 09 independently reproduces $291.75166628 versus the course rounded $291.75 |
| Original Lab 10 regression defect | evidence/lab-to-project-map.md; validation_checks.csv | Original engine accepted a $100m first-year FCFF corruption; consolidated engine refuses it |
| Bounded panel and failure recovery | evidence/panel-checks.json | 54 actual HTTP checks: changed input, reset, invalid requests, boundaries and real DCF failure |
| Browser interaction | evidence/workbench-browser-checks.json | Actual DOM input, reset, calculation failure, stale-output clearing and simulated network recovery |
| Fresh isolated environment | evidence/cold-run.log | Clean end-to-end reproduction; prior outputs omitted from the run copy |
| Beta reliability | outputs/wacc.json | Beta 0.852, R-squared 0.045, standard error 0.515, approximate 95% normal interval −0.16 to 1.86; total-return beta 0.891 |
| Named downside stresses | outputs/named_stresses.csv | No reacceleration $127.16; bookings-paced growth $122.63; beta 1.0 $125.56; total-return beta $134.15; terminal ROIC 20% $126.01 |

These tests establish consistency under documented conventions, not economic truth. An invariant can still be correct around an unrealistic forecast. Terminal value at 84.34% of EV and the imprecise beta are economic sensitivities I report rather than suppress.

## Independently evidenced AI output: QUALIFY

An early AI-assisted version of my DCF used reported company free cash flow as its FCFF starting point. I qualify that output. The FY2025 filing reports CFO of $387.823m, PPE purchases of $18.096m and software/intangible purchases of $9.303m, giving reported FCF of $360.424m. CFO includes a $137.437m SBC add-back and interest income. Company FCF is therefore not interchangeable with an operating FCFF valuation that retains compensation as a shareholder cost and values excess liquidity separately.

My final engine uses operating NOPAT plus D&A less capex and operating working-capital investment. It retains SBC in EBIT/FCFF while the accounting cash-flow statement adds the noncash charge back. The noncash tax-allowance release is not subtracted a second time from CFO. Independent evidence: the filing's cash-flow statement (10-K PDF p.122), the retained XBRL comparison in validate.py, the reported-FCF identity test and the normalized-earnings bridge. Disposition: QUALIFY the early reported-FCF interpretation; MODIFY the final valuation implementation.

## Cash-bridge correction and regression tests

The audit found that economic FCFF had been used as a proxy for accumulated accounting cash. The corrected bridge works from CFO, CFI and financing cash, retaining the SBC add-back and deducting withholding. H1 repurchases reconcile $70.278m recognized to $69.603m paid plus $0.675m payable. The payable is excluded from operating NWC and its settlement does not reduce equity twice. The approximately $1.622m new post-June trades and $0.675m settlement are assumed paid by September 21. The rounded purchase disclosure and uniform H2 timing remain estimates.

Validation independently rolls December cash back to September and reconstructs repurchase recognition, cash settlement and equity. Regression tests reject the old economic-cash proxy, corrupted settlement/withholding and future-cash double counting. The correction changes the prior $136.89 base to $137.57; Watch / Defer is unchanged. Gross margin and SBC still tie for 2030 EBIT and FCFF at equal shocks, but their valuation impacts differ slightly because of accounting cash accumulation.

## Normalization, sources and dated inputs

The normalized base-year record is docs/contamination-catalog.csv and outputs/normalization.json. Reported net income is $414.065m. Subtracting the $256.7m tax release alone gives $157.365m. My selected normalized equity earnings instead remove other nonoperating income and replace the entire reported tax line using 24% on EBIT plus interest, yielding $137.409m. Normalized operating NOPAT is $103.033m. These are analytical definitions, not management-reported adjusted figures.

The source map identifies FY2025 and H1 2026 statement evidence, the September 21 market price, share basis and September 1 Treasury/ERP inputs. Beta is recomputed from 60 monthly DUOL/SPY returns; WACC is risk-free rate plus beta times ERP with zero financial-debt weight. The Damodaran page retrieved October 16 corroborates the earlier rate pair through its previous-month section; it is not a contemporaneous September download. Data are not refreshed to October while retaining a September valuation label.

All material assumptions have values, basis, challenge and revision evidence in data/assumptions.csv and docs/assumption-challenges.csv, including credited partner challenges from Labs 10-12. Their bounds are judgment stress ranges, not probability estimates. The 24% normal-tax proxy, $100m reserve, 2027 growth recovery and terminal reinvestment are my most consequential judgments. The panel exposes growth, margin, SBC, WACC and perpetual growth while keeping accounting and source definitions locked.

## Highest-risk failures and recovery

My original Lab 10 balance-sheet check did not prevent an independently corrupted FCFF number from reaching valuation. The final FCFF-identity check recomputes operating NOPAT, depreciation, capex and working-capital change before valuation and rejects that exact $100m corruption. Corruptions to cash, receivables, CFO and PPE are also rejected.

A separate bridge reconstruction tests the dangerous addition of forecast terminal cash after cash flows have already been discounted. Adding that future cash to equity violates the independently constructed bridge even if the balance sheet still balances. The expected bridge uses filed H1 liquidity, 83/184 of recurring H2 accounting cash generation, separately dated repurchase payments and the operating reserve, with no duplicated future cash.

In the live panel, the failure button sets terminal growth equal to WACC in a copy of the actual engine. Valuation is refused, visible results are cleared and Reset recomputes base. A simulated network error also clears stale results. The tests exercise actual error paths rather than turning a status label red without calculation.

## Direction tests

Automated direction tests record their expectations in validate.py before execution: higher growth/margin increases value; higher SBC/WACC decreases value; higher coherent terminal growth increases value. Actual deltas are saved in validation_checks.csv, and base restoration is tested. These AI-written tests are separate from my human AI-off prediction below.

## Complete Locked Changed-Input Record

This documents my Lab 11 experiment from preserved prediction and result records; it is not a newly invented test.

### Authorship and precommit evidence

I wrote the original prediction myself in class with AI closed. The prediction-only snapshot is Git commit 3c6dab3, September 29, 2026 at 17:28:03 -0400, preserved as evidence/lab11-record-original.md, which labels itself locked before scenario execution. Commit e3aefff, 17:38:25 -0400, preserves the matching gross-margin results in evidence/lab11-original-results.md. The timestamps establish prediction-before-result-record chronology; the precise historical execution time was not separately logged.

### Selected input and prediction

- Model: original Lab 10/11 DUOL engine, FY2026-2030, valuation date September 21, 2026; USD millions except per-share values; 50.7m diluted shares.
- Driver: AI-feature efficiency, implemented as a gross-margin adjustment. All other assumptions reset to base.
- Old adjustment: 0.00 percentage points. New adjustment: +1.00 percentage point in each forecast year. Lower diagnostic case: -1.00 percentage point.
- Base gross-margin path: 71.6%, 72.0%, 73.0%, 74.0%, 74.0%. Higher path: 72.6%, 73.0%, 74.0%, 75.0%, 75.0%.
- My prediction: lower AI efficiency should reduce 2030 operating profit, FCFF and value per share; higher efficiency should increase all three, with an effect smaller than the wider revenue-growth shock.
- Basis for the range: guidance and AI-cost/feature discussion in the Q2 shareholder letter, with a judgment stress of one percentage point. It is not a probability or a separately measured AI contribution.

### Recorded and reproduced results

| Case | Margin adjustment (pp) | 2030 EBIT ($m) | 2030 FCFF ($m) | Value/share |
| --- | --- | --- | --- | --- |
| Lower | -1.00 | 441.536562 | 357.691290 | $135.190427 |
| Base | 0.00 | 462.073147 | 373.299094 | $140.183217 |
| Higher | +1.00 | 482.609731 | 388.906898 | $145.176007 |

Higher minus base is +$4.992790 per share; lower minus base is -$4.992790. The higher case increases EBIT by $20.536584m and FCFF by $15.607804m. The predicted directions hold. The margin-case value span of $9.985581 is less than the $24.515695 span of the original ±2pp growth test; this ranking is conditional on unequal shock widths. On October 18, Codex reran the preserved e3aefff script; all six original cases reproduced and restoration returned $140.18321713393624 (evidence/lab11-original-reconciliation.json).

### Decision effect and diagnosis

At the time, the result led me to prioritize paid conversion/retention research while continuing to monitor AI costs and monetization; I did not record a formal committee action then. All three margin cases remain below the dated $149.42 market price, so an isolated margin improvement does not create an initiation cushion, and my action stays Watch / Defer. The wider growth high case exceeds market, which is why growth evidence remained my first research priority.

There is no direction failure to diagnose. The documentation failure was a version mismatch: later commit f9d2c2e changed the AI input to revenue growth, producing different results. That later output must not be paired with the original margin prediction. Both versions remain preserved; the final model tests growth and margin separately.

## Peer and method validation

The IBM partner challenged growth, AI channels and sensitivity ranges in Labs 10-11. The Apple partner challenged AI versus paid conversion in Lab 12. docs/assumption-challenges.csv links their contributions to the original records; historical peer checks do not validate the revised model.

Primary-source tests retain the original peer policy: COUR's negative GAAP EPS and UDMY's merger prevent an unreconciled peer target. DUOL EV and equity multiples use consistent dates and diluted-share conventions. The memo explains disagreement without averaging incompatible methods.

## AI-use register

| Tool/model and version | Date | Material task | Disposition and independent evidence | Effect on decision |
| --- | --- | --- | --- | --- |
| Codex, gpt-6-astra (low reasoning) | October 16-18, 2026 | Lab-to-requirement mapping; consolidation of labs into one engine | MODIFY: original labs preserved; $140.18 Lab 10/11 and $291.75 Lab 09 rerun; Git prediction history retained | None; consolidation only |
| Codex, gpt-6-astra (low reasoning) | October 16-18, 2026 | Accounting, timing and bridge corrections | MODIFY: primary-source inputs, reconstructed identities, deliberately broken FCFF/cash/bridge tests | Value moved $140.18 → $137.57; action unchanged |
| Codex, gpt-6-astra (low reasoning) | October 16-18, 2026 | Sensitivity design and peer definitions | QUALIFY: equal-input test shows two growth labels are one mechanism; merger/GAAP evidence rejects unsupported peers | Ranking reported as range-dependent |
| Codex, gpt-6-astra (low reasoning) | October 16-18, 2026 | Code, panel, visible report and document drafts | ACCEPT after review: runnable source, tests, fresh run and browser checks | None |
| Codex, gpt-6-astra | October 18, 2026 | Cash accumulation and repurchase-settlement audit; validation and document refresh | MODIFY: statement-based bridge, independent year-end rollback and deliberate-corruption tests; clean rerun | Prior $136.89 becomes $137.57; Watch / Defer unchanged |
| Claude Code, Claude Opus 5.5 | October 18, 2026 | Requirements review; beta reliability statistics; named downside stresses; first-person document revision | ACCEPT the beta statistics (recomputed from monthly_prices.csv) and stresses (rerun through model.py); base assumptions left unchanged | Added model-risk section; strengthens Watch / Defer, no action change |

Final investment judgment and acceptance of material AI contributions are my responsibility.

## Limitations, monitoring and kill rules

Edition A was not submitted to Brightspace before AI-assisted work began; checkpoint recovery is handled with the instructor through the course process. Estimated September liquidity is not an observed filed balance. Peer exclusions leave no independent peer target. The $206m deferred tax asset is not valued. Gross margin below 70.6%, growth 3pp below the path, SBC above 17% of revenue or FY2027 bookings growth below 13% triggers a rebuild; failed source, articulation or bridge checks suspend the numerical recommendation.
