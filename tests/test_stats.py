import numpy as np
import pytest
from scipy import stats as sps

from abkit import bootstrap_mean_diff, mean_test, proportion_test


def test_proportion_test_known_example():
    result = proportion_test(200, 2000, 250, 2000)
    assert result.abs_diff == pytest.approx(0.025)
    assert result.p_value == pytest.approx(0.0126, abs=0.001)
    assert result.significant
    assert result.ci_low > 0


def test_identical_groups_are_not_significant():
    result = proportion_test(120, 1000, 120, 1000)
    assert result.p_value == pytest.approx(1.0)
    assert result.ci_low < 0 < result.ci_high


def test_relative_lift_matches_ratio():
    result = proportion_test(100, 1000, 110, 1000)
    assert result.rel_lift == pytest.approx(0.10)
    assert result.rel_ci_low < 0.10 < result.rel_ci_high


def test_mean_test_matches_scipy_welch():
    rng = np.random.default_rng(0)
    control, treatment = rng.normal(10, 3, 800), rng.normal(10.5, 4, 900)
    ours = mean_test(control, treatment)
    theirs = sps.ttest_ind(treatment, control, equal_var=False)
    assert ours.p_value == pytest.approx(theirs.pvalue)
    interval = theirs.confidence_interval(0.95)
    assert ours.ci_low == pytest.approx(interval.low)
    assert ours.ci_high == pytest.approx(interval.high)


def test_bootstrap_agrees_with_t_test_on_skewed_data():
    rng = np.random.default_rng(1)
    control, treatment = rng.lognormal(3, 1, 4000), rng.lognormal(3.1, 1, 4000)
    welch = mean_test(control, treatment)
    _, low, high = bootstrap_mean_diff(control, treatment, n_boot=1500, seed=2)
    assert low == pytest.approx(welch.ci_low, abs=0.4)
    assert high == pytest.approx(welch.ci_high, abs=0.4)


def test_empty_group_is_rejected():
    with pytest.raises(ValueError):
        proportion_test(0, 0, 5, 10)
    with pytest.raises(ValueError):
        mean_test([1.0], [1.0, 2.0])
