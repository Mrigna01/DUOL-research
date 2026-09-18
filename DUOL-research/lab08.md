# Lab 08 — Deal Evidence and Valuation Triangulation

**FIN 43900 | Duolingo, Inc. (NASDAQ: DUOL) | Comparison date: September 10, 2026**
Prepared September 17, 2026. USD per common share unless otherwise stated.

**Decision: watch-defer.** The saved Week 3 DCF is $251.99 per diluted share, with a $166.53–$268.11 sensitivity range. This investigation produces **no defensible peer P/E estimate**: Coursera has negative annual reported diluted EPS, and Udemy had ceased to be a standalone public equity before the comparison date. Neither belongs in the calculator. This is a supported comparability limitation, not a zero-dollar valuation or evidence that the DCF is correct.

## 1. Target, date, and existing work

Duolingo sells digital learning through a freemium model, monetized through subscriptions, advertising, testing and in-app purchases. Consumer engagement and conversion economics guide peer selection. [S1, Item 1, business model]

The saved Week 3 work is [`Lab 6.md`](./Lab%206.md), prepared September 10, and [`dcf.py`](./dcf.py). Earlier September 1 and September 3 research memos were inspected but do not override that later DCF date. The DCF filename linked in `sources.md` does not exist locally; actual saved results are in `Lab 6.md`. No replacement DCF was constructed.

The September 10 regular-session closes were **DUOL $145.16** and **COUR $5.23**, verified in Nasdaq historical data. DUOL's close equals the saved DCF quote, whose original timestamp was after the close. Historical-price evidence establishes a common closing-price basis without changing the date or price. UDMY has no comparable standalone share on that date. [S5–S7]

Research question: can an independently listed company with similar learning-platform economics supply a positive, reported annual earnings multiple valid for this date? Research covered business fit, earnings sign and definition, publication dates, corporate actions and same-date prices.

## 2. P/E applicability

| Field | Verified Duolingo evidence |
|---|---|
| Fiscal period | Year ended December 31, 2025 |
| Annual reported diluted EPS | **$8.57**, positive; basic EPS of $9.05 is not used |
| Document | FY2025 Form 10-K [S1] |
| Public availability | SEC filing date February 27, 2026; accepted February 26 at 18:35:35 [S2]. Both precede September 10 |
| Locator | Item 8 statements of operations, printed p. 84 / saved PDF p. 120; Note 13 EPS table, printed p. 110 / saved PDF p. 156 |
| Currency / shares | USD; Class A and B common shares have identical economic rights; quote is Class A |
| Qualification | Net income of $414.065m includes a $256.7m one-time income-tax benefit from releasing a deferred-tax valuation allowance; Item 7, printed p. 60 / saved PDF p. 85 |

Duolingo passes the positive-earnings gate. The tax benefit limits how well reported EPS represents recurring earnings. The calculator retains the required **reported annual** basis, with no adjusted EPS, quarterly annualization or forecast substituted. [S1]

## 3. Initial peer-selection policy — before names

This policy was saved before candidate searches. The [policy and pre-run prediction checkpoint](./lab08_evidence/policy-and-prerun-prediction.md) preserves that sequence.

Prefer listed operating companies that sell scalable digital learning products to individual learners, with recurring subscriptions or repeat purchases, low physical capital requirements, and broad geographic reach. Evaluate customer acquisition, free-to-paid conversion, retention, content economics, growth, profitability and scale. Enterprise or institutional distribution may qualify a learning-platform candidate but must be disclosed; dependence on physical delivery, financing, or unrelated segments can warrant exclusion. A shared education label alone is insufficient. Require primary-source business evidence and latest annual reported diluted EPS publicly available by the comparison date. Use positive GAAP diluted EPS in the same currency and per-share basis as the closing price. Exclude loss-making candidates from P/E even if their business fit is useful. Qualify material growth, margin, revenue-mix or earnings-quality differences; do not choose peers based on the implied valuation. Investigate at most two names. Missing prices stay UNRESOLVED; no fabricated multiple or substituted date.

**Rejection criteria:** nonpositive reported earnings; no independently traded share at the comparison date; incompatible price/EPS share bases; economically dominant noncomparable operations; or inadequate evidence. The policy was not relaxed after seeing the results.

