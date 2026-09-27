# Design Bitset

Implement a bitset with `size` initially zero bits. `fix(i)` sets bit `i` to 1 and `unfix(i)` sets it to 0, both idempotently. `flip()` complements every bit. `all()` reports whether all bits are 1; `one()` whether any bit is 1; `count()` returns the number of 1 bits; `toString()` returns a binary string whose character at index `i` is bit `i`. `1 ≤ size ≤ 10^5`; indices are valid. There are at most `10^5` operation calls in total and at most five `toString()` calls.
