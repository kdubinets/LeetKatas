# Maximum Points in an Archery Competition

An archery target has sections numbered `0` through `11`. Alice has already allocated exactly `numArrows` arrows, with `aliceArrows[k]` in section `k`. Allocate exactly the same number for Bob. Bob earns `k` points from section `k` only if he shoots strictly more arrows there than Alice; otherwise he earns zero from it. Return any nonnegative integer array of 12 allocations maximizing Bob total score and summing to `numArrows`.

`1 <= numArrows <= 10^5`; `0 <= aliceArrows[k] <= numArrows`; Alice allocations sum to `numArrows`.
