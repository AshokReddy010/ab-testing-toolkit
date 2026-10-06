import numpy as np
import pandas as pd

from abkit import analyse_experiment, render_readout


def make(n, control_rate, treatment_rate, seed=0, refund_treatment=0.005, drop_treatment=0.0):
    rng = np.random.default_rng(seed)
    group = np.repeat(["control", "treatment"], n)
    rate = np.where(group == "treatment", treatment_rate, control_rate)
    converted = rng.random(2 * n) < rate
    pre = rng.gamma(2, 30, 2 * n)
    revenue = np.where(converted, 40 + 0.3 * pre + rng.normal(0, 5, 2 * n), 0.0)
    refund_rate = np.where(group == "treatment", refund_treatment, 0.005)
    df = pd.DataFrame(
        {
            "group": group, "converted": converted.astype(int), "revenue": revenue,
            "pre_revenue": pre, "refunded": (rng.random(2 * n) < refund_rate).astype(int),
        }
    )
    keep = ~((df["group"] == "treatment") & (rng.random(2 * n) < drop_treatment))
    return df[keep]


def test_clear_win_ships():
    readout = analyse_experiment(make(20000, 0.10, 0.13))
    assert readout.decision == "Ship"
    assert readout.srm.passed


def test_no_effect_is_inconclusive():
    assert analyse_experiment(make(5000, 0.10, 0.10, seed=1)).decision == "Inconclusive"


def test_clear_loss_does_not_ship():
    assert analyse_experiment(make(20000, 0.13, 0.10, seed=2)).decision == "Do not ship"


def test_guardrail_blocks_a_win():
    readout = analyse_experiment(make(20000, 0.10, 0.13, seed=3, refund_treatment=0.02))
    assert readout.decision == "Do not ship"
    assert "refund" in readout.reason.lower()


def test_sample_ratio_mismatch_overrides_everything():
    readout = analyse_experiment(make(20000, 0.10, 0.13, seed=4, drop_treatment=0.05))
    assert readout.decision == "Do not trust"


def test_readout_renders_as_markdown():
    text = render_readout(analyse_experiment(make(20000, 0.10, 0.13), name="Test run"))
    assert text.startswith("# Test run")
    assert "Conversion rate" in text and "Variance reduction" in text
