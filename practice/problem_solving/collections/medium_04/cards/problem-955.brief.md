# Delete Columns to Make Sorted II

You receive `n` lowercase strings of equal length. You may delete any set of column indices; deleting a column removes that position from **every** string. Return the fewest columns to delete so the resulting strings, in their original row order, are lexicographically nondecreasing. Empty resulting strings are allowed. Both the number of strings and their length are at most 100.

For `['ca','bb','ac']`, deleting the first column gives `['a','b','c']`, so the answer is 1. The characters within each row need not be sorted.
