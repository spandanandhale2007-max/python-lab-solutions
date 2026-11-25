"""
Experiment 12 - shared chart styling.

Every script in this folder imports this module so the ten charts read as one
system. Import it BEFORE pyplot, because it selects the non-interactive Agg
backend (charts are written to plots/*.png instead of opening a window, so the
scripts run the same way on a lab machine with no display).

The categorical palette was checked for colour-vision deficiency separation
(worst adjacent pair deltaE 11.0 deutan, 22.5 normal vision), so the charts stay
readable for red-green colourblind viewers and in greyscale print. Every chart
also carries direct value labels, so colour is never the only encoding.
"""

import os

import matplotlib
matplotlib.use("Agg")                 # must happen before pyplot is imported

import matplotlib.pyplot as plt       # noqa: E402

# fixed categorical order - assigned in this order, never cycled
CATEGORICAL = ["#0072B2", "#D55E00", "#009E73", "#8C5FA8", "#56B4E9",
               "#8C6D1F"]

# reserved status colours, never reused as "series 5"
GOOD = "#1B7F4B"
WARNING = "#B3651A"
CRITICAL = "#B3261E"
NEUTRAL = "#8A8A82"

# single hue for magnitude (sequential), light to dark
SEQUENTIAL = ["#D6E8F5", "#A8CFE8", "#6FAFD6", "#2E8BC0", "#0072B2",
              "#004E7C"]

SURFACE = "#FCFCFB"
INK = "#2B2B28"
INK_MUTED = "#6B6B64"

PLOTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plots")


def apply_style():
    """Recessive grid and axes, text in ink tokens, thin marks."""
    plt.rcParams.update({
        "figure.facecolor": SURFACE,
        "axes.facecolor": SURFACE,
        "savefig.facecolor": SURFACE,
        "axes.edgecolor": "#D8D8D2",
        "axes.labelcolor": INK,
        "axes.titlecolor": INK,
        "axes.titlesize": 12,
        "axes.titleweight": "bold",
        "axes.labelsize": 10,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.color": "#E8E8E2",
        "grid.linewidth": 0.8,
        "axes.axisbelow": True,
        "xtick.color": INK_MUTED,
        "ytick.color": INK_MUTED,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "text.color": INK,
        "legend.frameon": False,
        "legend.fontsize": 9,
        "lines.linewidth": 2.0,
        "lines.markersize": 7,
        "font.size": 10,
        "figure.titlesize": 13,
        "figure.titleweight": "bold",
    })


def save(fig, filename):
    """Writes the figure into exp12/plots/ and returns the full path."""
    os.makedirs(PLOTS_DIR, exist_ok=True)
    path = os.path.join(PLOTS_DIR, filename)
    fig.tight_layout()
    fig.savefig(path, dpi=140, bbox_inches="tight")
    plt.close(fig)
    print(f"\n  [chart saved] {path}")
    return path


def label_bars(ax, bars, values, fmt="{:,.0f}", offset=0.01, horizontal=False):
    """Direct value labels, so the chart never relies on colour alone."""
    if horizontal:
        span = max(values) if len(values) else 1
        for bar, value in zip(bars, values):
            ax.text(bar.get_width() + span * offset,
                    bar.get_y() + bar.get_height() / 2,
                    fmt.format(value), va="center", ha="left",
                    fontsize=9, color=INK)
    else:
        span = max(values) if len(values) else 1
        for bar, value in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + span * offset,
                    fmt.format(value), ha="center", va="bottom",
                    fontsize=9, color=INK)
