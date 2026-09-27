# Number of Strings Which Can Be Rearranged to Contain Substring

Count the length-`n` strings over lowercase English letters whose characters
can be rearranged so that the rearranged string contains `"leet"` as a
contiguous substring. Different original strings count separately, even when
they have the same letters in a different order.

For `n = 4`, the answer is `12`: these are the distinct arrangements of the
letters in `"leet"`.

Return the count modulo `10^9 + 7`. `1 ≤ n ≤ 10^5`.
