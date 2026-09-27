# Maximum Number of Operations to Move Ones to the End

Given a binary string, you may repeatedly choose a `1` immediately followed
by `0` and move that `1` right across the **entire consecutive run of zeros**
until it reaches the end of the string or sits immediately before the next
`1`. Each such move counts as one operation. Return the maximum possible
number of operations over all choices of move order.

For example, `"100001"` permits one move across its four-zero run. The string
has between 1 and `10^5` characters.
