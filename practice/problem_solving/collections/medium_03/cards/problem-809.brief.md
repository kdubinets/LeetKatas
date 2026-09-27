# Expressive Words

A target string `s` and a list of query words contain lowercase letters. A query word is *stretchy* if it can become `s` by repeatedly choosing one run of equal adjacent letters and adding copies of that letter so that the run’s **new length is at least three**. Runs may also be left unchanged. Return the number of stretchy query words.

`1 ≤ |s|, |words|, |word| ≤ 100`. For target `heeellooo`, `hello` qualifies, but `helo` does not: making its single `l` into `ll` would end at length two.
