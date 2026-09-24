"""FIN43900 Lab 10: self-contained Duolingo pro-forma model.

Standard-library only.  This follows the Lab 09 engine: forecast the operating
statement, forecast non-cash balance-sheet lines, calculate FCFF and cash last,
enforce checks, then calculate value per share.
"""

from math import isfinite

YEARS = [2026, 2027, 2028, 2029, 2030]

# FY2025 historical opening balance sheet, USD millions, from DUOL's 2025 Form 10-K.
OPENING = {
    "revenue": 1037.589, "cash": 1036.389, "investments": 239.176,
    "ar": 162.827, "deferred_cost": 102.663, "prepaid": 16.582,
    "ppe": 36.297, "intangibles": 28.309, "other_assets": 369.939,
    "ap": 7.998, "accrued": 45.688, "deferred_revenue": 496.205,
    "other_liabilities": 95.285, "equity": 1347.006,
}

# Every forecast input is labelled as required by Lab 10.
ASSUMPTIONS = {
    "growth": ([0.1633, 0.1800, 0.1600, 0.1300, 0.1000], "GUIDANCE/JUDGMENT"),
    "gross_margin": ([0.716, 0.720, 0.730, 0.740, 0.740], "GUIDANCE/JUDGMENT"),
    "rd_ex_sbc": ([0.230, 0.225, 0.220, 0.215, 0.210], "JUDGMENT"),
    "sm_ex_sbc": ([0.130, 0.125, 0.120, 0.115, 0.110], "JUDGMENT"),
    "ga_ex_sbc": ([0.105, 0.100, 0.095, 0.090, 0.085], "JUDGMENT"),
    "sbc_ratio": ([0.150, 0.140, 0.130, 0.120, 0.110], "GUIDANCE/JUDGMENT"),
    "tax_rate": ([0.240] * 5, "GUIDANCE/JUDGMENT"),
    "ar_ratio": ([0.157] * 5, "HISTORY"),
    "deferred_cost_ratio": ([0.099] * 5, "HISTORY"),
    "prepaid_ratio": ([0.016] * 5, "HISTORY"),
    "ap_ratio": ([0.008] * 5, "HISTORY"),
    "accrued_ratio": ([0.044] * 5, "HISTORY"),
    "deferred_revenue_ratio": ([0.476] * 5, "JUDGMENT"),
    "da_ratio": ([0.0139] * 5, "HISTORY"),
    "capex_ratio": ([0.0264] * 5, "HISTORY"),
    "investment_yield": ([0.046] * 5, "HISTORY"),
}

MINIMUM_CASH = 100.0
WACC = 0.08276376244240655
TERMINAL_GROWTH = 0.03
DILUTED_SHARES = 50.7
CURRENT_PRICE = 149.42


def project(cash_override=None):
    previous = dict(OPENING)
    rows = []
    for i, year in enumerate(YEARS):
        get = lambda key: ASSUMPTIONS[key][0][i]
        revenue = previous["revenue"] * (1.0 + get("growth"))
        gross_profit = revenue * get("gross_margin")
        rd = revenue * get("rd_ex_sbc")
        sm = revenue * get("sm_ex_sbc")
        ga = revenue * get("ga_ex_sbc")
        sbc = revenue * get("sbc_ratio")
        da = revenue * get("da_ratio")
        capex = revenue * get("capex_ratio")
        ebit = gross_profit - rd - sm - ga - sbc
        interest_income = previous["investments"] * get("investment_yield")
        pretax = ebit + interest_income
        tax = max(0.0, pretax) * get("tax_rate")
        net_income = pretax - tax

        ar = revenue * get("ar_ratio")
        deferred_cost = revenue * get("deferred_cost_ratio")
        prepaid = revenue * get("prepaid_ratio")
        ppe = previous["ppe"] + capex * 0.66 - da
        intangibles = previous["intangibles"] + capex * 0.34
        ap = revenue * get("ap_ratio")
        accrued = revenue * get("accrued_ratio")
        deferred_revenue = revenue * get("deferred_revenue_ratio")

        change_operating_assets = ((ar - previous["ar"]) + (deferred_cost - previous["deferred_cost"])
                                   + (prepaid - previous["prepaid"]))
        change_operating_liabilities = ((ap - previous["ap"]) + (accrued - previous["accrued"])
                                        + (deferred_revenue - previous["deferred_revenue"]))
        change_nwc = change_operating_assets - change_operating_liabilities
        fcff = ebit * (1.0 - get("tax_rate")) + da - capex - change_nwc

        # SBC is added back for the cash bridge but remains an economic expense in FCFF.
        cfo = net_income + da + sbc - change_operating_assets + change_operating_liabilities
        cash = previous["cash"] + cfo - capex
        if cash_override and year in cash_override:
            cash = cash_override[year]

        assets = (cash + previous["investments"] + ar + deferred_cost + prepaid + ppe
                  + intangibles + previous["other_assets"])
        liabilities = ap + accrued + deferred_revenue + previous["other_liabilities"]
        equity = previous["equity"] + net_income + sbc
        balance_gap = assets - liabilities - equity
        cash_gap = cash - MINIMUM_CASH
        rows.append({"year": year, "revenue": revenue, "gross_profit": gross_profit,
                     "ebit": ebit, "net_income": net_income, "sbc": sbc, "da": da,
                     "capex": capex, "ar": ar, "deferred_cost": deferred_cost,
                     "prepaid": prepaid, "ppe": ppe, "intangibles": intangibles,
                     "ap": ap, "accrued": accrued, "deferred_revenue": deferred_revenue,
                     "fcff": fcff, "cash": cash, "equity": equity,
                     "balance_gap": balance_gap, "cash_gap": cash_gap})
        previous.update({"revenue": revenue, "cash": cash, "ar": ar,
                         "deferred_cost": deferred_cost, "prepaid": prepaid,
                         "ppe": ppe, "intangibles": intangibles, "ap": ap,
                         "accrued": accrued, "deferred_revenue": deferred_revenue,
                         "equity": equity})
    return rows


