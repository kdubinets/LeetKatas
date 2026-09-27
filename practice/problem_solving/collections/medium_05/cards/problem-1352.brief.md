# Product of the Last K Numbers

Design a stream supporting `add(num)`, which appends an integer, and `getProduct(k)`, which returns the product of the last `k` appended numbers. Every query has at least `k` preceding additions. Numbers lie in `[0,100]`; there are at most `4·10^4` calls. At any time, the product of any contiguous sequence of appended numbers fits in a signed 32-bit integer. Aim for constant time per addition and query.
