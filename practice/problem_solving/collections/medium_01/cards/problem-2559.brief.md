# Count Vowel Strings in Ranges

You have an array of nonempty lowercase words and a list of index pairs
`[left, right]`. For each pair, count the words at indices from `left` through
`right`, inclusive, whose first **and** last characters are vowels. The vowels
are `a`, `e`, `i`, `o`, and `u`. Return the counts in query order. A one-letter
vowel word qualifies.

There are at most `10^5` words and `10^5` queries. Each word has at most 40
letters; every query has `0 ≤ left ≤ right < words.length`.
