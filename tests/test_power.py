import pytest

from abkit import duration_days, mde_proportions, power_proportions, sample_size_means, sample_size_proportions


def test_sample_size_matches_textbook_value():
    # 10% -> 12% at 5% significance and 80% power is the standard worked example: about 3,841 per group.
    assert sample_size_proportions(0.10, 0.02) == pytest.approx(3841, abs=5)


def test_relative_and_absolute_mde_agree():
    assert sample_size_proportions(0.10, 0.20, relative=True) == sample_size_proportions(0.10, 0.02)


def test_smaller_effect_needs_more_users():
    assert sample_size_proportions(0.12, 0.005) > 3.5 * sample_size_proportions(0.12, 0.01)


def test_power_at_planned_sample_size_is_target():
    n = sample_size_proportions(0.12, 0.01)
    assert power_proportions(0.12, 0.13, n) == pytest.approx(0.80, abs=0.005)


def test_mde_is_inverse_of_sample_size():
    n = sample_size_proportions(0.12, 0.01)
    assert mde_proportions(0.12, n) == pytest.approx(0.01, abs=0.0002)


def test_sample_size_means_known_value():
    # 2 * (1.96 + 0.8416)^2 * 10^2 / 1^2 = 1,569.8
    assert sample_size_means(sd=10, mde=1) == 1570


def test_duration_rounds_up():
    assert duration_days(17169, daily_users=2500) == 14


def test_invalid_inputs_are_rejected():
    with pytest.raises(ValueError):
        sample_size_proportions(1.2, 0.01)
    with pytest.raises(ValueError):
        sample_size_proportions(0.99, 0.02)
    with pytest.raises(ValueError):
        duration_days(1000, daily_users=0)
