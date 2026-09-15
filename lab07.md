# FIN 439 Lab 07 — Comparable-Company Valuation

## 1. Purpose and P/E explanation

Price-to-earnings (P/E) equals price per share divided by earnings per share (EPS). It shows how much investors pay for each dollar of annual earnings and puts differently sized companies on a common per-share basis. This market-based comparison complements a DCF, which values forecast cash flows. Differences between the two methods can highlight assumptions worth reviewing.

A lower P/E is not automatically a bargain. Negative earnings make a positive P/E comparison not meaningful, while unusual profits can make P/E look artificially low. Differences in growth, risk, debt, or business mix can also justify different multiples.

## 2. Case inputs

| Company | Role | Price | Diluted EPS |
|---|---|---:|---:|
| Asbury Automotive (ABG) | Target | $243.03 | $21.50 |
| AutoNation (AN) | Peer | $169.84 | $16.92 |
| Group 1 Automotive (GPI) | Peer | $421.48 | $36.81 |

Prices are December 31, 2024 closing prices. EPS is FY2024 total GAAP diluted EPS. This is a retrospective exercise because the annual earnings were released afterward; all information was not available on the pricing date.

## 3. Peer decisions

Both candidates are included as qualified peers. AutoNation operates franchised vehicle stores and earns meaningful gross profit from parts/service, closely matching Asbury's core business. It requires qualification because AutoNation Finance is a captive finance company. Group 1 also fits the vehicle retail and parts/service model, but its U.S./U.K. exposure and 2024 acquisition of 54 Inchcape dealerships create geographic and integration differences.

An industry label alone is insufficient because companies in the same industry may have different economics, risks, and growth profiles. Asbury is excluded from its own peer set because including the target would make the benchmark partly circular.

## 4. Calculation and validation

The calculator was run with:

```powershell
python .\lab07_comps.py
```

| Check | Calculator output | Expected | Result |
|---|---:|---:|---|
| AutoNation P/E | 10.037825× | 10.037825× | Match |
| Group 1 P/E | 11.450149× | 11.450149× | Match |
| Median peer P/E | 10.743987× | 10.743987× | Match |
| Asbury implied range | $215.81–$246.18 | $215.81–$246.18 | Match |
| Median-implied price | $231.00 | $231.00 | Match |

One peer-implied price is:

\[(169.84 / 16.92) \times 21.50 \approx \$215.81\]

The calculator retains full decimal precision for calculations, then displays multiples to six decimals and prices to cents.

## 5. Removing Group 1

Group 1 has the higher P/E, so removing it leaves AutoNation's lower multiple and lowers the estimate to $215.81. The change from the full-peer estimate is −$15.18, calculated from unrounded values. With only one peer, this is a reference estimate rather than a range. The expected direction is downward, but peer inclusion should depend on business evidence—not on which valuation result is preferred.

## 6. Reflection and limitations

The range does not prove that Asbury is fairly valued. It relies on only two peers and is sensitive to their differences in financing, geography, acquisitions, growth, and risk. P/E already applies an equity multiple to earnings available to shareholders, so cash is not added and debt is not subtracted afterward. That enterprise-to-equity bridge belongs with enterprise-value multiples, not P/E.

## 7. Sources

- [Lab 07 assignment](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-04/lab-07-comparable-policy.md)
- [Worked comparable-company case](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-04/teach-comps-worked-example.md)
- [Asbury FY2024 results (SEC)](https://www.sec.gov/Archives/edgar/data/1144980/000114498025000008/a2024q4ex991.htm)
- [AutoNation FY2024 results (SEC)](https://www.sec.gov/Archives/edgar/data/350698/000035069825000026/anearningsrelease123124ex9.htm)
- [Group 1 FY2024 results](https://www.group1corp.com/2025-01-29-Group-1-Automotive-Reports-2024-Fourth-Quarter-Financial-Results-and-Record-Full-Year-Revenues-of-19-9-billion)
