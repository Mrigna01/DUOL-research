"""Lab 10 entry point for the validated Duolingo pro-forma model.

Run from the repository root with ``python duol_proforma.py``.  The detailed
model remains in duol_valuation/src; this file gives Lab 10 a single, clear
company-specific command and refuses to report a value unless the generated
checks pass.
"""

import csv
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PROJECT = ROOT / "duol_valuation"


def main():
    print("Running the five-year Duolingo pro-forma and its enforced checks...", flush=True)
    subprocess.run([sys.executable, "run.py"], cwd=PROJECT, check=True)
    valuation = json.loads((PROJECT / "outputs" / "tables" / "valuation.json").read_text(encoding="utf-8"))
    checks = list(csv.DictReader((PROJECT / "model_checks.csv").open(encoding="utf-8", newline="")))
    failed = [row for row in checks if row.get("status", "").upper() != "PASS"]
    if failed:
        raise RuntimeError("MODEL CHECK FAILED — valuation disabled: %s" % failed[:3])
    print("History: FY2023–FY2025; interim actuals: H1 2026")
    print("Forecast: FY2026E–FY2030E")
    print("Valuation date: %s" % valuation["valuation_date"])
    print("Current share price used: $149.42")
    print("Implied value per share: $%.2f" % valuation["value_per_share"])
    print("Enterprise value: $%.1f million" % valuation["enterprise_value"])
    print("Equity value: $%.1f million" % valuation["equity_value"])
    print("WACC: %.2f%%" % (100 * valuation["wacc"]))
    print("Terminal growth: %.2f%%" % (100 * valuation["terminal_growth"]))
    print("Checks passed: %d" % len(checks))
    print("VALUATION ENABLED")


if __name__ == "__main__":
    main()
