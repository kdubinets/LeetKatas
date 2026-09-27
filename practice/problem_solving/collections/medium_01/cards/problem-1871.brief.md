# Jump Game VII

You start at index `0` of a binary string `s`, where `s[0]` is `0`. From an
index `i`, you may jump to an index `j` only when
`i + minJump ≤ j ≤ i + maxJump`, `j` is within the string, and `s[j]` is `0`.
Return whether you can reach the last index.

The string has between 2 and `10^5` characters, and
`1 ≤ minJump ≤ maxJump < s.length`.
