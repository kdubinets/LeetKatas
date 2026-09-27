# Merge Adjacent Equal Elements

Repeatedly find the **leftmost** pair of equal adjacent values in the current
array and replace that pair with one value equal to their sum. Continue until
no equal adjacent pair remains, then return the resulting array. A merge may
create another equal pair, and the choice of the leftmost pair is mandatory
after every change.

For example, `[2,2,4,4]` becomes `[8,4]`: the leftmost `2,2` merges first,
then its result merges with the next `4`.

The input contains between 1 and `10^5` positive integers, each at most
`10^5`. Merged values can exceed the input value limit.
