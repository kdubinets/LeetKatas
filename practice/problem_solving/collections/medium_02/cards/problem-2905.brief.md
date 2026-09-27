# Find Indices With Index and Value Difference II

Given an integer array `nums` and nonnegative thresholds `indexDifference`
and `valueDifference`, return **any** index pair `[i,j]` satisfying both
`|i-j| ≥ indexDifference` and
`|nums[i]-nums[j]| ≥ valueDifference`. Return `[-1,-1]` if no pair works.
The two indices may be equal when the thresholds permit it.

`1 ≤ nums.length ≤ 10^5`; values are between `0` and `10^9`,
`indexDifference ≤ 10^5`, and `valueDifference ≤ 10^9`.
