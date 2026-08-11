# String to Integer (atoi)

Convert a string to a 32-bit signed integer using only its valid leading numeric
prefix. Ignore leading space characters, then consume at most one optional `+`
or `-`, then consume consecutive decimal digits until the first other character
or the end. If no digits are consumed, return zero. Leading zeros do not change
the value.

Clamp results below `-2^31` to `-2^31` and results above `2^31 - 1` to
`2^31 - 1`. The string has length at most 200 and contains only English letters,
digits, spaces, `+`, `-`, and `.`.
