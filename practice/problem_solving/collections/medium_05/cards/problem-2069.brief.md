# Walking Robot Simulation II

A robot starts at `(0,0)` in a `width × height` cell grid, facing East. A `step(num)` instruction makes exactly `num` successful one-cell moves. For each move it first tries straight ahead; if that destination is outside the grid, it turns 90° counterclockwise and retries the same move. `getPos()` returns `[x,y]`; `getDir()` returns North, East, South, or West. `2 ≤ width,height ≤ 100`, `1 ≤ num ≤ 10^5`, and there are at most `10^4` calls. The bottom-left cell is `(0,0)` and the top-right is `(width−1,height−1)`. A turn after a blocked attempt does not count as a step; at a corner the direction remains that of the arriving move until another step is requested.

On a `2 × 2` grid, the untouched robot at `(0,0)` faces East. After `step(4)` it returns to `(0,0)` facing South.