**Process disclosure:** the agent drafted the policy before searching and proposed Coursera and Udemy as research leads based on digital learning and subscription economics. Udemy's historical ticker failed the subsequent listing check. This is not represented as a student-authored pre-AI policy, two independent AI consultations, student personal source inspection or a completed live partner discussion. Those personal course requirements remain checkout actions.

## 4. Candidate investigation and evidence table

Exactly two candidates were investigated. Both exclusions remain visible.

| Field | Coursera | Udemy |
|---|---|---|
| Company / ticker | Coursera, Inc. / NYSE: COUR | Udemy, Inc. / former NASDAQ: UDMY |
| Business model | Online courses and credentials; consumer and institutional customers; university and industry content partners [S3–S4] | Instructor-created courses, individual purchases/subscriptions and Udemy Business subscriptions [S8] |
| Similarity | Global digital learning and repeat learner monetization | Scalable learning platform with subscriptions and consumer access |
| Important difference | Career credentials, degrees and institutional distribution; merger changes the business represented by the stock | Enterprise was 66% of FY2025 revenue; instructor marketplace differs from Duolingo's consumer product; no standalone equity at valuation date [S8, S5] |
| Scale / growth | FY2025 revenue $757.5m; release reports 9% growth [S3] | FY2025 revenue $789.8m, essentially flat; 72% subscription revenue [S8] |
| Stock price | **$5.23**, regular-session close [S7] | **N/A — no standalone share**, following conversion into COUR shares [S5] |
| Price date | **September 10, 2026** | September 10 requested; structurally inapplicable, not a missing price to estimate |
| Annual reported diluted EPS | **−$0.31**, GAAP basic and diluted loss per share [S3] | **+$0.03**, GAAP diluted EPS [S8] |
| Fiscal period | Year ended December 31, 2025 | Year ended December 31, 2025 |
| Publication / filing date | Annual-results release **February 5, 2026** [S3] | Verified annual filing **February 19, 2026** [S9]; this establishes availability before the cutoff |
| Primary financial source | Coursera FY2025 earnings release [S3] | Udemy FY2025 10-K [S8–S9] |
| Earnings locator | “Condensed Consolidated Statements of Operations,” **Year Ended December 31, 2025** column, “Net loss per share—basic and diluted” row | Note 13, “Net income (loss) per share,” FY2025 **Diluted** row, printed p. 118 |
| Business locator | 10-K Item 1, “Overview,” p. 4; release “About Coursera” | 10-K Item 1, pp. 1–3; Item 7 “Enterprise segment” |
| Decision | **EXCLUDE from P/E** | **EXCLUDE from P/E** |
| Reason | Negative annual GAAP EPS; pre-merger earnings also differ in entity scope from September equity | Shares converted into COUR shares on May 11; positive historical EPS does not cure the share/object mismatch |

Both models justified investigation, but not automatic admission. Institutional selling and content-partner economics can change the multiple a learning business deserves. Digital distribution suggests some shared scalability; it does not establish equal capital intensity, margins or growth. Their operating information remains useful even though neither supplies an admissible multiple.

## 5. Peer decisions and corporate actions

Coursera separately reports **$0.39 non-GAAP diluted EPS**. That cannot replace its negative reported denominator without changing the required earnings definition. [S3, GAAP-to-non-GAAP net income reconciliation]

On May 11, each eligible UDMY share converted into the right to receive **0.800 COUR shares**, and Udemy became a wholly owned subsidiary. A stale UDMY quote, or 0.800 times COUR's September price, would not price Udemy's former standalone earnings. The companies also cannot be counted as two independent public peers after the transaction. [S5, Item 2.01; S10]

The **admitted set is empty**. No third candidate was added to seek a preferred result or bypass the two-candidate scope. This does not establish that no suitable peer exists anywhere; it states what these investigations support under the unchanged policy.

## 6. P/E calculator and output

The original [`lab07_comps.py`](../lab07_comps.py) was understood and rerun successfully. Its Asbury case still returns $215.81–$246.18 with median-implied $231.00; those figures appear only in the [labeled original-case regression baseline](./lab08_evidence/lab07-baseline-output.txt). Previous Lab 07 files remain unchanged.

