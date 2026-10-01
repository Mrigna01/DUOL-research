# Lab 12 — Duolingo Pro-Forma Sensitivity: Present and Review

**Company:** Duolingo, Inc. (NASDAQ: DUOL)  
**Valuation date:** September 21, 2026  
**Currency:** USD  
**Model basis:** FCFF discounted at WACC  

## The question

How did I get from choosing Duolingo to my valuation conclusion, which assumptions drive it, and
what evidence could change my mind?

## 1. Target selection

I selected Duolingo because it is a publicly traded subscription-learning company with strong user
growth, recurring subscription revenue, high gross margins, and enough SEC disclosure to build a
company-specific forecast. It also requires a different model from the ABG training case because
Duolingo has no inventory or floor-plan financing.

My initial view was that Duolingo's value would depend mainly on whether it could keep engaged free
learners active, convert more of them into paying subscribers, and maintain operating leverage as
the platform grows.

## 2. Company and evidence

Duolingo earns revenue from subscriptions, advertising, the Duolingo English Test, and in-app
purchases. The most important operating links are engagement, paid conversion, retention, bookings,
and deferred revenue.

The FY2025 Form 10-K and Q2 2026 shareholder letter provide the key evidence:

- Q2 2026 DAUs were **58.7 million**, up **23%** year over year.
- Q2 2026 MAUs were **140.6 million**, up **10%**.
- Paid subscribers were **12.7 million**, up **17%**.
- Current-user retention was **84%**.
- Q2 2026 revenue was **$298.5 million**, up **18%**.
- Subscription bookings were **$250.3 million**, up **10%**.
- Q2 2026 gross margin was **72.6%**.
- FY2026 revenue guidance was **$1.207 billion**, or **16.3%** growth.
- FY2026 gross-margin guidance was approximately **71.6%**.

The 2025 Form 10-K provides the FY2023–FY2025 financial history used for the forecast. The
company's operating metrics are internally measured, so they are useful for identifying trends but
are not independently audited. Reported 2025 net income also includes a large deferred-tax benefit,
so I did not extrapolate that reported margin as if it were a normal recurring result.

## 3. Pro-forma model

I used historical statements for revenue, margins, D&A, capex, working capital, deferred revenue,
SBC, and share counts. I used management guidance for the 2026 revenue, gross-margin, SBC and tax
assumptions. I used judgment for the 2027–2030 growth and margin path.

The company-specific assumptions are:

- Paid-subscriber conversion and retention support the revenue-growth path.
- Deferred revenue reflects subscription payments received before revenue recognition.
- AI features can improve conversion and monetization, but may also create development and delivery costs.
- R&D remains important because Duolingo's product and learning outcomes drive engagement.
- Sales and marketing and G&A gradually scale more efficiently than revenue.
- SBC remains an economic expense in FCFF.
- Duolingo has no floor-plan facility or traditional debt in this model.

The model forecasts FY2026E–FY2030E. Revenue is forecast first, followed by gross profit, operating
expenses, EBIT, taxes, working capital, capex, and FCFF. Cash is calculated last from the cash
bridge. The balance sheet balances in every forecast year, cash remains above the minimum, and the
deliberately broken cash test blocks valuation.

## 4. Valuation

The model uses FCFF:

> FCFF = after-tax EBIT + D&A − capital expenditures − increase in net working capital

The five FCFF amounts are discounted at WACC and a terminal value is calculated using perpetual
growth. The main valuation inputs and output are:

| Item | Result |
|---|---:|
| WACC | 8.28% |
| Terminal growth | 3.00% |
| Diluted shares | 50.7 million |
| Current market price used | $149.42 |
| Base-case value per share | **$140.18** |

The market price is above the base-case value, but the difference is modest. The market is therefore
assuming somewhat stronger future operating performance than my central forecast.

I did not force a peer P/E valuation. Coursera had negative annual GAAP diluted EPS, and Udemy was
no longer a standalone public equity at the comparison date. That makes a sourced peer multiple
unreliable for this analysis, so the peer work is treated as a comparability limitation rather than
an invented valuation input.

## 5. Sensitivity and drivers

### Paid-subscriber conversion and retention

I changed annual revenue growth by −2.0, 0.0, and +2.0 percentage points in every forecast year.
The causal chain is:

> conversion and retention → paid subscribers → revenue → EBIT → FCFF → value per share

