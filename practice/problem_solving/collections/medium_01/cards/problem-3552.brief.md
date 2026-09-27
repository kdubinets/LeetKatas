# Grid Teleportation Traversal

You have an `m × n` grid of `.` cells, `#` obstacles, and uppercase-letter
portals. Start at the top-left cell and reach the bottom-right cell. A move to
an orthogonally adjacent non-obstacle cell costs one move. While on a portal,
you may teleport to any other cell bearing the same letter at no move cost.
Each letter can be used for teleportation at most once during a journey. A
portal at the start may be used before the first move.

For example, in the one-row grid `["A#A"]`, teleporting from the start to
the destination takes 0 moves.

Return the minimum number of moves, or `-1` if the destination is unreachable.
The start is never an obstacle; the destination may be one. Each dimension is
between 1 and 1,000.
