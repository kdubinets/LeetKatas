# Sentence Similarity III

Each input is a nonempty sentence made of English-letter words separated by
single spaces, with no leading or trailing spaces. The two sentences are
similar if one can be made exactly equal to the other by inserting one
contiguous sequence of whole words at a single position. The inserted sequence
may be empty, and insertion may occur at the beginning or end. Letters within
a word cannot be inserted or changed.

For example, `"My Haley"` and `"My name is Haley"` are similar, but
`"Frog cool"` and `"Frogs are cool"` are not.

Return whether the two sentences are similar. Each sentence has at most 100
characters. Letter case matters.
