# Smallest Subarrays With Maximum Bitwise OR

For each starting index `i` in a nonnegative integer array, consider every nonempty contiguous subarray beginning at `i`. Return the length of the **shortest** such subarray whose bitwise OR is as large as any subarray beginning at `i` can achieve.

`1 ≤ n ≤ 100,000`, and each value is at most `10^9`. For `[0,0]`, the answer is `[1,1]`: OR zero is already the maximum at either start.
