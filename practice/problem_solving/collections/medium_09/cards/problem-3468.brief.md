# Find the Number of Copy Arrays

Given an integer array `original` of length `n` and inclusive integer bounds `[u_i,v_i]` for each index, count arrays `copy` satisfying both rules: every `copy[i]` lies in its bounds, and for every `1 <= i < n`, `copy[i]-copy[i-1]` equals `original[i]-original[i-1]`.

`2 <= n <= 100000`, `1 <= original[i] <= 10^9`, and `1 <= u_i <= v_i <= 10^9`.
