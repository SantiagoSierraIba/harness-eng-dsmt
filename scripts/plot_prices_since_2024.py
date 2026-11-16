"""Plot each stock's closing price as a percentage change since the start of 2024.

Run with: uv run python scripts/plot_prices_since_2024.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import PercentFormatter

from prices import TICKERS, load_prices

START = "2024-01-01"
OUT = Path(__file__).resolve().parents[1] / "figures" / "prices_since_2024.png"

# Categorical slots 1-3 of the reference dataviz palette, in fixed order.
COLORS = {"AAPL": "#2a78d6", "NVDA": "#eb6834", "ULVR.L": "#1baf7a"}


def main() -> None:
    closes = {t: load_prices(t)["Close"].loc[START:] for t in TICKERS}

    # Index every stock to the first date all of them traded, so they share a base.
    base_date = max(s.index[0] for s in closes.values())

    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=150)
    for ticker, close in closes.items():
        # Each stock keeps its own trading days; no prices are filled in.
        change = (close.loc[base_date:] / close.loc[base_date] - 1) * 100
        ax.plot(change.index, change, color=COLORS[ticker], linewidth=2, label=ticker)
        ax.annotate(
            f"{ticker} {change.iloc[-1]:+.0f}%",
            xy=(change.index[-1], change.iloc[-1]),
            xytext=(6, 0),
            textcoords="offset points",
            va="center",
            color="#0b0b0b",
            fontsize=9,
        )

    ax.axhline(0, color="#52514e", linewidth=0.8)
    ax.yaxis.set_major_formatter(PercentFormatter(decimals=0))
    ax.set_ylabel("Change in closing price")
    ax.set_title(
        f"Closing price, % change since {base_date:%-d %b %Y}",
        loc="left",
        fontsize=12,
    )
    ax.grid(axis="y", color="#e4e3df", linewidth=0.8)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.legend(loc="upper left", frameon=False)
    ax.margins(x=0.01)
    fig.text(
        0.01, 0.01,
        "Source: Yahoo Finance. ULVR.L quoted in pence, AAPL and NVDA in dollars; "
        "each line uses its own exchange's trading days.",
        fontsize=7.5, color="#52514e",
    )
    fig.tight_layout(rect=(0, 0.03, 0.93, 1))

    OUT.parent.mkdir(exist_ok=True)
    fig.savefig(OUT)
    print(f"Saved {OUT}")


if __name__ == "__main__":
    main()
