import numpy as np
import pytest

from abkit import benjamini_hochberg, bonferroni, cuped_adjust, holm, srm_check
from abkit.simulate import interval_coverage, peeking_false_positive_rate, rejection_rate


def test_srm_passes_on_even_split():
    assert srm_check(10000, 10050).passed


def test_srm_fails_on_lopsided_split():
    result = srm_check(10000, 9400)
    assert not result.passed
    assert result.p_value < 0.001


def test_srm_respects_unequal_design():
    assert srm_check(9000, 1000, expected_control_share=0.9).passed
    assert not srm_check(9000, 1000, expected_control_share=0.5).passed


def test_cuped_keeps_the_mean_and_cuts_variance():
    rng = np.random.default_rng(3)
    before = rng.normal(50, 10, 5000)
    during = before * 0.8 + rng.normal(0, 5, 5000)
    adjusted, reduction = cuped_adjust(during, before)
    assert adjusted.mean() == pytest.approx(during.mean())
    assert reduction == pytest.approx(np.corrcoef(before, during)[0, 1] ** 2, abs=0.001)
    assert adjusted.var() < during.var()


def test_cuped_with_useless_covariate_changes_nothing():
    adjusted, reduction = cuped_adjust([1.0, 2.0, 3.0], [5.0, 5.0, 5.0])
    assert reduction == 0.0
    assert list(adjusted) == [1.0, 2.0, 3.0]


def test_corrections_known_values():
    p = [0.01, 0.04, 0.03]
    assert list(bonferroni(p)) == pytest.approx([0.03, 0.12, 0.09])
    assert list(holm(p)) == pytest.approx([0.03, 0.06, 0.06])
    assert list(benjamini_hochberg(p)) == pytest.approx([0.03, 0.04, 0.04])


def test_corrections_never_lower_a_p_value():
    p = np.array([0.001, 0.2, 0.04, 0.5])
    for method in (bonferroni, holm, benjamini_hochberg):
        adjusted = method(p)
        assert (adjusted >= p - 1e-12).all() and (adjusted <= 1).all()


def test_false_positive_rate_is_near_alpha():
    assert rejection_rate(0.12, 0.12, 5000, n_sims=20000, seed=5) == pytest.approx(0.05, abs=0.006)


def test_intervals_cover_the_truth_95_percent_of_the_time():
    assert interval_coverage(0.12, 0.13, 5000, n_sims=20000, seed=6) == pytest.approx(0.95, abs=0.006)


def test_peeking_inflates_false_positives_and_correction_fixes_it():
    naive = peeking_false_positive_rate(0.12, 10000, looks=10, n_sims=10000, seed=7)
    fixed = peeking_false_positive_rate(0.12, 10000, looks=10, n_sims=10000, seed=7, corrected=True)
    assert naive > 0.15
    assert fixed <= 0.05
