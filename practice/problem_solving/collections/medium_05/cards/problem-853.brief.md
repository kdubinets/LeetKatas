# Car Fleet

Cars have distinct starting positions before a destination `target`, and positive constant speeds. A car cannot pass a car ahead; if it catches up, they travel together at the slower fleet speed. Catching up exactly at `target` counts as joining the same fleet. Return the number of fleets that arrive. `1 ≤ n ≤ 10^5`; `0 ≤ position[i] < target ≤ 10^6`; positions are unique and `1 ≤ speed[i] ≤ 10^6`.

For example, with `target = 10`, cars starting at positions `8` and `6` with speeds `1` and `2` meet at the destination, so they count as one fleet.
