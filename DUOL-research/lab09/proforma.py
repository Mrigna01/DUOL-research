"""FIN43900 Lab 09: five-year ABG pro-forma engine.

This file intentionally uses only the Python standard library.  It builds the
three statements in the order specified in the lab, calculates cash last,
enforces the accounting and liquidity checks, and demonstrates that a broken
cash link blocks valuation.
"""

from math import isfinite


YEARS = [2026, 2027, 2028, 2029, 2030]
SHARES = 17.951349

ASSUMPTIONS = {
    "growth": 0.018,
    "gross_margin": 0.1705,
    "sga_ratio": [0.665, 0.655, 0.645, 0.645, 0.645],
    "depreciation_ratio": 82.4 / 3070.4,
    "impairment": 120.0,
    "capex": 250.0,
    "tax_rate": 0.255,
    "inventory_days": 2135.8 / (17999.0 - 3071.7) * 365.0,
    "floor_plan_ratio": 2027.0 / 2135.8,
    "other_working_capital_ratio": 0.008,
    "minimum_cash": 25.0,
    "revolver_limit": 850.0,
    "revolver_rate": 0.06,
    "debt_repayment": 150.0,
    "buyback": 150.0,
    "floor_plan_rate": 0.0467,
    "term_debt_rate": 0.0544,
    "cost_of_equity": 0.10,
    "terminal_growth": 0.025,
}

OPENING = {
    "revenue": 17999.0,
    "inventory": 2135.8,
    "ppe": 3070.4,
    "other_assets": 6371.6,
    "cash": 40.4,
    "floor_plan": 2027.0,
    "term_debt": 3572.0,
    "other_liabilities": 2127.5,
    "equity": 3891.7,
    "revolver": 0.0,
}


def project(cash_override=None):
    """Return five years of statements; cash_override may inject a broken link."""
    previous = dict(OPENING)
    rows = []
    for i, year in enumerate(YEARS):
        revenue = previous["revenue"] * (1.0 + ASSUMPTIONS["growth"])
        gross_profit = revenue * ASSUMPTIONS["gross_margin"]
        cost_of_sales = revenue - gross_profit
        sga = gross_profit * ASSUMPTIONS["sga_ratio"][i]
        depreciation = previous["ppe"] * ASSUMPTIONS["depreciation_ratio"]
        impairment = ASSUMPTIONS["impairment"]
        operating_income = gross_profit - sga - depreciation - impairment
        interest = (
            previous["floor_plan"] * ASSUMPTIONS["floor_plan_rate"]
            + previous["term_debt"] * ASSUMPTIONS["term_debt_rate"]
            + previous["revolver"] * ASSUMPTIONS["revolver_rate"]
        )
        pretax_income = operating_income - interest
        tax = max(0.0, pretax_income) * ASSUMPTIONS["tax_rate"]
        net_income = pretax_income - tax

        inventory = cost_of_sales * ASSUMPTIONS["inventory_days"] / 365.0
        floor_plan = inventory * ASSUMPTIONS["floor_plan_ratio"]
        change_revenue = revenue - previous["revenue"]
        other_working_capital = ASSUMPTIONS["other_working_capital_ratio"] * change_revenue
        ppe = previous["ppe"] + ASSUMPTIONS["capex"] - depreciation
        other_assets = previous["other_assets"] + other_working_capital - impairment
        term_debt = previous["term_debt"] - ASSUMPTIONS["debt_repayment"]
        other_liabilities = previous["other_liabilities"]
        equity = previous["equity"] + net_income - ASSUMPTIONS["buyback"]

        fcfe = (
            net_income
            + depreciation
            + impairment
            - ASSUMPTIONS["capex"]
            - (inventory - previous["inventory"])
            - other_working_capital
            + (floor_plan - previous["floor_plan"])
            - ASSUMPTIONS["debt_repayment"]
        )
        cash_before_financing = previous["cash"] + fcfe - ASSUMPTIONS["buyback"]
        draw = min(
            max(ASSUMPTIONS["minimum_cash"] - cash_before_financing, 0.0),
            max(ASSUMPTIONS["revolver_limit"] - previous["revolver"], 0.0),
        )
        revolver_repayment = min(
            previous["revolver"] + draw,
            max(cash_before_financing + draw - ASSUMPTIONS["minimum_cash"], 0.0),
        )
        cash = cash_before_financing + draw - revolver_repayment
        revolver = previous["revolver"] + draw - revolver_repayment
        if cash_override and year in cash_override:
            cash = cash_override[year]

        assets = cash + inventory + ppe + other_assets
        liabilities = floor_plan + term_debt + revolver + other_liabilities
        balance_gap = assets - liabilities - equity
        cash_gap = cash - ASSUMPTIONS["minimum_cash"]
        rows.append(
            {
                "year": year,
                "revenue": revenue,
                "gross_profit": gross_profit,
                "sga": sga,
                "depreciation": depreciation,
                "impairment": impairment,
                "operating_income": operating_income,
                "interest": interest,
                "pretax_income": pretax_income,
                "tax": tax,
                "net_income": net_income,
                "inventory": inventory,
                "floor_plan": floor_plan,
                "ppe": ppe,
                "other_assets": other_assets,
                "term_debt": term_debt,
                "other_liabilities": other_liabilities,
                "equity": equity,
                "fcfe": fcfe,
                "cash": cash,
                "revolver": revolver,
                "draw": draw,
                "revolver_repayment": revolver_repayment,
                "assets": assets,
                "liabilities": liabilities,
                "balance_gap": balance_gap,
                "cash_gap": cash_gap,
            }
        )
        previous.update(
            revenue=revenue,
            inventory=inventory,
            ppe=ppe,
            other_assets=other_assets,
            cash=cash,
            floor_plan=floor_plan,
            term_debt=term_debt,
            equity=equity,
            revolver=revolver,
        )
    return rows


