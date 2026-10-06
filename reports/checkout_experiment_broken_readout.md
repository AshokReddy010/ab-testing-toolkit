# Checkout redesign (faulty assignment)

**Decision: Do not trust.** Sample ratio mismatch: expected 50% of users in control, observed 51.05% (p = 0.00012). Find the assignment or logging fault before reading any metric.

## Health check

- Users: 17,169 control, 16,463 treatment
- Sample ratio mismatch: FAILED (p = 0.000118, threshold 0.001)

## Results

| Metric                   | Control   | Treatment   | Difference   | 95% interval             | Relative lift   |   p-value |
|:-------------------------|:----------|:------------|:-------------|:-------------------------|:----------------|----------:|
| Conversion rate          | 11.72%    | 12.79%      | +1.07% pts   | +0.37% pts to +1.77% pts | +9.1%           |    0.0028 |
| Revenue per user         | 8.240     | 9.189       | +0.950       | +0.353 to +1.546         | +11.5%          |    0.0018 |
| Revenue per user (CUPED) | 8.236     | 9.193       | +0.958       | +0.387 to +1.529         | +11.6%          |    0.001  |
| Refund rate              | 0.40%     | 0.47%       | +0.07% pts   | -0.07% pts to +0.21% pts | +17.9%          |    0.3177 |

## Variance reduction

- CUPED with pre-experiment revenue removed 8.3% of the variance in revenue per user.
- Interval width went from 1.193 to 1.142 (4.3% narrower).

## Notes

- Bootstrap check on revenue per user: interval +0.328 to +1.536, against +0.353 to +1.546 from the t-test.
- Holm-adjusted p-values for the non-primary metrics: revenue per user 0.0036, refund rate 0.3177.
