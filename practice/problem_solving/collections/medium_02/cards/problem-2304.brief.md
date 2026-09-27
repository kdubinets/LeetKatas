# Minimum Path Cost in a Grid

An `m × n` grid contains each integer from `0` through `m*n - 1` exactly
once. A path starts in **any** cell of the first row and, from each row, may
move to **any** column of the next row. It ends in any cell of the last row.
The cost is the sum of every visited cell value plus the costs of its moves.

For a move from a cell containing value `v` to column `j` in the next row,
the additional cost is `moveCost[v][j]`. The `moveCost` table has `m*n` rows
and `n` columns. Return the minimum possible total cost.

`2 ≤ m,n ≤ 50`; move costs are between 1 and 100.
