"""Generate the synthetic experiments used in the examples.

The data is simulated, not real. That is deliberate: because the true effect is
known (conversion +1.0 point, refunds unchanged), the analysis can be checked
against the right answer.

    python scripts/make_example_data.py
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from abkit import sample_size_proportions  # noqa: E402

BASELINE = 0.12
TRUE_LIFT = 0.01
REFUND_SHARE = 0.04


def simulate(n_per_group, seed, lift=TRUE_LIFT):
    rng = np.random.default_rng(seed)
    n = n_per_group * 2
    # Each user has a hidden "how much they buy" level that drives both their
    # spending before the experiment and their behaviour during it.
    appetite = rng.normal(0, 1, n)
    group = rng.permutation(np.repeat(["control", "treatment"], n_per_group))
    base_rate = np.clip(BASELINE * np.exp(0.9 * appetite - 0.405), 0, 0.95)
    rate = np.clip(base_rate + np.where(group == "treatment", lift, 0.0), 0, 0.97)
    converted = rng.random(n) < rate
    order_value = rng.lognormal(3.9 + 0.25 * appetite, 0.5, n)
    revenue = np.where(converted, order_value, 0.0).round(2)
    pre_orders = rng.poisson(np.clip(0.9 * np.exp(0.9 * appetite - 0.405), 0, None))
    pre_revenue = (pre_orders * rng.lognormal(3.9 + 0.25 * appetite, 0.4, n)).round(2)
    refunded = converted & (rng.random(n) < REFUND_SHARE)
    return pd.DataFrame(
        {
            "user_id": np.arange(1, n + 1),
            "group": group,
            "pre_revenue": pre_revenue,
            "converted": converted.astype(int),
            "revenue": revenue,
            "refunded": refunded.astype(int),
        }
    )


def main():
    out = Path("data")
    out.mkdir(exist_ok=True)
    n = sample_size_proportions(BASELINE, TRUE_LIFT)
    simulate(n, seed=2024).to_csv(out / "checkout_experiment.csv", index=False)

    # Second experiment with a deliberate fault: 4% of treatment users are lost
    # before they are logged, as happens when a slower page drops sessions.
    broken = simulate(n, seed=7)
    rng = np.random.default_rng(11)
    lost = (broken["group"] == "treatment") & (rng.random(len(broken)) < 0.04)
    broken[~lost].to_csv(out / "checkout_experiment_broken.csv", index=False)
    print(f"{n:,} users per group written to data/")


if __name__ == "__main__":
    main()
