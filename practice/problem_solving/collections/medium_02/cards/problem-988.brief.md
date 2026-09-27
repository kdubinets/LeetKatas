# Smallest String Starting From Leaf

Each binary-tree node holds an integer from `0` through `25`, representing
`a` through `z`. For every **leaf**, read its letters along the path from
that leaf **up to the root**. Return the lexicographically smallest of these
strings. A leaf has no children; if one string is a prefix of another, the
shorter one is smaller.

For a root `a` with two leaf children `b` and `c`, the candidates are `"ba"`
and `"ca"`, so the answer is `"ba"`. The tree has between 1 and 8,500 nodes.
