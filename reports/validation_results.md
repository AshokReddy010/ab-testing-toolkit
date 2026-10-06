# Validation results

Settings: baseline 12%, true lift 1.0% points, 17,169 users per group, 20,000 simulated experiments per check.

| Check                                            | Theory   | Simulated   |
|:-------------------------------------------------|:---------|:------------|
| False positive rate when there is no real effect | 5.0%     | 4.85%       |
| Power at the planned sample size and effect      | 80.0%    | 80.33%      |
| 95% intervals that contain the true effect       | 95.0%    | 94.98%      |

## Peeking

|   Times the result is checked | False positive rate, stop at first win   | With corrected threshold   |
|------------------------------:|:-----------------------------------------|:---------------------------|
|                             1 | 4.8%                                     | 4.8%                       |
|                             2 | 8.4%                                     | 4.3%                       |
|                             5 | 14.2%                                    | 3.3%                       |
|                            10 | 19.4%                                    | 2.5%                       |
|                            20 | 25.1%                                    | 1.8%                       |

## CUPED on the example experiment

- Variance removed: 11.1%
- Interval width: 1.190 to 1.122
