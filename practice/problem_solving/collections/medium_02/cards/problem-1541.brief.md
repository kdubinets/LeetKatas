# Minimum Insertions to Balance a Parentheses String

You may insert `(` or `)` anywhere in a string containing only those two
characters. A balanced result pairs each `(` with a **consecutive `))`**
closing token that comes after it, with pairs nested in the usual parenthesis
order. Return the minimum number of inserted characters needed.

For example, `"())"` is balanced, whereas `"(()))"` needs one inserted
`)` to become `"(())))"`. The string has between 1 and `10^5` characters.
A lone `")"` needs two insertions: one `"("` before it and one `")"`
after it.
