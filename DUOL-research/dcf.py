"""Simple five-year discounted cash flow (DCF) valuation."""

# Inputs (USD millions except rates and per-share value)
STARTING_FCFF = 360.424
GROWTH_RATES = [0.15, 0.18, 0.16, 0.13, 0.10]
WACC = 0.085286
TERMINAL_GROWTH = 0.03
NON_OPERATING_CASH = 1275.565
DEBT = 0.0
DILUTED_SHARES = 48.308

# Sensitivity and reverse-DCF settings
SENSITIVITY_WACCS = [0.09, 0.10, 0.11]
SENSITIVITY_TERMINAL_GROWTH_RATES = [0.02, 0.03, 0.04]
TRAINING_STARTING_FCFF = 100.0
TRAINING_GROWTH_RATES = [0.08, 0.06, 0.05, 0.04, 0.03]
TRAINING_WACC = 0.10
TRAINING_TERMINAL_GROWTH = 0.03
TRAINING_NON_OPERATING_CASH = 50.0
TRAINING_DEBT = 300.0
TRAINING_DILUTED_SHARES = 50.0
TRAINING_TARGET_SHARE_PRICE = 30.00
COMPANY_TARGET_SHARE_PRICE = 145.16
REVERSE_DCF_LOWER_SHIFT = -0.20
REVERSE_DCF_UPPER_SHIFT = 0.10


def calculate_value_per_share(
    growth_rates: list[float],
    wacc: float,
    terminal_growth: float,
    starting_fcff: float = STARTING_FCFF,
    non_operating_cash: float = NON_OPERATING_CASH,
    debt: float = DEBT,
    diluted_shares: float = DILUTED_SHARES,
) -> float:
    """Return DCF value per diluted share for the supplied rates."""
    fcff = starting_fcff
    fcff_by_year = []
    for growth_rate in growth_rates:
        fcff *= 1.0 + growth_rate
        fcff_by_year.append(fcff)

    present_value_explicit_fcff = sum(
        yearly_fcff / (1.0 + wacc) ** year
        for year, yearly_fcff in enumerate(fcff_by_year, start=1)
    )
    terminal_value_year_5 = (
        fcff_by_year[-1]
        * (1.0 + terminal_growth)
        / (wacc - terminal_growth)
    )
    present_value_terminal = terminal_value_year_5 / (1.0 + wacc) ** 5
    enterprise_value = present_value_explicit_fcff + present_value_terminal
    equity_value = enterprise_value + non_operating_cash - debt
    return equity_value / diluted_shares


def print_sensitivity_grid() -> None:
    """Print value per share across the configured WACC/growth combinations."""
    print("\nSensitivity grid: value per diluted share ($)")
    headers = ["WACC / Terminal growth"] + [
        f"{growth:.1%}" for growth in SENSITIVITY_TERMINAL_GROWTH_RATES
    ]
    rows = []
    for sensitivity_wacc in SENSITIVITY_WACCS:
        cells = [f"{sensitivity_wacc:.1%}"]
        for sensitivity_growth in SENSITIVITY_TERMINAL_GROWTH_RATES:
            if sensitivity_growth >= sensitivity_wacc:
                cells.append("invalid")
            else:
                value = calculate_value_per_share(
                    GROWTH_RATES, sensitivity_wacc, sensitivity_growth
                )
                cells.append(f"${value:.2f}")
        rows.append(cells)

    widths = [
        max(len(headers[column]), *(len(row[column]) for row in rows))
        for column in range(len(headers))
    ]
    print(" | ".join(cell.ljust(widths[index]) for index, cell in enumerate(headers)))
    print("-+-".join("-" * width for width in widths))
    for row in rows:
        print(" | ".join(cell.ljust(widths[index]) for index, cell in enumerate(row)))


