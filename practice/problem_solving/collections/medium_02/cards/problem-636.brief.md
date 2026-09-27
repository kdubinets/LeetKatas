# Exclusive Time of Functions

A single-threaded CPU executes calls to `n` functions, identified by integers
from `0` through `n - 1`. Calls can nest or recur. You receive chronological
logs of the form `"id:start:time"` or `"id:end:time"`. A start occurs at the
**beginning** of its timestamp; an end occurs at the **end** of its timestamp.
Only the function at the top of the call stack executes at any moment, and a
call that starts and ends at the same timestamp uses one time unit.

Return an array whose entry for each function ID is the total time it executes
across all its calls, excluding time spent in nested calls. For example,
`["0:start:0", "1:start:2", "1:end:5", "0:end:6"]` gives `[3,4]`.

`1 ≤ n ≤ 100`; there are between 2 and 500 logs with properly matched calls.
Timestamps range from `0` through `10^9`.
