# Closest Prime Numbers in Range

Given inclusive bounds `left` and `right` with `1 ≤ left ≤ right ≤ 10^6`, find two **prime** integers `p<q` in that range with the smallest gap `q-p`. If several pairs share the smallest gap, choose the one with the smaller `p`. Return `[p,q]`, or `[-1,-1]` if fewer than two primes lie in the range. A prime is an integer greater than 1 divisible only by 1 and itself.

For `[10,19]`, the primes are 11, 13, 17, and 19; the closest pairs tie at gap 2, so the answer is `[11,13]`.
