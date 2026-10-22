"""Original diagrams for textbook (TB) concepts. Run: python3 work/make_tb_figures.py
Illustrative values only; the concepts come from Katzung 16e (cited in each caption)."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent
BLUE, RED, GREEN, INK, GREY = "#0a84ff", "#ff3b30", "#34c759", "#1d1d1f", "#8e8e93"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 13, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": GREY, "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK})


def quantal():
    x = np.linspace(0, 3, 400)               # log10 dose (illustrative)
    eff = 100 / (1 + np.exp(-(x - 1.0) * 6))  # ED50 at 10^1.0
    tox = 100 / (1 + np.exp(-(x - 2.0) * 6))  # TD50 at 10^2.0
    fig, ax = plt.subplots(figsize=(10, 5.6), dpi=160)
    ax.plot(x, eff, color=BLUE, lw=3, label="Therapeutic effect")
    ax.plot(x, tox, color=RED, lw=3, label="Toxic effect")
    lo, hi = 0.62, 1.62                      # min therapeutic (~1%) and min toxic (~1%) doses (illustrative)
    ax.axvspan(lo, hi, color=GREEN, alpha=.12)
    ax.text((lo + hi) / 2, 104, "Therapeutic window", ha="center", color="#1d7a36", fontweight="bold")
    for xv, lab, c in [(1.0, "ED₅₀", BLUE), (2.0, "TD₅₀", RED)]:
        ax.plot([xv, xv], [0, 50], color=c, ls="--", lw=1.5); ax.plot([0, xv], [50, 50], color=GREY, ls=":", lw=1)
        ax.text(xv, -9, lab, ha="center", color=c, fontweight="bold")
    ax.annotate("", xy=(2.0, 30), xytext=(1.0, 30), arrowprops=dict(arrowstyle="<->", color=INK, lw=1.5))
    ax.text(1.5, 33, "TI = TD₅₀ ÷ ED₅₀", ha="center", color=INK)
    ax.set_xlabel("Dose (log scale)"); ax.set_ylabel("% of population responding")
    ax.set_xticks([]); ax.set_ylim(-14, 112); ax.set_yticks([0, 50, 100]); ax.legend(loc="center right", frameon=False)
    fig.tight_layout(); out = ROOT / "L01" / "figures" / "TB_quantal.png"; fig.savefig(out); print("wrote", out)


def fill_empty():
    n = np.arange(0, 6)
    fill = 100 * (1 - 0.5 ** n); empty = 100 * 0.5 ** n
    t = np.linspace(0, 5, 300)
    fig, ax = plt.subplots(figsize=(10, 5.6), dpi=160)
    ax.plot(t, 100 * (1 - 0.5 ** t), color=BLUE, lw=3, label="Starting regular dosing: % of steady state")
    ax.plot(t, 100 * 0.5 ** t, color=RED, lw=3, label="After stopping: % of drug remaining")
    for i in range(1, 6):
        ax.plot(i, fill[i], "o", color=BLUE); ax.plot(i, empty[i], "o", color=RED)
        if i == 1:
            ax.text(1.08, 53, "50%", color=INK, fontsize=12)
            continue
        ax.text(i, fill[i] + 4, {2: "75%", 3: "87.5%", 4: "93.75%", 5: "~97%"}[i], ha="center", color=BLUE, fontsize=12)
        ax.text(i, empty[i] + 4, {2: "25%", 3: "12.5%", 4: "6.25%", 5: "3.125%"}[i], ha="center", color=RED, fontsize=12)
    ax.axvspan(4, 5, color=GREEN, alpha=.1); ax.text(4.5, 55, "4–5 half-lives:\n>90% there\n(~97% by 5)", ha="center", color="#1d7a36", fontsize=12)
    ax.set_xlabel("Number of half-lives"); ax.set_ylabel("Percent"); ax.set_ylim(0, 112); ax.set_xticks(range(6))
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.14), ncol=2, frameon=False, fontsize=12)
    fig.tight_layout(); out = ROOT / "L02" / "figures" / "TB_fill_empty.png"; fig.savefig(out); print("wrote", out)


if __name__ == "__main__":
    quantal(); fill_empty()
