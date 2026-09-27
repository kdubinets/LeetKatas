# Minimum Generations to Target Point

Initially you have a list of distinct integer points in 3D. Generation zero is this list. In each later generation, take every pair of coordinate-distinct points available from earlier generations and produce their coordinate-wise floor midpoint. All points of the new generation are produced simultaneously and become available only to later generations. Points remain available once produced.

Return the first generation number by which `target` appears, or `-1` if it never appears. Return `0` when the target is initial.

There are `1` to `20` initial points; every initial and target coordinate is in `[0,6]`. Floor means rounding down; a point cannot pair with itself or an identical coordinate triple.