def print_reverse_dcf(
    label: str,
    target_share_price: float,
    starting_fcff: float,
    growth_rates: list[float],
    wacc: float,
    terminal_growth: float,
    non_operating_cash: float,
    debt: float,
    diluted_shares: float,
) -> None:
    """Solve for a uniform shift to all explicit FCFF growth rates."""
    lower = REVERSE_DCF_LOWER_SHIFT
    upper = REVERSE_DCF_UPPER_SHIFT

    print(f"\nReverse DCF - {label}: uniform shift to all five explicit growth rates")
    print(f"Target share price: ${target_share_price:.2f}")
    print(f"Search bracket: {lower:+.2%} to {upper:+.2%}")
    print(
        "Inputs held fixed: "
        f"starting FCFF=${starting_fcff:.3f}m; "
        f"base growth rates={[f'{rate:.2%}' for rate in growth_rates]}; "
        f"WACC={wacc:.4%}; terminal growth={terminal_growth:.2%}; "
        f"non-operating cash=${non_operating_cash:.3f}m; "
        f"debt=${debt:.3f}m; diluted shares={diluted_shares:.3f}m"
    )

    if lower >= upper:
        print("No solution: reverse-DCF lower bound must be less than upper bound.")
        return
    if any(
        growth_rate + shift <= -1.0
        for growth_rate in growth_rates
        for shift in (lower, upper)
    ):
        print("Refused: bracket pushes an annual growth rate to -100% or below.")
        return

    def price_difference(shift: float) -> float:
        shifted_growth_rates = [rate + shift for rate in growth_rates]
        return (
            calculate_value_per_share(
                shifted_growth_rates,
                wacc,
                terminal_growth,
                starting_fcff,
                non_operating_cash,
                debt,
                diluted_shares,
            )
            - target_share_price
        )

    lower_difference = price_difference(lower)
    upper_difference = price_difference(upper)
    if lower_difference == 0.0:
        solved_shift = lower
    elif upper_difference == 0.0:
        solved_shift = upper
    elif lower_difference * upper_difference > 0.0:
        print(
            "No solution in bracket: target price is not reached between "
            f"{lower:+.2%} and {upper:+.2%}."
        )
        print(
            "Interpretation: bracket result for the stated fixed inputs; "
            "not proof of mispricing."
        )
        return
    else:
        for _ in range(200):
            midpoint = (lower + upper) / 2.0
            midpoint_difference = price_difference(midpoint)
            if abs(midpoint_difference) < 0.000001:
                lower = midpoint
                upper = midpoint
                break
            if lower_difference * midpoint_difference <= 0.0:
                upper = midpoint
            else:
                lower = midpoint
                lower_difference = midpoint_difference
        solved_shift = (lower + upper) / 2.0

    solved_growth_rates = [rate + solved_shift for rate in growth_rates]
    solved_price = calculate_value_per_share(
        solved_growth_rates,
        wacc,
        terminal_growth,
        starting_fcff,
        non_operating_cash,
        debt,
        diluted_shares,
    )
    print(f"Solved uniform growth shift: {solved_shift:+.6%}")
    print(f"Shifted growth rates: {[f'{rate:.6%}' for rate in solved_growth_rates]}")
    print(f"DCF value per diluted share at solution: ${solved_price:.6f}")
    print("Interpretation: implied growth shift for the stated fixed inputs; not proof of mispricing.")


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
    print_sensitivity_grid()
    print_reverse_dcf(
        "training inputs",
        TRAINING_TARGET_SHARE_PRICE,
        TRAINING_STARTING_FCFF,
        TRAINING_GROWTH_RATES,
        TRAINING_WACC,
        TRAINING_TERMINAL_GROWTH,
        TRAINING_NON_OPERATING_CASH,
        TRAINING_DEBT,
        TRAINING_DILUTED_SHARES,
    )
    print_reverse_dcf(
        "Duolingo company inputs",
        COMPANY_TARGET_SHARE_PRICE,
        STARTING_FCFF,
        GROWTH_RATES,
        WACC,
        TERMINAL_GROWTH,
        NON_OPERATING_CASH,
        DEBT,
        DILUTED_SHARES,
    )


if __name__ == "__main__":
    main()
