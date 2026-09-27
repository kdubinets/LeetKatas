# Lexicographically Smallest String After Applying Operations

You have an **even-length** string of decimal digits. You may apply either
operation any number of times, in any order:

- Add `a` to each digit at an **odd 0-based index**, wrapping each result
  modulo `10`.
- Rotate the entire string **right** by `b` positions.

For example, with `s = "3456"` and `a = 5`, one add operation gives
`"3951"`.

Return the lexicographically smallest string reachable, including the
original string if it is best. The length is between 2 and 100;
`1 ≤ a ≤ 9` and `1 ≤ b < s.length`.