| Case | 2030 EBIT | 2030 FCFF | Value/share |
|---|---:|---:|---:|
| Lower | $423.1m | $333.7m | $128.42 |
| Base | $462.1m | $373.3m | $140.18 |
| Higher | $503.8m | $416.3m | $152.94 |

### AI features

I modeled AI feature adoption as a paid-conversion and revenue-growth adjustment of −1.0, 0.0,
and +1.0 percentage points in every forecast year. The causal chain is:

> AI feature adoption → paid conversion → revenue → EBIT → FCFF → value per share

| Case | 2030 EBIT | 2030 FCFF | Value/share |
|---|---:|---:|---:|
| Lower | $442.3m | $353.1m | $134.18 |
| Base | $462.1m | $373.3m | $140.18 |
| Higher | $482.6m | $394.4m | $146.43 |

Over these selected ranges, paid conversion and retention had the larger value span: **$24.52 per
share**, compared with **$12.25 per share** for AI features. This ranking is conditional on the
ranges; it does not prove that paid conversion is inherently more important under every possible
range. Sensitivity analysis shows conditional outcomes, not probabilities.

## 6. Interpretation

My conclusion is that Duolingo appears **reasonably valued overall**, with a modest premium in the
market relative to my base case. The model value is $140.18 per share and the market price is
$149.42, but the market price remains inside the tested sensitivity range of $128.42–$152.94.

The market price could be supported if Duolingo continues growing DAUs, converting free learners
into paid subscribers, retaining those subscribers, and turning AI features into useful paid
products without materially increasing costs. The conclusion would weaken if paid-subscriber growth
slowed, retention declined, bookings disappointed, or AI features increased costs without improving
conversion or monetization.

My next research priority is paid-subscriber conversion and retention because it had the largest
modeled effect over the selected ranges. I would next investigate bookings, retention, gross-margin
performance, and evidence that AI features are producing measurable monetization benefits.

## 7. Partner review record

### Questions I received about Duolingo

**Selection and evidence:** Why did you choose Duolingo, and which source supports the most important
operating claim?

**Answer:** I chose Duolingo because its subscription model, engagement metrics, and public filings
make the forecast testable. The Q2 2026 shareholder letter supports the key operating claim with
58.7 million DAUs, 12.7 million paid subscribers, 84% current-user retention, and 16.3% FY2026
revenue-growth guidance.

**Model and valuation:** How does paid conversion reach the share price?

**Answer:** Higher paid conversion increases paid subscribers and revenue. Revenue raises gross
profit and EBIT, EBIT raises after-tax FCFF, and higher FCFF raises both the explicit-period value
and terminal value. The resulting enterprise value is adjusted for cash, investments and shares to
arrive at value per share.

**Sensitivity and interpretation:** Do you think AI could become Duolingo's primary growth and
value driver in the future, or will paid-subscriber conversion and retention remain more important?

**Answer:** AI could become a primary driver if its features materially increase paid conversion,
retention, or revenue per subscriber. In the current model, however, paid conversion and retention
remain more important because they have the larger tested range and the larger value span. The
conclusion is conditional: future evidence showing strong AI adoption and monetization could change
the ranking.

### Evidence and calculation checked

I showed the AI higher case of **$146.43 per share** beside the base case of **$140.18**. The
difference is **+$6.25**, which the reviewer recomputed. The reviewer also checked that paid
conversion and retention remained at base and traced AI feature adoption through paid conversion,
revenue, EBIT, FCFF, and value. Both cases passed the accounting checks.

### Review of my partner's Apple analysis

I asked: **How strong is customer loyalty toward Apple, and what evidence shows that customers will
continue buying Apple products and services rather than switching to competitors?**

The partner's conclusion was that Apple appears **reasonably valued**, because its customer loyalty
and installed base support repeat product purchases and recurring Services revenue, while hardware
replacement cycles and competition still limit how aggressively future growth should be assumed.
That conclusion is conditional rather than a claim that Apple can grow indefinitely.

### Keep, revise, investigate

I will keep the conclusion that Duolingo is reasonably valued within the modeled range. I will keep
paid conversion and retention as the first research priority because they produced the largest value
span. I would revise the model if new filings showed that AI features were changing paid conversion
or gross margin materially differently from the current judgment range. I would investigate bookings,
retention, AI monetization, and gross-margin performance before changing the valuation conclusion.
