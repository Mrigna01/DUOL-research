# Locked Changed-Input Record - Lab 11 reconciliation

This documents my Lab 11 experiment from preserved prediction and result records; it is not a newly invented AI-off test.

## Authorship and precommit evidence

I wrote the original prediction myself in class with AI closed.

The prediction-only snapshot is Git commit 3c6dab3, September 29, 2026 at 17:28:03 -0400, preserved as evidence/lab11-record-original.md. That record labels itself locked before scenario execution. Commit e3aefff, 17:38:25 -0400, preserves the matching gross-margin results in evidence/lab11-original-results.md. The timestamps establish prediction-before-result-record chronology. The precise historical execution time was not separately logged.

## Selected input and prediction

- Model: original Lab 10/11 DUOL engine, FY2026-2030, valuation date September 21, 2026; USD millions except per-share values; 50.7m diluted shares.
- Driver: AI-feature efficiency, implemented as a gross-margin adjustment. All other assumptions reset to base.
- Old adjustment: 0.00 percentage points. New adjustment: +1.00 percentage point in each forecast year. Lower diagnostic case: -1.00 percentage point.
- Base gross-margin path: 71.6%, 72.0%, 73.0%, 74.0%, 74.0%. Higher path: 72.6%, 73.0%, 74.0%, 75.0%, 75.0%.
- My prediction: lower AI efficiency should reduce 2030 operating profit, FCFF and value per share; higher efficiency should increase all three, with an effect smaller than the wider revenue-growth shock.
- Basis for the range: guidance and AI-cost/feature discussion in the Q2 shareholder letter, with a judgment stress of one percentage point. It is not a probability or a separately measured AI contribution.

## Recorded and reproduced results

| Case | Margin adjustment (pp) | 2030 EBIT ($m) | 2030 FCFF ($m) | Value/share |
| --- | --- | --- | --- | --- |
| Lower | -1.00 | 441.536562 | 357.691290 | $135.190427 |
| Base | 0.00 | 462.073147 | 373.299094 | $140.183217 |
| Higher | +1.00 | 482.609731 | 388.906898 | $145.176007 |

Higher minus base is +$4.992790 per share; lower minus base is -$4.992790. The higher case increases EBIT by $20.536584m and FCFF by $15.607804m. The predicted directions hold. The margin-case value span is $9.985581, less than the $24.515695 span of the original ±2pp growth test. This ranking is conditional on unequal shock widths.

On October 18, Codex (gpt-6-astra) reran the preserved e3aefff script. All six original growth/margin cases reproduced and restoration returned $140.18321713393624. The rerun output and UTC timestamp are in evidence/lab11-original-reconciliation.json. This is a reproduction, not the historical classroom execution and not a replacement prediction.

## Decision effect and diagnosis

At the time, the result led me to prioritize paid conversion/retention research while continuing to monitor AI costs and monetization; I did not record a formal committee action then.

All three margin cases remain below the dated $149.42 market price, so an isolated margin improvement does not create an initiation cushion, and my action stays Watch / Defer. The wider growth high case exceeds market, which is why growth evidence remained my first research priority.

There is no direction failure to diagnose in the matching margin experiment. The documentation failure was a version mismatch: later commit f9d2c2e changed the AI input to revenue growth, producing different results. That later output must not be paired with the original margin prediction. Both versions remain preserved; the final model tests growth and margin separately.

## Limits

Git snapshots and reproduced outputs support the recorded sequence and arithmetic. The exact historical run timestamp and a contemporaneous formal investment-action statement are not independently established. No timestamp, judgment or receipt has been fabricated. Edition A checkpoint evidence is a separate matter handled with the instructor.
