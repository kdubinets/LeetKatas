# Minimum Sideway Jumps

A frog starts at point 0 in lane 2 of a three-lane road and wants to reach point `n` in **any** lane. `obstacles[i]` is 0 when no lane is blocked at point `i`, otherwise it names the single blocked lane (1, 2, or 3). Points 0 and `n` have no obstacles. The frog may move from point `i` to `i+1` in the same lane if the destination is open, or side-jump at its current point to either other open lane, even a nonadjacent one. Return the fewest side jumps needed. There are up to 500,000 road steps.
