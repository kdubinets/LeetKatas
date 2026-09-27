# Maximum Xor Product

Given nonnegative integers `a`, `b`, and `n`, choose an integer `x` with
`0 ≤ x < 2^n` to maximize the **ordinary integer product**
`(a XOR x) × (b XOR x)`. Return that maximum product modulo `10^9 + 7`.
The modulus applies to the result after choosing the maximizing `x`; it does
not change how products are compared.

`0 ≤ a,b < 2^50` and `0 ≤ n ≤ 50`. When `n = 0`, the only possible `x` is `0`.
