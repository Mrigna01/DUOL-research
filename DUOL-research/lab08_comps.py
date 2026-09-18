# Lab 08 DUOL adaptation of lab07_comps.py; valuation logic preserved.
"""Simple P/E comparable-company valuation using only Python's standard library."""

from decimal import Decimal
from statistics import median


# ----------------------------- Editable inputs -----------------------------
# Use strings for exact decimal input. Use None for a missing price or EPS.
TARGET = {
    "company": "Duolingo",
    "ticker": "DUOL",
    "price": "145.16",
    "diluted_eps": "8.57",
}

# No admitted peers: COUR has negative annual GAAP EPS; UDMY merged into COUR.
# Excluded candidates remain documented in lab08.md, never in PEERS.
PEERS = []
PRICE_DATE = "September 10, 2026 (regular-session close; Nasdaq)"
EPS_PERIOD = "FY2025 total GAAP diluted EPS, year ended December 31, 2025"
# ---------------------------------------------------------------------------


def as_decimal(value):
    """Return an exact Decimal, or None for a missing value."""
    if value is None or (isinstance(value, str) and not value.strip()):
        return None
    return Decimal(str(value))


def deduplicate_peers(peers, target_ticker):
    """Keep the first occurrence of each ticker and exclude the target."""
    unique = []
    seen = {target_ticker.strip().upper()}
    for peer in peers:
        ticker = str(peer.get("ticker", "")).strip().upper()
        if not ticker or ticker in seen:
            continue
        seen.add(ticker)
        unique.append(peer)
    return unique


def peer_multiple(peer):
    price = as_decimal(peer.get("price"))
    eps = as_decimal(peer.get("diluted_eps"))
    if price is None or eps is None or price <= 0 or eps <= 0:
        return None
    return price / eps


def median_decimal(values):
    """statistics.median preserves Decimal arithmetic and full precision."""
    return median(values)


def money(value):
    return f"${value:,.2f}"


def money_change(value):
    sign = "+" if value >= 0 else "-"
    return f"{sign}${abs(value):,.2f}"


def multiple(value):
    return f"{value:.6f}x"


def main():
    target_ticker = str(TARGET.get("ticker", "")).strip().upper()
    target_price = as_decimal(TARGET.get("price"))
    target_eps = as_decimal(TARGET.get("diluted_eps"))
    peers = deduplicate_peers(PEERS, target_ticker)

    print(f"Target: {TARGET.get('company')} ({target_ticker})")
    if target_price is None or target_price <= 0:
        print("Target market price: not meaningful")
    else:
        print(f"Target market price: {money(target_price)}")
    print(f"Price date: {PRICE_DATE}")
    print(f"EPS basis: {EPS_PERIOD}")
    print("\nPeer P/E multiples")

    valid = []
    for peer in peers:
        ticker = str(peer.get("ticker", "")).strip().upper()
        pe = peer_multiple(peer)
        if pe is None:
            print(f"  {peer.get('company')} ({ticker}): not meaningful")
        else:
            valid.append((peer, pe))
            print(f"  {peer.get('company')} ({ticker}): {multiple(pe)}")

    print("\nValuation")
    if target_eps is None or target_eps <= 0:
        print("  Target EPS is missing or nonpositive; implied prices are not meaningful.")
        full_estimate = None
    elif not valid:
        print("  No usable peers; no estimate (not zero dollars).")
        full_estimate = None
    elif len(valid) == 1:
        pe = valid[0][1]
        full_estimate = pe * target_eps
        print(f"  Reference peer P/E: {multiple(pe)}")
        print(f"  Reference implied price: {money(full_estimate)} (reference estimate; no range)")
    else:
        multiples = [pe for _, pe in valid]
        minimum_pe = min(multiples)
        median_pe = median_decimal(multiples)
        maximum_pe = max(multiples)
        full_estimate = median_pe * target_eps
        print(f"  Minimum peer P/E: {multiple(minimum_pe)}")
        print(f"  Median peer P/E:  {multiple(median_pe)}")
        print(f"  Maximum peer P/E: {multiple(maximum_pe)}")
        print(f"  Minimum implied price: {money(minimum_pe * target_eps)}")
        print(f"  Median implied price:  {money(full_estimate)}")
        print(f"  Maximum implied price: {money(maximum_pe * target_eps)}")

    print("\nPeer-removal sensitivity")
    if not peers:
        print("  No admitted peers to remove; removal experiment is not applicable.")
        return

    for removed in peers:
        removed_ticker = str(removed.get("ticker", "")).strip().upper()
        remaining_multiples = [
            peer_multiple(peer)
            for peer in peers
            if str(peer.get("ticker", "")).strip().upper() != removed_ticker
            and peer_multiple(peer) is not None
        ]
        label = f"  Remove {removed_ticker}:"
        if target_eps is None or target_eps <= 0:
            print(f"{label} target EPS is not meaningful; no estimate")
        elif not remaining_multiples:
            print(f"{label} no estimate")
        else:
            removal_estimate = median_decimal(remaining_multiples) * target_eps
            if full_estimate is None:
                print(f"{label} {money(removal_estimate)}; dollar change not meaningful")
            else:
                change = removal_estimate - full_estimate
                print(f"{label} {money(removal_estimate)}; change {money_change(change)}")


if __name__ == "__main__":
    main()
