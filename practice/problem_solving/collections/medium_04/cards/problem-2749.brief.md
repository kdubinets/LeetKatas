# Minimum Operations to Make the Integer Zero

Start with integers `num1` and `num2`. One operation chooses an exponent `i` from 0 through 60 and subtracts `2^i + num2` from the current `num1`; exponents may be reused. Return the minimum operations needed to reach exactly zero, or `-1` if impossible. `num1` is between 1 and 10^9; `num2` is between -10^9 and 10^9. Intermediate values may be negative.

For `num1=3`, `num2=-2`, three operations suffice; for `num1=5`, `num2=7`, the answer is `-1`.
