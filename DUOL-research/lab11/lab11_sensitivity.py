"""FIN43900 Lab 11: one-at-a-time DUOL sensitivity analysis.

This is a separate, standard-library-only copy of the Lab 10 company model.
It resets every independent input before each run and changes only one selected
driver. It writes a reproducible results table and restores the base case last.
"""

import csv
from copy import deepcopy
from math import isfinite
from pathlib import Path

YEARS = [2026, 2027, 2028, 2029, 2030]
OPENING = {
    "revenue": 1037.589, "cash": 1036.389, "investments": 239.176,
    "ar": 162.827, "deferred_cost": 102.663, "prepaid": 16.582,
    "ppe": 36.297, "intangibles": 28.309, "other_assets": 369.939,
    "ap": 7.998, "accrued": 45.688, "deferred_revenue": 496.205,
    "other_liabilities": 95.285, "equity": 1347.006,
}
BASE = {
    "growth": [0.1633, 0.1800, 0.1600, 0.1300, 0.1000],
    "gross_margin": [0.716, 0.720, 0.730, 0.740, 0.740],
    "rd_ex_sbc": [0.230, 0.225, 0.220, 0.215, 0.210],
    "sm_ex_sbc": [0.130, 0.125, 0.120, 0.115, 0.110],
    "ga_ex_sbc": [0.105, 0.100, 0.095, 0.090, 0.085],
    "sbc_ratio": [0.150, 0.140, 0.130, 0.120, 0.110],
    "tax_rate": [0.240] * 5, "ar_ratio": [0.157] * 5,
    "deferred_cost_ratio": [0.099] * 5, "prepaid_ratio": [0.016] * 5,
    "ap_ratio": [0.008] * 5, "accrued_ratio": [0.044] * 5,
    "deferred_revenue_ratio": [0.476] * 5, "da_ratio": [0.0139] * 5,
    "capex_ratio": [0.0264] * 5, "investment_yield": [0.046] * 5,
}
DRIVERS = {
    "paid_conversion_retention": {"low": -0.020, "base": 0.0, "high": 0.020},
    "ai_features": {"low": -0.010, "base": 0.0, "high": 0.010},
}
WACC = 0.08276376244240655
TERMINAL_GROWTH = 0.03
SHARES = 50.7
MINIMUM_CASH = 100.0


