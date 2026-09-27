# Minimum XOR Path in a Grid

Starting at the top-left cell of an integer grid, reach the bottom-right cell
by moving only right or down. A path's cost is the bitwise XOR of **all** cell
values on the path, including the start and destination. Return the smallest
possible path cost.

For `[[1,2],[3,4]]`, the two path costs are `1 XOR 2 XOR 4 = 7` and
`1 XOR 3 XOR 4 = 6`, so the answer is `6`.

The grid dimensions are at most 1,000 each, with at most 1,000 cells in
total. Each cell value is between `0` and `1023`.
