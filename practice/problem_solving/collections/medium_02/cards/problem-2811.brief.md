# Check if it is Possible to Split Array

Given an array of positive integers and a threshold `m`, repeatedly split
one current array of length at least two into two nonempty **contiguous**
pieces. A split is allowed only if **both resulting pieces** are good. A piece
is good when it has length one or its sum is at least `m`.

For `nums = [1,1]` and `m = 200`, the answer is `true`: both resulting
singletons are good.

Return whether some sequence of allowed splits ends with every original
element in its own one-element array. The input contains between 1 and 100
elements, each between 1 and 100; `1 ≤ m ≤ 200`.
