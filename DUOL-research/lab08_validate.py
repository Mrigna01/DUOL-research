"""Independent arithmetic and evidence checks for Lab 08; standard library only."""
from contextlib import redirect_stdout
from decimal import Decimal as D
from io import StringIO
import json
from pathlib import Path
import subprocess
import sys
import lab08_comps as model

ROOT = Path(__file__).resolve().parent


def main():
    for ticker, expected in (("DUOL", "145.16"), ("COUR", "5.23")):
        payload = json.loads((ROOT / "lab08_evidence" / f"nasdaq-{ticker.lower()}-final.json").read_text())
        row = next(r for r in payload["data"]["tradesTable"]["rows"] if r["date"] == "09/10/2026")
        assert D(row["close"].replace("$", "").replace(",", "")) == D(expected)
        print(f"PASS Nasdaq {ticker} 2026-09-10 close: ${expected}")
    assert model.TARGET["ticker"] == "DUOL"
    assert D(model.TARGET["price"]) == D("145.16")
    assert D(model.TARGET["diluted_eps"]) == D("8.57")
    assert model.PEERS == []
    own_pe = D("145.16") / D("8.57")
    eps_crosscheck = D("414.065") / D("48.308")
    assert eps_crosscheck.quantize(D(".01")) == D("8.57")
    print(f"DUOL EPS cross-check: 414.065 / 48.308 = {eps_crosscheck:.9f}, reported $8.57")
    print(f"DUOL own P/E only (not peer valuation): 145.16 / 8.57 = {own_pe:.9f}x")
    print(f"COUR raw signed quotient only: 5.23 / -0.31 = {D('5.23') / D('-0.31'):.9f}; not meaningful")
    assert model.peer_multiple({"price": "5.23", "diluted_eps": "-0.31"}) is None
    assert model.peer_multiple({"price": None, "diluted_eps": "0.03"}) is None
    print("PASS negative EPS and missing price rejected; excluded candidates never admitted")
    outputs = []
    for _ in range(2):
        stream = StringIO()
        with redirect_stdout(stream):
            model.main()
        outputs.append(stream.getvalue())
    assert outputs[0] == outputs[1]
    assert "No usable peers; no estimate (not zero dollars)." in outputs[0]
    assert "removal experiment is not applicable" in outputs[0]
    print("PASS empty-set rerun: no estimate both times; no actual peer-removal experiment possible")

    # Recompute saved Week 3 DCF independently, without calling dcf.py functions.
    flows = []
    flow = D("360.424")
    for growth in map(D, (".15", ".18", ".16", ".13", ".10")):
        flow *= 1 + growth
        flows.append(flow)

    def independent_dcf(wacc, growth):
        explicit = sum(f / (1 + wacc) ** year for year, f in enumerate(flows, 1))
        terminal_pv = flows[-1] * (1 + growth) / (wacc - growth) / (1 + wacc) ** 5
        enterprise = explicit + terminal_pv
        equity_per_share = (enterprise + D("1275.565")) / D("48.308")
        return equity_per_share, terminal_pv / enterprise

    base, terminal_fraction = independent_dcf(D(".085286"), D(".03"))
    assert base.quantize(D(".01")) == D("251.99")
    expected_grid = ["209.01", "233.63", "268.11", "185.10", "202.90", "226.64", "166.53", "179.89", "197.06"]
    grid = [independent_dcf(w, g)[0] for w in map(D, (".09", ".10", ".11")) for g in map(D, (".02", ".03", ".04"))]
    assert [x.quantize(D(".01")) for x in grid] == list(map(D, expected_grid))
    current_dcf = subprocess.run([sys.executable, str(ROOT / "dcf.py")], capture_output=True, text=True, check=True).stdout
    assert f"Value per diluted share: {base:.4f}" in current_dcf
    for expected in expected_grid:
        assert f"${expected}" in current_dcf
    print(f"PASS saved DCF: ${base:.9f}; sensitivity ${min(grid):.2f}-${max(grid):.2f}")
    print(f"DCF terminal PV / enterprise value: {terminal_fraction:.9%}")
    print(f"Conditional DCF upside versus verified close: {(base / D('145.16') - 1):.6%}")
    print("PASS all checks; no peer range, median, or sensitivity price exists")


if __name__ == "__main__":
    main()
