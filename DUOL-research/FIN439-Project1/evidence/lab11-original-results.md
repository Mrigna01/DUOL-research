# Lab 11 — Locked Changed-Input Record

Locked before scenario execution: **2026-09-29 America/Indianapolis**

The two inputs below are independent scenario inputs. Every run resets the other input to base.

| Driver | Lower | Base | Higher | Units | Affected years | Prediction before execution |
|---|---:|---:|---:|---|---|---|
| Paid-subscriber conversion and retention adjustment | -2.0 | 0.0 | +2.0 | percentage points added to annual revenue growth | FY2026E–FY2030E | Lower conversion/retention should reduce 2030 operating profit, FCFF and value per share; higher conversion/retention should increase all three. Expected effect: material because subscription revenue is the core monetization channel. |
| AI-feature efficiency adjustment | -1.0 | 0.0 | +1.0 | percentage points added to gross margin | FY2026E–FY2030E | Lower AI efficiency should reduce 2030 operating profit, FCFF and value per share; higher efficiency should increase all three. Expected effect: meaningful but smaller than the revenue-growth driver because it changes margin rather than users. |

Evidence used to set the ranges: Duolingo's Q2 2026 letter reports paid subscribers of 12.7 million,
DAUs of 58.7 million, current-user retention of 84%, and AI-powered feature expansion with AI cost
efficiencies. The ranges are judgment shocks around the Lab 10 base case, not management guidance.

## Prediction reconciliation after execution

The predictions were directionally correct. The paid conversion/retention cases produced value per
share of $128.42 / $140.18 / $152.94 for lower/base/higher, so the changes from base were −$11.76
and +$12.75. The AI-feature cases produced $135.19 / $140.18 / $145.18, so the changes were −$4.99
and +$4.99. The subscriber driver had the larger output span over the selected ranges. The main
prediction limitation was that the initial note described the effects as material without a precise
dollar estimate; the actual runs quantify the difference and show that AI remains meaningful but
secondary to the chosen subscriber-growth range.

The result changes my research priority: I would investigate paid-subscriber conversion and
retention first because they moved value by $24.52 across the tested range, while continuing to
monitor AI feature costs and monetization because the AI range still moved value by $9.99.
