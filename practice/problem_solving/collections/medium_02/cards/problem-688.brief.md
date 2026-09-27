# Knight Probability in Chessboard

A knight starts at the given `(row, column)` of an `n × n` board. On each
attempted move, it chooses uniformly among the eight offsets
`(±1, ±2)` and `(±2, ±1)`, **including** choices that leave the board.
After leaving the board, it stops; otherwise it attempts the next move.

Return the probability that the knight remains on the board after `k`
attempted moves. `1 ≤ n ≤ 25`, `0 ≤ k ≤ 100`, and the starting cell is
on the board. With `k = 0`, the answer is `1`.
