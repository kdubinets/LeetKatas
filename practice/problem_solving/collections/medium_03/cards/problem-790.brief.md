# Domino and Tromino Tiling

Count the tilings of a `2 × n` board using any number of dominoes (two edge-adjacent unit squares) and **L-shaped trominoes** (three unit squares forming a `2 × 2` square with one corner removed). Tiles may be rotated, must cover every square exactly once, and may not extend outside the board. Return the count modulo `1,000,000,007`.

Two tilings count as different when their tile boundaries differ. `1 ≤ n ≤ 1,000`. At `n=3`, there are five tilings.
