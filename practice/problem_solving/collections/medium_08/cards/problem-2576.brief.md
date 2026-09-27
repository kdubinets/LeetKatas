# Find the Maximum Number of Marked Indices

Initially every index of positive integer array `nums` is unmarked. Repeatedly choose two different unmarked indices i,j satisfying `2*nums[i] <= nums[j]`, and mark both. Return the greatest number of indices that can be marked. Each index may participate only once; original index order does not restrict a pair.

`1 <= n <= 100000`; `1 <= nums[i] <= 10^9`.