def run_case(driver, level):
    """Run one independent shock; all other inputs remain BASE."""
    inputs = deepcopy(BASE)
    shock = DRIVERS[driver][level]
    if driver == "paid_conversion_retention":
        inputs["growth"] = [x + shock for x in inputs["growth"]]
    elif driver == "ai_features":
        inputs["gross_margin"] = [x + shock for x in inputs["gross_margin"]]
    previous = dict(OPENING)
    rows = []
    for i, year in enumerate(YEARS):
        revenue = previous["revenue"] * (1 + inputs["growth"][i])
        gross_profit = revenue * inputs["gross_margin"][i]
        rd = revenue * inputs["rd_ex_sbc"][i]; sm = revenue * inputs["sm_ex_sbc"][i]
        ga = revenue * inputs["ga_ex_sbc"][i]; sbc = revenue * inputs["sbc_ratio"][i]
        da = revenue * inputs["da_ratio"][i]; capex = revenue * inputs["capex_ratio"][i]
        ebit = gross_profit - rd - sm - ga - sbc
        pretax = ebit + previous["investments"] * inputs["investment_yield"][i]
        tax = max(0, pretax) * inputs["tax_rate"][i]; ni = pretax - tax
        ar = revenue * inputs["ar_ratio"][i]; dcost = revenue * inputs["deferred_cost_ratio"][i]
        prepaid = revenue * inputs["prepaid_ratio"][i]; ap = revenue * inputs["ap_ratio"][i]
        accrued = revenue * inputs["accrued_ratio"][i]; drev = revenue * inputs["deferred_revenue_ratio"][i]
        da_assets = (ar - previous["ar"]) + (dcost - previous["deferred_cost"]) + (prepaid - previous["prepaid"])
        da_liabilities = (ap - previous["ap"]) + (accrued - previous["accrued"]) + (drev - previous["deferred_revenue"])
        ppe = previous["ppe"] + capex * 0.66 - da; intangibles = previous["intangibles"] + capex * 0.34
        nwc_change = da_assets - da_liabilities
        fcff = ebit * (1 - inputs["tax_rate"][i]) + da - capex - nwc_change
        cash = previous["cash"] + ni + da + sbc - da_assets + da_liabilities - capex
        assets = cash + previous["investments"] + ar + dcost + prepaid + ppe + intangibles + previous["other_assets"]
        liabilities = ap + accrued + drev + previous["other_liabilities"]
        equity = previous["equity"] + ni + sbc
        rows.append({"year": year, "ebit": ebit, "fcff": fcff, "cash": cash,
                     "balance_gap": assets - liabilities - equity, "cash_gap": cash - MINIMUM_CASH})
        previous.update({"revenue": revenue, "cash": cash, "ar": ar, "deferred_cost": dcost,
                         "prepaid": prepaid, "ppe": ppe, "intangibles": intangibles,
                         "ap": ap, "accrued": accrued, "deferred_revenue": drev, "equity": equity})
    checks_pass = all(abs(r["balance_gap"]) <= 0.05 and r["cash_gap"] >= -0.05 and
                      all(isfinite(v) for v in r.values() if isinstance(v, float)) for r in rows)
    if not checks_pass or WACC <= TERMINAL_GROWTH:
        return {"driver": driver, "case": level, "input_value": shock, "status": "INVALID",
                "final_ebit": rows[-1]["ebit"], "final_fcff": rows[-1]["fcff"], "value_per_share": ""}
    pv = sum(r["fcff"] / (1 + WACC) ** (i + 1) for i, r in enumerate(rows))
    tv = rows[-1]["fcff"] * (1 + TERMINAL_GROWTH) / (WACC - TERMINAL_GROWTH)
    ev = pv + tv / (1 + WACC) ** 5
    equity_value = ev + OPENING["cash"] + OPENING["investments"]
    return {"driver": driver, "case": level, "input_value": shock, "status": "PASS",
            "final_ebit": rows[-1]["ebit"], "final_fcff": rows[-1]["fcff"],
            "value_per_share": equity_value / SHARES}


def main():
    results = [run_case(driver, level) for driver in DRIVERS for level in ("low", "base", "high")]
    base = {r["driver"]: r for r in results if r["case"] == "base"}
    for r in results:
        if r["status"] == "PASS":
            b = base[r["driver"]]
            r["ebit_change"] = r["final_ebit"] - b["final_ebit"]
            r["fcff_change"] = r["final_fcff"] - b["final_fcff"]
            r["value_change"] = r["value_per_share"] - b["value_per_share"]
        else:
            r["ebit_change"] = r["fcff_change"] = r["value_change"] = ""
    for driver in DRIVERS:
        group = [r for r in results if r["driver"] == driver and r["status"] == "PASS"]
        print("\n" + driver)
        for r in group:
            print("%s: input %+.1f pp | 2030 EBIT %.1f | 2030 FCFF %.1f | value/share $%.2f | value change $%+.2f" %
                  (r["case"], 100 * r["input_value"], r["final_ebit"], r["final_fcff"], r["value_per_share"], r["value_change"]))
        print("spans: EBIT %.1f; FCFF %.1f; value/share $%.2f" %
              (max(r["final_ebit"] for r in group) - min(r["final_ebit"] for r in group),
               max(r["final_fcff"] for r in group) - min(r["final_fcff"] for r in group),
               max(r["value_per_share"] for r in group) - min(r["value_per_share"] for r in group)))
    out = Path(__file__).with_name("sensitivity_results.csv")
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["driver", "case", "input_value", "status", "final_ebit", "final_fcff", "value_per_share", "ebit_change", "fcff_change", "value_change"])
        writer.writeheader(); writer.writerows(results)
    restored = run_case("paid_conversion_retention", "base")
    assert restored["status"] == "PASS" and abs(restored["value_per_share"] - base["paid_conversion_retention"]["value_per_share"]) < 1e-9
    print("\nBASE RESTORED: PASS")
    print("Results written to %s" % out)


if __name__ == "__main__":
    main()
