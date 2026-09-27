# Maximum Trailing Zeros in a Cornered Path

Given a positive integer grid, choose a path of side-adjacent cells with at most one turn and no repeated cell. Before the turn it moves in one horizontal or vertical direction; after a turn it moves in one perpendicular direction. Either part may be absent, so straight paths and a single cell are allowed. Return the maximum number of trailing decimal zeroes in the product of values on such a path.

Both dimensions are positive, their product is at most `100000`, and `1 <= grid[i][j] <= 1000`.