[`lab08_comps.py`](./lab08_comps.py) retains the working Decimal calculations, screening, median/minimum/maximum methodology and removal logic. Inputs are now DUOL, price $145.16, annual diluted EPS $8.57 and an empty peer list. Only the no-estimate messages were clarified. Excluded companies never enter valuation inputs.

For an admitted peer: `peer P/E = peer price / annual diluted EPS`; `DUOL implied price = peer P/E × 8.57`. Multiple peers supply minimum/maximum and median-implied values; one supplies a reference rather than a range. P/E directly values equity, so no cash/debt bridge is added afterward.

Run from this folder:

```powershell
python .\lab08_comps.py
python .\lab08_validate.py
```

Actual [calculator output](./lab08_evidence/calculator-output.txt):

```text
Target: Duolingo (DUOL)
Target market price: $145.16
Price date: September 10, 2026 (regular-session close; Nasdaq)
EPS basis: FY2025 total GAAP diluted EPS, year ended December 31, 2025

Peer P/E multiples

Valuation
  No usable peers; no estimate (not zero dollars).

Peer-removal sensitivity
  No admitted peers to remove; removal experiment is not applicable.
```

No minimum, maximum, mean, median, reference estimate or target implied price exists for the empty set. The obstacle is peer admissibility, **not nonpositive DUOL earnings**. The official lab allows a checked, sourced comparability limitation. [S11, “Validate” and merit criteria]

## 7. Manual validation

There is **no admitted peer to validate by hand**. The following calculations diagnose the obstacle; they are not presented as a successful peer valuation.

| Check | Independent arithmetic / expected result | Validation |
|---|---|---|
| Target EPS | $414.065m / 48.308m = $8.571354641, rounding to **$8.57** | Matches annual diluted EPS [S1] |
| Target's own reported P/E | $145.16 / $8.57 = **16.938156359×** | Context only; DUOL is not its own peer |
| COUR signed quotient | $5.23 / (−$0.31) = **−16.870967742** | `peer_multiple` returns `None`; a negative quotient is not a usable positive-earnings multiple |
| UDMY | +$0.03 EPS but no September 10 standalone price | Missing-price guard returns `None`; corporate-action exclusion precedes calculator inputs |
| Empty set | No estimate, not $0 | Matches output |
| Saved DCF | Independently compounded/discounted FCFF = **$251.992040357** | Matches `dcf.py` $251.9920 and saved $251.99 |
| Saved sensitivity | All nine cells reproduced; minimum **$166.53**, maximum **$268.11** | Matches `Lab 6.md` |

[`lab08_validate.py`](./lab08_validate.py) checks Nasdaq date rows, target inputs, invalid denominators and empty-set behavior, then independently recomputes the DCF using Decimal arithmetic. [Validation output](./lab08_evidence/validation-output.txt) records passing checks. Diagnostic calls do not admit excluded candidates.

## 8. Peer-removal / sensitivity test

**Prediction saved before the first Lab 08 run:** both candidates fail admission. With zero admitted peers, the calculator should return no estimate. There is no admitted peer to remove; rerunning the empty set should still return no estimate. No excluded company will be inserted to manufacture a sensitivity result.

**Observed:** initial and repeat runs return no estimate; the validator checks identical output. No actual peer was removed, so there is **no numerical removal experiment or dollar change** to report. Calling the change $0 would incorrectly imply that a value existed.

Information is lost at admission: the investigation supplies operating comparisons but no transferable market multiple. Dependence on peer eligibility is clear, although numerical sensitivity cannot be measured. In a genuine single-peer case, removal would eliminate the sole reference; that is a methodological explanation, not an experiment claimed here.

Resolution requires an independently listed operating peer satisfying the policy, with positive annual reported diluted EPS public by September 10 and a compatible closing price. Any expanded investigation must preserve these exclusions and explain policy revisions before recalculation. Later positive earnings cannot retroactively fix this dated comparison.

## 9. Week 3 DCF versus peer P/E

| Method | DUOL result and date | Main assumption / limitation |
|---|---|---|
| Week 3 DCF | **$251.99** base; **$166.53–$268.11** saved sensitivity; September 10, 2026 | FCFF $360.424m; growth 15%, 18%, 16%, 13%, 10%; WACC 8.5286%; terminal growth 3%; cash/investments $1,275.565m; debt $0; diluted shares 48.308m. Grid uses WACC 9%–11% and terminal growth 2%–4% |
| Peer P/E | **No estimate / range withheld**; September 10, 2026 | COUR's negative annual reported EPS and changed entity scope; UDMY no longer independently listed |

