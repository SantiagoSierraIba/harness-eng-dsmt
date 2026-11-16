"""Plot Unilever (ULVR.L) against Apple (AAPL) in 2025, as % change in closing price.

Run with: uv run python scripts/plot_ulvr_vs_aapl_2025.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

from prices import load_prices

TICKERS = ["ULVR.L", "AAPL"]
START, END = "2025-01-01", "2025-12-31"
OUT = Path(__file__).resolve().parents[1] / "figures" / "ulvr_vs_aapl_2025.png"

# House style colours from the charts skill.
COLORS = {"AAPL": "#555555", "ULVR.L": "#1F36C7"}


def main() -> None:
    closes = {t: load_prices(t)["Close"].loc[START:END] for t in TICKERS}

    # Index both stocks to the first date both traded, so they share a base.
    base_date = max(s.index[0] for s in closes.values())
    end_date = max(s.index[-1] for s in closes.values())

    fig, ax = plt.subplots(figsize=(10, 5.5))
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
            color=COLORS[ticker],
            fontsize=9,
        )

    ax.axhline(0, color="#52514e", linewidth=0.8)
    ax.yaxis.set_major_formatter(PercentFormatter(decimals=0))
    ax.set_ylabel("Change since first day (%)")
    ax.set_title(
        f"Unilever vs Apple: closing price, % change, "
        f"{base_date:%-d %b %Y} to {end_date:%-d %b %Y}",
        loc="left",
        fontsize=12,
    )
    ax.grid(axis="y", color="#e4e3df", linewidth=0.8)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.legend(loc="upper left", frameon=False)
    ax.margins(x=0.01)
    fig.text(0.99, 0.01, "Source: Yahoo Finance", ha="right", fontsize=7.5, color="#52514e")
    fig.tight_layout(rect=(0, 0.03, 0.93, 1))

    OUT.parent.mkdir(exist_ok=True)
    fig.savefig(OUT, dpi=150)
    print(f"Saved {OUT}")


if __name__ == "__main__":
    main()
