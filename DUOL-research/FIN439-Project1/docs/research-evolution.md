# Research Evolution | DUOL

## Baseline and provenance

Edition A below reproduces the existing source without revising its content. docs/edition-a.md remains byte-identical to the original repository draft. PDF formatting and pagination are new; the underlying text is unchanged. I did not submit Edition A to Brightspace before AI-assisted work began. Preserving the draft does not establish a checkpoint receipt; checkpoint eligibility and recovery are handled with the instructor through the course process.

## Edition A - unchanged

<!-- UNCHANGED EDITION A -->

<!-- PAGEBREAK -->

## Edition B - integrated valuation model

Prepared October 17, 2026 local time; valuation remains September 21, 2026. Intended user: a buy-side committee with no existing position. Investment horizon: 3-5 years. Recommendation: **Watch / Defer** at the dated $149.42 price. The corrected five-year pro-forma DCF gives **$137.57**, with conditional low/base/high operating cases of **$114.20 / $137.57 / $165.01**.

The application links the operating forecast, valuation, sensitivity analysis and validation in one model. model.py follows Lab 10's revenue-to-statements-to-cash sequence and Lab 6's FCFF valuation method. analysis.py carries forward Lab 11's reset-and-change-one-input discipline. Lab 08 supplies the peer policy, Lab 09 the independently runnable training answer, and Lab 12 the decision narrative. A small panel, explicit validation and final documents close the project-specific gaps. The previous expanded implementation is preserved outside this submission as an archive; it is not another active engine.

| Source | Retained contribution | Final correction or addition |
| --- | --- | --- |
| Edition A and September research | Thesis, assumptions, evidence, unknowns | Preserve A; qualify tax-contaminated earnings and unresolved claims in B |
| Lab 6 | WACC, FCFF DCF, terminal share, sensitivity and reverse DCF methods | Drive DCF with the operating pro forma instead of extrapolating reported FCF; reconcile date and shares |
| Lab 08 | Peer policy, GAAP earnings gate, merger exclusion and method disagreement | Add consistent DUOL EV and equity ratios; retain absence of an eligible independent peer target |
| Lab 09 | ABG known-answer and deliberate cash failure | Retain the $291.75 training fixture as validation, not a DUOL FCFF model |
| Lab 10 | DUOL five-year drivers and cash-last accounting | Show full statements; add cash/FCFF identities, H1 actuals, dated liquidity, asset roll-forwards and terminal reinvestment |
| Lab 11 | OAT EBIT/FCFF/value and reset behavior | Fix AI growth versus margin inconsistency; preserve original prediction history; test equal-width rankings |
| Lab 12 | Presentation logic, monitoring and partner questions | Translate reasonably-valued language into a conditional committee action and an explicit final range |
| Final project requirements | Usable workbench, complete validation and deliverables | Bounded controls, reset, visible failures, executed report, cold run, memo and disclosure |

### Why the value changed

Lab 6's $251.99 result starts with reported company CFO less capital spending and uses September 10 price evidence, 48.308m weighted-average diluted shares and 8.5286% WACC. Labs 10-12 use $140.18, a September 21 price, 50.7m diluted shares and 8.2764% WACC. The final model produces $137.57 after correcting the later lab's timing, liquidity, cash-flow and terminal conventions. This is a multi-change reconciliation, not an isolated experiment attributing the entire $2.61 difference to a single correction.

The final engine uses FY2025 historical statements and filed H1 2026 balances/flows, forecasts H2 separately, and displays full-year 2026 through 2030. DCF excludes the elapsed portion of H2 at September 21 using an explicitly approximate uniform-accrual convention. The dated equity bridge adds estimated excess liquidity only once, including a $100m operating reserve deduction. Final-year working-capital investment is recomputed at mature terminal growth rather than carrying the high-growth year mechanically into perpetuity. D&A is allocated across PPE/software assets rather than charging all depreciation to PPE while software never amortizes.

The earlier expanded implementation and initial consolidation both produced $136.89. The final cash-bridge correction increases that estimate to $137.57. The bridge now uses accounting cash accumulation rather than economic FCFF, and excludes the $0.675m repurchase payable from operating working capital. It settles in financing without reducing equity twice. This correction is separately tested; it does not change the operating growth assumptions. The model uses Python's standard library, with retained source evidence and original file hashes.

### Normalization and company-specific drivers

FY2025 reported net income is $414.065m. Removing the $256.7m valuation-allowance release alone yields $157.365m. The selected analytical earnings measure is instead $137.409m: remove other nonoperating income and replace the entire reported tax line with a normal 24% tax assumption applied to EBIT plus interest income. Operating NOPAT excludes interest. SBC remains an economic operating cost, and capital spending includes both software and PPE. These definitions are reconciled in outputs/normalization.json and the contamination catalog; none is relabeled as GAAP.