DCF values forecast cash flows and assumes growth and operating leverage. **80.07% of enterprise value** comes from terminal value. The grid is an assumption sensitivity, not a confidence interval or guaranteed downside floor. The base WACC is below the grid's lowest WACC; both are preserved exactly as saved.

The $145.16 close is below all saved grid values, but that does not establish mispricing. Historical weighted-average shares, future dilution, treatment of all cash/investments as non-operating, and lower realized FCFF could change the result.

There is no numerical disagreement to explain: only DCF supplies a value. Peer research adds evidence about comparability limitations, not a second estimate. A future usable P/E result could differ because market multiples embed different growth, margins, risks and sentiment, while DCF fixes forecasts and terminal assumptions. DUOL's one-time earnings benefit would amplify an implied price at any fixed positive multiple. An unavailable P/E estimate neither confirms nor refutes DCF, and the methods are not averaged.

The earlier saved call was conditional initiation below approximately $166.53 if operating assumptions remained intact. That historical rule remains documented; this lab's final call withholds initiation pending stronger evidence.

## 10. Skeptical AI review

**Provisional call:** watch-defer; retain DCF as conditional evidence, withhold a peer range.

The weakest supported assumption is durable forecast FCFF with the selected discount rate, because terminal value dominates enterprise value. The company/object check finds UDMY absorbed into COUR and pre-merger annual EPS paired with post-merger equity. The date check confirms common September 10 closes for surviving tickers. The earnings-definition check rejects replacing COUR's reported loss with adjusted earnings. No arithmetic discrepancy was found. Independent historical provenance for the DCF's market-derived WACC inputs remains incomplete.

**One skeptical question:** Does the saved DCF justify initiating at $145.16 if its cash-flow growth and terminal assumptions have not been independently supported by recurring operating performance, while reported EPS includes a large tax benefit and the investigated peers cannot corroborate a valuation?

Evidence identified before resolving the criticism that could change the call: sustained cash-flow conversion and operating margins, historical discount-rate support, dilution analysis, and an admissible comparable with matching price and earnings bases.

## 11. Evaluation of the criticism — ACCEPT, with limits

**ACCEPT** the criticism as a reason to withhold a confident initiation call. The independently recomputed terminal contribution, disclosed tax benefit and two failed admissions support it. Forecasts remain assumptions, not proven outcomes. [S1; saved Week 3 work; validation output]

It does **not** prove that DUOL is overvalued or that the tax benefit inflated operating cash flow dollar-for-dollar. Accounting net income and FCFF are different quantities. No unsupported tax adjustment was subtracted from the saved DCF. The evidence supports a conditional decision, not a fabricated replacement valuation.

This is an agent self-review checked against actual sources, not a second AI provider's review or a human partner's question.

## 12. Date and calculation integrity audit

| Input / issue | Cutoff check and treatment |
|---|---|
| DUOL annual EPS / historical DCF financial inputs | FY2025 filing public February 2026, before September 10; latest completed fiscal year [S1–S2] |
| COUR annual EPS | FY2025 release February 5, 2026; no quarterly or adjusted figure substituted [S3] |
| UDMY annual EPS | FY2025 filing February 19, 2026 [S8–S9] |
| Merger | Completed and publicly announced May 11, 2026; incorporated into September eligibility [S5, S10] |
| Prices | Exact **09/10/2026** Nasdaq rows, USD close; later rows/quotes are not valuation inputs [S6–S7] |
| Forecasts | Saved analyst assumptions, not relabeled company guidance |
| DCF WACC provenance | **PARTLY UNRESOLVED:** Damodaran's dated September 1 update confirms the saved 4.14% ERP. StockAnalysis currently shows beta 0.89 (5Y), but a September 10 snapshot is unverified. Investing.com's September 10 daily historical yield is **4.944%**, not the saved **4.844%** live quote. The exact timestamped quote cannot be established from that daily row; it is not silently replaced. Saved arithmetic remains correct: 4.844% + 0.89 × 4.14% = 8.5286% [S13] |
| Intraday timing | Date-level comparison with regular-session closes. The saved DCF risk-free quote was later that day; this is not a strict 4 p.m. executable-information backtest |
| Prior narrative | The cited Q2 2026 10-Q was reopened [S12], but no quarterly EPS replaces annual EPS. This lab does not certify every earlier forecast rationale or unsourced memo claim |
| Share bases | DUOL price/EPS use compatible common-share economics; UDMY/Coursera conversion prevents interchanging their shares |
| Calculations | Nasdaq dates/prices, EPS rounding, invalid denominators, empty-set result, DCF base and all nine grid cells checked; no unexplained numeric discrepancy |

