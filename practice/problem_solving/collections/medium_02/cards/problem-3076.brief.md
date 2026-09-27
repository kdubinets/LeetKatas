# Shortest Uncommon Substring in an Array

For each string in an array, find its shortest **contiguous substring** that
does not occur as a substring of **any other array entry**. If several
qualifying substrings share that shortest length, choose the lexicographically
smallest. If none exists, use the empty string. Return one answer per input
string, in the original order.

Repeated occurrences inside the same input string do not make a substring
common to another entry. The array has between 2 and 100 nonempty lowercase
strings, each at most 20 characters long.
