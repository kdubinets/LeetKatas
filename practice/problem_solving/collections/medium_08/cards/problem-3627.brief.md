# Maximum Median Sum of Subsequences of Size 3

An array `nums` has length divisible by three. Repeatedly select any three remaining elements, add their median to a total, and remove them. The median is the middle value after sorting those three values. Return the greatest total possible when the array is emptied. Original positions do not restrict which elements may be selected.

`1 <= n <= 500000`, `n % 3 == 0`, and `1 <= nums[i] <= 10^9`. The total may require a wide integer.
