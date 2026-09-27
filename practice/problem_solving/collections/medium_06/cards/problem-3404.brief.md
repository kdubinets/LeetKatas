# Count Special Subsequences

Count index quadruples `(p,q,r,s)` from positive integer array `nums` such that `p<q<r<s`, at least one unused index lies between every adjacent chosen pair, and `nums[p]*nums[r] = nums[q]*nums[s]`. Different index quadruples count separately even when their values match.

`7 <= |nums| <= 1000`; `1 <= nums[i] <= 1000`. The answer can exceed 32-bit range.
