# Making File Names Unique

Process requested folder names in order. If the exact requested string has never been assigned, assign it unchanged. Otherwise append `(k)`, using the smallest positive integer k for which the entire resulting string has not been assigned. Return the actual assigned name for every request.

Names already containing parentheses are ordinary exact strings: a duplicate request for `a(1)` can become `a(1)(1)`. Names remain reserved after assignment.

There are 1 to 50000 requests. Each input name has 1 to 20 lowercase letters, digits, or parentheses.