No comparison-date change was needed. No known post-cutoff financial information enters calculations. Unverified historical WACC provenance remains a limitation rather than being replaced with current market inputs.

## 13. Final conclusion

**Watch-defer.** Coursera and Udemy merit investigation for digital-learning economics but fail this dated P/E admission policy. Coursera's annual GAAP loss defeats a positive-earnings multiple; Udemy's merger defeats standalone share-price comparability. No peer-derived estimate can be defended from these two candidates.

The saved DCF remains **$251.99**, with **$166.53–$268.11** as its conditional sensitivity range. This is the only numerical valuation range retained; comparable P/E does not corroborate it. Forecast growth, WACC, terminal growth, available cash and dilution govern the result. The accepted criticism supports waiting for evidence rather than mechanically carrying forward the earlier initiation threshold.

Sustained results supporting the cash-flow path, documented historical discount-rate inputs, and an admissible peer would strengthen the case. Operating deterioration would weaken it. Later evidence may support a new valuation date but cannot be silently imported into September 10.

## 14. Checkout and authorship

Analytical files are complete as a **supported limitation submission**. Admitted-peer hand calculation and removal are inapplicable for the documented empty set and are not represented as completed numerical experiments. The official lab permits a sourced comparability limitation; no alternative model is required. [S11]

Before submitting, review the sources and own or revise the policy, exclusions and conclusion; explain the P/E method to a partner; and answer that partner's actual skeptical question. The official assignment also requests independent candidate suggestions from two AI partners. Only this Codex session was used. If required at checkout, send the unchanged policy and date to the second partner and reconcile its response without erasing these exclusions. The pre-AI policy exercise cannot honestly be claimed retroactively.

This folder has **no Git metadata**. Nothing has been committed, pushed or submitted to Brightspace. Upload/commit the files listed in the [submission manifest](./lab08_evidence/README.md) to the course GitHub repository, verify the links, then submit them in Brightspace → Quizzes → Lab 08 when instructed.

AI disclosure: Codex inspected local work and external sources, drafted this analysis, adapted the calculator and validated calculations. Student personal verification, independent partner work and final ownership are not claimed by the agent.

## Sources

Opened/inspected September 17, 2026 unless existing local coursework. Publication dates are document dates, not search-engine crawl dates. Filing and saved-PDF pages differ.

