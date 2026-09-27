# Zero Array Transformation III

Given nonnegative `nums` and intervals `queries=[l,r]`, each retained query may be used once. At each covered index independently, it may subtract either zero or one. Choose queries to remove so that using the remaining queries can make every array entry exactly zero. Return the greatest number removable, or -1 if even all queries cannot suffice.

`1 <= n,q <= 100000`, `0 <= nums[i] <= 100000`, and `0 <= l <= r < n`. Identical intervals are separate queries.