def assert_balanced(rows):
    for row in rows:
        for key, value in row.items():
            if isinstance(value, float) and not isfinite(value):
                raise ValueError("MODEL CHECK FAILED — FY%dE contains invalid %s" % (row["year"], key))
        if abs(row["balance_gap"]) > 0.05:
            raise ValueError("MODEL CHECK FAILED — FY%dE balance-sheet gap %.1f" % (row["year"], row["balance_gap"]))
        if row["cash"] < MINIMUM_CASH - 0.05:
            raise ValueError("MODEL CHECK FAILED — FY%dE cash below minimum %.1f" % (row["year"], row["cash"]))


def valuation(rows):
    assert_balanced(rows)
    if WACC <= TERMINAL_GROWTH:
        raise ValueError("MODEL CHECK FAILED — WACC must exceed terminal growth")
    pv_explicit = sum(row["fcff"] / (1.0 + WACC) ** (i + 1) for i, row in enumerate(rows))
    terminal_fcf = rows[-1]["fcff"] * (1.0 + TERMINAL_GROWTH)
    terminal_value = terminal_fcf / (WACC - TERMINAL_GROWTH)
    pv_terminal = terminal_value / (1.0 + WACC) ** len(rows)
    enterprise_value = pv_explicit + pv_terminal
    equity_value = enterprise_value + OPENING["cash"] + OPENING["investments"]
    return enterprise_value, equity_value, equity_value / DILUTED_SHARES, pv_terminal / enterprise_value


def print_table(title, rows, fields):
    print("\n" + title)
    print("Line | " + " | ".join("FY%dE" % year for year in YEARS))
    for label, key in fields:
        print(label + " | " + " | ".join("%.1f" % row[key] for row in rows))


def main():
    rows = project()
    print_table("DUOLINGO INCOME STATEMENT (USD millions)", rows,
                [("Revenue", "revenue"), ("Gross profit", "gross_profit"),
                 ("EBIT", "ebit"), ("Net income", "net_income")])
    print_table("DUOLINGO BALANCE SHEET (USD millions)", rows,
                [("Cash", "cash"), ("Accounts receivable", "ar"),
                 ("Deferred revenue", "deferred_revenue"), ("Equity", "equity")])
    print_table("DUOLINGO CASH FLOW / FCFF (USD millions)", rows,
                [("FCFF", "fcff"), ("Cash, year end", "cash")])
    print("\nMODEL CHECKS")
    for row in rows:
        print("FY%dE | Assets - liabilities - equity: %.1f | Cash >= minimum: %s" %
              (row["year"], row["balance_gap"], "PASS" if row["cash_gap"] >= -0.05 else "FAIL"))
    enterprise_value, equity_value, value_per_share, terminal_share = valuation(rows)
    print("\nVALUATION")
    print("Enterprise value: $%.1f million" % enterprise_value)
    print("Equity value: $%.1f million" % equity_value)
    print("Value per share: $%.2f" % value_per_share)
    print("Terminal value share of EV: %.1f%%" % (100.0 * terminal_share))
    print("Market price used: $%.2f" % CURRENT_PRICE)

    try:
        valuation(project({2026: 0.0}))
    except ValueError as exc:
        print("\nBROKEN-MODEL TEST: PASS")
        print(str(exc))
    else:
        raise AssertionError("Broken cash test unexpectedly passed")


if __name__ == "__main__":
    main()