- **S1 — Duolingo / SEC:** [FY2025 10-K](https://www.sec.gov/Archives/edgar/data/1562088/000162828026012494/duol-20251231.htm), year ended December 31, 2025; filed February 27, 2026. Item 1 business; Item 7 p. 60 tax benefit; Item 8 p. 84 / Note 13 p. 110 EPS. [Existing PDF](./DUOL-10-K.pdf); the existing filing and canonical SEC URL provide the evidence without duplicate downloads.
- **S2 — SEC:** [DUOL filing detail](https://www.sec.gov/Archives/edgar/data/1562088/000162828026012494/0001628280-26-012494-index.htm), “Filing Date,” “Accepted,” “Period of Report.” February 27 filing / February 26 acceptance.
- **S3 — Coursera IR:** [Fourth Quarter and Full Year 2025 Financial Results](https://investor.coursera.com/news/news-details/2026/Coursera-Reports-Fourth-Quarter-and-Full-Year-2025-Financial-Results/default.aspx), February 5, 2026. FY2025 statements of operations: diluted loss **$0.31**; “About Coursera”; separate non-GAAP reconciliation. HTML section/table locators, no invented page number. Opened with web reader; direct download returned 403.
- **S4 — Coursera / SEC:** [FY2025 10-K](https://www.sec.gov/Archives/edgar/data/1651562/000165156226000015/cour-20251231.htm), fiscal year ended December 31, 2025, Item 1 “Overview,” p. 4. Business corroboration; S3 establishes annual financial publication date.
- **S5 — Coursera / SEC:** [May 11, 2026 merger 8-K](https://www.sec.gov/Archives/edgar/data/1651562/000114036126020399/ef20072971_8k.htm), Item 2.01, completed acquisition and **0.800** exchange ratio. Same-day publication corroborated by S10.
- **S6 — Nasdaq:** [DUOL historical page](https://www.nasdaq.com/market-activity/stocks/duol/historical), [API](https://api.nasdaq.com/api/quote/DUOL/historical?assetclass=stocks&fromdate=2026-09-01&todate=2026-09-10&limit=20). `data.tradesTable.rows`, **09/10/2026**, `close` **$145.16**. [Saved response](./lab08_evidence/nasdaq-duol-final.json).
- **S7 — Nasdaq:** [COUR historical page](https://www.nasdaq.com/market-activity/stocks/cour/historical), [API](https://api.nasdaq.com/api/quote/COUR/historical?assetclass=stocks&fromdate=2026-09-01&todate=2026-09-10&limit=20). Same date row, close **$5.23**. [Saved response](./lab08_evidence/nasdaq-cour-final.json).
- **S8 — Udemy / SEC:** [FY2025 10-K](https://www.sec.gov/Archives/edgar/data/1607939/000160793926000034/udmy-20251231.htm), filed February 19, 2026. Item 1 pp. 1–3; Item 7 segment revenue; Note 13 p. 118 annual diluted EPS **$0.03**. The canonical SEC filing linked above supplies the source evidence.
- **S9 — SEC:** [UDMY filing detail](https://www.sec.gov/Archives/edgar/data/1607939/000160793926000034/0001607939-26-000034-index.htm), filing/acceptance February 19, 2026; report period December 31, 2025.
- **S10 — Coursera IR:** [Coursera Completes Combination with Udemy](https://investor.coursera.com/news/news-details/2026/Coursera-Completes-Combination-with-Udemy-to-Build-the-Worlds-Most-Comprehensive-Skills-Platform/default.aspx), May 11, 2026; headline/date and opening paragraph.
- **S11 — Official course:** [Session 08 slides](https://cinderzhang.github.io/FIN43900-Fall2026/lessons/week-04/slides-session-08.html) and [Lab 08 assignment](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-04/lab-08-deal-triangulation.md). Both read in full. Official pages above are the canonical sources; local research snapshots are not duplicated in this submission.
- **S12 — Duolingo / SEC:** [Q2 2026 10-Q](https://www.sec.gov/Archives/edgar/data/1562088/000162828026053603/duol-20260630.htm), quarter ended June 30, 2026. Reopened to trace earlier research, not used as the annual EPS denominator.
- **S13 — WACC provenance follow-up:** [Aswath Damodaran / NYU](https://pages.stern.nyu.edu/adamodar/New_Home_Page/home.htm), “Implied ERP on September 1, 2026,” trailing-12-month adjusted-payout estimate **4.14%**; [StockAnalysis DUOL statistics](https://stockanalysis.com/stocks/duol/statistics/), “Stock Price Statistics,” current “Beta (5Y)” **0.89**, not an archived September 10 observation; [Investing.com Treasury history](https://www.investing.com/rates-bonds/u.s.-10-year-bond-yield-historical-data), September 10, 2026 row, daily yield **4.944%**. The last two are reopened original secondary providers, not substitutes for primary annual financial evidence. No saved DCF input was changed.
- **Saved valuation:** [`Lab 6.md`](./Lab%206.md), September 10, 2026, final inputs, valuation floor/conditional call, sensitivity grid and full code output; [`dcf.py`](./dcf.py); [rerun output](./lab08_evidence/week03-dcf-rerun.txt).
- **Price corroboration:** ChartExchange [DUOL](https://chartexchange.com/symbol/nasdaq-duol/historical/) and [COUR](https://chartexchange.com/symbol/nyse-cour/historical/), September 10 close rows $145.1600 and $5.2300. Nasdaq supplies final inputs.
