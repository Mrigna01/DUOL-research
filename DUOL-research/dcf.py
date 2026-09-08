"""Simple five-year discounted cash flow (DCF) valuation."""

# Inputs (USD millions except rates and per-share value)
STARTING_FCFF = 100.0
GROWTH_RATES = [0.08, 0.06, 0.05, 0.04, 0.03]
WACC = 0.10
TERMINAL_GROWTH = 0.03
NON_OPERATING_CASH = 50.0
DEBT = 300.0
DILUTED_SHARES = 50.0


def main() -> None:
    if TERMINAL_GROWTH >= WACC:
        raise SystemExit(
            "Error: terminal growth must be less than WACC for the "
            "Gordon-growth formula."
        )

    fcff_by_year = []
    fcff = STARTING_FCFF
    for growth_rate in GROWTH_RATES:
        fcff *= 1.0 + growth_rate
        fcff_by_year.append(fcff)

    present_value_explicit_fcff = sum(
        yearly_fcff / (1.0 + WACC) ** year
        for year, yearly_fcff in enumerate(fcff_by_year, start=1)
    )
    terminal_value_year_5 = (
        fcff_by_year[-1]
        * (1.0 + TERMINAL_GROWTH)
        / (WACC - TERMINAL_GROWTH)
    )
    present_value_terminal = terminal_value_year_5 / (1.0 + WACC) ** 5
    enterprise_value = present_value_explicit_fcff + present_value_terminal
    equity_value = enterprise_value + NON_OPERATING_CASH - DEBT
    value_per_diluted_share = equity_value / DILUTED_SHARES
    terminal_value_share = present_value_terminal / enterprise_value

    for year, yearly_fcff in enumerate(fcff_by_year, start=1):
        print(f"FCFF Year {year}: {yearly_fcff:.4f}")
    print(f"Present value of five explicit FCFF: {present_value_explicit_fcff:.4f}")
    print(f"Terminal value at Year 5: {terminal_value_year_5:.4f}")
    print(f"Present value of terminal value: {present_value_terminal:.4f}")
    print(f"Enterprise value: {enterprise_value:.4f}")
    print(f"Equity value: {equity_value:.4f}")
    print(f"Value per diluted share: {value_per_diluted_share:.4f}")
    print(
        "Present value of terminal value as share of enterprise value: "
        f"{terminal_value_share:.4f}"
    )


if __name__ == "__main__":
    main()
