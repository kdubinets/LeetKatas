# Find Maximum Removals From Source String

Given a lowercase string `source`, a nonempty string `pattern` that is initially a subsequence of source, and sorted distinct original indices `targetIndices`, remove as many indexed characters as possible while pattern remains a subsequence after each removal. Only listed indices may be removed, in any order. Indices of other characters never change. Return the maximum number of removals.

`1 <= pattern.length <= source.length <= 3000`; there are between one and source.length target indices, all in range.
