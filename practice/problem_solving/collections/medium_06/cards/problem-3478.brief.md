# Choose K Elements With Maximum Sum

You have positive arrays `nums1` and `nums2` of equal length `n`, and an integer `k`. For each index `i`, consider indices `j` with `nums1[j] < nums1[i]`. Choose **at most** `k` of their `nums2[j]` values to maximize their sum. Return one answer per original index. Equal `nums1` values do not qualify one another.

`1 <= n <= 100000`; `1 <= nums1[i], nums2[i] <= 1000000`; `1 <= k <= n`. Answers may exceed 32-bit range.
