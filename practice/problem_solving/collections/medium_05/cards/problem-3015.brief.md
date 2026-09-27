# Count the Number of Houses at a Certain Distance I

Houses `1..n` are joined by streets between consecutive numbers, plus one additional street joining `x` and `y`; the extra street may be a self-loop when `x=y`. Streets can be traversed both ways. For each distance `k` from 1 to `n`, count **ordered** pairs of distinct houses `(a,b)` whose shortest street distance is `k`. Return an array of length `n` with the count for distance `k` at index `k−1`. `2 ≤ n ≤ 100`; `x,y` are any house numbers.
