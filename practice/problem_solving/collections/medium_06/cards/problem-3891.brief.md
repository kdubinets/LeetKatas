# Minimum Increase to Maximize Special Indices

An inner index `i` (`0 < i < n-1`) is **special** when `nums[i]` is strictly greater than both immediate neighbors. One operation increases any one array element by `1`. First maximize the number of special indices achievable; among arrays attaining that maximum, return the **fewest operations** required. You may increase any indices, including endpoints, as often as needed.

`3 <= n <= 100000`; `1 <= nums[i] <= 1000000000`. The operation count may exceed 32-bit range.
