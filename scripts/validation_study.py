"""Check the toolkit against simulation, and draw the figures for the README.

Each check has a known right answer from statistics, so a wrong formula in the
toolkit would show up here as a number that is off.

    python scripts/validation_study.py
"""
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from abkit import analyse_experiment, sample_size_proportions  # noqa: E402
from abkit.simulate import interval_coverage, peeking_false_positive_rate, rejection_rate  # noqa: E402

BASELINE, LIFT, ALPHA, POWER = 0.12, 0.01, 0.05, 0.80
SIMS = 20000
BLUE, ORANGE, INK, MUTED, GRID = "#1D5BFF", "#C96A00", "#0E1626", "#556277", "#D9E0EC"
FIGURES = Path("reports/figures")

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans", "font.size": 11, "axes.edgecolor": GRID, "axes.labelcolor": MUTED,
        "xtick.color": MUTED, "ytick.color": MUTED, "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.8, "axes.axisbelow": True,
        "figure.dpi": 150, "savefig.bbox": "tight", "savefig.facecolor": "white",
    }
)


def title(ax, main, sub):
    ax.set_title(main, loc="left", color=INK, fontsize=14, fontweight="bold", pad=26)
    ax.text(0, 1.035, sub, transform=ax.transAxes, color=MUTED, fontsize=10.5)