The 2026 $1,207m revenue and 71.6% gross-margin anchors are guidance-based. The later 18% to 10% growth path, margin recovery, declining SBC intensity and $100m reserve are judgments. Subscription conversion/retention and bookings support revenue and deferred-revenue reasoning; AI delivery costs affect margin. Neither channel is separately identified from a causal statistical model. Each of the 24 material assumptions has a value, basis, challenge and evidence that would cause revision in the assumption ledger and challenge record.

### Lab 11 correction and prediction history

Both current Lab 11 named drivers change the same revenue-growth vector, at different widths. One prose passage incorrectly describes a gross-margin shock. Equal growth shifts necessarily give identical outputs, so the larger observed span does not establish that one business mechanism intrinsically matters more.

Git commit 3c6dab3 preserves an earlier prediction-only record with AI efficiency modeled through gross margin. Later commits e3aefff and f9d2c2e add results and change the AI channel to revenue growth. The final package retains original and current versions under evidence/ and records the mismatch in docs/locked-changed-input-record.md. The old prediction is not silently rewritten. I wrote the original prediction myself in class with AI closed; the prediction-only commit precedes the matching result record, and the original gross-margin results were reproduced from preserved code. The exact historical execution time and a contemporaneous formal action statement are not separately established.

The final OAT analysis separately tests revenue growth, gross margin and SBC, plus the other assumptions. Growth leads under the wider +/-3pp growth range; under equal +/-1pp shocks, margin slightly exceeds SBC for value, and both exceed growth. Both EBIT/FCFF and valuation changes are visible. These are conditional stress comparisons, not probabilities.

### Decision, disagreement and monitoring

At the dated market price, the base DCF does not provide a valuation cushion. Terminal value is 84.34% of EV; a 20% terminal ROIC stress reduces value to approximately $126.01. This is material economic uncertainty, even when accounting checks pass. Reverse DCF separately solves approximately 7.78% WACC, 3.53% perpetual growth, or a +2.32pp growth-path shift to match the market price. It does not reveal investors' actual beliefs.

Five named downside stresses each change one disputed judgment: no 2027 reacceleration ($127.16), growth at the FY2026 bookings pace of about 11% ($122.63), beta 1.0 ($125.56), total-return beta ($134.15) and terminal ROIC 20% ($126.01). The 2027 reacceleration to 18% is my weakest assumption because bookings guidance (+10.9% for FY2026, +8.9% for Q3) leads subscription revenue. The regression beta of 0.85 has an R-squared of only 0.045. Every stress lowers value, so none reverses Watch / Defer; together they move the case toward Do Not Initiate.

Market EV/sales is 5.99x under the diluted-equity convention; equity/reported earnings is 18.30x but equity/normalized earnings is 55.13x. Reported-tax effects and differing forecast horizons explain why these measures suggest different valuation burdens. The COUR/UDMY exclusions remain: negative annual GAAP earnings and post-merger entity mismatch prevent a defensible peer target. These incompatible methods are not averaged; own-company multiples do not provide independent peer corroboration.

Watch the next two reports for revenue/bookings, margin, SBC and investment needs. Gross margin below 70.6%, growth 3pp below the path, SBC above 17% of revenue, or FY2027 bookings growth below 13% requires a rebuild; persistent thesis failure supports Do Not Initiate. A proposed initiation rule requires both price at or below the current low-case estimate and evidence supporting the base economics, with updated dated inputs. These are judgment conditions, not guaranteed outcomes.

### Attribution and remaining personal evidence

The IBM partner challenged the growth path in Lab 10 and the AI cost/revenue channel and sensitivity ranges in Lab 11. The Apple partner challenged the AI-versus-paid-conversion interpretation in Lab 12. Their exchanges and responses are credited in docs/assumption-challenges.csv. Codex (gpt-6-astra, low reasoning) assisted consolidation, corrections, testing and drafting on October 16-18, 2026. Claude Code (Claude Opus 5.5) reviewed the package against the course requirements on October 18, 2026, adding the beta reliability statistics and named stresses. Dispositions are in the validation record.

| Item | Edition A | Edition B | Primary driver of change | Evidence/test |
| --- | --- | --- | --- | --- |
| Thesis/recommendation | Watch / defer; no price or valuation | Watch / Defer; $114.20-$165.01 range vs $149.42 | Own analysis | DCF, causal cases, named stresses |
| Data/source choice | FY2025 10-K only | 10-K, H1 2026 10-Q, Q2 letter, dated price, Damodaran rates | Course instruction / own analysis | sources.md; XBRL source tests |
| Assumption/model design | Not yet modeled | Three-statement pro-forma driving FCFF DCF | Course instruction / AI | 148 model checks; known answer |
| Risk/limitation | Valuation burden unknown | Terminal 84% of EV; imprecise beta; 2027 growth vs bookings | Own analysis / AI review | wacc.json; named_stresses.csv |

Remaining requirements are the three recordings with corrected transcripts and final access/checkpoint/receipt evidence. See Validation-and-AI-Use.pdf and submission-manifest.csv.
