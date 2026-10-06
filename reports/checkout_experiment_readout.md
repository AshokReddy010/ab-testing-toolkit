# Checkout redesign

**Decision: Ship.** Conversion rose by +1.25% points (95% interval +0.55% to +1.95%), with no guardrail harmed.

## Health check

- Users: 17,169 control, 17,169 treatment
- Sample ratio mismatch: passed (p = 1, threshold 0.001)

## Results

| Metric                   | Control   | Treatment   | Difference   | 95% interval             | Relative lift   |   p-value |
|:-------------------------|:----------|:------------|:-------------|:-------------------------|:----------------|----------:|
| Conversion rate          | 11.85%    | 13.10%      | +1.25% pts   | +0.55% pts to +1.95% pts | +10.5%          |    0.0005 |
| Revenue per user         | 8.612     | 9.253       | +0.641       | +0.046 to +1.237         | +7.4%           |    0.0346 |
| Revenue per user (CUPED) | 8.634     | 9.231       | +0.596       | +0.035 to +1.157         | +6.9%           |    0.0374 |
| Refund rate              | 0.58%     | 0.60%       | +0.02% pts   | -0.14% pts to +0.19% pts | +4.0%           |    0.7777 |

## Variance reduction

- CUPED with pre-experiment revenue removed 11.1% of the variance in revenue per user.
- Interval width went from 1.190 to 1.122 (5.7% narrower).

## Notes

- Bootstrap check on revenue per user: interval +0.064 to +1.231, against +0.046 to +1.237 from the t-test.
- Holm-adjusted p-values for the non-primary metrics: revenue per user 0.0693, refund rate 0.7777.