def main():
    FIGURES.mkdir(parents=True, exist_ok=True)
    n = sample_size_proportions(BASELINE, LIFT, ALPHA, POWER)

    false_positive = rejection_rate(BASELINE, BASELINE, n, SIMS, ALPHA, seed=1)
    power = rejection_rate(BASELINE, BASELINE + LIFT, n, SIMS, ALPHA, seed=2)
    coverage = interval_coverage(BASELINE, BASELINE + LIFT, n, SIMS, ALPHA, seed=3)

    looks = [1, 2, 5, 10, 20]
    naive = [peeking_false_positive_rate(BASELINE, n, k, SIMS, ALPHA, seed=4) for k in looks]
    fixed = [peeking_false_positive_rate(BASELINE, n, k, SIMS, ALPHA, seed=4, corrected=True) for k in looks]

    readout = analyse_experiment(pd.read_csv("data/checkout_experiment.csv"), name="Checkout redesign")
    cuped = readout.cuped

    checks = pd.DataFrame(
        [
            ["False positive rate when there is no real effect", f"{ALPHA:.1%}", f"{false_positive:.2%}"],
            ["Power at the planned sample size and effect", f"{POWER:.1%}", f"{power:.2%}"],
            ["95% intervals that contain the true effect", "95.0%", f"{coverage:.2%}"],
        ],
        columns=["Check", "Theory", "Simulated"],
    )
    peeking = pd.DataFrame(
        {
            "Times the result is checked": looks,
            "False positive rate, stop at first win": [f"{v:.1%}" for v in naive],
            "With corrected threshold": [f"{v:.1%}" for v in fixed],
        }
    )
    lines = [
        "# Validation results",
        "",
        f"Settings: baseline {BASELINE:.0%}, true lift {LIFT:.1%} points, {n:,} users per group, "
        f"{SIMS:,} simulated experiments per check.",
        "",
        checks.to_markdown(index=False),
        "",
        "## Peeking",
        "",
        peeking.to_markdown(index=False),
        "",
        "## CUPED on the example experiment",
        "",
        f"- Variance removed: {cuped['variance_reduction']:.1%}",
        f"- Interval width: {cuped['ci_width_raw']:.3f} to {cuped['ci_width_cuped']:.3f}",
        "",
    ]
    Path("reports/validation_results.md").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))

    # Figure 1: peeking
    fig, ax = plt.subplots(figsize=(8, 4.4))
    ax.plot(looks, [v * 100 for v in naive], color=ORANGE, lw=2, marker="o", ms=7, mec="white", mew=1.5)
    ax.plot(looks, [v * 100 for v in fixed], color=BLUE, lw=2, marker="o", ms=7, mec="white", mew=1.5)
    ax.axhline(ALPHA * 100, color=MUTED, lw=1, ls=(0, (4, 3)))
    ax.text(24.3, ALPHA * 100 + 0.5, "5% target", color=MUTED, va="bottom", ha="right", fontsize=10)
    ax.text(21.0, naive[-1] * 100 - 0.4, "Stop at the\nfirst win", color=INK, va="center", fontsize=10)
    ax.text(21.0, fixed[-1] * 100 + 0.2, "Corrected\nthreshold", color=INK, va="center", fontsize=10)
    for k, v in zip(looks, naive):
        ax.annotate(f"{v:.0%}", (k, v * 100), textcoords="offset points", xytext=(-4, 9), ha="center", color=INK, fontsize=10)
    ax.set_xticks(looks)
    ax.set_xlim(0, 24.5)
    ax.set_ylim(0, max(naive) * 100 + 5)
    ax.set_xlabel("Times the result is checked during the test")
    ax.set_ylabel("False positive rate (%)")
    title(ax, "Checking early and often creates false wins", f"No real effect in any of these {SIMS:,} simulated tests per point")
    fig.savefig(FIGURES / "peeking.png")
    plt.close(fig)

    # Figure 2: sample size against effect size
    lifts = [0.005, 0.0075, 0.01, 0.0125, 0.015, 0.02, 0.025, 0.03]
    sizes = [sample_size_proportions(BASELINE, d, ALPHA, POWER) for d in lifts]
    fig, ax = plt.subplots(figsize=(8, 4.4))
    ax.plot([d * 100 for d in lifts], sizes, color=BLUE, lw=2, marker="o", ms=7, mec="white", mew=1.5)
    ax.scatter([LIFT * 100], [n], s=130, facecolor="none", edgecolor=INK, lw=1.5, zorder=3)
    ax.annotate(f"This experiment\n{n:,} per group", (LIFT * 100, n), textcoords="offset points", xytext=(16, 14), color=INK, fontsize=10)
    ax.annotate(f"{sizes[0]:,}", (lifts[0] * 100, sizes[0]), textcoords="offset points", xytext=(10, -4), color=INK, fontsize=10)
    ax.annotate(f"{sizes[-1]:,}", (lifts[-1] * 100, sizes[-1]), textcoords="offset points", xytext=(-6, 10), ha="center", color=INK, fontsize=10)
    ax.set_ylim(0, sizes[0] * 1.1)
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
    ax.set_xlabel("Smallest lift worth detecting (percentage points)")
    ax.set_ylabel("Users needed per group")
    title(ax, "Halving the effect you want to detect needs four times the users", f"Baseline conversion {BASELINE:.0%}, 5% significance, 80% power")
    fig.savefig(FIGURES / "sample_size.png")
    plt.close(fig)

    # Figure 3: results of the example experiment
    rows = [readout.primary] + readout.secondary + readout.guardrails
    fig, ax = plt.subplots(figsize=(8, 3.9))
    for i, r in enumerate(reversed(rows)):
        colour = MUTED if r.metric == "Refund rate" else BLUE
        ax.plot([r.rel_ci_low * 100, r.rel_ci_high * 100], [i, i], color=colour, lw=2, solid_capstyle="round")
        ax.plot(r.rel_lift * 100, i, "o", color=colour, ms=9, mec="white", mew=1.5)
        ax.text(r.rel_ci_high * 100 + 1.5, i, f"{r.rel_lift:+.1%}", va="center", color=INK, fontsize=10)
    ax.axvline(0, color=INK, lw=1)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r.metric for r in reversed(rows)], color=INK)
    ax.set_ylim(-0.6, len(rows) - 0.4)
    ax.grid(axis="y", visible=False)
    ax.set_xlabel("Relative change, treatment against control (%), with 95% interval")
    title(ax, "Checkout redesign: conversion up, refunds unchanged", "An interval that does not cross zero is a statistically significant change")
    fig.savefig(FIGURES / "results.png")
    plt.close(fig)


if __name__ == "__main__":
    main()
