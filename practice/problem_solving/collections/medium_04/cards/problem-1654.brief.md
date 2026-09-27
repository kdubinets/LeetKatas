# Minimum Jumps to Reach Home

A bug starts at position 0 on the nonnegative integer line and wants to land exactly at `x`. It may jump `a` forward or `b` backward, but cannot jump backward twice consecutively. It cannot land on forbidden positions or negative positions; it **may overshoot x**. Return the fewest jumps, or `-1` if unreachable. `0 ≤ x ≤ 2,000`; `1 ≤ a,b,forbidden[i] ≤ 2,000`; there are 1–1,000 distinct forbidden positions, and `x` is not forbidden.

For `a=16`, `b=9`, `x=7`, a forward jump to 16 followed by a backward jump reaches home in 2 jumps.
