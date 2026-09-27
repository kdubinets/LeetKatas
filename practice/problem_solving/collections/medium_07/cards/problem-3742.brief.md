# Maximum Path Score in a Grid

Given an `m` by `n` grid with cell values `0`, `1`, or `2`, move from the top-left to the bottom-right using only right and down steps. A zero cell adds no score and costs zero; a one cell adds one score and costs one; a two cell adds two score and costs one. The starting cell has value zero. Return the largest score from a path with total cost at most `k`, or `-1` if no path fits. All visited cells contribute.

`1 <= m,n <= 200`; `0 <= k <= 1000`.
