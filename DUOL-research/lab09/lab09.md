# Lab 09 — ABG Pro-Forma Build

This submission contains the standalone engine requested in Lab 09: [`proforma.py`](proforma.py).
It uses only the Python standard library and projects Asbury Automotive Group (ABG) from the
FY2025 opening balance sheet through FY2030E.

## Method implemented

The script follows the instruction's order: revenue, gross profit, SG&A, depreciation,
impairment, operating income, interest, tax and net income; then the non-cash balance-sheet
lines; then FCFE; and cash last. Cash draws the revolver only when it would fall below the
$25 million minimum and repays the revolver when excess cash is available. The script checks
assets − liabilities − equity and the minimum-cash requirement after every year. `value()` calls
`assert_balanced()` before calculating the DCF, so a failed model cannot produce a valuation.

## Known-answer check

Running `python proforma.py` produces the required displayed values:

| Line | FY2026E | FY2030E |
|---|---:|---:|
| Revenue | 18,323.0 | 19,678.3 |
| Operating income | 844.2 | 971.4 |
| Net income | 413.6 | 527.5 |
| Free cash flow to equity | 211.4 | 342.3 |
| Cash, year end | 101.8 | 719.8 |
| Assets − liabilities − equity | 0.0 | 0.0 |
| Value per share | **$291.75** | |

The terminal value is 79.8% of total equity value, which is the approximately 80% result shown
in the course case.

## Deliberate break test

The script reruns the model with FY2026 cash forced to the opening $40.4 million instead of the
calculated $101.8 million. It refuses valuation and prints:

`MODEL CHECK FAILED — FY2026E balance-sheet gap -61.4`

The base model is restored for the final valuation run.

## Floor-plan explanation

Floor-plan financing is inventory borrowing provided by manufacturers' finance arms or banks.
It rises with inventory and carries interest on the opening balance. In the ABG model it is part
of operating FCFE because it finances the inventory that generates revenue. Removing the line
removes the matching source of inventory financing, so the cash balance falls sharply.

## Reflection prompts

Cash is calculated last because it is the residual result of the operating, investing and
financing decisions. Forecasting it independently would hide an error in one of those schedules
and could make an unbalanced balance sheet appear correct. A −61.4 gap means the balance sheet is
missing exactly the $61.4 million of cash generated during FY2026E; the model should stop before
any valuation is accepted.

The partner explanation, partner-file swap, and oral discussion are human course activities.
They are not represented as completed by this code.