def assert_balanced(rows):
    """Refuse to value a model with an accounting or liquidity failure."""
    for row in rows:
        for key in row:
            if isinstance(row[key], float) and not isfinite(row[key]):
                raise ValueError("MODEL CHECK FAILED — %s contains %s" % (row["year"], key))
        if abs(row["balance_gap"]) > 0.05:
            raise ValueError(
                "MODEL CHECK FAILED — %s balance-sheet gap %.1f"
                % ("FY%dE" % row["year"], row["balance_gap"])
            )
        if row["cash"] < ASSUMPTIONS["minimum_cash"] - 0.05:
            raise ValueError(
                "MODEL CHECK FAILED — %s cash below minimum: %.1f"
                % ("FY%dE" % row["year"], row["cash"])
            )


def value(rows):
    assert_balanced(rows)
    r = ASSUMPTIONS["cost_of_equity"]
    g = ASSUMPTIONS["terminal_growth"]
    if r <= g:
        raise ValueError("MODEL CHECK FAILED — cost of equity must exceed terminal growth")
    pv_forecast = sum(row["fcfe"] / (1.0 + r) ** (i + 1) for i, row in enumerate(rows))
    terminal_fcfe = (rows[-1]["fcfe"] + ASSUMPTIONS["debt_repayment"]) * (1.0 + g)
    terminal_value = terminal_fcfe / (r - g)
    pv_terminal = terminal_value / (1.0 + r) ** len(rows)
    equity_value = pv_forecast + pv_terminal
    return {
        "pv_forecast": pv_forecast,
        "terminal_value": terminal_value,
        "pv_terminal": pv_terminal,
        "equity_value": equity_value,
        "terminal_share": pv_terminal / equity_value,
        "value_per_share": equity_value / SHARES,
    }


def print_table(title, rows, fields):
    print("\n" + title)
    print("Line" + "".join(" | FY%dE" % y for y in YEARS))
    for label, key in fields:
        print(label + " | " + " | ".join("%.1f" % row[key] for row in rows))


def main():
    rows = project()
    print_table("INCOME STATEMENT (USD millions)", rows, [("Revenue", "revenue"), ("Gross profit", "gross_profit"), ("SG&A", "sga"), ("Depreciation", "depreciation"), ("Impairment", "impairment"), ("Operating income", "operating_income"), ("Interest", "interest"), ("Net income", "net_income")])
    print_table("BALANCE SHEET (USD millions)", rows, [("Cash", "cash"), ("Inventory", "inventory"), ("PP&E", "ppe"), ("Other assets", "other_assets"), ("Floor plan", "floor_plan"), ("Term debt", "term_debt"), ("Equity", "equity")])
    print_table("CASH FLOW / FCFE (USD millions)", rows, [("FCFE", "fcfe"), ("Cash, year end", "cash"), ("Revolver", "revolver")])
    print("\nMODEL CHECKS")
    for row in rows:
        print("FY%dE | Assets - liabilities - equity: %.1f | Cash >= minimum: %s" % (row["year"], row["balance_gap"], "PASS" if row["cash_gap"] >= -0.05 else "FAIL"))
    result = value(rows)
    print("\nVALUATION")
    print("Equity value: %.1f" % result["equity_value"])
    print("Share of value after 2030: %.1f%%" % (100.0 * result["terminal_share"]))
    print("Value per share: $%.2f" % result["value_per_share"])
    broken = project({2026: OPENING["cash"]})
    try:
        value(broken)
    except ValueError as exc:
        print("\nBROKEN-MODEL TEST: PASS")
        print(str(exc))
    else:
        raise AssertionError("Broken cash test unexpectedly passed")


if __name__ == "__main__":
    main()
